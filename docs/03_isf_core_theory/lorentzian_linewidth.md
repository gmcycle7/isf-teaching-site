---
title: Lorentzian 線寬：解開 1/f² 在 Δf→0 發散的矛盾
description: 從相位 random walk（Var[Δφ]=2D|t|）經高斯特徵函數推出載波自相關 ½cos(ω₀τ)e^{-D|τ|}，再用 Wiener-Khinchin 得 Lorentzian S∝D/(D²+Δω²) 與 3-dB 線寬 D/π，並把 1/f² 在近載波的「假發散」修正為有限峰、總功率守恆，連 ISF 的 D=Γrms²/(2qmax²)·S_i 與 [E2] Demir 2000。
---

# Lorentzian 線寬：解開 1/f² 在 Δf→0 發散的矛盾

> **前置閱讀**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（$1/f^2$ 招牌結果 [P1] Eq.(21)）、[rms_isf](/03_isf_core_theory/rms_isf)（$\Gamma_{rms}^2/q_{max}^2$ 設定 phase diffusion）、[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)（自相關 ↔ Wiener–Khinchin）。

上一頁 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 推出了振盪器
phase noise 的招牌結果 [P1] Eq.(21)：白噪造成的相位雜訊裙邊是

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right).
$$

這條式子很美，但藏了一個**令人不安的數學病灶**：分母有 $\Delta\omega^2$，當 offset
$\Delta\omega\to0$（無限靠近載波）時，括號內 $\to\infty$，$\mathcal{L}\to+\infty$。
照字面讀，**載波正中央的雜訊功率密度是無窮大**——這顯然是錯的：一個真實振盪器
總功率是有限的（就是它的輸出功率），不可能在某個頻率點塞進無限大功率密度。

這頁就是要**正面解開這個矛盾**。結論先講：$1/\Delta\omega^2$ 是「相位線性化」近似下的**遠端漸近**，
不是近載波的真相。把相位的**隨機漫步（random walk）**本質老實算進去，載波頻譜會在近載波處
**轉平成一條 Lorentzian（洛倫茲線型）**，峰值有限、總功率守恆、而且自然定義出一個
**有限的 3-dB 線寬（linewidth）** $\Delta f_{3\mathrm{dB}}=D/\pi$。

> **物理直覺（先講結論）**：白噪持續踢相位，相位 $\phi(t)$ 不是停在某個值，而是像醉漢走路一樣
> **無界地隨機漫步**（Wiener process，維納過程）。相位的方差**線性成長** $\mathrm{Var}[\Delta\phi]=2D|t|$。
> 載波 $\cos(\omega_0t+\phi)$ 因此**逐漸失憶**：隔得越久，相位差越大、越不相關，自相關
> $R_x(\tau)$ **指數衰減**。一個指數衰減的自相關，傅立葉變換出來就是 **Lorentzian**——
> 一條有限高、有限寬的鐘形線。$1/f^2$ 只是這條 Lorentzian「遠離中心」時的尾巴。
> 近中心它**必然轉平**，因為「相位完全失憶」這件事最多只能讓功率攤平，不可能讓它發散。

本頁全程用規範 11.2 的 Lorentzian 全套逐步推導。所用的「相位擴散 → 指數自相關 → Lorentzian」
這套機制屬**外部文獻**，主要對應 **[E2] A. Demir, A. Mehrotra, and J. Roychowdhury,
"Phase Noise in Oscillators: A Unifying Theory and Numerical Methods for Characterization,"
IEEE Trans. Circuits Syst. I, vol. 47, no. 5, pp. 655–674, May 2000（DOI: 10.1109/81.847872）**，
**不在本站下載的 5 篇 PDF 內**（卷期/頁碼/DOI 已查證，見 [references](/99_appendix/references) 的 [E2]）。
[P1] 本身用線性化得到 $1/f^2$，但 [P1] 並未處理 $\Delta\omega\to0$ 的發散；Demir 等人的相位擴散
模型正是補上這塊的標準工具。

## 第 0 步：問題的根——相位是 random walk，不是一個固定值

回到 [P1] Eq.(11) 的相位積分（見 [convolution_derivation](/03_isf_core_theory/convolution_derivation)）：

$$
\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau .
$$

白噪 $i_n$ 的**積分**是一個 **Wiener process（維納過程）**——也就是布朗運動式的隨機漫步。
它的關鍵性質：**沒有恢復力**（相位是 Floquet 的 $\lambda_1=0$ 中性方向，見
[derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)），所以相位**不會回到某個平衡值**，
而是無界地擴散開來。

- **數學特徵**：白噪積分的方差**隨時間線性成長**（這是 Wiener process 的定義性質）。我們把比例常數
  記為 $2D$：

