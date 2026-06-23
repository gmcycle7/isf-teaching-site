---
title: Flicker noise 上轉成 1/f³ phase noise
description: 為何 device 1/f 雜訊被 ISF 的 DC 項 c₀ 上轉成 close-in 1/f³；推導 [P1] Eq.(22),(23),(24)，並說明 1/f³ corner ≠ device 1/f corner、波形對稱性為何關鍵。
---

# Flicker noise 上轉成 1/f³ phase noise

> **前置閱讀**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（白噪 → $1/f^2$ 的同一機制）、[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（DC 項 $c_0$ 的角色）、[rms_isf](/03_isf_core_theory/rms_isf)（$c_0$ 與 $\Gamma_{rms}$ 比值定 corner）。
>
> **動手驗證**：本頁「對稱 vs 非對稱波形決定 close-in $1/f^3$」的模擬見 [lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion)。

上一頁 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 解釋了白噪怎麼變
$1/f^2$。但你看任何真實振盪器的 phase noise 圖，**最靠近載波**那一段通常更陡——斜率
$-30$ dB/decade，也就是 $1/f^3$。這段陡裙邊是哪來的？答案是 **device flicker noise（閃爍雜訊、
$1/f$ 雜訊，電晶體在低頻特別大的那種雜訊）被振盪器「上轉」（upconvert）到載波附近**。

這頁回答三件事：(1) flicker noise 是什麼、(2) 為什麼**只有 ISF 的 DC 項 $c_0$** 能把它上轉、
(3) 為什麼 $1/f^3$ corner **不等於** device 的 $1/f$ corner，以及波形對稱性如何幫上忙。

> **物理直覺（先講結論）**：低頻 flicker 雜訊本身在 baseband（接近 DC）。要讓它出現在
> **載波附近**，必須有某個機制把它「搬」上去 $\omega_0$。ISF 是個週期函數，它的傅立葉級數裡
> **唯一的 DC 成分就是 $c_0/2$**。只有這個 DC 項會跟「就在 DC 附近的 flicker」相乘並被相位積分器
> 累積成 close-in 相位抖動。換句話說：**$c_0$ 是 flicker 通往載波的唯一閘門。** 把 $c_0$ 壓到 0
> （靠波形對稱），這扇門就關上了，$1/f^3$ 裙邊大幅下降。

## 第 1 步：flicker noise 是什麼，model 怎麼寫

flicker（$1/f$）noise 是電晶體的本質低頻雜訊，PSD 隨頻率往低處**上升**（$\propto 1/f$），
通常歸因於通道-氧化層介面的載子捕捉/釋放。在 device 的 **$1/f$ corner** $\omega_{1/f}$ 以下，
flicker 超過白噪；以上則白噪主導。[P1] 用一個簡潔模型描述（[P1] Eq.(22), p.185）：

$$
\overline{i_{n,1/f}^2}=\overline{i_n^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}\qquad(\Delta\omega<\omega_{1/f})
$$

- **怎麼讀**：$\overline{i_n^2}$ 是白噪平台（per-Hz）；乘上 $\omega_{1/f}/\Delta\omega$ 後，
  在 $\Delta\omega<\omega_{1/f}$ 時放大、且隨 $1/\Delta\omega$ 上升——這就是 $1/f$ 形狀。
  在 $\Delta\omega=\omega_{1/f}$ 處兩者相等（corner 的定義）。
- **單位檢查**：$\omega_{1/f}/\Delta\omega$ 無因次（rad/s 除以 rad/s）；
  乘上 $\overline{i_n^2}$（$\text{A}^2/\text{Hz}$）仍是 $\text{A}^2/\text{Hz}$ ✓。
- **注意符號**：$\omega_{1/f}$ 是 **device** 的 $1/f$ corner（rad/s），來自電晶體製程，
  跟稍後的 phase-noise $1/f^3$ corner 是**兩回事**（見第 4 步，notation 頁也特別警告過）。

## 第 2 步：為何低頻雜訊需要被「上轉」才看得見

回到 [P1] Eq.(13), p.183 的分諧波相位響應：

$$
\phi(t)=\frac{1}{q_{max}}\!\left[\frac{c_0}{2}\!\int_{-\infty}^{t}\!i_n\,d\tau+\sum_{n=1}^{\infty}c_n\!\int_{-\infty}^{t}\!i_n\cos(n\omega_0\tau+\theta_n)\,d\tau\right].
$$

flicker 的能量集中在**低頻（接近 DC）**。看求和裡的每一項：

- $n\ge1$ 的項都帶 $\cos(n\omega_0\tau+\theta_n)$——它把「就在 $n\omega_0$ 附近」的 noise 下變頻到
  baseband。但 flicker 在 $n\omega_0$（$\ge\omega_0$，很高）幾乎**沒有能量**，所以這些項抓不到 flicker。
- **唯一的 $n=0$（DC）項** $\dfrac{c_0}{2}\int i_n\,d\tau$ **沒有** $\cos$ 乘子——它直接積分
  baseband 的 noise。flicker 的能量正好都在 baseband，所以**只有這一項**會把 flicker 累積成相位。

- **用到的數學**：頻率轉換（mixing）。$\cos(n\omega_0 t)\times$noise 把 noise 搬到 $\pm n\omega_0$；
  只有 DC 乘子（$=1$）讓 baseband noise 留在 baseband 被積分。
- **物理意義（claim C4）**：**$c_0$（ISF 的 DC 傅立葉係數）是 flicker→close-in 的唯一通道。**
  $c_0=0$ 則 flicker 根本上不來，$1/f^3$ 裙邊消失。

## 第 3 步：推導 1/f³ phase noise（Eq.(22)→(23) 的逐步代數）

這一步要把三件事「乘」起來：(i) flicker 經 $c_0$ 注入、(ii) 與 $1/f^2$ 機制（積分器）相乘、
(iii) 結果就是 $1/f^3$。我們不跳步，一條一條算。

**第 3.1 步：白噪求和式只保留 DC 項。** 白噪結果（規範第 3 節公式 10、[P1] Eq.(19), p.185）是

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{(\overline{i_n^2}/\Delta f)\,\sum_{n=0}^{\infty}c_n^2}{8\,q_{max}^2\,\Delta\omega^2}\right).
$$

