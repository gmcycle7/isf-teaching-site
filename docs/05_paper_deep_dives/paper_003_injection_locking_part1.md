---
title: "[P3] Injection Locking & Pulling — Part I (Time-Synchronous Modeling)"
description: Hong–Hajimiri 2019 Part I 精讀：ISF-based time-synchronous model、廣義 Adler 方程、lock range、injection waveform design（進階，核心公式已對照 [P3] 原文核實）。
---

# A General Theory of Injection Locking and Pulling in Electrical Oscillators—Part I

> **先備**：[paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)（[P1] 的 ISF 定義與 Eq.(11) 相位推力）、[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（ISF 的傅立葉諧波 $c_n$） ｜ **接下來**：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)（Part II：APF 振幅、transient、frequency division）。

這是**進階**篇。它把 [P1] 的 ISF 從「自由振盪器的 phase noise」延伸到「振盪器被外部訊號注入
時的 injection locking／pulling（注入鎖定／拉扯）」。核心結果：一個用 ISF 寫成的**單一一階微分
方程**（廣義 Adler 方程）就能預測 lock range（鎖定範圍）、鎖定相位與穩定性，對**任意**振盪器
拓樸與**任意**注入波形都成立——並由此導出「怎麼設計注入波形把 lock range 做到最大」。

> **本頁定位**：進階 deep-dive，**不是核心教學章節**。核心公式（脈衝列 Eq.(19)–(23)、廣義 Adler
> Eq.(26)、(28)–(30)、(33)、(35)）已對照 [P3] 原始 PDF 核實。先確定你已讀懂 [P1] 的 ISF（[paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)）再讀這裡。

## Citation

> **[P3]** B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in
> Electrical Oscillators—Part I: Time-Synchronous Modeling and Injection Waveform Design,"*
> IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2109–2121, Aug. 2019.
> （檔案 `BHongGenTheor-I_JSSC2019_Postprint.pdf`，paper_003）

## One-sentence contribution

同一個 ISF $\Gamma$ 不只算 phase noise，也能寫出一個 topology-independent 的廣義 Adler 方程，
預測任意振盪器、任意注入波形下的 lock range、鎖定相位與穩定性，並指出如何設計注入波形來放大
lock range（claim C10）。

## Why this paper matters

**injection locking** 是指：一個振盪器被一個頻率接近自身的外部訊號注入時，會「跟著外部訊號
同步」——相位、頻率被外部拉住。當頻率差太大跟不上時，相位週期性滑動，產生不想要的 spurs，這
叫 **injection pulling**。這現象在 PLL、clock distribution、quadrature 產生、frequency division
裡到處都是，既被利用也被害怕。

1946 年 **Adler** 用一條一階相位方程描述 LC 振盪器在**弱、正弦、近自由頻率**注入下的行為。
[P3] 指出 Adler 方程的五大限制（只適用弱注入、只適用 LC、假設正弦注入、需要難以準確量測的
$Q$ 與 $I_{osc}$、且預測對稱 lock range），然後用 ISF 把它**徹底推廣**：

- 用 $\Gamma$ 取代「只對 LC 成立」的 $Q$／$I_{osc}$ 參數——任何能萃取出 ISF 的振盪器都適用。
- 允許**任意注入波形**（不只正弦），於是可以**設計**注入波形使 lock range 最大。
- 自然產生**不對稱 lock range**（真實電路常見，Adler 抓不到）。
- 涵蓋 subharmonic／superharmonic locking（注入頻率在 $\omega_0/m$ 或 $m\omega_0$ 附近）。

## Main assumptions

照 paper_metadata（paper_003.assumptions）：

1. **振盪器 autonomy 與週期時變**（與 ISF 同一基礎）。
2. 注入（擾動）透過 ISF 映射到相位；振幅留到 Part II（APF）處理。
3. **time-synchronous averaging**：在一個週期上做時間同步平均。

> **物理直覺**：phase noise 把擾動換成隨機 noise；injection 把擾動換成一個**確定的、週期性的
> 注入電流 $i_{inj}$**。同一台「ISF 加權後積分」的機器，輸入從隨機變確定，輸出就從統計量
> （$\Gamma_{rms}$、PSD）變成確定的相位動態（鎖定／滑動）。

## Key equations

### 經典 Adler 方程（基準線）

**Original formula**（[P3] Sec. III（SURVEY OF EXISTING MODELS）, 約 p.2111，對照原文 Eq.(15)）：

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}\sin\theta
$$

寫成規範第 3 節的簡化形式（$\omega_L\equiv\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}$、
$\Delta\omega_{inj}\equiv\omega_0-\omega_{inj}$）：