$$
\operatorname{Var}[\Delta\phi(t)]=\big\langle(\phi(t+t_0)-\phi(t_0))^2\big\rangle=2D\,|t|.
$$

  這裡 $D$ 叫 **phase diffusion constant（相位擴散常數）**，單位 $\text{rad}^2/\text{s}$
  （規範 11.2）。$|t|$ 取絕對值是因為往前往後看方差都一樣大（過程平穩增量）。

- **單位檢查**：$[\operatorname{Var}\Delta\phi]=\text{rad}^2$；右邊 $[2D]\cdot[t]=(\text{rad}^2/\text{s})\cdot\text{s}=\text{rad}^2$ ✓。

- **為什麼是線性而不是別的**：白噪不同時刻不相關，積分 $N$ 個獨立增量，方差像「擲 $N$ 次骰子求和」
  一樣**線性疊加**（$N\propto t$）——這就是 $\sqrt{t}$ 漫步、$t$ 方差的由來，也正是
  [numerical_feeling](/04_simulation_labs/numerical_feeling) 裡 $\sigma_{\Delta t}\propto\sqrt{\Delta t}$
  的同一件事（accumulated jitter 是相位漫步的時間版）。

> **這一步就把矛盾的種子點破了**：$1/f^2$ 推導把 $\phi$ 當成「小、可線性化、有界」；但真實 $\phi$
> 是**無界漫步**。當你問「無限靠近載波（$\Delta\omega\to0$，即觀察無限久 $t\to\infty$）會怎樣」，
> $\phi$ 早就漫步到 $\gg 1$ rad，線性化失效。所以發散不是物理、是**近似用在它失效的地方**。

## 第 1 步：載波自相關——用高斯特徵函數把相位漫步轉成指數衰減

把載波寫成（[P1] Eq.(1) 的純相位版，振幅 $A$ 設為常數、只看相位）：

$$
x(t)=A\cos\big(\omega_0 t+\phi(t)\big).
$$

我們要算它的**自相關函數**（autocorrelation，訊號與自己延遲 $\tau$ 後的平均相乘）：

$$
R_x(\tau)=\big\langle x(t)\,x(t+\tau)\big\rangle .
$$

**第 (i) 步：用積化和差展開兩個餘弦。** 令 $\Delta\phi\equiv\phi(t+\tau)-\phi(t)$：

$$
x(t)x(t+\tau)=A^2\cos(\omega_0t+\phi(t))\cos(\omega_0(t+\tau)+\phi(t+\tau)).
$$

用 $\cos\alpha\cos\beta=\tfrac12[\cos(\alpha-\beta)+\cos(\alpha+\beta)]$：

$$
x(t)x(t+\tau)=\frac{A^2}{2}\Big[\cos\big(\omega_0\tau+\Delta\phi\big)+\cos\big(2\omega_0t+\omega_0\tau+\phi(t)+\phi(t+\tau)\big)\Big].
$$

- **慢項** $\cos(\omega_0\tau+\Delta\phi)$ 與絕對時間 $t$ 無關（只含 $\tau$ 與相位差），平均後存活。
- **快項** 含 $2\omega_0t$，對 $t$ 做時間平均（或對隨機相位平均）後**歸零**——它在 $2\omega_0$ 附近振盪，
  載波長期平均看不到。丟掉它。

於是

$$
R_x(\tau)=\frac{A^2}{2}\big\langle\cos(\omega_0\tau+\Delta\phi)\big\rangle.
$$

**第 (ii) 步：把平均搬進來，用高斯特徵函數。** 展開 $\cos(\omega_0\tau+\Delta\phi)=
\cos\omega_0\tau\cos\Delta\phi-\sin\omega_0\tau\sin\Delta\phi$。$\Delta\phi$ 是**零均值高斯**
（白噪積分 → 高斯；且對稱分佈 $\langle\sin\Delta\phi\rangle=0$）：

$$
R_x(\tau)=\frac{A^2}{2}\Big[\cos\omega_0\tau\,\langle\cos\Delta\phi\rangle-\sin\omega_0\tau\,\underbrace{\langle\sin\Delta\phi\rangle}_{=0}\Big]=\frac{A^2}{2}\cos\omega_0\tau\,\langle\cos\Delta\phi\rangle.
$$

剩下的 $\langle\cos\Delta\phi\rangle$ 用**高斯特徵函數（characteristic function）**——對零均值高斯
變數 $\Delta\phi\sim\mathcal{N}(0,\sigma^2)$，

$$
\big\langle e^{j\Delta\phi}\big\rangle=e^{-\sigma^2/2}\quad\Longrightarrow\quad\langle\cos\Delta\phi\rangle=\operatorname{Re}\big\langle e^{j\Delta\phi}\big\rangle=e^{-\sigma^2/2}.
$$

