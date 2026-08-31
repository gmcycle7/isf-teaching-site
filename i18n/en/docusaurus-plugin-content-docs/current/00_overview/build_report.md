---
title: Build Report
description: Which PDFs this automated build read, what it generated, what succeeded, and what still needs manual verification.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Build Report

This page honestly records the build results and their limitations (**current state**). Re-check anytime with `python scripts/check_site_quality.py`.
(Note: this page deliberately avoids bare math dollar signs in prose so Markdown does not parse them as formulas.)

> **Want the version-by-version history?** The full v1→v8 record (including every audit,
> correction incident, and deployment note in detail) has moved to its own page →
> **[Changelog](/00_overview/changelog)**. This page keeps only "the current answers."

## 1. How many PDFs were read?

The source folder contains **5 PDFs** (`scripts/extract_papers.py` scans all of them and dumps plain text).

## 2. Title / author / year of each paper

| id | Filename | Title | Authors | Year | Relation to ISF |
|---|---|---|---|---|---|
| paper_001 | `general.pdf` | A General Theory of Phase Noise in Electrical Oscillators | A. Hajimiri, T. H. Lee | 1998 | **Core foundation** |
| paper_002 | `jitter_ring.pdf` | Jitter and Phase Noise in Ring Oscillators | A. Hajimiri, S. Limotyrakis, T. H. Lee | 1999 | **Ring extension** |
| paper_003 | `BHongGenTheor-I_JSSC2019_Postprint.pdf` | Injection Locking and Pulling…Part I | B. Hong, A. Hajimiri | 2019 | Advanced (injection) |
| paper_004 | `BHongGenTheor-II_JSSC2019_Postprint.pdf` | Injection Locking and Pulling…Part II | B. Hong, A. Hajimiri | 2019 | Advanced (APF) |
| paper_005 | `Hajimiri_ISCS_98.pdf` | Design Issues in Cross-Coupled Inverter Sense Amplifier | A. Hajimiri, R. Heald | 1998 | **Unrelated to ISF** (honestly flagged) |

> **Important honesty note**: the filename `Hajimiri_ISCS_98.pdf` looks like an ISF paper, but the content is actually cross-coupled
> sense-amplifier design — **unrelated** to oscillator phase noise / ISF. It is honestly explained only in the
> [paper_005 deep-dive](/05_paper_deep_dives/paper_005_cross_coupled_sense_amp),
> and used solely as a conceptual bridge for "regeneration / positive feedback".

## 3. Which equations were successfully converted to LaTeX?

The core equations of [P1] (general.pdf), **Eq.(1),(9),(10),(11),(12),(13),(15)–(24)**, were all converted to LaTeX via
**high-resolution page rendering → manual line-by-line comparison**, and used verbatim in the teaching pages and `extracted/*.json`;
there are also step-by-step algebraic expansions (downconversion integral, factor-8 summation, L≈½S_φ small-angle PM, jitter
high-pass kernel, flicker 1/f³ corner, the three classes of Parseval terms) plus two derivation appendices (Floquet/PPV,
Leeson↔ISF). See [changelog](/00_overview/changelog) (v1, v2 entries) for how these were built up over time.

## 4. What is the current status of each equation (verified / still TODO)?

