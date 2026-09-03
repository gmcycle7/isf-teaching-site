---
title: Changelog 版本歷史
description: v1 → v8 的完整版本演進紀錄，含每一版新增內容、修正事件與稽核細節。
---

# Changelog 版本歷史

本頁完整保留 [build_report](/00_overview/build_report) 曾記錄過的逐版歷史細節（v1→v8，
含稽核過程、修正事件、部署備註）。若只想看**目前**站台狀態與誠實原則，請看
[build_report](/00_overview/build_report)；本頁是給想追溯「某個數字/公式怎麼演變」的讀者。

新版在最上面（newest first）。

---

## v10：Subharmonic injection、注入鎖定頻率轉換小章、成長債清償

**退回點**：`v9-stable`（`ab33656`）／備份分支 `backup/v9-stable`／v9 線上 gh-pages `0bd6af7b4`；中間點 `v10-w1-partial`（`dd35ce7`）。

- **Subharmonic injection（本版主角）**：[subharmonic_injection](/06_design_insights/subharmonic_injection)——從 [P3] p.2112 impulse-train（每 M 週期注入＝subharmonic locking，逐字轉錄）與 [P4] Eq.(28)–(30) 推出倍頻端：只有注入波形的第 N 諧波與 ISF 基波作用（$\omega_L=\tfrac12\lvert I_N\rvert\lvert\tilde\Gamma_1\rvert$）⇒ **純弦波次諧波一階不鎖**；impulse-train 路線 $\Delta\omega_L\propto1/N$；realignment factor $\beta=-q_{inj}\tilde\Gamma'(\theta_{ss})$；離散時間雜訊迴路、corner、閉式輸出 jitter（MC 比 0.999）；ILCM vs PLL vs sub-sampling 對照。誠實修正兩個簡報假設：ring 的優勢來自 $q_{max}$（×100）而非 ISF 斜率；固定 $f_0$ 下 N 無內部最佳點（真正最佳在 β）。lab_40（六組實驗：1/N 斜率 −1.000、pulse-train 15/15 鎖 vs 純弦波 0/15、β 量測 0.0486 vs 0.0498、spur 誤差 ≤0.01 dB）＋ SubharmonicInjectionExplorer widget。
- **ILFD 獨立頁**：[injection_locked_division](/06_design_insights/injection_locked_division)（除頻↔倍頻對偶；M:N 雜訊 corner $\omega_c=N\sqrt{\omega_L^2-\Delta\omega^2}$＝[P4] Eq.(32)）。
- **[P4] 大注入模型與暫態**：[paper_004_large_injection_transient](/05_paper_deep_dives/paper_004_large_injection_transient)＋lab_41（Eq.(31) 閉式 vs RK4 差 2e-14；大注入 $\omega_L=\omega_{L0}/\sqrt{1-a^2}$）。
- **理論地圖**：[theory_map](/00_overview/theory_map)（236 條 breadcrumb 邊、56 節點 mermaid）。
- **成長債**：06 章 20 頁分 3 組並修回 3 頁遺失的側欄條目；print CSS；GitHub Discussions＋issue 模板；棄用警告修正；EN 全量平價 91 頁（8 處修正）。
- **Pagefind 評估：NO-GO**（中文核心詞召回 ~1%，報告 `scripts/pagefind_integration_patch.md`），保留現有搜尋。
- 過程備註：fable 5 三度 529 過載，S2 頁面改由 sonnet 依既有模擬補完；EN lab_40 front matter 未加引號再炸 en build，已修並納入 gate。
- 規模：**97 頁×2 語系、56 圖、49 模擬、21 互動元件、160 可驗證例題（147 自動過/0 錯）**。

## v9：成長債清償＋學習動線 v2＋EN 稽核＋論文收官（G1–G4）

- equation_index 28→62 列；figure_index 52→53 圖零孤兒；cheat_sheet v2；`scripts/update_stats.py` 門面數字自動同步；build_report 瘦身＋本 changelog 分頁。
- learning_path 9→12 步（進度打勾 12 項）；quiz 10→33 題；[final_exam](/04_simulation_labs/final_exam)（10 題跨章）；capstone 工具箱指標。
- EN：92 檔術語稽核（0 真漂移；4 檔修正）、16 頁平價抽查全過；widget a11y（12 元件補 aria）。
- [P2] Appendix A 教學化（實際位置 p.802–803，簡報頁碼猜錯已照實修）；[P1] Fig.29/30 概念復刻。
- 規模：92 頁×2、53 圖、46 模擬、20 互動元件、156 例題（145/0/0）。

