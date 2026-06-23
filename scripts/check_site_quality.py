#!/usr/bin/env python3
"""
check_site_quality.py — lint the ISF teaching site for the quality criteria
required by the project brief.

Checks (per docs/*.md|mdx):
  1.  every page has a title (front-matter `title:` or an H1)
  2.  formula pages (03_*, 05_*, or pages with $$) carry a source citation
  3.  every referenced figure /figures/x.png exists in static/figures/
  4.  every generated figure has a corresponding script (extracted_figures.json)
  5.  each simulation lab page has a code block
  6.  each simulation lab page has a parameter table
  7.  each simulation lab page has a unit explanation
  8.  each paper deep-dive page has a citation
  9.  count / list unresolved TODOs
 10.  (optional, --build) whether `npm run build` succeeds

Usage:
  python scripts/check_site_quality.py            # static checks
  python scripts/check_site_quality.py --build     # also run npm run build
  python scripts/check_site_quality.py --json out.json
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
FIGDIR = os.path.join(ROOT, "static", "figures")
FIGJSON = os.path.join(ROOT, "extracted", "extracted_figures.json")

REQUIRED_FIGURES = [
    "limit_cycle_phase_amplitude.png", "lti_vs_ltv_impulse_response.png",
    "sinusoidal_impulse_phase_sweep.png", "waveform_with_impulse_markers.png",
    "isf_impulse_sweep_sinusoidal.png", "isf_fourier_reconstruction.png",
    "isf_fourier_coefficients.png", "symmetric_vs_asymmetric_isf_c0.png",
    "white_noise_phase_noise_psd.png",
    "flicker_upconversion_symmetric_vs_asymmetric.png",
    "phase_noise_to_jitter_integration.png", "lc_vs_ring_isf_comparison.png",
    "ring_oscillator_timing_noise_accumulation.png",
    # v2 additions
    "rf_spectrum_phase_noise_sidebands.png", "monte_carlo_jitter_histogram.png",
    "serdes_eye_ber_bathtub.png", "pll_cdr_jitter_transfer.png",
    "cyclostationary_effective_isf.png", "nonlinear_oscillator_isf.png",
    "leeson_vs_isf_overlay.png", "design_tradeoff_sweeps.png",
]

# Heuristic: lines that perform a numeric computation (number + unit/sci + '=')
_NUM_UNIT = re.compile(r"\d\s*(fs|ps|ns|pC|fC|aC|GHz|MHz|kHz|Hz|dBc|mrad|rad|V|mV|A|kT)\b")


def numeric_example_count(txt):
    body = re.sub(r"```.*?```", "", txt, flags=re.S)
    n = 0
    for ln in body.split("\n"):
        if ("=" in ln or "\\approx" in ln) and (_NUM_UNIT.search(ln)
                                                or "\\times10" in ln or "\\times 10" in ln):
            n += 1
    return n


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def has_title(txt):
    fm = re.search(r"^---\s*\n(.*?)\n---", txt, re.S)
    if fm and re.search(r"^\s*title\s*:", fm.group(1), re.M):
        return True
    return bool(re.search(r"^\s*#\s+\S", txt, re.M))


def has_citation(txt):
    return bool(re.search(r"\[P[1-5]\]|Eq\.\s*\(|paper_00|IEEE|JSSC|Hajimiri", txt))


def has_code_block(txt):
    return "```python" in txt or "```py" in txt or txt.count("```") >= 2


def has_param_table(txt):
    # a markdown table whose context mentions parameters/units
    if "|" not in txt:
        return False
    return bool(re.search(r"參數|parameter|Parameter|param", txt))


def has_unit_explanation(txt):
    return bool(re.search(r"單位|\bunit\b|Unit|\[s\]|\[rad\]|A²/Hz|dBc/Hz|fs\b", txt))


def figure_refs(txt):
    return re.findall(r"/figures/([A-Za-z0-9_\-]+\.png)", txt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true", help="also run npm run build")
    ap.add_argument("--json", default=None, help="write a JSON summary here")
    args = ap.parse_args()

    pages = sorted(glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True) +
                   glob.glob(os.path.join(DOCS, "**", "*.mdx"), recursive=True))
    issues = []
    warnings = []
    todos = []
    fig_have = {os.path.basename(p) for p in glob.glob(os.path.join(FIGDIR, "*.png"))}

    for p in pages:
        rel = os.path.relpath(p, ROOT)
        txt = read(p)
        is_lab = "/04_simulation_labs/lab_" in p.replace("\\", "/")
        is_dd = "/05_paper_deep_dives/paper_" in p.replace("\\", "/")
        is_formula = ("/03_isf_core_theory/" in p.replace("\\", "/")
                      or "/05_paper_deep_dives/" in p.replace("\\", "/")
                      or "$$" in txt)

        if not has_title(txt):
            issues.append(f"{rel}: missing title (no front-matter title and no H1)")
        if is_formula and not has_citation(txt):
            issues.append(f"{rel}: formula page lacks a source citation ([Px]/Eq./IEEE)")
        if is_dd and not has_citation(txt):
            issues.append(f"{rel}: deep-dive page lacks a citation")
        if is_lab:
            if not has_code_block(txt):
                issues.append(f"{rel}: lab page has no python code block")
            if not has_param_table(txt):
                issues.append(f"{rel}: lab page has no parameter table")
            if not has_unit_explanation(txt):
                issues.append(f"{rel}: lab page has no unit explanation")
        for fig in figure_refs(txt):
            if fig not in fig_have:
                issues.append(f"{rel}: references missing figure /figures/{fig}")
        # soft: core-theory & design pages should carry >=2 numeric worked examples
        relu = p.replace("\\", "/")
        is_core = "/03_isf_core_theory/" in relu
        is_design = "/06_design_insights/" in relu
        if is_core or is_design:
            ne = numeric_example_count(txt)
            if ne < 2:
                warnings.append(f"{rel}: only {ne} numeric-example line(s) (want >=2)")
        for m in re.finditer(r"TODO[:：].*", txt):
            todos.append(f"{rel}: {m.group(0).strip()[:120]}")

    # required figures present?
    missing_required = [f for f in REQUIRED_FIGURES if f not in fig_have]

    # figures <-> script mapping
    fig_without_script = []
    if os.path.exists(FIGJSON):
        meta = json.load(open(FIGJSON, encoding="utf-8"))
        for gf in meta.get("generated_figures", []):
            sp = os.path.join(ROOT, gf["script"])
            if not os.path.exists(sp):
                fig_without_script.append(f"{gf['file']} -> missing script {gf['script']}")

    build_ok = None
    build_log = ""
    if args.build:
        print("Running `npm run build` (this can take a minute) ...")
        proc = subprocess.run(["npm", "run", "build"], cwd=ROOT,
                              capture_output=True, text=True)
        build_ok = proc.returncode == 0
        build_log = (proc.stdout + proc.stderr)[-3000:]

    # ---- report ----
    print("=" * 70)
    print("ISF site quality check")
    print("=" * 70)
    print(f"pages scanned        : {len(pages)}")
    print(f"figures present      : {len(fig_have)}")
    print(f"required figs missing: {len(missing_required)} {missing_required or ''}")
    print(f"fig->script problems : {len(fig_without_script)}")
    print(f"content issues       : {len(issues)}")
    print(f"soft warnings        : {len(warnings)}")
    print(f"open TODOs           : {len(todos)}")
    if build_ok is not None:
        print(f"npm run build        : {'OK' if build_ok else 'FAILED'}")

    if issues:
        print("\n-- ISSUES --")
        for i in issues:
            print("  -", i)
    if warnings:
        print("\n-- SOFT WARNINGS (non-blocking) --")
        for w in warnings:
            print("  -", w)
    if missing_required:
        print("\n-- MISSING REQUIRED FIGURES --")
        for f in missing_required:
            print("  -", f)
    if fig_without_script:
        print("\n-- FIGURE/SCRIPT MISMATCH --")
        for f in fig_without_script:
            print("  -", f)
    if todos:
        print(f"\n-- OPEN TODOs ({len(todos)}) --")
        for t in todos[:80]:
            print("  -", t)

    summary = {
        "pages": len(pages),
        "figures_present": len(fig_have),
        "missing_required_figures": missing_required,
        "fig_without_script": fig_without_script,
        "issues": issues,
        "warnings": warnings,
        "todos": todos,
        "build_ok": build_ok,
    }
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\nWrote summary -> {args.json}")

    hard_fail = bool(issues) or bool(missing_required) or (build_ok is False)
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
