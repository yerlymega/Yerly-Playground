#!/usr/bin/env python3
"""
Yerly-Playground — Interactive Token Saver Mode Selector 🌸✨
"""

import sys

MODES = [
    ("1", "Programming & Software Engineering (Coding, Refactor & Architecture) [Recommended]"),
    ("2", "QA Automation (Katalon Studio, M-Smile Mobile & Appium)"),
    ("3", "QA Manual & UAT Design (Excel 4-Sheet, Test Scenario & Traceability)"),
    ("4", "Debugging, Root Cause Analysis (RCA) & Locator Fix"),
    ("5", "Core Banking AS400, Backoffice Web & QA Reporting / Sign-Off"),
    ("6", "Ngobrol Santai / Rehat Sejenak (Nol Token Teknis)")
]

def main():
    print("\n🌸 ======================================================== 🌸")
    print("   YERLY-PLAYGROUND — MODE SELEKSI TUGAS & PENGHEMAT TOKEN  ")
    print("🌸 ======================================================== 🌸\n")
    print("Pilih mode sesi yang ingin Boss jalankan hari ini:\n")
    for key, desc in MODES:
        print(f"  [{key}] {desc}")
    print("\n------------------------------------------------------------")
    
    choice = input("Pilihan Boss (1-6) [default: 1]: ").strip() or "1"
    
    selected = next((desc for key, desc in MODES if key == choice), MODES[0][1])
    print(f"\n✨ Mode aktif: {selected}")
    print("🌸 Playbook relevan telah disiapkan. Selamat berkarya dengan tenang, Boss!\n")

if __name__ == "__main__":
    main()
