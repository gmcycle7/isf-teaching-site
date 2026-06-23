---
title: Worked Examples 例題庫
description: 15 道分級例題（基礎換算、ISF→phase noise、jitter 積分、設計反推），每題逐步解、帶單位、dimension check、一行 Python 驗證。
---

# Worked Examples 例題庫

這頁是 ISF / phase noise / jitter 的**動手例題庫**。理論頁教你公式怎麼來，這裡教你
**把數字代進去、算到底、檢查單位、用一行 Python 驗證**。所有公式都從
[AUTHORING_SPEC 權威公式表] 逐字沿用，數值以
[numerical_feeling](/04_simulation_labs/numerical_feeling) 與規範第 8 節 canonical
為主（$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、$f_0=5$ GHz、$\mathcal{L}(1\text{MHz})=-100$ dBc/Hz）。

> **怎麼用這頁**：先遮住「逐步解」，自己算一遍，再對答案。類比設計師的核心能力是
> **在白板上估數量級**——看到「$-100$ dBc/Hz @ 1 MHz、5 GHz」要能 30 秒內喊出
> 「幾百 fs jitter」。每題最後的 Python 一行只用來「驗算」，不是用來「代替手算」。

分四級：

- **(A) 基礎換算**：rad ↔ fs、dBc ↔ linear、phase PSD ↔ $\mathcal{L}$。練到變反射動作。
- **(B) ISF → phase noise**：Eq.(21)/(23)/(24) 代數，把 $\Gamma_{rms},c_0,q_{max}$ 代成 dBc/Hz。
- **(C) jitter 積分**：由 $\mathcal{L}(f)$ 積分得 $\sigma_t$；period jitter 的高通核。
- **(D) 設計反推**：要 $-120$ dBc/Hz 需多大 $q_{max}/\Gamma_{rms}$；ring 級數 $N$ 怎麼選。

每題格式固定：**題目 → 逐步解（帶單位）→ 結果 → dimension check → 一行 Python 驗證**。
Python 都引用 `simulations/common/` 的真實函式（見規範第 5 節 API），可直接跑。

---

## A 級：基礎換算

這一級只有兩條核心關係，務必背到底：

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0},\qquad \mathcal{L}_{\text{linear}}=10^{\mathcal{L}_{\text{dBc/Hz}}/10},\qquad S_\phi=2\,\mathcal{L}_{\text{linear}} .
$$

### 例 A1：phase → time（1 mrad 在 5 GHz 是幾 fs？）

> **題目**：$f_0=5$ GHz、$\Delta\phi=1$ mrad，求 timing error $\Delta t$。

**逐步解**

第 1 步，寫出 phase→time 換算（規範公式 17，$\Delta t=\Delta\phi/(2\pi f_0)$）。$2\pi f_0$ 的單位是
rad/s（角頻率），$\Delta\phi$ 是 rad，相除得秒：

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0}=\frac{1\times10^{-3}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{rad/s}} .
$$

第 2 步，算分母：$2\pi\times5\times10^{9}=3.1416\times10^{10}$ rad/s。

$$
\Delta t=\frac{10^{-3}}{3.1416\times10^{10}}\ \text{s}=3.183\times10^{-14}\ \text{s}=31.8\ \text{fs} .
$$

**結果**：$\Delta t\approx31.8$ fs。

**Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。手感記憶點：**5 GHz 下「1 mrad ≈ 32 fs」**；
反過來「1 rad ≈ 31.8 ps」（剛好同樣的 $31.83$ 數字，差 $10^3$ 倍級）。週期 $T=200$ ps，所以
1 mrad 約是週期的 $1.6\times10^{-4}$。

**Python 驗證**

```python
from simulations.common.noise_utils import phase_to_time_error
print(phase_to_time_error(1e-3, 5e9) * 1e15, "fs")   # -> 31.83 fs
```

### 例 A2：dBc/Hz → linear（−100 dBc/Hz 是多少？）

> **題目**：$\mathcal{L}=-100$ dBc/Hz，換成 linear（每 Hz 相對載波的功率比），再還原 phase PSD $S_\phi$。

**逐步解**

第 1 步，dBc/Hz 是 $10\log_{10}(\cdot)$ 的「分貝相對載波」單位，反運算除以 10 再取 10 的次方：

$$
\mathcal{L}_{\text{linear}}=10^{\mathcal{L}/10}=10^{-100/10}=10^{-10}\ [\text{1/Hz}] .
$$

第 2 步，小角單音 PM 近似下 $\mathcal{L}(f)\approx\tfrac12 S_\phi(f)$（規範公式 16 與第 10.2 節
「$L\approx\tfrac12 S_\phi$」推導），故反推 phase PSD：

$$
S_\phi=2\,\mathcal{L}_{\text{linear}}=2\times10^{-10}\ \text{rad}^2/\text{Hz} .
$$

**結果**：$\mathcal{L}_{\text{linear}}=10^{-10}$／Hz、$S_\phi=2\times10^{-10}$ rad²/Hz。

**Dimension check**：dBc/Hz 是無因次功率比 per Hz；$\mathcal{L}_{\text{linear}}$ 也是 1/Hz；乘 2 後當 phase PSD
讀作 rad²/Hz（rad² 是相位方差的單位，方差密度對 $f$ 積分後得 rad²）✓。**口訣**：每 $-10$ dB
= 線性少一個數量級；每 $-20$ dB = 電壓/相位幅度少一個數量級。

**Python 驗證**

```python
import numpy as np
from simulations.common.noise_utils import phase_psd_to_l_dbc_per_hz
s_phi = 2 * 10**(-100/10)
print(s_phi, "rad^2/Hz")                       # -> 2e-10
print(phase_psd_to_l_dbc_per_hz(s_phi), "dBc/Hz")  # -> -100.0 (來回一致)
```

### 例 A3：injected charge → phase step → time（1 fC 踢一下）

> **題目**（canonical 例 A）：$q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$、$f_0=5$ GHz。
> 求單一脈衝造成的 phase step $\Delta\phi$ 與 timing error $\Delta t$。

**逐步解**

