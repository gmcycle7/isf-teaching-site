---
title: Jitter 核的嚴格推導（TIE / N-period / cycle-to-cycle）
description: 在「單邊 S_φ、∫₀^∞」單一慣例下，從 φ(t+NT)−φ(t) 一步步推出 TIE 核 1、period 核 4sin²(πfNT)、cycle-to-cycle 核 16sin⁴(πfT)；白噪 FM 封閉式精確回收 [P2] Eq.(8)/(11) 的 σ_Δφ=κ√(NT)；flicker 1/f³ 給含 log 項的封閉式；再合成 [P2] Fig.16 的兩段式 σ(Δt)=√(κ²Δt+ζ²Δt²)、corner Δt_c=κ²/ζ² 與頻域 1/f³ corner 的映射；lab_24 Monte-Carlo 驗證比值 ≈1.00，正式關閉 worked_examples 例 C3 的前置常數 TODO。新增「論文原生推導」節：[P2] Appendix A（Eq.(40)–(51)，p.802–803）逐字轉錄與逐因子對帳，時域自相關路與頻域核路重演同一顆 κ²ΔT。
---

import NumericQuiz from "@site/src/components/NumericQuiz";

# Jitter 核的嚴格推導：TIE、N-period、cycle-to-cycle

> 先備：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) · [stochastic_noise_basics](/02_foundations/stochastic_noise_basics) · [dsp_view_of_phase_noise](/02_foundations/dsp_view_of_phase_noise) ｜ 接下來：[allan_variance](/02_foundations/allan_variance) · [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)

[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) 已經給了三種 jitter 權重核的
「操作版」；本頁把它們**從第一原理嚴格推出來**，並且回答那個一直懸著的問題：
**前置常數到底是多少？哪個 2 屬於哪個慣例？** 答案用三把尺互相校準：
（1）逐步推導、（2）與 [P2] 已核實的 $\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$ 精確對上、
（3）Monte-Carlo 時域量測（`simulations/lab_24_jitter_kernels.py`），三者吻合到 ~0.1%。

> **本頁取代先前的外部慣例 TODO**：本站先前在 worked_examples 例 C3 把 period-jitter
> 核的前置常數標為「外部文獻、待確認」。本頁已從第一原理推導並經 Monte-Carlo 驗證：
> 在「**單邊 $S_\phi$、$\int_0^\infty$**」慣例下前置常數就是 $1/\omega_0^2$（**不是**
> $2/\omega_0^2$——那個 2 屬於雙邊譜或 $\mathcal{L}=\tfrac12 S_\phi$ 的記帳，見第 0 步
> 對照表）。例 C3 所用的核與常數**正確**；其數值 27.6 fs 是封閉解 28.28 fs 在
> $10^3$–$10^{10}$ Hz 頻帶截斷後的結果（本頁第 7 節有逐一對帳的標記）。

> **物理直覺（先講結論）**：三種 jitter 是**同一條相位過程 $\phi(t)$ 的三種讀法**——
> 直接讀（TIE）、隔 $N$ 拍相減讀（N-period）、相鄰差再相減讀（cycle-to-cycle）。
> 「相減」在頻域就是乘一個確定的濾波器；把 $S_\phi(f)$ 乘上那個濾波器的 $\lvert H\rvert^2$
> 再積分，就是該種 jitter 的變異數。核的形狀決定「哪一段頻率的 phase noise 會被算進來」：
> TIE 吃低頻、period 是一階高通、c2c 是二階高通。所有 2 與 4 都能被追蹤到出處。

## 第 0 步：唯一慣例宣告（本頁所有公式的地基）

**本頁只用一種慣例**：$S_\phi(f)$ 是 **excess phase 的單邊（one-sided）功率譜密度**，
單位 $\text{rad}^2/\text{Hz}$，定義在 $f\ge0$，所有積分都是 $\int_0^\infty df$。
變異數與它的關係是

$$
\sigma_\phi^2=\int_0^\infty S_\phi(f)\,df\qquad[\text{rad}^2].
$$

沒有任何額外的 2。文獻上常見的其他寫法，換算如下（**同一個物理量、三種記帳**；
$S_\phi^{DS}=S_\phi/2$ 是雙邊譜、$\mathcal{L}_{\text{lin}}=\tfrac12 S_\phi$ 是小角 SSB，
見 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) 的推導）：

| 量 | 單邊 $S_\phi$（本頁） | 雙邊 $S_\phi^{DS}$（積 $f\ge0$） | $\mathcal{L}_{\text{lin}}$（小角） |
|---|---|---|---|
| $\sigma_{\text{TIE}}^2$ | $\dfrac{1}{\omega_0^2}\displaystyle\int S_\phi\,df$ | $\dfrac{2}{\omega_0^2}\displaystyle\int S_\phi^{DS}\,df$ | $\dfrac{2}{\omega_0^2}\displaystyle\int \mathcal{L}_{\text{lin}}\,df$ |
| $\sigma_{P}^2(N)$ | $\dfrac{1}{\omega_0^2}\displaystyle\int S_\phi\,4\sin^2(\pi fNT)\,df$ | $\dfrac{2}{\omega_0^2}\displaystyle\int S_\phi^{DS}\,4\sin^2\,df$ | $\dfrac{8}{\omega_0^2}\displaystyle\int \mathcal{L}_{\text{lin}}\sin^2\,df$ |
| $\sigma_{c2c}^2$ | $\dfrac{1}{\omega_0^2}\displaystyle\int S_\phi\,16\sin^4(\pi fT)\,df$ | $\dfrac{2}{\omega_0^2}\displaystyle\int S_\phi^{DS}\,16\sin^4\,df$ | $\dfrac{32}{\omega_0^2}\displaystyle\int \mathcal{L}_{\text{lin}}\sin^4\,df$ |

- 三欄算出來**數字完全一樣**——lab_24 用同一條白噪譜以三種記帳各算一次 period jitter，
  印出 `0.1592 / 0.1592 / 0.1592 fs`（見第 8 節 code）。
- 文獻上寫成 $\frac{2}{\omega_0^2}\int S_\phi\cdot4\sin^2 df$ 的版本，其 $S_\phi$ 若不是雙邊譜
  就是把 $\mathcal{L}$ 叫成了 $S_\phi$；把單邊譜塞進那條式會**多算 2 倍變異數**（jitter 多
  $\sqrt2$）。這正是例 C3 當年標 TODO 的癥結，也是本站 factor-of-2 紀律的又一案例
  （對照規範第 3 節的 SSB $/4$ vs 時域 $/2$ 註記）。
- $\mathcal{L}$ 欄只在小角（$\sigma_\phi\ll1$ rad）成立，因為 $\mathcal{L}\approx\tfrac12 S_\phi$
  本身是小角近似。

## 第 1 步：edge 時間誤差 = 相位的取樣（時域起點）

振盪輸出的總相位是 $\Phi(t)=\omega_0 t+\phi(t)$（[P1] Eq.(1), p.181 的相位項；
$\phi$ 為 excess phase，rad）。第 $k$ 個上升過零點 $t_k$ 由「總相位走滿 $k$ 圈」定義：

$$
\omega_0 t_k+\phi(t_k)=2\pi k.
$$

解 $t_k$（把 $\phi$ 視為小擾動、對 $t_k=kT$ 展開一階）：

$$
t_k=kT-\frac{\phi(t_k)}{\omega_0}\approx kT-\frac{\phi(kT)}{\omega_0}.
$$

- **用到的近似**：一階展開，要求 $\lvert\phi(t_k)-\phi(kT)\rvert\ll\lvert\phi(kT)\rvert$ 的效應
  可忽略，等價於 $\lvert\dot\phi\rvert\ll\omega_0$（瞬時頻率偏移遠小於載波）與
  $\sigma_t\ll T$（jitter 遠小於週期）。實務振盪器 jitter 是 fs、週期是百 ps，輕鬆成立。
- **失效條件**：cycle slip（$\Delta\phi$ 在一個相關時間內累到 $\sim$rad 量級）、大注入拉扯、
  或 AM-PM 轉換不可忽略時，edge 與相位不再一對一。
- **單位**：$[\phi/\omega_0]=\text{rad}/(\text{rad/s})=\text{s}$ ✓。

於是第 $k$ 個 edge 的**時間誤差**（TIE，time interval error，對理想時鐘的偏差）是

$$
\text{TIE}_k=t_k-kT=-\frac{\phi(kT)}{\omega_0}.
$$

負號只是「相位超前 = edge 提早」，取變異數後不影響任何結果。

## 第 2 步：三種 jitter = 相位的 0/1/2 階差分

沿用 [notation](/00_overview/notation)（規範第 2 節）的定義，全部改寫成 $\phi$ 的語言：

$$
\begin{aligned}
\text{TIE（absolute）：}\quad &\text{TIE}_k=-\frac{\phi(kT)}{\omega_0}
&&(\text{0 階：直接取樣})\\
\text{N-period jitter：}\quad &P_k(N)=\big(t_{k+N}-t_k\big)-NT=-\frac{\phi\big((k{+}N)T\big)-\phi(kT)}{\omega_0}
&&(\text{1 階差分，間隔 }NT)\\
\text{cycle-to-cycle：}\quad &C_k=T_{k+1}-T_k=-\frac{\phi\big((k{+}2)T\big)-2\phi\big((k{+}1)T\big)+\phi(kT)}{\omega_0}
&&(\text{2 階差分}).
\end{aligned}
$$

$N=1$ 的 $P_k(1)=T_k-T$ 就是一般說的 **period jitter**；$C_k$ 是相鄰兩個週期長度之差
（差分的差分）。三者都是 $\phi$ 的**線性運算**，所以下一步可以整批用頻域處理。

## 第 3 步：差分的變異數 ← 頻域核（核心引理，兩條路推）

要算的是 $\operatorname{Var}\big[\phi(t+\tau_0)-\phi(t)\big]$（$\tau_0=NT$）。給兩條互相
獨立的推導路；第二條在數學上更強，**連 $\phi$ 本身是隨機漫步（非平穩）都成立**。

### 路 A：假設 $\phi$ 廣義平穩（WSS），走自相關

**第 1 步：展開平方。** 設 $\phi$ WSS、零均值，自相關 $R_\phi(\tau)=\langle\phi(t)\phi(t+\tau)\rangle$：

$$
\operatorname{Var}\big[\phi(t+\tau_0)-\phi(t)\big]
=\big\langle\phi^2(t+\tau_0)\big\rangle+\big\langle\phi^2(t)\big\rangle-2\big\langle\phi(t)\phi(t+\tau_0)\big\rangle
=2\big[R_\phi(0)-R_\phi(\tau_0)\big].
$$

**第 2 步：Wiener–Khinchin。** 單邊譜的自相關表示（同
[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)；[P2] 在 p.803 走的
也是這條 Khinchin 路，其 Eq.(46)–(48)）：

