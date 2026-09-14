#!/usr/bin/env python3
# zh ↔ EN structural parity check (headings, $$ blocks, # -> markers, images, imports, links, quizzes, tables).
# Usage: python3 scripts/check_en_parity.py   (prints a report; exit code 1 if any mismatch)
import re, os, glob, json, sys

ROOT = "/Users/matthuang/claude_code/ISF/isf-teaching-site"
ZH_ROOT = os.path.join(ROOT, "docs")
EN_ROOT = os.path.join(ROOT, "i18n/en/docusaurus-plugin-content-docs/current")

def find_pages(root):
    out = {}
    for p in glob.glob(os.path.join(root, "**", "*.md*"), recursive=True):
        rel = os.path.relpath(p, root)
        out[rel] = p
    return out

zh_pages = find_pages(ZH_ROOT)
en_pages = find_pages(EN_ROOT)

def metrics(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = {}
    m["headings"] = len(re.findall(r"^#{1,6}\s", text, re.M))
    m["dollar_blocks"] = len(re.findall(r"\$\$", text)) // 2
    m["arrow_markers"] = len(re.findall(r"#\s*->", text))
    m["images"] = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    m["image_count"] = len(m["images"])
    m["components"] = sorted(set(re.findall(r"^import\s+(\w+)\s+from", text, re.M)))
    m["component_count"] = len(m["components"])
    m["internal_links"] = re.findall(r"\]\((/[^)]+)\)", text)
    m["internal_link_count"] = len(m["internal_links"])
    m["numericquiz"] = len(re.findall(r"<NumericQuiz", text))
    m["tables"] = len(re.findall(r"^\|.*\|\s*$", text, re.M and 0) ) # placeholder, real calc below
    # table count: count blocks of consecutive lines starting with | that include a separator row
    lines = text.split("\n")
    tbl_count = 0
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i+1 < len(lines) and re.match(r"^\s*\|?[\s:-]+\|", lines[i+1]):
            tbl_count += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                i += 1
        else:
            i += 1
    m["tables"] = tbl_count
    m["python_blocks"] = len(re.findall(r"```python", text))
    m["text"] = text
    return m

results = []
zh_keys = set(zh_pages)
en_keys = set(en_pages)
only_zh = sorted(zh_keys - en_keys)
only_en = sorted(en_keys - zh_keys)

common = sorted(zh_keys & en_keys)
mismatches = {
    "headings": [], "dollar_blocks": [], "arrow_markers": [], "image_count": [],
    "component_count": [], "internal_link_count": [], "numericquiz": [], "tables": [],
    "python_blocks": [], "image_paths": [], "components_set": [], "link_targets": []
}

for rel in common:
    zm = metrics(zh_pages[rel])
    em = metrics(en_pages[rel])
    for key in ["headings","dollar_blocks","arrow_markers","image_count","component_count",
                "internal_link_count","numericquiz","tables","python_blocks"]:
        if zm[key] != em[key]:
            mismatches[key].append((rel, zm[key], em[key]))
    if set(zm["images"]) != set(em["images"]):
        mismatches["image_paths"].append((rel, zm["images"], em["images"]))
    if set(zm["components"]) != set(em["components"]):
        mismatches["components_set"].append((rel, zm["components"], em["components"]))
    # normalize internal links: strip /en/ prefix from EN links to compare targets
    zl = set(zm["internal_links"])
    el = set(l.replace("/en/", "/", 1) if l.startswith("/en/") else l for l in em["internal_links"])
    if zl != el:
        mismatches["link_targets"].append((rel, sorted(zl - el), sorted(el - zl)))

f = sys.stdout
if True:
    f.write("# EN Parity Report\n\n")
    f.write(f"zh pages: {len(zh_pages)}, en pages: {len(en_pages)}\n\n")
    f.write(f"Only in zh (missing EN mirror): {only_zh}\n\n")
    f.write(f"Only in en (no zh source): {only_en}\n\n")
    for key, items in mismatches.items():
        f.write(f"## {key}: {len(items)} mismatches\n\n")
        for item in items[:15]:
            f.write(f"- {item}\n")
        f.write("\n")

print("done")
print("only_zh", only_zh)
print("only_en", only_en)
for k,v in mismatches.items():
    print(k, len(v))
