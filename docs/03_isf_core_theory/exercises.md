---
title: 核心理論章習題（含完整解答）
description: ISF 核心理論章成套習題：由 ISF 算 Γrms、c0→1/f³ corner、白噪→L、impulse→phase、Fourier 係數、effective ISF。每題附逐步解、單位與 dimension check、數值答案、一行 Python 驗證。
---

# 核心理論章習題（含完整解答）

> **前置閱讀**：本章理論頁 [isf_definition](/03_isf_core_theory/isf_definition)、[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)、[rms_isf](/03_isf_core_theory/rms_isf)、[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)、[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)、[effective_isf](/03_isf_core_theory/effective_isf)（先讀完再做題）。

這頁是 **03 ISF 核心理論章** 的成套習題。題型涵蓋**推導題**、**數值題**、與**設計反推題**，
全部圍繞 [P1] Hajimiri–Lee 的 ISF 框架展開，沿用全站 notation。

> **格式**：每題解答 = **逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證**。
> Python 一律引用 `simulations/common/`（真實函式，不杜撰）。

涉及的權威公式（逐字取自規範第 3 節，含引用）：

- impulse→phase（操作型 ISF）：$\Delta\phi=\dfrac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q$（規範公式 5）
- ISF 傅立葉級數：$\Gamma(\omega_0\tau)=\dfrac{c_0}{2}+\displaystyle\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)$（[P1] Eq.(12), p.183）
- Parseval / rms ISF：$\displaystyle\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}\lvert\Gamma(x)\rvert^2dx=2\,\Gamma_{rms}^2$（[P1] Eq.(20), p.185）
- 白噪 1/f² 招牌結果：$\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)$（[P1] Eq.(21), p.185）
- 1/f³ corner：$\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\dfrac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\dfrac{c_0}{c_1}\right)^2$（[P1] Eq.(24), p.185）
- effective ISF（cyclostationary）：$\Gamma_{eff}=\Gamma\cdot\alpha$（[P1] Eqs.(25)–(27), p.186）

---

## 題目

### 習題 1（數值題）— impulse → phase step

理想 LC（$\Gamma(\theta)=-\sin\theta$），$q_{max}=1$ pC，$f_0=5$ GHz。一顆 $\Delta q=1$ fC
的電荷脈衝注入。求：
(a) 在 $\theta=3\pi/2$（$\Gamma$ 取最大值 $+1$）注入的相位步階 $\Delta\phi$（rad）與 timing error $\Delta t$（fs）。
(b) 在波峰 $\theta=0$ 注入的 $\Delta\phi$。

### 習題 2（推導題 + 數值）— 由 ISF 算 $\Gamma_{rms}$

某 toy ISF 是雙諧波 $\Gamma(\theta)=\cos\theta+\tfrac12\cos(2\theta)$。
(a) 直接寫出傅立葉係數 $c_0,c_1,c_2$。
(b) 用 Parseval 求 $\sum c_n^2$ 與 $\Gamma_{rms}$。

### 習題 3（數值題）— 白噪 → $\mathcal{L}$（套 Eq.(21)）

$f_0=5$ GHz、$\Delta f=1$ MHz、$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、$S_i=\overline{i_n^2}/\Delta f=10^{-24}\ \text{A}^2/\text{Hz}$。
用 [P1] Eq.(21) 求 $\mathcal{L}(1\,\text{MHz})$（dBc/Hz）。

### 習題 4（設計反推題）— 反推所需 $q_{max}$

延續習題 3 的數字，但目標規格是 $\mathcal{L}(1\,\text{MHz})=-160$ dBc/Hz（比習題 3 更乾淨）。
其餘參數（$\Gamma_{rms}=0.5$、$S_i=10^{-24}$、$\Delta f=1$ MHz）不變，問需要把 $q_{max}$
放大到多少？

### 習題 5（推導題 + 數值）— $c_0\to1/f^3$ corner

某振盪器 ISF 量到 $c_0=0.2$、$c_1=1.0$（即有可觀的 DC 偏移、波形上下不對稱），
device 的 1/f corner $f_{1/f}=1$ MHz（即 $\omega_{1/f}=2\pi\times10^6$ rad/s）。
用 [P1] Eq.(24) 估 $1/f^3$ corner 頻率 $\Delta f_{1/f^3}$（用 $c_0/c_1$ 近似式）。
若把電路改成對稱（$c_0\to0.02$），corner 變多少？