flicker 的能量只在 baseband，由第 2 步知**只有 $n=0$（DC）項**抓得到它（其餘 $n\ge1$ 帶 $\cos(n\omega_0\tau)$，
把 noise 移到 $n\omega_0$，那裡 flicker 沒能量）。所以對 flicker 而言，求和 $\sum_{n=0}^{\infty}c_n^2$
**塌縮成單一項** $c_0^2$：

$$
\sum_{n=0}^{\infty}c_n^2\ \xrightarrow{\ \text{flicker 只剩 DC}\ }\ c_0^2.
$$

- **這個 $c_0^2$ 與分母 $8$ 的搭配怎麼來**：Eq.(19) 的分母是 $8q_{max}^2\Delta\omega^2$，分子帶 $\sum c_n^2$。
  ISF 傅立葉級數（[P1] Eq.(12)）的 DC **項**寫成 $\tfrac{c_0}{2}$，但 Parseval（[P1] Eq.(20)）裡
  DC 的功率係數記為 $c_0^2$（與其他 $c_n^2$ 同一套記法），所以直接代 $c_0^2$、分母維持 $8$。
  代入得「只有 DC、仍是白噪」的中間式：

$$
\mathcal{L}\{\Delta\omega\}\Big|_{1/f^2,\,\text{DC only}}=10\log_{10}\!\left(\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\right).
$$

**第 3.2 步：把白噪平台換成 flicker（乘 Eq.(22) 的放大因子）。** 上式分子的 $\overline{i_n^2}/\Delta f$
還是**白噪**平台。device flicker（[P1] Eq.(22), p.185）說在 $\Delta\omega<\omega_{1/f}$ 時，
電流 noise 被放大 $\omega_{1/f}/\Delta\omega$ 倍：

$$
\overline{i_{n,1/f}^2}=\overline{i_n^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}.
$$

