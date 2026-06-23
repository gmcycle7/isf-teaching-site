---
title: Tuning line 與 supply pushing 的相位雜訊
description: 定義 K_VCO=∂f0/∂V_tune 與 supply pushing K_push=∂f0/∂V_DD；推導 tune/supply 節點的低頻雜訊電壓如何 FM 載波得 S_φ=K_VCO²·S_v/Δω²（white→1/f²、1/f→1/f³，與 device flicker c0 機制平行）；varactor C(V) 非線性的 AM-PM；split tuning、平坦偏壓點、LDO/共模抑制等 design knobs；worked example K_VCO=50 MHz/V、100 nV/√Hz @ 1 MHz、f0=5 GHz → L=-109 dBc/Hz。
---

# Tuning line 與 supply pushing 的相位雜訊

**前置（先讀這些）**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（白噪 → $1/f^2$ 的 $1/\Delta\omega^2$ 積分器）、[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)（$1/f$ → $1/f^3$，本頁要畫平行）、[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)（AM-PM 後門）。本頁假設你已經接受「相位無恢復力 → noise 經 $1/\Delta\omega^2$ 積分成裙邊」這條主線。

前面整套 ISF 理論講的都是 **device 自己的雜訊電流** $i_n(t)$ 直接注入 tank 節點。但真實 VCO（voltage-controlled oscillator，壓控振盪器，輸出頻率由一條控制電壓決定）還有兩個**完全不靠 device 內部 $i_n$、而是靠「外部電壓節點抖動」**的相位雜訊大門：

1. **tuning line（調諧線）**：你用一條 $V_{tune}$ 電壓去調 varactor（變容二極體，加偏壓改變電容的二極體），把 $f_0$ 調到想要的頻道。這條線上任何雜訊電壓 $v_n$ 都會**直接被頻率調變（FM）**進載波。
2. **supply（電源 $V_{DD}$）**：電源電壓變動會經由 device 工作點、寄生電容等路徑改變有效 $f_0$——這叫 **supply pushing（電源推移，電源電壓推著振盪頻率跑）**。

這頁要回答：**這兩條外部電壓門，怎麼把低頻雜訊電壓變成 close-in 相位雜訊？為什麼它跟 device flicker 的 $1/f^3$ 機制長得一模一樣？以及怎麼用設計把這兩扇門關小？**

> **物理直覺（先講結論）**：把 VCO 想成「電壓 → 頻率」的轉換器，靈敏度就是 $K_{VCO}=\partial f_0/\partial V_{tune}$（Hz/V）。控制節點上有 $v_n(t)$ 的雜訊電壓，瞬時頻率就抖 $\Delta f(t)=K_{VCO}\,v_n(t)$。**頻率是相位的微分，所以相位是頻率的積分**——這個積分器就是把 $S_v$（電壓雜訊）變成 $1/\Delta\omega^2$ 裙邊的同一台機器，跟 ISF 白噪結果用的 $1/\Delta\omega^2$ 是**字面上同一個積分器**。於是：tune line 的**白噪** → $1/f^2$；tune line 的 **$1/f$ 雜訊** → $1/f^3$。$K_{VCO}$ 越大這扇門開越大；把它做小（粗調用 switched-cap、細調才用 varactor）、把 $V_{tune}/V_{DD}$ 變乾淨（LDO、共模抑制），就是這頁所有 design knob 的核心。

本頁的 varactor $C$–$V$ 模型、LDO/cross-coupled VCO 拓樸細節、量測方法等**電路/拓樸/儀器層面的具體**屬於**標準 RF IC 設計文獻**（Razavi、Leeson、廠商 datasheet）；**不在本站下載的 5 篇 PDF 之內**，本頁明確標示「（外部文獻，非本站 5 篇 PDF）」。但「電壓雜訊 → FM → $1/\Delta\omega^2$ 相位裙邊」這條主幹**完全用 [P1] 既有的相位積分觀念**就能嚴格推出來，下面就這麼做。

## 第 1 步：定義 $K_{VCO}$ 與 supply pushing $K_{push}$

VCO 的工作定義是「輸出頻率隨控制電壓而變」。把振盪頻率 $f_0$ 看成控制電壓 $V_{tune}$ 與電源 $V_{DD}$ 的函數，在工作點做一階泰勒展開：

