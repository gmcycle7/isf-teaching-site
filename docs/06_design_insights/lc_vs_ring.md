---
title: 從 ISF 看 LC vs ring oscillator
description: 用 ISF 框架逐項比較 LC 與 ring：波形、amplitude restoration、transition slope、tank energy、noisy device 數目、相位敏感度分佈、jitter accumulation、design knobs。
---

# 從 ISF 看 LC vs ring oscillator

> **先備**：[tank_swing](/06_design_insights/tank_swing)（$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$ 與 swing 槓桿）、[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)（LC「高 $Q$ 儲能」到底買到什麼、ring 為何無此優勢）、[rms_isf](/03_isf_core_theory/rms_isf)（$\Gamma_{rms}$ 與 Parseval、ring 的 $N^{-3/2}$ scaling）｜ **接下來**：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)、[varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)

這頁把 ISF 當成一支**統一的尺**，逐項量 LC 與 ring 兩種振盪器的差別。重點不是「誰比較好」
（各有用途），而是**ISF 框架讓我們看見什麼、看不見什麼**。我們會先建一個誠實標明的 toy model，
再用 [P1] / [P2] 的公式把差異量化。

> **物理直覺（先講結論）**：LC 像一個**沉重的鐘擺**——能量大半儲在 tank（$L$、$C$ 來回交換），
> 只有少數 device 偶爾補一點損耗，波形接近正弦、ISF 平滑（$-\sin$）、相位敏感度分散在整個週期。
> ring 像一排**接力傳球的閘**——沒有能量儲存元件，每一級都在切換、每一級都在漏雜訊，波形接近方波、
> ISF 集中在 transition、相位敏感度尖銳。LC 用「儲能 + 高 $Q$」買低 phase noise；ring 用「面積小、
> 可調、多相位輸出」換較差的 phase noise。

## Toy model 假設（誠實標明）

> 以下是 **pedagogical toy model（教學玩具模型，非 transistor-level）**。它抓住定性差異，
> 但不是任何真實電路的量測。

- **LC**：理想 sinusoidal state（正弦狀態），$V(\theta)=\cos\theta$，ISF $\Gamma_{LC}(\theta)=-\sin\theta$
  （[P1] Fig. 7(a)）。amplitude restoration 由 limit cycle 提供（[P1] Sec. III-A）。
- **ring**：$N$ 級 inverter delay + 每級獨立 timing noise；ISF 用 triangular（三角形）toy 形狀，
  峰值 $\sim1/\sqrt{N}$、能量集中在 transition（實際模擬 ISF 曲線見 [P2] Fig. 5, p.793；三角形近似見 [P2] Fig. 6, p.793）。累積 jitter 用 random walk 模型
  $\sigma_{\Delta t}=\sigma_{edge}\sqrt{\Delta N}$（[P2] Eq.(8)）。
- 完整 script：`simulations/lab_02_lc_toy_model.py`、`simulations/lab_03_ring_toy_model.py`。

## 逐項比較表

| 面向 | LC oscillator | Ring oscillator | ISF 怎麼解釋 |
|---|---|---|---|
| 波形 | 接近正弦 | 接近方波（rail-to-rail） | 決定 ISF 形狀（平滑 vs 集中於 transition） |
| ISF 形狀 | $-\sin\theta$，平滑、全週分佈 | 三角形，尖、集中於 transition | 見 [P1] Fig. 7 |
| amplitude restoration | tank + 非線性 $g_m$，徑向擾動衰減 | 每級飽和到 rail，強 restoration | 振幅擾動衰減→只追蹤相位（claim C2） |
| transition slope | 中等（正弦過零斜率） | 陡（快速切換） | 陡邊緣→低 threshold jitter、$\Gamma_{rms}$ 集中 |
| 儲能（tank energy） | 高（$L$、$C$ 來回交換） | 幾乎無儲能 | 高儲能→大 $q_{max}$→低 phase noise |
| noisy device 數目 | 少（1～2 個主動 device） | 多（$N$ 級，每級都漏雜訊） | noise 源越多、貢獻越多（但每級 swing 較小） |
| 相位敏感度分佈 | 分散整個週期 | 集中在 transition 視窗 | $\Gamma_{eff}=\Gamma\cdot\alpha$ 集中 |
| $\Gamma_{rms}$ | $0.5$（$-\sin$ 的 rms） | $\Gamma_{rms}\propto N^{-3/2}$（[P2] Eq.16） | [P2] Eq.(16) |
| jitter accumulation | 慢（高 $Q$ 抗漂移） | 快（無 reference，random walk） | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ |
| 典型 phase noise | 低（好 10～30 dB） | 高 | $\propto\Gamma_{rms}^2/q_{max}^2$ |
| 面積／可調性／多相位 | 大（spiral inductor）、調諧範圍窄 | 小、寬調諧、天生多相位輸出 | （非 ISF 量，但設計常衡量） |

## 第 1 步：$\Gamma_{rms}$——為什麼 LC 的相位敏感度「攤平」

