---
title: 統一符號表 Notation
description: 全站一致的符號、單位、與各論文之間的符號對照。
---

# 統一符號表 Notation

不同論文用不同符號寫同一件事，這頁把它們**統一**，往後所有章節都照這張表。
若你在某篇論文看到不同寫法，回到這裡對照即可。

> **怎麼用這頁**：先掃一遍混個臉熟；真正讀推導時，遇到不懂的符號回來查。
> 每個量都標了**單位**——做 dimension check（因次檢查）是抓錯最快的方法。

## 主要符號

| Symbol | Meaning（中文直覺） | Unit | Used in | Notes |
|---|---|---|---|---|
| $t$ | 時間 | s | all | — |
| $\tau$ | noise／impulse 的「注入時刻」 | s | [P1] | ISF 的自變數是注入相位 $\omega_0\tau$；**碰撞提示**：本頁另有 $\tau_0$（振幅記憶時間／jitter 平均窗，三義見下方辨析）與 Allan $\sigma_y(\tau)$ 的 $\tau$（平均時間），三者字面相近但物理不同 |
| $T$ | 振盪週期 $T=1/f_0$ | s | all | — |
| $\omega_0$ | 振盪角頻率 $=2\pi f_0$ | rad/s | all | — |
| $f_0$ | 振盪頻率（carrier） | Hz | all | 例：5 GHz |
| $\phi(t)$ | excess phase（多餘相位，理想相位之外的偏差） | rad | [P1][P2] | phase noise／jitter 就住在這裡 |
| $\Delta\phi$ | 相位步階／相位誤差 | rad | all | 一次 impulse 造成的跳變 |
| $A(t)$ | 瞬時振幅 | V 或 normalized | [P1][P4] | 擾動會被拉回（見 [P4] APF） |
| $\Gamma(\omega_0\tau)$ | **ISF**，振盪器對 noise 的「相位敏感度」，無因次、$2\pi$ 週期 | — | [P1] | 不是 noise 本身，是權重函數；**碰撞提示**：大寫 $\Gamma$（ISF）與小寫 $\gamma$（MOSFET 熱雜訊係數，見下方新增列）字形相近但無關 |
| $\tilde\Lambda(\phi)$ | **振幅 ISF**（amplitude ISF，電荷歸一）：單位脈衝電荷打在相位 $\phi$ 造成的**初始**相對振幅變化 $D(0,\phi)$ | 1/C | [P4] | [P4] Eq.(18),(24)；tilde 表電荷歸一（同 $\tilde\Gamma=\Gamma/q_{max}$）；ideal LC $\tilde\Lambda=\cos\phi/q_{max}$；[P4] 註 6 的 $\Lambda\equiv q_{max}\tilde\Lambda$ 是其引文 [28] 的無因次版，本站不用 |
| $\Delta(\phi)$ | **APF**（amplitude perturbation function，振幅擾動函數）$=\int_0^\infty D\,d\tau=\tilde\Lambda\int_0^\infty d\,d\tau$；ideal LC $=\tau_0\tilde\Lambda$ | 1/A | [P4] | [P4] Eq.(19),(25)；APF 本身**不帶 tilde**；基波 $\Delta_1=\frac{\tau_0}{q_{max}}\angle0°$（Eq.(26)）；帶引數的函數 $\Delta(\cdot)$，勿與差分前綴 $\Delta q$、$\Delta\omega$ 混淆 |
| $q_{max}$ | 節點最大電荷擺幅 $=C\cdot V_{max}$ | C | [P1] | normalize 用；越大 phase noise 越低 |
| $\Delta q$ | 注入電荷 $=\int i\,dt$ | C | [P1] | 例：1 fC |
| $i_n(t)$ | noise 電流 | A | [P1][P2] | 注入到節點的雜訊源 |
| $\overline{i_n^2}/\Delta f$ | 電流 noise 功率譜密度（單邊） | A²/Hz | [P1] | white：與頻率無關 |
| $S_i(f)$ | 電流 noise PSD | A²/Hz | all | 同上的另一寫法 |
| $S_\phi(f)$ | phase PSD（單邊） | rad²/Hz | all | 對 $f$ 積分得 $\sigma_\phi^2$ |
| $\mathcal{L}(\Delta f)$ | SSB phase noise（單邊帶相位雜訊） | dBc/Hz | all | $\approx\frac12 S_\phi$；論文原文常寫 $\mathcal{L}\{\Delta\omega\}$ 或 $\mathcal{L}\{\Delta f\}$（大括號，見規範第 3 節 Eq.(19)–(23)），本站頁面多用 $\mathcal{L}(\Delta f)$（圓括號）——**同一個 SSB 量**，$\Delta\omega=2\pi\Delta f$ 只是引數換算，不做全站符號替換 |
| $\Delta f,\ \Delta\omega$ | offset 頻率（離 carrier 多遠） | Hz, rad/s | phase-noise 頁 | $\Delta\omega=2\pi\Delta f$；**這是 phase-noise／PSD 語境的定義**。注入鎖定群（injection_locking_noise、lab_36、paper_004_large_injection_transient、subharmonic_injection、interactive_calculator）改用 $\Delta\omega$ 表**失諧**，見下方「$\Delta\omega$（injection）」列與多義辨析 |
| $\Delta\omega$（injection，失諧） | 振盪器與注入訊號的頻率差 | rad/s | [P3][P4] 及注入群頁面 | 本站慣例 $\Delta\omega\equiv\omega_0-\omega_{inj}$（injection_locking_noise、lab_36 皆如此定義）；[P3]/[P4] 原文本身正負號不一致（[P3] Eq.(9) 前用 $\omega_{inj}-\omega_0$、[P4] p.2130 用 $\omega_{inj}/N-\omega_0$，subharmonic_injection 另寫 $\Delta\omega_0$）——**站內結果只依賴 $\Delta\omega^2$ 或明寫分支**，符號差不影響物理；鎖定條件 $\lvert\Delta\omega\rvert\le\omega_L$ |
| $c_0$ | ISF 的 DC 傅立葉係數（DC 值 $=c_0/2$） | — | [P1] | 控制 1/f upconversion 的關鍵 |
| $c_n,\ \theta_n$ | ISF 第 $n$ 諧波的幅度／相位 | — | [P1] | 把 $n\omega_0$ 附近 noise 搬到 carrier |
| $\Gamma_{rms}$ | ISF 的 rms 值 | — | [P1][P2] | 決定 1/f² phase noise 大小 |
| $\Gamma_{eff}$ | effective ISF（含 cyclostationary） | — | [P1] | $\Gamma_{eff}=\Gamma\cdot\alpha$ |
| $\alpha(\omega_0 t)$ | noise-modulating function（NMF），device 何時在「漏雜訊」 | — | [P1] | $0\le\alpha\le1$，週期；**多義提醒**：fourier_series_of_isf.md 的 toy 模型 `gamma_asymmetric` 另用純量 $\alpha$ 表 ISF 的 DC 偏移（$\Gamma=\cos\theta+\alpha$，$c_0=2\alpha$）、Allan variance 頁的冪律雜訊指數也寫 $\alpha$（$S_y(f)=h_\alpha f^\alpha$，$-2\le\alpha\le2$）——**NMF 函數、toy DC 偏移純量、Allan 冪指數三者字母相同、意義各不相干**，見下方辨析 |
| $\sigma_t$ | rms timing jitter | s | [P2] | SerDes 最在意這個 |
| $\sigma_\phi$ | rms phase | rad | all | $\sigma_t=\sigma_\phi/(2\pi f_0)$ |
| $\kappa$ | ring 累積 jitter 比例常數 | $\sqrt{\mathrm{s}}$ | [P2] | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ |
| $\omega_{1/f}$ | device 的 1/f noise corner | rad/s | [P1] | 注意：≠ phase noise 的 1/f³ corner |
| $N$ | ring oscillator 級數 | — | [P2] | $\Gamma_{rms}\propto N^{-3/2}$；**多義提醒**：注入除頻／子諧波群（[P4] $M{:}N$、subharmonic_injection、injection_locked_division）另用 $N$ 表**頻率比**（$\div N$ 或 $\times N$，$\omega_{inj}\approx N\omega_0$），jitter_kernels.md 的 $\tau_0=NT$ 又用 $N$ 表**週期數**——三個 $N$ 語境不同，見下方辨析 |
| $Q$ | tank 品質因子 | — | [P1] | 出現在 Leeson 對照 |
| $\eta$ | ring 頻率／FOM 的比例常數 | — | [P2] | $f_0=1/(2N\tau_D)$ |
| $\tilde\Gamma=\Gamma/q_{max}$ | 有單位 ISF（電荷歸一） | rad/C | [P3] | $\tilde\Gamma(x)\equiv\Gamma(x)/q_{max}$（[P3] Eq.(26)）；tilde＝電荷歸一，同 $\tilde\Lambda=\Lambda/q_{max}$（見上方振幅 ISF 列）；本站核心教學仍以無因次 $\Gamma$ 為主，注入鎖定各頁改用 $\tilde\Gamma$ |
| $\omega_L,\ \omega_L^{\pm}$ | （半）lock range | rad/s | [P3][P4] | 正弦注入 $\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$（[P3] Eq.(35), p.2114）；ideal LC $=I_{inj}/(2q_{max})$；鎖定條件 $\lvert\Delta\omega\rvert\le\omega_L$；canonical $f_L=\omega_L/2\pi=5$ MHz（injection_locking_noise 例）；不對稱時 $\omega_L^+\ne-\omega_L^-$（[P4] Eq.(23)） |
| $I_{inj},\ i_{inj}(t)$ | 注入電流的振幅／瞬時波形 | A | [P3] | $i_{inj}(t)$ 出現在時間同步平均積分 $\Omega(\theta)=\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma\,i_{inj}\,dt$（[P3] Eq.(30), p.2113）；正弦注入時 $I_{inj}$ 為其振幅 |
| $q_{inj}$ | 一根注入脈衝的電荷 | C | [P3] | [P3] Sec. IV, p.2112（脈衝列思想實驗）；canonical 50 fC（$q_{max}$ 的 5%，見 injection_locking_noise 數值例） |
| $\omega_{inj}$ | 注入訊號角頻率 | rad/s | [P3][P4] | 與 $\omega_0$ 的差即失諧，見上方 $\Delta\omega$（injection）列 |
| $\theta(t),\ \theta_{ss}$ | 振盪器相對注入的相對相位／其穩態值 | rad | [P3] | 座標變換 $\theta=\phi-\omega_{inj}t$（[P3] Eq.(4)：$\phi(t)\equiv\omega_{inj}t+\theta(t)$）；鎖定穩態 $\sin\theta_{ss}=\Delta\omega/\omega_L$、穩定支 $\cos\theta_{ss}\gt0$；**與上方 ISF 引數 $\omega_0\tau$ 同軸、但與 $c_n,\theta_n$ 列的傅立葉相位 $\theta_n$ 無關** |
| $\Omega(\theta)$ | lock characteristic（注入造成的平均頻率偏移，隨 $\theta$ 的函數） | rad/s | [P3] | [P3] Eq.(33), p.2114：$\Omega(\theta)=\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt$；lock range＝其值域寬度 |
| $a$ | LC 注入強度比 | — | [P4] | $a\equiv I_{inj}/I_{osc}$（[P4] Eq.(8), Mirzaei's Generalized Adler）；大注入 $\omega_L=\omega_{L0}/\sqrt{1-a^2}$；恆等式 $\omega_0 q_{max}=Q\,I_{osc}$ 下 $a=\tau_0\,\omega_{L0}$（精確） |
| $M$ | （因語境而異，見下方辨析） | — | [P4] 及量測頁 | [P4] Eq.(28)–(30), p.2129 的 $M{:}N$ 次諧波鎖定比（$M=1$ 即除頻）；measurement_and_spurs.md 的 cross-correlation **平均次數**——二者字母相同、意義無關 |
| $\beta$（realignment factor） | 一根脈衝把相位誤差拉回的比例 | — | 本站／ILCM 慣例 | $\beta\equiv-q_{inj}\,\tilde\Gamma'(\theta_{ss})$（subharmonic_injection.md 定義，**非 [P3][P4] 原文符號**）；穩定 $0\lt\beta\lt2$；連續極限 $\omega_c=\beta/T_{inj}$（見下方 $\omega_c$ 辨析）；**與下列 $\beta_{[P4]}$、FM 調變指數 $\beta$（varactor 頁）、MOS $\beta$（lab_32 平方律增益因子）四義不同** |
| $\beta_{[P4]}$ | ISF 基波與 APF 基波的相位差 | rad | [P4] | $\beta\equiv\angle\tilde\Gamma_1-\angle\Delta_1$（[P4] Eq.(23), p.2127）；ideal LC：$\angle\tilde\Gamma_1=90°,\ \angle\Delta_1=0°\Rightarrow\beta_{[P4]}=90°$（quadrature）；決定大注入 lock range 是否對稱（$\beta_{[P4]}=\pm90°$ 時對稱，見 [P4] Eq.(23) 下方討論） |
| $\gamma$ | MOSFET 通道熱雜訊係數 | — | [P2] | $\overline{i_n^2}=4kT\gamma g_m$；長通道 $\gamma=2/3$；**$\gamma\ne\Gamma$（ISF，見上）、$\gamma\ne$ Euler–Mascheroni 常數**（99_appendix 用到後者時另註）；ring FOM（[P2] Eq.(23)）前置係數是 $8/(3\eta)$，$\gamma$ 僅透過下列 $V_{char}=\Delta V/\gamma$ 進入 |
| $\Delta V$ | 差動對線性化電壓擺幅 | V | [P2] | 長通道 $\Delta V=V_{GS}-V_T$、短通道 $\Delta V=E_cL$（[P2] p.796） |
| $V_{char}$ | ring FOM 的特徵電壓 | V | [P2] | $V_{char}=\Delta V/\gamma$；出現在 [P2] Eq.(23) 的 $V_{DD}/V_{char}$ 項 |
| $F_{eff}$ | 拓樸雜訊因子（FOM 天花板的可變部分） | — | 本站（fom_limit.md，外部 FOM 慣例） | $\mathrm{FOM}=173.8-10\log_{10}F_{eff}$ dB（300 K）；常數 $173.8=-10\log_{10}(kT\cdot1\,\text{Hz}/1\,\text{mW})$ 對應 $1\cdot kT$（**不是** $2kT$，那會給 $170.8$）；ring $F_{eff}\ge3.6$（天花板 168.3 dB）、LC $F_{eff}\propto1/Q^2$ |
| $K_{VCO}$ | VCO tuning gain | Hz/V（或 rad/s/V） | 本站（varactor_tuning_supply_pushing.md） | $K_{VCO}\equiv\partial f_0/\partial V_{tune}$；worked example 50 MHz/V |
| $K_{push}$ | supply pushing gain | Hz/V | 本站 | $K_{push}\equiv\partial f_0/\partial V_{DD}$；lab_38（Level-1 MOS ring，第一性量測）實測 2.936 GHz/V |
| $H_{lp}(f),\ H_{hp}(f)$ | PLL 閉環低通／高通轉移函數 | — | 本站（pll_noise_budget.md） | $S_{out}=(S_{ref}N^2+S_{cp})\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$；type-II 二階，以 $\omega_n,\zeta$ 參數化（見下方 $\omega_n/f_n$、$\zeta$ 辨析） |
| $S_{ref},\ S_{vco},\ S_{cp}$ | PLL 各雜訊源（reference／VCO／charge-pump）的 PSD | rad²/Hz | 本站 | 三個統計獨立源，功率相加進 $S_{out}$（見上列） |
| $D$（本站慣例乙） | phase diffusion 係數 | rad²/s | 本站／外部文獻（Demir 2000） | $D=\kappa^2/2=\Gamma_{rms}^2 S_i/(4q_{max}^2)$，canonical $0.0625$（diffusion_dictionary.md 規範 11.2, v5）；配 $\mathrm{Var}[\Delta\phi]=2D\lvert t\rvert$；3-dB 線寬 $\Delta f_{3dB}=D/\pi=\kappa^2/2\pi\approx19.9$ mHz（真 LC $39.8$ mHz）；**$\ne$ [P4] 的 $D(\tau,\phi)$**（振幅擾動函數，見上方 $\tilde\Lambda$ 列） |
| $\sigma_y(\tau),\ h_\alpha$ | Allan deviation／frequency-metrology 冪律雜訊係數 | 無因次／依 $\alpha$ 而定 | 外部文獻（IEEE 1139，非本站 5 篇 PDF） | $S_y(f)=h_\alpha f^\alpha$，$\alpha=-2,\dots,+2$；此處的 $\tau$ 是**平均時間（gate time）**——與上方 ISF 注入時刻 $\tau$ 碰撞但無關，見該列提示 |
| RJ／DJ／TJ | random／deterministic／total jitter | s | SerDes 業界慣例（dj_dual_dirac.md） | dual-Dirac 外插：$\mathrm{TJ}(\mathrm{BER})=\mathrm{DJ}_{\delta\delta}+2\,Q^{-1}(\mathrm{BER})\,\mathrm{RJ}_{rms}$；$\mathrm{RJ}_{rms}=\sigma_t$（見上方列）；BER $=10^{-12}$ 時乘數 $2Q^{-1}=14.07$ |

