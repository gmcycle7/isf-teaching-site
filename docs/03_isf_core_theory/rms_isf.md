---
title: rms ISF 與 Parseval 關係
description: 由 Parseval 推 Σcₙ²=(1/π)∫|Γ|²dx=2Γrms²；解釋 Γrms 如何決定 1/f² phase noise、DC factor 的慣例，以及 ring 的 Γrms∝N^(−3/2)。
---

# rms ISF 與 Parseval 關係

> **前置閱讀**：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（$\Gamma$ 的 $c_n$ 係數）、[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)（Parseval / 功率譜）、[convolution_derivation](/03_isf_core_theory/convolution_derivation)（相位積分式）。

上一頁 [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) 把 ISF 拆成一組
Fourier 係數 $c_0,c_1,c_2,\dots$，並指出**每個 $c_n$ 把 $n\omega_0$ 附近的 noise 折回 carrier**。
這頁要回答：

**當 device noise 是平坦白噪、各個 band 的貢獻都要加總時，能不能用「一個數」描述整支 ISF
對 phase noise 的貢獻？** 能——那個數就是 ISF 的 rms 值 $\Gamma_{rms}$，由 **Parseval 定理**
把它和係數平方和綁在一起（[P1] Eq.(20), p.185）：

$$
\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}|\Gamma(x)|^2dx=2\,\Gamma_{rms}^2
$$

> **物理直覺（先講結論）**：白噪在每個 $n\omega_0$ band 都一樣強，所以「總折回功率」正比於
> **所有係數的平方和** $\sum c_n^2$。Parseval 告訴我們，這個平方和等於 ISF 在一個週期上的
> **均方（mean-square）的兩倍**，也就是 $2\Gamma_{rms}^2$。於是雜亂的「逐 band 加總」被收成
> 一個乾淨的形狀指標 $\Gamma_{rms}$——它（連同 $q_{max}$）就決定了 $1/f^2$ phase noise 的高低。
> 直覺上：**ISF 整體越「平靜」（rms 越小），振盪器對白噪越不敏感。**

## 第 1 步：Parseval 定理——時域能量 = 頻域係數平方和

Parseval（帕塞瓦爾）定理說：一個週期函數在「一個週期上的均方」等於它各 Fourier 分量的「均方之和」。
對標準 cos/sin 展開 $\Gamma(x)=\dfrac{a_0}{2}+\sum_{n\ge1}[a_n\cos nx+b_n\sin nx]$：

$$
\frac{1}{2\pi}\int_0^{2\pi}|\Gamma(x)|^2\,dx
=\left(\frac{a_0}{2}\right)^2+\frac{1}{2}\sum_{n=1}^{\infty}(a_n^2+b_n^2).
$$

- **用到的數學**：基底 $\{1,\cos nx,\sin nx\}$ 正交。展開 $|\Gamma|^2$ 後，所有交叉項
  $\int\cos mx\cos nx\,dx$（$m\neq n$）等都積成 0，只剩「自己跟自己」的項。
- **每一項的係數從哪來**：$\dfrac{1}{2\pi}\int_0^{2\pi}\cos^2(nx)\,dx=\dfrac12$（$n\ge1$），
  所以每個 $a_n\cos nx$ 的均方貢獻是 $\dfrac12 a_n^2$；而常數項 $\dfrac{a_0}{2}$ 的均方就是
  $\left(\dfrac{a_0}{2}\right)^2$（常數的均方等於自己平方，沒有 $\frac12$）。**這個 DC 與 AC
  項的 factor 差異是整段推導最容易出錯的地方**，第 4 步會專門講。

**逐步代數（把交叉項一項一項消掉，不跳步）**：先把 $\Gamma$ 的平方完整展開，再逐類積分。

$$
\begin{aligned}
\frac{1}{2\pi}\int_0^{2\pi}|\Gamma|^2dx
&=\frac{1}{2\pi}\int_0^{2\pi}\!\left[\frac{a_0}{2}+\sum_{m\ge1}(a_m\cos mx+b_m\sin mx)\right]^2 dx\\
&=\underbrace{\frac{1}{2\pi}\int_0^{2\pi}\left(\frac{a_0}{2}\right)^2 dx}_{\text{(I) DC×DC}}
+\underbrace{\frac{1}{2\pi}\int_0^{2\pi}2\cdot\frac{a_0}{2}\sum_{m\ge1}(a_m\cos mx+b_m\sin mx)\,dx}_{\text{(II) DC×AC}}\\
&\quad+\underbrace{\frac{1}{2\pi}\int_0^{2\pi}\Big[\sum_{m\ge1}(a_m\cos mx+b_m\sin mx)\Big]^2 dx}_{\text{(III) AC×AC}}.
\end{aligned}
$$