### 習題 6（推導題）— Fourier 係數的頻率搬移意義

對近 $n\omega_0$ 注入的單音 $i(\tau)=I_0\cos((n\omega_0+\Delta\omega)\tau)$，用積化和差
親手證明：經 ISF 第 $n$ 諧波 $c_n\cos(n\omega_0\tau+\theta_n)$ 加權再積分後，存活下來的
慢項給出 $\phi_n(t)\approx\dfrac{I_0 c_n}{2q_{max}}\cdot\dfrac{\sin(\Delta\omega t-\theta_n)}{\Delta\omega}$，
並說明這就是「振盪器當 mixer，把 $n\omega_0$ 附近 noise 下變頻到 $\Delta\omega$」。

### 習題 7（數值題）— effective ISF（cyclostationary）

某 noise 源只在波形某半週導通，用 noise modulating function（NMF）$\alpha(\theta)$
近似為「方波閘控」：$\alpha(\theta)=1$ 當 $\theta\in[0,\pi)$、$\alpha(\theta)=0$ 當 $\theta\in[\pi,2\pi)$。
基礎 ISF 仍是 $\Gamma(\theta)=-\sin\theta$。求 effective ISF $\Gamma_{eff}=\Gamma\cdot\alpha$ 的
$\Gamma_{eff,rms}$，並與全程導通的 $\Gamma_{rms}=1/\sqrt2$ 比較。

### 習題 8（設計反推題）— 由 $\mathcal{L}$ 反推 $\Gamma_{rms}/q_{max}$

某 5 GHz LC 振盪器量到 $\mathcal{L}(1\,\text{MHz})=-130$ dBc/Hz，已知白噪源
$S_i=2\times10^{-23}\ \text{A}^2/\text{Hz}$（多源等效）。假設 $1/f^2$ 區由白噪主導、套 Eq.(21)，
反推有效的 $\Gamma_{rms}/q_{max}$（單位 $1/\text{C}$）。若 $q_{max}=1.5$ pC，則 $\Gamma_{rms}$ 約多少？

---

## 解答展開

<details>
<summary><strong>習題 1 解答</strong>（impulse → phase step）</summary>

**(a) $\theta=3\pi/2$。** $\Gamma=-\sin(3\pi/2)=-(-1)=+1$。用規範公式 5：

$$
\Delta\phi=\frac{\Gamma}{q_{max}}\Delta q=\frac{1\times(1\times10^{-15}\ \text{C})}{1\times10^{-12}\ \text{C}}=1\times10^{-3}\ \text{rad}=1\ \text{mrad}.
$$

timing error（規範公式 17）：

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0}=\frac{10^{-3}}{2\pi\times5\times10^{9}}\approx3.18\times10^{-14}\ \text{s}=31.8\ \text{fs}.
$$

**(b) $\theta=0$。** $\Gamma=-\sin0=0\Rightarrow\Delta\phi=0$（波峰注入只改振幅，被 restoring 拉回）。

**結果**：(a) $\Delta\phi=1$ mrad、$\Delta t\approx31.8$ fs；(b) $\Delta\phi=0$。

**手感**：這正是 canonical 例 A（$\Gamma=0.5$ 給 15.9 fs）的「滿格」版——$\Gamma=1$ 給兩倍即 31.8 fs。

**Dimension check**：$\Gamma$ 無因次 $\times$ (C/C) $=$ rad ✓；$\dfrac{\text{rad}}{\text{rad/s}}=\text{s}$ ✓。

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error
for th in (3*np.pi/2, 0.0):
    dphi = impulse_to_phase_step(1e-15, gamma_lc_ideal(th), qmax=1e-12)
    print(round(dphi*1e3,3), "mrad ;", round(phase_to_time_error(dphi,5e9)*1e15,1), "fs")
