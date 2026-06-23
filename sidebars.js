// @ts-check
// Explicit sidebar so the teaching path order is fully controlled.

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  mainSidebar: [
    {
      type: 'category',
      label: '00 · 課程導覽 Overview',
      collapsed: false,
      items: [
        '00_overview/index',
        '00_overview/learning_path',
        '00_overview/notation',
        '00_overview/cheat_sheet',
        '00_overview/build_report',
      ],
    },
    {
      type: 'category',
      label: '01 · 論文地圖 Paper Map',
      collapsed: true,
      items: [
        '01_paper_map/paper_summary_table',
        '01_paper_map/equation_index',
        '01_paper_map/figure_index',
        '01_paper_map/claims_cross_reference',
      ],
    },
    {
      type: 'category',
      label: '02 · 基礎 Foundations',
      collapsed: true,
      items: [
        '02_foundations/oscillator_phase',
        '02_foundations/tank_Q_and_energy_restoration',
        '02_foundations/phase_vs_amplitude_noise',
        '02_foundations/lti_vs_ltv',
        '02_foundations/stochastic_noise_basics',
        '02_foundations/psd_phase_noise_jitter',
        '02_foundations/allan_variance',
        '02_foundations/dsp_view_of_phase_noise',
        '02_foundations/exercises',
      ],
    },
    {
      type: 'category',
      label: '03 · ISF 核心理論 Core Theory',
      collapsed: true,
      items: [
        '03_isf_core_theory/isf_definition',
        '03_isf_core_theory/impulse_to_phase_shift',
        '03_isf_core_theory/convolution_derivation',
        '03_isf_core_theory/fourier_series_of_isf',
        '03_isf_core_theory/white_noise_to_phase_noise',
        '03_isf_core_theory/lorentzian_linewidth',
        '03_isf_core_theory/flicker_noise_upconversion',
        '03_isf_core_theory/rms_isf',
        '03_isf_core_theory/effective_isf',
        '03_isf_core_theory/capstone_lc_end_to_end',
        '03_isf_core_theory/exercises',
      ],
    },
    {
      type: 'category',
      label: '04 · 模擬實驗 Simulation Labs',
      collapsed: true,
      items: [
        {
          type: 'category',
          label: '基礎手感',
          collapsed: true,
          items: [
            '04_simulation_labs/numerical_feeling',
            '04_simulation_labs/worked_examples',
            '04_simulation_labs/interactive_calculator',
            '04_simulation_labs/lab_01_sinusoidal_oscillator',
            '04_simulation_labs/lab_02_lc_oscillator_toy_model',
            '04_simulation_labs/lab_03_ring_oscillator_toy_model',
            '04_simulation_labs/lab_04_impulse_injection_sweep',
            '04_simulation_labs/lab_05_isf_fourier_coefficients',
          ],
        },
        {
          type: 'category',
          label: '雜訊與抖動',
          collapsed: true,
          items: [
            '04_simulation_labs/lab_06_white_noise_phase_noise',
            '04_simulation_labs/lab_07_flicker_noise_upconversion',
            '04_simulation_labs/lab_08_jitter_integration',
            {
              type: 'doc',
              id: '04_simulation_labs/lab_09_design_tradeoffs',
              label: 'Lab 09 — 設計取捨入門',
            },
            '04_simulation_labs/lab_10_rf_spectrum',
            '04_simulation_labs/lab_11_monte_carlo_jitter',
            '04_simulation_labs/lab_12_serdes_eye_ber',
          ],
        },
        {
          type: 'category',
          label: '系統與進階',
          collapsed: true,
          items: [
            '04_simulation_labs/lab_13_pll_cdr_transfer',
            '04_simulation_labs/lab_14_cyclostationary_isf',
            '04_simulation_labs/lab_15_nonlinear_isf',
            '04_simulation_labs/lab_16_leeson_vs_isf',
            {
              type: 'doc',
              id: '04_simulation_labs/lab_17_design_tradeoffs',
              label: 'Lab 17 — 設計掃描進階',
            },
          ],
        },
      ],
    },
    {
      type: 'category',
      label: '05 · 論文逐篇精讀 Paper Deep Dives',
      collapsed: true,
      items: [
        '05_paper_deep_dives/index',
        '05_paper_deep_dives/paper_001_general_theory_phase_noise',
        '05_paper_deep_dives/paper_002_jitter_phase_noise_ring',
        '05_paper_deep_dives/paper_003_injection_locking_part1',
        '05_paper_deep_dives/paper_004_injection_locking_part2',
        '05_paper_deep_dives/paper_005_cross_coupled_sense_amp',
      ],
    },
    {
      type: 'category',
      label: '06 · 設計直覺 Design Insights',
      collapsed: true,
      items: [
        '06_design_insights/symmetry',
        '06_design_insights/waveform_slope',
        '06_design_insights/tank_swing',
        '06_design_insights/device_noise_mapping',
        '06_design_insights/lc_vs_ring',
        '06_design_insights/serdes_clocking_connection',
        '06_design_insights/pll_noise_budget',
        '06_design_insights/real_oscillator_topologies',
        '06_design_insights/varactor_tuning_supply_pushing',
        '06_design_insights/quadrature_and_coupled_oscillators',
        '06_design_insights/measurement_and_spurs',
        '06_design_insights/exercises',
      ],
    },
    {
      type: 'category',
      label: '99 · 附錄 Appendix',
      collapsed: true,
      items: [
        '99_appendix/math_identities',
        '99_appendix/ltv_htm',
        '99_appendix/derivation_floquet_ppv',
        '99_appendix/derivation_leeson',
        '99_appendix/python_environment',
        '99_appendix/glossary',
        '99_appendix/references',
      ],
    },
  ],
};

module.exports = sidebars;