$$
f_0(V_{tune},V_{DD})\approx f_{0,op}+\underbrace{\frac{\partial f_0}{\partial V_{tune}}}_{K_{VCO}}\,(V_{tune}-V_{op})+\underbrace{\frac{\partial f_0}{\partial V_{DD}}}_{K_{push}}\,(V_{DD}-V_{DD,op}).
$$

兩個斜率就是本頁的兩個主角：

$$
K_{VCO}\equiv\frac{\partial f_0}{\partial V_{tune}}\qquad(\text{單位 Hz/V})
$$

$$
K_{push}\equiv\frac{\partial f_0}{\partial V_{DD}}\qquad(\text{單位 Hz/V})
$$

- **$K_{VCO}$（VCO 增益，又叫 tuning sensitivity）**：每 1 V 控制電壓能把頻率挪多少。它決定**調諧範圍**（tuning range，能掃過的頻段），也決定 **tune line 雜訊的放大倍率**——這就是本頁的核心張力：$K_{VCO}$ 要夠大才能涵蓋頻段、又要夠小才不放大雜訊。
- **$K_{push}$（supply pushing，電源推移係數）**：每 1 V 電源變動把頻率推多少。理想上 VCO 對電源免疫（$K_{push}=0$），實務上電源經 device 偏壓、寄生電容、有效 swing 改 $f_0$，$K_{push}\ne0$。（廠商常另給 $\text{Hz/V}$ 或 $\text{ppm/V}$ 的 pushing figure——外部文獻，非本站 5 篇 PDF。）
- **單位檢查**：$[\partial f_0/\partial V]=\text{Hz}/\text{V}$ ✓。兩者量綱相同，數學上**完全平行**——下面所有推導對 tune line 與 supply 一字不差，只是把 $K_{VCO},v_{n,tune}$ 換成 $K_{push},v_{n,DD}$。
- **物理意義**：這兩個係數把「外部電壓世界」接到「頻率世界」。它們是**設計者可控**的——不像 device 的 $i_n$（被製程/物理決定），$K_{VCO}$ 和 $K_{push}$ 是拓樸與偏壓選擇的結果。

> **與 ISF $\Gamma$ 的分工**：ISF $\Gamma(\omega_0\tau)$ 處理「電流脈衝 $\Delta q$ 在哪個相位注入 tank 節點 → 多少相位」；$K_{VCO}/K_{push}$ 處理「一個準靜態（quasi-static，相對載波很慢）的控制/電源電壓 → 多少頻率」。tune/supply 雜訊很慢（offset $\ll f_0$），所以**不必走 ISF 的逐脈衝相位投影**，直接走「電壓 → 頻率 → 積分成相位」這條更直接的 FM 路徑。兩條路最後都匯到同一個 $1/\Delta\omega^2$ 積分器（見第 2 步末），這正是本頁要畫的平行。

## 第 2 步：電壓雜訊如何 FM 載波 → $S_\phi=K_{VCO}^2 S_v/\Delta\omega^2$

現在讓 tune 節點帶一個**低頻**雜訊電壓 $v_n(t)$（offset 頻率 $\Delta\omega\ll\omega_0$，所以在一個載波週期內近乎不變，準靜態成立）。逐步推。

**第 2.1 步：電壓雜訊 → 瞬時頻率偏差。** 由 $K_{VCO}$ 的定義，瞬時振盪頻率隨 $v_n$ 抖動：

$$
\Delta f(t)=K_{VCO}\,v_n(t)\qquad\Longleftrightarrow\qquad \Delta\omega_{inst}(t)=2\pi K_{VCO}\,v_n(t).
$$

- **單位檢查**：$\text{Hz/V}\times\text{V}=\text{Hz}$ ✓（角頻率版乘 $2\pi$ 得 rad/s ✓）。
- 這就是 **FM（frequency modulation，頻率調變）**：控制電壓直接調載波的瞬時頻率。

**第 2.2 步：頻率是相位的微分 → 相位是頻率的積分。** excess phase $\phi(t)$ 的定義就是「瞬時頻率對 nominal 的偏差之時間積分」：

