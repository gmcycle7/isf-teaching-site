---
title: "[P4] Injection Locking & Pulling — Part II (APF / Frequency Division)"
description: Hong–Hajimiri 2019 Part II 精讀：APF（振幅版 ISF，單位 1/A，[P4] Eq.(18)–(22)）、ISF/APF quadrature（Eq.(26)）、amplitude modulation、M:N 次諧波鎖定與 ILFD（Eq.(28)–(30)：ω_L=½I_inj|Γ̃_N|，÷2 騎在 c2 上）。
---

# A General Theory of Injection Locking and Pulling in Electrical Oscillators—Part II

> **先備知識（建議先讀）**：[paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)（ISF $\Gamma$ 是切向投影）→ [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)（為何振幅被拉回、相位累積）→ [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1)（phase-only 廣義 Adler）。本頁屬**進階**，APF 是 ISF 在徑向的對偶。

[P3] 只談相位；本篇（Part II，**進階**）補上**振幅**這一維。它引入 **APF（Amplitude
Perturbation Function，振幅擾動函數）** $\Lambda(\phi)$——這是「振幅版的 ISF」，單位 $1/\text{A}$
——並用它解釋 LC 振盪器在注入下的 amplitude modulation（振幅調變）、transient（暫態）鎖定行為，
以及 **injection-locked frequency division（注入鎖定頻率除法，ILFD）**。對 ideal LC，ISF 與 APF
**互相正交（quadrature）**。

> **本頁定位**：進階 deep-dive，**非核心教學章節**。APF 的定義式（[P4] Eq.(18)–(22), p.2126）、ideal-LC
> quadrature（Eq.(26), p.2128）與 M:N 次諧波鎖定（Eq.(28)–(30), p.2129；$\omega_L=I_{inj}\vert\tilde\Gamma_N\vert/2$, p.2130）
> 皆已對照原文核實。先讀 [P1]（ISF）與
> [P3](/05_paper_deep_dives/paper_003_injection_locking_part1)（phase-only injection）再讀這裡。

## Citation

> **[P4]** B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in
> Electrical Oscillators—Part II: Amplitude Modulation in LC Oscillators, Transient Behavior,
> and Frequency Division,"* IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2122–2139,
> Aug. 2019.（檔案 `BHongGenTheor-II_JSSC2019_Postprint.pdf`，paper_004）

## One-sentence contribution

定義振幅版的 ISF——APF $\Lambda(\phi)$（單位 $1/\text{A}$）——把 [P3] 的相位框架補成
phase + amplitude 完整模型，解釋注入下的振幅調變、暫態鎖定與 ILFD 頻率除法；對 ideal LC，ISF
與 APF 互成 quadrature（claim C11）。

## Why this paper matters

[P1] 與 [P3] 都假設「振幅擾動會被拉回、可以忽略」。這個假設在 phase noise 與弱注入時很好，但在
**強注入、暫態、或頻率除法**時就不夠了——這時振幅會被明顯調變，相位與振幅互相耦合。Part II 補上
這一維：

- **APF 是振幅的 ISF**：ISF $\Gamma$ 把注入電荷投影到 limit cycle 的**切向**（相位）；APF
  $\Lambda$ 把它投影到**徑向**（振幅）。兩者合起來才是擾動的完整投影。
- **ISF 與 APF 在 ideal LC 互成 quadrature**（差 90°）：相位最敏感的時刻（zero-crossing），
  振幅最不敏感；振幅最敏感的時刻（波峰），相位最不敏感。這正是
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 講「為何振幅噪聲會衰減」
  的數學版本。
- **frequency division（ILFD）**：把一個 $N$ 倍頻的訊號注入振盪器，讓它鎖定在 $1/N$ 子諧波，
  就得到一個低功耗的除頻器。Part II 用 ISF/APF 框架設計這種除頻器，並做出可切換除數的
  dual-modulus prescaler（雙模除頻器）。

## Main assumptions

照 paper_metadata（paper_004.assumptions）：

1. 建立在 Part I 的 time-synchronous ISF 模型之上。
2. 振幅動態以一階方式用 **APF 與 amplitude decay function（振幅衰減函數）** 捕捉。
3. amplitude-modulation 結果聚焦在 **LC 振盪器**。

