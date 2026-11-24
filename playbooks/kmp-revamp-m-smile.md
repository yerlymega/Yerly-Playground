# 📱 Playbook: Bank Mega M-Smile KMP & Revamp Automation Standard — Yerly-Playground 🌸

> **Document ID**: `KB-YERLY-KMP-REVAMP-001`  
> **Status**: `CANONICAL & ACTIVE (P0 CRITICAL)`  
> **Scope**: `Bank-Mega-QA/KMP-Revamp_M-Smile` (Compose Multiplatform / KMP) & `Bank-Mega-QA/Revamp_M-Smile` (React Native)  
> **Companion**: [`qa-katalon-mobile.md`](qa-katalon-mobile.md) · [`locara-self-healing.md`](locara-self-healing.md) · [`datacore-ssot.md`](datacore-ssot.md)

---

## 1. Pergeseran Arsitektur: Revamp (React Native) vs. KMP (Compose Multiplatform)

| Aspek Teknis | `Revamp_M-Smile` (React Native Legacy) | `KMP-Revamp_M-Smile` (Kotlin / Compose Multiplatform) |
|---|---|---|
| **Ukuran APK & Runtime** | ~234.8 MB, Hermes JS bridge, multi-ABI | ~36.9 MB (-84%), native rendering tanpa JS bridge, single DEX |
| **Pohon Visual UI** | Hierarki `ViewGroup` berlapis, rentan collapse di Android 14–16 | Hierarki Compose datar dan deterministik lintas versi Android |
| **Kontrak Locator** | Relative XPath (`/ancestor::`, `/parent::`) + Accessibility ID | Universal `testID` (`testTagsAsResourceId = true` → `@resource-id` di Android & `accessibilityIdentifier` di iOS) |
| **Katalog Produk** | Sebagian berpindah screen/modal terpisah | **Dynamic In-Page Catalog**: muncul di layar yang sama pasca-input nomor |
| **Organisasi Test** | `Test Cases/Master/` + `Test Cases/Screen Flow/` | `Test Cases/Master Test Case/` + `Test Cases/Child Test Case/` (dipisah `Positive/` & `Negative/`) |
| **Self-Healing Engine** | Legacy exception handler | `LocaraHook` (`ENABLE_LOCARA`, profil `KMP` / `REVAMP` / `AUTO`) |

### Kontrak Universal `testID` KMP (`<layar>_<elemen>_<sufiks>`)
- **Sama persis antara Android (`@resource-id`) dan iOS (`Accessibility ID`)**, serta netral lintas bahasa (ID/EN).
- **Aturan Mutlak**: Gunakan `testID` untuk menemukan elemen; gunakan teks **hanya untuk asersi** (`VerificationHelper`).
- **Sufiks Kanonikal**: `_screen`, `_button`, `_input`, `_tap`, `_error`, `_value`, `_title`, `_sheet`, `_scrim`, `_item_<key>`, `_card`, `_back_button`, `_close_button`.
- **Dynamic PIN Pad (`confirm_pin_sheet`)**: Keypad diacak setiap kali sheet dibuka atau PIN salah, namun `pin_key_<digit>` selalu menempel pada **nilai angkanya**, bukan posisi grid. Digit ke-6 memicu **auto-submit** (`pin_processing`) tanpa tombol OK.

---

## 2. Doktrin Dua Pilar Verifikasi (Two-Pillar Verification Invariant)

Untuk menghilangkan penggunaan Groovy raw `assert` yang tidak informatif **tanpa** membuat wrapper boolean palsu (`verifyTrue`/`verifyFalse`):
1. **Pilar 1 — Kesiapan Layar & Navigasi (`WaitUtil`)**:
   Gunakan `WaitUtil.waitForScreen(...)` / `WaitUtil.waitForElementPresent(...)` lalu `if (!isLoaded) KeywordUtil.markFailedAndStop(...)`.
