---
title: 從波形直接算 ISF：[P1] 附錄的三種方法
description: 逐字轉錄並逐步推導 [P1] 附錄「Calculation of the Impulse Sensitivity Function」的三種 ISF 計算法——打脈衝直接量測、state-space 投影 closed form Γ=f′/(f′²+f″²)、一階導數近似 Γ=f′/f′²max——並在 van der Pol 上做「三法對決」，誠實量化 closed form 何時可用、何時失準。
---

# 從波形直接算 ISF：[P1] 附錄的三種方法

> **先備**：[isf_definition](/03_isf_core_theory/isf_definition)（$\Gamma$ 的定義、切向投影直覺）、[waveform_slope](/06_design_insights/waveform_slope)（$1/\text{slope}$ heuristic 與它在波峰發散的問題）｜**接下來**：[derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)（嚴格 adjoint/PPV，本頁「真值」的來源）、[lab_32](/04_simulation_labs/lab_32_mos_level1_ring)（方程級 ring 上實作打脈衝法）

前面幾頁把 $\Gamma(\omega_0\tau)$ 定義得很清楚，但留了一個非常實務的問題：**手上有一個振盪器
（SPICE netlist、方程、或量測到的穩態波形），$\Gamma$ 到底怎麼「算」出來？**
[P1] 的附錄「Calculation of the Impulse Sensitivity Function」（[P1] pp.192–193）給了三種方法，
從最準到最快排成一個光譜。本頁把三種方法**逐字轉錄、逐步推導、標清楚各自的失效條件**，
最後在同一顆 van der Pol 振盪器上讓三法對決，把「差多少」變成數字。

> **物理直覺（先講結論）**：三種方法其實是同一件事的三個層次。**方法 A**（打脈衝）是「直接做實驗」：
> 戳一下、量相位偏移，什麼都不假設，所以最準、也最慢。**方法 B**（closed form）是「用幾何代替實驗」：
> 假設戳出去的位移中，只有**沿軌跡切向**的分量留下相位——把實驗換成一個內積，只要一個週期的波形就能算。
> **方法 C**（一階導數）再砍一刀：假設分母（軌跡「速率」平方）近似常數，$\Gamma$ 就直接正比波形斜率。
> 每砍一刀就快一截、也多一個會失效的假設。本頁的核心教訓是：**方法 B 的「切向投影」偷偷假設了
> 「振幅擾動衰減時不留相位」——振幅–相位耦合（AM→PM）一出現，它就開始漏**。

## 方法 A：直接量脈衝響應（[P1] Appendix A, p.192）

[P1] p.192 的描述（轉錄自原文）：在波形的**不同相對相位**注入一個 impulse，讓振盪器多跑幾個
週期；把脈衝注入時刻掃過一整個週期、量每次造成的時間偏移 $\Delta t$，就能得到
$h_\phi(t,\tau)$，換算用的關係是

$$
\Delta\phi=2\pi\,\frac{\Delta t}{T},
$$

其中 $T$ 是振盪週期（[P1] p.192；這正是 [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) 用過的相位–時間換算）。原文並提到多數 SPICE 實作可自動做這個 sweep，且每個
impulse 只需要模擬幾個週期，執行很快；得到 $h_\phi(t,\tau)$ 後「**乘上 $q_{max}$ 就得到 ISF**」
（對照 [P1] Eq.(10)：$h_\phi=\Gamma/q_{max}\cdot u(t-\tau)$，所以 $\Gamma=q_{max}h_\phi$ 的步階高度）。

[P1] 對它的評價（p.192，原文）：*"This method is the most accurate of the three methods presented."*
——**三法中最準**。代價是要做 $N_{phase}$ 次 transient（每個注入相位一次）。

- **單位檢查**：$\Delta\phi=2\pi\,[\text{s}]/[\text{s}]=$ rad ✓；$\Gamma=q_{max}\cdot h_\phi$，$[C]\cdot[\text{rad/C}]=$ 無因次 ✓。
- 本站已三度實作這個方法：正弦振盪器（[lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep)，誤差 ~0.001）、van der Pol（[lab_15](/04_simulation_labs/lab_15_nonlinear_isf)）、MOS Level-1 方程級 ring（[lab_32](/04_simulation_labs/lab_32_mos_level1_ring)）。
- **注意 wrap-around**：$\Delta t$ 要摺回 $[-T/2,\,T/2)$ 再換算，否則相位差一整圈（lab_15/lab_32 的實作細節）。

