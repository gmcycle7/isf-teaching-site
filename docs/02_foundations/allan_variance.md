---
title: Allan variance：相位雜訊的時域對應
description: 從兩樣本（Allan）變異數 σy²(τ)=⟨½(ȳ_{k+1}−ȳ_k)²⟩ 出發，逐步推頻域積分 σy²=2∫S_y sin⁴(πfτ)/(πfτ)² df、S_y=(f²/f0²)S_φ，並推導五種冪律雜訊的 ADEV 斜率對照表（white/flicker PM τ⁻¹、white FM τ⁻¹ᐟ²、flicker FM τ⁰ floor、RW FM τ^{+1/2}），解釋為何時鐘界用 ADEV 而非普通頻率方差。嵌入 allan_deviation 圖，含 2 個 worked example（由 L(f) 估 ADEV）。
---

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

（此處 white FM 閉式 $\sigma_y^2=h_0/2\tau$ 是標準頻率計量結果；本站 lab_19 只驗斜率不驗絕對常數，數值為示範用。)

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 雜訊可寫成冪律疊加 | 斜率表直接可讀型態 | 含 spur（離散譜線）時 ADEV 出現 $\tau$ 週期性凸起，需另判讀 |
| white PM vs flicker PM 要區分 | ADEV **不行**（都 $\tau^{-1}$） | 改用 MDEV（modified Allan）才分得開 |
| 資料夠長、$\tau\ll$ 總時長 | 估計可靠 | $\tau$ 接近總時長時樣本數少、信賴區間爆大 |
| 過程到 RW FM 為止 | ADEV 收斂 | 比 RW 更低頻（$S_y\sim f^{-3}$ 以上）ADEV 也發散，需 Hadamard variance |
| 量測系統本身夠乾淨 | 測到的是 DUT | 否則左端（小 $\tau$）被儀器 white PM 蓋住 |

## 與哪些 paper／公式對應

- 本頁的 ADEV 定義、$\sigma_y^2=2\int S_y\sin^4(\pi f\tau)/(\pi f\tau)^2 df$、$S_y=(f^2/f_0^2)S_\phi$ 與斜率表，全部依規範 11.2「Allan variance / ADEV」逐字採用。
- **外部文獻（不在下載的 5 篇 PDF 內，以標準文獻補充）**：
  - **[E1] D. W. Allan, "Statistics of Atomic Frequency Standards," Proc. IEEE, vol. 54, no. 2, pp. 221–230, Feb. 1966.**（ADEV 原始提出）
  - **IEEE Std 1139**（"IEEE Standard Definitions of Physical Quantities for Fundamental Frequency and Time Metrology—Random Instabilities"）、**NIST Special Publication 1065**（W. Riley, "Handbook of Frequency Stability Analysis," 2008）——冪律斜率對照表與 overlapping ADEV 估計法的標準參考。
  - 上述卷期/頁碼依公開標準文獻慣例引用；`TODO: 若需正式投稿可再核對 IEEE Std 1139 最新版年份與 SP1065 頁碼。`
- 與本站頻域結果的對接：$S_\phi\sim1/f^2$（[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 的 [P1] Eq.(21)）↔ white FM ↔ ADEV $\tau^{-1/2}$；$1/f^3$（[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) 的 [P1] Eq.(23)）↔ flicker FM ↔ ADEV $\tau^0$ floor。

## 重點回顧

- ADEV $\sigma_y(\tau)$ 是 phase noise 的**時域對應**：同一條 $S_\phi(f)$，先轉 $S_y=(f^2/f_0^2)S_\phi$，再代 $\sigma_y^2(\tau)=2\int_0^\infty S_y\,\sin^4(\pi f\tau)/(\pi f\tau)^2\,df$。
- 定義 $\sigma_y^2(\tau)=\langle\tfrac12(\bar y_{k+1}-\bar y_k)^2\rangle$ 的精髓是**相鄰相減**（一階差分、高通），把慢漂移與未知總平均擋掉。
- 五種冪律斜率：white/flicker PM $\tau^{-1}$、**white FM $\tau^{-1/2}$**、flicker FM $\tau^{0}$（floor）、RW FM $\tau^{+1/2}$；ADEV 圖呈先掉、見底、再爬的澡盆形，底部 $\tau_{\text{opt}}$ 最穩。
- 招牌對接：$1/f^2$ phase noise ↔ white FM ↔ ADEV $-1/2$ 斜率。
- **為何用 ADEV**：普通頻率方差對 flicker/RW **不收斂**（隨量測時長發散）；ADEV 的差分核在 $f\to0$ 像 $f^2$，把低頻發散壓住，得到可重複的穩定度指標。
- 例 2 示範由 $\mathcal{L}(1\text{MHz})=-100$ dBc/Hz（5 GHz）估出 $S_y$ 白色、$\sigma_y(1\text{ms})\approx6.3\times10^{-8}$。

## 延伸閱讀

- 頻域版的同一件事：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- $1/f^2$ 的來源（white FM 的頻域起點）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- $1/f^3$ ↔ flicker FM floor：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- 為什麼要鎖相把長期頻率釘住：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- 隨機程序與 PSD 基礎：[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)
