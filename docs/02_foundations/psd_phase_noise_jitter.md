---
title: Phase Noise → Jitter
description: 逐步推導 Δt=Δφ/(2πf₀)、σ_φ²=∫S_φ df、σ_t=σ_φ/(2πf₀)、L≈½S_φ；dBc/Hz 轉 linear；四種 jitter 差異；canonical 例 C（5GHz, -100dBc/Hz → 447.9 fs）。
---

# Phase Noise → Jitter

> 先備：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) · [stochastic_noise_basics](/02_foundations/stochastic_noise_basics) ｜ 接下來：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)

這頁回答一個工程上最常被問的問題：**手上拿到一張 phase noise 圖（$\mathcal{L}(f)$，dBc/Hz），
怎麼把它變成一個時域數字——rms jitter $\sigma_t$（fs）？** 這是 frequency-domain（頻域，
通訊/RF 的語言）與 time-domain（時域，數位/SerDes 的語言）之間的橋。

整條鏈是四步：

$$
\mathcal{L}(f)\ \xrightarrow{\ \times2,\ \text{de-dB}\ }\ S_\phi(f)\ \xrightarrow{\ \int_{f_1}^{f_2}\ }\ \sigma_\phi^2\ \xrightarrow{\ \sqrt{\ }\ }\ \sigma_\phi\ \xrightarrow{\ \div(2\pi f_0)\ }\ \sigma_t.
$$

我們把每一步都拆開、帶單位、帶 dimension check，最後用 canonical 例 C
（5 GHz、$-100$ dBc/Hz @ 1 MHz、1/f² 斜率、1→100 MHz）算出 $\sigma_t=447.9$ fs。

> **物理直覺（先講結論）**：相位誤差 $\Delta\phi$ 就是「時鐘的指針偏了多少角度」；
> 把角度除以角速度 $2\pi f_0$，就得到「指針偏了多少時間」$\Delta t$。phase noise 圖
> 告訴你每個 offset 頻率有多少相位功率密度；把它們**全部加起來（積分）**就是總相位
> 變異數；開根號是 rms 相位；再除 $2\pi f_0$ 就是 rms timing jitter。整張圖被壓成一個 fs 數字。

## 第 1 步：phase error 為什麼能轉成 timing error

一個理想振盪 $\cos(2\pi f_0 t)$，加上 excess phase 後是 $\cos(2\pi f_0 t+\Delta\phi)$。
把相位項提出來看 zero crossing（過零點）落在哪：

$$
2\pi f_0 t+\Delta\phi=2\pi f_0\Big(t+\underbrace{\frac{\Delta\phi}{2\pi f_0}}_{=\ \Delta t}\Big).
$$

也就是說，多出 $\Delta\phi$ 的相位，等效於整條波形**在時間軸上平移了** $\Delta t$
（規範第 3 節公式 17）：

$$
\boxed{\ \Delta t=\frac{\Delta\phi}{2\pi f_0}\ }
$$

- **用到的物理**：phase 與 time 之間的轉換率就是角頻率 $\omega_0=2\pi f_0$（rad/s）。
- **dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。注意分母是 $2\pi f_0$
  （rad/s），**不是** $f_0$（Hz）——這個 $2\pi$ 漏掉是最常見的錯。
- **為何合理**：在小相位（$\Delta\phi\ll1$ rad）下，相位偏移與邊緣時間偏移是線性、
  一對一的。timing jitter 就是 zero crossing 的時間誤差，所以它 = $\Delta\phi/(2\pi f_0)$。
- **手感**：5 GHz 下 $\Delta\phi=1$ mrad $\Rightarrow\Delta t=31.8$ fs（見
  [numerical_feeling](/04_simulation_labs/numerical_feeling) Example 1）。

## 第 2 步：dBc/Hz 怎麼轉 linear，並還原 phase PSD

phase noise 圖的縱軸是 **$\mathcal{L}(f)$，SSB phase noise（single-sideband，
單邊帶相位雜訊），單位 dBc/Hz**——意思是「在 offset $f$ 處、每 1 Hz 頻寬內，
單邊帶的雜訊功率比 carrier 低幾 dB」（dBc = dB relative to carrier）。

**de-dB（從 dB 換回線性）**：dBc/Hz 是 $10\log_{10}(\cdot)$，所以

$$
\mathcal{L}_{\text{lin}}(f)=10^{\mathcal{L}(f)/10}\quad[\text{1/Hz}].
$$

**再連到 phase PSD**：小角近似下，SSB phase noise 與單邊 phase PSD 的關係是
（規範第 3 節公式 16）：

$$
\boxed{\ \mathcal{L}(f)\approx\tfrac12\,S_\phi(f)\ }\quad\Longrightarrow\quad S_\phi(f)=2\cdot10^{\mathcal{L}(f)/10}\ [\text{rad}^2/\text{Hz}].
$$