$$
\frac{d\phi}{dt}=-\omega_L\sin\phi+\Delta\omega_{inj}
$$

**Meaning**：注入鎖定的相位差 $\theta$（或 $\phi$）滿足一條一階非線性 ODE。$\omega_L$ 是
（半）lock range。**鎖定**＝存在穩態解 $d\theta/dt=0$，要求 $|\Delta\omega_{inj}|\le\omega_L$。

**Step-by-step（[P3] 對 LC 的簡化推導摘要）**：把注入電流寫成 phasor
$i_{inj}=I_{inj}e^{j\omega_{inj}t}$，對 LC tank 寫 KCL（注入電流要供應 tank 偏離共振時的
無功電流），在弱注入（$I_{inj}\ll I_{osc}$）與慢相位（$|d\theta/dt|\ll\omega_{inj}$）近似下取
實部，即得上式。穩態解給出 lock characteristic 與**對稱** lock range
$\omega_L=\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}$。

**Numerical example**：$f_0=5$ GHz、$Q=10$、$I_{inj}/I_{osc}=0.1$。半 lock range

$$
\omega_L=\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}=\frac{2\pi\times5\times10^{9}}{2\times10}\times0.1=1.57\times10^{8}\ \text{rad/s},
$$

換成頻率 $f_L=\omega_L/2\pi\approx25$ MHz。手感：lock range 隨注入強度線性增加、隨 $Q$ 反比
下降（高 $Q$ 的 LC 比較「固執」、不容易被拉走）。

> **註**：經典 Adler 為標準結果（[P3] Sec. III, p.2111 回顧 Adler [20]）；本頁採通用簡化記法。
> 下一節的**脈衝列思想實驗**與其後的**廣義 Adler** 皆已對照原始 PDF 逐字核實。

### 脈衝列鎖定（locking to an impulse train）——零微積分版的 Adler（[P3] Sec. IV, p.2112，已核實 ✓）

在經典 Adler（Sec. III）與 time-synchronous model（Sec. V）之間，[P3] 安插了一個純算術的思想實驗
（Sec. IV *Locking to an Impulse Train*, p.2112）：讓 ideal LC 振盪器吃一列電流脈衝。它的價值是
**一滴微積分都不用**——只靠「一根 impulse ＝ 一個相位 kick」的離散記帳，就把 lock range 算到與
經典 Adler 的 Eq.(18) 一字不差。而「一根 impulse ＝ 一個 kick」正是你在
[isf_definition](/03_isf_core_theory/isf_definition) 玩過的互動動畫 **ImpulseAnimation**：按一次「注入！」＝吃一個

$$
\Delta\phi=\Gamma(\theta)\,\frac{\Delta q}{q_{max}}
$$

這一節只是把「手動按一次」換成「每 $T_{inj}$ 秒自動按一次」——同一套物理，變成週期性事件。
（動畫沿電壓軸打 $\Delta V=\Delta q/C$、[P3] Fig. 3 沿電荷軸打 $q_{inj}$，因 $V=q/C$ 是同一件事。）

**Setup（[P3] Fig. 3(a), p.2112）**：ideal 並聯 LC（$C$、$L$、$R_P$、$-G_m$），注入電流為週期脈衝列

$$
i_{inj}(t)=\pm\,q_{inj}\sum_{n=-\infty}^{\infty}\delta(t-nT_{inj}),\qquad T_{inj}\equiv\frac{2\pi}{\omega_{inj}}
$$

（[P3] 約定 $q_{inj}\ge0$；正負號對應 Fig. 3(b) 加速、Fig. 3(c) 減速）。每根脈衝把固定電荷
$q_{inj}$ [C] 一次倒進電容。關鍵安排：脈衝打在電容電荷 $q(t)$ 的 zero crossing 上——把電容電壓
「從零交越的一側搬到對稱的另一側」（[P3] 原文 "moving the capacitor voltage to the opposite side
of the zero-crossing"），state-space 圓上從 $q=-q_{inj}/2$ 水平搬到 $q=+q_{inj}/2$，兩端都落在
**同一個圓**上，所以振幅永遠不動、只有相位跳（"the amplitude remains perpetually unaffected",
p.2112）——正是 [P1]／lab_02 的「ZC 注入＝純相位跳」。

**Step 1｜每根脈衝的 kick（[P3] Eq.(19), p.2112）**：小注入（$q_{inj}\ll q_{max}$）時

$$
\Delta\phi=\pm\frac{q_{inj}}{q_{max}}\qquad[\text{rad}]
$$

