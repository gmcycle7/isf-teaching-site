---
title: 基礎章習題（含完整解答）
description: 基礎章成套習題：phase↔jitter 換算、PSD/Parseval、LTI vs LTV、Allan 斜率判讀、Lorentzian 線寬估算。每題附逐步解、單位與 dimension check、數值答案、一行 Python 驗證。
---

# 基礎章習題（含完整解答）

> 先備：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) · [lti_vs_ltv](/02_foundations/lti_vs_ltv) ｜ 接下來：[03 核心理論章習題](/03_isf_core_theory/exercises)

這頁是 **02 基礎章** 的成套習題。題型涵蓋**推導題**（要你把式子親手導出來）、**數值題**
（代數字、帶單位、做 dimension check）、與**設計反推題**（給目標規格、反算所需參數）。

> **怎麼用這頁**：先把題目自己做一遍，再展開「解答」對照。每題解答都遵守同一套格式：
> **逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證**。Python 驗證一律
> 引用本站真實函式庫 `simulations/common/`（不杜撰 API），你可以直接貼進 REPL 跑。

涉及的核心公式（都來自規範與本章頁面，沿用同一 notation）：

- phase→time：$\Delta t=\dfrac{\Delta\phi}{2\pi f_0}$（規範公式 17）
- phase variance：$\sigma_\phi^2=\displaystyle\int_{f_1}^{f_2}S_\phi(f)\,df$（規範公式 18）
- rms jitter：$\sigma_t=\dfrac{1}{2\pi f_0}\sqrt{\displaystyle\int_{f_1}^{f_2}S_\phi(f)\,df}$（規範公式 19）
- SSB↔phase PSD（小角）：$\mathcal{L}(\Delta f)\approx\tfrac12 S_\phi(\Delta f)$（規範公式 16）
- Parseval：$\displaystyle\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}\lvert\Gamma(x)\rvert^2dx=2\,\Gamma_{rms}^2$（[P1] Eq.(20), p.185）
- Lorentzian 線寬（FWHM）：$\Delta f_{3\mathrm{dB}}=\dfrac{D}{\pi}$，相位擴散 $\operatorname{Var}[\Delta\phi(t)]=2D\lvert t\rvert$（規範 11.2；連 [E2] Demir 2000，不在 5 篇 PDF 內）
- Allan 斜率對照：white FM $\to\tau^{-1/2}$、flicker FM $\to\tau^{0}$、random-walk FM $\to\tau^{+1/2}$（規範 11.2；Allan 為外部文獻）

---

## 題目

### 習題 1（數值題）— phase ↔ time 換算

一顆 $f_0=5$ GHz 的振盪器，某瞬間 excess phase 偏移 $\Delta\phi=5\times10^{-4}$ rad。
求對應的 timing error $\Delta t$（fs），並把 $\Delta\phi$ 換成「度」。

### 習題 2（數值題）— rms jitter 由相位變異反推

已知某時鐘的 rms phase $\sigma_\phi=14.07$ mrad（在 1→100 MHz 積分頻段內），$f_0=5$ GHz。
求 rms timing jitter $\sigma_t$（fs）。

### 習題 3（推導題 + 數值）— Parseval：由 ISF 算 $\Gamma_{rms}$ 與 $\sum c_n^2$

理想 LC 振盪器的 ISF 是 $\Gamma(\theta)=-\sin\theta$。

(a) 用定義 $\Gamma_{rms}^2=\dfrac{1}{2\pi}\displaystyle\int_0^{2\pi}\Gamma^2(\theta)\,d\theta$ 親手算 $\Gamma_{rms}$。
(b) 用 Parseval（規範公式 11）求 $\sum_{n=0}^{\infty}c_n^2$，並說明只有哪個 $c_n$ 非零。

### 習題 4（數值題）— PSD 積分得相位變異

某振盪器在 offset $f$ 的單邊 phase PSD 在 $1/f^2$ 區可寫成 $S_\phi(f)=\dfrac{K}{f^2}$，
其中 $K=10^{-4}\ \text{rad}^2\cdot\text{Hz}$（即 $S_\phi(1\,\text{Hz})=10^{-4}$）。求積分頻段
$f_1=10^3$ Hz 到 $f_2=10^6$ Hz 的相位變異 $\sigma_\phi^2$ 與 $\sigma_\phi$（mrad）。