把分子的 $\overline{i_n^2}/\Delta f$ 換成 $\overline{i_{n,1/f}^2}/\Delta f=(\overline{i_n^2}/\Delta f)\cdot(\omega_{1/f}/\Delta\omega)$，
就是「flicker 機制 × $1/f^2$ 機制」的相乘：

$$
\frac{c_0^2}{q_{max}^2}\cdot\underbrace{\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}}_{1/f^2\ \text{機制（積分器）}}\;\times\;\underbrace{\frac{\omega_{1/f}}{\Delta\omega}}_{\text{flicker 機制}}.
$$

**第 3.3 步：合併，得 [P1] Eq.(23)。** 兩個括號相乘、套回 $10\log_{10}$，就是
**flicker 上轉的 $1/f^3$ phase noise**（[P1] Eq.(23), p.185）：

$$
\boxed{\ \mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}\right)\ }
$$

- **看出 $1/f^3$ 了嗎**：分母有 $\Delta\omega^2$（積分器，$1/f^2$）再乘一個 $\Delta\omega$（flicker 的 $1/\Delta\omega$），
  合起來 $\Delta\omega^3$。每升一 decade 掉 $1000$ 倍 $\Rightarrow 30$ dB $\Rightarrow$ 斜率 $-30$ dB/decade ✓。
- **關鍵對比**：白噪結果裡是 $\Gamma_{rms}^2$（含**全部**諧波，$=\tfrac12\sum c_n^2$）；flicker 結果裡是
  $c_0^2$（**只有 DC**）。這就是「對稱性只救得了 flicker、救不了白噪」的數學根源——稍後第 4 步把這兩個
  分子相除，就直接得到 corner。
- **單位檢查**：相對白噪式多乘無因次的 $\omega_{1/f}/\Delta\omega$（rad/s ÷ rad/s），因次不變、仍是 per-Hz ✓。

## 第 4 步：1/f³ corner（Eq.(24)）——它不是 device 的 1/f corner

phase noise 譜上，$1/f^3$ 段與 $1/f^2$ 段交會的那個 offset 叫 **$1/f^3$ corner** $\Delta\omega_{1/f^3}$。
把 $1/f^3$ 式（Eq.(23)，含 $c_0^2$）與 $1/f^2$ 式（Eq.(21)，含 $\Gamma_{rms}^2$）令相等，解出交點
（[P1] Eq.(24), p.185）：

$$
\boxed{\ \Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2\ }
$$

**逐步代數（解交點，不跳步）**：corner 的定義是「$1/f^3$ 段 = $1/f^2$ 段」的那個 $\Delta\omega$。
把 $\log_{10}$ 內的兩個括號令相等（對數相等 ⇔ 引數相等）：

$$
\underbrace{\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}}_{\text{Eq.(23)：}1/f^3}
=\underbrace{\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}}_{\text{Eq.(21)：}1/f^2}.
$$

- **第 (a) 步：約掉兩邊共同因子。** 兩邊都有 $\dfrac{1}{q_{max}^2}$、$\dfrac{\overline{i_n^2}/\Delta f}{\Delta\omega^2}$，
  同除掉：

$$
\frac{c_0^2}{8}\cdot\frac{\omega_{1/f}}{\Delta\omega}=\frac{\Gamma_{rms}^2}{4}.
$$

- **第 (b) 步：解 $\Delta\omega$。** 兩邊乘 $\Delta\omega$、再除 $\Gamma_{rms}^2/4$：

$$
\frac{c_0^2\,\omega_{1/f}}{8}=\frac{\Gamma_{rms}^2}{4}\,\Delta\omega
\;\Longrightarrow\;
\Delta\omega=\frac{c_0^2\,\omega_{1/f}}{8}\cdot\frac{4}{\Gamma_{rms}^2}=\omega_{1/f}\cdot\frac{4c_0^2}{8\,\Gamma_{rms}^2}=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}.
$$

  $4/8=1/2$，正好得到 boxed 式的 $\dfrac{c_0^2}{2\Gamma_{rms}^2}$ ✓。注意這裡 factor 是 $\tfrac12$（不是
  $\tfrac14$），來源就是 Eq.(23) 分母的 $8$ 與 Eq.(21) 分母的 $4$ 之比。