這是本頁的**數學樞紐**：高斯的「平均一個複指數」等於「$e^{-\tfrac12\text{方差}}$」。把第 0 步的
$\sigma^2=\operatorname{Var}[\Delta\phi(\tau)]=2D|\tau|$ 代進去：

$$
\langle\cos\Delta\phi\rangle=e^{-\tfrac12\cdot 2D|\tau|}=e^{-D|\tau|}.
$$

**第 (iii) 步：合起來得到載波自相關（規範 11.2）。** 把 $A^2$ 吸收進歸一化（取單位功率
$A^2/2\to\tfrac12$ 慣例，與 lab_18 一致）：

$$
\boxed{\ R_x(\tau)=\frac{1}{2}\cos(\omega_0\tau)\,e^{-D|\tau|}\ }
$$

- **物理意義**：$\cos(\omega_0\tau)$ 是載波本身的振盪；$e^{-D|\tau|}$ 是**失憶包絡**——隔越久，
  相位差累積越大、$\langle\cos\Delta\phi\rangle$ 越小，自相關指數衰減。$D$ 越大（噪越凶），失憶越快。
- **單位檢查**：$[D|\tau|]=(\text{rad}^2/\text{s})\cdot\text{s}=\text{rad}^2$？——注意 $D|\tau|$ 出現在指數裡
  必須無因次。這裡的慣例是把 $D$ 的「$\text{rad}^2$」當無因次（相位本就是無因次弧度），故 $D$ 等效
  $[1/\text{s}]$、$D|\tau|$ 無因次 ✓。$R_x$ 無因次（功率歸一化）✓。
- **與 [P1] 的銜接**：[P1] 從沒寫過這條 $e^{-D|\tau|}$；它停在「相位小、線性」。一旦承認相位是
  無界漫步，這條指數衰減是**唯一**自洽的結果（[E2] Demir 2000 的核心）。

## 第 2 步：Wiener-Khinchin——指數衰減的自相關 ⇒ Lorentzian 頻譜

**Wiener-Khinchin 定理**：平穩隨機過程的功率譜密度 $S_x(\omega)$ 是自相關 $R_x(\tau)$ 的傅立葉變換：

$$
S_x(\omega)=\int_{-\infty}^{\infty}R_x(\tau)\,e^{-j\omega\tau}\,d\tau .
$$

代入第 1 步的 $R_x(\tau)=\tfrac12\cos(\omega_0\tau)e^{-D|\tau|}$。把 $\cos(\omega_0\tau)=
\tfrac12(e^{j\omega_0\tau}+e^{-j\omega_0\tau})$ 拆開，得到兩個一樣的雙邊指數變換，分別搬到
$\pm\omega_0$。我們只需要其中**繞 $+\omega_0$** 那一支（正頻載波附近）。

**用到的標準變換**（雙邊指數的傅立葉變換，是 Lorentzian 的標準對）：

$$
\int_{-\infty}^{\infty}e^{-D|\tau|}\,e^{-j\Omega\tau}\,d\tau=\frac{2D}{D^2+\Omega^2}.
$$

把它親手算一遍（拆 $\tau>0$ 與 $\tau<0$ 兩段）：

$$
\begin{aligned}
\int_{-\infty}^{\infty}e^{-D|\tau|}e^{-j\Omega\tau}d\tau
&=\int_{0}^{\infty}e^{-(D+j\Omega)\tau}d\tau+\int_{0}^{\infty}e^{-(D-j\Omega)\tau}d\tau\\
&=\frac{1}{D+j\Omega}+\frac{1}{D-j\Omega}=\frac{(D-j\Omega)+(D+j\Omega)}{D^2+\Omega^2}=\frac{2D}{D^2+\Omega^2}.
\end{aligned}
$$

令載波附近的 offset 角頻率 $\Omega=\omega-\omega_0\equiv\Delta\omega$（把 $\cos$ 的 $e^{j\omega_0\tau}$
那支吸收掉，等於把頻率原點平移到載波），並帶上 $R_x$ 的前置 $\tfrac12\cdot\tfrac12=\tfrac14$：

$$
\boxed{\ S_x(\Delta\omega)\propto\frac{D}{D^2+\Delta\omega^2}\ }\qquad(\textbf{Lorentzian，規範 11.2}).
$$

- **這就是 Lorentzian**：一條以載波為中心、峰值有限、左右對稱的鐘形線。
- **看出「不再發散」了嗎**：$\Delta\omega\to0$ 時 $S_x\to D/D^2=1/D$——**有限**！峰值是 $1/D$，
  不是無窮大。發散被治好了。
- **單位/形狀檢查**：分母 $D^2+\Delta\omega^2$ 兩項同因次（都是 $[\text{s}^{-2}]$），比值形狀正確；
  整體常數由總功率歸一化（見第 4 步）固定。

### 為什麼遠端又回到 $1/f^2$（與 [P1] 一致）

