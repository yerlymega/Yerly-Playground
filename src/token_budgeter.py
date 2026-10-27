#!/usr/bin/env python3
"""
Yerly-Playground — Token Budgeting & Context Monitor Utility 🌸✨
Menghitung estimasi token berkas-berkas di workspace untuk menjaga efisiensi konteks.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def estimate_tokens(text: str) -> int:
    """Estimasi kasar 1 token ~ 4 karakter."""
    return len(text) // 4

def analyze_workspace():
    print("🌸 ======================================================= 🌸")
    print("   YERLY-PLAYGROUND — TOKEN BUDGET & CONTEXT MONITOR       ")
    print("🌸 ======================================================= 🌸\n")
    
    categories = {
        "Core Documents": list((BASE_DIR / "core").glob("*.md")),
        "Core Engines": list((BASE_DIR / "core" / "engines").glob("*.md")),
        "Documentation": list((BASE_DIR / "docs").glob("*.md")),
        "Playbooks": list((BASE_DIR / "playbooks").glob("*.md")),
        "Characters & Guides": [BASE_DIR / "characters" / "yerly.md", BASE_DIR / "README.md", BASE_DIR / "AGENTS.md"]
    }

    total_tokens = 0

    for cat_name, file_list in categories.items():
        cat_tokens = 0
        print(f"📁 [{cat_name}]")
        for fpath in file_list:
            if fpath.exists() and fpath.is_file():
                try:
                    content = fpath.read_text(encoding="utf-8")
                    tokens = estimate_tokens(content)
                    cat_tokens += tokens
                    print(f"   • {fpath.name:<30} : ~{tokens:>5} tokens")
                except Exception as e:
                    print(f"   • {fpath.name:<30} : Error ({e})")
        print(f"   ↳ Subtotal: ~{cat_tokens} tokens\n")
        total_tokens += cat_tokens

    print("-----------------------------------------------------------")
    print(f"🌸 TOTAL KONTEN KANONIKAL: ~{total_tokens} tokens")
    print("💡 Rekomendasi Yer: Gunakan mode task selektif untuk menghemat!")
    print("🌸 ======================================================= 🌸")

if __name__ == "__main__":
    analyze_workspace()
