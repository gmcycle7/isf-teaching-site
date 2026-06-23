---
title: 設計章習題（含完整解答）
description: 設計章成套習題：q_max/Γrms/對稱性設計反推、ring vs LC 比較、PLL 最佳 loop BW、σt→BER、tail noise 對策。每題附逐步解、單位與 dimension check、數值答案、一行 Python 驗證。
---

# 設計章習題（含完整解答）

> **先備**：[tank_swing](/06_design_insights/tank_swing)、[symmetry](/06_design_insights/symmetry)、[lc_vs_ring](/06_design_insights/lc_vs_ring)、[pll_noise_budget](/06_design_insights/pll_noise_budget)、[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)（本頁題目全部用這些頁的 ISF 公式作答）｜ **其他習題**：[02 基礎章習題](/02_foundations/exercises)、[03 核心理論章習題](/03_isf_core_theory/exercises)

這頁是 **06 設計洞見章** 的成套習題，重點在**設計反推題**（給目標規格、反算旋鈕）與
**比較/取捨題**（ring vs LC、loop BW 權衡、tail noise 對策），全部用 ISF 公式作答。

> **格式**：每題 = **逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證**。
> Python 引用 `simulations/common/`（含 `pll_utils`、`serdes_utils`、`isf_utils`、`noise_utils`）。

涉及的權威公式（逐字取自規範，含引用）：

- 白噪 1/f² 招牌：$\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)$（[P1] Eq.(21), p.185）
- 1/f³ corner：$\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\dfrac{c_0^2}{2\,\Gamma_{rms}^2}$（[P1] Eq.(24), p.185）
- ring $\Gamma_{rms}\propto N^{-3/4}$（[P2] Eq.(16), p.794）；ring 頻率 $f_0=\dfrac{1}{2N\tau_D}$（[P2] Eq.(14), p.794）
- PLL 輸出：$S_{out}=S_{ref}\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$，$\lvert H_{lp}\rvert^2,\lvert H_{hp}\rvert^2$ 見規範 10.2
- SerDes BER（RJ）：$\text{BER}(t)=\tfrac12\big[Q(\tfrac{UI/2-t}{\sigma_t})+Q(\tfrac{UI/2+t}{\sigma_t})\big]$，$Q(x)=\tfrac12\,\mathrm{erfc}(x/\sqrt2)$（規範 10.2）
- rms jitter：$\sigma_t=\dfrac{1}{2\pi f_0}\sqrt{\int S_\phi df}$（規範公式 19）

---

## 題目

### 習題 1（設計反推題）— $q_{max}$、$\Gamma_{rms}$ 達標組合

某 5 GHz LC 振盪器目前 $\mathcal{L}(1\,\text{MHz})=-140$ dBc/Hz（套 Eq.(21)，$\Gamma_{rms}=0.7$、
$q_{max}=1$ pC、$S_i=10^{-23}\ \text{A}^2/\text{Hz}$）。目標把它再壓低 9 dB 到 $-149$ dBc/Hz。
列出兩種達標方案：(a) 只動 $q_{max}$；(b) 只動 $\Gamma_{rms}$。各需多少？

### 習題 2（設計反推題）— 對稱性壓 $1/f^3$ corner

某環振 $\Gamma_{rms}=0.9$、$c_0=0.3$、device $f_{1/f}=2$ MHz。
(a) 用 [P1] Eq.(24)（精確式 $\Delta\omega_{1/f^3}=\omega_{1/f}c_0^2/(2\Gamma_{rms}^2)$）求 $1/f^3$ corner $\Delta f_{1/f^3}$。
(b) 若透過 rise/fall 對稱化把 $c_0$ 壓到 $0.05$，corner 變多少？要達 corner < 1 kHz，$c_0$ 最多多少？

### 習題 3（比較題）— ring vs LC 的 $\Gamma_{rms}$ scaling

(a) 用 [P2] Eq.(16) 的 scaling $\Gamma_{rms}\propto N^{-3/4}$，問把 ring 級數從 $N=5$ 加到 $N=15$，
$\Gamma_{rms}$ 降幾倍？相位雜訊（$\propto\Gamma_{rms}^2$）改善幾 dB？
(b) 一句話說明為何 LC 通常仍比 ring 乾淨（從 $\Gamma_{rms}$ 與 $q_{max}$ 兩個旋鈕談）。

