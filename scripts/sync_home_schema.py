#!/usr/bin/env python3
"""Mantém o JSON-LD da home sincronizado com home.json."""

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SCHEMA = ROOT / "home.json"
SCRIPT_RE = re.compile(
    r'<script type="application/ld\+json">.*?</script>', re.S
)


def render(source):
    payload = json.loads(SCHEMA.read_text(encoding="utf-8"))
    compact = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    replacement = f'<script type="application/ld+json">{compact}</script>'
    rendered, count = SCRIPT_RE.subn(replacement, source, count=1)
    if count != 1:
        raise SystemExit("JSON-LD principal não encontrado em index.html")
    return rendered


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = INDEX.read_text(encoding="utf-8")
    rendered = render(source)
    if args.check:
        if rendered != source:
            raise SystemExit("JSON-LD da home desatualizado; rode python3 scripts/sync_home_schema.py")
        print("JSON-LD da home está sincronizado")
        return
    INDEX.write_text(rendered, encoding="utf-8")
    print("JSON-LD da home sincronizado com home.json")


if __name__ == "__main__":
    main()