## 方法 B：從波形來的 closed form（[P1] Appendix B, pp.192–193）

### 第 1 步：把擾動投影到「運動方向」——Eq. (31)

考慮 $n$ 階系統的 state-space 軌跡（[P1] Fig. 29, p.192：*"State-space trajectory of an
$n$th-order oscillator"*）。一群外部 impulse 的效果是一個擾動向量 $\Delta\vec X$，把狀態瞬間改成
$\vec X+\Delta\vec X$。原文的關鍵假設句（p.192，逐字）：*"As discussed earlier, amplitude
variations eventually die away, but phase variations do not."*——振幅擾動終會消散、相位擾動不會。
於是要算等效時間偏移，就把擾動投影到**單位速度向量**（normalized velocity vector）上（[P1] Eq.(31), p.192）：

$$
l=\Delta\vec X\cdot\frac{\dot{\vec X}}{\bigl|\dot{\vec X}\bigr|}
$$

- $l$ 是「沿軌跡的等效位移」（原文：*equivalent displacement along the trajectory*），$\dot{\vec X}$ 是狀態向量的一階導數（軌跡的「速度」）。
- **單位檢查**：設狀態都是電壓，$[\Delta\vec X]=$ V、$\dot{\vec X}/|\dot{\vec X}|$ 無因次 → $l$ 單位 V ✓（位移與狀態同單位）。
- **隱藏假設一**：內積要求各狀態分量**同單位／同尺度**。狀態混了 V 與 A（例如 LC 的 $v_C,i_L$）就要先 normalize，而 normalize 的方式會改答案（見「失效條件」）。

下圖把 Fig. 29 的 state-space 圖景（左）與 Fig. 30 的三法對比（右，方法 C 那節會回頭引用）用本站的 van der Pol toy 實算復刻出來：

![[P1] Fig. 29 與 Fig. 30 的概念復刻：左為 van der Pol μ=2.0 實算的 state-space 軌跡（粗線極限環、狀態向量、擾動向量、重返軌跡與 Δφ），右為 μ=0.2 上三種 ISF 計算法的單色對比](/figures/p1_fig2930_replica.png)

**概念復刻，非原圖數位化**。左：對應 [P1] Fig. 29（p.192），原標題逐字：*"State-space trajectory of an $n$th-order oscillator."*——原圖是 $n$ 維示意手繪（未指定系統）；復刻改用 van der Pol（μ=2.0）**實算**：粗線＝極限環，細線＝在 $x$ 軸踢 $\Delta x=0.45$（刻意放大以便看圖）後真實積分出來的重返軌跡，$\Delta\phi$ 標在兩軌同時刻的落差上、以晚期零交越實測得 $-0.768$ rad（$-0.122$ 週期）。右：對應 [P1] Fig. 30（p.193），原標題逐字：*"ISF's obtained from different methods."*，原圖標題列 *"Calculation of Impulse Sensitivity Function"*——原圖振盪器未載明；復刻用 μ=0.2 的同一顆 vdP（與下方「三法對決」同一套機器），線型沿用原圖：實線＝1st Method（法 A）、點線＝2nd Method（法 B）、虛線＝3rd Method（法 C），相位零點對齊波形谷值使正 lobe 在前、負 lobe 在後（同原圖的排列）。**誠實差異**：原圖是 1st≈2nd、虛線 3rd 偏離（$N$ 級相同 stage 的 ring 把 Eq.(36) 分母撐成常數）；本復刻的單節點 vdP 上反而是法 B≈法 C（rms 差 0.134），打脈衝真值 A 在波形極值附近離開兩者（AM→PM，見下方對決）。數字：$\Gamma_{rms}$ A／B／C $=0.7777$／$0.7097$／$0.6758$；rms $|B-A|=0.2365$、rms $|C-A|=0.3219$。腳本：`simulations/fig_p1_fig2930_replica.py`（跑法 `PYTHONPATH=. python simulations/fig_p1_fig2930_replica.py`，約 1 s）。

### 第 2 步：位移 ÷ 速率 = 時間偏移——Eq. (32)

沿軌跡移了 $l$，等效於時間上移了「$l$ 除以速率 $|\dot{\vec X}|$」（[P1] Eq.(32), p.193）：

$$
\Delta t=\frac{l}{\bigl|\dot{\vec X}\bigr|}=\Delta\vec X\cdot\frac{\dot{\vec X}}{\bigl|\dot{\vec X}\bigr|^{2}}
$$

