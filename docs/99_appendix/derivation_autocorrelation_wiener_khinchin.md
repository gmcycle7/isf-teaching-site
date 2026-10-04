---
title: 自相關 → Wiener-Khinchin 嚴格推導
description: 用 LTV 相位導數的雙時間自相關、對絕對時間的週期平均、Wiener-Khinchin 三步，把 white_noise_to_phase_noise 的啟發式 Eq.(19)→(20)→(21) 推導路線嚴格重做一遍，讓 Σcₙ²=2Γrms² 從自相關的週期平均裡自然掉出來，並與啟發式版逐項對照。
---

# 自相關 → Wiener-Khinchin 嚴格推導

> 先備：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（啟發式版 Eq.(19)→(20)→(21)、canonical 例 B）｜ 接下來：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)（把 $\dot\phi$ 白噪積成相位 random walk，Wiener-Khinchin 出 Lorentzian）

[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 那條「把白噪當成無數獨立小單音、算每根的 sideband 再求和」的路線是 [P1] 的原始路線，
物理直覺很強、但代數上是**啟發式（heuristic）**的：它在「白噪 $=$ 單音疊加」「factor-8 記帳」
那幾步用了手算的功率簿記。這一頁把同一個結果用**訊號與系統的嚴格機器**重做一遍——
直接寫下 LTV 輸出相位的**時間平均自相關（time-averaged autocorrelation）**，用 ISF 的傅立葉
係數展開，讓 $\sum c_n^2=2\Gamma_{rms}^2$ **自己從自相關裡掉出來**，再用 **Wiener-Khinchin 定理**
取頻譜。讀者若熟悉「LTI 系統 $S_y=|H|^2S_x$」，這頁會把它升級成「**LTV / cyclostationary**」版本。

> **為什麼要做這頁**：振盪器是**週期時變（periodically time-varying）**系統，它的輸出不是嚴格
> 平穩（stationary）而是 **cyclostationary（週期穩態，統計量以週期 $T$ 重複）**。對 cyclostationary
> 過程，正確的譜分析要先對**絕對時間 $t$ 做一個週期平均**，把它「平穩化」，再做 Wiener-Khinchin。
> 這一頁就是老實走完這條路；走完你會看到 $\Gamma_{rms}$ 不是被「湊」出來的，而是自相關的週期平均
> 的**必然產物**。

## 第 A 步：寫下相位的雙時間自相關（two-time autocorrelation）

從 [P1] Eq.(11) 的相位積分出發，定義 $g(\tau)\equiv\Gamma(\omega_0\tau)/q_{max}$（把 ISF 與
normalization 併成一個權重核），則 $\phi(t)=\int_{-\infty}^{t}g(\tau)\,i_n(\tau)\,d\tau$。
但為了乾淨看出頻譜，我們改看**相位的時間導數** $\dot\phi$（瞬時頻率擾動），它的自相關更直接
（相位本身是非平穩漫步，見 [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)；
$\dot\phi$ 才是 cyclostationary-平穩的）。由微積分基本定理：

$$
\dot\phi(t)=g(t)\,i_n(t)=\frac{\Gamma(\omega_0 t)}{q_{max}}\,i_n(t).
$$

這是一個**乘法型 LTV**：輸入白噪 $i_n(t)$ 被一個**確定的週期權重** $g(t)$ 逐點調制。算它的
**雙時間自相關**：

$$
R_{\dot\phi}(t,\,t+\tau)=\big\langle\dot\phi(t)\,\dot\phi(t+\tau)\big\rangle=g(t)\,g(t+\tau)\,\big\langle i_n(t)\,i_n(t+\tau)\big\rangle.
$$

- **用到的數學**：$g$ 是確定函數（可提到期望外），只有 $i_n$ 是隨機的。
- **白噪自相關是 delta，係數是 $S_i/2$**：白噪不同時刻不相關，所以自相關是一根 $\delta$。
  本站的 $S_i\equiv\overline{i_n^2}/\Delta f$ 是**單邊（single-sided）PSD**——只在 $f\gt0$ 上定義、
  $\int_0^{B}S_i\,df$ 就是頻寬 $B$ 內的 $\overline{i_n^2}$。Wiener-Khinchin 的傅立葉對是在
  $-\infty\lt f\lt\infty$ 上寫的，那裡的**雙邊（two-sided）平坦位準是 $S_i/2$**（同一份功率攤在正負頻兩邊），
  而 $\delta(\tau)$ 的係數等於雙邊位準：

$$
\big\langle i_n(t)\,i_n(t+\tau)\big\rangle=\frac{S_i}{2}\,\delta(\tau).
$$

檢查：頻寬 $B$ 的帶限白噪 $R(0)=\int_{-B}^{B}\tfrac{S_i}{2}df=S_iB=\overline{i_n^2}$ ✓。
這跟 [P2] Appendix A 在 Eq.(43) 前一行印的白噪自相關（p.802，帶 $(1/2)$ 因子）是**同一顆 $\tfrac12$**，
逐字對帳見 [p2_appendix_a_reconciliation](/99_appendix/p2_appendix_a_reconciliation)；
本頁末的「數值驗證」直接量出這顆 $\tfrac12$。代入：

$$
R_{\dot\phi}(t,\,t+\tau)=g(t)\,g(t+\tau)\,\frac{S_i}{2}\,\delta(\tau).
$$

- **關鍵觀察（cyclostationary）**：這個自相關**顯含絕對時間 $t$**（透過 $g(t)g(t+\tau)$），
  而且以週期 $T$ 重複（$g$ 是 $T$-週期）——這正是 **cyclostationary** 的定義特徵，**不是**平穩。
  不能直接 Wiener-Khinchin；要先對 $t$ 做週期平均。
- **單位檢查**：$[g]=1/\text{C}$（$\Gamma$ 無因次 $/q_{max}$），$[g^2 (S_i/2)\delta(\tau)]=
  \text{C}^{-2}\cdot(\text{A}^2/\text{Hz})\cdot(1/\text{s})$。以 $\delta(\tau)$ 帶 $1/\text{s}$、$\text{Hz}^{-1}=\text{s}$，
  化簡 $=\text{C}^{-2}\text{A}^2=\text{s}^{-2}$，即 $[\dot\phi^2]=(\text{rad/s})^2$ ✓（$\tfrac12$ 無因次，不影響單位）。

## 第 B 步：對絕對時間做週期平均 → 把 cyclostationary 平穩化

cyclostationary 過程的**時間平均自相關**定義為對絕對時間 $t$ 取一個週期的平均：

$$
\bar R_{\dot\phi}(\tau)=\frac{1}{T}\int_{0}^{T}R_{\dot\phi}(t,\,t+\tau)\,dt=\Big[\frac{1}{T}\int_{0}^{T}g(t)\,g(t+\tau)\,dt\Big]\,\frac{S_i}{2}\,\delta(\tau).
$$

中括號裡是權重核 $g$ 的**自相關（確定性、週期）**，記為

$$
\bar g(\tau)\equiv\frac{1}{T}\int_{0}^{T}g(t)\,g(t+\tau)\,dt=\frac{1}{q_{max}^2}\cdot\frac{1}{T}\int_{0}^{T}\Gamma(\omega_0 t)\,\Gamma(\omega_0(t+\tau))\,dt.
$$

因為 $\delta(\tau)$ 只在 $\tau=0$ 取值，我們**只需要 $\bar g(0)$**：

$$
\bar R_{\dot\phi}(\tau)=\bar g(0)\,\frac{S_i}{2}\,\delta(\tau),\qquad\bar g(0)=\frac{1}{q_{max}^2}\cdot\frac{1}{T}\int_{0}^{T}\Gamma^2(\omega_0 t)\,dt.
$$

- **用到的物理/數學**：把絕對時間平均掉，等於把振盪器在一個週期內「各個相位的敏感度」平均起來——
  這正是 cyclostationary 系統「等效平穩化」的標準手法。
- **這一步就要冒出 $\Gamma_{rms}$ 了**：$\dfrac{1}{T}\int_0^T\Gamma^2(\omega_0t)\,dt$ 就是 ISF 的**均方**。

## 第 C 步：用 ISF 傅立葉係數展開 → $\sum c_n^2=2\Gamma_{rms}^2$ 自然掉出來

把 $\Gamma$ 的傅立葉級數（[P1] Eq.(12)）代進 $\bar g(0)$ 的那個均方積分，**自己**就生出 $\sum c_n^2$。
先把均方積分換成對相位 $x=\omega_0 t$ 的積分（$dt=dx/\omega_0$，一個週期 $t:0\to T$ 對應 $x:0\to2\pi$）：

$$
\frac{1}{T}\int_{0}^{T}\Gamma^2(\omega_0 t)\,dt=\frac{1}{2\pi}\int_{0}^{2\pi}\Gamma^2(x)\,dx.
$$

代入 $\Gamma(x)=\dfrac{c_0}{2}+\sum_{n\ge1}c_n\cos(nx+\theta_n)$ 並平方。用三角函數的**正交性**
（不同諧波互相積分為零、同諧波 $\int_0^{2\pi}\cos^2=\pi$、DC 項 $\int_0^{2\pi}dx=2\pi$）：

$$
\frac{1}{2\pi}\int_{0}^{2\pi}\Gamma^2(x)\,dx=\Big(\frac{c_0}{2}\Big)^2+\sum_{n=1}^{\infty}\frac{c_n^2}{2}=\frac{c_0^2}{4}+\frac12\sum_{n=1}^{\infty}c_n^2.
$$

左邊正是 $\Gamma_{rms}^2$ 的**定義**（ISF 的均方）。把右邊的 $\tfrac12$ 提出來，DC 項的係數
$\tfrac14=\tfrac12\cdot\tfrac12$ 就明白寫成一條恆等式：

$$
\Gamma_{rms}^2\equiv\frac{1}{2\pi}\int_{0}^{2\pi}\Gamma^2(x)\,dx=\frac{c_0^2}{4}+\frac12\sum_{n=1}^{\infty}c_n^2=\frac12\Big[\frac{c_0^2}{2}+\sum_{n=1}^{\infty}c_n^2\Big]
\quad\Longrightarrow\quad
2\,\Gamma_{rms}^2=\frac{c_0^2}{2}+\sum_{n=1}^{\infty}c_n^2.
$$

也就是說：**DC 項以 $c_0^2/2$（半權重）進帳，$n\ge1$ 各項以整個 $c_n^2$ 進帳**。半權重的來源只有一個——
級數的 DC 項寫成 $\tfrac{c_0}{2}$ 而不是 $c_0$，所以它的均方是 $(c_0/2)^2=c_0^2/4$，而每個諧波的均方是
$c_n^2/2$；兩者都提出 $\tfrac12$ 後，DC 剩 $c_0^2/2$、諧波剩 $c_n^2$。[P1] Eq.(20) 把右邊這個和簡記成
$\sum_{n=0}^{\infty}c_n^2$（注意它用 $\tfrac1\pi$ 而非 $\tfrac1{2\pi}$）：

$$
\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}\Gamma^2(x)\,dx=2\cdot\frac{1}{2\pi}\int_0^{2\pi}\Gamma^2(x)\,dx=\boxed{\,2\,\Gamma_{rms}^2\,}.
$$

