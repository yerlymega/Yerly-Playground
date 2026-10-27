# 🏦 Bank Mega QA Standards & Core Systems — Yerly-Playground 🌸

Pedoman sistem perbankan Bank Mega, penamaan Datacore SSOT, Core Banking AS400, dan tata kelola keamanan data nasabah.

---

## 1. Standar Penamaan Datacore SSOT

Seluruh penamaan Master Test Case wajib merujuk secara ketat pada Spreadsheet SSOT Datacore Bank Mega:

$$\text{TC-}\{\text{P/N}\}\{\text{No}\}\_\{\text{MAINMOD}\}\_\{\text{SUBMOD}\}\_\{\text{SUBSUBMOD}\}\_\{\text{ScenarioName}\}$$

### Penjelasan Segmen:
- **`TC-`**: Prefix wajib entitas Test Case.
- **`{P/N}`**: Tipe skenario (**P** untuk Positif / Happy Path, **N** untuk Negatif / Edge Case).
- **`{No}`**: Nomor urut sekuensial (contoh: `01`, `53`, `89`).
- **`{MAINMOD}`**: Modul utama perbankan (contoh: `TRANSFER`, `TOPUP`, `ZAKU`, `VALAS`, `QRIS`, `APPLY`).
- **`{SUBMOD}`**: Sub-modul fitur (contoh: `BIFAST`, `ONLINE`, `PULSA`, `ZAKUARISAN`).
- **`{SUBSUBMOD}`**: Aksi atau layar spesifik (contoh: `INQUIRY`, `INPUTNOMINAL`, `KLIKICONPENGZAKU`).
- **`{ScenarioName}`**: Deskripsi singkat skenario uji.

> [!NOTE]
> **Datacore Truncation Immunity**: Token penamaan resmi yang terpotong dari SSOT (seperti `PULSAREGULETELK`, `LISTRI`, `PINJAM`) adalah konvensi resmi bawaan bank. Dilarang mengubah atau me-rename token tersebut.

---

## 2. Core Banking AS400 (IBM i) & Terminal 5250

Pengujian fitur finansial sering kali membutuhkan validasi sisi server/host menggunakan emulator IBM Personal Communications (PCOMM) 5250:
- **DD5000**: Inquiry Saldo & Mutasi Rekening Tabungan (Demand Deposit).
- **CD5000**: Inquiry Rekening Deposito (Certificate of Deposit).
- **LN5000**: Inquiry Fasilitas Pinjaman / Kredit (Loan).
- **GL5000**: Verifikasi Jurnal Umum Buku Besar (General Ledger).

---

## 3. Kebijakan Keamanan Zero PII Leakage

Sebagai penguji aplikasi finansial berlisensi Bank Indonesia & OJK:
1. **Dilarang Keras** menampilkan nomor kartu debit/kredit utuh (16 digit), CVV, password nasabah, atau PIN transaksi di log pengujian, commit message, maupun tangkapan layar publik.
2. Gunakan masking standar: `4201-92xx-xxxx-1679` atau format 4 digit terakhir.
3. Saldo nasabah riil pada evidence pengujian wajib dibersihkan atau ditutup.

---
*Bank Mega Standards Guide — Yerly-Playground 🌸*
