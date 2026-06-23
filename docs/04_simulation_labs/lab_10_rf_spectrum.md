---
title: Lab 10 — phase noise 如何把載波塗成 RF 裙帶
description: 從時域 PM v(t)=cos(ω₀t+φ(t)) 做 FFT，眼見為憑 phase noise 把單線載波塗成 sidebands 裙帶，對應 [P1] Fig.8 與 dBc/Hz 的物理意義。
---

# Lab 10 — phase noise 如何把載波塗成 RF 裙帶

> **麵包屑**：[模擬實驗室](/04_simulation_labs/numerical_feeling) › 雜訊與抖動 › **本頁（RF 頻譜裙帶）**。上游：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)；下游：[lab_08](/04_simulation_labs/lab_08_jitter_integration)。

這個 lab 把抽象的相位雜訊 PSD $S_\phi(f)$ 跟你在**頻譜分析儀（spectrum analyzer）**上真正
看到的東西連起來：一個理想載波是頻譜上的**一條線**；有了 phase noise，這條線就被「塗開」
成一片 **skirt（裙帶，載波兩側連續下滑的 sidebands）**。我們在時域直接合成
$v(t)=\cos(\omega_0 t+\phi(t))$、做 FFT，眼見為憑——這正是 [P1] Fig. 8 的圖像，也是
**dBc/Hz（相對載波每赫茲的功率，decibels relative to carrier per Hz）**這個單位的由來。

> **物理直覺（先講結論）**：相位雜訊不是「另外加一個雜訊源在旁邊」，而是**載波自己的相位
> 在抖**。把抖動的相位 $\phi(t)$ 塞進餘弦的相位裡，做 phase modulation（相位調變，PM），
> 載波的能量就會從那條乾淨的譜線「漏」到鄰近的 offset 頻率上。漏多遠、漏多少，由
> $\phi(t)$ 的頻譜形狀決定：$1/f^2$ 的相位雜訊 → 載波兩側 $-20$ dB/dec 下滑的裙帶。
> 看到裙帶，就是看到了 $S_\phi(f)$ 被「搬到」載波旁邊。

## 1. 教學目標

- 從**時域** PM 訊號 $v(t)=\cos(\omega_0 t+\phi(t))$ 出發，用 FFT 看出 phase noise 造成的
  **sideband skirt（裙帶）**。
- 對照「理想載波（幾乎只有單一譜線）」與「有 phase noise（連續裙帶）」，理解 dBc/Hz
  的物理意義。
- 把 $1/f^2$ 的相位雜訊（白噪積分而成）對應到載波兩側 $-20$ dB/dec 的裙帶斜率。
- 把這張圖認成 [P1] Fig. 8 的時域版本。

## 2. 數學模型

**載波 + excess phase。** 一個被相位雜訊污染的振盪輸出寫成（規範公式 1 的特例，$A(t)$ 視為常數）：

$$
v(t)=\cos\!\big(\omega_0 t+\phi(t)\big),\qquad \omega_0=2\pi f_0 .
$$

**$\phi(t)$ 是 $1/f^2$ 的相位雜訊。** 白噪 $w(t)$ 經過相位積分器（規範公式 11 的精神：noise
先被 $\Gamma/q_{max}$ 加權、再被 $\int dt$ 積分），得到一個**隨機漫步**式的相位：

$$
\phi(t)=\frac{1}{f_s}\sum_{k\le t f_s} w_k\;\;\Longrightarrow\;\; S_\phi(f)\propto\frac{1}{f^2}.
$$

- **為什麼積分白噪得到 $1/f^2$**：積分器在頻域是 $1/(j2\pi f)$，功率轉移為 $1/f^2$；白噪
  ($S_w$ 平坦) 通過後得 $S_\phi(f)\propto S_w/f^2$。這正是 free-running 振盪器最招牌的
  $1/f^2$ skirt（規範公式 21 的頻譜形狀）。

**RF 頻譜 = PM 訊號的功率譜。** 對 $v(t)$ 加窗（Hanning）後做 FFT、取模平方、normalize 到
載波峰值：

$$
P(f)=\frac{\lvert\mathcal{F}\{v(t)\,w_{\text{win}}(t)\}\rvert^2}{\max_f\lvert\cdots\rvert^2},\qquad
P_{\text{dBc}}(\Delta f)=10\log_{10}P(f_0+\Delta f).
$$

- **小角近似下的 sideband 機制**（規範第 10.2 節「$L\approx\tfrac12 S_\phi$」）：令
  $\phi(t)=\phi_p\sin\omega_m t$，小角下

$$
\cos(\omega_0 t+\phi)\approx\cos\omega_0 t-\frac{\phi_p}{2}\big[\cos(\omega_0-\omega_m)t-\cos(\omega_0+\omega_m)t\big].
$$

  每個 sideband 相對載波的功率是 $(\phi_p/2)^2$；對連續譜的 $\phi(t)$ 疊加起來，就是裙帶。