$$
R_\phi(\tau)=\int_0^\infty S_\phi(f)\cos(2\pi f\tau)\,df.
$$

**第 3 步：代回並用半角公式。** $1-\cos\theta=2\sin^2(\theta/2)$，取 $\theta=2\pi f\tau_0$：

$$
\operatorname{Var}\big[\Delta\phi(\tau_0)\big]
=2\int_0^\infty S_\phi(f)\big[1-\cos(2\pi f\tau_0)\big]df
=\int_0^\infty S_\phi(f)\,\underbrace{4\sin^2(\pi f\tau_0)}_{\text{核}}\,df.
$$

這就是 $4\sin^2$ 核的全部來源：**係數 2 來自「差的變異數 = $2[R(0)-R(\tau_0)]$」、
另一個 2 來自半角公式**，兩個 2 相乘得 4，一個都不多。等價地，用濾波器語言：
$y(t)=\phi(t+\tau_0)-\phi(t)$ 是 LTI 濾波 $H(f)=e^{j2\pi f\tau_0}-1$，

$$
\lvert H(f)\rvert^2=\big(\cos(2\pi f\tau_0)-1\big)^2+\sin^2(2\pi f\tau_0)=2-2\cos(2\pi f\tau_0)=4\sin^2(\pi f\tau_0),
$$

而 WSS 過程過 LTI 濾波器：$S_y=\lvert H\rvert^2S_\phi$（單邊進、單邊出），積分即得同式。

### 路 B：不假設 $\phi$ 平穩——只要求「頻率雜訊」平穩（嚴格版）

白噪 FM 之下 $\phi$ 是隨機漫步，$R_\phi(0)$ 根本發散，路 A 嚴格說不成立。
但**增量**沒問題。定義瞬時頻率偏移 $\nu(t)\equiv\dot\phi(t)$（rad/s），假設 $\nu$ WSS，
其單邊譜由微分關係給出：

$$
S_\nu(f)=(2\pi f)^2\,S_\phi(f)\qquad[(\text{rad/s})^2/\text{Hz}].
$$

**第 1 步：把差分寫成 $\nu$ 的窗積分。**

$$
\Delta\phi(\tau_0)=\phi(t+\tau_0)-\phi(t)=\int_t^{t+\tau_0}\nu(u)\,du,
$$

即 $\nu$ 通過一個長度 $\tau_0$ 的 boxcar（矩形窗）濾波器 $w$。

**第 2 步：窗的頻率響應。**

$$
W(f)=\int_0^{\tau_0}e^{-j2\pi fu}\,du=\frac{1-e^{-j2\pi f\tau_0}}{j2\pi f},\qquad
\lvert W(f)\rvert^2=\frac{4\sin^2(\pi f\tau_0)}{(2\pi f)^2}\quad[\text{s}^2].
$$

**第 3 步：組合。** $\operatorname{Var}[\Delta\phi]=\int_0^\infty S_\nu\lvert W\rvert^2df$，
$(2\pi f)^2$ 恰好對消：

$$
\operatorname{Var}\big[\Delta\phi(\tau_0)\big]
=\int_0^\infty (2\pi f)^2 S_\phi(f)\cdot\frac{4\sin^2(\pi f\tau_0)}{(2\pi f)^2}\,df
=\int_0^\infty S_\phi(f)\,4\sin^2(\pi f\tau_0)\,df.\qquad\checkmark
$$

**同一個核**，但這次只用了「$\nu$ 平穩」——對 $1/f^2$（白噪 FM）與截止後的 $1/f^3$
（flicker FM）都嚴格成立。核在 $f\to0$ 的 $f^2$ 零點正是讓 $1/f^2$ 譜積分收斂的機制
（與 [allan_variance](/02_foundations/allan_variance) 的差分核同一招；ADEV 的核
$2\sin^4(\pi f\tau)/(\pi f\tau)^2$ 是「閘平均＋相鄰差」的親戚）。

- **dimension check（路 B）**：$S_\nu\,[\text{rad}^2\text{s}^{-2}/\text{Hz}]\times\lvert W\rvert^2\,[\text{s}^2]\times df\,[\text{Hz}]=\text{rad}^2$ ✓。

### 核 (a)：TIE——不差分，核 $=1$

把第 1 步的 $\text{TIE}_k=-\phi(kT)/\omega_0$ 取變異數（這裡**必須**假設 $\phi$ 的功率
在觀測頻帶內有限，所以誠實地寫頻帶 $[f_1,f_2]$）：

$$
\boxed{\ \sigma_{\text{TIE}}^2=\frac{1}{\omega_0^2}\int_{f_1}^{f_2}S_\phi(f)\,df\ }
$$

- **頻帶的誠實聲明**：自由振盪器 $S_\phi\propto1/f^2$，$f_1\to0$ 時積分發散——這不是公式
  壞掉，而是隨機漫步的變異數本來就無上界（第 6 節的 $\kappa^2\Delta t$ 隨 $\Delta t$
  線性長）。實務上 $f_1$ 由量測時長或 PLL 迴路頻寬決定、$f_2$ 由量測頻寬決定；
  **不標頻帶的 TIE 數字沒有意義**。canonical 例 C（$-100$ dBc/Hz@1 MHz、積 1–100 MHz）
  給 $\sigma_t=447.9$ fs，見第 8 節標記。
- **dimension check**：$(\text{rad}^2/\text{Hz})\times\text{Hz}\,/\,(\text{rad/s})^2=\text{s}^2$ ✓。

### 核 (b)：N-period——一階差分，核 $4\sin^2(\pi fNT)$

把核心引理（$\tau_0=NT$）除以 $\omega_0^2$ 換成時間：

$$
\boxed{\ \sigma_P^2(N)=\frac{1}{\omega_0^2}\int_0^\infty S_\phi(f)\,4\sin^2(\pi fNT)\,df\ }
$$

- **核的形狀**：$f\to0$ 時 $4\sin^2(\pi fNT)\approx(2\pi fNT)^2\propto f^2$（一階高通，把
  close-in 壓掉）；$f=1/(2NT)$ 時達最大值 4；之後以週期 $1/(NT)$ 振盪於 0 與 4 之間，
  平均值 2。$N$ 越大、核的「窗」越往低頻搬——長區間差分看得到更慢的漂移。
- **與 [P2] 的對應**：[P2] p.803 由 Eq.(46)–(48)（自相關＋Khinchin 定理）導出「jitter 由
  phase spectrum 積分」的 Eq.(49)，路線與本頁路 A 完全相同（該處並註明大 offset 時
  $S_\phi$ 可用 $\mathcal{L}$ 近似——即上面對照表的第三欄）。
  （**v5 已對照 [P2] p.803 原始 PDF 渲染逐字核實**：Eq.(48) $R_\phi(\tau)=\int_{-\infty}^{\infty}S_\phi(f)e^{j2\pi f\tau}df$——**雙邊**譜；
  Eq.(49) $\sigma^2_{\Delta\phi}=\dfrac{8}{\omega_0^2}\int_0^\infty S_\phi(f)\sin^2(\pi f\tau)\,df$。
  以 $S_{os}=2S_{ds}$ 換算，$\tfrac{8}{\omega_0^2}S_{ds}\sin^2=\tfrac{1}{\omega_0^2}S_{os}\cdot4\sin^2$——**與本頁單邊 $4\sin^2$ 核精確等價**，
  正是上面「文獻 $8$ 係數版之 $S_\phi$ 為雙邊譜」推測的逐字證實。）
- **dimension check**：核無因次；其餘同核 (a) ✓。

### 核 (c)：cycle-to-cycle——二階差分，核 $16\sin^4(\pi fT)$

第 2 步的 $C_k$ 是「一階差分再差分一次」，濾波器是兩個一階差分串接：

$$
H_{c2c}(f)=\big(e^{-j2\pi fT}-1\big)^2\quad\Longrightarrow\quad
\lvert H_{c2c}(f)\rvert^2=\big\lvert e^{-j2\pi fT}-1\big\rvert^4=\big[4\sin^2(\pi fT)\big]^2=16\sin^4(\pi fT),
$$

$$
\boxed{\ \sigma_{c2c}^2=\frac{1}{\omega_0^2}\int_0^\infty S_\phi(f)\,16\sin^4(\pi fT)\,df\ }
$$

- **核的形狀**：$f\to0$ 像 $(2\pi fT)^4\propto f^4$（二階高通，最不吃 close-in），峰值 16
  在 $f=1/(2T)=f_0/2$，振盪平均值 6。
- **16 從哪來**：$4^2$。一次差分貢獻一個 4（其中各含一個「差的變異數」的 2 與一個半角
  公式的 2），平方即 16。**每個 2 都有名有姓**。

## 第 4 步：白噪 FM 封閉式——與 [P2] Eq.(8)/(11)/(12) 精確互鎖（本頁 punchline）

### 4.1 需要的一個標準積分（不跳步）

先求 $\displaystyle\int_0^\infty\frac{1-\cos(bx)}{x^2}dx$（$b\gt0$）。分部積分
（$u=1-\cos bx$、$dv=x^{-2}dx$、$v=-1/x$）：

$$
\int_0^\infty\frac{1-\cos bx}{x^2}dx
=\underbrace{\Big[-\frac{1-\cos bx}{x}\Big]_0^\infty}_{=0\ (\text{兩端皆}0)}
+\,b\int_0^\infty\frac{\sin bx}{x}dx
=b\cdot\frac{\pi}{2},
$$

末步用 Dirichlet 積分 $\int_0^\infty\frac{\sin x}{x}dx=\frac{\pi}{2}$（標準結果）。
邊界項：$x\to0$ 時 $1-\cos bx\approx b^2x^2/2$，比值 $\to0$；$x\to\infty$ 時分子有界、
$1/x\to0$ ✓。由 $\sin^2(ax)=\tfrac12\big[1-\cos(2ax)\big]$ 得

$$
\int_0^\infty\frac{\sin^2(ax)}{x^2}dx=\frac12\cdot\frac{\pi(2a)}{2}=\frac{\pi a}{2},
\qquad
\int_0^\infty\frac{\sin^4(ax)}{x^2}dx=\frac{\pi a}{4},
$$

第二式用 $\sin^4 u=\tfrac18\big[4(1-\cos2u)-(1-\cos4u)\big]$（把 $\cos^2$ 再降一次幂展開
即得）：$\tfrac18\big[4\cdot\tfrac{\pi(2a)}{2}-\tfrac{\pi(4a)}{2}\big]=\tfrac18(4\pi a-2\pi a)=\tfrac{\pi a}{4}$ ✓。

### 4.2 白噪 FM 的 $S_\phi$ 與 $\kappa$（從 ISF 來）

白噪電流（單邊 PSD $S_i$，$\text{A}^2/\text{Hz}$）經 ISF 加權積分成相位（[P1] Eq.(11), p.182）：

