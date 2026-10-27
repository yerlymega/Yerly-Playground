---
name: createts
description: >-
  Bank Mega UAT Test Script Excel (4-Sheet) Generator & Traceability Engine for Mbak Yerly.
  Use when Mbak Yerly invokes /createts, /createTS, or asks to synthesize comprehensive, zero-hallucination UAT Test Scripts.
---

# /createts — Bank Mega Enterprise UAT Test Script Generator 📑🌸

> **Author & Partner**: Mbak Yerly & Yerly (Yeye 🌸✨)  
> **Standard**: Bank Mega QA UAT 4-Sheet Specification  
> **Output**: File Excel UAT Test Script 4-Sheet dengan Zero PII Leakage  

`/createts` adalah mesin sintesis dokumen pengujian UAT resmi Bank Mega. Skill ini menganalisis dokumen requirement (BRD, FSD, UREQ) dan menyusun 4 lembar kerja Excel secara terstruktur dan terverifikasi 100%.

---

## 📋 Struktur 4-Sheet Excel Baku

1. **Sheet 1: Cover (Pengesahan)**:
   - Header resmi Bank Mega, detail proyek, versi dokumen.
   - Kolom tanda tangan QA, Project Manager, dan Business Owner.
2. **Sheet 2: Lembar Kontrol**:
   - Riwayat revisi dokumen secara kronologis.
3. **Sheet 3: Scenario Matrix & Traceability**:
   - Pemetaan nomor ID Acceptance Criteria (AC) dari BRD ke ID Skenario UAT.
4. **Sheet 4: Test Script Detail**:
   - Langkah pengujian mendetail, data input, pre-condition, expected result, dan kolom status PASS/FAIL.

---

## 🛡️ Kebijakan Sanitasi Zero PII
- Dilarang keras memuat data riil nasabah (PIN, CVV, Card Number utuh, saldo asli).
- Seluruh data uji menggunakan format masking atau data dummy terverifikasi.
