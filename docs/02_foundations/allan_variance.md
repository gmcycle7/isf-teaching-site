---
title: Allan variance：相位雜訊的時域對應
description: 從兩樣本（Allan）變異數 σy²(τ)=⟨½(ȳ_{k+1}−ȳ_k)²⟩ 出發，逐步推頻域積分 σy²=2∫S_y sin⁴(πfτ)/(πfτ)² df、S_y=(f²/f0²)S_φ，並推導五種冪律雜訊的 ADEV 斜率對照表（white/flicker PM τ⁻¹、white FM τ⁻¹ᐟ²、flicker FM τ⁰ floor、RW FM τ^{+1/2}），解釋為何時鐘界用 ADEV 而非普通頻率方差。進一步自推完整前因子表：證明 ∫sin⁴u/u³du=ln2，得 flicker-FM floor 常數 σy²=2·ln2·h₋₁；由 canonical 1/f³ corner 算 floor=1.06e-9 與 τ_knee=113 μs，lab_19 驗絕對高度（measured/theory=1.004）。嵌入 allan_deviation 與 allan_flicker_floor 圖，含 3 個 worked example。
---

import AdevLiveExplorer from '@site/src/components/AdevLiveExplorer';

# Allan variance：相位雜訊的時域對應

> 先備：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) · [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) ｜ 接下來：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)

前面幾頁我們都站在**頻域**看振盪器的不完美：把抖動寫成 SSB phase noise $\mathcal{L}(\Delta f)$（單位 dBc/Hz）或 phase PSD $S_\phi(f)$（單位 $\text{rad}^2/\text{Hz}$），再把它積分成 rms jitter $\sigma_t$（見 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)）。這套語言對 RF/通訊電路最自然。但**時鐘、頻率標準、GPS、原子鐘**這一行的人，講的是另一套語言：**Allan variance（亞倫變異數）** 與它的平方根 **Allan deviation / ADEV（亞倫偏差）** $\sigma_y(\tau)$。這頁要回答：

- $\sigma_y(\tau)$ 到底量的是什麼？為什麼定義成「**相鄰兩段平均頻率之差**」的均方？
- 它跟我們熟的 $S_\phi(f)$、$\mathcal{L}(\Delta f)$ 怎麼換算？
- 為什麼**五種冪律雜訊**在 ADEV log–log 圖上各有一條特徵斜率，而且這些斜率「一眼就能讀出雜訊型態」？
- 為什麼時鐘界**寧可用 ADEV 也不用普通的頻率樣本變異數**？

> **物理直覺（先講結論）**：你拿一支碼錶（被測振盪器）去比對一支完美時鐘，每隔 $\tau$ 秒記一次「這 $\tau$ 秒內我的平均頻率比標稱快/慢多少」，得到一串**分數頻率偏差** $\bar y_k$。普通變異數會問「這些 $\bar y_k$ 離它們的總平均有多遠」——可是對 flicker（$1/f$）與 random-walk 雜訊，**總平均根本不存在**（會隨資料越收越久而漂移），普通變異數會越算越大、不收斂。Allan 的高招是：**不跟總平均比，只跟隔壁那一段比**——$\tfrac12\langle(\bar y_{k+1}-\bar y_k)^2\rangle$。相鄰相減把「慢漂移」差掉了，於是即使對 flicker/RW 也收斂、也可重複量到一個穩定數字。代價是它變成一個**對 $\tau$ 的函數**：你選多長的觀測閘 $\tau$，就看到該時間尺度上的穩定度。

ADEV 是「時域版的 phase noise」：同一份物理（同一條 $S_\phi(f)$），換一個座標看而已。下面逐步把兩邊接起來。

## 第 1 步：分數頻率偏差 $y(t)$ 與它的 PSD $S_y(f)$

先定義主角。設被測訊號的瞬時相位為 $\omega_0 t+\phi(t)$，其中 $\phi(t)$ 是 excess phase（多餘相位，相對理想線性相位的隨機偏移，單位 rad）。**瞬時分數頻率偏差**（fractional frequency deviation，無因次）定義為相位偏差對時間的微分再除以標稱角頻率：

$$
y(t)=\frac{1}{\omega_0}\frac{d\phi(t)}{dt}=\frac{1}{2\pi f_0}\,\dot\phi(t).
$$

- **物理意義**：$y$ 是「此刻頻率比標稱頻率快了百分之多少」。$y=10^{-9}$ 表示頻率偏了 1 ppb（十億分之一）。
- **單位檢查**：$\dot\phi$ 是 $\text{rad/s}$，$\omega_0$ 是 $\text{rad/s}$，相除無因次 ✓。$y$ 無因次正是「分數」的意思。

**$y$ 的 PSD 與 $\phi$ 的 PSD 的關係。** 微分在頻域是乘 $j2\pi f$，功率譜就乘上其模平方 $(2\pi f)^2$。因此（規範 11.2）：

$$
S_y(f)=\frac{(2\pi f)^2}{(2\pi f_0)^2}\,S_\phi(f)=\frac{f^2}{f_0^2}\,S_\phi(f).
$$

- **用到的數學**：對平穩過程 $a(t)\to\dot a(t)$，PSD 乘 $|j2\pi f|^2=(2\pi f)^2$（LTI 濾波器 $H(f)=j2\pi f$）。
- **單位檢查**：$S_\phi$ 是 $\text{rad}^2/\text{Hz}$，乘無因次的 $f^2/f_0^2$，得 $S_y$ 單位 $1/\text{Hz}$（無因次量的 PSD）✓。
- **關鍵記號**：這條 $S_y=(f^2/f_0^2)S_\phi$ 是「相位雜訊 ↔ 頻率雜訊」的轉接頭，等一下整個斜率對照表都靠它。微分把 $f$ 的冪次**加 2**：$S_\phi\sim f^{-2}$（我們的招牌 $1/f^2$）對應 $S_y\sim f^{0}$（白色 FM）。

## 第 2 步：兩樣本（Allan）變異數的定義

把連續的 $y(t)$ 切成一段段長度 $\tau$ 的閘，第 $k$ 段的**平均分數頻率**是

$$
\bar y_k=\frac{1}{\tau}\int_{t_k}^{t_k+\tau}y(t)\,dt=\frac{x(t_k+\tau)-x(t_k)}{\tau},
\qquad x(t)\equiv\int^{t}y(t')\,dt'=\frac{\phi(t)}{2\pi f_0}.
$$

這裡 $x(t)$ 是**時間誤差**（time error，被測時鐘相對理想時鐘的累積時間偏移，單位 s）——注意它正是相位除以 $2\pi f_0$，也就是 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) 裡的 $\Delta t=\Delta\phi/(2\pi f_0)$。所以 $\bar y_k$ 不過是「相鄰兩個時刻的時間誤差之差，除以閘長」。

**兩樣本（Allan）變異數**定義為相鄰兩段平均頻率之差的均方，再乘 $\tfrac12$（規範 11.2）：

$$
\sigma_y^2(\tau)=\Big\langle\tfrac12\big(\bar y_{k+1}-\bar y_k\big)^2\Big\rangle.
$$

ADEV 就是它的平方根 $\sigma_y(\tau)=\sqrt{\sigma_y^2(\tau)}$。

- **那個 $\tfrac12$ 是幹嘛的**：若 $\bar y_{k+1}$ 與 $\bar y_k$ 互相獨立、各自變異數 $\sigma^2$，則 $\langle(\bar y_{k+1}-\bar y_k)^2\rangle=2\sigma^2$，乘 $\tfrac12$ 剛好還原成 $\sigma^2$。也就是說，**對白色 FM（相鄰段獨立）這個常態化讓 ADEV 等於古典標準差**——Allan 刻意這樣定，好讓最常見的情形下兩套語言數字一致。
- **為什麼用「相鄰差」**：差分是一個**高通**運算，把 DC 與極低頻（慢漂移、老化、未知總平均）擋掉。這就是它對 flicker/RW 仍收斂的祕密（第 5 步詳述）。
- **單位檢查**：$\bar y$ 無因次 → $\sigma_y^2$ 無因次、$\sigma_y$ 無因次 ✓。

**用時間誤差 $x$ 寫成「二階差分」。** 把 $\bar y_k=[x(t_{k}+\tau)-x(t_k)]/\tau$ 代入，相鄰兩段（$t_{k+1}=t_k+\tau$）：

$$
\bar y_{k+1}-\bar y_k=\frac{x_{k+2}-2x_{k+1}+x_k}{\tau},
$$

其中 $x_k\equiv x(t_k)$、取樣間隔 $\tau$。分子 $x_{k+2}-2x_{k+1}+x_k$ 正是時間誤差的**二階差分**（離散二次微分）。這正是模擬程式 `lab_19_allan.py` 裡 `d = x[2m:] - 2*x[m:-m] + x[:-2m]` 那一行在做的事。