$$
\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau .
$$

單邊 PSD $S_i$ 的白噪自相關是 $R_i(\tau)=\tfrac{S_i}{2}\delta(\tau)$（雙邊平坦位準
$S_i/2$；這個 $\tfrac12$ 是單邊↔雙邊記帳，見
[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)）。相隔 $\Delta t$
的相位增量變異數（$\Delta t$ 為整數個週期時 $\int\Gamma^2$ 精確等於 $\Gamma_{rms}^2\Delta t$）：

$$
\operatorname{Var}\big[\Delta\phi(\Delta t)\big]
=\frac{1}{q_{max}^2}\cdot\frac{S_i}{2}\int_t^{t+\Delta t}\Gamma^2(\omega_0\tau)\,d\tau
=\underbrace{\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{2}}_{\equiv\ \kappa^2}\ \Delta t .
$$

$$
\boxed{\ \sigma_{\Delta\phi}=\kappa\sqrt{\Delta t},\qquad
\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\frac12\cdot\frac{\overline{i_n^2}}{\Delta f}}\ }
\qquad(\text{[P2] Eq.(8), p.792；Eq.(11)/(12), p.793，已核實})
$$

- **單位（重要、常被搞混）**：這裡的 $\kappa$ 是**相位版**，
  $[\kappa]=\text{rad}/\sqrt{\text{s}}$：$\sqrt{\text{A}^2\cdot\text{s}}/\text{C}=\text{A}\sqrt{\text{s}}/(\text{A}\cdot\text{s})=1/\sqrt{\text{s}}$（rad 無因次記帳）✓。
  裡面**沒有 $\omega_0$**。**時間版**由 [P2] Eq.(10), p.793 的
  $\sigma_{\Delta\phi}=2\pi\,\sigma_{\Delta t}/T=\omega_0\sigma_{\Delta t}$ 換算：
  $\sigma_{\Delta t}=(\kappa/\omega_0)\sqrt{\Delta t}$，$[\kappa/\omega_0]=\sqrt{\text{s}}$
  ——[notation](/00_overview/notation) 表裡單位 $\sqrt{\text{s}}$ 的 $\kappa$ 指的是時間版。
  兩版差一個 $\omega_0$，混用會差 10 個數量級，務必先看單位。