逐項算（每一步用到的正交性都標出來）：

- **(I)**：被積函數是常數，$\dfrac{1}{2\pi}\int_0^{2\pi}\left(\dfrac{a_0}{2}\right)^2dx=\left(\dfrac{a_0}{2}\right)^2$。
- **(II)**：每個 $\int_0^{2\pi}\cos mx\,dx=\int_0^{2\pi}\sin mx\,dx=0$（$m\ge1$），整塊 **= 0**。這就是「常數與任何諧波正交」。
- **(III)**：展開平方會出現三種積分。其一 $\int_0^{2\pi}\cos mx\cos nx\,dx=\pi\,\delta_{mn}$、$\int_0^{2\pi}\sin mx\sin nx\,dx=\pi\,\delta_{mn}$（$m,n\ge1$），其二 $\int_0^{2\pi}\cos mx\sin nx\,dx=0$（**全部**消失，cos 與 sin 互相正交）。只有 $m=n$ 的「自己對自己」存活，各給 $\dfrac{1}{2\pi}\cdot\pi=\dfrac12$ 的權重：

$$
\text{(III)}=\frac12\sum_{n\ge1}(a_n^2+b_n^2).
$$

把 (I)+(II)+(III) 收回去，就回到上面那條 $\left(\frac{a_0}{2}\right)^2+\frac12\sum_{n\ge1}(a_n^2+b_n^2)$。**整段的靈魂只有一句話：基底正交，所以平方積分只留「對角線」項。**

## 第 2 步：換成 amplitude–phase 係數 $c_n$

用上一頁的對應：$c_n^2=a_n^2+b_n^2$（$n\ge1$），以及 DC 係數 $c_0\equiv a_0$。代入第 1 步：

$$
\frac{1}{2\pi}\int_0^{2\pi}|\Gamma|^2\,dx
=\left(\frac{c_0}{2}\right)^2+\frac12\sum_{n=1}^{\infty}c_n^2
=\frac{c_0^2}{4}+\frac12\sum_{n=1}^{\infty}c_n^2.
$$

- **化簡技巧**：注意 $\dfrac{c_0^2}{4}=\dfrac12\cdot\dfrac{c_0^2}{2}$。為了把 DC 併進同一個求和，
  Hajimiri–Lee 採用「$c_0$ 在求和裡權重減半」的記帳——也就是讓 $n=0$ 那項貢獻
  $\dfrac12\cdot\dfrac{c_0^2}{2}$。下一步會看到這正好讓總和寫成最乾淨的形式。

## 第 3 步：得到 [P1] Eq.(20)，定義 $\Gamma_{rms}$

把第 2 步兩邊乘以 2：

$$
\frac{1}{\pi}\int_0^{2\pi}|\Gamma|^2\,dx
=\frac{c_0^2}{2}+\sum_{n=1}^{\infty}c_n^2.
$$

Hajimiri–Lee 在 [P1] Eq.(20) 把左邊定義為 $2\Gamma_{rms}^2$，並把右邊寫成
$\sum_{n=0}^{\infty}c_n^2$——也就是約定**求和裡的 $n=0$ 項代表 $\dfrac{c_0^2}{2}$（而非 $c_0^2$）**。
於是得到本頁開頭的招牌式：

$$
\boxed{\ \sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}|\Gamma(x)|^2dx=2\,\Gamma_{rms}^2\ }\qquad[\text{P1] Eq.(20), p.185}
$$

其中 $\Gamma_{rms}$ 就是 ISF 的均方根：

$$
\Gamma_{rms}=\sqrt{\frac{1}{2\pi}\int_0^{2\pi}|\Gamma(x)|^2\,dx}.
$$

- **量綱檢查**：$\Gamma$ 無因次 ⟹ $|\Gamma|^2$ 無因次 ⟹ 積分除以 $2\pi$（rad）後開根號仍無因次 ✓。
  $c_n$ 也無因次，兩邊一致。