> **注意（DC 半權重）**：這裡的 $\sum_{n=0}^{\infty}c_n^2$ 中 DC 項是以 $c_0^2/2$（半權重）計入的；
> 若誤用整權 $c_0^2$，總和會比 $2\Gamma_{rms}^2$ 多出 $c_0^2/2$。這正是 Parseval 對 $\tfrac{c_0}{2}$ 形式 DC
> 的記帳（$\Gamma$ 級數第一項寫成 $\tfrac{c_0}{2}$，平方後給 $\tfrac{c_0^2}{4}=\tfrac12\cdot\tfrac{c_0^2}{2}$），
> 詳見 [rms_isf](/03_isf_core_theory/rms_isf)。

**$\sum c_n^2=2\Gamma_{rms}^2$ 就這樣從自相關的週期平均裡自然掉出來**——不需要 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
第 3b 步那種手算的 factor-8 簿記。差別只在「$\tfrac1\pi$ vs $\tfrac1{2\pi}$」這個 Parseval 慣例帶來的因子 2，與
[rms_isf](/03_isf_core_theory/rms_isf) 完全一致。於是

$$
\bar g(0)=\frac{1}{q_{max}^2}\cdot\Gamma_{rms}^2=\frac{\Gamma_{rms}^2}{q_{max}^2}.
$$

