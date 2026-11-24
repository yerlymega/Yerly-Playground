# 💻 Playbook: Clean Code, Modular Architecture & Engineering Craft — Yerly-Playground 🌸

> **Document ID**: `KB-YERLY-CLEANCODE-001`  
> **Status**: `CANONICAL & ACTIVE (P0 CRITICAL)`  
> **Golden Rule**: *"Solusi terbaik bukan yang paling rumit, melainkan solusi paling sederhana yang aman, mudah dibaca, teruji, dan memenuhi kebutuhan nyata."*

---

## 1. Standar 18 Pilar Clean Code & Software Engineering

Setiap kode produksi, skrip otomasi, maupun utility tool wajib mematuhi 18 pilar berikut:

| # | Pilar | Standar Wajib | Anti-Pattern yang Dilarang |
|---|---|---|---|
| **1** | **Clean Code & Readability** | Kode dibaca sekali langsung paham alurnya; alur lurus tanpa trik sintaks berbelit. | One-liner rumit, nested ternary, atau gaya "sok pintar" yang menyulitkan tim/junior. |
| **2** | **Modularisasi** | Pecah modul berdasarkan batas tanggung jawab jelas; target **< 300 baris** per modul/orchestrator; struktur ketergantungan DAG bebas circular import. | File monolitik 1.000+ baris (*God Object* / *Kitchen-Sink*) dengan dependensi melingkar. |
| **3** | **Anti-Redundancy (DRY)** | Satu sumber kebenaran (*Single Source of Truth*) per aturan/logika. Terapkan *Rule of Three* sebelum mengabstraksi. Lindungi *Intentional Duplication* yang disengaja demi isolasi. | Copy-paste blok logika identik di banyak file atau membuat file dokumen tumpang tindih. |
| **4** | **Single Responsibility (SRP)** | Setiap file, class, komponen, dan fungsi memiliki tepat satu alasan untuk berubah. | Satu fungsi sekaligus parsing input, memanggil API, menyimpan file, dan memformat UI. |
| **5** | **Naming Jelas & Konsisten** | Gunakan nama deskriptif yang mengungkap niat (*verb* untuk aksi, *noun* untuk data, `is`/`has`/`can` untuk boolean), konsisten casing (`camelCase` JS/Groovy, `snake_case` Python, `PascalCase` class). | Nama samar (`tmp`, `data2`, `handleStuff`, `x`, `flag`) atau campur aduk bahasa identifier. |
| **6** | **Fungsi Kecil & Fokus** | Satu tingkat abstraksi per fungsi; gunakan **guard clause / early return**; jaga kedalaman indentasi $\le 3$ level. | Fungsi ratusan baris dengan 5+ level `if/else` bersarang (*arrow anti-pattern*). |
| **7** | **Separation of Concerns (SoC)** | Pisahkan tegas Presentation/UI, Business Logic/Domain, Data Access/Infrastructure, dan Config. | Menaruh query database, panggilan HTTP mentah, atau logika bisnis berat di komponen UI/View. |
| **8** | **Reusable Components** | Ekstrak helper/komponen bersama yang bersih dan terparameterisasi tanpa abstraksi prematur berlebihan. | Membuat layer factory/adapter berlapis untuk logika yang cuma dipakai sekali. |
| **9** | **Proper Error Handling** | Fail fast, kembalikan pesan error kontekstual dengan sebab & aksi pemulihan; tangani batas kegagalan secara eksplisit. | `try { ... } catch (e) {}` kosong, menelan error diam-diam, atau mengembalikan dummy sukses palsu. |
| **10** | **Input Validation** | Validasi seluruh input di batas masuk (*boundary* — form, API, CLI, file config) menggunakan schema/allowlist ketat (*fail-closed*). | Mempercayai payload eksternal tanpa cek tipe, rentang nilai, atau karakter ilegal. |
| **11** | **Zero Hardcoded Values** | Simpan konstanta, timeout, URL, dan batas bisnis di `constants` / `config` / environment variables; gunakan `path.join()` / `pathlib.Path` untuk path lintas OS. | Magic numbers (`86400`, `30000`), path absolut mesin pribadi (`C:/Users/...`, `/Users/...`), atau URL mentah tersebar di banyak file. |
| **12** | **Style & Folder Consistency** | Patuhi konvensi penamaan, struktur direktori, dan pola kode yang sudah mapan di repositori sebelum memperkenalkan pola baru. | Mencampur dua pola arsitektur atau struktur folder berbeda dalam satu fitur tanpa alasan. |
| **13** | **Concise "Why" Comments** | Tulis komentar ringkas **1–2 baris** hanya untuk menjelaskan **"kenapa"** (aturan bisnis, bug upstream, invariansi keamanan/konkurensi) — bukan mengulang **"apa"** yang sudah jelas dari kode. | Banner ASCII (`// ====`), narasi `Step 1/2/3`, penutup `} // end if`, atau komentar bertele-tele 5+ baris. |
| **14** | **Zero Dead Code & Unused Imports** | Bersihkan seluruh import, variabel, dan helper yang tidak terpakai akibat perubahan kita; laporkan dead code warisan terpisah sebelum menghapusnya. | Meninggalkan blok kode di-comment-out, import menganggur, atau fungsi mati di file yang disentuh. |
| **15** | **Type Safety** | Gunakan tipe eksplisit (TypeScript strict, Python type hints, Zod/schema validation, static imports Groovy) agar bug tertangkap sebelum runtime. | Penggunaan `any` bebas, string reflection untuk method yang bisa diimpor statis, atau casting tanpa validasi. |
| **16** | **Efficient Performance (No Premature Opt)** | Hindari pemborosan nyata ($O(n^2)$ tak perlu, query `N+1`, memory/listener leak, polling rapat); optimasi lebih lanjut hanya berdasarkan profiling & bukti pengukuran. | Micro-optimization yang merusak keterbacaan tanpa benchmark, atau sebaliknya membiarkan bottleneck jelas. |
| **17** | **Testability & Maintainability** | Gunakan Dependency Injection eksplisit, pisahkan pure functions dari side effects, isolasi state test di temp dir, dan tulis assertion bermakna (anti false-green). | Hidden global singletons yang mustahil di-mock, atau test `assert true == true` yang tak pernah bisa gagal. |
| **18** | **Security & Backward Compatibility** | Nol secret/API key/PII di kode & git; sanitasi input (anti SQLi/XSS/path traversal/XXE); jaga kontrak publik dan fitur lama tetap berjalan utuh (*preserve behavior before refactoring*). | Hardcode token/password, mengubah perilaku endpoint/helper eksisting tanpa migrasi atau persetujuan. |

