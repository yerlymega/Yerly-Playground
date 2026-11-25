# 📱 Playbook: Bank Mega Revamp M-Smile Testing — Yerly-Playground 🌸

Pedoman pengujian fitur-fitur utama aplikasi Bank Mega Revamp M-Smile (Android & iOS).

---

## 1. Modul Utama & Alur Transaksi

| Modul | Sub-Modul | Skenario Kunci |
|---|---|---|
| **Transfer** | BI-FAST, Online, Sesama Mega, Valas | Validasi rekening tujuan, nomor referensi, biaya admin, limit harian |
| **Top Up** | Pulsa, Paket Data, PLN Prabayar, E-Wallet | Pilihan denom, normalisasi format nomor HP, validasi saldo sumber |
| **Zaku** | Zaku Arisan, Zaku Impian, Pengaturan | Pemilihan kelompok arisan, ganti rekening autodebet, status undian |
| **MPIN & Security**| Transaksi Finansial, Blokir Kartu, Ubah PIN | Masking 6 digit MPIN, verifikasi keypad acak, biometric fingerprint |

---

## 2. Penanganan Error & Kode Respons Perbankan

- **B5 / M68**: Transaksi Timeout / Koneksi Terputus ke Switcher.
- **F68**: Transaksi Sedang Diproses (butuh rekonsiliasi manual).
- **VLD077**: Status Rekening Dorman (harus aktivasi ke cabang).
- **ERR_SALDO**: Saldo sumber dana tidak mencukupi untuk nominal transaksi + biaya admin.

---

## 3. Rujukan Lanjutan KMP & Self-Healing
- Untuk arsitektur **M-Smile KMP (Compose Multiplatform)**, Universal `testID`, Rules 53–68, Live Spying `S0`–`S7`, flow Paket Data/E-Wallet, dan katalog `[RC]` terbaru: rujuk [`kmp-revamp-m-smile.md`](kmp-revamp-m-smile.md).
- Untuk self-healing locator in-process (`v1.16.1`): rujuk [`locara-self-healing.md`](locara-self-healing.md).

---
*Bank Mega M-Smile Playbook — Yerly-Playground 🌸*