> **物理直覺（2-D 投影）**：一顆注入電荷 $\Delta q$ 把狀態點推一下。把這推力分解到 limit
> cycle 的兩個正交方向——切向（相位，永久留）用 $\Gamma$ 量、徑向（振幅，會被拉回）用 $\Lambda$
> 量。phase noise 只關心切向；injection 的完整動態兩者都要。

## Key equations

### APF 定義與 amplitude decay function（已對照原始 PDF 核實 ✓）

APF $\tilde\Lambda$ 是 Part I 有單位 ISF $\tilde\Gamma=\Gamma/q_{max}$ 的**振幅類比**：一顆注入電流脈衝
投影到 limit cycle **徑向（振幅）方向**的權重。[P4] 把振幅擾動分解成 APF 與衰減的乘積
$D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$（[P4] Eq.(18), p.2126），並定義 **APF**
$\Delta(\phi):=\int_0^\infty D(\tau,\phi)\,d\tau$（[P4] Eq.(19), p.2126，單位 $1/\text{A}$）。和相位不同，振幅擾動會衰減——
ideal-LC 的 **amplitude decay function（振幅衰減函數）**（在 ideal-LC 一節 [P4] p.2127–2128）為：

$$
d(t,\phi)=e^{-t/\tau_0},\qquad \int_0^\infty d(t,\phi)\,dt=\tau_0=\frac{2Q}{\omega_{osc}}
$$

**關鍵物理（gem）**：振幅的「記憶時間」是 $\tau_0=2Q/\omega_{osc}$——高 $Q$ 的 LC 振幅恢復**慢**（$\tau_0$ 大），
但**終究會恢復**（指數衰減回 limit cycle）；相位則沒有這種恢復力（脈衝響應是 unit step，記憶無限長）。
這正是「為何振幅噪聲被抑制、相位噪聲累積」（claim C2）的**量化版本**。對 ideal LC，APF 與 decay 的關係為
$\Delta(\phi)=\tau_0\,\tilde\Lambda(\phi)$。

**對照表（ISF vs APF）**：

| 量 | 投影方向 | 符號 | 擾動命運 |
|---|---|---|---|
| ISF | 切向（phase） | $\tilde\Gamma=\Gamma/q_{max}$ | 永久累積（脈衝響應 = unit step） |
| APF | 徑向（amplitude） | $\tilde\Lambda$ | 以 $e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$ 衰減回 limit cycle |

> **已核實**：APF 分解 $D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$（[P4] Eq.(18), p.2126）、APF 定義
> $\Delta(\phi)=\int_0^\infty D\,d\tau$（[P4] Eq.(19), p.2126，單位 $1/\text{A}$），以及 ideal-LC 的 decay function
> $e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$（[P4] ideal-LC 一節 p.2127–2128），皆對照原始 PDF 渲染逐字確認。

### ISF 與 APF 的 quadrature（ideal LC，已核實 ✓）

ideal LC 的 ISF 與 APF **基波**（[P4] Eq.(26), p.2128）：

$$
\tilde\Gamma_1=\frac{1}{q_{max}}\,\angle 90^\circ,\qquad
\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\,\angle 0^\circ
$$

兩者相位差正好 **$90^\circ$（quadrature）**（claim C11）。物理意義：在 zero-crossing 注入幾乎純改相位
（$\tilde\Gamma$ 大、$\tilde\Lambda$ 小）；在波峰注入幾乎純改振幅（$\tilde\Lambda$ 大、$\tilde\Gamma$ 小）。
注意 APF 基波比 ISF 多一個 $\tau_0$ 因子——**高 $Q$ 時振幅效應（$\propto\tau_0=2Q/\omega_0$）反而更顯著**，
這也是為何 LC 注入鎖定常伴隨可觀的 amplitude modulation。

**amplitude-corrected Adler（augmented pulling，ideal-LC 特例 [P4] Eq.(27), p.2128）**：把 ISF 與 APF
一起代入。一般正弦注入的形式是 [P4] Eq.(22), p.2126（帶 $+$ 號與 $\cos(\theta+\angle\tilde\Gamma_1)/\cos(\theta+\angle\tilde\Lambda_1)$ 的相位偏移項）；
再把 ideal-LC 的 quadrature 角 $\angle 90^\circ/\angle 0$（Eq.(26)）代入 Eq.(22)，正弦注入下的相位方程化簡成

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})-\frac{\tfrac12\,(I_{inj}/q_{max})\sin\theta}{1+\tfrac12\,(I_{inj}\tau_0/q_{max})\cos\theta}
$$