- **本站 Python**：`gamma_rms(theta, gamma)` 算的就是 $\sqrt{\frac{1}{2\pi}\int_0^{2\pi}\Gamma^2}$
  （見 `simulations/common/isf_utils.py` docstring，明確對應 Eq.(20)）。

## 第 4 步：DC 項 factor 的教學註記（最容易出錯的地方）

這一段務必看清楚，否則算 $1/f^3$ corner（[P1] Eq.(24)）時會差一個 factor。把三種「$c_0$」釐清：

| 名稱 | 表達式 | 出現在 |
|---|---|---|
| ISF 的 **DC 值**（平均值） | $\dfrac{c_0}{2}$ | Eq.(12) 的常數項、Eq.(15) 的單音響應 |
| Fourier **DC 係數** | $c_0$（$=a_0=\frac{1}{\pi}\int_0^{2\pi}\Gamma\,dx$） | bar chart、Eq.(20) 的 $n=0$ 項 |
| Parseval 求和裡 $n=0$ 的**貢獻** | $\dfrac{c_0^2}{2}$（不是 $c_0^2$！） | Eq.(20) 右邊 $\sum_{n=0}^\infty c_n^2$ |

- **為何 DC 要「減半」進求和**：AC 諧波 $c_n\cos(nx+\theta_n)$ 的均方是 $\dfrac12 c_n^2$（餘弦的
  時間平均 $\langle\cos^2\rangle=\frac12$）；但 DC 是常數，其均方是 $\left(\dfrac{c_0}{2}\right)^2
  =\dfrac{c_0^2}{4}$。為了讓「$\times2$ 後寫成 $\sum_{n\ge0}c_n^2$」對所有 $n$ 形式一致，
  必須讓 $n=0$ 項只算 $\dfrac{c_0^2}{2}$（即把 $c_0$ 在 rms 求和中視為「半個」）。
- **教學提醒**：很多教科書（與本站 [notation](/00_overview/notation) 的符號陷阱）反覆強調這點——
  $c_0$ 是「係數」，DC「值」是 $c_0/2$。算 phase noise 的式子（如 Eq.(23) 用 $c_0^2/8$、
  Eq.(24) 用 $c_0^2/(2\Gamma_{rms}^2)$）裡的常數，正是把這個 factor 一路帶下來的結果。**直接照抄
  規範第 3 節的式子，不要自己重新塞 factor，就不會錯。**

## 第 5 步：$\Gamma_{rms}$ 如何決定 $1/f^2$ phase noise

把 Eq.(20) 代進白噪 phase-noise 求和式（[P1] Eq.(19), p.185）：

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\overline{i_n^2}/\Delta f\;\sum_{n=0}^{\infty}c_n^2}{8\,q_{max}^2\,\Delta\omega^2}\right).
$$

用 $\sum_{n=0}^{\infty}c_n^2=2\Gamma_{rms}^2$ 把 $\sum c_n^2$ 換掉，分母的 $8$ 與分子的 $2$
約成 $4$，得到那條招牌結果（[P1] Eq.(21), p.185）：

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right).
$$

- **讀法**：phase noise 正比於 $\dfrac{\Gamma_{rms}^2}{q_{max}^2}$，並隨 offset $\Delta\omega$ 以
  $1/\Delta\omega^2$ 下降（即 $-20$ dB/dec，$1/f^2$ region）。設計上兩個旋鈕：**加大 $q_{max}$**
  （訊號電荷擺幅）、**壓小 $\Gamma_{rms}$**（讓 ISF 整體平靜）。