這是 [P1] 操作型定義 $\Delta\phi=\Gamma(\theta)\,\Delta q/q_{max}$ 在 $\Gamma=-\sin\theta$、脈衝打在
$\theta=\mp\pi/2$（$q$ 的 zero crossing、$\lvert\Gamma\rvert=1$ 的最敏感點）的特例。
Dimension check：$\tilde\Gamma=\Gamma/q_{max}$ 單位 rad/C（[P3] 寫 1/Coulomb；rad 無因次），
乘上 $q_{inj}$ [C] 得 rad ✓。

精確幾何（[P3] footnote 9, p.2112）：圓上兩點被水平弦長 $q_{inj}$ 相連，$q_{inj}=2q_{max}\sin(\Delta\phi/2)$，故

$$
\Delta\phi=\pm2\sin^{-1}\!\left[\frac{q_{inj}}{2q_{max}}\right]
$$

小注入時 $2\sin^{-1}\!\big(\tfrac{q_{inj}}{2q_{max}}\big)\approx q_{inj}/q_{max}$ 退回 Eq.(19)；
極端 $q_{inj}=2q_{max}$（弦＝直徑）時 $\Delta T=\mp T_0/2$，即 $\Delta\omega=+\omega_0$（週期砍半）
或 $-\omega_0/3$（週期變 1.5 倍）——footnote 9 特別點名：**就連 ideal LC，這個思想實驗的強注入
「lock range」都不對稱**。這預告了廣義 Adler 的不對稱 lock range 不是病態、是常態。

**Step 2｜kick → 頻率移動（[P3] Eq.(20)–(21), p.2112）**：每個週期吃同一個 kick，等效於週期被改寫：

$$
\frac{\Delta\phi}{2\pi}=-\frac{\Delta T}{T_0}=\frac{\Delta\omega}{\omega_{inj}}
$$

（相位往前跳 $\Delta\phi>0$ ⇒ 週期變短 $\Delta T<0$ ⇒ 頻率變高）。平均頻率移動為

$$
\Delta\omega=\frac{\Delta\phi}{T_{inj}}=\pm\frac{1}{T_{inj}}\frac{q_{inj}}{q_{max}}\qquad[\text{rad/s}]
$$

Dimension check：rad ÷ s ＝ rad/s ✓。這已是 lock range 的雛形：**一列脈衝每週期最多能把振盪器
搬走 $q_{inj}/(q_{max}T_{inj})$ 的角頻率**。

**Step 3｜離散映射、固定點、lock range**（本站把 Sec. IV 的文字敘述寫成顯式映射）：

脈衝不一定打在最敏感點——鎖定時它會自己找位置。令 $\theta_n$ ＝ 第 $n$ 根脈衝抵達瞬間振盪器的
相對相位（就是下一節座標 $\theta=\phi-\omega_{inj}t$ 在 $t=nT_{inj}$ 的取樣）。兩根脈衝之間振盪器
自由跑、相位差以 detuning 漂移；脈衝瞬間吃一個 ISF kick：

$$
\theta_{n+1}=\theta_n+\underbrace{(\omega_0-\omega_{inj})\,T_{inj}}_{\text{每週期漂移 [rad]}}+\underbrace{\Gamma(\theta_n)\,\frac{q_{inj}}{q_{max}}}_{\text{每脈衝 kick [rad]}}
$$

其中每週期漂移 $(\omega_0-\omega_{inj})T_{inj}=2\pi\dfrac{\omega_0-\omega_{inj}}{\omega_{inj}}\approx2\pi\dfrac{\omega_0-\omega_{inj}}{\omega_0}$ [rad]（小 detuning）。
**鎖定＝映射的固定點** $\theta_{n+1}=\theta_n=\theta^\*$：

$$
(\omega_{inj}-\omega_0)\,T_{inj}=\Gamma(\theta^\*)\,\frac{q_{inj}}{q_{max}}
$$

左邊是「每週期欠的相位」，右邊是「每根脈衝補的相位」——**每週期的 kick 恰好抵銷 detuning 漂移**。
這就是 [P3] Sec. IV 的原話：存在一個 $T_{inj}$ 使「下一根脈衝永遠打在波形的同一個位置」
（"the next impulse always occurs at the same place on the waveform", p.2112）。固定點存在的條件＝
右邊供應得起左邊：

$$
\lvert\omega_{inj}-\omega_0\rvert\le\frac{q_{inj}}{q_{max}\,T_{inj}}\,\max_\theta\lvert\Gamma(\theta)\rvert
$$

ideal LC 的 $\max\lvert\Gamma\rvert=1$，正是 Step 2 的極值——**lock range ＝ 每週期最大 kick ÷ $T_{inj}$**。

