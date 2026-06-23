---
title: 波形對稱性與 flicker upconversion
description: 為什麼 rise/fall 對稱的波形能把 1/f device noise「擋」在 close-in 之外——ISF 的 c0 如何決定 1/f³ corner，以及降低 c0 的 design knobs。
---

# 波形對稱性與 flicker upconversion

> **先備**：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)（flicker → $1/f^3$ 的完整推導，本頁是它的設計面）、[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（ISF 的傅立葉係數 $c_0,c_n$ 與 Parseval）、[device_noise_mapping](/06_design_insights/device_noise_mapping)（effective ISF $\Gamma_{eff}=\Gamma\cdot\alpha$ 的 $c_0$ 才是真元兇）｜ **接下來**：[waveform_slope](/06_design_insights/waveform_slope)、[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)

這頁回答一個 layout/topology 階段就要想清楚的問題：**為什麼一個 rise/fall（上升／下降）
對稱的波形，close-in（近載波）的 1/f³ phase noise（相位雜訊）會明顯比較低？**
答案完全藏在 ISF 的一個傅立葉係數——DC 項 $c_0$ 裡。

> **物理直覺（先講結論）**：device 的 flicker noise（1/f 雜訊，閘極/通道裡的慢變雜訊）
> 是一個**接近 DC 的低頻**雜訊。低頻雜訊本來不該污染高頻載波——但 ISF 是一個**週期函數**，
> 它的 DC 分量 $c_0/2$ 會像一個「整流器」一樣，把低頻 device noise **持續同號地**累積進相位，
> 把它**上轉（upconvert）**到載波附近，變成 close-in 的 1/f³ skirt（裙擺）。
> 如果波形 rise/fall 完全對稱，ISF 在一個週期裡正負面積相消，$c_0\to0$，這個上轉通道就被關掉了。

## 第 1 步：為什麼只有 $c_0$ 上轉 flicker

把 ISF 寫成傅立葉級數（[P1] Eq.(12), p.183）：

$$
\Gamma(\omega_0\tau)=\frac{c_0}{2}+\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)
$$

代進 LTV phase response（[P1] Eq.(13), p.183），把相位拆成各諧波貢獻：

$$
\phi(t)=\frac{1}{q_{max}}\!\left[\frac{c_0}{2}\!\int_{-\infty}^{t}\!i_n\,d\tau+\sum_{n=1}^{\infty}c_n\!\int_{-\infty}^{t}\!i_n\cos(n\omega_0\tau+\theta_n)\,d\tau\right]
$$

- **關鍵觀察**：device 的 flicker noise 能量集中在**接近 DC**（$\Delta\omega\ll\omega_0$）。
  上式中，$c_n$（$n\ge1$）那些項都帶一個 $\cos(n\omega_0\tau+\theta_n)$，會把低頻 noise
  乘上一個高頻載波——這是一個**搬移（mixing）**，把 noise 搬到 $\pm n\omega_0$ 附近，**遠離** DC。
- 只有 **$c_0/2$ 那一項沒有載波**：它直接對低頻 noise 做**純積分**。低頻 noise 在一段時間內
  幾乎同號，積分後**累積不消**，於是 close-in 相位被持續推動 → 上轉成 1/f³。
- **一句話**：$c_n$ 像 mixer（會把 noise 搬走），$c_0$ 像 integrator（會把 DC noise 留下並放大）。

## 第 2 步：1/f³ phase noise 與 corner 公式

把 device flicker model（[P1] Eq.(22), p.185）

$$
\overline{i_{n,1/f}^2}=\overline{i_n^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}
$$

接到只剩 $c_0$ 通道的 phase noise，得到 1/f³ 區（[P1] Eq.(23), p.185）：

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}\right)
$$

- **斜率 dimension check**：$1/\Delta\omega^2$（來自相位積分）再乘 $1/\Delta\omega$（來自 flicker 的
  $\omega_{1/f}/\Delta\omega$）= $1/\Delta\omega^3$ → 每十倍頻 $-30$ dB，正是 1/f³。✓
- **關鍵**：分子是 $c_0^2$。**對稱波形 $c_0\to0$ → 整個 1/f³ 區被壓下去。**

