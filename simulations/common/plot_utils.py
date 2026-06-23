"""
plot_utils.py — shared plotting helpers for the ISF teaching site.

All figures are written to <project_root>/static/figures/ so that Docusaurus
can serve them at /figures/<name>.png regardless of the current working
directory when a script is launched.
"""
import os
import matplotlib

matplotlib.use("Agg")  # headless backend; we never show() interactively
import matplotlib.pyplot as plt  # noqa: E402

# ---------------------------------------------------------------------------
# Path resolution: this file lives at simulations/common/plot_utils.py
#   common -> simulations -> <project_root>
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(_HERE))
FIG_DIR = os.path.join(PROJECT_ROOT, "static", "figures")

# Pick a CJK-capable font so Traditional-Chinese labels render (not tofu boxes).
# Math written as $...$ still uses matplotlib's mathtext fonts.
import matplotlib.font_manager as _fm  # noqa: E402

_available = {f.name for f in _fm.fontManager.ttflist}
_cjk_prefs = ["Heiti TC", "Arial Unicode MS", "STHeiti", "Hiragino Sans GB",
              "Songti SC", "PingFang TC"]
_cjk_font = next((f for f in _cjk_prefs if f in _available), None)

# A consistent, readable style for the whole site.
plt.rcParams.update(
    {
        "figure.dpi": 120,
        "savefig.dpi": 120,
        "axes.unicode_minus": False,  # use ASCII '-' so CJK fonts show it
        "font.family": ([_cjk_font] if _cjk_font else []) + ["DejaVu Sans", "sans-serif"],
        "font.size": 11,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
        "lines.linewidth": 1.8,
        "figure.autolayout": True,
    }
)


def figure_path(name):
    """Return the absolute path for a figure file name (ensures the dir exists)."""
    os.makedirs(FIG_DIR, exist_ok=True)
    if not name.lower().endswith((".png", ".svg", ".pdf")):
        name += ".png"
    return os.path.join(FIG_DIR, name)


def savefig(fig, name, verbose=True):
    """Save `fig` into static/figures/<name> and print the path."""
    path = figure_path(name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    if verbose:
        rel = os.path.relpath(path, PROJECT_ROOT)
        print(f"  [figure] {rel}")
    return path
