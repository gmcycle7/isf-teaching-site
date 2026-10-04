#!/usr/bin/env python3
"""Parse the YAML front matter of every docs page (zh + EN). Exit 1 if any page fails.

An unquoted value containing ': ' has broken the EN build before, so this runs in CI.
Usage: python3 scripts/check_front_matter.py
"""
import glob
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS = ["docs/**/*.md", "docs/**/*.mdx",
            "i18n/en/docusaurus-plugin-content-docs/current/**/*.md",
            "i18n/en/docusaurus-plugin-content-docs/current/**/*.mdx"]

bad = 0
total = 0
for pat in PATTERNS:
    for path in sorted(glob.glob(os.path.join(ROOT, pat), recursive=True)):
        total += 1
        text = open(path, encoding="utf-8").read()
        if not text.startswith("---"):
            continue
        try:
            meta = yaml.safe_load(text.split("---")[1])
            if not isinstance(meta, dict) or "title" not in meta:
                raise ValueError("front matter has no title")
        except Exception as exc:  # noqa: BLE001 - report every failure
            bad += 1
            print("FAIL", os.path.relpath(path, ROOT), "-", str(exc).splitlines()[0][:100])
print(f"front matter: {total} pages checked, {bad} failed")
sys.exit(1 if bad else 0)
