# 🎯 QA Engine: Two-Tier Katalon & UAT Design Orchestration 🌸

Modul ini menegakkan seluruh standar teknis pengujian mutu perangkat lunak pada **Yerly-Playground**.

---

## 1. Aturan Validasi Katalon Groovy

1. **Brace Balance Guard**:
   - Seluruh baris skrip Groovy wajib tervalidasi memiliki kedalaman kurung kurawal seimbang (`depth == 0`).
2. **Manual Mode GUI Safety**:
   - Dilarang menyematkan anonymous action closure (`{ -> ... }`) di dalam Map parameter `callTestCase`.
   - Gunakan binding closure standar:
     ```groovy
     def getVar = { String name, Object defaultValue = '' ->
         binding.hasVariable(name) && binding.getVariable(name) != null ? binding.getVariable(name) : defaultValue
     }
     ```
3. **KeywordUtil Method Check**:
   - Hanya panggil `KeywordUtil.logInfo`, `markWarning`, `markFailed`, `markPassed`, `markError`.
   - Dilarang keras menggunakan `logWarn` atau `logWarning`.
4. **Recovery Non-Destruktif**:
   - Dilarang menggunakan `Mobile.pressBack()` pada pemulihan modal dialog atau form yang gagal render.

---

## 2. Standar UAT Excel 4-Sheet Bank Mega
- **Sheet 1 (Cover)**: Pengesahan resmi tim QA, PM, dan Business Owner.
- **Sheet 2 (Lembar Kontrol)**: Version history revisi dokumen.
- **Sheet 3 (Traceability)**: Pemetaan ID Acceptance Criteria ke Skenario UAT.
- **Sheet 4 (Script Detail)**: Langkah aksi, data uji, dan ekspektasi hasil.
- **Zero PII**: Seluruh nomor kartu kredit, PIN, password, dan saldo riil wajib disanitasi.

---
*QA Engine — Yerly-Playground 🌸*
