---
title: "[P4] 大注入 LC 模型與暫態行為（Sec. III-E/F、V 剩料）"
description: "Hong–Hajimiri 2019 Part II 剩料精讀：Mirzaei 廣義 Adler（[P4] Eq.(7)–(9)）如何從 ISF/(1+A)（Eq.(13)、(21)–(22)、(27)）長出來；正弦 Adler 的精確暫態解一行統一——tan 半角把鎖內 tanh（Eq.(31)–(32)）與鎖外 tan（Eq.(33)–(34)）分成同一條二次式的兩個符號；鎖定時間閉式與邊緣發散（lab_36 的 4.435 逐位重現）；APF 驅動的振幅暫態（dip→overshoot→settle）與 Table I 的斜率配方（τ_p×(1+a)）；大注入 pulling 的拍頻閉式（本站推導）與 AM 抬高的 k=0/k=2 梳線。lab_41 四面板數值全對數。"
---

# [P4] 大注入 LC 模型與暫態行為：精確 pull-in 解、鎖定時間、APF 振幅暫態與 pulling 頻譜

> **先備**：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)（APF 定義 [P4] Eq.(18)–(22)、ISF/APF quadrature Eq.(26)、augmented Adler Eq.(27)）、[lab_36](/04_simulation_labs/lab_36_lock_acquisition)（鎖內 Adler 的 $R$ 形式精確解、臨界慢化、cycle slips）、[injection_locking_noise](/06_design_insights/injection_locking_noise)（Part A 一階 PLL、Part B 拍頻 $\omega_b$ 與單邊梳）、[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)（$\tau_0=2Q/\omega_0$ 的振幅恢復、OU 過程）｜**接下來**：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) 的 M:N／ILFD 段、lab_37（`simulations/lab_37_ilfd_lock.py`，收在 paper_004 頁內）、[quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators)。

[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) 已經把 [P4] 的 **APF**（amplitude
perturbation function，振幅擾動函數）定義、ideal-LC 的 ISF/APF quadrature 與 M:N 次諧波鎖定講完。
這一頁收 [P4] **Sec. III-E/F（大注入 LC 模型）與 Sec. V（暫態行為）**剩下的料，並把它們教完：

> **這頁要回答什麼**：
> 1. 「振幅版 Adler」——Mirzaei 的 **Generalized Adler's equation**（[P4] Eq.(8)）——為什麼恰好等於 [P4] 的
>    $\tilde\Gamma/(1+A)$ 模型（Eq.(13)、(27)）？大注入 lock range $\omega_L=\omega_{L0}/\sqrt{1-a^2}$（Eq.(9)、(23)）
>    的 $a$ 到底是 $I_{inj}/I_{osc}$ 還是 $I_{inj}/I_{max}$？為什麼 $a\ge1$ 時模型「無界」？
> 2. 正弦 Adler 的**精確暫態解**怎麼來的？[P4] Eq.(31) 的 $\tanh$（鎖內）與 Eq.(33) 的 $\tan$（鎖外）為何長得一樣？
> 3. **鎖定要多久**？有沒有閉式？為什麼靠近 lock range 邊緣時鎖得上卻鎖得極慢？[P4] Table I 那個星號
>    「用 lock characteristic 的斜率算 $\tau_p$」是什麼配方？
> 4. 鎖定捕獲期間**振幅**在做什麼？APF 怎麼把相位暫態轉成振幅的 dip／overshoot？quasi-static 假設何時失效？
> 5. 鎖不住（pulling）時，大注入的**拍頻**還是 $\sqrt{\Delta\omega^2-\omega_L^2}$ 嗎？AM 對 pulling 頻譜做了什麼
>    （[P4] Fig. 14(c) 的 "ISF + APF" vs "ISF Only"）？

> **物理直覺（先講結論）**：注入電流同時「推相位」（ISF，切向）與「改振幅」（APF，徑向）。振幅改了，ISF 就跟著
> **反比縮放**（$\tilde\Gamma_{LC}=\tilde\Gamma/(1+A)$：擺幅大 → 同一顆電荷推出的相位小）。這一個回饋就把 Adler 的
> $\sin\theta$ 變成 $\sin\theta/(1+a\cos\theta)$——注入與振盪同相（$\theta\approx0$）時振幅被撐大、恢復力**變弱**、
> 鎖得**慢**；反相（$\theta\approx\pm\pi$）時振幅被吸乾、恢復力**變強**、lock characteristic 被拉高——所以 lock range
> 從 $\omega_{L0}$ 撐到 $\omega_{L0}/\sqrt{1-a^2}$，$a\to1$ 時「振幅歸零」的非物理解讓它發散。至於暫態：正弦 Adler
> 用 tan 半角代換後只剩一條**二次式**，判別式的符號一翻，鎖內的 $\tanh$（指數收斂、率 $\omega_p$）就變成鎖外的
> $\tan$（週期滑動、拍頻 $\omega_b$）——同一個畢氏根號 $\sqrt{\lvert\omega_L^2-\Delta\omega^2\rvert}$。

> **本頁定位**：進階 deep-dive（[P4] 剩料），**非核心教學章節**。以下標「✓ 已核實」者皆由本人放大原始 PDF 逐字對照：
> [P4] Eq.(5)–(9) 與 Sec. III-B 的 $\tau_0=2Q/\omega_0$（p.2123）、Eq.(13)（p.2124）、Eq.(20)–(22) 與 footnote 7
> （p.2126）、Eq.(23) 與 $\theta\in[-110^\circ,110^\circ]$ 的經驗限制（p.2127）、Eq.(24)–(27) 與 Fig. 8 caption
> （p.2128）、Eq.(31)–(34)、Table I 與其星號註（p.2130）、Fig. 13/Fig. 14 caption、Table II 與 amplitude-conscious
> 波形（p.2131–2132）、Eq.(35)–(38)（p.2132）。**本站自行推導、不在 [P4] 內**的部分明標：Eq.(31)/(33) 的逐步推導
> （[P4] 只寫 "one can show that [29]"）、大注入 pulling 的拍頻閉式（Sec. 5.2）、振幅一階遲滯模型（Sec. 4.3）。
> 外部文獻一律標「（外部文獻，非本站 5 篇 PDF）」並附 [P4] 參考書目中逐字核對的出處。

## 0. 符號與慣例對帳（先把 2 與正負號釘死）

| 量 | 本站寫法 | [P4] 寫法 | 對帳 |
|---|---|---|---|
| 失諧 | $\Delta\omega\equiv\omega_0-\omega_{inj}$ | $\Delta\omega\equiv\omega_{inj}/N-\omega_0$（p.2130） | 差一個整體正負號；本頁所有結果只依賴 $\Delta\omega^2$ 或明寫分支 |
| ISF-only 半 lock range | $\omega_{L0}\equiv\dfrac{I_{inj}}{2q_{max,0}}$ | $\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$，ideal LC $\lvert\tilde\Gamma_1\rvert=1/q_{max,0}$（Eq.(26)） | 那個 $\tfrac12$ 是**積化和差的 $\tfrac12$**（[P3] Eq.(34)–(35), p.2114，本站 injection_locking_noise 已核實），與 phase-noise 的 SSB $/4$ vs 時域 $/2$ 慣例無關 |
| 大注入半 lock range | $\omega_L\equiv\omega_{L0}/\sqrt{1-a^2}$ | Eq.(9)＝Eq.(23) at $\beta=90^\circ$ | 本頁凡寫 $\omega_L$ 皆指**含 APF 修正**的值；ISF-only 一律寫 $\omega_{L0}$ |
| 注入強度（LC 專用） | $a\equiv\dfrac{I_{inj}}{I_{osc}}$ | $\tfrac12 I_{inj}\lvert\Delta_1\rvert=\tfrac12\tau_0\dfrac{I_{inj}}{q_{max,0}}$ | 恆等式 $\omega_0 q_{max,0}=Q\,I_{osc}$（p.2124）⟹ $a=\tau_0\,\omega_{L0}$（精確） |
| 線性有效性 | $I_{inj}/I_{max}$，$I_{max}\equiv\omega_0 q_{max,0}$ | footnote 11, p.2130；Eq.(35), p.2132 | $I_{osc}=I_{max}/Q$（p.2132）：**兩個不同的歸一化**——$I_{max}$ 管一階線性是否成立，$I_{osc}$ 管 LC 的振幅效應多大 |
| 振幅記憶時間 | $\tau_0=2Q/\omega_0$ [s] | Sec. III-B, p.2123；Eq.(25), p.2128 | 是**振幅**時間常數；能量時間常數是 $Q/\omega_0$（差 2 倍，見 [tank_Q](/02_foundations/tank_Q_and_energy_restoration)） |
| 移位相位 | $\psi\equiv\theta+\pi/2$ | $N\tilde\theta\equiv N\theta+\angle\tilde\Gamma_N-\angle I_{inj}$ | ideal LC、餘弦注入、$N=1$：$\angle\tilde\Gamma_1=90^\circ$、$\angle I_{inj}=0$ ⟹ $\tilde\theta=\theta+\pi/2=\psi$ |

本頁除 Sec. 2 末段外全取 $N=1$（基波注入）。**dimension check 通用**：$[\omega_{L0}]=[\text{A}]/[\text{C}]=[\text{C/s}]/[\text{C}]=\text{rad/s}$ ✓（rad 無因次）；$[a]=[\text{s}]\cdot[\text{rad/s}]=$ 無因次 ✓。

## 1. 論文原文：本單元新增核實的段落（逐字轉錄）

### 1.1 既有模型：Adler 與 Mirzaei 的 Generalized Adler（[P4] Sec. III-A, p.2123 ✓）

Adler 方程（[P4] Eq.(5)）與 tank $Q$（Eq.(6)）：

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}\sin\theta,\qquad
Q=\frac{R_P}{\omega_0 L}=R_P\,\omega_0 C
$$