# -> 1.0 mrad ; 31.8 fs    and    0.0 mrad ; 0.0 fs
```

</details>

<details>
<summary><strong>習題 2 解答</strong>（由 ISF 算 $\Gamma_{rms}$）</summary>

**(a) 讀出係數。** 把 $\Gamma(\theta)=\cos\theta+\tfrac12\cos(2\theta)$ 對照傅立葉級數
$\Gamma=\tfrac{c_0}{2}+\sum c_n\cos(n\theta+\theta_n)$：沒有常數項 $\Rightarrow c_0=0$；
一次諧波幅度 $c_1=1$（$\theta_1=0$）；二次諧波幅度 $c_2=\tfrac12$（$\theta_2=0$）；$c_{n\ge3}=0$。

**(b) Parseval。** 規範公式 11：

$$
\sum_{n=0}^{\infty}c_n^2=c_0^2+c_1^2+c_2^2=0+1^2+\left(\tfrac12\right)^2=1.25.
$$

$$
\Gamma_{rms}^2=\frac{\sum c_n^2}{2}=\frac{1.25}{2}=0.625\quad\Longrightarrow\quad\Gamma_{rms}=\sqrt{0.625}\approx0.791.
$$

**結果**：$c_0=0,\ c_1=1,\ c_2=0.5$；$\sum c_n^2=1.25$；$\Gamma_{rms}\approx0.791$。

**交叉驗證**（直接積分）：$\Gamma_{rms}^2=\tfrac{1}{2\pi}\int_0^{2\pi}(\cos\theta+\tfrac12\cos2\theta)^2d\theta$，
交叉項 $\int\cos\theta\cos2\theta=0$（正交），餘 $\tfrac12+\tfrac12\cdot\tfrac14=0.5+0.125=0.625$ ✓。

**Dimension check**：$c_n$、$\Gamma_{rms}$ 全無因次 ✓。

```python
import numpy as np
from simulations.common.isf_utils import gamma_rms, compute_fourier_coefficients
theta = np.linspace(0, 2*np.pi, 8192, endpoint=False)
g = np.cos(theta) + 0.5*np.cos(2*theta)
print(gamma_rms(theta, g))                          # -> 0.7906
a0, a, b, c, ph = compute_fourier_coefficients(theta, g, n_harmonics=3)
print(c[:3], np.sum(c**2))                          # -> ~[1, 0.5] ... ; 1.25
```

</details>

<details>
<summary><strong>習題 3 解答</strong>（白噪 → $\mathcal{L}$，套 Eq.(21)）</summary>

**逐步代入（帶單位）。** 這是 canonical 例 B。

1. $\Delta\omega=2\pi\Delta f=2\pi\times10^6=6.283\times10^6\ \text{rad/s}$，$\Delta\omega^2=3.948\times10^{13}$。
2. $\dfrac{\Gamma_{rms}^2}{q_{max}^2}=\dfrac{0.25}{(10^{-12})^2}=2.5\times10^{23}\ \text{C}^{-2}$。
3. $\dfrac{S_i}{4\Delta\omega^2}=\dfrac{10^{-24}}{4\times3.948\times10^{13}}=6.332\times10^{-39}$。
4. 相乘：$2.5\times10^{23}\times6.332\times10^{-39}=1.583\times10^{-15}$。
5. $\mathcal{L}=10\log_{10}(1.583\times10^{-15})=-148.0\ \text{dBc/Hz}$。

**結果**：$\mathcal{L}(1\,\text{MHz})\approx-148.0$ dBc/Hz（單一理想白噪源的理論底線）。

**Dimension check**：括號內 $\text{C}^{-2}\cdot\dfrac{\text{A}^2/\text{Hz}}{(\text{rad/s})^2}$，以 $\text{C}=\text{A·s}$
化簡為 $\text{s}$（per-Hz），取 $10\log_{10}$ 讀作 dBc/Hz ✓。詳見
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

```python
import numpy as np
gamma_rms, qmax, Si = 0.5, 1e-12, 1e-24
dw = 2*np.pi*1e6
L = 10*np.log10((gamma_rms**2/qmax**2)*(Si/(4*dw**2)))
print(round(L,1), "dBc/Hz")   # -> -148.0 dBc/Hz
```

</details>

<details>
<summary><strong>習題 4 解答</strong>（反推所需 $q_{max}$）</summary>

**設計反推策略。** $\mathcal{L}\propto1/q_{max}^2$（Eq.(21) 分母）。目標比習題 3 低
$\Delta L=-160-(-148)=-12$ dB。把 $\mathcal{L}$ 寫成 linear、固定其餘變數，
$\mathcal{L}_{\text{lin}}\propto1/q_{max}^2$：

$$
\frac{q_{max,\text{new}}^2}{q_{max,\text{old}}^2}=\frac{\mathcal{L}_{\text{lin,old}}}{\mathcal{L}_{\text{lin,new}}}=10^{(-148-(-160))/10}=10^{12/10}=10^{1.2}=15.85.
$$

$$
\frac{q_{max,\text{new}}}{q_{max,\text{old}}}=\sqrt{15.85}=3.98\quad\Longrightarrow\quad q_{max,\text{new}}\approx3.98\times1\ \text{pC}=3.98\ \text{pC}.
$$

**直接驗算**（直接套 Eq.(21) 解 $q_{max}$）：
$q_{max}=\sqrt{\dfrac{\Gamma_{rms}^2}{\mathcal{L}_{\text{lin}}}\cdot\dfrac{S_i}{4\Delta\omega^2}}$，
$\mathcal{L}_{\text{lin}}=10^{-16}$：

$$
q_{max}=\sqrt{\frac{0.25}{10^{-16}}\times6.332\times10^{-39}}=\sqrt{1.583\times10^{-23}}=3.98\times10^{-12}\ \text{C}=3.98\ \text{pC}.
$$

**結果**：需把 $q_{max}$ 放大約 **4 倍** 到 $\approx3.98$ pC（即每降 6 dB 相位雜訊，$q_{max}$ 要 $\times2$）。

**手感**：這量化了「**加大訊號擺幅**是降低 $1/f^2$ 相位雜訊最直接的旋鈕」（claim C3），
但 12 dB 要 4 倍電荷擺幅，代價是功耗/面積——這正是 [tank_swing](/06_design_insights/tank_swing) 的取捨。

**Dimension check**：$\sqrt{\text{C}^{-2}\text{·s}^{-1}\cdots}$ 反解回 $q_{max}$ 為 C ✓。

```python
import numpy as np
gamma_rms, Si, dw = 0.5, 1e-24, 2*np.pi*1e6
L_lin = 10**(-160/10)
qmax = np.sqrt((gamma_rms**2/L_lin)*(Si/(4*dw**2)))
print(qmax*1e12, "pC")        # -> 3.98 pC
```

</details>

<details>
<summary><strong>習題 5 解答</strong>（$c_0\to1/f^3$ corner）</summary>

**逐步代入（帶單位）。** 用 [P1] Eq.(24) 的 $c_0/c_1$ 近似式
$\Delta\omega_{1/f^3}\approx\omega_{1/f}\left(\dfrac{c_0}{c_1}\right)^2$，再換成 $\Delta f_{1/f^3}=\Delta\omega_{1/f^3}/(2\pi)$，
而 $\omega_{1/f}=2\pi f_{1/f}$，故 $2\pi$ 約掉：$\Delta f_{1/f^3}\approx f_{1/f}\left(\dfrac{c_0}{c_1}\right)^2$。

**不對稱情形**（$c_0=0.2$、$c_1=1.0$）：

$$
\Delta f_{1/f^3}\approx10^6\times\left(\frac{0.2}{1.0}\right)^2=10^6\times0.04=4\times10^{4}\ \text{Hz}=40\ \text{kHz}.
$$

**對稱化後**（$c_0=0.02$、$c_1=1.0$）：

$$
\Delta f_{1/f^3}\approx10^6\times\left(\frac{0.02}{1.0}\right)^2=10^6\times4\times10^{-4}=400\ \text{Hz}.
$$

**結果**：不對稱時 $1/f^3$ corner $\approx40$ kHz；對稱化（$c_0$ 降 10 倍）後 corner 降 $100$ 倍到 $\approx400$ Hz。

**適用條件（近似式 vs 精確式）**：$(c_0/c_1)^2$ 近似假設 ISF **由基波主導**（$\Gamma_{rms}^2\approx c_1^2/2$）。
此處 $c_0=0.2$ 不可忽略，用精確式 $\Delta f_{1/f^3}=f_{1/f}\cdot\dfrac{c_0^2}{2\Gamma_{rms}^2}$，
其中 $\Gamma_{rms}^2=(c_0^2+c_1^2)/2=(0.04+1)/2=0.52$，得
$\Delta f_{1/f^3}=10^6\times\dfrac{0.04}{2\times0.52}\approx38.5$ kHz，與近似的 40 kHz 差約 4%。
對稱化後（$c_0=0.02$，$\Gamma_{rms}^2\approx0.5$）兩式幾乎一致。

**設計訊息**：$1/f^3$ corner $\propto c_0^2$。**讓波形上下對稱（壓 $c_0$）** 是把 flicker 上轉的
close-in $1/f^3$ 雜訊推離載波最有效的手段（見 [symmetry](/06_design_insights/symmetry)、
[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)）。

**Dimension check**：$(c_0/c_1)^2$ 無因次 $\times\ f_{1/f}$（Hz）$=$ Hz ✓。

```python
f_1f = 1e6
for c0 in (0.2, 0.02):
    f_corner = f_1f*(c0/1.0)**2
    print(c0, "->", f_corner, "Hz")   # -> 0.2 -> 40000.0 Hz ; 0.02 -> 400.0 Hz