把 1/f³ 區與 1/f² 區（[P1] Eq.(21)）相交，定義 **1/f³ corner**（[P1] Eq.(24), p.185）：

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2
$$

**逐步代數：corner 是怎麼從「兩區相等」解出來的。** corner 的定義是「1/f³ 區與 1/f² 區
在這個 offset 上**剛好一樣高**」。把兩條（線性、未取 log 的）功率密度令相等：

$$
\begin{aligned}
\underbrace{\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}}_{\text{1/f}^3\text{ 區（Eq.23 內括號）}}
&=\underbrace{\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}}_{\text{1/f}^2\text{ 區（Eq.21 內括號）}} \\[4pt]
\frac{c_0^2}{8}\cdot\frac{\omega_{1/f}}{\Delta\omega}&=\frac{\Gamma_{rms}^2}{4}
\qquad(\text{兩邊同消 }q_{max}^2,\ \overline{i_n^2}/\Delta f,\ \Delta\omega^2) \\[4pt]
\frac{\omega_{1/f}}{\Delta\omega}&=\frac{\Gamma_{rms}^2}{4}\cdot\frac{8}{c_0^2}=\frac{2\,\Gamma_{rms}^2}{c_0^2} \\[4pt]
\Rightarrow\quad \Delta\omega=\Delta\omega_{1/f^3}&=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}.
\end{aligned}
$$

- **每一步用到什麼**：第 2 行只是「同除以兩邊都有的因子」（純代數，不引入新物理）；
  注意 $\overline{i_n^2}/\Delta f$、$q_{max}^2$、$\Delta\omega^2$ 三者在兩區是**同一個值**，所以可消。
- **為什麼 $\Delta\omega^2$ 也能消**：1/f³ 區是 $1/\Delta\omega^3$、1/f² 區是 $1/\Delta\omega^2$，相除剩一個 $1/\Delta\omega$
  ——那個 $1/\Delta\omega$ 正是上面第 2 行左邊還留著的 $\omega_{1/f}/\Delta\omega$ 因子。解這個一次式就得 corner。
- **再到 $\approx(c_0/c_1)^2$**：用 Parseval（[P1] Eq.(20)）$2\Gamma_{rms}^2=\sum c_n^2$；若 ISF 由基波主導
  （$c_1\gg c_2,c_3,\dots$），則 $2\Gamma_{rms}^2\approx c_1^2$，代入得 $\Delta\omega_{1/f^3}\approx\omega_{1/f}(c_0/c_1)^2$。
- **dimension check**：右邊 $\omega_{1/f}$ 是 rad/s，$c_0^2/(2\Gamma_{rms}^2)$ 是「無因次/無因次」=無因次，
  故 $\Delta\omega_{1/f^3}$ 是 rad/s ✓。

- **最重要的設計啟示（claim C5）**：1/f³ corner **不等於** device 的 1/f corner $\omega_{1/f}$！
  它被一個 $c_0^2/(2\Gamma_{rms}^2)$ 因子縮放。$c_0$ 越小，corner 被**推到遠低於** $\omega_{1/f}$
  的地方——亦即同一顆 transistor、同一個 device 1/f corner，光靠把波形做對稱，就能把
  1/f³ skirt 的轉折點往低頻移好幾個 decade。
- **符號陷阱**（見 [notation](/00_overview/notation)）：$c_0$ 是傅立葉**係數**，ISF 的 DC**值**是 $c_0/2$。
  Eq.(24) 用的是係數 $c_0$，別在這裡掉一個 factor 2。

## 第 3 步：對稱性怎麼讓 $c_0\to0$

$c_0$ 是 ISF 在一個週期上的平均（的兩倍）：

$$
\frac{c_0}{2}=\frac{1}{2\pi}\int_0^{2\pi}\Gamma(x)\,dx\quad\Rightarrow\quad c_0=\frac{1}{\pi}\int_0^{2\pi}\Gamma(x)\,dx
$$

- ISF 的形狀大致**正比於波形斜率**（ZC 附近斜率大→$|\Gamma|$ 大；波峰斜率為 0→$\Gamma\approx0$，
  見 [waveform_slope](/06_design_insights/waveform_slope)）。
