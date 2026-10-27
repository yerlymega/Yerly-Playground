# 📱 Playbook: Mobile QA Automation (Katalon Studio) — Yerly-Playground 🌸

Standar operasional penulisan skrip otomasi mobile Bank Mega Revamp M-Smile di Katalon Studio Enterprise.

---

## 1. Arsitektur Dua Pilar (Two-Tier Standard)

### A. Master Test Case Template (`Test Cases/Master/...`)
```groovy
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import core.AppManager
import utils.ResetToDashboardUtil

// 1. Launch / Connect to App
AppManager.launchMainApp()

// 2. Setup Data Binding
def getVar = { String name, Object defaultValue = '' ->
    binding.hasVariable(name) && binding.getVariable(name) != null ? binding.getVariable(name) : defaultValue
}

String scenarioId = getVar('SCENARIO_ID', 'TC-P01')
String nominalTransfer = getVar('NOMINAL', '50000')

try {
    // 3. Calling-Only Sequence ke Screen Flows
    Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/Dashboard/Navigasi Transfer'), [:])
    Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/Transfer/Form Transfer'), ['NOMINAL': nominalTransfer])
    Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/MPIN/Input MPIN'), [:])
    Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/Transfer/Verifikasi Sukses'), [:])
} finally {
    // 4. Safe Teardown Mutlak
    ResetToDashboardUtil.resetToDashboard()
}
```

### B. Screen Flow Template (`Test Cases/Screen Flow/...`)
```groovy
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import helpers.VerificationHelper
import utils.WaitUtil
import utils.ScrollUtil

// Binding closure
def getVar = { String name, Object defaultValue = '' ->
    binding.hasVariable(name) && binding.getVariable(name) != null ? binding.getVariable(name) : defaultValue
}

String nominal = getVar('NOMINAL', '100000')

// Tunggu Entry Anchor Element
WaitUtil.waitForElementPresent(findTestObject('Object Repository/Transfer/00. Header - Transfer'), 15)

// Input Form
Mobile.setText(findTestObject('Object Repository/Transfer/01. Input - Nominal'), nominal, 10)
Mobile.hideKeyboard()

// Tap Lanjut
Mobile.tap(findTestObject('Object Repository/Transfer/02. Button - Lanjut'), 10)
```

---

## 2. Recovery Non-Destruktif Invariant
- **Dilarang memanggil `Mobile.pressBack()`** pada penanganan error modal.
- Jika form gagal submit:
  1. Periksa apakah keyboard masih terbuka $\rightarrow$ panggil `Mobile.hideKeyboard()`.
  2. Periksa apakah ada toast/pop-up error $\rightarrow$ baca teks error via `VerificationHelper`.
  3. Tutup pop-up dengan menekan tombol batal/tutup spesifik.

---
*QA Katalon Mobile Playbook — Yerly-Playground 🌸*