第 1 步，用 ISF 操作型定義（規範公式 5，$\Delta\phi=\Gamma(\omega_0\tau)\,\Delta q/q_{max}$）。
$\Gamma$ 無因次、$\Delta q/q_{max}$ 無因次，所以 $\Delta\phi$ 是純數（rad）：

$$
\Delta\phi=\frac{\Gamma\,\Delta q}{q_{max}}=\frac{0.5\times(1\times10^{-15}\ \text{C})}{1\times10^{-12}\ \text{C}}=5\times10^{-4}\ \text{rad} .
$$

換成度：$5\times10^{-4}\times\dfrac{180}{\pi}\approx0.0286^\circ$。

第 2 步，用 A1 的換算轉成時間（$f_0=5$ GHz）：

$$
\Delta t=\frac{5\times10^{-4}}{2\pi\times5\times10^{9}}\ \text{s}\approx1.59\times10^{-14}\ \text{s}=15.9\ \text{fs} .
$$

**結果**：$\Delta\phi=5\times10^{-4}$ rad（$0.0286^\circ$）、$\Delta t\approx15.9$ fs。

**Dimension check**：$\Delta\phi$：$[\text{C}]/[\text{C}]=$ 無因次 ✓；$\Delta t$：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。
**手感**：1 fC ≈ 6240 個電子；在最敏感相位也只踢出 ~16 fs。單顆很小，但 noise **持續**踢、
會被相位積分器累積（見 [convolution_derivation](/03_isf_core_theory/convolution_derivation)）。

**Python 驗證**

```python
from simulations.common.isf_utils import impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error
dphi = impulse_to_phase_step(delta_q=1e-15, gamma_value=0.5, qmax=1e-12)
print(dphi, "rad ->", phase_to_time_error(dphi, 5e9)*1e15, "fs")  # 0.0005 rad -> 15.92 fs
```

### 例 A4：相位敏感度隨注入相位變（LTV 的味道）

> **題目**：理想 LC 振盪器 ISF 為 $\Gamma(\theta)=-\sin\theta$。同樣 $\Delta q=1$ fC、$q_{max}=1$ pC，
> 分別在 zero-crossing（$\theta=\pi/2$，波形斜率最大）與 peak（$\theta=0$，波形頂點）注入，
> 求各自的 $\Delta\phi$。

**逐步解**

第 1 步，先取兩處 ISF 值。注意這裡的相位約定：$V\propto\cos\theta$ 時波峰在 $\theta=0$、
zero-crossing（下降沿）在 $\theta=\pi/2$，理想 LC 的 $\Gamma=-\sin\theta$：

$$
\Gamma(\theta=\pi/2)=-\sin\tfrac{\pi}{2}=-1,\qquad \Gamma(\theta=0)=-\sin 0=0 .
$$

第 2 步，各代入 $\Delta\phi=\Gamma\,\Delta q/q_{max}$（$\Delta q/q_{max}=10^{-15}/10^{-12}=10^{-3}$）：

$$
\Delta\phi_{\text{ZC}}=(-1)(10^{-3})=-1\times10^{-3}\ \text{rad},\qquad
\Delta\phi_{\text{peak}}=(0)(10^{-3})=0\ \text{rad}.
$$

**結果**：在 zero-crossing 注入 → $-1$ mrad（最大相位效應）；在 peak 注入 → 0 rad（**純改振幅、不改相位**）。

**Dimension check**：兩者皆 $[\,]\cdot[\text{C}]/[\text{C}]=$ rad ✓。**這就是 LTV（線性時變）的本質**：
同一個 impulse，效果取決於「踢在波形的哪個相位」。peak 處 $\Gamma=0$ 是因為那裡只有徑向（振幅）
擾動、沒有切向（相位）分量，而振幅會被 restoring 拉回。見
[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)。

**Python 驗證**

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
for name, th in [("ZC", np.pi/2), ("peak", 0.0)]:
    g = gamma_lc_ideal(th)                       # = -sin(theta)
    print(name, impulse_to_phase_step(1e-15, g, 1e-12), "rad")