### 習題 4（設計題）— PLL 最佳 loop BW（直覺 + 數值）

一顆 ring VCO 自身相位雜訊 $1/f^2$ 很差（$S_{vco}=K_v/f^2$，$K_v=10^{2}\ \text{rad}^2\text{Hz}$），
參考源很乾淨且為白底（$S_{ref}=K_r=10^{-14}\ \text{rad}^2/\text{Hz}$，分頻比 $N=1$）。
用規範 10.2 的 type-II 2nd-order transfer，掃 loop 自然頻率 $f_n$，找使輸出積分 jitter
（$\int S_{out}df$，積 1 kHz→100 MHz）最小的 $f_n$。直覺上 $f_n$ 該落在哪？

### 習題 5（數值題）— $\sigma_t\to$ BER bathtub

某 25 Gb/s SerDes，UI $=1/25\text{G}=40$ ps，取樣時鐘 RJ $\sigma_t=1.2$ ps（高斯）。
求 (a) 在 eye 中心（$t=0$）取樣的 BER；(b) 達 $\text{BER}=10^{-12}$ 的時間裕度（取樣可偏離中心多少 ps）。

### 習題 6（設計反推題）— BER 預算反推容許 $\sigma_t$

同上 SerDes（UI $=40$ ps），規格要求在中心取樣 $\text{BER}\le10^{-15}$。求容許的最大 RJ $\sigma_t$（ps）。
（提示：$\text{BER}\approx Q(\tfrac{UI/2}{\sigma_t})$，查 $Q^{-1}(10^{-15})\approx7.94$。）

### 習題 7（對策題）— tail noise 對策（cross-coupled LC VCO）

cross-coupled LC VCO 的 tail current source 的雜訊，會經 $2\times$ 上轉（落在 $2\omega_0$ 附近，
經 ISF 的 $c_2$ 與其 DC 分量 $c_0$ 折回 close-in）。用「effective ISF 的 $c_0,c_2$ 才是 tail 雜訊
的麻煩」這個觀點，列出三個降低 tail 雜訊貢獻的設計手段，並各用一條 ISF 量（$c_0$、$c_2$、
$\Gamma_{eff,rms}$、$q_{max}$）說明為什麼有效。此題為 illustrative（標明）。

### 習題 8（設計反推題）— jitter 預算分配到 PLL 頻段

一個時鐘總 rms jitter 預算 $\sigma_{t,\text{tot}}=300$ fs（$f_0=10$ GHz）。已知近載波（ref/in-band）
貢獻 $\sigma_{t,\text{ref}}=180$ fs。RJ 各源不相關（方差相加）。問留給 VCO（out-of-band）的
jitter 預算 $\sigma_{t,\text{vco}}$ 最多多少 fs？對應的相位變異 $\sigma_{\phi,\text{vco}}^2$（rad²）是多少？

---

## 解答展開

<details>
<summary><strong>習題 1 解答</strong>（$q_{max}$、$\Gamma_{rms}$ 達標組合）</summary>

**設計反推策略。** Eq.(21) 內 $\mathcal{L}_{\text{lin}}\propto\Gamma_{rms}^2/q_{max}^2$。要降 9 dB，即
linear 降 $10^{0.9}=7.94$ 倍。

**(a) 只動 $q_{max}$**（$\mathcal{L}_{\text{lin}}\propto1/q_{max}^2$）：

$$
\frac{q_{max,\text{new}}}{q_{max,\text{old}}}=10^{9/20}=10^{0.45}=2.818\quad\Longrightarrow\quad q_{max,\text{new}}\approx2.82\ \text{pC}.
$$

**(b) 只動 $\Gamma_{rms}$**（$\mathcal{L}_{\text{lin}}\propto\Gamma_{rms}^2$）：

$$
\frac{\Gamma_{rms,\text{new}}}{\Gamma_{rms,\text{old}}}=10^{-9/20}=10^{-0.45}=0.3548\quad\Longrightarrow\quad\Gamma_{rms,\text{new}}\approx0.7\times0.3548=0.248.
$$