## 第 3 步：把定義搬到頻域——傳遞函數核 $\sin^4(\pi f\tau)/(\pi f\tau)^2$

我們要證明的目標是（規範 11.2）：

$$
\sigma_y^2(\tau)=2\int_0^{\infty}S_y(f)\,\frac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df.
$$

推導思路：$\sigma_y^2(\tau)$ 是某個**線性濾波後訊號的功率**，而線性濾波後的功率 $=\int S_{\text{in}}(f)\,|H(f)|^2\,df$。我們只要找出「從 $y(t)$ 算到 $\tfrac{1}{\sqrt2}(\bar y_{k+1}-\bar y_k)$」這個運算的轉移函數 $H(f)$，把 $|H(f)|^2$ 算出來即可。

**第 (i) 步：閘平均 = 與矩形窗卷積。** $\bar y_k=\frac1\tau\int_{t_k}^{t_k+\tau}y\,dt$ 是 $y$ 與一個寬 $\tau$、高 $1/\tau$ 的矩形窗卷積後在 $t_k$ 取樣。矩形窗的頻率響應是 sinc：

$$
H_{\text{avg}}(f)=\frac{1}{\tau}\int_0^{\tau}e^{-j2\pi f t}\,dt=e^{-j\pi f\tau}\,\frac{\sin(\pi f\tau)}{\pi f\tau}.
$$

- **用到的數學**：矩形窗 $\leftrightarrow$ sinc（傅立葉變換的基本對）。
- $\dfrac{\sin(\pi f\tau)}{\pi f\tau}$ 就是 normalized sinc；前面 $e^{-j\pi f\tau}$ 是窗中心造成的線性相位。

**第 (ii) 步：相鄰相減 = 乘一個一階差分核。** $\bar y_{k+1}-\bar y_k$ 把同一個閘平均錯開 $\tau$ 再相減，對應頻域乘上 $\big(e^{-j2\pi f\tau}-1\big)$，其模平方是

$$
\big|e^{-j2\pi f\tau}-1\big|^2=2-2\cos(2\pi f\tau)=4\sin^2(\pi f\tau).
$$

（用了半角 $1-\cos2\theta=2\sin^2\theta$，這裡 $\theta=\pi f\tau$。）

**第 (iii) 步：把三件事乘起來。** 整體運算 $g(t)=\tfrac{1}{\sqrt2}(\bar y_{k+1}-\bar y_k)$（那個 $\tfrac{1}{\sqrt2}$ 來自定義裡的 $\tfrac12$ 開根號），其轉移函數模平方：

$$
|H(f)|^2=\underbrace{\tfrac12}_{\text{def.}\,\frac12}\cdot\underbrace{\Big(\frac{\sin(\pi f\tau)}{\pi f\tau}\Big)^2}_{\text{閘平均}}\cdot\underbrace{4\sin^2(\pi f\tau)}_{\text{相鄰差}}=\frac{2\sin^4(\pi f\tau)}{(\pi f\tau)^2}.
$$

**第 (iv) 步：套 Wiener–Khinchin（功率 = ∫ PSD × |H|²）。** 用單邊 PSD（$\int_0^\infty$）：

$$
\sigma_y^2(\tau)=\int_0^{\infty}S_y(f)\,|H(f)|^2\,df=2\int_0^{\infty}S_y(f)\,\frac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df.\qquad\checkmark
$$

得到規範 11.2 的頻域積分式。

- **物理意義**：$\sin^4/(\cdot)^2$ 是一個**帶通核**：在 $f\to0$ 像 $f^2$（高通、把慢漂移擋掉）、在高頻像 $1/f^2$（低通、把超快雜訊壓掉）、峰值落在 $f\tau\sim 0.5$ 附近。**選 $\tau$ 等於選這個帶通看哪一段頻率**——大 $\tau$ 看低頻、小 $\tau$ 看高頻。
- **單位檢查**：$S_y$ 是 $1/\text{Hz}$、核無因次、$df$ 是 Hz，積出無因次 → $\sigma_y^2$ 無因次 ✓。

> **這就是「時域 ↔ 頻域同一件事」的橋**：給你任何 $S_\phi(f)$，先用第 1 步轉成 $S_y$，再代進這條積分就得 ADEV；反之量到的 ADEV 也能反推 $S_y$、$S_\phi$。下面的斜率表全部是這條積分對冪律 $S_y\sim f^\alpha$ 的結果。

## 第 4 步：五種冪律雜訊的 ADEV 斜率對照表

頻率標準界把雜訊寫成**冪律疊加**（power-law model）。用 $S_y(f)=h_\alpha f^\alpha$ 描述每一種，$\alpha$ 從 $-2$ 到 $+2$。把每種代進第 3 步的積分，就得到 $\sigma_y(\tau)\propto\tau^\mu$ 的特徵斜率。下表是頻率計量學的**核心對照表**（PM = phase modulation 相位調制型、FM = frequency modulation 頻率調制型）：

| 雜訊型態 | $S_\phi(f)$ 斜率 | $S_y(f)=\frac{f^2}{f_0^2}S_\phi$ 斜率 | $\sigma_y^2(\tau)\propto$ | **ADEV $\sigma_y(\tau)\propto$** |
|---|---|---|---|---|
| white PM（白相位） | $f^{0}$ | $f^{+2}$ | $\tau^{-2}$ | $\tau^{-1}$ |
| flicker PM（閃爍相位） | $f^{-1}$ | $f^{+1}$ | $\tau^{-2}$（含 $\ln$ 修正） | $\tau^{-1}$ |
| white FM（白頻率） | $f^{-2}$ | $f^{0}$ | $\tau^{-1}$ | $\tau^{-1/2}$ |
| flicker FM（閃爍頻率） | $f^{-3}$ | $f^{-1}$ | $\tau^{0}$ | $\tau^{0}$（floor，地板） |
| random-walk FM（隨機漫步頻率） | $f^{-4}$ | $f^{-2}$ | $\tau^{+1}$ | $\tau^{+1/2}$ |

> 注意最關鍵的一列：我們招牌的 **white FM（$S_\phi\sim1/f^2$，由白噪經相位積分而來，見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)）對應 ADEV 斜率 $\tau^{-1/2}$**。換句話說，那條 $-20$ dB/decade 的 phase noise 裙邊，在時域 ADEV 圖上長成一條 $-1/2$ 斜率的線。

### 每種斜率「為何是這斜率」的直覺

**(a) white FM → $\tau^{-1/2}$（最該記住的一條）。** $S_y\sim f^0$ 是白色，$y(t)$ 是白噪。$\bar y_k$ 是把白噪在閘 $\tau$ 內平均——白噪平均 $N$ 個獨立樣本，變異數降 $1/N\propto1/\tau$，故 $\sigma_y^2\propto1/\tau$、$\sigma_y\propto\tau^{-1/2}$。**直覺**：量越久平均越穩，標準誤差像 $1/\sqrt{\tau}$ 掉——這就是「白頻率雜訊下，越長平均越準」的那個你熟悉的 $\sqrt N$ 律。等價地，$y$ 白 ⇒ 時間誤差 $x=\int y$ 是 random walk，相鄰段差的方差 $\propto\tau$，除以 $\tau^2$ 得 $\propto1/\tau$。

**(b) flicker FM → $\tau^{0}$（地板 / floor）。** $S_y\sim1/f$（$1/f$ 頻率雜訊）。$1/f$ 過程的奇妙性質是**尺度不變（scale-invariant）**：在任何時間尺度看起來統計一樣。把它丟進那個帶通核，積分結果**與 $\tau$ 無關**——ADEV 變成一條水平線。**直覺**：device 的 $1/f$（flicker）雜訊上轉成 $1/f^3$ phase noise（見 [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)），到了時域就是「再怎麼延長平均時間都不會更穩」的那塊**地板**。這塊地板是石英/原子振盪器中長期穩定度的**根本極限**，工程上稱 flicker floor。

**(c) random-walk FM → $\tau^{+1/2}$（往上走）。** $S_y\sim1/f^2$，$y(t)$ 本身是 random walk（積分白噪）。平均時間越長，$y$ 自己已經漂走更多，相鄰段差反而**變大**：$\sigma_y^2\propto\tau$、$\sigma_y\propto\tau^{+1/2}$。**直覺**：溫度漂移、老化前兆這類「會越走越遠」的低頻過程，量越久越糟。ADEV 圖右半邊往上翹通常就是它。