- **單位檢查**：$[\text{V}]\cdot[\text{V/s}]/[\text{V/s}]^2=[\text{V}]/[\text{V/s}]=$ s ✓。
- 注意分母變成**平方**：一次來自單位化切向量、一次來自「位移換時間」。這正是 [isf_definition](/03_isf_core_theory/isf_definition) 推 ideal LC 時「除以 $\vert\partial\mathbf z/\partial\theta\vert^2$」的同一件事。

### 第 3 步：時間偏移 → 相位——Eq. (33)

（[P1] Eq.(33), p.193）：

$$
\Delta\phi=2\pi\,\frac{\Delta t}{T}=\frac{2\pi}{T}\left(\Delta\vec X\cdot\frac{\dot{\vec X}}{\bigl|\dot{\vec X}\bigr|^{2}}\right).
$$

$2\pi/T=\omega_0$，所以這就是審稿人常引的「state-space 投影」形：$\Delta\phi=\omega_0\,(\Delta\vec X\cdot\dot{\vec X})/|\dot{\vec X}|^2$。

### 第 4 步：狀態＝節點電壓的特例——Eq. (34)

若狀態變數是**節點電壓**、impulse 打在第 $i$ 個節點，電壓跳變由 [P1] Eq.(9)（$\Delta V_i=\Delta q_i/C_i$）給出，Eq.(33) 化簡為（[P1] Eq.(34), p.193）：

$$
\Delta\phi_i=\frac{2\pi}{T}\cdot\frac{\Delta q_i}{C_i}\cdot\frac{\dot v_i}{\bigl|\dot{\vec v}\bigr|^{2}}
$$

其中 $\vert\dot{\vec v}\vert^2$ 是**波形向量一階導數的範數**、$\dot v_i$ 是第 $i$ 個節點電壓的導數（p.193 原文定義）。

- **逐步理解**：$\Delta\vec X$ 只有第 $i$ 分量非零（$=\Delta q_i/C_i$），內積 $\Delta\vec X\cdot\dot{\vec v}$ 就只剩 $\dot v_i$ 那一項。
- **單位檢查**：$\dfrac{[\text{rad/s}]\cdot[\text{C}]/[\text{F}]\cdot[\text{V/s}]}{[\text{V/s}]^2}=\dfrac{[\text{rad/s}]\cdot[\text{V}]}{[\text{V/s}]}=$ rad ✓。

### 第 5 步：用 normalized 波形改寫——Eqs. (35), (36)

代入 [P1] Eq.(1) 的 normalized 波形 $f$（$v_i=V_{max}\,f_i(x)$，$x=\omega_0\tau$，$f$ 的導數對 $x$ 取）。逐步：