**結果**：(a) $q_{max}$ 放大 $\approx2.82$ 倍到 $\approx2.82$ pC；(b) $\Gamma_{rms}$ 壓到 $\approx0.248$
（約原來 1/2.82）。兩者效果相同（各 $-9$ dB），但成本不同：加大 $q_{max}$ 要更大擺幅/功耗，
壓 $\Gamma_{rms}$ 要改波形對稱性與 noise 注入時機（見 [waveform_slope](/06_design_insights/waveform_slope)）。

**驗證一致性**：$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$，9 dB $=10\log_{10}(7.94)$，$\sqrt{7.94}=2.818$ ✓。

**Dimension check**：兩個比值皆無因次（同物理量相除）；$q_{max}$ 仍為 C、$\Gamma_{rms}$ 仍無因次 ✓。

```python
import numpy as np
g = 10**(9/10)                     # linear factor for 9 dB
print("qmax x", round(np.sqrt(g),3), "; Gamma_rms x", round(1/np.sqrt(g),3))
# -> qmax x 2.818 ; Gamma_rms x 0.355
print("new qmax", round(1.0*np.sqrt(g),2), "pC ; new Grms", round(0.7/np.sqrt(g),3))
# -> 2.82 pC ; 0.248
```

</details>

<details>
<summary><strong>習題 2 解答</strong>（對稱性壓 $1/f^3$ corner）</summary>

**(a) 精確式。** [P1] Eq.(24)：$\Delta\omega_{1/f^3}=\omega_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}$。
換成 $\Delta f$（$2\pi$ 約掉，因 $\omega_{1/f}=2\pi f_{1/f}$）：$\Delta f_{1/f^3}=f_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}$。

$$
\Delta f_{1/f^3}=2\times10^6\times\frac{0.3^2}{2\times0.9^2}=2\times10^6\times\frac{0.09}{1.62}=2\times10^6\times0.05556=1.111\times10^{5}\ \text{Hz}\approx111\ \text{kHz}.
$$

**(b) 對稱化 $c_0\to0.05$。**

$$
\Delta f_{1/f^3}=2\times10^6\times\frac{0.05^2}{1.62}=2\times10^6\times1.543\times10^{-3}=3086\ \text{Hz}\approx3.09\ \text{kHz}.
$$

**要 corner < 1 kHz，$c_0$ 上限**：令 $f_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}<10^3$：

$$
c_0^2<\frac{10^3\times2\times0.81}{2\times10^6}=\frac{1620}{2\times10^6}=8.1\times10^{-4}\quad\Longrightarrow\quad c_0<0.0285.
$$

**結果**：(a) $\approx111$ kHz；(b) 壓 $c_0$ 到 0.05 後 $\approx3.09$ kHz；要 corner < 1 kHz 需 $c_0<0.0285$。

**設計訊息**：$1/f^3$ corner $\propto c_0^2$，**波形對稱性（壓 $c_0$）是壓 close-in flicker 上轉
最有效的旋鈕**（見 [symmetry](/06_design_insights/symmetry)）。$c_0$ 來自 rise/fall 不對稱、
duty-cycle 偏差。

**Dimension check**：$(c_0/\Gamma_{rms})^2$ 無因次 $\times\ f_{1/f}$（Hz）$=$ Hz ✓。

```python
import numpy as np
def corner(c0, Grms=0.9, f1f=2e6): return f1f*c0**2/(2*Grms**2)
print(corner(0.3), "Hz ;", corner(0.05), "Hz")           # -> 111111 ; 3086
c0_max = np.sqrt(1e3*2*0.9**2/2e6)
print("c0 <", round(c0_max,4))                            # -> 0.0285
```

</details>

<details>
<summary><strong>習題 3 解答</strong>（ring vs LC 的 $\Gamma_{rms}$ scaling）</summary>

**(a) scaling。** [P2] Eq.(16)：$\Gamma_{rms}\propto N^{-3/4}$。$N:5\to15$（$\times3$）：

$$
\frac{\Gamma_{rms}(15)}{\Gamma_{rms}(5)}=\left(\frac{15}{5}\right)^{-3/4}=3^{-0.75}=0.4387.
$$

相位雜訊 $\propto\Gamma_{rms}^2$，改善：

$$
\Delta\mathcal{L}=10\log_{10}\big(0.4387^2\big)=10\log_{10}(0.1924)=-7.16\ \text{dB}.
$$