[P4] 原文（p.2123）："A powerful improvement to Adler's equation was derived by Mirzaei *et al.* [11], where they forgo
the assumption of a weak injection signal. ... the oscillation amplitude under injection is roughly given by"

$$
V_{osc}=(I_{osc}+I_{inj}\cos\theta)\,R_P\qquad\text{([P4] Eq.(7))}
$$

"which leads to an augmented differential equation for the oscillator's phase:"

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\omega_0}{2Q}\,\frac{I_{inj}\sin\theta}{I_{osc}+I_{inj}\cos\theta}\qquad\text{([P4] Eq.(8))}
$$

"The lock range associated with (8) was derived independently by a number of authors [9]–[12] to be"

$$
\omega_L=\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}\,\frac{1}{\sqrt{1-\dfrac{I_{inj}^2}{I_{osc}^2}}}\qquad\text{([P4] Eq.(9))}
$$

[P4] 隨即列出這個模型的三個限制（p.2123）：只處理正弦注入；$Q$ 與 $I_{osc}$ 受寄生影響難以準確決定、現代積體振盪器
未必能用 Fig. 1 的電路建模；預測的 lock range **對稱**，"which is not always the case [8], [12]"。同頁 Sec. III-B
的思想實驗明寫振幅時間常數："we assume that any excess amplitude decays exponentially with a time constant of
$\tau_0=2Q/\omega_0$ in between successive injections due to the energetics of the oscillator."

### 1.2 反比於振幅的有效 ISF 與 augmented pulling equation（[P4] Sec. III-C/E, p.2124 與 p.2126 ✓）

$$
\tilde\Gamma_{LC}=\frac{\tilde\Gamma}{1+A}\qquad\text{([P4] Eq.(13), p.2124)}
$$

p.2124 原文的物理："the oscillation amplitude controls the slope of the waveform (for a fixed oscillation frequency), and a
steeper waveform corresponds to a proportionally smaller phase shift from the same injection of charge." footnote 4 誠實
註記：這個反比關係**只在狀態變數互相正交（無 AM-to-PM）時精確成立**，LC 與 Bose 振盪器滿足。

振幅偏差（[P4] Eq.(20), p.2126）與 augmented pulling equation（Eq.(21)）：

$$
A=\frac{1}{T_{inj}}\int_{T_{inj}}\Delta\big(\omega_{inj}t+\theta\big)\,i_{inj}(t)\,dt
$$

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}+\frac{\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\tilde\Gamma\big(\omega_{inj}t+\theta\big)\,i_{inj}(t)\,dt}{1+\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\Delta\big(\omega_{inj}t+\theta\big)\,i_{inj}(t)\,dt}
$$

[P4] 稱之為 "quasi-nonlinear" 模型：非線性只藏在 ISF 與 APF 的**除法**裡，兩者各自仍線性於注入電流。正弦注入
$i_{inj}=I_{inj}\cos(\omega_{inj}t)$ 時只留基波（Eq.(22), p.2126；footnote 7：ideal LC 的 ISF/APF 是純正弦，其餘諧波
"effectively *filtered out*"）：

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}+\frac{\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert\cos(\theta+\angle\tilde\Gamma_1)}{1+\tfrac12 I_{inj}\lvert\Delta_1\rvert\cos(\theta+\angle\Delta_1)}
$$

### 1.3 不對稱 lock range 與模型的「無界」（[P4] Eq.(23), p.2127 ✓）

$$
\omega_L^{\pm}=\frac{\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert}{\tfrac12 I_{inj}\lvert\Delta_1\rvert\cos\beta\pm\sqrt{1-\big(\tfrac12 I_{inj}\lvert\Delta_1\rvert\sin\beta\big)^2}},\qquad
\beta\equiv\angle\tilde\Gamma_1-\angle\Delta_1
$$

原文（p.2127）："This lock range is generally asymmetric, meaning $\omega_L^+\ne-\omega_L^-$. ... Only in the specific
case of the ISF and the APF being in perfect quadrature with respect to each other ($\beta=\pm\pi/2$) is the lock range
symmetric." 以及本頁最重要的警語："the lock characteristic from (22) is no longer bounded for all $\theta$ when
$I_{inj}\lvert\Delta_1\rvert\ge2$, resulting in an infinite lock range [i.e., (23) no longer holds]. Physically, this is
because the fractional amplitude change $A$ is able to dip below $-1$ for certain values of $\theta$, corresponding to
the nonphysical scenario of an oscillation amplitude which is zero or negative." 處置："roughly restricting
$\theta\in[-110^\circ,110^\circ]$ for very large injection amplitudes usually results in reliable estimates of the lock
range."（footnote 8：Generalized Adler (8) 與 [9]–[12] 同樣在 $I_{inj}\ge I_{osc}$ 時預測無限 lock range。）

### 1.4 Ideal LC：從 ISF/APF 回到 Generalized Adler（[P4] Sec. III-F, p.2128 ✓）

$$
\tilde\Gamma(\varphi)=-\frac{1}{q_{max,0}}\sin\varphi,\qquad\tilde\Lambda(\varphi)=\frac{1}{q_{max,0}}\cos\varphi\qquad\text{(Eq.(24))}
$$

$$
d(t,\varphi)=e^{-t/\tau_0},\quad\tau_0=\frac{2Q}{\omega_0},\quad\int_0^\infty d\,dt=\tau_0\ \Longrightarrow\ \Delta(\varphi)=\tau_0\,\tilde\Lambda(\varphi)\qquad\text{(Eq.(25))}
$$

$$
\tilde\Gamma_1=\frac{1}{q_{max,0}}\angle90^\circ,\qquad\Delta_1=\frac{\tau_0}{q_{max,0}}\angle0\qquad\text{(Eq.(26))}
$$

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\tfrac12\dfrac{I_{inj}}{q_{max,0}}\sin\theta}{1+\tfrac12\tau_0\dfrac{I_{inj}}{q_{max,0}}\cos\theta}\qquad\text{(Eq.(27))}
$$

原文收尾："Finally, if we use the identity $\omega_0 q_{max,0}=QI_{osc}$ shown in Fig. 2(a) ... to eliminate the maximum
charge swing $q_{max,0}$, we arrive at Generalized Adler's equation (8)." **驗算**：$\tfrac12\tau_0 I_{inj}/q_{max,0}=\tfrac12\cdot\dfrac{2Q}{\omega_0}\cdot\dfrac{I_{inj}}{q_{max,0}}=\dfrac{Q\,I_{inj}}{\omega_0 q_{max,0}}=\dfrac{I_{inj}}{I_{osc}}=a$ ✓、
$\tfrac12 I_{inj}/q_{max,0}=\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}=\omega_{L0}$ ✓——Eq.(27) 逐項等於 Eq.(8)。
物理讀法：Mirzaei 用 $V_{osc}=(I_{osc}+I_{inj}\cos\theta)R_P$ 猜到的振幅，在 [P4] 框架裡就是 APF 的基波
$A=a\cos\theta$。

Fig. 8 caption（p.2128 ✓）給了本頁 Table I 反推要用的實際數字："Injection amplitudes of $I_{inj}=0.75$ mA and
$I_{inj}=1.5$ mA, respectively, for a CMOS differential *LC* oscillator with tank parameters $L=6$ nH, $C=4.15$ pF, and
$Q=15$ and biased at $I_{tail}=1$ mA, resulting in $I_{osc}=(4/\pi)$ mA and $2/\lvert\Delta_1\rvert=1.25$ mA. (c) Bipolar
Colpitts oscillator shown in Fig. 6 subjected to an injection amplitude of $I_{inj}=7.5$ mA." 同頁兩句話留給 Sec. 4：
"the stable mode must feature a negative lock characteristic slope, which also corresponds to the larger oscillation
amplitude"；以及模型的極限——"the deviation between theory and simulation near the center of the oscillation amplitude
plot for larger injection strengths ... occurs since nonlinear amplitude restoring effects, which are not captured by
the APF, are more prominent at larger oscillation amplitudes."

### 1.5 Sec. V-A Pull-In Process（p.2130 ✓）

原文設定："Suppose the injection is *within* the lock range ($\lvert\Delta\omega\rvert\lt\omega_L$) and $\theta_0$ denotes
the locked phase; i.e., $\Delta\omega\equiv\omega_{inj}/N-\omega_0=\Omega(\theta_0)$. Then one can show that [29]"

$$
\tan\!\left(\frac{N\tilde\theta}{2}\right)=\tan\!\left(\frac{N\tilde\theta_0}{2}\right)\tanh\!\left(\frac{\omega_p t+\phi_0}{2}\right)\qquad\text{([P4] Eq.(31))}
$$

"where we denoted $N\tilde\theta\equiv N\theta+\angle\tilde\Gamma_N-\angle I_{inj}$ out of convenience, $\phi_0$ is set by
initial conditions, and $\omega_p:=-\Omega'(\theta_0)$ is the *pull-in frequency*. As time persists and $\theta$
approaches $\theta_0$, the difference between them $\hat\theta$ approaches $\hat\theta\propto e^{-\omega_p t}$. (See
[1, Sec. V-F].)" 畢氏關係：

$$
\omega_p=N\sqrt{\omega_L^{\,2}-\Delta\omega^2}\qquad\text{([P4] Eq.(32))}
$$

**Table I（p.2130 ✓）THEORETICAL AND SIMULATED PULL-IN TIME CONSTANTS**：

| | Fig. 13(a) | Fig. 13(b) | Fig. 13(c) |
|---|---|---|---|
| Simulated $\tau_p/T_{inj}$ | $1/0.1667=6$ | $1/0.5358=1.87$ | $1/0.0590=16.9$ |
| Theoretical $\tau_p/T_{inj}$ | 5.95 | 1.79 | $17.4^{*}$ |