穩定性（本站補充；論文未寫離散版）：把映射在 $\theta^\*$ 線性化，
$\delta\theta_{n+1}=\big[1+\tfrac{q_{inj}}{q_{max}}\Gamma'(\theta^\*)\big]\delta\theta_n$，穩定需乘子
絕對值小於 1，即 $-2<\tfrac{q_{inj}}{q_{max}}\Gamma'(\theta^\*)<0$。弱注入下退化成
$\Gamma'(\theta^\*)<0$——和下一節連續版「$d\Omega/d\theta<0$ 才穩」同一句話；離散版還多說了一件
連續平均看不到的事：kick 強到 $\tfrac{q_{inj}}{q_{max}}\lvert\Gamma'(\theta^\*)\rvert\ge2$ 會過度修正、
$\theta_n$ 來回振盪（映射失穩）——但強注入本來就超出本節與 time-averaging 的適用範圍（見 [P4]）。

**Step 4｜代回 Adler——一字不差（[P3] Eq.(22)–(23), p.2112）**：Sec. IV 收尾的「curiously」時刻。
tank 損耗與能量回填機制的平衡給出

$$
\omega_0\,q_{max}=Q\,I_{osc}
$$

（[P3] Eq.(22)，$Q$ 依 Eq.(16), p.2111；check：(rad/s)·C ＝ A ✓）。脈衝列的**基波振幅**（[P3] Eq.(23)）：

$$
I_{inj}=\frac{2q_{inj}}{T_{inj}}
$$

> **這個 2 是誰？** 面積 $q_{inj}$、週期 $T_{inj}$ 的 δ 列，傅立葉級數為
> $\frac{q_{inj}}{T_{inj}}\big[1+2\sum_{n\ge1}\cos(n\omega_{inj}t)\big]$：每個諧波（含基波）的振幅都是
> DC 的 2 倍。這是「實數傅立葉級數」的 2，與本站在 phase-noise 各頁一路標記的 SSB 記帳 $/4$
> （例 B 的 $-148$ dBc/Hz）vs 時域記帳 $/2$（$-145$）**無關**。

把 Eq.(23)（$q_{inj}=I_{inj}T_{inj}/2$）與 Eq.(22)（$q_{max}=QI_{osc}/\omega_0$）代入 Step 2 的極值：

$$
\lvert\Delta\omega\rvert_{max}=\frac{1}{T_{inj}}\frac{q_{inj}}{q_{max}}=\frac{I_{inj}}{2\,q_{max}}=\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}
$$

＝經典 Adler 的半 lock range（Eq.(18), p.2111）。[P3] 原文用 "curiously yields an (absolute)
frequency shift exactly equal to Adler's lock range" 描述這個巧合。再對第三本帳：ideal LC 的
$\Gamma=-\sin$ 基波振幅為 1、$\lvert\tilde\Gamma_1\rvert=1/q_{max}$，下一節廣義 Adler 的 Eq.(35) 給
$\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert=I_{inj}/(2q_{max})$——**離散算術、經典 Adler、
廣義 Adler 三條路算出同一個數**。（Eq.(35) 的 $\tfrac12$ 是「單音×ISF 基波、$\cos^2$ 平均＝$\tfrac12$」
的平均因子；Adler 的 $\omega_0/2Q$ 那個 2 來自 tank 相位斜率 $d\varphi/d\omega\approx2Q/\omega_0$；
都與 SSB 的 2/4 記帳無關。）

**Step 5｜連續極限＝廣義 Adler Eq.(30)（零微積分橋的另一端）**：把脈衝列餵進下一節的
time-averaged 方程（[P3] Eq.(30), p.2113）。一個平均窗 $T_{inj}$ 內恰好一根 δ
（在 $t=nT_{inj}$，此時 $\tilde\Gamma$ 的引數 $\omega_{inj}t+\theta=2\pi n+\theta\equiv\theta$）：

$$
\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt
=\frac{q_{inj}}{T_{inj}}\,\tilde\Gamma(\theta)
\;\Longrightarrow\;
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\frac{q_{inj}}{T_{inj}}\,\tilde\Gamma(\theta)
$$

而 Step 3 的映射兩邊除以 $T_{inj}$：

$$
\frac{\theta_{n+1}-\theta_n}{T_{inj}}=(\omega_0-\omega_{inj})+\frac{q_{inj}}{T_{inj}}\,\tilde\Gamma(\theta_n)
$$