# ZC -0.001 rad ; peak 0.0 rad
```

---

## B 級：ISF → phase noise（代數）

這一級反覆用三條招牌公式（全部 [P1]，逐字沿用規範第 3 節）：

- **白噪 1/f²** [P1] Eq.(21), p.185：
  $\mathcal{L}=10\log_{10}\!\big(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\Delta\omega^2}\big)$
- **flicker 1/f³** [P1] Eq.(23), p.185：含 $c_0^2$ 與 $\omega_{1/f}/\Delta\omega$ 因子。
- **1/f³ corner** [P1] Eq.(24), p.185：$\Delta\omega_{1/f^3}=\omega_{1/f}\,c_0^2/(2\Gamma_{rms}^2)$。

> 提醒：Eq.(21) 的分母是 $4\Delta\omega^2$（SSB 記帳慣例）。時域乾淨推導會得到 $2\Delta\omega^2$，
> 差的 2 倍是文獻上著名的小爭議，**不影響** $\Gamma_{rms}^2/q_{max}^2$ scaling 與 $-20$ dB/dec 斜率。
> 詳見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。本頁一律用 [P1] 原式的 $4\Delta\omega^2$。

### 例 B1：白噪 → L（canonical 例 B，逐位算到底）

> **題目**：$f_0=5$ GHz、$\Delta f=1$ MHz offset、$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、
> 白噪 $\overline{i_n^2}/\Delta f=S_i=10^{-24}$ A²/Hz。用 Eq.(21) 求 $\mathcal{L}(1\text{MHz})$。

**逐步解**

第 1 步，把 offset 頻率換成角頻率：$\Delta\omega=2\pi\Delta f=2\pi\times10^{6}=6.283\times10^{6}$ rad/s，
$\Delta\omega^2=3.948\times10^{13}\ (\text{rad/s})^2$。

第 2 步，算 Eq.(21) 括號內的值（先把無因次與帶單位部分分開）：

$$
\frac{\Gamma_{rms}^2}{q_{max}^2}=\frac{0.25}{(10^{-12})^2}=0.25\times10^{24}=2.5\times10^{23}\ \text{C}^{-2} .
$$

$$
\frac{S_i}{4\Delta\omega^2}=\frac{10^{-24}}{4\times3.948\times10^{13}}=\frac{10^{-24}}{1.579\times10^{14}}=6.333\times10^{-39}\ \text{A}^2/\text{Hz}\cdot\text{s}^2 .
$$

第 3 步，相乘（單位下面再 check）：

$$
2.5\times10^{23}\times6.333\times10^{-39}=1.583\times10^{-15} .
$$

第 4 步，取 $10\log_{10}$：

$$
\mathcal{L}=10\log_{10}(1.583\times10^{-15})=-148.0\ \text{dBc/Hz} .
$$

**結果**：$\mathcal{L}(1\text{MHz})=-148.0$ dBc/Hz。

**Dimension check**：括號內必須無因次（log 的引數）。
$[\text{C}^{-2}]\cdot[\text{A}^2\,\text{Hz}^{-1}\,\text{s}^2]$；用 $\text{A}=\text{C/s}$ ⇒ $\text{A}^2=\text{C}^2/\text{s}^2$，
$\text{Hz}^{-1}=\text{s}$，整理 $\text{C}^{-2}\cdot(\text{C}^2/\text{s}^2)\cdot\text{s}\cdot\text{s}^2=\text{C}^{-2}\cdot\text{C}^2\cdot\text{s}^{-2}\cdot\text{s}^{3}=\text{s}$。
還差一個 $1/\text{s}$——它來自 PSD 的「per Hz」本質：結果是「每 Hz 的相對功率」，故引數實為 1/Hz，取 log 後是 dBc/Hz ✓。
（這就是為何單位很容易看走眼；記住「最終是 dBc/**Hz**」即可。）

**手感**：這是「**單一理想白噪源**」的下限。真實電路有多個 noise 源、cyclostationary、flicker，
實測會比這高出數十 dB。

**Python 驗證**

```python
import numpy as np
Grms, qmax, Si = 0.5, 1e-12, 1e-24
dw = 2*np.pi*1e6
L = 10*np.log10((Grms**2/qmax**2) * (Si/(4*dw**2)))
print(round(L, 2), "dBc/Hz")    # -> -148.0
```

### 例 B2：用 Parseval 從 $c_n$ 求 $\Gamma_{rms}$，再算 L

> **題目**：理想 LC 的 ISF 純粹是 $\Gamma(\theta)=-\sin\theta$，即只有一階諧波 $c_1=1$、其餘 $c_n=0$。
> （a）用 Parseval（Eq.(20)）求 $\Gamma_{rms}$；（b）若 $q_{max}=1$ pC、$S_i=10^{-24}$、$\Delta f=1$ MHz，求 L。

**逐步解**

第 1 步（a），Parseval（[P1] Eq.(20)）：$\sum_n c_n^2=2\Gamma_{rms}^2$。這裡 $\sum_n c_n^2=c_1^2=1$，故

$$
2\Gamma_{rms}^2=1\ \Rightarrow\ \Gamma_{rms}=\frac{1}{\sqrt2}\approx0.707 .
$$

（直接驗：$\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta=\tfrac12$，亦得 $\Gamma_{rms}=1/\sqrt2$ ✓。）

第 2 步（b），代 Eq.(21)，$\Gamma_{rms}^2=0.5$：

$$
\mathcal{L}=10\log_{10}\!\left(\frac{0.5}{(10^{-12})^2}\cdot\frac{10^{-24}}{4\times3.948\times10^{13}}\right)
=10\log_{10}(3.166\times10^{-15})=-145.0\ \text{dBc/Hz} .
$$

**結果**：$\Gamma_{rms}=0.707$；$\mathcal{L}(1\text{MHz})=-145.0$ dBc/Hz。

**Dimension check**：$\Gamma_{rms}$ 無因次（$c_n$ 無因次）✓；L 同例 B1，dBc/Hz ✓。
注意 $\Gamma_{rms}=0.707$ 比 canonical 的 $0.5$ 大，故 L 比 B1 高約 $3$ dB（$10\log_{10}(0.5/0.25)=3$ dB），
合理。

**Python 驗證**

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, gamma_rms
theta = np.linspace(0, 2*np.pi, 100000, endpoint=False)
Grms = gamma_rms(theta, gamma_lc_ideal(theta))
print("Grms =", round(Grms, 4))                       # -> 0.7071
L = 10*np.log10((Grms**2/(1e-12)**2)*(1e-24/(4*(2*np.pi*1e6)**2)))
print(round(L, 2), "dBc/Hz")                           # -> -145.0
```

### 例 B3：對稱性與 1/f³（$c_0$ 的角色）

> **題目**：兩顆振盪器，白噪與 $q_{max}$ 相同，$\omega_{1/f}=2\pi\times1$ MHz。A 波形完全對稱（$c_0=0$），
> B 略不對稱（$c_0=0.2$，$c_1=1$）。問：哪顆有 close-in 1/f³ 上轉？在 $\Delta f=10$ kHz 各自的 1/f³ 貢獻如何？

**逐步解**

第 1 步，看 Eq.(23)：1/f³ 區的 phase noise 正比於 $c_0^2$。

$$
\mathcal{L}_{1/f^3}=10\log_{10}\!\left(\frac{c_0^2}{q_{max}^2}\cdot\frac{S_i}{8\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}\right) .
$$

第 2 步，對 A：$c_0=0\Rightarrow$ 括號 $=0\Rightarrow \mathcal{L}_{1/f^3}\to-\infty$ dBc/Hz（**沒有** flicker 上轉，
1/f³ 區被完全抑制）。實務上不會真的 $-\infty$（其他機制接手），但相對 B 可低非常多。

第 3 步，對 B：$c_0=0.2$，有限值。用 Eq.(24) 比較兩者的 1/f³ corner：

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\Gamma_{rms}^2} .
$$

對 B，$\sum c_n^2=c_0^2+c_1^2=0.04+1=1.04\Rightarrow\Gamma_{rms}^2=0.52$，故

$$
\Delta\omega_{1/f^3,B}=\omega_{1/f}\cdot\frac{0.04}{2\times0.52}=\omega_{1/f}\times0.0385 .
$$