- **factor-of-2 教學註記**：用時域「白噪×ISF→積分」乾淨推導會得到
  $S_\phi(f)=\Gamma_{rms}^2 S_i/(q_{max}^2(2\pi f)^2)$，對應
  $\mathcal{L}=\Gamma_{rms}^2 S_i/(2q_{max}^2\Delta\omega^2)$；而 [P1] Eq.(21) 寫成
  $/(4\Delta\omega^2)$。差的 2 倍來自 SSB（單邊帶）記帳慣例，是文獻上著名的小爭議，**不影響**
  $\Gamma_{rms}^2/q_{max}^2$ scaling 與 $-20$ dB/dec 斜率。完整討論見
  [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

## 數值例子（建立手感）

### 例 1：理想 LC 的 $\Gamma_{rms}$（兩種算法互相驗證）

取 $\Gamma(\theta)=-\sin\theta$。

**算法 A（積分）**：

$$
\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta=\frac{1}{2\pi}\cdot\pi=\frac12
\ \Rightarrow\ \Gamma_{rms}=\frac{1}{\sqrt2}\approx0.707.
$$

**算法 B（係數）**：上一頁得 $c_0=0,\ c_1=1$，其餘為 0。由 Eq.(20)
$\sum c_n^2=c_1^2=1=2\Gamma_{rms}^2$ ⟹ $\Gamma_{rms}=1/\sqrt2\approx0.707$。兩者一致 ✓。

- **手感**：$\Gamma_{rms}\approx0.707$ 是「乾淨單頻 ISF」的基準值。本站 canonical 例題（例 B）用
  $\Gamma_{rms}=0.5$ 當代表值——比理想 $-\sin$ 略小，對應 ISF 被 $q_{max}$ 之外因素略為攤平的情形。

### 例 2：用 $\Gamma_{rms}=0.5$ 算 $1/f^2$ phase noise（canonical 例 B）

> $f_0=5$ GHz、$\Delta f=1$ MHz、$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、$S_i=10^{-24}$ A²/Hz。

先算 $\Delta\omega=2\pi\times10^6=6.283\times10^6$ rad/s，$\Delta\omega^2=3.948\times10^{13}$。
用 Eq.(21)（即 SSB 的 $/(4\Delta\omega^2)$ 慣例，見第 5 步的 factor-of-2 註記；若改用時域乾淨版 $/(2\Delta\omega^2)$ 會高 3 dB）：

$$
\mathcal{L}=10\log_{10}\!\left[\frac{0.25}{10^{-24}}\cdot\frac{10^{-24}}{4\times3.948\times10^{13}}\right]
=10\log_{10}\!\left[\frac{0.25}{4\times3.948\times10^{13}}\right].
$$

括號內 $=\dfrac{0.25}{1.579\times10^{14}}=1.583\times10^{-15}$，故

$$
\mathcal{L}=10\log_{10}(1.583\times10^{-15})\approx-148.0\ \text{dBc/Hz}.
$$

- **量綱檢查**：$\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{\Delta\omega^2}
  =\dfrac{1}{[\text{C}]^2}\cdot\dfrac{[\text{A}^2/\text{Hz}]}{[\text{rad/s}]^2}$；因
  $\text{C}=\text{A}\cdot\text{s}$、$\text{Hz}=1/\text{s}$、rad 無因次，化簡為
  $\dfrac{\text{A}^2\cdot\text{s}}{\text{A}^2\text{s}^2}\cdot\text{s}=$ 無因次（per Hz 已含），$\log$ 後得 dBc/Hz ✓。
- **手感**：這是「單一理想白噪源」的數值；真實電路有多個源、cyclostationary、flicker，會比這更高
  （更差）。完整推導見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

## 圖一：用係數頻譜驗證 $\sum c_n^2=2\Gamma_{rms}^2$

下圖（`lab_05` 的 `fig_coefficients`，`n_harmonics=8`）把 $c_n$ 畫成 bar chart，並在圖上比對
「$\sum_{n=0}^{\infty}c_n^2$（係數那邊算）」與「$2\Gamma_{rms}^2$（積分那邊算）」——兩者吻合，
正是 Parseval（[P1] Eq.(20)）的數值驗證。

![ISF Fourier 係數與 Parseval 驗證 sum c_n^2 = 2 Gamma_rms^2](/figures/isf_fourier_coefficients.png)

- **對應公式**：[P1] Eq.(20)。
- **怎麼解讀**：把每根 bar 高度平方再相加（記得 $n=0$ 那根要按「半權重」$c_0^2/2$ 計），會等於
  $2\Gamma_{rms}^2$。這提供一個實用的健全性檢查：算完係數後，用 Parseval 對一次帳，能立刻抓出
  數值積分窗口沒對齊（沒含端點 $2\pi$）之類的錯誤。
- 程式驗證：

```python
import numpy as np
from simulations.common.isf_utils import (
    gamma_lc_ideal, compute_fourier_coefficients, gamma_rms,
)

theta = np.linspace(0.0, 2 * np.pi, 4096, endpoint=True)  # 必含端點 2*pi
gamma = gamma_lc_ideal(theta)                              # -sin(theta)

a0, a, b, c, phase = compute_fourier_coefficients(theta, gamma, n_harmonics=8)

# 左邊：sum c_n^2，n=0 用半權重 (c0^2 / 2)
lhs = 0.5 * c[0] ** 2 + np.sum(c[1:] ** 2)
# 右邊：2 * Gamma_rms^2
rhs = 2.0 * gamma_rms(theta, gamma) ** 2

print(lhs, rhs)        # -> 1.0 , 1.0   (理想 LC：c1=1，其餘≈0)
print(gamma_rms(theta, gamma))  # -> 0.7071  (= 1/sqrt(2))
```

- **toy model 註記**：使用的 ISF 為 pedagogical toy / 理想 LC 解析式，**非 transistor-level**。
- 完整 script：`simulations/lab_05_fourier_isf.py`。

## 圖二：LC vs ring 的 ISF——$\Gamma_{rms}$ 隨 $N$ 怎麼變

下圖（`lab_03` 的 `fig_lc_vs_ring_isf`）對比理想 LC 的 $-\sin$ 與 ring 的 toy 三角形 ISF
（$N=5,15$）。ring 的敏感度集中在 transition（轉態）處；級數 $N$ 越多，ISF 整體越被攤平、
$\Gamma_{rms}$ 越小。

![LC 的 -sin ISF 與 ring 三角形 ISF 對照](/figures/lc_vs_ring_isf_comparison.png)

- **對應公式**：[P1] Fig. 7（LC vs ring 的波形與 ISF）；[P2] Fig. 8（$\Gamma_{rms}$ vs $N$）。
- **怎麼解讀**：LC 的 ISF 是平滑的單頻；ring 的能量擠在窄窄的 transition，級數越多、每次轉態
  佔週期比例越小，$\Gamma_{rms}$ 下降。
- **toy model 註記**：本站 `gamma_triangular` 是「能量集中在 transition」的 pedagogical toy ISF，
  **非 transistor-level**萃取結果（見 `isf_utils.py` docstring）。

## ring 的 $\Gamma_{rms}\propto N^{-3/4}$ scaling

[P2] 把上面的觀察量化為一條 scaling law（[P2] Eq.(16), p.794）：

$$
\Gamma_{rms}\propto N^{-3/4}
$$

- **直覺**：級數 $N$ 增加時，(i) 每級 transition 變陡、ISF 脈衝變窄（rms 降），(ii) 每週期內
  transition 次數增加但被週期長度稀釋。綜合給出 $\Gamma_{rms}^2\propto N^{-3/2}$（即 $\Gamma_{rms}\propto N^{-3/4}$）。
- **完整式（已核實，對照原始 PDF p.794）**：[P2] Eq.(16) 為

  $$
  \Gamma_{rms}=\sqrt{\frac{2\pi^2}{3\eta^3}\cdot\frac{1}{N^{1.5}}}=\sqrt{\frac{2\pi^2}{3\eta^3}}\,N^{-3/4},
  $$

  其中 $\eta$ 為級延遲比例常數（[P2] Eq.(14)，$\eta\approx1$，非 $\gamma$）。根號涵蓋整個 $1/N^{1.5}$，故開根號後 $\Gamma_{rms}\propto N^{-3/4}$（[P2] Eq.(16), p.794，已核實）。
- **重要結論**：[P2] 進一步指出，在**固定 $f_0$ 與功率 $P$** 的約束下，single-ended
  ring 的 $1/f^2$ phase noise／jitter **幾乎與級數 $N$ 無關**（[P2] Sec.V，Eq.(23)/(25), p.796，
  $\mathcal{L}\big|_{1/f^2}\approx\dfrac{8}{3\eta}\,\dfrac{V_{DD}}{V_{char}}\,\dfrac{kT}{P}(\omega_0/\Delta\omega)^2$）。
- **前置係數說明**：[P2] Eq.(23) 的前置係數是 $\dfrac{8}{3\eta}$（$\eta$ 為級延遲比例常數 Eq.(14)，$\approx1$）；
  $\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入。其 $V_T=0$ 下限（[P2] Eq.(25)）為 $\dfrac{16\gamma}{3\eta}$。
  （v2 曾誤改為 $8/(3\gamma)$ 並誤標「逐字核實」，v3 已對照原始 PDF p.796 更正。）
- 完整 LC vs ring 討論見 [lc_vs_ring](/06_design_insights/lc_vs_ring)；累積 jitter 的隨機漫步
  $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$（[P2] Eq.(8)）見
  [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model)。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| $\Gamma$ 為 $2\pi$ 週期穩態函數 | Parseval 嚴格成立 | 非週期（暫態/injection）時不可用 |
| 白噪平坦（各 band 同強） | 可用 $\sum c_n^2$ 一次加總 | 有色噪要逐 band 加權，不能只用 $\Gamma_{rms}$ |
| 數值積分窗對齊一週期 | 係數與 Parseval 對得上 | 窗沒含端點 $2\pi$ → off-by-one，Parseval 對不起來 |
| stationary noise | $\Gamma_{rms}$ 直接用 | cyclostationary 要改用 $\Gamma_{eff}$（見 [effective_isf](/03_isf_core_theory/effective_isf)） |

## Worked examples 數值例題

這三題照規範第 10.4 格式：題目 → 逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證。

### 例題 1：$\Gamma=-\sin$ 的 $\Gamma_{rms}=1/\sqrt2$

> **題目**：理想 LC 的 $\Gamma(\theta)=-\sin\theta$，求 $\Gamma_{rms}$。

**逐步代入**：直接套定義 $\Gamma_{rms}^2=\dfrac{1}{2\pi}\displaystyle\int_0^{2\pi}\Gamma^2\,d\theta$。

$$
\begin{aligned}
\Gamma_{rms}^2
&=\frac{1}{2\pi}\int_0^{2\pi}(-\sin\theta)^2\,d\theta
=\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta\\
&=\frac{1}{2\pi}\int_0^{2\pi}\frac{1-\cos2\theta}{2}\,d\theta
=\frac{1}{2\pi}\left[\frac{\theta}{2}-\frac{\sin2\theta}{4}\right]_0^{2\pi}
=\frac{1}{2\pi}\cdot\frac{2\pi}{2}=\frac12.
\end{aligned}
$$

**結果**：$\Gamma_{rms}=\sqrt{1/2}=\dfrac{1}{\sqrt2}\approx0.707$。其中第二行用了半角恆等式 $\sin^2\theta=\tfrac12(1-\cos2\theta)$，$\cos2\theta$ 在整個週期上積分為 0。

**dimension check**：$\Gamma=-\sin\theta$ 無因次 → $\Gamma^2$ 無因次 → 對 $\theta$（rad）積分再除以 $2\pi$（rad）後開根號，仍無因次 ✓。

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, gamma_rms
theta = np.linspace(0.0, 2*np.pi, 4096, endpoint=True)   # 含端點 2*pi
print(gamma_rms(theta, gamma_lc_ideal(theta)))            # -> 0.7071  (= 1/sqrt(2))
```

### 例題 2：三角形（ring toy）ISF 的 $\Gamma_{rms}$

> **題目**：ring 的 pedagogical toy ISF 用本站 `gamma_triangular`（$N=5$）：它是一個峰值 $P=1/\sqrt N=1/\sqrt5$、在 $[-P,P]$ 之間線性來回的三角波（每週期兩個 transition）。求 $\Gamma_{rms}$。**（toy model，非 transistor-level。）**

**逐步代入**：三角波在一個基本斜邊上是線性的，均方可用「線性段 $[-P,P]$ 的均方 $=P^2/3$」這個標準結果。理由：設線性段 $\Gamma=P\,s$（$s$ 從 $-1$ 均勻掃到 $1$），

$$
\langle\Gamma^2\rangle=\frac{1}{2}\int_{-1}^{1}(P s)^2\,ds=\frac{P^2}{2}\cdot\frac{s^3}{3}\Big|_{-1}^{1}=\frac{P^2}{2}\cdot\frac{2}{3}=\frac{P^2}{3}.
$$

代 $P=1/\sqrt5$：

$$
\Gamma_{rms}^2=\frac{P^2}{3}=\frac{1/5}{3}=\frac{1}{15}\approx0.0667
\ \Rightarrow\ \Gamma_{rms}=\frac{1}{\sqrt{15}}\approx0.258.
$$

**結果**：$\Gamma_{rms}\approx0.258$，**遠小於 LC 的 0.707**——和「ring 把敏感度擠進窄 transition、能量被攤平、$\Gamma_{rms}$ 隨 $N$ 變小」的物理一致（呼應 $\Gamma_{rms}\propto N^{-3/4}$ 的趨勢；此處 toy 的 $N$ 依賴是 $1/\sqrt N$，非真實 scaling）。

**dimension check**：$P$ 無因次（ISF 無因次）→ $\Gamma_{rms}$ 無因次 ✓。

```python
import numpy as np
from simulations.common.isf_utils import gamma_triangular, gamma_rms
theta = np.linspace(0.0, 2*np.pi, 200001, endpoint=True)
print(gamma_rms(theta, gamma_triangular(theta, n_stages=5)))  # -> 0.2582  (= 1/sqrt(15))
```

### 例題 3：數值驗證 $\sum c_n^2=2\Gamma_{rms}^2$（Parseval 對帳）

> **題目**：對例題 2 的三角形 ISF（$N=5$），分別從**係數那邊**算 $\sum_{n=0}^{\infty}c_n^2$、從**積分那邊**算 $2\Gamma_{rms}^2$，驗證兩者相等。

**逐步代入**：由例題 2，$2\Gamma_{rms}^2=2\times\dfrac{1}{15}=\dfrac{2}{15}\approx0.1333$。係數側則把 $c_n$ 平方相加，**記得 $n=0$ 用半權重** $c_0^2/2$（三角波對稱、$c_0=0$，所以 DC 不貢獻）。Parseval 保證兩數相等。

**結果**：$\sum_{n=0}^{\infty}c_n^2=2\Gamma_{rms}^2\approx0.1333$ ✓。

**dimension check**：$c_n$、$\Gamma_{rms}$ 皆無因次，兩邊一致 ✓。

```python
import numpy as np
from simulations.common.isf_utils import (
    gamma_triangular, compute_fourier_coefficients, gamma_rms,
)
theta = np.linspace(0.0, 2*np.pi, 4096, endpoint=True)
gamma = gamma_triangular(theta, n_stages=5)
a0, a, b, c, ph = compute_fourier_coefficients(theta, gamma, n_harmonics=32)
lhs = 0.5*c[0]**2 + np.sum(c[1:]**2)   # n=0 半權重
rhs = 2.0*gamma_rms(theta, gamma)**2
print(lhs, rhs)                        # -> ~0.1333 , 0.1333  (諧波越多越逼近)
```

- **手感**：三角波是「無窮多奇次諧波」，所以係數側要取夠多 `n_harmonics`（如 32）才會逼近 $2\Gamma_{rms}^2$；諧波取太少（如 8）會略低於積分值——這本身就是「ring ISF 能量散在高次諧波」的數值寫照。
- 完整 script：`simulations/lab_05_fourier_isf.py`、函式庫 `simulations/common/isf_utils.py`。

## 重點回顧

- Parseval：$\sum_{n=0}^{\infty}c_n^2=\dfrac{1}{\pi}\int_0^{2\pi}|\Gamma|^2dx=2\Gamma_{rms}^2$（[P1] Eq.(20), p.185）。
- $\Gamma_{rms}$ 把「逐 band 折回」收成一個形狀指標；它（與 $q_{max}$）決定 $1/f^2$ phase noise：$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$（[P1] Eq.(21)）。
- **DC factor 慣例**：$c_0$ 是係數、DC 值是 $c_0/2$；Parseval 求和裡 $n=0$ 項貢獻 $c_0^2/2$（不是 $c_0^2$）。照抄規範式子即可。
- 理想 LC：$\Gamma_{rms}=1/\sqrt2\approx0.707$；canonical 例 B 用 $\Gamma_{rms}=0.5$ 得 $\mathcal{L}(1\text{MHz})\approx-148$ dBc/Hz。
- ring：$\Gamma_{rms}\propto N^{-3/4}$（[P2] Eq.(16)，已核實）。

## 延伸閱讀

- ISF 的 Fourier 係數（前一步）：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- 用 $\Gamma_{rms}$ 算 $1/f^2$（下一步）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- LC vs ring 的設計取捨：[lc_vs_ring](/06_design_insights/lc_vs_ring)
- cyclostationary 修正：[effective_isf](/03_isf_core_theory/effective_isf)
- 數值手感速查：[numerical_feeling](/04_simulation_labs/numerical_feeling)
