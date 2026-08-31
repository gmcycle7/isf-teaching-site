#!/usr/bin/env python3
"""
update_stats.py — U4 門面數字同步：一鍵重數「頁/圖/模擬/互動工具/可驗證例題」
五個門面數字，並把它們 regex-patch 進 README.md、
docs/04_simulation_labs/interactive_calculator.mdx 開場白（+ EN sibling 的對應句），
最後用同一組數字重繪 static/img/social-card.png（PIL）。

冪等（idempotent）：每個 patch 都是「找到已存在的『N 頁推導 · M 張圖 · ...』或
README 規模行 pattern，整段替換成新數字」，不會每跑一次就疊加文字。

計數規則（與 extracted/_AUTHORING_SPEC.md、README「Project structure」一致）：
  (a) zh 頁數      = docs/**/*.md 和 docs/**/*.mdx 的檔案數
  (b) 圖            = static/figures/*.png 的檔案數
  (c) 模擬          = simulations/lab_*.py + simulations/fig_*.py 的檔案數
  (d) 互動元件      = src/components/*.js 扣掉 useIsEn.js（一個純 hook，不是元件）
  (e) 可驗證例題    = 呼叫 scripts/verify_examples.py 並解析它印出的
                     "checkable blocks (with '# ->' numbers): <N>"

Usage:
    python scripts/update_stats.py            # 計算 + patch + 重繪 social card
    python scripts/update_stats.py --dry-run  # 只印出數字，不寫檔
"""
import glob
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DOCS = os.path.join(ROOT, "docs")
FIGDIR = os.path.join(ROOT, "static", "figures")
SIMDIR = os.path.join(ROOT, "simulations")
COMPDIR = os.path.join(ROOT, "src", "components")
README = os.path.join(ROOT, "README.md")
CALC_ZH = os.path.join(DOCS, "04_simulation_labs", "interactive_calculator.mdx")
CALC_EN = os.path.join(
    ROOT, "i18n", "en", "docusaurus-plugin-content-docs", "current",
    "04_simulation_labs", "interactive_calculator.mdx",
)
SOCIAL_CARD = os.path.join(ROOT, "static", "img", "social-card.png")

VERIFY_SCRIPT = os.path.join(HERE, "verify_examples.py")


# ---------------------------------------------------------------------------
# (a)-(d): filesystem counts
# ---------------------------------------------------------------------------

def count_pages():
    """docs/**/*.md + docs/**/*.mdx — zh source pages."""
    md = glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True)
    mdx = glob.glob(os.path.join(DOCS, "**", "*.mdx"), recursive=True)
    return len(md) + len(mdx)


def count_figures():
    """static/figures/*.png — reproducible figures."""
    return len(glob.glob(os.path.join(FIGDIR, "*.png")))


def count_sims():
    """simulations/lab_*.py + simulations/fig_*.py (top-level only, not common/)."""
    lab = glob.glob(os.path.join(SIMDIR, "lab_*.py"))
    fig = glob.glob(os.path.join(SIMDIR, "fig_*.py"))
    return len(lab) + len(fig)


def count_interactive_components():
    """src/components/*.js minus useIsEn.js (a hook, not a standalone widget)."""
    js = glob.glob(os.path.join(COMPDIR, "*.js"))
    js = [f for f in js if os.path.basename(f) != "useIsEn.js"]
    return len(js)


# ---------------------------------------------------------------------------
# (e): checkable examples — reuse verify_examples.py's own functions so the
# counting logic can never drift from what the gate actually checks.
# ---------------------------------------------------------------------------

def count_checkable_examples():
    spec = importlib.util.spec_from_file_location("verify_examples", VERIFY_SCRIPT)
    ve = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ve)

    pages = sorted(
        glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True)
        + glob.glob(os.path.join(ROOT, "docs", "**", "*.mdx"), recursive=True)
    )
    total = 0
    for p in pages:
        text = open(p, encoding="utf-8").read()
        for code in ve.python_blocks(text):
            if ve.expected_from(code):
                total += 1
    return total


def run_verify_examples_gate():
    """Run the real script as a subprocess too, so a mismatch between the
    reused-function count and the script's own printed count is caught loudly
    instead of silently diverging."""
    p = subprocess.run(
        [sys.executable, VERIFY_SCRIPT], cwd=ROOT, capture_output=True, text=True
    )
    m = re.search(r"checkable blocks \(with '# ->' numbers\):\s*(\d+)", p.stdout)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Patchers (idempotent regex replace)
# ---------------------------------------------------------------------------

