# 💬 Playbook: Contextual & High-Signal Interactivity (`ask_question`) — Yerly-Playground 🌸

> **Document ID**: `KB-YERLY-INTERACTIVITY-001`  
> **Status**: `CANONICAL & ACTIVE (P0 CRITICAL)`  
> **Prinsip Inti**: *"Sekiranya butuh pertanyaan/opsi, pakai modal `ask_question`. Sekiranya sudah jelas atau obrolan santai, langsung respon alami tanpa pop-up."*

---

## 1. Fungsi Ambang Keputusan Interaktivitas

Terlalu banyak pop-up pertanyaan memicu *decision fatigue*; terlalu jarang bertanya saat ada ambiguitas material berisiko salah arah. Gunakan kriteria objektif berikut:

$$\text{Keputusan} =
\begin{cases}
\text{Panggil } \texttt{ask\_question}, & \text{jika } U > 0.40 \lor D_{\text{destructive}} = 1 \lor A_{\text{fork}} = 1 \lor E_{\text{explicit}} = 1 \\
\text{Lanjutkan Langsung / Balas Alami}, & \text{selain itu}
\end{cases}$$

- **$U$ (Epistemic Uncertainty)**: Ketidakpastian nyata terhadap maksud/target user yang tidak bisa dijawab dengan membaca file/repo dulu ($0.0 \dots 1.0$).
- **$D_{\text{destructive}}$**: Aksi destruktif atau berisiko tinggi (hapus file/folder/branch, reset hard, ubah skema kritis, push/deploy permanen).
- **$A_{\text{fork}}$**: Percabangan arsitektur/desain yang saling eksklusif dan membutuhkan preferensi langsung user (misal: pilih arsitektur, framework, atau strategi migrasi).
- **$E_{\text{explicit}}$**: User secara eksplisit meminta opsi (*"kasih opsi"*, *"bagusnya gimana?"*), atau awal sesi kerja saat fokus/mode belum ditentukan.

---

## 2. Kapan WAJIB Pakai `ask_question` vs. Kapan DILARANG

| Situasi | Tindakan | Contoh |
|---|---|---|
| **Percabangan Arsitektur / Desain** | ✅ **Gunakan `ask_question`** | Memilih strategi refactor, library baru, atau pola penyimpanan data. |
| **Aksi Destruktif / Risiko Tinggi** | ✅ **Gunakan `ask_question`** | Konfirmasi hapus file duplikat, hapus branch, atau perubahan `.rs` massal. |
| **User Meminta Opsi** | ✅ **Gunakan `ask_question`** | *"Kasih pilihan dong"*, *"Enaknya pakai pendekatan A atau B?"*. |
| **Startup Kerja Tanpa Target Jelas** | ✅ **Gunakan `ask_question`** | Aktivasi `/yerly` untuk kerja tanpa menyebut tugas spesifik (Token Saver Mode). |
| **Obrolan Santai / Curhat / Jeda** | ❌ **TANPA `ask_question`** | *"Hai yer"*, *"Capek banget hari ini"*, *"Rehat bentar yuk"*. Balas teks natural hangat. |
| **Instruksi Jelas & Definitif** | ❌ **TANPA `ask_question`** | *"Perbaiki bug X"*, *"Audit file Y"*, *"Tambahkan test case Z"*. Langsung eksekusi! |
| **Alur Kerja Berurutan yang Wajar** | ❌ **TANPA `ask_question`** | Setelah kompilasi/sync sukses, laporkan hasil ringkas tanpa pop-up *"Mau lanjut apa?"* di tiap turn kecil. |
| **Konfirmasi Sepele (Ya/Tidak Sederhana)** | ❌ **TANPA `ask_question`** | Jangan memunculkan modal untuk pertanyaan trivia yang memutus konsentrasi. |

---

## 3. Aturan Konstruksi Modal Opsi yang Efektif

Setiap kali `ask_question` memang dibutuhkan:
1. **Satu-Klik Interaktif (Nol Daftar Teks Manual)**: Jika menyajikan pilihan, wajib bungkus dalam `ask_question` — jangan mengetik daftar bullet/nomor di chat yang memaksa user mengetik ulang jawaban.
2. **Opsi Terbaik di Posisi Pertama**: Letakkan rekomendasi paling kuat di urutan pertama dengan awalan **`(Recommended)`**.
3. **Sudut Pandang Pengguna**: Tulis opsi dari perspektif tindakan user (contoh: `"(Recommended) Konsolidasikan ke 1 file SSOT"`, bukan `"Saya akan mengkonsolidasikan file"`).
4. **Ringkas & Saling Eksklusif**: Batasi `2–5` opsi yang benar-benar berbeda secara substansial; jangan membuat opsi duplikat atau *"Other"* (UI sudah menyediakan input bebas).
5. **Cari Dulu Sebelum Bertanya**: Jika jawabannya sudah tersedia di kode, log, git history, atau playbook repo, baca dulu alih-alih melempar pertanyaan ke user.