分母那一項就是 APF 帶來的 **amplitude modulation 修正**；Part I 的純相位 Adler 是分母 $=1$ 的特例。

> **已核實**：$\tilde\Gamma_1,\tilde\Lambda_1$ 的 quadrature（[P4] Eq.(26), p.2128；sin/cos 形式見 Eq.(24)）
> 與上方顯示的 amplitude-corrected Adler——即 **ideal-LC 特例 [P4] Eq.(27), p.2128**（由 Eq.(26) 的 $\angle 90^\circ/\angle 0$ 代入一般式 Eq.(22), p.2126 得到，帶 $-$ 號、$\sin\theta$ 分子與 $\tau_0$ 因子）——皆對照原始 PDF 渲染逐字確認。

### amplitude modulation（APF 的傅立葉觀點）

**Meaning**：把 APF 展成傅立葉級數後，可算出注入波形如何被「濾」成 amplitude modulation
（[P4] Sec. III-D 文字）。具體級數分配與除數切換見
[P4] Sec. VIII（dual-modulus prescaler，p.2135 起；schematic Fig.19、Table VIII、Fig.21 在 p.2137）。

### M:N 次諧波鎖定與 ILFD 的正式數學（[P4] Sec. IV, Eq.(28)–(30), p.2129，已核實 ✓）

[P3] 的廣義 Adler 只處理 $\omega_{inj}\approx\omega_0$。[P4] Sec. IV 把它推廣到**任意有理數頻率比**：
鎖定時 $M\omega_{inj}=N\omega_{osc}$（$M,N$ 互質正整數）。這就是 **ILFD**（$M=1$：輸出
$=\omega_{inj}/N$，÷$N$ 除頻）與 injection-locked frequency multiplier（$N=1$：×$M$ 倍頻）共用的
數學。整個推導只用一招：**時間同步平均只留下「共振」的那一個 ISF 諧波**。以下逐步。

**第 1 步（重新定義相對相位，[P4] Eq.(28), p.2129）**：

$$
\varphi(t)\equiv\frac{M}{N}\,\omega_{inj}t+\theta(t)
$$

$\varphi$ 是振盪器總相位 [rad]，$\theta$ 是相對注入時鐘的慢變相位 [rad]。÷2 ILFD 取 $M=1$、$N=2$：
注入 $\omega_{inj}\approx2\omega_0$，振盪器跑在 $\omega_{inj}/2$。

**第 2 步（廣義 pulling equation，[P4] Eq.(29), p.2129）**：把 Eq.(28) 代入瞬時 pulling 方程（與
[P3] Eq.(28)–(29), p.2113 同一步驟，只是把 $\omega_{inj}t$ 換成 $(M/N)\,\omega_{inj}t$），再在
$NT_{inj}$（**不是** $T_{inj}$）的窗上做時間同步平均：

$$
\frac{d\theta}{dt}=\omega_0-\frac{M}{N}\omega_{inj}+\frac{1}{NT_{inj}}\int_{NT_{inj}}\tilde\Gamma\!\left(\frac{M}{N}\omega_{inj}t+\theta\right)i_{inj}(t)\,dt
$$

為何窗取 $NT_{inj}$？窗內注入波形走 $N$ 整圈；ISF 引數前進 $(M/N)\,\omega_{inj}\cdot NT_{inj}=2\pi M$，
走 $M$ 整圈。[P4] p.2129 原文明說：框架**不要求**注入或 ISF 的基本週期等於平均區間，
"they need only iterate through an *integer* number of cycles over a single averaging period"——
這是整個 M:N 理論的樞紐。

**第 3 步（逐項平均——只有共振諧波存活）**：取 $M=1$、正弦注入 $i_{inj}=I_{inj}\cos(\omega_{inj}t)$
（$I_{inj}$ 單位 A）。把 $\tilde\Gamma$ 展成 phasor 傅立葉級數（與 [P1] Eq.(12) 同一展開；對應關係
$\vert\tilde\Gamma_n\vert=c_n/q_{max}$，單位 rad/C）：