即 B 的 1/f³ corner 在 $\approx0.0385\,\omega_{1/f}=2\pi\times38.5$ kHz。對 A，corner $\to0$。

**結果**：A（對稱、$c_0=0$）**沒有** 1/f³ 上轉；B（$c_0=0.2$）有，corner 約 $38.5$ kHz。
**設計守則**：靠波形對稱性壓低 $c_0$，就能把 1/f³ corner 推到遠低於 device 的 $\omega_{1/f}$。

**Dimension check**：Eq.(24) 中 $c_0^2/\Gamma_{rms}^2$ 無因次，乘 $\omega_{1/f}$（rad/s）得 rad/s ✓。

**Python 驗證**

```python
import numpy as np
w_1f = 2*np.pi*1e6
for name, c0, c1 in [("A", 0.0, 1.0), ("B", 0.2, 1.0)]:
    Grms2 = 0.5*(c0**2 + c1**2)          # Parseval: sum cn^2 = 2 Grms^2
    corner = w_1f * c0**2/(2*Grms2)
    print(name, "1/f^3 corner =", corner/(2*np.pi)*1e-3, "kHz")
# A 0.0 kHz ; B 38.46 kHz
```

### 例 B4：白噪 floor 與 offset 的 −20 dB/dec 斜率

> **題目**：沿用 B1 的振盪器（$\mathcal{L}(1\text{MHz})=-148$ dBc/Hz，1/f² 區）。問 $\Delta f=10$ MHz 時的 L？
> （即把 offset 拉遠 10 倍。）

**逐步解**

第 1 步，Eq.(21) 中 $\mathcal{L}\propto1/\Delta\omega^2$，取 log 後是 $-20\log_{10}\Delta\omega+$const，
即每 offset ×10，L 掉 20 dB（$-20$ dB/decade）。

第 2 步，$\Delta f$ 由 1 MHz → 10 MHz（×10）：

$$
\mathcal{L}(10\text{MHz})=\mathcal{L}(1\text{MHz})-20\log_{10}(10)=-148-20=-168\ \text{dBc/Hz} .
$$

**結果**：$\mathcal{L}(10\text{MHz})=-168$ dBc/Hz。

**Dimension check**：$-20\log_{10}(\Delta f_2/\Delta f_1)$ 的引數無因次（頻率比）✓，結果是 dB 差，加到 dBc/Hz 仍是 dBc/Hz ✓。
**手感**：1/f² 區「每 decade 掉 20 dB」是 phase noise 圖最常用的目視斜率；對照 1/f³ 區是 $-30$ dB/dec。

**Python 驗證**

```python
import numpy as np
Grms, qmax, Si = 0.5, 1e-12, 1e-24
def L(df): return 10*np.log10((Grms**2/qmax**2)*(Si/(4*(2*np.pi*df)**2)))
print(round(L(1e6),2), round(L(10e6),2), "dBc/Hz",
      "slope =", round(L(10e6)-L(1e6),1), "dB/dec")   # -148.0 -168.0 ; -20.0
```

---

## C 級：jitter 積分

核心：phase noise 是頻域密度，jitter 是時域的 rms，兩者用「積分 + 開根號 + $\div(2\pi f_0)$」連起來
（規範公式 18、19）：

$$
\sigma_\phi^2=\int_{f_1}^{f_2}S_\phi(f)\,df,\qquad \sigma_t=\frac{\sigma_\phi}{2\pi f_0} .
$$

### 例 C1：L(f) → rms jitter（canonical 例 C，1/f² 積分）

> **題目**：$\mathcal{L}(1\text{MHz})=-100$ dBc/Hz、1/f² 斜率、由 $f_1=1$ MHz 積到 $f_2=100$ MHz、
> $f_0=5$ GHz，求 $\sigma_\phi$ 與 $\sigma_t$。

**逐步解**

第 1 步，把 datasheet 點換成 phase PSD（用 A2）：$S_\phi(f_{ref})=2\times10^{-10}$ rad²/Hz，$f_{ref}=1$ MHz。

第 2 步，寫 1/f² 形狀（以 $f_{ref}$ 錨定）：

$$
S_\phi(f)=S_\phi(f_{ref})\left(\frac{f_{ref}}{f}\right)^2=2\times10^{-10}\,(10^6)^2\,\frac1{f^2} .
$$

第 3 步，積分（$\int f^{-2}df=-1/f$）：

$$
\sigma_\phi^2=2\times10^{-10}(10^6)^2\!\int_{10^6}^{10^8}\!\frac{df}{f^2}
=2\times10^{2}\left(\frac1{10^6}-\frac1{10^8}\right)=200\times9.9\times10^{-7}=1.98\times10^{-4}\ \text{rad}^2 .
$$

故 $\sigma_\phi=\sqrt{1.98\times10^{-4}}=1.407\times10^{-2}$ rad $=14.07$ mrad。

第 4 步，換成 rms jitter（$f_0=5$ GHz）：

$$
\sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{1.407\times10^{-2}}{2\pi\times5\times10^{9}}\approx4.48\times10^{-13}\ \text{s}=447.9\ \text{fs} .
$$

**結果**：$\sigma_\phi=14.07$ mrad、$\sigma_t=447.9$ fs。

**Dimension check**：$\sigma_\phi^2$：$[\text{rad}^2/\text{Hz}]\cdot[\text{Hz}]=\text{rad}^2$ ✓；$\sigma_t$：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。
**手感**：1/f² 積分**被下限 $f_1$ 主導**（$1/f_1\gg1/f_2$）——「從哪裡開始積」對結果最關鍵。
若改成 $-120$ dBc/Hz @ 1 MHz（好 20 dB = 功率 1/100、幅度 1/10），jitter 縮到 ~45 fs。

![由 L(f) 積分得 rms jitter](/figures/phase_noise_to_jitter_integration.png)