## 多義符號辨析（同一符號、不同語境不同意思）

以下符號在**不同頁面**代表不同物理量；每頁自己的定義以該頁為準，這裡只列出「別跟哪個搞混」。

**$\omega_c$（三義，皆非 1/f³ corner $\omega_{1/f^3}$）**：
1. **AM／振幅衰減 corner**（phase_vs_amplitude_noise.md）：$\omega_c=1/\tau_0=\omega_0/2Q$——tank 振幅回復的頻寬。
2. **注入鎖定的 pull-in frequency**（injection_locking_noise.md，即 [P3] Eq.(40) 的原生結果）：$\omega_c=\omega_L\cos\theta_{ss}=\sqrt{\omega_L^2-\Delta\omega^2}$——鎖定範圍正中央最強、邊緣歸零；離散版 $\omega_c=\beta/T_{inj}$（subharmonic_injection.md）。
3. **PLL 開環交越頻率**（pll_noise_budget.md 一帶而過的用法）：loop filter 設計的頻寬指標，與前兩義無關。

**$\tau_0$（三義）**：
1. **振幅記憶時間**（[P4] Sec. III-B, Eq.(25)）：$\tau_0=2Q/\omega_{osc}$，LC 振幅衰減 $e^{-t/\tau_0}$ 的時間常數。
2. **jitter 平均窗**（jitter_kernels.md）：$\tau_0=NT$，累積 $N$ 個週期的觀測窗（$T$ 為振盪週期）。
3. **impulse 注入時刻**（convolution_derivation.md 退化檢查段）：單一 impulse 打在 $\tau_0$，$\phi(t)=\Gamma(\omega_0\tau_0)\Delta q/q_{max}$——這其實是本頁上方 $\tau$ 列的特例，只是那裡剛好也標成 $\tau_0$。

