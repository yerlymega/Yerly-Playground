# 📐 SRS.md — Software Requirements Specification (Yerly-Playground) 🌸

**Specification ID**: `SRS-YERLY-1.0`  
**Standard**: ISO/IEC/IEEE 29148:2018 Systems and Software Engineering  
**Scope**: Workspace Architecture, Runtime Constraints, and Verification Gates  

---

## 1. External Interface Requirements
- **CLI & IDE Interfaces**: Google Antigravity, Claude Code, Gemini CLI, Terminal Zsh/Bash, PowerShell.
- **Git Repositories**:
  - Remote: `https://github.com/yerlymega/Yerly-Playground.git`
  - Target Project: `KMP-Revamp_M-Smile` & `Revamp_M-Smile`.

---

## 2. Non-Functional & Quality Requirements
1. **Performance & Token Budgeting**:
   - Initial context payload saat sesi santai harus berada di bawah 20.000 tokens.
   - Pemuatan playbook teknis harus dibatasi hanya pada file yang dipilih saat `ask_question`.
2. **Security & Privacy (Zero PII)**:
   - Dilarang menyimpan atau mencetak credential, nomor PIN asli, password login, nomor kartu kredit/debit lengkap, atau saldo riil nasabah Bank Mega ke dalam file git.
3. **Cross-Platform Compatibility**:
   - Skrip utilitas harus dapat dieksekusi tanpa modifikasi kode di macOS Darwin, Linux Ubuntu, dan Windows NT.
4. **Code Safety & AST Integrity**:
   - Skrip Groovy yang dihasilkan wajib lolos verifikasi kurung kurawal (`brace depth == 0`).
   - Dilarang menggunakan raw anonymous action closure (`{ -> ... }`) di Map parameter test case.

---
*Software Requirements Specification — Yerly-Playground 🌸*