**Python 驗證**

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter
f = np.logspace(6, 8, 4000)                              # 1 MHz -> 100 MHz
L = leeson_one_over_f2(f, L_ref_dbc=-100, f_ref=1e6)     # 1/f^2 skirt
sigma_t, sigma_phi = integrate_rms_jitter(f, L, f0=5e9, fmin=1e6, fmax=100e6)
print(round(sigma_phi*1e3,2), "mrad ;", round(sigma_t*1e15,1), "fs")  # 14.07 mrad ; 447.9 fs
```

### 例 C2：積分下限主導——換下限會怎樣？

> **題目**：同 C1 的譜（$-100$ dBc/Hz @ 1 MHz、1/f²、$f_0=5$ GHz），但改成從 $f_1=100$ kHz 積到 100 MHz。
> 估 $\sigma_t$，並和 C1 比較。

**逐步解**

第 1 步，1/f² 的 $\sigma_\phi^2\propto(1/f_1-1/f_2)\approx1/f_1$（下限主導）。下限由 $10^6$ 變 $10^5$（小 10 倍），
$1/f_1$ 大 10 倍：

$$
\sigma_\phi^2\approx2\times10^{2}\left(\frac1{10^5}-\frac1{10^8}\right)=200\times(10^{-5}-10^{-8})\approx2.0\times10^{-3}\ \text{rad}^2 .
$$

第 2 步，$\sigma_\phi=\sqrt{2.0\times10^{-3}}=4.47\times10^{-2}$ rad $=44.7$ mrad（約 C1 的 $\sqrt{10}\approx3.16$ 倍）。

第 3 步，$\sigma_t=\dfrac{4.47\times10^{-2}}{2\pi\times5\times10^{9}}\approx1.42\times10^{-12}$ s $=1.42$ ps。

**結果**：$\sigma_t\approx1.42$ ps（C1 是 448 fs）。下限降 10 倍 → jitter 約增 $\sqrt{10}\approx3.16$ 倍。

**Dimension check**：同 C1 ✓。**手感**：這就是為什麼「rms jitter」一定要附上**積分頻段**才有意義；
量測儀器的下限（或 PLL 的迴路頻寬）決定你「看得到多少」累積 jitter。

**Python 驗證**

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter
f = np.logspace(5, 8, 6000)                              # 100 kHz -> 100 MHz
L = leeson_one_over_f2(f, L_ref_dbc=-100, f_ref=1e6)
sigma_t, sigma_phi = integrate_rms_jitter(f, L, f0=5e9, fmin=1e5, fmax=100e6)
print(round(sigma_phi*1e3,1), "mrad ;", round(sigma_t*1e12,2), "ps")  # ~44.7 mrad ; ~1.42 ps
```

### 例 C3：period jitter 的高通核

> **題目**：period jitter（單一週期長度的偏差 $T_k-T$）是相位的一階差分。用規範第 10.2 節的核
> $\lvert1-e^{-j2\pi fT}\rvert^2$，對 C1 的譜（$-100$ dBc/Hz @ 1 MHz、1/f²、$f_0=5$ GHz、$T=200$ ps）
> 估 period jitter $\sigma_T$。

**逐步解**

第 1 步，寫出 period jitter 公式（規範第 10.2 節 period/cycle-to-cycle 核）：

$$
\sigma_T^2=\frac1{(2\pi f_0)^2}\int_0^{\infty}S_\phi(f)\,\lvert1-e^{-j2\pi fT}\rvert^2\,df .
$$

第 2 步，理解核的作用：$\lvert1-e^{-j2\pi fT}\rvert^2=2(1-\cos2\pi fT)=4\sin^2(\pi fT)$ 是**高通**——
低頻（$fT\ll1$）被壓掉（$\propto f^2$），所以 period jitter **不被低頻 1/f² 的下限主導**（和 C1/C2 的累積 jitter 相反）。
這就是為什麼 period jitter 通常比同譜的「accumulated jitter」小很多。

第 3 步，數值積分（手算不可行，直接交給電腦；常數已對齊規範核）。結果見下方 Python：$\sigma_T\approx27.6$ fs。

**結果**：$\sigma_T\approx27.6$ fs（對照 C1 的累積 $\sigma_t=448$ fs，小一個量級以上）。

**Dimension check**：核 $\lvert1-e^{-j2\pi fT}\rvert^2$ 無因次；$\int S_\phi\,(\text{核})\,df$ 得 rad²；
除 $(2\pi f_0)^2$ 的 $(\text{rad/s})^2$… 注意這裡先得 rad² 再除 $(2\pi f_0)^2$ 得 s²，開根號得 s ✓。
**TODO: manual verification needed**——period/cycle-to-cycle jitter 的確切前置常數（與單邊/雙邊譜慣例有關）
請對照標準文獻再確認；此處用規範第 10.2 節給的核，數值僅供量級手感。

**Python 驗證**

```python
import numpy as np
T, f0, fref, Lref = 1/5e9, 5e9, 1e6, -100
f = np.logspace(3, 10, 2_000_000)                        # 寬頻段：高通核會壓掉低頻
S_phi = 2 * 10**((Lref + 20*np.log10(fref/f))/10)        # 1/f^2 phase PSD
kernel = np.abs(1 - np.exp(-1j*2*np.pi*f*T))**2          # 一階差分高通核
trapz = getattr(np, "trapezoid", np.trapz)
sigma_T = np.sqrt(trapz(S_phi*kernel, f)) / (2*np.pi*f0)
print(round(sigma_T*1e15, 1), "fs")                      # ~27.6 fs
```

### 例 C4：ring 累積 jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$

> **題目**（[P2] Eq.(8)）：某 ring 的 jitter 比例常數 $\kappa=1\times10^{-8}\ \sqrt{\text{s}}$（toy 數值）。
> 求量測間隔 $\Delta t=1\ \mu$s 與 $\Delta t=1$ ms 的累積 rms jitter。

**逐步解**

第 1 步，random-walk 律（[P2] Eq.(8)，無絕對時間參考的振盪器特徵）：$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$。

第 2 步，$\Delta t=10^{-6}$ s：

$$
\sigma_{\Delta t}=10^{-8}\sqrt{10^{-6}}=10^{-8}\times10^{-3}=10^{-11}\ \text{s}=10\ \text{ps} .
$$