**(d) white PM 與 flicker PM → 都 $\tau^{-1}$（最陡、左半邊）。** PM 型雜訊集中在高頻（$S_y\sim f^{+2}$、$f^{+1}$），被閘平均的 $\text{sinc}^2$ 強力壓制，$\tau$ 一拉長就掉得很快，ADEV $\propto\tau^{-1}$（比 white FM 的 $\tau^{-1/2}$ 還陡）。**直覺**：純相位雜訊（例如量測系統的加性白噪、緩衝器熱雜訊）在短 $\tau$ 顯著、長 $\tau$ 被平均掉。**注意**：white PM 與 flicker PM 在 ADEV 上**斜率相同（都 $\tau^{-1}$）無法區分**——這正是 ADEV 的一個弱點，催生了改良版 **MDEV（modified Allan deviation）**，它讓 white PM 走 $\tau^{-3/2}$、flicker PM 走 $\tau^{-1}$ 而可分辨（MDEV 屬延伸主題，此處不展開）。

**口訣**：從左到右、$\tau$ 由小到大，ADEV 斜率走 $-1\to-1/2\to0\to+1/2$，像一個「先掉、見底、再爬」的**澡盆曲線（bathtub）**。底部那個最低點對應**最佳平均時間** $\tau_{\text{opt}}$——量測或守時時就挑這個 $\tau$ 最穩。

## 第 5 步：為什麼時鐘界用 ADEV，而不用普通頻率方差？

這是本頁的「為什麼」核心。考慮你想用最直覺的方式描述頻率穩定度：取 $M$ 個頻率樣本 $\bar y_k$，算**普通樣本變異數**（也叫 N-sample / standard variance）

$$
\sigma^2_{\text{std}}(M,\tau)=\frac{1}{M-1}\sum_{k=1}^{M}\big(\bar y_k-\overline{\bar y}\big)^2,\qquad\overline{\bar y}=\frac1M\sum_k\bar y_k.
$$

問題出在它**減的是「全體平均」$\overline{\bar y}$**。

**對 white FM 沒事。** white FM 是平穩的，$\overline{\bar y}$ 收斂到真值，$\sigma^2_{\text{std}}$ 也收斂，跟 ADEV 一致。

**對 flicker FM 與 random-walk FM 就爆掉。** 這兩種有很強的低頻（甚至發散的）能量：

- 它們**不是均值遍歷（non-ergodic in the mean）**：$\overline{\bar y}$ 不收斂，你量越久、$M$ 越大，$\overline{\bar y}$ 自己還在漂。
- 結果 $\sigma^2_{\text{std}}(M,\tau)$ **隨樣本數 $M$ 單調增大、不收斂**——你報出來的「頻率不穩定度」會取決於「你量了多久」，這在計量上是災難（不可重複、不可比較）。
- 數學上：標準變異數對 $S_y(f)$ 的等效核在 $f\to0$ 只像 $f^0$（DC 不被擋），碰到 $S_y\sim1/f$ 或 $1/f^2$ 時積分 $\int_0\frac{df}{f}$、$\int_0\frac{df}{f^2}$ **在低頻發散**。

**ADEV 的解法：用「相鄰差」代替「減全體平均」。** 第 3 步算過 ADEV 的等效核在 $f\to0$ 像 $f^2$（$\sin^4(\pi f\tau)\sim(\pi f\tau)^4$，除以 $(\pi f\tau)^2$ 得 $\sim f^2$）。這個 $f^2$ 的高通**把低頻發散壓住了**：

- flicker FM（$S_y\sim1/f$）：被積函數 $\sim f^2\cdot f^{-1}=f$，在 $f\to0$ 收斂 ✓。
- random-walk FM（$S_y\sim1/f^2$）：被積函數 $\sim f^2\cdot f^{-2}=f^0$，在 $f\to0$ 仍收斂（邊界情形，但有限）✓。

所以 ADEV 對到 random-walk FM 為止都是**收斂、可重複、與量測時長無關**的良好定義。這就是 1966 年 David Allan 提出它、而頻率標準界（NIST、IEEE）採為標準的根本原因：

> **一句話**：普通頻率方差對 flicker/RW 雜訊**不收斂**（隨資料越收越久而發散），ADEV 用「相鄰兩段相減」這個一階差分把低頻漂移擋掉，換來一個**對 $\tau$ 收斂、可重複量測**的穩定度指標。

- **延伸**：若需要對 white PM 與 flicker PM 也能區分，用 MDEV；若要看「某時間誤差有沒有界」，用 TDEV / time variance。本頁聚焦最常用的 overlapping ADEV。

## 對應模擬圖

**lab_19**（`simulations/lab_19_allan.py`） 用 FFT 整形產生三種 FM 雜訊的分數頻率 $y(t)$，積分成時間誤差 $x(t)=\int y\,dt$，再用**重疊式（overlapping）Allan deviation** 估計：對每個 $\tau=m\tau_0$，算二階差分 $x_{k+2m}-2x_{k+m}+x_k$ 的均方並開根。圖中實線是模擬量到的 ADEV、虛線是理論斜率，三條斜率精準落在 $-1/2$、$0$、$+1/2$：

![三種 FM 雜訊的 Allan deviation，斜率分別為 white FM τ⁻¹ᐟ²、flicker FM τ⁰、random-walk FM τ^{+1/2}](/figures/allan_deviation.png)

| 項目 | 值 | 說明 |
|---|---|---|
| 模型 | toy / illustrative（非 transistor-level） | 用 FFT 冪律整形合成 $S_y\sim f^\alpha$ |
| white FM | $S_y\sim f^{0}$ | ADEV 斜率 $\tau^{-1/2}$（藍） |
| flicker FM | $S_y\sim f^{-1}$ | ADEV 斜率 $\tau^{0}$，flicker floor（綠） |
| random-walk FM | $S_y\sim f^{-2}$ | ADEV 斜率 $\tau^{+1/2}$（紅） |
| 估計法 | overlapping ADEV | 二階差分核 $x_{k+2m}-2x_{k+m}+x_k$ |
| 縱軸 | 正規化 $\sigma_y/\sigma_y(\tau_0)$ | 只比斜率，絕對值任意 |

核心 Python（完整 script：`simulations/lab_19_allan.py`，函式 `overlapping_adev`）：

```python
import numpy as np

def overlapping_adev(x, tau0, ms):
    """由時間誤差樣本 x（間隔 tau0）算重疊式 Allan deviation。"""
    x = np.asarray(x); N = len(x); out = []
    for m in ms:
        if N - 2 * m < 1:
            out.append(np.nan); continue
        d = x[2 * m:] - 2 * x[m:-m] + x[:-2 * m]      # 時間誤差二階差分
        avar = np.sum(d ** 2) / (2 * (N - 2 * m) * (m * tau0) ** 2)
        out.append(np.sqrt(avar))
    return np.array(out)
```

`d` 那一行就是第 2 步的二階差分 $x_{k+2m}-2x_{k+m}+x_k$；除以 $2(N-2m)(m\tau_0)^2$ 對應 $\sigma_y^2=\langle\tfrac12(\bar y_{k+1}-\bar y_k)^2\rangle$ 的離散估計（$\tau=m\tau_0$）。

## 互動：自己「生」一條時間序列、自己估 ADEV（統計 vs 解析）

上面的 lab_19 圖是**先驗地**告訴你三條斜率；但實務上你手上永遠只有**一條有限長的量測時間序列**，ADEV 是從這條序列**估計**出來的統計量，不是天上掉下來的解析曲線。下面這個小工具把「生成 → 估計」的完整流程搬進瀏覽器，跟上面的 [interactive_calculator](/04_simulation_labs/interactive_calculator) 頁的 `AllanDeviationExplorer`（純解析斜率、沒有隨機性）互補：

- 用種子化亂數（seeded PRNG，換句話說「同一顆種子永遠生出同一條序列」）生一條長度 $N=4096$ 的分數頻率序列 $y[k]$，成分是滑桿控制的 white FM + random-walk FM，外加一個可選的、用簡易 $-10$dB/decade 濾波器串接**近似**出來的 flicker FM（誠實地說：只是近似，見下方說明）。
- 對這條序列積分成時間誤差 $x[k]=\sum y[k]\tau_0$，再用第 2–3 步同一條**重疊式（overlapping）二階差分**公式，對 $\tau=\tau_0,2\tau_0,4\tau_0,\dots$（倍頻，一路到 $N/4$）**直接估計** ADEV，疊上 $\pm\sigma/\sqrt{\text{pairs}}$ 誤差棒。
- 虛線是同一組 $h$ 係數的**解析**閉式（第 4 步/前因子表的公式，獨立過程變異數相加）——藍點應該圍著虛線散布。
- 按「重抽」換一顆新種子：**小 $\tau$ 的點幾乎不動**（幾千個獨立 pairs，統計穩定），**大 $\tau$ 的點會明顯亂跳**（$\tau=N/4$ 時只剩約 4 個獨立 pairs）——這正是本節要傳達的教訓：**ADEV 曲線最右端那幾個點的「地板」或「上翹」看起來很像一個確定的物理現象，但如果背後只有個位數的獨立樣本支撐，那幾個點本身就有很大的統計不確定性**，量測時该做的是拉長總記錄長度、而不是照單全收最右端的形狀。

