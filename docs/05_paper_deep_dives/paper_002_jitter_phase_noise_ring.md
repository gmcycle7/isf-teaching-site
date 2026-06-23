---
title: "[P2] Jitter and Phase Noise in Ring Oscillators"
description: Hajimiri–Limotyrakis–Lee 1999 精讀：accumulated jitter、Γrms∝N^(-3/4)、N-independence（已核實）、symmetry 與 Fig.17。
---

# Jitter and Phase Noise in Ring Oscillators

> **先備知識（建議先讀）**：先把 [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)（ISF、$\Gamma_{rms}^2/q_{max}^2$、symmetry 法則）讀懂——本頁所有結論都是 [P1] 的 ISF 套到 ring。jitter 的時域／頻域語言見 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)。

[P2] 把 [P1] 的 ISF 框架**套到 ring oscillator（環形振盪器）**。它回答三個非常實際的問題：
（1）自由振盪的 ring 的 long-term jitter 怎麼隨時間長大？（2）級數 $N$ 對 phase noise 有什麼
影響？（3）為什麼波形對稱性能壓低 close-in noise？答案分別是 $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$、
$\Gamma_{rms}\propto N^{-3/4}$（與「固定功率與頻率下幾乎與 $N$ 無關」），以及 Fig. 17 的對稱性實驗。

## Citation

> **[P2]** A. Hajimiri, S. Limotyrakis, and T. H. Lee, *"Jitter and Phase Noise in Ring
> Oscillators,"* IEEE J. Solid-State Circuits, vol. 34, no. 6, pp. 790–804, Jun. 1999.
> （檔案 `jitter_ring.pdf`，paper_002）

## One-sentence contribution

把 [P1] 的 ISF 用到 ring oscillator，得到 jitter 與 phase noise 的封閉式、
$\Gamma_{rms}\propto N^{-3/4}$ 的 scaling、以及「固定 $f_0$ 與功率時 single-ended ring 的
phase noise／jitter 幾乎與級數 $N$ 無關」這個反直覺結論（claim C7, C8）。

## Why this paper matters

LC 振盪器要電感，面積大、不好整合；**ring oscillator 全用反相器、面積小、好整合、調頻範圍寬**，
是 PLL／CDR 裡最常見的 VCO。但 ring 的 phase noise 通常比 LC 差很多——[P2] 用 ISF 解釋
**為什麼**，並給出可操作的設計法則：

- 它把 ring 的 jitter 連到**和 phase noise 同一個 $\Gamma_{rms}^2/q_{max}^2$ 比例**（claim C6），
  讓「時域 jitter」與「頻域 phase noise」在 ISF 框架下統一。
- 它澄清一個常被誤解的問題：「ring 級數 $N$ 加多會不會比較好？」答案在固定功率與頻率的約束下
  是「**幾乎沒差**」（claim C7）——多了級數、$\Gamma_{rms}$ 變小，但每級擺幅也變小、device 變多，
  彼此抵消。
- 它用實測（Fig. 17）證實 [P1] 的 symmetry 法則：把控制電壓調到讓上升／下降對稱的點，phase
  noise 出現**極小值**（claim C4）。

## Main assumptions

照 paper_metadata（paper_002.assumptions）：

1. 與 [P1] 相同的 LTV／ISF 小擾動假設。
2. 每級 device noise 為白噪（加上用 symmetry 處理的 1/f 成分）。
3. 各級相同；延遲與 noise 在每次 transition 獨立相加。

> **物理直覺**：ring 的能量幾乎全集中在 transition（邊緣翻轉）那一瞬間注入，所以它的 ISF
> 不像 LC 的平滑 $-\sin$，而是**集中在 transition 的尖峰**（[P2] Fig. 5）。哪裡敏感、哪裡踢
> 一下最傷相位，就在那些尖峰上。級數越多、單一 transition 佔整個週期的比例越小，rms ISF 越小。

## Key equations

### Eq.(8)：accumulated jitter（隨機漫步指紋）

**Original formula**（[P2] Eq.(8), p.792；κ 由 Eq.(12), p.793）：

$$
\sigma_{\Delta t}=\kappa\sqrt{\Delta t}
$$

**Meaning**：自由振盪器相隔 $\Delta t$ 的兩個邊緣，其時間誤差的標準差**正比於
$\sqrt{\Delta t}$**——這是「沒有絕對時間參考」的振盪器的**隨機漫步（random walk）指紋**
（claim C6）。$\kappa$ 是每顆 device 的比例常數，單位 $\sqrt{\text{s}}$。

**Step-by-step derivation**：每次 transition 注入一筆獨立、零均值、變異數 $\sigma_{step}^2$
的時間擾動。經過 $\Delta t$ 共約 $M=\Delta t/T$ 次 transition，獨立量相加變異數相加：

