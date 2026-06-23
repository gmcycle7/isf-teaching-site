---
title: Tank swing、q_max 與 phase noise
description: 為什麼更大的 signal swing 降低 phase sensitivity——phase noise 正比於 1/q_max²（[P1] Eq.(21)），以及 power / voltage headroom 的取捨。
---

# Tank swing、$q_{max}$ 與 phase noise

> **先備**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（[P1] Eq.(21) 招牌結果 $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$）、[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)（$q_{max}=CV_{max}$ 為何進到分母）、[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)（高 $Q$ 為何是「接近免費的 swing」、$R_p$ 從哪來）｜ **接下來**：[varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)、[lc_vs_ring](/06_design_insights/lc_vs_ring)

這頁回答 oscillator 設計裡「最先被問、最常被低估」的問題：**為什麼把 tank（LC 諧振槽）的
voltage swing（電壓擺幅）做大，phase noise 就會降？** 答案是 ISF 理論裡最乾淨的 scaling：
phase noise **反比於 $q_{max}^2$**，而 $q_{max}=C_{node}V_{max}$ 直接由 swing 決定。

> **物理直覺（先講結論）**：相位誤差 $=\dfrac{\Gamma}{q_{max}}\Delta q$ ——分母是 $q_{max}$。
> swing 越大，訊號攜帶的電荷 $q_{max}$ 越多，同一坨 noise 電荷 $\Delta q$ 相對它就越「微不足道」，
> 推得動的相位就越小。把訊號做大、把雜訊比下去——這是所有低 phase noise 設計的第一原則。
> 代價是：swing 受 supply / headroom（電壓餘裕）限制，做大 swing 往往要燒更多功率。

## 第 1 步：$q_{max}$ 是什麼、為什麼進到分母

$q_{max}$ 是節點上「訊號擺幅對應的最大電荷」：

$$
q_{max}=C_{node}\,V_{max}
$$

- **單位檢查**：$[\text{F}]\cdot[\text{V}]=[\text{C}]$ ✓。
- 它出現在 impulse→phase 的分母（[P1] Eq.(10)–(11), p.182）：$\Delta\phi=\dfrac{\Gamma}{q_{max}}\Delta q$。
- **意義**：$\Delta q/q_{max}$ 是「注入電荷相對訊號電荷的比例」。$q_{max}$ 越大 → 同樣 $\Delta q$
  造成的相對擾動越小 → 相位越穩。$\Gamma$（無因次形狀）本身**不隨 swing 改變**；swing 只動 $q_{max}$。

## 第 2 步：phase noise ∝ $1/q_{max}^2$ 的 scaling

白噪 1/f² phase noise 的招牌結果（[P1] Eq.(21), p.185）：

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)
$$

- 分母有 **$q_{max}^2$**。所以 $\mathcal{L}\propto1/q_{max}^2$。
- **scaling（claim C3）**：$q_{max}$ 加倍 → $\mathcal{L}$ 降 $10\log_{10}(2^2)=6.02$ dB。
  每把 swing（在 $C$ 固定下）加倍，phase noise **改善 6 dB**。

**逐步代數：「$q_{max}$ 加倍 → −6 dB」是怎麼從 Eq.(21) 一步步掉出來的。**
令 $q_{max}\to q_{max}'=2q_{max}$，其餘（$\Gamma_{rms}$、$\overline{i_n^2}/\Delta f$、$\Delta\omega$）全不變。
phase noise 是「dB = $10\log_{10}$(括號內功率比)」，所以只要看括號內**新舊比值**：

$$
\begin{aligned}
\frac{P_{new}}{P_{old}}
&=\frac{\dfrac{\Gamma_{rms}^2}{(2q_{max})^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\Delta\omega^2}}
       {\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\Delta\omega^2}}
\;=\;\frac{1/(2q_{max})^2}{1/q_{max}^2}
\;=\;\frac{q_{max}^2}{(2q_{max})^2}
\;=\;\frac{1}{4}, \\[6pt]
\Delta\mathcal{L}&=\mathcal{L}_{new}-\mathcal{L}_{old}
=10\log_{10}\!\left(\frac{P_{new}}{P_{old}}\right)
=10\log_{10}\!\left(\frac14\right)
=-10\log_{10}4 \\[4pt]
&=-20\log_{10}2=-20\times0.30103=-6.02\ \text{dB}.
\end{aligned}
$$

