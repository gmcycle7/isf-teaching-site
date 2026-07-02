---
title: Jitter 核的嚴格推導（TIE / N-period / cycle-to-cycle）
description: 在「單邊 S_φ、∫₀^∞」單一慣例下，從 φ(t+NT)−φ(t) 一步步推出 TIE 核 1、period 核 4sin²(πfNT)、cycle-to-cycle 核 16sin⁴(πfT)；白噪 FM 封閉式精確回收 [P2] Eq.(8)/(11) 的 σ_Δφ=κ√(NT)；flicker 1/f³ 給含 log 項的封閉式；lab_24 Monte-Carlo 驗證比值 ≈1.00，正式關閉 worked_examples 例 C3 的前置常數 TODO。
---

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
  （Eq.(49)–(51) 的印刷字面本站尚未逐字核對：TODO: manual verification needed from [P2] p.803；
  本頁公式為獨立推導，數值與 [P2] 已核實的 Eq.(8)/(11)/(12) 完全互鎖，見第 6 節。）
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

### 4.5 實用推論：從 $\mathcal{L}$ 一步讀出 $\kappa$（注意是哪個慣例的 $\mathcal{L}$）

在 $1/f^2$ 區域，時域 $/2$ 慣例下 $\mathcal{L}_{\text{lin}}(\Delta f)=\kappa^2/(2\pi\Delta f)^2$，反解：

$$
\kappa=2\pi\,\Delta f\sqrt{\mathcal{L}_{\text{lin}}(\Delta f)}\quad[\text{rad}/\sqrt{\text{s}}],
\qquad
\frac{\kappa}{\omega_0}=\frac{\Delta f}{f_0}\sqrt{\mathcal{L}_{\text{lin}}(\Delta f)}\quad[\sqrt{\text{s}}].
$$

這對應 [P2] Eq.(50), p.803（白噪特例：由 $1/f^2$ 區的 $\mathcal{L}$ 讀出 $\kappa$；
原式字面同上方 TODO 註記）。**factor-of-2 陷阱**：這條式吃的是
$\mathcal{L}=\tfrac12S_\phi$（時域 $/2$）慣例的數字——canonical 振盪器要代 $-145$ dBc/Hz
得 $\kappa=0.354$ ✓；若誤代 [P1] Eq.(21) $/4$ 慣例的 $-148$，會少 $\sqrt2$（得 0.25）。
同一顆振盪器、同一條譜，**先問清楚 dBc/Hz 是哪種記帳再代公式**。

- **dimension check**：$\text{Hz}\times\sqrt{1/\text{Hz}}=\sqrt{\text{Hz}}=1/\sqrt{\text{s}}$ ✓。

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

## 第 6 步：Monte-Carlo 驗證（lab_24）

![jitter 核 Monte-Carlo 驗證](/figures/jitter_kernels_mc.png)

完整 script：`simulations/lab_24_jitter_kernels.py`（跑法
`PYTHONPATH=. python simulations/lab_24_jitter_kernels.py`）。模擬分四部分，
全部使用 canonical 參數：

| 參數 | 值 | 單位 | 說明 |
|---|---|---|---|
| $f_0$ / $T$ | 5 GHz / 200 ps | Hz / s | 載波 |
| $q_{max}$ | 1 | pC | 節點電荷擺幅 |
| $S_i$ | $10^{-24}$ | A²/Hz | 單邊白噪電流 PSD |
| $\Gamma(\theta)$ | $-\sqrt2\times0.5\,\sin\theta$ | — | rms 恰為代表值 $\Gamma_{rms}=0.5$（reuse `gamma_lc_ideal`） |
| $\kappa$ | 0.3536 | rad/$\sqrt{\text{s}}$ | $=(\Gamma_{rms}/q_{max})\sqrt{S_i/2}$，$\kappa^2=0.125$ rad²/s |
| 取樣 | 32 點/週期 × 2×10⁵ 週期（Part 1）；2×10⁶ 週期（Part 2） | — | Part 2 的每週期增量 $\mathcal{N}(0,\kappa^2T)$ 由 Part 1 證成 |

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

## 對應的 paper / 公式

- $\phi(t)=\frac{1}{q_{max}}\int\Gamma i_n\,d\tau$：[P1] Eq.(11), p.182。
- $\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$（相位 jitter 隨機漫步）：[P2] Eq.(8), p.792；
  $\kappa=(\Gamma_{rms}/q_{max})\sqrt{S_i/2}$（無 $\omega_0$）：[P2] Eq.(11)/(12), p.793（皆已核實）；
  相位↔時間 jitter 換算 $\sigma_{\Delta\phi}=2\pi\sigma_{\Delta t}/T$：[P2] Eq.(10), p.793。
- 相關（1/f）雜訊 $\sigma\propto\Delta t$：[P2] Eq.(9), p.792 與 Fig. 4。
- jitter ← phase spectrum（自相關＋Khinchin 路線）：[P2] Eq.(46)–(49), p.803；白噪特例
  $\kappa$←$\mathcal{L}$：Eq.(50), p.803；cycle-to-cycle「based on (8)」：Eq.(51), p.803
  （此三式字面 TODO: manual verification needed from [P2] p.803；本頁為獨立推導＋數值互鎖）。
- SSB $/4$ 慣例：[P1] Eq.(21), p.185（$-148$ dBc/Hz）；時域 $/2$ 慣例 $-145$ dBc/Hz：
  規範第 3 節 factor-of-2 註記。
- 核的操作版與例 D：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)；
  例 C3：worked_examples（其 TODO 由本頁關閉）。
- 圖：`jitter_kernels_mc.png`（lab_24）。

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