星號註（逐字）："$^*$To incorporate the APF into our prediction, we calculated $\tau_p$ directly from the slope of the
theoretical lock characteristic instead of from (32)." Fig. 13 caption：(a) 1-GHz 17-stage ring locked to a 1-GHz 1.5-mA
sinusoidal injection；(b) 同 ring、1-GHz 5-mA；(c) 1-GHz CMOS differential *LC* locked to a 1-GHz 0.5-mA injection。
三張圖的擬合式 $y=0.9983e^{-0.1667x}$、$1.0001e^{-0.5358x}$、$0.9988e^{-0.0590x}$（$R^2=1.0000$），橫軸為
"Number of Cycles"。$\tau_p\equiv1/\omega_p$。

### 1.6 Sec. V-B Spectrum of an Injection-Pulled Oscillator（p.2130–2132 ✓）

"If the injection is *outside* the lock range ($\lvert\Delta\omega\rvert\gt\omega_L$), then one can show that [29]"

$$
\tan\!\left(\frac{N\tilde\theta}{2}\right)=-\frac{1}{N}\frac{\omega_b}{\omega_L+\Delta\omega}\tan\!\left(\frac{\omega_b t+\phi_0}{2}\right)\qquad\text{([P4] Eq.(33))}
$$

$$
\omega_b:=N\sqrt{\Delta\omega^2-\omega_L^{\,2}}\qquad\text{([P4] Eq.(34))}
$$

"The tangent function has a period of $\pi$, and so $\theta(t)$ is periodic with the beat frequency $\omega_b$ (hence
its name). Thus, elementary phase modulation theory tells us that the distance between adjacent sidebands is
$\omega_b$." 以及 "The tone at one edge of the spectrum always occurs right at the injection frequency."

**Table II（p.2132 ✓）THEORETICAL AND SIMULATED BEAT FREQUENCIES**：Fig. 14(a) simulated $f_b=30.4$ MHz、theoretical
$f_b=\sqrt{\Delta f^2-f_L^{\,2}}=30.6$ MHz；Fig. 14(b) $6.8$ vs $6.6$ MHz。Fig. 14 caption：(a) 1-GHz 17-stage ring pulled
by a 1.04-GHz 1.5-mA sinusoidal injection；(b) 同 ring、0.97-GHz 1.5-mA；(c) 1-GHz bipolar Colpitts pulled by a 0.7-GHz
7.5-mA sinusoidal injection。p.2131："the oscillator shown in Fig. 14(b) is on the cusp of being locked—the injection is
only 0.7 MHz below the lower edge of the lock range. To account for amplitude modulation in the *LC* oscillator example
of Fig. 14(c), we solved the pulling equation of (21) and assumed the following amplitude-conscious form for the
oscillation voltage: $v_{osc}(t)\propto[1+A(t)]\cdot\cos[\omega_{inj}t+\theta(t)]$. As we can see, incorporating the APF
into the analysis improves the model's accuracy dramatically."

### 1.7 Sec. VI Injection Compliance（p.2132 ✓，只取與本頁有關的三式）

$$
\eta_N:=\frac{2\omega_L/\omega_0}{I_{inj}/I_{max}}\ \text{(Eq.(35))},\qquad
\eta_N=q_{max,0}\lvert\tilde\Gamma_N\rvert\ \text{(Eq.(36))},\qquad
\eta_{LC}:=\frac{2\omega_L/\omega_0}{I_{inj}/I_{osc}}=\frac{q_{max,0}}{Q}\lvert\tilde\Gamma_1\rvert\ \text{(Eq.(38))}
$$

**慣例 flag**：$\eta$ 用的是 **two-sided** lock range $2\omega_L$（"fractional, two-sided, sinusoidal lock range"）；本頁的
$\omega_L$ 是半寬。原文對 LC 的定性結論："for the same power consumption, an *LC* oscillator with a higher tank $Q$ has a
narrower lock range"（Table III：$\eta_{LC}=0.212$ CMOS diff.、$0.533$ NMOS-only diff.、$0.325$ MOS Colpitts）。ideal LC
的 $\eta_{LC}=q_{max,0}\cdot(1/q_{max,0})/Q=1/Q$——canonical $Q=10$ 給 $0.1$；量測的 CMOS 差動 LC（$Q=15$）為 0.212，
比 $1/Q=0.067$ 大 3 倍，這是實際 ISF 幅度大於 $1/q_{max,0}$（波形非純弦、注入節點的等效 $q_{max}$ 較小）的證據，
[P4] 沒有進一步拆解、本站也不猜。

## 2. 教學 (1)：正弦 Adler 的精確暫態解——一條二次式、兩個符號

[P4] 對 Eq.(31)、(33) 只寫 "one can show that [29]"（[29] 是 Hong 的博士論文，外部文獻，見文末）。這裡從頭推，並且
**一次推出兩式**。取 ideal LC、餘弦注入、$N=1$，本站慣例（Sec. 0）：

$$
\frac{d\theta}{dt}=\Delta\omega-\omega_{L0}\sin\theta,\qquad\Delta\omega=\omega_0-\omega_{inj}\ [\text{rad/s}].
$$

**第 1 步（把 lock characteristic 移成偶函數）**：令 $\psi\equiv\theta+\pi/2$（＝[P4] 的 $\tilde\theta$，Sec. 0），
$\sin\theta=-\cos\psi$：

$$
\frac{d\psi}{dt}=\Delta\omega+\omega_{L0}\cos\psi .
$$

鎖定點 $\cos\psi_0=-\Delta\omega/\omega_{L0}$；線性化 $d(\delta\psi)/dt=-\omega_{L0}\sin\psi_0\,\delta\psi$，穩定分支
$\sin\psi_0\gt0$，即 $\psi_0\in(0,\pi)$。**單位**：rad/s ＝ rad/s ＋ (rad/s)·無因次 ✓。

**第 2 步（Weierstrass 半角代換，同 lab_36／injection_locking_noise）**：$u\equiv\tan(\psi/2)$，
$\cos\psi=\dfrac{1-u^2}{1+u^2}$、$\dfrac{d\psi}{dt}=\dfrac{2}{1+u^2}\dfrac{du}{dt}$。代入、兩邊乘 $(1+u^2)$：

$$
2\frac{du}{dt}=\Delta\omega\,(1+u^2)+\omega_{L0}(1-u^2)
=\underbrace{(\omega_{L0}+\Delta\omega)}_{\gt0}-\underbrace{(\omega_{L0}-\Delta\omega)}_{\text{符號決定一切}}\,u^2 .
$$

這就是整頁的樞紐：右邊是 $u$ 的**二次式**，$u^2$ 項係數 $(\omega_{L0}-\Delta\omega)$ 的正負號決定解是 $\tanh$ 還是 $\tan$。
（$\Delta\omega\ge0$ 不失一般性；$\Delta\omega\lt0$ 用 $\theta\to-\theta$（即 $\psi\to\pi-\psi$）的對稱即得。）

**第 3 步 A（鎖內 $0\le\Delta\omega\lt\omega_{L0}$ → $\tanh$）**：令 $u_0^2\equiv\dfrac{\omega_{L0}+\Delta\omega}{\omega_{L0}-\Delta\omega}$，
則 $2\dot u=(\omega_{L0}-\Delta\omega)(u_0^2-u^2)$。用半角恆等式 $\tan^2(\psi_0/2)=\dfrac{1-\cos\psi_0}{1+\cos\psi_0}=\dfrac{1+\Delta\omega/\omega_{L0}}{1-\Delta\omega/\omega_{L0}}=u_0^2$——所以 $u_0=\tan(\psi_0/2)$ **就是鎖定點的半角正切**。
分離變數 $\displaystyle\int\frac{du}{u_0^2-u^2}=\frac{1}{u_0}\operatorname{artanh}\frac{u}{u_0}$（$\lvert u\rvert\lt u_0$）：

$$
\frac{2}{u_0}\operatorname{artanh}\frac{u}{u_0}=(\omega_{L0}-\Delta\omega)\,t+C
\ \Longrightarrow\
u=u_0\tanh\!\Big(\frac{(\omega_{L0}-\Delta\omega)\,u_0\,t+\phi_0}{2}\Big).
$$

而 $(\omega_{L0}-\Delta\omega)\,u_0=\sqrt{(\omega_{L0}-\Delta\omega)(\omega_{L0}+\Delta\omega)}=\sqrt{\omega_{L0}^2-\Delta\omega^2}\equiv\omega_p$。
寫回 $\psi=\tilde\theta$：

$$
\boxed{\ \tan\frac{\tilde\theta}{2}=\tan\frac{\tilde\theta_0}{2}\,\tanh\!\Big(\frac{\omega_p t+\phi_0}{2}\Big),\qquad\omega_p=\sqrt{\omega_{L0}^2-\Delta\omega^2}\ }
$$

——**逐字是 [P4] Eq.(31)–(32)（$N=1$）**。$\omega_p=\omega_{L0}\sin\psi_0=-\Omega'(\theta_0)$（$\Omega=\omega_{L0}\cos\psi$，
$\Omega'=-\omega_{L0}\sin\psi_0$）也對上 [P4] 的定義 $\omega_p:=-\Omega'(\theta_0)$ ✓。**單位**：$[\omega_p t]=$
(rad/s)(s)＝無因次 ✓；$\tanh$ 引數裡的 $/2$ 與 $u=\tan(\psi/2)$ 的半角是**同一個 2**（記帳，不是物理）：
$\tanh(z/2)\to1$ 的速率 $e^{-z}$，所以 $\hat\theta\propto e^{-\omega_p t}$、衰減率是 $\omega_p$ 而非 $\omega_p/2$。

**第 3 步 B（鎖外 $\Delta\omega\gt\omega_{L0}$ → $\tan$）**：現在 $\omega_{L0}-\Delta\omega\lt0$，寫成
$2\dot u=(\Delta\omega-\omega_{L0})(u^2+b^2)$，$b^2\equiv\dfrac{\Delta\omega+\omega_{L0}}{\Delta\omega-\omega_{L0}}\gt0$。
$\displaystyle\int\frac{du}{u^2+b^2}=\frac1b\arctan\frac ub$：

