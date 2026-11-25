# 🛡️ Playbook: Locara by Qureon — Autonomous Mobile Locator Healing — Yerly-Playground 🌸

> **Document ID**: `KB-YERLY-LOCARA-001`  
> **Status**: `CANONICAL & ACTIVE (P1 HIGH)`  
> **Reference Release**: Locara Core `v1.16.1` (`Qureon/Locara`)  
> **Companion**: [`kmp-revamp-m-smile.md`](kmp-revamp-m-smile.md) · [`qa-katalon-mobile.md`](qa-katalon-mobile.md)

---

## 1. Mengapa Locara by Qureon?

Pengujian regresi mobile enterprise (M-Smile Revamp & KMP) sering tersandung 3 masalah utama yang tidak tertangani sempurna oleh locator statis atau self-healing eksternal berbasis Docker/PostgreSQL:
1. **Infrastructure Friction**: Server healing eksternal menambah latensi jaringan dan merepotkan runner lokal/offline.
2. **Silent Boolean Failure**: `Mobile.waitForElementPresent()` / `verifyElementVisible()` mengembalikan `false` tanpa melempar exception, sehingga interceptor berbasis exception biasa tidak pernah terpicu.
3. **Copywriting Drift pada Negative Test**: Perubahan kecil teks validasi (misal `"kurang dari 10 digit"` vs `"minimal 10 digit"`) memicu false-red meski intent bisnis sama.

**Locara** berjalan **in-process di dalam JVM Katalon/Appium** lewat satu file `.jar` ringan (< 250 KB): `0 ms` overhead saat locator asli valid, rata-rata `< 35 ms` saat melakukan healing.

---

## 2. Fitur & Komponen Arsitektur Utama (`v1.16.1`)

1. **Native Hook & Probing Airbag (`LocaraHook` + `LocaraKeywords`)**:
   - Mencegat keyword aksi (`tap`, `setText`, `getText`, `verifyElementText`) dan probe kehadiran (`verifyElementPresent`, serta `waitForElementPresent` secara opt-in).
   - Standar variabel penamaan resmi hanya **`ENABLE_LOCARA`** / **`ENABLE_QUREON`** (seluruh nama legacy ZeroHealing sudah dipensiunkan).
2. **2-Tier Semantic Intent Matcher (`LocaraIntentMatcher`)**:
   - Mengelompokkan pesan error validasi form perbankan ke klaster semantik (`PHONE_LENGTH`, `PHONE_PREFIX`, `INSUFFICIENT_BALANCE`, `LIMIT_EXCEEDED`, `INVALID_MPIN`).
   - Menggabungkan *Keyword Coverage Ratio* + *Jaro-Winkler / Token Overlap* dengan ambang skor $\ge 0.70$.
3. **Universal 2D Spatial Alignment & Field Relationship Parser**:
   - **Left-to-Right Row Alignment**: memasangkan label di kiri dengan nilai di kanan pada baris yang sama (irisan vertikal $\ge 40\%$).
   - **Top-to-Bottom Label Pairing**: memasangkan label header dengan input/dropdown di bawahnya ($\le 350\text{px}$, irisan horizontal $\ge 30\%$).
   - **Field Relationship Parser**: membedah layar konfirmasi dan struk menjadi pasangan *key-value* terstruktur (`locara inspect-fields --xml <file>`).
4. **Object Repository Sanitizer (`LocaraOrSanitizer`)**:
   - Mendeteksi XPath absolut rapuh (`//hierarchy/android.widget.FrameLayout[1]/...`) dan membantu mengubahnya menjadi XPath relatif yang tangguh:
     - Dry-run: `locara sanitize-or --path="Object Repository/"`
     - Fix ber-backup `.bak`: `locara sanitize-or --path="Object Repository/" --fix`
   - **Anti-Tampering**: File `.rs` asli tidak pernah ditimpa diam-diam tanpa izin `--fix` atau mode karantina `.healed.rs`.
5. **Autonomous Overlay & Permission Airbag (`OverlayAirbag`)**:
   - Menangani popup sistem Android 14+ (`com.google.android.permissioncontroller` termasuk normalisasi curly apostrophe `U+2019` pada `"Don’t allow"`, `permission_allow_foreground_only_button`, `permission_deny_and_dont_ask_again_button`), Android `"Open with"` (`com.android.intentresolver`), dan Google Autofill Save (`autofill_save_no`), sembari melindungi tombol `"OK"` pada layar form aktif dengan `EditText`.