$$
\begin{aligned}
\dot v_i&=\frac{d}{dt}\bigl[V_{max}f_i(x)\bigr]=V_{max}\,f_i'(x)\,\omega_0
&&(\text{鏈鎖律},\ dx/dt=\omega_0)\\[4pt]
\bigl|\dot{\vec v}\bigr|^{2}&=\sum_j\bigl(V_{max}f_j'\omega_0\bigr)^2=\omega_0^2V_{max}^2\,\bigl|\vec f\,'\bigr|^{2}
&&(\text{各節點同振幅 }V_{max}\text{：相同級的假設})\\[4pt]
\Delta\phi&=\omega_0\cdot\frac{\Delta q}{C_i}\cdot\frac{V_{max}f_i'\,\omega_0}{\omega_0^2V_{max}^2\bigl|\vec f\,'\bigr|^{2}}
=\frac{\Delta q}{C_iV_{max}}\cdot\frac{f_i'}{\bigl|\vec f\,'\bigr|^{2}}
&&(\omega_0\text{ 全部消掉})
\end{aligned}
$$

認出 $C_iV_{max}=$ 該節點的最大電荷擺幅，得（[P1] Eq.(35), p.193，逐字轉錄）：

$$
\Delta\phi=\frac{\Delta q}{q_i}\cdot\frac{f_i'}{\bigl|\vec f\,'\bigr|^{2}}
$$

> **記號註**：[P1] Eq.(35) 印的是 $q_i$——即第 $i$ 節點的最大電荷擺幅，就是主文（與本站）的
> $q_{max}$（該節點版本）。$f_i'$ 是「該節點 normalized 波形對相位 $x$ 的導數」（p.193 原文：
> *"$f_i'$ represents the derivative of the normalized waveform on node $i$"*）。

對照定義 $\Delta\phi=\Gamma\,\Delta q/q_{max}$，ISF 直接讀出來（[P1] Eq.(36), p.193）：

$$
\Gamma_i(x)=\frac{f_i'}{\bigl|\vec f\,'\bigr|^{2}}=\frac{f_i'}{\displaystyle\sum_{j=1}^{n}f_j'^{\,2}}
$$

- **單位檢查**：$f'$ 無因次（無因次波形對 rad 取導）→ $\Gamma$ 無因次 ✓。
- [P1] 在 Eq.(36) 後的觀察（p.193，重要，轉錄大意＋關鍵句）：這個表達式在 **transition（$f$ 導數最大處）取得最大值**，且最大值**反比於最大斜率**——原文：*"waveforms with larger slope show a smaller peak in the ISF function."* 這就是 [waveform_slope](/06_design_insights/waveform_slope) 整頁 design 直覺的原始出處。

### 第 6 步：二階系統特例——Eq. (37)，以及對 $f=\cos$ 的精確檢查

二階系統可以直接拿 **normalized 波形 $f$ 與它的導數 $f'$ 當狀態變數**，Eq.(36) 的分母只剩兩項（[P1] Eq.(37), p.193）：

$$
\Gamma(x)=\frac{f'}{f'^{\,2}+f''^{\,2}}
$$

其中 $f''$ 是 $f$ 的二階導數（p.193 原文定義）。**親手驗證理想正弦**（[P1] p.193 的自我檢查，我們把代數寫全）：取 $f(x)=\cos x$，

$$
\begin{aligned}
f'(x)&=-\sin x,\qquad f''(x)=-\cos x,\\[4pt]
f'^{\,2}+f''^{\,2}&=\sin^2x+\cos^2x=1\qquad(\text{畢氏恆等式，分母恆為 }1),\\[4pt]
\Gamma(x)&=\frac{-\sin x}{1}=-\sin x.
\end{aligned}
$$

原文結論（p.193，逐字）：*"In the case of an ideal sinusoidal oscillator $f=\cos(x)$, so that
$\Gamma(\omega t)=-\sin(\omega t)$, which is consistent with the argument of Section III."*
數值上我們也驗證到機器精度（`simulations/fig_isf_three_methods.py` 印出
`max |Eq.(37) on cos - (-sin)| = 2.2e-16`）。

> **這一步同時解掉 [waveform_slope](/06_design_insights/waveform_slope) 留下的「$1/\text{slope}$ 在波峰發散」矛盾**：
>
> - 在 **transition 上**（$f'^2\gg f''^2$）：$\Gamma\approx f'/f'^{\,2}=1/f'$——正是 $1/\text{slope}$ heuristic 的適用區。
> - 在**波峰附近**（$f'\to0$）：分子 $f'\to0$，分母被 $f''^{\,2}$ 撐住不歸零，$\Gamma\approx f'/f''^{\,2}\to0$——**有界、且趨於 0**，不發散。
> - 所以 $1/\text{slope}$ 是 Eq.(37) 在「斜率項主導」極限下的影子；Eq.(37) 才是它的嚴格母公式，在兩個極限之間連續內插。
> - **但注意**：Eq.(37) 自己也有病點——若某相位上 $f'$ 與 $f''$ **同時**趨近 0（波形有「斜率與曲率都平」的死區），分母整個垮掉、$\Gamma$ 會飆高（下面例題 2 的波形就在 $x\approx2.81$ 出現 $\vert\Gamma\vert\approx22.8$ 的假尖峰）。高階系統的 Eq.(36) 靠其他節點的 $f_j'^{\,2}$ 撐住分母，比較不會踩到。

## 方法 C：一階導數近似——Eq. (38)（[P1] Appendix C, p.193）

原文（p.193，段落大意）：這是**第二法的簡化版**。某些情況下 Eq.(36) 的分母變化不大、可近似為常數
——具體例子是 **$N$ 個相同級的 ring oscillator**（各級 transition 輪流發生，$\sum_j f_j'^2$ 幾乎恆定）。
此時分母用 $f_{max}'^{\,2}$ 取代（[P1] Eq.(38), p.193）：

$$
\Gamma_i(x)=\frac{f_i'(x)}{f_{max}'^{\,2}}
$$

**ISF 直接正比波形斜率**（除以一個常數）。[P1] 的誠實評價（p.193，逐字）：*"Although this method
is approximate, it is the easiest to use and allows a designer to rapidly develop important
insights into the behavior of an oscillator."*——近似、但最好用。[P1] Fig. 30（p.193，*"ISF's
obtained from different methods"*）把三法畫在同一張圖上比較，方法 C（虛線）在 lobe 高度與細節上
偏離另外兩法，但形狀對（其概念復刻見方法 B 第 1 步那張復刻圖的右半）。

- **它就是本站互動工具的引擎**：[互動工具 7 IsfSandbox](/04_simulation_labs/interactive_calculator)（畫波形→看 ISF）用的正是這個 slope 近似的 [P2]-Appendix 變體（每個 edge 各自用自己的最大斜率 normalize，才能重現上升／下降不對稱給出 $c_0\neq0$）；本頁就是那個 widget 的「嚴格出身證明」。
- [P2] App. B 的 ring closed form（Eq.(52)–(55)，$\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\,N^{-1.5}$，見 [rms_isf](/03_isf_core_theory/rms_isf)）本質上就是把方法 C 的三角形 ISF 積分出來的結果。
- **失效**：分母 $\sum_j f_j'^2$ 若隨相位大幅變化（單節點觀察、級數少、波形嚴重扭曲），常數近似崩潰——下面對決中 μ=2 的 van der Pol 就是這種情況。

## 三法對決：同一顆 van der Pol，三個答案差多少？

理論講完，上數字。我們在 van der Pol 振盪器（$\ddot x-\mu(1-x^2)\dot x+x=0$；
[lab_15](/04_simulation_labs/lab_15_nonlinear_isf) 與 [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv) 的同一顆 toy）上，
把電荷「打在 $x$ 軸」（$x$ 就是這顆 toy 的「節點電壓」——vdP 可改寫成並聯 RLC＋非線性電導，$x=v_C$，
電流脈衝瞬改的正是 $x$），三法同台：

- **法 A（真值）**：打脈衝實測，24 個相位（重用 lab_25 的 `extract_isf_impulse_axis`，機器已與 adjoint/PPV 互驗到 rms 0.0023）。
- **法 B**：Eq.(37)，$f=x/A$、$f'=y/(\omega_0A)$、$f''=\dot y/(\omega_0^2A)$，只用一個週期的波形。
- **法 C**：Eq.(38)，$f'/f_{max}'^{\,2}$。
- **參考**：諧波極限 $-\sin\theta$（相位 $\theta=0$ 對齊波形峰值，即 $f\approx\cos\theta$ 的慣例）與嚴格 adjoint/PPV 曲線（lab_25；PPV 屬外部文獻 [E2] Demir 2000，非本站 5 篇 PDF）。

![三種 ISF 計算法在 van der Pol μ=0.2 與 μ=2.0 上的對決：法 B/C 在近諧波時形狀正確但峰值附近漏掉 AM→PM 貢獻，強非線性時明顯失準](/figures/isf_three_methods.png)

**參數表**：$\mu\in\{0.2,\,2.0\}$；脈衝 $\Delta q=0.02$（$\Delta q/q_{max}\approx1\%$，$q_{max}\!=\!A\approx2$）；24 個注入相位；RK4 步長 $2.5\times10^{-3}$（脈衝 run）／$T/6000$（波形 grid）；全部為正規化無因次單位。**Pedagogical toy model，非 transistor-level**。完整 script：`simulations/fig_isf_three_methods.py`（跑法 `PYTHONPATH=. python simulations/fig_isf_three_methods.py`，約 3 s）。實測輸出：

```text
--- mu = 0.2 ---
T  = 6.2989                          # -> 6.2989（2π(1+μ²/16) 的預測值）
A  = 2.0004                          # -> 2.0004（諧波極限 A=2）
Gamma_rms (Method B) = 0.7097        # -> 0.7097（≈ 真 LC 的 1/√2=0.7071，非代表值 0.5）
Gamma_rms (Method A points) = 0.7777 # -> 0.7777（真值比法 B 高 9%）
peak |Gamma_B| = 0.9762              # -> 0.9762
peak |Gamma_A| = 1.0144              # -> 1.0144
rms |B - A(impulse)| = 0.2365        # -> 0.2365（法 B 的投影誤差）
rms |C - A(impulse)| = 0.3219        # -> 0.3219
rms |B - (-sin)|     = 0.078         # -> 0.078（法 B 幾乎就是 −sin）
rms |A - (-sin)|     = 0.28          # -> 0.28（真值早就離開 −sin 了）
--- mu = 2.0 ---
Gamma_rms (Method B) = 1.9898        # -> 1.9898
Gamma_rms (Method A points) = 3.2151 # -> 3.2151（法 B 低估 38%，≈4.2 dB 的相位雜訊低估）
peak |Gamma_A| = 5.0011              # -> 5.0011
rms |B - A(impulse)| = 2.072         # -> 2.072（失準）
rms |C - A(impulse)| = 3.1803        # -> 3.1803（崩潰：單節點沒有 N 級和撐分母）
rms |B - A(impulse)| at mu=0.05 = 0.0586  # -> 0.0586（μ 縮 4 倍誤差縮 4.0 倍：誤差 ∝ O(μ)）
rms |B - PPV| (mu=0.2) = 0.237       # -> 0.237（脈衝≡PPV 到 0.002，差距全是法 B 的投影誤差）
```

**怎麼讀這張圖（與這串數字）**：

1. **左圖（μ=0.2，近諧波）**：法 B（藍）與法 C（綠）幾乎就是 $-\sin\theta$（黑虛線，rms 差 0.078），
   $\Gamma_{rms}$ 也對到真 LC 的 $1/\sqrt2$（0.7097 vs 0.7071——注意這是**真 LC 值** $1/\sqrt2$，
   不是全站慣用的代表值 0.5）。**但打脈衝實測（紅圈）與嚴格 PPV（紫點劃線）互相重合，
   卻在波形峰值附近系統性地離開法 B**：在峰值上法 B 說 $\Gamma\approx-0.11$、真值是 $-0.59$。
2. **這個差不是數值誤差，是方法 B 的原理性漏項**。回頭看第 1 步的假設句：*"amplitude variations
   eventually die away, but phase variations do not"*——它假設**振幅擾動在衰減的過程中不夾帶相位**。
   van der Pol 的振幅卻會回頭調制瞬時頻率（isochron 扭曲，AM→PM）：徑向偏移 $\Delta r$ 以
   $e^{-\mu t}$ 衰減、衰減期間讓頻率偏 $O(\mu\Delta r)$，累積相位 $\int O(\mu\Delta r e^{-\mu t})dt=O(\Delta r)$
   ——**衰減率與調制強度的 $\mu$ 對消，留下有限殘相**。這筆帳只有斜（oblique）的 adjoint/PPV 投影
   記得到，正交切向投影記不到（詳見 [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)；此判準屬外部文獻 [E2]）。
   數值證據：$\mu$ 從 0.2 降到 0.05（縮 4 倍），rms 差從 0.2365 → 0.0586（恰縮 4.0 倍）——**誤差 $\propto O(\mu)$**，
   且集中在「法 B 預言 $\Gamma\approx0$」的峰值區（正是 [isf_definition](/03_isf_core_theory/isf_definition) 失效表中「高 AM–PM 時波峰注入也會殘留相位」那一格）。
3. **右圖（μ=2.0，強非線性）**：法 B 的 lobe 高度（3.85 vs 真值 5.00）、位置、寬度都不對，
   $\Gamma_{rms}$ 低估 38%；由 $\mathcal L\propto\Gamma_{rms}^2$（[P1] Eq.(21)，分母 $4\Delta\omega^2$ 為
   **SSB 記帳慣例**；時域乾淨推導為 $2\Delta\omega^2$，見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)），
   等於把相位雜訊**低估約 4.2 dB**。法 C（綠）更慘：relaxation 波形的 $f'_{max}$ 巨大，把整條 ISF 壓到近 0（rms 差 3.18）。