$$
u=b\tan\!\Big(\frac{(\Delta\omega-\omega_{L0})\,b\,t+\phi_0}{2}\Big),\qquad
(\Delta\omega-\omega_{L0})\,b=\sqrt{\Delta\omega^2-\omega_{L0}^2}\equiv\omega_b,\qquad
b=\frac{\omega_b}{\Delta\omega-\omega_{L0}}.
$$

換回 [P4] 的符號 $\Delta\omega_{[P4]}=-\Delta\omega$：$b=\dfrac{\omega_b}{-\Delta\omega_{[P4]}-\omega_{L0}}=-\dfrac{\omega_b}{\omega_L+\Delta\omega_{[P4]}}$——
**逐字是 [P4] Eq.(33)–(34)（$N=1$）** ✓。$\tan$ 週期 $\pi$ ⟹ $u$（故 $\psi$ mod $2\pi$）週期 $2\pi/\omega_b$：
每拍 $\theta$ 淨走 $2\pi$，這就是 [P4] 那句 "$\theta(t)$ is periodic with the beat frequency"。

**兩個分支的關係**：$b^2=-u_0^2$——同一個表達式 $\dfrac{\omega_{L0}+\Delta\omega}{\omega_{L0}-\Delta\omega}$，鎖內為正
（實根 $\pm u_0$＝穩定／不穩定鎖定點）、鎖外為負（無實根、$\dot u$ 恆正、永不停）。lab_36 的 $R$ 形式
$R(\theta)=R(\theta_0)e^{-\omega_c t}$ 與這裡的 $\tanh$ 形式由恆等式 $x=x_0\tanh z\Leftrightarrow\dfrac{x-x_0}{x+x_0}=-e^{-2z}$
互換（lab_36 第 2 步已寫）；$\tanh$ 分支只覆蓋起點落在 $(-\psi_0,\psi_0)$ 弧段（含 $\Omega$ 的峰）的初值，起點在另一弧段時
取 $\coth$、衰減率相同。**數值核實（lab_41）**：$r_0=\Delta\omega/\omega_{L0}=0.5$、$\theta(0)=0$，Eq.(31) 閉式與 RK4 整條
軌跡最大差 $2.16\times10^{-14}$ rad；$r_0=2.276$ 的 Eq.(33) 閉式跨 427 拍最大差 $3.32\times10^{-7}$ rad（浮點 unwrapping
累積）。

**推廣到 $N$ 次超諧波**（[P4] Sec. V 的一般式）：Eq.(30) 的 $\Omega(\theta)=\omega_L\cos(N\tilde\theta)$，
$d(N\tilde\theta)/dt=N\big[-\Delta\omega_{[P4]}+\omega_L\cos(N\tilde\theta)\big]$——把上面每個 $(\omega_{L0},\Delta\omega)$
換成 $(N\omega_L,N\Delta\omega)$、$\psi\to N\tilde\theta$，立刻得 $\omega_p=N\sqrt{\omega_L^2-\Delta\omega^2}$、
$\omega_b=N\sqrt{\Delta\omega^2-\omega_L^2}$、係數 $-\dfrac{N\sqrt{\cdot}}{N(\omega_L+\Delta\omega)}=-\dfrac1N\dfrac{\omega_b}{\omega_L+\Delta\omega}$ ✓——
Eq.(31)–(34) 的 $N$ 全部歸位。

## 3. 教學 (2)：鎖定（pull-in）時間閉式與邊緣發散

### 3.1 從 Eq.(31) 反解時間

把 $\tanh$ 反過來：$t(u)=\dfrac{2}{\omega_p}\Big[\operatorname{artanh}\dfrac{u}{u_0}-\operatorname{artanh}\dfrac{u(0)}{u_0}\Big]$。
定義「鎖定」為 $\theta$ 進入 $\theta_{ss}-\varepsilon$（本站與 lab_36 同用 $\varepsilon=0.01$ rad）：

$$
\boxed{\ T_{lock}=\frac{2}{\omega_p}\left[\operatorname{artanh}\frac{\tan\frac{\psi_0-\varepsilon}{2}}{\tan\frac{\psi_0}{2}}-\operatorname{artanh}\frac{\tan\frac{\psi(0)}{2}}{\tan\frac{\psi_0}{2}}\right]\ }\qquad[\text{s}]
$$

**單位**：$\operatorname{artanh}$ 無因次，$2/\omega_p$ 是 s ✓。**漸近展開**（$\varepsilon\ll1$）：
$\dfrac{\tan((\psi_0-\varepsilon)/2)}{\tan(\psi_0/2)}\approx1-\dfrac{\varepsilon}{\sin\psi_0}$，而
$\operatorname{artanh}(1-\delta)\approx\tfrac12\ln\dfrac{2}{\delta}$，所以

$$
T_{lock}\approx\frac{1}{\omega_p}\left[\ln\frac{2\sin\psi_0}{\varepsilon}-2\operatorname{artanh}\frac{u(0)}{u_0}\right]
=\tau_p\cdot\big[\text{幾個 }\ln\big],\qquad\tau_p\equiv\frac1{\omega_p}.
$$

$1/\omega_p$ 是主角，起點與門檻只進對數——與 lab_36 的結論一致。**數值**：$r_0=0.5$（$\theta_{ss}=30^\circ$、
$\psi_0=120^\circ$、$u_0=\tan60^\circ=\sqrt3$、$u(0)=\tan45^\circ=1$）、$\varepsilon=0.01$：精確閉式
$\omega_{L0}T_{lock}=4.435$，RK4 量測 $4.435$，**lab_36 用 $R$ 形式獨立算出的也是 4.435**——三路對上；漸近式給 4.431
（差 0.1%，是 $\operatorname{artanh}(1-\delta)$ 展開丟掉的 $O(\delta)$）。

### 3.2 邊緣發散（臨界慢化）

$\omega_p=\omega_{L0}\sqrt{1-r^2}$，$r=\Delta\omega/\omega_{L0}\to1$ 時 $\omega_p\approx\sqrt2\,\omega_{L0}\sqrt{1-r}\to0$、
$T_{lock}\propto(1-r)^{-1/2}\to\infty$：鎖定點 $\psi_0$ 與不穩定點 $-\psi_0$ 在 $\psi=0$ 合併（saddle-node），恢復力斜率歸零。
lab_36 量到 $\omega_{L0}T_{lock}$ 從 4.435（$r=0.5$）長到 22.913（$r=0.99$）；[P4] Table I 的三組 $\tau_p$ 就是在驗這條
$e^{-\omega_p t}$（$R^2=1.0000$）。**canonical 尺度**（本頁 $I_{inj}=1.5$ mA、$q_{max}=1$ pC ⟹ $f_{L0}=119.4$ MHz）：
$r_0=0.5$ 的 $T_{lock}=4.435/\omega_{L0}=5.913$ ns ＝ 29.6 個 5 GHz 週期；lab_36 的 $f_L=5$ MHz 尺度則是 141.2 ns（706 週期）
——同一個無因次 4.435，只差 $1/\omega_{L0}$。

### 3.3 大注入修正：Table I 星號的「斜率配方」

augmented 模型 $\dot\theta=\Delta\omega-\omega_{L0}\,g(\theta)$、$g(\theta)\equiv\dfrac{\sin\theta}{1+a\cos\theta}$，沒有像 Eq.(31)
那麼漂亮的 $\tanh$ 閉式，但 [P4] 的定義 $\omega_p:=-\Omega'(\theta_0)$ 直接可用——這正是 Table I 星號註的做法。逐步：

$$
g'(\theta)=\frac{\cos\theta\,(1+a\cos\theta)+a\sin^2\theta}{(1+a\cos\theta)^2}=\frac{\cos\theta+a}{(1+a\cos\theta)^2}
\ \Longrightarrow\
\boxed{\ \omega_p^{APF}=\omega_{L0}\,\frac{\cos\theta_0+a}{(1+a\cos\theta_0)^2}\ },\qquad
\frac{\sin\theta_0}{1+a\cos\theta_0}=\frac{\Delta\omega}{\omega_{L0}} .
$$

三件立刻可讀的事：

1. **穩定分支與 lock range 邊緣**：$g'\gt0\Leftrightarrow\cos\theta_0\gt-a$；$g$ 的極大在 $\cos\theta_{max}=-a$，
   $g_{max}=\dfrac{\sqrt{1-a^2}}{1-a^2}=\dfrac{1}{\sqrt{1-a^2}}$ ⟹ $\omega_L=\omega_{L0}/\sqrt{1-a^2}$——[P4] Eq.(9)＝Eq.(23) at
   $\beta=90^\circ$ ✓（lab_41 數值：$\max_\theta g=1.13811$ vs $1/\sqrt{1-a^2}=1.13811$）。$a\to1$ 時 $\theta_{max}\to180^\circ$、
   $1+a\cos\theta_{max}\to0$：振幅歸零的非物理解，就是 Sec. 1.3 那個「無界」（lab_41：$a=1.2$ 時分母在 $146.4^\circ$ 過零）。
2. **band centre 慢 $(1+a)$ 倍**：$\Delta\omega=0\Rightarrow\theta_0=0$，$\omega_p^{APF}=\omega_{L0}\dfrac{1+a}{(1+a)^2}=\dfrac{\omega_{L0}}{1+a}$，
   $\tau_p^{APF}=(1+a)\,\tau_p^{ISF}$。物理：同相注入把振幅撐成 $1+a$，有效 ISF 縮成 $1/(1+a)$（Eq.(13)），恢復力斜率就少
   $(1+a)$。canonical：$\tau_p^{ISF}=1/\omega_{L0}=1.333$ ns → $\tau_p^{APF}=1.970$ ns（9.8 個週期）。