**$\zeta$（二義）**：
1. **PLL 阻尼比**（pll_noise_budget.md）：$\zeta\gt0$，本站 worked design 取臨界附近 $\zeta=0.707$；控制 $H_{lp}/H_{hp}$ 的 peaking。
2. **[P2] Fig.16 accumulated jitter 的二次項係數**（jitter_kernels.md 第 5b 步）：$\sigma(\Delta t)=\sqrt{\kappa^2\Delta t+\zeta^2\Delta t^2}$，時間版無因次（本站已核實印刷值 $2.5\text{e}5$ 缺負號，訂正為 $\zeta=2.5\times10^{-5}$）；相位版 $\zeta_\phi=\omega_0\zeta$（rad/s）。

**$\omega_n,\ f_n$（PLL 自然頻率，本站 PLL 教材慣例，非 5 篇 PDF 內符號）**：loop bandwidth 的中心指標；type-II 二階 peaking 閉式解在 $\zeta=0.707$ 時峰值 $2.09$ dB，位置 $f_{pk}=0.786\,f_n$（pll_noise_budget.md，`# ->` 已驗證：`0.707: closed 0.7862/2.0903 dB`）。

**$\alpha$（三義，皆與上方主表的 NMF $\alpha(\omega_0t)$ 不同語境）**：NMF 函數（本頁主表，$0\le\alpha\le1$、週期）；fourier_series_of_isf.md toy 模型的**純量** DC 偏移（$\Gamma=\cos\theta+\alpha$，$c_0=2\alpha$）；Allan variance 頁的冪律**指數**（$S_y=h_\alpha f^\alpha$）。三者字母相同，定義域、物理意義完全不同，讀到 $\alpha$ 先看頁面語境。