- **每一步用到什麼**：第 1 行把所有共同因子（$\Gamma_{rms}^2$、$\overline{i_n^2}/\Delta f$、$4\Delta\omega^2$）約掉，
  只剩 $q_{max}$ 的比；第 2→3 行用 log 恆等式 $\log_{10}4=\log_{10}2^2=2\log_{10}2$。
- **為什麼是「6 dB／octave」而非 3 dB**：因為 $\mathcal{L}\propto q_{max}^{-2}$ 是**平方**反比——功率比 $\tfrac14$
  對應 $-6$ dB（不是 $-3$ dB，$-3$ dB 是 $\tfrac12$）。電壓／電荷量翻倍 → 功率比 $4\times$ → $20\log_{10}2$。
- **dimension check**：比值 $P_{new}/P_{old}$ 無因次（同單位相除）→ $10\log_{10}$ 給 dB（無因次）✓。
- **dimension check（整個括號要無因次給 dBc/Hz）**：
  $\dfrac{(\text{無因次})^2}{[\text{C}]^2}\cdot\dfrac{[\text{A}^2/\text{Hz}]}{[\text{rad/s}]^2}
  =\dfrac{[\text{A}^2/\text{Hz}]}{[\text{C}^2][\text{s}^{-2}]}$。用 $[\text{A}]=[\text{C/s}]$：
  $=\dfrac{[\text{C}^2\text{s}^{-2}/\text{Hz}]}{[\text{C}^2\text{s}^{-2}]}=\dfrac{1}{[\text{Hz}]}$。
  $\overline{i_n^2}/\Delta f$ 本身已是 per-Hz，正是這個 per-Hz 讓絕對 $\mathcal{L}$ 成為 per-Hz（dBc/Hz）；
  而（如上一條）$P_{new}/P_{old}$ 這個比值本身無因次，取 $10\log_{10}$ 給 dB ✓。

同樣的 $1/q_{max}^2$ 也出現在 ring 的累積 jitter 比例常數（[P2] Eq.(11)–(12), p.793）：

$$
\kappa^2\propto\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}
$$

- 所以「加大 swing 降 phase noise」與「加大 swing 降 jitter」是**同一件事**——它們共用
  $\Gamma_{rms}^2/q_{max}^2$ 這個核心比值。（[P2] Eq.(12), p.793 已核實：$\kappa=\dfrac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\,\overline{i_n^2}/\Delta f}$。）

## 第 3 步：增大 $q_{max}$ 的兩條路——加 $V_{max}$ vs 加 $C$

$q_{max}=C\cdot V_{max}$，理論上加 $C$ 或加 $V_{max}$ 都能提 $q_{max}$。但兩條路代價完全不同：

| 路徑 | $q_{max}$ 變化 | 對 phase noise | 副作用 |
|---|---|---|---|
| 加大 $V_{max}$（swing） | $q_{max}\propto V_{max}$ | $\mathcal{L}\propto1/V_{max}^2$（最有效） | 受 supply / breakdown / headroom 限制；要更多 bias 電流維持 swing |
| 加大 $C$（tank 電容） | $q_{max}\propto C$ | 看似 $\propto1/C^2$，但有陷阱 ↓ | 為維持 $f_0$ 要降 $L$；要更大 $g_m$／電流維持 swing；$f_0=1/\sqrt{LC}$ 被綁住 |

- **加 swing 通常是首選**：直接、6 dB/octave，且不動 $f_0$。
- **加 $C$ 有陷阱**：在 LC 中 $f_0=1/(2\pi\sqrt{LC})$，加 $C$ 必須同比例降 $L$；維持同樣 swing
  電壓需要更大的 tank 電流（$Q$、$g_m$ 限制），實際改善常被「為了驅動更大 $C$ 而多花的功率/雜訊」吃掉。
  真正乾淨的槓桿是**在 power budget 內把 swing 推到 headroom 上限**。

## 第 4 步：power / voltage headroom 取捨

swing 不能無限大——它撞到 supply 與 device 的兩道牆：

1. **Voltage headroom（電壓餘裕）**：差動 LC 的 single-ended swing 上限約是 supply $V_{DD}$
   （current-limited regime）到 $\sim\dfrac{4}{\pi}\,I_{bias}R_p$（其中 $R_p$ 是 tank 並聯等效電阻）。
   推到 voltage-limited regime 後，再加電流也不會再加 swing——這時 phase noise 改善飽和。