理想 LC $\Gamma_{LC}(\theta)=-\sin\theta$，其 rms：

$$
\Gamma_{rms,LC}=\sqrt{\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta}=\sqrt{\frac{1}{2}}\approx0.707
$$

注意 normalization 慣例：本站用 $\sum_{n=0}^{\infty}c_n^2=2\Gamma_{rms}^2$（[P1] Eq.(20)）。
對 $-\sin\theta$ 只有 $c_1=1$，故 $\sum c_n^2=1=2\Gamma_{rms}^2\Rightarrow\Gamma_{rms}=1/\sqrt2\approx0.707$。
本站 canonical 例子取 $\Gamma_{rms}=0.5$ 作為「含 cyclostationary 折扣後」的代表值——兩者都用，
但**算具體 dBc/Hz 時一律用 canonical $\Gamma_{rms}=0.5$**（見 [notation](/00_overview/notation) 與 [rms_isf](/03_isf_core_theory/rms_isf)）。

下圖把 LC 的 $-\sin$ 與 ring（$N=5,15$）的 triangular ISF 疊在一起：ring 的尖峰隨 $N$ 增大而**變矮**
（峰值 $\sim1/\sqrt N$），但**數目變多**（$N$ 個 transition），整體 $\Gamma_{rms}$ 隨 $N$ 下降。

![LC vs ring 的 ISF 比較](/figures/lc_vs_ring_isf_comparison.png)

## 第 2 步：ring 的三條 [P2] 公式（已對照 PDF 核實）

**(a) ring 頻率**（[P2] Eq.(15), p.794）：

$$
f_0=\frac{1}{2N\,\tau_D}
$$

- $\tau_D$ 是每級延遲。factor 2 因為訊號要繞環**兩圈**才完成一個完整週期（單端 ring 需奇數級反相）。
- **單位檢查**：$1/(N\cdot[\text{s}])=[\text{Hz}]$ ✓。
- **設計含意**：固定 $f_0$ 下，$N$ 越大每級延遲 $\tau_D$ 越小（每級要更快、更陡 transition）。

**(b) ring $\Gamma_{rms}$ scaling**（[P2] Eq.(16), p.794（v7 已重核：根號只蓋常數，Γrms ∝ N^{-3/2}；正文 4/N^{1.5}@η=0.75 與 App.B Eq.(55) 三重驗證。v3 曾誤讀為 N^{-3/4}））：

$$
\Gamma_{rms}=\sqrt{\frac{2\pi^2}{3\eta^3}}\;\dfrac{1}{N^{1.5}}\;\Rightarrow\;\Gamma_{rms}\propto N^{-3/2}\quad(\Gamma_{rms}^2\propto N^{-3})
$$

- 直覺：級數越多，每個 transition 佔週期的「敏感視窗」越窄、單級 ISF 峰值越矮，rms 隨之下降。
- **根號範圍註記**：印刷公式的根號**只蓋常數** $2\pi^2/(3\eta^3)$，$1/N^{1.5}$ 在根號外，故
  $\Gamma_{rms}\propto N^{-3/2}$；$\eta=0.75$ 時 $\sqrt{2\pi^2/(3\cdot0.75^3)}\approx3.95$，即論文正文
  「solid line = $\Gamma_{rms}\approx4/N^{1.5}$」（[P2] Fig. 8），與正文「the $1/N^{1.5}$ dependence of
  $\Gamma_{rms}$」及 App.B Eq.(52)+(54) 的獨立代數三方一致。逐字公式與完整討論見
  [paper_002 deep-dive](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)。

**(c) ring 白噪 phase noise FOM**（[P2] Eq.(23), p.796，已對照原始 PDF 核實 ✓）：

$$
\mathcal{L}\{\Delta f\}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{V_{char}}\cdot\left(\frac{f_0}{\Delta f}\right)^2
$$

- 前置係數是 $8/(3\eta)$：$\eta$ 是級延遲比例常數（[P2] Eq.(14)，$\eta\approx1$）；$\gamma$（MOSFET 通道熱雜訊係數，
  長通道 $2/3$）**僅透過** $V_{char}=\Delta V/\gamma$ 進入。$P$ 是功耗（[P2] Eq.(21)：$P=2\eta N V_{DD}q_{max}f_0$）。
  **注意 $\gamma$（噪聲係數）≠ $\eta$（頻率比例常數）。**
- **單位檢查**：$\dfrac{[\text{J}]}{[\text{W}]}\cdot(\text{無因次})^2=\dfrac{[\text{J}]}{[\text{J/s}]}=[\text{s}]$，取 $10\log_{10}$ 得 dBc/Hz ✓。
- $V_T=0$ 的下限為 [P2] Eq.(25)：$\mathcal{L}>\frac{16\gamma}{3\eta}\frac{kT}{P}(f_0/\Delta f)^2$。
  [P2] Eq.(23) 的前置係數是 $8/(3\eta)$（$\eta$ 為級延遲比例常數 Eq.(14)，$\approx1$）；$\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入。
  （v2 曾誤改為 $8/(3\gamma)$ 並誤標「逐字核實」，v3 已對照原始 PDF p.796 更正。）

