# 🏷️ Playbook: Datacore SSOT Standard & Naming Conventions — Yerly-Playground 🌸

Pedoman standardisasi penamaan skenario dan entitas pengujian merujuk pada Single Source of Truth (SSOT) Google Spreadsheet Datacore Bank Mega.

---

## 1. Rumus Penamaan Kanonikal Master TC

$$\text{TC-}\{\text{P/N}\}\{\text{No}\}\_\{\text{MAINMOD}\}\_\{\text{SUBMOD}\}\_\{\text{SUBSUBMOD}\}\_\{\text{ScenarioName}\}$$

### Contoh Baku:
- `TC-P01_TRANSFER_BIFAST_INQUIRY_NominalNormal`
- `TC-N12_TRANSFER_ONLINE_INPUTNOMINAL_MelebihiLimitHarian`
- `TC-P89_ZAKU_ZAKUARISAN_KLIKICONPENGZAKU_GantiSumberDanaAutodebet-Normal`

---

## 2. Invarian Truncation Immunity

Token resmi dari Datacore yang terpotong (misal: `PULSAREGULETELK`, `LISTRI`, `PINJAM`) **DILARANG** diubah atau dikoreksi ejaannya secara sepihak. Token tersebut adalah identifier baku sistem perbankan.

---
*Datacore SSOT Playbook — Yerly-Playground 🌸*