$$
\begin{aligned}
\sigma_{\Delta t}^2 &= M\,\sigma_{step}^2 = \frac{\Delta t}{T}\,\sigma_{step}^2 \\
\Rightarrow\quad \sigma_{\Delta t} &= \underbrace{\frac{\sigma_{step}}{\sqrt{T}}}_{\equiv\,\kappa}\sqrt{\Delta t}=\kappa\sqrt{\Delta t}.
\end{aligned}
$$

**Dimension check**：$\kappa$ 是 $\sqrt{\text{s}}$，$\sqrt{\Delta t}$ 是 $\sqrt{\text{s}}$，
相乘得 $\text{s}$ ✓。對照 [P1] 的頻域：$\sigma_{\Delta t}\propto\sqrt{\Delta t}$ 對應頻域的
1/f² phase noise（兩者是同一件事的時域／頻域兩面）。

**Numerical example**：toy ring 設 per-edge $\sigma_{step}=50$ fs（見
`ring_oscillator_timing_noise_accumulation.png` 參數）。隔 $\Delta t=1$ µs（$f_0=5$ GHz
下約 5000 個週期）的累積 jitter：先求 $\kappa$。若 $T=200$ ps，
$\kappa=50\text{fs}/\sqrt{200\text{ps}}=50\times10^{-15}/\sqrt{2\times10^{-10}}=3.54\times10^{-9}\ \sqrt{\text{s}}$，
故 $\sigma_{\Delta t}=3.54\times10^{-9}\times\sqrt{10^{-6}}=3.54\ \text{ps}$。手感：隔越久、偏越多，但只以 $\sqrt{\Delta t}$ 慢慢長。

**Python verification**：

```python
import numpy as np
from simulations.common.oscillator_models import accumulated_jitter_curve

# toy 隨機漫步：每個 edge 加一筆 50 fs 的獨立 timing 擾動
lags, sigma = accumulated_jitter_curve(f0=5e9, sigma_edge=50e-15, max_lag_periods=500, n_trials=2000)
# 期望 sigma(lag) ~ sigma_edge * sqrt(lag) -> log-log 斜率 0.5
slope = np.polyfit(np.log(lags[1:]), np.log(sigma[1:]), 1)[0]
print(round(slope, 2))  # -> 0.50
```

完整 toy 推導在 [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
（**pedagogical toy model，非 transistor-level**）。

### Eq.(11)–(12)：jitter 常數 κ 與 ISF 的關係（已核實 ✓）

**Original formula**（[P2] Eq.(11)–(12), p.793，比例關係）：

$$
\kappa^2\;\propto\;\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}
$$

**Meaning**：jitter 比例常數 $\kappa$ 由**和 phase noise 一模一樣的 $\Gamma_{rms}^2/q_{max}^2$
比例**決定（claim C6）。這把時域 jitter 與頻域 phase noise 綁在同一個 ISF 量上：壓低 phase
noise 的旋鈕同時壓低 jitter。

> **已核實**：[P2] Eq.(12), p.793 給 $\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$（對照原始 PDF 渲染逐字確認）；
> 與 phase noise 共用同一個 $\Gamma_{rms}^2/q_{max}^2$ 比例（claim C6）。

### Eq.(14)：ring 頻率與級數

**Original formula**（[P2] Eq.(14), p.794）：

$$
f_0=\frac{1}{2N\tau_D}
$$

**Meaning**：$N$ 級、每級延遲 $\tau_D$ 的 ring，振盪頻率為此式。**因子 2** 來自訊號每個週期
要繞 ring **兩圈**（一圈反相、再一圈才回到同相）才完成一個完整週期。

**Dimension check**：$1/(N\cdot\text{s})=\text{Hz}$ ✓（$N$ 無因次）。

**Numerical example**：要做 $f_0=5$ GHz 的 5 級 ring，每級延遲
$\tau_D=1/(2\times5\times5\times10^9)=2\times10^{-11}\ \text{s}=20$ ps。級數加倍到 $N=10$
又要維持 5 GHz，每級延遲就得砍半到 10 ps——這正是「固定頻率時 $N$↑ 必須讓每級更快、擺幅更
小」的由來，連到下面的 N-independence。

### Eq.(16)：rms ISF 隨級數的 scaling（已對照原始 PDF 核實 ✓）

**Original formula**（[P2] Eq.(16), p.794，已用高解析度渲染逐字確認）：

$$
\Gamma_{rms}=\sqrt{\frac{2\pi^2}{3\eta^3}\cdot\frac{1}{N^{1.5}}}
$$