當 $\Delta\omega\gg D$（離載波夠遠），分母 $D^2+\Delta\omega^2\approx\Delta\omega^2$：

$$
S_x(\Delta\omega)\xrightarrow[\Delta\omega\gg D]{}\frac{D}{\Delta\omega^2}\propto\frac{1}{\Delta\omega^2}.
$$

**遠端漸近正是 $1/f^2$**——與 [P1] Eq.(21) 完全吻合。所以 Lorentzian 不是推翻 [P1]，而是
**把 [P1] 的 $1/f^2$ 嵌進一條近載波轉平的完整線型裡**：遠端 $1/f^2$、近端 flat，轉折點就在
$\Delta\omega\approx D$。下圖把這三件事（模擬 / Lorentzian 理論 / $1/f^2$ 漸近）疊在一起。

## 第 3 步：3-dB 線寬（FWHM）= D/π

Lorentzian 的**半高全寬（FWHM，full width at half maximum）**就是工程上講的「**3-dB 線寬**」
或「linewidth」。求它：峰值在 $\Delta\omega=0$ 為 $D/D^2=1/D$；半高處 $S_x=\tfrac12\cdot\tfrac1D$：

$$
\frac{D}{D^2+\Delta\omega^2}=\frac{1}{2D}\quad\Longrightarrow\quad D^2+\Delta\omega^2=2D^2\quad\Longrightarrow\quad\Delta\omega=\pm D.
$$

所以半高處在 $\Delta\omega=\pm D$（rad/s）。

- **HWHM（半寬）**：$\Delta\omega_{\text{HWHM}}=D$ rad/s $\Rightarrow$
  $\Delta f_{\text{HWHM}}=\dfrac{D}{2\pi}$ Hz。
- **FWHM（3-dB 全寬）**：是 HWHM 的兩倍，$\Delta\omega_{\text{FWHM}}=2D$ rad/s $\Rightarrow$

$$
\boxed{\ \Delta f_{3\mathrm{dB}}=\frac{2D}{2\pi}=\frac{D}{\pi}\ \text{Hz}\ }\qquad(\textbf{規範 11.2}).
$$

- **物理意義**：$D$ 越大（噪越凶、相位失憶越快），線寬越寬、載波越「胖」。理想無噪振盪器
  $D\to0$ → 線寬 $\to0$ → 退化成 delta 線（純載波）。
- **單位檢查**：$[D/\pi]=(1/\text{s})/(\text{無因次})=\text{Hz}$ ✓。
- **「3-dB」的由來**：半高 $=$ 功率掉一半 $=10\log_{10}(1/2)=-3.01$ dB，故稱 3-dB 線寬。

## 第 4 步：總功率守恆——Lorentzian 把無限大攤平成有限積分

$1/f^2$ 在近載波發散最致命的後果是：對 $1/\Delta\omega^2$ 從 $0$ 積分**發散**
（$\int_0 d(\Delta\omega)/\Delta\omega^2=\infty$），等於說相位雜訊功率無限大。Lorentzian 治好了它，
因為 Lorentzian 的積分**收斂**。用標準積分 $\int_{-\infty}^{\infty}\dfrac{d\Omega}{D^2+\Omega^2}=\dfrac{\pi}{D}$：

$$
\int_{-\infty}^{\infty}\frac{D}{D^2+\Delta\omega^2}\,d(\Delta\omega)=D\cdot\frac{\pi}{D}=\pi\quad(\text{有限}).
$$

- **物理意義**：把所有 offset 的功率加起來是**有限的常數**——正好等於載波的總功率
  （經適當歸一化）。相位漫步只是把原本集中在 delta 線的功率**塗抹**成一條有限寬的 Lorentzian，
  **總功率一點沒少**（能量守恆）。這就是「總功率守恆」（規範 11.2 的關鍵教學點）。
- **對照 delta 線**：$D\to0$ 時 Lorentzian $\to\pi\,\delta(\Delta\omega)$（高瘦無限），退化回理想載波；
  $D > 0$ 時被攤平成有限峰。**功率從未發散，只是被重新分佈。**

> **一句話解開矛盾**：$1/f^2$ 的發散是「假發散」——它源自把無界的相位漫步硬塞進有界的線性近似。
> 真實頻譜近載波必然轉平成 Lorentzian（峰 $=1/D$、寬 $=D/\pi$、總功率 $=$ 載波功率守恆）。
> [P1] Eq.(21) 的 $1/f^2$ 只在 $\Delta\omega\gg D$ 成立，是 Lorentzian 的遠端尾巴。

## 第 5 步：與 ISF 連結——把 D 寫成 Γrms 與 qmax

現在把抽象的 $D$ 接回 [P1] 的 ISF 物理量。比對「兩種寫法的近載波 $1/f^2$ skirt」即可定出 $D$。