## v8：增補三波（A/B/C/D 全做）

**23 個單元全數完成**（困難→fable、機械/互動→sonnet；每單元同步寫入英文版）：

- **論文 verbatim（7）**：App.B 非對稱 ISF 閉式 Eq.(52)–(57)（lab_33，閉式 vs 數值 1.6e-9；corner∝1/N 新設計律；另抓到 [P1] Eq.24 vs [P2] Eq.7 的 DC 記帳 2× 差，兩頁誠實雙列）；[P1] 附錄三種 ISF 算法 Eq.(31)–(38)（三法對決；誠實揭露閉式法 O(μ) isochron-shear 誤差）；差動 ring 隨 N 變差（Eq.31–35, p.796）；[P3] 最佳注入波形 Eq.(43)–(45)（Cauchy–Schwarz，lab_39）；相關供電 N·f₀ 選擇律 Eq.(37)–(38)（lab_34）；[P4] M:N 次諧波鎖定 Eq.(28)–(30)（lab_37；c₂=0 不能 ÷2）；[P3] impulse-train 鎖定 Eq.(19)–(23)。
- **推導/例題（5）**：Flicker ADEV floor＝√(2ln2·h₋₁)（∫sin⁴u/u³=ln2 嚴格證＋lab_19 驗絕對值）；[P2] Fig.16 兩段式 jitter（lab_24 Part 5；**發現論文印刷勘誤 ζ=2.5e5 應為 2.5e-5**，6× 放大驗證後誠實標注）；PLL peaking 閉式（ζ=0.707→2.09 dB @0.786fₙ）＋fractional-N ΔΣ 第三項；[P1] Sec.V 真矽 ring 全數字重演（**發現論文 p.191 "58.8 fF" 量綱勘誤應為 fC**）；大角度 Bessel 邊帶梯＋多源 superposition 例題。
- **互動（8 新 widget，全部雙語）**：AsymmetricIsfExplorer（2646 組合掃描 0 NaN）、AdlerWashboard（washboard 位能＋cycle-slip 計數）、PullingSpectrumExplorer（內建 radix-2 FFT，ω_b 誤差 0.59%@r=1.5）、HtmFoldingExplorer、DualDiracFitter、EffectiveIsfExplorer、LineshapeExplorer（RBW 抹平）、AdevLiveExplorer（有限資料誤差棒）。
- **新模擬（6）**：lab_33 非對稱 corner、lab_34 相關供電選擇律、lab_35 cross-correlation 量測（floor∝1/√M）、lab_36 鎖定捕獲＋Kramers 逃逸、lab_38 K_push 第一性（2.936 GHz/V，FM 邊帶比 1.002）、lab_39 最佳注入。

站點規模：**90 頁×2 語系、52 圖、45 個模擬、20 個互動元件、144 個可驗證例題（133 自動通過、0 錯）**。

---

## v7：[P2] Eq.(16) ring $\Gamma_{rms}$ 的 N-scaling 重核（根號範圍誤讀修正）

**裁決**（三重證據鎖死，對照 p.794/p.803 高倍渲染親驗）：[P2] Eq.(16) 的正確讀法是根號**只蓋常數**，
即 $\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\cdot(1/N^{1.5})$，故 $\Gamma_{rms}\propto N^{-3/2}$（而非 v3 誤改的
$N^{-3/4}$）。三重證據：(1) 論文正文明言「$1/N^{1.5}$ dependence of $\Gamma_{rms}$」；(2) $\eta=0.75$
數值錨——正文給出 solid line $\approx4/N^{1.5}$，代入 $\sqrt{2\pi^2/(3\cdot0.75^3)}=3.95\approx4$ ✓（若
$N^{1.5}$ 在根號內則得 $4/N^{0.75}$，與正文矛盾）；(3) App.B Eq.(52)+(54) 獨立代數推出
$\Gamma_{rms}^2\propto N^{-3}$，與 $N^{-3/2}$ 一致。**歷史**：v1 原寫 $N^{-3/2}$（正確），v3 稽核把根號
範圍看錯、誤改為 $N^{-3/4}$ 並誤標「已核實」，v7 對照原文修回並記錄本次事件（與 FOM $8/(3\gamma)$
誤讀事件同型）。全站受影響頁面（real_oscillator_topologies、waveform_slope、references 等）已同步
修正指數與相關數值（如 $N{=}5\to15$ 的比例由 $0.4387$／$-7.16$ dB 改為 $0.1925$／$-14.31$ dB）；
Eq.(23) FOM 的 N-independence、$8/(3\eta)$、$\kappa$、Eq.(15) $f_0$、Eq.(17)/(18)/(21) 均不受影響。