- **物理意義**：$\dot\phi$ 的時間平均自相關強度（$\tau=0$ 的權重）**正比於 $\Gamma_{rms}^2/q_{max}^2$**——
  振盪器把白噪「攪拌」進相位的有效增益，就是 ISF 的均方除以 $q_{max}^2$。所有 $c_n$ 的細節都被
  Parseval 收進一個 $\Gamma_{rms}$。

## 第 D 步：Wiener-Khinchin → 相位頻譜 $S_\phi\propto1/\Delta\omega^2$

代入第 C 步的 $\bar g(0)=\Gamma_{rms}^2/q_{max}^2$，現在 $\bar R_{\dot\phi}(\tau)=\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{2}\,\delta(\tau)$ 已經是**只依賴 $\tau$**
的平穩自相關了，可以放心套 **Wiener-Khinchin**（自相關的傅立葉變換 $=$ PSD）。
**慣例旗標**：這個變換對 $\tau\in(-\infty,\infty)$ 積分，得到的是定義在**正負頻兩側**的
**雙邊（two-sided）PSD**，以上標 $DS$ 標記：

$$
S_{\dot\phi}^{DS}(\Delta\omega)=\int_{-\infty}^{\infty}\bar R_{\dot\phi}(\tau)\,e^{-j\Delta\omega\tau}\,d\tau=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{2}\int_{-\infty}^{\infty}\delta(\tau)e^{-j\Delta\omega\tau}d\tau=\frac{\Gamma_{rms}^2\,S_i}{2\,q_{max}^2},\qquad-\infty\lt\Delta\omega\lt\infty.
$$