- 若 rise 段與 fall 段**形狀對稱**（rise 斜率 = fall 斜率的鏡像），則 ISF 在上升半週與下降半週
  的值**大小相等、正負相反**，一個週期積分相消 → $c_0=0$。
- 理想 LC 的 $\Gamma(\theta)=-\sin\theta$ 就是這種**奇對稱**：$\int_0^{2\pi}(-\sin\theta)\,d\theta=0$，
  所以理想 LC 天生 $c_0=0$、1/f³ 上轉極弱。
- 不對稱（例如 rise 快、fall 慢，或有偶次諧波讓波形上下不對稱）會讓 ISF 平均值偏離 0 → $c_0\neq0$。

下圖把對稱與不對稱兩種 ISF 疊在一起：對稱者 DC 平均線壓在 0，不對稱者整條被抬起一個 $c_0/2$
的「直流偏置」——那個偏置就是 flicker 上轉的元兇。

![對稱 vs 不對稱 ISF 與其 c0](/figures/symmetric_vs_asymmetric_isf_c0.png)

把 device flicker 真的灌進去模擬，close-in 的差別非常明顯：不對稱波形出現一段陡峭的 1/f³ skirt，
對稱波形則幾乎沒有（只剩 1/f² 與 floor）。

![對稱 vs 不對稱波形的 flicker 上轉](/figures/flicker_upconversion_symmetric_vs_asymmetric.png)

> 這兩張都是 **pedagogical toy model（教學玩具模型，非 transistor-level）**：
> ISF 用解析形狀（對稱 $\cos\theta$、不對稱 $\cos\theta+0.4$ 之類），flicker 用合成 1/f 序列。
> 它們忠實呈現「$c_0$ 決定 1/f³」的因果，但不是某顆真實電晶體的量測。
> 完整 script：`simulations/lab_05_fourier_isf.py`、`simulations/lab_07_flicker_noise.py`。

## 數值例子（建立手感）

> 用 canonical 數值 + 一個假設的 device 1/f corner。

**對稱波形（$c_0\approx0$）**：理論上 $\Delta\omega_{1/f^3}=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)\to0$，
1/f³ corner 被壓到極低頻——實務上由 residual mismatch 決定的小 $c_0$ 主導（見下表 knobs）。

**不對稱波形**：取 $c_0=0.4$、$\Gamma_{rms}=0.5$（則 $c_0^2/(2\Gamma_{rms}^2)=0.16/(2\times0.25)=0.32$）。
若 device $f_{1/f}=1$ MHz，則

$$
f_{1/f^3}=f_{1/f}\cdot\frac{c_0^2}{2\Gamma_{rms}^2}=1\ \text{MHz}\times0.32=320\ \text{kHz}.
$$

- **手感**：把 $c_0$ 從 0.4 降到 0.04（小 10 倍），corner 降 100 倍（$c_0^2$）→ 從 320 kHz 降到 3.2 kHz。
  也就是說**對稱性每改善一個量級，1/f³ skirt 的影響範圍縮小兩個量級**——這是極划算的設計槓桿。
- 對應實驗證據：[P2] Fig. 17, p.802 量到 ring oscillator 的 phase noise 對「symmetry 控制電壓」
  畫出來會在**對稱點出現一個最小值**——直接支持「對稱 → 低 1/f³」這條設計規則。
  （[P2] Fig. 17, p.802「Phase noise versus symmetry voltage for oscillator number 7」已核實：
  y 軸為 1/f³ corner frequency，在 symmetry point 出現明顯下凹的最小值。）

## 降低 $c_0$ 的 design knobs（清單）