4. **工程結論**：正式數字用法 A（或 adjoint/PPV）；法 B 用來「一個週期波形快速看形狀」，在近諧波、
   低 AM–PM 的振盪器上定量可信（誤差 $\sim O(\mu)$）；法 C 只用於「N 級相同 stage 的 ring」這個它被發明的場景
   （[lab_32](/04_simulation_labs/lab_32_mos_level1_ring) 的雙葉 ISF 就是這個場景的方程級驗證）。

## Worked examples 數值例題

### 例題 1：用 Eq.(37) 算 $\Gamma(\pi/6)$，接到 canonical 例 A

> **題目**：理想正弦 $f(x)=\cos x$。用 closed form Eq.(37) 求 $\Gamma(\pi/6)$，再以
> $q_{max}=1$ pC、$\Delta q=1$ fC、$f_0=5$ GHz 算相位步階與時間誤差。

**逐步代入（帶單位）**：

$$
\begin{aligned}
f'(\pi/6)&=-\sin\frac{\pi}{6}=-0.5,\qquad f''(\pi/6)=-\cos\frac{\pi}{6}=-0.8660,\\[4pt]
f'^{\,2}+f''^{\,2}&=0.25+0.75=1\qquad(\text{正弦的分母恆為 }1),\\[4pt]
\Gamma(\pi/6)&=\frac{-0.5}{1}=-0.5\qquad(\text{無因次}),\\[4pt]
\Delta\phi&=\frac{\vert\Gamma\vert\,\Delta q}{q_{max}}=\frac{0.5\times(1\times10^{-15}\,\text{C})}{1\times10^{-12}\,\text{C}}=5\times10^{-4}\ \text{rad},\\[4pt]
\Delta t&=\frac{\Delta\phi}{2\pi f_0}=\frac{5\times10^{-4}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=1.59\times10^{-14}\ \text{s}=15.9\ \text{fs}.
\end{aligned}
$$

- **結果**：closed form 在 $\theta=\pi/6$ 給 $\Gamma=-0.5$，正是全站 canonical 例 A 的 $\vert\Gamma\vert=0.5$、$5\times10^{-4}$ rad、15.9 fs。
- **Dimension check**：$\Gamma$ 無因次 ✓；$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。
- **Python 驗證**：

```python
import numpy as np
th = np.pi/6
fp, fpp = -np.sin(th), -np.cos(th)
g = fp/(fp**2 + fpp**2)
dphi = abs(g)*1e-15/1e-12
print(round(g, 4), round(dphi, 6), round(dphi/(2*np.pi*5e9)*1e15, 1))
# -> -0.5 0.0005 15.9（Γ、Δφ [rad]、Δt [fs]）
```

### 例題 2：二次諧波失真下，法 C 比法 B 高估多少？

> **題目**：波形帶 30% 二次諧波：$f(x)=\cos x+0.3\cos 2x$。在 zero crossing 附近的 $x=\pi/2$，
> 分別用法 B（Eq.(37)）與法 C（Eq.(38)）算 $\Gamma$，比較兩者。

**逐步代入**：先求導數，

$$
f'(x)=-\sin x-0.6\sin 2x,\qquad f''(x)=-\cos x-1.2\cos 2x.
$$

在 $x=\pi/2$：$\sin x=1$、$\sin 2x=0$、$\cos x=0$、$\cos 2x=-1$，所以

$$
\begin{aligned}
f'&=-1,\qquad f''=+1.2,\\[4pt]
\Gamma_B&=\frac{f'}{f'^{\,2}+f''^{\,2}}=\frac{-1}{1+1.44}=-0.4098,\\[4pt]
f_{max}'^{\,2}&=1.9247\quad(\text{數值求極值：}f'_{max}=1.3873\text{ 出現在 }x\approx58^\circ),\\[4pt]
\Gamma_C&=\frac{f'}{f_{max}'^{\,2}}=\frac{-1}{1.9247}=-0.5196,\qquad
\frac{\Gamma_C}{\Gamma_B}=1.27.
\end{aligned}
$$

