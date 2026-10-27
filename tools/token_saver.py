#!/usr/bin/env python3
"""
Yerly-Playground — Interactive Token Saver Mode Selector 🌸✨
"""

import sys

MODES = [
    ("1", "Bank Mega M-Smile QA Automation (Katalon Studio & Mobile) [Recommended]"),
    ("2", "QA Manual & UAT Test Case Design (Excel 4-Sheet & Traceability)"),
    ("3", "Root Cause Analysis & Locator Debugging"),
    ("4", "Core Banking AS400 & Backoffice Web"),
    ("5", "QA Reporting, Sign-Off & Documentation"),
    ("6", "Ngobrol Santai / Rehat Feminin (Nol Token Teknis)")
]

def main():
    print("\n🌸 ======================================================== 🌸")
    print("   YERLY-PLAYGROUND — MODE SELEKSI TUGAS & PENGHEMAT TOKEN  ")
    print("🌸 ======================================================== 🌸\n")
    print("Pilih mode sesi yang ingin Mbak Yerly jalankan hari ini:\n")
    for key, desc in MODES:
        print(f"  [{key}] {desc}")
    print("\n------------------------------------------------------------")
    
    choice = input("Pilihan Mbak Yerly (1-6) [default: 1]: ").strip() or "1"
    
    selected = next((desc for key, desc in MODES if key == choice), MODES[0][1])
    print(f"\n✨ Mode aktif: {selected}")
    print("🌸 Playbook relevan telah disiapkan. Selamat bekerja cerdas, Mbak Yerly!\n")

if __name__ == "__main__":
    main()
