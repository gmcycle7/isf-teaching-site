"""
make_notebooks.py — generate downloadable Jupyter notebooks from selected labs.

Converts a fixed list of `simulations/lab_*.py` scripts into self-contained
.ipynb files under `static/notebooks/`, so the site can offer them as
downloadable assets (served at <baseUrl>/notebooks/<name>.ipynb).

Each generated notebook is a *snapshot* of the lab script at generation time:

  cell 0  (markdown) : title + the lab's module docstring + provenance note
  cell 1  (code)     : setup — locate the repo root (the notebooks import from
                       simulations/common), sys.path.insert, CJK font pick
  cell 2  (code)     : the lab's imports / module-level constants, with the
                       script-only boilerplate removed (import os/sys +
                       sys.path.insert(__file__...)) and `from plot_utils
                       import savefig` replaced by an inline-display shim
                       (the original savefig writes PNGs to static/figures/
                       and never shows; notebooks want plt.show() instead)
  cells 3+ (code)    : one cell per top-level function (comment banners kept)
  last cell (code)   : `main()` (replaces the `if __name__ == "__main__"` guard)

Run (from the project root; requires nbformat):

    python scripts/make_notebooks.py

Regenerate after editing any of the source labs — the notebooks are build
artifacts, not hand-edited files.
"""
import ast
import os
import re
import sys

import nbformat as nbf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM_DIR = os.path.join(ROOT, "simulations")
OUT_DIR = os.path.join(ROOT, "static", "notebooks")

# Labs selected for notebook export (the "main spine" of the course).
LABS = [
    "lab_01_sinusoidal_oscillator",
    "lab_05_fourier_isf",
    "lab_06_white_noise_phase_noise",
    "lab_08_jitter_integration",
    "lab_18_lorentzian",
    "lab_22_capstone_lc_end_to_end",
    "lab_24_jitter_kernels",
]

REPO_URL = "https://github.com/gmcycle7/isf-teaching-site"

# ---------------------------------------------------------------------------
# Cell templates
# ---------------------------------------------------------------------------
SETUP_CELL = f'''\
# --- Setup：本 notebook 需要教學網站 repo 的 simulations/common 模組 ---
# 還沒有原始碼的話，先 clone repo，並把本 notebook 放在 repo 目錄樹內執行：
#     git clone {REPO_URL}.git
# 相依套件只有三個：pip install numpy scipy matplotlib（外加 jupyter 本身）
import sys
from pathlib import Path

def _find_repo_root():
    """從目前工作目錄往上找，直到看到 simulations/common 為止。"""
    for base in [Path.cwd(), *Path.cwd().parents]:
        if (base / "simulations" / "common").is_dir():
            return base
    raise FileNotFoundError(
        "找不到 simulations/common —— 請把本 notebook 放進 isf-teaching-site "
        "repo 目錄樹內執行（git clone {REPO_URL}.git），"
        "或手動把 <repo>/simulations/common 加入 sys.path")

ROOT = _find_repo_root()
for _p in (str(ROOT), str(ROOT / "simulations" / "common")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
print("repo root:", ROOT)

# CJK 字型：圖的標籤有繁體中文；找不到 CJK 字型只影響文字顯示、不影響任何數值
import matplotlib.pyplot as plt
import matplotlib.font_manager as _fm
_avail = {{f.name for f in _fm.fontManager.ttflist}}
_cjk = next((f for f in ["Heiti TC", "Arial Unicode MS", "STHeiti",
                         "Hiragino Sans GB", "Songti SC", "PingFang TC",
                         "Noto Sans CJK TC", "Microsoft JhengHei"]
             if f in _avail), None)
if _cjk:
    plt.rcParams["font.family"] = [_cjk, "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False   # ASCII 減號，避免變方塊
print("CJK font:", _cjk or "(none found — 中文標籤可能顯示為方塊)")'''

SAVEFIG_SHIM = '''\
# notebook 版 savefig：改成 inline 顯示。
# （原始 lab script 的 plot_utils.savefig 會把 PNG 寫進 static/figures/ 且從不
#   show()；在 notebook 裡我們直接把圖畫在 cell 輸出。）
def savefig(fig, name, verbose=True):
    plt.show()
    plt.close(fig)'''

# script-only boilerplate lines to drop from the imports cell
_DROP_PATTERNS = (
    re.compile(r"^import os\s*$"),
    re.compile(r"^import sys\s*$"),
    re.compile(r"^sys\.path\.insert\(.*__file__.*\)\s*$"),
)
_SAVEFIG_IMPORT = re.compile(r"^from plot_utils import savefig\s*$")