**從 Lorentzian 端**：遠端 $S_x\to D/\Delta\omega^2$。把它寫成 phase PSD（雙邊指數的相位漫步，
phase PSD 是 $S_\phi=2D/\Delta\omega^2$，這是 Wiener 過程相位的標準頻譜）：

$$
S_\phi(\Delta\omega)=\frac{2D}{\Delta\omega^2}\qquad[\text{rad}^2/\text{Hz}].
$$

**從 ISF 端**（上一頁的時域乾淨版 $S_\phi=\Gamma_{rms}^2 S_i/(q_{max}^2\Delta\omega^2)$，
記 $S_i=\overline{i_n^2}/\Delta f$）：

$$
S_\phi(\Delta\omega)=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{\Delta\omega^2}.
$$

**令兩者相等**（同一條 $1/\Delta\omega^2$ skirt，係數必須一致）：

$$
2D=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}\quad\Longrightarrow\quad\boxed{\ D=\frac{\Gamma_{rms}^2}{2q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}\ }\qquad(\textbf{規範 11.2}).
$$

代進第 3 步的線寬公式，得到**用 ISF 物理量直接算 3-dB 線寬**：

$$
\boxed{\ \Delta f_{3\mathrm{dB}}=\frac{D}{\pi}=\frac{\Gamma_{rms}^2}{2\pi\,q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}\ }\qquad(\textbf{規範 11.2}).
$$

- **設計訊息**：線寬 $\propto\Gamma_{rms}^2/q_{max}^2\cdot S_i$——和 [P1] Eq.(21) 的 $\mathcal{L}$
  **同一組旋鈕**！要窄線寬（乾淨載波），一樣是**加大電荷擺幅 $q_{max}$、壓低 $\Gamma_{rms}$、降低
  noise PSD $S_i$**。Lorentzian 沒有引入任何新旋鈕，只是把同一組物理量重新包裝成「線寬」這個
  直接可量的數字。
- **單位檢查**：$[D]=\dfrac{1}{\text{C}^2}\cdot\dfrac{\text{A}^2}{\text{Hz}}=\dfrac{\text{A}^2}{\text{A}^2\text{s}^2}\cdot\text{s}=\dfrac{1}{\text{s}}$
  （用 $\text{C}=\text{A}\cdot\text{s}$、$\text{Hz}^{-1}=\text{s}$）✓，故 $D/\pi$ 是 Hz ✓。
- **factor-of-2 註記**：這裡用時域乾淨版（$S_\phi=\Gamma_{rms}^2S_i/(q_{max}^2\Delta\omega^2)$）對應出
  $D=\Gamma_{rms}^2S_i/(2q_{max}^2)$。若改用 [P1] Eq.(21) 的 SSB $/4$ 慣例，$D$ 會差個常數 2——
  這跟上一頁講的 factor-of-2 是**同一件記帳事**，不影響 scaling，只讓線寬數值差 $\times2$。
  本頁全程用時域乾淨版，與 lab_18 一致。

## 對應模擬圖

`simulations/lab_18_lorentzian.py` 用一段 **Wiener 相位**（白噪累積 $\phi=\operatorname{cumsum}(\text{N}(0,2D\,dt))$）
合成載波 $x=\cos(2\pi f_0t+\phi)$，用 Welch 估其頻譜，疊上 Lorentzian 理論與 $1/f^2$ 漸近；
右圖直接量 $\operatorname{Var}[\Delta\phi(\tau)]$ 驗證它線性成長（$=2D\tau$）。

![載波是 Lorentzian：近載波轉平成有限峰，1/f² 只是遠端漸近；右圖相位方差線性成長驗證 random walk](/figures/lorentzian_carrier_lineshape.png)

| 項目 | 值（lab_18） | 說明 |
|---|---|---|
| 模型 | toy / illustrative（非 transistor-level） | 直接合成 Wiener 相位，標 normalized 單位 |
| 載波 $f_0$ | $400$（normalized） | 任意載波，只看相對 offset |
| 相位擴散 $D$ | $2.0\ \text{rad}^2/\text{s}$ | 控制線寬的唯一旋鈕 |
| 相位增量 | $d\phi\sim\mathcal{N}(0,\,2D/f_s)$ | Wiener：方差 $=2D\,dt$ |
| 3-dB 線寬 | $\Delta f_{3\mathrm{dB}}=D/\pi\approx0.64$ Hz | FWHM；HWHM $=D/2\pi\approx0.32$ Hz |
| 近載波 | 轉平成有限峰 $\propto1/D$ | 不再發散 |
| 遠載波 | $\propto1/\Delta f^2$ 漸近 | 與 [P1] Eq.(21) 一致 |

