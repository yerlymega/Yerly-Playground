import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import core.AppManager
import utils.ResetToDashboardUtil

/**
 * ============================================================================
 * MASTER TEST CASE — CALLING-ONLY ORCHESTRATOR
 * Scenario : ${SCENARIO_NAME}
 * Standard : Datacore SSOT Bank Mega
 * Author   : Mbak Yerly & Yerly (Yer 🌸✨)
 * ============================================================================
 */

// 1. Launch & Connect Appium Session
AppManager.launchMainApp()

// 2. Canonical Binding Helper (Manual Mode GUI Safe)
def getVar = { String name, Object defaultValue = '' ->
    binding.hasVariable(name) && binding.getVariable(name) != null ? binding.getVariable(name) : defaultValue
}

// 3. Extract Test Data
String scenarioId = getVar('SCENARIO_ID', 'TC-P01')
String nomorRekening = getVar('REKENING_TUJUAN', '')
String nominalTransfer = getVar('NOMINAL', '50000')

try {
    // 4. Calling-Only Sequence to Screen Flows
    Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/Dashboard/Navigasi Ke Fitur'), [:])
    Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/Transfer/Form Input'), [
        'REKENING_TUJUAN': nomorRekening,
        'NOMINAL': nominalTransfer
    ])
    Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/MPIN/Input MPIN'), [:])
    Mobile.callTestCase(findTestCase('Test Cases/Screen Flow/Transfer/Verifikasi Sukses'), [:])

} finally {
    // 5. Mandatory Safe Teardown
    ResetToDashboardUtil.resetToDashboard()
}