---

## v6：互動、內容、英文版與門面（C+D 波）

- **互動**：三章習題共 9 題即時作答（NumericQuiz）；isf_definition 的 **impulse→相位動畫**（切向/徑向分解、ghost 參考、Δφ 累積）；**ISF 沙盒**（拉波形→即時 c_n/Γrms/L/corner，slope 近似、正弦錨點 −145 dBc/Hz 驗證）；learning_path 進度打勾（localStorage）；7 本可下載 Jupyter notebooks（nbclient 全數執行驗證）。
- **內容**：lab_32 **MOS Level-1 方程級 ring**（Shichman–Hodges，impulse 法萃取真 ISF；Parseval 1.7308 vs 1.7309；能量集中在 transition，符合 [P2]）；sampling/sub-sampling PLL、crystal/MEMS 參考源、**常見錯誤陳列室**（12 條全取材本站抓過的錯）。
- **英文版 β**：en locale＋語言切換器＋UI 翻譯＋7 頁核心翻譯（其餘 fallback 中文）。
- **門面/bug**：favicon＋logo＋og 社群卡；**手機水平捲動修復**（滑桿列 flexWrap，375px 實測歸零）；LICENSE（內容 CC BY-NC-SA 4.0／程式 MIT）；README、repo topics、editUrl。
- **[P2] p.803 逐字核實**：Eq.(45)–(51) 轉錄；(49) 的 8 係數＝雙邊譜（與 jitter_kernels 單邊 4sin² 核精確等價）；(50) κ 數值互鎖 2.0×10⁻⁹√s；(51) 印刷無 √2（定義差異註明）。
- **Lighthouse 基線**（線上站）：Performance 89 / Accessibility 93 / SEO 100。
- 誠實不採用（量測後還原）：搜尋索引 zh-only（僅 −2%）、PNG 無損重編碼（+10%）。
- 部署備註：雙語 build ~200MB，Pages 曾卡 "building" 35 分，`POST /pages/builds` 重建後 30 秒完成——大型部署卡住時用此招。

---

## v5：理論深化波（12 項）＋一個被抓到的 factor-2

**v5 新增 12 項理論單元**（8 新頁＋2 頁擴充＋9 個新 lab＋2 個 fig 腳本），每項都是「推導頁＋實跑模擬拿到數字才寫進頁面」：