**如何解讀左圖**：藍線（模擬頻譜）在大 offset 沿著紅色點線（$1/\Delta f^2$ 漸近）下滑；越靠近載波，
藍線**離開** $1/f^2$、貼上黑色虛線（Lorentzian）並**轉平**；綠色點劃線標出 HWHM $=D/2\pi$ 的位置，
正是「轉折」發生處。**這張圖一眼就說明：$1/f^2$ 是尾巴、Lorentzian 才是全貌。**
**如何解讀右圖**：量到的 $\operatorname{Var}[\Delta\phi(\tau)]$（藍）精準落在 $2D\tau$（黑虛）直線上，
證實相位確實是線性擴散的 random walk——這就是指數自相關、進而 Lorentzian 的根。

核心 Python（完整 script：`simulations/lab_18_lorentzian.py`）：

```python
import numpy as np
from scipy.signal import welch

RNG = np.random.default_rng(18)
fs, n, f0, D = 4096.0, 2**20, 400.0, 2.0          # D = phase diffusion [rad^2/s]
t = np.arange(n) / fs

# Wiener 相位：增量 ~ N(0, 2 D dt) -> Var[phi(t)] = 2 D t
dphi = RNG.standard_normal(n) * np.sqrt(2 * D / fs)
phi = np.cumsum(dphi)
x = np.cos(2 * np.pi * f0 * t + phi)

f, P = welch(x, fs=fs, nperseg=2**16, scaling="density")   # 頻譜：載波是 Lorentzian
off = f - f0
lor = D / (D**2 + (2 * np.pi * off)**2)                     # Lorentzian 理論
fwhm = D / np.pi                                            # 3-dB 線寬 = D/pi Hz
```

## Worked examples 數值例題

兩題都用嚴格格式：**題目 → 逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證**。
例 1 由「實際 PN 規格」反推 $D$ 與線寬（最有設計感的算法）；例 2 由「ISF 物理量」正推。

> **例 1（canonical：由 5 GHz、$-100$ dBc/Hz @ 1 MHz 反推 $D$ 與線寬）**：一顆 $f_0=5$ GHz 振盪器，
> 量到 $\mathcal{L}(1\,\text{MHz})=-100$ dBc/Hz、$1/f^2$ 斜率。求相位擴散 $D$ 與 3-dB 線寬 $\Delta f_{3\mathrm{dB}}$。

**逐步代入：**

1. **把 dBc/Hz 還原成 linear。** $\mathcal{L}=-100$ dBc/Hz 表示
   $\mathcal{L}_{\text{lin}}(1\,\text{MHz})=10^{-100/10}=10^{-10}\ /\text{Hz}$。

2. **由 $\mathcal{L}\approx\tfrac12 S_\phi$ 得 phase PSD。** $S_\phi(1\,\text{MHz})=2\mathcal{L}_{\text{lin}}=2\times10^{-10}\ \text{rad}^2/\text{Hz}$。

3. **用 $1/f^2$ 形狀外推係數。** $S_\phi(\Delta\omega)=\dfrac{2D}{\Delta\omega^2}$，在 $\Delta f=1$ MHz：
   $\Delta\omega=2\pi\times10^6=6.283\times10^6$ rad/s，$\Delta\omega^2=3.948\times10^{13}$。故

$$
2D=S_\phi\cdot\Delta\omega^2=2\times10^{-10}\times3.948\times10^{13}=7.896\times10^{3}\ \text{rad}^2/\text{s}.
$$

4. **解出 $D$。** $D=\dfrac{7.896\times10^3}{2}=3.948\times10^{3}\ \text{rad}^2/\text{s}$。

5. **算 3-dB 線寬。** $\Delta f_{3\mathrm{dB}}=\dfrac{D}{\pi}=\dfrac{3.948\times10^3}{3.1416}\approx1.257\times10^{3}\ \text{Hz}\approx1.26\ \text{kHz}$。

**結果：** $D\approx3.95\times10^{3}\ \text{rad}^2/\text{s}$，**3-dB 線寬 $\approx1.26$ kHz**。

**手感檢查**：一顆 5 GHz、$-100$ dBc/Hz@1MHz 的振盪器，其載波其實是一條約 1.3 kHz 寬的
Lorentzian——相對 5 GHz 載波是 $2.5\times10^{-7}$ 的相對線寬（$Q$ 等級 $\sim 4\times10^6$ 的等效）。
量測時若解析頻寬（RBW）遠大於 1.3 kHz，你看到的是被 RBW 抹平的「尖峰」，根本看不到 Lorentzian
轉平；要看到轉平得用 sub-kHz RBW 或 cross-correlation 法。**這就是為什麼日常 PN 圖只看到 $1/f^2$
而看不到 Lorentzian 平頂——量測解析度不夠近載波。**