### 習題 5（概念 + 推導題）— LTI vs LTV：同 impulse、不同相位

理想 LC 的 ISF $\Gamma(\theta)=-\sin\theta$。同一顆 $\Delta q$ 的電荷脈衝，分別在
(a) 波形**過零點**（zero-crossing，$\theta=\pi/2$，此處 $\cos$ 波形斜率最大、$-\sin$ 取極值）
與 (b) 波形**峰值**（$\theta=0$）注入。用 $\Delta\phi=\Gamma(\theta)\,\Delta q/q_{max}$
說明兩者相位效果差多少，並一句話講清楚這「為什麼是 LTV 而不是 LTI」。
取 $\Delta q=1$ fC、$q_{max}=1$ pC。

### 習題 6（設計反推題）— Lorentzian 線寬反推 phase diffusion

某自由運轉振盪器量到的載波 3-dB 線寬（FWHM）$\Delta f_{3\mathrm{dB}}=1$ kHz。

(a) 反推 phase diffusion 係數 $D$（rad²/s）。
(b) 估計相位累積到變異 $\operatorname{Var}[\Delta\phi]=1\ \text{rad}^2$（相位「跑掉約 1 rad」、相干性大致瓦解）需要多久 $t$。

### 習題 7（概念 + 斜率判讀題）— Allan deviation 斜率

在 log–log 的 Allan deviation 圖 $\sigma_y(\tau)$ 上量到三段不同斜率：
$-1/2$、$0$、$+1/2$。分別對應哪一種 FM 雜訊型態？並說明為何「flicker FM」會在 ADEV 上
形成一段**平台（floor）**。

### 習題 8（數值題）— 由 $\mathcal{L}(\Delta f)$ 換 $S_\phi$ 再換單音 jitter

某 spur-free 振盪器在 $\Delta f=1$ MHz 量到 $\mathcal{L}(1\,\text{MHz})=-120$ dBc/Hz。
(a) 求該 offset 的 $S_\phi$（rad²/Hz）。
(b) 若在 1→10 MHz 這 1 decade 內 PSD 為 $1/f^2$（即 $S_\phi=K/f^2$，用 (a) 定 $K$），
$f_0=5$ GHz，求此頻段 rms jitter $\sigma_t$（fs）。

---

## 解答展開

<details>
<summary><strong>習題 1 解答</strong>（phase ↔ time 換算）</summary>