```

</details>

<details>
<summary><strong>習題 6 解答</strong>（Fourier 係數的頻率搬移意義 — 推導）</summary>

**目標式。** 第 $n$ 諧波項的相位貢獻（[P1] Eq.(13)）：

$$
\phi_n(t)=\frac{1}{q_{max}}\int^{t}\!\!c_n\cos(n\omega_0\tau+\theta_n)\,I_0\cos\big((n\omega_0+\Delta\omega)\tau\big)\,d\tau.
$$

**第 (i) 步：積化和差。** 令 $A=n\omega_0\tau+\theta_n$、$B=(n\omega_0+\Delta\omega)\tau$，用
$\cos A\cos B=\tfrac12[\cos(A-B)+\cos(A+B)]$：

$$
A-B=\theta_n-\Delta\omega\tau,\qquad A+B=(2n\omega_0+\Delta\omega)\tau+\theta_n.
$$

被積函數 $=\dfrac{I_0c_n}{2}\Big[\underbrace{\cos(\Delta\omega\tau-\theta_n)}_{\text{慢，}\approx\Delta\omega}+\underbrace{\cos((2n\omega_0+\Delta\omega)\tau+\theta_n)}_{\text{快，}\approx2n\omega_0}\Big]$。

**第 (ii) 步：積分器是低通，快項被平均掉。**

- 慢項：$\int\cos(\Delta\omega\tau-\theta_n)d\tau=\dfrac{\sin(\Delta\omega\tau-\theta_n)}{\Delta\omega}$——分母只有小小的 $\Delta\omega$，**被放大、存活**。
- 快項：$\dfrac{\sin(\cdots)}{2n\omega_0+\Delta\omega}$——分母是巨大的 $2n\omega_0$，幅度被壓到 $\sim\Delta\omega/(2n\omega_0)$ 倍，**可忽略**。

**第 (iii) 步：只留慢項。**

$$
\phi_n(t)\approx\frac{1}{q_{max}}\cdot\frac{I_0c_n}{2}\cdot\frac{\sin(\Delta\omega t-\theta_n)}{\Delta\omega}=\frac{I_0 c_n}{2q_{max}}\cdot\frac{\sin(\Delta\omega t-\theta_n)}{\Delta\omega}.\qquad\blacksquare
$$

**物理意義（mixer 觀點）**：ISF 的第 $n$ 諧波 $c_n$ 像一個 LO（本地振盪）梳齒，把
注入頻率 $n\omega_0+\Delta\omega$ 處的 noise **下變頻**到 baseband 的 $\Delta\omega$ 處；
快項（和頻 $\approx2n\omega_0$）被積分器這個低通濾掉。**振盪器本身就是一個對自己各諧波取樣的 mixer**——
這就是 $c_n$ 為什麼是「相位輸出對各諧波的轉換係數」（連 [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)）。

**Dimension check**：$\phi_n=\dfrac{I_0 c_n}{2q_{max}}\cdot\dfrac{\sin(\cdots)}{\Delta\omega}$ 的單位為
$\dfrac{[\text{A}]\cdot(\text{無因次})}{[\text{C}]\cdot[\text{rad/s}]}$；以 $\text{C}=\text{A·s}$、rad 視為無因次代入，
$=\dfrac{\text{A}}{(\text{A·s})\cdot(1/\text{s})}=\dfrac{\text{A}}{\text{A}}=1$（無因次），故 $\phi$ 無因次（相位以 rad 計）✓。

```python
import numpy as np
# 數值驗證：直接做積分，看慢項存活、快項消失
n, w0, dw, c_n, I0, qmax, th_n = 1, 1.0, 1e-3, 1.0, 1.0, 1.0, 0.4
tau = np.linspace(0, 2000*np.pi, 4_000_000)         # 涵蓋多個慢週期
integrand = c_n*np.cos(n*w0*tau+th_n)*I0*np.cos((n*w0+dw)*tau)
phi = np.cumsum(integrand)*(tau[1]-tau[0])/qmax
analytic = I0*c_n/(2*qmax)*np.sin(dw*tau-th_n)/dw
print(np.max(np.abs(phi-analytic-np.mean(phi-analytic)))/np.max(np.abs(analytic)))
# -> 慢項包絡吻合（相對誤差 ~5e-4，殘差為被平均掉的快項）
```

</details>

<details>
<summary><strong>習題 7 解答</strong>（effective ISF，cyclostationary）</summary>

**逐步代入。** effective ISF（[P1] Eqs.(25)–(27)）$\Gamma_{eff}(\theta)=\Gamma(\theta)\,\alpha(\theta)$。
這裡 $\alpha$ 是方波閘控（半週導通），故

$$
\Gamma_{eff}(\theta)=\begin{cases}-\sin\theta,&\theta\in[0,\pi)\\[2pt]0,&\theta\in[\pi,2\pi).\end{cases}
$$

求 rms：

$$
\Gamma_{eff,rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\Gamma_{eff}^2\,d\theta=\frac{1}{2\pi}\int_0^{\pi}\sin^2\theta\,d\theta=\frac{1}{2\pi}\cdot\frac{\pi}{2}=\frac14.
$$

$$
\Gamma_{eff,rms}=\frac12=0.5.
$$

**比較**：全程導通 $\Gamma_{rms}=1/\sqrt2\approx0.707$；半週閘控後 $\Gamma_{eff,rms}=0.5$。
比值 $0.5/0.707=1/\sqrt2$——閘掉一半相位，rms 降 $\sqrt2$ 倍（功率降一半）。

**結果**：$\Gamma_{eff,rms}=0.5$（比全程的 $0.707$ 低 $\approx3$ dB 功率）。

**設計訊息**：noise 在「ISF 小的相位」才導通，可大幅降低有效雜訊貢獻——這就是
**讓 noise 電流避開高敏感區（過零點）** 的設計直覺（見 [effective_isf](/03_isf_core_theory/effective_isf)）。
這裡的方波閘控是 illustrative toy；真實 NMF $\alpha(\theta)$ 由 device bias-dependent 熱雜訊決定。

**Dimension check**：$\Gamma$、$\alpha$、$\Gamma_{eff}$ 全無因次 ✓。

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, gamma_rms, effective_isf
theta = np.linspace(0, 2*np.pi, 8192, endpoint=False)
g = gamma_lc_ideal(theta)
alpha = (theta < np.pi).astype(float)          # 半週方波閘控
g_eff = effective_isf(g, alpha)                # = g*alpha
print(gamma_rms(theta, g_eff))                 # -> 0.5
```