每週期淨變化 $\ll2\pi$ 時左邊就是 $d\theta/dt$——**離散記帳與 Eq.(30) 是同一條方程**。對脈衝列而言，
Eq.(30) 那個嚇人的平均積分只做了一件事：把那一根 kick 挑出來。反過來讀更有價值：任意注入波形的
Eq.(30) ＝「把連續的 $i_{inj}$ 切成無限多根小脈衝，每根照 ImpulseAnimation 記一筆
$d\phi=\tilde\Gamma\,i_{inj}\,dt$，再每週期平均」——這就是從動畫到 Adler 的零微積分橋。
順帶一提：脈衝列的 lock characteristic $\Omega(\theta)=\frac{q_{inj}}{T_{inj}}\tilde\Gamma(\theta)$
**就是 ISF 自己的縮放**——因為 δ 列的所有諧波等重（$\lvert I_{inj,n}\rvert=2q_{inj}/T_{inj}$ 對所有
$n\ge1$），把 ISF 的每個諧波等權重激發（對照 [P3] Fig. 6「注入諧波被 ISF 諧波濾波」的圖像）。

**Worked example（canonical $\Gamma=-\sin\theta$）**：$q_{max}=1$ pC、$f_0=5$ GHz（例 A 的振盪器）、
$q_{inj}=10$ fC（$q_{max}$ 的 1%）、$f_{inj}=5.005$ GHz（detuning $+5$ MHz）、$T_{inj}=1/f_{inj}=199.8$ ps。

1. **每脈衝 kick 預算**：$\lvert\Delta\phi\rvert_{max}=q_{inj}/q_{max}=10^{-14}/10^{-12}=0.01$ rad。
   精確式 $2\sin^{-1}(0.005)=0.0100000417$ rad，差 $4\times10^{-6}$——線性化極好。
2. **每週期漂移**：$(\omega_0-\omega_{inj})T_{inj}=2\pi\times(-5\times10^{6}\ \text{Hz})\times199.8\ \text{ps}=-6.277\times10^{-3}$ rad
   （check：Hz × s 無因次、乘 $2\pi$ 得 rad ✓）。
3. **鎖得住嗎**：$6.277\ \text{mrad}<10\ \text{mrad}$ ✓。固定點：$-\sin\theta^\*\times0.01=+6.277\times10^{-3}$
   ⇒ $\sin\theta^\*=-0.6277$ ⇒ $\theta^\*=-0.679$ rad $=-38.9^\circ$
   （另一解 $\theta=-\pi+0.679=-2.463$ rad 因 $\Gamma'(\theta)>0$ 不穩定）。
4. **半 lock range**：$f_L=\dfrac{q_{inj}}{q_{max}T_{inj}}\cdot\dfrac{1}{2\pi}=\dfrac{0.01\times5.005\times10^{9}}{2\pi}=7.97$ MHz；
   detuning 5 MHz 在範圍內 ✓。
5. **Adler 對帳**：$I_{inj}=2q_{inj}/T_{inj}=100.1\ \mu\text{A}$、
   $\omega_L=I_{inj}/(2q_{max})=5.005\times10^{7}$ rad/s $=2\pi\times7.97$ MHz——同一個數。
6. **收斂手感**：乘子 $1-0.01\cos\theta^\*=0.9922$，$1/e$ 收斂約 128 個週期（$\approx25.7$ ns）——
   弱注入的鎖定是「幾百個週期」的慢動態，這也正是把 $\theta$ 當慢變數做 time-averaging 的正當性。

```python
import numpy as np

q_max, q_inj = 1e-12, 10e-15      # C
f0, f_inj = 5e9, 5.005e9          # Hz
T_inj = 1/f_inj                   # s
drift = 2*np.pi*(f0 - f_inj)*T_inj            # rad per period
print(q_inj/q_max)                            # -> 0.01
print(drift)                                  # -> -0.0062769083987808056
theta = 0.0
for n in range(3000):             # discrete map
    theta += drift + (-np.sin(theta))*q_inj/q_max
print(theta, np.degrees(theta))               # -> -0.6785833433413406 -38.879961621335696
print((q_inj/(q_max*T_inj))/(2*np.pi)/1e6)    # -> 7.965704901749362
I_inj = 2*q_inj/T_inj
print(I_inj, I_inj/(2*q_max))                 # -> 0.0001001 50050000.0
print(1 - (q_inj/q_max)*np.cos(theta))        # -> 0.9922153727798411
print(1/((q_inj/q_max)*np.cos(theta)))        # -> 128.45830271877517
```

（3000 步只是保守收斂；固定點 $\theta^\*$、lock range 與 Adler 對帳全部與手算一致。）

**適用與失效條件**：

