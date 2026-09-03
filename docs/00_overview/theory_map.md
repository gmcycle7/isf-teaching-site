---
title: "全站理論地圖 Theory Map"
description: "把全站 92 頁壓成一張 56 節點的 mermaid 依賴圖：每條邊都從每頁的「先備／接下來」麵包屑列直接抽取；12 步學習路徑主幹以金色標出；並附連結度最高的 8 個樞紐頁面與分組節點圖例。"
---

# 全站理論地圖 Theory Map

> 先備：[learning_path](/00_overview/learning_path)（十二步主幹的頁面順序，本頁圖上以金色標出對應節點）、[notation](/00_overview/notation)（符號表；本頁不需要新符號，但連結圖裡出現的每個頁名都可在此查對應概念）｜接下來：[cheat_sheet](/00_overview/cheat_sheet)、[paper_summary_table](/01_paper_map/paper_summary_table)

這頁只做一件事：把全站 **92 頁**（zh；每頁在 `i18n/en/` 都有英文鏡像）之間「誰要先讀誰」的
關係，畫成**一張圖**。圖不是我手畫的——邊是**逐頁掃描每一頁開頭的「> 先備：…｜接下來：…」
（或舊格式「> **前置閱讀**：…」）麵包屑列**、用程式抽取連結後自動生成的，所以它反映的是**網站
實際的連結結構**，不是憑印象畫的示意圖。

## 怎麼讀這張圖 How to read this map

- **箭頭方向 = 先備關係**：`A --> B` 讀作「A 是 B 的先備／A 教的東西 B 會直接用到」。跟著箭頭走
  就是一條合理的閱讀順序；反過來，一個節點的**入邊**（箭頭指向它的）就是它列出的先備頁，
  **出邊**（它指向別人的）就是把它列為先備的下游頁。
- **方形節點**＝單一頁面（02 基礎、03 核心理論兩章因為是主幹，**逐頁**畫成獨立節點；00/01/05
  三個小章節也逐頁畫）。**圓角節點**＝把好幾頁**收攏**成一叢的分組節點（04 模擬實驗全部收攏、
  06 設計直覺與 99 附錄收攏度數較低的頁面），因為 92 頁若逐一畫節點會超過可讀上限——分組後全圖
  只剩 **56 個節點**（見下方「節點數如何從 92 頁壓到 56 個」表）。每個分組節點底下實際包含哪些頁，
  列在下方「分組節點圖例」。
- **金色高亮**＝[學習路徑](/00_overview/learning_path) 十二步主幹碰到的節點。這是全站建議的**主幹**，其餘節點是主幹之外的延伸、深化或參考頁。
  一個分組節點只要**任一**成員頁落在 12 步裡，整個分組節點就標金色（例如「系統與進階 Labs」
  因為含 lab_36 而整塊金色，不代表組內每一頁都是主幹）。
- **點節點可直接開頁**：每個節點都掛了 mermaid `click` 指令，滑鼠點下去會在新分頁開啟該頁
  （分組節點沒有單一目的地，所以不掛 click——請改用下方圖例表的連結）。若你的瀏覽器 / 檢視器
  封鎖了跳轉，圖例表與下面所有連結一樣可用。
- **這不是嚴格的 DAG**：少數頁彼此互為「先備」（例如 A 講一半連去 B 補概念、B 又把 A 列為延伸），
  圖上會看到一來一往的雙箭頭——這忠實反映網站的實際交叉引用，不是抽取錯誤。
- **兩個例外的邊來源**：`tank_Q_and_energy_restoration` 與 `capstone_lc_end_to_end` 兩頁沒有標準
  「先備／接下來」麵包屑列（它們是較早或屬於全站收官性質的頁面），這兩頁的邊改採頁面本文明列的
  「延伸閱讀」連結（見頁面原文，連結逐字照抄、未新增未列出的關係）。除此之外全部 236 條邊
  （含極少數「動手驗證」提示連去對應 lab 的邊）都直接來自麵包屑列的 markdown 連結。

## 全站依賴圖 Full Dependency Map