- **這頁最重要的觀念（claim C5）**：$\Delta\omega_{1/f^3}\ne\omega_{1/f}$。
  $1/f^3$ corner 等於 device 的 $1/f$ corner **再乘上一個比例 $c_0^2/(2\Gamma_{rms}^2)$**。
  因為對稱波形 $c_0\ll\Gamma_{rms}$，這個比例**遠小於 1**，所以 **$1/f^3$ corner 被推到遠低於
  device 的 $1/f$ corner**。這推翻了早期經驗模型「$1/f^3$ corner $=$ device $1/f$ corner」的迷思
  —— [P1] 摘要與引言特別強調「contrary to widely held beliefs，$1/f^3$ corner 比 device $1/f$ corner
  小，差一個由波形對稱性決定的因子」。
- **$\approx\omega_{1/f}(c_0/c_1)^2$ 的由來**：當 ISF 以基波為主時 $\Gamma_{rms}^2\approx c_1^2/2$
  （Parseval 只剩 $n=1$ 項），代入即得右式。它讓你直接從「DC 係數 vs 基波係數」估 corner。
- **單位檢查**：$\omega_{1/f}$（rad/s）乘無因次比例 → rad/s ✓，是個角頻率。

## 第 5 步：為什麼波形對稱性決定 $c_0$

$c_0$ 是 ISF 的 DC 傅立葉係數，ISF 的 DC **值**是 $c_0/2$（notation 頁的符號陷阱）。
DC 值就是 ISF 在一個週期上的**平均**。[P1] 在設計章節（p.187–188，Fig. 16）指出：

> ISF 的 DC 值由波形的**對稱性**決定，特別是**上升與下降的對稱**（rise/fall symmetry）。
> 若上升時間與下降時間明顯不同，ISF 會有**很大的 DC 值**（大 $c_0$）。

直覺：ISF 在「敏感區」（波形 transition 附近）有正負起伏。若上升段與下降段**鏡像對稱**，
正負起伏相互抵消，**平均 $\approx0$**（小 $c_0$）；若不對稱（例如上升快、下降慢），正負不抵消，
**平均不為零**（大 $c_0$），flicker 的閘門就開大了。

- **奇對稱波形**（odd-symmetric，如理想 $-\sin$，半週期反相）有 $c_0=0$，是極佳特例；但 [P1]
  特別澄清：**小 $c_0$ 不限於奇對稱波形**，只要 rise/fall 對稱即可，類別更廣。
- **toy 對照**：lab_05 用 $\Gamma=\cos\theta$（對稱、$c_0=0$）對比 $\Gamma=\cos\theta+0.4$
  （刻意加 DC、$c_0=0.8$），直接看出 DC 項的有無。

![對稱 vs 不對稱 ISF 的 c0 比較（DC 值是否為零）](/figures/symmetric_vs_asymmetric_isf_c0.png)

| 波形 | ISF DC 值 $c_0/2$ | $c_0$ | flicker 上轉 |
|---|---|---|---|
| 對稱（$\cos\theta$, rise=fall） | $0$ | $0$ | 幾乎沒有 $1/f^3$ |
| 不對稱（$\cos\theta+0.4$） | $0.4$ | $0.8$ | 明顯 $1/f^3$ 裙邊 |

## 第 6 步：differential / complementary 波形的幫助與限制

實務上常用兩招逼近對稱、壓 $c_0$：

- **differential（差動）**：用一對互補節點，把偶次諧波與共模誤差抵消，改善對稱。
- **complementary（互補 CMOS，PMOS/NMOS 對稱配置）**：刻意配對 pull-up/pull-down，使上升/下降
  時間相等 → rise/fall 對稱 → 小 $c_0$。

[P2]（ring oscillator 論文）用實驗直接證實這條規則：**phase noise 隨「對稱控制電壓」變化、在
對稱點出現極小值**，且 $1/f^3$ corner 在對稱點**急遽下降**（[P2] Fig. 17, p.802；對應 claim C4）。

![對稱 vs 不對稱波形的 flicker 上轉（1/f³ 裙邊高度差異）](/figures/flicker_upconversion_symmetric_vs_asymmetric.png)

