# 📘 PLAYBOOKS.md — Indeks Standar Operasional & Token Governance 🌸

Workspace **Yerly-Playground** dilengkapi dengan playbook kanonikal yang dirancang untuk dieksekusi secara terarah (*on-demand*).

---

## ⚡ Token Saving Mode & Ingestion Rules

> [!IMPORTANT]
> **DILARANG meng-ingest seluruh file playbook sekaligus ke dalam konteks!**  
> Muat HANYA berkas yang relevan dengan mode tugas aktif yang dipilih oleh Boss melalui dialog `ask_question`.

| Mode Tugas Aktif | Playbook Wajib Dimuat |
|---|---|
| **1. Programming & Software Engineering** | *On-demand sesuai task* (`git-governance.md` / `debugging-forensics.md` bila relevan) |
| **2. QA Automation (Katalon & M-Smile)** | `qa-katalon-mobile.md`, `bank-mega-m-smile.md`, `datacore-ssot.md` |
| **3. QA Manual & UAT Design** | `uat-test-script-design.md`, `bank-mega-m-smile.md`, `qa-reporting-and-docs.md` |
| **4. Debugging, RCA & Locator Fix** | `debugging-forensics.md`, `qa-katalon-mobile.md` |
| **5. Core Banking AS400, Backoffice & Reporting** | `host-as400-core-banking.md`, `qa-reporting-and-docs.md` |
| **6. Ngobrol Santai / Rehat Sejenak** | *Tidak perlu memuat playbook teknis* |

---

## 📂 Katalog Playbook

1. [`qa-katalon-mobile.md`](qa-katalon-mobile.md) — Arsitektur Two-Tier Katalon, Screen Flow, dan recovery.
2. [`bank-mega-m-smile.md`](bank-mega-m-smile.md) — Spesifikasi alur transaksi M-Smile dan penanganan error.
3. [`host-as400-core-banking.md`](host-as400-core-banking.md) — Validasi mutasi dan saldo via terminal 5250 AS400.
4. [`uat-test-script-design.md`](uat-test-script-design.md) — Panduan desain UAT Excel 4-Sheet Bank Mega.
5. [`datacore-ssot.md`](datacore-ssot.md) — Standar penamaan 5 segmen Datacore SSOT.
6. [`debugging-forensics.md`](debugging-forensics.md) — Forensik stack trace, broken locators, dan AST balance.
7. [`git-governance.md`](git-governance.md) — Tata kelola commit, push, dan multi-branch.
8. [`qa-reporting-and-docs.md`](qa-reporting-and-docs.md) — Standar Berita Acara UAT dan penyusunan evidence pack.

---
*Playbooks Index — Yerly-Playground 🌸*