**(d) N-independence 結論**（claim C7，已核實）：

關鍵事實：**[P2] Eq.(23) 的 FOM 裡完全沒有 $N$**——固定 $f_0$ 與功率 $P$ 時，single-ended ring 的
phase noise 與級數 $N$ 無關。微觀上，$N$↑ 會降 $\Gamma_{rms}$（Eq.16），但同時降每級擺幅 $q_{max}$
（固定 $f_0$ 下每級要更快）、又增加噪聲級數；這些隨 $N$ 的效應在固定 $P$、$f_0$ 下相互抵消，
最後 Eq.(23) 不含 $N$。完整推導見 [P2] Sec. V 與
[paper_002 deep-dive](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)。

- **結論**：固定中心頻率與功耗下，加級數**不會**改善 ring 的 phase noise／jitter——[P2] 的招牌反直覺結果。
- **設計含意**：選 $N$ 要看調諧範圍、多相位需求、面積、最高 $f_0$，而**不是**為了 phase noise。

## 第 2b 步：差動 ring——N-independence 失落的另一半（[P2] Eq.(31)–(35), p.796，已核實 ✓）

上面的 N-independence 只講了**一半的故事**：它是 **single-ended** CMOS ring 的結論。
[P2] Sec. V-B（p.796）對 **differential（差動）** MOS ring（電阻負載 $R_L$、tail current 偏置）
重做同一套記帳，結局反轉——**phase noise 公式裡明含一個因子 $N$**。以下五條公式均已對照
[P2] 原始 PDF p.796 逐字核實（渲染頁截圖比對）。

**(a) 功率記帳從「動態」變「靜態」**（[P2] Eq.(31), p.796）：

$$
P=N\,I_{tail}\,V_{DD}
$$

- 差動對由 tail current source（尾電流源）恆流偏置：**不管有沒有在切換**，每級都持續從
  $V_{DD}$ 抽 $I_{tail}$（class-A 式的靜態記帳），$N$ 級就是 $N$ 份。
- **單位檢查**：$(\text{無因次})\cdot[\text{A}]\cdot[\text{V}]=[\text{W}]$ ✓。
- 對照 single-ended 的 Eq.(21) $P=2\eta N V_{DD}q_{max}f_0$：那邊是「每週期充放 $q_{max}$」
  的**動態**功耗，功率自動綁著 $f_0$；這邊的**靜態**功耗與 $f_0$ 無關——這個記帳差異就是
  結局反轉的種子。

**(b) 頻率＝tail 電流對節點電荷 slew**（[P2] Eq.(32), p.796）：

$$
f_0=\frac{1}{2Nt_D}\approx\frac{1}{2\eta N t_r}\approx\frac{I_{tail}}{2\eta N q_{max}}
$$

- 最後一步的物理：每級 transition 是 tail current 對節點電荷 $q_{max}$ 做 slew（斜率充放），
  $t_r\approx q_{max}/I_{tail}$，比例常數收進 $\eta$（同 Eq.(14)–(15) 的級延遲常數，$\approx1$）。
- **單位檢查**：$[\text{A}]/([\text{C}])=[\text{A/(A·s)}]=1/\text{s}=[\text{Hz}]$ ✓。
- **factor-2 flag**：$1/(2Nt_D)$ 的 2 是「訊號繞環兩圈才回同相」的物理計數（同 Eq.(15)），
  與 SSB／時域慣例**無關**。

**(c) 固定 $P$、$f_0$ 之下加 $N$：兩條鏈子同時勒緊**

- 由 Eq.(31) 反解：$I_{tail}=P/(N V_{DD})\propto 1/N$——功率固定，多一級就得砍每級電流。
- 代入 Eq.(32)：$q_{max}=I_{tail}/(2\eta N f_0)\propto 1/N^2$——電流變小（$1/N$）**又**要
  在更短的級延遲內完成 transition（再一個 $1/N$）。[P2] p.797 原文（逐字）：
  "increasing the number of stages at a fixed total power dissipation demands a proportional
  reduction of tail-current sources, which will reduce the swing, and hence $q_{max}$,
  **by a factor of $1/N^2$**."
- 對照 single-ended：Eq.(21) 在固定 $P$、$f_0$ 下只給 $q_{max}\propto1/N$（一次方）。差動多
  被勒一次的原因：功率不再隨 $f_0$ 的充放電自動記帳，砍 tail 電流是唯一途徑，而砍電流直接砍 swing。

**(d) 每個節點的雜訊**（[P2] Eq.(33), p.796）：

$$
\frac{\overline{i_n^2}}{\Delta f}=\left(\frac{\overline{i_n^2}}{\Delta f}\right)_{N}+\left(\frac{\overline{i_n^2}}{\Delta f}\right)_{Load}=4kT\,I_{tail}\left(\frac{1}{V_{char}}+\frac{1}{R_L I_{tail}}\right)
$$

