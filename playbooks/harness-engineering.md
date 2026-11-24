# 🛡️ Playbook: Harness Engineering & Deterministic Execution Guards — Yerly-Playground 🌸

> **Document ID**: `KB-YERLY-HARNESS-001`  
> **Status**: `CANONICAL & ACTIVE (P0 CRITICAL)`  
> **Axiom**: *"LLM menghasilkan hipotesis; Harness memvalidasi dan menegakkan realitas deterministik."*

---

## 1. Filosofi Harness Engineering

Prompt engineering menentukan **apa yang ingin dilakukan AI**, sedangkan **Harness Engineering** menentukan **apa yang secara nyata diizinkan terjadi di sistem**. Tanpa harness deterministik, perubahan kode/skrip berisiko menyisakan sintaks pincang, API halusinasi, kebocoran PII, perubahan di luar cakupan, atau hilangnya kode rekan tim saat merge Git.

---

## 2. Arsitektur 5-Lapis Defense-in-Depth Harness

| Layer | Tanggung Jawab | Mekanisme & Alat | Kondisi Penolakan (Fail-Closed) |
|---|---|---|---|
| **L1 — Syntactic & AST Guard** | Kebenaran struktur kode, keseimbangan kurung, API valid | Lexical brace counter (sadar string & komentar), AST parser (`python3 -m py_compile`, `groovyc`, `tsc`, `tools/audit_katalon.py`) | `brace_depth != 0`, syntax error, pemanggilan API fiktif (`KeywordUtil.logWarn` / `logWarning`) |
| **L2 — Sanitization & PII Guard** | Nol PII produksi & nol kebocoran rahasia | Regex scanner untuk NIK 16-digit, PAN kartu, CVV, PIN/password riil, API key/token | Terdeteksinya data nasabah asli atau kredensial mentah di kode/log/test data |
| **L3 — Scope & Anti-Tamper Guard** | Isolasi blast radius & integritas Object Repository | Whitelist folder fitur aktif, proteksi file `.rs`, diff review | Modifikasi file di luar cakupan tugas atau perubahan locator `.rs` tanpa izin |
| **L4 — Semantic & Behavioral Guard** | Kebenaran logika runtime & anti-hang | Eksekusi sandbox terisolasi (`os.tmpdir()`), unit/regression tests, assertion proof, watchdog timeout | `exit_code != 0`, test gagal, false-green assertion, proses hang/timeout |
| **L5 — VCS Lossless Guard** | Keselamatan kolaborasi Git multi-branch | `git worktree` ephemeral 3-way merge simulation, audit commit rekan tim | Konflik tak terselesaikan, hilangnya kode rekan tim, force-push destruktif |

---

## 3. Pre-Flight Harness: Blast Radius Scoring ($BR$)

Evaluasi dampak perubahan sebelum menyentuh disk:

$$BR = (N_{\text{files}} \times 2.0) + (N_{\text{dependents}} \times 1.5) + (C_{\text{contract}} \times 5.0)$$

- $N_{\text{files}}$: jumlah file yang diubah/dibuat.
- $N_{\text{dependents}}$: jumlah modul hilir yang mengimpor/memanggil file tersebut.
- $C_{\text{contract}}$: `1` bila signature publik, skema kontrak, atau locator OR berubah; `0` bila tidak.

**Ambang Tindakan**:
- **$BR \le 5.0$ (Rendah)**: Lanjutkan mandiri dengan validasi L1–L4.
- **$5.0 < BR \le 12.0$ (Menengah)**: Wajib uji di branch/worktree terisolasi sebelum digabung.
- **$BR > 12.0$ (Tinggi / Kritis)**: Hentikan sementara dan minta persetujuan eksplisit via `ask_question` dengan paparan blast radius.

---

## 4. In-Flight Harness: Lexical Guard & Execution Watchdogs

### A. Lexical Brace Balance (`depth == 0`)
Penghitung kurung kurawal wajib mengabaikan karakter `{` dan `}` di dalam literal string (`"..."`, `'...'`) maupun komentar (`//`, `/* ... */`) agar bebas false-positive/false-negative.

### B. Filter API Katalon `KeywordUtil`
| Panggilan Diblokir (Halusinasi) | Pengganti Resmi |
|---|---|
| `KeywordUtil.logWarn(...)` / `logWarning(...)` | `KeywordUtil.markWarning(...)` atau `KeywordUtil.logInfo("[WARN] ...")` |
| `KeywordUtil.logError(...)` | `KeywordUtil.markError(...)` atau `KeywordUtil.markFailed(...)` |
| `KeywordUtil.logDebug(...)` | `KeywordUtil.logInfo("[DEBUG] ...")` |

### C. Batas Waktu Eksekusi (Watchdog)
- **Lint / AST / Static Check**: maks **15 detik**.
- **Unit / Integration Test**: maks **60 detik**.
- **Mobile / Appium Session Step**: maks **120 detik** (sinkron dengan Rule 67 untuk layar hang).
- **Anti-Infinite-Loop**: Output identik berulang > 30 detik harus dihentikan dan dilaporkan.

### D. Isolasi State Pengujian
Setiap test otomatis yang menulis file state/jurnal/laporan wajib diarahkan ke direktori temporer terisolasi (`tempfile.TemporaryDirectory()` / `os.tmpdir()`) agar tidak pernah merusak data produksi atau proses dev yang sedang berjalan.

---

## 5. Post-Flight Harness: Lossless 3-Way Git Worktree Guard

Sebelum merge antar-branch kolaborasi tim, simulasikan merge di worktree sementara tanpa menyentuh working directory utama:

```bash
WORKTREE_DIR=$(mktemp -d)
git worktree add -d "$WORKTREE_DIR" HEAD
git -C "$WORKTREE_DIR" merge --no-commit --no-ff <feature_branch>
# Verifikasi zero conflict, test lulus, dan nol file rekan tim terhapus
git -C "$WORKTREE_DIR" merge --abort
git worktree remove --force "$WORKTREE_DIR"
```

---

## 6. Payload Umpan Balik Terstruktur & 3-Strike Circuit Breaker

1. **Structured Rejection Feedback**: Setiap kegagalan harness harus menyebutkan secara presisi: `layer`, `failure_type`, `target_file`, `line_number`, `invariant_violated`, dan `remediation_hint` (hindari pesan error samar).
2. **3-Strike Circuit Breaker**: Jika **3 kali** perbaikan berturut-turut tetap gagal pada Layer 1–3, hentikan loop seketika, kembalikan file ke kondisi bersih, dan laporkan akar kendala ke Boss Yerly.
3. **PII Leak Instant Halt**: Bila data sensitif riil terdeteksi sebelum ditulis/dikirim, batalkan operasi seketika dan bersihkan payload.

---

## 7. Checklist Harness Pra-Selesai
- [ ] **L1**: AST & sintaks valid (`depth == 0`), nol unused imports, nol method fiktif.
- [ ] **L2**: Zero raw PII & zero secrets.
- [ ] **L3**: Scope terkunci pada target; `.rs` tidak diubah tanpa izin.
- [ ] **L4**: Build & test suite dijalankan nyata dengan `exit_code == 0` (anti false-green).
- [ ] **L5**: Kode rekan tim 100% utuh; `git status` & `git diff` bersih.

