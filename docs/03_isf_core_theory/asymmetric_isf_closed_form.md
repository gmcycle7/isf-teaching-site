---
title: 非對稱三角 ISF 的閉式解（[P2] 附錄 B）
description: 逐步推導 [P2] Appendix B Eq.(52)–(57)：rise/fall 不對稱的三角 ISF 之 Γrms、Γdc 與 1/f³ corner 閉式；A=1 精確退化為 Eq.(16)、corner ∝ (1−A)²/(1−A+A²) 且 ∝ 1/N；含數值例、慣例 2 倍旗標與 lab_33 模擬驗證。
---

import NumericQuiz from "@site/src/components/NumericQuiz";
import AsymmetricIsfExplorer from "@site/src/components/AsymmetricIsfExplorer";

# 非對稱三角 ISF 的閉式解（[P2] 附錄 B）

> **先備**：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（$c_0$ 與 Parseval）、[rms_isf](/03_isf_core_theory/rms_isf)（$\Gamma_{rms}$ 的定義與角色）、[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)（$c_0$ 為何是 flicker 上轉的唯一閘門）｜**接下來**：[symmetry](/06_design_insights/symmetry)（把本頁閉式變成設計旋鈕）、[lab_32](/04_simulation_labs/lab_32_mos_level1_ring)（方程級 ring 的 ISF 萃取，看三角近似何時失真）

[symmetry](/06_design_insights/symmetry) 頁講了「rise/fall 對稱 → $c_0\to0$ → 1/f³ 被壓下去」
這條定性法則，但那頁的數值例把 $c_0$ 當**假設值**代入。本頁把缺的那塊補上：
**給定 ring oscillator 的級數 $N$ 與波形不對稱程度，$\Gamma_{rms}$、$c_0$、1/f³ corner
到底是多少？** [P2] Appendix B（p.803）用一個非對稱三角 ISF 模型給出了全套閉式解
Eq.(52)–(57)——這是全站少數「從拓樸參數直接算出 $c_0$」的地方，值得逐步走一遍。

> **物理直覺（先講結論）**：ring 的 ISF 集中在兩個 transition（轉態）處：上升緣一個**正葉**、
> 下降緣一個**負葉**，葉的高度反比於該緣的斜率（緣越陡、越不敏感）。若 rise 比 fall 陡
> （$A=f'_{rise}/f'_{fall}>1$），正葉又矮又窄、負葉又高又寬，兩葉面積不再相消——
> 差出來的那塊淨面積就是 $\Gamma_{dc}$（即 $c_0/2$），它把 device 的 1/f noise 上轉成
> close-in 的 1/f³。閉式解把這個幾何圖像變成三個公式：$\Gamma_{rms}^2$（Eq.55）、
> $\Gamma_{dc}$（Eq.56）、corner（Eq.57），而且 corner 只由**兩個無因次數** $A$ 與 $N$ 決定。

## 第 0 步：模型——[P2] Fig. 18 的非對稱三角 ISF

[P2] Fig. 18, p.803（本次由 PDF 渲染頁核實）：*"Approximate waveform and the ISF for
asymmetric rising and falling edges."* 圖中 $\Gamma(x)$ 對 $x$（一個週期 $0$ 到 $2\pi$）畫出兩個三角葉：

| 葉 | 高度（峰值） | 底寬 | 對應 |
|---|---|---|---|
| 正葉 | $1/f'_{rise}$ | $2/f'_{rise}$ | 上升緣（rising edge） |
| 負葉 | $1/f'_{fall}$（深度） | $2/f'_{fall}$ | 下降緣（falling edge） |

其中 $f'_{rise}$、$f'_{fall}$ 是**正規化波形**（振幅正規化到 1 的 $f(x)$，$x=\omega_0\tau$）
在上升／下降緣的**最大斜率**（原文：*"where $f'_{rise}$ and $f'_{fall}$ are the maximum slope
during the rising and falling edge, respectively"*，p.803）。

- **單位檢查**：$x=\omega_0\tau$ 是 $[\text{rad/s}]\cdot[\text{s}]=[\text{rad}]$，本站把 rad
  視為無因次純數；$f(x)$ 無因次，故 $f'=df/dx$ 無因次、$1/f'$ 也無因次——與 $\Gamma$ 無因次一致 ✓。
- **為什麼高度是 $1/f'$**：ISF 峰值反比於波形斜率——緣越陡，同樣的電荷擾動造成的相位偏移越小
  （見 [waveform_slope](/06_design_insights/waveform_slope)；這是 [P2] 主文三角近似的出發點）。