$$
\phi(t)=\int^{t}\Delta\omega_{inst}(t')\,dt'=2\pi K_{VCO}\int^{t}v_n(t')\,dt'.
$$

- **這個積分器是關鍵**：它跟 [P1] Eq.(11)/(13) 把 $i_n$ 積成 $\phi$ 用的**是同一台積分器**——只是這裡被積的不是「$\Gamma\cdot i_n$」而是「$K_{VCO}\cdot v_n$」。**積分 = 頻域乘 $1/(j\Delta\omega)$**（訊號與系統基本功），所以功率域乘 $1/\Delta\omega^2$，下一步就靠這個。
- **物理意義**：相位沒有恢復力（[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 第 1 步），所以「慢慢漂的頻率」會被**一路累積**成越來越大的相位偏移——offset 越靠近載波（$\Delta\omega$ 越小），積分器增益 $1/\Delta\omega$ 越大，裙邊越高。

**第 2.3 步：取 PSD（積分器在功率域是 $1/\Delta\omega^2$）。** 一個 LTI 系統 $\phi=\mathcal{H}\,v$ 對輸入 PSD 的作用是 $S_\phi=|\mathcal{H}(j\Delta\omega)|^2 S_v$。這裡 $\mathcal{H}=2\pi K_{VCO}/(j\Delta\omega)$，故 $|\mathcal{H}|^2=(2\pi K_{VCO})^2/\Delta\omega^2$：

$$
\boxed{\ S_\phi(\Delta\omega)=\frac{(2\pi K_{VCO})^2\,S_v(\Delta\omega)}{\Delta\omega^2}=\frac{K_{VCO}^2\,S_v(\Delta\omega)}{\Delta f^2}\ }
$$

右式用 $\Delta\omega=2\pi\Delta f$ 把 $2\pi$ 約掉（分子 $(2\pi)^2$、分母 $(2\pi)^2$），所以**用 Hz 算更乾淨**：$S_\phi=K_{VCO}^2 S_v/\Delta f^2$。

- **單位檢查**：$\dfrac{(\text{Hz/V})^2\cdot(\text{V}^2/\text{Hz})}{\text{Hz}^2}=\dfrac{\text{Hz}^2/\text{Hz}}{\text{Hz}^2}=\dfrac{1}{\text{Hz}}$，而相位無因次（rad），故 $S_\phi$ 是 $\text{rad}^2/\text{Hz}$ ✓。（嚴格說 $K_{VCO}^2$ 帶的「無因次相位」是隱含的；FM 的相位本來就無因次。）
- **跟 ISF 白噪結果並排看**——[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 的招牌式 $S_\phi=\dfrac{\Gamma_{rms}^2}{q_{max}^2}\dfrac{\overline{i_n^2}/\Delta f}{\Delta\omega^2}$ 與本式 $S_\phi=\dfrac{(2\pi K_{VCO})^2 S_v}{\Delta\omega^2}$ **分母都是 $\Delta\omega^2$**。device noise 版的「轉換增益」是 $\Gamma_{rms}/q_{max}$（A → rad），tune line 版的是 $2\pi K_{VCO}$（V → rad/s 再積分）。**同一個 $1/\Delta\omega^2$ 積分器、不同的入口**——這就是本頁要你記住的結構同構。

**第 2.4 步：套 SSB 相位雜訊（小角近似）。** 用全站慣例 $\mathcal{L}(\Delta f)\approx\tfrac12 S_\phi(\Delta f)$（規範第 3 節公式 16）：

$$
\mathcal{L}(\Delta f)=10\log_{10}\!\left[\frac{1}{2}\cdot\frac{K_{VCO}^2\,S_v(\Delta f)}{\Delta f^2}\right]\qquad(\text{dBc/Hz}).
$$

supply 版完全平行：把 $K_{VCO}\to K_{push}$、$S_v\to S_{v,DD}$（電源電壓雜訊 PSD）即可。**兩條門的貢獻是兩個獨立源，功率相加**：$S_\phi^{tot}=\dfrac{K_{VCO}^2 S_{v,tune}+K_{push}^2 S_{v,DD}}{\Delta f^2}+(\text{device ISF 那一份})$。

## 第 3 步：白噪 tune line → $1/f^2$；$1/f$ tune line → $1/f^3$（與 device $c_0$ 平行）

第 2 步的 $S_\phi\propto S_v/\Delta\omega^2$ 把 tune line 的**頻譜形狀**原樣繼承，再乘 $1/\Delta\omega^2$。兩種情形：

**情形 A — tune line 是白噪（$S_v=$ 常數）：** 例如串聯電阻熱雜訊、buffer 寬頻雜訊。則

$$
S_\phi=\frac{K_{VCO}^2\,S_{v,0}}{\Delta f^2}\ \propto\ \frac{1}{\Delta f^2}\quad\Rightarrow\quad -20\ \text{dB/decade}\ (1/f^2).
$$

這跟 device 白噪經 ISF 得到的 $1/f^2$ **斜率一模一樣、機制一模一樣**（都是白入口 → $1/\Delta\omega^2$ 積分器）。

**情形 B — tune line 是 $1/f$ 雜訊（$S_v=k_v/\Delta f$）：** 例如 charge pump / band-gap / LDO 參考的低頻 flicker，或 varactor 偏壓電路的 $1/f$。則

$$
S_\phi=\frac{K_{VCO}^2}{\Delta f^2}\cdot\frac{k_v}{\Delta f}=\frac{K_{VCO}^2\,k_v}{\Delta f^3}\ \propto\ \frac{1}{\Delta f^3}\quad\Rightarrow\quad -30\ \text{dB/decade}\ (1/f^3).
$$

**這正是 device flicker 機制的「外部電壓版」**。把兩條 $1/f^3$ 路並排：

| 機制 | 入口（低頻源） | 上轉的「閘門」 | $1/f^3$ 公式骨架 |
|---|---|---|---|
| **device flicker**（[P1] Eq.(23)） | device $1/f$ 電流 $\overline{i_n^2}\,\omega_{1/f}/\Delta\omega$ | ISF 的 DC 項 $c_0$ | $\mathcal{L}\propto\dfrac{c_0^2}{q_{max}^2}\dfrac{\overline{i_n^2}/\Delta f}{\Delta\omega^2}\dfrac{\omega_{1/f}}{\Delta\omega}$ |
| **tune/supply $1/f$**（本頁） | 控制電壓 $1/f$ 雜訊 $S_v=k_v/\Delta f$ | VCO 增益 $K_{VCO}$（或 $K_{push}$） | $\mathcal{L}\propto K_{VCO}^2\,\dfrac{k_v}{\Delta f^3}$ |

- **平行在哪**：device 版的「閘門」是 ISF 的 DC 傅立葉係數 $c_0$（[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) 第 2 步說「$c_0$ 是 flicker 通往載波的唯一閘門」）；tune line 版的「閘門」就是 $K_{VCO}$。**$K_{VCO}$ 在外部電壓世界扮演的角色，就是 $c_0$ 在 device 電流世界扮演的角色**——兩者都是「把一個低頻源接上 $1/\Delta\omega^2$ 積分器」的轉換增益，且都以**平方**進入 $\mathcal{L}$（$c_0^2$ vs $K_{VCO}^2$）。
- **差別（誠實講）**：device 版的 $c_0$ 可以靠**波形對稱**壓到近 0（救得了 flicker）；tune line 版的 $K_{VCO}$ **不能歸零**（歸零就調不動頻率了）——只能**縮小**（split tuning）或**把入口 $S_v$ 弄乾淨**（LDO）。所以這扇門是「永遠半開」的，設計上反而更需要正面對付。
- **斜率記憶法**：分母每多一個 $1/\Delta\omega$ 就多 $-10$ dB/dec。白噪入口 + 積分器 = $1/\Delta\omega^2$（$-20$）；$1/f$ 入口（$+1$ 個 $1/\Delta\omega$）+ 積分器 = $1/\Delta\omega^3$（$-30$）。和 device 端的數法完全一致。

## 第 4 步：varactor $C(V)$ 非線性 → AM-PM

到此為止 $K_{VCO}$ 都當常數。但 varactor 的本質是**非線性電容** $C(V)$——這帶來第二條更隱蔽的門：**AM-PM conversion（振幅調變轉相位調變）**，也就是 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 第 4 步講的後門。

機制鏈（每一環都用既有觀念）：

1. **頻率由 tank 總電容決定**：LC 振盪 $f_0=\dfrac{1}{2\pi\sqrt{L\,C_{tot}}}$，而 $C_{tot}$ 含 varactor 的 $C(V)$。
2. **varactor 看到的是「偏壓 + 振盪 swing」**：node 電壓是 $V_{tune}+v_{osc}(t)$，振幅 $A$ 的正弦擺幅每週期掃過 $C(V)$ 曲線。
3. **非線性 → 有效電容隨 swing 變**：因為 $C(V)$ 彎曲，一個週期內的**平均有效電容** $\bar C(A)$ 會隨振幅 $A$ 改變（把 $C(V)$ 在偏壓點泰勒展開，二階項 $\tfrac12 C''(V_{tune})\langle v_{osc}^2\rangle$ 正比於 $A^2$，不為零）。於是 $f_0$ 變成振幅的函數 $f_0(A)$。
4. **這就是 $\partial\omega/\partial A\ne0$**：振幅雜訊 $\Delta A$（本來會被 limit cycle 的恢復力吃掉）透過 $\partial f_0/\partial A$ 漏成頻率/相位雜訊，再被第 2 步的積分器**永久累積**成 close-in 裙邊。

$$
\Delta\omega_{AM\text{-}PM}=\frac{\partial\omega_0}{\partial A}\,\Delta A,\qquad \frac{\partial\omega_0}{\partial A}\propto C''(V_{tune})\ \ (\text{varactor 曲率}).
$$

- **物理意義**：原本「被抑制」的振幅雜訊（[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 主張振幅有恢復力）走了 varactor 曲率這條後門，**復活成長壽的相位雜訊**，尤其把 device 的 $1/f$ 振幅起伏上轉到 close-in，惡化 $1/f^3$。
- **關鍵設計推論**：AM-PM 正比於 $C''(V_{tune})$（曲線**曲率**），不是 $C'$（斜率，那是 $K_{VCO}$）。所以**偏壓在 $C(V)$ 的反曲/平坦點**可使 $C''\approx0$，AM-PM 大幅下降——這跟「縮小 $K_{VCO}$」是**兩個不同的鈕**（一個管曲率、一個管斜率）。
- **單位/量綱**：$\partial\omega_0/\partial A$ 是 $(\text{rad/s})/\text{V}$；乘振幅雜訊 $\Delta A$（V）得 rad/s，再積分成相位 ✓。
- **詳細的 amplitude-modulation 與大訊號分析是 [P4] 的主軸（進階）**；varactor $C(V)$ 的精確閉式屬器件文獻（外部文獻，非本站 5 篇 PDF）。本頁只把鏈條接到既有的 AM-PM 觀念。

## 第 5 步：Design knobs（把兩扇門關小）

把上面的物理直接翻成可操作的鈕。每個鈕標明它**動哪個量**。

- **Split tuning（分段調諧）——縮小 $K_{VCO}$。** 最重要的一招（外部文獻，非本站 5 篇 PDF）。把調諧拆成兩層：
  - **coarse（粗調）：switched-capacitor bank（開關電容陣列，用數位碼切入/切出固定電容）**。它用**數位碼**選頻段，提供大部分調諧範圍，但**對連續電壓雜訊免疫**（碼不抖，電容就不抖）。
  - **fine（細調）：varactor**，只負責一個小子頻段的連續微調。
  - 效果：總調諧範圍 = 粗調（數位、無雜訊）⊕ 細調（小範圍），而 **fine varactor 的 $K_{VCO}$ 因為只跨小頻段而大幅下降**。由第 2 步 $S_\phi\propto K_{VCO}^2$，$K_{VCO}$ 減半 → tune line 那一份相位雜訊**降 6 dB**。這是把「範圍 vs 雜訊」的張力解開的標準手法。
- **偏壓在 $C(V)$ 平坦點——壓 AM-PM（管 $C''$）。** 選 varactor 工作點讓 $C''(V_{tune})\approx0$（曲率小），$\partial\omega/\partial A\to0$，AM-PM 後門關小。注意這跟縮 $K_{VCO}$ 是不同鈕：平坦點壓的是**二階曲率**，不是一階斜率。
- **Supply regulation / LDO——壓 $S_{v,DD}$ 入口（外部文獻，非本站 5 篇 PDF）。** 對付 supply pushing：在 VCO 前面放一顆 **LDO（low-dropout regulator，低壓差穩壓器，把髒電源濾成乾淨的本地電源）**，把 $S_{v,DD}$（到達 VCO 的電源雜訊 PSD）壓低數十 dB。由 supply 版公式 $S_\phi\propto K_{push}^2 S_{v,DD}$，降 $S_{v,DD}$ 等比降相位雜訊。也可同時降 $K_{push}$（拓樸層面：對稱 bias、減少電源對 swing 的調變）。
- **Common-mode rejection（共模抑制）——讓差動 VCO 對共模電源/基板雜訊免疫。** 差動 tank 上，電源/基板雜訊多以**共模**形式出現；好的 differential 對稱使共模擾動**不轉成差模頻率偏移**（理想上 $K_{push,CM}\to0$）。這跟 [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) 第 6 步的 differential 觀念同源，但這裡對付的是**外部共模電壓**而非 device $c_0$。
- **乾淨的 $V_{tune}$ 路徑——壓 $S_{v,tune}$ 入口。** loop filter 的電阻熱雜訊、charge-pump 的 $1/f$、band-gap 參考雜訊都會灌進 $V_{tune}$；這些是 [pll_noise_budget](/06_design_insights/pll_noise_budget) 裡「in-band」那幾項的物理出口。在 PLL 內，loop bandwidth 也決定這些 tune line 雜訊被高通/低通到何種程度。

> **設計鐵律（一句話）**：tune/supply 這兩扇門的相位雜訊 $=$（轉換增益 $K^2$）$\times$（入口電壓雜訊 $S_v$）$\times$（$1/\Delta f^2$ 積分器）。三個因子各有對應的鈕：$K$ 用 **split tuning / 對稱拓樸**壓、$S_v$ 用 **LDO / 乾淨參考 / 低雜訊 loop filter** 壓、曲率衍生的 AM-PM 用**平坦偏壓點**壓。

## Worked example（帶單位 + dimension check）

> **例 G（tune line 白噪 → $\mathcal{L}$）**：$K_{VCO}=50$ MHz/V、tune line 電壓雜訊 $100$ nV$/\sqrt{\text{Hz}}$（即 $\sqrt{S_v}=100$ nV$/\sqrt{\text{Hz}}$）於 $\Delta f=1$ MHz offset、$f_0=5$ GHz。求 $\mathcal{L}(1\,\text{MHz})$。

**步驟 1（把 $\sqrt{S_v}$ 平方成 PSD）**：

$$
S_v=(100\ \text{nV}/\sqrt{\text{Hz}})^2=(10^{-7}\ \text{V}/\sqrt{\text{Hz}})^2=10^{-14}\ \text{V}^2/\text{Hz}.
$$

**步驟 2（電壓雜訊 → 頻率偏差密度，建立手感）**：頻率偏差的 rms 密度 $=K_{VCO}\sqrt{S_v}=5\times10^7\ \text{Hz/V}\times10^{-7}\ \text{V}/\sqrt{\text{Hz}}=5\ \text{Hz}/\sqrt{\text{Hz}}$。也就是這條 tune line 在 1 MHz offset「每 $\sqrt{\text{Hz}}$ 抖 5 Hz 的頻率」。

**步驟 3（套第 2 步的 $S_\phi$，用 Hz 形式）**：

$$
S_\phi=\frac{K_{VCO}^2\,S_v}{\Delta f^2}=\frac{(5\times10^{7})^2\times10^{-14}}{(10^{6})^2}=\frac{(2.5\times10^{15})\times10^{-14}}{10^{12}}=\frac{25}{10^{12}}=2.5\times10^{-11}\ \text{rad}^2/\text{Hz}.
$$

**步驟 4（SSB）**：$\mathcal{L}=\tfrac12 S_\phi=1.25\times10^{-11}$，取 $10\log_{10}$：

$$
\mathcal{L}(1\,\text{MHz})=10\log_{10}(1.25\times10^{-11})=-109.0\ \text{dBc/Hz}.
$$

- **結果**：$\mathcal{L}(1\,\text{MHz})\approx-109$ dBc/Hz——**單這一條 tune line 白噪源**就貢獻 $-109$ dBc/Hz。對照「單一 device 白噪源」的 canonical 例 B（$-148$ dBc/Hz，[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)），tune line 在同一 offset **高了近 40 dB**——這說明**一條沒處理好的 tune line 可以輕易主導整顆 VCO 的 $1/f^2$ 區**，正是為什麼 split tuning / 乾淨 $V_{tune}$ 這麼關鍵。
- **dimension check**：$\dfrac{(\text{Hz/V})^2\cdot(\text{V}^2/\text{Hz})}{\text{Hz}^2}=\dfrac{\text{Hz}^2\cdot\text{V}^{-2}\cdot\text{V}^2\cdot\text{Hz}^{-1}}{\text{Hz}^2}=\text{Hz}^{-1}$ → $S_\phi$ 為 $\text{rad}^2/\text{Hz}$ ✓。
- **$f_0=5$ GHz 去哪了？（誠實註記）**：本式的 $\mathcal{L}$ **不顯含 $f_0$**——$f_0$ 是這條裙邊「坐在哪根載波上」的位置，但 $1/f^2$ 裙邊的高度由 $K_{VCO}^2 S_v/\Delta f^2$ 決定，與 $f_0$ 無關。$f_0$ 真正進場是在換算 timing jitter 時（$\Delta t=\Delta\phi/2\pi f_0$，見 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)），或在以 $\text{ppm/V}$ 表示 $K_{VCO}/f_0$ 的相對靈敏度時。給定 $f_0=5$ GHz 是為了讓你知道這是顆 5 GHz VCO，但別把它硬塞進 $\mathcal{L}$ 公式。

```python
import math
K_vco = 50e6          # Hz/V
S_v   = (100e-9)**2   # V^2/Hz  (100 nV/sqrt(Hz))
df    = 1e6           # Hz offset
S_phi = K_vco**2 * S_v / df**2          # rad^2/Hz
L     = 10*math.log10(0.5*S_phi)        # SSB, L = (1/2) S_phi
print(S_phi, L)        # -> 2.5e-11 rad^2/Hz, -109.03 dBc/Hz
```

> **例 H（supply pushing → $\mathcal{L}$，平行驗證）**：$K_{push}=2$ MHz/V、電源雜訊 $1\ \mu\text{V}/\sqrt{\text{Hz}}$（$S_{v,DD}=10^{-12}\ \text{V}^2/\text{Hz}$）於 $\Delta f=1$ MHz。求 supply 那一份 $\mathcal{L}$。

$$
S_\phi=\frac{K_{push}^2 S_{v,DD}}{\Delta f^2}=\frac{(2\times10^{6})^2\times10^{-12}}{(10^{6})^2}=\frac{4\times10^{12}\times10^{-12}}{10^{12}}=4\times10^{-12}\ \text{rad}^2/\text{Hz},
$$

$$
\mathcal{L}=10\log_{10}(\tfrac12\times4\times10^{-12})=10\log_{10}(2\times10^{-12})=-117.0\ \text{dBc/Hz}.
$$

- **手感**：即使 $K_{push}$ 比 $K_{VCO}$ 小 25 倍，一個「只有」$1\ \mu\text{V}/\sqrt{\text{Hz}}$ 的髒電源仍貢獻 $-117$ dBc/Hz。放一顆把 $S_{v,DD}$ 降 20 dB 的 LDO（電壓雜訊降 10 倍），這一份就降 20 dB 到 $-137$ dBc/Hz——這就是 LDO 對 supply pushing 的直接價值。
- **dimension check**：同例 G，$\text{Hz}^{-1}$ → $\text{rad}^2/\text{Hz}$ ✓。

```python
# supply pushing 平行版：同一公式，K_vco->K_push, S_v->S_vdd
K_push, S_vdd, df = 2e6, (1e-6)**2, 1e6
S_phi = K_push**2 * S_vdd / df**2
print(10*math.log10(0.5*S_phi))   # -> -117.0 dBc/Hz
```

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 控制/電源雜訊很慢（$\Delta\omega\ll\omega_0$，準靜態） | $K_{VCO}/K_{push}$ 為常數、FM 模型成立 | 高頻（接近 $f_0$）時要回到 ISF/HTM 的逐諧波處理 |
| $K_{VCO}$ 在工作點近似線性 | 單一斜率 $\partial f_0/\partial V$ 足夠 | varactor 強非線性 → $K_{VCO}$ 隨 $V_{tune}$ 變、且生 AM-PM（第 4 步） |
| 小擾動、相位線性 | $S_\phi=K^2 S_v/\Delta f^2$ 成立 | 大電壓擺動 → 高階 FM sidebands、頻譜失真 |
| AM-PM 可忽略（$C''\approx0$） | 「只算 FM」近似良好 | 強曲率 → 振幅雜訊復活成相位雜訊，需 [P4] APF 框架 |
| 各源獨立 | 功率直接相加 $S_\phi^{tot}=\sum$ | 相關源（共用參考）需考慮相關項，共模抑制可幫忙 |

## 與哪些 paper／公式對應

- **相位積分器 $1/\Delta\omega^2$** 與 device 白噪 $1/f^2$、flicker $1/f^3$ 的結構：[P1] Eq.(11)/(13), p.182–183（相位是 noise 的積分）、Eq.(21) p.185（$1/f^2$）、Eq.(23) p.185（$1/f^3$，$c_0$ 閘門）。本頁把「$c_0$ 閘門」類比成「$K_{VCO}$ 閘門」。
- **AM-PM / amplitude modulation** 的完整框架：[P4]（APF、amplitude decay，進階；見 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)）。
- **$K_{VCO}/K_{push}$ 定義、split tuning、switched-cap bank、LDO、varactor $C(V)$、共模抑制、pushing figure** 等電路/拓樸/儀器具體：**標準 RF IC 設計文獻（外部文獻，非本站 5 篇 PDF）**——Razavi *RF Microelectronics*、Leeson 模型、廠商 datasheet。
- $\mathcal{L}\approx\tfrac12 S_\phi$：規範第 3 節公式 16（小角 PM）。

## 重點回顧

- **$K_{VCO}=\partial f_0/\partial V_{tune}$、$K_{push}=\partial f_0/\partial V_{DD}$**（皆 Hz/V）：把外部電壓世界接到頻率世界的轉換增益。
- tune/supply 節點的雜訊電壓 $v_n$ **FM 載波**：$\Delta f=K\,v_n$ → 相位是頻率的積分 → **$S_\phi=K^2 S_v/\Delta f^2$**（與 ISF 白噪用的是**同一個 $1/\Delta\omega^2$ 積分器**）。
- **白噪 tune line → $1/f^2$**；**$1/f$ tune line → $1/f^3$**。$K_{VCO}$ 在外部電壓世界的角色 $=$ ISF 的 $c_0$ 在 device 電流世界的角色（都以平方進 $\mathcal{L}$），但 $K_{VCO}$ 不能歸零、只能縮小。
- **varactor $C(V)$ 非線性 → AM-PM**：$\partial\omega/\partial A\propto C''(V_{tune})$，把被抑制的振幅雜訊復活成相位雜訊；**偏壓平坦點（小 $C''$）** 壓它（與縮 $K_{VCO}$ 是不同鈕）。
- design knobs：**split tuning（coarse switched-cap + fine varactor，縮 $K_{VCO}$）**、平坦偏壓點（壓 AM-PM）、**LDO / 乾淨參考（壓 $S_v$ 入口）**、**共模抑制（對付 supply/基板共模）**。
- 數值：$K_{VCO}=50$ MHz/V、$100$ nV$/\sqrt{\text{Hz}}$ @ 1 MHz → $\mathcal{L}(1\,\text{MHz})=-109$ dBc/Hz（單一條 tune line 就能主導 $1/f^2$ 區）；$\mathcal{L}$ 不顯含 $f_0$。

## 延伸閱讀

- $1/\Delta\omega^2$ 積分器與白噪 $1/f^2$ 的母源：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- 與本頁畫平行的 $c_0$ → $1/f^3$ 機制：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- AM-PM 後門與 amplitude noise 為何被抑制：[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)
- tune line 雜訊在環路中如何被高通/低通、最佳 loop BW：[pll_noise_budget](/06_design_insights/pll_noise_budget)
- swing/$q_{max}$ 槓桿（另一條獨立鈕）：[tank_swing](/06_design_insights/tank_swing)
- 哪些 knob 改 $\Gamma_{rms}$、哪些改 $q_{max}$：[device_noise_mapping](/06_design_insights/device_noise_mapping)
