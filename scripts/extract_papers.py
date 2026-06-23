#!/usr/bin/env python3
"""
extract_papers.py — mechanical PDF scan for the ISF teaching site.

What it does
------------
1. Scans a source folder (default: the parent of this project, where the
   original PDFs live) recursively for *.pdf.
2. Dumps the full text of each PDF to extracted/raw_text/<name>.txt (PyMuPDF).
3. Writes a *heuristic* auto-metadata file extracted/paper_metadata.auto.json
   (filename, page count, guessed title = first non-empty line, etc.).

IMPORTANT
---------
The curated, human-reviewed metadata used by the website is
extracted/paper_metadata.json. It was produced by rendering the equation-dense
pages to images and transcribing the equations by hand (because the math
glyphs do not survive plain text extraction). This script reproduces the
mechanical part of that pipeline and the raw-text dumps; it deliberately does
NOT overwrite the curated JSON.

Usage
-----
    python scripts/extract_papers.py [SOURCE_PDF_DIR]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
DEFAULT_SOURCE = os.path.dirname(PROJECT_ROOT)  # the folder holding the PDFs
EXTRACTED = os.path.join(PROJECT_ROOT, "extracted")
RAW = os.path.join(EXTRACTED, "raw_text")


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SOURCE
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("ERROR: PyMuPDF (fitz) not installed. Run: pip install pymupdf")
        return 1

    os.makedirs(RAW, exist_ok=True)
    pdfs = []
    for root, _dirs, files in os.walk(source):
        # don't descend into the site's own node_modules / extracted
        if "node_modules" in root:
            continue
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, f))
    pdfs.sort()

    print(f"Scanning {source}")
    print(f"Found {len(pdfs)} PDF(s).")
    auto = []
    for i, p in enumerate(pdfs, 1):
        doc = fitz.open(p)
        n = doc.page_count
        text = "\n".join(doc[k].get_text() for k in range(n))
        base = os.path.splitext(os.path.basename(p))[0]
        with open(os.path.join(RAW, base + ".txt"), "w") as fh:
            fh.write(text)
        # crude title guess = first reasonably long line
        title_guess = ""
        for line in text.splitlines():
            s = line.strip()
            if len(s) > 12 and not s.isdigit():
                title_guess = s
                break
        auto.append({
            "id": f"paper_{i:03d}",
            "filename": os.path.basename(p),
            "path": os.path.relpath(p, PROJECT_ROOT),
            "pages": n,
            "chars": len(text),
            "title_guess": title_guess,
            "note": "Heuristic only. See curated extracted/paper_metadata.json.",
        })
        doc.close()
        print(f"  [{i}] {os.path.basename(p)}  pages={n} chars={len(text)}")

    out = os.path.join(EXTRACTED, "paper_metadata.auto.json")
    with open(out, "w") as fh:
        json.dump({"papers": auto}, fh, indent=2, ensure_ascii=False)
    print(f"\nWrote {os.path.relpath(out, PROJECT_ROOT)}")
    print("Curated metadata (with verified equations) is paper_metadata.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