**(b) 為何 LC 仍乾淨。** 兩個旋鈕都對 LC 有利：
- **$\Gamma_{rms}$**：LC 波形是平滑正弦（$\Gamma=-\sin$，$\Gamma_{rms}=0.707$，敏感度低且分散）；
  ring 的 ISF 集中在 transition（陡邊），rms 較高、且能量集中在最敏感處。
- **$q_{max}$**：LC tank 的高 $Q$ 允許大電壓擺幅 → 大 $q_{max}=C V_{max}$；ring 每級 swing 受限於
  $V_{DD}$ 且電容小，$q_{max}$ 通常小很多。$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$，
  LC 在分子小、分母大兩頭佔優。

**結果**：(a) $N:5\to15$ 使 $\Gamma_{rms}$ 降 $\approx0.44$ 倍、相位雜訊改善 $\approx7.2$ dB；
(b) LC 在 $\Gamma_{rms}$（小且分散）與 $q_{max}$（高 Q 大擺幅）兩個旋鈕都優於 ring。

**注意**：加 $N$ 同時降頻率（$f_0=1/(2N\tau_D)$）、增功耗；ring 的真正吸引力是面積/可調性/無電感，
不是低相位雜訊。見 [lc_vs_ring](/06_design_insights/lc_vs_ring)。

**Dimension check**：$N$ 無因次、$\Gamma_{rms}$ 無因次；比值與 dB 皆無因次 ✓。

```python
import numpy as np
ratio = (15/5)**(-0.75)
print("Grms ratio", round(ratio,4), "; dPN", round(10*np.log10(ratio**2),2), "dB")
# -> Grms ratio 0.4387 ; dPN -7.16 dB
```

</details>

<details>
<summary><strong>習題 4 解答</strong>（PLL 最佳 loop BW）</summary>

**直覺。** PLL 把 **ref 低通、VCO 高通**（規範 10.2）。
- loop BW $f_n$ **太小** → VCO 的 close-in $1/f^2$ 沒被環路壓掉，in-band 全是 VCO 噪 → jitter 大。
- loop BW $f_n$ **太大** → 把 ref 的噪（與 CP 噪）大量放進來，且 VCO 高通轉折太高、out-of-band
  VCO 噪也多 → jitter 大。
- **最佳 $f_n^\*$** 落在「ref+CP 上升曲線」與「VCO 下降曲線」的**交叉點**附近——讓兩條被整形後的
  曲線在 $f_n$ 附近交會、總積分面積最小。

**數值（掃 $f_n$）。** 用 `shape_output_phase_noise` 與梯形積分，掃 $f_n=10^4\to10^7$ Hz，
找 $\int S_{out}df$（1 kHz→100 MHz）最小者：

**結果**：最佳 $f_n^\*\approx$ 數百 kHz 到 ~1 MHz（落在 ref 白底曲線與 VCO $1/f^2$ 曲線交點附近）。
本題參數下 grid 掃描給 $f_n^\*\approx3\times10^5$ Hz 量級（隨 $S_{ref},K_v$ 而移）。
**這就是 PLL 雜訊預算的核心取捨：loop BW 不是越大越好、也不是越小越好，存在最佳值。**

**Dimension check**：$S_{out}$ 是 rad²/Hz，$\int S_{out}df$ 是 rad²（相位變異）；
$\sigma_t=\sqrt{\cdot}/(2\pi f_0)$ 為 s ✓。

```python
import numpy as np
from simulations.common.pll_utils import shape_output_phase_noise
f = np.logspace(3, 8, 4000)
S_ref = np.full_like(f, 1e-9)           # 白底參考（調到讓最佳 BW 落在掃描範圍內）
S_vco = 1e2 / f**2                       # VCO 1/f^2
fn_grid = np.logspace(4, 7, 60)
var = []
for fn in fn_grid:
    S_out, _, _ = shape_output_phase_noise(f, S_ref, S_vco, fn_hz=fn)
    var.append(np.trapezoid(S_out, f))       # rad^2
fn_opt = fn_grid[int(np.argmin(var))]
print("optimal f_n ~", f"{fn_opt:.2e}", "Hz")   # -> ~1.9e5 Hz（量級 10^5；非理想 brick-wall 故略低於 10/√S_ref≈3e5）
```