$$
\tilde\Gamma(\varphi)=\tilde\Gamma_{dc}+\sum_{n=1}^{\infty}\vert\tilde\Gamma_n\vert\cos\!\big(n\varphi+\angle\tilde\Gamma_n\big)
$$

第 $n$ 項與注入相乘後用積化和差（$\cos A\cos B=\tfrac12[\cos(A-B)+\cos(A+B)]$）：

$$
\vert\tilde\Gamma_n\vert\cos\!\Big(\tfrac{n}{N}\omega_{inj}t+n\theta+\angle\tilde\Gamma_n\Big)\,I_{inj}\cos(\omega_{inj}t)
=\frac{I_{inj}\vert\tilde\Gamma_n\vert}{2}\left[\cos\!\Big(\tfrac{n-N}{N}\omega_{inj}t+n\theta+\angle\tilde\Gamma_n\Big)+\cos\!\Big(\tfrac{n+N}{N}\omega_{inj}t+n\theta+\angle\tilde\Gamma_n\Big)\right]
$$

在 $NT_{inj}$ 窗上，差頻項相位前進 $2\pi(n-N)$、和頻項前進 $2\pi(n+N)$——除了 $n=N$ 的差頻項
（頻率恰為 0）之外，**全部走整數圈、平均精確歸零**（這是恆等式，不是「近似很小」；lab_37 數值驗證
到 $10^{-15}$）。存活的唯一一項就是 [P4] Eq.(30), p.2129：

$$
\Omega(\theta)=\frac{1}{2}\,I_{inj}\,\vert\tilde\Gamma_N\vert\cos\!\big(N\theta+\angle\tilde\Gamma_N\big)
$$

> **factor-of-2 記帳**：這裡的 $\tfrac12$ 是**積化和差的 $\tfrac12$**（兩個餘弦相乘、只有差頻項存活），
> 與 phase-noise 頁的 SSB $/4$ vs 時域 $/2$ 記帳慣例（[P1] Eq.(21) 的那個 4）**無關**。

**第 4 步（lock range 與 $2\pi/N$ 簡併）**：dimension check：$[\text{A}]\times[\text{rad/C}]=[\text{C/s}]\times[\text{rad/C}]=[\text{rad/s}]$ ✓。
鎖定 ＝ $d\theta/dt=0$ 有穩定解 ⟺
$\vert\omega_{inj}/N-\omega_0\vert\le\max_\theta\Omega(\theta)$，故半鎖定範圍
（[P4] p.2130 原文 "which can be calculated from (30) to be $\omega_L=I_{inj}\vert\tilde\Gamma_N\vert/2$"）：

$$
\omega_L=\frac{1}{2}\,I_{inj}\,\vert\tilde\Gamma_N\vert=\frac{I_{inj}\,c_N}{2\,q_{max}}
$$

三個立刻可讀的物理：

1. **除頻比 $N$ 不直接出現在公式裡**——它只決定「用哪一個諧波 $c_N$」。÷2 的 lock range 騎在
   $c_2$ 上、÷3 騎在 $c_3$ 上（lab_37 圖 (b)：兩組量測落在**同一條** $f_L\propto c_N$ 直線上）。
2. $\omega_L$ 以**輸出（振盪）頻率軸**計（$\Delta\omega\equiv\omega_{inj}/N-\omega_0$，[P4] p.2130）；
   換到注入頻率軸，可鎖的 $\omega_{inj}$ 窗寬是 $2N\omega_L$。
3. $\Omega(\theta)$ 的週期是 $2\pi/N$ ⟹ 有 **$N$ 個相距 $2\pi/N$、彼此不可分辨的穩定鎖定相位**
   （[P4] p.2129 原文："relative phases that are $2\pi/N$ apart are indistinguishable"）。這正是除頻器
   眾所周知的 output phase ambiguity（÷$N$ 輸出有 $N$ 個可能的相位起點），做多相/quadrature 時鐘時要另行處理。