</details>

<details>
<summary><strong>習題 8 解答</strong>（由 $\mathcal{L}$ 反推 $\Gamma_{rms}/q_{max}$）</summary>

**設計反推策略。** 套 Eq.(21) 解 $\dfrac{\Gamma_{rms}^2}{q_{max}^2}$：

$$
\frac{\Gamma_{rms}^2}{q_{max}^2}=\frac{\mathcal{L}_{\text{lin}}}{S_i/(4\Delta\omega^2)}=\mathcal{L}_{\text{lin}}\cdot\frac{4\Delta\omega^2}{S_i}.
$$

**逐步代入（帶單位）。**

1. $\mathcal{L}_{\text{lin}}=10^{-130/10}=10^{-13}$。
2. $\Delta\omega=2\pi\times10^6=6.283\times10^6$，$4\Delta\omega^2=4\times3.948\times10^{13}=1.579\times10^{14}$。
3. $\dfrac{4\Delta\omega^2}{S_i}=\dfrac{1.579\times10^{14}}{2\times10^{-23}}=7.896\times10^{36}$。
4. $\dfrac{\Gamma_{rms}^2}{q_{max}^2}=10^{-13}\times7.896\times10^{36}=7.896\times10^{23}\ \text{C}^{-2}$。
5. $\dfrac{\Gamma_{rms}}{q_{max}}=\sqrt{7.896\times10^{23}}=8.886\times10^{11}\ \text{C}^{-1}$。