$\delta$ 的傅立葉變換是常數 $1$——所以 **$\dot\phi$（瞬時頻率擾動）的頻譜是白的**，雙邊位準
$\Gamma_{rms}^2 S_i/(2q_{max}^2)$。這個數就是 [P2] Eq.(11), p.793 的**相位**方差成長率
（$\sigma_{\Delta\phi}^2=\Gamma_{rms}^2S_i\,\Delta T/(2q_{max}^2)$；本站把它記作 $\kappa^2$，單位 $\text{rad}^2/\text{s}$。
注意 [P2] 自己的 $\kappa$（Eq.(12)）是**時間** jitter 常數 $\sigma_{\Delta T}=\kappa\sqrt{\Delta T}$，兩者差 $\omega_0$ 倍，
換算見 [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)），也等於 $2D$（$D=\Gamma_{rms}^2S_i/(4q_{max}^2)$）；
canonical 值 $0.25\times10^{-24}/(2\times10^{-24})=0.125\ \text{rad}^2/\text{s}$。
單位：$\text{C}^{-2}\cdot\text{A}^2/\text{Hz}=\text{s}^{-2}\cdot\text{s}=\text{rad}^2/\text{s}$，
即 $(\text{rad/s})^2/\text{Hz}$ ✓（密度是對 $f=\Delta\omega/2\pi$ 的每 Hz 計，$\Delta\omega$ 只是橫軸的標記）。

下一步：相位是頻率的積分，**頻域積分等於除以 $j\Delta\omega$**，功率譜要除以 $\Delta\omega^2$：