**Dimension check：** $[2D]=[S_\phi]\cdot[\Delta\omega^2]=\dfrac{\text{rad}^2}{\text{Hz}}\cdot\dfrac{\text{rad}^2}{\text{s}^2}$；
以 $\text{Hz}^{-1}=\text{s}$ 且把 rad 當無因次，$=\dfrac{1}{\text{s}}\cdot\text{s}\cdot\dfrac{1}{\text{s}^2}\cdot\text{s}=\dfrac{1}{\text{s}}$... 化簡得 $[D]=\text{rad}^2/\text{s}=1/\text{s}$，$[D/\pi]=\text{Hz}$ ✓。

```python
import numpy as np
L_dbc = -100.0                      # dBc/Hz @ 1 MHz, 1/f^2 slope
df = 1e6
L_lin = 10**(L_dbc/10)             # -> 1e-10 /Hz
S_phi = 2 * L_lin                  # L ~ S_phi/2  -> rad^2/Hz
dw = 2*np.pi*df
D = S_phi * dw**2 / 2              # S_phi = 2D/dw^2  -> D
linewidth = D / np.pi             # 3-dB linewidth [Hz]
print(round(D), "rad^2/s ;", round(linewidth), "Hz")   # -> 3948 rad^2/s ; 1257 Hz
```

> **例 2（由 ISF 物理量正推 $D$ 與線寬）**：用上一頁 canonical 例 B 的數字——$q_{max}=1$ pC、
> $\Gamma_{rms}=0.5$、$S_i=\overline{i_n^2}/\Delta f=10^{-24}\ \text{A}^2/\text{Hz}$。求 $D$ 與 3-dB 線寬。

**逐步代入：**

1. **算 $D=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\,S_i$。**
   $\dfrac{\Gamma_{rms}^2}{2q_{max}^2}=\dfrac{0.25}{2\times(10^{-12})^2}=\dfrac{0.25}{2\times10^{-24}}=1.25\times10^{23}\ \text{C}^{-2}$。

2. 乘上 $S_i$：$D=1.25\times10^{23}\times10^{-24}=0.125\ \text{rad}^2/\text{s}$。

3. **線寬。** $\Delta f_{3\mathrm{dB}}=\dfrac{D}{\pi}=\dfrac{0.125}{3.1416}\approx0.0398\ \text{Hz}\approx40\ \text{mHz}$。

**結果：** $D=0.125\ \text{rad}^2/\text{s}$，**3-dB 線寬 $\approx40$ mHz**。

**手感對照**：這組「單一理想白噪源」的數字對應上一頁**時域乾淨版**的 $\mathcal{L}(1\text{MHz})\approx-145$ dBc/Hz
（SSB $/4$ 慣例為 $-148$；本頁全程用時域 $/2$ 版，故以 $-145$ 為自洽基準）——比例 1 的 $-100$ dBc/Hz
乾淨約 45 dB（$-100-(-145)=45$），所以線寬也窄得多（40 mHz vs 1.26 kHz，
窄約 $3\times10^4$ 倍 $\approx 45$ dB 的功率比，自洽 ✓）。**驗證了「線寬與 $\mathcal{L}$ 同一組物理、
只差包裝」**：$\mathcal{L}$ 低 45 dB $\Leftrightarrow$ $D$ 與線寬小約 $10^{4.5}$ 倍。

> **與 capstone 的 $80$ mHz 對齊（$\Gamma_{rms}^2$ 包裝，非誤差）**：本例用**規範代表值**
> $\Gamma_{rms}=0.5$（$\Gamma_{rms}^2=0.25$）得 $D=0.125\ \text{rad}^2/\text{s}$、線寬 $\approx40$ mHz；
> 而 [capstone_lc_end_to_end](/03_isf_core_theory/capstone_lc_end_to_end) 主脊用**真・理想 LC** 的
> $\Gamma_{rms}=1/\sqrt2$（$\Gamma_{rms}^2=0.5$，剛好兩倍）得 $D=0.25\ \text{rad}^2/\text{s}$、線寬 $\approx80$ mHz。
> 兩個數字都對——差的 **$2\times$ 正是 $\Gamma_{rms}^2$（$0.5$ vs $0.25$）的包裝**，不是哪一頁算錯（對應
> capstone 站⑤的 $-145$ vs $-148$ dBc/Hz 那 3 dB 差，$10\log_{10}2=3.01$，同一件事）。本頁取代表值
> $0.5$ 以與全站 canonical 例 B 對齊；capstone 取 $-\sin$ 的理想值 $1/\sqrt2$ 一以貫之。

**Dimension check：** $[D]=\text{C}^{-2}\cdot\dfrac{\text{A}^2}{\text{Hz}}=\text{A}^{-2}\text{s}^{-2}\cdot\text{A}^2\text{s}=\dfrac{1}{\text{s}}$ ✓，$[D/\pi]=\text{Hz}$ ✓。

