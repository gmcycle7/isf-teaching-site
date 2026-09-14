---
title: "規格驅動設計配方：從 spec 到 jitter 的 7 步"
description: "一條反向設計流程：規格 L(1 MHz)≤−120 dBc/Hz @ 5 GHz、P≤5 mW、TR 10% → 所需 FOM 187.0 dB → 對 fom_limit 天花板判定 ring（168.3）不可行、LC Q=10（197.6）可行 → tank C=1 pF、L=1.013 nH、Rp=318 Ω → V_max=1 V、q_max=1 pC、I_bias=2.47 mA → S_i=4kT(1+γ)/Rp=1.04e-22 A²/Hz → [P1] Eq.(21) 得 −124.8 dBc/Hz（餘裕 4.8 dB、FOM 194.9 dB）→ 1–100 MHz 積分 jitter 25.7 fs；附迭代規則（每個旋鈕買幾 dB、花多少功率）與 FOM_T 定義。"
sidebar_position: 9
---

import NumericQuiz from "@site/src/components/NumericQuiz";

# 規格驅動設計配方：從 spec 到 jitter 的 7 步

> **先備**：[fom_limit](/06_design_insights/fom_limit)（$\mathrm{FOM}=173.8-10\log_{10}F_{eff}$ 天花板家族）、[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)（$Q$ 的三種寫法、$4kT/R_p$）、[tank_swing](/06_design_insights/tank_swing)（$q_{max}=CV_{max}$、current/voltage-limited、$\tfrac{4}{\pi}I_{bias}R_p$）、[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（[P1] Eq.(21) 與 /2 vs /4 慣例）｜ **接下來**：[pll_noise_budget](/06_design_insights/pll_noise_budget)、[clock_chain_budget](/06_design_insights/clock_chain_budget)、[lab_09_design_tradeoffs](/04_simulation_labs/lab_09_design_tradeoffs)

本站其他設計頁都是「**正向**」的：給你 $q_{max}$、$\Gamma_{rms}$、$S_i$，算出 $\mathcal{L}(\Delta f)$；
或是「**單旋鈕反推**」：只動 $q_{max}$ 要放大幾倍（[exercises](/06_design_insights/exercises) 習題 1）、
只動 $Q$ 該多高（[fom_limit](/06_design_insights/fom_limit) 例 2）。真正的設計工作卻是反過來的：
**手上只有一張規格表**（phase noise、功率、調諧範圍），要一路決定拓樸、tank 元件值、swing、
偏壓電流，最後回頭驗證規格達標、再換算成系統要的 jitter。這頁把這條路寫成一份可以重複套用的
**配方（recipe）**：7 個步驟、一組數字從頭算到尾、每一步都標明用了哪條公式、單位是否合、
什麼情況下會失效；最後給出「餘裕不夠時該轉哪個旋鈕、每轉一格買幾 dB、花多少功率」的迭代規則。

> **物理直覺（先講結論）**：規格表裡的三個數字 $\mathcal{L}$、$P$、$f_0/\Delta f$ 合成**一個**數字——
> 所需 FOM。這個數字跟 [fom_limit](/06_design_insights/fom_limit) 的天花板家族一比，**拓樸就決定了**
> （ring 的天花板 168.3 dB 是一道硬牆）。拓樸定了之後，LC 的 $\mathcal{L}$ 只由四樣東西決定：
> $Q$（雜訊源 $4kT/R_p$ 有多小）、$q_{max}=CV_{max}$（訊號電荷有多大）、$F$（除了 tank 還有誰在吵）、
> $\Gamma_{rms}$（波形形狀）——這正是 [P1] Eq.(21) 的四個因子。配方的工作就是把這四個因子一個一個
> **釘死成元件值與偏壓**，然後用 Eq.(21) 驗收。

```mermaid
flowchart LR
  S0["Step 0<br/>規格 L, P, f0, TR"] --> S1["Step 1<br/>FOM_req"]
  S1 --> S2["Step 2<br/>對天花板：ring / LC？"]
  S2 --> S3["Step 3<br/>tank：C, L, Rp（Q）"]
  S3 --> S4["Step 4<br/>swing：V_max, q_max, I_bias, P"]
  S4 --> S5["Step 5<br/>雜訊：S_i = F·4kT/Rp"]
  S5 --> S6["Step 6<br/>[P1] Eq.(21) 驗收 L(Δf)"]
  S6 --> S7["Step 7<br/>jitter σ_t → PLL/時脈鏈"]
  S6 -. "餘裕 < 0：迭代" .-> S3
```

## Step 0：把規格寫成數學

假設系統工程師交來的規格是（本頁全程用這一組）：

| 規格項 | 值 | 讀法 |
|---|---|---|
| 載波 $f_0$ | $5$ GHz | 站台 canonical 頻率 |
| SSB phase noise $\mathcal{L}(\Delta f)$ | $\le-120$ dBc/Hz @ $\Delta f=1$ MHz | 白噪 $1/f^2$ 區的一點（假設 1 MHz 已在 $1/f^3$ corner 之外） |
| 總 DC 功耗 $P$ | $\le5$ mW | 含 core 與 bias，不含 buffer（見失效條件） |
| 調諧範圍 TR | $10\%$（$4.75\sim5.25$ GHz） | 影響 varactor 佔比與 FOM$_T$（本頁末） |
| 溫度 | $300$ K | $kT=4.142\times10^{-21}$ J |

- **為什麼只需要「一點」的 $\mathcal{L}$**：在 $1/f^2$ 區，$\mathcal{L}$ 對 $\Delta f$ 是 $-20$ dB/dec 的直線
  （[P1] Eq.(21) 的 $1/\Delta\omega^2$），一點就定整段。若規格點落在 $1/f^3$ 區（close-in），
  本配方要先用 [symmetry](/06_design_insights/symmetry) 把 corner 壓到規格點以下，再回來套。
- **spec 的三個數字不獨立**：$\mathcal{L}$ 越嚴可以用 $P$ 換（[tank_swing](/06_design_insights/tank_swing) 第 4 步的
  「$\mathcal{L}\times P\approx$ 常數」），所以下一步先把它們合成一個與功率無關的數字。

## Step 1：規格 → 所需 FOM

用 [fom_limit](/06_design_insights/fom_limit) 第 0 步的正值慣例（越大越好），把規格的三個數字合成**所需 FOM**：

$$
\mathrm{FOM}_{req}=-\mathcal{L}_{spec}+20\log_{10}\!\left(\frac{f_0}{\Delta f}\right)-10\log_{10}\!\left(\frac{P_{max}}{1\ \text{mW}}\right)
$$

逐項代入（帶單位）：

$$
\begin{aligned}
20\log_{10}\!\left(\frac{f_0}{\Delta f}\right)&=20\log_{10}\!\left(\frac{5\times10^{9}\ \text{Hz}}{10^{6}\ \text{Hz}}\right)=20\log_{10}(5000)=73.98\ \text{dB},\\[4pt]
10\log_{10}\!\left(\frac{P_{max}}{1\ \text{mW}}\right)&=10\log_{10}\!\left(\frac{5\ \text{mW}}{1\ \text{mW}}\right)=6.99\ \text{dB},\\[4pt]
\mathrm{FOM}_{req}&=120+73.98-6.99=186.99\approx187.0\ \text{dB}.
\end{aligned}
$$

- **讀法**：這是「在 5 mW 預算內達到 $-120$ dBc/Hz」所需的**最低** FOM。功率用得比 5 mW 少、
  或 $\mathcal{L}$ 做得比 $-120$ 好，實際 FOM 都要比 187.0 高。
- **Dimension check**：三項都是無因次比值的 $\log_{10}$（$\text{Hz}/\text{Hz}$、$\text{W}/\text{W}$、$\mathcal{L}$ 的 1 Hz 頻寬歸一）→ dB ✓。
- **為什麼用 $P_{max}$**：FOM 對 $P$ 的符號是負的——功率上限給的是**最寬鬆**的 FOM 需求；
  之後若實作只燒 2.5 mW，所需 FOM 會自動升 3 dB（Step 6 會看到）。

```python
import numpy as np
f0, df, L_spec, P_max = 5e9, 1e6, -120.0, 5e-3
print(round(20*np.log10(f0/df), 2))                       # -> 73.98
print(round(10*np.log10(P_max/1e-3), 2))                  # -> 6.99
FOM_req = -L_spec + 20*np.log10(f0/df) - 10*np.log10(P_max/1e-3)
print(round(FOM_req, 2))                                  # -> 186.99 （所需 FOM，dB）
```

<NumericQuiz
  prompt="先自己算：若規格改成 L(1 MHz) ≤ −125 dBc/Hz、P ≤ 2 mW（f0 仍 5 GHz），所需 FOM_req = ？（dB）"
  answer={195.97}
  tol={0.01}
  unit="dB"
  hint="FOM_req = −L + 20log10(f0/Δf) − 10log10(P/1 mW)；20log10(5000)=73.98。"
  solutionNote="125 + 73.98 − 10log10(2) = 125 + 73.98 − 3.01 = 195.97 dB——已經逼近 Q=10 的 LC 天花板 197.6 dB，Step 2 會判定「幾乎不可行」。"
/>

## Step 2：對天花板——ring 還是 LC？

把 $\mathrm{FOM}_{req}$ 拿去對 [fom_limit](/06_design_insights/fom_limit) 第 4 步的天花板家族
（$\mathrm{FOM}_{max}=173.83-10\log_{10}F_{eff}$，300 K）：

| 候選拓樸 | $F_{eff}$ | $\mathrm{FOM}_{max}$ | 對 $\mathrm{FOM}_{req}=187.0$ | 判定 |
|---|---|---|---|---|
| ring（[P2] Eq.(25) 下限：$V_T=0$、$\gamma=2/3$、$\eta=1$） | $16\gamma/(3\eta)=3.56$ | $168.32$ dB | $168.32-186.99=-18.67$ dB | **不可行**——連理想極限都差 18.7 dB |
| LC、$Q=10$（[P1] Eq.(21) SSB /4；$F=1+\gamma$、$\gamma=2/3$、$\Gamma_{rms}^2=\tfrac12$、$\eta_P=1$） | $4.17\times10^{-3}$ | $197.63$ dB | $197.63-186.99=+10.64$ dB | **可行**，理想餘裕 10.6 dB |
| 同上、時域 /2 慣例 | $8.33\times10^{-3}$ | $194.62$ dB | $+7.63$ dB | 同一物理、記帳保守 3.01 dB |

- **判定規則**：$\mathrm{FOM}_{max}-\mathrm{FOM}_{req}$ 是「**理想餘裕**」。
  [fom_limit](/06_design_insights/fom_limit) 說好的發表 LC 離自己的 $Q$ 天花板約 $5\sim10$ dB
  （$\eta_P\lt1$、$F\gt1+\gamma$、varactor 損耗），所以**理想餘裕至少要 5 dB 以上才敢往下做**；
  10.6 dB 是舒服的。ring 差了 18.7 dB——沒有任何 $N$、swing 或功率調整救得回來
  （[P2] N-independence；FOM 對 $P$ 已歸一化）。
- **結論：選 LC，且製程要給得出 $Q\approx10$ 的 tank**。若製程只有 $Q=5$，天花板降 $6$ dB 到 $191.6$ dB，
  餘裕只剩 4.6 dB——就會進入本頁末的迭代。

```python
import numpy as np
kB, T = 1.380649e-23, 300.0
Cref = -10*np.log10(kB*T*1.0/1e-3)                        # 173.83 dB（fom_limit 第 1 步）
FOM_req = 186.99
gamma = 2/3
FOM_ring = Cref - 10*np.log10(16*gamma/3)                 # [P2] Eq.(25) 下限
print(round(FOM_ring, 2), round(FOM_ring - FOM_req, 2))   # -> 168.32 -18.67 （ring 天花板、差距：不可行）
FOM_lc10 = Cref - 10*np.log10((1+gamma)*0.5/(2*10**2))    # [P1] Eq.(21) /4 慣例，Q=10
print(round(FOM_lc10, 2), round(FOM_lc10 - FOM_req, 2))   # -> 197.63 10.64 （LC Q=10 天花板、理想餘裕）
print(round(FOM_lc10 - 10*np.log10(2) - FOM_req, 2))      # -> 7.63 （時域 /2 慣例下的餘裕）
FOM_lc5 = Cref - 10*np.log10((1+gamma)*0.5/(2*5**2))
print(round(FOM_lc5, 2), round(FOM_lc5 - FOM_req, 2))     # -> 191.61 4.62 （Q=5 天花板、理想餘裕）
print(round(-10*np.log10(310/300), 2))                    # -> -0.14 （C_ref 每 +10 K 的變化，dB）
```

## Step 3：tank——選 $C$，推 $L$ 與 $R_p$

LC 的三個 tank 量只有兩個自由度（$f_0$ 綁住 $LC$），加上製程給的 $Q$ 就全定了。
**先選 $C$**（不是 $L$）——因為 $C$ 直接進 $q_{max}=CV_{max}$，也決定 varactor 與寄生的比例：

1. **$C$ 的下界**：device、varactor、走線寄生在 5 GHz 通常已有幾百 fF；$C$ 太小會被寄生吃掉調諧範圍。
2. **$C$ 的上界**：$C$ 越大 → $L$ 越小、$R_p=Q\omega_0L$ 越小 → 同 swing 要更多電流（Step 4）。

取 $C=1$ pF（站台 canonical，也是 [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 例子的量級）：

$$
\begin{aligned}
\omega_0&=2\pi f_0=2\pi\times5\times10^{9}=3.1416\times10^{10}\ \text{rad/s},\\[4pt]
L&=\frac{1}{\omega_0^2C}=\frac{1}{(3.1416\times10^{10})^2\times10^{-12}}
   =\frac{1}{9.870\times10^{20}\times10^{-12}}=1.013\times10^{-9}\ \text{H}=1.013\ \text{nH},\\[4pt]
R_p&=Q\,\omega_0L=10\times3.1416\times10^{10}\times1.013\times10^{-9}=318.3\ \Omega .
\end{aligned}
$$

- **用到的公式**：$\omega_0=1/\sqrt{LC}$ 與 $Q=R_p/(\omega_0L)=\omega_0R_pC=R_p\sqrt{C/L}$
  （[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 第 1 步的三種等價寫法；
  標準教科書內容，外部、非本站 5 篇 PDF）。三式互相驗證：$Q=\omega_0R_pC=3.1416\times10^{10}\times318.3\times10^{-12}=10.0$ ✓；
  $R_0=\sqrt{L/C}=\sqrt{1.013\times10^{-9}/10^{-12}}=31.83\ \Omega$，$R_p/R_0=10.0$ ✓。
- **Dimension check**：$[1/(\omega_0^2C)]=1/[(\text{s}^{-2})(\text{F})]=\text{s}^2/\text{F}=\text{H}$ ✓
  （$\text{H}\cdot\text{F}=\text{s}^2$）；$[Q\omega_0L]=(\text{s}^{-1})(\text{H})=\Omega$ ✓。
- **物理讀法**：$R_p=318\ \Omega$ 就是 tank 每週期把能量漏給誰——它同時決定 Step 4 的偏壓電流
  （要把這個電阻「推」到 1 V）與 Step 5 的雜訊電流 $4kT/R_p$。$Q=10$ 意味 3-dB 頻寬 $f_0/Q=500$ MHz，
  諧振並不尖。
- **調諧範圍在這一步的代價**：$f_0\propto1/\sqrt{C}$，$4.75\sim5.25$ GHz 要求
  $C_{max}/C_{min}=(f_{max}/f_{min})^2=(5.25/4.75)^2=1.222$——tank 總電容要能變化 22%，
  這部分 varactor（或 switched-cap 陣列）的有限 $Q$ 會拖累有效 $Q$
  （[varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)；
  [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 第 5 步）。本頁假設 $Q=10$ 已是**含 varactor 的 loaded $Q$**。

```python
import numpy as np
f0, Q, C = 5e9, 10.0, 1e-12
w0 = 2*np.pi*f0
L = 1/(w0**2*C)
Rp = Q*w0*L
print(round(L*1e9, 3))                       # -> 1.013 （nH）
print(round(Rp, 1))                          # -> 318.3 （Ω）
print(round(w0*Rp*C, 2), round(Rp/np.sqrt(L/C), 2))   # -> 10.0 10.0 （Q 三種寫法互驗）
print(round((5.25/4.75)**2, 3))              # -> 1.222 （10% TR 要求的 C_max/C_min）
print(round(np.sqrt(L/C), 2), round(f0/Q/1e6, 0))   # -> 31.83 500.0 （R_0 Ω、3-dB 頻寬 MHz）
```

## Step 4：swing → $q_{max}$、偏壓電流、功率

現在把 [P1] Eq.(21) 的分母 $q_{max}=CV_{max}$ 釘死。swing 的上限由 **headroom** 決定：
[tank_swing](/06_design_insights/tank_swing) 第 4 步——差動 LC 的單端 swing 在 current-limited 區約為
$\tfrac{4}{\pi}I_{bias}R_p$，上限約在 supply $V_{DD}$（voltage-limited）。**配方的選擇是把偏壓推到剛好碰到
voltage-limited 邊界**：再多的電流只是浪費（swing 不再長、$\mathcal{L}$ 不再降）。

取 $V_{DD}=1$ V、$V_{max}=1$ V（單端峰值）：

$$
\begin{aligned}
q_{max}&=C\,V_{max}=10^{-12}\ \text{F}\times1\ \text{V}=10^{-12}\ \text{C}=1\ \text{pC},\\[4pt]
I_{bias}&=\frac{\pi}{4}\cdot\frac{V_{max}}{R_p}=\frac{\pi}{4}\cdot\frac{1\ \text{V}}{318.3\ \Omega}=0.7854\times3.142\times10^{-3}\ \text{A}=2.467\ \text{mA},\\[4pt]
P_{DC}&=V_{DD}\,I_{bias}=1\ \text{V}\times2.467\ \text{mA}=2.467\ \text{mW}\ \le\ 5\ \text{mW},\\[4pt]
P_{tank}&=\frac{V_{max}^2}{2R_p}=\frac{1}{2\times318.3}=1.571\ \text{mW},\qquad
\eta_P=\frac{P_{tank}}{P_{DC}}=\frac{1/(2R_p)}{(\pi/4)/R_p}=\frac{2}{\pi}=0.637 .
\end{aligned}
$$

- **站台 canonical 自然落出**：$C=1$ pF、$V_{max}=1$ V 給 $q_{max}=1$ pC——本站例 A/B 一直在用的數字，
  原來就是「1 pF tank、1 V swing」。
- **Dimension check**：$[\text{F}][\text{V}]=[\text{C}]$ ✓；$[\text{V}]/[\Omega]=[\text{A}]$ ✓；$[\text{V}][\text{A}]=[\text{W}]$ ✓；
  $\eta_P$ 無因次 ✓。
- **$\eta_P=2/\pi$ 的物理**：在 voltage-limited 邊界上，tank 吃到的是 $V_{max}^2/(2R_p)$，
  supply 付的是 $V_{DD}\times I_{bias}$；兩者的比在 $V_{DD}=V_{max}$ 時剛好是 $\tfrac{1}{2}\big/\tfrac{\pi}{4}=2/\pi$。
  這個 $\eta_P\lt1$ 之後會在 Step 6 的 FOM 記帳裡吃掉 $-10\log_{10}(2/\pi)=1.96$ dB。
- ⚠️ **慣例警告（係數 $4/\pi$）**：這條 swing–電流關係是**標準 LC 設計知識（外部教科書，非本站 5 篇 PDF；
  Razavi《RF Microelectronics》、Hajimiri–Lee 教科書）**，本頁沿用 [tank_swing](/06_design_insights/tank_swing) 的寫法。
  不同教科書對「單端 vs 差動 swing」與「$R_p$ 是單端還是差動等效」的定義不同，係數可差 $2\times$；
  因此 $I_{bias}$ 與 $P_{DC}$ 要當成**量級估計**（$2.5\sim5$ mW）——注意即使差 $2\times$ 仍在 5 mW 預算內，
  這正是 Step 2 要求餘裕的原因之一。精確值要用 transistor-level 模擬（本站不做 SPICE，見
  [python_environment](/99_appendix/python_environment)）。

```python
import numpy as np
C, Vmax, VDD, Rp = 1e-12, 1.0, 1.0, 318.3
qmax = C*Vmax
Ibias = (np.pi/4)*Vmax/Rp
P_dc = VDD*Ibias
P_tank = Vmax**2/(2*Rp)
print(qmax*1e12)                                  # -> 1.0 （pC：站台 canonical）
print(round(Ibias*1e3, 3), round(P_dc*1e3, 3))    # -> 2.467 2.467 （mA、mW；P≤5 mW ✓）
print(round(P_tank*1e3, 3), round(P_tank/P_dc, 3))  # -> 1.571 0.637 （P_tank mW、η_P=2/π）
```

## Step 5：雜訊源——$S_i=F\cdot4kT/R_p$

[P1] Eq.(21) 的分子需要「折算到 tank 節點的總白噪電流 PSD」。tank 損耗本身給 $4kT/R_p$
（[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 第 3 步）；
active core 的 device 雜訊經各自的 $\Gamma_{eff}$ 加權後，用**噪聲因子** $F$ 收成 $F\cdot4kT/R_p$
（[fom_limit](/06_design_insights/fom_limit) 第 3 步）。理想 class-B cross-coupled（tail 雜訊被濾掉）
的下限是 $F=1+\gamma$——Hegazi–Sjöland–Abidi 2001 的標準結果（外部文獻，非本站 5 篇 PDF，見頁尾）。
本配方取**短通道** $\gamma=1$（比 Step 2 天花板用的長通道 $2/3$ 保守），故 $F=2$：

$$
\begin{aligned}
\frac{4kT}{R_p}&=\frac{4\times1.380649\times10^{-23}\ \text{J/K}\times300\ \text{K}}{318.3\ \Omega}
   =\frac{1.6568\times10^{-20}\ \text{J}}{318.3\ \Omega}=5.205\times10^{-23}\ \text{A}^2/\text{Hz},\\[4pt]
S_i&=F\cdot\frac{4kT}{R_p}=2\times5.205\times10^{-23}=1.041\times10^{-22}\ \text{A}^2/\text{Hz}.
\end{aligned}
$$

- **Dimension check**：$\text{J}/\Omega=(\text{V}\cdot\text{A}\cdot\text{s})/(\text{V}/\text{A})=\text{A}^2\text{s}=\text{A}^2/\text{Hz}$ ✓（單邊 PSD，與規範 notation 一致）。
- **跟 canonical 例 B 的 $S_i=10^{-24}$ 比**：這裡大了 100 倍（$+20$ dB）。例 B 的 $10^{-24}$ 對應
  $R_p=16.6$ kΩ、$Q\approx521$（[fom_limit](/06_design_insights/fom_limit) 第 3 步的「FOM 會抓包」）；
  **真實 $Q=10$ tank 的雜訊電流就是 $10^{-22}$ 量級**——這是本頁跟教學例最大的差別。
- **$F$ 的失效面**：tail 沒濾（$c_0$、$c_2$ 的 2× upconversion，[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)）、
  bias 電流源 flicker、varactor 上的 AM-PM，都讓 $F$ 高於 $1+\gamma$；設計後期要用 [device_noise_mapping](/06_design_insights/device_noise_mapping)
  的方法逐源核算。

```python
kB, T, Rp, gamma = 1.380649e-23, 300.0, 318.3, 1.0
Si_tank = 4*kB*T/Rp
Si = (1+gamma)*Si_tank
print(f"{Si_tank:.3e}")                           # -> 5.205e-23 （tank 自己的 4kT/Rp，A²/Hz）
print(f"{Si:.3e}")                                # -> 1.041e-22 （F=1+γ=2 折算後的總 S_i）
Rp_B = 4*kB*T/1e-24
print(round(Rp_B/1e3, 1), round(Rp_B/31.83))      # -> 16.6 521 （例 B 的 S_i=1e-24 對應的 R_p kΩ 與 Q）
```

## Step 6：驗收——[P1] Eq.(21) 算 $\mathcal{L}(1\ \text{MHz})$

四個因子都釘死了：$\Gamma_{rms}=1/\sqrt2$（true LC，$\Gamma=-\sin\theta$；[lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model)）、
$q_{max}=1$ pC、$S_i=1.041\times10^{-22}$ A²/Hz、$\Delta\omega=2\pi\times10^6$ rad/s。代入 [P1] Eq.(21), p.185（已對照 PDF 渲染頁）：

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)
$$

$$
\begin{aligned}
\Delta\omega^2&=(6.2832\times10^{6})^2=3.948\times10^{13}\ (\text{rad/s})^2,\\[4pt]
\frac{\Gamma_{rms}^2}{q_{max}^2}&=\frac{0.5}{(10^{-12})^2}=5\times10^{23}\ \text{C}^{-2},\\[4pt]
\frac{S_i}{4\Delta\omega^2}&=\frac{1.041\times10^{-22}}{4\times3.948\times10^{13}}=6.592\times10^{-37},\\[4pt]
\text{括號}&=5\times10^{23}\times6.592\times10^{-37}=3.296\times10^{-13},\\[4pt]
\mathcal{L}(1\ \text{MHz})&=10\log_{10}(3.296\times10^{-13})=-124.8\ \text{dBc/Hz}.
\end{aligned}
$$

- **驗收**：$-124.8\le-120$ ✓，**餘裕 4.8 dB**；功率 $2.47\le5$ mW ✓。
- **同一件事用 FOM 記帳**：實際只燒 $P_{DC}=2.467$ mW，所需 FOM 從 Step 1 的 187.0 升為
  $120+73.98-10\log_{10}(2.467)=190.06$ dB（升了 $10\log_{10}(5/2.467)=3.07$ dB，就是 Step 1 預告的那 3 dB）；
  $194.88-190.06=4.82$ dB，與直接比 $\mathcal{L}$ 的餘裕**一模一樣**——兩種記帳互相印證。
- **Dimension check**（同 [tank_swing](/06_design_insights/tank_swing)）：$\dfrac{1}{[\text{C}]^2}\cdot\dfrac{[\text{A}^2/\text{Hz}]}{[\text{s}^{-2}]}$，
  用 $\text{A}=\text{C/s}$ → $\dfrac{\text{C}^2\text{s}^{-2}/\text{Hz}}{\text{C}^2\text{s}^{-2}}=1/\text{Hz}$，配 1 Hz 頻寬歸一 → 無因次 → dBc/Hz ✓。
- **實際 FOM 與距天花板**：
  $\mathrm{FOM}=124.82+73.98-10\log_{10}(2.467)=124.82+73.98-3.92=194.88$ dB。
  距 $Q=10$ 天花板 $197.63-194.88=2.75$ dB，來源可以**逐項對帳**：
  $F=2$ 而非 $5/3$ → $10\log_{10}(2/(5/3))=0.79$ dB；$\eta_P=2/\pi$ 而非 1 → $-10\log_{10}(2/\pi)=1.96$ dB；
  合計 $2.75$ dB ✓（$\Gamma_{rms}^2=\tfrac12$ 兩邊相同）。
  同一件事用 [fom_limit](/06_design_insights/fom_limit) 的萬用形驗證：$F_{eff}=F\Gamma_{rms}^2/(2Q^2\eta_P)=7.85\times10^{-3}$，
  $\mathcal{L}=10\log_{10}[F_{eff}(kT/P_{DC})(f_0/\Delta f)^2]=-124.8$ dBc/Hz——與 Eq.(21) 直接代入**逐位一致**。
- ⚠️ **factor-of-2 慣例**：上式是 [P1] 的 SSB「/4」記帳；時域乾淨推導的「/2」給 $-121.8$ dBc/Hz、餘裕只剩 1.8 dB
  （[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)）。**驗收時請用保守的那個**，
  或至少確認量測儀器的 $\mathcal{L}$ 定義與你的公式同一族。

```python
import numpy as np
kB, T, f0, df = 1.380649e-23, 300.0, 5e9, 1e6
grms2, qmax, Si, Q, P_dc = 0.5, 1e-12, 1.041e-22, 10.0, 2.467e-3
dw = 2*np.pi*df
L_db = 10*np.log10(grms2/qmax**2 * Si/(4*dw**2))       # [P1] Eq.(21), p.185（SSB /4）
print(round(L_db, 2), round(-120.0 - L_db, 2))         # -> -124.82 4.82 （dBc/Hz、對規格餘裕 dB）
print(round(10*np.log10(grms2/qmax**2 * Si/(2*dw**2)), 2))   # -> -121.81 （時域 /2 慣例）
FOM = -L_db + 20*np.log10(f0/df) - 10*np.log10(P_dc/1e-3)
print(round(FOM, 2))                                   # -> 194.88 （實際 FOM，dB）
FOM_req_actual = 120.0 + 20*np.log10(f0/df) - 10*np.log10(P_dc/1e-3)
print(round(FOM_req_actual, 2), round(FOM - FOM_req_actual, 2))   # -> 190.06 4.82 （2.467 mW 下的所需 FOM、餘裕：與上面一致）
print(round(10*np.log10(5.0/2.467), 2))                # -> 3.07 （少燒功率使所需 FOM 上升的 dB）
Cref = -10*np.log10(kB*T/1e-3)
FOM_lc10 = Cref - 10*np.log10((5/3)*0.5/(2*Q**2))
print(round(FOM_lc10 - FOM, 2))                        # -> 2.75 （距 Q=10 天花板）
print(round(10*np.log10(2/(5/3)), 2), round(-10*np.log10(2/np.pi), 2))   # -> 0.79 1.96 （F 項、η_P 項；和 = 2.75）
Feff = 2.0*grms2/(2*Q**2*(2/np.pi))
print(round(10*np.log10(Feff*(kB*T/P_dc)*(f0/df)**2), 2))   # -> -124.82 （萬用形交叉驗證）
```

## Step 7：交棒——$\mathcal{L}(\Delta f)$ → rms jitter

系統端要的不是 dBc/Hz，是 jitter。用 $1/f^2$ 的閉式（[lab_08](/04_simulation_labs/lab_08_jitter_integration)、
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) 第 2 步），積分 $f_1=1$ MHz 到 $f_2=100$ MHz：

$$
\begin{aligned}
S_\phi(1\ \text{MHz})&=2\times10^{\mathcal{L}/10}=2\times10^{-12.482}=6.59\times10^{-13}\ \text{rad}^2/\text{Hz},\\[4pt]
\sigma_\phi^2&=S_\phi(f_{ref})\,f_{ref}^2\left(\frac{1}{f_1}-\frac{1}{f_2}\right)
  =6.59\times10^{-13}\times(10^{6})^2\times(10^{-6}-10^{-8})=6.53\times10^{-7}\ \text{rad}^2,\\[4pt]
\sigma_\phi&=8.08\times10^{-4}\ \text{rad}=0.808\ \text{mrad},\\[4pt]
\sigma_t&=\frac{\sigma_\phi}{2\pi f_0}=\frac{8.08\times10^{-4}}{3.1416\times10^{10}}=2.57\times10^{-14}\ \text{s}=25.7\ \text{fs}.
\end{aligned}
$$

- **Dimension check**：$[\text{rad}^2/\text{Hz}][\text{Hz}^2][1/\text{Hz}]=\text{rad}^2$ ✓；$\text{rad}\div(\text{rad/s})=\text{s}$ ✓。
- **對照例 C**：例 C 是 $-100$ dBc/Hz → $447.9$ fs；本設計好 24.8 dB，$\sigma_t$ 縮 $10^{-24.82/20}=0.0574$ 倍 → $25.7$ fs ✓
  （同積分頻寬、同 $1/f^2$ 斜率下 $\sigma_t\propto10^{\Delta\mathcal{L}/20}$，[lab_09](/04_simulation_labs/lab_09_design_tradeoffs)）。
  規格點 $-120$ dBc/Hz 本身對應 $44.8$ fs——jitter 餘裕跟 dB 餘裕是同一件事的兩種寫法。
- **交棒條件**：這個 25.7 fs 是**free-running VCO、只含 $1/f^2$、積分 1–100 MHz** 的數字。放進 PLL 之後，
  VCO 貢獻被 $\lvert H_{hp}\rvert^2$ 高通、reference/CP 在帶內接手，積分下限與上限由 loop BW 與資料率決定
  （[pll_noise_budget](/06_design_insights/pll_noise_budget) 的最佳 BW；[clock_chain_budget](/06_design_insights/clock_chain_budget)
  的整條時脈鏈 27.6 fs 例）；flicker（$1/f^3$）與 floor 也要補進去。**本頁的產出是那條鏈的 $S_{vco}$ 輸入**。

```python
import numpy as np
f0, L_db, f1, f2 = 5e9, -124.82, 1e6, 1e8
Sphi_ref = 2*10**(L_db/10)                     # 單邊 S_phi(1 MHz)，rad²/Hz
sphi2 = Sphi_ref*(1e6)**2*(1/f1 - 1/f2)         # 1/f² 閉式
sigma_t = np.sqrt(sphi2)/(2*np.pi*f0)
print(round(np.sqrt(sphi2)*1e3, 3))             # -> 0.808 （mrad）
print(round(sigma_t*1e15, 1))                   # -> 25.7 （fs，1–100 MHz、1/f²）
print(round(10**((L_db + 100.0)/20), 4))        # -> 0.0574 （相對例 C 的 σ_t 縮放倍率）
print(round(447.9*10**((L_db + 100.0)/20), 1))  # -> 25.7 （由例 C 的 447.9 fs 按 dB 縮放，交叉驗證）
print(round(447.9*10**((-120.0 + 100.0)/20), 1))  # -> 44.8 （規格點 −120 dBc/Hz 對應的 fs）
```

## 迭代規則：餘裕不夠時轉哪個旋鈕、買幾 dB、花多少功率

Step 6 若得到**負餘裕**（或 Step 2 的理想餘裕不足 5 dB），不要憑感覺加電流。把 Eq.(21) 與 Step 3–5 的關係鏈
（$L=1/(\omega_0^2C)$、$R_p=Q\omega_0L$、$q_{max}=CV_{max}$、$I_{bias}=\tfrac{\pi}{4}V_{max}/R_p$、$S_i=F\cdot4kT/R_p$）
合起來，$\mathcal{L}_{lin}\propto\dfrac{F\,\Gamma_{rms}^2}{C\,V_{max}^2\,Q\,\omega_0}$、$P_{DC}\propto\dfrac{V_{DD}V_{max}C\omega_0}{Q}$，
每個旋鈕對 $\mathcal{L}$、$P$、FOM 的效果就能一次列清楚（**其他量固定、留在 voltage-limited 邊界上**）：

| 旋鈕（×2） | $\Delta\mathcal{L}$ | $\Delta P_{DC}$ | $\Delta\mathrm{FOM}$ | 讀法 |
|---|---|---|---|---|
| tank $Q$（$R_p$ 加倍，$C$、$V_{max}$ 不變） | $-3.0$ dB | $\times\tfrac12$ | $+6.0$ dB | **唯一同時降雜訊又省電的旋鈕**——$S_i\propto1/R_p$、$I_{bias}\propto1/R_p$；受製程 inductor/varactor $Q$ 鎖死 |
| tank $C$（$L$ 減半、$R_p$ 減半） | $-3.0$ dB | $\times2$ | $0$ | $q_{max}$ 加倍賺 $-6$ dB，但 $S_i$ 加倍還 $+3$ dB；用功率買 dB，FOM 不動 |
| swing $V_{max}$（需 $V_{DD}$ 一起加倍） | $-6.0$ dB | $\times4$ | $0$ | $q_{max}$ 加倍；$I_{bias}$ 與 $V_{DD}$ 都加倍 → 功率四倍；受 breakdown 限制 |
| 只加 $I_{bias}$（已在 voltage-limited） | $0$ | $\times2$ | $-3.0$ dB | **純浪費**：swing 不再長（[tank_swing](/06_design_insights/tank_swing) 第 4 步） |
| 噪聲因子 $F$：$2\to5/3$（tail filter） | $-0.8$ dB | $\times1$ | $+0.8$ dB | Hegazi 一族技巧；不花功率 |
| $\Gamma_{rms}$（波形／class-F 整形） | $1\sim2$ dB | $\times1$ | $1\sim2$ dB | [fom_limit](/06_design_insights/fom_limit) knobs 表；[lab_09](/04_simulation_labs/lab_09_design_tradeoffs) |

- **迭代順序**：(1) 先問製程還有沒有 $Q$（每加倍 $-3$ dB 且省一半電）；(2) 再把 swing 推到 headroom 上限（$-6$ dB／加倍，但功率四倍且撞 $V_{DD}$）；
  (3) 最後才用 $C$（或等價地用電流）在 FOM 不變下**拿功率預算換 dB**——這一步的極限是 $P_{max}$。
- **FOM 不變的「功率換 dB」極限**：在 $Q=10$、$\mathrm{FOM}=194.9$ dB 下，把 5 mW 預算用滿能買到的最低 $\mathcal{L}$ 是
  $-\mathrm{FOM}+73.98-10\log_{10}(5)=-194.88+73.98+6.99=-127.9$ dBc/Hz。**任何比 $-127.9$ 更嚴的規格，在 $Q=10$、5 mW 下都要靠 $Q$、$F$、$\Gamma_{rms}$（或放寬功率）。**
- **一次具體迭代**：若規格改成 $-127$ dBc/Hz（現行設計餘裕 $-2.2$ dB）：把 $C$ 提到 2 pF（$L=0.507$ nH、$R_p=159$ Ω、$q_{max}=2$ pC、$S_i=2.08\times10^{-22}$）
  → $\mathcal{L}=-127.8$ dBc/Hz（餘裕 0.8 dB）、$I_{bias}=4.93$ mA、$P_{DC}=4.93$ mW（仍 $\le5$ mW，但已用滿）。
  這正是表中「$C\times2$：$-3$ dB、功率 $\times2$、FOM 不動」的實例。

```python
import numpy as np
kB, T, f0, df, Q, Vmax, VDD, F, grms2 = 1.380649e-23, 300.0, 5e9, 1e6, 10.0, 1.0, 1.0, 2.0, 0.5
w0, dw = 2*np.pi*f0, 2*np.pi*df
def design(C, Q=Q, Vmax=Vmax, VDD=VDD, F=F):
    L = 1/(w0**2*C); Rp = Q*w0*L
    qmax = C*Vmax; Ib = (np.pi/4)*Vmax/Rp; P = VDD*Ib
    Si = F*4*kB*T/Rp
    Ldb = 10*np.log10(grms2/qmax**2 * Si/(4*dw**2))
    return Ldb, P, -Ldb + 20*np.log10(f0/df) - 10*np.log10(P/1e-3), Rp, Ib
L0, P0, F0, _, _ = design(1e-12)
Lq, Pq, Fq, _, _ = design(1e-12, Q=20.0)
print(round(Lq-L0, 2), round(Pq/P0, 2), round(Fq-F0, 2))   # -> -3.01 0.5 6.02 （Q×2：ΔL、P 比、ΔFOM）
Lc, Pc, Fc, Rp2, Ib2 = design(2e-12)
print(round(Lc-L0, 2), round(Pc/P0, 2), round(Fc-F0, 2))   # -> -3.01 2.0 0.0 （C×2）
Lv, Pv, Fv, _, _ = design(1e-12, Vmax=2.0, VDD=2.0)
print(round(Lv-L0, 2), round(Pv/P0, 2), round(Fv-F0, 2))   # -> -6.02 4.0 0.0 （V_max×2 且 V_DD×2）
print(round(-F0 + 20*np.log10(f0/df) - 10*np.log10(5.0), 2))   # -> -127.89 （Q=10、5 mW 用滿的最低 L）
print(round(-127.0 - L0, 2))                                  # -> -2.18 （規格改 −127 時現行設計的餘裕）
print(round(Lc, 2), round(Pc*1e3, 2), round(Rp2, 1), round(Ib2*1e3, 2))   # -> -127.83 4.93 159.2 4.93 （C=2 pF 迭代：L、P mW、Rp Ω、I_bias mA）
```

## FOM$_T$：把調諧範圍也記進去

Step 0 的 TR 到目前只在 Step 3 以「varactor 拖累 $Q$」的形式出現。文獻比較寬調諧 VCO 時常用
**tuning-range-normalized FOM**（外部慣例，非本站 5 篇 PDF；首次出處待查證，近代 JSSC VCO 論文普遍採用此形式）：

$$
\mathrm{FOM}_T=\mathrm{FOM}+20\log_{10}\!\left(\frac{\mathrm{TR}\,[\%]}{10}\right)
$$

- **讀法**：以 10% 調諧範圍為基準，TR 每加倍加 $6$ dB——理由是同樣 $Q$ 下，調得越寬 varactor 佔比越大、
  能維持的有效 $Q$ 越低，所以「同 FOM、更寬 TR」值得加分。這是**經驗慣例**，不是像 FOM 那樣由 Eq.(21) 推得的恆等式，
  比較時務必確認對方用的是同一條定義。
- **本設計**：TR $=10\%$ → $\mathrm{FOM}_T=194.88+20\log_{10}(1)=194.88$ dB（基準點，加分為 0）。若同一顆做到 TR $=20\%$ 而 $Q$ 不掉，$\mathrm{FOM}_T=200.9$ dB。

```python
import numpy as np
FOM = 194.88
print(round(FOM + 20*np.log10(10/10), 2), round(FOM + 20*np.log10(20/10), 2))   # -> 194.88 200.9 （TR=10%、20%）
```

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 規格點在 $1/f^2$ 白噪區 | 一點定整段、FOM 有意義 | 規格點在 $1/f^3$ 區：先用 [symmetry](/06_design_insights/symmetry) 壓 corner；floor 區另算 |
| 小擾動 LTV（[P1] 框架）、$\Gamma=-\sin\theta$ | $\Gamma_{rms}^2=\tfrac12$ 可直接用 | 大 swing 波形失真、class-F 等整形：$\Gamma_{rms}$ 要由 [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep) 方法重萃取 |
| $F=1+\gamma$（tail 濾除、bias 乾淨） | Step 5 的 $S_i$ 成立 | tail $c_0/c_2$ upconversion、bias flicker、varactor AM-PM → $F$ 上升（[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)） |
| current-limited 到 voltage-limited 邊界 | $V_{max}\approx\tfrac{4}{\pi}I_{bias}R_p\approx V_{DD}$ | 超過邊界加電流無效；係數 $4/\pi$ 依單端/差動定義可差 $2\times$（外部教科書） |
| $Q$ 為含 varactor 的 loaded $Q$ | $R_p$、$S_i$、$I_{bias}$ 一致 | 用 inductor unloaded $Q$ 會高估餘裕（[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 第 5 步） |
| $P$ 為總 DC 功耗、$T=300$ K | FOM 可跨設計比較 | 漏掉 buffer/bias 會虛胖；其他溫度 $C_{ref}$ 每 $+10$ K 降 $0.14$ dB |
| 慣例（/4 vs /2）前後一致 | 餘裕 4.8 dB 或 1.8 dB 各自成立 | 混用會生出幽靈 3 dB——驗收用保守的 /2 |
| jitter 積分 1–100 MHz、free-running | $25.7$ fs 成立 | 進 PLL 後積分限與轉移函數改變，交給 [pll_noise_budget](/06_design_insights/pll_noise_budget) |

## 重點回顧

- **7 步**：spec → $\mathrm{FOM}_{req}$ → 對天花板選拓樸 → $C\to L,R_p$ → $V_{max}\to q_{max},I_{bias},P$ → $S_i=F\cdot4kT/R_p$ → [P1] Eq.(21) 驗收 → $\sigma_t$ 交棒。
- 本例：$\mathrm{FOM}_{req}=187.0$ dB；ring 天花板 168.3 差 18.7 dB 不可行；LC $Q=10$ 天花板 197.6 餘裕 10.6 dB。
- $C=1$ pF → $L=1.013$ nH、$R_p=318$ Ω；$V_{max}=1$ V → $q_{max}=1$ pC（站台 canonical）、$I_{bias}=2.47$ mA、$P=2.47$ mW、$\eta_P=2/\pi$。
- $S_i=2\times4kT/R_p=1.04\times10^{-22}$ A²/Hz（比例 B 的 $10^{-24}$ 大 20 dB——真實 $Q=10$ tank 的量級）。
- $\mathcal{L}(1\ \text{MHz})=-124.8$ dBc/Hz（/4；/2 給 $-121.8$），餘裕 4.8 dB；$\mathrm{FOM}=194.9$ dB，距天花板 2.75 dB $=0.79$（$F$）$+1.96$（$\eta_P$）。
- $\sigma_t(1\text{–}100\ \text{MHz})=25.7$ fs（規格點對應 44.8 fs）。
- 迭代：$Q\times2$ → $-3$ dB 且省一半電（FOM $+6$）；$C\times2$ 或 $V_{max}\times2$ 用功率買 dB（FOM 不動）；voltage-limited 後加電流是純浪費。$Q=10$、5 mW 的極限是 $-127.9$ dBc/Hz。
- $\mathrm{FOM}_T=\mathrm{FOM}+20\log_{10}(\mathrm{TR}\%/10)$ 是外部經驗慣例，非恆等式。

## 延伸閱讀

- 天花板家族與 $F_{eff}$ 的推導：[fom_limit](/06_design_insights/fom_limit)
- $Q$ 三種寫法、$R_p$ 與 $4kT/R_p$：[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)
- swing、$q_{max}$、current/voltage-limited：[tank_swing](/06_design_insights/tank_swing)
- [P1] Eq.(21) 推導與 /2 vs /4：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- 每個旋鈕幾 dB 的口算表：[lab_09_design_tradeoffs](/04_simulation_labs/lab_09_design_tradeoffs)
- $\mathcal{L}$ → jitter 積分：[lab_08_jitter_integration](/04_simulation_labs/lab_08_jitter_integration)、[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- 交棒對象：[pll_noise_budget](/06_design_insights/pll_noise_budget)、[clock_chain_budget](/06_design_insights/clock_chain_budget)
- 單旋鈕反推練習：[exercises](/06_design_insights/exercises) 習題 1；正向 end-to-end：[capstone_lc_end_to_end](/03_isf_core_theory/capstone_lc_end_to_end)

## 外部文獻（不在下載的 5 篇 PDF 內）

- **[E-Hegazi]** E. Hegazi, H. Sjöland, and A. A. Abidi, *"A Filtering Technique to Lower LC Oscillator Phase Noise,"*
  IEEE J. Solid-State Circuits, vol. 36, no. 12, pp. 1921–1930, Dec. 2001.（噪聲因子下限 $F\to1+\gamma$；本站 [fom_limit](/06_design_insights/fom_limit) 已引用並查證。）
- swing $\approx\tfrac{4}{\pi}I_{bias}R_p$、current/voltage-limited regime：標準 LC 振盪器教科書內容
  （B. Razavi, *RF Microelectronics*；T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*），沿用 [tank_swing](/06_design_insights/tank_swing) 的標註。
- $\mathrm{FOM}_T$ 的 $20\log_{10}(\mathrm{TR}\%/10)$ 形式：近代 VCO 論文的通用比較慣例，首次出處**待查證**。