2. **Pilar 2 — Verifikasi Data Transaksi (`helpers.VerificationHelper`)**:
   - `verificationValidationText`: validasi status (`BERHASIL`) dan pesan error.
   - `verificationValidationTextAny`: validasi multi-pola dipisah `|` dengan loop `for` sederhana (ramah QA junior).
   - `verificationMaskedNumber`: rekening sumber ter-masking (`1074****8114`).
   - `verificationMatch`: pencocokan provider, produk, atau inline error form.
   - `verificationNumeric`: nominal, biaya admin, total pembayaran, dan integritas aritmatika (`Nominal + Biaya Admin == Total`, `Header Total == Detail Total`).

---

## 3. Aturan Operasional Baku KMP & Revamp (Rules 53–68)

| Rule | Nama Aturan | Ketentuan Inti |
|---|---|---|
| **Rule 53** | **In-Page Dynamic Catalog** | Dilarang mengetuk `Continue`/`Lanjut` pada child input nomor HP. Katalog paket/denom muncul di layar yang sama; `Continue` hanya diketuk **setelah** item dipilih. |
| **Rule 54** | **3-Stage Balance Pre-Check** | Master transaksional wajib inspeksi saldo awal melalui 2 rute baku: **Rute 1** (Login → Dashboard Saldo Awal → Akun Saya → Detail Tabungan & Hold Balance → Reset Dashboard → Transaksi → Rekonsiliasi Saldo Akhir → `finally` Reset) atau **Rute 2** (langsung shortcut transaksi dari Detail Tabungan tanpa balik ke Dashboard). |
| **Rule 55** | **Object Repository First** | Wajib pakai `findTestObject('Object Repository/...')` untuk elemen yang sudah ada `.rs`-nya. Inline `new TestObject` hanya boleh untuk secondary fallback berparameter dinamis saat runtime. |
| **Rule 56** | **Domain Variable Segregation** | Pisahkan tegas `nominal` (Pulsa) dan `packageName` (Paket Data). Dilarang nesting `getVar` redundant. |
| **Rule 57** | **Master Parameter Hygiene** | Dilarang mengoper konfigurasi infrastruktur (`delayDuration`, `pageLoadDuration`) dari Master ke Child; Child ambil langsung dari `MobileBaseConfig`. Master hanya oper data bisnis dinamis & konteks screenshot (`screenshotPath`, `screenshotCounter`). |
| **Rule 58** | **Static Import Over `CustomKeywords`** | Dilarang memanggil `CustomKeywords.'screens.X.method'(...)`. Wajib static import Groovy (`import screens.DashboardScreen` → `DashboardScreen.method(...)`) demi type safety dan compile-time verification. |
| **Rule 59** | **Anti-Skeleton Shimmer (3-Lapis)** | Jangan screenshot hanya karena `home_screen` muncul (<0.5s saat shimmer). Urutan wajib: (1) `WaitUtil.waitForScreen([PnlHomeScreen], 20)`, (2) tunggu data riil (`TxtCardNumber`/`TxtGreeting`), (3) jeda stabilisasi singkat (`Mobile.delay(2..3)`). |
| **Rule 60** | **Anti-Legacy DOM/XPath Crawling** | Dilarang memakai `/../..`, `/parent::*`, `/following-sibling::*`, `/ancestor::*`, `com.horcrux.svg.SvgView`, atau asumsi `ViewGroup`/`TextView[1]` di KMP. Utamakan `findTestObject(...)`; fallback hanya predicate `@resource-id`. |
| **Rule 61** | **Junior-Friendly Explicit Child TC** | Dilarang membuat Child TC berupa 1-baris black-box wrapper. Langkah inti (`findTestObject`, `tap`, `setText`, `hideKeyboard`, `takeScreenshot`) wajib eksplisit dan berurutan. Pisahkan subfolder `Positive/` dan `Negative/`. |
| **Rule 62** | **100% English Identifiers & Package Boundary** | Class, method, konstanta, dan variabel wajib English bersih. `Keywords/screens/*Screen.groovy` khusus aksi UI per-layar (`100% findTestObject`); `Keywords/helpers/*Helper.groovy` khusus utilitas lintas-modul. |
| **Rule 63** | **Multi-Surface Login & Keyboard Guard** | Login muncul via 3 permukaan: Cold Launch (`lock_screen`), Guest Home (`home_login_button`), atau Modal Sheet (`shell_modal_sheet` + `lock_password_input` tanpa `lock_screen`). Saat keyboard terbuka, `lock_register_button` tersembunyi — wajib `hideKeyboard` sebelum mencarinya. |
| **Rule 64** | **Compose `*_error`, Timing & Android 14+ Overlays** | Node `*_error` berupa `android.view.View` (`text=""`) pembungkus `TextView` anak → baca via `MobileElementUtil.safeGetText(...)`. Validasi awal terjadi **On-Submit**, lalu **Real-Time Re-Validation**. Tangani overlay opsional Android 14+ (`com.google.android.permissioncontroller` dengan curly apostrophe `Don’t allow`, `intentresolver`, `autofill_save_no`) dan universal alert (`*[ends-with(@resource-id, '_alert_message')]`). |
| **Rule 65** | **Per-Screen Numbered OR (Anti-Flat-Dump)** | Dilarang menumpuk puluhan `.rs` dari banyak layar dalam 1 folder flat. Pecah urut per-layar (`01. ...`, `02. ...`, `03. ...`) lengkap dengan `.meta`, pindahkan via `git mv` tanpa mengubah `<locator>`. |
| **Rule 66** | **Anti-Over-Clever Groovy di Child TC** | Dilarang memakai inline closure kompleks, spread-dot (`*.trim()`), atau chaining `.findAll { ... } as String[]` di Child TC. Gunakan `VerificationHelper.verificationValidationTextAny(...)` yang lugas. |
| **Rule 67** | **Infinite Loading Watchdog & Cold-Restart** | Jika `loading_overlay`, `pin_processing`, shimmer, atau `login_timeout_sheet` macet melewati batas (**15–20s** navigasi/katalog; **45–60s** transaksi uji timeout), wajib **force-stop** app → **cold-launch** → **re-login** (Rule 63) → tunggu `home_screen` stabil (Rule 59) → lanjutkan checkpoint (**maks 2x** retry). |
| **Rule 68** | **Deterministic Live Spying State Machine (`S0`–`S7`)** | Dilarang aksi UI buta tanpa verifikasi state. Wajib jalankan gerbang tertutup `S0`–`S7` di bawah ini. |