<AdevLiveExplorer />

**estimator 的獨立驗證**：把生成器切純 white FM（關掉 random-walk 與 flicker）、$h_0=10^{-19}$，在 Node 用同一套演算法跑 200 次重抽：每個倍頻 $\tau$ 的「量測/理論（$h_0/2\tau$ 閉式）」比值都落在 $0.94$–$1.00$（最大 $\tau$ 因 pairs 最少而略偏低，正是上一段講的效應），200 條曲線平均後 log–log 斜率擬合得 $-0.508$（理論 $\tau^{-1/2}$）；預設種子（seed=1234）單獨一次在最小 $\tau$ 已給出比值 $0.993$。widget 內的「最小 τ 的量測/理論」讀數就是這個自我檢查的即時版本。

## Worked examples 數值例題

下面兩題用嚴格格式：**題目 → 逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證**。第一題練「斜率讀圖」、第二題示範**由 $\mathcal{L}(f)$ 估 ADEV**（最實用的工程換算）。

### 例 1：由 ADEV 兩點讀出雜訊型態並外推

> **題**：某 OCXO（恆溫晶振）量到 $\sigma_y(1\,\text{s})=2\times10^{-12}$、$\sigma_y(10\,\text{s})=6.3\times10^{-13}$。問此區段是哪種雜訊主導？並外推 $\sigma_y(100\,\text{s})$。

**逐步：**

1. 算斜率 $\mu$（$\sigma_y\propto\tau^\mu$）：

$$
\mu=\frac{\log_{10}\!\big(\sigma_y(10)/\sigma_y(1)\big)}{\log_{10}(10/1)}=\frac{\log_{10}(6.3\times10^{-13}/2\times10^{-12})}{\log_{10}10}=\frac{\log_{10}(0.315)}{1}\approx-0.5.
$$

2. 對照第 4 步的表：$\mu=-1/2$ ⇒ **white FM 主導**（$S_y\sim f^0$，等價 $S_\phi\sim1/f^2$）。
3. 外推到 $\tau=100\,\text{s}$（仍 white FM、$\tau^{-1/2}$）：

$$
\sigma_y(100)=\sigma_y(1)\times(100)^{-1/2}=2\times10^{-12}\times\frac{1}{10}=2\times10^{-13}.
$$

**結果：** white FM 主導；$\sigma_y(100\,\text{s})\approx2\times10^{-13}$。

**Dimension check：** $\sigma_y$ 全程無因次（分數頻率）；斜率 $\mu$ 由兩個無因次量取 log 相除得無因次 ✓。

```python
import numpy as np
mu = np.log10(6.3e-13/2e-12)/np.log10(10)          # -> -0.50  => white FM
adev_100 = 2e-12*(100/1)**mu
print(round(mu,2), f"{adev_100:.2e}")              # -> -0.5  2.00e-13
```

### 例 2：由白噪 $1/f^2$ 的 $\mathcal{L}(f)$ 估 ADEV

> **題**：5 GHz 振盪器在 1/f² 區量到 $\mathcal{L}(1\,\text{MHz})=-100\,\text{dBc/Hz}$（白色 FM 段）。估 $\sigma_y(\tau)$ 隨 $\tau$ 的關係，並給 $\sigma_y(1\,\text{ms})$ 的數值。沿用 canonical 例 C 的設定（$f_0=5\,\text{GHz}$）。

**逐步：**

1. **dBc/Hz → linear $\mathcal{L}$**：$\mathcal{L}(1\,\text{MHz})=10^{-100/10}=10^{-10}\,\text{rad}^2/\text{Hz}$（單邊）。
2. **$\mathcal{L}\to S_\phi$**（小角 $\mathcal{L}\approx\tfrac12 S_\phi$，見規範 Eq.16）：$S_\phi(1\,\text{MHz})=2\mathcal{L}=2\times10^{-10}\,\text{rad}^2/\text{Hz}$。
3. **寫成 $1/f^2$ 顯式**：white FM 段 $S_\phi(f)=\dfrac{h_{-2}}{f^2}$。代 $f=10^6$：$h_{-2}=S_\phi(10^6)\cdot(10^6)^2=2\times10^{-10}\times10^{12}=2\times10^{2}=200\,\text{rad}^2\,\text{Hz}$。
4. **轉成 $S_y$**：$S_y(f)=\dfrac{f^2}{f_0^2}S_\phi=\dfrac{f^2}{f_0^2}\cdot\dfrac{h_{-2}}{f^2}=\dfrac{h_{-2}}{f_0^2}\equiv h_0$（果然白色、與 $f$ 無關）。
   $h_0=\dfrac{200}{(5\times10^9)^2}=\dfrac{200}{2.5\times10^{19}}=8.0\times10^{-18}\,\text{Hz}^{-1}$。
5. **white FM 的 ADEV 閉式**（標準結果，對 $S_y=h_0$ 積分第 3 步的核得）：

$$
\sigma_y^2(\tau)=\frac{h_0}{2\tau}\quad\Longrightarrow\quad\sigma_y(\tau)=\sqrt{\frac{h_0}{2\tau}}.
$$

6. 代 $\tau=10^{-3}\,\text{s}$：$\sigma_y^2=\dfrac{8.0\times10^{-18}}{2\times10^{-3}}=4.0\times10^{-15}$，$\sigma_y=6.3\times10^{-8}$。

**結果：** $S_y$ 為白色 $h_0=8.0\times10^{-18}\,\text{Hz}^{-1}$；$\sigma_y(\tau)=\sqrt{h_0/2\tau}\propto\tau^{-1/2}$（符合 white FM）；$\sigma_y(1\,\text{ms})\approx6.3\times10^{-8}$。

**Dimension check：** $h_0$ 單位 $\text{Hz}^{-1}=\text{s}$；$h_0/\tau$ 得無因次；開根仍無因次 → $\sigma_y$ 無因次 ✓。斜率 $\sigma_y\propto\tau^{-1/2}$ 與表中 white FM 列一致 ✓。

> **手感**：$6.3\times10^{-8}$ 在 1 ms 看似大，但 5 GHz 自由振盪器在 1 ms 內本來就會漂掉很多相位（這就是為什麼要鎖相環 PLL/CDR 把長期頻率釘住，見 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)）。把 $\tau$ 拉到 1 s，$\sigma_y$ 再掉 $\sqrt{1000}\approx31.6$ 倍到 $\sim2\times10^{-9}$。

```python
import numpy as np
f0, L_dbc, foff = 5e9, -100.0, 1e6
S_phi = 2*10**(L_dbc/10)                 # rad^2/Hz at foff (小角 L≈½S_φ)
h_2   = S_phi*foff**2                     # S_phi = h_2/f^2  => h_2
h0    = h_2/f0**2                         # S_y = h0 (white FM)
adev  = lambda tau: np.sqrt(h0/(2*tau))
print(f"{h0:.1e}", f"{adev(1e-3):.1e}")  # -> 8.0e-18  6.3e-08
```

（此處 white FM 閉式 $\sigma_y^2=h_0/2\tau$ 是標準頻率計量結果——下一節會用 $I_2=\pi/4$ 在站內把它完整推出來，且 lab_19 已擴充為**連絕對高度一起驗證**，不只驗斜率。）

## 完整前因子表：flicker-FM floor 常數 $\sigma_y^2=2\ln 2\cdot h_{-1}$

第 4 步的斜率表只回答「$\sigma_y\propto\tau^\mu$」，沒說**絕對高度**。工程上真正要的是：給定 $S_y$ 的冪律係數，ADEV 每一段的**確切數值**——尤其是 flicker-FM 那塊「再怎麼平均都下不去」的地板到底多高。這一節把第 3 步的積分對五種冪律**逐一積出來**：重頭戲是 flicker FM 的 floor 常數，它是一個漂亮的 $\ln 2$；white FM 與 RW FM 用同一招順手拿下；兩個 PM 型則會看到「為什麼非得引入高頻截止 $f_h$ 不可」。

### 記號：冪律係數 $h_\alpha$（IEEE 1139 標準記法）

頻率計量標準把 $S_y$ 寫成冪律疊加：

$$
S_y(f)=\sum_{\alpha=-2}^{+2}h_\alpha f^{\alpha}.
$$