2. **Power**：在 current-limited regime，swing $\approx\dfrac{4}{\pi}I_{bias}R_p$ 正比於 bias 電流。
   要 swing 加倍 → 電流加倍 → 功率加倍。

把這兩件事接起來看 **FOM（figure of merit，品質因子）的取捨**：

- phase noise $\mathcal{L}\propto1/q_{max}^2\propto1/V_{max}^2$（swing 越大越好），
- 但 $V_{max}\propto I_{bias}$（current-limited）→ $\mathcal{L}\propto1/I_{bias}^2$，而 $P\propto I_{bias}$，
- 所以 $\mathcal{L}\propto1/P^2$？——**不會**。因為 noise 電流 $\overline{i_n^2}$ 也隨 bias 電流上升
  （更多電流→更多 device noise），通常 $\overline{i_n^2}\propto I_{bias}$，於是淨效果回到
  **$\mathcal{L}\cdot P\approx$ 常數**（每多燒 1 dB 的功率，買到約 1 dB 的 phase noise）。
- 這就是為什麼業界用 **FOM $=\mathcal{L}-20\log_{10}(f_0/\Delta f)+10\log_{10}(P/1\text{mW})$**
  來公平比較不同功耗的振盪器：它把這條「phase noise × power ≈ 常數」的取捨歸一化掉。

> ⚠️ 上面的「current-limited / voltage-limited」分界與 $\dfrac{4}{\pi}I_{bias}R_p$ 是
> **標準 LC oscillator 設計知識（不在下載的 5 篇 PDF 內，以標準文獻補充，如 Hajimiri-Lee 教科書、
> Razavi RF Microelectronics）**。[P1] 本身給的是 $1/q_{max}^2$ 的 scaling，沒展開 swing-vs-power 的
> 電路層細節。確切的 swing 上限係數與 phase-noise factor 下限見 E. Hegazi, H. Sjöland, A. A. Abidi, *A Filtering Technique to Lower LC Oscillator Phase Noise*, IEEE JSSC **36**(12):1921–1930, 2001（已查證），及 Razavi《RF Microelectronics》。

## 數值例子（建立手感）

> 用 canonical 例 B 當基準，看 swing 翻倍的效果。

**基準**（例 B）：$f_0=5$ GHz、$\Delta f=1$ MHz、$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、$S_i=10^{-24}$ A²/Hz：

$$
\mathcal{L}=10\log_{10}\!\left(\frac{0.25}{(10^{-12})^2}\cdot\frac{10^{-24}}{4(2\pi\cdot10^6)^2}\right).
$$

先算 $\Delta\omega=2\pi\cdot10^6=6.283\times10^6$ rad/s，$\Delta\omega^2=3.948\times10^{13}$。
括號 $=\dfrac{0.25}{10^{-24}}\cdot\dfrac{10^{-24}}{4\cdot3.948\times10^{13}}=\dfrac{0.25}{1.579\times10^{14}}=1.583\times10^{-15}$，
$\mathcal{L}=10\log_{10}(1.583\times10^{-15})=-148.0$ dBc/Hz。

**swing 加倍**（$q_{max}=2$ pC，其餘不變）：$q_{max}^2$ 變 4 倍 → 括號變 1/4 →

$$
\mathcal{L}_{new}=-148.0-10\log_{10}(4)=-148.0-6.02=-154.0\ \text{dBc/Hz}.
$$

- **手感**：swing 加倍 → phase noise **改善 6.0 dB**，分毫不差等於 $20\log_{10}2$。
- **取捨提醒**：但若這 6 dB 是靠 bias 電流加倍換來（current-limited，且 $\overline{i_n^2}\propto I$），
  $S_i$ 也會上升 ~3 dB，淨改善約 3 dB——這正是「phase noise × power ≈ 常數」在起作用。
  真正的 free lunch 是「在不加電流的前提下提高 $V_{max}$」（例如更高 $Q$ 的 tank、更高 $R_p$）。

## 降低 phase noise / 提高 $q_{max}$ 的 design knobs（清單）

