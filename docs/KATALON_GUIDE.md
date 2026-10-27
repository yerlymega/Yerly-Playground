# 💻 Katalon Studio Enterprise Standards — Yerly-Playground 🌸

Pedoman teknis koding Groovy, arsitektur Object Repository, dan integritas runtime Katalon Studio untuk Bank Mega Revamp M-Smile.

---

## 1. Konvensi Sintaks Groovy & AST Integrity

### A. Keseimbangan Kurung Kurawal (Brace Balance Depth)
Setiap skrip Groovy wajib memiliki kedalaman kurung kurawal yang seimbang sempurna (`brace depth == 0` dari baris awal hingga akhir). Kegagalan menutup kurung kurawal akan memicu crash startup parser Katalon.

### B. Larangan Anonymous Action Closure (Manual Mode AST Invariant)
Dilarang menggunakan *raw anonymous closure* tanpa parameter (`{ -> ... }`) sebagai parameter callback di Map `callTestCase`. Hal ini akan menyebabkan GUI Manual Mode Katalon Studio mengalami crash fatal:  
`NullPointerException: Cannot read the array length because "this.parameters" is null`.

### C. Deklarasi Binding Variabel Resmi
Untuk membaca variabel binding secara aman di Master maupun Screen Flow, gunakan helper closure berparameter resmi:
```groovy
def getVar = { String name, Object defaultValue = '' ->
    binding.hasVariable(name) && binding.getVariable(name) != null ? binding.getVariable(name) : defaultValue
}
```

---

## 2. API SSOT VerificationHelper & KeywordUtil

### A. Method Resmi KeywordUtil
Hanya gunakan method bawaan resmi Katalon Studio:
- `KeywordUtil.logInfo(String message)`
- `KeywordUtil.markWarning(String message)`
- `KeywordUtil.markFailed(String message)`
- `KeywordUtil.markPassed(String message)`
- `KeywordUtil.markError(String message)`

> [!WARNING]
> DILARANG memanggil method fiktif seperti `KeywordUtil.logWarn(...)` atau `KeywordUtil.logWarning(...)` karena akan memicu runtime `MissingMethodException`.

### B. Method Resmi VerificationHelper
- **Teks / String**:  
  `helpers.VerificationHelper.verificationValidationText(String fieldName, Object expected, Object actual)`  
  `helpers.VerificationHelper.verificationMatch(String fieldName, Object expected, Object actual)`
- **Nilai Numerik / Saldo**:  
  `helpers.VerificationHelper.verificationNumeric(String fieldName, Object expected, Object actual)`  
  *(Menerima tipe `long` maupun String berformat mata uang seperti `'Rp. 250.000'`).*
- **Nomor Rekening / Format Masking**:  
  `helpers.VerificationHelper.verificationMaskedNumber(String fieldName, Object expected, Object actual)`

---

## 3. Standardisasi Object Repository (`.rs`)

### A. Strategi Accessibility ID untuk Tombol & Dialog
Untuk elemen tombol aksi, dialog konfirmasi, atau container `android.view.ViewGroup` yang memiliki `content-desc` (misal: `OK`, `Lanjut`, `Batal`, `Tutup`), ubah properti XML `.rs` menjadi:
```xml
<selectorMethod>ACCESSIBILITY</selectorMethod>
<locatorStrategy>ACCESSIBILITY</locatorStrategy>
<locator>Nama Content Desc</locator>
```

### B. Strict Anti-Tampering
Dilarang mengubah properti atau menghapus file `.rs` hasil tangkapan spy Rio/Yerly tanpa konfirmasi tertulis.

---
*Katalon Standards Guide — Yerly-Playground 🌸*