- **結果**：才 30% 的諧波失真，法 C 在 ZC 就比法 B **高估 27%**——因為它把「分母恆定」硬套在一個
  分母其實隨相位變的波形上。換算 $\Gamma^2$ 就是約 2 dB 的相位雜訊誤差來源。
- **同場加映（法 B 的病點）**：這條波形在 $x\approx2.81$ 處 $f'$ 與 $f''$ 同時近 0，Eq.(37) 的
  $\vert\Gamma\vert$ 飆到 22.8（假尖峰）——法 B「治好了 $1/\text{slope}$ 在波峰的發散」，但**自己的分母
  也可能死**，用之前先掃一眼 $f'^{\,2}+f''^{\,2}$ 有沒有貼地。
- **Dimension check**：全程無因次 ✓（$f$、$f'$、$f''$、$\Gamma$ 皆無因次）。
- **Python 驗證**：

```python
import numpy as np
x = np.linspace(0, 2*np.pi, 200001)
fp  = -(np.sin(x) + 0.6*np.sin(2*x))
fpp = -(np.cos(x) + 1.2*np.cos(2*x))
i = np.argmin(np.abs(x - np.pi/2))
gB = fp[i]/(fp[i]**2 + fpp[i]**2)
gC = fp[i]/np.max(fp**2)
print(round(gB,4), round(gC,4), round(gC/gB,4), round(np.max(fp**2),4))
# -> -0.4098 -0.5196 1.2677 1.9247（Γ_B、Γ_C、比值、f'²max）
```

