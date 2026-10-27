# 💻 Playbook: AS400 Core Banking (IBM i 5250) — Yerly-Playground 🌸

Pedoman verifikasi transaksi perbankan langsung ke host AS400 melalui emulator terminal 5250 (PCOMM).

---

## 1. Katalog Program Inquiry

1. **DD5000 (Demand Deposit)**:
   - Digunakan untuk memeriksa saldo efektif, saldo mengendap, dan mutasi debit/kredit rekening tabungan nasabah.
   - Shortcut F-Key: `F3` (Exit), `F12` (Cancel), `F5` (Refresh).
2. **CD5000 (Certificate of Deposit)**:
   - Digunakan untuk memeriksa penempatan deposito berjangka, suku bunga, dan tanggal jatuh tempo.
3. **LN5000 (Loan)**:
   - Digunakan untuk memeriksa jadwal angsuran kredit, sisa pokok pinjaman, dan status kolektibilitas.
4. **GL5000 (General Ledger)**:
   - Digunakan untuk audit pembukuan jurnal perbankan dan memastikan keseimbangan debit/kredit.

---

## 2. Prosedur Navigasi Aman
- Selalu periksa status indikator `X System` atau `MW (Message Wait)` sebelum mengirim input.
- Tekan `Reset` pada emulator jika layar terkunci.
- Pastikan melakukan sign-off (`SO` / `SIGNOFF`) setelah selesai melakukan inquiry untuk menjaga slot sesi host.

---
*AS400 Host Playbook — Yerly-Playground 🌸*
