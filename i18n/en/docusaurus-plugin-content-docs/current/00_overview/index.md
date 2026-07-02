---
title: ISF and Oscillator Phase Noise
description: From paper to design intuition — home page of the Impulse Sensitivity Function teaching site.
slug: /
---

> 🌐 English translation (β). Most other pages are currently in Traditional Chinese — they will show in Chinese until translated.

# ISF and Oscillator Phase Noise: From Paper to Design Intuition

> From paper to design intuition. This site takes the Hajimiri–Lee **Impulse Sensitivity
> Function (ISF)** theory from first principles all the way to hands-on design feel for
> SerDes clock jitter. **Every formula is derived step by step, with units, numerical
> examples, Python code and figures, and explicit paper citations.**

## Who this site is for

We assume you are an **EE graduate**: you know circuit theory, electronics, signals and
systems, random processes, the Fourier transform, and basic DSP, but you have **not yet**
truly mastered oscillator phase noise, timing jitter (the deviation of a clock edge from
its ideal instant), the ISF, cyclostationary noise, or the LTV (linear time-variant)
oscillator model. After finishing this site, you should be able to:

- read and **re-derive on your own** the core equations of [P1] Hajimiri–Lee 1998;
- explain "why an oscillator is LTV — not LTI — with respect to noise";
- compute phase noise from the ISF and convert phase noise into rms jitter;
- name the **design knobs** that lower 1/f² and 1/f³ phase noise;
- connect all of this to practical **SerDes clocking** intuition (LC-VCO / ring-VCO / PLL / CDR).

## Start from your goal

The full 9-step sequential path is in the [Learning Path](/00_overview/learning_path);
but if you already have a concrete goal in mind, it is faster to jump in through one of
the three "entry cards" below.

### I want to learn ISF from scratch

You are not in a hurry and want to understand oscillator phase noise (the random
fluctuation of an oscillation signal's phase) from the ground up. First build the
physical intuition of "what an oscillator's phase actually is", then follow the
planned path.

- [What is oscillator phase?](/02_foundations/oscillator_phase) — phase vs. amplitude seen from the limit cycle
- [Learning Path](/00_overview/learning_path) — the complete 9-step route, from basics to advanced

### I have a phase-noise plot and need jitter

You already have a measured or spec-sheet $\mathcal{L}(\Delta f)$ curve and want to know
how to convert it into rms timing jitter, and what that means for a SerDes link.

- [Phase Noise → Jitter](/02_foundations/psd_phase_noise_jitter) — PSD, $\mathcal{L}(f)$, jitter definitions and conversions
- [From ISF to SerDes clocking](/06_design_insights/serdes_clocking_connection) — how jitter closes the eye and sets BER
- [Lab 08 — Integrating L(f) into rms jitter](/04_simulation_labs/lab_08_jitter_integration) — hands-on integration of $\mathcal{L}(f)$ into $\sigma_t$

### I am reading a Hajimiri paper

You are sitting in front of one of the papers and want to know "where on this site is
this equation derived step by step".

- [Paper Deep Dives](/05_paper_deep_dives) — the five source papers, read one by one
- [Equation Index](/01_paper_map/equation_index) — look up this site's derivation from [Px] Eq.(n)

### Quick reference

You do not want to read a whole page — you just need one symbol, one term, or one formula:

- [Cheat Sheet](/00_overview/cheat_sheet) — signature formulas and numerical feel, packed into one page
- [Notation](/00_overview/notation) — site-wide consistent symbols, meanings, units
- [Glossary](/99_appendix/glossary) — intuitive explanations of the English terms
- [Equation Index](/01_paper_map/equation_index) — formula ↔ paper source ↔ derivation page

## Required background

Linear systems and convolution, Fourier series/transform, random processes and PSD
(power spectral density), basic circuits (RLC, capacitor $q=Cv$), and a little
Python/NumPy. You do **not** need any prior knowledge of oscillator noise — that is
exactly what this site teaches.

## How to run the simulations

```bash
# Install the site dependencies
npm install
# Start the local site (http://localhost:3000)
npm run start
# Re-run all simulations in one shot; regenerates every figure under static/figures/
python scripts/run_all_sims.py
```

Every figure is traceable to its script and formula in the [figure_index](/01_paper_map/figure_index).

## How to read the equations

Equations are rendered with KaTeX. Every important formula comes with: its **[Px] Eq.(n)
page** source, its **physical meaning**, its **units**, a **numerical example**, and its
**conditions of validity and failure**. A `TODO:` marker means that spot still needs
manual verification against the original PDF. A "toy model" label means it is a
pedagogical simplification, not transistor-level accuracy.

## References

The five source papers and external supplements are in [references](/99_appendix/references);
per-paper close readings are in the [paper deep dives](/05_paper_deep_dives/); the paper
map is in [paper_summary_table](/01_paper_map/paper_summary_table).

> **Honest disclosure**: the source folder contains 5 PDFs. Four of them are Hajimiri-series
> oscillator phase noise / injection papers, but **one (`Hajimiri_ISCS_98.pdf`) is actually a
> cross-coupled sense amplifier paper, unrelated to the ISF**. This site labels it honestly
> and uses it only as a side note. See the
> [build_report](/00_overview/build_report) for details.
