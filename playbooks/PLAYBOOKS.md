# 📘 PLAYBOOKS.md — Indeks Standar Operasional & Token Governance 🌸

Workspace **Yerly-Playground** dilengkapi dengan playbook kanonikal berprinsip **Single Source of Truth (SSOT)** yang dimuat secara selektif (*on-demand*) demi efisiensi token.

---

## ⚡ Token Saving Mode & Ingestion Rules

> [!IMPORTANT]
> **DILARANG meng-ingest seluruh file playbook sekaligus ke dalam konteks!**  
> Muat HANYA berkas yang relevan dengan mode tugas aktif. Panduan kapan memakai atau melewati modal `ask_question` berada di [`contextual-interactivity.md`](contextual-interactivity.md).

| Mode Tugas Aktif | Playbook Wajib Dimuat |
|---|---|
| **1. Programming & Software Engineering** | `clean-code-engineering.md`, `harness-engineering.md`, `semver-release-engineering.md` (+ `anti-slop-craft-gate.md` bila menyentuh UI/copy/komentar) |
| **2. QA Automation (KMP, Revamp & Locara)** | `kmp-revamp-m-smile.md`, `qa-katalon-mobile.md`, `locara-self-healing.md`, `datacore-ssot.md` |
| **3. QA Manual & UAT Design** | `uat-test-script-design.md`, `bank-mega-m-smile.md`, `qa-reporting-and-docs.md` |
| **4. Debugging, RCA & Locator Fix** | `debugging-forensics.md`, `locara-self-healing.md`, `harness-engineering.md` |
| **5. Core Banking AS400, Backoffice & Release** | `host-as400-core-banking.md`, `qa-reporting-and-docs.md`, `git-governance.md` |
| **6. Ngobrol Santai / Rehat Sejenak** | *Tidak perlu memuat playbook teknis* |

---

## 📂 Katalog Playbook Kanonikal (15 Modul SSOT)

### A. Software Engineering, Craft & Governance
1. [`clean-code-engineering.md`](clean-code-engineering.md) — 18 Pilar Clean Code, Modularisasi (`<300L`), DRY, SRP, Type Safety, Security & Audit Redundansi 7-Kelas.
2. [`anti-slop-craft-gate.md`](anti-slop-craft-gate.md) — Native Anti-Slop Filter (40 aturan 3-tier), Liveliness Dials, Copy EN/ID, WCAG `rgba()` Contrast, 3-State Mobile & Delivery Gate.
3. [`harness-engineering.md`](harness-engineering.md) — 5-Layer Defense-in-Depth Harness, Blast Radius Scoring, Lexical AST Guard, Watchdogs & Lossless Worktree Merge.
4. [`semver-release-engineering.md`](semver-release-engineering.md) — SemVer 2.0.0, 7-Layer Breaking Change Detector, Expand-and-Contract, Changelog & Golden 6-Step GitHub Release.
5. [`contextual-interactivity.md`](contextual-interactivity.md) — Protokol `ask_question` kontekstual (ambang batas bertanya vs eksekusi langsung & konstruksi opsi).
6. [`git-governance.md`](git-governance.md) — Tata kelola commit, push, dan multi-branch.
7. [`debugging-forensics.md`](debugging-forensics.md) — Forensik stack trace, broken locators, dan AST balance.

### B. Bank Mega QA, KMP, Revamp & Locara
8. [`kmp-revamp-m-smile.md`](kmp-revamp-m-smile.md) — Arsitektur M-Smile KMP vs Revamp, Universal `testID`, Two-Pillar Verification, Rules 53–68, Live Spying State Machine (`S0`–`S7`) & KMP Datacore SSOT.
9. [`locara-self-healing.md`](locara-self-healing.md) — Locara by Qureon (`v1.16.1`), Probing Airbag, Semantic Intent Matcher, 2D Spatial Alignment, Tri-Target (`UMUM`/`REVAMP`/`KMP`), Anti-Double-Scroll & True Ghost Mode.
10. [`qa-katalon-mobile.md`](qa-katalon-mobile.md) — Template Two-Tier Katalon (Calling-Only Master & Screen Flow) dan recovery non-destruktif.
11. [`bank-mega-m-smile.md`](bank-mega-m-smile.md) — Ringkasan modul transaksi M-Smile dan kode respons perbankan.
12. [`datacore-ssot.md`](datacore-ssot.md) — Standar penamaan 5 segmen Datacore SSOT legacy Revamp.
13. [`host-as400-core-banking.md`](host-as400-core-banking.md) — Validasi mutasi dan saldo via terminal 5250 AS400.
14. [`uat-test-script-design.md`](uat-test-script-design.md) — Panduan desain UAT Excel 4-Sheet Bank Mega.
15. [`qa-reporting-and-docs.md`](qa-reporting-and-docs.md) — Standar Berita Acara UAT dan penyusunan evidence pack.

---
*Playbooks Index — Yerly-Playground 🌸*
