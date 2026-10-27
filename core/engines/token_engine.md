# ⚡ Token Engine: Context Budgeting & Selective Playbook Ingestion 🌸

Modul ini mengelola efisiensi token context window pada **Yerly-Playground** guna mencegah *context exhaustion* dan penurunan akurasi penalaran.

---

## 1. Ambang Batas Anggaran Token (Token Budget Thresholds)

| Kategori Sesi | Target Batas Token | Kebijakan Pemuatan File |
|---|---|---|
| **Sesi Santai / Kasual** | $< 20.000$ tokens | Hanya memuat `SOUL.md`, `USER.md`, dan ringkasan harian. Dilarang memuat playbook teknis. |
| **Sesi Kerja Terarah (Single Task)** | $30.000 - 60.000$ tokens | Memuat `CONSTITUTION.md` + 1-2 playbook yang dipilih via `ask_question`. |
| **Sesi Full Regression / Audit** | $< 100.000$ tokens | Memuat dokumen arsitektur dan pedoman audit secara selektif. |

---

## 2. Dynamic Playbook Routing

Ketika Mbak Yerly memulai sesi kerja baru, engine menampilkan dialog `ask_question`:
1. **Mode Mobile QA Automation** $\rightarrow$ Muat `qa-katalon-mobile.md` + `bank-mega-m-smile.md` + `datacore-ssot.md`.
2. **Mode QA Manual & UAT Design** $\rightarrow$ Muat `uat-test-script-design.md` + `qa-reporting-and-docs.md`.
3. **Mode Debugging & RCA** $\rightarrow$ Muat `debugging-forensics.md` + `qa-katalon-mobile.md`.
4. **Mode Core Banking AS400** $\rightarrow$ Muat `host-as400-core-banking.md`.
5. **Mode Ngobrol Santai** $\rightarrow$ Nol playbook teknis yang dimuat.

---
*Token Engine — Yerly-Playground 🌸*
