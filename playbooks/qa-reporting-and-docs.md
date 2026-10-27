# 📑 Playbook: QA Reporting, Sign-Off & Evidence Compilation — Yerly-Playground 🌸

Pedoman penyusunan laporan pengujian mutu, Berita Acara UAT Sign-Off (.docx), dan kompilasi bukti pengujian.

---

## 1. Kompilasi Screenshot Evidence UAT
- Format folder evidence: `Include/evidence/Master_[TC_NAME]/`
- Penomoran screenshot wajib 2-digit berurutan: `01.png`, `02.png`, `03.png`, dst.
- Screenshot harus merepresentasikan setiap transisi state penting:
  1. Halaman input data / nominal.
  2. Halaman konfirmasi rincian transaksi & biaya admin.
  3. Layar input MPIN (tersanitasi).
  4. Layar resi transaksi sukses (atau pesan error).

---

## 2. Penyusunan Berita Acara UAT
- Dokumen Word (.docx) Berita Acara UAT memuat:
  1. Ringkasan eksekusi (Total TC, Pass rate 100%, Defect count = 0).
  2. Matriks hasil pengujian.
  3. Lampiran tangkapan layar 2 kolom yang rapi dan mudah dibaca oleh stakeholder bisnis.

---
*QA Reporting Playbook — Yerly-Playground 🌸*
