#!/usr/bin/env python3
"""
WCAG 2.x Contrast Checker for Yerly-Playground (Native Anti-Slop Human/A11y Engine).

Supports #RGB, #RRGGBB, #RRGGBBAA, rgb(), rgba() alpha-composited over background,
and named colors. Evaluates thresholds against the unrounded ratio and can suggest
the closest passing foreground hex.
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Optional, Tuple

NAMED_COLORS: Dict[str, Tuple[int, int, int, float]] = {
    "black": (0, 0, 0, 1.0),
    "white": (255, 255, 255, 1.0),
    "transparent": (0, 0, 0, 0.0),
}

REFERENCE_CASES: Tuple[Tuple[str, str, float, bool, bool], ...] = (
    ("#000000", "#FFFFFF", 21.00, True, True),
    ("#FFFFFF", "#000000", 21.00, True, True),
    ("#FFFFFF", "#333333", 12.63, True, True),
    ("#FFFFFF", "#666666", 5.74, True, True),
    ("#777777", "#FFFFFF", 4.48, False, True),
    ("#777777", "#070707", 4.50, False, True),
    ("#FFFFFF", "#888888", 3.54, False, True),
    ("#FFFFFF", "#999999", 2.85, False, False),
    ("#555555", "#000000", 2.82, False, False),
)


def parse_color(value: str) -> Tuple[int, int, int, float]:
    """Parse hex (#RGB, #RRGGBB, #RRGGBBAA), rgb(), rgba(), or named colors into RGBA."""
    raw = value.strip()
    low = raw.lower()
    if low in NAMED_COLORS:
        return NAMED_COLORS[low]

    rgb_match = re.fullmatch(
        r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*([0-9]*\.?[0-9]+%?))?\s*\)",
        low,
    )
    if rgb_match:
        r, g, b = (int(rgb_match.group(i)) for i in (1, 2, 3))
        if any(c > 255 for c in (r, g, b)):
            raise ValueError(f"RGB channels must be 0..255, got {value!r}")
        alpha_raw = rgb_match.group(4)
        if alpha_raw is None:
            alpha = 1.0
        elif alpha_raw.endswith("%"):
            alpha = float(alpha_raw[:-1]) / 100.0
        else:
            alpha = float(alpha_raw)
        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"Alpha must be 0..1, got {value!r}")
        return (r, g, b, alpha)

    h = raw.lstrip("#")
    if len(h) == 3 and re.fullmatch(r"[0-9A-Fa-f]{3}", h):
        h = "".join(ch * 2 for ch in h)
    if len(h) == 6 and re.fullmatch(r"[0-9A-Fa-f]{6}", h):
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    if len(h) == 8 and re.fullmatch(r"[0-9A-Fa-f]{8}", h):
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16) / 255.0)
    raise ValueError(f"Unsupported color format {value!r}; use #RRGGBB, #RGB, rgb(), or rgba()")


def composite_over(
    fg: Tuple[int, int, int, float], bg: Tuple[int, int, int, float]
) -> Tuple[int, int, int]:
    """Alpha-composite foreground RGBA over an opaque background RGB."""
    a = fg[3]
    if a >= 1.0:
        return (fg[0], fg[1], fg[2])
    return (
        round(fg[0] * a + bg[0] * (1.0 - a)),
        round(fg[1] * a + bg[1] * (1.0 - a)),
        round(fg[2] * a + bg[2] * (1.0 - a)),
    )


def _linearize(channel: int) -> float:
    c = channel / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    r, g, b = (_linearize(ch) for ch in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg_color: str, bg_color: str) -> float:
    """Compute unrounded WCAG 2.x contrast ratio, compositing semi-transparent foregrounds."""
    fg_rgba = parse_color(fg_color)
    bg_rgba = parse_color(bg_color)
    if bg_rgba[3] < 1.0:
        raise ValueError("Background color must be opaque (alpha = 1.0) for deterministic WCAG ratio")
    bg_rgb = (bg_rgba[0], bg_rgba[1], bg_rgba[2])
    fg_rgb = composite_over(fg_rgba, bg_rgb)
    l1, l2 = relative_luminance(fg_rgb), relative_luminance(bg_rgb)
    lighter, darker = (l1, l2) if l1 >= l2 else (l2, l1)
    return (lighter + 0.05) / (darker + 0.05)