$$
S_\phi^{DS}(\Delta\omega)=\frac{S_{\dot\phi}^{DS}(\Delta\omega)}{\Delta\omega^2}=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{2\,\Delta\omega^2}\qquad[\text{rad}^2/\text{Hz}],\quad-\infty\lt\Delta\omega\lt\infty.
$$

**最後一步：雙邊 → 單邊。** 本站（與量測儀器）的 $S_\phi$ 一律是**單邊**譜：只看 $\Delta\omega\gt0$，
把負頻那一半的功率摺到正頻上。$S_\phi^{DS}$ 是偶函數，所以摺疊就是乘 2：

$$
S_\phi(\Delta\omega)=2\,S_\phi^{DS}(\Delta\omega)=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{\Delta\omega^2}\qquad[\text{rad}^2/\text{Hz}],\quad\Delta\omega\gt0.
$$

**兩顆 2 的帳**：第 A 步的 $\tfrac12$（單邊 $S_i$ → 雙邊位準 $S_i/2$）與這裡的 $2$（雙邊 $S_\phi^{DS}$ →
單邊 $S_\phi$）**一進一出、剛好相消**——「單邊輸入 PSD → 單邊輸出 PSD」的轉換增益裡不留任何 2；
只有在中途的自相關與雙邊譜上才看得到那顆 $\tfrac12$。若把 $S_i$ 誤當雙邊（寫成 $R=S_i\delta$）又忘了
最後的摺疊，兩個錯會互相抵消而得到同一個答案，但中間每一條式子都差 2；若只犯其中一個，
$S_\phi$ 差 2 倍（$3$ dB）。

於是單邊結果跟 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)「時域乾淨版」（factor-of-2 註記裡的）
$S_\phi=\Gamma_{rms}^2S_i/(q_{max}^2(2\pi f)^2)$ **逐字相同**（$\Delta\omega=2\pi f$）。

- **$1/f^2$ 的嚴格出處**：這條 $1/\Delta\omega^2$ **完全來自「$\dot\phi\to\phi$ 的那次積分」**
  （$1/(j\Delta\omega)$ 濾波器），與 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
  開頭的物理直覺一字不差——只是現在是用 Wiener-Khinchin 嚴格證出來的，不是手算 sideband 湊出來的。
- **白噪頻譜的角色**：$\dot\phi$ 白、$\phi$ 才 $1/f^2$——這也解釋了為什麼相位是 random walk
  （白色頻率擾動的積分 $=$ Wiener process），正是下一頁 Lorentzian 的起點。

## 嚴格版 vs 啟發式版：對照表