The **[P2] ring constants** (Eq.16 Γrms's N-scaling, Eq.23 FOM prefactor) and the **[P3]/[P4] injection & APF**
equations (generalized Adler Eq.(30)/(35), APF Fig.5/Eq.(18)–(22)) have **all been verified verbatim against the
original PDFs**; the current authoritative versions on the site are:

- Eq.(16): $\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\cdot\dfrac{1}{N^{1.5}}$ ⇒ $\Gamma_{rms}\propto N^{-3/2}$ ($\Gamma_{rms}^2\propto N^{-3}$; the radical covers only the constant $2\pi^2/(3\eta^3)$ — $N^{-1.5}$ sits outside it). [P2] Eq.(16), p.794.
- Eq.(23) FOM: $\mathcal{L}\approx\frac{8}{3\eta}\frac{kT}{P}\frac{V_{DD}}{V_{char}}(f_0/\Delta f)^2$. The prefactor is $8/(3\eta)$ ($\eta$ is the stage-delay proportionality constant of Eq.(14), $\approx 1$); $\gamma$ enters only through $V_{char}=\Delta V/\gamma$; the $V_T=0$ lower bound Eq.(25) is $\frac{16\gamma}{3\eta}$.
- Eq.(8)/(11)/(12): $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ (Eq.8), $\kappa=(\Gamma_{rms}/q_{max})\sqrt{(\overline{i_n^2}/\Delta f)/2}$ (Eq.12).
- Eq.(17)/(18) per-stage noise $4kT\gamma\mu C_{ox}(W/L)\Delta V$ and Eq.(21) power $P=2\eta N V_{DD}q_{max}f_0$.
- **[P3]** Eq.(26) $\tilde\Gamma=\Gamma/q_{max}$; generalized Adler Eq.(30),(33); lock range Eq.(35) $\omega_L=\frac12 I_{inj}|\tilde\Gamma_1|$.
- **[P4]** amplitude decay $\tau_0=2Q/\omega_{osc}$; Eq.(26) ideal-LC fundamental quadrature; Eq.(27) amplitude-corrected Adler.

The **evolution** of these constants (including two caught misreadings, and who fixed what in which
version) is recorded in [the three-misreading-incident summary below](#5-summary-of-three-misreading-correction-incidents)
and in the v3/v4/v7 entries of the [changelog](/00_overview/changelog).

The following remain flagged ⚠️ / `TODO` (external literature or secondary details, not core
ISF/injection physics, deliberately retained):

- **External literature (not among the five source PDFs)**: formal volume/issue/page numbers for Leeson 1966, Demir et al. 2000 (PPV), Kärtner 1990 (volume/issue/page numbers and equation notation have been checked; the period/cycle-to-cycle jitter kernels have been derived in-house from first principles and Monte-Carlo verified at [jitter_kernels](/02_foundations/jitter_kernels), no longer relying on external conventions).
- **[P2]** exact axes of the Fig.17 symmetric-voltage plot; **[P4]** stage-allocation details of the dual-modulus prescaler (Sec. VIII).
- **[P5]** (sense amplifier, unrelated to ISF, deliberately not transcribed).
- **[P4]** exact defining equation and Fourier expansion of the APF (Sec. III-D, p.2127); Fig. 3 subplot captions.

Use `python scripts/check_site_quality.py` to scan for all `TODO:` markers.

## 5. Summary of three misreading-correction incidents

This site has had **3 incidents where an audit mistakenly "corrected" already-verified content into
an error and mislabeled it "verified"** — each was only caught by going back and cross-checking the
original PDF at high zoom, a numerical anchor, and independent algebra:

1. **Ring FOM prefactor**: v2 mistakenly changed it to $8/(3\gamma)$ (mislabeled "verified verbatim") → v4 restored $8/(3\eta)$ against PDF p.796.
2. **The D mapping in the Lorentzian linewidth**: v3 took the variance growth rate κ² as the diffusion constant D → v5 adjudicated with MC + analytic fit and restored $D=\kappa^2/2$.
3. **[P2] Eq.(16) Γrms's N-scaling**: v3 misread the radical's scope and "corrected" v1's originally-correct $N^{-3/2}$ to $N^{-3/4}$ → v7 restored $N^{-3/2}$ after triple-checking the paper's body text ("$1/N^{1.5}$" wording), the $\eta=0.75$ numerical anchor, and App.B's algebra.

Full incident details (exactly what was wrong, how it was caught, and which pages were updated
site-wide after the fix) are in the v2/v3, v4, v5, and v7 entries of the
[changelog](/00_overview/changelog).

## 6. Which figures are conceptual simulations regenerated from the papers?

All figures are **conceptual simulations regenerated** in Python (not bitmaps extracted from the PDFs), reproducing the mechanisms of [P1]/[P2].
See [figure_index](/01_paper_map/figure_index) for the mapping.

## 7. Which figures are only toy models (not transistor-level)?

The vast majority are toy / conceptual models (explicitly flagged as not transistor-level). A few purely mathematical figures (jitter integration,
Leeson↔ISF overlay, design sweeps, PLL transfer, BER bathtub) are computed from formulas and agree with the analytic expressions.

## 8. Which chapters are complete?

All 7 major chapters (00 Overview / 01 Paper Map / 02 Foundations / 03 ISF Core Theory / 04 Simulation
Labs / 05 Paper Deep Dives / 06 Design Insights / 99 Appendix) are complete, with verified equations,
step-by-step derivations, worked examples, interactive widgets, and problem sets with full solutions.
See the [changelog](/00_overview/changelog) for how the content scope evolved.

## 9. Which chapters still have TODOs?

Core-theory TODOs have all been closed (see item 4 above). The remaining `TODO`s are all
**deliberately retained "external-literature scope" flags** (e.g. the source of period-jitter kernel
conventions, standard LC-VCO design lore) and transistor-level exclusion statements (see items 3–4
in Section 12), which do not affect the correctness of the core theory. Use
`python scripts/check_site_quality.py` to scan all `TODO:` markers.

## 10. Does `npm run build` succeed?

**Yes** (Docusaurus 3.10.1, bilingual zh+en): **0 broken links, 0 KaTeX warnings**. A page-by-page
scan of math rendering passed (no residual raw LaTeX, no KaTeX parse errors; matplotlib dollar signs
inside code blocks are expected).

Historical fixes (the rendering-bug class) are recorded in the v2 entry of the [changelog](/00_overview/changelog).

## 11. Does `python scripts/run_all_sims.py` succeed?

**Yes**: **all 45 simulation scripts (38 `lab_*` + 7 `fig_*`) pass**, producing 52 figures in
`static/figures/`. Key validations: the simulated Lorentzian spectrum matches theory, flattening near
the carrier; Allan deviation slopes for the three FM types land precisely at −1/2, 0, +1/2; PLL
optimal loop BW≈6.9 MHz, σ_t≈259 fs; numerically extracted ISF vs theoretical −sinθ max error ~0.001;
white-noise S_φ matches the 1/f² line over ~3 decades; jitter integration numerical = analytic (447.9 fs).

## 12. Current site size and example QA

**Site size: 90 pages × 2 locales, 52 figures, 45 simulations, 20 interactive components.**

`scripts/verify_examples.py` actually runs every Python worked example in docs that has a "reference
answer" (`# ->`) and checks the numbers: **of 144 verifiable blocks, 133 pass automatically, 0
mismatches, 0 errors**; the rest are verifier false positives on formula constants in comments (such
as the "2" in $2\Gamma_{rms}^2$) or comparison numbers, manually confirmed correct. See the terminal
output of `check_site_quality.py` for the latest numbers on pages / figures present / required figs
missing / content issues / soft warnings / open TODOs.

See the [changelog](/00_overview/changelog) for evolution details (what was added and what bugs were fixed in each version).

## Honesty and TODO principles

- Toy models are always flagged as "a pedagogical toy model, not transistor-level."
- Content from external literature (PPV / adjoint / Floquet / Leeson / Demir) is always flagged as
  "not among the five downloaded PDFs, supplemented from standard literature."
- Uncertain constants/figures/citations are always written as `TODO: manual verification needed ...`
  — never guessed to fill a gap.
- [P5] is always honestly explained as a sense-amplifier paper unrelated to ISF, used only as a
  conceptual side note.
- Any "correction claimed by an audit" must be triple-verified in person — original PDF at high
  zoom, numerical anchor, and independent algebra — before being applied site-wide. This site has 3
  real counterexamples where that discipline mattered (see item 5 above); the principle is not just
  theoretical.
- Printing errata in the papers themselves (e.g. [P2] Fig.16's ζ=2.5e5 which should read 2.5e-5, and
  [P1] p.191's "58.8 fF" which should read fC) are also honestly flagged, not silently "corrected"
  without a note.

## Suggested next steps for manual verification

1. ~~Check the exact constants and equation forms of [P2]/[P3]/[P4] against the original PDFs~~ →
   **done** (see item 4 above and the v3/v4/v7 entries of the [changelog](/00_overview/changelog)).
2. ~~Fill in the formal volume/issue/page/DOI for the external literature (Leeson, Demir PPV,
   Kärtner, Adler)~~ → **done** (see the v4 entry of the [changelog](/00_overview/changelog)).
3. For transistor-level accuracy: use Spectre PSS+PNoise/PXF or the adjoint method to extract the ISF and cyclostationary α(x)
   from a real LC-VCO / ring-VCO, replacing the toy models. (Still deliberately out of scope.)
4. Calibrate the absolute numbers of the interactive calculators and the toy models to an actual process.

## Deployment

Publicly deployed as a **GitHub Pages (project page)**:

- Site: `https://gmcycle7.github.io/isf-teaching-site/`
- Source (public): `https://github.com/gmcycle7/isf-teaching-site`
- `baseUrl` set to `/isf-teaching-site/`; KaTeX CSS/fonts bundled via webpack (baseUrl-safe, fully offline).
- Deployment mechanism: local `npm run build`, then push `build/` to the `gh-pages` branch (with
  `.nojekyll`); Pages serves from that branch. Packaged as the one-click script **`./scripts/deploy.sh`**
  (needs only `repo` scope, no `workflow` scope).
- **Copyright handling**: the full text and PDFs of the 5 papers are **not committed** (`.gitignore` excludes `extracted/raw_text/` and `*.pdf`);
  the footer and each page state that copyright belongs to the original authors and the content is for teaching purposes.
- CI (optional): `.github/workflows/deploy.yml` is ready; pushing the workflow file requires a token with `workflow` scope
  (`gh auth refresh -s workflow`) to enable push-to-deploy.

Individual deployment incidents (e.g. how a stuck large deployment was resolved) are in the [changelog](/00_overview/changelog).

---

> **Full version history (v1→v8, with every audit and correction in detail)** → **[Changelog](/00_overview/changelog)**