def suggest_passing_hex(fg_color: str, bg_color: str, target_ratio: float = 4.5) -> Optional[str]:
    """Find the closest foreground hex along white/black blend that satisfies target_ratio."""
    fg_rgba = parse_color(fg_color)
    bg_rgba = parse_color(bg_color)
    bg_rgb = (bg_rgba[0], bg_rgba[1], bg_rgba[2])
    base = composite_over(fg_rgba, bg_rgb)
    bg_lum = relative_luminance(bg_rgb)
    pole = (255, 255, 255) if bg_lum < 0.5 else (0, 0, 0)
    for step in range(1, 201):
        t = step / 200.0
        cand = tuple(round(base[i] + (pole[i] - base[i]) * t) for i in range(3))
        hex_cand = f"#{cand[0]:02x}{cand[1]:02x}{cand[2]:02x}"
        if contrast_ratio(hex_cand, bg_color) >= target_ratio:
            return hex_cand
    return None


def check_contrast(fg_color: str, bg_color: str, suggest: bool = False) -> Dict[str, object]:
    """Return structured WCAG 2.x contrast evaluation using unrounded thresholds."""
    raw = contrast_ratio(fg_color, bg_color)
    normal_pass = raw >= 4.5
    large_pass = raw >= 3.0
    aaa_pass = raw >= 7.0
    result: Dict[str, object] = {
        "foreground": fg_color,
        "background": bg_color,
        "ratio": round(raw, 2),
        "raw_ratio": round(raw, 4),
        "normal_text_aa": {"threshold": 4.5, "pass": normal_pass},
        "large_and_ui_aa": {"threshold": 3.0, "pass": large_pass},
        "normal_text_aaa": {"threshold": 7.0, "pass": aaa_pass},
        "pass": normal_pass and large_pass,
    }
    if suggest and not normal_pass:
        result["suggested_foreground_aa"] = suggest_passing_hex(fg_color, bg_color, 4.5)
    return result


def run_selftest() -> Tuple[bool, List[str]]:
    errors: List[str] = []
    for fg, bg, expected_disp, expected_norm, expected_large in REFERENCE_CASES:
        res = check_contrast(fg, bg)
        if f"{res['ratio']:.2f}" != f"{expected_disp:.2f}":
            errors.append(f"{fg} on {bg}: display {res['ratio']:.2f} != {expected_disp:.2f}")
        if res["normal_text_aa"]["pass"] != expected_norm:
            errors.append(f"{fg} on {bg}: normal AA {res['normal_text_aa']['pass']} != {expected_norm}")
        if res["large_and_ui_aa"]["pass"] != expected_large:
            errors.append(f"{fg} on {bg}: large AA {res['large_and_ui_aa']['pass']} != {expected_large}")
    return (len(errors) == 0, errors)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Yerly-Playground WCAG 2.x Contrast Checker (Anti-Slop R-25)")
    parser.add_argument("foreground", nargs="?", help="Foreground color (#hex, rgb(), rgba(), or name)")
    parser.add_argument("background", nargs="?", help="Opaque background color (#hex, rgb(), or name)")
    parser.add_argument("--suggest", action="store_true", help="Suggest closest passing AA foreground hex")
    parser.add_argument("--json", action="store_true", help="Print structured JSON output")
    parser.add_argument("--selftest", action="store_true", help="Verify reference WCAG boundary cases")
    args = parser.parse_args(argv)

    if args.selftest:
        ok, errs = run_selftest()
        if ok:
            print(f"selftest: {len(REFERENCE_CASES)} WCAG reference pairs OK")
            return 0
        for err in errs:
            print(f"FAIL: {err}")
        return 1

    if not args.foreground or not args.background:
        parser.print_usage()
        return 2

    try:
        res = check_contrast(args.foreground, args.background, suggest=args.suggest)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"ratio: {res['ratio']:.2f}:1 (raw {res['raw_ratio']:.4f}:1)")
        print(f"normal text (4.5:1): {'PASS' if res['normal_text_aa']['pass'] else 'FAIL'}")
        print(f"large / UI  (3.0:1): {'PASS' if res['large_and_ui_aa']['pass'] else 'FAIL'}")
        print(f"enhanced   (7.0:1): {'PASS' if res['normal_text_aaa']['pass'] else 'FAIL'}")
        if res.get("suggested_foreground_aa"):
            print(f"suggested AA foreground: {res['suggested_foreground_aa']}")
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

