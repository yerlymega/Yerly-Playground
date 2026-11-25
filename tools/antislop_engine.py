#!/usr/bin/env python3
"""
Yerly-Playground Native Anti-Slop Static Scanner & Delivery Gate Engine.

Scans files or directories across 5 Anti-Slop domains (ui, copy, human, mobile, code),
applies cluster filtering to avoid false positives on isolated prose terms, checks
glassmorphism dose caps (R-10) and over-explained comment blocks (Value != Length),
and emits either a terminal summary, JSON report, or PASS/FAIL Delivery Gate report.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from tools.antislop_rules import CODE_EXTS, DOMAIN_ALIASES, RULES, SKIP_DIRS, STYLE_EXTS, SlopRule
except ImportError:
    from antislop_rules import CODE_EXTS, DOMAIN_ALIASES, RULES, SKIP_DIRS, STYLE_EXTS, SlopRule  # type: ignore

GLASS_PATTERN = re.compile(r"(?:backdrop-blur(?:-\w+)?|backdrop-filter\s*:\s*blur)")
FOCUS_SAFE_PATTERN = re.compile(r"(?:focus-visible|focus:ring|focus-visible:ring|focus-visible:outline)")
COMMENT_LINE_PATTERN = re.compile(r"^\s*(?://|#)(?!\!)\s*\S")


class AntiSlopEngine:
    """Deterministic static filter for UI, Bilingual EN+ID copy, A11y, mobile, and code comments."""

    def __init__(self, target_path: Path, domain: str = "all", cluster_threshold: int = 2):
        self.target_path = target_path.resolve()
        self.domains = DOMAIN_ALIASES.get(domain.lower(), DOMAIN_ALIASES["all"])
        self.cluster_threshold = max(1, cluster_threshold)
        self.files_scanned = 0
        self.findings: List[Dict[str, Any]] = []

    def run(self) -> Dict[str, Any]:
        if not self.target_path.exists():
            return {"error": f"Target path does not exist: {self.target_path}", "passed": False}

        files = [self.target_path] if self.target_path.is_file() else self._discover_files(self.target_path)
        for fp in files:
            self._scan_file(fp)
        return self._compile_report()

    def _discover_files(self, root: Path) -> List[Path]:
        allowed_exts = {ext for rule in RULES if rule.domain in self.domains for ext in rule.extensions}
        discovered: List[Path] = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
            for name in sorted(filenames):
                if name.endswith(".min.js") or name.endswith(".min.css"):
                    continue
                fp = Path(dirpath) / name
                if fp.suffix.lower() in allowed_exts:
                    discovered.append(fp)
        return discovered

    def _add_finding(
        self,
        filepath: Path,
        line_no: int,
        rule_id: str,
        core_ref: str,
        domain: str,
        tier: str,
        title: str,
        snippet: str,
        fix_hint: str,
    ) -> None:
        rel = str(filepath.relative_to(self.target_path)) if filepath != self.target_path and self.target_path.is_dir() else filepath.name
        self.findings.append({
            "rule_id": rule_id,
            "core_ref": core_ref,
            "domain": domain,
            "tier": tier,
            "file": rel,
            "line": line_no,
            "title": title,
            "snippet": snippet.strip()[:120],
            "fix_hint": fix_hint,
        })

    def _scan_file(self, filepath: Path) -> None:
        ext = filepath.suffix.lower()
        try:
            text = filepath.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return
        self.files_scanned += 1
        lines = text.splitlines()

        cluster_hits: Dict[str, List[Tuple[SlopRule, int, str]]] = {}
        active_rules = [r for r in RULES if r.domain in self.domains and ext in r.extensions]

        for line_no, line in enumerate(lines, 1):
            for rule in active_rules:
                if not rule.pattern.search(line):
                    continue
                # Suppress outline-none false positive when focus-visible replacement is on the same line.
                if rule.rule_id == "AS-HUMAN-01" and FOCUS_SAFE_PATTERN.search(line):
                    continue
                if rule.cluster_only:
                    cluster_hits.setdefault(rule.rule_id, []).append((rule, line_no, line))
                else:
                    self._add_finding(
                        filepath, line_no, rule.rule_id, rule.core_ref,
                        rule.domain, rule.tier, rule.title, line, rule.fix_hint,
                    )

        for hits in cluster_hits.values():
            if len(hits) >= self.cluster_threshold:
                for rule, line_no, line in hits:
                    self._add_finding(
                        filepath, line_no, rule.rule_id, rule.core_ref,
                        rule.domain, rule.tier, rule.title, line, rule.fix_hint,
                    )

        if "ui" in self.domains and ext in STYLE_EXTS:
            self._check_glass_dose_cap(filepath, lines)
        if "code" in self.domains and ext in CODE_EXTS:
            self._check_over_explained_comments(filepath, lines)

    def _check_glass_dose_cap(self, filepath: Path, lines: List[str]) -> None:
        glass_lines = [idx for idx, ln in enumerate(lines, 1) if GLASS_PATTERN.search(ln)]
        if len(glass_lines) > 2:
            self._add_finding(
                filepath,
                glass_lines[2],
                "AS-UI-GLASS",
                "R-10",
                "ui",
                "PURPOSE_GATE",
                f"Glassmorphism dose cap exceeded ({len(glass_lines)} surfaces > max 2)",
                lines[glass_lines[2] - 1],
                "Limit backdrop-blur to at most 1-2 focal surfaces; keep remaining containers solid.",
            )

    def _check_over_explained_comments(self, filepath: Path, lines: List[str]) -> None:
        run_start = 0
        run_len = 0
        for idx, line in enumerate(lines, 1):
            is_comment = bool(COMMENT_LINE_PATTERN.match(line))
            if is_comment and idx <= 6:
                continue
            if is_comment:
                if run_len == 0:
                    run_start = idx
                run_len += 1
            else:
                if run_len >= 4:
                    self._add_finding(
                        filepath,
                        run_start,
                        "AS-CODE-LEN",
                        "R-31",
                        "code",
                        "QUALITY_LOCK",
                        f"Over-explained comment block ({run_len} consecutive lines; keep 1-2 lines)",
                        lines[run_start - 1],
                        "Distill comment to the core constraint or workaround in 1-2 short lines.",
                    )
                run_len = 0
        if run_len >= 4:
            self._add_finding(
                filepath,
                run_start,
                "AS-CODE-LEN",
                "R-31",
                "code",
                "QUALITY_LOCK",
                f"Over-explained comment block ({run_len} consecutive lines; keep 1-2 lines)",
                lines[run_start - 1],
                "Distill comment to the core constraint or workaround in 1-2 short lines.",
            )

    def _compile_report(self) -> Dict[str, Any]:
        counts = {"HARD_GATE": 0, "PURPOSE_GATE": 0, "QUALITY_LOCK": 0}
        for item in self.findings:
            counts[item["tier"]] = counts.get(item["tier"], 0) + 1
        return {
            "target": str(self.target_path),
            "domains": list(self.domains),
            "files_scanned": self.files_scanned,
            "total_findings": len(self.findings),
            "tier_counts": counts,
            "hard_gate_passed": counts["HARD_GATE"] == 0,
            "strict_passed": len(self.findings) == 0,
            "findings": self.findings,
        }


def format_terminal_report(report: Dict[str, Any], gate_mode: bool = False) -> str:
    if report.get("error"):
        return f"ERROR: {report['error']}"
    tc = report["tier_counts"]
    lines = [
        f"Yerly Anti-Slop Audit | target={report['target']} | files={report['files_scanned']}",
        f"Summary: HARD_GATE={tc['HARD_GATE']} | PURPOSE_GATE={tc['PURPOSE_GATE']} | QUALITY_LOCK={tc['QUALITY_LOCK']}",
    ]
    if gate_mode:
        lines.append("")
        lines.append("Delivery Gate (Static Automated Layer):")
        lines.append(f"- Block 1 Hard Gate: {'PASS' if tc['HARD_GATE'] == 0 else 'FAIL'} ({tc['HARD_GATE']} violation(s))")
        lines.append(f"- Block 2 Purpose-Gate: {'PASS' if tc['PURPOSE_GATE'] == 0 else 'REVIEW'} ({tc['PURPOSE_GATE']} item(s) need written reason)")
        lines.append(f"- Block 4 Quality Locks: {'PASS' if tc['QUALITY_LOCK'] == 0 else 'REVIEW'} ({tc['QUALITY_LOCK']} item(s))")
    if report["findings"]:
        lines.append("")
        for idx, item in enumerate(report["findings"], 1):
            lines.append(
                f"{idx}. [{item['tier']}] {item['rule_id']} ({item['core_ref']}) "
                f"{item['file']}:{item['line']} - {item['title']}"
            )
            lines.append(f"   snippet: {item['snippet']}")
            lines.append(f"   fix: {item['fix_hint']}")
    else:
        lines.append("Result: PASS (0 static anti-slop findings).")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Yerly-Playground Native Anti-Slop Scanner & Delivery Gate")
    parser.add_argument("path", nargs="?", default=".", help="Target file or directory")
    parser.add_argument("--domain", "-d", choices=sorted(DOMAIN_ALIASES.keys()), default="all")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on Purpose-Gate and Quality Lock items too")
    parser.add_argument("--gate", action="store_true", help="Include Delivery Gate PASS/FAIL summary")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    report = AntiSlopEngine(Path(args.path), domain=args.domain).run()
    print(json.dumps(report, indent=2) if args.json else format_terminal_report(report, gate_mode=args.gate))
    passed = report.get("strict_passed", False) if args.strict else report.get("hard_gate_passed", False)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