- 兩份來源：**差動電晶體**（下標 $N$，指 NMOS 差動管）＋**負載電阻** $R_L$。$V_{char}$：
  long-channel 平衡級為 $(V_{GS}-V_T)/\gamma$、short-channel 為 $E_cL/\gamma$（[P2] p.796 原文）。
- **單位檢查**：$4kT I_{tail}/V_{char}=[\text{J}][\text{A}]/[\text{V}]$；$[\text{J}]=[\text{V·A·s}]$，
  故 $=[\text{V·A·s·A/V}]=[\text{A}^2\text{·s}]=[\text{A}^2/\text{Hz}]$ ✓。
- **$2N$ 個節點**：每級差動有**兩個**輸出節點，全環共 $2N$ 個 single-ended 節點；[P2] p.796
  原文："The phase noise and jitter due to all $2N$ noise sources is $2N$ times the value given
  by (6) and (12)."——這個 2 是**節點計數**，不是 SSB 慣例的 2。
- **tail 源哪去了？**同頁原文："Surprisingly, tail-current source noise in the vicinity of $f_0$
  does not affect the phase noise."——影響 phase noise 的是 tail 的**低頻**雜訊（走 symmetry／$c_0$
  那條 1/f³ 路，見 [symmetry](/06_design_insights/symmetry)）與**偶次諧波附近**的雜訊（可用串聯電感
  ／並聯電容壓制），所以白噪記帳只算差動管＋負載兩份。

**(e) 收斂：差動 ring 的 phase noise 與 jitter 下限**（[P2] Eq.(34)/(35), p.796）：

$$
\mathcal{L}_{min}\{\Delta f\}=\frac{8}{3\eta}\cdot N\cdot\frac{kT}{P}\cdot\left(\frac{V_{DD}}{V_{char}}+\frac{V_{DD}}{R_L I_{tail}}\right)\cdot\frac{f_0^2}{\Delta f^2}
$$

$$
\kappa_{min}=\sqrt{\frac{8}{3\eta}}\cdot\sqrt{N\cdot\frac{kT}{P}\cdot\left(\frac{V_{DD}}{V_{char}}+\frac{V_{DD}}{R_L I_{tail}}\right)}
$$

（$\mathcal{L}$ 即論文的 $L\{\Delta f\}$，本站記號；原文明述兩式 "valid in both long- and
short-channel regimes of operation with the right choice of $V_{char}$"；bipolar 差動 ring 由
Eq.(36), p.797 的 shot＋load noise 併回**同兩式**，$V_{char}=4kT/q_e$。）

與 single-ended 的 Eq.(23) 相比**只差兩處**：多了明含的 $N$；括號多了負載電阻那份
$V_{DD}/(R_L I_{tail})$。$N$ 是從哪裡冒出來的？把 $\mathcal{L}\propto(\text{源數})\cdot\Gamma_{rms}^2\cdot S_i/q_{max}^2$
的指數逐項記帳（toy 記帳，固定 $P$、$f_0$、固定 swing $R_L I_{tail}$）：

| 因子 | single-ended（Eq.23 之路） | differential（Eq.34 之路） |
|---|---|---|
| noise 源數 | $\times N$（每級 NMOS+PMOS 已併入 Eq.18） | $\times 2N\propto N$（每級兩個輸出節點） |
| $\Gamma_{rms}^2$（Eq.16） | $\propto N^{-3}$ | $\propto N^{-3}$ |
| 每源 $S_i$ | $\propto N^{0}$（固定 $P,f_0$ 下 $W$ 不變） | $\propto I_{tail}\propto N^{-1}$（Eq.33 兩項皆是） |
| $1/q_{max}^2$ | $\propto N^{2}$（$q_{max}\propto1/N$） | $\propto N^{4}$（$q_{max}\propto1/N^2$） |
| **乘積** | $N^{1-3+0+2}=N^{0}$ | $N^{1-3-1+4}=N^{+1}$ |

single-ended 恰好全消（$N^0$＝Eq.23 無 $N$）；差動的 $q_{max}\propto1/N^2$ 多貢獻兩個正冪，
淨剩 $N^{+1}$——正是 Eq.(34) 明擺著的那個 $N$。

> **[P2] 自己的結論句（pp.796–797，逐字）**："Note that, in contrast with the single-ended ring
> oscillator, a differential oscillator **does** exhibit a phase noise and jitter dependency on the
> number of stages, with the phase noise **degrading as the number of stages increases** for a given
> frequency and power dissipation. This result may be understood as a consequence of the necessary
> reduction in the charge swing that is required to accommodate a constant frequency of oscillation
> at a fixed power level as $N$ increases."
> ——固定頻率與功耗下，差動 ring 的 phase noise **隨 $N$ 增加而變差**；禍首是被迫縮小的
> charge swing（$q_{max}\propto1/N^2$）。