| Knob | 怎麼做 | 為什麼降 $c_0$ | 代價／註記 |
|---|---|---|---|
| rise/fall 對稱 | NMOS/PMOS 驅動強度、pull-up/pull-down 對稱（ring）；differential（差動）topology | ISF 上下半週相消 → 平均→0 | 需要 sizing/偏壓微調；製程偏移會殘留 $c_0$ |
| differential / 偶次諧波抑制 | 全差動、對稱負載、抑制偶次 harmonic | 偶次諧波讓波形上下不對稱 → 抬升 $c_0$ | 兩倍 device、面積、功耗 |
| 對稱負載（symmetric load，ring） | 用 symmetric load（[P2] 的做法）取代單端 inverter delay cell | 讓 rise/fall 波形匹配 | [P2] Fig. 17 的「symmetry voltage」就在調這個 |
| 降低 DC bias 點漂移 | 控制 duty cycle 接近 50% | duty 偏離 50% 等於波形 DC 不對稱 → $c_0\neq0$ | 需要 duty-cycle correction |
| 直接降 device flicker | 用大面積、PMOS、buried-channel device | 降 $\omega_{1/f}$ 本身（不改 $c_0$，但降 1/f³ 大小） | 大面積→大寄生電容→降 $f_0$ |

> 注意分兩類：前四個 knob 改 **$c_0$／$f_{1/f^3}$ corner 位置**；最後一個改 **device $\omega_{1/f}$／1/f³ 的整體高度**。
> 設計時兩者都可用，但「做對稱」通常 free（不花額外功耗），是第一槍。

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 小擾動、ISF 已知且固定 | $c_0$ 完全決定 1/f³ | 大注入／強非線性下 ISF 本身會變 |
| device noise 是純 1/f | $\omega_{1/f}/\Delta\omega$ 模型成立 | 有 RTS／burst noise 時要另計 |
| cyclostationary 已折進 effective ISF | 用 $\Gamma_{eff}=\Gamma\cdot\alpha$ 算 $c_0$ | 若 $\alpha$ 也不對稱，會「重新」製造出有效 $c_0$（見 [device_noise_mapping](/06_design_insights/device_noise_mapping)） |

> **重要警告**：真正決定上轉的是 **effective ISF $\Gamma_{eff}=\Gamma\cdot\alpha$** 的 $c_0$，不只是裸 $\Gamma$ 的 $c_0$。
> 就算 $\Gamma$ 對稱，如果 device 只在半週「漏雜訊」（$\alpha$ 不對稱），$\Gamma_{eff}$ 的 $c_0$ 仍可能不為零。
> 詳見 [device_noise_mapping](/06_design_insights/device_noise_mapping) 與 [effective_isf](/03_isf_core_theory/effective_isf)。

## Worked examples 數值例題

以下兩題示範「對稱性改善 → 1/f³ corner 下降」這條最划算的設計槓桿，沿用本站 canonical
$\Gamma_{rms}=0.5$、device $f_{1/f}=1$ MHz。

> **例 1（基準：算不對稱波形的 1/f³ corner）**
> 給定 $c_0=0.4$、$\Gamma_{rms}=0.5$、device 1/f corner $f_{1/f}=1$ MHz，求 1/f³ corner $f_{1/f^3}$。

**逐步代入（帶單位）**，用上面剛推導的 $f_{1/f^3}=f_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$：

$$
\begin{aligned}
\frac{c_0^2}{2\Gamma_{rms}^2}&=\frac{(0.4)^2}{2\times(0.5)^2}=\frac{0.16}{0.50}=0.32\quad(\text{無因次}) \\[4pt]
f_{1/f^3}&=f_{1/f}\times0.32=1\ \text{MHz}\times0.32=0.32\ \text{MHz}=320\ \text{kHz}.
\end{aligned}
$$

- **結果**：$f_{1/f^3}=320$ kHz——比 device 自己的 1 MHz corner **還低**，因為 $c_0^2/(2\Gamma_{rms}^2)=0.32 < 1$。
- **Dimension check**：$[\text{Hz}]\times[\text{無因次}]=[\text{Hz}]$ ✓（ratio of frequencies 用 Hz 或 rad/s 都行，
  因為 $f_{1/f^3}/f_{1/f}=\omega_{1/f^3}/\omega_{1/f}$，$2\pi$ 同消）。
- **一行 Python 驗證**（引用 canonical 換算；`simulations/common/` 無專屬 corner 函式，直接算）：