（完整圖見 [pll_noise_budget](/06_design_insights/pll_noise_budget)。）

</details>

<details>
<summary><strong>習題 5 解答</strong>（$\sigma_t\to$ BER bathtub）</summary>

**(a) 中心取樣 BER（$t=0$）。** 規範 10.2 的 RJ bathtub，$t=0$ 時兩 $Q$ 項相等：

$$
\text{BER}(0)=\tfrac12\big[Q(\tfrac{UI/2}{\sigma_t})+Q(\tfrac{UI/2}{\sigma_t})\big]=Q\!\left(\frac{UI/2}{\sigma_t}\right)=Q\!\left(\frac{20\ \text{ps}}{1.2\ \text{ps}}\right)=Q(16.67).
$$

$Q(16.67)$ 是天文數字級的小（$\sim10^{-62}$）——中心取樣幾乎不可能錯。

**(b) $\text{BER}=10^{-12}$ 的裕度。** 解 $Q\!\left(\dfrac{UI/2-t}{\sigma_t}\right)=10^{-12}$（單邊主導）。
$Q^{-1}(10^{-12})\approx7.03$，故

$$
\frac{UI/2-t}{\sigma_t}=7.03\quad\Longrightarrow\quad t=\frac{UI}{2}-7.03\,\sigma_t=20-7.03\times1.2=20-8.44=11.56\ \text{ps}.
$$

即取樣點可偏離中心 $\pm11.56$ ps 仍保 $\text{BER}\le10^{-12}$；**eye 開口（@$10^{-12}$）$\approx2\times11.56=23.1$ ps**
（佔 UI 的 58%）。

**結果**：(a) $\text{BER}(0)\approx Q(16.67)\sim10^{-62}$（中心極安全）；(b) $10^{-12}$ 裕度 $\pm11.56$ ps、
eye 開口 $\approx23$ ps。

**Dimension check**：$Q$ 的引數 $\dfrac{\text{ps}}{\text{ps}}$ 無因次 ✓；裕度單位 ps ✓。

```python
import numpy as np
from scipy.special import erfcinv
from simulations.common.serdes_utils import Q, ber_bathtub
ui, sigma_t = 40e-12, 1.2e-12
print("BER(0) =", ber_bathtub(np.array([0.0]), sigma_t, ui)[0])      # ~1e-62
qinv = np.sqrt(2)*erfcinv(2*1e-12)                                    # Q^-1(1e-12) ~ 7.03
margin = ui/2 - qinv*sigma_t
print("margin", round(margin*1e12,2), "ps ; eye", round(2*margin*1e12,1), "ps")
# -> margin 11.56 ps ; eye 23.1 ps
```

</details>

<details>
<summary><strong>習題 6 解答</strong>（BER 預算反推容許 $\sigma_t$）</summary>

**設計反推策略。** 中心取樣 $\text{BER}(0)=Q\!\left(\dfrac{UI/2}{\sigma_t}\right)$。要求 $\le10^{-15}$，
即 $\dfrac{UI/2}{\sigma_t}\ge Q^{-1}(10^{-15})\approx7.94$。反解 $\sigma_t$ 上限：

$$
\sigma_{t,\max}=\frac{UI/2}{Q^{-1}(10^{-15})}=\frac{20\ \text{ps}}{7.94}=2.519\ \text{ps}.
$$

**結果**：容許最大 RJ $\sigma_t\approx2.52$ ps（即 $UI/2$ 要 $\ge7.94\sigma_t$，俗稱「$\approx16\,\sigma$ 全開口」
法則的一半：$UI\ge15.9\,\sigma_t$）。

**設計訊息**：BER 規格越嚴（$10^{-15}$ vs $10^{-12}$），$Q^{-1}$ 越大（7.94 vs 7.03），容許 jitter
越小。25 Gb/s 下要 $\sigma_t<2.5$ ps——這直接把規格丟回時鐘源：用 Eq.(19) 反推容許的
$\int S_\phi df$，再回到 $\Gamma_{rms}/q_{max}$（連 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)）。

**Dimension check**：$\dfrac{\text{ps}}{\text{無因次}}=\text{ps}$ ✓。