```python
import numpy as np
gamma_rms, qmax, Si = 0.5, 1e-12, 1e-24
D = gamma_rms**2 / (2 * qmax**2) * Si      # rad^2/s
linewidth = D / np.pi                       # Hz
print(D, "rad^2/s ;", round(linewidth, 4), "Hz")   # -> 0.125 rad^2/s ; 0.0398 Hz
```

（兩題都用時域乾淨版 $D=\Gamma_{rms}^2S_i/(2q_{max}^2)$。若用 [P1] Eq.(21) 的 SSB $/4$ 慣例，
$D$ 與線寬各 $\times2$——同上一頁 factor-of-2 註記，不影響 scaling。
完整函式庫：`simulations/common/noise_utils.py`、`simulations/lab_18_lorentzian.py`。）

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 相位為純 random walk（白噪主導） | 自相關 $e^{-D\lvert\tau\rvert}$、頻譜純 Lorentzian | 含 flicker（$1/f^3$）時近載波不是單純 Lorentzian，要 Demir 一般式 |
| 相位差 $\Delta\phi$ 為高斯 | 特徵函數 $\langle\cos\Delta\phi\rangle=e^{-\sigma^2/2}$ 精確 | 強非線性/大注入使 $\Delta\phi$ 非高斯時近似失準 |
| 小 $D$（窄線寬、高 $Q$） | Lorentzian 與遠端 $1/f^2$ 清楚分離 | $D$ 大（很吵）時整條被展寬，$1/f^2$ 區縮小 |
| 振幅穩定（只追相位） | 只需 $D$ 一個參數 | 強 AM-PM 時要把振幅 noise 一起算 |
| 量測 RBW $\ll D/\pi$ | 量得到 Lorentzian 平頂 | RBW 太寬時只看到 $1/f^2$ 尖峰、看不到轉平 |

## 與哪些 paper／公式對應

- **本頁機制（相位擴散 → 指數自相關 → Lorentzian → 線寬 $D/\pi$）屬外部文獻、不在 5 篇 PDF 內**：
  [E2] Demir–Mehrotra–Roychowdhury 2000（DOI 10.1109/81.847872，見 [references](/99_appendix/references)）。
- **遠端 $1/f^2$ 漸近**與**$D=\Gamma_{rms}^2S_i/(2q_{max}^2)$ 的連結**接回 [P1] Eq.(21), p.185
  （見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)）。
- **相位積分／random walk 的根**：[P1] Eq.(11), p.182（見
  [convolution_derivation](/03_isf_core_theory/convolution_derivation)、
  [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv) 的 $\lambda_1=0$ 中性方向）。
- **accumulated jitter $\propto\sqrt{\Delta t}$** 是同一個 random walk 的時間版（[P2] Eq.(8), p.792，見
  [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)）。

## 重點回顧

- $1/f^2$ 在 $\Delta\omega\to0$ 的發散是**假發散**：源自把無界的相位 random walk 硬套線性近似。
- 相位是 Wiener process：$\operatorname{Var}[\Delta\phi]=2D|t|$（$D$=phase diffusion，$\text{rad}^2/\text{s}$）。
- 高斯特徵函數 $\langle e^{j\Delta\phi}\rangle=e^{-\sigma^2/2}$ → 載波自相關 $R_x(\tau)=\tfrac12\cos(\omega_0\tau)e^{-D|\tau|}$。
- Wiener-Khinchin → **Lorentzian** $S\propto\dfrac{D}{D^2+\Delta\omega^2}$：近載波轉平（峰 $=1/D$、不發散）、
  遠端回到 $1/f^2$、**總功率守恆**（積分 $=\pi$，有限）。
- **3-dB 線寬** $\Delta f_{3\mathrm{dB}}=\dfrac{D}{\pi}$ Hz；與 ISF 連結 $D=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$，
  故線寬 $=\dfrac{\Gamma_{rms}^2}{2\pi q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$——和 $\mathcal{L}$ 同一組旋鈕。
- canonical：5 GHz、$-100$ dBc/Hz@1MHz → $D\approx3.95\times10^3\ \text{rad}^2/\text{s}$、線寬 $\approx1.26$ kHz。
- 全套屬 [E2] Demir 2000 外部文獻、不在 5 篇 PDF 內（DOI 已查證）。

## 延伸閱讀

- 上游 $1/f^2$ 推導（本頁修正的對象）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- 相位積分的根（Wiener process 來源）：[convolution_derivation](/03_isf_core_theory/convolution_derivation)
- $\lambda_1=0$ 中性方向（為何相位無界漫步）：[derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)
- 時間版的同一漫步（accumulated jitter）：[lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
- 把 $\mathcal{L}$ 積回 rms jitter：[numerical_feeling](/04_simulation_labs/numerical_feeling)
- 外部文獻 [E2] Demir 2000 完整 citation：[references](/99_appendix/references)