第 3 步，$\Delta t=10^{-3}$ s：

$$
\sigma_{\Delta t}=10^{-8}\sqrt{10^{-3}}=10^{-8}\times3.162\times10^{-2}=3.16\times10^{-10}\ \text{s}=316\ \text{ps} .
$$

**結果**：1 μs → 10 ps；1 ms → 316 ps。間隔 ×1000，jitter ×$\sqrt{1000}\approx31.6$。

**Dimension check**：$\kappa$ 的單位 $\sqrt{\text{s}}$，$\sqrt{\Delta t}$ 是 $\sqrt{\text{s}}$，相乘得 s ✓
（這也是 $\kappa$ 為何取那個怪單位的原因）。**手感**：ring（無高 Q tank）的相位是純隨機漫步，
等得越久誤差越大、且**永不收斂**——這正是 ring 比 LC 更「吵」的時域圖像。對照圖：

![ring 累積 jitter 隨機漫步](/figures/ring_oscillator_timing_noise_accumulation.png)

**Python 驗證**

```python
import numpy as np
kappa = 1e-8                                  # sqrt(s)
for dt in [1e-6, 1e-3]:
    print(dt, "s ->", kappa*np.sqrt(dt)*1e12, "ps")
# 1e-06 s -> 10.0 ps ; 0.001 s -> 316.2 ps
```

---

## D 級：設計反推

把公式倒過來用：**給規格，求需要多少 $q_{max}$、多小 $\Gamma_{rms}$、多少級 $N$。**

### 例 D1：要 −120 dBc/Hz @ 1 MHz，$q_{max}$ 要多大？

> **題目**：規格 $\mathcal{L}(1\text{MHz})=-120$ dBc/Hz、$f_0=5$ GHz。假設單一白噪源
> $S_i=1\times10^{-21}$ A²/Hz（比 canonical 大 1000 倍，較接近真實節點注入）、$\Gamma_{rms}=0.5$。
> 反推所需 $q_{max}$。

**逐步解**

第 1 步，從 Eq.(21) 解 $q_{max}$。先把規格換 linear：$\mathcal{L}_{\text{lin}}=10^{-120/10}=10^{-12}$。

$$
10^{-12}=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{4\Delta\omega^2}
\ \Rightarrow\ q_{max}^2=\frac{\Gamma_{rms}^2\,S_i}{4\Delta\omega^2\,\mathcal{L}_{\text{lin}}} .
$$

第 2 步，代數值（$\Delta\omega^2=3.948\times10^{13}$，$\Gamma_{rms}^2=0.25$）：

$$
q_{max}^2=\frac{0.25\times10^{-21}}{4\times3.948\times10^{13}\times10^{-12}}
=\frac{0.25\times10^{-21}}{1.579\times10^{2}}=1.583\times10^{-24}\ \text{C}^2 .
$$

第 3 步，開根號：$q_{max}=\sqrt{1.583\times10^{-24}}=1.258\times10^{-12}$ C $=1.26$ pC。

**結果**：$q_{max}\approx1.26$ pC（即把 canonical 的 1 pC 提升約 26%，配合此噪聲位準即可達標）。

**Dimension check**：$q_{max}^2$：$[\,]\cdot[\text{A}^2\text{Hz}^{-1}]/([\text{rad/s}]^2\cdot[\,])$；
用 $\text{A}^2\text{Hz}^{-1}=\text{C}^2\text{s}^{-2}\cdot\text{s}=\text{C}^2\text{s}^{-1}$，除 $\text{s}^{-2}$ 得 $\text{C}^2\text{s}$，
再吸收 PSD 的 per-Hz 後為 $\text{C}^2$ ✓。**設計手感**：$\mathcal{L}\propto1/q_{max}^2$，所以
**$q_{max}$ 加倍 → phase noise 降 6 dB**。增大 $q_{max}=C_{node}V_{max}$ 的方法：加大擺幅 $V_{max}$ 或節點電容/電流。

**Python 驗證**

```python
import numpy as np
Grms, Si, dw, Llin = 0.5, 1e-21, 2*np.pi*1e6, 10**(-120/10)
qmax = np.sqrt(Grms**2 * Si / (4*dw**2 * Llin))
print(round(qmax*1e12, 3), "pC")     # -> 1.258 pC
```

### 例 D2：固定 $q_{max}$，要 −120 dBc/Hz 需多小 $\Gamma_{rms}$？

> **題目**：同 D1 規格與噪聲（$-120$ dBc/Hz、$S_i=10^{-21}$、$\Delta f=1$ MHz、$f_0=5$ GHz），但這次
> $q_{max}=1$ pC 固定（不能再加大擺幅）。反推所需 $\Gamma_{rms}$。

**逐步解**

第 1 步，從 Eq.(21) 解 $\Gamma_{rms}$：

$$
\Gamma_{rms}^2=\frac{\mathcal{L}_{\text{lin}}\,q_{max}^2\,4\Delta\omega^2}{S_i}
=\frac{10^{-12}\times(10^{-12})^2\times4\times3.948\times10^{13}}{10^{-21}} .
$$

第 2 步，逐項算分子：$10^{-12}\times10^{-24}=10^{-36}$；$\times1.579\times10^{14}=1.579\times10^{-22}$。
除 $10^{-21}$：$\Gamma_{rms}^2=0.1579$。

第 3 步，$\Gamma_{rms}=\sqrt{0.1579}=0.397$。

**結果**：$\Gamma_{rms}\approx0.40$（須把 ISF rms 從 0.5 降到 0.40，約降 20%）。

**Dimension check**：$\Gamma_{rms}^2$ 無因次（同 B1 引數分析，所有帶單位項相消）✓。
**設計手感**：$\mathcal{L}\propto\Gamma_{rms}^2$，**$\Gamma_{rms}$ 減半 → phase noise 降 6 dB**。
降 $\Gamma_{rms}$ 的手段：波形對稱（壓 $c_0$）、把 noise 注入安排在 ISF 小的相位、ring 增加級數（見 D3）。
D1（調 $q_{max}$）與 D2（調 $\Gamma_{rms}$）是達同一規格的兩個獨立旋鈕。