```mermaid
graph LR
  subgraph SG_00_overview["00 · 課程導覽 Overview"]
    n_00_overview_build_report["Build Report 建置報告"]
    n_00_overview_changelog["Changelog 版本歷史"]
    n_00_overview_cheat_sheet["速查表 Cheat Sheet"]
    n_00_overview_index["首頁 ISF 與相位雜訊導覽"]
    n_00_overview_learning_path["循序學習路徑 Learning Path"]
    n_00_overview_notation["統一符號表 Notation"]
  end
  subgraph SG_01_paper_map["01 · 論文地圖 Paper Map"]
    n_01_paper_map_claims_cross_reference["教學主張交叉索引 C1–C13"]
    n_01_paper_map_equation_index["公式推導索引 Equation Index"]
    n_01_paper_map_figure_index["圖片索引 Figure Index"]
    n_01_paper_map_paper_summary_table["五篇論文速覽 Paper Summary Table"]
  end
  subgraph SG_02_foundations["02 · 基礎 Foundations"]
    n_02_foundations_oscillator_phase["Oscillator phase 是什麼？"]
    n_02_foundations_phase_vs_amplitude_noise["Phase vs Amplitude Noise"]
    n_02_foundations_lti_vs_ltv["LTI vs LTV"]
    n_02_foundations_tank_Q_and_energy_restoration["Tank Q 與能量恢復"]
    n_02_foundations_stochastic_noise_basics["隨機雜訊基礎 Noise Basics"]
    n_02_foundations_psd_phase_noise_jitter["Phase Noise → Jitter"]
    n_02_foundations_jitter_kernels["Jitter 核的嚴格推導"]
    n_02_foundations_allan_variance["Allan variance"]
    n_02_foundations_dsp_view_of_phase_noise["Phase Noise 的 DSP 視角"]
    n_02_foundations_exercises["基礎章習題"]
  end
  subgraph SG_03_isf_core_theory["03 · ISF 核心理論 Core Theory"]
    n_03_isf_core_theory_isf_definition["ISF 的定義"]
    n_03_isf_core_theory_impulse_to_phase_shift["Impulse → Phase Shift"]
    n_03_isf_core_theory_convolution_derivation["Impulse → Noise 卷積推導"]
    n_03_isf_core_theory_fourier_series_of_isf["ISF 的 Fourier series"]
    n_03_isf_core_theory_rms_isf["rms ISF 與 Parseval 關係"]
    n_03_isf_core_theory_asymmetric_isf_closed_form["非對稱三角 ISF 的閉式解"]
    n_03_isf_core_theory_isf_from_waveform["從波形算 ISF：三種方法"]
    n_03_isf_core_theory_white_noise_to_phase_noise["白噪如何變成 1/f² phase noise"]
    n_03_isf_core_theory_flicker_noise_upconversion["Flicker noise 上轉成 1/f³ ph…"]
    n_03_isf_core_theory_lorentzian_linewidth["Lorentzian 線寬"]
    n_03_isf_core_theory_diffusion_dictionary["擴散常數字典 κ/D/線寬/ADEV"]
    n_03_isf_core_theory_beyond_lorentzian["超越 Lorentzian"]
    n_03_isf_core_theory_effective_isf["Effective ISF（cyclostationary）"]
    n_03_isf_core_theory_capstone_lc_end_to_end["Capstone：LC 一條龍 state→BER"]
    n_03_isf_core_theory_exercises["核心理論章習題"]
  end
  subgraph SG_04_simulation_labs["04 · 模擬實驗 Simulation Labs"]
    g_lab_basic(["基礎手感 Labs（numerical_feeling · worked_examples · interactive_calculator · lab01–05）"])
    g_lab_noise(["雜訊與抖動 Labs（lab06–12）"])
    g_lab_sys(["系統與進階 Labs（lab13–17 · 32 · 34 · 36 · final_exam）"])
  end
  subgraph SG_05_paper_deep_dives["05 · 論文逐篇精讀 Paper Deep Dives"]
    n_05_paper_deep_dives_index["逐篇精讀導覽 Paper Deep Dives"]
    n_05_paper_deep_dives_paper_001_general_theory_phase_noise["[P1] 相位雜訊通論"]
    n_05_paper_deep_dives_paper_002_jitter_phase_noise_ring["[P2] Ring 振盪器 jitter"]
    n_05_paper_deep_dives_paper_003_injection_locking_part1["[P3] 注入鎖定 Part I"]
    n_05_paper_deep_dives_paper_004_injection_locking_part2["[P4] 注入鎖定 Part II"]
    n_05_paper_deep_dives_paper_005_cross_coupled_sense_amp["[P5] Sense Amp（與 ISF 無關）"]
  end
  subgraph SG_06_design_insights["06 · 設計直覺 Design Insights"]
    g_dsg_map(["波形與元件設計對映 Waveform & Device Mapping"])
    g_dsg_meas(["量測、預算收官與地雷 Measurement, Budget & Pitfalls"])
    g_dsg_sys(["系統時脈鏈與參考源 System Clocking & References"])
    g_dsg_topo(["真實拓樸與注入 Real Topologies & Injection"])
    n_06_design_insights_exercises["設計章習題"]
    n_06_design_insights_lc_vs_ring["從 ISF 看 LC vs ring oscill…"]
    n_06_design_insights_pll_noise_budget["PLL 完整相位雜訊預算與最佳 loop BW"]
    n_06_design_insights_serdes_clocking_connection["從 ISF 到 SerDes clocking"]
    n_06_design_insights_symmetry["波形對稱性與 flicker upconversi…"]
    n_06_design_insights_tank_swing["Tank Swing 與 q_max"]
  end
  subgraph SG_99_appendix["99 · 附錄 Appendix"]
    g_app_ref(["查閱工具 Reference Tools"])
    g_app_theory(["嚴格數學基礎 Rigorous Math Foundations"])
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

## 節點數如何從 92 頁壓到 56 個

| 章節 | 原始頁數 | 圖中節點數 | 處理方式 |
|---|---|---|---|
| 00 · 課程導覽 Overview | 6 | 6 | 逐頁（小章節，本身多為查閱型 hub） |
| 01 · 論文地圖 Paper Map | 4 | 4 | 逐頁 |
| 02 · 基礎 Foundations | 10 | 10 | 逐頁（核心主幹，規格要求逐頁） |
| 03 · ISF 核心理論 Core Theory | 15 | 15 | 逐頁（核心主幹，規格要求逐頁） |
| 04 · 模擬實驗 Simulation Labs | 24 | 3 | 按側邊欄三個子分類收攏（基礎手感／雜訊與抖動／系統與進階） |
| 05 · 論文逐篇精讀 Paper Deep Dives | 6 | 6 | 逐頁（每頁對應一篇論文，數量小、意義大，不收攏） |
| 06 · 設計直覺 Design Insights | 20 | 10 | 度數最高的 6 頁（symmetry、tank_swing、lc_vs_ring、pll_noise_budget、serdes_clocking_connection、exercises）逐頁保留，其餘 14 頁按主題收攏成 4 叢 |
| 99 · 附錄 Appendix | 7 | 2 | 收攏成「嚴格數學基礎」與「查閱工具」兩叢 |
| **總計** | **92** | **56** | |

## 8 個連結度最高的樞紐頁面 Top-8 Hub Pages

「度數」= 該頁在麵包屑抽取出的**頁面層級**（未分組前）有向圖中，入邊數 + 出邊數。入邊多代表
「這頁自己列了很多先備」，出邊多代表「很多下游頁把它列為先備」——出邊多的頁通常是全站真正的
**概念樞紐**。並列時的排序規則：度數相同先比入邊數，再相同則按頁面 id 字母序（見下方註）。

| 排名 | 頁面 | 章節 | 度數（in+out） | 先備數 in | 被列為先備 out |
|---|---|---|---|---|---|
| 1 | [白噪如何變成 1/f² phase noise](/03_isf_core_theory/white_noise_to_phase_noise) | 03_isf_core_theory | 24 | 4 | 20 |
| 2 | [Capstone — 一顆 ideal LC 從 state equations 到 BER（全嚴格一條龍）](/03_isf_core_theory/capstone_lc_end_to_end) | 03_isf_core_theory | 18 | 17 | 1 |
| 3 | [ISF 的 Fourier series（傅立葉級數）](/03_isf_core_theory/fourier_series_of_isf) | 03_isf_core_theory | 16 | 3 | 13 |
| 4 | [從 ISF 到 SerDes clocking](/06_design_insights/serdes_clocking_connection) | 06_design_insights | 14 | 10 | 4 |
| 5 | [設計章習題（含完整解答）](/06_design_insights/exercises) | 06_design_insights | 13 | 10 | 3 |
| 6 | [Phase Noise → Jitter](/02_foundations/psd_phase_noise_jitter) | 02_foundations | 13 | 3 | 10 |
| 7 | [Oscillator phase 是什麼？](/02_foundations/oscillator_phase) | 02_foundations | 13 | 2 | 11 |
| 8 | [Tank Q 與能量恢復](/02_foundations/tank_Q_and_energy_restoration) | 02_foundations | 12 | 7 | 5 |

> 註：這欄度數採**完整**麵包屑格式擷取（含各頁不同措辭的變體——`> 先備：`／`> **先備**：`／
> `> **前置閱讀**：`／`> **先備知識（建議先讀）**：`／lab 頁的「麵包屑…上游／下游」——不只是
> 唯一標準寫法那一種；兩個無麵包屑的例外頁 `tank_Q_and_energy_restoration`、`capstone_lc_end_to_end`
> 仍用其「延伸閱讀」連結），比只認單一固定格式的擷取更完整、也更接近網站真實連結量。
> 第 5–7 名三頁度數同為 13，用上述規則（先比入邊）排序：`exercises`（in=10）＞
> `psd_phase_noise_jitter`（in=3）＞`oscillator_phase`（in=2）。第 8 名（度數 12）與
> `03_isf_core_theory/isf_definition`（in=3, out=9）同分，因先備數較高（7>3）故
> `tank_Q_and_energy_restoration` 居第 8、`isf_definition` 緊追第 9。度數 11 還有四頁：
> `06_design_insights/symmetry`、`06_design_insights/tank_swing`、`03_isf_core_theory/rms_isf`、
> `02_foundations/stochastic_noise_basics`——這些頁同樣是名符其實的樞紐，值得在圖上留意。
> `symmetry`、`lc_vs_ring`、`tank_swing`、`isf_definition`、`tank_Q_and_energy_restoration`
> 因為度數高，都以**獨立節點**（非分組）畫在圖上，一眼就能在 02/03/06 章節裡認出來。

## 分組節點圖例 Grouped-Node Legend

分組節點在圖上沒有單一目的地，因此不掛 `click`；下面依章節列出每個分組節點實際包含哪些頁。

### 04 · 模擬實驗

**基礎手感 Labs（numerical_feeling · worked_examples · interactive_calculator · lab01–05）**（節點 `g_lab_basic`）：
　[互動計算器 Interactive Calculator](/04_simulation_labs/interactive_calculator)、[Lab 01 — 正弦振盪器與 limit cycle 的相位/振幅幾何](/04_simulation_labs/lab_01_sinusoidal_oscillator)、[Lab 02 — 理想 LC 振盪器 toy model：Γ(θ) = −sin θ 與電荷線性度](/04_simulation_labs/lab_02_lc_oscillator_toy_model)、[Lab 03 — Ring 振盪器 toy model：累積 jitter 隨機漫步與 ISF 比較](/04_simulation_labs/lab_03_ring_oscillator_toy_model)、[Lab 04 — impulse injection sweep 與 LTI vs LTV](/04_simulation_labs/lab_04_impulse_injection_sweep)、[Lab 05 — ISF 的傅立葉係數與 Parseval](/04_simulation_labs/lab_05_isf_fourier_coefficients)、[數值手感 Numerical Feeling](/04_simulation_labs/numerical_feeling)、[Worked Examples 例題庫](/04_simulation_labs/worked_examples)

**雜訊與抖動 Labs（lab06–12）**（節點 `g_lab_noise`）：
　[Lab 06 — 白噪 → 1/f² 相位雜訊](/04_simulation_labs/lab_06_white_noise_phase_noise)、[Lab 07 — 1/f 噪聲上轉與 ISF 對稱性](/04_simulation_labs/lab_07_flicker_noise_upconversion)、[Lab 08 — 從 L(f) 積分得 rms jitter](/04_simulation_labs/lab_08_jitter_integration)、[Lab 09 — 設計取捨綜合 scaling](/04_simulation_labs/lab_09_design_tradeoffs)、[Lab 10 — phase noise 如何把載波塗成 RF 裙帶](/04_simulation_labs/lab_10_rf_spectrum)、[Lab 11 — Monte-Carlo 累積 jitter：RJ 是高斯、σ 隨 √ΔN](/04_simulation_labs/lab_11_monte_carlo_jitter)、[Lab 12 — 從 jitter 到 eye 到 BER（SerDes bathtub）](/04_simulation_labs/lab_12_serdes_eye_ber)

**系統與進階 Labs（lab13–17 · 32 · 34 · 36 · final_exam）**（節點 `g_lab_sys`）：
　[期末總測驗：5 GHz LC VCO 到 25 Gb/s SerDes 一條龍](/04_simulation_labs/final_exam)、[Lab 13 — PLL/CDR 的 jitter transfer：VCO 高通、reference 低通](/04_simulation_labs/lab_13_pll_cdr_transfer)、[Lab 14 — Cyclostationary noise 與 effective ISF](/04_simulation_labs/lab_14_cyclostationary_isf)、[Lab 15 — 非線性振盪器的 ISF（van der Pol）](/04_simulation_labs/lab_15_nonlinear_isf)、[Lab 16 — Leeson 模型 vs ISF 模型（三段對照）](/04_simulation_labs/lab_16_leeson_vs_isf)、[Lab 17 — 設計掃描：swing / Γrms / N 三條設計曲線](/04_simulation_labs/lab_17_design_tradeoffs)、[Lab 32 — MOS Level-1 方程級 ring：從電晶體方程萃取 ISF](/04_simulation_labs/lab_32_mos_level1_ring)、[Lab 34 — 相關供電/基板雜訊的 N·f0 選擇律（P2 Eq.37–38）](/04_simulation_labs/lab_34_correlated_supply)、[Lab 36 — 鎖定捕獲暫態與 noise-induced cycle slips](/04_simulation_labs/lab_36_lock_acquisition)

### 06 · 設計直覺

**波形與元件設計對映 Waveform & Device Mapping**（節點 `g_dsg_map`）：
　[Device noise → ISF harmonics 的映射](/06_design_insights/device_noise_mapping)、[波形斜率與相位敏感度](/06_design_insights/waveform_slope)

**量測、預算收官與地雷 Measurement, Budget & Pitfalls**（節點 `g_dsg_meas`）：
　[ADC aperture jitter：時脈 jitter 如何吃掉 SNR 與 ENOB](/06_design_insights/adc_aperture_jitter)、[常見錯誤陳列室：12 個真實地雷](/06_design_insights/common_mistakes)、[DJ 與 dual-Dirac 模型](/06_design_insights/dj_dual_dirac)、[FOM 的理論天花板](/06_design_insights/fom_limit)、[相位雜訊量測與 spur](/06_design_insights/measurement_and_spurs)

**系統時脈鏈與參考源 System Clocking & References**（節點 `g_dsg_sys`）：
　[時脈鏈雜訊記帳：×N、÷N、PLL、buffer 一頁查表](/06_design_insights/clock_chain_budget)、[參考源振盪器：crystal 與 MEMS 的 phase noise](/06_design_insights/reference_oscillators)、[Sampling / sub-sampling PLL：把 divider 踢出迴路](/06_design_insights/sampling_pll)

**真實拓樸與注入 Real Topologies & Injection**（節點 `g_dsg_topo`）：
　[注入鎖定的雜訊整形與 injection pulling 頻譜](/06_design_insights/injection_locking_noise)、[Quadrature 產生與 coupled-oscillator phase noise](/06_design_insights/quadrature_and_coupled_oscillators)、[真實拓樸的 ISF：cross-coupled LC VCO、Colpitts、CMOS ring stage](/06_design_insights/real_oscillator_topologies)、[Tuning line 與 supply pushing 的相位雜訊](/06_design_insights/varactor_tuning_supply_pushing)

### 99 · 附錄

**查閱工具 Reference Tools**（節點 `g_app_ref`）：
　[中英對照詞彙表 Glossary](/99_appendix/glossary)、[Python 環境與模擬程式庫 Python Environment](/99_appendix/python_environment)、[參考文獻 References](/99_appendix/references)

**嚴格數學基礎 Rigorous Math Foundations**（節點 `g_app_theory`）：
　[Floquet / adjoint / PPV：ISF 的嚴格基礎](/99_appendix/derivation_floquet_ppv)、[Leeson 模型推導與 ISF 對照](/99_appendix/derivation_leeson)、[嚴格 LTV 框架：Zadeh 時變傳函與 harmonic transfer matrix](/99_appendix/ltv_htm)、[數學工具箱 Math Identities](/99_appendix/math_identities)

## 重點回顧

- 這張圖的邊 100% 來自每頁自己聲明的「先備／接下來」（兩個例外頁改用「延伸閱讀」，見上）——
  它是網站**實際**依賴結構的鏡子，不是重新設計的理想教學順序（理想順序仍以
  [learning_path](/00_overview/learning_path) 十二步為準，圖上以金色標出）。
- 92 頁 → 56 節點：02／03 兩個核心章節逐頁保留（教學規格要求），04 全收攏、06／99 依連結度
  部分收攏，讓圖維持在「一眼掃得完」的規模。
- 連結度最高的樞紐不在 00/01（查閱型字典頁本身很少被其他頁列為「先備」，麵包屑度數自然低），
  而是白噪→1/f²、SerDes clocking、capstone、ISF 傅立葉級數、章末習題這幾頁——它們是全站
  教學邏輯真正的收束點。
- 圖不是嚴格 DAG：少數頁彼此互列先備，屬於忠實反映，不代表抽取有誤。

## 延伸閱讀

- 十二步學習路徑完整說明：[learning_path](/00_overview/learning_path)
- 五篇論文的分工與速覽：[paper_summary_table](/01_paper_map/paper_summary_table)
- 每條公式 → 推導頁 → 論文出處：[equation_index](/01_paper_map/equation_index)
- 一頁速查公式與數值：[cheat_sheet](/00_overview/cheat_sheet)
- 全站符號表：[notation](/00_overview/notation)