- **Dimension check**：$\phi$、$\phi_p$ 都是 rad（無因次），$P/P_{\max}$ 無因次，
  取 $10\log_{10}$ 得 dBc ✓。offset $\Delta f$ 與 $f$ 同單位（此 lab 用 normalized 單位）。

## 3. Block diagram

```mermaid
flowchart LR
    A["white noise w(t)"] --> B["∫ dt (cumsum/fs) → φ(t)"]
    B --> C["scale → ~0.03 rad rms (小角)"]
    C --> D["v(t)=cos(2π f0 t + φ(t))"]
    D --> E["× Hanning window"]
    E --> F["|rFFT|² → normalize to carrier"]
    F --> G["10·log10 vs offset Δf → dBc skirt"]
```

## 4. Python 核心 code

逐字摘自 `simulations/lab_10_rf_spectrum.py` 的 `main()`：先把白噪 `cumsum` 成 $1/f^2$ 的
相位 `phi`（scale 到 ~0.03 rad rms 以維持小角），再合成乾淨載波與含雜訊載波，最後加 Hanning
窗做 rFFT、normalize 到峰值、轉 dB。

```python
fs = 8192.0
n = 2 ** 18
t = np.arange(n) / fs
f0 = 512.0  # carrier (normalized units), 16 samples/cycle

# 1/f^2 phase noise: integrate white noise, scale to a visible (small) rms
white = RNG.standard_normal(n)
phi = np.cumsum(white) / fs
phi -= phi.mean()
phi *= 0.03 / np.std(phi)  # ~0.03 rad rms -> small-angle regime

v_clean = np.cos(2 * np.pi * f0 * t)
v_noisy = np.cos(2 * np.pi * f0 * t + phi)

win = np.hanning(n)
def spec(x):
    X = np.fft.rfft(x * win)
    P = np.abs(X) ** 2
    return P / P.max()
f = np.fft.rfftfreq(n, 1 / fs)
Pc = spec(v_clean)
Pn = spec(v_noisy)

off = f - f0  # offset from carrier
```

- `phi = np.cumsum(white) / fs` 就是離散積分器（$1/f^2$ 的來源）。
- `phi *= 0.03 / np.std(phi)` 把 rms 壓到 ~0.03 rad，確保停留在**小角區**（這樣裙帶才正比
  $S_\phi$，不會冒出強的高階諧波 sideband）。
- `P / P.max()` 把功率 normalize 到載波峰值，於是縱軸自然是 **dBc**。

## 5. 完整 script path

`simulations/lab_10_rf_spectrum.py`
（相依模組：`simulations/common/plot_utils.py` 的 `savefig`。其餘全用 numpy/matplotlib。）

執行方式：`python scripts/run_all_sims.py`。

## 6. 參數表

| 參數 | 變數 | 值 | 說明 |
|---|---|---|---|
| 取樣率 | `fs` | $8192$（normalized） | 每秒取樣數（無因次單位） |
| 樣本數 | `n` | $2^{18}=262144$ | FFT 長度，決定頻率解析度 |
| 載波頻率 | `f0` | $512$（normalized） | 每週期 16 個取樣點 |
| 相位 rms | — | $\approx0.03$ rad | scale 後的 $\phi$ rms（小角） |
| 相位形狀 | — | $1/f^2$（cumsum 白噪） | free-running 招牌 skirt |
| 窗函數 | `win` | Hanning | 降低 FFT 旁瓣洩漏 |
| 顯示 offset | `off` | $1\sim2000$（normalized） | 載波右側裙帶範圍 |
| 隨機種子 | `RNG` | `default_rng(10)` | 結果可重現 |

> 註：此 lab 刻意用 **normalized 單位**（fs、f0 無物理量綱），重點在**形狀**（裙帶斜率與
> 單線 vs 連續譜的對比），不是絕對 Hz。

## 7. 單位表

| 量 | 符號 | 單位 | 本 lab 取值 |
|---|---|---|---|
| 時間 | $t$ | （normalized）s | $0\sim n/f_s$ |
| 載波頻率 | $f_0$ | （normalized）Hz | $512$ |
| excess phase | $\phi(t)$ | rad | rms $\approx0.03$ |
| offset 頻率 | $\Delta f$ | （normalized）Hz | $1\sim2000$ |
| 相對功率 | $P/P_{\max}$ | dBc | $-90\sim0$ |
| 相位 PSD | $S_\phi(f)$ | rad²/Hz | $\propto1/f^2$ |

## 8. 模擬圖

![phase noise 把載波塗成裙帶：藍線為理想載波（近單一譜線），紅線為含 1/f² phase noise 的連續 sideband 裙帶，橫軸為對載波 offset、縱軸為 dBc](/figures/rf_spectrum_phase_noise_sidebands.png)