**Python 驗證**

```python
import numpy as np
qmax, Si, dw, Llin = 1e-12, 1e-21, 2*np.pi*1e6, 10**(-120/10)
Grms = np.sqrt(Llin * qmax**2 * 4*dw**2 / Si)
print(round(Grms, 3))     # -> 0.397
```

### 例 D3：ring 級數 $N$ 的選擇（頻率 vs ISF）

> **題目**：要做 $f_0=5$ GHz single-ended ring。（a）若每級延遲 $\tau_D=20$ ps，需幾級 $N$？
> （b）若把級數從 $N=5$ 增到 $N=15$（同時調 $\tau_D$ 維持 $f_0$），用 $\Gamma_{rms}\propto N^{-3/4}$
> 估 phase noise 改變幾 dB（只看 $\Gamma_{rms}$ 這個因子）？

**逐步解**

第 1 步（a），ring 頻率（[P2] Eq.(15)）：$f_0=\dfrac1{2N\tau_D}\Rightarrow N=\dfrac1{2f_0\tau_D}$。

$$
N=\frac1{2\times5\times10^{9}\times20\times10^{-12}}=\frac1{0.2}=5 .
$$

第 2 步（b），$\Gamma_{rms}\propto N^{-3/4}$（[P2] Eq.(16), p.794，已核實；scaling 為主）。比值：

$$
\frac{\Gamma_{rms}(15)}{\Gamma_{rms}(5)}=\left(\frac{15}{5}\right)^{-3/2}=3^{-1.5}=0.1925 .
$$

第 3 步，phase noise $\propto\Gamma_{rms}^2$，故改變量（dB）：

$$
\Delta\mathcal{L}=10\log_{10}\!\big(0.1925^2\big)=10\log_{10}(0.0370)=-14.3\ \text{dB} .
$$

**結果**：（a）$N=5$ 級。（b）只看 $\Gamma_{rms}$ 這一項，$N$ 由 5→15 使 phase noise 低約 **14.3 dB**。

**Dimension check**：$N=1/(2f_0\tau_D)$：$1/([\text{Hz}][\text{s}])=1/([\text{s}^{-1}][\text{s}])=$ 無因次 ✓
（$N$ 應為整數，這裡剛好整）。$\Delta\mathcal{L}$：$10\log_{10}$ 的引數是無因次比值 ✓。

> **重要警語**：上面只孤立看了 $\Gamma_{rms}$。[P2] 的完整結論是——**固定 $f_0$ 與總功率 $P$ 時，
> single-ended ring 的 phase noise / jitter 幾乎與 $N$ 無關**（見 [P2] Eq.(23), p.796 的 FOM，已核實）。
> 因為增加 $N$ 雖降 $\Gamma_{rms}$，但同時 noise 源變多、每級擺幅/功率分配改變，互相抵消。
> 所以 D3(b) 的「14.3 dB」是**只變一個因子的教學示意**，不是真實設計可白拿的增益。
> 詳見 [lc_vs_ring](/06_design_insights/lc_vs_ring) 與
> [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)。這是 pedagogical toy scaling，非 transistor-level。

**Python 驗證**

```python
import numpy as np
f0, tauD = 5e9, 20e-12
N = 1/(2*f0*tauD)
print("N =", N)                                   # -> 5.0
ratio = (15/5)**-1.5                               # Grms scaling
print("dPN =", round(10*np.log10(ratio**2), 1), "dB")   # -> -14.3 dB (僅 Grms 因子)
```

### 例 D4：jitter 規格反推 phase noise（SerDes 連結）

> **題目**：某 5 GHz 時脈要求積分 rms jitter $\sigma_t\le100$ fs（積 1 MHz→100 MHz，1/f² 譜）。
> 反推 1 MHz 處需要多低的 $\mathcal{L}$。

**逐步解**

第 1 步，C1 已建立映射：在同積分頻段與 1/f² 形狀下，$\sigma_t\propto\sqrt{\mathcal{L}_{\text{lin}}(f_{ref})}$
（因 $\sigma_\phi^2\propto S_\phi(f_{ref})\propto\mathcal{L}_{\text{lin}}$，再開根號）。C1 的基準：
$\mathcal{L}=-100$ dBc/Hz → $\sigma_t=447.9$ fs。

第 2 步，要把 447.9 fs 降到 100 fs，是 $447.9/100=4.479$ 倍。jitter 是「電壓/幅度」類量，
降 $k$ 倍對應 phase noise 功率降 $k^2$ 倍：

$$
\Delta\mathcal{L}=-20\log_{10}(4.479)=-13.0\ \text{dB} .
$$

第 3 步，所需位準：$-100-13.0=-113.0$ dBc/Hz @ 1 MHz。

**結果**：需 $\mathcal{L}(1\text{MHz})\approx-113$ dBc/Hz（1/f²、積 1→100 MHz）才能達到 $\sigma_t\le100$ fs。

**Dimension check**：$-20\log_{10}(\text{比值})$ 引數無因次 ✓；結果 dB 差加到 dBc/Hz 仍是 dBc/Hz ✓。
**SerDes 連結**：100 fs RJ 在高速 SerDes（例如 UI = 1/(28 Gbps) ≈ 35.7 ps）會直接決定 eye 閉合與 BER；
見 [lab_12](/04_simulation_labs/lab_12_serdes_eye_ber) 與
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