> **例（÷2 ILFD：10 GHz 進、5 GHz 出，canonical 數值）**：給定 $f_0=5$ GHz、$q_{max}=1$ pC、
> $I_{inj}=0.5$ mA 正弦注入在 $f_{inj}\approx10$ GHz、ISF 第 2 諧波 $c_2=0.5$。
> 1. $\vert\tilde\Gamma_2\vert=c_2/q_{max}=0.5/10^{-12}=5\times10^{11}$ rad/C。
> 2. $\omega_L=\tfrac12 I_{inj}\vert\tilde\Gamma_2\vert=\tfrac12\,(5\times10^{-4}\,\text{A})(5\times10^{11}\,\text{rad/C})=1.25\times10^{8}$ rad/s。
> 3. $f_L=\omega_L/2\pi=19.9$ MHz（只有 $f_0$ 的 $0.40\%$）；注入頻率軸的可鎖窗寬
>    $2Nf_L=79.6$ MHz（在 10 GHz 附近）。
> 4. dimension check：A $\times$ rad/C ＝ rad/s ✓。弱注入檢查：$I_{max}:=\omega_0 q_{max}=31.4$ mA
>    （[P4] footnote 11, p.2130），$I_{inj}/I_{max}=1.6\%$ ⟹ 一階線性模型適用。
>
> 一行 Python 驗證：`0.5*0.5e-3*0.5/1e-12` → $1.25\times10^{8}$。

**Payoff：半波對稱的 ISF 不能 ÷2**。回看
[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) 第 7 步的對稱表：**半波對稱**
$\Gamma(x+\pi)=-\Gamma(x)$ ⟹ 偶次諧波 $c_2=c_4=\cdots=0$。代進
$\omega_L=I_{inj}c_2/(2q_{max})$：÷2 的 lock range **恆等於零**——一階內，任你把 $I_{inj}$ 加多大，
$2f_0$ 注入就是鎖不上。同一張對稱表在 phase-noise 那邊是好消息（$2\omega_0$ 的 noise 不折回
carrier），在 ILFD 這邊卻是壞消息：**對稱是雙面刃**。設計上的出路是換注入節點——ISF 是「每個注入
節點各一條」的（同 [P1]），差動輸出節點因對稱 $c_2\approx0$，但 **tail（尾流）節點本來就以 $2f_0$
擺動、從那裡看進去的等效 ISF 偶次諧波很大**；[P4] 的 ÷2 實驗正是把 $2f_0$ 打進 differential LC 的
tail（Fig. 11(a)(b) caption 與 Fig. 12(d)，p.2130–2131，已核實）。

**暫態與鎖外行為（[P4] Eq.(31)–(34), p.2130，已核實 ✓）**：鎖內，相位以 pull-in frequency
$\omega_p=N\sqrt{\omega_L^2-\Delta\omega^2}$（Eq.(32)）指數收斂到鎖定相位（Eq.(31) 給出 tanh 閉式
解）；鎖外，$\theta$ 以 beat frequency $\omega_b=N\sqrt{\Delta\omega^2-\omega_L^2}$（Eq.(34)）拍動、
平均漂移率為 $\omega_b/N$，頻譜長出間距 $\omega_b$ 的 sideband——[P3] 的 quasi-lock/pulling 故事在
M:N 版重演。

**適用／失效條件**：

- 一階平均要求**弱注入**（$I_{inj}\ll I_{max}=\omega_0 q_{max}$，[P4] footnote 11, p.2130）與
  $\omega_L\ll\omega_0$；強注入要加上一節的 APF 修正（Eq.(27) 的分母）與振幅動態。
- $M\neq1$（subharmonic 注入、倍頻器）需要注入訊號的第 $M$ 諧波——正弦注入沒有諧波，實務上靠
  **振盪器內部混頻**產生；[P4] footnote 10, p.2129 明說這不在框架內（部分由其引文 [25] 的模型處理）。
  本站把倍頻方向獨立成一頁：假設注入波形自帶第 $N$ 諧波（脈衝產生器即可），從本頁 Eq.(29)
  直接推出倍頻閉式 $\omega_L=\tfrac12\vert I_N\vert\vert\tilde\Gamma_1\vert$——見
  [subharmonic_injection](/06_design_insights/subharmonic_injection)；除頻方向（本節主線）
  的完整教學頁在 [injection_locked_division](/06_design_insights/injection_locked_division)。
- 「$c_2=0$ 不能 ÷2」是一階結論：更高階的混頻仍可能留下極小的殘餘 lock range（在 lab_37 的偵測
  底線之下）。