| Knob | 對哪個量 | 機制 | 代價／註記 |
|---|---|---|---|
| 加大 voltage swing $V_{max}$ | $q_{max}\uparrow$ | $\mathcal{L}\propto1/V_{max}^2$，6 dB/octave | 受 headroom / breakdown 限制 |
| 提高 tank $Q$（低損 $R_p$↑） | $V_{max}\uparrow$（同電流更大 swing） | 更高 $R_p$→同 $I_{bias}$ 給更大 swing，免費降 noise | 受製程 inductor $Q$、寄生限制 |
| differential（差動）topology | 有效 swing ×2 | 差動擺幅是單端兩倍 → $q_{max}\uparrow$ | 兩倍 device/面積/功耗 |
| 把 $bias$ 推到 current/voltage 邊界 | $V_{max}$ 最大化 | 拿滿 headroom | 過了 voltage-limited 點就飽和、只剩浪費電流 |
| 降 $\Gamma_{rms}$（另一個槓桿） | $\mathcal{L}\propto\Gamma_{rms}^2$ | 與 $q_{max}$ 同等重要 | 見 [device_noise_mapping](/06_design_insights/device_noise_mapping) |

> 注意：$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$ —— **$q_{max}$ 與 $\Gamma_{rms}$ 是兩個獨立槓桿**。
> 本頁談 $q_{max}$（swing）；$\Gamma_{rms}$（波形形狀、cyclostationary）見 [device_noise_mapping](/06_design_insights/device_noise_mapping)。

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 小擾動、ISF 不隨 swing 變 | $\mathcal{L}\propto1/q_{max}^2$ 乾淨成立 | swing 大到改變波形形狀/$\Gamma$ 時 scaling 偏離 |
| current-limited regime | swing $\propto I_{bias}$，能買 phase noise | voltage-limited 後加電流無效 |
| $\overline{i_n^2}$ 不隨 swing 變 | 6 dB/octave 全拿 | 若 noise 隨 bias 上升，淨改善打折 |

## Worked examples 數值例題

以下兩題用 [P1] Eq.(21) 逐步算「swing/$q_{max}$ 改變 → $\mathcal{L}$ 改變」，沿用 canonical 例 B：
$f_0=5$ GHz、$\Delta f=1$ MHz、$\Gamma_{rms}=0.5$、$S_i=\overline{i_n^2}/\Delta f=10^{-24}$ A²/Hz。

> **例 1（$q_{max}$ 加倍 → $\mathcal{L}$ 降 6 dB，用 Eq.(21) 逐步）**
> 基準 $q_{max}=1$ pC 的 $\mathcal{L}=-148.0$ dBc/Hz（例 B）。把 swing 加倍使 $q_{max}=2$ pC（$C$ 固定、
> $V_{max}$ 加倍），其餘不變。求新的 $\mathcal{L}$。

**逐步代入（帶單位）**，直接代 Eq.(21) 算絕對值（不靠近似），再對照 −6 dB：

