# 🔬 Playbook: Debugging & Root Cause Analysis Forensics — Yerly-Playground 🌸

Panduan ilmiah penanganan kegagalan eksekusi skrip (*test failure triage*), broken locators, dan stack trace error.

---

## 1. Matriks Triage Kegagalan Katalon

| Gejala Error | Akar Masalah | Solusi Bedah |
|---|---|---|
| `StepFailedException: Object not found` | 1. Elemen belum selesai render.<br>2. ID / text berubah di APK baru.<br>3. Terhalang keyboard. | 1. Gunakan `WaitUtil.waitForElementPresent`.<br>2. Cek class restriction di `.rs` (gunakan union XPath).<br>3. Panggil `Mobile.hideKeyboard()`. |
| `MissingMethodException: No signature of method: KeywordUtil.logWarn` | Katalon tidak memiliki method `logWarn` | Ganti dengan `KeywordUtil.markWarning(...)` atau `KeywordUtil.logInfo(...)`. |
| `Apparent variable '...' was found in a static scope` | Import class belum dideklarasikan di file Keyword | Tambahkan `import <package>.<Class>` secara eksplisit di bagian atas file. |
| `Layar kembali ke dashboard sebelumnya` | Pemanggilan destruktif `pressBack()` pada modal | Ganti dengan tapping tombol tutup atau tombol icon [X] eksplisit. |

---
*Debugging Forensics Playbook — Yerly-Playground 🌸*