$S_y$ 的單位是 $1/\text{Hz}$，所以 $h_\alpha$ 的單位是 $\text{Hz}^{-(\alpha+1)}$：$h_{+2}$ 是 $\text{Hz}^{-3}$、$h_{+1}$ 是 $\text{Hz}^{-2}$、$h_0$ 是 $\text{Hz}^{-1}=\text{s}$、**$h_{-1}$ 無因次**、$h_{-2}$ 是 $\text{Hz}$。

> **符號警告**：$h_\alpha$ 一律掛在 **$S_y$** 身上（IEEE 1139 的標準用法）。上面例 2 我們把 $S_\phi$ 的 $1/f^2$ 係數順手記成了 $h_{-2}$——那是 $S_\phi$ 側的係數，與這裡 RW FM 的 $h_{-2}$（$S_y$ 側、單位 Hz）**不是同一個東西**。本節起把 $S_\phi$ 側的係數一律加上標 $\phi$ 區分：白 FM 段寫 $S_\phi=h^{\phi}_{-2}/f^2$（$h^{\phi}_{-2}$ 單位 $\text{rad}^2\cdot\text{Hz}$）。

### 一般式：一個變數代換蓋掉全部五列

把 $S_y=h_\alpha f^\alpha$ 代進第 3 步的積分，做變數代換 $u=\pi f\tau$（無因次；$f=u/(\pi\tau)$、$df=du/(\pi\tau)$、$f^\alpha=u^\alpha/(\pi\tau)^\alpha$）：

$$
\sigma_y^2(\tau)=2\int_0^{\infty}h_\alpha f^{\alpha}\,\frac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df
=\frac{2\,h_\alpha}{(\pi\tau)^{\alpha+1}}\,I_{2-\alpha},
\qquad
I_k\equiv\int_0^{\infty}\frac{\sin^4 u}{u^{k}}\,du.
$$

- **逐步**：被積函數 $=h_\alpha\dfrac{u^\alpha}{(\pi\tau)^\alpha}\cdot\dfrac{\sin^4u}{u^2}\cdot\dfrac{du}{\pi\tau}=h_\alpha\,(\pi\tau)^{-(\alpha+1)}\,\dfrac{\sin^4u}{u^{2-\alpha}}\,du$，抽出常數即得。
- **斜率表免費重現**：$\sigma_y^2\propto\tau^{-(\alpha+1)}$——$\alpha=0\Rightarrow\tau^{-1}$（white FM）、$\alpha=-1\Rightarrow\tau^{0}$（floor）、$\alpha=-2\Rightarrow\tau^{+1}$（RW FM），與第 4 步的表一致 ✓。剩下的工作只是算出**純數字** $I_k$。
- **收斂性（重要）**：$u\to0$ 時被積函數 $\sim u^{4-k}$（$k=2-\alpha\le4$ 對 $\alpha\ge-2$ 都可積 ✓）；$u\to\infty$ 時 $\sim u^{-k}$，需要 $k>1$ 即 $\alpha<1$。**$\alpha=+1,+2$（兩個 PM 型）在高頻端發散**——物理意義：PM 雜訊的 ADEV 取決於量測系統看得到多高的頻率，必須引入高頻截止 $f_h$（Hz）截斷在 $u_h=\pi f_h\tau$。這就是第 4 步表中 PM 兩列非帶 $f_h$ 不可的深層原因。
- **單位檢查**：$h_\alpha$ 是 $\text{Hz}^{-(\alpha+1)}$、$(\pi\tau)^{-(\alpha+1)}$ 是 $\text{Hz}^{+(\alpha+1)}$、$I_k$ 純數 ⇒ $\sigma_y^2$ 無因次 ✓。

### flicker FM（$\alpha=-1$）：證明 $I_3=\ln 2$

$\alpha=-1$ 時 $(\pi\tau)^{\alpha+1}=(\pi\tau)^{0}=1$——**$\tau$ 在第一步就整個消失**，floor 的「$\tau$-無關」性質此刻已經確立，還沒算任何積分：

$$
\sigma_y^2(\tau)=2\,h_{-1}\,I_3=2\,h_{-1}\int_0^{\infty}\frac{\sin^4u}{u^3}\,du.
$$

剩下的就是求純數 $I_3$。下面四小步，不跳步。

**第 (i) 步：$\sin^4$ 降冪成諧波。** 用 $\sin^2u=\tfrac12(1-\cos2u)$ 平方，再用 $\cos^2 2u=\tfrac12(1+\cos4u)$：

$$
\sin^4u=\frac{(1-\cos2u)^2}{4}=\frac{1-2\cos2u+\cos^2 2u}{4}=\frac{3-4\cos2u+\cos4u}{8}=\frac{4(1-\cos2u)-(1-\cos4u)}{8}.
$$

最後一個等號驗算：$4-4\cos2u-1+\cos4u=3-4\cos2u+\cos4u$ ✓。小 $u$ 檢查：$1-\cos(au)=\tfrac{a^2u^2}{2}-\tfrac{a^4u^4}{24}+\dots$，$u^2$ 項係數 $4\cdot\tfrac{4}{2}-\tfrac{16}{2}=8-8=0$ 相消，$u^4$ 項 $-4\cdot\tfrac{16}{24}+\tfrac{256}{24}=8$，得組合 $\approx8u^4=8\sin^4u$ ✓（$\sin^4u\approx u^4$）。

**第 (ii) 步：為什麼要湊成「$(1-\cos)$ 組合」而不能拆項。** 若把 $3-4\cos2u+\cos4u$ 逐項對 $u^{-3}$ 積分，每一項 $\dfrac{1-\cos(au)}{u^3}\approx\dfrac{a^2}{2u}$ 在 $u\to0$ **對數發散**；只有組合裡 $1/u$ 的係數 $4\cdot\tfrac{2^2}{2}-\tfrac{4^2}{2}=0$ 恰好抵消，整體才可積（低頻端 $\sin^4u/u^3\sim u\to0$、高頻端 $\le1/u^3$ ✓）。所以下面**整體處理、不得拆項**——這種「個別發散、組合有限」的結構，正是 $1/f$ 雜訊一貫的脾氣（比較第 5 步：標準變異數發散、差分組合收斂）。

**第 (iii) 步：兩次分部積分，把 $u^{-3}$ 降到 $u^{-1}$。** 記 $g(u)\equiv8\sin^4u=3-4\cos2u+\cos4u$，$I_3=\tfrac18\int_0^\infty g(u)\,u^{-3}du$。

第一次分部（$u^{-3}du=d(-\tfrac{1}{2u^2})$）：

$$
\int_0^{\infty}\frac{g(u)}{u^3}\,du=\Big[-\frac{g(u)}{2u^2}\Big]_0^{\infty}+\frac12\int_0^{\infty}\frac{g'(u)}{u^2}\,du,
\qquad g'(u)=8\sin2u-4\sin4u.
$$

邊界項檢查：$u\to\infty$ 時 $\lvert g\rvert\le8$ ⇒ $g/u^2\to0$；$u\to0$ 時 $g\approx8u^4$ ⇒ $g/(2u^2)\approx4u^2\to0$ ✓ 兩端皆零。

第二次分部（$u^{-2}du=d(-u^{-1})$）：

$$
\int_0^{\infty}\frac{g'(u)}{u^2}\,du=\Big[-\frac{g'(u)}{u}\Big]_0^{\infty}+\int_0^{\infty}\frac{g''(u)}{u}\,du,
\qquad g''(u)=16\cos2u-16\cos4u.
$$

邊界項檢查：$\infty$ 端 $g'$ 有界 ⇒ $g'/u\to0$；$0$ 端 $g'=8\sin2u-4\sin4u=(16u-16u)+O(u^3)=32u^3+O(u^5)$ ⇒ $g'/u\approx32u^2\to0$ ✓。合併：

$$
I_3=\frac18\cdot\frac12\int_0^{\infty}\frac{16(\cos2u-\cos4u)}{u}\,du=\int_0^{\infty}\frac{\cos2u-\cos4u}{u}\,du.
$$

**第 (iv) 步：Frullani 型餘弦積分 → $\ln2$。** 兩項各自在 $u\to0$ 發散（$\int du/u$），但組合可積（$\cos2u-\cos4u=6u^2+O(u^4)$，被積 $\sim6u\to0$）。取 $\varepsilon>0$ 下限，兩項分別代換 $v=2u$、$v=4u$：

$$
\int_{\varepsilon}^{\infty}\frac{\cos2u-\cos4u}{u}\,du=\int_{2\varepsilon}^{\infty}\frac{\cos v}{v}\,dv-\int_{4\varepsilon}^{\infty}\frac{\cos v}{v}\,dv=\int_{2\varepsilon}^{4\varepsilon}\frac{\cos v}{v}\,dv.
$$

（$\infty$ 端兩個積分各自條件收斂——Dirichlet 判準——同一條尾巴相減歸零，只剩 $[2\varepsilon,4\varepsilon]$ 一小段。）小段上 $\lvert\cos v-1\rvert\le v^2/2$：