## 適用與失效條件（三法總表）

| 方法 | 需要什麼 | 成本 | 準度 | 失效條件 |
|---|---|---|---|---|
| **A 打脈衝**（p.192） | 可重跑的 transient（模擬器或方程） | $N_{phase}$ 次 transient | 三法最準（[P1] 原話），與 adjoint/PPV 互驗 rms ~0.002 | $\Delta q$ 太大（非線性）、$\Delta t$ 沒 wrap、尚未進穩態 |
| **B closed form**（Eqs.(31)–(37)） | 一個週期的穩態波形＋導數 | 一次代數 | 近諧波、低 AM–PM 時誤差 $\sim O(\mu)$；本例 μ=0.2 rms 0.24 | **AM→PM（isochron 扭曲）**：正交切向投影漏掉振幅衰減期間累積的相位；狀態單位混雜／尺度選擇改變答案；$f'$、$f''$ 同時近 0 處分母垮掉 |
| **C 一階導數**（Eq.(38)） | 一個週期的波形斜率 | 最便宜 | 「N 級相同 stage ring」內定性佳（[P1] Fig.30） | 分母 $\sum_j f_j'^2$ 隨相位大幅變化：單節點、少級數、強失真（本例 μ=2 rms 3.18）；上升／下降不對稱需改用 per-edge normalize（[P2] App.、IsfSandbox 的作法） |

