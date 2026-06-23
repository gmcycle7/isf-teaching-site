---
title: 數值手感 Numerical Feeling
description: 三個必做的口算練習，把 rad、fs、dBc/Hz、jitter 之間的換算變成肌肉記憶。
---

# 數值手感 Numerical Feeling

理論再漂亮，沒有數字就沒有手感。這頁用三個小例子，把 phase、time、dBc/Hz、jitter
之間的換算練成反射動作。每個例子都附 Python 驗證；完整函式庫在
`simulations/common/`。

> **公式來源**：相位/時間/jitter 換算與 1/f² 積分皆為標準結果，並與
> [P1] A. Hajimiri and T. H. Lee, *"A General Theory of Phase Noise in Electrical
> Oscillators,"* IEEE JSSC, 33(2), 1998（尤其 Eq.(21)）一致；逐步推導見
> [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) 與
> [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)。

> **為什麼先練數字**：類比設計師在白板上估數量級的能力，比記公式重要。看到
> 「$-100$ dBc/Hz @ 1 MHz、5 GHz」，你要能在 30 秒內估出「大概幾百 fs jitter」。

## Example 1：phase → time

> 若 $f_0=5$ GHz、$\Delta\phi=1$ mrad，求 timing error。

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0}=\frac{1\times10^{-3}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=\frac{10^{-3}}{3.1416\times10^{10}}\ \text{s}\approx3.18\times10^{-14}\ \text{s}=31.8\ \text{fs}.
$$

- **Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓（$2\pi f_0$ 是 rad/s）。
- **手感**：5 GHz 下「1 mrad ≈ 32 fs」。週期是 200 ps，所以 1 mrad 約是週期的 $1.6\times10^{-4}$。

```python
from simulations.common.noise_utils import phase_to_time_error
print(phase_to_time_error(1e-3, 5e9) * 1e15, "fs")   # -> 31.83 fs
```

## Example 2：injected charge → phase step → time

> 若 $q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$，求 phase step 與（在 5 GHz 的）timing error。

**相位步階**：

$$
\Delta\phi=\frac{\Gamma\,\Delta q}{q_{max}}=\frac{0.5\times10^{-15}}{10^{-12}}=5\times10^{-4}\ \text{rad}\;(\approx0.0286^\circ).
$$

**時間誤差**（$f_0=5$ GHz）：

$$
\Delta t=\frac{5\times10^{-4}}{2\pi\times5\times10^{9}}\approx15.9\ \text{fs}.
$$

- **手感**：1 fC ≈ 6240 個電子；在最敏感相位也只踢出 ~16 fs。單顆很小，但 noise 持續踢、
  會被相位積分器累積（見 [convolution_derivation](/03_isf_core_theory/convolution_derivation)）。
- 完整推導見 [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)（例 A）。

```python
from simulations.common.isf_utils import impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error
dphi = impulse_to_phase_step(1e-15, 0.5, 1e-12)
print(dphi, "rad ->", phase_to_time_error(dphi, 5e9)*1e15, "fs")  # 0.0005 rad -> 15.92 fs
```

## Example 3：phase noise plot → rms jitter（要會積分）

> 若 $\mathcal{L}(1\,\text{MHz})=-100$ dBc/Hz、假設 1/f² 斜率、由 1 MHz 積到 100 MHz、
> $f_0=5$ GHz，估 rms jitter。

**步驟 1：dBc/Hz 換成 linear 並還原 phase PSD。**
單音小角近似下 $\mathcal{L}(f)\approx\frac12 S_\phi(f)$，所以 $S_\phi(f)=2\cdot10^{\mathcal{L}(f)/10}$。
在 1 MHz：$\mathcal{L}=-100$ dBc/Hz $\Rightarrow 10^{-10}$，$S_\phi(1\text{MHz})=2\times10^{-10}$ rad²/Hz。

**步驟 2：寫出 1/f² 形狀。** 以 $f_{ref}=1$ MHz 錨定：

$$
S_\phi(f)=S_\phi(f_{ref})\left(\frac{f_{ref}}{f}\right)^2=2\times10^{-10}\left(\frac{10^6}{f}\right)^2.
$$

**步驟 3：積分得 phase variance。**

$$
\sigma_\phi^2=\int_{f_1}^{f_2}S_\phi(f)\,df=2\times10^{-10}\,(10^6)^2\!\int_{10^6}^{10^8}\frac{df}{f^2}=2\times10^{2}\left(\frac{1}{10^6}-\frac{1}{10^8}\right).
$$

$$
\sigma_\phi^2=200\times(10^{-6}-10^{-8})=200\times9.9\times10^{-7}=1.98\times10^{-4}\ \text{rad}^2\Rightarrow\sigma_\phi=1.407\times10^{-2}\ \text{rad}=14.07\ \text{mrad}.
$$

**步驟 4：換成 rms jitter。**

$$
\sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{1.407\times10^{-2}}{2\pi\times5\times10^{9}}\approx4.48\times10^{-13}\ \text{s}=447.9\ \text{fs}.
$$

- **手感**：積分被**下限 $f_1$ 主導**（$1/f_1$ 項最大）——所以「從哪裡開始積」對 1/f² 很關鍵。
- **參考點**：若這顆是 $-120$ dBc/Hz @ 1 MHz（好 10 倍功率、$\sqrt{10^2}=10$ 倍電壓），jitter 約縮到 ~45 fs。
- 這正是 [lab_08](/04_simulation_labs/lab_08_jitter_integration) 的圖；數值積分與解析式完全一致。

![由 L(f) 積分得 rms jitter](/figures/phase_noise_to_jitter_integration.png)

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter

f  = np.logspace(6, 8, 4000)                 # 1 MHz -> 100 MHz
L  = leeson_one_over_f2(f, L_ref_dbc=-100, f_ref=1e6)   # 1/f^2 skirt
sigma_t, sigma_phi = integrate_rms_jitter(f, L, f0=5e9, fmin=1e6, fmax=100e6)
print(sigma_phi*1e3, "mrad ;", sigma_t*1e15, "fs")   # -> 14.07 mrad ; 447.9 fs
```

完整 script：`simulations/lab_08_jitter_integration.py`。

## 參數與單位速查

| 量 | 符號 | 單位 | 換算 |
|---|---|---|---|
| 相位誤差 | $\Delta\phi,\sigma_\phi$ | rad | $1$ rad $=180/\pi\approx57.3^\circ$ |
| 時間誤差 | $\Delta t,\sigma_t$ | s | $\Delta t=\Delta\phi/(2\pi f_0)$ |
| phase PSD | $S_\phi$ | rad²/Hz | $S_\phi=2\cdot10^{\mathcal{L}/10}$ |
| SSB phase noise | $\mathcal{L}$ | dBc/Hz | $\mathcal{L}\approx\frac12 S_\phi$（→ dB） |
| 電荷 | $\Delta q,q_{max}$ | C | 1 fC $=10^{-15}$ C |

## 重點回顧

- **5 GHz 換算記憶點**：1 mrad ≈ 32 fs；1 rad ≈ 31.8 ps。
- dBc/Hz → linear → $S_\phi=2\times$linear → 積分 → 開根號 → $\div(2\pi f_0)$ = rms jitter。
- 1/f² 的 jitter 由積分**下限**主導。
- 三個例子的數字都能用 `simulations/common/` 內建函式一行驗證。