- 而這個隨機漫步的單邊相位譜正是（[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 的時域乾淨版結果）

$$
S_\phi(f)=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{(2\pi f)^2}=\frac{2\kappa^2}{(2\pi f)^2}
\qquad[\text{rad}^2/\text{Hz}],
$$

  這裡的 2 是「隨機漫步 $\operatorname{Var}=\kappa^2 t$ ↔ 單邊譜 $2\kappa^2/\Delta\omega^2$」
  的標準對應（雙邊平坦位準 $\kappa^2$、單邊乘 2）。對到 SSB：時域 $/2$ 慣例
  $\mathcal{L}=\tfrac12S_\phi=\kappa^2/\Delta\omega^2$ 給 $-145.0$ dBc/Hz@1 MHz、
  [P1] Eq.(21), p.185 的 $/4$ 慣例給 $-148.0$ dBc/Hz（canonical 例 B；lab_24 兩個都印出，
  見第 8 節標記）。

### 4.3 把 $S_\phi=2\kappa^2/(2\pi f)^2$ 代入核 (b)——punchline

$$
\begin{aligned}
\sigma_{\Delta\phi}^2(N)
&=\int_0^\infty \frac{2\kappa^2}{(2\pi f)^2}\cdot4\sin^2(\pi fNT)\,df
=\frac{2\kappa^2}{\pi^2}\int_0^\infty\frac{\sin^2(\pi NT\,f)}{f^2}\,df\\[2pt]
&=\frac{2\kappa^2}{\pi^2}\cdot\frac{\pi\cdot(\pi NT)}{2}
=\boxed{\ \kappa^2\,NT\ }.
\end{aligned}
$$

（第二步用 4.1 的 $\int_0^\infty\sin^2(ax)/x^2\,dx=\pi a/2$，$a=\pi NT$。）

**一個係數都不差**：頻域核積分給出的 N-period 相位 jitter **精確等於** [P2] Eq.(8)
的隨機漫步 $\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$（取 $\Delta t=NT$），
$\kappa$ 就是 Eq.(11)/(12) 那顆。這就是「核圖像」與 [P2] 時域圖像的閉環——
如果前置常數用了 $2/\omega_0^2$（把單邊譜當雙邊用），這裡會多出 $\sqrt2$，
和 [P2] 對不上；Monte-Carlo 也站在 $\kappa^2NT$ 這邊（第 8 節，比值 0.999–1.001）。

時間版（除 $\omega_0^2$）：

$$
\sigma_P(N)=\frac{\kappa\sqrt{NT}}{\omega_0},\qquad
\sigma_P(1)=\frac{\kappa\sqrt{T}}{\omega_0}.
$$

若用譜係數寫（$S_\phi=b_2/f^2$，$b_2=\kappa^2/(2\pi^2)$，單位 $\text{rad}^2\cdot\text{Hz}$）：

$$
\sigma_P^2(N)=\frac{b_2\,N\,T^3}{2}\qquad[\text{s}^2].
$$

- **dimension check**：$\kappa^2NT=(\text{rad}^2/\text{s})\cdot\text{s}=\text{rad}^2$ ✓；
  $b_2NT^3=(\text{rad}^2\cdot\text{Hz})\cdot\text{s}^3=\text{rad}^2\cdot\text{s}^2$，
  rad 無因次化後得 $\text{s}^2$ ✓（$1/\omega_0^2$ 已用 $1/f_0^2=T^2$ 吸收進去：
  $(2\pi NT)^2$ 分子的 $(2\pi)^2$ 和 $\omega_0^2$ 的 $(2\pi)^2$ 對消）。
- **canonical 數值**（代表值 $\Gamma_{rms}=0.5$、$q_{max}=1$ pC、$S_i=10^{-24}$ A²/Hz、
  $f_0=5$ GHz）：$\kappa=0.354$ rad/$\sqrt{\text{s}}$、$\kappa^2=0.125$ rad²/s
  （真 LC 的 $\Gamma_{rms}=1/\sqrt2$ 時剛好翻倍成 $0.25$，差別只是 $\Gamma_{rms}^2$ 的包裝）。
  $\sigma_{\Delta\phi}(1T)=\sqrt{0.125\times2\times10^{-10}}=5.00\ \mu\text{rad}$、
  $\sigma_P(1)=5.00\times10^{-6}/(2\pi\times5\times10^9)=0.159$ fs（週期的 0.8 ppm）；
  $N=10^4$ 時 $\sigma_{\Delta\phi}=0.50$ mrad、$\sigma_P=15.9$ fs——$\sqrt N$ 成長。

<NumericQuiz
  prompt="先自己算：canonical 振盪器（κ²=0.125 rad²/s，T=200 ps，f₀=5 GHz）的 period jitter σ_P(1) = ？（以 fs 作答）"
  answer={0.159}
  tol={0.02}
  unit="fs"
  hint="先算 σ_Δφ(1T)=√(κ²T)（rad），再除以 ω₀=2πf₀ 換成時間。"
  solutionNote="σ_Δφ(1T)=√(0.125×2×10⁻¹⁰)=5.00 µrad → σ_P(1)=5.00×10⁻⁶/(2π×5×10⁹)≈0.159 fs（與 lab_24 MC 比值 0.999 吻合）。"
/>

### 4.4 cycle-to-cycle 封閉式與 $\sqrt2$ 關係

把同一條 $S_\phi$ 代入核 (c)，用 4.1 的 $\int\sin^4(ax)/x^2\,dx=\pi a/4$（$a=\pi T$）：

$$
\sigma_{c2c,\phi}^2=\frac{2\kappa^2}{\pi^2}\cdot4\int_0^\infty\frac{\sin^4(\pi Tf)}{f^2}df
=\frac{8\kappa^2}{\pi^2}\cdot\frac{\pi^2T}{4}=2\kappa^2T
\quad\Longrightarrow\quad
\boxed{\ \sigma_{c2c}=\sqrt2\,\sigma_P(1)\ }
$$

**物理意義**：白噪 FM 下相鄰兩個週期的長度偏差是**獨立**的（不重疊的隨機漫步增量），
獨立差的變異數相加，所以恰好 $\sqrt2$。這與 [P2] p.803「based on (8)」導出 rms
cycle-to-cycle jitter 的 Eq.(51) 是同一件事（該處同樣限定 phase noise 在 $1/f^2$ 區域）。
若譜不是純 $1/f^2$（例如 flicker 主導），相鄰週期**相關**，$\sqrt2$ 不成立——這是判斷
量測是否落在白噪區的快速體檢。

<NumericQuiz
  prompt="先自己算：canonical 振盪器 σ_P(1)=0.159 fs，白噪限定下 cycle-to-cycle σ_c2c = ？（以 fs 作答）"
  answer={0.225}
  tol={0.02}
  unit="fs"
  hint="σ_c2c = √2 × σ_P(1)（相鄰週期長度偏差獨立，方差相加）。"
  solutionNote="σ_c2c = √2×0.159 ≈ 0.225 fs（與 lab_24 MC 0.2248 fs、理論 0.2251 fs 吻合，ratio 0.999）。"
/>

### 4.5 實用推論：從 $\mathcal{L}$ 一步讀出 $\kappa$（注意是哪個慣例的 $\mathcal{L}$）

在 $1/f^2$ 區域，時域 $/2$ 慣例下 $\mathcal{L}_{\text{lin}}(\Delta f)=\kappa^2/(2\pi\Delta f)^2$，反解：

$$
\kappa=2\pi\,\Delta f\sqrt{\mathcal{L}_{\text{lin}}(\Delta f)}\quad[\text{rad}/\sqrt{\text{s}}],
\qquad
\frac{\kappa}{\omega_0}=\frac{\Delta f}{f_0}\sqrt{\mathcal{L}_{\text{lin}}(\Delta f)}\quad[\sqrt{\text{s}}].
$$

這對應 [P2] Eq.(50), p.803（白噪特例：由 $1/f^2$ 區的 $\mathcal{L}$ 讀出 $\kappa$；
原式字面已於上方 v5 核實註記逐字轉錄）。**factor-of-2 陷阱**：這條式吃的是
$\mathcal{L}=\tfrac12S_\phi$（時域 $/2$）慣例的數字——canonical 振盪器要代 $-145$ dBc/Hz
得 $\kappa=0.354$ ✓；若誤代 [P1] Eq.(21) $/4$ 慣例的 $-148$，會少 $\sqrt2$（得 0.25）。
同一顆振盪器、同一條譜，**先問清楚 dBc/Hz 是哪種記帳再代公式**。

- **dimension check**：$\text{Hz}\times\sqrt{1/\text{Hz}}=\sqrt{\text{Hz}}=1/\sqrt{\text{s}}$ ✓。

## 論文原生推導：[P2] Appendix A（Eq.(11) 的紙上出處，逐字轉錄＋逐因子對帳）

第 3、4 步是本站自己的推導；其實 [P2] 在 **Appendix A "Relationship Between
Jitter and Phase Noise"** 把同一件事**用兩條路各走了一遍**——它**起於 p.802 右欄、
收於 p.803 左欄**（p.803 右欄起是 Appendix B 的非對稱邊沿推導，別搞混）：
Eq.(40)–(44) 是白噪時域路（＝本頁 4.2）、Eq.(45)–(49) 是自相關＋Khinchin 路
（＝本頁路 A），末尾附兩條實用推論 Eq.(50)/(51)（＝本頁 4.5 與 4.4 的一週期版）。
主文 p.793 明說 Eq.(11) 的出處就是這裡（"As shown in Appendix A, for
$\Delta T\gg T$ or $\Delta T=nT$…"，緊接著給出
$\sigma_{\Delta\phi}^2=\frac{\Gamma_{rms}^2\cdot\overline{i_n^2}/\Delta f}{2q_{max}^2}\Delta T$）。
以下逐字轉錄自 p.802–803 的 PDF 渲染頁（放大核對），照排如實——包括印刷滑失。

### A.1 白噪時域路：Eq.(40)–(44)（p.802 右欄）

phase jitter 的定義（原文："The phase jitter is"）：

$$
\sigma_{\Delta\phi}^2=E\{\Delta\phi^2\}=E\big\{[\phi(t+\Delta T)-\phi(t)]^2\big\}
\qquad(\text{[P2] Eq.(40), p.802})
$$

其中（把 [P1] 的 ISF 相位積分限截到觀測窗）：

$$
\Delta\phi=\int_0^{\Delta T}\frac{\Gamma(\omega_0\tau)}{q_{max}}\,i(\tau)\,d\tau.
\qquad(\text{Eq.(41)})
$$

平方、期望與積分交換：

$$
\sigma_{\Delta\phi}^2=\frac{1}{q_{max}^2}\int_0^{\Delta T}\!\!\int_0^{\Delta T}
\Gamma(\omega_0\tau_1)\,\Gamma(\omega_0\tau_2)\cdot E[i(\tau_1)i(\tau_2)]\,d\tau_1\,d\tau_2.
\qquad(\text{Eq.(42)})
$$

白噪電流的自相關原文明寫為
$R_{ii}(t_1,t_2)=(1/2)\big(\overline{i_n^2}/\Delta f\big)\delta(t_1-t_2)$，
代入後雙重積分塌成單重：

$$
\sigma_{\Delta\phi}^2=\frac12\,\frac{\overline{i_n^2}/\Delta f}{q_{max}^2}
\int_0^{\Delta T}\Gamma^2(\omega_0\tau)\,d\tau
\qquad(\text{Eq.(43)})
$$

$$
\sigma_{\Delta\phi}^2=\frac12\,\frac{\overline{i_n^2}/\Delta f}{q_{max}^2}\,
\Gamma_{rms}^2\,\Delta T
\quad\text{for}\quad\Delta T\gg T\ \text{or}\ \Delta T=mT.
\qquad(\text{Eq.(44)})
$$

**Eq.(44) 字面就是主文 Eq.(11)**（p.793，僅排版不同），其係數
$\tfrac12\,(\overline{i_n^2}/\Delta f)\,\Gamma_{rms}^2/q_{max}^2$ 正是本頁 4.2 的
$\kappa^2$（$S_i\equiv\overline{i_n^2}/\Delta f$）——論文的時域路與 4.2
**一個符號都不差**。

### A.2 自相關＋Khinchin 路：Eq.(45)–(51)（p.803 左欄）

論文接著換第二條路——開頭明說 timing jitter 是時間不確定度的標準差：

$$
\sigma_{\Delta\phi}^2=\frac{1}{\omega_0^2}E\big\{[\phi(t+\Delta T)-\phi(t)]^2\big\}
=\frac{E[\phi^2(t)]}{\omega_0^2}+\frac{[\phi^2(t+\Delta T)]}{\omega_0^2}
-\frac{E[\phi(t)\phi(t+\Delta T)]}{\omega_0^2}
\qquad(\text{Eq.(45)，照排如此})
$$

$$
R_\phi(\tau)=E[\phi(t)\phi(t+\Delta T)]
\qquad(\text{Eq.(46)，照排如此})
$$

$$
\sigma_{\Delta\phi}^2=\frac{2}{\omega_0^2}\big[R_\phi(0)-R_\phi(\Delta T)\big].
\qquad(\text{Eq.(47)})
$$

$$
R_\phi(\tau)=\int_{-\infty}^{\infty}S_\phi(f)\,e^{j2\pi f\tau}\,df
\qquad(\text{Eq.(48)，Khinchin 定理})
$$

$$
\sigma_{\Delta\phi}^2=\frac{8}{\omega_0^2}\int_0^{\infty}S_\phi(f)\sin^2(\pi f\tau)\,df.
\qquad(\text{Eq.(49)})
$$

以及兩條白噪（$1/f^2$ 區）限定的實用推論——Eq.(50) 由主文 (6)+(12) 組合而得、
Eq.(51) 再 "based on (8)"（即 $\sigma=\kappa\sqrt T$）接上；**都不是**由積分 (49) 而得：

$$
\kappa=\frac{\Delta f}{f_0}\cdot10^{-\mathcal{L}\{\Delta f\}/20}
\qquad(\text{Eq.(50)})
$$

$$
\sigma_{CTC}=\frac{f}{f_0^{1.5}}\cdot10^{-\mathcal{L}\{\Delta f\}/20}.
\qquad(\text{Eq.(51)，照排如此})
$$

**照排聲明（渲染放大核對；符號重載與排印滑失都如實列出）**：

1. **$\sigma_{\Delta\phi}^2$ 一符兩用**：Eq.(40)–(44) 的 LHS 是**相位** jitter（rad²）；
   Eq.(45) 起 LHS 印的還是 $\sigma_{\Delta\phi}^2$，卻多了 $1/\omega_0^2$、原文也明說是
   timing jitter——實為 $\sigma_{\Delta T}^2=\sigma_{\Delta\phi}^2/\omega_0^2$（s²，
   即 Eq.(10) 的換算）。本頁把 $\sigma_{\Delta\phi}$ 與 $\sigma_{\Delta t}$ 分開命名，
   就是為了拆掉這顆地雷。
2. **Eq.(45) 展開行漏了兩個記號**：中項漏印 $E$、交叉項漏印係數 2（$[a-b]^2$ 的
   交叉項是 $2ab$；平穩下前兩項合為 $2R_\phi(0)$，要落到 Eq.(47) 交叉項非
   $2R_\phi(\Delta T)$ 不可）。Eq.(47) 本身印刷正確——滑失沒有傳染下去。
3. **$\tau$ 與 $\Delta T$ 混用**：Eq.(46) LHS 寫 $R_\phi(\tau)$、RHS 用 $\Delta T$；
   Eq.(49) 的核寫 $\sin^2(\pi f\tau)$，這個 $\tau$ 就是延遲 $\Delta T$。
4. **Eq.(51) 分子印作 $f$**：由 Eq.(50) 的 $\kappa$（時間版）乘 $\sqrt T=f_0^{-0.5}$
   得 $\sigma_{CTC}=\kappa\sqrt T$，分子應是 offset 頻率 $\Delta f$——印刷把
   $\Delta$ 吃掉了（「對應的 paper / 公式」節的轉錄已同步標注）。
5. Eq.(48) 的積分限 $\int_{-\infty}^{\infty}$ 宣告了此處 $S_\phi$ 是**雙邊**譜——
   全文唯一洩漏慣例的地方，Eq.(49) 的 8 因此內建一顆記帳的 2（見下表）。

### A.3 逐步對照：論文的兩條路 ↔ 本頁的推導

| [P2] | 那一步在做什麼 | 本頁對應 | 因子對帳（對第 0 步表） |
|---|---|---|---|
| Eq.(40) | 定義相位 jitter | 第 2 步的一階差分 $P_k(N)$（相位語言） | — |
| Eq.(41) | $\Delta\phi$＝ISF 加權的窗積分 | 4.2 引用的 [P1] Eq.(11)（積分限改成窗） | — |
| Eq.(42) | 平方展開成雙重積分＋$E[i(\tau_1)i(\tau_2)]$ | 4.2 第一行（代入自相關前的一般式） | 對任意（非白）自相關都成立 |
| Eq.(43) | 白噪 $R_{ii}=\tfrac12(\overline{i_n^2}/\Delta f)\delta$ 塌成單重積分 | 4.2 的 $R_i(\tau)=\tfrac{S_i}{2}\delta(\tau)$ | **同一顆 $\tfrac12$**：單邊 PSD ↔ 雙邊平坦位準 |
| Eq.(44) | $\int\Gamma^2\to\Gamma_{rms}^2\Delta T$（$\Delta T\gg T$ 或 $=mT$） | 4.2 括號註「整數週期精確」＋4.3 的 $\kappa^2NT$ | Eq.(44)＝主文 Eq.(11)＝$\kappa^2\Delta T$ |
| Eq.(45)–(47) | WSS 展開：差的變異數 $=2[R_\phi(0)-R_\phi(\Delta T)]$ | 路 A 第 1 步（同式） | **Eq.(47) 的 2**＝「差的變異數」的 2 |
| Eq.(48) | Khinchin 定理（雙邊譜、$\int_{-\infty}^{\infty}$） | 路 A 第 2 步（單邊 cos 版） | $S_\phi^{DS}=S_\phi/2$ |
| Eq.(49) | $\dfrac{8}{\omega_0^2}\displaystyle\int_0^\infty S_\phi^{DS}\sin^2(\pi f\tau)\,df$ | 核 (b) 的 $\dfrac{1}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\,4\sin^2 df$ | **8＝2（雙邊→單邊）×4（差分核）**，$1/\omega_0^2$＝相位→時間——第 0 步表第二欄字面重現 |
| Eq.(50) | 由主文 (6)+(12) 讀出 $\kappa\leftarrow\mathcal{L}$ | 4.5（負指數＝「低於載波 dB 數」讀法，v5 註） | 吃 $/2$ 慣例的 $\mathcal{L}$ |
| Eq.(51) | $\sigma_{CTC}=\kappa\sqrt T$（一週期版） | 4.4 末註（相鄰差定義再乘 $\sqrt2$） | 印刷分子 $f$ 應讀 $\Delta f$ |

### A.4 誰跳過了什麼（兩個方向都記帳）

**[P2] 跳過、本頁補上的**：

- **平穩性的 rigor gap**：Eq.(45)–(47) 需要 $R_\phi(0)$ 有限；自由振盪器的 $\phi$
  是隨機漫步，$R_\phi(0)$ 發散（正是本頁路 A 開頭的坦白）。差
  $R_\phi(0)-R_\phi(\Delta T)$ 有限、結論不受影響，但嚴格化要走本頁**路 B**
  （只要求 $\nu=\dot\phi$ 平穩）——論文沒有處理這一步。
- **慣例不聲明**：$S_\phi$ 單邊還是雙邊，全文沒有一句話；只有 Eq.(48) 的積分限
  洩底。本頁第 0 步的三欄表就是把這件事攤開（v5 正是靠這個積分限反推，才把
  「文獻 8 係數版」對上單邊 $4\sin^2$ 核）。
- **兩條路在論文裡沒有互鎖**：Eq.(44) 停在時域、Eq.(49) 停在頻域；論文從未把
  白噪譜代入 (49) 驗證會回到 (44)。本頁 4.1 的
  $\int_0^\infty\sin^2(ax)/x^2\,dx=\pi a/2$ ＋ 4.3 的代入就是補上的閉環
  （下方 code 把兩路各算一遍，同一個數）。
- flicker $1/f^3$ 的時域封閉式（第 5 步的 log 式）與 c2c 的 $16\sin^4$ 核
  （核 (c)；Eq.(51) 只是一週期版）論文都沒有給。

**本頁帶過、[P2] 寫全的**：

- **Eq.(42) 的一般雙重積分**：本頁 4.2 直接跳「白噪 δ 相關 ⇒ 單重積分」；論文把
  $\Gamma(\omega_0\tau_1)\Gamma(\omega_0\tau_2)\,E[i(\tau_1)i(\tau_2)]$ 的一般式
  明寫出來——那是任何色噪自相關都能接的起點，白噪只是特例。
- **成立條件印在式子裡**：Eq.(44) 的 "for $\Delta T\gg T$ or $\Delta T=mT$" 把
  「$\int\Gamma^2$ 換 $\Gamma_{rms}^2\Delta T$ 何時精確」印在等號旁；本頁 4.2 只在
  括號裡帶過。短或非整數 $\Delta T$ 時有 $O(T/\Delta T)$ 級的 $\Gamma^2$ 漣漪殘差。

### A.5 兩路重演白噪 FM 變異數（# -> 可驗證）

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal

F0, T = 5e9, 2e-10
W0 = 2 * np.pi * F0
QMAX, SI, GRMS = 1e-12, 1e-24, 0.5      # canonical 參數
N = 100
DT = N * T                              # ΔT = mT（Eq.(44) 的成立條件）

# 路線一：[P2] Appendix A 時域自相關路——Eq.(42) 代 R_ii=(S_i/2)δ 塌成 Eq.(43)
tau = np.linspace(0.0, DT, 200 * N + 1)
gam = np.sqrt(2.0) * GRMS * gamma_lc_ideal(W0 * tau)     # Γrms=0.5 的 LC 形 ISF
var_43 = 0.5 * SI / QMAX**2 * np.trapezoid(gam**2, tau)  # Eq.(43) 數值積分
var_44 = 0.5 * SI / QMAX**2 * GRMS**2 * DT               # Eq.(44) ＝主文 Eq.(11)
print(f"{var_43:.4e}")            # -> 2.5000e-09 rad^2（Eq.(43)，σ²_Δφ @ N=100）
print(f"{var_43/var_44:.4f}")     # -> 1.0000（ΔT=mT 時 ∫Γ² 精確 = Γrms²ΔT）

# 路線二：本頁核路——單邊 S_φ=2κ²/(2πf)² 乘 4sin²(πfΔT) 核
kappa2 = GRMS**2 / QMAX**2 * SI / 2                      # κ²=Γrms²S_i/(2q_max²)
print(f"{kappa2:.4f}")            # -> 0.1250 rad^2/s（與 Eq.(44) 前置常數同一顆）
x = np.linspace(1e-8, 1e4, 4_000_001)                    # x = fΔT
core = np.trapezoid(np.sin(np.pi * x)**2 / x**2, x) + 0.5 / x[-1]  # 尾巴 sin²→1/2
var_kernel = 2 * kappa2 * DT / np.pi**2 * core           # = κ²ΔT（4.3 節解析值）
print(f"{var_kernel/var_43:.4f}") # -> 1.0000（頻域核 = Appendix A 自相關路，同一數）

# 對帳 [P2] Eq.(49)：8/ω₀² × 雙邊譜 S_φ^DS=κ²/(2πf)²，LHS 是時間版變異數
var_49 = 8 / W0**2 * (kappa2 * DT / 4 / np.pi**2) * core
print(f"{var_49/(kappa2*DT/W0**2):.4f}")   # -> 1.0000（8 = 2(雙邊→單邊)×4(核)）
print(f"{np.sqrt(var_49)*1e15:.2f} fs")    # -> 1.59 fs（σ_ΔT @ N=100 = √100×0.159 fs）
```

前兩個 print 走 [P2] Eq.(43)→(44)（時域自相關路），其餘四個走本頁核 (b) 與
Eq.(49) 的雙邊記帳版——**同一顆振盪器、兩條路、同一個數
$\kappa^2\Delta T=2.5\times10^{-9}\ \text{rad}^2$**。Appendix A 與本頁第 3/4 步
是同一個定理的兩份證明；差別只在論文把慣例藏在積分限裡、本頁把它印在第 0 步。

## 第 5 步：flicker（$1/f^3$）的封閉式——log 項與它的誠實條件

flicker FM 的相位譜是 $S_\phi(f)=b_3/f^3$（$b_3$ 單位 $\text{rad}^2\cdot\text{Hz}^2$；
來源見 [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)）。
核 (b) 的積分在 $f\to0$ 是 $\int(b_3/f^3)(2\pi fNT)^2df\propto\int df/f$——**對數發散**，
所以必須誠實引入低頻截止 $f_l$（物理上：量測時長 $T_{obs}$ 給 $f_l\sim1/T_{obs}$，
或 PLL 把更低頻拉住）。要算的是

$$
\sigma_{\Delta\phi}^2(N)=4b_3\int_{f_l}^{\infty}\frac{\sin^2(af)}{f^3}\,df,\qquad a=\pi NT .
$$

**第 1 步（半角）**：$\sin^2(af)=\tfrac12[1-\cos(2af)]$，記 $b=2a$、
$J(b,f_l)=\int_{f_l}^\infty\frac{1-\cos(bf)}{f^3}df$，則積分 $=\tfrac12 J$。

**第 2 步（分部一次，$v=-1/(2f^2)$）**：

$$
J=\frac{1-\cos(bf_l)}{2f_l^2}+\frac{b}{2}\int_{f_l}^\infty\frac{\sin(bf)}{f^2}\,df .
$$

**第 3 步（再分部一次，$v=-1/f$）**：

$$
\int_{f_l}^\infty\frac{\sin(bf)}{f^2}df=\frac{\sin(bf_l)}{f_l}+b\int_{f_l}^\infty\frac{\cos(bf)}{f}df
=\frac{\sin(bf_l)}{f_l}-b\,\mathrm{Ci}(bf_l),
$$

其中 $\mathrm{Ci}(z)=-\int_z^\infty\frac{\cos u}{u}du$ 是餘弦積分函數。

**第 4 步（小引數展開，$bf_l\ll1$）**：$1-\cos(bf_l)\to\tfrac{b^2f_l^2}{2}$、
$\sin(bf_l)/f_l\to b$、$\mathrm{Ci}(z)=\gamma+\ln z+O(z^2)$（$\gamma=0.5772\ldots$ 為
Euler–Mascheroni 常數；Ci 級數為標準結果——M. Abramowitz and I. A. Stegun,
*Handbook of Mathematical Functions*, Dover, 1964, Eq. 5.2.16（外部文獻，非本站 5 篇 PDF））：

$$
J\to\frac{b^2}{4}+\frac{b^2}{2}\big[1-\gamma-\ln(bf_l)\big]
=\frac{b^2}{2}\Big[\frac32-\gamma-\ln(bf_l)\Big].
$$

**第 5 步（組回，$b=2a=2\pi NT$）**：

$$
\boxed{\ \sigma_{\Delta\phi}^2(N)=4\pi^2\,b_3\,(NT)^2\Big[\tfrac32-\gamma-\ln\big(2\pi NT f_l\big)\Big]\ }
\qquad
\sigma_P^2(N)=\frac{\sigma_{\Delta\phi}^2(N)}{\omega_0^2}=b_3\,N^2T^4\Big[\tfrac32-\gamma-\ln\big(2\pi NTf_l\big)\Big].
$$

- **dimension check**：$b_3(NT)^2=(\text{rad}^2\text{Hz}^2)(\text{s}^2)=\text{rad}^2$ ✓；
  log 引數 $2\pi NTf_l$ 是 $\text{s}\times\text{Hz}$，無因次 ✓。
- **成立條件**：$2\pi NTf_l\ll1$（展開到 $O((bf_l)^2)$）；且 $1/f^3$ 要在 $f_l$ 以上主導。
- **log-band caveat（誠實聲明）**：這個數字**對數地依賴 $f_l$**，也就是依賴你量多久——
  flicker 主導的 period jitter **沒有唯一值**，report 時必須附 $f_l$（或量測時長）。
  例：$b_3=1\ \text{rad}^2\text{Hz}^2$、$f_l=100$ Hz、$N=1$、$T=200$ ps：
  $2\pi NTf_l=1.26\times10^{-7}$，括號 $=0.9228+15.89=16.81$，
  $\sigma_{\Delta\phi}^2=1.579\times10^{-18}\times16.81=2.65\times10^{-17}\ \text{rad}^2$。
  把 $f_l$ 改 10 倍只讓括號變 $16.81\mp2.30$（$\mp14\%$ 變異數）——log 的遲鈍是好消息，
  但不是零。
- **$N$ 的成長律**：$\sigma_{\Delta\phi}(N)\propto N\sqrt{\ln(\cdot)}$——**幾乎線性**
  （lab_24 印出 $\sigma(N{=}10)/\sigma(N{=}1)=9.29$，白噪 FM 是 $\sqrt{10}=3.16$）。
  這正是 [P2] Eq.(9), p.792 說的：相關（低頻/flicker）雜訊讓 jitter $\propto\Delta t$、
  白噪讓 jitter $\propto\sqrt{\Delta t}$，log-log 圖上斜率 1 與 1/2 的兩段（[P2] Fig. 4）。
  時域量測 $\kappa$ 的實務（斜率分段擬合）可另見 J. A. McNeill, "Jitter in ring
  oscillators," IEEE J. Solid-State Circuits, vol. 32, no. 6, pp. 870–879, Jun. 1997
  （外部文獻，非本站 5 篇 PDF）。

## 第 5b 步：兩段式成長——[P2] Fig.16 的 $\sigma(\Delta t)=\sqrt{\kappa^2\Delta t+\zeta^2\Delta t^2}$

第 4 步（白噪 FM：$\sigma^2=\kappa^2\Delta t$，斜率 1/2）與第 5 步（flicker FM：
$\sigma^2\sim\zeta^2\Delta t^2$，斜率 $\approx1$）在真實振盪器裡**同時存在**。
[P2] 把這件事直接「量」給你看——這就是著名的 Fig. 16 兩段式 log-log 圖。

### 5b.1 [P2] 原文逐字（已對照 PDF 渲染頁核實）

- **Fig. 16 caption（p.802）**："RMS jitter versus measurement interval for the
  four-stage, 2.8-GHz differential ring oscillator (oscillator number 12)."
  縱軸 "Rms jitter (second)"、橫軸 "$\Delta T$ (second)"；圖上兩條漸近線分別標註
  $\kappa=6.18\text{e-}9\ \text{sec}^{0.5}$ 與 $\zeta=2.5\text{e}5$。
- **兩個比例常數的定義（p.792）**：Eq.(8) $\sigma_{\Delta T}=\kappa\sqrt{\Delta T}$，
  "where $\kappa$ is a proportionality constant determined by circuit parameters"；
  Eq.(9) $\sigma_{\Delta T}=\zeta\,\Delta T$，"where $\zeta$ is another
  proportionality constant"。Eq.(9) 的前提是雜訊源**完全相關**——原文："when the
  noise sources are totally correlated with one another … the standard deviations
  rather than the variances add"；substrate/supply 雜訊與低頻 1/f 雜訊屬於此類。
  同頁結論："a log–log plot of the timing jitter $\sigma_{\Delta T}$ versus the
  measurement delay $\Delta T$ for an open-loop oscillator will demonstrate regions
  with slopes of 1/2 and 1, as shown in Fig. 4."
- **量測對帳（p.801）**："The best fit $\kappa$ for the data shown in Fig. 16 is
  $\kappa=6.18\times10^{-9}\sqrt{s}$. Equations (12) and (35) result in
  $\kappa=5.95\times10^{-9}\sqrt{s}$ and $\kappa=6.07\times10^{-9}\sqrt{s}$,
  respectively."——ISF 理論預測與量測差 2–4%，是 [P2] 全篇最漂亮的閉環之一。
  斜率 1 段的歸因也在同頁："The region of the jitter plot with the slope of one
  can be attributed to the $1/f$ noise of the devices, as discussed at the end of
  Section VI."（Section VI 結尾，pp.797–798："Low-frequency noise can also result
  in correlation between uncertainties introduced during different cycles … the
  uncertainties add up in amplitude rather than power, resulting in a region with
  a slope of one … even in the absence of external noise sources"。）
- **印刷勘誤（誠實聲明）**：圖上 $\zeta$ 印作「2.5e5」。但由 Eq.(9)
  $\sigma=\zeta\Delta T$（秒＝$\zeta\times$秒）知 $\zeta$ **無因次**，且該條
  slope-1 擬合線通過（$10^{-6}$ s, $\approx2\times10^{-11}$ s），
  $\zeta=\sigma/\Delta T\approx2.5\times10^{-5}$——印刷指數少了負號。
  本頁一律用 $\zeta=2.5\times10^{-5}$。（順帶 dimension check：$\kappa$ 標成
  $\text{sec}^{0.5}$ ✓，$\text{s}/\sqrt{\text{s}}=\sqrt{\text{s}}$。）

### 5b.2 合成推導：獨立 ⇒ 變異數相加

白噪 FM（device 熱雜訊）與 flicker FM（device 1/f）來自不同的物理機制，
統計上獨立；獨立隨機變數之和的變異數相加（交叉項期望值為零）：

$$
\sigma_{\Delta t}^2(\Delta t)=\underbrace{\kappa^2\,\Delta t}_{\text{第 4 步（白噪）}}+\underbrace{\zeta^2\,\Delta t^2}_{\text{第 5 步（flicker）}}
$$

$$
\boxed{\ \sigma_{\Delta t}(\Delta t)=\sqrt{\kappa^2\,\Delta t+\zeta^2\,\Delta t^2}\ }
$$

- **出處的誠實聲明**：這條合成式在 [P2] **沒有逐字出現**——論文給的是 Eq.(8)/(9)
  兩個極限行為與 Fig.4/Fig.16 的雙段圖；平方相加是「獨立 ⇒ 變異數相加」的直接推論
  （[P2] p.792 對相關源說 "standard deviations add"、對獨立源說 variances add，
  白噪與 1/f 兩**類**之間取的是後者）。
- **單位（時間版）**：本節的 $\kappa,\zeta$ 都是時間版——$[\kappa]=\sqrt{\text{s}}$
  （$\kappa^2\Delta t:\ \text{s}\cdot\text{s}=\text{s}^2$ ✓）、$\zeta$ 無因次
  （$\zeta^2\Delta t^2=\text{s}^2$ ✓）。相位版（rad 記帳）各乘 $\omega_0$：
  $\kappa_\phi=\omega_0\kappa$（第 4.2 節）、$\zeta_\phi=\omega_0\zeta$
  （$[\zeta_\phi]=\text{rad/s}$）。
- **交界（corner）**：兩項相等 $\kappa^2\Delta t_c=\zeta^2\Delta t_c^2$，解出

$$
\boxed{\ \Delta t_c=\frac{\kappa^2}{\zeta^2}\ }\qquad
\Big[\frac{\text{s}}{1}\Big]=\text{s}\ \checkmark
$$

  $\Delta t\ll\Delta t_c$ 時白噪主導（斜率 1/2）、$\Delta t\gg\Delta t_c$ 時
  flicker 主導（斜率 1）；在 $\Delta t_c$ 處合成曲線比任一條漸近線高
  $\sqrt2$（3 dB，兩項各佔一半）。

### 5b.3 與第 5 步 log 封閉式對帳——「$\zeta$ 是常數」其實是慢變近似

第 5 步的嚴格結果（換到時間單位，除 $\omega_0^2$）是

$$
\sigma_{\Delta t,\text{flicker}}^2(\Delta t)=\frac{4\pi^2 b_3}{\omega_0^2}\,\Delta t^2\Big[\tfrac32-\gamma-\ln(2\pi\Delta t\,f_l)\Big]
\quad\Longrightarrow\quad
\zeta_{\rm eff}^2(\Delta t)=\frac{4\pi^2 b_3}{\omega_0^2}\Big[\tfrac32-\gamma-\ln(2\pi\Delta t\,f_l)\Big],
$$

即 $\zeta$ 並非常數，而是隨 $\Delta t$ 以 $\sqrt{\log}$ 慢慢**變小**（單位檢查：
$b_3/\omega_0^2=[\text{rad}^2\text{Hz}^2]/[\text{rad/s}]^2=$ 無因次 ✓）。log-log
局部斜率跟著偏離 1：

$$
\frac{d\ln\sigma}{d\ln\Delta t}=1-\frac{1}{2\big[\tfrac32-\gamma-\ln(2\pi\Delta t f_l)\big]} .
$$

- lab_24 Part 5 的 MC（$f_l=298$ Hz，受模擬長度限制）在 flicker 區擬合出斜率
  0.909，而 exact 曲線同窗口給 0.911——MC 偏離 1.0 是**物理**（log 修正），
  不是雜訊。
- 真實量測的 $f_l$ 由量測時長決定（秒級 ⇒ $f_l\sim1$ Hz），括號 $\approx13$–$16$，
  局部斜率 $=0.967$（$\Delta t=10^{-7}$ s、$f_l=1$ Hz，lab_24 印出）——
  這就是 [P2] Fig.16 能用**乾淨的 slope-1 直線**擬合的原因：log 修正在硬體
  frequency 十進位跨距下小到看不見。paper 的常數 $\zeta$ 是「括號凍結在 corner
  附近取值」的切線近似；本站圖（下方）同時畫出兩者，幾乎重合。

### 5b.4 時域 corner ↔ 頻域 $1/f^3$ corner（誠實映射）

定義頻譜 corner $f_{1/f^3}\equiv b_3/b_2$（$S_\phi$ 的 $1/f^3$ 段與 $1/f^2$ 段
等值的 offset 頻率）。因為它是**同一條譜內的比值**，SSB 的 $/2$ 與 $/4$ 記帳
在分子分母對消——這是本頁少見「完全不用管慣例」的量。把第 4 步的
$\kappa_\phi^2=2\pi^2b_2$ 與上面的 $\zeta_{\rm eff}$ 代入 $\Delta t_c=\kappa^2/\zeta^2$
（時間版與相位版之比相同，$\omega_0^2$ 對消）：

$$
\Delta t_c=\frac{2\pi^2 b_2}{4\pi^2 b_3\big[\cdot\big]}
=\boxed{\ \frac{1}{2\big[\cdot\big]\,f_{1/f^3}}\ },\qquad
\big[\cdot\big]=\tfrac32-\gamma-\ln(2\pi\Delta t_c f_l)\ (\text{自洽解}).
$$

- **這個 2 不是 SSB 記帳的 2**：分母的 2 來自兩個核積分的係數比——白噪核積分
  $\int\sin^2(ax)/x^2\,dx=\pi a/2$（4.1 節）對上 flicker 核積分的 log 式
  （第 5 步），是 convention-free 的物理常數。
- **數量級直覺**：$[\cdot]\approx10$–$16$，所以 $\Delta t_c$ 比天真猜測的
  $1/f_{1/f^3}$ **短 20–30 倍**。「頻域 corner 在 1 MHz，所以時域 1 µs 處轉折」
  這句話錯一個半數量級——log 括號是罪魁禍首。
- **它與 [P2] Eq.(57) 不同**：App. B 的 $f_{1/f^3}=f_{1/f}\cdot\frac{3}{2\eta N}\frac{(1-A)^2}{1-A+A^2}$
  是「device 1/f corner → 頻譜 corner」的電路級映射；本節的
  $f_{1/f^3}=b_3/b_2$ 是頻譜 corner 的觀測定義。兩者指同一個角，路徑不同。

### 5b.5 數值例（全部數字皆 lab_24 Part 5 實印）

**例 1——[P2] Fig.16 的 oscillator 12（2.8 GHz differential ring）**：

$$
\Delta t_c=\frac{\kappa^2}{\zeta^2}=\Big(\frac{6.18\times10^{-9}\sqrt{\text{s}}}{2.5\times10^{-5}}\Big)^2=6.11\times10^{-8}\ \text{s}\approx61\ \text{ns}=171\ \text{個週期}.
$$

dimension check：$(\sqrt{\text{s}})^2=\text{s}$ ✓。對照 Fig.16，兩條擬合線正是在
$\Delta T\approx6\times10^{-8}$ s 附近交叉 ✓。再反推頻譜 corner（取 $f_l=1$ Hz，
括號 $=15.7$）：$f_{1/f^3}=1/(2\times15.7\times6.11\times10^{-8})=5.21\times10^5$ Hz
——而 [P2] Fig.17（p.802，隨 symmetry voltage 掃描）對同家族 oscillator 7 量到的
$1/f^3$ corner 落在約 $10^5$–$10^6$ Hz 之間，量級正中（不同顆振盪器，只驗量級
不驗個位數）。
時域 jitter 圖與頻域 phase-noise 圖用同一套 $\kappa/\zeta$ 語言互鎖。

**例 2——canonical 5 GHz 振盪器（lab_24 Part 5 的 MC）**：代表值
$\kappa_\phi^2=0.125$ rad²/s（$\Gamma_{rms}=0.5$；真 LC 的 $1/\sqrt2$ 會翻倍成
0.25，白噪段跟著上移、$\Delta t_c$ 加倍——白噪愈強，斜率 1/2 段撐得愈久），
flicker 取 $b_3=6.333\times10^3$ rad²Hz²，使 $f_{1/f^3}=b_3/b_2=1.000$ MHz
（canonical offset）。模擬紀錄長 $2^{24}$ 週期 $=3.36\times10^{-3}$ s
⇒ $f_l=298$ Hz。自洽解 $\Delta t_c=4.89\times10^{-8}$ s（245 週期，括號 $=10.22$）；
MC 兩段擬合線交點 $4.31\times10^{-8}$ s（216 週期，MC/理論 $=0.88$——交點對
擬合窗的選擇敏感，log-log 上僅差 0.06 decade）。恆等式檢查：
$\Delta t_c\,f_{1/f^3}=0.0489=1/(2\times10.22)$ ✓。

![兩段式 jitter 成長：MC 與 [P2] Fig.16 漸近線](/figures/jitter_two_regime.png)

**如何解讀圖**：左圖（canonical 5 GHz）——MC 十字點橫跨 5 個 decade，完全落在
exact 曲線（離散 bin 和）上；藍線 $\kappa\sqrt{\Delta t}$ 與紅線 $\zeta\Delta t$
在 $\Delta t_c=49$ ns 交叉；紅虛線是 log 修正版 flicker（斜率 $0.91$，非 1.0）。
右圖——用 [P2] Fig.16 印出的 $\kappa=6.18\times10^{-9}\sqrt{\text{s}}$、
$\zeta=2.5\times10^{-5}$ 重繪兩條漸近線與合成曲線，corner 標在 61 ns；灰虛線是
log 修正版（$f_l=1$ Hz），與常數-$\zeta$ 版幾乎重合——正是 5b.3 說的「硬體上
看不出 log」。這是 pedagogical 重繪（漸近線與合成式），不是論文量測資料點本身。

## 第 6 步：Monte-Carlo 驗證（lab_24）

![jitter 核 Monte-Carlo 驗證](/figures/jitter_kernels_mc.png)

完整 script：`simulations/lab_24_jitter_kernels.py`（跑法
`PYTHONPATH=. python simulations/lab_24_jitter_kernels.py`）。模擬分五部分，
全部使用 canonical 參數：

| 參數 | 值 | 單位 | 說明 |
|---|---|---|---|
| $f_0$ / $T$ | 5 GHz / 200 ps | Hz / s | 載波 |
| $q_{max}$ | 1 | pC | 節點電荷擺幅 |
| $S_i$ | $10^{-24}$ | A²/Hz | 單邊白噪電流 PSD |
| $\Gamma(\theta)$ | $-\sqrt2\times0.5\,\sin\theta$ | — | rms 恰為代表值 $\Gamma_{rms}=0.5$（reuse `gamma_lc_ideal`） |
| $\kappa$ | 0.3536 | rad/$\sqrt{\text{s}}$ | $=(\Gamma_{rms}/q_{max})\sqrt{S_i/2}$，$\kappa^2=0.125$ rad²/s |
| 取樣 | 32 點/週期 × 2×10⁵ 週期（Part 1）；2×10⁶ 週期（Part 2） | — | Part 2 的每週期增量 $\mathcal{N}(0,\kappa^2T)$ 由 Part 1 證成 |
| $b_3$（Part 5） | $6.333\times10^3$ | rad²·Hz² | flicker FM 位準，使 $f_{1/f^3}=b_3/b_2=1$ MHz；紀錄 $2^{24}$ 週期 ⇒ $f_l=298$ Hz |

**Part 1——不是抽象隨機漫步，而是 [P1] Eq.(11) 的機制**：細取樣白噪電流 → ISF 加權 →
累積積分 → 每週期相位增量。驗證增量標準差 $=\kappa\sqrt T$ 且相鄰週期無相關：

```python
i_n   = white_noise(n, psd=SI, fs=fs, rng=RNG)          # 單邊 PSD = S_i
gamma = np.sqrt(2.0) * GRMS * gamma_lc_ideal(W0 * t)    # rms = 0.5
phi   = np.concatenate(([0.0], np.cumsum(gamma * i_n * dt / QMAX)))
d1    = np.diff(phi[::n_per])                           # 每週期相位增量
print(f"{rms(d1):.4e}")        # -> 5.0051e-06 rad（理論 kappa*sqrt(T)=5.0000e-06）
print(f"{ratio:.3f}")          # -> 1.001
print(f"{corr1:+.4f}")         # -> -0.0012（相鄰週期增量不相關）
```

**Part 2——時域直接量三種 jitter**（2×10⁶ 週期的隨機漫步；圖中間欄與右欄）：

```text
# N-period 相位 jitter：rms(phi[N:]-phi[:-N]) vs 理論 kappa*sqrt(N*T)
# N=1   ratio MC/theory  # -> 0.999
# N=10  ratio            # -> 0.999
# N=100 ratio            # -> 1.001
# period jitter [fs]     # -> 0.1590 fs（理論 0.1592 fs, ratio 0.999）
# cycle-to-cycle [fs]    # -> 0.2248 fs（理論 sqrt(2)*sigma_P=0.2251 fs, ratio 0.999）
```

**Part 3——核積分 = 封閉式（數值 cross-check）**，同時做三種記帳的對帳：

```python
S_phi = 2 * KAPPA**2 / (2*np.pi*f)**2                   # 白噪 FM 單邊譜
num   = trapz(S_phi * 4*np.sin(np.pi*f*N*T)**2, f) + tail
print(f"{num / (KAPPA**2 * N * T):.4f}")
# -> 1.0000 白噪 N=1（N=10 亦 1.0000）
# -> 1.0000 c2c 16sin^4 核 vs 2*kappa^2*T
# -> 1.0000 flicker 數值積分 vs 第 5 步含 log 的封閉式
# -> 0.1592 / 0.1592 / 0.1592 fs（單邊 / 雙邊 / L 記帳三算同值）
# -> -145.0 dBc/Hz（同一條 S_phi 的時域 /2 慣例 SSB）
# -> -148.0 dBc/Hz（[P1] Eq.(21) 的 /4 慣例）
```

**Part 4——canonical 例 C 的譜（$-100$ dBc/Hz@1 MHz、$1/f^2$）**，把本站三個數字接起來：

```python
sigma_t, sigma_phi = integrate_rms_jitter(fgrid, L, f0=5e9, fmin=1e6, fmax=100e6)
print(f"{sigma_t*1e15:.1f} fs")     # -> 447.9 fs TIE（例 C，下限主導）
print(f"{np.sqrt(b2*T**3/2)*1e15:.2f} fs")   # -> 28.28 fs period jitter 封閉式
print(f"{kappa_c:.2f}")             # -> 62.83 rad/sqrt(s)（=2π·1MHz·√L_lin；κ_C√T/ω0 也= 28.28 fs）
print(f"{sigma_c3*1e15:.1f} fs")    # -> 27.6 fs 例 C3 的 10^3–10^10 Hz 截斷數值
```

**Part 5——兩段式成長（白噪＋flicker FM 合成，對應第 5b 步與 [P2] Fig.16）**：
以每週期相位增量合成兩類雜訊——白噪增量 $\mathcal{N}(0,\kappa^2T)$（由 Part 1
證成）＋ flicker 增量（`flicker_noise` 頻譜整形，位準經 Welch 校準），
$2^{24}$ 週期、$\sigma(\Delta t)$ 橫跨 5 個 decade：

```python
b2      = KAPPA2 / (2*np.pi**2); b3 = b2 * 1e6        # 目標 f_{1/f^3} = 1 MHz
k_flick = 2*np.pi**2 * b3 * T**2 * fs                 # 使 S_d(f) = 4pi^2 b3 T^2 / f
d_fl    = flicker_noise(n_periods, fs=fs, k_flicker=k_flick, rng=RNG)
d_w     = RNG.normal(0.0, KAPPA*np.sqrt(T), n_periods)
phi     = np.concatenate(([0.0], np.cumsum(d_w + d_fl)))
sig_t   = np.array([rms(phi[N:] - phi[:-N]) for N in Ns]) / W0   # [s]
```

```text
# flicker 位準校準 S_d*f      # -> 1.000e-14 rad^2（nominal 亦 1.000e-14）
# b3 / f_{1/f^3}              # -> 6.333e+03 rad^2*Hz^2 / 1.000e+06 Hz
# 白噪區擬合斜率（N≤32）      # -> 0.519（理論 0.5；exact 曲線同窗口 0.520）
# flicker 區擬合斜率（N≥3200） # -> 0.909（乾淨 ζΔt 為 1.0；exact 同窗口 0.911）
# corner：MC 擬合線交點        # -> 4.31e-08 s（216 週期）
# corner：自洽理論             # -> 4.89e-08 s（245 週期；MC/理論 = 0.88）
# 恆等式 dt_c·f_{1/f^3}        # -> 0.0489（= 1/(2×bracket)，bracket = 10.22）
# bin 和 vs log 式（N=10⁴）    # -> 1.089（f_l=1/T_rec）；0.984（半 bin 修正 f_l/2）
# 硬體 f_l=1 Hz 局部斜率       # -> 0.967（Δt=1e-7 s；paper 乾淨 slope-1 擬合的正當性）
# [P2] osc-12 corner           # -> 6.11e-08 s（171 週期 @2.8 GHz）
# 反推 f_{1/f^3}               # -> 5.21e+05 Hz（f_l=1 Hz, bracket=15.7）
```

（bin 和 vs log 式差 9% 的出處：log 封閉式以 $f_l=1/T_{rec}$ 為**連續**積分下限，
而離散 FFT 頻譜的第一個 bin 實際涵蓋 $[f_l/2,\,3f_l/2]$ 的功率——把 $f_l$ 換成
半 bin 修正的 $f_l/2$ 後比值變 0.984。又一次 log 的遲鈍：差半個 bin 只動 9%。）

**如何解讀圖**：左欄是三個核（log-log），可直接看到 TIE 平坦、period $\propto f^2$、
c2c $\propto f^4$ 的低頻行為與 4/16 的峰值。中欄是 MC 的
$\sigma_{\Delta\phi}(N)$ 落在 $\kappa\sqrt{NT}$ 理論線上（斜率 1/2，橫跨 4 個 decade）。
右欄是 period 與 c2c 的直方圖：高斯、且 $\sigma_{c2c}=\sqrt2\,\sigma_P$。
這是 **pedagogical 模擬**（單一白噪源、線性相位累積），非 transistor-level。

**與例 C3 / 例 D 的對帳**：worked_examples 例 C3 的 27.6 fs = 封閉式 28.28 fs 截掉
$10^{10}$ Hz 以上尾巴（那裡核平均值 2、$1/f^2$ 譜仍有 ~5% 的變異數貢獻）；
[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) 例 D 的 5.6 fs 是同一條核
只積 1–100 MHz 的頻帶限定版。**同一組公式、同一個前置常數 $1/\omega_0^2$，三個數字全對**。

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 小 jitter：$\sigma_t\ll T$、$\lvert\dot\phi\rvert\ll\omega_0$ | edge↔相位一階映射（第 1 步） | cycle slip、強注入、大 AM-PM |
| 頻率雜訊 $\nu=\dot\phi$ 平穩 | 核公式對隨機漫步 $\phi$ 仍嚴格成立（路 B） | 確定性漂移（溫度、aging）——先去趨勢再套核 |
| $1/f^2$ 在 $f\sim1/(2NT)$ 附近主導 | 白噪封閉式 $\kappa^2NT$、$\sqrt2$ 關係 | flicker corner 高於 $\sim1/(2\pi NT)$：改用第 5 步 log 式；$\sqrt2$ 檢驗失效 |
| flicker 封閉式：$2\pi NTf_l\ll1$ | log 式準到 $O((2\pi NTf_l)^2)$ | 長延遲/高截止：直接數值積分 |
| TIE 有明確頻帶 $[f_1,f_2]$ | 數字可重現 | 自由振盪器 $f_1\to0$ 發散；不標頻帶無意義 |
| 高斯 RJ | $\sigma$ 完整描述分佈（BER 外推可用） | spur/DJ：變異數公式仍對，但分佈非高斯，BER 要 RJ/DJ 分解 |
| 兩段式合成：白噪與 flicker 統計獨立 | $\sigma^2$ 相加、$\Delta t_c=\kappa^2/\zeta^2$（第 5b 步） | supply/substrate 同時打進多級（源間相關）：交叉項不為零，[P2] Eq.(9) 的「標準差相加」接管 |
| 自由振盪（open-loop） | 兩段式無上界成長 | PLL 鎖住後：loop BW 以下被拉回，長 $\Delta t$ 轉平，Fig.16 型曲線只在 loop 時間常數以內成立 |
| 量測底噪已扣除 | $\sigma_{\Delta T,\text{eff}}=\sqrt{\sigma_{\Delta T,\text{meas}}^2-\sigma_{\Delta T,\text{min}}^2}$（[P2] Eq.(39), p.801） | 短 $\Delta t$ 端被 trigger jitter 淹沒：白噪段斜率看起來變平，先扣底噪再擬合 $\kappa$ |

## 對應的 paper / 公式

- $\phi(t)=\frac{1}{q_{max}}\int\Gamma i_n\,d\tau$：[P1] Eq.(11), p.182。
- $\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$（相位 jitter 隨機漫步）：[P2] Eq.(8), p.792；
  $\kappa=(\Gamma_{rms}/q_{max})\sqrt{S_i/2}$（無 $\omega_0$）：[P2] Eq.(11)/(12), p.793（皆已核實）；
  相位↔時間 jitter 換算 $\sigma_{\Delta\phi}=2\pi\sigma_{\Delta t}/T$：[P2] Eq.(10), p.793。
- 相關（1/f）雜訊 $\sigma\propto\Delta t$：[P2] Eq.(9), p.792 與 Fig. 4
  （$\zeta$ 的定義："where $\zeta$ is another proportionality constant"，已核實）。
- 兩段式量測與擬合：[P2] Fig.16, p.802（caption 與 $\kappa=6.18\text{e-}9\ \text{sec}^{0.5}$、
  $\zeta=2.5\text{e}5$ 標註皆已對照渲染頁逐字核實；$\zeta$ 指數缺負號的印刷勘誤見第 5b.1 節）；
  best-fit vs Eq.(12)/(35) 理論值 $6.18/5.95/6.07\times10^{-9}\sqrt{\text{s}}$：p.801；
  slope-1 歸因 device 1/f：p.801 與 Section VI 結尾 pp.797–798；
  量測底噪扣除：Eq.(39), p.801。
- jitter ← phase spectrum（自相關＋Khinchin 路線）：[P2] Eq.(46)–(49), p.803
  （Appendix A 全文 Eq.(40)–(51) 起 p.802 右欄、收 p.803 左欄；逐字轉錄與逐因子
  對帳見本頁「論文原生推導」節）；白噪特例
  $\kappa$←$\mathcal{L}$：Eq.(50), p.803；cycle-to-cycle「based on (8)」：Eq.(51), p.803
  （**此三式已於 v5 逐字核實**（p.803 渲染）：Eq.(49) $\sigma^2_{\Delta\phi}=\tfrac{8}{\omega_0^2}\int_0^\infty S_\phi\sin^2(\pi f\tau)df$（$S_\phi$ 依 Eq.(48) 為**雙邊**譜，故＝本頁單邊 $4\sin^2$ 核）；
  Eq.(50) $\kappa=\tfrac{\Delta f}{f_0}\cdot10^{-\mathcal{L}\{\Delta f\}/20}$——指數的負號表示論文把 $\mathcal{L}$ 讀成「低於載波的 dB 數」（正值）；以帶號 dBc 值代入應讀 $10^{\mathcal{L}/20}=\sqrt{\mathcal{L}_{lin}}$。數值互鎖：$-100$ dBc/Hz、$\Delta f=1$ MHz、$f_0=5$ GHz → $\kappa_t=2.0\times10^{-9}\ \sqrt{\text{s}}$，與本頁第 6 節完全一致 ✓；
  Eq.(51) $\sigma_{CTC}=\tfrac{f}{f_0^{1.5}}\cdot10^{-\mathcal{L}\{\Delta f\}/20}$（照排——分子印作 $f$；由 Eq.(50)×$\sqrt T$ 的因次可知應讀 offset 頻率 $\Delta f$，$\Delta$ 為印刷遺漏，見「論文原生推導」節 A.2）——**印刷式無 $\sqrt2$**：其 $\sigma_{CTC}=\kappa\sqrt{T}$ 是「一個週期的累積」（即本頁的 $\sigma_P$）；若取「相鄰週期差」定義（本頁 $16\sin^4$ 核）則再乘 $\sqrt2$。兩種定義並存於文獻，本頁已分開命名。）
- SSB $/4$ 慣例：[P1] Eq.(21), p.185（$-148$ dBc/Hz）；時域 $/2$ 慣例 $-145$ dBc/Hz：
  規範第 3 節 factor-of-2 註記。
- 核的操作版與例 D：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)；
  例 C3：worked_examples（其 TODO 由本頁關閉）。
- 圖：`jitter_kernels_mc.png`、`jitter_two_regime.png`（皆 lab_24）。

## 重點回顧

- **一個慣例走全程**：單邊 $S_\phi$（rad²/Hz）、$\int_0^\infty$、前置 $1/\omega_0^2$。
  「$2/\omega_0^2$」版本屬於雙邊譜或 $\mathcal{L}$ 記帳——換記帳要整條式一起換。
- 三種 jitter = $\phi$ 的 0/1/2 階差分；核 $=1$、$4\sin^2(\pi fNT)$、$16\sin^4(\pi fT)$。
  每個 2 都有出處：差的變異數的 2 × 半角公式的 2（平方再得 16）。
- 核公式的嚴格成立只需要**頻率雜訊平穩**（boxcar 推導），隨機漫步相位也適用。
- **punchline**：白噪 FM 代入核 (b) 精確得 $\sigma_{\Delta\phi}^2(N)=\kappa^2NT$ ——
  頻域核圖像與 [P2] Eq.(8)/(11)/(12) 的時域隨機漫步是同一件事；MC 比值 0.999–1.001。
- $\sigma_{c2c}=\sqrt2\,\sigma_P$（白噪限定）；$\kappa=2\pi\Delta f\sqrt{\mathcal{L}_{\text{lin}}}$
  （記得用 $/2$ 慣例的 $\mathcal{L}$，$-145$ 而非 $-148$）。
- flicker：$\sigma_{\Delta\phi}^2(N)=4\pi^2b_3(NT)^2[\tfrac32-\gamma-\ln(2\pi NTf_l)]$，
  **對數依賴低頻截止**，report 必附 $f_l$；成長律近似 $\propto N$（[P2] Eq.(9) 的斜率 1 段）。
- **兩段式全貌**（[P2] Fig.16）：$\sigma(\Delta t)=\sqrt{\kappa^2\Delta t+\zeta^2\Delta t^2}$
  （獨立 ⇒ 變異數相加），corner $\Delta t_c=\kappa^2/\zeta^2$；
  時↔頻映射 $\Delta t_c=1/(2[\cdot]f_{1/f^3})$，$[\cdot]\approx10$–$16$ ⇒ 比
  $1/f_{1/f^3}$ 短 20–30 倍；osc-12：61 ns（171 週期）、canonical：49 ns（245 週期）；
  MC 斜率 0.519/0.909 = exact 曲線的 0.520/0.911（偏離 0.5/1.0 是 log 物理）。
- canonical 數字：代表振盪器 $\kappa^2=0.125$ rad²/s、$\sigma_P=0.159$ fs、
  $\sigma_{c2c}=0.225$ fs、$\mathcal{L}(1\text{MHz})=-145/-148$ dBc/Hz（$/2$、$/4$ 慣例）；
  例 C 譜：TIE(1–100 MHz)$=447.9$ fs、period jitter 封閉式 $28.28$ fs（例 C3 的 27.6 fs
  為頻帶截斷）。

## 延伸閱讀

- 核的操作版、$\mathcal{L}\to S_\phi\to\sigma_t$ 四步鏈與例 C/例 D：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- 同家族的差分核（閘平均＋相鄰差）：[allan_variance](/02_foundations/allan_variance)
- $\kappa$ 的 ISF 來源與 ring oscillator 的 $\Gamma_{rms}$：[paper_002 深讀](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)
- 白噪 → $1/f^2$ 相位譜（$/2$ vs $/4$ 慣例的完整討論）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- 隨機漫步相位的頻譜長相（Lorentzian 線形）：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- jitter 對 SerDes BER 的影響：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