**慣例 flag（每次出現 2 或 4 都要交代）**：Eq.(34) 的前置係數 $8/(3\eta)$ 與 Eq.(23) 同族，
繼承 [P2] Eq.(6) 的 **SSB 記帳**（與 [P1] Eq.(21) 分母的 4 同一慣例家族；換成時域 $/2$ 慣例
所有絕對 dBc/Hz 數字整體 $+3$ dB，如例 B 的 $-148$（SSB, $/4$）對 $-145$（時域, $/2$），見
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)）。下面例 3 的
$\Delta\mathcal{L}$ 是兩個 $\mathcal{L}$ **相減**，慣例因子相消——**兩種慣例答案相同**。

> **例 3（差動 ring：$N=4$ vs $N=12$，同 $P$、同 $f_0$，$\Delta\mathcal{L}$ 是多少？）**
> 取 $f_0=5$ GHz、$\Delta f=1$ MHz、$kT=4.0\times10^{-21}$ J（300 K）、$P=1$ mW、$\eta\approx1$、
> $V_{DD}/V_{char}=3$（沿用本頁後文例 1 的示意值）、固定-swing 設計 $R_L I_{tail}=V_{DD}/2$
> $\Rightarrow V_{DD}/(R_L I_{tail})=2$（括號 $=3+2=5$，設計上把 $R_L\propto N$ 放大以維持 swing，
> 故括號不隨 $N$ 變）。用 [P2] Eq.(34)。

**逐步代入（帶單位）**：

$$
\begin{aligned}
\left(\frac{f_0}{\Delta f}\right)^2&=(5000)^2=2.5\times10^{7},\qquad
\frac{kT}{P}=\frac{4.0\times10^{-21}\ \text{J}}{1\times10^{-3}\ \text{W}}=4.0\times10^{-18}\ \text{s},\\[4pt]
N=4:\ \mathcal{L}_{min}&=10\log_{10}\!\Big(\tfrac{8}{3}\cdot4\cdot(4.0\times10^{-18})\cdot5\cdot(2.5\times10^{7})\Big)
=10\log_{10}(5.33\times10^{-9})=-82.7\ \text{dBc/Hz},\\[4pt]
N=12:\ \mathcal{L}_{min}&=10\log_{10}\!\Big(\tfrac{8}{3}\cdot12\cdot(4.0\times10^{-18})\cdot5\cdot(2.5\times10^{7})\Big)
=10\log_{10}(1.60\times10^{-8})=-78.0\ \text{dBc/Hz},\\[4pt]
\Delta\mathcal{L}&=10\log_{10}\frac{12}{4}=10\log_{10}3=+4.77\ \text{dB}.
\end{aligned}
$$

- **結果**：級數 4→12（$\times3$），phase noise 從 $-82.7$ 惡化到 $-78.0$ dBc/Hz，差
  $+4.77$ dB。一般式：固定 $P$、$f_0$、電壓比下 $\Delta\mathcal{L}=10\log_{10}(N_2/N_1)$。
  jitter 常數同理：Eq.(35) 給 $\kappa_{min}\propto\sqrt{N}$，$N\times3$ → $\kappa\times\sqrt3\approx1.732$。
- **交叉檢查（對後文例 1 的 single-ended 值）**：差動 $N=4$ 的 $-82.7$ 比 single-ended 的 $-91.0$ 高，可分解為
  括號多了負載份（$3\to5$，$10\log_{10}(5/3)=2.2$ dB）加上 $\times N$（$10\log_{10}4=6.0$ dB）：
  $-91.0+2.2+6.0=-82.8\approx-82.7$（0.1 dB 為中間捨入）✓。
- **Dimension check**：同 Eq.(23)：$\dfrac{[\text{J}]}{[\text{W}]}\cdot(\text{無因次})\cdot(\text{無因次})^2=[\text{s}]$
  → per-Hz 功率比 → $10\log_{10}$ 得 dBc/Hz ✓。
- **Python 驗證**：

```python
import numpy as np
def L_ring_diff(N, kT, P, f0, df, eta=1.0, vdd_vchar=3.0, vdd_swing=2.0):  # [P2] Eq.(34)
    return 10*np.log10(8/(3*eta) * N * (kT/P) * (vdd_vchar + vdd_swing) * (f0/df)**2)
L4  = L_ring_diff(4,  4.0e-21, 1e-3, 5e9, 1e6)
L12 = L_ring_diff(12, 4.0e-21, 1e-3, 5e9, 1e6)
print(round(L4,1), round(L12,1), round(L12-L4,2))   # -> -82.7 -78.0 4.77
```

**適用／失效條件**：

- **適用**：white-noise dominated（symmetry 條件已滿足、1/f 上轉已壓——[P2] Sec. V 開頭的前提）；
  差動對完全切換、電阻負載；Eq.(34)/(35) 在 long-/short-channel 皆成立（選對 $V_{char}$）；
  MOS 或 bipolar（後者經 Eq.(36) 換 $V_{char}=4kT/q_e$）。
