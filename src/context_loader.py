#!/usr/bin/env python3
"""
Yerly-Playground — Context Loader & Selective Playbook Router 🌸✨
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PLAYBOOKS_DIR = BASE_DIR / "playbooks"

ROUTING_MAP = {
    "1": ["qa-katalon-mobile.md", "bank-mega-m-smile.md", "datacore-ssot.md"],
    "2": ["uat-test-script-design.md", "qa-reporting-and-docs.md"],
    "3": ["debugging-forensics.md", "qa-katalon-mobile.md"],
    "4": ["host-as400-core-banking.md"],
    "5": ["qa-reporting-and-docs.md", "uat-test-script-design.md"],
    "6": []
}

def get_playbooks_for_mode(mode_key: str):
    files = ROUTING_MAP.get(str(mode_key), [])
    loaded_content = []
    for fname in files:
        fpath = PLAYBOOKS_DIR / fname
        if fpath.exists():
            loaded_content.append((fname, fpath.read_text(encoding="utf-8")))
    return loaded_content

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "1"
    results = get_playbooks_for_mode(mode)
    print(f"🌸 Terpilih {len(results)} playbook untuk mode [{mode}]:")
    for name, _ in results:
        print(f"   • {name}")