| 項目 | 啟發式（[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 第 3 步，[P1] 原路線） | 嚴格（本頁，cyclostationary 自相關） |
|---|---|---|
| 出發點 | 白噪 $=$ 無數獨立單音 | $\dot\phi=g(t)i_n(t)$ 的雙時間自相關 |
| 平穩化 | 隱含在「對 $n$ 求和」 | 顯式對絕對時間 $t$ 做週期平均 |
| $\Gamma_{rms}$ 來源 | Parseval 手動代入（Eq.20） | 週期平均積分 $\tfrac1{2\pi}\int\Gamma^2$ 自然生出 |
| $\sum c_n^2=2\Gamma_{rms}^2$ | 外加套用 | 從自相關 $\bar g(0)$ 掉出來 |
| $1/\Delta\omega^2$ 來源 | 單音 sideband 的 $1/\Delta\omega^2$ | $\dot\phi\to\phi$ 積分的 $1/(j\Delta\omega)$ |
| 取頻譜 | 累加 sideband 功率 | Wiener-Khinchin（自相關 FT） |
| factor-of-2 | SSB 記帳（$\mathcal{L}$ 的 $/4$） | 單邊 $S_i$ → $\tfrac{S_i}{2}\delta$ → 雙邊 $S_\phi^{DS}$ → $\times2$ → 單邊 $S_\phi$；$\mathcal{L}=S_\phi/2$ 給 $/2$，與 $/4$ 差 2 同前述 |

> **小結**：嚴格版用「cyclostationary 自相關 → 週期平均 → Wiener-Khinchin」三板斧，把 $\Gamma_{rms}$
> 與 $1/f^2$ 都變成**機械化的必然結果**。$\sum c_n^2=2\Gamma_{rms}^2$ 不是巧合，而是 ISF 均方的
> Parseval 化身。這套自相關機器也正是下一頁 [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
> 的入口：那裡把「$\dot\phi$ 白 ⇒ $\phi$ 是 random walk」推到底，得出**載波自相關
> $R_x(\tau)=\tfrac12\cos(\omega_0\tau)e^{-D|\tau|}$**，再 Wiener-Khinchin 出 **Lorentzian**——
> 解開 $1/f^2$ 在 $\Delta\omega\to0$ 的假發散。本頁算出的**單邊** $S_\phi=\Gamma_{rms}^2S_i/(q_{max}^2\Delta\omega^2)$
> 正是那裡 $D=\Gamma_{rms}^2S_i/(4q_{max}^2)$ 的來源（本站單邊記帳 $S_\phi=4D/\Delta\omega^2$，雙邊
> $2D/\Delta\omega^2$，即本頁第 D 步的 $S_\phi^{DS}$；對帳見 [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)）。

## 數值驗證：直接量出那顆 $\tfrac12$

下面這段不畫圖，只做四件事：產生一筆**單邊 PSD $=S_i$** 的帶限白噪（取樣率 $f_s$，頻寬 $f_s/2$），
(1) 用 Welch 確認它的單邊 PSD 真的是 $S_i$；(2) 數值算自相關、對 $\tau$ 求面積
$\int R(\tau)d\tau\approx\sum_kR[k]\,\Delta t$——$\delta$ 的係數就是這個面積，應為 $S_i/2$；
(3) 乘上 ISF 權重 $g(t)$ 得 $\dot\phi$，它的自相關面積就是雙邊 $S_{\dot\phi}^{DS}$；
(4) 同一筆 $\dot\phi$ 的 Welch **單邊** PSD 應為雙邊的 2 倍。最後附 canonical 例 B 與第 C 步恆等式的數值。

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal
from simulations.common.noise_utils import white_noise, estimate_psd

F0 = 5e9
W0 = 2 * np.pi * F0
QMAX, SI, GRMS = 1e-12, 1e-24, 0.5        # canonical 參數
FS = 64 * F0                              # 取樣率：每週期 64 點（noise 頻寬 fs/2 = 160 GHz）
DT = 1 / FS
N = 2**20                                 # = 16384 個整數週期
rng = np.random.default_rng(12)

i_n = white_noise(N, SI, FS, rng)         # 單邊 PSD = S_i 的帶限白噪

# (1) Welch 單邊 PSD：確認輸入真的是「單邊 S_i」
f, pxx = estimate_psd(i_n, FS, nperseg=4096)
print(f"{np.mean(pxx[1:-1])/SI:.2f}")     # -> 1.00 (單邊 PSD / S_i)

# (2) 自相關面積 ∫R(τ)dτ ≈ Σ_k R[k]·dt：δ 的係數應為 S_i/2
K = 20
def acorr_area(x):
    r = [np.mean(x[:N - k] * x[k:]) for k in range(K + 1)]
    return (r[0] + 2 * sum(r[1:])) * DT

print(f"{acorr_area(i_n)/SI:.2f}")        # -> 0.50 (自相關面積 / S_i：就是那顆 1/2)

# (3) ISF 加權後的 φ̇ = g(t) i_n(t)：自相關面積 = 雙邊 S_φ̇ 位準
t = np.arange(N) * DT
g = np.sqrt(2.0) * GRMS * gamma_lc_ideal(W0 * t) / QMAX
phidot = g * i_n
s_ds = acorr_area(phidot)
print(f"{s_ds:.3f}")                      # -> 0.126 rad^2/s (雙邊 S_φ̇，理論 κ² = 0.125)
print(f"{s_ds/(GRMS**2*SI/QMAX**2):.2f}") # -> 0.50 (雙邊位準 / [Γrms² S_i/q_max²])

# (4) 同一筆 φ̇ 的 Welch 單邊 PSD（低頻平坦段）
f, pxx = estimate_psd(phidot, FS, nperseg=4096)
s_ss = np.mean(pxx[(f > 0) & (f < 0.4 * F0)])
print(f"{s_ss:.3f}")                      # -> 0.254 rad^2/s (單邊 S_φ̇，理論 0.25)
print(f"{s_ss/s_ds:.2f}")                 # -> 2.02 (單邊 / 雙邊，理論 2)

# (5) canonical 例 B：單邊 S_φ(1 MHz) 與兩個 L 家族
dw = 2 * np.pi * 1e6
s_phi = GRMS**2 * SI / (QMAX**2 * dw**2)
print(f"{s_phi:.3e}")                     # -> 6.333e-15 rad^2/Hz (單邊 S_φ @ 1 MHz)
print(f"{10*np.log10(s_phi/2):.1f}")      # -> -145.0 dBc/Hz (L = S_φ/2，「/2」家族)
print(f"{10*np.log10(s_phi/4):.1f}")      # -> -148.0 dBc/Hz ([P1] Eq.(21) 的「/4」家族)

# (6) 第 C 步的 DC 半權重恆等式：Γ = c0/2 + c1 cos x
x = np.linspace(0, 2 * np.pi, 100000, endpoint=False)
c0, c1 = 0.6, 1.0
gam = c0 / 2 + c1 * np.cos(x)
print(f"{np.mean(gam**2):.3f}")           # -> 0.590 (直接數值均方 Γrms²)
print(f"{0.5*(c0**2/2 + c1**2):.3f}")     # -> 0.590 ((1/2)[c0²/2 + c1²]：DC 半權重，吻合)
print(f"{0.5*(c0**2 + c1**2):.3f}")       # -> 0.680 ((1/2)[c0² + c1²]：DC 誤用整權，多出 c0²/4 = 0.09)
```

- **怎麼讀**：(1) 印 1.00、(2) 印 0.50——同一筆資料，單邊 PSD 是 $S_i$、自相關的 $\delta$ 係數是 $S_i/2$，
  這就是第 A 步的 $\tfrac12$。(3) 的 0.126 對上 $\kappa^2=0.125\ \text{rad}^2/\text{s}$（雙邊）；
  (4) 的 0.254 對上 $0.25$（單邊），比值 2.02 對上 2。(5) 的 $-145.0$ / $-148.0$ dBc/Hz 就是本站 canonical 的
  「$/2$」與「$/4$」兩個家族——本頁的更動沒有改任何最終數字。
- **誠實的限制**：這是有限長度（$2^{20}$ 點）的統計估計，(3)(4) 有約 1–2% 的取樣誤差（0.126、0.254、2.02 而非
  0.125、0.250、2.00）；離散時間的「$\delta$」是寬度 $\Delta t$ 的一格，所以白噪只白到 $f_s/2=160$ GHz（帶限），
  連續時間的理想白噪是 $f_s\to\infty$ 的極限。$\dot\phi$ 是 cyclostationary，Welch 對絕對時間的平均
  扮演的正是第 B 步的週期平均；這裡只取 $f\lt0.4f_0$ 的平坦段。這段檢查驗證的是**記帳**（單邊／雙邊的 2），
  不是電晶體層級的振盪器。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| $i_n(t)$ 為（近似）白噪，$\langle i_n(t)i_n(t+\tau)\rangle=\tfrac{S_i}{2}\delta(\tau)$ | 第 A 步的 delta 自相關成立，後續才能只取 $\bar g(0)$ | 若雜訊本身有色（如 flicker），自相關不是 delta，第 B 步不能只看 $\tau=0$，需另外處理（見 [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)） |
| $g(t)=\Gamma(\omega_0t)/q_{max}$ 為週期 $T$ 的確定函數（cyclostationary） | 第 B 步的週期平均把過程「平穩化」，才能套 Wiener-Khinchin | 非週期或隨機調制（如頻率抖動的振盪器）需要更一般的時變譜分析，本頁結果不直接適用 |
| 小擾動、相位對 noise 呈線性（[P1] Eq.(11) 成立） | $\dot\phi=g(t)i_n(t)$ 的線性關係成立 | 大注入使 ISF 本身被擾動改變，線性疊加失效 |
| 只關心 $\dot\phi$ 的平穩化自相關（不含 $\tau\neq0$ 的細節） | Step D 只用到 $\bar g(0)$，$S_{\dot\phi}$ 為白 | 若要近載波（$\Delta\omega\to0$）的精確線形，需保留相位本身的 random-walk 統計，見 [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |

## 與哪些 paper／公式對應

- 起點：LTV 相位積分 [P1] Eq.(11), p.182；ISF 傅立葉級數 [P1] Eq.(12), p.183。
- 對照的 Parseval 記帳：[P1] Eq.(20), p.185（本頁 Step C 重新推出同一個 $2\Gamma_{rms}^2$，但走自相關路線而非單音求和）。
- 最終結果與啟發式版的 [P1] Eq.(19)→(21)（p.185）等價，見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。
- 第 A 步白噪自相關的 $\tfrac12$：[P2] Appendix A，Eq.(43) 前一行與 Eq.(43)–(44), p.802（已對照 PDF 渲染頁）；
  雙邊位準 $\Gamma_{rms}^2S_i/(2q_{max}^2)$（本站記作 $\kappa^2$）對應 [P2] Eq.(11), p.793 的相位方差成長率。逐字對帳見
  [p2_appendix_a_reconciliation](/99_appendix/p2_appendix_a_reconciliation)。
- Wiener-Khinchin 定理本身是標準訊號與系統結果，不在 5 篇 PDF 內；本頁只用它做工具，不改變 [P1] 的物理結論。

## 重點回顧

- 啟發式版（[P1] 原路線）靠「白噪 = 無數獨立單音」手算 sideband 功率再求和；嚴格版改走
  「LTV 自相關 → cyclostationary 週期平均 → Wiener-Khinchin」三板斧，同一個結果**機械化**推出。
- 振盪器輸出是 **cyclostationary**（統計量隨絕對時間 $t$ 以週期 $T$ 重複），不是嚴格平穩；
  必須先對 $t$ 做週期平均「平穩化」，才能套用 Wiener-Khinchin。
- $\sum c_n^2=2\Gamma_{rms}^2$ **不是外加代入**的 Parseval 關係，而是週期平均積分
  $\tfrac1{2\pi}\int_0^{2\pi}\Gamma^2(x)dx$ 的自然結果。
- **單邊／雙邊的帳**：$S_i$ 是單邊 PSD，白噪自相關是 $\tfrac{S_i}{2}\delta(\tau)$；Wiener-Khinchin 給的是
  **雙邊** $S_\phi^{DS}=\Gamma_{rms}^2S_i/(2q_{max}^2\Delta\omega^2)$，單邊 $S_\phi=2S_\phi^{DS}$。
- 單邊結果與啟發式版逐字相同：$S_\phi(\Delta\omega)=\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{\Delta\omega^2}$，
  $1/\Delta\omega^2$ 完全來自 $\dot\phi\to\phi$ 的那次積分。
- 本頁是 [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 的入口：那裡把同一套自相關機器
  用在相位本身（而非 $\dot\phi$），解開 $1/f^2$ 在載波處的假發散。

## 延伸閱讀

- 啟發式版全文（含 canonical 例 B、factor-of-2 註記）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- $\Gamma_{rms}$ 與 Parseval 的完整討論：[rms_isf](/03_isf_core_theory/rms_isf)
- 同一顆 $\tfrac12$ 在 [P2] Appendix A 的出處與逐因子對帳：[p2_appendix_a_reconciliation](/99_appendix/p2_appendix_a_reconciliation)
- 近載波 Lorentzian、線寬 $D/\pi$：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- diffusion 常數 $D$ 與各頁記帳慣例對帳：[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
- close-in 的 $1/f^3$ 上轉：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