1. **[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)**：κ↔D↔線寬↔ADEV↔S_φ 五件衣服一次對帳（lab_23 一次模擬、四路萃取同一個 0.125）。
2. **[jitter_kernels](/02_foundations/jitter_kernels)**：TIE／period／cycle-to-cycle 核（4sin²、16sin⁴）第一性推導＋MC（理論/實測比 0.999–1.001）；白噪閉式精確重現 [P2] Eq.(8)。**關掉全站最後一個理論 TODO**。
3. **Floquet/PPV 數值化**（[derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv) 擴充 + lab_25）：算 monodromy（μ₁=1.000000）、adjoint 萃取 v₁、與 impulse 法 ISF 疊圖 rms 0.0016——「PPV=ISF」從散文變成算出來的事實。
4. **[injection_locking_noise](/06_design_insights/injection_locking_noise)**（lab_26/27）：鎖定＝一階 PLL（自身雜訊高通、reference 低通、corner=ω_L cosθ_ss）＋ pulling 的不對稱 beat 頻譜。
5. **AM 雜訊完整譜**（[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 擴充 + lab_28）：OU 過程 → 平頂 Lorentzian（corner=ω₀/2Q）。
6. **[beyond_lorentzian](/03_isf_core_theory/beyond_lorentzian)**（lab_29）：flicker 下線形偏離 Lorentzian（近 Gaussian core）＋「自由振盪器嚴格上沒有 S_φ」的非平穩性。
7. **[adc_aperture_jitter](/06_design_insights/adc_aperture_jitter)**（lab_30）：SNR=−20log₁₀(2πf·σ_t) 推導＋447.9 fs 的 ENOB 表。
8. **[dj_dual_dirac](/06_design_insights/dj_dual_dirac)**（lab_31）：dual-Dirac、TJ@BER、DJ_δδ≤DJ_pp 的誠實差異。
9. **[clock_chain_budget](/06_design_insights/clock_chain_budget)**：×N/÷N/PLL/buffer 四條記帳規則＋整鏈 worked example。
10. **[fom_limit](/06_design_insights/fom_limit)**：FOM 天花板 = 173.8−10log₁₀F_eff dB@300K（自算驗證，非記憶值）。

> **v5 的 factor-2 戰果**：jitter_kernels 的 MC 交叉檢查抓到**規範 11.2 的 D 映射錯 2 倍**——v3 把方差成長率 κ²（[P2] Eq.11）誤當擴散常數 D 塞進 Δf=D/π。經 lab_23 與獨立 MC＋Lorentzian 擬合裁決（擬合 FWHM/κ²·2π=0.992），**全站修正**：D=Γ²rms·S_i/(4q²max)=κ²/2；代表值線寬 40→**19.9 mHz**、真 LC 80→**39.8 mHz**、−100 dBc/Hz 錨點 1257→**628 Hz**（lorentzian／capstone／lab_22／規範 11.2 同步更新）。scaling 與 −145/−148 dBc/Hz 均不受影響。

---

## v4：Deep 稽核改善流程（研究式多-agent harness）

第四輪用「研究式多-agent harness」對全站做深度稽核與修正，分階段、每階段後跑 gate
（`run_all_sims` + `verify_examples` + `check_site_quality` + `npm run build` + 數學掃描）：

1. **WF-1 多透鏡稽核**：7 個 lens（correctness / pedagogy / citation / consistency / completeness /
   figure / code）＋逐頁深讀，產出 ~45 條結構化發現。
2. **WF-2 PDF 引用驗證**：對每條引用發現**實際渲染原始 PDF 頁面逐字核對**（adversarial）。
3. **WF-3 修正**：每頁一個 owner agent 套用統一校訂 spec；新增 **3 頁**（varactor 調諧／supply pushing、
   quadrature／coupled-oscillator、tank Q 與能量回補）、**lab_22 端到端模擬**、**4 張概念圖**、
   **3 個互動 widget**（injection-locking Adler、Allan deviation、PLL loop-BW），與全站導覽
   （breadcrumb／延伸閱讀／goal-based landing）。
4. **WF-4 + round-2/3 複審**：逐頁深讀抓回 round-1 殘留與新 bug，再修。

關鍵成果（皆對照原始 PDF 核實）：

- **環形 FOM 前置係數 `8/(3γ)→8/(3η)` 再更正**（v2 曾誤改並誤標「逐字核實」；γ 僅透過
  `V_char=ΔV/γ` 進入），worked 例題 `−89.2→−91.0 dBc/Hz`、與理想 LC 差 57 dB。
- **`[P4]` ISF／APF 圖 `Fig.3→Fig.5, p.2126`**；APF 定義 Eq.(18)–(22)、理想 LC quadrature
  Eq.(26) p.2128（非舊標的「Eq.25/26/27」）。
- 引用頁碼／式號更正：`Fig.17 p.800→p.802`、`Sec.VIII p.1163→p.2135`、`Fig.4 p.182→p.181`、
  `f₀=1/(2Nτ_D)` 引用 `Eq.(14)→Eq.(15)`（Eq.14 其實是正規化級延遲 `t̂_D`）。
- 關掉可關的 TODO：cyclostationary `[P1] Eq.(25)–(27) p.186`、廣義 Adler `[P3] Eq.(30)/(35)`、
  Γrms `Eq.(16) p.794`；統一「週期穩態（cyclostationary）」中文詞。
- 程式 bug：lab_05 Parseval DC 重複計（`c₀²→c₀²/2`，修後 = `2Γ²rms`）、`accumulated_jitter_curve`
  壞掉的呼叫簽章；lab_06/07/15 加數值一致性指標；lab_10/20 圖修正；`verify_examples` 收緊正規式。
- **誠實擋下一個假修正**：稽核宣稱「κ Eq.(12) 漏了 ω₀」，放大原始 PDF p.793 確認 Eq.(12) 本來就
  沒有 ω₀——κ√Δt 是**相位** jitter `σ_Δφ`（Eq.11），**時間** jitter 才 `÷ω₀`（Eq.10）；未亂改。
- 外部文獻補上經 CrossRef 查證 DOI：Leeson 1966（10.1109/PROC.1966.4682）、Demir PPV 2000
  （10.1109/81.847872）、Kärtner 1990（10.1002/cta.4490180505）、Adler 1946（10.1109/JRPROC.1946.229930）。

**收斂（loop is dry）**：3 輪稽核所有實質發現皆已處理；`verify_examples` 88 個可驗證 block 中
**73 通過、0 錯誤**，其餘 13 為驗證器對「公式常數／上下文數字／刻意留白習題」的誤判（人工確認正確）。
最終站台規模 **74 頁、30 圖、25 模擬腳本、6 互動 widget**；最終 gate：build 綠燈、0 broken link、
0 KaTeX error、0 內容問題、0 軟性警告。

> **過程限制（誠實交代）**：WF-4 的平行 fix-agent 多次遇到 **Anthropic 端伺服器限流**（"not your
> usage limit"，非帳號用量上限），故引用類與機械式修正改以 inline 直接完成並逐項驗證。

---

## v3：例題數值 QA ＋ ring 常數稽核更正

新增 `scripts/verify_examples.py`：把 docs 內每個有「標準答案」(`# ->`) 的 Python 例題實際跑一遍對數值。**80 個可驗證 block 中 65 個自動通過、0 個錯誤**；其餘 14 個經人工確認正確（驗證器對註解裡的公式常數如 $2\Gamma_{rms}^2$ 的「2」、或對照用數字如「遠小於 447.9 fs」誤判）。過程修了真實 bug：`np.trapz`→`np.trapezoid`（NumPy 2.0）×3、壞掉的 `import`（補 `simulations/__init__.py` 使套件可匯入）、2 個寫錯的例題數值（effective_isf 的 $c_2$、PLL 最佳 BW 的 $S_{ref}$）。並修了 **dark-mode 圖**：matplotlib PNG 在深色模式加白底卡片（`.markdown img` CSS）。

**[P2] ring 常數對照原始 PDF（高解析度渲染）逐字核實並更正**：

- Eq.(23) FOM：前置係數由誤改的 $8/(3\gamma)$（v2 曾誤標「逐字核實」）對照原始 PDF p.796 更正為
  $8/(3\eta)$（$\eta$ 為級延遲比例常數 Eq.(14)，$\approx 1$；$\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入）；
  $V_T=0$ 下限 Eq.(25) 為 $\frac{16\gamma}{3\eta}$。
- Eq.(16) $\Gamma_{rms}$ 的 N-scaling：v3 稽核當時把根號範圍看錯，將 v1 原本正確的 $N^{-3/2}$
  「更正」成 $N^{-3/4}$ 並誤標「已核實」——此誤讀直到 **v7** 才被對照論文正文、數值錨與 App.B
  三重交叉驗證後修回（見上方 v7 條目）。

**v3 audit corrections（其餘對照原始 PDF 的稽核更正）**：**[P4]** ISF/APF 圖由 Fig. 3 更正為
Fig. 5（p.2126）；citation 頁碼更正：**[P2]** Fig.17（對稱電壓圖）p.802、**[P4]** Sec. VIII p.2135、
**[P1]** Fig.4 p.181、$f_0=1/(2N\tau_D)$ 改引 Eq.(15)；TODO 關閉：**[P1]** cyclostationary
$i_n(t)=i_{n0}(t)\alpha(\omega_0 t)$、$\Gamma_{eff}=\Gamma\cdot\alpha$（Sec. II-D, Eq.(25)–(27), p.186）
與廣義 Adler（**[P3]** Eq.(30)/(35)）皆已核實；另修 2 個程式 bug：lab_05 的 Parseval DC 項應以
$(c_0/2)^2$ 計入、`accumulated_jitter_curve` 呼叫缺 `f0`/誤用 `max_lag` 已修正。

**[P3]/[P4] injection & APF 公式也已於 v3 對照原始 PDF 逐字核實**：

- **[P3]** Eq.(26) $\tilde\Gamma=\Gamma/q_{max}$；廣義 Adler Eq.(30),(33) $\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$，
  $\Omega(\theta)=\frac{1}{T_{osc}}\int\tilde\Gamma(\omega_0 t+\theta)i_{inj}dt$；正弦退化 Eq.(34)、lock range Eq.(35) $\omega_L=\frac12 I_{inj}|\tilde\Gamma_1|$。
- **[P4]** amplitude decay $d(t,\phi)=e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$（Sec. III-F p.2128 正文；Eq.(25) 本身是 $\Lambda=\tau_0\tilde\Lambda$）；Eq.(26) ideal-LC 基波
  $\tilde\Gamma_1=\frac{1}{q_{max}}\angle90°$、$\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\angle0°$（quadrature）；Eq.(27) amplitude-corrected Adler。

> **v3 深化（研究所等級）**：新增 **Lorentzian 線寬**（解 1/f² 在 Δf→0 發散矛盾）、
> **Allan variance / ADEV**（時域頻率穩定度）、**嚴格頻譜推導**（cyclostationary 自相關→Wiener-Khinchin）、
> **PLL 完整雜訊預算 + 最佳 loop BW**、**真實拓樸 ISF**（cross-coupled VCO tail 上轉、Colpitts、ring stage）、
> **量測與 spur**、**LTV/HTM** 附錄、**Capstone**（ideal LC 從 state equations 一路到 BER）、
> 以及 **02/03/06 三章成套習題（含完整解答）**。配 4 個新模擬（lab_18–21）。

---

## v4 補記：稽核仍標 TODO 的項目

**v4 Deep 稽核（見上方 v4 條目）已關掉絕大多數 TODO**：[P2] ring 常數（FOM `8/(3η)`、Γrms `Eq.16`）、
[P3]/[P4] 的引用與頁碼（廣義 Adler `Eq.(30)/(35)`、APF `Fig.5`/`Eq.(18)–(22)`）、cyclostationary
`[P1] Eq.(25)–(27)`、外部文獻 DOI，皆已對照原始 PDF 逐字核實。剩下的 `TODO` 多是**刻意保留的
「外部文獻範圍」標註**（如 period-jitter kernel 慣例、標準 LC-VCO 設計常識）與 transistor-level
排除聲明，不影響核心理論正確性。

以下曾標 ⚠️ / `TODO`（外部文獻或次要細節，非核心 ISF/injection 物理）：

- **外部文獻（不在 5 篇 PDF 內）**：Leeson 1966、Demir et al. 2000（PPV）、Kärtner 1990 的正式卷期／頁碼——
  卷期／頁碼／公式記號已於 v4 查證；period/cycle-to-cycle jitter 核已於 **v5** 在
  [jitter_kernels](/02_foundations/jitter_kernels) **自行從第一性推導＋Monte-Carlo 驗證**（不再依賴外部慣例）。
- **[P2]** Fig.17 對稱電壓圖的確切座標軸；**[P4]** dual-modulus prescaler 的級數分配細節（Sec. VIII）。
- **[P5]**（sense amplifier，與 ISF 無關，刻意未轉錄）。
- **[P4]** APF 的確切定義式與傅立葉展開（Sec. III-D, p.2127）；Fig. 3 子圖標題。

---

## v2：逐步推導擴充 + Wave A/B/C/D

[P1]（general.pdf）的核心方程式 Eq.(1),(9),(10),(11),(12),(13),(15)–(24) 全部由高解析度渲染頁面
→ 人工逐條對照轉成 LaTeX 之後，v2 另補上逐步代數展開（down-conversion 積分、factor-8 求和、
$\mathcal{L}\approx\frac12 S_\phi$ 小角 PM、jitter 高通核、flicker 1/f³ corner、Parseval 三類項），
以及兩個推導附錄（Floquet/PPV、Leeson↔ISF）。

新增 8 張模擬圖（`lab_10`–`lab_17`：RF spectrum sidebands、Monte Carlo jitter histogram、SerDes eye/BER
bathtub、PLL/CDR jitter transfer、cyclostationary effective ISF、nonlinear oscillator ISF、Leeson vs ISF
overlay、design tradeoff sweeps）與對應 2 個新 util 模組（`pll_utils.py`、`serdes_utils.py`）。

**v2 曾誤植的錯誤**（後於 v3/v4 更正，見上）：ring FOM 前置係數一度誤改為 $8/(3\gamma)$ 並誤標
「逐字核實」——實為 $8/(3\eta)$。

`npm run build` 成功（Docusaurus 3.10.1）；歷史修正：曾修兩類渲染 bug——(a) 多行 display math 的圍欄
未獨立成行，導致 micromark 連鎖吃掉後續公式（已用 normalizer 全站修正並設為固定流程）；(b) 數學內
誤用 HTML 實體（gt/lt entity）→ 已改回數學用的大於/小於符號。

`python scripts/run_all_sims.py`：**36/36 通過**（29 labs + 7 個 `fig_*` 腳本），產生 41 張圖到
`static/figures/`（v4 再增 4 張概念圖）。

---

## v1：初版建置

- 掃描來源資料夾共 **5 個 PDF**（`scripts/extract_papers.py` 全部掃描、dump 純文字）：
  paper_001 `general.pdf`（[P1]，核心基礎）、paper_002 `jitter_ring.pdf`（[P2]，ring 延伸）、
  paper_003 `BHongGenTheor-I_JSSC2019_Postprint.pdf`（[P3]，injection，進階）、
  paper_004 `BHongGenTheor-II_JSSC2019_Postprint.pdf`（[P4]，APF，進階）、
  paper_005 `Hajimiri_ISCS_98.pdf`（[P5]，與 ISF **無關**，誠實標註為 cross-coupled sense amplifier 論文）。
- [P1] 核心方程式 Eq.(1),(9),(10),(11),(12),(13),(15)–(24) 全部由高解析度渲染頁面 → 人工逐條對照
  轉成 LaTeX，逐字用於教學頁與 `extracted/*.json`。
- 全部圖都是用 Python 重新產生的概念模擬（非從 PDF 擷取點陣圖），重現 [P1]/[P2] 的機制。
- 絕大多數圖為 toy / 概念模型（明確標註非 transistor-level）。少數純數學圖（jitter 積分、
  Leeson↔ISF 疊圖、設計掃描、PLL transfer、BER bathtub）為公式計算，與解析式一致。
- 完成章節：00 導覽 / 01 論文地圖 / 02 基礎 / 03 ISF 核心理論（公式已驗證）、04 模擬實驗
  （numerical_feeling、互動工具、lab_01–08）、05 逐篇精讀（5 篇）/ 06 設計直覺 / 99 附錄。
- Eq.(16) $\Gamma_{rms}$ 的 N-scaling **v1 原寫 $N^{-3/2}$（正確）**——此結論後於 v3 被誤改為
  $N^{-3/4}$，直到 v7 才修回（見上方 v3／v7 條目，完整事件記錄）。

---

## v8 之後：部署上線

以 **GitHub Pages（project page）** 公開上線：

- 網站：`https://gmcycle7.github.io/isf-teaching-site/`
- 原始碼（public）：`https://github.com/gmcycle7/isf-teaching-site`
- `baseUrl` 設為 `/isf-teaching-site/`；KaTeX CSS／字型經 webpack 打包（baseUrl-safe、完全離線）。
- 部署機制：本機 `npm run build` 後將 `build/` 推到 `gh-pages` 分支（含 `.nojekyll`），Pages 由該分支供應；
  每次更新重 build + force-push `gh-pages` 即可——已封裝成一鍵腳本 **`./scripts/deploy.sh`**（只需 `repo`
  權限，不需 `workflow` scope）。
- **版權處理**：5 篇論文**全文與 PDF 不入庫**（`.gitignore` 排除 `extracted/raw_text/` 與 `*.pdf`）；
  footer 與各頁標註版權屬原作者，內容為教學用途。
- CI（選配）：`.github/workflows/deploy.yml` 已備；需 token `workflow` 權限
  （`gh auth refresh -s workflow`）才能推送 workflow 檔，啟用 push-to-deploy 自動部署。
- 雙語 build ~200MB，Pages 曾卡 "building" 35 分，`POST /pages/builds` 重建後 30 秒完成
  ——大型部署卡住時用此招（v6 記錄）。
