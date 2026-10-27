# ⚙️ TECH.md — Master Technical Architecture & Stack Specification v1.0 🌸

**Document Identifier**: `TECH-YERLY-2026-V1.0`  
**Status**: `MANDATORY & ACTIVE`  
**Architecture Pattern**: Modular Engine DAG · Dynamic Context Router · Enterprise Banking Core · Cross-Platform Local-First  
**Repository**: [`Yerly-Playground`](https://github.com/yerlymega/Yerly-Playground)  
**Release Date**: 2026-10-27  

---

## 1. 🏛️ System Architecture Topology

```mermaid
graph TD
    User(["Mbak Yerly / Channels: Antigravity IDE, Claude, Gemini, Terminal"]) --> Router["Intent & Context Router"]
    
    subgraph ENGINE_DAG["🌸 Yerly Modular Engine DAG"]
        Router --> EmoEng["1. Emotion & Empathy Engine (Mature 27 y.o. Feminine)"]
        Router --> TokenEng["2. Token Saver & Budgeting Engine (Selective Loader)"]
        Router --> QAEng["3. Enterprise QA & Two-Tier Katalon Orchestrator"]
        Router --> CoreBankEng["4. AS400 Core Banking & Host Terminal 5250"]
        Router --> SecretEng["5. Mastermind Resolver (Mucho R Easter Egg)"]
    end
    
    subgraph ARTIFACTS["📑 Outputs & Test Deliverables"]
        QAEng --> KatalonScript["Katalon Calling-Only Master & Reusable Screen Flow"]
        QAEng --> ExcelUAT["4-Sheet Excel UAT Test Script & Sign-Off .docx"]
        QAEng --> EvidencePack["Sequential Screenshots (01.png - NN.png)"]
    end
    
    subgraph SYNC["🔄 Continuous Synchronization"]
        QAEng --> DailyNotes["memory/daily/YYYY-MM-DD.md"]
        QAEng --> GitSync["tools/learn.sh -> Remote GitHub yerlymega"]
    end
```

---

## 2. 🧩 Core Engine Modules

1. **`core/engines/emotion_engine.md`**: Mengatur adaptasi nada bicara feminin yang santun, hangat, cerdas, dan suportif.
2. **`core/engines/token_engine.md`**: Melakukan kalkulasi konsumsi token, penentuan mode tugas via `ask_question`, dan lazy-loading berkas playbook.
3. **`core/engines/qa_engine.md`**: Penegak aturan calling-only Master Test Case, validasi kurung kurawal Groovy AST, dan integrasi UAT.

---

## 3. 🌐 Universal Cross-Platform Standard (macOS, Linux, Windows)

- **Path Resolving**: Selalu menggunakan separator netral (`os.path.join`, `pathlib.Path`, `path.join`, atau `File.separator`).
- **Line Endings**: Normalisasi LF di Git melalui `.gitattributes` (`* text=auto eol=lf`).
- **Dual Launcher**: Sediakan skrip `.sh` untuk Unix dan `.bat`/`.ps1` untuk Windows.

---
*Technical Architecture Specification — Yerly-Playground 🌸*
