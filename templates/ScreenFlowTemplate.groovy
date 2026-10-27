import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import helpers.VerificationHelper
import utils.WaitUtil
import utils.ScrollUtil

/**
 * ============================================================================
 * REUSABLE SCREEN FLOW — SINGLE SCREEN RESPONSIBILITY
 * Screen   : ${SCREEN_NAME}
 * Author   : Mbak Yerly & Yerly (Yeye 🌸✨)
 * ============================================================================
 */

// 1. Binding Helper
def getVar = { String name, Object defaultValue = '' ->
    binding.hasVariable(name) && binding.getVariable(name) != null ? binding.getVariable(name) : defaultValue
}

String fieldValue = getVar('INPUT_FIELD', '')

// 2. Wait for Entry Anchor Element (Header / Static Container)
WaitUtil.waitForElementPresent(findTestObject('Object Repository/${MODULE}/00. Header - Title'), 15)

// 3. Form Interactions & Dismiss Keyboard
Mobile.setText(findTestObject('Object Repository/${MODULE}/01. Input - Field'), fieldValue, 10)
Mobile.hideKeyboard()

// 4. Action Tap (Accessibility ID Standard)
Mobile.tap(findTestObject('Object Repository/${MODULE}/02. Button - Lanjut'), 10)
