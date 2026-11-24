#!/usr/bin/env python3
"""
Declarative Multi-Domain Rule Registry for Yerly-Playground Native Anti-Slop Engine.

Maps deterministic static checks cleanly to the 3-tier Anti-Slop rule model
(HARD_GATE, PURPOSE_GATE, QUALITY_LOCK) across UI, Bilingual EN+ID Copywriting,
Human/A11y, Mobile Reflow, and Code Comment Hygiene.
"""

import re
from dataclasses import dataclass
from typing import Dict, Pattern, Tuple


@dataclass(frozen=True)
class SlopRule:
    rule_id: str
    core_ref: str
    domain: str
    tier: str
    title: str
    pattern: Pattern[str]
    fix_hint: str
    extensions: Tuple[str, ...]
    cluster_only: bool = False


UI_EXTS = (".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".css", ".scss")
MARKUP_EXTS = (".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte")
STYLE_EXTS = (".css", ".scss", ".jsx", ".tsx", ".html", ".vue", ".svelte")
COPY_EXTS = (".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".md", ".txt")
CODE_EXTS = (".js", ".jsx", ".ts", ".tsx", ".py", ".go", ".java", ".groovy", ".rs", ".cs")

RULES: Tuple[SlopRule, ...] = (
    SlopRule(
        rule_id="AS-COPY-01",
        core_ref="R-02",
        domain="copy",
        tier="HARD_GATE",
        title="Em dash character in UI or product copy",
        pattern=re.compile(r"\u2014"),
        fix_hint="Replace em dash with period, comma, colon, or parentheses.",
        extensions=MARKUP_EXTS,
    ),
    SlopRule(
        rule_id="AS-COPY-02",
        core_ref="R-16",
        domain="copy",
        tier="QUALITY_LOCK",
        title="AI marketing buzzword or hype filler (EN/ID)",
        pattern=re.compile(
            r"\b(?:ai[\s-]powered|next[\s-]generation|next[\s-]level|game[\s-]changer|"
            r"cutting[\s-]edge|revolutionary|seamless(?:ly)?|unlock the power|elevate your|"
            r"effortless(?:ly)?|supercharge your|delve into|vibrant tapestry|"
            r"solusi revolusioner|era digital yang serba cepat|lanskap digital yang terus berkembang|"
            r"tanpa batas dan mulus|bukan sekadar\s+\w+,?\s+melainkan)\b",
            re.IGNORECASE,
        ),
        fix_hint="Replace hype wording with concrete, verifiable product behavior.",
        extensions=COPY_EXTS,
        cluster_only=True,
    ),
    SlopRule(
        rule_id="AS-COPY-03",
        core_ref="R-15",
        domain="copy",
        tier="QUALITY_LOCK",
        title="Generic placeholder CTA label (EN/ID)",
        pattern=re.compile(
            r">\s*(?:Get Started|Learn More|Try Now|Explore Now|Discover More|"
            r"Mulai Sekarang|Pelajari Lebih Lanjut)\s*<",
            re.IGNORECASE,
        ),
        fix_hint="Name the concrete outcome (e.g. 'Create Free Account', 'Buka Demo Live').",
        extensions=MARKUP_EXTS,
    ),
    SlopRule(
        rule_id="AS-COPY-04",
        core_ref="R-17",
        domain="copy",
        tier="HARD_GATE",
        title="Unsourced vanity stat or fake filler persona",
        pattern=re.compile(
            r"\b(?:10K\+\s*Users|99\.9%\s*Uptime|500M\s*Requests|120\+\s*Countries|"
            r"Trusted by thousands of teams|Dipercaya oleh ribuan bisnis|"
            r"Sarah Chen|John Doe|johndoe@example\.com|Budi Santoso|budi@example\.com)\b",
            re.IGNORECASE,
        ),
        fix_hint="Use verified real data, honest '[REAL DATA]' placeholder, or omit the block.",
        extensions=MARKUP_EXTS,
    ),
    SlopRule(
        rule_id="AS-COPY-05",
        core_ref="R-36",
        domain="copy",
        tier="HARD_GATE",
        title="Chatbot meta-closer or theatrical signposting leaked into copy",
        pattern=re.compile(
            r"\b(?:I hope this helps!?|Let me know if you have any questions|"
            r"Let'?s dive in\b|Without further ado|Read that again\.|Let that sink in\.|"
            r"Semoga membantu!?|Mari kita selami lebih dalam)\b",
            re.IGNORECASE,
        ),
        fix_hint="Strip chat artifact and end on the last concrete fact.",
        extensions=COPY_EXTS,
    ),
    SlopRule(
        rule_id="AS-HUMAN-01",
        core_ref="R-32",
        domain="human",
        tier="HARD_GATE",
        title="Removed keyboard focus outline without focus-visible replacement",
        pattern=re.compile(r"(?:outline\s*:\s*(?:none|0)\b|\boutline-none\b)"),
        fix_hint="Keep visible :focus-visible ring (>= 3:1 contrast) whenever suppressing outline.",
        extensions=STYLE_EXTS,
    ),
    SlopRule(
        rule_id="AS-HUMAN-02",
        core_ref="R-39",
        domain="human",
        tier="HARD_GATE",
        title="Non-semantic clickable div or span acting as a button",
        pattern=re.compile(r"<(?:div|span)\b[^>]*\bon[Cc]lick\s*="),
        fix_hint="Use native <button type='button'> or <a href> instead of clickable div/span.",
        extensions=MARKUP_EXTS,
    ),
    SlopRule(
        rule_id="AS-HUMAN-03",
        core_ref="R-39",
        domain="human",
        tier="HARD_GATE",
        title="Viewport meta blocks user pinch-zoom",
        pattern=re.compile(r"(?:user-scalable\s*=\s*(?:no|0)|maximum-scale\s*=\s*1(?:\.0)?\b)", re.I),
        fix_hint="Remove user-scalable=no and maximum-scale=1 so users can zoom to 200%.",
        extensions=MARKUP_EXTS,
    ),
    SlopRule(
        rule_id="AS-HUMAN-04",
        core_ref="R-26",
        domain="human",
        tier="HARD_GATE",
        title="Dead anchor link using href='#' or javascript:void",
        pattern=re.compile(r"""href\s*=\s*["'](?:#|javascript:void\(0\))["']""", re.IGNORECASE),
        fix_hint="Point href to a real section/URL, or use a <button> for state actions.",
        extensions=MARKUP_EXTS,
    ),
    SlopRule(
        rule_id="AS-MOBILE-01",
        core_ref="R-03",
        domain="mobile",
        tier="PURPOSE_GATE",
        title="Rigid 100vh section height causes mobile browser bar overflow",
        pattern=re.compile(r"(?:\bh-screen\b|\bmin-h-screen\b|(?<!d)100vh\b)"),
        fix_hint="Prefer auto content height or dynamic viewport units (100dvh / min-h-dvh).",
        extensions=STYLE_EXTS,
    ),
    SlopRule(
        rule_id="AS-UI-01",
        core_ref="R-01",
        domain="ui",
        tier="PURPOSE_GATE",
        title="Default AI blue/purple/cyan gradient palette without documented brand purpose",
        pattern=re.compile(
            r"(?:from-(?:blue|indigo|violet|purple)-\d{3}\s+(?:via-\w+-\d{3}\s+)?to-(?:purple|pink|fuchsia|cyan)-\d{3})",
            re.IGNORECASE,
        ),
        fix_hint="Derive palette from DESIGN.md tokens and record a 1-line hierarchy reason (R-31).",
        extensions=UI_EXTS,
    ),
    SlopRule(
        rule_id="AS-UI-02",
        core_ref="R-04",
        domain="ui",
        tier="PURPOSE_GATE",
        title="Decorative AI emoji inside UI headings or buttons",
        pattern=re.compile(r"<(?:h[1-6]|button|a|span)\b[^>]*>[^<]*[\U0001F680\U0001F525\u2728\U0001F4A1\U0001F389\u2705]"),
        fix_hint="Remove decorative emoji from UI chrome; use purposeful vector icons or clean copy.",
        extensions=MARKUP_EXTS,
    ),
    SlopRule(
        rule_id="AS-UI-03",
        core_ref="R-40",
        domain="ui",
        tier="HARD_GATE",
        title="Lazy-loaded hero or high-priority image",
        pattern=re.compile(
            r"<img\b(?=[^>]*(?:hero|fetchpriority\s*=\s*[\"']high[\"']))[^>]*loading\s*=\s*[\"']lazy[\"']",
            re.IGNORECASE,
        ),
        fix_hint="Never lazy-load the hero image; keep loading eager with fetchpriority='high'.",
        extensions=MARKUP_EXTS,
    ),
    SlopRule(
        rule_id="AS-CODE-01",
        core_ref="R-31",
        domain="code",
        tier="QUALITY_LOCK",
        title="Decorative ASCII banner separator in code comments",
        pattern=re.compile(r"^\s*(?://|#|/\*)\s*(?:={5,}|-{5,}|\*{5,})"),
        fix_hint="Delete decorative comment banners; keep a concise plain comment only if needed.",
        extensions=CODE_EXTS,
    ),
    SlopRule(
        rule_id="AS-CODE-02",
        core_ref="R-31",
        domain="code",
        tier="QUALITY_LOCK",
        title="Step-by-step workflow narration or redundant end marker comment",
        pattern=re.compile(
            r"^\s*(?://|#)\s*(?:Step\s+\d+\s*:|end\s+(?:of\s+)?(?:if|for|while|function|class|block)\b)",
            re.IGNORECASE,
        ),
        fix_hint="Remove narration/end markers; let clean code structure express control flow.",
        extensions=CODE_EXTS,
    ),
    SlopRule(
        rule_id="AS-CODE-03",
        core_ref="R-31",
        domain="code",
        tier="QUALITY_LOCK",
        title="Vague placeholder TODO or decorative emoji in code comments",
        pattern=re.compile(
            r"^\s*(?://|#)\s*(?:TODO\s*:?\s*(?:improve this|optimize|refactor|fix later|add more validation)\b|"
            r"[\U0001F680\U0001F525\u2728\u2705\U0001F512])",
            re.IGNORECASE,
        ),
        fix_hint="Write concrete actionable TODOs with context and plain sentence-case comments.",
        extensions=CODE_EXTS,
    ),
)

DOMAIN_ALIASES: Dict[str, Tuple[str, ...]] = {
    "all": ("ui", "copy", "human", "mobile", "code"),
    "ui": ("ui",),
    "copy": ("copy",),
    "human": ("human",),
    "a11y": ("human",),
    "mobile": ("mobile",),
    "code": ("code",),
}

SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    "coverage",
    ".cache",
}