- **小注入**：kick 線性化要 $q_{inj}\ll q_{max}$；大注入改用 footnote 9 的精確式（本身就不對稱）。
- **慢相位**：每週期淨相位變化 $\ll2\pi$ rad，映射→ODE 的連續極限（也是 Eq.(30) time-averaging 的前提）才成立。
- **振幅假設**：「振幅永遠不動」只對 ideal LC＋跨零點電荷 kick 成立；一般振盪器靠振幅回復機制拉回
  limit cycle——那是 Part II APF 的主題（[P4]）。
- **Subharmonic**：脈衝也可以每 $M$ 個週期打一根（[P3] footnote 7, p.2112）——同一套算術、
  漂移改成累積 $M$ 個週期，這就是 subharmonic locking 的離散圖像。
  > **[P3] footnote 7 原文**（p.2112）："...injection could also occur every $M$ periods
  > ($M$ a positive integer), corresponding to subharmonic locking."
  > 換句話說：**當 $T_{inj}=N\cdot T_0$（每 $N$ 個振盪週期注入一次）就是 subharmonic
  > locking**——把上面的 $M$ 換成本站慣用的倍頻比 $N$，逐項展開、算出閉式 lock range
  > 見 [subharmonic_injection](/06_design_insights/subharmonic_injection) 頁。
- **超強 kick**：乘子出界（$\tfrac{q_{inj}}{q_{max}}\lvert\Gamma'\rvert\ge2$）時離散映射失穩——平均化 ODE 看不到這件事。

> **已核實**：Sec. IV 的 Eq.(19)、(20)、(21)、(22)、(23) 與 footnote 7（subharmonic）、footnote 9
> （精確 kick、$\Delta\omega=+\omega_0$ vs $-\omega_0/3$ 的強注入不對稱）皆已對照 [P3] p.2112 原始
> PDF 渲染逐字確認；經典 Adler 的 Eq.(15)/(18) 與 $Q$ 的 Eq.(16) 在 p.2111。

### 廣義 Adler 方程 / lock characteristic（本篇核心，已對照原始 PDF 核實 ✓）

[P3] 先把 Hajimiri 的**無因次** ISF $\Gamma$ 換成**有單位**的版本（[P3] Eq.(26), p.2113）：

$$
\tilde\Gamma(x)\equiv\frac{\Gamma(x)}{q_{max}}\qquad[\text{單位 rad/C}]
$$

於是注入電流對相位的瞬時推力，以及換到相對相位 $\theta=\phi-\omega_{inj}t$ 的座標（[P3] Eq.(28)–(29), p.2113）：

$$
\frac{d\phi}{dt}=\tilde\Gamma(\phi)\,i_{inj}(t)
\;\xrightarrow{\ \theta=\phi-\omega_{inj}t\ }\;
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)
$$

對「快變的一個注入週期」做時間同步平均（$\theta$ 慢變視為常數），得 **time-averaged 廣義 Adler 方程**（[P3] Eq.(30), p.2113）：

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt
$$

整理成 lock characteristic 形式（[P3] Eq.(33), p.2114）：

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta),\qquad
\boxed{\ \Omega(\theta)=\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt\ }
$$

其中 $\Omega(\theta)$ 稱為 **lock characteristic**（[P3] Eq.(33), p.2114）：注入造成的平均頻率偏移隨相位差 $\theta$ 的函數。注意平均項前為 **加號**（與 [P3] Eq.(30) 同號慣例）。

**Meaning**：一條一階 ODE，由**有單位 ISF $\tilde\Gamma=\Gamma/q_{max}$** 與**注入波形 $i_{inj}$** 組成，
預測任意振盪器、任意注入波形下的行為（claim C10）。**鎖定**＝存在 $\theta^\*$ 使
$\omega_{inj}-\omega_0=\Omega(\theta^\*)$；lock range ＝ $\Omega(\theta)$ 的值域寬度；**穩定性**由 $d\Omega/d\theta$ 的符號決定。

**正弦注入退化回經典 Adler（[P3] Eq.(34)–(35)）**：若注入為單音 $i_{inj}=I_{inj}\cos\omega_{inj}t$，
只有 ISF 基波 $\tilde\Gamma_1$ 存活：

$$
\Omega(\theta)=\tfrac12 I_{inj}\,\lvert\tilde\Gamma_1\rvert\cos(\theta+\angle\tilde\Gamma_1),
\qquad
\omega_L=\tfrac12 I_{inj}\,\lvert\tilde\Gamma_1\rvert
$$

半 lock range $\omega_L=\frac12 I_{inj}\lvert\tilde\Gamma_1\rvert$（[P3] Eq.(35)）——$\Omega\propto\cos\theta$ 對稱於 0，正是經典 Adler。