**若 $q_{max}=1.5$ pC**：

$$
\Gamma_{rms}=\frac{\Gamma_{rms}}{q_{max}}\times q_{max}=8.886\times10^{11}\times1.5\times10^{-12}=1.33.
$$

**結果**：$\Gamma_{rms}/q_{max}\approx8.89\times10^{11}\ \text{C}^{-1}$；若 $q_{max}=1.5$ pC 則 $\Gamma_{rms}\approx1.33$。

**手感檢查**：$\Gamma_{rms}\approx1.33$ 略大於理想 $-\sin$ 的 $0.707$——合理，因為這顆量到的相位雜訊
（$-130$ dBc/Hz）比 canonical 單一理想白噪源（$-148$）高約 18 dB，反映多源、cyclostationary、
較大 ISF 的真實情況。**反推法可用來「從量測 PN 體檢有效 $\Gamma_{rms}$ 是否偏大」。**

**Dimension check**：$\mathcal{L}_{\text{lin}}$（per-Hz $=$ s）$\times\dfrac{(\text{rad/s})^2}{\text{A}^2/\text{Hz}}=\text{s}\cdot\dfrac{\text{s}^{-2}}{\text{A}^2\text{s}}=\text{A}^{-2}\text{s}^{-2}=\text{C}^{-2}$ ✓。