其中 $\eta$ 是頻率比例常數（Eq.(14)–(15)：$\hat t_D=\eta/f_{max}$、$2\pi=2N\eta/f_{max}$）。

**Meaning**：把根號內的 $1/N^{1.5}$ 開根號後得 **$\Gamma_{rms}\propto N^{-3/4}$**（即 $\Gamma_{rms}^2\propto N^{-3/2}$）。
直覺：級數越多，每個 transition 在 $2\pi$ 週期裡佔的「敏感時間窗」越窄、尖峰越矮，rms 自然變小。

> **Formula-vs-prose 註記（重要，已核實）**：[P2] p.794 的**印刷公式**根號同時涵蓋
> $2\pi^2/(3\eta^3)$ 與 $1/N^{1.5}$ 兩項（已逐字確認），所以嚴格依公式 $\Gamma_{rms}\propto N^{-3/4}$。
> 但同頁**文字**寫「the $1/N^{1.5}$ dependence of $\Gamma_{rms}$」，許多二手文獻也引用為
> $\Gamma_{rms}\propto N^{-3/2}$——那個 $N^{-3/2}$ 其實是**根號內項（即 $\Gamma_{rms}^2$）**的指數。
> 這是論文本身「公式 vs 文字」的小不一致；下方的 N-independence 結論不依賴於怎麼解讀此指數。

### Eq.(23)：ring 白噪 phase noise FOM 與 N-independence（前置係數已更正為 8/(3η) 並核實）

**Original formula**（[P2] Eq.(23), p.796；$V_T=0$ 的下限為 Eq.(25)）：

$$
\mathcal{L}\{\Delta f\}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{V_{char}}\cdot\left(\frac{f_0}{\Delta f}\right)^2
\qquad\Big(\min_{V_T=0}:\ \frac{16\gamma}{3\eta}\cdot\frac{kT}{P}\cdot\frac{f_0^2}{\Delta f^2}\Big)
$$

其中 $\gamma$ 是 MOSFET 通道熱雜訊係數（長通道 $2/3$，短通道更大）、$V_{char}$ 是元件的
**characteristic voltage**（長通道 $\approx\Delta V/\gamma$），$P$ 是功率耗散（Eq.(21)：$P=2\eta N V_{DD}q_{max}f_0$），
每級雜訊由 Eq.(17),(18) $\overline{i_n^2}/\Delta f=4kT\gamma\mu C_{ox}(W/L)\Delta V$ 給出。

**Meaning**：ring 白噪 phase noise 收成一個 figure of merit——只看 $kT/P$、電壓比 $V_{DD}/V_{char}$
與 $(f_0/\Delta f)^2$。**關鍵結論（claim C7）：Eq.(23) 裡完全沒有 $N$——固定 $f_0$ 與功率 $P$ 時，
single-ended ring 的 phase noise 與級數 $N$ 無關。**

**為何與 $N$ 無關**：微觀上，$N$↑ 會降 $\Gamma_{rms}$（Eq.16）但同時降每級擺幅 $q_{max}$、又增加噪聲級數；
[P2] 證明這些效應在固定 $P$、$f_0$ 下剛好抵消，最後 Eq.(23) 不含 $N$。所以「ring 要不要多加級數」
不是靠 phase noise 決定，而看相位裕度、調頻範圍、面積、quadrature 需求等其他考量。

> **校訂註記（v3）**：[P2] Eq.(23) 的前置係數是 $8/(3\eta)$（$\eta$ 為級延遲比例常數 Eq.14，$\approx1$）；
> $\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入。（v2 曾誤改為 $8/(3\gamma)$ 並誤標「逐字核實」，v3 已對照原始 PDF p.796 更正。）
> $V_T=0$ 的下限亦由此修為 $16\gamma/(3\eta)$。$\gamma$（噪聲係數）與 $\eta$（頻率比例常數，Eq.14）是不同的量，勿混淆。

## Key figures

| 論文圖 | 頁 | 內容 | 本站對應 | 註 |
|---|---|---|---|---|
| Fig. 5 | 793 | 同頻、不同級數 $N$（3/5/15）的 ISF 疊圖 | scaling 直覺（$\Gamma_{rms}\propto N^{-3/4}$） | ✓ |
| Fig. 6 | 793 | single-ended ring 單級的近似波形與 ISF（能量集中在 transition） | toy 三角 ISF（lab_03） | ✓ |
| Fig. 8 | 794 | 不同級數 ring 的 rms ISF vs $N$ | `lc_vs_ring_isf_comparison.png` 的 scaling 論證 | — |
| **Fig. 17** | 802 | phase noise vs symmetry（控制）電壓，在對稱點有**極小值** | symmetry 設計法則的直接實驗佐證 | ✓ |