**逐步代入（帶單位）。** 用 phase→time（規範公式 17）：

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0}=\frac{5\times10^{-4}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=\frac{5\times10^{-4}}{3.1416\times10^{10}}\ \text{s}.
$$

$$
\Delta t\approx1.59\times10^{-14}\ \text{s}=15.9\ \text{fs}.
$$

換成度：

$$
\Delta\phi=5\times10^{-4}\times\frac{180}{\pi}\approx0.0286^\circ.
$$

**結果**：$\Delta t\approx15.9$ fs，$\Delta\phi\approx0.0286^\circ$。

**Dimension check**：$\dfrac{[\text{rad}]}{[\text{rad/s}]}=[\text{s}]$ ✓（$2\pi f_0$ 的單位是 rad/s，rad 是
無因次，相除得秒）。這正是規範第 8 節 canonical 例 A 的 timing error。

```python
from simulations.common.noise_utils import phase_to_time_error
dt = phase_to_time_error(5e-4, f0=5e9)
print(dt*1e15, "fs")   # -> 15.92 fs
```

</details>

<details>
<summary><strong>習題 2 解答</strong>（rms jitter 由相位變異反推）</summary>

**逐步代入（帶單位）。** rms jitter（規範公式 19）。這裡已直接給 $\sigma_\phi$，所以
$\sqrt{\int S_\phi df}=\sigma_\phi$，公式退化成 phase→time 在 rms 意義下的版本：

$$
\sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{14.07\times10^{-3}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=\frac{1.407\times10^{-2}}{3.1416\times10^{10}}\ \text{s}.
$$

$$
\sigma_t\approx4.479\times10^{-13}\ \text{s}=447.9\ \text{fs}.
$$

**結果**：$\sigma_t\approx447.9$ fs。這對應規範第 8 節 canonical 例 C（$f_0=5$ GHz、
$\mathcal{L}(1\text{MHz})=-100$ dBc/Hz、1/f² 斜率、積分 1→100 MHz 的 lab_08 結果）。

**Dimension check**：$\dfrac{[\text{rad}]}{[\text{rad/s}]}=[\text{s}]$ ✓。

```python
import numpy as np
sigma_phi = 14.07e-3            # rad
f0 = 5e9
sigma_t = sigma_phi/(2*np.pi*f0)
print(sigma_t*1e15, "fs")      # -> 447.9 fs
```

（完整積分版見 [numerical_feeling](/04_simulation_labs/numerical_feeling) 與
`simulations/common/noise_utils.py` 的 `integrate_rms_jitter`。）

</details>

<details>
<summary><strong>習題 3 解答</strong>（Parseval：由 ISF 算 $\Gamma_{rms}$ 與 $\sum c_n^2$）</summary>

**(a) 直接積分算 $\Gamma_{rms}$。** 用 $\sin^2\theta$ 在一個週期上平均為 $\tfrac12$：

$$
\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}(-\sin\theta)^2\,d\theta=\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta=\frac{1}{2\pi}\cdot\pi=\frac12.
$$

$$
\Gamma_{rms}=\frac{1}{\sqrt2}\approx0.707.
$$

**(b) 用 Parseval 求 $\sum c_n^2$。** 規範公式 11（[P1] Eq.(20), p.185）：

$$
\sum_{n=0}^{\infty}c_n^2=2\,\Gamma_{rms}^2=2\times\frac12=1.
$$

**哪個 $c_n$ 非零**：$\Gamma(\theta)=-\sin\theta=\cos(\theta+\tfrac{\pi}{2})$，是**純一次諧波**，
所以只有 $c_1=1$（且 $\theta_1=\pi/2$），其餘 $c_0=c_2=\dots=0$。驗證：$\sum c_n^2=c_1^2=1$ ✓。

**結果**：$\Gamma_{rms}=1/\sqrt2\approx0.707$、$\sum c_n^2=1$、唯一非零係數 $c_1=1$。

**Dimension check**：$\Gamma$ 無因次（規範 notation 表），故 $\Gamma_{rms}^2$、$\sum c_n^2$ 皆無因次 ✓。

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, gamma_rms, compute_fourier_coefficients
theta = np.linspace(0, 2*np.pi, 4096, endpoint=False)
g = gamma_lc_ideal(theta)                     # = -sin(theta)
print(gamma_rms(theta, g))                    # -> 0.7071
a0, a, b, c, ph = compute_fourier_coefficients(theta, g, n_harmonics=5)
print(np.sum(c**2))                           # -> ~1.0  (== 2*Gamma_rms^2)
```

</details>

<details>
<summary><strong>習題 4 解答</strong>（PSD 積分得相位變異）</summary>

**逐步代入（帶單位）。** phase variance（規範公式 18），代 $S_\phi(f)=K/f^2$：

$$
\sigma_\phi^2=\int_{f_1}^{f_2}\frac{K}{f^2}\,df=K\left[-\frac1f\right]_{f_1}^{f_2}=K\left(\frac{1}{f_1}-\frac{1}{f_2}\right).
$$

代 $K=10^{-4}\ \text{rad}^2\cdot\text{Hz}$、$f_1=10^3$ Hz、$f_2=10^6$ Hz：

$$
\sigma_\phi^2=10^{-4}\left(\frac{1}{10^3}-\frac{1}{10^6}\right)=10^{-4}\times(10^{-3}-10^{-6})=10^{-4}\times9.99\times10^{-4}=9.99\times10^{-8}\ \text{rad}^2.
$$

$$
\sigma_\phi=\sqrt{9.99\times10^{-8}}\approx3.16\times10^{-4}\ \text{rad}=0.316\ \text{mrad}.
$$

**結果**：$\sigma_\phi^2\approx9.99\times10^{-8}\ \text{rad}^2$，$\sigma_\phi\approx0.316$ mrad。

**手感**：$1/f^2$ 積分由**低頻端 $f_1$ 主導**（$1/f_1\gg1/f_2$）——這就是為什麼近載波相位
雜訊對總 jitter 貢獻最大。

**Dimension check**：$[K]\cdot[1/f]=(\text{rad}^2\cdot\text{Hz})\cdot(1/\text{Hz})=\text{rad}^2$ ✓
（$\sigma_\phi^2$ 是 rad²）。

```python
import numpy as np
K, f1, f2 = 1e-4, 1e3, 1e6
var = K*(1/f1 - 1/f2)
print(var, "rad^2 ->", np.sqrt(var)*1e3, "mrad")   # -> 9.99e-8 rad^2 -> 0.316 mrad
```

</details>

<details>
<summary><strong>習題 5 解答</strong>（LTI vs LTV：同 impulse、不同相位）</summary>

**逐步代入（帶單位）。** 用操作型 ISF（規範公式 5）$\Delta\phi=\Gamma(\theta)\,\Delta q/q_{max}$。
$\Delta q/q_{max}=10^{-15}/10^{-12}=10^{-3}$。

**(a) 過零點 $\theta=\pi/2$**（$\Gamma=-\sin(\pi/2)=-1$，敏感度最大）：

$$
\Delta\phi_a=(-1)\times10^{-3}=-1\times10^{-3}\ \text{rad}=-1\ \text{mrad}.
$$

**(b) 峰值 $\theta=0$**（$\Gamma=-\sin 0=0$，敏感度為零）：

$$
\Delta\phi_b=0\times10^{-3}=0\ \text{rad}.
$$

**結果**：在過零點注入造成 $\lvert\Delta\phi\rvert=1$ mrad 的相位跳變；在波峰注入造成 **0** 相位跳變
（該處電荷只改振幅、隨後被 amplitude restoring 拉回）。

**為什麼是 LTV 不是 LTI**：一個 **LTI（線性非時變）**系統的 impulse response 只跟「**經過多久**」
$t-\tau$ 有關，跟「**何時注入**」$\tau$ 無關。但這裡同樣大小的 $\Delta q$，在 $\theta=\pi/2$ 與 $\theta=0$
得到**完全不同**的 $\Delta\phi$——響應顯式依賴**絕對注入相位** $\Gamma(\omega_0\tau)$，這正是
**LTV（線性時變）**的定義特徵（見 [lti_vs_ltv](/02_foundations/lti_vs_ltv)）。

**Dimension check**：$\Gamma$ 無因次 $\times\ \Delta q/q_{max}$（C/C 無因次）$=$ rad ✓。

```python
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
import numpy as np
dq, qmax = 1e-15, 1e-12
for name, theta in [("zero-crossing", np.pi/2), ("peak", 0.0)]:
    g = gamma_lc_ideal(theta)                       # -sin(theta)
    dphi = impulse_to_phase_step(dq, g, qmax)
    print(name, dphi*1e3, "mrad")                   # -> -1.0 mrad ; 0.0 mrad
```

</details>

<details>
<summary><strong>習題 6 解答</strong>（Lorentzian 線寬反推 phase diffusion）</summary>

> 註：Lorentzian 線寬與 phase diffusion 屬**外部文獻**（[E2] Demir 2000），**不在 5 篇 PDF 內**；
> 公式逐字取自規範 11.2。

**(a) 反推 $D$。** FWHM 線寬（規範 11.2）：

$$
\Delta f_{3\mathrm{dB}}=\frac{D}{\pi}\quad\Longrightarrow\quad D=\pi\,\Delta f_{3\mathrm{dB}}=\pi\times10^{3}\ \text{Hz}=3.142\times10^{3}\ \text{rad}^2/\text{s}.
$$

**(b) 估累積到 1 rad² 的時間。** 相位擴散（規範 11.2）$\operatorname{Var}[\Delta\phi(t)]=2D\lvert t\rvert$，令其 $=1\ \text{rad}^2$：

$$
t=\frac{1}{2D}=\frac{1}{2\times3.142\times10^{3}}\approx1.59\times10^{-4}\ \text{s}=159\ \mu\text{s}.
$$

**結果**：$D\approx3.14\times10^{3}\ \text{rad}^2/\text{s}$；相位累積到 $\approx1\ \text{rad}^2$ 約需 **159 µs**
（即相干時間 $\tau_c\sim1/(2D)$ 量級）。注意 $1/\Delta f_{3\mathrm{dB}}=1$ ms 與此同數量級——
**線寬越窄，相干時間越長**，兩者倒數關係。

**Dimension check**：(a) $[\,\Delta f\,]=\text{Hz}=1/\text{s}$，乘 $\pi$（無因次）得 $D$ 的 rad²/s
（rad² 是相位方差的無因次「rad」平方，per second）✓。(b) $\dfrac{\text{rad}^2}{\text{rad}^2/\text{s}}=\text{s}$ ✓。

```python
import numpy as np
df_3db = 1e3                       # Hz (FWHM)
D = np.pi*df_3db                   # rad^2/s
t = 1/(2*D)                        # Var = 2 D t = 1 rad^2
print(D, "rad^2/s ;", t*1e6, "us")   # -> 3141.6 rad^2/s ; 159.2 us
```

（背景與完整推導見 [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)。）

</details>

<details>
<summary><strong>習題 7 解答</strong>（Allan deviation 斜率判讀）</summary>

> 註：Allan variance 屬**外部文獻**（Allan 1966），**不在 5 篇 PDF 內**；斜率對照表逐字取自規範 11.2。

**斜率對照（規範 11.2）。** 在 log–log 的 $\sigma_y(\tau)$ 圖上：

| 量到的斜率 $\sigma_y(\tau)\propto\tau^{?}$ | 對應雜訊型態 | 物理 |
|---|---|---|
| $\tau^{-1/2}$ | **white FM**（white frequency modulation） | 頻率是白噪 → 相位是隨機漫步；平均越久越穩 |
| $\tau^{0}$（平台/floor） | **flicker FM**（1/f frequency） | $\sigma_y$ 與閘門時間 $\tau$ 無關 → ADEV 形成平地板 |
| $\tau^{+1/2}$ | **random-walk FM**（頻率隨機漫步） | 頻率本身漂移 → 平均越久越**差**，斜率上揚 |

**為什麼 flicker FM 形成平台**：把 $S_y(f)\propto1/f$（flicker FM）代入規範 11.2 的
$\sigma_y^2(\tau)=2\displaystyle\int_0^\infty S_y(f)\dfrac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df$，做變數代換
$u=\pi f\tau$，$\tau$ 會從被積函數裡**完全約掉**——積分變成一個與 $\tau$ 無關的純數常數，
所以 $\sigma_y^2(\tau)=$ 常數 $\Rightarrow\sigma_y(\tau)\propto\tau^0$，在 log–log 上是一條**水平線（floor）**。
這個 floor 是石英/原子鐘等長期穩定度的招牌特徵，標定「再怎麼延長平均時間都壓不下去」的底限。

**結果**：$\tau^{-1/2}\to$ white FM、$\tau^{0}\to$ flicker FM（floor）、$\tau^{+1/2}\to$ random-walk FM。

**Dimension check**：$\sigma_y(\tau)$ 是**無因次的分數頻率穩定度**（$y=\Delta f/f_0$），與 $\tau$
的冪次關係只比斜率、本身無量綱 ✓。

```python
import numpy as np
# 用斜率定義判讀：對某段 sigma_y(tau) 取 log-log 斜率
tau = np.logspace(-3, 1, 200)
for label, slope in [("white FM", -0.5), ("flicker FM", 0.0), ("random-walk FM", 0.5)]:
    sy = tau**slope
    fit = np.polyfit(np.log10(tau), np.log10(sy), 1)[0]
    print(label, "slope =", round(fit, 2))   # -> -0.5 ; 0.0 ; 0.5
```

（完整推導與圖見 [allan_variance](/02_foundations/allan_variance)。）

</details>

<details>
<summary><strong>習題 8 解答</strong>（由 $\mathcal{L}$ 換 $S_\phi$ 再換單音 jitter）</summary>

**(a) $\mathcal{L}\to S_\phi$。** 先把 dBc/Hz 還原成 linear：

$$
\mathcal{L}_{\text{lin}}(1\,\text{MHz})=10^{-120/10}=10^{-12}\ \text{(per Hz)}.
$$

小角關係（規範公式 16）$\mathcal{L}\approx\tfrac12 S_\phi\Rightarrow S_\phi=2\mathcal{L}_{\text{lin}}$：

$$
S_\phi(1\,\text{MHz})=2\times10^{-12}=2\times10^{-12}\ \text{rad}^2/\text{Hz}.
$$

**(b) 定 $K$ 再積分得 $\sigma_t$。** $1/f^2$ 模型 $S_\phi(f)=K/f^2$，用 (a) 在 $f=10^6$ Hz 定 $K$：

$$
K=S_\phi(10^6)\cdot(10^6)^2=2\times10^{-12}\times10^{12}=2\ \text{rad}^2\cdot\text{Hz}.
$$

相位變異（規範公式 18），積分 $f_1=10^6\to f_2=10^7$ Hz：

$$
\sigma_\phi^2=\int_{f_1}^{f_2}\frac{K}{f^2}df=K\!\left(\frac{1}{f_1}-\frac{1}{f_2}\right)=2\left(\frac{1}{10^6}-\frac{1}{10^7}\right)=2\times9\times10^{-7}=1.8\times10^{-6}\ \text{rad}^2.
$$

$$
\sigma_\phi=\sqrt{1.8\times10^{-6}}\approx1.342\times10^{-3}\ \text{rad}=1.342\ \text{mrad}.
$$

rms jitter（規範公式 19），$f_0=5$ GHz：

$$
\sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{1.342\times10^{-3}}{2\pi\times5\times10^{9}}\approx4.27\times10^{-14}\ \text{s}=42.7\ \text{fs}.
$$

**結果**：$S_\phi(1\text{MHz})=2\times10^{-12}\ \text{rad}^2/\text{Hz}$、$\sigma_\phi\approx1.34$ mrad、
$\sigma_t\approx42.7$ fs（1→10 MHz 頻段）。

**Dimension check**：(a) $\mathcal{L}$、$S_\phi$ 都是 per-Hz（rad²/Hz）✓；
(b) $[K]\cdot[1/f]=\text{rad}^2\cdot\text{Hz}\cdot\text{Hz}^{-1}=\text{rad}^2$ ✓；$\dfrac{\text{rad}}{\text{rad/s}}=\text{s}$ ✓。

```python
import numpy as np
from simulations.common.noise_utils import integrate_rms_jitter
# 解析路徑（直接代式）
L_dbc = -120.0
S_phi_1M = 2*10**(L_dbc/10)              # = 2e-12 rad^2/Hz
K = S_phi_1M*(1e6)**2                    # = 2 rad^2*Hz
var = K*(1/1e6 - 1/1e7)
sigma_phi = np.sqrt(var)
sigma_t = sigma_phi/(2*np.pi*5e9)
print(sigma_phi*1e3, "mrad ;", sigma_t*1e15, "fs")   # -> 1.342 mrad ; 42.7 fs

# 數值路徑（用 L(f)=K/f^2 折回 dBc/Hz 後積分），與解析一致
f = np.logspace(6, 7, 2000)
L_curve = 10*np.log10(0.5*K/f**2)        # L = S_phi/2 = (K/f^2)/2
st, sp = integrate_rms_jitter(f, L_curve, f0=5e9, fmin=1e6, fmax=1e7)
print(st*1e15, "fs (numeric)")           # -> ~42.7 fs
```

</details>

---

## 重點回顧

- **phase↔time**：$\Delta t=\Delta\phi/(2\pi f_0)$；rms 版 $\sigma_t=\sigma_\phi/(2\pi f_0)$（習題 1、2）。
- **Parseval**：$\sum c_n^2=2\Gamma_{rms}^2$；$-\sin$ 的 $\Gamma_{rms}=1/\sqrt2$、$\sum c_n^2=1$（習題 3）。
- **PSD 積分**：$1/f^2$ 區的 $\sigma_\phi^2$ 由**低頻端**主導；$\sigma_\phi^2=K(1/f_1-1/f_2)$（習題 4、8）。
- **LTV 本質**：響應依**絕對注入相位**，同 impulse 不同相位給不同 $\Delta\phi$（習題 5）。
- **Lorentzian**：$D=\pi\Delta f_{3\mathrm{dB}}$、相干時間 $\sim1/(2D)$（習題 6，外部文獻）。
- **Allan 斜率**：$\tau^{-1/2}/\tau^0/\tau^{+1/2}\to$ white/flicker/random-walk FM；flicker FM 形成 floor（習題 7，外部文獻）。
- 全部 Python 驗證引用 `simulations/common/`（`noise_utils`、`isf_utils`），可直接重現。

## 延伸閱讀

- 相位/振幅與 jitter 定義：[oscillator_phase](/02_foundations/oscillator_phase)、[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)
- PSD / phase noise / jitter：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- LTI vs LTV：[lti_vs_ltv](/02_foundations/lti_vs_ltv)
- Allan variance：[allan_variance](/02_foundations/allan_variance)
- Lorentzian 線寬：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- 其他習題：[03 核心理論章習題](/03_isf_core_theory/exercises) · [06 設計章習題](/06_design_insights/exercises) · [04 模擬章 worked examples](/04_simulation_labs/worked_examples)