def patch_readme(n_pages, n_figs, n_sims, n_widgets, n_examples, dry_run=False):
    text = open(README, encoding="utf-8").read()
    pattern = re.compile(
        r"\*\*規模\*\*：\d+\s*頁教學、\d+\s*張重現圖、\d+\s*個可重跑模擬、"
        r"\d+\s*個互動工具、\d+\+?\s*個可自動驗證的數值例題"
    )
    replacement = (
        f"**規模**：{n_pages} 頁教學、{n_figs} 張重現圖、{n_sims} 個可重跑模擬、"
        f"{n_widgets} 個互動工具、{n_examples} 個可自動驗證的數值例題"
    )
    if not pattern.search(text):
        raise RuntimeError("README.md: 找不到規模行 pattern，請手動確認格式未變")
    new_text = pattern.sub(replacement, text)

    # Same file also states the figure count inline in the "Run all
    # simulations" section ("...（41 張）").  Patch it too so the two figure
    # counts in one README can never contradict each other after this script
    # runs.
    fig_pattern = re.compile(r"（\d+\s*張）(?=。\n\n## Build)")
    fig_replacement = f"（{n_figs} 張）"
    if not fig_pattern.search(new_text):
        raise RuntimeError("README.md: 找不到「（N 張）」圖片計數 pattern，請手動確認格式未變")
    new_text = fig_pattern.sub(fig_replacement, new_text)

    changed = new_text != text
    if changed and not dry_run:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new_text)
    return changed, replacement


CJK_NUM = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
           "十一", "十二", "十三", "十四", "十五"]
EN_NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven",
          "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
          "fifteen"]


def _count_top_level_widgets(mdx_path):
    text = open(mdx_path, encoding="utf-8").read()
    return len(re.findall(r"^<[A-Z][A-Za-z]*\s*/>", text, re.M))


def patch_calculator_blurb(dry_run=False):
    """Patch the '七個互動工具 / Seven interactive tools' sentence in both the
    zh page and its EN sibling so the number always matches how many top-level
    <Widget /> tags are actually mounted on that page (idempotent: regex finds
    the CJK/English number word regardless of what it currently says)."""
    results = []
    n = _count_top_level_widgets(CALC_ZH)
    n_en = _count_top_level_widgets(CALC_EN)
    if n != n_en:
        raise RuntimeError(
            f"interactive_calculator.mdx widget count mismatch zh={n} en={n_en}; "
            "zh/en pages have drifted out of sync — fix content before patching stats"
        )

    word_zh = CJK_NUM[n] if n < len(CJK_NUM) else str(n)
    word_en = EN_NUM[n] if n < len(EN_NUM) else str(n)

    # zh: "七個互動工具（計算器、探索器、動畫與沙盒）"
    zh_text = open(CALC_ZH, encoding="utf-8").read()
    zh_pat = re.compile(r"^[一二三四五六七八九十]+個互動工具(?=（)", re.M)
    if not zh_pat.search(zh_text):
        raise RuntimeError(f"{CALC_ZH}: 找不到『N個互動工具』開場白 pattern")
    zh_new = zh_pat.sub(f"{word_zh}個互動工具", zh_text)
    changed_zh = zh_new != zh_text
    if changed_zh and not dry_run:
        with open(CALC_ZH, "w", encoding="utf-8") as f:
            f.write(zh_new)
    results.append(("zh", changed_zh, n, word_zh))

    # en: "Seven interactive tools (calculators, explorers, animations, and a sandbox)"
    en_text = open(CALC_EN, encoding="utf-8").read()
    en_pat = re.compile(
        r"^(?:Zero|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen)"
        r"(?= interactive tools \()",
        re.M,
    )
    if not en_pat.search(en_text):
        raise RuntimeError(f"{CALC_EN}: 找不到 'N interactive tools (' 開場白 pattern")
    en_new = en_pat.sub(word_en.capitalize(), en_text)
    changed_en = en_new != en_text
    if changed_en and not dry_run:
        with open(CALC_EN, "w", encoding="utf-8") as f:
            f.write(en_new)
    results.append(("en", changed_en, n_en, word_en))

    return results


# ---------------------------------------------------------------------------
# Social card regeneration (PIL) — reuses the exact v1 recipe:
#   font "/System/Library/Fonts/STHeiti Medium.ttc" index 0; 1200x630 bg (14,32,52);
#   -sin curve + orange impulse arrow + Lorentzian-skirt background lines;
#   stats line with the counted numbers; title + subtitle.
# ---------------------------------------------------------------------------