---

## 2. Taksonomi Audit Redundansi (7 Kelas) & Safe Deletion

Sebelum mengkonsolidasikan atau menghapus duplikasi, klasifikasikan temuan ke 7 kategori:
1. **Exact Duplication** — konten identik persis (wajib disatukan).
2. **Functional Duplication** — dua implementasi berbeda untuk tanggung jawab identik (konsolidasikan ke satu SSOT).
3. **Architectural Duplication** — dua lapisan/modul dengan peran tumpang tindih.
4. **Configuration Duplication** — definisi setting ganda yang rawan konflik/drift.
5. **Instruction Duplication** — aturan/prompt yang diulang di banyak file (ganti duplikat dengan pointer ke SSOT).
6. **Dependency Duplication** — dua library berbeda untuk kebutuhan yang sama.
7. **Intentional Duplication *(PROTECTED)*** — pengulangan yang disengaja demi isolasi, kompatibilitas lintas OS/platform, atau keamanan — **jangan dihapus otomatis**.

### 7-Check Safe Deletion Policy
Sebelum menghapus file atau simbol apapun, verifikasi: (1) seluruh referensi langsung, (2) dynamic import/reflection, (3) runtime discovery/manifest, (4) build & CI scripts, (5) integrasi eksternal, (6) keunikan perilaku, dan (7) pastikan pengganti sudah utuh serta minta konfirmasi eksplisit pemilik sebelum `rm`.

---

## 3. Urutan Prioritas Keputusan Rekayasa

`1. Security & Safety` > `2. Production Stability` > `3. Correctness` > `4. Root Cause` > `5. Data Integrity` > `6. Reliability` > `7. Maintainability` > `8. Performance` > `9. Scalability` > `10. Elegance`

### Checklist Pra-Serah Kode
- [ ] Semua perubahan terkunci pada scope tugas (*zero unsolicited refactor*).
- [ ] Nol unused imports, nol hardcoded secrets/paths, nol empty `try-catch`.
- [ ] Fungsi ringkas, nama konsisten, komentar seperlunya (jelaskan *kenapa*).
- [ ] Backward compatibility & fitur lama terverifikasi tidak rusak.
- [ ] Build, linter/AST, dan test suite berjalan nyata dengan `exit_code == 0`.