**為何一般不對稱**：任意注入時 $\Omega(\theta)$ 含**多個諧波**，值域不再對稱於 0，於是
$\omega_L^+\ne-\omega_L^-$——真實電路常見、Adler 抓不到的不對稱。

**Injection waveform design**：lock range ＝ $\Omega(\theta)$ 的值域寬度，把注入波形 $i_{inj}$ 的諧波
**對齊 ISF $\tilde\Gamma$ 的諧波**（讓內積更大）就能放大 lock range——比「只能加大注入電流」多一個自由度（波形形狀）。

> **已核實**：$\tilde\Gamma=\Gamma/q_{max}$（Eq.26）、pulling 方程 Eq.(28)–(30)、lock characteristic
> Eq.(33)、正弦退化 Eq.(34)、lock range Eq.(35) 皆已對照 [P3] p.2113–2114 原始 PDF 渲染逐字確認。

### lock range = $\Omega(\theta)$ 的值域（toy 圖示）

把 lock characteristic $\Omega(\theta)$ 直接照 [P3] Eq.(33) 的時間同步平均積分畫出來，就能一眼看懂
「lock range ＝ $\Omega(\theta)$ 的值域寬度、邊緣 ＝ $\Omega(\theta)$ 的 max/min」這句話：

![lock characteristic Ω(θ)：左為正弦注入（Γ̃=−sinθ/q_max）給出乾淨餘弦、對稱於 0（ω_L⁺=−ω_L⁻，經典 Adler）；右為諧波豐富注入給出不對稱 Ω，使 ω_L⁺≠−ω_L⁻，三角形/倒三角標出 lock range 上下邊緣。toy model，[P3] Eq.(33)。](/figures/lock_characteristic_omega.png)

- **左 (a) 正弦注入**：單音 $i_{inj}=I_{inj}\cos\omega_{inj}t$ 注入 ideal-LC ISF $\tilde\Gamma=-\sin\theta/q_{max}$。
  只有 ISF 基波存活（Eq.(34)），$\Omega(\theta)$ 是乾淨餘弦、對稱於 0，邊緣
  $\pm\omega_L=\pm\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$（此 toy 值 $=\pm0.50$ rad/s，正是 Eq.(35)）——這就是經典 Adler。
- **右 (b) 諧波豐富注入**：注入帶基波＋刻意定相的二次諧波、ISF 也含二次諧波。多個諧波同時貢獻，
  $\Omega(\theta)$ **不對稱於 0**：上邊緣 $\omega_L^+=+0.56$、下邊緣 $\omega_L^-=-0.63$ rad/s
  （$\omega_L^+\ne-\omega_L^-$）——真實電路常見、Adler 抓不到的不對稱 lock range。

**怎麼讀**：要鎖定，需 $\omega_{inj}-\omega_0=\Omega(\theta^\*)$ 有解；可達的 $\omega_{inj}-\omega_0$ 範圍正是
$\Omega$ 曲線的值域（兩條水平虛線之間）。把注入波形諧波對齊 ISF 諧波（讓 Eq.(33) 的內積更大）就能把這條曲線
撐高、放大 lock range——比「只能加大 $I_{inj}$」多一個自由度（波形形狀）。

> **toy model 聲明**：這是 pedagogical toy model，**非 transistor-level**。ideal-LC 的 $\Gamma=-\sin\theta$ 為嚴格結果；
> 諧波豐富的 ISF 與被設計的注入波形僅為**示意**，只用來暴露不對稱機制。$\Omega(\theta)$ 由 Eq.(33) 的時間平均積分數值算出。
> 完整 script：`simulations/fig_lock_characteristic.py`（產生 `static/figures/lock_characteristic_omega.png`）。

## Key figures

| 論文圖 | 頁 | 內容 | 教學用途 |
|---|---|---|---|
| Fig. 6 | 2113 | block diagram：注入電流的諧波被 ISF 的諧波**濾波**，形成 lock characteristic | 說明 $\Omega(\theta)$ 為何只留下對齊的諧波 |
| Fig. 7 | 2114 | lock characteristic 的**時域**圖：上/下邊緣與 free-running 三種情形的 ISF×injection 面積 | 直覺看 lock range = 每週期淨面積的極值 |

> 本站**刻意不重畫** [P3] 的 Fig. 6／Fig. 7 這兩張進階圖（無對應 transistor-level toy 模擬）；
> 以上頁碼/內容已對照 [P3] 原文。上方 Key equations 內的 $\Omega(\theta)$ 圖是**獨立的 toy 示意**
> （只示範「lock range ＝ $\Omega(\theta)$ 值域」這個概念），**不是** Fig. 6／Fig. 7 的重畫。