# ---------------------------------------------------------------------------
# Source splitting
# ---------------------------------------------------------------------------
def split_lab_source(source):
    """Split a lab script into (docstring, preamble, [function chunks], has_guard).

    All chunks are lists of source lines. Comment banners immediately above a
    top-level `def` are attached to that function's chunk.
    """
    tree = ast.parse(source)
    lines = source.splitlines()

    docstring = ast.get_docstring(tree) or ""
    body = tree.body
    idx = 0
    doc_end = 0  # 1-based line where the module docstring ends
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        doc_end = body[0].end_lineno
        idx = 1

    def_starts = []   # 1-based, adjusted upward over attached comment lines
    guard_start = None
    for node in body[idx:]:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = node.lineno
            # attach the comment banner (contiguous '#' lines) above the def
            while start - 2 >= 0 and lines[start - 2].lstrip().startswith("#"):
                start -= 1
            def_starts.append(start)
        elif isinstance(node, ast.If):
            seg = ast.get_source_segment(source, node.test) or ""
            if "__name__" in seg:
                guard_start = node.lineno
                # attach banner above the guard too (so it is dropped with it)
                while guard_start - 2 >= 0 and lines[guard_start - 2].lstrip().startswith("#"):
                    guard_start -= 1

    if not def_starts:
        raise ValueError("lab has no top-level functions")

    preamble = lines[doc_end:def_starts[0] - 1]
    bounds = def_starts + [guard_start if guard_start else len(lines) + 1]
    chunks = [lines[bounds[i] - 1:bounds[i + 1] - 1] for i in range(len(def_starts))]
    return docstring, preamble, chunks, guard_start is not None


def clean_chunk(chunk_lines):
    """Strip leading/trailing blank lines; collapse runs of 3+ blank lines."""
    text = "\n".join(chunk_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip("\n")


def transform_preamble(preamble_lines):
    """Drop script-only boilerplate; swap the savefig import for the shim."""
    out = []
    for ln in preamble_lines:
        if any(p.match(ln) for p in _DROP_PATTERNS):
            continue
        if _SAVEFIG_IMPORT.match(ln):
            out.extend(["", SAVEFIG_SHIM])
            continue
        out.append(ln)
    return clean_chunk(out)


def title_markdown(lab, docstring):
    """Markdown title cell: H1 + docstring body + provenance note."""
    doc_lines = docstring.splitlines()
    if doc_lines and doc_lines[0].strip() == lab + ".py":
        doc_lines = doc_lines[1:]
    doc_body = "\n".join(doc_lines).strip("\n")
    return (
        f"# {lab}\n"
        "\n"
        f"{doc_body}\n"
        "\n"
        "---\n"
        "\n"
        f"> 本 notebook 由 `scripts/make_notebooks.py` 從 "
        f"`simulations/{lab}.py` **自動產生**（generated snapshot，非手寫檔）。\n"
        f"> 權威版本是 repo 裡的 lab script；lab 更新後請重跑產生器同步。\n"
        f"> 執行需求：clone [isf-teaching-site]({REPO_URL})（要 import "
        f"`simulations/common`）＋ `numpy` / `scipy` / `matplotlib`。"
    )


# ---------------------------------------------------------------------------
# Notebook assembly
# ---------------------------------------------------------------------------
def build_notebook(lab):
    src_path = os.path.join(SIM_DIR, lab + ".py")
    with open(src_path, encoding="utf-8") as fh:
        source = fh.read()

    docstring, preamble, chunks, had_guard = split_lab_source(source)
    if not had_guard:
        raise ValueError(f"{lab}: expected an `if __name__` guard")

    cells = [
        nbf.v4.new_markdown_cell(title_markdown(lab, docstring)),
        nbf.v4.new_code_cell(SETUP_CELL),
        nbf.v4.new_code_cell(transform_preamble(preamble)),
    ]
    for chunk in chunks:
        cells.append(nbf.v4.new_code_cell(clean_chunk(chunk)))
    cells.append(nbf.v4.new_code_cell("# 執行整個 lab（對應原 script 的 __main__）\nmain()"))

    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "version": "3.12"}
    nb.cells = cells
    nbf.validate(nb)
    return nb


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"[make_notebooks] {len(LABS)} labs -> {os.path.relpath(OUT_DIR, ROOT)}/")
    for lab in LABS:
        nb = build_notebook(lab)
        out_path = os.path.join(OUT_DIR, lab + ".ipynb")
        nbf.write(nb, out_path)
        n_md = sum(1 for c in nb.cells if c.cell_type == "markdown")
        n_code = sum(1 for c in nb.cells if c.cell_type == "code")
        print(f"  {lab + '.ipynb':<45s} {len(nb.cells):2d} cells "
              f"({n_md} markdown, {n_code} code)")
    print("[make_notebooks] done.")


if __name__ == "__main__":
    main()