- **注意**：$\mathcal{L}_{min}$／$\kappa_{min}$ 是**下限**（同 Eq.(25)/(26) 的邏輯——額外雜訊源、
  不對稱、supply/substrate 都只會更差）；若設計**固定 $R_L$** 而非固定 swing，則
  $V_{DD}/(R_L I_{tail})\propto N$，惡化比 $10\log_{10}N$ **更陡**；$\Gamma_{rms}$ 的 $N^{-3/2}$
  沿用 Eq.(16)，[P2] Fig. 9（p.795）以三種約束情境（fixed power/fixed swing、fixed power/fixed
  $R_L$、fixed tail current/fixed $R_L$）量測差動 ring 的 rms ISF，都貼近同一 scaling。

> **一行設計心法**：single-ended ring＝phase noise 對 $N$ 免疫（Eq.23 無 $N$）；差動 ring＝
> **級數最少的贏**（Eq.34 明含 $N$，每加倍級數 $+3.01$ dB）——在 phase margin、quadrature／
> 多相位、除頻需求允許的**最小 $N$** 停下。

## 第 3 步：jitter accumulation——LC 慢、ring 快

ring 是 free-running、無絕對時間參考，每級 transition 加一點獨立 timing noise，edge 時間做
**random walk（隨機漫步）**，累積 jitter 隨量測區間平方根成長（[P2] Eq.(8), p.792；κ 由 Eq.(12), p.793）：

$$
\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}
$$

- **這是相位 jitter（無因次）**：依 [P2] Eq.(11) $\sigma_{\Delta\phi}^2=\dfrac{\Gamma_{rms}^2\,\overline{i_n^2}/\Delta f}{2q_{max}^2}\,\Delta t$，故 $\kappa\sqrt{\Delta t}$ 給的是 phase jitter $\sigma_{\Delta\phi}$。**時間 jitter** 再經 [P2] Eq.(10) 的相位→時間換算 $\sigma_{\Delta t}=\sigma_{\Delta\phi}/\omega_0$。$\omega_0$ 住在 Eq.(10)，**不在** $\kappa$ 裡。
- **單位檢查**：$\kappa$ 單位 $1/\sqrt{\text{s}}$（$\overline{i_n^2}/\Delta f$ 為 $[\text{A}^2\!\cdot\!\text{s}]$、$q_{max}$ 為 $[\text{A}\!\cdot\!\text{s}]$），故 $\kappa\sqrt{\Delta t}=[1/\sqrt{\text{s}}]\cdot[\sqrt{\text{s}}]=$ 無因次 ✓（phase）；除以 $\omega_0$ $[1/\text{s}]$ 後得 $\sigma_{\Delta t}=[\text{s}]$ ✓（time）。
- $\kappa^2\propto\Gamma_{rms}^2/q_{max}^2\cdot\overline{i_n^2}/\Delta f$（[P2] Eq.(12), p.793，已核實：$\kappa=(\Gamma_{rms}/q_{max})\sqrt{(\overline{i_n^2}/\Delta f)/2}$，無 $\omega_0$）——
  同一個核心比值又出現。
- LC 因高 $Q$，相位漂移慢得多（等效小 $\kappa$）；但**只要是 free-running，兩者長期都會漂**——
  要鎖住絕對時間得靠 PLL/CDR（見 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)）。

下圖是 ring edge 時間的 random walk 蒙地卡羅：rms 累積 jitter 對量測 lag 在 log–log 上是斜率 1/2 的直線：

![ring 累積 timing noise](/figures/ring_oscillator_timing_noise_accumulation.png)

> toy 參數：$f_0=5$ GHz、$\sigma_{edge}=50$ fs/transition、2000 trials。
> 完整 script：`simulations/lab_03_ring_toy_model.py`（`fig_accumulation`）。

## 第 4 步：ISF 看得見什麼、看不見什麼

| 看得見（ISF 框架擅長） | 看不見／需另外處理 |
|---|---|
| 相位敏感度隨注入相位的分佈（$\Gamma$ 形狀） | tank $Q$ 的絕對值、inductor 寄生（要電路模型） |
| white→1/f²、flicker→1/f³ 的 scaling | 強非線性、AM–PM 大訊號效應（一階 ISF 不足） |
| 對稱性→$c_0$→1/f³ corner | supply/substrate 耦合（[P2] 另段定性處理） |
| $\Gamma_{rms}$、$q_{max}$ 的相對槓桿 | 真實 $\Gamma$ 形狀（要 transient/adjoint 萃取） |
| 累積 jitter random walk | 確切 $\kappa$、FOM 常數的絕對值（需完整 device 模型；公式本身見 [P2] Eq.(12)/(23)，已核實） |

## design knobs（LC vs ring 對照）