$$
\begin{aligned}
\Delta\omega&=2\pi\Delta f=2\pi\times10^{6}=6.283\times10^{6}\ \text{rad/s},\quad \Delta\omega^2=3.948\times10^{13}\ \text{(rad/s)}^2, \\[4pt]
\text{括號}_{new}&=\frac{\Gamma_{rms}^2}{(q_{max}')^2}\cdot\frac{S_i}{4\Delta\omega^2}
=\frac{(0.5)^2}{(2\times10^{-12}\,\text{C})^2}\cdot\frac{10^{-24}\,\text{A}^2/\text{Hz}}{4\times3.948\times10^{13}} \\[4pt]
&=\frac{0.25}{4\times10^{-24}}\cdot\frac{10^{-24}}{1.579\times10^{14}}
=\frac{0.25}{4\times1.579\times10^{14}}=3.958\times10^{-16}, \\[4pt]
\mathcal{L}_{new}&=10\log_{10}(3.958\times10^{-16})=-154.0\ \text{dBc/Hz}.
\end{aligned}
$$

- **結果**：$\mathcal{L}_{new}=-154.0$ dBc/Hz，正好比基準 $-148.0$ 低 **6.0 dB**——與上面 $-20\log_{10}2$ 的代數結論一致。
- **Dimension check**：括號內 $\dfrac{\text{無因次}}{[\text{C}]^2}\cdot\dfrac{[\text{A}^2/\text{Hz}]}{[\text{rad/s}]^2}$，
  用 $[\text{A}]=[\text{C/s}]$ → $[\text{A}^2]=[\text{C}^2\text{s}^{-2}]$，分子 $[\text{C}^2\text{s}^{-2}/\text{Hz}]$、分母 $[\text{C}^2\text{s}^{-2}]$
  → 剩 $1/[\text{Hz}]$，再吸收 per-Hz → 無因次功率比，取 $10\log_{10}$ 得 dBc/Hz ✓。
- **一行 Python 驗證**：

```python
import numpy as np
def L_eq21(grms, qmax, Si, dw):
    return 10*np.log10(grms**2/qmax**2 * Si/(4*dw**2))
dw = 2*np.pi*1e6
L0 = L_eq21(0.5, 1e-12, 1e-24, dw)   # baseline
L1 = L_eq21(0.5, 2e-12, 1e-24, dw)   # qmax doubled
print(round(L0,1), round(L1,1), round(L1-L0,2))  # -> -148.0 -154.0 -6.02
```

> **例 2（同時動兩個槓桿：swing 加倍 + $\Gamma_{rms}$ 減半）**
> 從基準（$q_{max}=1$ pC、$\Gamma_{rms}=0.5$）出發，swing 加倍（$q_{max}=2$ pC）**且**波形改善使
> $\Gamma_{rms}=0.25$（減半）。求總改善 $\Delta\mathcal{L}$。

**逐步代入**，因為 $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$，兩個槓桿在 log 域**相加**：

$$
\begin{aligned}
\Delta\mathcal{L}&=10\log_{10}\!\left(\frac{(\Gamma_{rms}')^2/(q_{max}')^2}{\Gamma_{rms}^2/q_{max}^2}\right)
=\underbrace{10\log_{10}\!\left(\frac{(0.25)^2}{(0.5)^2}\right)}_{\Gamma_{rms}\,\text{減半}}
+\underbrace{10\log_{10}\!\left(\frac{(10^{-12})^2}{(2\times10^{-12})^2}\right)}_{q_{max}\,\text{加倍}} \\[4pt]
&=10\log_{10}(0.25)+10\log_{10}(0.25)=(-6.02)+(-6.02)=-12.04\ \text{dB}.
\end{aligned}
$$

- **結果**：總改善 **−12 dB**（每個槓桿各貢獻 −6 dB）。對照例 B 的 $-148.0$ → $-160.0$ dBc/Hz。
  這展示了 $\Gamma_{rms}$ 與 $q_{max}$ 是**兩個獨立、可疊加**的槓桿（[P1] Eq.(21) 的分子與分母）。
- **Dimension check**：兩個 ratio 都無因次 → dB 相加仍是 dB ✓。
- **一行 Python 驗證**：

```python
import numpy as np
print(round(L_eq21(0.25, 2e-12, 1e-24, 2*np.pi*1e6) - L_eq21(0.5, 1e-12, 1e-24, 2*np.pi*1e6), 2))
# -> -12.04 dB   (reuse L_eq21 from 例 1)
```

> 提醒（見第 4 步）：若這些改善是靠 bias 電流換來（current-limited，$\overline{i_n^2}\propto I_{bias}$），
> $S_i$ 會跟著上升、淨改善打折——這正是「phase noise × power ≈ 常數」。上兩題假設 $S_i$ 固定（理想上限）。

## 重點回顧

- $q_{max}=C\cdot V_{max}$；phase noise $\mathcal{L}\propto1/q_{max}^2$（[P1] Eq.(21)）。
- $q_{max}$ 加倍 → $\mathcal{L}$ 改善 **6.02 dB**（例：$-148\to-154$ dBc/Hz）。
- 加 swing 比加 $C$ 乾淨（加 $C$ 會綁 $f_0$、要更多電流）；提高 tank $Q$ 是接近免費的 swing。
- 取捨：current-limited 下 swing∝電流、device noise 也∝電流 → **phase noise × power ≈ 常數**；用 FOM 公平比較。
- $q_{max}$ 與 $\Gamma_{rms}$ 是兩個獨立槓桿（[P1] Eq.(21) 的分子分母）。

## 延伸閱讀

- 招牌公式推導：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- impulse→phase 的 $q_{max}$ 角色：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)
- tank $Q$ 怎麼來、為何高 $Q$ 等於免費 swing、$R_p$ 與 $4kT/R_p$ 熱雜訊：[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)
- tuning line／supply 抖動如何 FM 載波（另一條 phase noise 大門）：[varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)
- 另一個槓桿 $\Gamma_{rms}$：[device_noise_mapping](/06_design_insights/device_noise_mapping)
- 斜率／swing 的關聯：[waveform_slope](/06_design_insights/waveform_slope)
- LC vs ring 的 swing 差異：[lc_vs_ring](/06_design_insights/lc_vs_ring)
