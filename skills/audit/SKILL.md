---
name: audit
description: >-
  Master Codebase & Repository Redundancy Audit Engine for Mbak Yerly.
  Use when Mbak Yerly invokes /audit, /adt, or asks to audit files or folders for duplicate locators, syntax errors, and orphaned scripts.
---

# /audit — Codebase & Object Repository Audit Engine 🔬🌸

> **Author & Partner**: Mbak Yerly & Yerly (Yeye 🌸✨)  

Skill ini melakukan audit mendalam terhadap basis kode pengujian Katalon Studio untuk mendeteksi:
- **Missing Scripts**: File Test Case `.tc` tanpa folder pasangan di `Scripts/`.
- **Duplicate Locators**: Objek `.rs` dengan selector identik pada path berbeda.
- **Brace Balance Errors**: Ketidakseimbangan kurung kurawal pada file skrip Groovy.
- **Method Deprecated / Fake**: Pemanggilan method terlarang seperti `KeywordUtil.logWarn`.
- **Raw Spy Leftovers**: File sisa tangkapan spy yang belum distandarisasi atau dibersihkan.