**Python 驗證**

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter
target_fs = 100.0
# 從 -100 基準量出 sigma_t，再用平方反推所需 dBc/Hz
f = np.logspace(6, 8, 4000)
L0 = leeson_one_over_f2(f, L_ref_dbc=-100, f_ref=1e6)
st0, _ = integrate_rms_jitter(f, L0, f0=5e9, fmin=1e6, fmax=100e6)
L_req = -100 - 20*np.log10((st0*1e15)/target_fs)
print(round(L_req, 1), "dBc/Hz @ 1 MHz")     # -> -113.0 dBc/Hz
```

### 例 D5：SerDes BER bathtub（RJ 對 eye 的影響）

> **題目**：UI = 35.7 ps（28 Gbps）、RJ-only $\sigma_t=2$ ps。問在 eye 中央（sampling offset $t=0$）的 BER？
> 又若 $\sigma_t$ 惡化到 4 ps，BER 變多少？

**逐步解**

第 1 步，RJ-only BER bathtub（規範第 10.2 節 SerDes BER）：
$\text{BER}(t)=\tfrac12[Q(\tfrac{UI/2-t}{\sigma_t})+Q(\tfrac{UI/2+t}{\sigma_t})]$，$Q(x)=\tfrac12\mathrm{erfc}(x/\sqrt2)$。

第 2 步，eye 中央 $t=0$ 時兩項相同：$\text{BER}=Q\!\big(\tfrac{UI/2}{\sigma_t}\big)$。

第 3 步，$\sigma_t=2$ ps：$\dfrac{UI/2}{\sigma_t}=\dfrac{17.85}{2}=8.93$。$Q(8.93)$ 是極小數（高斯尾），
$\approx2\times10^{-19}$。$\sigma_t=4$ ps：$\dfrac{17.85}{4}=4.46$，$Q(4.46)\approx4\times10^{-6}$。

**結果**：$\sigma_t=2$ ps → BER $\approx2\times10^{-19}$；$\sigma_t=4$ ps → BER $\approx4\times10^{-6}$。
**jitter 加倍 → BER 惡化 13 個數量級**（高斯尾對 $\sigma$ 極度敏感）。

**Dimension check**：$Q$ 的引數 $\dfrac{UI/2}{\sigma_t}=\dfrac{[\text{s}]}{[\text{s}]}$ 無因次 ✓；BER 無因次（機率）✓。
**手感**：這就是為什麼 SerDes 規格用 $\sigma_t$（rms）但 BER 看的是 $\sigma$ 的「倍數」（$Q$ 函數）；
省一點 jitter 能換來 BER 巨幅改善。對照圖：

![SerDes eye / BER bathtub](/figures/serdes_eye_ber_bathtub.png)

**Python 驗證**

```python
import numpy as np
from simulations.common.serdes_utils import ber_bathtub
ui = 1/28e9
for st in [2e-12, 4e-12]:
    ber = ber_bathtub(np.array([0.0]), sigma_t=st, ui=ui)[0]
    print(st*1e12, "ps -> BER =", f"{ber:.2e}")
# 2.0 ps -> BER ~ 2e-19 ; 4.0 ps -> BER ~ 4e-06
```

---

## 自我檢查表

做完上面 15 題後，遮住答案問自己——每一項都該能在腦中「秒答方向」：

**A 級（換算反射）**

- [ ] 看到 phase 誤差（rad），能立刻 $\div(2\pi f_0)$ 換成時間（s），並做 $[\text{rad}]/[\text{rad/s}]=[\text{s}]$ check。
- [ ] 記得「5 GHz：1 mrad ≈ 32 fs、1 rad ≈ 31.8 ps」。
- [ ] dBc/Hz → linear（$10^{\mathcal{L}/10}$）→ phase PSD（$\times2$）一氣呵成。
- [ ] 懂 $\Delta\phi=\Gamma\,\Delta q/q_{max}$ 為何無因次，且 ISF 隨注入相位變（LTV）。

**B 級（ISF → phase noise）**

- [ ] 能默寫 Eq.(21) 並代數值得 dBc/Hz；知道分母是 $4\Delta\omega^2$（SSB 慣例）。
- [ ] 會用 Parseval（$\sum c_n^2=2\Gamma_{rms}^2$）從 $c_n$ 求 $\Gamma_{rms}$。
- [ ] 知道**只有 $c_0\ne0$ 才有 1/f³ 上轉**，且 corner $=\omega_{1/f}c_0^2/(2\Gamma_{rms}^2)$。
- [ ] 1/f² 是 $-20$ dB/dec、1/f³ 是 $-30$ dB/dec，能目視判讀。

**C 級（jitter 積分）**

- [ ] 會 dBc/Hz →（積分）→ $\sigma_\phi$ →（$\div2\pi f_0$）→ $\sigma_t$ 全流程。
- [ ] 知道 1/f² 的累積 jitter **被積分下限主導**，rms jitter 一定要附頻段。
- [ ] 懂 period jitter 用**高通核**、不被低頻主導；和 accumulated jitter 區別。
- [ ] 記得 ring 累積 jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$（隨機漫步、永不收斂）。

**D 級（設計反推）**

- [ ] 給 dBc/Hz 規格，能反解 $q_{max}$ 或 $\Gamma_{rms}$（$q_{max}$ 加倍或 $\Gamma_{rms}$ 減半皆 $-6$ dB）。
- [ ] 會用 $f_0=1/(2N\tau_D)$ 算 ring 級數，並記得「固定 $f_0,P$ 時 ring PN 幾乎與 $N$ 無關」的警語。
- [ ] 能把 jitter 規格（fs）反推成 1 MHz 處的 dBc/Hz（$\sigma_t$ 降 $k$ 倍 ⇒ $\mathcal{L}$ 降 $20\log_{10}k$ dB）。
- [ ] 知道 RJ 的 BER 對 $\sigma_t$ 極敏感（高斯尾），jitter 小改善 → BER 大改善。

**誠實標記**

- 例 C3 的 period jitter 前置常數標了 `TODO: manual verification needed`（與單邊/雙邊譜慣例有關）。
- 例 D3 的 ring $\Gamma_{rms}\propto N^{-3/4}$（[P2] Eq.(16), p.794，已核實），且「14.3 dB」僅為孤立因子示意，
  非真實設計增益（toy scaling，非 transistor-level）。

## 延伸閱讀

- 換算手感總整理：[numerical_feeling](/04_simulation_labs/numerical_feeling)
- impulse → phase 的完整推導：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)
- 白噪 → phase noise（Eq.(21) 推導與 factor-of-2）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- flicker 上轉與對稱性：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- jitter 積分模擬：[lab_08](/04_simulation_labs/lab_08_jitter_integration)
- 設計旋鈕（$q_{max},\Gamma_{rms},N$）：[lab_09](/04_simulation_labs/lab_09_design_tradeoffs)