**$N$（三義）**：[P2] ring 級數（$\Gamma_{rms}\propto N^{-3/2}$）；注入除頻／子諧波群的頻率比（$\omega_{inj}\approx N\omega_0$，$\div N$ 或 $\times N$）；jitter_kernels.md 的累積週期數（$\tau_0=NT$）。

**$M$（二義）**：[P4] $M{:}N$ 次諧波鎖定比（$M=1$ 即除頻，見 injection_locked_division.md）；measurement_and_spurs.md 的 cross-correlation 平均次數（本底隨 $M$ 以 $1/\sqrt{M}$ 收斂）。

## jitter 的四種「方言」

很多人把 jitter 混為一談，其實量到的是不同東西：

| 名稱 | 定義 | 直覺 |
|---|---|---|
| **period jitter** | $T_k-T$（單一週期相對 nominal） | 這一拍多長／多短 |
| **cycle-to-cycle jitter** | $T_{k+1}-T_k$（相鄰兩拍差） | 拍與拍之間變化多快 |
| **accumulated / long-term jitter** | 相隔 $\Delta t$ 的兩 edge 誤差，$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ | 開環振盪器越跑越偏 |
| **random jitter (RJ)** | 高斯、無上界，用 $\sigma$ 描述 | SerDes BER 用它估 eye 閉合 |