**實驗證據（[P4] Fig. 12, p.2131，已核實 ✓）**：Bose relaxation oscillator（$f_0=11.9$ MHz）在
$N=2,3,4,5$、17 級單端 inverter-chain ring（$f_0=1.09$ GHz）在 $N=2,5$、6 級差動 ring 與 NMOS
astable multivibrator 在 $N=3$、differential LC tail 在 $N=2$——量測 lock range 全部隨 $I_{inj}$
線性、斜率由 $\vert\tilde\Gamma_N\vert$ 決定，與 Eq.(30) 的預測吻合。

#### 數值驗證：lab_37（未平均 ODE 掃頻 + 諧波地圖）

用**未平均**的瞬時方程直接積分（若拿已平均的 Eq.(30) 來驗證 Eq.(30) 就是循環論證）：

$$
\frac{d\theta}{dt}=\Big(\omega_0-\frac{\omega_{inj}}{N}\Big)+\tilde\Gamma\!\Big(\frac{\omega_{inj}}{N}t+\theta\Big)\,I_{inj}\cos(\omega_{inj}t)
$$

ISF 用 3 諧波 toy（**pedagogical toy，非 transistor-level**）：
$\tilde\Gamma(x)=-\big(c_1\sin x+c_2\sin2x+c_3\sin3x\big)/q_{max}$（即 $\angle\tilde\Gamma_n=90^\circ$）。

| 參數 | 值 | 單位 |
|---|---|---|
| $f_0$ | 5 | GHz |
| $q_{max}$ | 1 | pC |
| $I_{inj}$ | 0.5 | mA |
| $(c_1,c_2,c_3)$ | $(1.0,\,0.5,\,0.2)$ | — |
| ODE 步長 / 總時長 | 1 ps / 600 ns | — |
| 理論 $f_L$（$N=2$, $c_2=0.5$） | 19.89 | MHz |
| 理論 $f_L$（$N=3$, $c_3=0.2$） | 7.96 | MHz |

```bash
PYTHONPATH=. python simulations/lab_37_ilfd_lock.py
# -> 1.13e-15 / 3.19e-15（Eq.(29) 數值平均 vs Eq.(30) 閉式，N=2 / N=3 的最大相對誤差：恆等式等級）
# -> 1.033（2f0 掃頻：量測 omega_L / 理論 1.25e8 rad/s；61 點網格的解析度 ~3%）
# -> 1.000（3f0 掃頻：量測 omega_L / 理論 5e7 rad/s）
# -> 0/61（半波對稱 c2=0 ISF 在同一 ±2 omega_L 網格上的鎖定點數：完全鎖不上、無 ÷2）
# -> 1.004 / 1.019（lock range 對 c2（N=2）、對 c3（N=3）掃描的量測/理論平均比值：線性成立）
# -> 1.000（鎖外平均漂移率 / (omega_b/N)，[P4] Eq.(34)）
# -> 3.1330（N=2 兩個不同初始相位收斂後的差，理論 2pi/2=3.1416：2pi/N 簡併）
```

![lab_37：(a) N=2/N=3 掃頻的鎖定平台（c2=0 無平台）；(b) 量測 lock range 對 c_N 線性、兩組落在同一條線；(c) 時間同步平均只留第 N 諧波、Ω(θ) 週期 2π/N](/figures/ilfd_lock_ranges.png)

**如何解讀**（完整 script：`simulations/lab_37_ilfd_lock.py`，runtime ≈ 19 s）：

- **(a)**：橫軸 $\Delta\omega/\omega_L$、縱軸 $\theta$ 的平均漂移率。鎖定＝漂移率 0 的平台，平台半寬
  正好 $\omega_L$；平台外量測點落在理論曲線
  $\mathrm{sgn}(\Delta\omega)\sqrt{\Delta\omega^2-\omega_L^2}$（$=\omega_b/N$，Eq.(34)）上。紅色
  $c_2=0$（半波對稱）的曲線是一條過原點的直線（漂移＝失諧）：**任何失諧都不鎖**。
- **(b)**：量測半鎖定範圍對 $c_N$ 作圖——$N=2$ 與 $N=3$ 的點落在**同一條**理論直線
  $f_L=I_{inj}c_N/(4\pi q_{max})$ 上（$N$ 只挑諧波、不進公式）。