**限制（要誠實講）**——[P2] 也指出（Sec. VII Design Implications, p.798 原文）：

- **differential 對稱不一定夠**：[P2] 明言「differential symmetry is insufficient」；要的是
  **每個半週期內** rise/fall 的對稱，而不只是兩支差動之間的對稱。
- **tail / bias 源是大破口**：tail current source 的 ISF 常有**大 DC 值**，會把 tail 的 flicker
  強烈上轉，常常主導 close-in 雜訊。對稱化主訊號路徑沒用，要另外處理 tail。
- **更線性的負載有幫助**：[P2] 建議用較線性的負載（如電阻或長通道元件）使波形更對稱，
  進一步壓 corner。
- 即便如此，對稱只壓 **flicker（$1/f^3$）**；它**不改變白噪 $1/f^2$ 那段**（那段由 $\Gamma_{rms}$ 決定，
  不是 $c_0$）。別期待對稱能救整條曲線。

## 數值例子（建立手感）

> **承例 B**：$f_0=5$ GHz、$q_{max}=1$ pC、$\Gamma_{rms}=0.5$。
> 假設 device $1/f$ corner $f_{1/f}=1$ MHz（$\omega_{1/f}=2\pi\times10^6$ rad/s）。
> 比較對稱（$c_0=0.04$）與不對稱（$c_0=0.4$）兩種波形的 $1/f^3$ corner。

用 [P1] Eq.(24)：$\Delta\omega_{1/f^3}=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$，$2\Gamma_{rms}^2=2\times0.25=0.5$。

**不對稱**（$c_0=0.4$，$c_0^2=0.16$）：

$$
\frac{f_{1/f^3}}{f_{1/f}}=\frac{c_0^2}{2\Gamma_{rms}^2}=\frac{0.16}{0.5}=0.32\;\Rightarrow\;f_{1/f^3}=0.32\times1\,\text{MHz}=320\ \text{kHz}.
$$

**對稱**（$c_0=0.04$，$c_0^2=1.6\times10^{-3}$）：

$$
\frac{f_{1/f^3}}{f_{1/f}}=\frac{1.6\times10^{-3}}{0.5}=3.2\times10^{-3}\;\Rightarrow\;f_{1/f^3}=3.2\times10^{-3}\times1\,\text{MHz}=3.2\ \text{kHz}.
$$

- **手感**：device $1/f$ corner 同樣是 1 MHz，但 phase-noise 的 $1/f^3$ corner 從不對稱的 **320 kHz**
  降到對稱的 **3.2 kHz**——整整低了 100 倍（因為 $c_0^2$ 差 100 倍）。這正是「$1/f^3$ corner ≠ device
  $1/f$ corner」的數值寫照：**好的對稱性把陡裙邊推得離載波很近**，close-in 乾淨得多。
- **dimension check**：corner 是頻率，$\text{MHz}\times$（無因次比例）$=$ 頻率 ✓。

## 對應模擬圖（toy model，非 transistor-level）

[lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion) 把 flicker 電流分別餵給對稱
（$\cos$，$c_0=0$）與不對稱（$\cos+0.5$）兩種 toy ISF，估 close-in phase PSD：對稱者幾乎沒有
$1/f^3$、不對稱者出現明顯 $-30$ dB/decade 裙邊。$c_0$ 的視覺化見 lab_05 的
`symmetric_vs_asymmetric_isf_c0.png`（上方表格）。

核心 Python（完整 script：`simulations/lab_07_flicker_noise.py`）：