### Protokol Keyboard Bersih (Anti-Double-Back Invariant)
- Dilarang chaining `Mobile.hideKeyboard()` lalu langsung `Mobile.pressBack()` (jika keyboard sudah turun, `pressBack()` melempar runner mundur ke layar sebelumnya).
- Standar baku pasca-setter: `Mobile.hideKeyboard(FailureHandling.OPTIONAL)` + `Mobile.delay(1)` → ambil screenshot evidence (viewport bersih tanpa keyboard) → tap tombol target.
- Pada modal input React Native (Revamp lama), gunakan `Mobile.pressKeyCode('ENTER', FailureHandling.OPTIONAL)` agar event commit form terpicu sebelum tap tombol `Ok`.

---

## 4. State Machine Live Spying Deterministik (Rule 68: `S0`–`S7`)

```text
[S0: Pre-Flight & Focus] -> [S1: Clean Screen Entry] --(Hang)--> [S7: Rule 67 Cold-Restart]
         |
         v
[S2: Atomic Clear + Verify-After-Clear]  (assert digits(field.text) == "" ; fallback: re-enter screen)
         |
         v
[S3: Input Injection + Verify-After-Input] (assert digits(field.text) == target BEFORE hide keyboard)
         |
         v
[S4: Deterministic Keyboard Dismiss] (cek dumpsys input_method mInputShown=true -> ESCAPE/header tap)
         |
         v
[S5: Anti-Stale-UI & Transition Proof] (assert field == target AND katalog/operator/error baru segar)
         |
         v
[S6: No-Progress Circuit Breaker] (jika fingerprint state tak berubah maks 2x -> ABORT & log diff)
```