$$
\int_{2\varepsilon}^{4\varepsilon}\frac{\cos v}{v}\,dv=\int_{2\varepsilon}^{4\varepsilon}\frac{dv}{v}+O(\varepsilon^2)=\ln\frac{4\varepsilon}{2\varepsilon}+O(\varepsilon^2)\ \xrightarrow{\ \varepsilon\to0\ }\ \ln2.
$$

所以：

$$
\boxed{\ I_3=\int_0^{\infty}\frac{\sin^4u}{u^3}\,du=\ln2
\quad\Longrightarrow\quad
\sigma_y^2(\tau)=2\ln2\cdot h_{-1}\ (\text{與 }\tau\text{ 無關}),\quad
\sigma_{y,\text{floor}}=\sqrt{2\ln2\cdot h_{-1}}\approx1.1774\,\sqrt{h_{-1}}\ }
$$

> **物理直覺**：$\ln2=\ln\frac{4}{2}$ 是降冪出來的兩個諧波 $2u$、$4u$ 的**頻率比取對數**。$1/f$ 過程每個 octave（頻率倍程）貢獻等量功率；ADEV 的帶通核在 log-頻率軸上是一個「形狀固定、隨 $\tau$ 平移」的窗（對 $S_y\sim1/f$ 加權後每 decade 的貢獻密度 $\propto\sin^4u/u^2$，峰在 $\tan u=2u$ 即 $u\approx1.17$、$f\approx0.37/\tau$）——窗只平移不變形，看到的「octave 數」不隨 $\tau$ 變，所以積分值是常數。這就是 flicker floor「與 $\tau$ 無關」的頻域圖像。

**數值驗證**（`scipy.integrate.quad` 積到 $200\pi$ 加 $\langle\sin^4\rangle=3/8$ 的解析尾巴修正；已在 lab_19 印出）：

```python
import numpy as np
from scipy.integrate import quad
U = 200*np.pi
I3, _ = quad(lambda u: np.sin(u)**4/u**3, 0, U, limit=4000)
I3 += (3/8)/(2*U**2)                  # 尾巴 ∫_U^∞ (3/8)/u^3 du
print(f"{I3:.4f} {np.log(2):.4f}")    # -> 0.6931 0.6931
```

> **factor-2/4 記帳（本節每個 2 與 4 的來歷，一次講清楚）**：
> - $\sigma_y^2=2\ln2\cdot h_{-1}$ 開頭的 **2**：來自第 3 步的核 $\lvert H\rvert^2=2\sin^4u/u^2$（定義的 $\tfrac12$ × 相鄰差分的 $4\sin^2$），是 **ADEV 數學**，與 phase-noise 的 SSB $/2$-vs-$/4$ 記帳**無關**。
> - $\cos2u$ 與 $\cos4u$ 的 **2、4**：$\sin^4$ 降冪的第二、第四諧波；$\ln2=\ln(4/2)$ 就是它們的頻率比。
> - white FM $h_0/(2\tau)$ 分母的 **2**：$2\cdot\frac{I_2}{\pi}=2\cdot\frac{\pi/4}{\pi}=\frac12$，同樣是 ADEV 數學，非 SSB 記帳。
> - 下面例 3 的 $h^{\phi}_{-2}$ 分母的 **$4\pi^2$**：來自 $(2\pi f)^2$，純粹是 rad ↔ Hz 換算。
> - 例 3 的 $\tau_{knee}$ 分母的 **4**：$=2\times2$（$h_0/\mathbf{2}\tau$ 的 2 × $\mathbf{2}\ln2$ 的 2）。
> - 真正的 SSB $/2$-vs-$/4$ 慣例只在「把 $S_\phi$ 換算成 dBc/Hz 報表」時出現（例 3 步驟 1 會標記）。

### 同一招順手拿下 white FM 與 RW FM（以及 PM 兩列的 $f_h$）

**white FM（$\alpha=0$）**：$\sigma_y^2=\dfrac{2h_0}{\pi\tau}I_2$。$I_2$ 只要一次分部（邊界項同樣兩端歸零：$\sin^4u/u\sim u^3\to0$、$\le1/u\to0$）：

$$
I_2=\int_0^{\infty}\frac{\sin^4u}{u^2}\,du=\Big[-\frac{\sin^4u}{u}\Big]_0^{\infty}+\int_0^{\infty}\frac{4\sin^3u\cos u}{u}\,du=\int_0^{\infty}\frac{\sin2u-\tfrac12\sin4u}{u}\,du=\frac{\pi}{2}-\frac12\cdot\frac{\pi}{2}=\frac{\pi}{4}.
$$

（中間用了 $4\sin^3u\cos u=2\sin2u\sin^2u=\sin2u(1-\cos2u)=\sin2u-\tfrac12\sin4u$，以及 Dirichlet 積分 $\int_0^\infty\frac{\sin(au)}{u}du=\frac{\pi}{2}$，$a>0$。）代回：

$$
\sigma_y^2(\tau)=\frac{2h_0}{\pi\tau}\cdot\frac{\pi}{4}=\frac{h_0}{2\tau}.
$$

例 2 引用的「標準結果」就這樣在站內自推出來了 ✓。

**RW FM（$\alpha=-2$）**：$\sigma_y^2=2h_{-2}(\pi\tau)\,I_4$，其中 $I_4=\int_0^\infty\sin^4u/u^4\,du=\dfrac{\pi}{3}$（同一家族：三次分部後歸到 Dirichlet 積分；標準積分表亦載，lab_19 以 quad 驗得 1.0472 $=\pi/3$）。代回：

$$
\sigma_y^2(\tau)=2\pi\tau\,h_{-2}\cdot\frac{\pi}{3}=\frac{2\pi^2}{3}\,h_{-2}\,\tau.
$$

**PM 兩列（$\alpha=+1,+2$）**：$I_1,I_0$ 在 $u\to\infty$ 發散，截斷在 $u_h=\pi f_h\tau$。white PM 用 $\int_0^{u_h}\sin^4u\,du=\tfrac38u_h-\tfrac14\sin2u_h+\tfrac1{32}\sin4u_h\approx\tfrac38u_h$（$u_h\gg1$，$\langle\sin^4\rangle=3/8$）：

$$
\sigma_y^2\approx\frac{2h_{+2}}{(\pi\tau)^3}\cdot\frac38\,\pi f_h\tau=\frac{3\,f_h\,h_{+2}}{4\pi^2\tau^2},
$$

正好是標準表的 white-PM 前因子（條件 $2\pi f_h\tau\gg1$）✓。flicker PM 同理：$I_1$ 的對數發散給 $\langle\sin^4\rangle\cdot\ln$ 項，係數 $\tfrac{3}{4\pi^2\tau^2}$；加法常數 $1.038$ 需要更細的振盪簿記，本頁直接引用標準值（外部文獻）。

### 五種冪律的完整前因子表

| 雜訊型態 | $S_y(f)$ | $h_\alpha$ 單位 | $\sigma_y^2(\tau)$ | 條件 | 出處 |
|---|---|---|---|---|---|
| white PM | $h_{+2}f^{2}$ | $\text{Hz}^{-3}$ | $\dfrac{3\,f_h\,h_{+2}}{4\pi^2\tau^2}$ | $2\pi f_h\tau\gg1$ | 標準表；前因子本頁以 $\langle\sin^4\rangle=\tfrac38$ 推得 |
| flicker PM | $h_{+1}f$ | $\text{Hz}^{-2}$ | $\dfrac{\big[1.038+3\ln(2\pi f_h\tau)\big]h_{+1}}{4\pi^2\tau^2}$ | $2\pi f_h\tau\gg1$ | 標準表；$\ln$ 係數本頁推得、常數 1.038 引用 |
| white FM | $h_0$ | $\text{Hz}^{-1}=\text{s}$ | $\dfrac{h_0}{2\tau}$ | — | **本頁自推**（$I_2=\pi/4$） |
| **flicker FM** | $h_{-1}/f$ | 無因次 | $2\ln2\cdot h_{-1}$（$\approx1.386\,h_{-1}$，floor） | — | **本頁自推**（$I_3=\ln2$） |
| random-walk FM | $h_{-2}/f^{2}$ | $\text{Hz}$ | $\dfrac{2\pi^2}{3}\,h_{-2}\,\tau$ | — | **本頁自推**（$I_4=\pi/3$） |