```python
import numpy as np
L_lin, Si, dw = 10**(-130/10), 2e-23, 2*np.pi*1e6
ratio2 = L_lin*(4*dw**2/Si)              # (Gamma_rms/qmax)^2
ratio = np.sqrt(ratio2)
print(ratio, "1/C ;", ratio*1.5e-12, "= Gamma_rms")   # -> 8.89e11 1/C ; 1.33
```

</details>

---

## 重點回顧

- **impulse→phase**：$\Delta\phi=\Gamma\,\Delta q/q_{max}$；$\Gamma=1$ 在 5 GHz 給 31.8 fs（習題 1）。
- **由 ISF 算 $\Gamma_{rms}$**：Parseval $\sum c_n^2=2\Gamma_{rms}^2$；雙諧波例 $\Gamma_{rms}=0.791$（習題 2）。
- **白噪→$\mathcal{L}$**：canonical 例 B $\approx-148$ dBc/Hz（習題 3）；反推 $q_{max}$：降 6 dB 要 $\times2$（習題 4）。
- **$c_0\to1/f^3$ corner**：corner $\propto c_0^2$；對稱化 10 倍 → corner 降 100 倍（習題 5）。
- **Fourier 係數 = mixer 轉換**：$c_n$ 把 $n\omega_0$ 附近 noise 下變頻到 $\Delta\omega$，快項被積分器濾掉（習題 6）。
- **effective ISF**：半週閘控 $\Gamma_{eff,rms}=0.5 < 0.707$；noise 避開高敏感區可降雜訊（習題 7）。
- **反推 $\Gamma_{rms}/q_{max}$**：可由量測 PN 體檢有效 ISF 是否偏大（習題 8）。
- 全部 Python 驗證引用 `simulations/common/`（`isf_utils`、`noise_utils`）。

## 延伸閱讀

- impulse→phase：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)
- 白噪→$\mathcal{L}$：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- Fourier 級數：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- $\Gamma_{rms}$ 與 Parseval：[rms_isf](/03_isf_core_theory/rms_isf)
- flicker 上轉與對稱性：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- effective ISF：[effective_isf](/03_isf_core_theory/effective_isf)

## 其他習題

- 基礎章習題（PSD / jitter 方言 / 隨機過程）：[02 基礎章習題](/02_foundations/exercises)
- 設計章習題（swing / 拓樸 / PLL 預算 / SerDes 反推）：[06 設計章習題](/06_design_insights/exercises)
- 分級 worked examples（基礎換算／ISF→PN／jitter 積分／設計反推，每題逐步解＋Python 驗證）：[worked_examples](/04_simulation_labs/worked_examples)