### Guard Keamanan Live Spying Perbankan
1. **Verify-After-Clear**: Jangan pakai loop `while` shell ad-hoc tanpa cek hasil. Kirim satu panggilan `adb shell input keyevent 123 67 67 ...` lalu dump XML untuk memastikan field kosong; jika gagal, keluar-masuk layar agar Compose me-mount state bersih.
2. **Anti-Lockout M-PIN Mutlak**: Uji salah M-PIN (`999999`) **maksimal 1x** lalu segera tutup sheet (`pin_key_cancel` / `confirm_pin_close_button`). Dilarang memicu 3x lockout!
3. **Zero Paid Transaction Waste**: Saat sekadar memetakan katalog/validasi client, hentikan di `seluler_screen` atau `confirm_screen` tanpa mengirim M-PIN.

---

## 5. Flow Transaksi KMP Terverifikasi & Katalog Response Code (`[RC]`)

### A. Flow Universal Top Up Paket Data (`seluler_screen`, Lintas Operator)
1. `home_menu_09_button` (`Topup & Bayar`) → `topup_bayar_topup_paket_data` → `seluler_screen` (`seluler_tab_1`, cek sumber dana).
2. Input nomor ke `seluler_number_input` *(format LPZ 13-digit `008...` → hapus satu `0` di depan)* → tutup keyboard (anti double-back) → `seluler_operator_name` & katalog dinamis muncul di layar yang sama.
3. Pilih `seluler_tile_<N>` → `seluler_continue_button` → `confirm_screen` → `confirm_continue_button` (tangani `repeat_warning_proceed_button` bila muncul) → `confirm_pin_sheet` (keypad acak).
4. **Permukaan Akhir**:
   - **Positive**: `receipt_screen` (`receipt_close_button` → `home_screen`).
   - **Negative / Host RC**: `confirm_alert_message` (`confirm_alert_ok_button` → `home_screen`).
   - **Timeout 30–60s**: `confirm_status_unknown_sheet` (**DILARANG retry otomatis**; cek status transaksi di **Inbox** & **Mutasi**).

### B. Flow Top Up E-Wallet (3 Layar Terpisah — Rule 65)
- `01. Pilih Provider dan Nomor/` (`ewallet_screen`, `ewallet_number_error`) + `Provider/` (`BtnProviderShopeePay`, `Ovo`, `GoPay`, `Dana`, `LinkAja`, `MMoney`).
- `02. Pilih Nominal/` (`ewallet_amount_screen`, `BtnAmountTile0..6`, `BtnAmountCustomInputTap`).
- `03. Sheet Nominal Kustom/` (`ewallet_amount_sheet`, `ewallet_amount_sheet_error`).

### C. Pola Locator Alert Response Code (`Object Repository/Alert/Response Code/`)
- Pola umum lintas modul: `//*[@resource-id="confirm_alert_message" and contains(@text, "[<RC>]")]` + tombol `Alert/_Alert Object/BtnConfirmAlertOk.rs`.
- RC terverifikasi: `[RCM05]` (Undefined Error), `[RCM06]` (Reversal Reject), `[RCM40]` (Transaksi Tidak Dikenal), `[RCM50]` (Denom Tidak Sesuai), `[RCM68]` & `[RC99]` (Transaksi Timeout).

---

## 6. Standar Penamaan Datacore SSOT KMP & Sanitasi Nama File

- **Master Test Case ID KMP**: `TC{P/N}-{D}-{M}-{S}-{SS}-{NormalizedScenarioName}` (contoh: `TCP-1-1-1-1-KirimViaWhatsApp`; pertahankan `-0-` bila `Sub-Sub ID` bernilai `0`).
- **Test Suite ID KMP**: `TS-{DD}-{MM}-{SS} - {DashMap} - {MainModule} - {SubModule}` (zero-padded 2 digit).
- **Anti-Mass-Rename**: Biarkan Test Case / Test Suite eksisting utuh kecuali diminta eksplisit.
- **Sanitasi Simbol Ilegal OS/Katalon**: Hapus/ubah karakter `/`, `:`, `<`, `>`, `'`, `(`, `)`, `&`, `=`, `.` ke `[A-Za-z0-9_-]` PascalCase saat membuat file `.tc`/`.groovy`/`.ts`/folder bukti, dan simpan ID mentah sheet di `<description>` `.tc`. Selalu cek bentrok nama file sebelum menulis agar tidak menimpa test case lain.