**Fig. 17 是 symmetry 法則的鐵證**：把控制電壓掃過，調到 PMOS 上拉電流 = NMOS 下拉電流、
波形上下對稱的那一點，$c_0$ 被壓到最小、1/f³ 上轉被抑制，phase noise 出現一個**碗底**。這直接
驗證 [P1] Eq.(24)（claim C4）。

本站用 toy model 對照 LC（$-\sin$）與 ring（三角 ISF、峰隨 $N$ 變矮），**非 transistor-level**：

![LC 與 ring 的 ISF 對照（toy）](/figures/lc_vs_ring_isf_comparison.png)
![ring 累積 jitter 隨時間以 √Δt 長大（toy）](/figures/ring_oscillator_timing_noise_accumulation.png)

## Design insights

- **jitter 與 phase noise 同源**：壓低 $\Gamma_{rms}^2/q_{max}^2$ 同時降低兩者；別把 long-term
  jitter 與 close-in phase noise 當兩件事處理。
- **加級數不是 phase noise 的解藥**：固定 $f_0$、$P$ 下 phase noise 近似與 $N$ 無關（結論
  已核實）；加級數的真正理由是 quadrature／多相位輸出、調頻範圍、相位裕度。
- **對稱性是 close-in noise 的主旋鈕**：調 rise/fall 對稱（如 Fig. 17 的控制電壓）壓 $c_0$、
  推遠 1/f³ corner。差動 ring（differential）的對稱性通常比 single-ended 好。
- **transition 越陡越好**：能量集中在 transition，斜率越大、$q_{max}$ 越大、$\Gamma_{rms}$
  相對越小。

設計面整理見 [lc_vs_ring](/06_design_insights/lc_vs_ring) 與 [symmetry](/06_design_insights/symmetry)；
SerDes 觀點見 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

## Limitations

照 paper_metadata（paper_002.limitations）：

- toy／一階：短通道效應與細部 device noise 是近似的。
- **N-independence 結論**只在固定功率、固定頻率與特定 noise 模型下成立（[P2] Sec.V, Eq.(23)/(25), p.796，已核實，claim C7）。
- substrate／supply noise 是分開、定性處理的。

## Relationship to other papers

- **[P1]** 是地基：本頁的 jitter $\kappa$、$\Gamma_{rms}$、symmetry 全用 [P1] 的 ISF 與
  Eq.(21)/(24)。
- **[P3]/[P4]** 也用 ring 當載具（[P4] 的 ILFD/prescaler 就是 inverter-chain ring），把 ISF
  從 phase noise 延伸到 injection。
- **[P5]** 與本頁無關；但 latch-based／差動 ring 的起振也靠 cross-coupled 正回授（claim C12 的
  邊角橋樑）。

## 延伸閱讀 / 對應教學頁

| 本頁的哪一塊 | 對應教學頁 | 那頁多給你什麼 |
|---|---|---|
| LC（$-\sin$）vs ring（集中於 transition）的 ISF 對照、N-scaling 論證 | [lc_vs_ring](/06_design_insights/lc_vs_ring) | 兩種拓樸的 $\Gamma_{rms}$、$q_{max}$、phase noise 取捨整理成設計表 |
| Eq.(8) accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ 的隨機漫步 | [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model) | 可跑的 toy model：每 edge 加獨立擾動，log-log 斜率驗證 $\sqrt{\Delta t}$（**pedagogical toy，非 transistor-level**） |
| Fig. 17 對稱點的 phase noise 碗底、$c_0$ 與 1/f³ corner | [symmetry](/06_design_insights/symmetry) | rise/fall 對稱如何壓 $c_0$、differential vs single-ended、設計旋鈕 |

> **怎麼讀**：本頁是「論文怎麼把 [P1] 套到 ring」的故事；想動手看 jitter 怎麼以 $\sqrt{\Delta t}$ 長大，回 lab_03；想把結論變成拓樸選型，回 lc_vs_ring 與 symmetry。SerDes 觀點另見 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

## What to remember

- **accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$**：自由振盪器的隨機漫步指紋（[P2] Eq.(8), p.792）。
- $\kappa$ 由**和 phase noise 同一個 $\Gamma_{rms}^2/q_{max}^2$** 決定（[P2] Eq.16/23，已核實）。
- **$\Gamma_{rms}\propto N^{-3/4}$**（[P2] Eq.(16), p.794，已核實）；但固定 $f_0$、$P$ 下 phase noise
  **幾乎與 $N$ 無關**（[P2] Eq.(23) 無 $N$，claim C7，已核實）。
- **Fig. 17**：對稱點 phase noise 有碗底——symmetry 法則的鐵證（claim C4）。
- ring 比 LC 好整合，但 phase noise 通常較差；本頁告訴你旋鈕在哪。