6. **Offline Mission Control Dashboard (`100% Zero Outbound Network`)**:
   - Menampilkan metrik healed actions, negative/probe healed, sanitized `.rs`, safety lockouts, serta **Spatial & Form Inspector** tanpa ketergantungan CDN eksternal.

---

## 3. Tri-Target Preset Architecture (`UMUM`, `REVAMP`, `KMP`, `AUTO`)

| Profil Target | Lingkungan | Fokus Heuristik |
|---|---|---|
| **`UMUM`** | Aplikasi Android XML / iOS UIKit umum | Bobot seimbang (Teks 35%, ID 25%, Desc 20%, Class 10%, Proximity 10%) + 2D Spatial Alignment |
| **`REVAMP`** | React Native (`Revamp_M-Smile`) | Pohon `ViewGroup` dalam, missing testID; bobot Teks 55% + Parent Container Ascension |
| **`KMP`** | Kotlin / Compose Multiplatform (`KMP-Revamp_M-Smile`) | `KmpMorphologyResolver` (`<screen>_<element>`, afinitas sufiks `_button`/`_input`/`_error`, scrambled `pin_key_<digit>`); bobot ID 45%, Teks 30%, Desc 15% |
| **`AUTO`** | Default adaptif | `FrameworkDetector` mendeteksi sidik jari pohon UI saat runtime dan memilih profil otomatis |

```groovy
import com.qureon.locara.katalon.Locara

Locara.setProfileAuto()    // Default adaptif
Locara.setProfileKmp()     // Kunci profil M-Smile KMP
Locara.setProfileRevamp()  // Kunci profil Revamp React Native
```

---

## 4. Anti-Double-Scroll Guard & True Ghost Mode

### A. Mencegah Double Scrolling (`ManualScrollGuard` + `ActionWindow`)
- Saat skrip QA sudah melakukan scroll manual (`ScrollUtil.scrollDown()`, `Mobile.swipe`, `Mobile.scrollToText`, atau `mobile: scrollGesture`), `ActionWindow` mengambil snapshot status `ManualScrollGuard` **sebelum** timeout native berjalan agar jendela cooldown (`15000 ms`) tidak hangus oleh waktu tunggu.
- `ScrollRecoveryEngine` membandingkan hash halaman (`seenPageSources`) sebelum & sesudah auto-scroll internal — jika halaman sudah mentok/stagnan, loop langsung berhenti.
- Untuk raw Appium `mobile: scrollGesture`, beri tahu Locara via reflection ghost-mode safe (`Class.forName("com.qureon.locara.katalon.Locara").getMethod("notifyManualScroll").invoke(null)`).

### B. True Ghost Mode & Opt-Out Lokal (`locara.local.properties`)
- **Tanpa JAR di `Drivers/`**: `LocaraHook` otomatis menjadi no-op bersih dan meneruskan panggilan ke `Mobile.*` bawaan tanpa error kompilasi.
- **Opt-Out Perorangan**: Buat berkas gitignored `locara.local.properties` di root proyek dengan isi `locara.enabled=false`.
- **Urutan Prioritas Konfigurasi**: `GlobalVariable` / `-Dlocara.*` → Env `LOCARA_*` → `locara.local.properties` → `locara.properties` → `Include/config/locara.properties`.

```properties
locara.enabled=true
locara.target=AUTO
locara.threshold=0.70
locara.scroll.enabled=true
locara.scroll.max_attempts=2
locara.scroll.manual_guard.enabled=true
locara.scroll.manual_cooldown_ms=15000
locara.hook.heal_wait_present=false
```

---

## 5. Invarian Keamanan Mutlak Locara

1. **Bank Mega Zero-Loss / Financial Commitment Polarity Isolation (`DangerKeywordGuard`)**: Dilarang keras mencocokkan atau mengklik tombol komitmen finansial/destruktif (`Bayar`, `Transfer`, `Checkout`, `Beli`, `Hapus`, `Batalkan`, `Jual Unit`, `Penambahan Unit`) ketika target skrip hanya aksi netral (`OK`, `Lanjut`, `Tutup`, `Simpan`) atau pembacaan teks.
2. **Fail-Closed XML Security**: `PageSourceParser` gagal tertutup (`IllegalStateException`) jika proteksi XXE tidak aktif.
3. **PII Masking di Log**: Nomor rekening & nama pemilik otomatis tersamarkan (`****XXXX`) pada objek hasil resolusi.
4. **Java 17+ Accessible Reflection**: Menggunakan `ReflectiveAccessUtil.findAccessibleMethod` agar seluruh keyword bekerja mulus di Katalon Studio modern tanpa `NoSuchMethodException`.

