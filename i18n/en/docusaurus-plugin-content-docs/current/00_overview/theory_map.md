---
title: "Theory Map"
description: "The whole site's 92 pages compressed into a 56-node mermaid dependency graph: every edge is extracted directly from each page's \"Prerequisites / Next\" breadcrumb line; the 12-step learning-path spine is highlighted in gold; includes a table of the 8 most-connected hub pages and a grouped-node legend."
---

# Theory Map

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

> **Prerequisites**: [learning_path](/00_overview/learning_path) (the page order of the twelve-step spine; this page highlights the corresponding nodes in gold), [notation](/00_overview/notation) (the symbol table — this page introduces no new symbols, but every page name in the graph can be looked up there) | **Next**: [cheat_sheet](/00_overview/cheat_sheet), [paper_summary_table](/01_paper_map/paper_summary_table)

This page does exactly one thing: it draws the "who must be read before whom" relationship among
the site's **92 pages** (Chinese originals; every page also has an English mirror under `i18n/en/`)
as **a single graph**. The graph was not hand-drawn — its edges were **extracted programmatically**
by scanning the "> Prerequisites: … | Next: …" breadcrumb line (or the older format,
"> **Prerequisite Reading**: …") at the top of every page and pulling out the markdown links, so it
reflects the site's **actual link structure**, not an idealized sketch drawn from memory.

## How to read this map

- **Arrow direction = prerequisite relation**: `A --> B` reads "A is a prerequisite of B / what A
  teaches is used directly by B." Following the arrows gives a valid reading order; conversely, a
  node's **incoming edges** are the prerequisite pages it lists, and its **outgoing edges** are the
  downstream pages that list it as a prerequisite.
- **Rectangular nodes** = a single page (chapters 02 Foundations and 03 Core Theory are the main
  spine, so every page there gets its own node, per the map's editorial rule; the three small
  chapters 00/01/05 are also drawn page-by-page). **Rounded (stadium) nodes** = several pages
  **clustered** into one node (all of chapter 04 Simulation Labs is clustered; chapter 06 Design
  Insights and chapter 99 Appendix cluster their lower-degree pages), because drawing all 92 pages
  as separate nodes would be unreadable — after clustering, the whole graph has only **56 nodes**
  (see the "How 92 pages compress to 56 nodes" table below). Exactly which pages sit inside each
  clustered node is listed in the "Grouped-Node Legend" section below.
- **Gold highlight** = nodes touched by the 12 steps of the [learning path](/00_overview/learning_path).
  This is the site's recommended **main spine**; every other node is an extension, a deeper dive, or
  reference material beyond the spine. A clustered node is marked gold as soon as **any one** of its
  member pages falls inside the 12 steps (e.g. "Systems & Advanced Labs" is entirely gold because it
  contains lab_36 — that does not mean every page in the cluster is on the spine).
- **Click a node to open its page**: every node carries a mermaid `click` directive that opens the
  page in a new tab (clustered nodes have no single destination, so they carry no `click` — use the
  legend table below instead). If your browser or viewer blocks the navigation, every link in the
  legend table and the rest of this page still works normally.
- **This is not a strict DAG**: a handful of pages list each other as prerequisites in both
  directions (page A explains half a concept and links to B for the rest; B in turn lists A under
  further reading) — the graph shows this as a back-and-forth pair of arrows. That is a faithful
  reflection of the site's actual cross-referencing, not an extraction error.