- **關鍵幾何觀察（斜率 = 1）**：每個葉「高度 $=1/f'$、底寬 $=2/f'$」，所以**半寬＝高度**，
  三角形兩腰在 $x$ 座標上的斜率恰為 $\pm1$。這不是巧合：敏感峰值 $\propto 1/f'$、
  敏感窗（transition 佔的相位寬）也 $\propto 1/f'$，兩者同源，比值固定為 1。
  這個「單位斜率」讓下面的積分變得非常乾淨。
- 葉在 $x$ 軸上的**位置**（正葉在哪、負葉在哪）不影響 $\Gamma_{rms}$ 與 $\Gamma_{dc}$
  （只影響諧波相位 $\theta_n$），所以推導時可以把葉放在任何不重疊的位置。

## 第 1 步：分段積分算 $\Gamma_{rms}^2$ —— Eq.(52)

從 $\Gamma_{rms}$ 的定義出發（[P1] Eq.(20) 的形式，見 [rms_isf](/03_isf_core_theory/rms_isf)），
對兩個三角葉分段積分。因為兩腰斜率 $=\pm1$，在每個半腰上可以直接用「ISF 的值」當積分變數
（$\Gamma$ 從 0 線性走到峰值 $1/f'$，$d\Gamma = \pm\,dx$），一個葉＝兩個半腰＝
$2\int_0^{1/f'}x^2\,dx$。原文逐字（[P2] Eq.(52), p.803，本次渲染核實）：

$$
\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\Gamma^2(x)\,dx
=\frac{1}{\pi}\!\left[\int_0^{1/f'_{rise}}x^2\,dx+\int_0^{1/f'_{fall}}x^2\,dx\right]
=\frac{1}{3\pi}\left(\frac{1}{f'_{rise}}\right)^{\!3}(1+A^3)
$$

逐步展開中間那步到最後一步：

$$
\begin{aligned}
\frac{1}{2\pi}\!\left[2\!\int_0^{1/f'_{rise}}\!x^2dx+2\!\int_0^{1/f'_{fall}}\!x^2dx\right]
&=\frac{1}{\pi}\!\left[\frac{x^3}{3}\Big\vert_0^{1/f'_{rise}}+\frac{x^3}{3}\Big\vert_0^{1/f'_{fall}}\right] \\[4pt]
&=\frac{1}{3\pi}\!\left[\left(\frac{1}{f'_{rise}}\right)^{\!3}+\left(\frac{1}{f'_{fall}}\right)^{\!3}\right] \\[4pt]
&=\frac{1}{3\pi}\left(\frac{1}{f'_{rise}}\right)^{\!3}\left(1+A^3\right).
\end{aligned}
$$

- 第 1 行：每葉兩個半腰，正負號在平方後消失，所以正、負葉各貢獻 $2\int_0^{h}x^2dx$（$h$=峰高）。
- 第 3 行：提出 $(1/f'_{rise})^3$，用到 $\dfrac{1}{f'_{fall}}=\dfrac{A}{f'_{rise}}$，
  其中 $A$ 是**不對稱比**（[P2] Eq.(53), p.803，逐字）：

$$
A\equiv\frac{f'_{rise}}{f'_{fall}}
$$

- **dimension check**：$[x^2\,dx]=\text{rad}^3$（無因次），除以 $\pi$（rad）→ 無因次；
  $\Gamma_{rms}^2$ 無因次 ✓。
- **健全性檢查**：$A=1$（對稱）時 $1+A^3=2$，兩葉貢獻相等；$A>1$（rise 陡）時
  $1/f'_{fall}$ 大、負葉主導 $\Gamma_{rms}^2$——**慢的那個緣決定 rms 敏感度**。

## 第 2 步：把 $f'_{rise}$ 換成電路參數——週期約束 Eq.(54)

Eq.(52) 還含著波形斜率。要變成「設計者手上的參數」（級數 $N$），用 ring 的週期約束。
[P2] Eq.(14), p.794 定義**正規化級延遲** $\hat t_D=\eta/f'_{max}$（$\eta\approx1$ 是比例常數：
一級的延遲約等於「transition 斜率的倒數」乘上 $\eta$）。在單端反相 ring 裡，一個完整週期
內訊號繞環**兩圈**（每個節點升一次、降一次），共 $2N$ 個級延遲——其中 $N$ 個是上升緣延遲
$\eta/f'_{rise}$、$N$ 個是下降緣延遲 $\eta/f'_{fall}$。把一個週期的相位長度 $2\pi$ 寫成
這些延遲之和（[P2] Eq.(54), p.803，逐字）：

$$
2\pi=\eta N\!\left(\frac{1}{f'_{rise}}+\frac{1}{f'_{fall}}\right)=\frac{\eta N}{f'_{rise}}(1+A)
$$

解出正葉峰高：

$$
\frac{1}{f'_{rise}}=\frac{2\pi}{\eta N(1+A)},\qquad
\frac{1}{f'_{fall}}=\frac{2\pi A}{\eta N(1+A)}.
$$

- **dimension check**：兩邊都是 rad（無因次）✓；$\eta,N,A$ 皆無因次。
- **健全性檢查**：$A=1$ 時回到對稱情形 $2\pi=2N\hat t_D$（正是 [P2] Eq.(15) $f_0=1/(2N\tau_D)$
  的相位域寫法）；$N$ 越大或 $A+1$ 越大，正葉越矮——一切幾何都被 $2\pi$ 的預算「攤薄」。

## 第 3 步：合併成 $\Gamma_{rms}^2(N,A)$ —— Eq.(55)，並驗證 $A=1$ 退化

把第 2 步的 $1/f'_{rise}$ 代入 Eq.(52)：

$$
\Gamma_{rms}^2=\frac{1}{3\pi}\cdot\frac{(2\pi)^3}{\eta^3N^3(1+A)^3}\,(1+A^3)
=\frac{8\pi^2}{3\eta^3N^3}\cdot\frac{1+A^3}{(1+A)^3}
$$

整理成原文形式（[P2] Eq.(55), p.803，逐字）：

$$
\Gamma_{rms}^2=\frac{2\pi^2}{3\eta^3}\,\frac{1}{N^3}\left[4\,\frac{1+A^3}{(1+A)^3}\right]
$$

- **$A=1$ 檢查（必做）**：括號 $=4\cdot\dfrac{2}{8}=1$，故
  $\Gamma_{rms}^2=\dfrac{2\pi^2}{3\eta^3}\dfrac{1}{N^3}$——**精確**退化為 [P2] Eq.(16), p.794
  的 v7 讀法 $\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\cdot N^{-1.5}$（根號只蓋常數）。
  數值：$N=5$、$\eta=1$ 時兩式同給 $\Gamma_{rms}=0.229429$（lab_33 印出）。
  這也是 Eq.(16) N-scaling 的第三重驗證（見 [paper_002 深讀](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)）。
- **不對稱的代價很溫和**：括號在 $A=1.5$ 時 $=1.12$、$A=3$ 時 $=1.75$——
  $\Gamma_{rms}$ 只多 6%／32%。**不對稱對 1/f²（白噪）區的傷害不大**；它真正的殺傷力在下面的 $c_0$。
- **對 $A\to1/A$ 不變**：$\dfrac{1+A^3}{(1+A)^3}$ 把 $A$ 換成 $1/A$ 後不變（上下同乘 $A^3$）。
  「rise 陡 fall 慢」與「fall 陡 rise 慢」的 rms 敏感度相同——方向不重要，不對稱程度才重要。

## 第 4 步：DC 值 $\Gamma_{dc}$ —— Eq.(56)，接上 $c_0$

$\Gamma_{dc}$ 是 ISF 在一個週期上的平均。三角形面積 $=\tfrac12\cdot$底$\cdot$高：
正葉面積 $\tfrac12\cdot\dfrac{2}{f'_{rise}}\cdot\dfrac{1}{f'_{rise}}=\dfrac{1}{f'^2_{rise}}$，
負葉同理 $\dfrac{1}{f'^2_{fall}}$（帶負號）：

$$
\Gamma_{dc}=\frac{1}{2\pi}\!\left[\frac{1}{f'^2_{rise}}-\frac{1}{f'^2_{fall}}\right]
=\frac{1}{2\pi}\,\frac{1-A^2}{f'^2_{rise}}
=\frac{1}{2\pi}\cdot\frac{4\pi^2}{\eta^2N^2(1+A)^2}\,(1-A^2)
$$

用 $1-A^2=(1-A)(1+A)$ 約掉一個 $(1+A)$，得原文形式（[P2] Eq.(56), p.803，逐字）：

$$
\Gamma_{dc}=\frac{2\pi}{\eta^2}\,\frac{1}{N^2}\left(\frac{1-A}{1+A}\right)
$$

- **接上傅立葉係數**：ISF 級數（[P1] Eq.(12)）的 DC **值**是 $c_0/2$，所以
  $c_0=2\,\Gamma_{dc}$——這就是餵給 [P1] Eq.(24) corner 公式的那個 $c_0$
  （符號陷阱同 [symmetry](/06_design_insights/symmetry) 頁：$c_0$ 是係數、$c_0/2$ 才是 DC 值）。
- **符號**：$A>1$（rise 陡）→ $\Gamma_{dc}<0$（負葉面積大）；$A<1$ 反號。上轉只看 $c_0^2$，符號不進 corner。
- **scaling 重點**：$\Gamma_{dc}\propto N^{-2}$ 掉得比 $\Gamma_{rms}\propto N^{-1.5}$ **快**
  （葉面積 $\propto$ 峰高平方 $\propto N^{-2}$，rms 平方 $\propto$ 峰高立方 $\propto N^{-3}$）。
  這個「快半格」正是下一步 corner $\propto 1/N$ 的來源。
- **dimension check**：面積 $[\Gamma\cdot dx]=$ rad（無因次），除以 $2\pi$ → 無因次 ✓。

## 第 5 步：1/f³ corner —— Eq.(57)（含 2 倍慣例旗標）

[P2] 主文給的 corner 關係（[P2] Eq.(7), p.792，本次渲染核實，逐字）：

$$
f_{1/f^3}=f_{1/f}\cdot\frac{\Gamma_{dc}^2}{\Gamma_{rms}^2}
$$

把 Eq.(55)、(56) 代入，用 $1+A^3=(1+A)(1-A+A^2)$ 因式分解：

$$
\frac{\Gamma_{dc}^2}{\Gamma_{rms}^2}
=\frac{\dfrac{4\pi^2}{\eta^4N^4}\dfrac{(1-A)^2}{(1+A)^2}}
      {\dfrac{2\pi^2}{3\eta^3N^3}\cdot\dfrac{4(1+A^3)}{(1+A)^3}}
=\frac{3}{2\eta N}\cdot\frac{(1-A)^2(1+A)}{1+A^3}
=\frac{3}{2\eta N}\cdot\frac{(1-A)^2}{1-A+A^2}
$$

得原文結果（[P2] Eq.(57), p.803，逐字）：

$$
f_{1/f^3}=f_{1/f}\cdot\frac{3}{2\eta N}\cdot\frac{(1-A)^2}{(1-A+A^2)}
$$

> **慣例 2 倍旗標（每次出現 2 或 4 都要標）**：把 $c_0=2\Gamma_{dc}$ 代進 [P1] Eq.(24)
> $\Delta\omega_{1/f^3}=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$ 會得到
> $2\,\omega_{1/f}\Gamma_{dc}^2/\Gamma_{rms}^2$——**恰是 [P2] Eq.(7)/(57) 的 2 倍**。
> 這與 white_noise 頁講的 SSB $/4$ vs 時域 $/2$ 是同一族記帳問題（DC 通道在
> $\sum c_n^2$ 求和裡怎麼計權；[P2] Eq.(6), p.792 本身就用 $/(8\pi^2f^2)$ = 時域 $/2$ 慣例）。
> 兩篇論文內部各自自洽；**scaling（$\propto(1-A)^2/(1-A+A^2)$、$\propto1/N$）與任何比值
> 都不受影響**。本站數值：報 [P2] Eq.(57) 值為主，並附 [P1] Eq.(24) 慣例值（=2×）。

**互動探索**：下面的小工具讓你直接拉 $N$、$A$、$\eta$、$f_{1/f}$，即時看 Eq.(55)–(57)
算出的 $\Gamma_{rms}$、$c_0$、corner，以及左邊 Fig.18 三角葉形狀、右邊 corner 對 $A$
的 V 形谷（本頁 Fig.17 式量測碗底的解析版）現在的位置：

<AsymmetricIsfExplorer />

Eq.(57) 有三個結構性質，每個都是設計訊息：

1. **$A\to1$ 時 corner 二次趨零**：分子 $(1-A)^2$——對稱點附近 corner 對不對稱度是
   **二次不敏感**，但一旦偏離，惡化也是二次加速（lab_33：$A=1.01$ 時 corner$/f_{1/f}$
   只有 $2.97\times10^{-5}$，$A=1.10$ 已到 $2.70\times10^{-3}$，差近 100 倍）。
   這就是 [P2] Fig. 17, p.802「phase noise vs 對稱控制電壓」在對稱點出現碗底的解析版。
2. **對 $A\to1/A$ 不變**：$(1-A)^2/(1-A+A^2)$ 把 $A$ 換 $1/A$ 後不變（上下同乘 $A^2$；
   lab_33 驗證 corner$(A{=}2)=$ corner$(A{=}0.5)=1.000000\times10^{-1}\,f_{1/f}$）。
   V 形谷在 log-$A$ 軸上左右對稱——「哪個緣比較陡」無所謂。
3. **corner $\propto 1/N$**：固定 $A$ 下，級數越多 corner 越低。原文逐字（p.803，App. B 結尾）：
   *"As can be seen for a constant rise-to-fall ratio, the 1/f³ corner decreases inversely
   with the number of stages; therefore, ring oscillators with a smaller number of stages
   will have a larger 1/f³ noise corner. As a special case, if the rise and fall time are
   symmetric, A = 1, and the 1/f³ corner approaches zero."*
   （中譯：固定 rise/fall 比之下，1/f³ corner 與級數成反比；所以**級數少的 ring 有較高的
   1/f³ corner**。特例：rise/fall 對稱時 $A=1$，1/f³ corner 趨近於零。）

> **與「$N$ 無關」結論的和解**：[P2] 主文 Eq.(23) 說固定 $f_0$、功率下**白噪（1/f²）區**的
> phase noise 近似與 $N$ 無關（見 [paper_002 深讀](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)、
> [lc_vs_ring](/06_design_insights/lc_vs_ring)）。兩者不矛盾：$N$ 不動 1/f² 的**高度**，
> 但把 1/f³ 的**轉折點**往低頻推（$\propto1/N$）。設計訊息：若你的痛點是 close-in flicker
> （例如 PLL loop BW 不夠寬、洗不掉 VCO 的 1/f³），**多級數是有效槓桿**；
> 若痛點是白噪區 jitter，加級數沒有用。這是本頁新增、[P2] 原文自己點名的設計結論。

## 數值例子（canonical：$N=5$、$\eta=1$、$f_{1/f}=1$ MHz）

> **例 1（$A=1.5$：中度不對稱——rise 比 fall 陡 1.5 倍）**

逐步代入（全部無因次，corner 才帶 Hz）：

$$
\begin{aligned}
\Gamma_{rms}^2&=\frac{2\pi^2}{3}\cdot\frac{1}{125}\cdot\left[4\cdot\frac{1+3.375}{(2.5)^3}\right]
=6.5797\times0.008\times1.12=0.05895
\;\Rightarrow\;\Gamma_{rms}=0.2428 \\[4pt]
\Gamma_{dc}&=\frac{2\pi}{25}\cdot\frac{1-1.5}{1+1.5}=0.25133\times(-0.2)=-0.05027
\;\Rightarrow\;c_0=2\Gamma_{dc}=-0.1005 \\[4pt]
f_{1/f^3}&=1\ \text{MHz}\times\frac{3}{2\times1\times5}\times\frac{(-0.5)^2}{1-1.5+2.25}
=1\ \text{MHz}\times0.3\times\frac{0.25}{1.75}=42.9\ \text{kHz}.
\end{aligned}
$$

- **結果**：$\Gamma_{rms}=0.2428$、$c_0=-0.1005$、corner $=42.86$ kHz（[P2] Eq.(57) 慣例）；
  [P1] Eq.(24) 慣例則為 $85.71$ kHz（$=2\times$，旗標同上）。
- **Dimension check**：$[\text{Hz}]\times[\text{無因次}]\times[\text{無因次}]=[\text{Hz}]$ ✓。
- **手感**：$N=5$ ring 的 $\Gamma_{rms}\approx0.24$，比全站代表值 $\Gamma_{rms}=0.5$ 低約一半。
  套 canonical 例 B（$q_{max}=1$ pC、$S_i=10^{-24}$ A²/Hz、$f_0=5$ GHz、$\Delta f=1$ MHz）：
  $\mathcal{L}$ 比 $-148.0$ dBc/Hz 再低 $20\log_{10}(0.2428/0.5)=-6.3$ dB → 約 $-154.3$ dBc/Hz
  （SSB $/4$ 慣例；時域 $/2$ 慣例整條 $+3$ dB → 約 $-151.3$ dBc/Hz）。
- **一行 Python 驗證**（閉式直算；完整驗證見 lab_33）：

```python
import numpy as np
N, A, eta, f1f = 5, 1.5, 1.0, 1e6
grms2 = (2*np.pi**2/(3*eta**3))/N**3 * 4*(1+A**3)/(1+A)**3
gdc = (2*np.pi/eta**2)/N**2 * (1-A)/(1+A)
print(round(np.sqrt(grms2), 4), round(2*gdc, 4))
# -> 0.2428 -0.1005（Γrms 與 c0=2Γdc；lab_33 同值）
print(round(f1f*3/(2*eta*N)*(1-A)**2/(1-A+A**2)/1e3, 2), "kHz")
# -> 42.86 kHz（[P2] Eq.(57)；[P1] Eq.(24) 慣例 = 85.71 kHz）
```

> **例 2（$A=3$：重度不對稱——rise 比 fall 陡 3 倍）**

$$
\begin{aligned}
\Gamma_{rms}^2&=6.5797\times0.008\times\left[4\cdot\frac{28}{64}\right]
=6.5797\times0.008\times1.75=0.09212\;\Rightarrow\;\Gamma_{rms}=0.3035 \\[4pt]
c_0&=2\times\frac{2\pi}{25}\times\frac{1-3}{1+3}=-0.2513 \\[4pt]
f_{1/f^3}&=1\ \text{MHz}\times0.3\times\frac{4}{7}=171.4\ \text{kHz}
\qquad(\text{[P1] Eq.(24) 慣例：}342.9\ \text{kHz}).
\end{aligned}
$$

- **對照例 1**：$A$ 從 1.5 惡化到 3，$\Gamma_{rms}$ 只從 0.2428 升到 0.3035（+25%，
  1/f² 區小傷），但 $c_0$ 從 $-0.1005$ 到 $-0.2513$（$\times2.5$）、corner 從 42.86 kHz
  跳到 171.43 kHz（**$\times4.0$，lab_33 印出**；比值與 2/4 慣例無關，因為 2 倍同乘同除）。
  1/f³ 裙邊的高度 $\propto c_0^2$ 則抬高 $10\log_{10}(2.5^2)=+8.0$ dB。
- **與 [symmetry](/06_design_insights/symmetry) 頁的假設例對照**：那頁的示意值 $c_0=0.4$、
  $\Gamma_{rms}=0.5$ 給 corner 320 kHz（[P1] Eq.(24) 慣例）；本頁從 $(N,A)$ 直接算出
  同一個量，不再需要假設 $c_0$。

<NumericQuiz
  prompt="同一顆 N = 5、η = 1 的 ring，device 1/f corner f₁/f = 1 MHz。波形不對稱比從 A = 1.5 惡化到 A = 3，1/f³ corner 變成原來的幾倍？（提示：這個比值與 [P1]/[P2] 的 2 倍慣例無關）"
  answer={4}
  tol={0.02}
  unit="倍"
  hint="Eq.(57) 裡只有 (1−A)²/(1−A+A²) 隨 A 變：A=1.5 給 0.25/1.75 = 1/7，A=3 給 4/7。"
  solutionNote="corner 從 42.86 kHz → 171.43 kHz，比值 = (4/7)/(1/7) = 4.0（lab_33 印出）。[P1] Eq.(24) 慣例下兩數各 ×2（85.71 → 342.86 kHz），比值仍是 4——慣例因子在比值中相消。"
/>

## 模擬驗證：lab_33（閉式 vs 數值積分）

`simulations/lab_33_asymmetry_corner.py`（runtime 約 1.5 s）把 Fig. 18 的分段三角 $\Gamma(x)$
在 $(N,A)$ 網格上數值建出來（$4\times10^5$ 點/週期），對 Eq.(55)/(56) 做三重驗證：
數值 trapezoid 積分、`compute_fourier_coefficients` 的 $a_0$（$=c_0=2\Gamma_{dc}$）、
與純代數（Eq.(52)+(54) 合併 = Eq.(55)）。

| 參數 | 值 | 單位 |
|---|---|---|
| $N$ 網格 | 3, 4, 5, 7, 9, 12, 15 | — |
| $A$ 網格 | 1.0, 1.25, 1.5, 2.0, 3.0, 4.0 | — |
| $\eta$ | 1.0 | — |
| $f_{1/f}$ | 1 | MHz |
| $\theta$ 取樣 | 400001 點 / $2\pi$ | — |

核心驗證程式（節錄；`gamma_fig18` 用兩個單位斜率三角葉組出 $\Gamma$）：

```python
g = gamma_fig18(theta, n_st, a_r)            # Fig.18 分段三角（單位斜率）
g2_num  = gamma_rms(theta, g)**2             # 數值 (1/2π)∫Γ²dx
gdc_num = np.trapezoid(g, theta) / (2*np.pi) # 數值 (1/2π)∫Γdx
a0, *_  = compute_fourier_coefficients(theta, g, 2)   # a0 = c0
# 42 組 (N,A) 全部對照 Eq.(55)/(56)：
# -> 1.17e-09（max 相對誤差，Γrms²，遠低於 0.5% 門檻）
# -> 1.60e-09（max 相對誤差，Γdc 與 c0=2Γdc 兩項同值）
```

![非對稱三角 ISF：Fig.18 幾何、corner 對 A 的 V 形谷、corner 對 N 的 1/N 律](/figures/asymmetry_corner.png)

**怎麼讀這張圖**：

- **(a)** $N=5$ 的 $\Gamma(x)$，$A=1/1.5/3$ 三條。$A$ 越大正葉越矮窄、負葉越高寬
  （總相位預算 $2\pi/(\eta N)$ 固定，由 $1:A$ 分帳）；虛線是各自的 $\Gamma_{dc}$（Eq.56）——
  不對稱把整條 ISF 的平均值拉離 0，那個偏移就是 flicker 上轉的閘門。
- **(b)** Eq.(57) 的 corner 對 $A$（log 軸）：對稱點 $A=1$ 是 V 形谷底（corner → 0），
  左右對 $A\to1/A$ 鏡像對稱；$N$ 越大整條曲線越低。這就是 [P2] Fig. 17 量測碗底的解析版。
  標註點：$N=5$ 時 $A=1.5\to42.9$ kHz、$A=3\to171.4$ kHz。
- **(c)** 固定 $A$ 下 corner 對 $N$（log-log）：斜率 $-1$（$\propto1/N$ 參考虛線重合；
  lab_33 印出 $A=1.5$ 時 $N=3/5/9/15\to71.43/42.86/23.81/14.29$ kHz，$N{=}3$ 與 $N{=}15$
  比值 5.0 = 15/3 精確）。**級數少的 ring，flicker corner 高**——挑 $N$ 時要把這條放進取捨。

## 適用與失效條件

| 假設 | 成立時 | 失效時 |
|---|---|---|
| 三角 ISF（線性斜坡 transition、峰 $=1/f'$、寬 $=2/f'$、單位斜率） | $N$ 大、edge 佔週期比例小、波形接近梯形 | $N$ 小或波形近正弦：[lab_32](/04_simulation_labs/lab_32_mos_level1_ring) 的方程級 $N=3$ ring 量到 $\Gamma_{rms}=0.9303$，而 Eq.(16) 給 0.4937——差近 2 倍；閉式此時只當 scaling 指引 |
| 兩葉不重疊 | 葉總寬 $4\pi/(\eta N)\le2\pi$，即 $N\ge2/\eta$ | $N$ 太小（近似本來就已失效） |
| $\eta\approx1$（[P2] Eq.(14) 的級延遲比例常數） | 典型 inverter 級 | $\eta$ 偏離 1 時公式仍對，但要用實際 $\eta$（$\Gamma_{rms}^2\propto\eta^{-3}$、corner $\propto\eta^{-1}$） |
| flicker 只經 $\Gamma_{dc}$（$c_0$）上轉 | 裸 ISF 的不對稱主導 | cyclostationary NMF $\alpha(t)$ 本身不對稱時，要看 **effective ISF** 的 $c_0$（見 [effective_isf](/03_isf_core_theory/effective_isf)、[device_noise_mapping](/06_design_insights/device_noise_mapping)）——$A=1$ 也可能殘留上轉 |
| corner 記帳慣例 | [P2] Eq.(7)/(57) 自洽 | 與 [P1] Eq.(24)（$c_0=2\Gamma_{dc}$ 代入）差 2 倍；引用數字時必須標明用哪個慣例 |
| $A=1\Rightarrow$ corner $\to0$ | 模型內精確 | 真實電路由 duty cycle、偶次諧波、$\alpha(t)$、製程偏移決定殘餘 $c_0$，corner 不會真的到 0 |

## 與論文公式對應

| 本頁內容 | 論文出處 | 核實狀態 |
|---|---|---|
| 非對稱三角 ISF 幾何（兩葉高 $1/f'$、寬 $2/f'$） | [P2] Fig. 18, p.803 | ✓ 本次渲染 |
| $\Gamma_{rms}^2$ 分段積分 | [P2] Eq.(52), p.803 | ✓ 本次渲染 |
| 不對稱比 $A\equiv f'_{rise}/f'_{fall}$ | [P2] Eq.(53), p.803 | ✓ 本次渲染 |
| 週期約束 $2\pi=\eta N(1/f'_{rise}+1/f'_{fall})$ | [P2] Eq.(54), p.803 | ✓ 本次渲染 |
| $\Gamma_{rms}^2(N,A)$ 閉式 | [P2] Eq.(55), p.803 | ✓ 本次渲染 |
| $\Gamma_{dc}(N,A)$ 閉式 | [P2] Eq.(56), p.803 | ✓ 本次渲染 |
| corner 閉式 $\propto(1-A)^2/(1-A+A^2)$、$\propto1/N$ | [P2] Eq.(57), p.803 | ✓ 本次渲染 |
| corner 關係 $f_{1/f^3}=f_{1/f}\Gamma_{dc}^2/\Gamma_{rms}^2$ | [P2] Eq.(7), p.792 | ✓ 本次渲染 |
| 對稱特例（括號 $=1$） | [P2] Eq.(16), p.794 | ✓ 既有 v7 核實 |
| $c_0$ 版 corner（$=2\times$ Eq.(7)，慣例旗標） | [P1] Eq.(24), p.185 | ✓ 權威公式表 |
| 對稱點碗底的量測對照 | [P2] Fig. 17, p.802 | ✓ 既有核實 |

## 重點回顧

- [P2] App. B 把 ring 的 ISF 建成**兩個單位斜率的三角葉**（高 $1/f'$、寬 $2/f'$），
  分段積分即得 $\Gamma_{rms}^2=\frac{1}{3\pi}(1/f'_{rise})^3(1+A^3)$（Eq.52）。
- 週期約束 $2\pi=\eta N(1+A)/f'_{rise}$（Eq.54）把斜率換成 $(N,A)$，得
  $\Gamma_{rms}^2=\frac{2\pi^2}{3\eta^3N^3}[4(1+A^3)/(1+A)^3]$（Eq.55）；$A=1$ 時括號 $=1$，
  精確退化為 Eq.(16)。
- $\Gamma_{dc}=\frac{2\pi}{\eta^2N^2}\frac{1-A}{1+A}$（Eq.56），$c_0=2\Gamma_{dc}$；
  $\Gamma_{dc}\propto N^{-2}$ 掉得比 $\Gamma_{rms}$ 快 → corner $\propto1/N$。
- corner $=f_{1/f}\cdot\frac{3}{2\eta N}\cdot\frac{(1-A)^2}{1-A+A^2}$（Eq.57）：
  對稱點二次趨零、對 $A\to1/A$ 對稱、級數少 corner 高（[P2] 原句）。
- **慣例旗標**：[P1] Eq.(24)（代 $c_0=2\Gamma_{dc}$）$=2\times$ [P2] Eq.(7)/(57)；
  比值與 scaling 不受影響。
- 數值手感（$N=5$、$\eta=1$、$f_{1/f}=1$ MHz）：$A=1.5\to c_0=-0.1005$、corner 42.86 kHz；
  $A=3\to c_0=-0.2513$、corner 171.43 kHz（比值 4.0）。
- 模型失效警戒：$N$ 小、波形近正弦時三角近似大幅偏離（lab_32 實測差近 2 倍）；
  cyclostationary $\alpha$ 不對稱時要看 effective ISF 的 $c_0$。

## 延伸閱讀

- 設計面應用與 design knobs：[symmetry](/06_design_insights/symmetry)（本頁閉式的「使用手冊」）
- $c_0$ 為何是 flicker 的唯一閘門：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- $c_0,c_n$ 與 Parseval：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- $\Gamma_{rms}$ 進 phase noise 的地方：[rms_isf](/03_isf_core_theory/rms_isf)、[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（$/4$ vs $/2$ 慣例的完整說明）
- 三角近似何時失真：[lab_32](/04_simulation_labs/lab_32_mos_level1_ring)（方程級 ring 的 ISF 萃取）
- ring vs LC 拓樸取捨：[lc_vs_ring](/06_design_insights/lc_vs_ring)、[paper_002 深讀](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)