def regenerate_social_card(n_pages, n_figs, n_sims, n_widgets, dry_run=False):
    from PIL import Image, ImageDraw, ImageFont
    import math

    W, H = 1200, 630
    BG = (14, 32, 52)
    BLUE = (102, 204, 255)
    ORANGE = (255, 165, 40)
    SKIRT = (70, 100, 140)
    BASELINE = (90, 110, 135)
    WHITE = (240, 245, 250)
    SUBTITLE = (150, 190, 225)
    STATS_COLOR = (140, 170, 200)

    FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(FONT_PATH, 56, index=0)
    subtitle_font = ImageFont.truetype(FONT_PATH, 28, index=0)
    stats_font = ImageFont.truetype(FONT_PATH, 26, index=0)

    margin = 90

    # -- Lorentzian-skirt background lines: S(w) ~ D / (D^2 + w^2), several D's,
    #    centered around the same x as the orange arrow, drawn faint/thin so
    #    they read as decorative "phase-noise skirt" texture behind the -sin.
    baseline_y = 264
    skirt_amp = 210
    cx = W * 0.5
    for D, alpha in [(60, 90), (110, 80), (170, 70), (260, 60)]:
        pts = []
        for x in range(margin - 10, W - margin + 60):
            w = x - cx
            lorentz = D / (D + (w * w) / 900.0)
            y = baseline_y + skirt_amp - skirt_amp * lorentz
            pts.append((x, y))
        line_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(line_img)
        ld.line(pts, fill=SKIRT + (alpha,), width=2)
        img.paste(Image.alpha_composite(img.convert("RGBA"), line_img).convert("RGB"), (0, 0))

    # -- horizontal baseline
    draw.line([(margin - 5, baseline_y), (W - margin + 65, baseline_y)],
              fill=BASELINE, width=1)

    # -- blue -sin(theta) curve across the card width (ISF identity: Gamma=-sin)
    sin_pts = []
    x0, x1 = margin - 5, W - margin + 65
    amp = 118
    for x in range(x0, x1):
        frac = (x - x0) / (x1 - x0)
        theta = frac * 2 * math.pi
        y = baseline_y - amp * (-math.sin(theta))
        sin_pts.append((x, y))
    draw.line(sin_pts, fill=BLUE, width=5, joint="curve")

    # -- orange impulse arrow at the zero-crossing (mid-card), pointing up.
    #    Kept well clear of the subtitle line (which ends near y=155) so it
    #    never overlaps text.
    arrow_x = int((x0 + x1) / 2)
    arrow_top = baseline_y - 40
    arrow_bottom = baseline_y + 165
    draw.line([(arrow_x, arrow_bottom), (arrow_x, arrow_top)], fill=ORANGE, width=6)
    head_w, head_h = 16, 22
    draw.polygon(
        [
            (arrow_x - head_w, arrow_top + head_h),
            (arrow_x + head_w, arrow_top + head_h),
            (arrow_x, arrow_top),
        ],
        fill=ORANGE,
    )

    # -- title + subtitle (top-left)
    draw.text((margin, 45), "ISF & Oscillator Phase Noise", font=title_font, fill=WHITE)
    draw.text(
        (margin, 118),
        "從論文到設計直覺 — Hajimiri–Lee ISF 理論教學站",
        font=subtitle_font,
        fill=SUBTITLE,
    )

    # -- stats line (bottom-left)
    stats_text = f"『{n_pages} 頁推導 · {n_figs} 張圖 · {n_sims} 個模擬 · {n_widgets} 個互動工具』"
    draw.text((margin - 5, H - 90), stats_text, font=stats_font, fill=STATS_COLOR)

    if not dry_run:
        os.makedirs(os.path.dirname(SOCIAL_CARD), exist_ok=True)
        img.save(SOCIAL_CARD)
    return stats_text


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    dry_run = "--dry-run" in sys.argv

    n_pages = count_pages()
    n_figs = count_figures()
    n_sims = count_sims()
    n_widgets = count_interactive_components()
    n_examples = count_checkable_examples()
    n_examples_gate = run_verify_examples_gate()

    if n_examples_gate is not None and n_examples_gate != n_examples:
        raise RuntimeError(
            f"checkable-example count mismatch: reused-function count={n_examples} "
            f"but `python verify_examples.py` printed {n_examples_gate}. "
            "The two counting paths have diverged — investigate before patching."
        )

    print("=" * 70)
    print("update_stats.py — 門面數字同步")
    print("=" * 70)
    print(f"(a) zh 頁數           : {n_pages}")
    print(f"(b) 圖                : {n_figs}")
    print(f"(c) 模擬              : {n_sims}")
    print(f"(d) 互動元件          : {n_widgets}")
    print(f"(e) 可驗證例題        : {n_examples} (gate 印出: {n_examples_gate})")
    print()

    changed_readme, readme_line = patch_readme(
        n_pages, n_figs, n_sims, n_widgets, n_examples, dry_run=dry_run
    )
    print(f"[README.md] {'PATCHED' if changed_readme else 'already up to date'}")
    print(f"  -> {readme_line}")

    calc_results = patch_calculator_blurb(dry_run=dry_run)
    for locale, changed, n, word in calc_results:
        print(f"[interactive_calculator.mdx:{locale}] "
              f"{'PATCHED' if changed else 'already up to date'} "
              f"(widgets on page = {n}, word = '{word}')")

    stats_text = regenerate_social_card(n_pages, n_figs, n_sims, n_widgets, dry_run=dry_run)
    print(f"[static/img/social-card.png] {'regenerated' if not dry_run else 'DRY-RUN (not written)'}")
    print(f"  -> {stats_text}")

    print()
    print("done." if not dry_run else "dry-run complete (no files written).")


if __name__ == "__main__":
    main()