## Design insights

- **lock range 可設計**：lock range ＝ $\langle\Gamma\,i_{inj}\rangle$ 隨 $\phi$ 的值域寬度。
  把注入波形 $i_{inj}$ 的諧波對齊 ISF $\Gamma$ 的諧波（讓內積更大），就能放大 lock range——這比
  「只能加大注入電流」多了一個自由度（波形形狀）。
- **拓樸無關**：只要能萃取出 ISF，ring、LC、relaxation 都適用同一條方程；不必再去量難測的
  $Q$ 與 $I_{osc}$。
- **subharmonic／superharmonic locking**：注入頻率在 $\omega_0/m$ 或 $m\omega_0$ 附近時，是
  $\Gamma$ 的對應諧波在做平均——這直接連到 [P4] 的 frequency division（ILFD）。
- **pulling 是同一條方程的另一面**：當 $|\Delta\omega| > $ lock range，$d\phi/dt$ 不為零、相位
  週期性滑動，產生 pulling spurs。設計時要確保工作頻率落在 lock range 內。

## Limitations

照 paper_metadata（paper_003.limitations）：

- **Part I 只談相位**；振幅調變留到 Part II（APF，[P4]）。
- 依賴**準確萃取的 ISF**——ISF 不準，預測就不準。
- 本站把它當**進階 deep-dive，非核心教學章節**；核心廣義 Adler 公式已對照 [P3] 原文核實。

## Relationship to other papers

- **[P1]** 提供 ISF $\Gamma$ 與 Eq.(11) 的相位推力，是本篇的數學起點。
- **[P2]** 提供 ring 的 ISF，與本篇的 ring 注入（及 [P4] 的 ILFD）相連。
- **[P4]** 是直接續集：補上振幅（APF）、transient pulling 與 frequency division，見
  [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)。
- 廣義 Adler 方程列在 [equation_index](/01_paper_map/equation_index) 第 20 條（[P3] Eq.(30)/(33)/(35)）。

## What to remember

- **同一個 ISF 既算 phase noise，也算 injection locking**——輸入從隨機 noise 換成確定的
  $i_{inj}$（claim C10）。
- **廣義 Adler 方程**：$\dfrac{d\theta}{dt}=(\omega_0-\omega_{inj})+\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt$（[P3] Eq.(30), p.2113，平均項前為 **加號**）。
- **脈衝列思想實驗（[P3] Sec. IV, p.2112）**：每脈衝 kick $\Delta\phi=\pm q_{inj}/q_{max}$（Eq.(19)）；
  每週期 kick 抵銷 detuning 漂移＝鎖定；最大頻移 $\pm q_{inj}/(q_{max}T_{inj})$（Eq.(21)）經
  $\omega_0q_{max}=QI_{osc}$（Eq.(22)）與 $I_{inj}=2q_{inj}/T_{inj}$（Eq.(23)）改寫後與 Adler lock
  range Eq.(18) 一字不差——ImpulseAnimation 的一格 kick 週期化，就是 injection locking。
- **雜訊整形（v5 新增）**：鎖定後振盪器＝一階 PLL——自身雜訊被高通抑制、reference 雜訊低通進入，corner=ω_L cosθ_ss；完整推導與模擬見 [injection_locking_noise](/06_design_insights/injection_locking_noise)。
- **鎖定** = 存在穩態解 / $|\omega_0-\omega_{inj}|\le\omega_L$；**lock range** = lock characteristic $\Omega(\theta)$ 的值域寬度；正弦注入時 $\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$（[P3] Eq.(35), p.2114）。
- 比 Adler 強在：拓樸無關、任意波形、不對稱 lock range、可設計波形放大 lock range。
- 本頁屬**進階**；核心公式（Eq.19–23、26、28–30、33、35）已對照 [P3] p.2112–2114 原始 PDF 核實。

## 延伸閱讀

- 本篇的數學起點 ISF $\Gamma$：[paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)（[P1]）。
- ISF 的傅立葉諧波 $c_n$（為何只有對齊的諧波在 $\Omega(\theta)$ 存活）：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)。
- 直接續集 Part II（APF 振幅、transient pulling、frequency division）：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)（[P4]）。
- 廣義 Adler 在公式索引的位置：[equation_index](/01_paper_map/equation_index)（第 20 條，[P3] Eq.(30)/(33)/(35)）。
- 進階篇在整體路徑中的定位（選修）：[learning_path](/00_overview/learning_path)。
- 五篇論文分工速覽：[paper_summary_table](/01_paper_map/paper_summary_table)。