- **Two pages with a different edge source**: `tank_Q_and_energy_restoration` and
  `capstone_lc_end_to_end` do not carry the standard "Prerequisites / Next" breadcrumb (they are
  either an earlier-style page or the site's capstone/wrap-up page), so their edges were instead
  taken from the "Further Reading" links explicitly listed in the page body (copied verbatim from
  the page text — no relationship was added beyond what is actually written there). Apart from those
  two pages, all 236 edges (including a handful of "hands-on verification" pointers to the matching
  lab) come directly from markdown links inside the breadcrumb line.

## Full Dependency Map

```mermaid
graph LR
  subgraph SG_00_overview["00 - Overview"]
    n_00_overview_build_report["Build Report"]
    n_00_overview_changelog["Changelog"]
    n_00_overview_cheat_sheet["Cheat Sheet"]
    n_00_overview_index["Home: ISF & Phase Noise Overview"]
    n_00_overview_learning_path["Learning Path"]
    n_00_overview_notation["Unified Notation Table"]
  end
  subgraph SG_01_paper_map["01 - Paper Map"]
    n_01_paper_map_claims_cross_reference["Claims Cross-Reference C1-C13"]
    n_01_paper_map_equation_index["Equation Index"]
    n_01_paper_map_figure_index["Figure Index"]
    n_01_paper_map_paper_summary_table["Paper Summary Table"]
  end
  subgraph SG_02_foundations["02 - Foundations"]
    n_02_foundations_oscillator_phase["What Is Oscillator Phase?"]
    n_02_foundations_phase_vs_amplitude_noise["Why phase noise matters and why…"]
    n_02_foundations_lti_vs_ltv["LTI vs LTV"]
    n_02_foundations_tank_Q_and_energy_restoration["Tank Q & Energy Restoration"]
    n_02_foundations_stochastic_noise_basics["Stochastic Noise Basics"]
    n_02_foundations_psd_phase_noise_jitter["Phase Noise → Jitter"]
    n_02_foundations_jitter_kernels["Rigorous Derivation of the Jitt…"]
    n_02_foundations_allan_variance["Allan Variance"]
    n_02_foundations_dsp_view_of_phase_noise["The DSP View of Phase Noise"]
    n_02_foundations_exercises["Foundations Chapter Exercises"]
  end
  subgraph SG_03_isf_core_theory["03 - ISF Core Theory"]
    n_03_isf_core_theory_isf_definition["The Definition of the ISF"]
    n_03_isf_core_theory_impulse_to_phase_shift["Impulse → Phase Shift"]
    n_03_isf_core_theory_convolution_derivation["Impulse → Noise Convolution"]
    n_03_isf_core_theory_fourier_series_of_isf["Fourier Series of the ISF"]
    n_03_isf_core_theory_rms_isf["The rms ISF and the Parseval Re…"]
    n_03_isf_core_theory_asymmetric_isf_closed_form["Closed Forms for the Asymmetric…"]
    n_03_isf_core_theory_isf_from_waveform["ISF from Waveform: 3 Methods"]
    n_03_isf_core_theory_white_noise_to_phase_noise["How White Noise Becomes 1/f² Ph…"]
    n_03_isf_core_theory_flicker_noise_upconversion["Flicker noise upconversion into…"]
    n_03_isf_core_theory_lorentzian_linewidth["Lorentzian Linewidth"]
    n_03_isf_core_theory_diffusion_dictionary["Diffusion Dictionary κ/D/Linewidth/ADEV"]
    n_03_isf_core_theory_beyond_lorentzian["Beyond the Lorentzian"]
    n_03_isf_core_theory_effective_isf["Effective ISF (cyclostationary)"]
    n_03_isf_core_theory_capstone_lc_end_to_end["Capstone: LC End-to-End state→BER"]
    n_03_isf_core_theory_exercises["Core-Theory Chapter Exercises"]
  end
  subgraph SG_04_simulation_labs["04 - Simulation Labs"]
    g_lab_basic(["Foundations Labs (numerical_feeling / worked_examples / interactive_calculator / lab01-05)"])
    g_lab_noise(["Noise & Jitter Labs (lab06-12)"])
    g_lab_sys(["Systems & Advanced Labs (lab13-17, 32, 34, 36, final_exam)"])
  end
  subgraph SG_05_paper_deep_dives["05 - Paper Deep Dives"]
    n_05_paper_deep_dives_index["Paper Deep Dives"]
    n_05_paper_deep_dives_paper_001_general_theory_phase_noise["[P1] General Theory of Phase Noise"]
    n_05_paper_deep_dives_paper_002_jitter_phase_noise_ring["[P2] Ring Oscillator Jitter"]
    n_05_paper_deep_dives_paper_003_injection_locking_part1["[P3] Injection Locking Part I"]
    n_05_paper_deep_dives_paper_004_injection_locking_part2["[P4] Injection Locking Part II"]
    n_05_paper_deep_dives_paper_005_cross_coupled_sense_amp["[P5] Sense Amp (unrelated to ISF)"]
  end
  subgraph SG_06_design_insights["06 - Design Insights"]
    g_dsg_map(["Waveform & Device Mapping"])
    g_dsg_meas(["Measurement, Budget & Pitfalls"])
    g_dsg_sys(["System Clocking & References"])
    g_dsg_topo(["Real Topologies & Injection"])
    n_06_design_insights_exercises["Design Chapter Exercises"]
    n_06_design_insights_lc_vs_ring["LC vs ring oscillator through t…"]
    n_06_design_insights_pll_noise_budget["Complete PLL phase-noise budget…"]
    n_06_design_insights_serdes_clocking_connection["ISF → SerDes Clocking"]
    n_06_design_insights_symmetry["Waveform Symmetry and Flicker U…"]
    n_06_design_insights_tank_swing["Tank Swing & q_max"]
  end
  subgraph SG_99_appendix["99 - Appendix"]
    g_app_ref(["Reference Tools"])
    g_app_theory(["Rigorous Math Foundations"])
  end

  g_app_theory --> g_app_ref
  g_app_theory --> g_dsg_sys
  g_app_theory --> n_03_isf_core_theory_capstone_lc_end_to_end
  g_app_theory --> n_06_design_insights_symmetry
  g_dsg_map --> g_dsg_topo
  g_dsg_map --> n_03_isf_core_theory_isf_from_waveform
  g_dsg_map --> n_06_design_insights_serdes_clocking_connection
  g_dsg_map --> n_06_design_insights_symmetry
  g_dsg_map --> n_06_design_insights_tank_swing
  g_dsg_meas --> g_dsg_sys
  g_dsg_meas --> g_dsg_topo
  g_dsg_meas --> g_lab_sys
  g_dsg_meas --> n_00_overview_cheat_sheet
  g_dsg_meas --> n_03_isf_core_theory_lorentzian_linewidth
  g_dsg_meas --> n_06_design_insights_exercises
  g_dsg_meas --> n_06_design_insights_pll_noise_budget
  g_dsg_meas --> n_06_design_insights_serdes_clocking_connection
  g_dsg_sys --> g_dsg_meas
  g_dsg_sys --> n_06_design_insights_exercises
  g_dsg_sys --> n_06_design_insights_pll_noise_budget
  g_dsg_sys --> n_06_design_insights_serdes_clocking_connection
  g_dsg_topo --> g_dsg_meas
  g_dsg_topo --> g_lab_sys
  g_dsg_topo --> n_06_design_insights_lc_vs_ring
  g_dsg_topo --> n_06_design_insights_pll_noise_budget
  g_lab_basic --> g_lab_sys
  g_lab_basic --> n_03_isf_core_theory_capstone_lc_end_to_end
  g_lab_noise --> g_dsg_meas
  g_lab_noise --> n_03_isf_core_theory_capstone_lc_end_to_end
  g_lab_sys --> g_dsg_map
  g_lab_sys --> g_dsg_topo
  g_lab_sys --> n_05_paper_deep_dives_paper_004_injection_locking_part2
  n_00_overview_learning_path --> n_02_foundations_oscillator_phase
  n_00_overview_notation --> n_02_foundations_oscillator_phase
  n_00_overview_notation --> n_02_foundations_phase_vs_amplitude_noise
  n_00_overview_notation --> n_02_foundations_stochastic_noise_basics
  n_02_foundations_allan_variance --> n_03_isf_core_theory_diffusion_dictionary
  n_02_foundations_allan_variance --> n_06_design_insights_serdes_clocking_connection
  n_02_foundations_dsp_view_of_phase_noise --> n_02_foundations_jitter_kernels
  n_02_foundations_dsp_view_of_phase_noise --> n_02_foundations_psd_phase_noise_jitter
  n_02_foundations_exercises --> g_lab_sys
  n_02_foundations_exercises --> n_03_isf_core_theory_exercises
  n_02_foundations_exercises --> n_06_design_insights_exercises
  n_02_foundations_jitter_kernels --> n_02_foundations_allan_variance
  n_02_foundations_jitter_kernels --> n_06_design_insights_serdes_clocking_connection
  n_02_foundations_lti_vs_ltv --> g_app_theory
  n_02_foundations_lti_vs_ltv --> g_dsg_map
  n_02_foundations_lti_vs_ltv --> n_02_foundations_exercises
  n_02_foundations_lti_vs_ltv --> n_02_foundations_stochastic_noise_basics
  n_02_foundations_lti_vs_ltv --> n_03_isf_core_theory_impulse_to_phase_shift
  n_02_foundations_lti_vs_ltv --> n_05_paper_deep_dives_paper_001_general_theory_phase_noise
  n_02_foundations_oscillator_phase --> n_02_foundations_lti_vs_ltv
  n_02_foundations_oscillator_phase --> n_02_foundations_phase_vs_amplitude_noise
  n_02_foundations_oscillator_phase --> n_02_foundations_tank_Q_and_energy_restoration
  n_02_foundations_oscillator_phase --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_02_foundations_oscillator_phase --> n_03_isf_core_theory_convolution_derivation
  n_02_foundations_oscillator_phase --> n_03_isf_core_theory_impulse_to_phase_shift
  n_02_foundations_oscillator_phase --> n_03_isf_core_theory_isf_definition
  n_02_foundations_oscillator_phase --> n_05_paper_deep_dives_index
  n_02_foundations_oscillator_phase --> n_05_paper_deep_dives_paper_001_general_theory_phase_noise
  n_02_foundations_oscillator_phase --> n_05_paper_deep_dives_paper_005_cross_coupled_sense_amp
  n_02_foundations_phase_vs_amplitude_noise --> g_app_theory
  n_02_foundations_phase_vs_amplitude_noise --> n_02_foundations_lti_vs_ltv
  n_02_foundations_phase_vs_amplitude_noise --> n_03_isf_core_theory_isf_definition
  n_02_foundations_phase_vs_amplitude_noise --> n_05_paper_deep_dives_paper_004_injection_locking_part2
  n_02_foundations_psd_phase_noise_jitter --> g_app_theory
  n_02_foundations_psd_phase_noise_jitter --> g_dsg_meas
  n_02_foundations_psd_phase_noise_jitter --> g_dsg_sys
  n_02_foundations_psd_phase_noise_jitter --> n_02_foundations_allan_variance
  n_02_foundations_psd_phase_noise_jitter --> n_02_foundations_exercises
  n_02_foundations_psd_phase_noise_jitter --> n_02_foundations_jitter_kernels
  n_02_foundations_psd_phase_noise_jitter --> n_02_foundations_tank_Q_and_energy_restoration
  n_02_foundations_psd_phase_noise_jitter --> n_05_paper_deep_dives_paper_002_jitter_phase_noise_ring
  n_02_foundations_psd_phase_noise_jitter --> n_06_design_insights_serdes_clocking_connection
  n_02_foundations_stochastic_noise_basics --> n_02_foundations_dsp_view_of_phase_noise
  n_02_foundations_stochastic_noise_basics --> n_02_foundations_jitter_kernels
  n_02_foundations_stochastic_noise_basics --> n_02_foundations_psd_phase_noise_jitter
  n_02_foundations_stochastic_noise_basics --> n_03_isf_core_theory_beyond_lorentzian
  n_02_foundations_stochastic_noise_basics --> n_03_isf_core_theory_effective_isf
  n_02_foundations_stochastic_noise_basics --> n_03_isf_core_theory_lorentzian_linewidth
  n_02_foundations_stochastic_noise_basics --> n_03_isf_core_theory_rms_isf
  n_02_foundations_stochastic_noise_basics --> n_03_isf_core_theory_white_noise_to_phase_noise
  n_02_foundations_stochastic_noise_basics --> n_05_paper_deep_dives_paper_001_general_theory_phase_noise
  n_02_foundations_tank_Q_and_energy_restoration --> g_app_theory
  n_02_foundations_tank_Q_and_energy_restoration --> g_dsg_sys
  n_02_foundations_tank_Q_and_energy_restoration --> n_05_paper_deep_dives_paper_005_cross_coupled_sense_amp
  n_02_foundations_tank_Q_and_energy_restoration --> n_06_design_insights_lc_vs_ring
  n_02_foundations_tank_Q_and_energy_restoration --> n_06_design_insights_tank_swing
  n_03_isf_core_theory_asymmetric_isf_closed_form --> g_lab_sys
  n_03_isf_core_theory_asymmetric_isf_closed_form --> n_06_design_insights_symmetry
  n_03_isf_core_theory_beyond_lorentzian --> g_dsg_meas
  n_03_isf_core_theory_beyond_lorentzian --> n_02_foundations_allan_variance
  n_03_isf_core_theory_capstone_lc_end_to_end --> g_lab_sys
  n_03_isf_core_theory_convolution_derivation --> g_app_theory
  n_03_isf_core_theory_convolution_derivation --> n_03_isf_core_theory_fourier_series_of_isf
  n_03_isf_core_theory_convolution_derivation --> n_03_isf_core_theory_rms_isf
  n_03_isf_core_theory_convolution_derivation --> n_03_isf_core_theory_white_noise_to_phase_noise
  n_03_isf_core_theory_diffusion_dictionary --> g_lab_sys
  n_03_isf_core_theory_diffusion_dictionary --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_effective_isf --> g_dsg_topo
  n_03_isf_core_theory_effective_isf --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_effective_isf --> n_03_isf_core_theory_exercises
  n_03_isf_core_theory_exercises --> g_lab_sys
  n_03_isf_core_theory_exercises --> n_06_design_insights_exercises
  n_03_isf_core_theory_flicker_noise_upconversion --> g_dsg_map
  n_03_isf_core_theory_flicker_noise_upconversion --> g_lab_noise
  n_03_isf_core_theory_flicker_noise_upconversion --> n_03_isf_core_theory_asymmetric_isf_closed_form
  n_03_isf_core_theory_flicker_noise_upconversion --> n_03_isf_core_theory_beyond_lorentzian
  n_03_isf_core_theory_flicker_noise_upconversion --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_flicker_noise_upconversion --> n_03_isf_core_theory_exercises
  n_03_isf_core_theory_flicker_noise_upconversion --> n_06_design_insights_symmetry
  n_03_isf_core_theory_fourier_series_of_isf --> g_app_theory
  n_03_isf_core_theory_fourier_series_of_isf --> g_dsg_map
  n_03_isf_core_theory_fourier_series_of_isf --> g_dsg_meas
  n_03_isf_core_theory_fourier_series_of_isf --> g_lab_basic
  n_03_isf_core_theory_fourier_series_of_isf --> g_lab_sys
  n_03_isf_core_theory_fourier_series_of_isf --> n_03_isf_core_theory_asymmetric_isf_closed_form
  n_03_isf_core_theory_fourier_series_of_isf --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_fourier_series_of_isf --> n_03_isf_core_theory_exercises
  n_03_isf_core_theory_fourier_series_of_isf --> n_03_isf_core_theory_flicker_noise_upconversion
  n_03_isf_core_theory_fourier_series_of_isf --> n_03_isf_core_theory_rms_isf
  n_03_isf_core_theory_fourier_series_of_isf --> n_03_isf_core_theory_white_noise_to_phase_noise
  n_03_isf_core_theory_fourier_series_of_isf --> n_05_paper_deep_dives_paper_003_injection_locking_part1
  n_03_isf_core_theory_fourier_series_of_isf --> n_06_design_insights_symmetry
  n_03_isf_core_theory_impulse_to_phase_shift --> g_dsg_map
  n_03_isf_core_theory_impulse_to_phase_shift --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_impulse_to_phase_shift --> n_03_isf_core_theory_convolution_derivation
  n_03_isf_core_theory_impulse_to_phase_shift --> n_03_isf_core_theory_fourier_series_of_isf
  n_03_isf_core_theory_impulse_to_phase_shift --> n_03_isf_core_theory_isf_definition
  n_03_isf_core_theory_impulse_to_phase_shift --> n_06_design_insights_tank_swing
  n_03_isf_core_theory_isf_definition --> g_app_theory
  n_03_isf_core_theory_isf_definition --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_isf_definition --> n_03_isf_core_theory_convolution_derivation
  n_03_isf_core_theory_isf_definition --> n_03_isf_core_theory_effective_isf
  n_03_isf_core_theory_isf_definition --> n_03_isf_core_theory_exercises
  n_03_isf_core_theory_isf_definition --> n_03_isf_core_theory_fourier_series_of_isf
  n_03_isf_core_theory_isf_definition --> n_03_isf_core_theory_isf_from_waveform
  n_03_isf_core_theory_isf_definition --> n_05_paper_deep_dives_index
  n_03_isf_core_theory_isf_from_waveform --> g_app_theory
  n_03_isf_core_theory_isf_from_waveform --> g_lab_sys
  n_03_isf_core_theory_lorentzian_linewidth --> g_dsg_topo
  n_03_isf_core_theory_lorentzian_linewidth --> n_03_isf_core_theory_beyond_lorentzian
  n_03_isf_core_theory_lorentzian_linewidth --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_lorentzian_linewidth --> n_03_isf_core_theory_diffusion_dictionary
  n_03_isf_core_theory_rms_isf --> n_03_isf_core_theory_asymmetric_isf_closed_form
  n_03_isf_core_theory_rms_isf --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_rms_isf --> n_03_isf_core_theory_effective_isf
  n_03_isf_core_theory_rms_isf --> n_03_isf_core_theory_exercises
  n_03_isf_core_theory_rms_isf --> n_03_isf_core_theory_flicker_noise_upconversion
  n_03_isf_core_theory_rms_isf --> n_03_isf_core_theory_lorentzian_linewidth
  n_03_isf_core_theory_rms_isf --> n_03_isf_core_theory_white_noise_to_phase_noise
  n_03_isf_core_theory_rms_isf --> n_06_design_insights_lc_vs_ring
  n_03_isf_core_theory_white_noise_to_phase_noise --> g_app_theory
  n_03_isf_core_theory_white_noise_to_phase_noise --> g_dsg_map
  n_03_isf_core_theory_white_noise_to_phase_noise --> g_dsg_meas
  n_03_isf_core_theory_white_noise_to_phase_noise --> g_dsg_sys
  n_03_isf_core_theory_white_noise_to_phase_noise --> g_dsg_topo
  n_03_isf_core_theory_white_noise_to_phase_noise --> g_lab_noise
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_02_foundations_allan_variance
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_02_foundations_dsp_view_of_phase_noise
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_02_foundations_psd_phase_noise_jitter
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_03_isf_core_theory_diffusion_dictionary
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_03_isf_core_theory_exercises
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_03_isf_core_theory_flicker_noise_upconversion
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_03_isf_core_theory_lorentzian_linewidth
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_06_design_insights_pll_noise_budget
  n_03_isf_core_theory_white_noise_to_phase_noise --> n_06_design_insights_tank_swing
  n_05_paper_deep_dives_paper_001_general_theory_phase_noise --> n_05_paper_deep_dives_paper_002_jitter_phase_noise_ring
  n_05_paper_deep_dives_paper_001_general_theory_phase_noise --> n_05_paper_deep_dives_paper_003_injection_locking_part1
  n_05_paper_deep_dives_paper_001_general_theory_phase_noise --> n_05_paper_deep_dives_paper_004_injection_locking_part2
  n_05_paper_deep_dives_paper_001_general_theory_phase_noise --> n_05_paper_deep_dives_paper_005_cross_coupled_sense_amp
  n_05_paper_deep_dives_paper_003_injection_locking_part1 --> g_dsg_topo
  n_05_paper_deep_dives_paper_003_injection_locking_part1 --> g_lab_sys
  n_05_paper_deep_dives_paper_003_injection_locking_part1 --> n_05_paper_deep_dives_paper_004_injection_locking_part2
  n_06_design_insights_exercises --> g_lab_sys
  n_06_design_insights_lc_vs_ring --> g_dsg_meas
  n_06_design_insights_lc_vs_ring --> g_dsg_topo
  n_06_design_insights_lc_vs_ring --> n_06_design_insights_exercises
  n_06_design_insights_lc_vs_ring --> n_06_design_insights_pll_noise_budget
  n_06_design_insights_lc_vs_ring --> n_06_design_insights_serdes_clocking_connection
  n_06_design_insights_pll_noise_budget --> g_dsg_sys
  n_06_design_insights_pll_noise_budget --> g_lab_sys
  n_06_design_insights_pll_noise_budget --> n_06_design_insights_exercises
  n_06_design_insights_serdes_clocking_connection --> g_dsg_meas
  n_06_design_insights_serdes_clocking_connection --> n_03_isf_core_theory_capstone_lc_end_to_end
  n_06_design_insights_serdes_clocking_connection --> n_06_design_insights_exercises
  n_06_design_insights_serdes_clocking_connection --> n_06_design_insights_pll_noise_budget
  n_06_design_insights_symmetry --> g_dsg_map
  n_06_design_insights_symmetry --> g_dsg_meas
  n_06_design_insights_symmetry --> g_dsg_topo
  n_06_design_insights_symmetry --> n_06_design_insights_exercises
  n_06_design_insights_symmetry --> n_06_design_insights_serdes_clocking_connection
  n_06_design_insights_tank_swing --> g_dsg_meas
  n_06_design_insights_tank_swing --> g_dsg_topo
  n_06_design_insights_tank_swing --> n_06_design_insights_exercises
  n_06_design_insights_tank_swing --> n_06_design_insights_lc_vs_ring
  n_06_design_insights_tank_swing --> n_06_design_insights_serdes_clocking_connection

  classDef spine fill:#ffd54f,stroke:#e65100,stroke-width:3px,color:#3e2723;
  class g_dsg_meas,g_dsg_sys,g_dsg_topo,g_lab_basic,g_lab_noise,g_lab_sys,n_02_foundations_allan_variance,n_02_foundations_jitter_kernels,n_02_foundations_lti_vs_ltv,n_02_foundations_oscillator_phase,n_02_foundations_phase_vs_amplitude_noise,n_02_foundations_psd_phase_noise_jitter,n_03_isf_core_theory_asymmetric_isf_closed_form,n_03_isf_core_theory_beyond_lorentzian,n_03_isf_core_theory_capstone_lc_end_to_end,n_03_isf_core_theory_convolution_derivation,n_03_isf_core_theory_diffusion_dictionary,n_03_isf_core_theory_flicker_noise_upconversion,n_03_isf_core_theory_fourier_series_of_isf,n_03_isf_core_theory_impulse_to_phase_shift,n_03_isf_core_theory_isf_definition,n_03_isf_core_theory_isf_from_waveform,n_03_isf_core_theory_lorentzian_linewidth,n_03_isf_core_theory_rms_isf,n_03_isf_core_theory_white_noise_to_phase_noise,n_05_paper_deep_dives_paper_003_injection_locking_part1,n_05_paper_deep_dives_paper_004_injection_locking_part2,n_06_design_insights_lc_vs_ring,n_06_design_insights_serdes_clocking_connection,n_06_design_insights_symmetry spine;

  click n_00_overview_build_report "/00_overview/build_report" "_blank"
  click n_00_overview_changelog "/00_overview/changelog" "_blank"
  click n_00_overview_cheat_sheet "/00_overview/cheat_sheet" "_blank"
  click n_00_overview_index "/00_overview/index" "_blank"
  click n_00_overview_learning_path "/00_overview/learning_path" "_blank"
  click n_00_overview_notation "/00_overview/notation" "_blank"
  click n_01_paper_map_claims_cross_reference "/01_paper_map/claims_cross_reference" "_blank"
  click n_01_paper_map_equation_index "/01_paper_map/equation_index" "_blank"
  click n_01_paper_map_figure_index "/01_paper_map/figure_index" "_blank"
  click n_01_paper_map_paper_summary_table "/01_paper_map/paper_summary_table" "_blank"
  click n_05_paper_deep_dives_index "/05_paper_deep_dives/index" "_blank"
  click n_05_paper_deep_dives_paper_001_general_theory_phase_noise "/05_paper_deep_dives/paper_001_general_theory_phase_noise" "_blank"
  click n_05_paper_deep_dives_paper_002_jitter_phase_noise_ring "/05_paper_deep_dives/paper_002_jitter_phase_noise_ring" "_blank"
  click n_05_paper_deep_dives_paper_003_injection_locking_part1 "/05_paper_deep_dives/paper_003_injection_locking_part1" "_blank"
  click n_05_paper_deep_dives_paper_004_injection_locking_part2 "/05_paper_deep_dives/paper_004_injection_locking_part2" "_blank"
  click n_05_paper_deep_dives_paper_005_cross_coupled_sense_amp "/05_paper_deep_dives/paper_005_cross_coupled_sense_amp" "_blank"
  click n_02_foundations_allan_variance "/02_foundations/allan_variance" "_blank"
  click n_02_foundations_dsp_view_of_phase_noise "/02_foundations/dsp_view_of_phase_noise" "_blank"
  click n_02_foundations_exercises "/02_foundations/exercises" "_blank"
  click n_02_foundations_jitter_kernels "/02_foundations/jitter_kernels" "_blank"
  click n_02_foundations_lti_vs_ltv "/02_foundations/lti_vs_ltv" "_blank"
  click n_02_foundations_oscillator_phase "/02_foundations/oscillator_phase" "_blank"
  click n_02_foundations_phase_vs_amplitude_noise "/02_foundations/phase_vs_amplitude_noise" "_blank"
  click n_02_foundations_psd_phase_noise_jitter "/02_foundations/psd_phase_noise_jitter" "_blank"
  click n_02_foundations_stochastic_noise_basics "/02_foundations/stochastic_noise_basics" "_blank"
  click n_02_foundations_tank_Q_and_energy_restoration "/02_foundations/tank_Q_and_energy_restoration" "_blank"
  click n_03_isf_core_theory_asymmetric_isf_closed_form "/03_isf_core_theory/asymmetric_isf_closed_form" "_blank"
  click n_03_isf_core_theory_beyond_lorentzian "/03_isf_core_theory/beyond_lorentzian" "_blank"
  click n_03_isf_core_theory_capstone_lc_end_to_end "/03_isf_core_theory/capstone_lc_end_to_end" "_blank"
  click n_03_isf_core_theory_convolution_derivation "/03_isf_core_theory/convolution_derivation" "_blank"
  click n_03_isf_core_theory_diffusion_dictionary "/03_isf_core_theory/diffusion_dictionary" "_blank"
  click n_03_isf_core_theory_effective_isf "/03_isf_core_theory/effective_isf" "_blank"
  click n_03_isf_core_theory_exercises "/03_isf_core_theory/exercises" "_blank"
  click n_03_isf_core_theory_flicker_noise_upconversion "/03_isf_core_theory/flicker_noise_upconversion" "_blank"
  click n_03_isf_core_theory_fourier_series_of_isf "/03_isf_core_theory/fourier_series_of_isf" "_blank"
  click n_03_isf_core_theory_impulse_to_phase_shift "/03_isf_core_theory/impulse_to_phase_shift" "_blank"
  click n_03_isf_core_theory_isf_definition "/03_isf_core_theory/isf_definition" "_blank"
  click n_03_isf_core_theory_isf_from_waveform "/03_isf_core_theory/isf_from_waveform" "_blank"
  click n_03_isf_core_theory_lorentzian_linewidth "/03_isf_core_theory/lorentzian_linewidth" "_blank"
  click n_03_isf_core_theory_rms_isf "/03_isf_core_theory/rms_isf" "_blank"
  click n_03_isf_core_theory_white_noise_to_phase_noise "/03_isf_core_theory/white_noise_to_phase_noise" "_blank"
  click n_06_design_insights_exercises "/06_design_insights/exercises" "_blank"
  click n_06_design_insights_lc_vs_ring "/06_design_insights/lc_vs_ring" "_blank"
  click n_06_design_insights_pll_noise_budget "/06_design_insights/pll_noise_budget" "_blank"
  click n_06_design_insights_serdes_clocking_connection "/06_design_insights/serdes_clocking_connection" "_blank"
  click n_06_design_insights_symmetry "/06_design_insights/symmetry" "_blank"
  click n_06_design_insights_tank_swing "/06_design_insights/tank_swing" "_blank"
```

## How 92 pages compress to 56 nodes

| Chapter | Original pages | Nodes in graph | Treatment |
|---|---|---|---|
| 00 - Overview | 6 | 6 | One node per page (small chapter, mostly reference hubs) |
| 01 - Paper Map | 4 | 4 | One node per page |
| 02 - Foundations | 10 | 10 | One node per page (main spine, kept individual per the map's rule) |
| 03 - ISF Core Theory | 15 | 15 | One node per page (main spine, kept individual per the map's rule) |
| 04 - Simulation Labs | 24 | 3 | Clustered by the sidebar's three sub-categories (Foundations Labs / Noise & Jitter Labs / Systems & Advanced Labs) |
| 05 - Paper Deep Dives | 6 | 6 | One node per page (each page maps 1:1 to one paper — small in count but high in meaning, not clustered) |
| 06 - Design Insights | 20 | 10 | The 6 highest-degree pages (symmetry, tank_swing, lc_vs_ring, pll_noise_budget, serdes_clocking_connection, exercises) keep their own node; the remaining 14 pages are clustered into 4 themed groups |
| 99 - Appendix | 7 | 2 | Clustered into "Rigorous Math Foundations" and "Reference Tools" |
| **Total** | **92** | **56** | |

## Top-8 Hub Pages

"Degree" = a page's in-degree + out-degree in the **page-level** directed graph (before clustering)
extracted from the breadcrumbs. A high in-degree means "this page itself lists many prerequisites";
a high out-degree means "many downstream pages list this page as their prerequisite" — pages with a
high out-degree are usually the site's real **conceptual hubs**. Ties are broken by: higher degree
first, then higher in-degree, then alphabetically by page id (see the note below).

| Rank | Page | Chapter | Degree (in+out) | Listed as prereq (in) | Listed as prereq for (out) |
|---|---|---|---|---|---|
| 1 | [How White Noise Becomes 1/f² Phase Noise](/03_isf_core_theory/white_noise_to_phase_noise) | 03_isf_core_theory | 24 | 4 | 20 |
| 2 | [Capstone — One Ideal LC from State Equations to BER (Fully Rigorous, End to End)](/03_isf_core_theory/capstone_lc_end_to_end) | 03_isf_core_theory | 18 | 17 | 1 |
| 3 | [Fourier Series of the ISF](/03_isf_core_theory/fourier_series_of_isf) | 03_isf_core_theory | 16 | 3 | 13 |
| 4 | [From ISF to SerDes Clocking](/06_design_insights/serdes_clocking_connection) | 06_design_insights | 14 | 10 | 4 |
| 5 | [Design Chapter Exercises (with Full Solutions)](/06_design_insights/exercises) | 06_design_insights | 13 | 10 | 3 |
| 6 | [Phase Noise → Jitter](/02_foundations/psd_phase_noise_jitter) | 02_foundations | 13 | 3 | 10 |
| 7 | [What Is Oscillator Phase?](/02_foundations/oscillator_phase) | 02_foundations | 13 | 2 | 11 |
| 8 | [Tank Q and Energy Restoration](/02_foundations/tank_Q_and_energy_restoration) | 02_foundations | 12 | 7 | 5 |

> Note: this column is computed from the **full** breadcrumb extraction — every wording variant
> used across the site (`> Prerequisites:`, `> **Prerequisites**:`, `> **Prerequisite Reading**:`,
> `> **Prerequisite knowledge (read first)**:`, and the lab pages' "breadcrumb ... upstream/downstream"
> style — not only the single canonical format; the two breadcrumb-less exception pages
> `tank_Q_and_energy_restoration` and `capstone_lc_end_to_end` still use their "Further Reading" links),
> which is more complete — and closer to the site's true link volume — than counting only the one
> canonical format. Ranks 5-7 are tied at degree 13; the tie-break rule above (higher in-degree first)
> orders them `exercises` (in=10) > `psd_phase_noise_jitter` (in=3) > `oscillator_phase` (in=2).
> Rank 8 (degree 12) is tied with `03_isf_core_theory/isf_definition` (in=3, out=9); because
> `tank_Q_and_energy_restoration` has the higher in-degree (7 > 3) it takes rank 8, with
> `isf_definition` just behind at rank 9. Four more pages sit at degree 11: `06_design_insights/symmetry`,
> `06_design_insights/tank_swing`, `03_isf_core_theory/rms_isf`, and `02_foundations/stochastic_noise_basics`
> — genuine hubs in their own right and worth noting on the map. `symmetry`, `lc_vs_ring`, `tank_swing`,
> `isf_definition`, and `tank_Q_and_energy_restoration` all kept their own node (not clustered)
> precisely because of their high degree, so they are easy to spot in the 02/03/06
> sections of the diagram.

## Grouped-Node Legend

Clustered nodes have no single destination, so they carry no `click`; the tables below list, by
chapter, exactly which pages each clustered node contains.

### 04 - Simulation Labs

**Foundations Labs (numerical_feeling / worked_examples / interactive_calculator / lab01-05)** (node `g_lab_basic`):
  [Interactive Calculator](/04_simulation_labs/interactive_calculator), [Lab 01 — Sinusoidal Oscillator and the Phase/Amplitude Geometry of the Limit Cycle](/04_simulation_labs/lab_01_sinusoidal_oscillator), [Lab 02 — Ideal LC oscillator toy model: Γ(θ) = −sin θ and charge linearity](/04_simulation_labs/lab_02_lc_oscillator_toy_model), [Lab 03 — Ring-oscillator toy model: accumulated-jitter random walk and ISF comparison](/04_simulation_labs/lab_03_ring_oscillator_toy_model), [Lab 04 — impulse injection sweep and LTI vs LTV](/04_simulation_labs/lab_04_impulse_injection_sweep), [Lab 05 — ISF Fourier coefficients and Parseval](/04_simulation_labs/lab_05_isf_fourier_coefficients), [Numerical Feeling](/04_simulation_labs/numerical_feeling), [Worked Examples](/04_simulation_labs/worked_examples)

**Noise & Jitter Labs (lab06-12)** (node `g_lab_noise`):
  [Lab 06 — White Noise → 1/f² Phase Noise](/04_simulation_labs/lab_06_white_noise_phase_noise), [Lab 07 — 1/f Noise Upconversion and ISF Symmetry](/04_simulation_labs/lab_07_flicker_noise_upconversion), [Lab 08 — rms Jitter by Integrating L(f)](/04_simulation_labs/lab_08_jitter_integration), [Lab 09 — Design trade-off scaling synthesis](/04_simulation_labs/lab_09_design_tradeoffs), [Lab 10 — how phase noise smears the carrier into an RF skirt](/04_simulation_labs/lab_10_rf_spectrum), [Lab 11 — Monte Carlo accumulated jitter — RJ is Gaussian, σ grows as √ΔN](/04_simulation_labs/lab_11_monte_carlo_jitter), [Lab 12 — From jitter to eye to BER (SerDes bathtub)](/04_simulation_labs/lab_12_serdes_eye_ber)

**Systems & Advanced Labs (lab13-17, 32, 34, 36, final_exam)** (node `g_lab_sys`):
  [Final Exam: A 5 GHz LC VCO into a 25 Gb/s SerDes, End to End](/04_simulation_labs/final_exam), [Lab 13 — PLL/CDR jitter transfer: VCO high-pass, reference low-pass](/04_simulation_labs/lab_13_pll_cdr_transfer), [Lab 14 — Cyclostationary noise and the effective ISF](/04_simulation_labs/lab_14_cyclostationary_isf), [Lab 15 — ISF of a Nonlinear Oscillator (van der Pol)](/04_simulation_labs/lab_15_nonlinear_isf), [Lab 16 — Leeson Model vs ISF Model (Three-Region Comparison)](/04_simulation_labs/lab_16_leeson_vs_isf), [Lab 17 — Design Sweeps: Three Design Curves for swing / Γrms / N](/04_simulation_labs/lab_17_design_tradeoffs), [Lab 32 — MOS Level-1 Equation-Level Ring: Extracting the ISF from Transistor Equations](/04_simulation_labs/lab_32_mos_level1_ring), [Lab 34 — The N·f0 Selection Rule for Correlated Supply/Substrate Noise (P2 Eq.37–38)](/04_simulation_labs/lab_34_correlated_supply), [Lab 36 — Lock-Acquisition Transient and Noise-Induced Cycle Slips](/04_simulation_labs/lab_36_lock_acquisition)

### 06 - Design Insights

**Waveform & Device Mapping** (node `g_dsg_map`):
  [Device noise → ISF harmonics mapping](/06_design_insights/device_noise_mapping), [Waveform slope and phase sensitivity](/06_design_insights/waveform_slope)

**Measurement, Budget & Pitfalls** (node `g_dsg_meas`):
  [ADC aperture jitter: how clock jitter eats SNR and ENOB](/06_design_insights/adc_aperture_jitter), [Common Mistakes Showroom: 12 Real-World Landmines](/06_design_insights/common_mistakes), [DJ and the Dual-Dirac Model](/06_design_insights/dj_dual_dirac), [The Theoretical Ceiling of FOM](/06_design_insights/fom_limit), [Phase-noise measurement and spurs](/06_design_insights/measurement_and_spurs)

**System Clocking & References** (node `g_dsg_sys`):
  [Clock-chain noise accounting: ×N, ÷N, PLL, buffer — a one-page lookup table](/06_design_insights/clock_chain_budget), [Reference oscillators: crystal and MEMS phase noise](/06_design_insights/reference_oscillators), [Sampling / sub-sampling PLL — kicking the divider out of the loop](/06_design_insights/sampling_pll)

**Real Topologies & Injection** (node `g_dsg_topo`):
  [Noise shaping under injection locking and the injection-pulling spectrum](/06_design_insights/injection_locking_noise), [Quadrature generation and coupled-oscillator phase noise](/06_design_insights/quadrature_and_coupled_oscillators), [ISF in real topologies: cross-coupled LC VCO, Colpitts, CMOS ring stage](/06_design_insights/real_oscillator_topologies), [Tuning-line and supply-pushing phase noise](/06_design_insights/varactor_tuning_supply_pushing)

### 99 - Appendix

**Reference Tools** (node `g_app_ref`):
  [Chinese–English Glossary](/99_appendix/glossary), [Python Environment](/99_appendix/python_environment), [References](/99_appendix/references)

**Rigorous Math Foundations** (node `g_app_theory`):
  [Floquet / adjoint / PPV: the rigorous foundation of the ISF](/99_appendix/derivation_floquet_ppv), [Leeson Model Derivation and ISF Comparison](/99_appendix/derivation_leeson), [Rigorous LTV framework: Zadeh's time-varying transfer function and the harmonic transfer matrix](/99_appendix/ltv_htm), [Math Toolbox — Math Identities](/99_appendix/math_identities)

## Key takeaways

- Every edge on this map comes from a page's own declared "Prerequisites / Next" (two exception
  pages use "Further Reading" instead, see above) — it is a mirror of the site's **actual**
  dependency structure, not a redesigned "ideal" teaching order (the ideal order is still the
  [learning path](/00_overview/learning_path)'s twelve steps, highlighted in gold here).
- 92 pages -> 56 nodes: the two core chapters (02/03) keep one node per page as the authoring spec
  requires; chapter 04 is fully clustered, and 06/99 are partially clustered by connectivity, so the
  map stays a size you can scan at a glance.
- The highest-degree hubs are not in 00/01 (reference/dictionary pages are rarely listed as anyone's
  prerequisite, so their breadcrumb-degree is naturally low) — they are white-noise-to-1/f²,
  SerDes clocking, the capstone, the ISF Fourier series, and the chapter-end exercise pages. These
  are where the site's teaching logic genuinely converges.
- The graph is not a strict DAG: a few pages list each other as mutual prerequisites — that is a
  faithful reflection of the site, not an extraction bug.

## Further Reading

- Full write-up of the twelve-step learning path: [learning_path](/00_overview/learning_path)
- How the five papers divide the work, at a glance: [paper_summary_table](/01_paper_map/paper_summary_table)
- Every equation -> its derivation page -> its paper source: [equation_index](/01_paper_map/equation_index)
- One-page formula and numeric cheat sheet: [cheat_sheet](/00_overview/cheat_sheet)
- Site-wide notation table: [notation](/00_overview/notation)