| 目標 | LC knob | Ring knob |
|---|---|---|
| 降 phase noise（1/f²） | 提高 tank $Q$、加大 swing（$q_{max}$） | 加大每級電流/swing；single-ended：$N$ 幾乎無效；差動：$N$ 越少越好（Eq.34，見第 2b 步） |
| 降 1/f³（close-in） | 對稱 differential、低 $c_0$ | 對稱負載（[P2] Fig. 17 symmetry voltage） |
| 寬調諧 | varactor（範圍窄） | 改 bias 電流/$\tau_D$（範圍寬，ring 強項） |
| 多相位輸出 | 需額外電路 | 天生 $N$ 相位（ring 強項） |
| 小面積 | 大（spiral inductor） | 小（ring 強項） |

## Worked examples 數值例題

以下兩題用 [P2] 的 ring 白噪 FOM 算具體 $\mathcal{L}$，並驗證「固定 $f_0$/功率下 phase noise ~與 $N$ 無關」。
公式已對照 [P2] 原始 PDF 核實；以下取 $\eta\approx1$（級延遲比例常數，進入前置係數 $8/(3\eta)$）、$\gamma=2/3$（長通道，僅透過 $V_{char}=\Delta V/\gamma$ 進入）、$V_{DD}/V_{char}=3$（示意值），數值為量級示範。

> **例 1（用 ring FOM 算 1/f² phase noise，並比較 N=3/5/15）**
> 取 $f_0=5$ GHz、offset $\Delta f=1$ MHz、$kT=4.0\times10^{-21}$ J（300 K）、$P=1$ mW、
> $\eta\approx1$、$\gamma=2/3$（已吸入 $V_{DD}/V_{char}=3$）。用 [P2] Eq.(23) 算 $\mathcal{L}|_{1/f^2}$；此式中 $N$ **不顯式出現**
> （已被 N-independence 吸收），所以 N=3/5/15 給**同一個值**。

**逐步代入（帶單位）**，用 $\mathcal{L}|_{1/f^2}=\dfrac{8}{3\eta}\dfrac{kT}{P}\dfrac{V_{DD}}{V_{char}}\Big(\dfrac{f_0}{\Delta f}\Big)^2$：

$$
\begin{aligned}
\frac{f_0}{\Delta f}&=\frac{5\times10^9}{1\times10^6}=5000,\quad \left(\frac{f_0}{\Delta f}\right)^2=2.5\times10^{7}, \\[4pt]
\frac{kT}{P}&=\frac{4.0\times10^{-21}\ \text{J}}{1\times10^{-3}\ \text{W}}=4.0\times10^{-18}\ \text{s}, \\[4pt]
\frac{8}{3\eta}&=\frac{8}{3}\approx2.667\quad(\eta\approx1),\qquad \frac{V_{DD}}{V_{char}}=3, \\[4pt]
\text{括號}&=2.667\times3\times(4.0\times10^{-18})\times(2.5\times10^{7})=8.0\times(4.0\times10^{-18})\times(2.5\times10^{7})=8.0\times10^{-10}, \\[4pt]
\mathcal{L}|_{1/f^2}&=10\log_{10}(8.0\times10^{-10})=-91.0\ \text{dBc/Hz}.
\end{aligned}
$$

- **結果**：$\mathcal{L}|_{1/f^2}\approx-91.0$ dBc/Hz @ 1 MHz——對 **N=3、N=5、N=15 完全相同**，
  因為固定 $f_0$/$P$ 下各 $N$ 因子相消（claim C7）。這比例 B 的 LC 理想值（$-148$ dBc/Hz）差了 $\sim57$ dB，
  量級上合理：ring 沒有高 $Q$ 儲能、$q_{max}$ 小、device 多。
- **Dimension check**：$\dfrac{[\text{J}]}{[\text{W}]}\cdot(\text{無因次})^2=\dfrac{[\text{J}]}{[\text{J/s}]}=[\text{s}]$，
  per-Hz 的功率比（$1/\Delta\omega^2$ 已吸進 $(\omega_0/\Delta\omega)^2$）→ $10\log_{10}$ 得 dBc/Hz ✓。
- **一行 Python 驗證**：

```python
import numpy as np
def L_ring_fom(kT, P, f0, df, eta=1.0, vdd_vchar=3.0):   # [P2] Eq.(23), prefactor 8/(3*eta)
    return 10*np.log10(8/(3*eta) * (kT/P) * vdd_vchar * (f0/df)**2)
vals = {N: L_ring_fom(4.0e-21, 1e-3, 5e9, 1e6) for N in (3, 5, 15)}
print({N: round(v,1) for N,v in vals.items()})    # -> {3: -91.0, 5: -91.0, 15: -91.0}
```

N-independence 在這裡是「Eq.(23) 裡根本沒有 $N$」的直接後果；toy 指數也對得上——
$\Gamma_{rms}^2\propto N^{-3}$（Eq.16）、$q_{max}\propto N^{-1}$（固定 $P$、$f_0$ 下由 Eq.(21)）、noise 源數 $\times N$，
故 $\Gamma_{rms}^2/q_{max}^2\cdot N\propto N^{-3+2+1}=N^0$，與 Eq.(23) 一致（推演見 [lab_17](/04_simulation_labs/lab_17_design_tradeoffs)）。