```python
import numpy as np
from simulations.common.noise_utils import flicker_noise, estimate_psd
from simulations.common.isf_utils import gamma_symmetric, gamma_asymmetric

fs, n, qmax = 256.0, 2**20, 1.0
t = np.arange(n) / fs
theta = 2 * np.pi * 1.0 * t                          # f0 = 1 (toy 正規化頻率)

i_f = flicker_noise(n, fs, k_flicker=1e-4)           # 1/f 電流

# ISF 加權 + 積分器：phi = cumsum(Gamma * i_n / qmax) / fs
def phase_from_isf(i_n, gamma_vals, q_max, fs):
    g = gamma_vals * i_n / q_max
    return np.cumsum(g) / fs

gamma_sym  = gamma_symmetric(theta)                  # c0 = 0
gamma_asym = gamma_asymmetric(theta, alpha=0.5)      # c0 = 2*alpha = 1.0（DC = 0.5）

phi_sym  = phase_from_isf(i_f, gamma_sym,  qmax, fs)  # 對稱 -> close-in 幾乎平
phi_asym = phase_from_isf(i_f, gamma_asym, qmax, fs)  # 不對稱 -> 1/f^3 裙邊
```

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| $\Delta\omega<\omega_{1/f}$ | flicker model（Eq.22）成立、得 $1/f^3$ | 高於 corner 退回白噪 $1/f^2$ |
| 小擾動、相位線性 | Eq.(13) 分諧波式成立 | 大注入 → ISF 失真、$c_0$ 改變 |
| 已知正確的 $c_0$ | corner 預測準 | $c_0$ 對波形細節、tail、負載很敏感，需模擬萃取 |
| 對稱化主路徑 | 壓 $1/f^3$ 有效 | 對 tail flicker、白噪 $1/f^2$ 無效 |

## 與哪些 paper／公式對應

- device flicker model [P1] Eq.(22), p.185；$1/f^3$ phase noise [P1] Eq.(23), p.185；
  $1/f^3$ corner [P1] Eq.(24), p.185。
- 上游分諧波式 [P1] Eq.(13), p.183；對稱性設計討論 [P1] Sec. IV & Fig. 16, p.187–188。
- 對稱實驗證據 [P2] Fig. 17, p.802；differential 不足的限制 [P2] Sec. VII (Design Implications), p.798。
- claims C4（只有 $c_0$ 上轉、對稱抑制）、C5（corner ≠ device corner）。

## Worked examples 數值例題

兩題都用 [P1] Eq.(24) 的精確形式：$\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\dfrac{c_0^2}{2\Gamma_{rms}^2}$。
這裡沿用全站 canonical 的 $\Gamma_{rms}=0.5$（故 $2\Gamma_{rms}^2=0.5$），給定 $c_0,\omega_{1/f}$ 兩組數字代入。
**特例**：若 ISF 僅含基波（$c_1\gg c_2,c_3,\dots$），Parseval（[P1] Eq.(20)）給 $\Gamma_{rms}^2=c_1^2/2$，
此時精確式化簡為 $\dfrac{c_0^2}{2\Gamma_{rms}^2}=\dfrac{c_0^2}{c_1^2}=(c_0/c_1)^2$；本頁以精確形式為主，不用此特例算數字。
格式：題目 → 逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證。

### 例 E：不對稱波形（大 $c_0$）的 1/f³ corner

> **題目**：$c_0=0.4$、canonical $\Gamma_{rms}=0.5$、device $f_{1/f}=1$ MHz（$\omega_{1/f}=2\pi\times10^6$ rad/s）。
> 求 phase-noise 的 $1/f^3$ corner $f_{1/f^3}$。

**步驟 1（算比例 $c_0^2/(2\Gamma_{rms}^2)$）**：$\dfrac{c_0^2}{2\Gamma_{rms}^2}=\dfrac{0.4^2}{2\times0.5^2}=\dfrac{0.16}{0.5}=0.32$（無因次）。

**步驟 2（乘 device corner）**：corner 是頻率，可直接用 Hz 算（$2\pi$ 在比例式中約掉）：

$$
f_{1/f^3}=f_{1/f}\cdot\frac{c_0^2}{2\Gamma_{rms}^2}=1\,\text{MHz}\times0.32=320\ \text{kHz}.
$$

- **結果**：$f_{1/f^3}=320$ kHz，已經 **比 device 的 1 MHz corner 低** —— 即使是「不算對稱」的波形，
  $1/f^3$ corner 也已被壓到 device corner 之下（因 $c_0\ll\Gamma_{rms}\cdot\sqrt2$）。此值與
  [symmetry](/06_design_insights/symmetry)、[device_noise_mapping](/06_design_insights/device_noise_mapping) 一致。
- **dimension check**：$f_{1/f}$（Hz）× 無因次比例 = Hz ✓，是個頻率。

