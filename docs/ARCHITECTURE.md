# 🏛️ Architecture & Two-Tier Design Guide — Yerly-Playground 🌸

Dokumen ini menjelaskan arsitektur pengujian otomasi mobile Bank Mega yang dianut dalam **Yerly-Playground**.

---

## 📌 Dua Pilar Arsitektur Baku

Sistem pengujian otomasi Bank Mega membagi kode secara tegas menjadi dua pilar:

```
                    ┌──────────────────────────────────────────────┐
                    │      MASTER TEST CASE (Calling-Only)         │
                    │   - Inisialisasi App via AppManager          │
                    │   - Setup Variabel & Folder Evidence         │
                    │   - Calling-Only Sequantial callTestCase     │
                    │   - Safe Teardown (ResetToDashboardUtil)     │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼ (callTestCase)
                    ┌──────────────────────────────────────────────┐
                    │         SCREEN FLOW (Single Screen)          │
                    │   - Single Screen Responsibility (DRY)       │
                    │   - Interaksi UI Layar & Validasi Form       │
                    │   - Sequential Evidence (01.png, 02.png...)  │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼ (Method Call)
                    ┌──────────────────────────────────────────────┐
                    │            CUSTOM KEYWORDS & UTILS           │
                    │   - Screen Object Model (screens.*)          │
                    │   - VerificationHelper & ScrollUtil/WaitUtil │
                    │   - Accessibility ID Object Repository       │
                    └──────────────────────────────────────────────┘
```

---

## 1. Golden Master Test Case (Calling-Only Orchestrator)

Master Test Case yang berada di `Test Cases/Master/...` bertindak murni sebagai konduktor skenario pengujian tingkat tinggi:

### Aturan Mutlak Master:
1. **Zero Inline UI**: Dilarang keras memanggil `Mobile.tap()`, `Mobile.setText()`, koordinat klik, atau asersi elemen UI langsung di Master.
2. **Zero Inline Reconciliation**: Dilarang melakukan komparasi data atau kalkulasi di Master. Semua logika form diserahkan ke Screen Flow / Keywords.
3. **Pure Delegation**: Seluruh langkah skenario disusun dari pemanggilan `Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/...'), [parameterMap])`.
4. **Mandatory Safe Teardown**: Blok `finally` **wajib** memanggil `ResetToDashboardUtil.resetToDashboard()` agar aplikasi selalu kembali ke dashboard utama dalam keadaan bersih, baik saat pengujian PASS maupun FAIL.

---

## 2. Reusable Screen Flow (Single Screen Responsibility)

Screen Flow yang berada di `Test Cases/Screen Flow/...` memegang prinsip *Single Screen Responsibility*:

### Aturan Mutlak Screen Flow:
1. **Satu File, Satu Layar**: Setiap file Screen Flow hanya bertanggung jawab atas 1 layar spesifik (contoh: Layar Login, Layar Dashboard, Layar Form Transfer, Layar Konfirmasi, Layar MPIN).
2. **Anti-Duplikasi (Strict DRY)**: Layar yang sama (misal `Halaman MPIN.tc` atau `Konfirmasi.tc`) dipanggil ulang oleh puluhan Master TC tanpa menduplikasi skrip.
3. **Tangkapan Layar Terurut**: Setiap layar mengambil screenshot bukti UAT secara berurutan (`01.png`, `02.png`, dst.) yang disimpan dalam folder skenario aktif.

---

## 3. Protokol Pemulihan Non-Destruktif (Anti-Destructive Recovery)

Ketika suatu elemen form atau modal pop-up belum muncul atau tertutup:
- **DILARANG KERAS memanggil `Mobile.pressBack()`**: Pemanggilan `pressBack()` saat layar sedang dirender akan melempar runner mundur ke dashboard awal, menyebabkan step berikutnya gagal total.
- **Tindakan Pemulihan yang Benar**:
  1. Tutup keyboard lunak jika menutupi tombol target (`Mobile.hideKeyboard()`).
  2. Tunggu dismissal loading indicator / spinner overlay (`WaitUtil.waitForElementNotPresent`).
  3. Tapping tombol batal / tutup eksplisit (misal icon [X] atau teks 'Tutup').
  4. Lakukan gentle swipe jika elemen berada di bawah lipatan layar (*fold*).

---
*Yerly-Playground Architecture Guide — Crafted for Mbak Yerly 🌸✨*