$f_h$ = 量測系統高頻截止（Hz）。整表與 **IEEE Std 1139-2008**、**NIST SP 1065**（W. J. Riley, *Handbook of Frequency Stability Analysis*, 2008）的標準表逐項一致（外部文獻，非本站 5 篇 PDF）；其中 flicker-FM、white-FM、RW-FM 三列與 white-PM 前因子已在本頁自行推導。每列單位自檢：$h_\alpha\,\text{Hz}^{(\alpha+1)}$ 型的組合全部無因次 ✓（例如 RW FM：$\text{Hz}\times\text{s}$ ✓；flicker PM：$\text{Hz}^{-2}/\text{s}^2$ ✓）。

### 例 3：由 canonical $1/f^3$ corner 算 flicker floor（帶單位）

> **題**：canonical 振盪器（$f_0=5$ GHz、$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、$S_i=10^{-24}\ \text{A}^2/\text{Hz}$），波形對稱化後 $c_0=0.04$，[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) 例 F 算出 $1/f^3$ corner $f_c=3.2$ kHz。求 flicker-FM floor $\sigma_{y,\text{floor}}$，以及 white-FM 段與 floor 交叉的 $\tau_{knee}$。

**步驟 1（白 FM 段的物理 $S_\phi$）**：時域乾淨推導（見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 的 factor-of-2 註記）給單邊

$$
S_\phi(f)=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{(2\pi f)^2}=\frac{h^{\phi}_{-2}}{f^2},
\qquad
h^{\phi}_{-2}=\frac{\Gamma_{rms}^2\,S_i}{4\pi^2\,q_{max}^2}=\frac{0.25\times10^{-24}}{4\pi^2\times10^{-24}}=6.33\times10^{-3}\ \text{rad}^2\cdot\text{Hz}.
$$

- **單位檢查**：$\text{A}^2/\text{Hz}\div\text{C}^2=(\text{C/s})^2/(\text{Hz}\cdot\text{C}^2)=\text{Hz}^2/\text{Hz}=\text{Hz}$，乘無因次 $\Gamma_{rms}^2$ 得 $\text{rad}^2\cdot\text{Hz}$ ✓（分母 $4\pi^2$ 來自 $(2\pi f)^2$，是 rad↔Hz 換算，**不是**雜訊記帳慣例）。
- **慣例標記（每次都要標）**：這是**物理的**單邊 $S_\phi$。換算成 dBc/Hz 報表時：時域 $/2$ 慣例（$\mathcal{L}=S_\phi/2$）給 $\mathcal{L}(1\,\text{MHz})=-145.0$ dBc/Hz；[P1] Eq.(21) 的 SSB $/4$ 記帳給 $-148.0$ dBc/Hz（差 3 dB，canonical 例 B）。**ADEV 只吃物理 $S_\phi$**，本例對應 $-145$ 那組；若誤把 $-148$ 當 $S_\phi/2$ 反推，$h^{\phi}_{-2}$ 會小 2 倍、floor 低 $\sqrt2$ 倍（$-1.5$ dB）。

**步驟 2（flicker 段 → $h_{-1}$）**：corner 以下 $S_\phi$ 變陡為 $1/f^3$，在 $f_c$ 與白 FM 段連續：$S_\phi=\dfrac{h^{\phi}_{-2}\,f_c}{f^3}$（$f<f_c$）。轉成 $S_y$（第 1 步的轉接頭）：

$$
S_y(f)=\frac{f^2}{f_0^2}\,S_\phi=\frac{h^{\phi}_{-2}\,f_c}{f_0^2}\cdot\frac1f\equiv\frac{h_{-1}}{f},
\qquad
h_{-1}=\frac{h^{\phi}_{-2}\,f_c}{f_0^2}=\frac{6.33\times10^{-3}\times3.2\times10^{3}}{(5\times10^{9})^2}=8.11\times10^{-19}.
$$

- **單位檢查**：$\text{rad}^2\cdot\text{Hz}\times\text{Hz}\div\text{Hz}^2=$ 無因次 ✓（$h_{-1}$ 該無因次）。
- 順手記：$h_{-1}=h_0\,f_c$，其中 $h_0=h^{\phi}_{-2}/f_0^2=2.53\times10^{-22}\ \text{Hz}^{-1}$ 是白 FM 位準——flicker 係數就是「白 FM 位準 × corner 頻率」。

**步驟 3（floor）**：

$$
\sigma_{y,\text{floor}}=\sqrt{2\ln2\cdot h_{-1}}=\sqrt{1.3863\times8.11\times10^{-19}}=\sqrt{1.124\times10^{-18}}=1.06\times10^{-9}.
$$

**結果：** floor $\approx1.06\times10^{-9}$，約 1.1 ppb——換算成頻率：$\sigma_y f_0=1.06\times10^{-9}\times5\times10^{9}=5.3$ Hz。這顆自由振盪器**不管平均多久**，兩樣本頻率不穩定度都卡在約 5.3 Hz，這就是 flicker floor 的工程意義。

**步驟 4（knee：白 FM 段撞上 floor 的 $\tau$）**：令 $h_0/(2\tau)=2\ln2\cdot h_{-1}$，用 $h_{-1}=h_0f_c$：

$$
\tau_{knee}=\frac{h_0}{4\ln2\cdot h_{-1}}=\frac{1}{4\ln2\cdot f_c}=\frac{0.3607}{f_c}=\frac{0.3607}{3200\ \text{Hz}}=113\ \mu\text{s}.
$$

（分母的 **4** $=2\times2$：$h_0/\mathbf{2}\tau$ 的 2 × $\mathbf{2}\ln2$ 的 2，皆 ADEV 數學。）$\tau$ 短於 113 μs 由白 FM 主導（$\tau^{-1/2}$ 下降）、長於它就坐在 floor 上。順手法則：**$\tau_{knee}\approx0.36/f_c$**。

**對照（不對稱波形）**：例 E 的 $c_0=0.4$ 給 $f_c=320$ kHz ⇒ $h_{-1}=8.11\times10^{-17}$、floor $=1.06\times10^{-8}$。corner 高 **100 倍**，floor 只高 **10 倍**（$\sqrt{\ }$），knee 縮到 1.13 μs。因為 $f_c\propto c_0^2$（[P1] Eq.(24)）而 floor $\propto\sqrt{h_{-1}}\propto\sqrt{f_c}$，所以 **floor $\propto c_0$**：波形對稱化不只壓 close-in phase noise，它以一次方直接拉低長期穩定度地板。

**Dimension check（全程）**：$h_{-1}$ 無因次 → $2\ln2\,h_{-1}$ 無因次 → 開根仍無因次（分數頻率）✓；$\tau_{knee}=h_0/(4\ln2\,h_{-1})=\text{s}/\text{無因次}=\text{s}$ ✓。

```python
import numpy as np
g, Si, qmax, f0, fc = 0.5, 1e-24, 1e-12, 5e9, 3.2e3
h_phi = g**2*Si/(qmax**2*4*np.pi**2)          # S_phi 白 FM 段係數（rad^2·Hz）
h_m1  = h_phi*fc/f0**2                        # S_y = h_m1/f（無因次）
floor = np.sqrt(2*np.log(2)*h_m1)
print(f"{h_phi:.2e} {h_m1:.2e} {floor:.2e}")  # -> 6.33e-03 8.11e-19 1.06e-09
h0 = h_phi/f0**2
print(f"{h0:.2e} {1/(4*np.log(2)*fc)*1e6:.0f}")  # -> 2.53e-22 113
```

### 模擬驗證：絕對 floor 高度（lab_19 擴充）

lab_19（`simulations/lab_19_allan.py`）已擴充成**驗絕對值**、不只驗斜率，做三件事：

1. **積分家族**：`scipy.integrate.quad` 直接算 $I_2,I_3,I_4$（積到 $200\pi$、加 $\langle\sin^4\rangle=3/8$ 的解析尾巴），印出 0.7854、**0.6931**、1.0472，對上 $\pi/4$、$\ln2$、$\pi/3$ ✓。
2. **純 flicker FM 的 floor**：用 FFT 整形合成**絕對 PSD 精確已知**的 $y(t)$——單位變異白噪的單邊 PSD 是 $2/f_s$，整形 $\lvert H\rvert^2=S_{target}/(2/f_s)$（函式 `synth_y_from_psd`；與只對斜率正規化的 `power_law_y` 不同）——取 $h_{-1}=8.11\times10^{-19}$，8 個 seed、$\tau=10\dots2000$ s 量 overlapping ADEV，得 **measured/theory $=1.004$**（理論 $\sqrt{2\ln2\,h_{-1}}=1.06\times10^{-9}$）。
3. **white＋flicker 全曲線**：疊加 $S_y=h_0+h_{-1}/f$（canonical 兩係數），$f_s=1$ MHz、$2^{22}$ 點、6 seeds，整條曲線（含 knee）與 $\sqrt{h_0/2\tau+2\ln2\,h_{-1}}$ 的最大偏差 **2.3%**。