```python
import numpy as np
from scipy.special import erfcinv
ui = 40e-12
qinv = np.sqrt(2)*erfcinv(2*1e-15)        # Q^-1(1e-15) ~ 7.94
sigma_max = (ui/2)/qinv
print(round(sigma_max*1e12,3), "ps ; UI/sigma =", round(ui/sigma_max,1))
# -> 2.519 ps ; UI/sigma = 15.9
```

</details>

<details>
<summary><strong>習題 7 解答</strong>（tail noise 對策，illustrative）</summary>

> **標明 illustrative**：以下 cross-coupled LC VCO 的 tail 機制是教學用的定性模型，常數/具體 $c_n$
> 依拓樸而變；嚴格值需 transient/adjoint 萃取（見 [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)）。

**機制回顧。** tail current source 的 low-frequency（含 flicker）雜訊會被差動對的開關
**$2\times$ 上轉**到 $2\omega_0$ 附近；經有效 ISF 的 $c_2$（二次諧波）與其 DC 分量 $c_0$ 折回 close-in，
形成 $1/f^3$／$1/f^2$ 裙帶。所以「tail 雜訊的麻煩」主要寫在 ISF 的 $c_0$ 與 $c_2$ 上。

**三個對策（各配一條 ISF 量）：**

| 對策 | 為什麼有效（ISF 量） |
|---|---|
| **tail filter（在 tail 加 $2\omega_0$ 陷波/大電容濾波）** | 直接在頻域擋掉 $2\omega_0$ 附近的 tail 噪→等效降低被 $c_2$ 折回的能量，壓 close-in $1/f^2$。 |
| **波形對稱化（平衡上下半週、降 rise/fall 不對稱）** | 壓有效 ISF 的 $c_0$；$1/f^3$ corner $\propto c_0^2$（Eq.(24)），$c_0\downarrow$ 直接把 flicker 上轉的 corner 推離載波。 |
| **加大 tank swing / 提高 $q_{max}$** | $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$；$q_{max}\uparrow$ 把所有源（含 tail）的貢獻一起壓低（claim C3）。 |

（補充第四手段：用 noise 較低、$1/f$ corner 較低的 device 當 tail，或用電阻退化降 tail $g_m$ 噪——
等效降低注入到 $c_0,c_2$ 的 $\overline{i_n^2}$。）

**結果**：tail 雜訊靠「**tail filter 擋 $2\omega_0$**」「**對稱化壓 $c_0$**」「**加大 $q_{max}$**」三管齊下；
量化旋鈕分別是 $c_2$（折回能量）、$c_0$（$1/f^3$ corner $\propto c_0^2$）、$q_{max}$（$\mathcal{L}\propto1/q_{max}^2$）。

**Python 驗證（量化「對稱化壓 $c_0$」對 corner 的效果）：**

```python
import numpy as np
# 用 Eq.(24) 量化對稱化壓 c0 的好處（f1f=2 MHz, Grms=0.9 toy 值）
def f3_corner(c0, Grms=0.9, f1f=2e6): return f1f*c0**2/(2*Grms**2)
print("c0=0.3 ->", round(f3_corner(0.3)/1e3,1), "kHz ; c0=0.05 ->",
      round(f3_corner(0.05)/1e3,2), "kHz")
# -> c0=0.3 -> 111.1 kHz ; c0=0.05 -> 3.09 kHz  (對稱化把 corner 壓 ~36x)
```

</details>

<details>
<summary><strong>習題 8 解答</strong>（jitter 預算分配到 PLL 頻段）</summary>

**設計反推策略。** RJ 各源不相關 → **方差（不是 rms）相加**：

$$
\sigma_{t,\text{tot}}^2=\sigma_{t,\text{ref}}^2+\sigma_{t,\text{vco}}^2\quad\Longrightarrow\quad\sigma_{t,\text{vco}}=\sqrt{\sigma_{t,\text{tot}}^2-\sigma_{t,\text{ref}}^2}.
$$

**逐步代入（帶單位）。**

$$
\sigma_{t,\text{vco}}=\sqrt{(300\ \text{fs})^2-(180\ \text{fs})^2}=\sqrt{90000-32400}\ \text{fs}=\sqrt{57600}\ \text{fs}=240\ \text{fs}.
$$

**對應相位變異**（用 $\sigma_\phi=2\pi f_0\,\sigma_t$，規範公式 19 反向）：

