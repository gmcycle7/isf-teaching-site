#!/usr/bin/env python3
"""
build_equation_index.py — regenerate docs/01_paper_map/equation_index.md from
the curated extracted/extracted_equations.json.

Usage:
    python scripts/build_equation_index.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
SRC = os.path.join(PROJECT_ROOT, "extracted", "extracted_equations.json")
OUT = os.path.join(PROJECT_ROOT, "docs", "01_paper_map", "equation_index.md")


def esc(s):
    """Escape a LaTeX string so it survives a Markdown table cell.

    A literal '|' inside $...$ would be parsed as a table column separator,
    splitting the math. KaTeX's \\vert renders an identical single bar without
    using a literal pipe, so it is table-safe.
    """
    return s.replace("|", "\\vert ")


def main():
    with open(SRC) as f:
        data = json.load(f)

    lines = []
    lines.append("---")
    lines.append("title: 公式推導索引 Equation Index")
    lines.append("description: 每條核心公式 → 最終形式、推導頁、來源論文。")
    lines.append("---")
    lines.append("")
    lines.append("# 公式推導索引 Equation Index")
    lines.append("")
    lines.append("> 本頁由 `scripts/build_equation_index.py` 從 "
                 "`extracted/extracted_equations.json` 自動產生。")
    lines.append("> 標記 ⚠️ 者表示確切常數/形式仍需人工對照 PDF 確認。")
    lines.append("")
    lines.append("| # | Concept | Final Formula | 推導頁 Derivation | 來源 Source | Notes |")
    lines.append("|---|---|---|---|---|---|")
    for i, eq in enumerate(data["equations"], 1):
        flag = " ⚠️" if eq.get("manual_verification_needed") else ""
        formula = "$" + eq["latex"] + "$"
        page = eq["derivation_page"]
        link = f"[{page.split('/')[-1]}](/{page})"
        lines.append(
            f"| {i} | {esc(eq['concept'])} | {esc(formula)} | {link} | "
            f"{esc(eq['source_paper'])} | {eq['final_or_step']}{flag} |"
        )
    lines.append("")
    lines.append("## 圖例")
    lines.append("")
    lines.append("- **final**：該主題的最終結果公式。")
    lines.append("- **step**：推導過程中的中間步驟。")
    lines.append("- **reference**：作為對照/比較的外部模型（未必出自下載的 5 篇 PDF）。")
    lines.append("- ⚠️：`manual_verification_needed = true`，請對照原始 PDF 再確認。")
    lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write("\n".join(lines))
    print("Wrote", os.path.relpath(OUT, PROJECT_ROOT))


if __name__ == "__main__":
    main()
