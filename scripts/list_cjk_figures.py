#!/usr/bin/env python3
"""List every figure embedded in EN pages whose generating script bakes CJK
text into the image (title/xlabel/ylabel/legend/annotate/suptitle/text), and
report which EN pages embed that image and whether they already carry a
'Translator's note' near the image.

Usage: python3 scripts/list_cjk_figures.py [--missing-only]

This is a read-only inventory tool (part of R11-43's EN-parity gate). It does
not modify any files.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIM_DIR = ROOT / "simulations"
EN_DOCS = ROOT / "i18n/en/docusaurus-plugin-content-docs/current"

CJK_RE = re.compile(r'[一-鿿]')
# matplotlib calls that put text into a rendered figure
PLOT_TEXT_CALL_RE = re.compile(
    r'\.(set_title|set_xlabel|set_ylabel|suptitle|title|xlabel|ylabel|text|annotate|legend|set_label)\s*\('
    r'|label\s*=\s*[rf]*[\'"]'
)
SAVEFIG_RE = re.compile(r'savefig\(\s*(?:\w+\s*,\s*)?[\'"]([^\'"]+)[\'"]')
# Matches a Markdown *image* embed `![alt](/figures/name.png)`, tolerating one
# level of nested [..] inside the alt text (e.g. alt text that itself contains
# a "[P3]" citation marker). Plain links to /figures/... (not prefixed with
# "![") are intentionally NOT matched -- those are prose references, not embeds.
IMG_MD_RE = re.compile(r'!\[(?:[^\[\]]|\[[^\[\]]*\])*\]\(/figures/([^)\s]+)\)')


def script_has_cjk_plot_text(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if PLOT_TEXT_CALL_RE.search(line) and CJK_RE.search(line):
            return True
        # also catch continuation lines assigning label= / lines with f-strings across calls
    return False


def script_figures_with_cjk(path: Path):
    """Return {figure_basename: True/False} — whether the plotting block that
    ends at each savefig() call (i.e. since the previous savefig() call in the
    file) contains a CJK plot-text call. This avoids false positives when a
    script produces several figures and only some of them carry CJK text."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    result = {}
    block_has_cjk = False
    for line in lines:
        if PLOT_TEXT_CALL_RE.search(line) and CJK_RE.search(line):
            block_has_cjk = True
        m = SAVEFIG_RE.search(line)
        if m:
            base = Path(m.group(1)).name
            if not base.lower().endswith((".png", ".svg", ".pdf")):
                base += ".png"
            result[base] = result.get(base, False) or block_has_cjk
            block_has_cjk = False
    return result


def main():
    missing_only = "--missing-only" in sys.argv

    cjk_scripts = []
    for py in sorted(SIM_DIR.glob("*.py")):
        if py.name == "__init__.py":
            continue
        if script_has_cjk_plot_text(py):
            cjk_scripts.append(py)

    # figure basename -> set of scripts that produce it
    fig_to_scripts = {}
    for py in cjk_scripts:
        for base, has_cjk in script_figures_with_cjk(py).items():
            if has_cjk:
                fig_to_scripts.setdefault(base, set()).add(py.name)

    # EN page -> figures it embeds
    en_pages = sorted(EN_DOCS.rglob("*.md")) + sorted(EN_DOCS.rglob("*.mdx"))
    rows = []
    for page in en_pages:
        text = page.read_text(encoding="utf-8", errors="ignore")
        for m in IMG_MD_RE.finditer(text):
            img = m.group(1)
            if img in fig_to_scripts:
                # does this *specific* embed already have a Translator's note
                # (heuristic: a "Translator's note" line appears within 900 chars
                # after THIS match's end, not just anywhere the filename occurs)
                window = text[m.end(): m.end() + 900]
                has_note = "Translator" in window
                rows.append((str(page.relative_to(ROOT)), img,
                             sorted(fig_to_scripts[img]), has_note))

    n_scripts = len(cjk_scripts)
    n_figs = len(fig_to_scripts)
    print(f"# CJK-bearing simulation scripts: {n_scripts} / {len(list(SIM_DIR.glob('*.py')))-1}")
    print(f"# Figures produced by CJK-bearing scripts: {n_figs}")
    print(f"# EN-page x figure embeddings found: {len(rows)}")
    missing = [r for r in rows if not r[3]]
    print(f"# Embeddings still missing a Translator's note: {len(missing)}")
    print()
    for page, img, scripts, has_note in rows:
        if missing_only and has_note:
            continue
        flag = "OK  " if has_note else "MISS"
        print(f"{flag}  {page}  <-  {img}  <-  {','.join(scripts)}")


if __name__ == "__main__":
    main()
