---
title: 超越 Lorentzian：1/f³ 線形與非平穩性——儀器到底量什麼
description: 白噪假設 Var[Δφ]=2D|t| 給 Lorentzian；flicker FM 使 Var[Δφ] 以 t²×log 成長（含低頻截止 f_l 的角色），特徵函數給出近高斯線核而非 Lorentzian。再嚴格說明自由振盪相位是 random walk、S_φ 嚴格不存在為平穩 PSD，儀器量的是平穩的 V(t) 頻譜（Demir 觀點），本站 S_φ 公式是「有限觀察時間、offset ≫ 線寬」的條件譜。lab_29 數值驗證全套。
---

# 超越 Lorentzian：1/f³ 線形與非平穩性——儀器到底量什麼

> 先備：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)（白噪 → Lorentzian 全套與「假發散」）、[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)（$1/f^3$ 裙邊從哪來）、[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)（平穩性、Wiener–Khinchin）｜接下來：[allan_variance](/02_foundations/allan_variance)（時域刻畫 flicker FM 的正規工具）、[measurement_and_spurs](/06_design_insights/measurement_and_spurs)（儀器實作面）

[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 用一條乾淨的邏輯鏈解開了 $1/f^2$
在 $\Delta\omega\to0$ 的假發散：相位 random walk（$\operatorname{Var}[\Delta\phi]=2D|t|$）
→ 高斯特徵函數 → 指數自相關 → **Lorentzian** 線形。但那條鏈的第一環藏了一個假設：
**驅動相位的雜訊是白的**。真實振盪器最靠近載波的裙邊往往是 $1/f^3$
（flicker FM，見 [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)）——
那麼近載波的**線形**還是 Lorentzian 嗎？

這頁回答兩個問題：

1. **Part A（線形）**：flicker FM 之下 $\operatorname{Var}[\Delta\phi(t)]$ 不再線性成長，而是
   $t^2\times\log$ 成長（含一個**低頻截止 $f_l$** 的明確角色）；特徵函數那一步因此給出
   **近高斯（near-Gaussian）線核**，不是 Lorentzian。
2. **Part B（非平穩性）**：自由振盪的 $\phi(t)$ 是 random walk，**嚴格來說 $S_\phi(f)$
   不存在**（不是平穩過程、沒有平穩 PSD）；儀器真正量的是 $V(t)=\cos(\omega_0t+\phi)$
   的頻譜——它**是**平穩的（[E2] Demir 觀點）。本站所有 $S_\phi$ 公式是
   「有限觀察時間、offset $\gg$ 線寬」下的**條件譜**，兩者在該範圍內完全一致。

> **物理直覺（先講結論）**：線形由「相位失憶的速度曲線」決定。白噪之下相位方差**線性**累積
> （$\propto t$），失憶包絡是**指數** $e^{-D|t|}$，其傅立葉變換是 Lorentzian。flicker FM 之下，
> 低頻雜訊讓頻率本身長時間偏在一邊，相位方差以**近乎 $t^2$**（差一個 log）累積——像「帶漂移的
> 漫步」——失憶包絡變成**近高斯** $e^{-(\text{const})t^2\log}$，而高斯的傅立葉變換還是高斯：
> **線核變成鐘形的高斯，肩膀比 Lorentzian 陡得多**。同一個 $\mathcal{L}(10\,\text{kHz})$ 規格，
> 白噪版線寬 50 Hz、flicker 版線寬 3.1 kHz——**一個 offset 上的 dBc/Hz 數字完全不決定線寬，
> 雜訊「顏色」才決定**。這正是 lab_29 數值演示的主秀。

> **動手試**：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 頁面內嵌了一個
> 互動 explorer——同一個 $\mathcal{L}(10\,\text{kHz})$ 規格滑桿、white FM／flicker FM 切換、
> 外加頻譜儀 RBW 滑桿，可以親手看到本頁「同一規格、線寬差百倍」的結論，以及 RBW 太寬時
> 轉平／近高斯肩部怎麼被抹平。

---

## Part A：flicker FM 的 $1/f^3$ 線形

### 第 0 步：Lorentzian 的隱藏假設，與單邊/雙邊記帳（factor-of-2 紀律）

[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 的推導鏈是：

$$
\operatorname{Var}[\Delta\phi(t)]=2D|t|
\;\Rightarrow\;
\langle\cos\Delta\phi\rangle=e^{-\operatorname{Var}/2}=e^{-D|\tau|}
\;\Rightarrow\;
S_x(\Delta\omega)\propto\frac{D}{D^2+\Delta\omega^2},\quad
\Delta f_{3\mathrm{dB}}=\frac{D}{\pi}.
$$

第一環「方差**線性**成長」只對**白色頻率雜訊**（white FM：$\dot\phi$ 的 PSD 平坦）成立。
本頁把這一環換成 flicker FM，看整條鏈怎麼變。

先把記帳說死（本站 factor-of-2 紀律）。設白噪 FM 的**單邊** $\dot\phi$ PSD 為
$W_0$（單位 $\text{rad}^2/\text{s}^2/\text{Hz}=\text{rad}^2/\text{s}$）。第 1 步會嚴格證明
$\operatorname{Var}[\Delta\phi(t)]=\tfrac{W_0}{2}|t|$，所以 $\operatorname{Var}=2D|t|$ 對應
$W_0=4D$，而相位譜（積分器 $1/\Delta\omega^2$）為：

$$
S_\phi^{\text{單邊}}(f)=\frac{4D}{(2\pi f)^2},\qquad
S_\phi^{\text{雙邊}}(f)=\frac{2D}{(2\pi f)^2},\qquad
\mathcal{L}(\Delta f)\stackrel{\text{時域}/2}{=}\frac{S_\phi^{\text{單邊}}}{2}=\frac{2D}{\Delta\omega^2}.
$$

- **哪個慣例**：文獻寫「Wiener 相位的 $S_\phi=2D/\Delta\omega^2$」時，常是**雙邊**記帳
  （或等價地把因子 2 吸進 $D$ 的定義——即 [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
  的慣例甲 $D_{\text{甲}}=2D$）。本站規範 11.2（v5）與本頁一致：**單邊** $S_\phi=4D/\Delta\omega^2$、
  $\operatorname{Var}=2D|t|$。lab_29 用數值釘死：對 $\operatorname{Var}=2D|t|$ 合成的相位，Welch（單邊）量到
  $S_\phi(10\,\text{kHz})\div\big(4D/\Delta\omega^2\big)=1.001$——**是 4 不是 2**。
  單雙邊差的這個 2 倍**不影響**線形與 $\Delta f_{3\mathrm{dB}}=D/\pi$（線寬由包絡衰減率決定，
  與譜的記帳無關）。
- **與 SSB $/4$ 慣例的關係**：lab_29 直接量 $V(t)$ 頻譜的單邊裙帶再除以載波功率，得到的就是
  時域 $/2$ 慣例的 $\mathcal{L}=S_\phi/2$（10 kHz 處量測與理論差 $+0.12$ dB）；
  [P1] Eq.(21), p.185 的 SSB $/4$ 記帳會把同一物理再低 3 dB 引用——即本站
  [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 講過的著名
  factor-of-2 記帳事，本頁不重複爭論、只標明每個數字用哪個慣例。

### 第 1 步：相位增量方差的一般公式（一切的引擎）

要處理任意顏色的 FM 雜訊，需要一條「從 $S_\phi(f)$ 直接算 $\operatorname{Var}[\Delta\phi(\tau)]$」
的通式。逐步推：

**(i) 增量是 $\dot\phi$ 的窗積分。** 定義相位增量
$\Delta\phi(\tau)\equiv\phi(t_0+\tau)-\phi(t_0)=\displaystyle\int_{t_0}^{t_0+\tau}\dot\phi(\sigma)\,d\sigma$。
只要 $\dot\phi$ 是**平穩**零均值過程（白噪或有低頻截止的 flicker 都是），$\Delta\phi$ 的統計與
$t_0$ 無關——這就是「**增量平穩**」，Part B 會再回來用它。

**(ii) 窗積分是一個 LTI 濾波器。** 對頻率 $f$ 的成分，長度 $\tau$ 的矩形積分窗的響應是

$$
H_\tau(f)=\int_0^\tau e^{-j2\pi f\sigma}\,d\sigma=\frac{1-e^{-j2\pi f\tau}}{j2\pi f}
\quad\Longrightarrow\quad
\lvert H_\tau(f)\rvert^2=\frac{2-2\cos(2\pi f\tau)}{(2\pi f)^2}=\frac{\sin^2(\pi f\tau)}{(\pi f)^2}.
$$

- **單位檢查**：$[H_\tau]=\text{s}$（對時間積分），$[\lvert H\rvert^2]=\text{s}^2$ ✓。

**(iii) 平穩過程過 LTI 濾波器 → 輸出方差 = PSD × $\lvert H\rvert^2$ 積分。**

$$
\operatorname{Var}[\Delta\phi(\tau)]=\int_0^\infty S_{\dot\phi}^{\text{單邊}}(f)\,\lvert H_\tau(f)\rvert^2\,df .
$$

- **單位檢查**：$(\text{rad}^2/\text{s})\cdot\text{s}^2\cdot\text{Hz}=\text{rad}^2$ ✓。

**(iv) 換成 $S_\phi$ 寫法。** 用 $S_{\dot\phi}(f)=(2\pi f)^2S_\phi(f)$（微分器）代入，
$(2\pi f)^2\cdot\frac{\sin^2(\pi f\tau)}{(\pi f)^2}=4\sin^2(\pi f\tau)=2\big(1-\cos 2\pi f\tau\big)$：

$$
\boxed{\ \operatorname{Var}[\Delta\phi(\tau)]=2\int_0^\infty S_\phi^{\text{單邊}}(f)\,\big(1-\cos 2\pi f\tau\big)\,df\ }
$$

- **物理意義**：核 $\big(1-\cos2\pi f\tau\big)$ 是「增量高通」——比 $1/\tau$ 慢的成分
  （$f\tau\ll1$）被壓成 $2\pi^2f^2\tau^2$（慢漂移在短窗裡看不出來），比 $1/\tau$ 快的成分平均貢獻
  $2S_\phi$。**正因為有這個高通，即使 $\phi$ 本身發散，增量方差仍可有限**（Part B 的伏筆）。
- **白噪自我檢查（收回 $2D|t|$）**：代 $S_\phi=4D/(2\pi f)^2$，用標準積分
  $\int_0^\infty\frac{1-\cos u}{u^2}\,du=\frac{\pi}{2}$（變數代換 $u=2\pi f\tau$，見
  [math_identities](/99_appendix/math_identities)）：

$$
\operatorname{Var}=2\int_0^\infty\frac{4D}{(2\pi f)^2}\big(1-\cos2\pi f\tau\big)\,df
=\frac{8D}{(2\pi)^2}\cdot 2\pi\tau\int_0^\infty\frac{1-\cos u}{u^2}\,du
=\frac{8D}{4\pi^2}\cdot2\pi\tau\cdot\frac{\pi}{2}=2D\tau\ \checkmark
$$

  這同時再次驗證第 0 步的記帳：**單邊 $4D/\Delta\omega^2$ 才會收回 $2D|t|$**。
- **與 [P2] 的連結**：這條通式就是 ring 論文累積 jitter 律的引擎——[P2] Eq.(8), p.792 的
  $\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$ 正是「白噪 FM → 方差線性」這個特例（$\kappa$ 由
  [P2] Eq.(12), p.793 給出，不含 $\omega_0$）。

### 第 2 步：flicker FM 是什麼——$S_\phi=b_{-3}/f^3$，以及它在 ISF 理論的出處

**定義（頻域）**：flicker FM 指頻率漲落 $\dot\phi$ 帶 $1/f$ 譜：

$$
S_{\dot\phi}^{\text{單邊}}(f)=\frac{k_f}{f}
\quad\Longleftrightarrow\quad
S_\phi^{\text{單邊}}(f)=\frac{S_{\dot\phi}}{(2\pi f)^2}=\frac{b_{-3}}{f^3},
\qquad b_{-3}\equiv\frac{k_f}{4\pi^2}.
$$

- **單位**：$[k_f]=\text{rad}^2/\text{s}^2$（$S_{\dot\phi}$ 是 $\text{rad}^2/\text{s}$、乘回 $f$）；
  $[b_{-3}]=\text{rad}^2\cdot\text{Hz}^2$（$S_\phi$ 是 $\text{rad}^2/\text{Hz}$、乘 $f^3$）✓。
  用相對頻率 $y=\dot\phi/\omega_0$ 的話 $S_y=h_{-1}/f$、$b_{-3}=h_{-1}f_0^2$
  （[allan_variance](/02_foundations/allan_variance) 用的就是 $h_{-1}$ 記法）。
- **ISF 理論的出處**：$1/f^3$ 裙邊來自 device flicker 經 ISF 的 DC 項 $c_0$ 上轉——
  [P1] Eq.(22)→(23), p.185（推導見
  [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)）。把 [P1]
  Eq.(23) 的 $\mathcal{L}$ 用小角 $\mathcal{L}\approx\tfrac12S_\phi$ 反解成 $S_\phi$，
  可讀出對應的係數：

$$
b_{-3}=\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f\ \cdot\ \omega_{1/f}}{32\,\pi^3}.
$$

  - **單位檢查**：$\dfrac{1}{\text{C}^2}\cdot\dfrac{\text{A}^2}{\text{Hz}}\cdot\dfrac{1}{\text{s}}
    =\dfrac{1}{\text{A}^2\text{s}^2}\cdot\text{A}^2\text{s}\cdot\dfrac{1}{\text{s}}=\dfrac{1}{\text{s}^2}=\text{Hz}^2$ ✓
    （rad 無因次）。
  - **慣例註記**：Eq.(23) 沿用 [P1] 的 SSB 記帳（與 Eq.(21) 同族）；上式又疊了
    $\mathcal{L}\approx\tfrac12S_\phi$。這些 2 的組合屬「包裝」，不影響 $1/f^3$ 斜率與
    $c_0^2/q_{max}^2$ scaling——本頁後續一律以 $b_{-3}$（可直接從量測讀出：
    $b_{-3}=S_\phi f^3$）為單一參數，避免把包裝爭議帶進線形推導。

### 第 3 步：帶低頻截止的積分——$\operatorname{Var}\propto t^2\times\log$

把 $S_\phi=b_{-3}/f^3$ 代入第 1 步通式。先看**為什麼必須有低頻截止 $f_l$**：
被積函數在 $f\to0$ 時

$$
\frac{b_{-3}}{f^3}\big(1-\cos2\pi f\tau\big)\approx\frac{b_{-3}}{f^3}\cdot2\pi^2f^2\tau^2=\frac{2\pi^2 b_{-3}\tau^2}{f},
$$

是 $1/f$——**對數發散**。白噪時 $(1-\cos)$ 核的 $f^2$ 壓制剛好夠用（$1/f^2\cdot f^2=$ 常數，可積）；
flicker 多出一個 $1/f$，核壓不住。所以積分下限必須放一個**物理的低頻截止** $f_l$：

$$
\operatorname{Var}[\Delta\phi(\tau)]=2\int_{f_l}^{\infty}\frac{b_{-3}}{f^3}\big(1-\cos2\pi f\tau\big)\,df .
$$

$f_l$ 從哪來？三個常見來源，效果相同：**(a) 觀察時間**——量 $T_{obs}$ 秒就看不到比
$1/T_{obs}$ 慢的漲落（頻譜儀、我們的模擬都是這種）；**(b) 物理機制**——flicker 的
trap 時間常數再長也有限；**(c) 系統**——PLL 把載波鎖住，迴路頻寬以下的漂移被吃掉。
**截止的角色是「對數弱」的**：下面會看到 $f_l$ 只進到 $\ln$ 裡。

**逐步算積分。** 變數代換 $u=2\pi f\tau$（$f=u/2\pi\tau$、$df=du/2\pi\tau$、$1/f^3=(2\pi\tau)^3/u^3$）：

$$
\operatorname{Var}=2b_{-3}\,(2\pi\tau)^2\int_{u_0}^{\infty}\frac{1-\cos u}{u^3}\,du
\equiv 8\pi^2b_{-3}\tau^2\,K(u_0),\qquad u_0=2\pi f_l\tau .
$$

剩下就是把 $K(x)=\displaystyle\int_x^\infty\frac{1-\cos u}{u^3}\,du$ 在 $x\ll1$ 算出來。分部積分兩次：

**(i) 第一次分部**（$dw=u^{-3}du\Rightarrow w=-\tfrac{1}{2u^2}$）：

$$
K(x)=\Big[-\frac{1-\cos u}{2u^2}\Big]_x^\infty+\frac12\int_x^\infty\frac{\sin u}{u^2}\,du
=\frac{1-\cos x}{2x^2}+\frac12\int_x^\infty\frac{\sin u}{u^2}\,du .
$$

**(ii) 第二次分部**（$dw=u^{-2}du\Rightarrow w=-\tfrac1u$）：

$$
\int_x^\infty\frac{\sin u}{u^2}\,du=\Big[-\frac{\sin u}{u}\Big]_x^\infty+\int_x^\infty\frac{\cos u}{u}\,du
=\frac{\sin x}{x}-\operatorname{Ci}(x),
$$

其中 $\operatorname{Ci}(x)\equiv-\int_x^\infty\frac{\cos t}{t}\,dt$ 是標準**餘弦積分函數**，小 $x$ 展開
$\operatorname{Ci}(x)=\gamma_E+\ln x+O(x^2)$。這裡 $\gamma_E\approx0.5772$ 是
**Euler–Mascheroni 常數**——注意它**不是** ISF 的 $\Gamma$、也不是 MOS 雜訊係數 $\gamma$，
為避免撞名一律寫 $\gamma_E$。

**(iii) 合併取小 $x$ 極限**（$\frac{1-\cos x}{2x^2}\to\frac14$、$\frac{\sin x}{x}\to1$）：

$$
K(x)=\frac14+\frac12\big[1-\gamma_E-\ln x\big]+O(x^2)=\frac34-\frac{\gamma_E}{2}+\frac12\ln\frac1x+O(x^2).
$$

**(iv) 代回**，得本頁 Part A 的主結果：

$$
\boxed{\ \operatorname{Var}[\Delta\phi(\tau)]=4\pi^2 b_{-3}\,\tau^2\left[\ln\frac{1}{2\pi f_l\tau}+\frac32-\gamma_E\right]\ }
\qquad(2\pi f_l\tau\ll1).
$$

- **物理意義**：主導行為是 $\tau^2$——不是白噪的 $\tau^1$。$\tau^2$ 意味「**準相干的頻率偏移**」：
  在 $\tau$ 這個時間尺度上，比 $1/\tau$ 慢的 flicker 成分像一個暫時固定的頻率誤差 $\delta\omega$，
  相位誤差 $=\delta\omega\cdot\tau$、方差 $\propto\tau^2$。$\log$ 因子則是把「有多少十倍頻的慢成分
  在扮演這個角色」（從 $f_l$ 到 $\sim1/\tau$ 的每個 decade 貢獻相同）數出來。
- **單位檢查**：$[4\pi^2b_{-3}\tau^2]=\text{rad}^2\text{Hz}^2\cdot\text{s}^2=\text{rad}^2$ ✓；
  $\ln$ 內 $f_l\tau$ 無因次 ✓。
- **截止的角色（明確講）**：$f_l$ 只出現在 $\ln$ 裡——把 $f_l$ 改 10 倍，中括號只多/少
  $\ln10\approx2.30$（相對典型值 $\sim10$ 是 $\pm20\%$ 量級），**方差有限但永遠忘不掉截止**。
  對照白噪：$f_l\to0$ 完全無感。這正是 flicker「無限記憶」的數學指紋，也是 Part B
  「量測值弱依賴觀察時間」的根源。
- **適用/失效**：(a) 需 $2\pi f_l\tau\ll1$，否則 $O(x^2)$ 修正進場（$\tau$ 長到看得到截止時，
  方差成長趨緩）；(b) 需 $\dot\phi$ 在 $f\ge f_l$ 平穩；(c) 上限 $f\to\infty$ 收斂沒問題
  （核飽和、$1/f^3$ 可積），實務上高頻端會先被白噪 FM（$1/f^2$ 段）接手——本推導只管
  $1/f^3$ 主導的近載波段。
- **數值驗證（lab_29）**：量測增量方差 ÷ 閉式，在 $\tau=1$ ms 得 $0.957$、$\tau=10$ ms 得
  $0.944$（6 條 32 s 紀錄的 ensemble；殘差是 flicker 最慢成分的紀錄間漲落，見 Part B）；
  閉式 ÷「離散頻點精確和」在 10 ms 得 $1.000$——閉式本身是準的。

### 第 4 步：特徵函數 → 近高斯線核（不是 Lorentzian）

特徵函數那一步與 [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 完全相同：
$\Delta\phi$ 是零均值高斯（我們的合成是「高斯白噪過線性濾波」，**精確**高斯；實際電路近似成立），
所以

$$
R_x(\tau)=\frac12\cos(\omega_0\tau)\,E(\tau),\qquad
E(\tau)=\big\langle\cos\Delta\phi\big\rangle=e^{-\operatorname{Var}[\Delta\phi(\tau)]/2}.
$$

代入第 3 步的方差：

$$
\boxed{\ E(\tau)=\exp\!\left(-2\pi^2b_{-3}\,\tau^2\left[\ln\frac{1}{2\pi f_l\tau}+\frac32-\gamma_E\right]\right)\ }
$$

- **這是（差一個慢變 log 的）高斯包絡**：$e^{-(\text{const})\tau^2}$ 型。對比白噪的
  $e^{-D|\tau|}$ 指數包絡。
- **高斯的傅立葉變換還是高斯**：所以線核（載波附近的 $S_x$）是**近高斯鐘形**，
  不是 Lorentzian。把 $\log$ 凍結在失憶時刻 $\tau^\*$（$E(\tau^\*)=e^{-1}$）得到工程近似：

$$
S_x(\Delta f)\ \propto\ \exp\!\big(-2\pi^2\sigma_\tau^2\,\Delta f^2\big),\quad
\sigma_\tau=\frac{1}{2\pi\sqrt{b_{-3}L^\*}},\qquad
\Delta f_{3\mathrm{dB}}\approx2\sqrt{2\ln2}\,\sqrt{b_{-3}L^\*},
$$

  其中 $L^\*=\ln\frac{1}{2\pi f_l\tau^\*}+\frac32-\gamma_E$。lab_29 的參數下
  $\tau^\*=1.64\times10^{-4}$ s、$L^\*\approx12.1$，近似線寬 $3233$ Hz，對照「不做凍結、
  直接數值傅立葉」的精確線寬 $3176$ Hz——凍結近似誤差 $\approx2\%$。
- **線寬 scaling 的對比**（工程記憶點）：白噪 $\Delta f_{3\mathrm{dB}}=\pi b_{-2}$
  （$S_\phi=b_{-2}/f^2$，即 $D/\pi$ 的另一種寫法），**正比於雜訊強度**；flicker
  $\Delta f_{3\mathrm{dB}}\approx2.355\sqrt{b_{-3}L^\*}$，**正比於雜訊強度的平方根**（差一個 log）。
  雜訊降 6 dB：白噪線寬變 1/4，flicker 線寬只變約 1/2。
- **形狀指紋（$-3$ dB／$-10$ dB 半寬比）**——這是可直接量的線形判別量。令
  $x=\Delta f/\text{HWHM}$：
  - Lorentzian：$S\propto\dfrac{1}{1+x^2}$。$-3$ dB（$S=\tfrac12$）在 $x=1$；$-10$ dB
    （$S=\tfrac1{10}$）在 $1+x^2=10\Rightarrow x=3$。**比值恰為 $3.00$**。
  - Gaussian：$S\propto e^{-\ln2\,x^2}$（這樣寫使 $x=1$ 正好 $-3$ dB）。$-10$ dB 在
    $\ln2\,x^2=\ln10\Rightarrow x=\sqrt{\ln10/\ln2}=1.8226$。**比值 $1.82$**。
  - flicker 線（含 log 修正的精確數值理論）：**$1.86$**——比純高斯略「厚尾」，因為 log
    使包絡比凍結高斯稍慢衰減；量測得 $1.89$。Lorentzian 的 $3.00$ 與高斯族的 $1.8$ 上下
    相距甚遠，一量便知。

> **誠實分工（外部理論 vs 本站自算）**：「$f^{-\alpha}$ 雜訊下振盪器線形（含近高斯結論）」的
> 嚴格理論屬**外部文獻、不在本站 5 篇 PDF 內**：
> **[E3] F. X. Kärtner, "Analysis of White and $f^{-\alpha}$ Noise in Oscillators," Int. J.
> Circuit Theory Appl., vol. 18, no. 5, pp. 485–519, 1990**（本站 [references](/99_appendix/references)
> 已收）；colored-noise 的嚴格隨機模型見 **A. Demir, "Phase Noise and Timing Jitter in
> Oscillators with Colored-Noise Sources," IEEE Trans. Circuits Syst. I, vol. 49, no. 12,
> pp. 1782–1791, Dec. 2002（外部文獻，非本站 5 篇 PDF）**；教科書級整理見
> **E. Rubiola, "Phase Noise and Frequency Stability in Oscillators," Cambridge Univ. Press,
> Cambridge, U.K., 2009（外部文獻，非本站 5 篇 PDF）**。本頁**自己做**的部分是：第 1–4 步的
> 初等推導（增量濾波器＋分部積分＋特徵函數，全程不跳步），以及 lab_29 的全部數值驗證
> （方差 $t^2\log$ 律、線形、寬度比、線寬、$\mathcal{L}$ 匹配）。

### lab_29：同一個 $\mathcal{L}(10\,\text{kHz})$，兩種線形

`simulations/lab_29_flicker_lineshape.py` 合成兩顆振盪器，**刻意讓它們在 10 kHz offset 有
完全相同的 $\mathcal{L}$**（時域 $/2$ 慣例）：

1. **white FM**：相位增量 $\sim\mathcal{N}(0,\,2D\,dt)$，$D=50\pi\approx157.08\ \text{rad}^2/\text{s}$
   → 理論 Lorentzian、$\Delta f_{3\mathrm{dB}}=D/\pi=50.0$ Hz。
2. **flicker FM**：頻域校準合成 $S_{\dot\phi}=k_f/f$，取 $k_f=4D\cdot f_{match}$（$f_{match}=10$ kHz）
   → 兩者在 $f_{match}$ 處 $S_\phi$ 相同（$1/f^2$ 與 $1/f^3$ 線恰在 10 kHz 交叉，圖 (d)）。

| 參數 | 值 | 說明 |
|---|---|---|
| $f_s$ | $2^{18}=262144$ Hz | 取樣率（toy／normalized，模型即「相位＋餘弦」，非 transistor-level） |
| $n$ | $2^{23}$（$T=32$ s） | 紀錄長度 → 合成低頻截止 $f_l=1/T=1/32$ Hz |
| $f_0$ | $80$ kHz | 載波（只看相對 offset） |
| $D$ | $50\pi=157.08\ \text{rad}^2/\text{s}$ | white FM 擴散常數（$\operatorname{Var}=2D\vert t\vert$ 慣例） |
| $k_f$ | $4D\cdot10^4=6.283\times10^6\ \text{rad}^2/\text{s}^2$ | flicker FM 強度（10 kHz 匹配設計） |
| $b_{-3}$ | $k_f/4\pi^2=1.592\times10^5\ \text{rad}^2\text{Hz}^2$ | $S_\phi=b_{-3}/f^3$ |
| 匹配點 | $\mathcal{L}(10\,\text{kHz})=-71.0$ dBc/Hz | 兩顆相同（時域 $/2$ 慣例；SSB $/4$ 引用低 3 dB） |
| flicker ensemble | 6 條獨立 32 s 紀錄 | 慢成分不自平均（Part B），故做 ensemble 並回報單紀錄散佈 |

![同一個 L(10kHz) 之下：white FM 是 Lorentzian（線寬 50 Hz）、flicker FM 是近高斯線核（線寬約 3.1 kHz）；增量方差一個線性、一個 t²×log；S_φ 的 1/f² 與 1/f³ 在 10 kHz 交會](/figures/flicker_lineshape.png)

**如何解讀四張子圖**：

- **(a) 左上（PN 視角）**：兩條模擬 $\mathcal{L}(\Delta f)$ 在 10 kHz（黑點）重合於 $-71$ dBc/Hz；
  往載波走，白噪沿 $-20$ dB/dec 的 Lorentzian 裙邊爬升、在 $\sim25$ Hz（HWHM）轉平；flicker 沿
  $-30$ dB/dec 更陡地爬、在 $\sim1.6$ kHz 就轉平成一個**寬而平的高斯頂**。黑虛線
  （Lorentzian）與暗紅虛線（第 4 步特徵函數的數值傅立葉，**無自由參數**）分別壓在兩條模擬上。
- **(b) 右上（線核形狀，各自以 HWHM 歸一）**：白噪點雲貼 Lorentzian 參考線（$-10$ dB 半寬在
  $3\times$ HWHM）；flicker 點雲貼高斯參考線（$-10$ dB 半寬在 $1.82\times$ HWHM），
  尾端略高於純高斯——正是 log 修正（理論比值 1.86）。
- **(c) 左下（增量方差）**：白噪量測點落在斜率 1 的 $2D\tau$ 上；flicker 量測點落在斜率
  $\approx2$ 的 $4\pi^2b_{-3}\tau^2[\ln(1/2\pi f_l\tau)+3/2-\gamma_E]$ 上（虛線，無自由參數）。
- **(d) 右下（有限觀察時間的 $S_\phi$）**：對**非平穩**的 $\phi(t)$ 直接做 Welch——這正是
  Part B 說的「條件譜」——得到乾淨的 $1/f^2$（貼 $4D/\Delta\omega^2$ 單邊理論）與
  $1/f^3$（貼 $b_{-3}/f^3$），在 10 kHz 交會。

核心 Python 與**實跑輸出**（完整 script：`simulations/lab_29_flicker_lineshape.py`，
以 `PYTHONPATH=專案根目錄 python3 simulations/lab_29_flicker_lineshape.py` 執行；
共用 `simulations/common/plot_utils.py`、`noise_utils.py`）：

```python
# 匹配設計：K = 4D * f_match，使兩顆在 f_match 有同一個 S_phi（進而同一個 L）
D  = 50.0 * np.pi          # white FM: Var[dphi] = 2 D |t|  [rad^2/s]
K  = 4 * D * 1.0e4         # flicker FM: S_phidot = K/f     [rad^2/s^2]
B3 = K / (4 * np.pi**2)    # S_phi = B3 / f^3               [rad^2 Hz^2]

print(f"{cal_first:.3f}")   # -> 0.986 （合成校準：量測 S_phidot·f ÷ K，1 kHz 附近）
print(f"{L10_w:.1f}")       # -> -70.9 （white 量測 L(10 kHz)，理論 -71.0，時域 /2 慣例）
print(f"{L10_f:.1f}")       # -> -70.4 （flicker 量測 L(10 kHz)；精確線形理論也是 -70.4，見下）
print(f"{r_onesided:.3f}")  # -> 1.001 （單邊 S_phi(10 kHz) ÷ (4D/Δω²)：釘死「單邊是 4D」）
print(f"{fwhm_w:.1f}")      # -> 49.9 （white 線寬 FWHM [Hz]，理論 D/π = 50.0）
print(f"{fwhm_f:.0f}")      # -> 3067 （flicker 線寬 FWHM [Hz]，6 紀錄 ensemble；理論 3176）
print(f"{fwhm_f/fwhm_w:.1f}")  # -> 61.4 （同一個 L(10 kHz)，線寬差 61 倍！）
print(f"{ratio_w:.2f}")     # -> 2.87 （white −10dB/−3dB 半寬比；Lorentzian 理論 3.00）
print(f"{ratio_f:.2f}")     # -> 1.89 （flicker 半寬比；Gaussian 1.82、含 log 修正理論 1.86）
print(f"{rms_w:.2f}")       # -> 0.24 （white 對 Lorentzian 擬合 rms 誤差 [dB]，±4 HWHM：吻合）
print(f"{rms_f:.2f}")       # -> 4.37 （flicker 對 Lorentzian 擬合 rms 誤差 [dB]：明顯偏離）
print(f"{popt_w[1]:.1f}")   # -> 25.0 （white 擬合 HWHM [Hz]，理論 D/2π = 25.0）
print(f"{r_th_f:.2f}")      # -> 1.86 （特徵函數理論線的半寬比）
print(f"{2*hw_th_f[0.5]:.0f}")  # -> 3176 （特徵函數理論線寬 [Hz]；高斯凍結近似 3233）
print(f"{10*np.log10(L_th_f_10k):.1f}")  # -> -70.4 （精確線形在 10 kHz：比純 1/f³ 裙邊高 0.6 dB）
print(f"{slope_w/(2*D):.3f}")  # -> 1.010 （white 量測 Var/τ ÷ 2D：線性成長 ✓）
print(f"{var_f[i1ms]/var_f_cf[i1ms]:.3f}")   # -> 0.957 （flicker Var(1 ms) ÷ 閉式）
print(f"{var_f_cf[i10ms]/var_f_ex[i10ms]:.3f}")  # -> 1.000 （閉式 ÷ 離散精確和：推導無誤）
print(f"{r_cut:.2f}")       # -> 1.92 （截止實驗：f_l=1/32 Hz vs 1 Hz 的 Var(10 ms) 比，量測）
print(f"{r_cut_th:.2f}")    # -> 2.09 （同上、精確理論：截止以 ln(f_l) 進場）
```

三個值得停下來看的數字：

1. **$-70.4$ vs $-71.0$（flicker 的 0.6 dB）**：flicker 線只在 $\Delta f\gg$ 線寬時才收斂到
   $1/f^3$ 裙邊；10 kHz 只有 $\approx3\times$ HWHM，精確線形（特徵函數數值傅立葉）本來就
   預測 $-70.4$——量測與精確理論**完全一致**，偏離的是「純裙邊近似」。這順便量化了
   「offset $\gg$ 線寬」到底要多遠：$3\times$ HWHM 處誤差還有 0.6 dB。
2. **$61.4$ 倍線寬比**：同一個 datasheet 數字 $\mathcal{L}(10\,\text{kHz})=-71$ dBc/Hz，
   線寬可以差近兩個數量級。**單點 $\mathcal{L}$ 不決定線寬；斜率（雜訊顏色）才決定。**
3. **$1.92$ vs $2.09$（截止實驗）**：把合成截止從 $1/32$ Hz 挪到 1 Hz，$\tau=10$ ms 的相位
   方差近乎砍半——**方差確實記得 $f_l$**（$\ln f_l$ 進場）；量測略低於理論是 6 條紀錄的
   慢成分漲落（單紀錄線寬散佈 $2944\pm142$ Hz vs ensemble 3067 Hz），這本身就是 Part B 的
   實物教材。

> **toy-model 誠實標註**：lab_29 直接合成「相位 → 餘弦」，不含振幅動態、不含 transistor；
> 它驗證的是第 1–4 步的**數學**，不是任何特定電路。

---

## Part B：非平穩性——$S_\phi$ 嚴格不存在，儀器量什麼？

### 第 5 步：自由振盪的 $\phi(t)$ 不是平穩過程

平穩（wide-sense stationary）要求兩件事：均值不隨時間變、自相關
$R_\phi(t_1,t_2)$ 只依賴 $\tau=t_2-t_1$。對白噪驅動、從 $t=0$ 起跑（$\phi(0)=0$）的
Wiener 相位，逐步算 $R_\phi$：

**(i)** 設 $t_2\ge t_1$，拆 $\phi(t_2)=\phi(t_1)+\Delta$，其中 $\Delta=\phi(t_2)-\phi(t_1)$
是 $(t_1,t_2]$ 區間的噪音積分，**與 $\phi(t_1)$ 獨立**（白噪不同區間不相關；高斯下不相關=獨立）。

**(ii)** 

$$
R_\phi(t_1,t_2)=\big\langle\phi(t_1)\,[\phi(t_1)+\Delta]\big\rangle
=\big\langle\phi(t_1)^2\big\rangle+\underbrace{\langle\phi(t_1)\rangle\langle\Delta\rangle}_{=0}
=2D\,t_1 .
$$

一般寫法（不假設排序）：

$$
\boxed{\ R_\phi(t_1,t_2)=2D\min(t_1,t_2)\ }
$$

- **這不是 $\tau$ 的函數**——它依賴**絕對時間**（開機多久了）。且
  $\operatorname{Var}[\phi(t)]=2Dt\to\infty$：方差無界。兩條都違反平穩性。
- **後果**：Wiener–Khinchin 定理（[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)）
  的前提是平穩。**所以「$S_\phi(f)$」作為平穩 PSD 嚴格來說不存在**——
  $S_\phi=2D/\Delta\omega^2$ 這類式子不能按定義讀。flicker FM 更嚴重：連增量方差都要
  $f_l$ 才有限（第 3 步）。
- **但增量是平穩的**：$\operatorname{Var}[\Delta\phi(\tau)]=2D|\tau|$ 與 $t_0$ 無關（第 1 步 (i)）。
  這就是為什麼 [P2] 用 $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$（[P2] Eq.(8), p.792）這種
  **增量語言**描述 ring 的 jitter——增量統計是良定義的，PSD 不是。時域 jitter 語言在數學上
  反而比「$S_\phi$」更根本。

### 第 6 步：存在的是 $V(t)$ 的頻譜（[E2] Demir 觀點）

雖然 $\phi$ 發散，$V(t)=\cos(\omega_0t+\phi(t))$ **有界**，而且它的統計會**收斂到平穩**：

- 相位「絕對值」發散沒關係——$V$ 只看 $\phi\bmod 2\pi$，而 random walk 的 $\bmod 2\pi$
  分佈隨時間趨於**均勻**（初始相位被忘光）。
- 自相關只剩相位**差**：$\langle V(t)V(t+\tau)\rangle\to\tfrac12\cos(\omega_0\tau)E(\tau)$
  （[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 第 1 步的計算，
  用的正是平穩的**增量** $\Delta\phi$）——只依賴 $\tau$ ✓。

這是 **[E2] A. Demir, A. Mehrotra, and J. Roychowdhury, IEEE TCAS-I 47(5):655–674, 2000
（不在本站 5 篇 PDF 內，DOI 10.1109/81.847872）** 的核心觀點之一：帶噪振盪器的輸出收斂為
**平穩過程**，其頻譜（白噪下是 Lorentzian）是嚴格良定義的物件——**頻譜儀量的就是它**。
本頁 Part A 只是把同一套機器換上 flicker 的 $\operatorname{Var}(\tau)$，線形從 Lorentzian
變近高斯，「$V$ 平穩、譜良定義」這件事不變（flicker 需 $f_l$ 截止使 $\dot\phi$ 平穩）。

**一張表講清楚「什麼存在、誰在量它」**：

| 物件 | 嚴格存在嗎 | 誰量它 |
|---|---|---|
| $\phi(t)$ 樣本路徑 | ✓（但非平穩、無界漫步） | 無人直接量（無限長相位計不存在） |
| $S_\phi(f)$ 作為平穩 PSD | ✗（Wiener–Khinchin 前提不成立） | ——（是個方便的記號，見第 7 步） |
| 增量統計 $\operatorname{Var}[\Delta\phi(\tau)]$ | ✓（white 天生；flicker 需 $f_l$） | 時間區間分析儀／jitter 量測（[P2] 的 $\kappa\sqrt{\Delta t}$）、[allan_variance](/02_foundations/allan_variance) |
| 有限觀察譜 $S_\phi^{(T)}(f)$，$f\gg1/T$ | ✓（期望值良定義、收斂） | phase-noise analyzer（相位鑑別＋FFT；PLL 把迴路頻寬以下的漫步吃掉）——lab_29 圖 (d) 的 Welch 就是它 |
| $S_V(f)$（$V(t)$ 的 PSD） | ✓（$V$ 平穩，[E2]） | 頻譜儀直接量（linewidth、線形、$\mathcal{L}$ 皆由此讀出） |
| $\mathcal{L}(\Delta f)=\tfrac12S_\phi$ | ✓ 當 $\Delta f\gg$ 線寬（且 $\gg1/T$） | datasheet 上那個數字 |

### 第 7 步：和解——本站的 $S_\phi$ 公式在量什麼

那本站（與 [P1]）滿頁的 $S_\phi$、$\mathcal{L}$ 公式是什麼意思？它們是
**有限觀察時間的條件譜**：取一段長 $T$ 的紀錄（或讓 PLL/儀器把慢漂移扣掉），對「這一段裡
看起來平穩的增量」做譜估計。可以證明（且 lab_29 圖 (d) 數值演示）：對 $f\gg1/T$，
其期望值收斂到

$$
S_\phi^{(T)}(f)\ \xrightarrow[f\gg1/T]{}\ \frac{4D}{(2\pi f)^2}\ \text{（單邊，white FM）},\qquad
\frac{b_{-3}}{f^3}\ \text{（flicker FM）},
$$

量測 ÷ 理論 $=1.001$（10 kHz，marker 見上）。**所以本站全部 $S_\phi$ 公式在
$\Delta f\gg\max(1/T,\ \text{線寬})$ 的範圍內是嚴格可用的**；它們失效的地方正是
[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 的「假發散」區——
$\Delta f\lesssim$ 線寬時要換 $S_V$（Lorentzian／近高斯線形）來讀。兩套描述在共同適用區
無縫銜接（Part A 的 0.6 dB 練習就是銜接處的量化）。

flicker 再補一刀（本頁獨有的教訓）：因為 $f_l$ 以 $\ln$ 進到方差，**「有限觀察」對 flicker
永遠留下對數殘影**——lab_29 的截止實驗（$f_l$ 從 $1/32$ Hz 挪到 1 Hz，$\operatorname{Var}(10\,\text{ms})$
變一半）與單紀錄線寬散佈（$2944\pm142$ Hz，6 條紀錄各只有 32 s）都是它的直接展示。
實務語言：**flicker 主導的振盪器，其「線寬」與 close-in 積分 jitter 是「量多久」的（弱）函數**；
報告數字時要附觀察時間／量測頻寬——這也是 [allan_variance](/02_foundations/allan_variance)
存在的理由（flicker FM 在 ADEV 上是乾淨的平台，不需要 $f_l$ 就良定義）。此觀點的教科書處理見
Rubiola 2009（前引，外部文獻）。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| $\Delta\phi$ 為高斯 | 特徵函數 $E=e^{-\operatorname{Var}/2}$ 精確（合成雜訊、小訊號線性累積） | 強非線性／大注入使 $\Delta\phi$ 非高斯，線形偏離本頁兩族 |
| $2\pi f_l\tau\ll1$ | $t^2\log$ 閉式成立（誤差 $O((f_l\tau)^2)$） | $\tau\gtrsim1/f_l$ 時方差成長趨緩、包絡尾端偏離 |
| 純 flicker FM 段主導 | 線核近高斯、比值 $\approx1.86$ | 白噪 FM 混入時外圈回到 Lorentzian 裙邊、線形是兩族的卷積（[E3]、Demir 2002） |
| $\Delta f\gg$ 線寬 | $\mathcal{L}=\tfrac12S_\phi$ 可用（$3\times$HWHM 處仍差 0.6 dB） | 近線寬處必須用 $S_V$ 線形讀 |
| 觀察時間 $T\gg1/\Delta f$ | 條件譜 $S_\phi^{(T)}$ 收斂、與公式一致 | 太短的紀錄：譜估計偏差＋flicker 慢成分不自平均（單紀錄線寬散佈） |
| 振幅穩定（只追相位） | 單參數（$D$ 或 $b_{-3}$）描述線形 | 強 AM–PM 時需把振幅雜訊一起入模 |

## 與哪些 paper／公式對應

- **$1/f^2$、$1/f^3$ 的 $S_\phi$ 輸入**：[P1] Eq.(21), p.185（white）；[P1] Eq.(22)–(23),
  p.185（flicker 上轉，$b_{-3}$ 的 ISF 出處，含 SSB 記帳註記）。
- **增量語言**：[P2] Eq.(8), p.792（$\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$，相位增量）、
  Eq.(12), p.793（$\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\overline{i_n^2}/\Delta f}$，
  不含 $\omega_0$）——正是本頁「PSD 不存在、增量存在」的工程體現。
- **外部文獻（皆不在本站 5 篇 PDF 內）**：[E2] Demir–Mehrotra–Roychowdhury 2000
  （$V$ 平穩、譜良定義；TCAS-I 47(5):655–674，DOI 10.1109/81.847872）；[E3] Kärtner 1990
  （$f^{-\alpha}$ 線形；IJCTA 18(5):485–519）；A. Demir, IEEE TCAS-I 49(12):1782–1791,
  Dec. 2002（colored-noise 相位擴散）；E. Rubiola, *Phase Noise and Frequency Stability in
  Oscillators*, Cambridge Univ. Press, 2009（教科書整理）。

## Worked example（帶單位、可一行驗證）

> **例（同一個 $\mathcal{L}$、兩種線寬）**：某 5 GHz 振盪器在 10 kHz offset 量到
> $\mathcal{L}=-71.0$ dBc/Hz（時域 $/2$ 慣例）。(a) 若該處是 $1/f^3$ 段、低頻截止
> $f_l=0.0176$ Hz（32 s 觀察的有效截止），求 $b_{-3}$、$\operatorname{Var}[\Delta\phi(1\,\text{ms})]$
> 與線寬；(b) 若該處是 $1/f^2$ 段，求線寬。比較兩者。

**(a) flicker 情形，逐步：**

1. **還原 $S_\phi$。** $\mathcal{L}_{\text{lin}}=10^{-71/10}=7.94\times10^{-8}\ /\text{Hz}$；
   $S_\phi(10\,\text{kHz})=2\mathcal{L}_{\text{lin}}=1.589\times10^{-7}\ \text{rad}^2/\text{Hz}$。
2. **讀出 $b_{-3}$。** $b_{-3}=S_\phi f^3=1.589\times10^{-7}\times(10^4)^3=1.589\times10^{5}\ \text{rad}^2\text{Hz}^2$。
3. **方差（$\tau=1$ ms）。** $2\pi f_l\tau=2\pi\times0.0176\times10^{-3}=1.10\times10^{-4}$；
   中括號 $=\ln(1/1.10\times10^{-4})+1.5-0.5772=9.11+0.92=10.03$；
   $\operatorname{Var}=4\pi^2\times1.589\times10^5\times(10^{-3})^2\times10.03=6.27\times10.03\approx63.0\ \text{rad}^2$。
   ——1 ms 內相位已散掉 $\sqrt{63}\approx8$ rad：**完全失相干**（失憶時間 $\tau^\*\approx0.16$ ms）。
4. **線寬（高斯凍結近似）。** $L^\*\approx12.1$（在 $\tau^\*$ 評估）：
   $\Delta f_{3\mathrm{dB}}\approx2.355\sqrt{b_{-3}L^\*}=2.355\sqrt{1.589\times10^5\times12.1}\approx3.3\ \text{kHz}$
   （精確數值傅立葉：$3.2$ kHz）。

**(b) white 情形，逐步：** $b_{-2}=S_\phi f^2=1.589\times10^{-7}\times10^8=15.89\ \text{rad}^2\cdot\text{Hz}$；
$\Delta f_{3\mathrm{dB}}=\pi b_{-2}=49.9\ \text{Hz}$（等價 $D=\pi^2b_{-2}=156.8\ \text{rad}^2/\text{s}$、
$D/\pi=49.9$ Hz）；$\operatorname{Var}(1\,\text{ms})=2D\tau=0.314\ \text{rad}^2$——1 ms 時**仍相干**。

**比較：** 同一個 $-71$ dBc/Hz@10 kHz——flicker 版線寬 $3.2$ kHz、white 版 $50$ Hz（**64 倍**）；
1 ms 相位方差 $63$ vs $0.31\ \text{rad}^2$（**200 倍**）。單點 $\mathcal{L}$ 規格不封頂 close-in 行為。

**Dimension check：** $[b_{-3}]=\text{rad}^2\text{Hz}^2$，$\sqrt{b_{-3}\cdot(\text{無因次})}=\text{rad}\cdot\text{Hz}\to$
（rad 無因次）$\text{Hz}$ ✓；$[b_{-2}]=\text{rad}^2\text{Hz}$，$\pi b_{-2}$ 是 Hz ✓；
$[4\pi^2b_{-3}\tau^2]=\text{rad}^2$ ✓。

```python
import numpy as np
gE = 0.5772156649
L = 10**(-71/10); Sphi = 2*L
b3 = Sphi*1e4**3; b2 = Sphi*1e4**2
var_1ms = 4*np.pi**2*b3*1e-6*(np.log(1/(2*np.pi*0.0176*1e-3))+1.5-gE)
print(round(b3), round(var_1ms,1), round(np.pi*b2,1))   # -> 158866 63.0 49.9
```

## 重點回顧

- Lorentzian 是**白噪 FM 專屬**：它繼承自 $\operatorname{Var}[\Delta\phi]=2D|t|$ 的線性成長。
- 萬用引擎：$\operatorname{Var}[\Delta\phi(\tau)]=2\int_0^\infty S_\phi^{\text{單邊}}(f)(1-\cos2\pi f\tau)\,df$
  （增量高通核；單邊記帳，white 代入 $4D/\Delta\omega^2$ 收回 $2D|t|$——lab_29 量測比 1.001）。
- flicker FM（$S_\phi=b_{-3}/f^3$，需低頻截止 $f_l$）：
  $\operatorname{Var}=4\pi^2b_{-3}\tau^2[\ln\frac{1}{2\pi f_l\tau}+\frac32-\gamma_E]$——
  $t^2\times\log$ 成長，$f_l$ 只以 $\ln$ 進場（改 10 倍只差 $\ln10$）。
- 特徵函數 $E=e^{-\operatorname{Var}/2}$ ⇒ 近高斯包絡 ⇒ **近高斯線核**；線寬
  $\approx2.355\sqrt{b_{-3}L^\*}$（$\propto\sqrt{\text{噪}}$，白噪則 $\propto$ 噪）。
- 形狀指紋 $-10$ dB／$-3$ dB 半寬比：Lorentzian $3.00$、Gaussian $1.82$、flicker 含 log 修正
  $1.86$（lab_29 量測 white $2.87$、flicker $1.89$；Lorentzian 擬合 rms 誤差 0.24 vs 4.37 dB）。
- 同一個 $\mathcal{L}(10\,\text{kHz})=-71$ dBc/Hz：白噪線寬 50 Hz、flicker 線寬 3.1 kHz
  （61 倍）——**單點 PN 不決定線寬，雜訊顏色才決定**。
- 自由振盪 $\phi$：$R_\phi=2D\min(t_1,t_2)$、方差無界 ⇒ **非平穩** ⇒ $S_\phi$ 作為平穩 PSD
  **嚴格不存在**；存在的是增量統計（[P2] 的 $\kappa\sqrt{\Delta t}$）、有限觀察條件譜
  （$f\gg1/T$ 收斂到本站公式）、與**平穩的 $S_V$**（[E2] Demir；頻譜儀量的東西）。
- flicker 的量測值（線寬、close-in jitter）以 $\ln$ 依賴觀察時間／截止——報數字要附條件。

## 延伸閱讀

- 白噪版全套（本頁的對照組）：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- $1/f^3$ 從哪來（$c_0$ 上轉、[P1] Eq.(22)–(24)）：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)、[lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion)
- 平穩性、Wiener–Khinchin、ergodicity：[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)
- flicker FM 的時域正規刻畫（ADEV 平台、不需 $f_l$）：[allan_variance](/02_foundations/allan_variance)
- 儀器怎麼量 $\mathcal{L}$（SA／discriminator／cross-correlation）：[measurement_and_spurs](/06_design_insights/measurement_and_spurs)
- jitter 語言與 $S_\phi$ 的橋：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- 端到端數值鏈（含 Lorentzian 一站）：[capstone_lc_end_to_end](/03_isf_core_theory/capstone_lc_end_to_end)
- 外部文獻完整 citation（[E2]、[E3]）：[references](/99_appendix/references)