詳見 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) 與
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

## 各論文符號對照（需要統一之處）

| 概念 | 本站符號 | 各論文寫法／備註 |
|---|---|---|
| ISF | $\Gamma(\omega_0\tau)$ | [P1][P2] 用 $\Gamma$；有些後續文獻用 $h$ 或 ISF |
| 最大電荷 | $q_{max}$ | [P1] $q_{max}=C_{node}V_{max}$；ring 中對應每級節點電荷 |
| offset 頻率 | $\Delta\omega$ 或 $\Delta f$ | [P1] 多用 $\Delta\omega$；datasheet 用 $\Delta f$（Hz） |
| 相位敏感度的振幅版 | 振幅 ISF $\tilde\Lambda$（1/C）／APF $\Delta=\tau_0\tilde\Lambda$（1/A，ideal LC） | [P4] Eq.(18),(24)：$\tilde\Lambda(\phi)=D(0,\phi)$，tilde 表電荷歸一；Eq.(19),(25)：APF $\Delta(\phi)=\int_0^\infty D\,d\tau$，**不帶 tilde**（[P4] 註 6, p.2126：$\Lambda\equiv q_{max}\tilde\Lambda$ 是 [28] 的無因次振幅 ISF）；ideal LC 基波 $\tilde\Gamma_1=\frac{1}{q_{max}}\angle90°$、$\Delta_1=\frac{\tau_0}{q_{max}}\angle0°$（Eq.(26), p.2128），互成 quadrature；$\tau_0=2Q/\omega_0$ |
| 有單位的 ISF | $\tilde\Gamma=\Gamma/q_{max}$ | [P3] Eq.(26)：Hong 用有單位版本（rad/C）；本站核心用無因次 $\Gamma$ |
| 相位方程（injection） | 廣義 Adler | [P3] Eq.(30),(33)：$\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$，$\Omega=\langle\tilde\Gamma\,i_{inj}\rangle$ |
| PPV / adjoint / Floquet | — | **不在這 5 篇 PDF**；屬 Demir 等外部文獻，見 [effective_isf](/03_isf_core_theory/effective_isf) |

> **符號陷阱**：$c_0$ 是傅立葉「係數」，而 ISF 的 DC**值**是 $c_0/2$（見 Eq.(12)）。
> 這個 factor 在算 1/f³ corner（Eq.(24)）時很容易出錯，後面章節會反覆提醒。