$$
\sigma_{\phi,\text{vco}}=2\pi f_0\,\sigma_{t,\text{vco}}=2\pi\times10^{10}\times240\times10^{-15}=1.508\times10^{-2}\ \text{rad},
$$

$$
\sigma_{\phi,\text{vco}}^2=(1.508\times10^{-2})^2=2.274\times10^{-4}\ \text{rad}^2.
$$

**結果**：VCO 預算 $\sigma_{t,\text{vco}}=240$ fs；對應 $\sigma_{\phi,\text{vco}}^2\approx2.27\times10^{-4}$ rad²。

**手感**：因為**方差相加**，180 fs + 240 fs（rms）合起來是 300 fs（不是 420 fs）——RJ 預算
要用平方和分配。這 240 fs 就是 PLL out-of-band VCO 段允許的積分 jitter，回頭定 loop BW
與 VCO 規格（連習題 4 的最佳 BW、[pll_noise_budget](/06_design_insights/pll_noise_budget)）。

**Dimension check**：$\sqrt{\text{fs}^2-\text{fs}^2}=\text{fs}$ ✓；$2\pi f_0\,\sigma_t$ 為 $\text{rad/s}\cdot\text{s}=\text{rad}$ ✓。

```python
import numpy as np
sigma_tot, sigma_ref, f0 = 300e-15, 180e-15, 10e9
sigma_vco = np.sqrt(sigma_tot**2 - sigma_ref**2)
sigma_phi = 2*np.pi*f0*sigma_vco
print(sigma_vco*1e15, "fs ;", sigma_phi**2, "rad^2")   # -> 240.0 fs ; 2.27e-4 rad^2
```

</details>

---

## 重點回顧

- **$q_{max}$/$\Gamma_{rms}$ 反推**：$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$；每降 6 dB 要 $q_{max}\times2$ 或 $\Gamma_{rms}\div2$（習題 1）。
- **對稱性**：$1/f^3$ corner $\propto c_0^2$，壓 $c_0$ 最有效（習題 2、7）。
- **ring vs LC**：$\Gamma_{rms}\propto N^{-3/4}$；LC 在 $\Gamma_{rms}$（小/分散）與 $q_{max}$（高 Q 大擺幅）兩頭佔優（習題 3）。
- **PLL 最佳 BW**：ref 低通、VCO 高通；$f_n^\*$ 在兩曲線交點，存在最小積分 jitter（習題 4）。
- **$\sigma_t\to$BER**：bathtub $Q$ 函數；$10^{-12}$ 要 $UI/2\ge7.03\sigma_t$、$10^{-15}$ 要 $\ge7.94\sigma_t$（習題 5、6）。
- **tail noise**：tail filter（擋 $2\omega_0$）／對稱化（壓 $c_0$）／加大 $q_{max}$ 三管齊下（習題 7）。
- **jitter 預算**：RJ 各源**方差相加**，$\sigma_{t,\text{vco}}=\sqrt{\sigma_{tot}^2-\sigma_{ref}^2}$（習題 8）。
- 全部 Python 驗證引用 `simulations/common/`（`pll_utils`、`serdes_utils`、`isf_utils`）。

## 延伸閱讀

- 加大擺幅降噪：[tank_swing](/06_design_insights/tank_swing)
- 波形斜率與 ISF：[waveform_slope](/06_design_insights/waveform_slope)
- 對稱性壓 $1/f^3$：[symmetry](/06_design_insights/symmetry)
- ring vs LC：[lc_vs_ring](/06_design_insights/lc_vs_ring)
- PLL 雜訊預算與最佳 BW：[pll_noise_budget](/06_design_insights/pll_noise_budget)
- 真實拓樸與 tail noise：[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)
- SerDes 連結：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- tuning/supply pushing 的 phase noise：[varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)
- tank $Q$ 與能量恢復：[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)

## 其他習題

把同一套 ISF 機器用在不同層次的題目——基礎換算、核心 ISF→PN 推導，與本頁的設計反推互補：

- 基礎章習題（單位換算、PSD/jitter、隨機程序）：[02 基礎章習題](/02_foundations/exercises)
- 核心理論章習題（ISF 定義、卷積、白噪→$1/f^2$、flicker→$1/f^3$、傅立葉/Parseval）：[03 核心理論章習題](/03_isf_core_theory/exercises)