3. **同一失諧下鎖定相位外移**：$r_0=0.5$ 時 ISF-only $\theta_{ss}=30.00^\circ$、$\omega_p/\omega_{L0}=0.8660$；augmented
   $\theta_0=42.53^\circ$、$\omega_p^{APF}/\omega_{L0}=0.6645$（慢 1.30 倍）、鎖定振幅 $1+a\cos\theta_0=1.3519$。RK4 擬合
   衰減率／公式：$1.0046$（ISF）、$1.0006$（APF）——線性化率就是全程率（[P4] Fig. 13 的 $R^2=1.0000$ 同義）。

**Table I(c) 的 ideal-LC 反推（估計，非精確重現）**：用 Fig. 8 caption 的 $Q=15$、$f_0=1$ GHz、$I_{osc}=(4/\pi)$ mA、
$I_{inj}=0.5$ mA、$\tfrac12 I_{inj}\lvert\Delta_1\rvert=0.5/1.25=0.40=a$，以恆等式 $q_{max,0}=QI_{osc}/\omega_0=3.04$ pC 得
$\omega_{L0}=I_{inj}/(2q_{max,0})$，ISF-only $\tau_p/T_{inj}=f_0/\omega_{L0}=12.2$，乘 $(1+a)$ 得 **17.0**——[P4] 的斜率配方給
17.4、電路模擬 16.9。差 2% 來自我們用 ideal-LC 的 $\lvert\tilde\Gamma_1\rvert=1/q_{max,0}$ 與 $I_{osc}$ 反推 $q_{max,0}$，
而 [P4] 用的是該電路實際萃取的 ISF/APF（其 $2/\lvert\Delta_1\rvert=1.25$ mA 就比 $I_{osc}=1.273$ mA 小 2%）。重點不在 17.0 對
17.4，而在**沒有 APF 時只有 12.2**：Table I(c) 的星號是 APF 把 pull-in 時間拉長 40% 的直接證據。

## 4. 教學 (3)：捕獲期間的振幅暫態（APF 驅動）

### 4.1 quasi-static 振幅：$A(t)=a\cos\theta(t)$

[P4] Eq.(20) 在 ideal LC、正弦注入下（Eq.(26)）就是 $A=\tfrac12 I_{inj}\lvert\Delta_1\rvert\cos(\theta+\angle\Delta_1)=a\cos\theta$。
它是**代數式**——振幅瞬間跟著 $\theta$ 走（quasi-static，準靜態）。配上 p.2131 的 amplitude-conscious 波形：

$$
v_{osc}(t)\propto\big[1+a\cos\theta(t)\big]\cos\big[\omega_{inj}t+\theta(t)\big].
$$

**物理**：$\theta=0$ 注入電流與振盪電壓同相 → 往 tank 灌功率 → 振幅 $1+a$；$\theta=\pm\pi$ 反相 → 抽功率 → $1-a$；
$\theta=\pm\pi/2$ 正交 → 只推相位不改振幅（ISF/APF quadrature 的時域版）。**單位**：$a$ 無因次、$A$ 是相對振幅偏差 ✓。

### 4.2 每個失諧兩個振幅：穩定＝較大那個

鎖定時 $\dfrac{\sin\theta_0}{1+a\cos\theta_0}=\dfrac{\Delta\omega}{\omega_{L0}}$ 在 $\lvert\Delta\omega\rvert\lt\omega_L$ 內有**兩個根**
（[P4] p.2128："two mathematical solutions for the phase $\theta$ and therefore also two possible oscillation
amplitudes"），穩定根在 $\cos\theta_0\gt-a$ 分支（Sec. 3.3 第 1 點），其振幅 $1+a\cos\theta_0\gt1-a^2$——
就是 Fig. 8 下排實線（穩定、大振幅）與虛線（不穩定、小振幅）那個閉環，lab_41 圖 (c) 的實／虛線是同一件事在
lock characteristic 上的投影。

### 4.3 暫態：dip → overshoot → settle，與 quasi-static 何時失效

把 Sec. 2 的 $\theta(t)$ 代進 $A=a\cos\theta$：若注入打開時 $\theta(0)$ 落在 $\cos\theta\lt0$ 的半圈（注入反相），振幅先
**低於**自由跑（dip）；$\theta$ 掃過 $0$ 時振幅衝到 $1+a$（overshoot）；最後停在 $1+a\cos\theta_0$。lab_41 (b) 用
$\theta(0)=-2$ rad、$r_0=0.5$：quasi-static 的 $A$ 從 $-0.1987$ 起、峰 $+0.4775$（$=a$，在 $\omega_{L0}t=1.97$）、終值
$+0.3519$，overshoot $0.1256$。

**quasi-static 的前提**是振幅「立刻」跟上相位——但 [P4] 自己的 APF 定義 Eq.(19) 是 decay function 的**時間積分**
（Fig. 5(c)："the APF is equal to the area under the amplitude deviation impulse response"），對 ideal LC
$d(t)=e^{-t/\tau_0}$。所以振幅其實是把「驅動 $a\cos\theta(t)$」通過一個時間常數 $\tau_0$ 的一階低通。**本站延伸
（不在 [P4] 內，標 illustrative）**：

$$
\tau_0\frac{dA}{dt}=a\cos\theta(t)-A,\qquad
\tau_0\,\omega_{L0}=a\ \Longrightarrow\ a\,\frac{dA}{d\tau}=a\cos\theta-A\quad(\tau\equiv\omega_{L0}t).
$$