- **單位**：$S_\phi$ 是 $\text{rad}^2/\text{Hz}$（相位變異數的密度）。$\mathcal{L}_{\text{lin}}$
  本身無因次/Hz；乘 2 後解讀成 $\text{rad}^2/\text{Hz}$。
- **這個 $\frac12$ 從哪來**：phase modulation 的功率平均分到上、下兩個 sideband，
  $\mathcal{L}$ 只算**單邊**，所以是 $S_\phi$ 的一半。這正是規範第 3 節那段「factor-of-2
  教學註記」討論的記帳慣例；本站對 jitter 積分一律採 $S_\phi=2\mathcal{L}_{\text{lin}}$。
  深入討論見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

### 逐步推導：$\mathcal{L}\approx\tfrac12 S_\phi$ 從小角 PM（narrowband）來

上面那個 $\frac12$ 不是憑空塞的，它是**窄頻相位調變（narrowband PM，相位擺動很小的調變）**
的直接後果。我們把它一步步推出來，把「sideband 功率 $=(\phi_p/2)^2$」這件事講清楚。

**第 1 步：寫出一個單音相位調變的載波。** 設相位只被單一頻率 $\omega_m$（offset 角頻率）以
小幅度 $\phi_p$（peak phase，相位擺動峰值，rad）調變：

$$
v(t)=\cos\big(\omega_0 t+\phi(t)\big),\qquad \phi(t)=\phi_p\sin\omega_m t,\quad \phi_p\ll 1\ \text{rad}.
$$