- **(c)**：把 Eq.(29) 的平均積分逐 $\theta$ 數值算出，與 Eq.(30) 閉式重疊；$N=2$ 週期 $\pi$、$N=3$
  週期 $2\pi/3$，肉眼可見 $2\pi/N$ 簡併。

**限制**：一階 phase-only toy（無 APF/振幅動態、無雜訊）；ISF 諧波只到 $n=3$；
lock 邊緣判定受 600 ns 積分窗與網格解析度限制（~1–3%）。

## Key figures

| 論文圖 | 頁 | 內容 | 教學用途 |
|---|---|---|---|
| Fig. 5 | 2126 | characterizing 注入電荷瞬間對振盪器的影響：ISF／excess phase、amplitude decay function、及 ISF 與 APF 的 quadrature 關係（已核實） | 連結相位（ISF）與振幅（APF）敏感度的最佳單圖 |
| Fig. 11 | 2130 | superharmonic 正弦鎖定特性模擬：1 mA 與 2 mA 的二次諧波注入 differential LC 的 **tail**（$I_{tail}=1$ mA）、5 mA 三次諧波注入 ideal Bose oscillator（caption 已核實） | ÷2/÷3 的 lock characteristic 對照 Eq.(30)；÷2 打 tail＝繞過差動節點的 $c_2\approx0$ |
| Fig. 12 | 2131 | superharmonic lock range 量測：Bose relaxation（$N=2..5$）、17 級 ring（$N=2,5$）、多種振盪器（$N=3$）、differential LC tail（$N=2$）（caption 已核實） | $\omega_L=I_{inj}\vert\tilde\Gamma_N\vert/2$ 的實驗驗證：對 $I_{inj}$ 線性 |

這張圖是「為何振幅噪聲會衰減、相位噪聲不會」的最佳視覺：APF 對應的擾動會被 amplitude decay
function 拉回，ISF 對應的相位擾動則永久留下。本站在
[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 用這個概念（toy 對照圖
`limit_cycle_phase_amplitude.png`，**非 transistor-level**）。

> **已核實**：此圖為 [P4] Fig. 5, p.2126，標題「Characterizing the effect that an instantaneous injection of
> charge has on an oscillator」，已對照原始 PDF 渲染確認。（Fig. 3 p.2124 是 impulse-train↔sinusoid 等價、Fig. 6
> p.2127 是 bipolar Colpitts 範例，皆非此圖。）

![limit cycle：切向=相位（持續）、徑向=振幅（被拉回）（toy）](/figures/limit_cycle_phase_amplitude.png)

## Design insights

- **強注入／暫態要看振幅**：弱注入時忽略 APF 沒問題；強注入、暫態鎖定、頻率除法時，振幅調變
  不可忽略，必須 ISF + APF 一起算。
- **quadrature 是設計工具**：想純調相位就在相位敏感點（ISF 極值）注入；想做振幅鍵控／AM 就在
  振幅敏感點（APF 極值）注入。
- **ILFD 是低功耗除頻器**：相較 latch-based／CML divider 在高頻耗電大，ILFD 用注入鎖定除頻，
  功耗低；用 ISF/APF 的第 $N$ 諧波設計除數與 lock range。
- **dual-modulus prescaler**：靠 quadrature 注入方案在同一條 inverter-chain ring 上切換除數，
  省功耗。
- **大注入與暫態的剩料**：Mirzaei 廣義 Adler（Eq.(8)–(9)）、精確 pull-in/pulling 閉式解
  （Eq.(31)–(34)）、APF 驅動的振幅暫態（dip→overshoot）與大注入 pulling 頻譜的完整逐步推導、
  數值驗證收在 [paper_004_large_injection_transient](/05_paper_deep_dives/paper_004_large_injection_transient)。

## Limitations

照 paper_metadata（paper_004.limitations）：

- 強非線性、超出一階 APF 的效應只被部分捕捉；$M\neq1$ 所需的注入諧波靠內部混頻產生，
  不在框架內（[P4] footnote 10, p.2129）。
- 對本站核心 ISF phase-noise 目標而言屬**進階／邊陲**。
- APF 的確切方程（[P4] Eq.(18)–(22), p.2126；quadrature Eq.(26), p.2128）與 M:N 鎖定
  （Eq.(28)–(30), p.2129；$\omega_L$, p.2130）已對照原文核實（claim C11）。

## Relationship to other papers

- **[P3]** 是直接前傳：本篇用 Part I 的 time-synchronous ISF 模型，補上振幅（APF）。
- **[P1]** 提供 ISF $\Gamma$；APF 是其在徑向的對偶。ideal LC 的 $\Gamma=-\sin$ 也出現在本站
  [isf_definition](/03_isf_core_theory/isf_definition)。
- **[P2]** 提供 ring 的 ISF；本篇的 ILFD/prescaler 就用 inverter-chain ring 實作。
- **[P5]** 與本頁無關（sense amplifier）；但 LC／latch 振盪器的起振同樣靠 cross-coupled 正回授
  （claim C12 的邊角橋樑）。
- APF 列在 [equation_index](/01_paper_map/equation_index) 第 21 條（本頁已對照 [P4] Eq.(18)–(22) 核實）；相位／振幅幾何見
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)。