## 重點回顧

- [P1] 附錄給了三種 ISF 算法：**A 打脈衝（最準）→ B closed form $\Gamma=f'/(f'^{\,2}+f''^{\,2})$（一個週期波形就夠）→ C 斜率近似 $\Gamma=f'/f_{max}'^{\,2}$（最快，ring 專用）**（[P1] Eqs.(31)–(38), pp.192–193）。
- 法 B 的鏈條：投影到單位切向量（Eq.(31)）→ 除速率變時間（Eq.(32)）→ 乘 $2\pi/T$ 變相位（Eq.(33)）→ 節點電壓特例（Eq.(34)）→ normalized 波形（Eqs.(35)(36)）→ 二階特例（Eq.(37)）。
- $f=\cos x$ 代入 Eq.(37)：分母 $\sin^2+\cos^2=1$，$\Gamma=-\sin x$ **精確成立**——波峰處分子歸零、有界，**解掉 $1/\text{slope}$ heuristic 的發散**；$1/\text{slope}$ 只是它在 $f'^2\gg f''^2$ 區間的極限。
- 法 B 的原罪是**正交投影**：假設「振幅衰減不留相位」。AM→PM 一開（van der Pol 已足夠），真值離開法 B，誤差 $\propto O(\mu)$ 且集中在波峰；強非線性（μ=2）時 $\Gamma_{rms}$ 低估 38% ≈ 相位雜訊低估 4.2 dB。嚴格解是 adjoint/PPV 的**斜投影**（外部文獻）。
- 法 C 是 IsfSandbox 與 [P2] ring closed form 的引擎；離開「N 級相同 stage」的場景會崩。
- 實務順序：**先法 C/B 建直覺，正式數字用法 A 或 adjoint**。

## 延伸閱讀

- $\Gamma$ 的定義與切向投影直覺：[isf_definition](/03_isf_core_theory/isf_definition)
- $1/\text{slope}$ heuristic（本頁 Eq.(37) 的影子版）：[waveform_slope](/06_design_insights/waveform_slope)
- 嚴格 adjoint/PPV（法 B 漏項的完整數學）：[derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)（外部文獻 [E2] Demir 2000）
- 打脈衝法的三個實作：[lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep)（正弦）、[lab_15](/04_simulation_labs/lab_15_nonlinear_isf)（van der Pol）、[lab_32](/04_simulation_labs/lab_32_mos_level1_ring)（MOS Level-1 ring）
- 斜率近似的互動版：[互動工具 7 IsfSandbox](/04_simulation_labs/interactive_calculator)
- ring 的 $\Gamma_{rms}$ closed form（方法 C 的積分結果）：[rms_isf](/03_isf_core_theory/rms_isf)