- **用到的物理**：這就是把 [第 1 步](#第-1-步phase-error-為什麼能轉成-timing-error) 的 excess
  phase $\Delta\phi$ 換成一個會隨時間正弦擺動的相位；$\phi_p$ 是它的振幅。
- **單位**：$\phi_p$ 與 $\phi(t)$ 都是 rad；$\omega_0,\omega_m$ 都是 rad/s。

**第 2 步：用三角展開把相位調變攤開。** 用和角公式
$\cos(A+B)=\cos A\cos B-\sin A\sin B$，令 $A=\omega_0 t$、$B=\phi(t)$：

$$
v(t)=\cos\omega_0 t\,\cos\!\big(\phi_p\sin\omega_m t\big)-\sin\omega_0 t\,\sin\!\big(\phi_p\sin\omega_m t\big).
$$

**第 3 步：小角近似（這就是「small-angle」的全部內容）。** 因為 $\phi_p\ll1$：

$$
\cos\!\big(\phi_p\sin\omega_m t\big)\approx 1,\qquad \sin\!\big(\phi_p\sin\omega_m t\big)\approx \phi_p\sin\omega_m t.
$$

- **用到的數學**：泰勒展開 $\cos x\approx1-x^2/2$、$\sin x\approx x$，只留到一階（$x=\phi_p\sin\omega_m t$，
  其 $x^2$ 是 $O(\phi_p^2)$ 可丟）。這正是 Bessel 展開 $J_0\approx1,\ J_1\approx\phi_p/2$ 的小幅度極限。

代回得到：

$$
v(t)\approx\cos\omega_0 t-\phi_p\sin\omega_0 t\,\sin\omega_m t.
$$

**第 4 步：把 $\sin\times\sin$ 拆成上下兩個 sideband。** 用積化和差
$\sin\alpha\sin\beta=\tfrac12[\cos(\alpha-\beta)-\cos(\alpha+\beta)]$，令 $\alpha=\omega_0 t$、$\beta=\omega_m t$：

$$
\begin{aligned}
v(t)&\approx\cos\omega_0 t-\frac{\phi_p}{2}\Big[\cos(\omega_0-\omega_m)t-\cos(\omega_0+\omega_m)t\Big]\\
&=\underbrace{\cos\omega_0 t}_{\text{carrier}}-\underbrace{\frac{\phi_p}{2}\cos(\omega_0-\omega_m)t}_{\text{下邊帶}}+\underbrace{\frac{\phi_p}{2}\cos(\omega_0+\omega_m)t}_{\text{上邊帶}}.
\end{aligned}
$$

- **物理意義**：相位調變把載波旁邊長出**對稱的一對 sideband**，各落在 $\omega_0\pm\omega_m$，
  振幅都是 $\phi_p/2$。這就是 [P1] Fig. 8 那種「載波被塗成裙帶」的時域起源。

**第 5 步：每個 sideband 的相對功率。** carrier 振幅 $1$、功率 $\propto 1$（取 $\tfrac12\cdot1^2$）；
單一 sideband 振幅 $\phi_p/2$、功率 $\propto(\phi_p/2)^2$。所以**單邊帶相對載波的功率比**是

$$
\frac{P_{\text{1 sideband}}}{P_{\text{carrier}}}=\frac{\tfrac12(\phi_p/2)^2}{\tfrac12(1)^2}=\Big(\frac{\phi_p}{2}\Big)^2=\frac{\phi_p^2}{4}.
$$

- **dimension check**：功率比無因次 ✓；$\phi_p$（rad）平方後在「相位功率」語境下視為 $\text{rad}^2$。

**第 6 步：把它連到 $S_\phi$。** 對 $\phi(t)=\phi_p\sin\omega_m t$，相位的均方值（變異數）是

$$
\langle\phi^2(t)\rangle=\phi_p^2\langle\sin^2\omega_m t\rangle=\frac{\phi_p^2}{2}.
$$

這個單音的全部相位功率 $\phi_p^2/2$ 集中在 $\omega_m$ 這一根；把它解讀成「在 $\omega_m$ 處的單邊
phase PSD 強度」就是 $S_\phi(\omega_m)=\phi_p^2/2$（per-Hz，當作一根的權重）。

**第 7 步：兩者相除，$\frac12$ 出現。** $\mathcal{L}$（SSB）= 單一 sideband 功率比 $=\phi_p^2/4$；
$S_\phi=\phi_p^2/2$。所以

$$
\boxed{\ \mathcal{L}=\frac{\phi_p^2/4}{1}=\frac12\cdot\frac{\phi_p^2}{2}=\frac12 S_\phi\ }
$$

- **一句話總結**：$\mathcal{L}$ 只數**一個** sideband（功率 $(\phi_p/2)^2=\phi_p^2/4$），而 $S_\phi$
  是**全部**相位功率密度（$\phi_p^2/2$，等於兩個 sideband 加起來）。**單邊 ÷ 全部 $=\tfrac12$**，
  這就是 factor-of-$\tfrac12$ 的全部來源。
- **失效條件**：一旦 $\phi_p$ 不再 $\ll1$，第 3 步的高階 Bessel 項（$J_2,J_3,\dots$）長出更多 sideband，
  $\mathcal{L}=\tfrac12 S_\phi$ 不再成立——大相位時 carrier 還會「掉功率」給高階 sideband。
- **小角近似條件**：$\mathcal{L}\approx\frac12 S_\phi$ 只在 $\sigma_\phi\ll1$ rad 成立
  （Bessel 展開只留一階）。本例 $\sigma_\phi=14$ mrad $\ll1$，OK。
- **canonical 數值**：在 1 MHz、$\mathcal{L}=-100$ dBc/Hz：
  $\mathcal{L}_{\text{lin}}=10^{-100/10}=10^{-10}$；$S_\phi(1\text{MHz})=2\times10^{-10}\ \text{rad}^2/\text{Hz}$。

## 第 3 步：為什麼對 phase PSD 積分能得到 variance

這一步是純粹的 Parseval / Wiener–Khinchin：**把 PSD 對頻率積分，得到時域的變異數**
（規範第 3 節公式 18）：

$$
\boxed{\ \sigma_\phi^2=\int_{f_1}^{f_2}S_\phi(f)\,df\ }
$$

- **用到的數學**：$S_\phi(f)$ 是「每單位頻寬的相位功率」；把它在關心的 offset 頻段
  $[f_1,f_2]$ 上加總（積分）就是總相位功率 = 變異數 $\sigma_\phi^2$。這跟
  [stochastic_noise_basics](/02_foundations/stochastic_noise_basics) 第 3 節把電流 PSD
  積成 $\overline{i_n^2}$ 是**同一招**。
- **dimension check**：$(\text{rad}^2/\text{Hz})\times\text{Hz}=\text{rad}^2$ ✓。
- **為什麼積分頻寬 $[f_1,f_2]$ 很重要**：phase PSD 在低 offset 通常是 1/f²（甚至 1/f³），
  積分量會被**下限 $f_1$ 主導**。改 $f_1$ 一個 decade，jitter 可能差好幾倍。所以報
  jitter **一定要標積分頻寬**，否則數字沒有意義。
  - 上限 $f_2$：物理上由系統頻寬決定（SerDes 是 PLL loop bandwidth 或 Nyquist）。
  - 下限 $f_1$：對開環振盪器積到 DC 會發散（random walk），實務上由量測時間或
    PLL 把它「拉住」的頻率決定。
- **小角近似（$\sin\Delta\phi\approx\Delta\phi$）**：把相位調變的功率近似成 $\sigma_\phi^2$，
  同樣要求 $\sigma_\phi\ll1$ rad。

### 1/f² 的封閉積分（本例的核心）

把第 2 步的 1/f² 形狀以 $f_{ref}=1$ MHz 錨定：

$$
S_\phi(f)=S_\phi(f_{ref})\Big(\frac{f_{ref}}{f}\Big)^2=2\times10^{-10}\Big(\frac{10^6}{f}\Big)^2.
$$

代入積分（注意 $\int f^{-2}df=-1/f$）：

$$
\begin{aligned}
\sigma_\phi^2&=2\times10^{-10}\,(10^6)^2\int_{10^6}^{10^8}\frac{df}{f^2}
=2\times10^{2}\Big(\frac{1}{10^6}-\frac{1}{10^8}\Big)\\
&=200\times(10^{-6}-10^{-8})=200\times9.9\times10^{-7}=1.98\times10^{-4}\ \text{rad}^2.
\end{aligned}
$$

開根號：

$$
\sigma_\phi=\sqrt{1.98\times10^{-4}}=1.407\times10^{-2}\ \text{rad}=14.07\ \text{mrad}.
$$

- **手感確認**：括號裡 $10^{-6}\gg10^{-8}$，所以「$1/f_1$」這項主導——再次印證**下限主導**。
  把 $f_2$ 從 100 MHz 拉到 1 GHz 幾乎不改變答案；把 $f_1$ 從 1 MHz 降到 100 kHz 卻會
  讓 jitter 暴增 $\sqrt{10}\approx3.2$ 倍。

## 第 4 步：phase variance → rms jitter

把第 1 步的 $\Delta t=\Delta\phi/(2\pi f_0)$ 套用到 rms 量（規範第 3 節公式 19）：

$$
\boxed{\ \sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{1}{2\pi f_0}\sqrt{\int_{f_1}^{f_2}S_\phi(f)\,df}\ }
$$

代入本例（$f_0=5$ GHz、$\sigma_\phi=1.407\times10^{-2}$ rad）：

$$
\sigma_t=\frac{1.407\times10^{-2}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}
=\frac{1.407\times10^{-2}}{3.1416\times10^{10}}\ \text{s}
=4.479\times10^{-13}\ \text{s}=447.9\ \text{fs}.
$$

- **dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。
- **這就是 canonical 例 C**（規範第 8 節）：5 GHz、$-100$ dBc/Hz @ 1 MHz、1/f²、
  積 1→100 MHz $\Rightarrow\sigma_\phi=14.07$ mrad、$\sigma_t=447.9$ fs。
- **scaling 手感**：phase noise 好 10 dB（$\mathcal{L}=-110$）$\Rightarrow S_\phi$ 小 10 倍
  $\Rightarrow\sigma_t$ 小 $\sqrt{10}\approx3.2$ 倍 $\to\sim142$ fs。好 20 dB（$-120$）
  $\Rightarrow$ 小 10 倍 $\to\sim45$ fs（見 numerical_feeling 的參考點）。

![由 L(f) 積分得 rms jitter](/figures/phase_noise_to_jitter_integration.png)

上圖（`simulations/lab_08_jitter_integration.py`）畫出 $-100$ dBc/Hz @ 1 MHz 的 1/f²
skirt，以及累積積分如何隨頻寬收斂到 447.9 fs；數值積分與上面手算的解析式完全一致。
這是 **toy / 解析示範**（單一 1/f² 源、小角近似），非 transistor-level。

### 一行驗證（用內建函式）

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter

f = np.logspace(6, 8, 4000)                              # 1 MHz -> 100 MHz
L = leeson_one_over_f2(f, L_ref_dbc=-100, f_ref=1e6)     # 1/f^2 skirt
sigma_t, sigma_phi = integrate_rms_jitter(f, L, f0=5e9, fmin=1e6, fmax=100e6)
print(sigma_phi*1e3, "mrad ;", sigma_t*1e15, "fs")       # -> 14.07 mrad ; 447.9 fs
```

## jitter 的四種「方言」（用 notation 頁的表）

同樣是「jitter」，量到的可能是完全不同的東西。下表沿用
[notation](/00_overview/notation) 的定義（規範第 2 節）：

| 名稱 | 定義 | 直覺 | 跟 phase noise 的關係 |
|---|---|---|---|
| **random jitter (RJ)** | 高斯、無上界，用 $\sigma$ 描述 | 隨機踢出來的抖動 | 就是上面積分出的 $\sigma_t$；SerDes BER 用它估 eye 閉合 |
| **period jitter** | $T_k-T$（單一週期相對 nominal） | 這一拍多長／多短 | 對 $S_\phi$ 加一個 $\sin^2(\pi f/f_0)$ 類高通權重後積分 |
| **cycle-to-cycle jitter** | $T_{k+1}-T_k$（相鄰兩拍差） | 拍與拍之間變化多快 | 對相鄰差分，更強的高通加權，最不受 close-in 影響 |
| **accumulated / long-term jitter** | 相隔 $\Delta t$ 兩 edge 誤差，$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ | 開環振盪器越跑越偏 | random-walk；對應 1/f² 積到很低 offset（[P2] Eq.(8)） |

- **為什麼要分清楚**：period / cycle-to-cycle jitter 對 $S_\phi$ 施加**高通型**權重
  （差分會壓低低頻、放大高頻），所以它們**不被 close-in 1/f² 主導**；而上面算的
  random / 整合型 jitter（zero-crossing 絕對時間誤差）**被下限主導**。報數字時要說清楚
  是哪一種，否則會差好幾個數量級。
- **accumulated jitter**：自由振盪器沒有絕對時間參考，相位是 random walk，
  $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$（[P2] Eq.(8), p.792，claim C6）。
  ring 細節見 [P2] 與 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

### period / cycle-to-cycle / accumulated jitter 的權重核（逐步推導）

上表的「高通加權」不是手揮，它有確切的權重核。關鍵觀念：**不同種類的 jitter 是同一條相位過程
$\phi(t)$ 的不同「差分」**，而時域差分在頻域就是乘上一個 transfer function。我們一步步把核推出來。

**第 1 步：把每個 edge 的時間誤差寫成相位的取樣。** 第 $k$ 個 edge 名目上落在 $t_k=kT$，
其時間誤差就是該瞬間相位除以角速度（沿用第 1 步的 $\Delta t=\Delta\phi/(2\pi f_0)$）：

$$
\Delta t_k=\frac{\phi(kT)}{2\pi f_0}.
$$

**第 2 步：三種 jitter = 三種差分。** 由定義（規範第 2 節）：

$$
\begin{aligned}
\text{period jitter:}\quad &J^{\text{per}}_k=\Delta t_{k+1}-\Delta t_k=\frac{\phi((k{+}1)T)-\phi(kT)}{2\pi f_0}\quad(\text{相位的一階差分}),\\
\text{cycle-to-cycle:}\quad &J^{\text{c2c}}_k=J^{\text{per}}_{k+1}-J^{\text{per}}_k\quad(\text{相位的二階差分}),\\
\text{accumulated:}\quad &\Delta t_k=\frac{\phi(kT)}{2\pi f_0}\quad(\text{不差分，直接是相位本身}).
\end{aligned}
$$

**第 3 步：差分在頻域 = 乘上 $(1-e^{-j2\pi fT})$。** 對一個頻率分量 $\phi(t)\propto e^{j2\pi ft}$，
延遲一個週期 $T$ 就是乘 $e^{-j2\pi fT}$。所以「現在減去一個週期前」這個一階差分算子的頻率響應是

$$
H_{\text{per}}(f)=1-e^{-j2\pi fT},\qquad
\lvert H_{\text{per}}(f)\rvert^2=\big\lvert 1-e^{-j2\pi fT}\big\rvert^2=4\sin^2(\pi fT).
$$

- **代數展開**：$\lvert 1-e^{-j\theta}\rvert^2=(1-\cos\theta)^2+\sin^2\theta=2-2\cos\theta=4\sin^2(\theta/2)$，
  代 $\theta=2\pi fT$ 即得 $4\sin^2(\pi fT)$。
- **為什麼是高通**：在 $f\to0$，$\sin^2(\pi fT)\approx(\pi fT)^2\to0$——**低頻被狠狠壓掉**；
  在 $f=f_0/2=1/(2T)$ 達到最大 $4$。這就是 period jitter「不被 close-in 1/f² 主導」的數學原因。

**第 4 步：把核套進 phase-variance 積分。** 相位變異數密度乘上 $\lvert H\rvert^2$ 再積分、
最後除以 $(2\pi f_0)^2$ 換成時間（規範第 10.2 節 period/cycle-to-cycle jitter 核）：

$$
\sigma_{T}^2=\frac{1}{(2\pi f_0)^2}\int_0^{\infty}S_\phi(f)\,\big\lvert 1-e^{-j2\pi fT}\big\rvert^2\,df
=\frac{1}{(2\pi f_0)^2}\int_0^{\infty}S_\phi(f)\,4\sin^2(\pi fT)\,df.
$$

cycle-to-cycle 是再做一次差分，所以核**平方再平方**（二階差分 = 一階差分作用兩次）：

$$
\sigma_{cc}^2=\frac{1}{(2\pi f_0)^2}\int_0^{\infty}S_\phi(f)\,\big\lvert 1-e^{-j2\pi fT}\big\rvert^4\,df
=\frac{1}{(2\pi f_0)^2}\int_0^{\infty}S_\phi(f)\,16\sin^4(\pi fT)\,df.
$$

accumulated jitter 則**沒有差分核**（核 $=1$），所以它由**低頻主導**（1/f² 積到很低 offset 才發散），
這正是它隨 $\sqrt{\Delta t}$ random-walk 成長的頻域對應（[P2] Eq.(8), p.792；κ 由 Eq.(12), p.793）。

- **dimension check**：$S_\phi$（$\text{rad}^2/\text{Hz}$）× 無因次核 × $\text{Hz}$ = $\text{rad}^2$，
  再除 $(2\pi f_0)^2$（$\text{rad}^2/\text{s}^2$）= $\text{s}^2$ ✓，開根號得秒。
- **三句話對照**：accumulated 核 $=1$（低頻主導）；period 核 $\lvert1-e^{-j2\pi fT}\rvert^2$
  （一階高通）；cycle-to-cycle 核 $\lvert1-e^{-j2\pi fT}\rvert^4$（二階高通，最不吃 close-in）。

> **註（常數慣例）**：上式採「單邊 $S_\phi$、$\int_0^\infty$」慣例；若改用雙邊或不同 SSB 記帳，
> 前置常數可能差 factor-of-2，與規範第 3 節 factor-of-2 教學註記同源。本站對 jitter 一律採
> $S_\phi=2\mathcal{L}_{\text{lin}}$、單邊積分。確切常數見各文獻定義差異。

### canonical 數值：由 $S_\phi$ 積出 period jitter

> **承例 C**：$f_0=5$ GHz（$T=200$ ps）、$\mathcal{L}(1\text{MHz})=-100$ dBc/Hz、1/f² 斜率。
> 求 period jitter $\sigma_T$（積 1 MHz→100 MHz，與例 C 同頻段以便對照）。

把第 3 步的 1/f² 形狀 $S_\phi(f)=2\times10^{-10}(10^6/f)^2$ 代入 period 核。先看核在這個頻段的大小：
$T=2\times10^{-10}$ s，$\pi fT$ 在 $f=10^6$ 是 $\pi\times10^6\times2\times10^{-10}=6.28\times10^{-4}\ll1$，
在 $f=10^8$ 是 $6.28\times10^{-2}\ll1$。所以整段都可用小角 $\sin^2(\pi fT)\approx(\pi fT)^2$：

$$
\big\lvert 1-e^{-j2\pi fT}\big\rvert^2\approx 4(\pi fT)^2=(2\pi fT)^2.
$$

代入 period 積分：

$$
\begin{aligned}
\sigma_T^2&=\frac{1}{(2\pi f_0)^2}\int_{10^6}^{10^8}\!2\times10^{-10}\Big(\frac{10^6}{f}\Big)^2(2\pi fT)^2\,df\\
&=\frac{(2\pi T)^2}{(2\pi f_0)^2}\,2\times10^{-10}(10^6)^2\int_{10^6}^{10^8}\!df
=T^4\cdot 2\times10^{-10}(10^6)^2\int_{10^6}^{10^8}\!df.
\end{aligned}
$$

把常數收乾淨：$(2\pi T)^2/(2\pi f_0)^2=T^2/f_0^2=T^2\cdot T^2=T^4$（因 $f_0=1/T$），且
$f$ 的兩個冪次相消（$f^{-2}\cdot f^{2}=1$），積分變成 $\int_{10^6}^{10^8}df=9.9\times10^7$ Hz：

$$
\begin{aligned}
\sigma_T^2&=T^4\cdot 2\times10^{-10}\cdot(10^6)^2\cdot(9.9\times10^7)\\
&=(2\times10^{-10})^4\cdot 2\times10^{-10}\cdot10^{12}\cdot9.9\times10^7.
\end{aligned}
$$

逐項算：$T^4=(2\times10^{-10})^4=16\times10^{-40}=1.6\times10^{-39}$；
$2\times10^{-10}\cdot10^{12}=2\times10^{2}$；再乘 $9.9\times10^7$ 得 $1.98\times10^{10}$。所以

$$
\sigma_T^2=1.6\times10^{-39}\times1.98\times10^{10}=3.17\times10^{-29}\ \text{s}^2
\;\Rightarrow\;\sigma_T=5.6\times10^{-15}\ \text{s}=5.6\ \text{fs}.
$$

- **手感對照**：同一張 phase noise 圖、同一積分頻段，**accumulated/RJ 的 $\sigma_t=447.9$ fs**
  （例 C，下限主導），但 **period jitter 只有 $\sim5.6$ fs**——小了快兩個數量級！原因正是高通核
  $(2\pi fT)^2$ 把 close-in（1 MHz 那端，貢獻 RJ 的主力）狠狠壓掉，period jitter 反而由**高頻端**
  累積。這就是「報 jitter 一定要講清楚是哪一種」的最佳教材。
- **dimension check**：$T^4$（$\text{s}^4$）$\times\,\text{(rad}^2/\text{Hz)}\times\text{Hz}\times f^{0}$
  收乾後得 $\text{s}^2$ ✓。

```python
import numpy as np
from simulations.common.noise_utils import phase_psd_to_l_dbc_per_hz  # noqa: F401
# period jitter: 對 S_phi 乘上 |1-e^{-j2πfT}|^2 = 4 sin^2(πfT) 再積分、除 (2πf0)^2
f  = np.logspace(6, 8, 200000)
f0 = 5e9; T = 1.0/f0
S_phi = 2e-10 * (1e6/f)**2                      # 1/f^2, 由 -100 dBc/Hz @1MHz 還原
kernel = np.abs(1 - np.exp(-1j*2*np.pi*f*T))**2 # = 4 sin^2(πfT) 高通核
sigma_T = np.sqrt(np.trapezoid(S_phi*kernel, f)) / (2*np.pi*f0)
print(sigma_T*1e15, "fs period jitter")          # -> ~5.6 fs（遠小於 447.9 fs 的 RJ）
```

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 小角 $\sigma_\phi\ll1$ rad | $\mathcal{L}\approx\frac12 S_\phi$、$\Delta t=\Delta\phi/(2\pi f_0)$ 線性 | 大相位 → 要用完整 Bessel，$\mathcal{L}\neq\frac12 S_\phi$ |
| 積分頻寬有限且明確 | $\sigma_t$ 收斂、可重現 | 1/f² 積到 DC 發散；不標頻寬數字無意義 |
| 單一 1/f² 形狀（本例） | 解析封閉式可用 | 真實有 1/f³ + flat floor，要分段或數值積 |
| RJ 為高斯 | 用 $\sigma$ 估 BER | 有 deterministic jitter (DJ) 時要 RJ/DJ 分解 |

## 對應的 paper / 公式

- $\Delta t=\Delta\phi/(2\pi f_0)$、$\sigma_\phi^2=\int S_\phi df$、$\sigma_t=\sigma_\phi/(2\pi f_0)$、
  $\mathcal{L}\approx\frac12 S_\phi$：規範第 3 節公式 16–19。
- accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$：[P2] Eq.(8), p.792（claim C6）。
- phase noise 本身的來源（白噪 → 1/f²）：[P1] Eq.(21), p.185。
- 圖：`phase_noise_to_jitter_integration.png`（lab_08），對應規範第 4 節。

## Worked examples 數值例題

下面兩題把整頁的鏈條與權重核各跑一遍。格式：題目 → 逐步代入（帶單位）→ 結果 →
dimension check → 一行 Python 驗證（引用 `simulations/common/`）。

### 例 C：phase noise plot → rms jitter（canonical，$-100$ dBc/Hz → 447.9 fs）

> **題目**：$f_0=5$ GHz、$\mathcal{L}(1\text{MHz})=-100$ dBc/Hz、1/f² 斜率、積 1 MHz→100 MHz，
> 求 rms（accumulated/RJ）jitter $\sigma_t$。

**步驟 1（de-dB + 還原 $S_\phi$）**：$\mathcal{L}_{\text{lin}}=10^{-100/10}=10^{-10}$；
$S_\phi(1\text{MHz})=2\mathcal{L}_{\text{lin}}=2\times10^{-10}\ \text{rad}^2/\text{Hz}$。

**步驟 2（1/f² 形狀）**：

$$
S_\phi(f)=2\times10^{-10}\Big(\frac{10^6}{f}\Big)^2.
$$

**步驟 3（積分得 variance，$\int f^{-2}df=-1/f$）**：

$$
\sigma_\phi^2=2\times10^{-10}(10^6)^2\!\int_{10^6}^{10^8}\!\frac{df}{f^2}
=2\times10^{2}\Big(\frac{1}{10^6}-\frac{1}{10^8}\Big)=200\times9.9\times10^{-7}=1.98\times10^{-4}\ \text{rad}^2.
$$

$$
\sigma_\phi=\sqrt{1.98\times10^{-4}}=1.407\times10^{-2}\ \text{rad}=14.07\ \text{mrad}.
$$

**步驟 4（換成時間）**：

$$
\sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{1.407\times10^{-2}}{2\pi\times5\times10^{9}}=4.479\times10^{-13}\ \text{s}=447.9\ \text{fs}.
$$

- **結果**：$\sigma_\phi=14.07$ mrad、$\sigma_t=447.9$ fs。
- **dimension check**：步驟 3 $(\text{rad}^2/\text{Hz})\times\text{Hz}=\text{rad}^2$ ✓；
  步驟 4 $[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。
- **手感**：積分被**下限 $f_1=1$ MHz** 主導（$1/f_1\gg1/f_2$）；報 jitter 必標頻寬。

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter
f = np.logspace(6, 8, 4000)                            # 1 MHz -> 100 MHz
L = leeson_one_over_f2(f, L_ref_dbc=-100, f_ref=1e6)   # 1/f^2 skirt
sigma_t, sigma_phi = integrate_rms_jitter(f, L, f0=5e9, fmin=1e6, fmax=100e6)
print(sigma_phi*1e3, "mrad ;", sigma_t*1e15, "fs")     # -> 14.07 mrad ; 447.9 fs
```

### 例 D：同一張 L(f) → period jitter（套高通核 $\lvert1-e^{-j2\pi fT}\rvert^2$）

> **題目**：同例 C（$f_0=5$ GHz、$T=200$ ps、$-100$ dBc/Hz @ 1 MHz、1/f²、積 1→100 MHz），
> 改求 **period jitter** $\sigma_T$，看它跟例 C 的 RJ 差多少。

**步驟 1（核的小角化）**：本頻段 $\pi fT\le 6.28\times10^{-2}\ll1$，故
$\lvert1-e^{-j2\pi fT}\rvert^2=4\sin^2(\pi fT)\approx(2\pi fT)^2$。

**步驟 2（代入 period 積分並消冪）**：前置 $T^2/f_0^2=T^4$，且 $f^{-2}\cdot f^{2}=1$：

$$
\sigma_T^2=T^4\cdot2\times10^{-10}(10^6)^2\!\int_{10^6}^{10^8}\!df
=T^4\cdot2\times10^{2}\cdot(9.9\times10^7).
$$

**步驟 3（代 $T=2\times10^{-10}$ s）**：$T^4=1.6\times10^{-39}\ \text{s}^4$，後段 $=1.98\times10^{10}$（$\text{rad}^2\cdot\text{Hz}$，與 $T^4$ 相乘後得 $\text{s}^2$）：

$$
\sigma_T^2=1.6\times10^{-39}\times1.98\times10^{10}=3.17\times10^{-29}\ \text{s}^2
\;\Rightarrow\;\sigma_T=5.6\ \text{fs}.
$$

- **結果**：$\sigma_T\approx5.6$ fs，是例 C 之 RJ（447.9 fs）的約 $1/80$。
- **dimension check**：$T^4(\text{s}^4)\times(\text{rad}^2/\text{Hz})\times\text{Hz}$ 收乾後 $=\text{s}^2$ ✓。
- **物理**：period 的一階差分核 $(2\pi fT)^2$ 把 close-in（RJ 的主力）壓掉，period jitter 由**高頻端**
  累積 → 同一張圖、不同 jitter 種類，數字差兩個量級。

```python
import numpy as np
f  = np.logspace(6, 8, 200000)
f0 = 5e9; T = 1.0/f0
S_phi  = 2e-10 * (1e6/f)**2                          # 由 -100 dBc/Hz @1MHz 還原
kernel = np.abs(1 - np.exp(-1j*2*np.pi*f*T))**2      # 4 sin^2(πfT) 高通核
sigma_T = np.sqrt(np.trapezoid(S_phi*kernel, f)) / (2*np.pi*f0)
print(sigma_T*1e15, "fs period jitter")              # -> ~5.6 fs（<< 447.9 fs RJ）
```

## 重點回顧

- **四步鏈**：dBc/Hz $\xrightarrow{\times2,\text{de-dB}} S_\phi\xrightarrow{\int}\sigma_\phi^2
  \xrightarrow{\sqrt{}}\sigma_\phi\xrightarrow{\div2\pi f_0}\sigma_t$。
- $\Delta t=\Delta\phi/(2\pi f_0)$：相位除角速度 = 時間；分母是 $2\pi f_0$（rad/s），別漏 $2\pi$。
- $S_\phi=2\cdot10^{\mathcal{L}/10}$；$\mathcal{L}\approx\frac12 S_\phi$ 只在小角成立。
- 1/f² 的 jitter 積分被**下限 $f_1$ 主導**——報 jitter 一定要標積分頻寬。
- canonical 例 C：5 GHz、$-100$ dBc/Hz @ 1 MHz、1/f²、1→100 MHz $\Rightarrow$
  $\sigma_\phi=14.07$ mrad、$\sigma_t=447.9$ fs。
- 四種 jitter：RJ / period / cycle-to-cycle / accumulated，加權與主導頻段不同。
- $\mathcal{L}=\tfrac12 S_\phi$ 的根：小角 PM 長出對稱 sideband，單邊功率 $(\phi_p/2)^2=\phi_p^2/4$，
  全部相位功率 $\phi_p^2/2$，**單邊 ÷ 全部 $=\tfrac12$**。
- 權重核：accumulated 核 $=1$（低頻主導）、period 核 $\lvert1-e^{-j2\pi fT}\rvert^2=4\sin^2(\pi fT)$
  （一階高通）、cycle-to-cycle 核 $\lvert1-e^{-j2\pi fT}\rvert^4$（二階高通）。
- 同一張 $-100$ dBc/Hz 圖：RJ $\sigma_t=447.9$ fs，但 period jitter 只有 $\sim5.6$ fs——高通核壓掉 close-in。

## 延伸閱讀

- 三個必做口算（含本例）：[numerical_feeling](/04_simulation_labs/numerical_feeling)
- noise PSD / Parseval / cyclostationary 的前置基礎：[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)
- DSP 觀點：相位 = ISF 加權 + 積分器處理的隨機過程：[dsp_view_of_phase_noise](/02_foundations/dsp_view_of_phase_noise)
- phase noise 本身怎麼來（白噪 → 1/f²）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- jitter 與 SerDes 的關聯：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