> **例 2（LC vs ring：同數量級條件下 LC 好多少？）**
> 用 [P1] Eq.(21) 算一個代表性 LC 數字，和上面 ring 的 $-91.0$ dBc/Hz 並排比較。取 canonical
> $\Gamma_{rms}=0.5$、$q_{max}=1$ pC、$S_i=\overline{i_n^2}/\Delta f=10^{-24}$ A²/Hz、$f_0=5$ GHz、$\Delta f=1$ MHz。

**逐步代入（帶單位）**，用 [P1] Eq.(21) $\mathcal{L}=10\log_{10}\!\big(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{4\Delta\omega^2}\big)$：

$$
\begin{aligned}
\Delta\omega&=2\pi\times10^6=6.283\times10^6\ \text{rad/s},\quad \Delta\omega^2=3.948\times10^{13},\\[4pt]
\text{括號}&=\frac{0.25}{10^{-24}}\cdot\frac{10^{-24}}{4\times3.948\times10^{13}}=\frac{0.25}{1.579\times10^{14}}=1.583\times10^{-15},\\[4pt]
\mathcal{L}_{LC}&=10\log_{10}(1.583\times10^{-15})=-148.0\ \text{dBc/Hz}.
\end{aligned}
$$

- **比較**：理想單源下 LC $-148$ vs ring $-91$ → LC 約**好 57 dB**。（兩數來自兩篇論文各自的自然參數化：
  LC 用 $q_{max},\Gamma_{rms},S_i$、ring 用 $P,\gamma,V_{DD}/V_{char}$，故這是「量級對照」而非同一組參數。
  真實差距常為 10～30 dB，因 ring 有多個 noise 源、cyclostationary、flicker。）這量化了「LC 用高 $Q$ 儲能買低 phase noise」。
- **Dimension check**：同 [P1] Eq.(21)（見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)），括號無因次 ✓。
- **一行 Python 驗證**：

```python
import numpy as np
def L_lc(Grms, qmax, Si, f0, df):                 # [P1] Eq.(21)
    dw = 2*np.pi*df
    return 10*np.log10(Grms**2/qmax**2 * Si/(4*dw**2))
print(round(L_lc(0.5, 1e-12, 1e-24, 5e9, 1e6), 1))   # -> -148.0
```

> 以上 [P2] 常數（前置係數 $8/(3\eta)$、$\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\cdot N^{-1.5}$、Eq.(23) FOM）皆已對照原始 PDF 核實；唯一穩固且設計可直接用的是
> **N-independence 這個定性結論**與 $N^0$ 的指數相消。完整 script：`simulations/lab_03_ring_toy_model.py`。

## 重點回顧

- LC：正弦波形、$\Gamma=-\sin$、高 $Q$ 儲能、大 $q_{max}$、少 device、低 phase noise、慢 jitter 累積。
- ring：方波、ISF 集中於 transition、無儲能、$N$ 個 noise 源、$\Gamma_{rms}\propto N^{-3/2}$、快 random-walk jitter。
- [P2] 三公式：$f_0=1/(2N\tau_D)$（Eq.15）、$\Gamma_{rms}\propto N^{-3/2}$（Eq.16，v7 已重核：根號只蓋常數）、FOM $\frac{8}{3\eta}\,\frac{V_{DD}}{V_{char}}\,\frac{kT}{P}(\omega_0/\Delta\omega)^2$（Eq.23，前置係數 $8/(3\eta)$，已核實）。
- **N-independence**：固定 $f_0$/功率下 ring phase noise ~與 $N$ 無關（各 $N$ 因子相消）；選 $N$ 看調諧/多相位/面積。
- **差動 ring 例外**：[P2] Eq.(34), p.796 明含 $N$——固定 $f_0$/功率下 $\mathcal{L}$ 隨 $10\log_{10}N$ 惡化（$q_{max}\propto1/N^2$ 是禍首）；$N=4\to12$ 差 $+4.77$ dB。差動設計用最少必要級數。
- ISF 看得見相位敏感度分佈與 scaling；看不見絕對 $Q$、強非線性、耦合、確切常數。

## 延伸閱讀

- ring lab：[lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
- LC lab：[lab_02_lc_oscillator_toy_model](/04_simulation_labs/lab_02_lc_oscillator_toy_model)
- LC 的「高 $Q$ 儲能」到底買到什麼（$Q$ 三寫法、$-R$ 補償、$4kT/R_p$）：[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)
- tuning/supply 抖動的 phase noise（LC-VCO 的另一條大門）：[varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)
- $\Gamma_{rms}$：[rms_isf](/03_isf_core_theory/rms_isf)；swing：[tank_swing](/06_design_insights/tank_swing)
- 對稱性：[symmetry](/06_design_insights/symmetry)；斜率：[waveform_slope](/06_design_insights/waveform_slope)
- jitter 與 SerDes：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
