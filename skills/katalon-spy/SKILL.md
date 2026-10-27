---
name: katalon-spy
description: >-
  Master Katalon Mobile Automation UI Spying, Reconnaissance & Form Lifecycle Engine for Mbak Yerly.
  Use when Mbak Yerly invokes /katalon-spy, /spy, or asks to spy mobile UI elements and generate atomic screen flows.
---

# /katalon-spy — Mobile Automation Spying & Object Repository Engine 📱🌸

> **Author & Partner**: Mbak Yerly & Yerly (Yeye 🌸✨)  
> **Target**: Bank Mega Revamp M-Smile (Android & iOS)  

Skill ini memandu proses penangkapan elemen antarmuka (*UI spying*), standarisasi selector Object Repository (`.rs`), dan perancangan Reusable Screen Flow di Katalon Studio Enterprise.

---

## ⚡ Standar Standardisasi Elemen

1. **Tombol Aksi & Dialog Container**:
   - Seluruh elemen `android.view.ViewGroup` yang memiliki `content-desc` (seperti `OK`, `Lanjut`, `Batal`, `Tutup`) WAJIB diubah ke:
     - `selectorMethod: ACCESSIBILITY`
     - `locatorStrategy: ACCESSIBILITY`
     - `<locator>Nama Content Desc</locator>`
2. **Pembersihan File Mentah Spying (Strict Raw Spy Purge)**:
   - File tangkapan mentah bawaan Katalon (seperti `android.view.ViewGroup.rs` atau `TextView - Tutup.rs`) wajib dihapus setelah objek distandarisasi ke format baku kanonikal:
     - `00. TextView - <Deskripsi>.rs`
     - `00. ViewGroup - Tombol <Action>.rs`
3. **Naming Subfolder Hierarki**:
   - Elemen menu bottom-sheet dibungkus ke dalam subfolder terisolasi: `00. Menu <Nama Layar>/` untuk menjaga kerapian sidebar tree Katalon.