```python
from simulations.common.isf_utils import gamma_rms  # noqa: F401
# corner 由精確式 c0^2/(2*Gamma_rms^2) 決定（Eq.24）；canonical Gamma_rms=0.5
c0, gamma_rms_val, f_1f = 0.4, 0.5, 1e6
f_1f3 = f_1f * c0**2 / (2*gamma_rms_val**2)
print(f_1f3/1e3, "kHz")          # -> 320.0 kHz
```

### 例 F：對稱化（小 $c_0$）如何把 corner 壓低

> **題目**：把例 E 的波形對稱化，$c_0$ 從 0.4 降到 0.04（canonical $\Gamma_{rms}=0.5$、$f_{1/f}=1$ MHz 不變）。
> 求新的 $f_{1/f^3}$，並說明對稱性如何起作用。

**步驟 1（新比例）**：$\dfrac{c_0^2}{2\Gamma_{rms}^2}=\dfrac{0.04^2}{2\times0.5^2}=\dfrac{1.6\times10^{-3}}{0.5}=3.2\times10^{-3}$。

**步驟 2（乘 device corner）**：

$$
f_{1/f^3}=1\,\text{MHz}\times3.2\times10^{-3}=3.2\ \text{kHz}.
$$

- **結果**：$f_{1/f^3}=3.2$ kHz。$c_0$ 降 10 倍 $\Rightarrow c_0^2$ 降 100 倍 $\Rightarrow$ corner 從
  320 kHz 降到 3.2 kHz（**低 100 倍**）。
- **對稱性如何把它壓低（這題的重點）**：corner $\propto c_0^2$，而 $c_0/2$ 是 ISF 在一週期上的**平均**
  （DC 值）。把波形的 **rise/fall 做對稱**，ISF 在敏感區的正負起伏相互抵消 → $c_0$ 趨近 0 → corner 以
  **平方速率**崩塌。這就是「$1/f^3$ corner ≠ device $1/f$ corner」的數值寫照：device corner 還是 1 MHz，
  但 close-in 的陡裙邊被推到 3.2 kHz，載波附近乾淨得多。
- **dimension check**：Hz × 無因次 = Hz ✓。

```python
# 對稱化把 c0 壓小 -> corner ∝ c0^2 以平方崩塌（canonical Gamma_rms=0.5）
f_1f = 1e6; gamma_rms_val = 0.5
for c0 in (0.4, 0.04):
    print(c0, "->", f_1f*c0**2/(2*gamma_rms_val**2)/1e3, "kHz")   # 0.4 -> 320.0 kHz ; 0.04 -> 3.2 kHz
```

## 重點回顧

- flicker 是 device 低頻雜訊（$\propto1/f$），需被「上轉」才會出現在載波附近。
- **只有 ISF 的 DC 項 $c_0$** 能上轉 flicker → close-in 變 $-30$ dB/decade 的 $1/f^3$（Eq.23）。
- **$1/f^3$ corner $=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)\ne$ device $1/f$ corner**（Eq.24）；
  對稱波形（小 $c_0$）把 corner 推到遠低於 device corner。
- 波形 **rise/fall 對稱** $\Rightarrow$ ISF 平均（$c_0/2$）$\approx0$ $\Rightarrow$ $1/f^3$ 大幅下降。
- differential/complementary 幫助對稱，但 **differential 對稱不夠**、**tail 源的大 $c_0$ 是破口**、
  且對稱**不改善白噪 $1/f^2$ 段**。
- 數值：device corner 1 MHz、canonical $\Gamma_{rms}=0.5$ 下，$c_0$ 從 0.4→0.04 使 $1/f^3$ corner 從 320 kHz→3.2 kHz（差 100 倍）。

## 延伸閱讀

- 白噪那段：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- ISF 傅立葉與 $c_0$：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- cyclostationary 與 tail 閘控：[effective_isf](/03_isf_core_theory/effective_isf)
- 對稱性設計專頁：[symmetry](/06_design_insights/symmetry)
- 模擬驗證：[lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion)、[lab_05](/04_simulation_labs/lab_05_isf_fourier_coefficients)