## 延伸閱讀 / 對應教學頁

| 本頁的哪一塊 | 對應教學頁 | 那頁多給你什麼 |
|---|---|---|
| ÷$N$ lock range 騎在 $c_N$ 上、半波對稱 ⟹ $c_2=0$ 不能 ÷2 | [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) | ISF 傅立葉展開、第 7 步的對稱性表（奇函數 ⟹ $c_0=0$；半波對稱 ⟹ 偶次諧波歸零） |
| 注入相位決定 $\Gamma$／$\Lambda$ 的有效權重（cyclostationary 觀念） | [effective_isf](/03_isf_core_theory/effective_isf) | $\Gamma_{eff}=\Gamma\cdot\alpha$、bias-dependent 熱雜訊 NMF、switching-pair worked example |
| 注入相位如何改變有效 ISF（數值手感） | [lab_14_cyclostationary_isf](/04_simulation_labs/lab_14_cyclostationary_isf) | 可跑的 toy：noise 注入相位 $\to$ $\Gamma_{eff,rms}$（**pedagogical toy，非 transistor-level**） |
| ISF／APF 的 quadrature、injection locking 的耦合振盪器 | [quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators) | quadrature 注入、coupled-oscillator 的相位關係與設計 |

> **怎麼讀**：本頁把 [P3] 的相位框架補成 phase + amplitude；想理解「為何注入相位（或 noise 注入相位）會改變有效敏感度」，effective_isf 與 lab_14 是同一個 cyclostationary 觀念的理論與動手版本；想看 quadrature 如何變成可用的設計工具，回 quadrature_and_coupled_oscillators。相位／振幅幾何另見 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)。

## What to remember

- **APF = 振幅版 ISF**，單位 $1/\text{A}$；ISF 投影到切向（相位），APF 投影到徑向（振幅）。
- **ideal LC：ISF 與 APF 互成 quadrature（差 $90°$）**——相位最敏感時振幅最不敏感，反之亦然
  （claim C11）。
- **相位永久累積、振幅被 decay function 拉回**——這就是「只追相位」在 phase noise 成立的根據。
- **ILFD**：注入 $\omega_{inj}\approx N\omega_0$、靠 ISF 第 $N$ 諧波鎖定到 $\omega_{inj}/N$，
  半鎖定範圍 $\omega_L=\tfrac12 I_{inj}\vert\tilde\Gamma_N\vert=I_{inj}c_N/(2q_{max})$
  （[P4] Eq.(30) p.2129 與 p.2130）；$N$ 只挑諧波、不進公式；輸出有 $N$ 個相距 $2\pi/N$ 的
  不可分辨鎖定相位。
- **半波對稱 ISF（$c_2=0$）一階內不能 ÷2**——phase noise 的好對稱是 ILFD 的壞消息；
  [P4] 的 ÷2 實驗把 $2f_0$ 打進 differential LC 的 tail 來繞過它。
- 本頁屬**進階**；APF 確切式（[P4] Eq.(18)–(22), p.2126；quadrature Eq.(26), p.2128）與
  M:N 鎖定（Eq.(28)–(30), p.2129；$\omega_L$, p.2130）已對照原文核實。