```python
c0, gamma_rms, f_1f = 0.4, 0.5, 1e6
f_1f3 = f_1f * c0**2 / (2 * gamma_rms**2)
print(f_1f3 / 1e3, "kHz")   # -> 320.0 kHz
```

> **例 2（對稱性改善一個量級 → corner 降兩個量級）**
> 把波形做更對稱，使 $c_0$ 從 $0.4$ 降到 $0.04$（小 10 倍），$\Gamma_{rms}$、$f_{1/f}$ 不變。求新 corner，
> 並用 dB 表示「兩條 1/f³ 漸近線（外推 skirt）的高度差了多少」。

**逐步代入（帶單位）**：

$$
\begin{aligned}
f_{1/f^3}'&=f_{1/f}\cdot\frac{(c_0')^2}{2\Gamma_{rms}^2}=1\ \text{MHz}\times\frac{(0.04)^2}{2\times(0.5)^2}
=1\ \text{MHz}\times\frac{0.0016}{0.5}=1\ \text{MHz}\times3.2\times10^{-3}=3.2\ \text{kHz}.
\end{aligned}
$$

corner 從 $320$ kHz → $3.2$ kHz（降 100 倍 $=c_0$ 比值的平方 $10^2$）。注意改善後 corner 掉到
$3.2$ kHz，故 $\Delta f=10$ kHz 對改善後的波形已落在 **1/f² 區**（不再是 1/f³）；以下比較的是
兩條 **1/f³ 漸近線（外推 skirt）** 的高度。1/f³ phase noise（[P1] Eq.(23)）$\propto c_0^2$，所以高度的變化是

$$
\Delta\mathcal{L}=10\log_{10}\!\left(\frac{(c_0')^2}{c_0^2}\right)=10\log_{10}\!\left(\frac{0.04^2}{0.4^2}\right)=10\log_{10}(0.01)=-20\ \text{dB}.
$$

- **結果**：$c_0$ 降 10 倍 → 1/f³ skirt 整體**降 20 dB**、corner **降 100 倍**（到 3.2 kHz）。
  「對稱性每改善一個量級，1/f³ 影響範圍縮小兩個量級」就是這個 $c_0^2$ 律。
- **Dimension check**：dB 是功率比取 log（無因次）✓；corner 仍是 Hz ✓。
- **一行 Python 驗證**：

```python
import numpy as np
c0_old, c0_new = 0.4, 0.04
print("corner ratio:", (c0_new/c0_old)**2,            # -> 0.01  (3.2 kHz / 320 kHz)
      "; dL =", 10*np.log10((c0_new/c0_old)**2), "dB") # -> -20.0 dB
```

> 兩題都是 **pedagogical toy（非 transistor-level）**：$c_0$ 用假設值代表「殘餘不對稱」。真實電路的
> $c_0$ 要用 effective ISF（含 cyclostationary $\alpha$）萃取，見 [device_noise_mapping](/06_design_insights/device_noise_mapping)。

## 重點回顧

- 只有 ISF 的 DC 係數 $c_0$ 會把 device 1/f noise 上轉成 close-in 1/f³（[P1] Eq.(23)）。
- 1/f³ corner $=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$，**不等於** device 1/f corner（[P1] Eq.(24)）。
- rise/fall 對稱 → ISF 一週積分相消 → $c_0\to0$ → 1/f³ corner 被推到很低頻。
- $c_0$ 降 10 倍，1/f³ corner 降 100 倍（$c_0^2$）：不對稱 $c_0=0.4$、$f_{1/f}=1$ MHz → corner 320 kHz。
- 設計槓桿：differential、對稱負載、duty 50%；要看 **effective** ISF（含 $\alpha$）的 $c_0$。
- 實驗：[P2] Fig. 17 phase noise vs symmetry voltage 有最小值。

## 延伸閱讀

- 上轉的完整推導：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- 為何 $\Gamma$ 形狀像波形斜率：[waveform_slope](/06_design_insights/waveform_slope)
- effective ISF 與 $\alpha$：[device_noise_mapping](/06_design_insights/device_noise_mapping)、[effective_isf](/03_isf_core_theory/effective_isf)
- 傅立葉係數與 Parseval：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- SerDes 為何更在意 close-in：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
