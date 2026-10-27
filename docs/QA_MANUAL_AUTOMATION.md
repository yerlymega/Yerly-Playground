# 📑 QA Manual & Automation Comprehensive Guide — Yerly-Playground 🌸

Panduan komprehensif metodologi pengujian mutu perangkat lunak: integrasi harmonis antara **QA Manual (UAT Design)** dan **QA Automation (Katalon Studio & Appium)**.

---

## 📌 Ringkasan Komparasi

| Dimensi | QA Manual (Enterprise UAT) | QA Automation (Katalon Two-Tier) |
|---|---|---|
| **Fokus Utama** | Acceptance Criteria, Business Logic, UX, Edge Cases | Regression Suite, Smoke Test, High-Volume Data Runs |
| **Artefak Utama** | Excel 4-Sheet UAT Test Script & Berita Acara Sign-Off | Test Case `.tc`, Groovy Scripts, Test Suite `.ts`, Evidence PNG |
| **Teknik Kunci** | EP, BVA, Decision Table, Exploratory Testing | Page Object Model, Accessibility Locators, Safe Teardown |
| **Output Bukti** | Tangkapan layar terseleksi pada dokumen Word Sign-Off | Sequential screenshots (`01.png` - `NN.png`) & execution log |

---

## 1. QA Manual: Desain UAT Test Script Excel 4-Sheet

Standar baku Bank Mega QA untuk pelaporan UAT ke Business Analyst, Product Owner, dan IT PM:

### A. Struktur 4-Sheet Excel:
1. **Sheet 1: Cover / Lembar Pengesahan**:
   - Judul Proyek, Nama Modul, Versi Dokumen, Tanggal Pelaksanaan.
   - Tabel tanda tangan persetujuan: QA Lead, IT Project Manager, Business User / Product Owner.
2. **Sheet 2: Lembar Kontrol / Version History**:
   - Log histori revisi dokumen: No, Tanggal, Versi, Deskripsi Perubahan, Penulis (Author).
3. **Sheet 3: Scenario Matrix & Traceability**:
   - Pemetaan nomor Acceptance Criteria (AC) dari BRD/FSD ke skenario pengujian.
   - Status kelengkapan cakupan (*Coverage Status*).
4. **Sheet 4: Test Script Detail**:
   - Kolom baku: `Test Case ID`, `Scenario Description`, `Pre-Condition`, `Test Steps`, `Test Data`, `Expected Result`, `Actual Result`, `Status (PASS/FAIL)`, `Executed By`, `Date`.

### B. Metodologi Desain Kasus Uji:
- **Equivalence Partitioning (EP)**: Membagi input menjadi kelas valid dan invalid.
- **Boundary Value Analysis (BVA)**: Menguji batas minimum, minimum + 1, nominal normal, maksimum - 1, maksimum, dan melampaui batas maksimum (misal: limit transfer harian Rp 10.000 s/d Rp 100.000.000).
- **Prioritas Matriks Uji**:
  - **P0 (Blocker / Critical)**: Alur utama transaksional (Login, Transfer, Bayar Tagihan, MPIN).
  - **P1 (High)**: Validasi error saldo tidak cukup, limit harian terlampaui, nomor rekening salah.
  - **P2 (Medium)**: Navigasi riwayat mutasi, pencarian daftar favorit, ubah profil.
  - **P3 (Low)**: Tipografi teks, estetika warna, formatting tanggal/waktu.

---

## 2. QA Automation: Katalon Studio & Appium Mobile

### A. Siklus Eksekusi Deterministik:
1. **State Cleanliness**: Driver selalu memulai dari kondisi aplikasi yang bersih.
2. **Single-Action Verification**: Setiap aksi tapping atau input teks diverifikasi keberhasilannya sebelum melangkah ke step berikutnya.
3. **Evidence Isolation**: Screenshot bukti disimpan di folder terisolasi per skenario:
   `Include/evidence/Master_[TC_NAME]/01.png`, `02.png`, dst.
4. **Safe Teardown Mutlak**: Blok `finally` memanggil `ResetToDashboardUtil.resetToDashboard()` agar perangkat kembali siap untuk Test Case berikutnya tanpa menyisakan pop-up modal.

---
*QA Manual & Automation Guide — Yerly-Playground 🌸*
