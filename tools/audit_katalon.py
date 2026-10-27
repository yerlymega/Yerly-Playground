#!/usr/bin/env python3
"""
Yerly-Playground — Katalon Groovy AST & Code Quality Auditor 🌸✨
Memvalidasi keseimbangan kurung kurawal, larangan anonymous action closure, dan keabsahan method KeywordUtil.
"""

import sys
import re
from pathlib import Path

def audit_groovy_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    issues = []
    
    # 1. Brace Balance Check
    depth = 0
    for idx, char in enumerate(content):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth < 0:
                issues.append(f"Kurung kurawal tutup '}}' berlebih pada karakter ke-{idx}")
    if depth != 0:
        issues.append(f"Kurung kurawal tidak seimbang (Brace Depth = {depth}, wajib 0)")

    # 2. Fake KeywordUtil Check
    if re.search(r'KeywordUtil\s*\.\s*(logWarn|logWarning)\b', content):
        issues.append("Ditemukan pemanggilan method fiktif KeywordUtil.logWarn / logWarning! Ganti dengan markWarning / logInfo.")

    # 3. Anonymous Action Closure Check
    if re.search(r"['\"]action['\"]\s*:\s*\{\s*->", content):
        issues.append("Ditemukan raw anonymous closure {'action': { -> ... }}. Berisiko crash pada Manual Mode GUI!")

    # 4. Destructive pressBack Check
    if re.search(r"Mobile\s*\.\s*pressBack\s*\(", content):
        issues.append("Peringatan: Pemanggilan Mobile.pressBack() terdeteksi. Pastikan bukan pada error modal recovery!")

    return issues

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = Path(target)
    
    files = list(target_path.glob("**/*.groovy")) if target_path.is_dir() else [target_path]
    print(f"🌸 Mengaudit {len(files)} berkas Groovy Katalon...\n")
    
    total_issues = 0
    for f in files:
        issues = audit_groovy_file(f)
        if issues:
            print(f"❌ {f.name}:")
            for iss in issues:
                print(f"   • {iss}")
            total_issues += len(issues)
        else:
            print(f"✅ {f.name}: Clean (0 issues)")
            
    print(f"\n------------------------------------------------------------")
    if total_issues == 0:
        print("🌸 Luar biasa! Seluruh skrip lolos audit integritas Groovy AST! ✨")
    else:
        print(f"⚠️ Ditemukan {total_issues} isu yang perlu diperbaiki.")

if __name__ == "__main__":
    main()