推導只有一步：$A(t)=\displaystyle\int_0^\infty\frac{a\cos\theta(t-\tau')}{\tau_0}e^{-\tau'/\tau_0}\,d\tau'$（把 Eq.(17) 的
$D=\tilde\Lambda\,d$ 對基波做週期平均後，剩下慢變包絡與 $d/\tau_0$ 的卷積；歸一化使 $\theta$ 恆定時回到 Eq.(20) 的
$A=a\cos\theta$），微分即得。**單位**：$[\tau_0\dot A]=$ s·(1/s)＝無因次 ✓。**準靜態判準**：相位暫態的率 $\omega_p$ 對
振幅記憶 $1/\tau_0$——$\omega_p\tau_0=a\,\omega_p/\omega_{L0}\le a$。canonical $a=0.4775$、$r_0=0.5$：$\omega_p\tau_0=0.317$
——不算小。lab_41 (b) 的遲滯版：dip 只到 $-0.0443$（起點 $A(0)=0$：注入剛打開、振幅還沒反應）、峰 $+0.4577$、峰延後
$0.885$ ns、終值同為 $+0.3519$、相位軌跡幾乎不變（兩模型在 $\omega_{L0}t=24$ 時皆 $0.74223$ rad）。結論：**穩態與
lock range 不受遲滯影響，但暫態振幅的尖峰高度與時刻受 $\tau_0$ 抹平**；$a\ll1$（弱注入）時 quasi-static 精確，
$a\to1$ 時連 quasi-static 本身都是問題（Sec. 1.3 的無界）。[P4] p.2128 另指出**非線性振幅恢復**（APF 線性模型外）
在大振幅時更顯著——這是本頁模型的第二道天花板。

## 5. 教學 (4)：大注入 pulling——拍頻與 AM 抬高的梳線

### 5.1 ISF-only 的梳（回顧，已在站上）

[injection_locking_noise](/06_design_insights/injection_locking_noise) Part B 已推出 $\omega_b=\sqrt{\Delta\omega^2-\omega_{L0}^2}$、
梳線在 $\omega_{inj}+k\omega_b$、$k=0$ 恰在注入頻率、**嚴格單邊**且幾何遞減（比值 $\omega_{L0}/(\Delta\omega+\omega_b)$，
外部文獻 Armand 1969）。lab_41 (d) 的 ISF-only 曲線再驗一次：$r=2.276$ 時 $\omega_b/\omega_{L0}=2.0448$（Eq.(34)），量測
$2.0448$；幾何比 $0.2314$ ⟹ 每線 $-12.71$ dB，量測 $k_2-k_1=-12.71$、$k_3-k_2=-12.71$ dB；鏡像線 $-117.9$ dB（數值零）。

### 5.2 大注入的拍頻：本站閉式（[P4] 未給）

[P4] Eq.(34) 只對 ISF-only（或一般 lock characteristic 為純弦）成立；Fig. 14(c) 對 LC 是用數值解 Eq.(21) 畫的。
augmented 模型的拍頻可以精確積出來。無因次 $r\equiv\Delta\omega/\omega_{L0}$、$\tau=\omega_{L0}t$：

$$
\frac{d\theta}{d\tau}=r-\frac{\sin\theta}{1+a\cos\theta}
\ \Longrightarrow\
\omega_{L0}T_b=\oint\frac{(1+a\cos\theta)\,d\theta}{r+ra\cos\theta-\sin\theta}\equiv\oint\frac{(1+a\cos\theta)\,d\theta}{D(\theta)} .
$$

**第 1 步（分母寫成單一餘弦）**：$ra\cos\theta-\sin\theta=R\cos(\theta+\delta)$，$R^2=1+r^2a^2$，$\tan\delta=1/(ra)$。
鎖外 ⟺ $D\gt0$ 恆成立 ⟺ $r\gt R$ ⟺ $r^2(1-a^2)\gt1$ ⟺ $\Delta\omega\gt\omega_{L0}/\sqrt{1-a^2}=\omega_L$ ✓（與 Eq.(9) 自洽）。

**第 2 步（把分子拆成 $D$、$D'$ 與常數）**：解 $1+a\cos\theta=p\,D+q\,D'+s$，$D'=-ra\sin\theta-\cos\theta$。
比較 $\sin\theta$、$\cos\theta$、常數三個係數：$0=-p-qra$、$a=pra-q$、$1=pr+s$ ⟹

$$
p=\frac{ra^2}{R^2},\qquad q=-\frac{a}{R^2},\qquad s=\frac{1}{R^2}.
$$

（驗算：$pD+qD'+s=\dfrac{(r^2a^2+1)+a\cos\theta\,(r^2a^2+1)}{R^2}=1+a\cos\theta$ ✓。）

**第 3 步（三項分別繞一圈）**：$\oint p\,d\theta=2\pi p$；$\oint q\,D'/D\,d\theta=q\big[\ln D\big]_0^{2\pi}=0$（$D\gt0$ 週期）；
$\oint\dfrac{s\,d\theta}{r+R\cos(\theta+\delta)}=\dfrac{2\pi s}{\sqrt{r^2-R^2}}$（標準積分，$r\gt R$）。合計：

$$
\omega_{L0}T_b=\frac{2\pi}{R^2}\Big[ra^2+\frac1S\Big],\quad S\equiv\sqrt{r^2-R^2}=\sqrt{r^2(1-a^2)-1}
\ \Longrightarrow\
\boxed{\ \frac{\omega_b^{APF}}{\omega_{L0}}=\frac{R^2\,S}{1+ra^2S}\ }
$$

**單位**：$r,a,R,S$ 全無因次，$\omega_b^{APF}$ 以 $\omega_{L0}$ 計 ✓。**兩個極限**：$a\to0$：$R\to1$、$S\to\sqrt{r^2-1}$ ⟹
回到 Eq.(34) ✓；$S\to0$（$\Delta\omega\to\omega_L^+$）⟹ $\omega_b^{APF}\to0$：臨界慢化在**正確的**（augmented）邊緣發生 ✓。
**數值（$\Delta\omega=2\omega_L$，$r=2.2762$）**：閉式 $1.9896$、RK4 量測 $1.9897$（比 $1.0000$）；直接把 Eq.(9) 的 $\omega_L$
塞進 Eq.(34) 的「天真」算法 $\sqrt{r^2-1/(1-a^2)}=1.9713$ 差 0.9%——在這個 $a$ 下小，但**它不是正確公式**（$a$ 越大差越多）。
實際單位：$\Delta f=271.7$ MHz、$f_b^{ISF}=244.1$ MHz、$f_b^{APF}=237.5$ MHz。

### 5.3 AM 對頻譜做了什麼：$k=0$、$k=2$ 抬高，單邊性破口

相對 $\omega_{inj}$ 的複包絡（p.2131 的 amplitude-conscious 形式）：

$$
\big[1+a\cos\theta\big]e^{j\theta}=e^{j\theta}+\frac a2+\frac a2\,e^{j2\theta}.
$$

（$\tfrac a2$ 是 $\cos\theta=\tfrac12(e^{j\theta}+e^{-j\theta})$ 的 $\tfrac12$——展開記帳。）三項的頻譜意義：$e^{j\theta}$ 是
純相位梳；$\tfrac a2$ 是**直流**——精確落在 $\omega_{inj}$（$k=0$）上，把 [P4] 說的 "tone at one edge ... right at the
injection frequency" 那根抬高；$\tfrac a2e^{j2\theta}$ 是二倍相位，主要餵 $k\ge2$。lab_41 (d)（$\Delta\omega=2\omega_L$）
以整數拍窗精確算 Fourier 係數：

| 線（相對 $k=1$ 主線） | ISF-only | ISF+APF | 變化 |
|---|---|---|---|
| $k=0$（$\omega_{inj}$） | $-12.23$ dB | $-9.82$ dB | $\times1.299$（$+2.3$ dB） |
| $k=2$ | $-12.71$ dB | $-9.08$ dB | $\times1.494$（$+3.5$ dB） |
| $k=3$ | $-25.42$ dB | $-19.31$ dB | 幾何遞減變慢 |
| $k=-1$（鏡像側） | $-117.9$ dB（數值零） | $-30.4$ dB | **單邊性破口** |

鏡像線的歸因：只取 $e^{j\theta_{APF}(t)}$（不乘 AM 因子）算出 $k=-1$ 為 $-29.7$ dB——破口來自 augmented 模型的
$\theta(t)$ **不再是 Adler/Riccati 型**（Möbius 單邊論證失效），不是 AM 因子本身。這與 [P4] Fig. 14(c) 的訊息一致
（ISF+APF 才對得上電路模擬），但請記得這是 **quasi-static ISF+APF 模型內**的預測、非 transistor-level。

**Table II 反推（純算術，✓）**：由 [P4] 的理論 $f_b=\sqrt{\Delta f^2-f_L^2}$ 反解 $f_L$：(a) $\sqrt{40^2-30.6^2}=25.8$ MHz、
(b) $\sqrt{30^2-6.6^2}=29.3$ MHz ⟹ $\Delta f-f_L=0.7$ MHz——正是 p.2131 "only 0.7 MHz below the lower edge" ✓。順帶一讀：
同一顆 17 級 ring、同一個 1.5 mA，上邊 25.8 MHz、下邊 29.3 MHz——[P4] 所說「非 LC 的 lock range 一般不對稱」的數字版
（反推自 [P4] 的理論值，非本站量測）。

## 6. Worked example（canonical 數值，一行一驗證）

給定 $f_0=5$ GHz、$q_{max,0}=1$ pC、$Q=10$、$I_{inj}=1.5$ mA 正弦注入（本頁「大注入」代表值）。

1. **兩個歸一化**：$I_{max}=\omega_0q_{max,0}=2\pi\cdot5\times10^9\cdot10^{-12}=31.42$ mA；$I_{osc}=I_{max}/Q=3.142$ mA；
   $a=I_{inj}/I_{osc}=0.4775$、$I_{inj}/I_{max}=0.048$——線性有效（4.8%），但 LC 振幅效應大（48%）。
   dimension check：(rad/s)·C ＝ C/s ＝ A ✓。
2. **lock range**：$\omega_{L0}=I_{inj}/(2q_{max,0})=1.5\times10^{-3}/(2\times10^{-12})=7.5\times10^8$ rad/s ⟹ $f_{L0}=119.37$ MHz；
   $\omega_L=\omega_{L0}/\sqrt{1-a^2}=7.5\times10^8/0.8786=8.536\times10^8$ rad/s ⟹ $f_L=135.85$ MHz（撐大 13.8%）。
3. **振幅記憶**：$\tau_0=2Q/\omega_0=0.6366$ ns；核對恆等式 $\tau_0\omega_{L0}=0.4775=a$ ✓。
4. **鎖內 $\Delta\omega=0.5\,\omega_{L0}$（$\Delta f=59.7$ MHz）**：ISF-only $\theta_{ss}=30.0^\circ$、$\omega_p=0.866\,\omega_{L0}$
   ⟹ $\tau_p=1.540$ ns；augmented $\theta_0=42.53^\circ$、$\omega_p^{APF}=0.6645\,\omega_{L0}$ ⟹ $\tau_p^{APF}=2.007$ ns。
   鎖定時間（$\theta(0)=0\to\theta_{ss}-0.01$）：$\omega_{L0}T_{lock}=4.435$ ⟹ $5.913$ ns ＝ 29.6 個週期。
5. **band centre**：$\tau_p^{ISF}=1/\omega_{L0}=1.333$ ns、$\tau_p^{APF}=(1+a)/\omega_{L0}=1.970$ ns。
6. **鎖外 $\Delta\omega=2\omega_L$（$\Delta f=271.7$ MHz）**：$f_b^{ISF}=244.1$、$f_b^{APF}=237.5$、天真式 $235.3$ MHz。

```python
import numpy as np
from scipy.optimize import brentq
f0, qmax, Q, Iinj = 5e9, 1e-12, 10.0, 1.5e-3       # [Hz], [C], [-], [A]
w0 = 2 * np.pi * f0                                # [rad/s]
Imax = w0 * qmax                                   # [A]  I_max := w0*q_max,0  ([P4] fn.11, p.2130)
Iosc = Imax / Q                                    # [A]  I_osc = I_max/Q      ([P4] p.2132; w0*q_max,0 = Q*I_osc, p.2124)
a = Iinj / Iosc                                    # [-]  = (1/2)*tau0*Iinj/qmax = (1/2)*Iinj*|Delta_1|
print(round(Imax * 1e3, 2), round(Iosc * 1e3, 4), round(a, 4))          # -> 31.42 3.1416 0.4775
wL0 = Iinj / (2 * qmax)                            # [rad/s] ISF-only half lock range ([P3] Eq.(34)-(35))
wL = wL0 / np.sqrt(1 - a ** 2)                     # [rad/s] [P4] Eq.(9) = Eq.(23) at beta = 90 deg
print(round(wL0 / 2 / np.pi / 1e6, 2), round(wL / 2 / np.pi / 1e6, 2))  # -> 119.37 135.85
tau0 = 2 * Q / w0                                  # [s]  [P4] Sec. III-B, p.2123
print(round(tau0 * 1e9, 4), round(tau0 * wL0, 4))                         # -> 0.6366 0.4775
# (i) pull-in at Dw = 0.5*wL0: ISF-only [P4] Eq.(32) vs augmented slope recipe ([P4] Table I footnote)
r0 = 0.5
th_ss = np.arcsin(r0)                              # [rad] ISF-only locked phase
wp_isf = np.sqrt(1 - r0 ** 2)                      # [wL0] Eq.(32), N = 1
g = lambda th: np.sin(th) / (1 + a * np.cos(th)) - r0
th0 = brentq(g, -np.arccos(-a), np.arccos(-a))     # [rad] augmented locked phase (stable branch cos th + a > 0)
wp_apf = (np.cos(th0) + a) / (1 + a * np.cos(th0)) ** 2                 # [wL0] -Omega'(theta_0)/wL0
print(round(np.degrees(th_ss), 2), round(wp_isf, 4), round(np.degrees(th0), 2), round(wp_apf, 4))  # -> 30.0 0.866 42.53 0.6645
# (ii) lock time theta(0)=0 -> theta_ss - 0.01 rad from [P4] Eq.(31) (psi = theta + pi/2, alpha = tan(psi0/2))
eps = 0.01
psi0 = th_ss + np.pi / 2
alpha = np.tan(psi0 / 2)
T = (2 / wp_isf) * (np.arctanh(np.tan((psi0 - eps) / 2) / alpha) - np.arctanh(np.tan(np.pi / 4) / alpha))
print(round(T, 3), round(T / wL0 * 1e9, 3), round(T / wL0 * f0, 1))     # -> 4.435 5.913 29.6
print(round(1 / wL0 * 1e9, 3), round((1 + a) / wL0 * 1e9, 3))           # -> 1.333 1.97
# (iii) pulled at Dw = 2*wL: beat frequency, ISF-only Eq.(34) vs augmented closed form vs naive
r = 2 * wL / wL0
wb_isf = np.sqrt(r ** 2 - 1)                       # [wL0] [P4] Eq.(34), N = 1
R2 = 1 + (r * a) ** 2                              # [-]
S = np.sqrt(r ** 2 * (1 - a ** 2) - 1)             # [-]  -> 0 exactly at the augmented lock edge Dw = wL
wb_apf = R2 * S / (1 + r * a ** 2 * S)             # [wL0] site derivation (Sec. 5.2)
wb_naive = np.sqrt(r ** 2 - (wL / wL0) ** 2)       # [wL0] Eq.(34) with Eq.(9)'s wL plugged in
print(round(wb_isf * wL0 / 2 / np.pi / 1e6, 1), round(wb_apf * wL0 / 2 / np.pi / 1e6, 1),
      round(wb_naive * wL0 / 2 / np.pi / 1e6, 1))                        # -> 244.1 237.5 235.3
```

## 7. lab_41：大注入 LC 模型的四張面孔（模擬與圖）

### 7.1 模型（無因次 $\tau=\omega_{L0}t$；ideal-LC 動力學只依賴 $r=\Delta\omega/\omega_{L0}$ 與 $a$）

$$
\text{ISF-only：}\ \frac{d\theta}{d\tau}=r-\sin\theta;\qquad
\text{ISF+APF（[P4] Eq.(27)）：}\ \frac{d\theta}{d\tau}=r-\frac{\sin\theta}{1+A},\ A=a\cos\theta;\qquad
\text{遲滯（本站）：}\ a\frac{dA}{d\tau}=a\cos\theta-A .
$$

RK4 固定步長；(a) $d\tau=0.002$、$\tau_{max}=24$；(d) $d\tau=0.01$、$2^{17}$ 步（≈427 拍），頻譜以整數拍窗取 Fourier 係數
（無 leakage／scalloping），作圖用 Hann 窗＋4 倍零填。

### 7.2 參數表

| 參數 | 值 | 單位 | 來源／說明 |
|---|---|---|---|
| $f_0$ | 5 | GHz | canonical |
| $q_{max,0}$ | 1 | pC | canonical |
| $Q$ | 10 | — | canonical（[tank_Q](/02_foundations/tank_Q_and_energy_restoration)、phase_vs_amplitude_noise §5.6） |
| $I_{inj}$ | 1.5 | mA | 「大注入」代表值 |
| $I_{max}=\omega_0q_{max,0}$ | 31.42 | mA | [P4] fn.11 |
| $I_{osc}=I_{max}/Q$ | 3.142 | mA | [P4] p.2132 |
| $a=I_{inj}/I_{osc}$ | 0.4775 | — | $=\tau_0\omega_{L0}$ |
| $\omega_{L0}$／$f_{L0}$ | $7.5\times10^8$／119.37 | rad/s／MHz | ISF-only |
| $\omega_L$／$f_L$ | $8.536\times10^8$／135.85 | rad/s／MHz | Eq.(9) |
| $\tau_0=2Q/\omega_0$ | 0.6366 | ns | 3.18 個週期 |
| (a)(b) 失諧 | $r_0=0.5$ | — | $\Delta f=59.7$ MHz |
| (d) 失諧 | $\Delta\omega=2\omega_L$（$r=2.2762$） | — | $\Delta f=271.7$ MHz |
| 鎖定門檻 $\varepsilon$ | 0.01 | rad | 同 lab_36 |

### 7.3 單位表

| 量 | 單位 | 備註 |
|---|---|---|
| $\theta,\psi,\varepsilon$ | rad | 相對相位 |
| $\Delta\omega,\omega_{L0},\omega_L,\omega_p,\omega_b$ | rad/s | 圖上以 $\omega_{L0}$ 歸一 |
| $a,A,r,R,S$ | — | 無因次 |
| $\tau_0,\tau_p,T_{lock},T_b$ | s | 圖 (b) 用 ns |
| 頻譜 | dB | 相對 $k=1$ 主線功率 |

### 7.4 圖

![lab_41：(a) 鎖定捕獲的歸一化相位偏差（semilog）——ISF-only RK4、[P4] Eq.(31) tanh 閉式（圈）、e^(−ω_p t)（虛線），與 ISF+APF 的較慢 pull-in；(b) 捕獲期間的振幅 1+A(t)：quasi-static vs 一階遲滯，右軸 θ(t)；(c) 大注入 lock characteristic sinθ/(1+a cosθ)，a=0/0.477/0.9 與無界的 a=1.2；(d) pulled 頻譜（Δω=2ω_L）：ISF-only 單邊梳 vs ISF+APF 抬高 k=0、k=2 並出現鏡像線](/figures/large_injection_transient.png)

### 7.5 如何解讀

- **(a)**：縱軸 $\lvert\hat\theta(t)\rvert/\lvert\hat\theta(0)\rvert$（[P4] Fig. 13 同一種圖），橫軸 $\omega_{L0}t$。藍線（ISF-only RK4）
  被圈（Eq.(31) 閉式）與虛線 $e^{-\omega_pt}$、$\omega_p=0.866\,\omega_{L0}$ 完全蓋住；紅線（ISF+APF）斜率 $0.6645$——
  Table I 星號配方的 $-\Omega'(\theta_0)$。兩條都是直線：線性化率＝全程率。
- **(b)**：橫軸真實 ns。橘（quasi-static）從 $0.80$ 起、衝到 $1.4775$、落回 $1.3519$（黑點線）；綠（遲滯）起點 $1.0$（注入剛開）、
  峰 $1.4577$ 且晚 0.885 ns；紫（右軸）$\theta$ 從 $-115^\circ$ 爬到 $42.5^\circ$。灰虛線 $1.0$＝自由跑。
- **(c)**：$\Delta\omega/\omega_{L0}=\sin\theta/(1+a\cos\theta)$。實線穩定（$\cos\theta+a\gt0$）、虛線不穩定；點線是各自的邊緣
  $1/\sqrt{1-a^2}$（$a=0$：1；$0.477$：1.138；$0.9$：2.294）。$a=1.2$ 只畫 $\lvert\theta\rvert\le110^\circ$（[P4] p.2127 的經驗限制），
  分母在 $146.4^\circ$ 過零、曲線無界。注意 $a\gt0$ 的曲線在 $\theta\lt0$ 側被壓低、$\theta\gt0$ 側先被壓後被拉高：
  這就是「同相變弱、反相變強」。
- **(d)**：橫軸 $(\omega-\omega_{inj})/\omega_b$（各自的 $\omega_b$），縱軸相對 $k=1$。藍（ISF-only）$k\lt0$ 全空、$k\ge2$
  每線 $-12.71$ dB；紅（ISF+APF）$k=0$ 抬 2.3 dB、$k=2$ 抬 3.5 dB、$k=-1$ 冒出 $-30$ dB 的鏡像線。

### 7.6 核對數字（`PYTHONPATH=. python3 simulations/lab_41_large_injection_transient.py`，單機 1.7 s）

```bash
# -> 0.4775  a = I_inj/I_osc ; tau0*omega_L0 = 0.4775 (= a, 恆等式)
# -> 119.37 / 135.85 MHz  f_L0 (ISF-only) / f_L (Eq.9)，比 1.1381 = 1/sqrt(1-a^2)
# -> 1.00000  edge check: max_theta sin/(1+a cos) 對 1/sqrt(1-a^2) 的比
# -> 2.16e-14 rad  (a) Eq.(31) 閉式 vs RK4 整條軌跡最大差
# -> 4.435 / 4.435  (a) omega_L0*T_lock 閉式 / RK4（lab_36 獨立值 4.435）
# -> 0.8660 / 0.8700  (a) ISF-only omega_p/omega_L0：Eq.(32) / RK4 擬合（比 1.0046）
# -> 42.53 deg, 0.6645 / 0.6649  (a) augmented theta_0、omega_p/omega_L0：斜率配方 / RK4 擬合（比 1.0006）
# -> 1.4775  (a) Dw=0: tau_p(APF)/tau_p(ISF) = 1+a ; 1.333 ns -> 1.970 ns = 9.8 cycles
# -> 17.0  (a) Table I(c) ideal-LC 反推 tau_p/T_inj（paper 17.4*，simulated 16.9；ISF-only 只有 12.2）
# -> -0.1987 / +0.4775 / +0.3519  (b) quasi-static A_min / A_max / A_final（overshoot 0.1256）
# -> -0.0443 / +0.4577 / +0.3519  (b) 遲滯版 A_min / A_max / A_final；峰延後 0.885 ns；omega_p*tau0 = 0.317
# -> 3.32e-07 rad  (d) Eq.(33) 閉式 vs RK4，427 拍
# -> 2.0448 / 2.0441  (d) ISF-only omega_b/omega_L0：Eq.(34) / 量測
# -> 1.9896 / 1.9897 / 1.9713  (d) augmented omega_b/omega_L0：本站閉式 / 量測 / 天真式
# -> 244.1 / 237.5 MHz  (d) f_b ISF-only / augmented（Df = 271.7 MHz）
# -> 25.8 / 29.3 / 0.7 MHz  (d) Table II 反推 f_L(a) / f_L(b) / Df-f_L(b)
# -> -12.23 -12.71 -25.42 -117.9  (d) ISF-only 梳線 k0 k2 k3 mirror [dB rel. k1]
# -> -9.82 -9.08 -19.31 -30.4  (d) ISF+APF 梳線 k0 k2 k3 mirror [dB rel. k1]
# -> 0.2314 / -12.71  (d) 幾何比 omega_L0/(Dw+omega_b) / 每線步階 dB（量測 k2-k1 -12.71、k3-k2 -12.71）
# -> 1.299 / 1.494  (d) k0、k2 線的 (ISF+APF)/(ISF-only) 幅度比
# -> -29.7  (d) 只取 e^{j theta_APF}（不乘 AM）的鏡像線 dB：破口來自 theta(t)，非 AM 因子
```

完整 script：`simulations/lab_41_large_injection_transient.py`（依賴 `simulations/common/plot_utils.py` 的 `savefig`、
`scipy.optimize.brentq`；決定論、無 seed）。**限制**：pedagogical toy（ideal-LC ISF/APF，非 transistor-level）；quasi-static
APF 與一階遲滯皆線性振幅模型（無非線性恢復）；(d) 以整數拍窗算線幅，鏡像線 $-117.9$ dB 是浮點底。

## 8. 適用／失效條件與誠實範圍

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 一階線性（$I_{inj}\ll I_{max}=\omega_0q_{max,0}$，[P4] fn.11） | ISF、APF 各自線性於注入 | 強注入：ISF/APF 本身隨注入變形（[P4] Sec. III-E 稱 quasi-nonlinear，只捕捉除法那一層） |
| $a=I_{inj}/I_{osc}\lt1$ | Eq.(9)/(23) 有界、lock characteristic 有極值 | $a\ge1$：$1+A$ 可歸零，lock range 無界（非物理）；[P4] 經驗上限 $\theta\in[-110^\circ,110^\circ]$ |
| ideal LC：純弦 ISF/APF、$\beta=90^\circ$ | Eq.(27)＝Generalized Adler (8)、對稱 lock range、$\tanh$／$\tan$ 閉式 | 實際 LC：$\beta\ne90^\circ$ ⟹ 不對稱（Eq.(23)）、Eq.(31)/(33) 要用 $N\tilde\theta$ 的一般形式；非 LC 振盪器：Sec. 2 的推導仍對純弦 lock characteristic 成立，但 $\tilde\Gamma_{LC}=\tilde\Gamma/(1+A)$ 只對狀態變數正交的振盪器精確（fn.4） |
| quasi-static 振幅（$\omega_p\tau_0=a\,\omega_p/\omega_{L0}\ll1$） | $A=a\cos\theta(t)$ 逐點成立 | $a$ 不小：振幅落後、峰被抹平（Sec. 4.3 遲滯模型，illustrative）；穩態不受影響 |
| 線性振幅恢復（$d=e^{-t/\tau_0}$） | APF 積分＝$\tau_0\tilde\Lambda$ | 大振幅：非線性振幅恢復（[P4] p.2128 承認 APF 未捕捉，Fig. 8 中央偏差） |
| 決定論、無雜訊 | 本頁全部 | 加雜訊：鎖內整形／cycle slips 見 injection_locking_noise Part A、lab_36 Part b；[P4] p.2130 把「用 pulling equation 分析 phase noise」交給 [29, Ch. 7]（外部） |

**什麼仍是外部、本站沒有做**：(i) Eq.(31)/(33) 的 [P4] 原始推導在 Hong 的博士論文 [29]（本站以 Sec. 2 自證）；
(ii) Mirzaei 等人的 Generalized Adler 原始推導 [11] 與 [9]、[10]、[12] 的 lock range 推導（本站只用 [P4] 轉述的 Eq.(7)–(9)）；
(iii) pulling 梳的幾何閉式（Armand 1969）；(iv) 非線性振幅恢復、AM-to-PM、電路級（Spectre／PDK）驗證——本站的
Level-1 方程級模型做不到，Table I/II 的電路模擬值只能引用不能重現。

## 重點回顧

- **Generalized Adler ＝ ISF/(1+A)**：[P4] Eq.(27) 逐項等於 Eq.(8)，橋樑是恆等式 $\omega_0q_{max,0}=QI_{osc}$ 與
  $a=I_{inj}/I_{osc}=\tfrac12\tau_0I_{inj}/q_{max,0}=\tau_0\omega_{L0}$；lock range $\omega_{L0}/\sqrt{1-a^2}$（Eq.(9)＝Eq.(23) at
  $\beta=90^\circ$）；$a\ge1$ 無界＝振幅歸零的非物理解。**$I_{max}$ 管線性、$I_{osc}$ 管振幅效應**——兩個不同的歸一化。
- **一條二次式、兩個符號**：$2\dot u=(\omega_{L0}+\Delta\omega)-(\omega_{L0}-\Delta\omega)u^2$，$u=\tan(\tilde\theta/2)$。鎖內 →
  $\tanh$、率 $\omega_p=\sqrt{\omega_{L0}^2-\Delta\omega^2}$（Eq.(31)–(32)）；鎖外 → $\tan$、拍頻 $\omega_b=\sqrt{\Delta\omega^2-\omega_{L0}^2}$
  （Eq.(33)–(34)）。$\tanh$ 的 $/2$ 是半角記帳，衰減率仍是 $\omega_p$。
- **鎖定時間**：$T_{lock}=\dfrac{2}{\omega_p}[\operatorname{artanh}-\operatorname{artanh}]\approx\tau_p[\ln(2\sin\psi_0/\varepsilon)+\dots]$，
  $r_0=0.5$、$\varepsilon=0.01$ 給 $\omega_{L0}T=4.435$（與 lab_36 逐位相同）；邊緣 $\propto(1-r)^{-1/2}$ 發散。
- **APF 讓 pull-in 變慢**：$\omega_p^{APF}=\omega_{L0}(\cos\theta_0+a)/(1+a\cos\theta_0)^2$（Table I 星號的斜率配方）；band centre
  $\tau_p\times(1+a)$；Table I(c) ideal-LC 反推 17.0（paper 17.4／16.9；無 APF 只有 12.2）。
- **振幅暫態**：$A=a\cos\theta(t)$ ⟹ dip → overshoot（到 $1+a$）→ settle 在 $1+a\cos\theta_0$；穩定解＝大振幅；quasi-static 判準
  $\omega_p\tau_0\ll1$，canonical 為 0.317——遲滯抹平峰值、不改穩態。
- **大注入 pulling**：拍頻閉式 $\omega_b^{APF}/\omega_{L0}=R^2S/(1+ra^2S)$（本站推導；$a\to0$ 回 Eq.(34)、$S\to0$ 在 augmented 邊緣）；
  AM 因子 $=e^{j\theta}+\tfrac a2+\tfrac a2e^{j2\theta}$ 抬高 $k=0$（$\times1.30$）、$k=2$（$\times1.49$），鏡像線 $-30$ dB 來自非 Adler 的
  $\theta(t)$——[P4] Fig. 14(c) "ISF + APF" 的機制。

## 延伸閱讀

- [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)：APF 定義、quadrature、Eq.(27) 的來源與 M:N／ILFD——本頁的前半。
- [lab_36](/04_simulation_labs/lab_36_lock_acquisition)：同一個鎖內精確解的 $R$ 形式、$r$ 掃描到 0.99 的臨界慢化、加雜訊後的 cycle slips。
- [injection_locking_noise](/06_design_insights/injection_locking_noise)：Part A 鎖內雜訊整形（corner 就是 $\omega_p$）、Part B 拍頻與單邊梳（Armand）、注入波形設計。
- [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)：$\tau_0=2Q/\omega_0$ 的振幅恢復、OU 過程與平頂 Lorentzian——本頁遲滯模型的雜訊版。
- [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1)：廣義 Adler、lock characteristic、$\omega_p:=-\Omega'(\theta_0)$ 的原始定義（[P3] Eq.(38)–(40)）。
- [tank_Q](/02_foundations/tank_Q_and_energy_restoration)：$Q$、$2Q/\omega_0$ vs $Q/\omega_0$、canonical $Q=10$ 的來源。
- lab_37（`simulations/lab_37_ilfd_lock.py`，收在 [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) 頁內）：$N\ne1$ 時 Eq.(31)–(34) 的 $N$ 怎麼進來（鎖外漂移率 $\omega_b/N$）。

### 外部文獻（不在下載的 5 篇 PDF 內；出處逐字取自 [P4] 參考書目 p.2138）

- **[P4]-[11]** A. Mirzaei, M. E. Heidari, R. Bagheri, S. Chehrazi, and A. A. Abidi, *"The quadrature LC oscillator: A complete
  portrait based on injection locking,"* IEEE J. Solid-State Circuits, vol. 42, no. 9, pp. 1916–1932, Sep. 2007.
  （Generalized Adler's equation 與 $V_{osc}=(I_{osc}+I_{inj}\cos\theta)R_P$ 的原始出處。）
- **[P4]-[9]** L. J. Paciorek, *"Injection locking of oscillators,"* Proc. IEEE, vol. 53, no. 11, pp. 1723–1727, Nov. 1965；
  **[P4]-[10]** B. Razavi, *"A study of injection locking and pulling in oscillators,"* IEEE J. Solid-State Circuits, vol. 39,
  no. 9, pp. 1415–1424, Sep. 2004；**[P4]-[12]** B. Hong and A. Hajimiri, *"A phasor-based analysis of sinusoidal injection
  locking in LC and ring oscillators,"* IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 66, no. 1, pp. 355–368, Jan. 2019.
  （[P4] p.2123 所稱「獨立導出 Eq.(9)」的 [9]–[12]。）
- **[P4]-[29]** B. Hong, *"Periodically disturbed oscillators,"* Ph.D. dissertation, Dept. Elect. Eng., California Inst.
  Technol., Pasadena, CA, USA, 2018. doi: 10.7907/W0A7-4258.（Eq.(31)、(33) 的原始推導、Ch. 7 的 phase-noise-via-pulling-equation。）
- **[E-Armand]** M. Armand, *"On the Output Spectrum of Unlocked Driven Oscillators,"* Proc. IEEE, vol. 57, no. 5, pp. 798–799,
  May 1969.（ISF-only pulling 梳的單邊幾何閉式；已列於 injection_locking_noise。）
