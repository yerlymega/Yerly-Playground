# 🏛️ Playbook: Semantic Versioning (SemVer 2.0.0) & Release Engineering — Yerly-Playground 🌸

> **Document ID**: `KB-YERLY-SEMVER-001`  
> **Status**: `CANONICAL & ACTIVE (P1 HIGH)`  
> **Scope**: Versioning, Breaking-Change Detection, Changelog, Zero-Downtime Migration & GitHub Release Lifecycle

---

## 1. Filosofi & Invarian Utama

Semantic Versioning (`MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD_METADATA]`) adalah **kontrak kepercayaan** antara pengembang dan konsumen perangkat lunak:
1. **SemVer is a Promise, Not Proof**: Angka versi menyatakan niat; pembuktian kompatibilitas tetap dibuktikan lewat test kontrak & regression suite.
2. **No Stealth Breaking Changes**: Perubahan yang mematahkan kompatibilitas mundur **wajib** menaikkan `MAJOR`, dilarang diselipkan ke `MINOR` atau `PATCH`.
3. **Expand-and-Contract Doctrine**: Migrasi skema database, API, atau konfigurasi produksi wajib melewati fase transisi berdampingan (*dual-read / dual-write*) sebelum elemen lama dihapus.
4. **Deterministic Rollback**: Setiap rilis harus punya jalur rollback cepat dan teruji tanpa merusak data.

### Tata Bahasa & Precedence
- **`MAJOR` (`X.0.0`)**: Breaking change (mematahkan kontrak lama).
- **`MINOR` (`0.Y.0`)**: Fitur baru yang 100% backward-compatible.
- **`PATCH` (`0.0.Z`)**: Bugfix / keamanan / refactor internal yang 100% backward-compatible.
- **Precedence**: `1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0`. Build metadata (`+build.42`) tidak memengaruhi precedence.
- **Range Syntax**: `^1.2.3` (izinkan MINOR+PATCH `<2.0.0`), `~1.2.3` (PATCH saja `<1.3.0`), `1.2.3` (strict pinning untuk komponen mission-critical).

### Matriks Tata Kelola 2-Level
- **Level 1 (Strict Quality Gate)**: Repositori bersama/tim, rilis aplikasi perbankan, API publik, migrasi DB, merge ke `main`/`master` → wajib annotated tag `vX.Y.Z`, audit breaking change, `CHANGELOG.md`, dan Migration Guide (jika `MAJOR`).
- **Level 2 (Flexible Advisory)**: Skrip scratch lokal & eksperimen cabang pribadi → cukup commit message deskriptif.

---

## 2. Detektor Breaking Change 7-Lapis

Uji setiap perubahan terhadap 7 lapisan sebelum menentukan kenaikan versi:

| Lapisan | Breaking (`MAJOR`) | Backward-Compatible (`MINOR` / `PATCH`) |
|---|---|---|
| **1. API Contract** | Hapus endpoint/field, ubah tipe data, tambah parameter **wajib** | Tambah endpoint baru, field response opsional, parameter request opsional |
| **2. Database & State** | Hapus/rename kolom langsung, `NOT NULL` tanpa default, ubah tipe kolom | Tambah kolom `NULLABLE` / ber-`DEFAULT`, tambah index non-blocking |
| **3. CLI & Shell** | Rename flag, ubah exit code gagal, ubah format stdout terstruktur | Tambah flag opsional baru, perjelas pesan error stderr |
| **4. Config & Env** | Hapus env wajib, ubah struktur kunci root config | Beri nilai default aman jika kunci baru tidak diset |
| **5. Mobile Clients** | Matikan API lama yang masih dipakai versi APK/IPA aktif di store | Sediakan `/v1/` dan `/v2/` paralel sampai adopsi versi baru aman |
| **6. Wire / Serialization** | Ubah framing/skema payload tanpa fallback pembaca versi lama | Tambah field terstruktur dengan reader kompatibel versi sebelumnya |
| **7. Public Module API** | Hapus/ubah signature fungsi/keyword yang dipanggil modul lain | Deprecate dulu dengan peringatan jelas + pertahankan adapter sementara |

---

## 3. Pola Zero-Downtime: Expand-and-Contract

1. **Fase 1 — Expand (`MINOR`)**: Tambahkan kolom/field/endpoint baru secara paralel. Kode baru melakukan *dual-write* agar client lama tetap berjalan normal.
2. **Fase 2 — Migrate**: Jalankan backfill data lama secara aman dan verifikasi konsistensi.
3. **Fase 3 — Contract (`MAJOR`)**: Alihkan pembacaan penuh ke kontrak baru; hapus kolom/field lama hanya setelah trafik versi lama terbukti `0%`.

---

## 4. Standar `CHANGELOG.md` (Keep a Changelog) & Hotfix

Kelompokkan setiap versi dengan kategori baku: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- **Emergency Hotfix**: Buat branch `hotfix/vX.Y.Z+1` dari tag produksi terakhir → surgical patch minimal tanpa fitur baru → bump `PATCH` → merge kembali ke `main` + pasang tag baru → catat di `### Security` / `### Fixed`.
- **Migration Guide (Wajib pada `MAJOR`)**: Sertakan ringkasan breaking changes dan diff konkret cara migrasi dari `v(N-1).x` ke `vN.0.0`.

---

## 5. Golden 6-Step Release & GitHub Presentation Lattice

Untuk setiap peluncuran repositori perdana (`v1.0.0`) maupun rilis naik versi berikutnya:
1. **Descriptor & Changelog**: Selaraskan versi di `package.json` / `build.gradle` / `README.md` dan perbarui `CHANGELOG.md`.
2. **Empirical Clean Build & Zero-Secrets Audit**: Jalankan linter, test suite, dan build hingga 100% PASS (`exit_code == 0`), pastikan zero secrets/PII di `git ls-files`.
3. **Atomic Commit & Annotated Tag**: Gunakan Conventional Commits (`feat:`, `fix:`, `chore(release):`) dan `git tag -a vX.Y.Z -m "Release vX.Y.Z: ..."`.
4. **Push & GitHub About Metadata**: Push branch + tag, lalu pastikan deskripsi, homepage, dan topics terisi (`gh repo edit <org>/<repo> --description ... --add-topic ...`).
5. **Publikasi GitHub Release Resmi**: Terbitkan halaman rilis resmi via `gh release create vX.Y.Z <assets> --title "..." --notes "..."` agar tidak menyisakan `"No releases published"`, lalu verifikasi lewat `gh repo view`.
6. **Sinkronisasi Memori / Dokumentasi**: Catat hash commit, tag, dan catatan rilis di `memory/daily/` atau dokumentasi rilis proyek.