## 9. 如何解讀圖

- **藍線（理想載波）**：能量幾乎全集中在載波本身，offset 一拉開就掉到很低——在頻譜上
  「幾乎只有一條線」。殘留的小裙帶來自 FFT 的有限長度與窗洩漏，不是物理 phase noise。
- **紅線（有 phase noise）**：載波兩側出現連續、隨 offset 增大而下滑的 **skirt**。在
  log-offset 軸上接近直線下滑，對應 $1/f^2$ 的 $-20$ dB/dec：這就是 dBc/Hz 曲線的時域起源。
- **單線 vs 裙帶的對比**就是這張圖的核心訊息：相位在抖 → 載波能量外漏 → 譜線變裙帶。
  「裙帶越低、越陡」代表相位雜訊越小。
- **怎麼用**：頻譜分析儀上量到的裙帶高度（相對載波、每 Hz），就是 $\mathcal{L}(\Delta f)$
  (dBc/Hz)。把它積分（見 [lab_08](/04_simulation_labs/lab_08_jitter_integration)）就得到
  rms jitter。本 lab 讓你「看見」這條曲線是怎麼從時域 PM 長出來的。

## 10. 對應 paper 公式/figure

- **核心對應**：[P1] A. Hajimiri and T. H. Lee, *"A General Theory of Phase Noise in
  Electrical Oscillators,"* IEEE JSSC, 33(2), 1998，**Fig. 8**——展示相位雜訊把載波塗成
  sideband 裙帶。本 lab 是它的**時域合成版本**。
  [P1] Fig. 8 在 p.183（已對照原始 PDF）。
- 載波分解：規範公式 1，$V_{out}(t)=A(t)f(\omega_0 t+\phi(t))$（此處取 $A$ 常數、$f=\cos$）。
- sideband 機制（小角 PM → $\mathcal{L}\approx\tfrac12 S_\phi$）：規範第 10.2 節「$L\approx\tfrac12 S_\phi$（小角 PM）」。
- $1/f^2$ skirt 的根源：相位積分白噪，與規範公式 21（[P1] Eq.(21), p.185）的頻譜形狀一致。
- 對應網站圖 `rf_spectrum_phase_noise_sidebands.png`；延伸見
  [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)、
  [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)。

## 11. 限制與 approximation

- **這是 pedagogical toy model，非 transistor-level**：我們直接「注入」一個 $1/f^2$ 相位
  雜訊，沒有真正模擬電晶體 noise 經 ISF 加權的全流程；目的是看「裙帶長什麼樣」。
- **小角假設**：$\phi$ rms $\approx0.03$ rad $\ll1$，所以裙帶正比 $S_\phi$、無強高階 sideband。
  相位偏移大時 PM 會生出載波壓縮與高階 sidebands，本圖不涵蓋。
- **normalized 單位**：`fs`、`f0` 無物理量綱，橫軸 offset 也是 normalized；重點是**形狀與
  對比**，不是絕對 Hz。要對到真實 5 GHz、dBc/Hz，需設定真實取樣率與 $S_\phi$ 絕對位準。
- **FFT 假象**：藍線的殘留裙帶與紅線遠端的地板，部分來自有限長度 FFT 與 Hanning 窗洩漏，
  不全是物理 phase noise。加大 `n`、換更尖的窗可降低。
- **單一隨機實現**：圖來自固定種子的一條 $\phi(t)$；嚴格的 $\mathcal{L}(f)$ 要對多次實現
  做 ensemble 平均（Welch），見 [lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise)。

## 重點回顧

- phase noise 不是旁邊多一個源，而是**載波自己的相位在抖** → 能量從單線外漏成 sideband 裙帶。
- 時域 $v(t)=\cos(\omega_0 t+\phi(t))$ 做 FFT，就能「看見」[P1] Fig. 8 的裙帶。
- $1/f^2$ 相位雜訊（積分白噪）→ 載波兩側 $-20$ dB/dec 的裙帶；裙帶高度即 dBc/Hz。
- 小角 PM 下每個 sideband 相對功率 $(\phi_p/2)^2$，疊加成連續譜（$\mathcal{L}\approx\tfrac12 S_\phi$）。

## 延伸閱讀

- 裙帶怎麼從白噪長出來：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- dBc/Hz 與 jitter 種類：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- 把裙帶積成 jitter：[lab_08_jitter_integration](/04_simulation_labs/lab_08_jitter_integration)
- 數值換算手感：[numerical_feeling](/04_simulation_labs/numerical_feeling)
- **用在設計/理論**：實驗室如何量這條裙帶（SA／delay-line／cross-correlation）→ [measurement_and_spurs](/06_design_insights/measurement_and_spurs)