![white+flicker FM 的絕對 ADEV：模擬點落在理論曲線 √(h0/2τ+2ln2·h₋₁) 上，floor=1.06e-9、knee=113 μs](/figures/allan_flicker_floor.png)

| 項目 | 值 | 說明 |
|---|---|---|
| 模型 | toy / illustrative（非 transistor-level） | FFT 整形，**絕對單邊 PSD 精確已知** |
| $h_0$ | $2.53\times10^{-22}\ \text{Hz}^{-1}$ | canonical 白 FM 位準（例 3 步驟 2） |
| $h_{-1}$ | $8.11\times10^{-19}$（無因次） | canonical flicker 係數（$f_c=3.2$ kHz） |
| 理論 floor | $\sqrt{2\ln2\,h_{-1}}=1.06\times10^{-9}$ | 綠虛線 |
| 量測/理論（floor） | $1.004$ | 純 flicker、8 seeds 平均 |
| 全曲線最大偏差 | $2.3\%$ | 大 $\tau$ 端含 FFT 低頻截斷偏差 |
| $\tau_{knee}$ | $113\ \mu$s（紅點線） | $=1/(4\ln2\,f_c)$ |

**如何解讀**：模擬點（藍）在小 $\tau$ 沿白 FM 漸近線 $\sqrt{h_0/2\tau}$ 以 $-1/2$ 斜率下降，在 $\tau_{knee}=113\ \mu$s 轉彎，之後坐上 $1.06\times10^{-9}$ 的地板——**高度**與理論吻合到 0.4%（floor 帶）。注意兩個誠實的 caveat：(a) 合成雜訊的最低頻率被記錄長度截斷在 $f_s/N$，最大 $\tau$ 端 flicker 功率略缺、曲線輕微偏離（包含在 2.3% 內）；(b) 這是 toy 合成驗證「積分數學」，真實振盪器的 floor 高度由真實 $f_c$、$h^{\phi}_{-2}$ 決定。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 雜訊可寫成冪律疊加 | 斜率表直接可讀型態 | 含 spur（離散譜線）時 ADEV 出現 $\tau$ 週期性凸起，需另判讀 |
| white PM vs flicker PM 要區分 | ADEV **不行**（都 $\tau^{-1}$） | 改用 MDEV（modified Allan）才分得開 |
| 資料夠長、$\tau\ll$ 總時長 | 估計可靠 | $\tau$ 接近總時長時樣本數少、信賴區間爆大 |
| 過程到 RW FM 為止 | ADEV 收斂 | 比 RW 更低頻（$S_y\sim f^{-3}$ 以上）ADEV 也發散，需 Hadamard variance |
| 量測系統本身夠乾淨 | 測到的是 DUT | 否則左端（小 $\tau$）被儀器 white PM 蓋住 |
| floor 式 $\sigma_y^2=2\ln2\,h_{-1}$：$S_y\sim1/f$ 要覆蓋核所看的頻帶（$f\approx0.37/\tau$ 上下各約 1.5 decade） | floor 平坦、高度準 | $\tau$ 太靠近 $\tau_{knee}$ 時白 FM 貢獻不可忽略（改用完整式 $h_0/2\tau+2\ln2\,h_{-1}$）；$\tau$ 太大時 RW FM／drift 蓋過 floor |
| PM 兩列的前因子需 $2\pi f_h\tau\gg1$ | white/flicker PM 前因子成立 | $\tau$ 小到 $2\pi f_h\tau\sim1$ 時前因子失準（$f_h$＝量測高頻截止） |

## 與哪些 paper／公式對應

- 本頁的 ADEV 定義、$\sigma_y^2=2\int S_y\sin^4(\pi f\tau)/(\pi f\tau)^2 df$、$S_y=(f^2/f_0^2)S_\phi$ 與斜率表，全部依規範 11.2「Allan variance / ADEV」逐字採用。
- **外部文獻（不在下載的 5 篇 PDF 內，以標準文獻補充）**：
  - **[E1] D. W. Allan, "Statistics of Atomic Frequency Standards," Proc. IEEE, vol. 54, no. 2, pp. 221–230, Feb. 1966.**（ADEV 原始提出）
  - **IEEE Std 1139**（"IEEE Standard Definitions of Physical Quantities for Fundamental Frequency and Time Metrology—Random Instabilities"）、**NIST Special Publication 1065**（W. Riley, "Handbook of Frequency Stability Analysis," 2008）——冪律斜率對照表與 overlapping ADEV 估計法的標準參考。
  - 上述為 **IEEE Std 1139-2008**（前版 1139-1999）與 **NIST SP 1065**（W. J. Riley, *Handbook of Frequency Stability Analysis*, 2008）；卷期/版本已查證。
- 與本站頻域結果的對接：$S_\phi\sim1/f^2$（[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 的 [P1] Eq.(21)）↔ white FM ↔ ADEV $\tau^{-1/2}$；$1/f^3$（[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) 的 [P1] Eq.(23)）↔ flicker FM ↔ ADEV $\tau^0$ floor。
- **完整前因子表**：整表與 IEEE Std 1139-2008、NIST SP 1065 一致（外部文獻，非本站 5 篇 PDF）；其中 **flicker-FM 的 $2\ln2$（$I_3=\ln2$）、white-FM 的 $h_0/2\tau$（$I_2=\pi/4$）、RW-FM 的 $\tfrac{2\pi^2}{3}h_{-2}\tau$（$I_4=\pi/3$）與 white-PM 前因子已於本頁自行推導**，只用到第 3 步的積分式；flicker-PM 的加法常數 1.038 引用標準值。例 3 的 corner $f_c=3.2$ kHz 來自 [P1] Eq.(24)（[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) 例 F）。

## 重點回顧

- ADEV $\sigma_y(\tau)$ 是 phase noise 的**時域對應**：同一條 $S_\phi(f)$，先轉 $S_y=(f^2/f_0^2)S_\phi$，再代 $\sigma_y^2(\tau)=2\int_0^\infty S_y\,\sin^4(\pi f\tau)/(\pi f\tau)^2\,df$。
- 定義 $\sigma_y^2(\tau)=\langle\tfrac12(\bar y_{k+1}-\bar y_k)^2\rangle$ 的精髓是**相鄰相減**（一階差分、高通），把慢漂移與未知總平均擋掉。
- 五種冪律斜率：white/flicker PM $\tau^{-1}$、**white FM $\tau^{-1/2}$**、flicker FM $\tau^{0}$（floor）、RW FM $\tau^{+1/2}$；ADEV 圖呈先掉、見底、再爬的澡盆形，底部 $\tau_{\text{opt}}$ 最穩。
- 招牌對接：$1/f^2$ phase noise ↔ white FM ↔ ADEV $-1/2$ 斜率。
- **為何用 ADEV**：普通頻率方差對 flicker/RW **不收斂**（隨量測時長發散）；ADEV 的差分核在 $f\to0$ 像 $f^2$，把低頻發散壓住，得到可重複的穩定度指標。
- 例 2 示範由 $\mathcal{L}(1\text{MHz})=-100$ dBc/Hz（5 GHz）估出 $S_y$ 白色、$\sigma_y(1\text{ms})\approx6.3\times10^{-8}$。
- **前因子不只斜率**：$u=\pi f\tau$ 代換給 $\sigma_y^2=2h_\alpha(\pi\tau)^{-(\alpha+1)}I_{2-\alpha}$；$I_2=\pi/4$、$I_3=\ln2$、$I_4=\pi/3$ ⇒ white FM $h_0/2\tau$、**flicker floor $2\ln2\,h_{-1}$**（$\tau$-無關）、RW FM $\tfrac{2\pi^2}{3}h_{-2}\tau$；PM 兩列因 $I_1,I_0$ 高頻發散必須帶 $f_h$。
- **$\ln2$ 的由來**：$\sin^4$ 降冪成 $2u,4u$ 兩諧波、兩次分部積分、Frullani 型 $\int(\cos2u-\cos4u)/u\,du=\ln(4/2)$；quad 驗證 0.6931 ✓。
- canonical 數值（例 3）：$f_c=3.2$ kHz ⇒ $h_{-1}=8.11\times10^{-19}$、floor $=1.06\times10^{-9}$（$\approx5.3$ Hz @ 5 GHz）、$\tau_{knee}=1/(4\ln2 f_c)=113\ \mu$s（$\approx0.36/f_c$）；floor $\propto c_0$——對稱化直接拉低長期穩定度地板。lab_19 以絕對 PSD 已知的合成雜訊量得 measured/theory $=1.004$。

## 延伸閱讀

- 頻域版的同一件事：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- $1/f^2$ 的來源（white FM 的頻域起點）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- $1/f^3$ ↔ flicker FM floor：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- 為什麼要鎖相把長期頻率釘住：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- 隨機程序與 PSD 基礎：[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)
