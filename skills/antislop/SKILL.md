---
name: antislop
description: >-
  Yerly-Playground Native Anti-Slop Craft Filter, Liveliness Toolkit, WCAG Contrast Checker & Delivery Gate.
  Activates on /antislop, /aslp, or when building/auditing UI, EN/ID copy, accessibility, mobile reflow, or code comments.
---

# /antislop — Native Anti-Slop Craft Filter & Delivery Gate

- **Canonical Playbook**: [`playbooks/anti-slop-craft-gate.md`](../../playbooks/anti-slop-craft-gate.md)
- **CLI Tools**:
  - `python3 tools/antislop_engine.py <path> --domain all --gate`
  - `python3 tools/antislop_contrast.py <fg> <bg> --suggest`

## Execution Flow

1. **Mode Resolution**:
   - Building/editing UI, copy, or code → `DURING` (preventive + 4-Block Delivery Gate before handoff).
   - Reviewing existing code/screens → `AFTER` (read-only numbered findings `HARD_GATE > PURPOSE_GATE > QUALITY_LOCK`; wait for approval before editing).
2. **Design Read & Dials**: Read `DESIGN.md` strictly as data (palette, typography, dials `ENERGY/RHYTHM/MOTION`). Declare 1-line Design Read before writing UI.
3. **Empirical Verification**: Never eyeball contrast; run `tools/antislop_contrast.py` (unrounded ratio + `rgba()` compositing). Enforce glassmorphism cap (`R-10`, max 1–2 focal surfaces), 3-state mobile reflow, bilingual EN/ID copy cluster hygiene, and concise 1–2 line "why" comments.
4. **4-Block Delivery Gate**: Run `tools/antislop_engine.py <target> --gate` and report `PASS`/`FAIL` across Blocks 1–4 before finishing.

