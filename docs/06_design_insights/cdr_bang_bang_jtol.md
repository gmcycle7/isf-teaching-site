---
title: "Bang-bang CDR：把 ISF 的 σ_t 變成 K_bb、JTOL 與 SSC 追蹤"
description: "真正的 SerDes 時脈資料回復（CDR）長什麼樣：Alexander bang-bang 相位偵測器的 sign(Δt) 輸出、高斯 jitter 下的線性化增益 K_bb=√(2/π)/σ_j（本站 σ_t=447.9 fs → 1.78e12 s⁻¹ = 71.3/UI）、相位內插器（PI）UI/2^b 量化與 hunting 極限環 (2D+1)K_p、JTOL(f)=(UI−TJ_eye)/|1−H(f)| 與 −40/−20 dB/dec mask 段、以及 PCIe-style 展頻（SSC：−0.5%、30 kHz 三角 FM → 521 UI 峰峰相位）為什麼非 type-II 不可。全部數值可跑。"
sidebar_position: 28
---

import NumericQuiz from "@site/src/components/NumericQuiz";
import BbCdrExplorer from "@site/src/components/BbCdrExplorer";

# Bang-bang CDR：把 ISF 的 σ_t 變成 K_bb、JTOL 與 SSC 追蹤

> **先備**：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)（§6 的 loop high-pass 直覺、UI/eye/BER）、[pll_noise_budget](/06_design_insights/pll_noise_budget)（$\lvert H_{lp}\rvert^2,\lvert H_{hp}\rvert^2$、jitter transfer vs jitter tolerance 的區分與 JTOL worked example——本頁直接沿用）、[dj_dual_dirac](/06_design_insights/dj_dual_dirac)（$Q^{-1}(10^{-12})=7.03$、TJ@BER）｜ **接下來**：[exercises](/06_design_insights/exercises)、[lab_13_pll_cdr_transfer](/04_simulation_labs/lab_13_pll_cdr_transfer)

[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) 把 CDR（clock and data
recovery，時脈資料回復）畫成一個「對 VCO noise 高通、對輸入 jitter 低通」的黑盒子。真實的 SerDes
接收端幾乎都不是這種線性 PLL：它是一個 **bang-bang（二元、只輸出「早／晚」）** 的數位迴路，
相位偵測器（phase detector, PD）只吐出 $\pm1$，時脈相位由**相位內插器（phase interpolator, PI）**
以 $\text{UI}/2^b$ 的離散步伐移動。這一頁回答三個設計者天天遇到、但前面各頁都沒回答的問題：

1. bang-bang PD 沒有「增益」這回事，那 loop bandwidth 由誰決定？——答案是**由 jitter 的 rms 值決定**，
   而 jitter 的 rms 值正是本站一路算到的 $\sigma_t$。ISF 在這裡不只決定雜訊，還決定迴路動態。
2. 規格書上的 **jitter tolerance mask（JTOL）** 那條「低頻 $-40$ dB/dec、中間 $-20$ dB/dec、高頻平台」
   的折線從哪裡來？
3. **SSC（spread-spectrum clocking，展頻時脈）** 是 CDR 必須追的一個**巨大的、確定性的**低頻相位擺動；
   多大、為什麼一階迴路追不上。

> **物理直覺（先講結論）**：bang-bang PD 是一個 comparator，$\text{sign}(\Delta t)$ 對 $\Delta t$ 的斜率在
> 0 點是無限大——但在**有雜訊**時，輸出的期望值 $E[\text{sign}(\Delta t+n)]$ 被雜訊「抹平」成一條
> 誤差函數，斜率變成有限的 $\sqrt{2/\pi}/\sigma_j$。雜訊越大、增益越小、迴路越慢：**這是一個
> 「頻寬隨 jitter 自動縮放」的迴路**。JTOL 則是「眼圖剩下多少裕度」除以「迴路追不上的比例
> $\lvert1-H\rvert$」；SSC 的三角 FM 積分後是幾百 UI 的拋物線相位，只有帶頻率積分器的 type-II
> 迴路才能把它追到剩零點幾 UI。

## 第 1 步：Alexander（bang-bang）相位偵測器輸出的是 sign(Δt)

**Alexander PD**（外部文獻，非本站 5 篇 PDF：J. D. H. Alexander, *Electron. Lett.*, vol. 11, no. 22,
pp. 541–542, Oct. 1975）用三個取樣點判斷時脈相對資料邊緣是早還是晚：資料位元中心的兩個取樣
$D_{k-1}, D_k$ 與兩者之間、**名義上**對準資料轉態的邊緣取樣 $E_k$。整個判斷只靠一句話：
**邊緣取樣器若在資料轉態「之前」動作，看到的還是舊位元；在轉態「之後」動作，看到的已經是新位元。**

- 時脈**早**：$E_k$ 落在轉態之前，還看到舊位元 → $E_k=D_{k-1}\ne D_k$。
- 時脈**晚**：$E_k$ 落在轉態之後，已看到新位元 → $E_k=D_k\ne D_{k-1}$。
- $D_{k-1}=D_k$（沒有轉態）→ 沒有資訊，不輸出。

| $D_{k-1}$ | $E_k$ | $D_k$ | 判斷 | $e_k$ |
|---|---|---|---|---|
| 0 | 0 | 1 | 早（邊緣取樣還是舊位元） | $+1$ |
| 1 | 1 | 0 | 早 | $+1$ |
| 0 | 1 | 1 | 晚（邊緣取樣已是新位元） | $-1$ |
| 1 | 0 | 0 | 晚 | $-1$ |
| 0 | 任意 | 0 | 無轉態 | $0$ |
| 1 | 任意 | 1 | 無轉態 | $0$ |

（邏輯上就是兩個 XOR 相減：$e_k=(E_k\oplus D_k)-(D_{k-1}\oplus E_k)$。三個取樣點的時序圖見下方
[數值驗證](#numerical-check) 的圖 (a)。）

定義時間誤差 $\Delta t\equiv t_{\text{data}}-t_{\text{clk}}$：資料轉態時刻減去邊緣取樣時脈的時刻，
**時脈早為正**。上面的真值表就是

$$
e_k=\begin{cases}\text{sign}(\Delta t_k), & \text{有資料轉態（transition）}\\ 0, & \text{無轉態}\end{cases}
$$

三個要點：

- **輸出只有 $\pm1$（與 0）**：沒有「誤差有多大」的資訊，只有方向。所以它沒有傳統意義的 PD 增益
  $K_{PD}$（V/rad 或 1/s）——這正是第 2 步要解決的事。
- **只在轉態時更新**：隨機 NRZ 資料的轉態密度（transition density）$\rho_T\approx0.5$；長串 0 或 1
  時迴路「失明」，這是規格要求 8b/10b、64b/66b 或 scrambling 限制 run length 的原因之一。
- **它同時是資料取樣器**：$D_k$ 就是恢復出的資料。所以 CDR 鎖定的目標「時脈對準資料邊緣」
  自動等於「資料取樣點在眼圖中央」——和第 4 步 JTOL 的裕度 $\text{UI}-\text{TJ}_{eye}$ 直接對接。

```mermaid
flowchart LR
  D["資料邊緣 φ_data"] --> PD["Alexander BBPD: e = sign(Δt), Δt = φ_data − φ_clk"]
  PD --> P["比例路徑 K_p"]
  PD --> I["積分（頻率）路徑 K_i Σ"]
  P --> ACC["相位累加 φ[k+1] = φ[k] + …"]
  I --> ACC
  ACC --> PI["相位內插器 PI：UI/2^b 一步"]
  PI --> CLK["取樣時脈 φ_clk"]
  CLK --> PD
```

**迴路極性**：圖中 $\phi_{data},\phi_{clk}$ 記的是資料轉態與取樣時脈邊緣的**時間位置**（延遲，單位 s 或 UI）。
時脈早（$\Delta t=\phi_{data}-\phi_{clk}\gt0$）→ $e=+1$ → 相位碼把 $\phi_{clk}$ **加大**（時脈往後移）→
$\Delta t$ 變小：這是負回授。若把早／晚接反，同一個迴路會變成正回授，鎖到眼圖邊緣而不是中央。

## 第 2 步：線性化——高斯 jitter 把 sign 抹成 erf，增益 K_bb = √(2/π)/σ_j

**設定**：真實的 $\Delta t$ 不是常數，而是「名義誤差 $\Delta t$ ＋ 一個零均值高斯隨機項 $n$」，
$n\sim\mathcal N(0,\sigma_j^2)$。這個 $\sigma_j$ 是**資料邊緣與取樣時脈之間**的總 rms jitter：
輸入資料的 RJ、恢復時脈自己的 jitter（VCO 經迴路整形後的 $\sigma_t$、第 3 步的 hunting）都算在內。
PD 的**期望輸出**是：

$$
\begin{aligned}
\langle e\rangle(\Delta t)&=E\big[\text{sign}(\Delta t+n)\big]=P(n>-\Delta t)-P(n<-\Delta t)
=2\Phi\!\left(\frac{\Delta t}{\sigma_j}\right)-1 \\[4pt]
&=\operatorname{erf}\!\left(\frac{\Delta t}{\sqrt2\,\sigma_j}\right),
\qquad \Phi(x)=\tfrac12\Big[1+\operatorname{erf}\big(x/\sqrt2\big)\Big].
\end{aligned}
$$

**逐步**：(i) sign 的期望值 $=(+1)\cdot P(\text{正})+(-1)\cdot P(\text{負})$；(ii) $n>-\Delta t$ 的機率是
高斯 CDF $\Phi(\Delta t/\sigma_j)$；(iii) 用 $\Phi$ 與 erf 的標準關係整理。**線性化增益**是這條曲線在
$\Delta t=0$ 的斜率：

$$
\boxed{\ K_{bb}\equiv\frac{\partial\langle e\rangle}{\partial\Delta t}\bigg|_{\Delta t=0}
=\frac{2}{\sqrt\pi}\cdot\frac{1}{\sqrt2\,\sigma_j}=\sqrt{\frac{2}{\pi}}\,\frac{1}{\sigma_j}\ }
$$

（用 $\frac{d}{dx}\operatorname{erf}(x)=\frac{2}{\sqrt\pi}e^{-x^2}$，在 $x=0$ 取值 $2/\sqrt\pi$，再乘
內層 $1/(\sqrt2\sigma_j)$。）

- **Dimension check**：$\langle e\rangle$ 無因次、$\Delta t$ 是秒 → $K_{bb}$ 單位 $\text{s}^{-1}$ ✓。
  乘上 UI 得「每 UI 誤差輸出多少」的無因次增益 $K_{bb}\cdot\text{UI}$。
- **物理意義**：$\sigma_j$ 越大，erf 越平緩、增益越小。**bang-bang 迴路的增益是 jitter 的倒數**——
  這是 Lee–Kundert–Razavi 的核心結論（外部文獻，非本站 5 篇 PDF：J. Lee, K. S. Kundert, and B. Razavi,
  "Analysis and Modeling of Bang-Bang Clock and Data Recovery Circuits," *IEEE J. Solid-State Circuits*,
  vol. 39, no. 9, pp. 1571–1580, Sep. 2004）。
- **線性區**：erf 在 $\lvert\Delta t\rvert\lesssim\sigma_j$ 才近似直線（$\langle e\rangle(\sigma_j)=0.683$、
  $\langle e\rangle(2\sigma_j)=0.954$ 已飽和）；切線與 $\pm1$ 相交於 $\Delta t=\pm\sigma_j\sqrt{\pi/2}$。
  更大的誤差進入 **slew-limited（斜率受限）** 區——第 4 步 JTOL 的 $-20$ dB/dec 段就住在這裡。
- **轉態密度**：只有轉態才更新，平均增益再乘 $\rho_T$（隨機資料 $\approx0.5$）。

> **worked example（站台值）**：資料邊緣與時脈之間的 rms jitter 取本站 canonical 例 C 的
> $\sigma_t=447.9$ fs（free-running 5 GHz VCO、$-100$ dBc/Hz @ 1 MHz、積 1→100 MHz；這裡當作
> $\sigma_j$ 的代表值），UI $=40$ ps（25 Gb/s NRZ，同 [final_exam](/04_simulation_labs/final_exam) 題 10）。

$$
K_{bb}=\sqrt{\frac{2}{\pi}}\cdot\frac{1}{447.9\times10^{-15}\ \text{s}}
=\frac{0.7979}{4.479\times10^{-13}\ \text{s}}=1.78\times10^{12}\ \text{s}^{-1},
\qquad K_{bb}\cdot\text{UI}=1.78\times10^{12}\times40\times10^{-12}=71.3\ \text{(per UI)}.
$$

也就是說 PD 的期望輸出在時脈偏離 $1/71.3\ \text{UI}=0.014$ UI $=0.56$ ps 時就打到 $\pm1$——
線性區只有半個 ps 寬。**ISF 算出來的 $\sigma_t$ 越小（VCO 越乾淨），$K_{bb}$ 越大、迴路越快，
但線性區也越窄**：這是 bang-bang 與線性 PLL 最不一樣的地方。

```python
import numpy as np
from scipy.special import erf
sigma_t = 447.9e-15   # s, canonical example C (free-running VCO, 1-100 MHz)
UI = 40e-12           # s, 25 Gb/s NRZ
K_bb = np.sqrt(2/np.pi)/sigma_t
print(f"{K_bb:.3e}", round(K_bb*UI, 1))
# -> 1.781e+12 71.3
d = 1e-18             # numerical derivative of erf(dt/(sqrt2 sigma)) at 0
slope = (erf(d/(np.sqrt(2)*sigma_t)) - erf(-d/(np.sqrt(2)*sigma_t)))/(2*d)
print(f"{slope:.3e}", round(sigma_t*np.sqrt(np.pi/2)*1e12, 3))
# -> 1.781e+12 0.561
```

## 第 3 步：PI 迴路——φ[k+1] = φ[k] + K_p·sign(e)、UI/2^b 量化、hunting 極限環

現代 SerDes CDR 多半沒有 VCO 在迴路裡：一顆共用的 PLL 產生固定頻率的多相位時脈，CDR 用
**相位內插器（PI）** 在這些相位之間內插出取樣時脈；PI 由一個 $b$ 位元的相位碼控制，一個 UI
分成 $2^b$ 步：

$$
\Delta\phi_{PI}=\frac{\text{UI}}{2^b}\qquad(b=6:\ \frac{40\ \text{ps}}{64}=0.625\ \text{ps}=0.0156\ \text{UI}).
$$

最簡單的**一階 bang-bang 迴路**每隔一個更新週期 $T_u=N_{dec}\cdot\text{UI}$（$N_{dec}$ 是 PD 輸出的
降頻／投票倍數）把相位碼往 PD 說的方向推一步：

$$
\phi[k+1]=\phi[k]+K_p\,\text{sign}(e[k]),\qquad K_p=m\cdot\Delta\phi_{PI}\ (m\ \text{個 LSB}).
$$

**三個離散化後果**（外部文獻，非本站 5 篇 PDF：R. C. Walker, "Designing Bang-Bang PLLs for Clock and
Data Recovery in Serial Data Transmission Systems," in *Phase-Locking in High-Performance Systems*,
B. Razavi, Ed., IEEE Press, 2003）：

1. **Hunting（極限環）**：鎖定後 PD 仍然只會說「早」或「晚」，相位碼在最佳點兩側來回跳，形成
   峰峰 $K_p$ 的確定性抖動；若迴路有 $D$ 個更新週期的延遲（判斷到執行之間的 pipeline），
   相位在反向前會多走 $D$ 步，極限環放大成 **峰峰 $(2D+1)K_p$**（下方 Python 用無雜訊模型直接數）。
   這是一個 **DJ**：進 TJ 預算時用 $\text{DJ}_{pp}$ 直接相加，不隨 BER 放大（見
   [dj_dual_dirac](/06_design_insights/dj_dual_dirac)）。
2. **量化雜訊**：若把 PI 的相位誤差視為均勻分布，rms $=\Delta\phi_{PI}/\sqrt{12}=0.18$ ps——
   與 $\sigma_t=0.45$ ps 同量級，不能忽略。
3. **線性化頻寬**：把第 2 步的 $K_{bb}$ 代進去，每次更新的相位修正 $\approx K_p K_{bb}\rho_T\,\Delta t$，
   連續時間近似得一階迴路

$$
\frac{d\phi_{clk}}{dt}\approx\frac{K_pK_{bb}\rho_T}{T_u}\,(\phi_{data}-\phi_{clk})
\ \Rightarrow\ f_{BW}\approx\frac{K_pK_{bb}\rho_T f_u}{2\pi},\qquad f_u=\frac{1}{T_u}.
$$

- **Dimension check**：$K_p$ [s] $\times K_{bb}$ [1/s] $\times f_u$ [1/s] $=$ [1/s] ✓；
  $K_pK_{bb}$ 是「每次更新的迴路增益」（無因次），離散迴路要 $K_pK_{bb}\rho_T\lt2$ 才穩定、
  且線性化本身只在 $K_p\lesssim\sigma_j$（步伐小於雜訊）時成立。
- **worked（站台值）**：$K_p=1$ LSB $=0.625$ ps、$K_{bb}=1.78\times10^{12}$ s$^{-1}$、$\rho_T=0.5$。
  $N_{dec}=1$（每 UI 更新）：$K_pK_{bb}=1.11$ 每次更新——已超出線性化能描述的範圍（步伐
  $0.625$ ps 大於 $\sigma_j=0.448$ ps），名義 $f_{BW}=2.2$ GHz 無意義；$N_{dec}=16$
  （$f_u=1.5625$ GHz）：$f_{BW}\approx0.5\times0.625\text{ ps}\times1.78\times10^{12}\text{ s}^{-1}
  \times1.5625\times10^9\text{ s}^{-1}/2\pi=138$ MHz（位元率的 $0.55\%$）。這是**比例路徑的
  小訊號頻寬**，只在誤差 $\lesssim\sigma_j$ 的線性區內成立；它**不是**第 4–5 步用來畫 mask 的
  type-II $f_n=1$ MHz 樣板——兩者差兩個量級，關係在第 4 步的 slew 線與第 5 步的積分路徑交代。
  誠實聲明：這裡 $K_p\approx\sigma_j$，hunting 會把有效 $\sigma_j$ 推高、$K_{bb}$ 拉低；下方
  「數值驗證」的 Monte-Carlo 量到每次更新的有效增益 $0.38$（線性化 $0.557$）、有效頻寬 $94$ MHz。
- **比例路徑的追頻能力（slew）**：每秒最多移動 $(K_p/\text{UI})\,f_u$ 個 UI（每次更新都有判斷時的
  上限），換算成可追的頻率偏移 $(K_p/\text{UI})\,f_u/f_b$：$N_{dec}=1$ 為 $1/64=15\,625$ ppm、
  $N_{dec}=16$ 為 $977$ ppm。若像上面的線性化模型那樣每次更新只取**一個** PD 判斷，隨機資料有一半的
  更新沒有轉態、相位不動，平均 slew 再乘 $\rho_T$（$N_{dec}=16$：$488$ ppm）；對 $N_{dec}$ 個判斷做
  多數決則幾乎每次更新都有輸出，回到 $977$ ppm。第 5 步會拿它對照 SSC 的 5000 ppm。

```python
import numpy as np
fb, UI, b = 25e9, 40e-12, 6
Kp = UI/2**b
print(round(Kp*1e12, 3), round(Kp/UI, 4), round(Kp/np.sqrt(12)*1e12, 3))
# -> 0.625 0.0156 0.18
K_bb = np.sqrt(2/np.pi)/447.9e-15
for Ndec in (1, 16):
    fu = fb/Ndec
    f_bw = 0.5*Kp*K_bb*fu/(2*np.pi)     # rho_T = 0.5 (random data); one sign per update, no voting
    print(Ndec, f"{f_bw:.3e}", f"{(Kp/UI)*fu/fb*1e6:.0f}")
# -> 1 2.215e+09 15625
# -> 16 1.384e+08 977
def hunting_pp(D, n=400):               # noise-free limit cycle, latency D updates, units of Kp
    phi, q, hist = 0.3, [0.0]*D, []
    for k in range(n):
        q.append(-np.sign(phi) if phi != 0 else 1.0)
        phi += q.pop(0)
        hist.append(phi)
    h = np.array(hist[n//2:])
    return float(h.max() - h.min())
print([hunting_pp(D) for D in (0, 1, 2, 4)])
# -> [1.0, 3.0, 5.0, 9.0]
```

> **側欄：DLL 為什麼「不累積」jitter**（外部文獻，非本站 5 篇 PDF：J. G. Maneatis, "Low-Jitter
> Process-Independent DLL and PLL Based on Self-Biased Techniques," *IEEE J. Solid-State Circuits*,
> vol. 31, no. 11, pp. 1723–1732, Nov. 1996）。上面的 PI 架構其實是 DLL（delay-locked loop）思維：
> 迴路裡**沒有振盪器**，只有「對參考時脈的延遲」。振盪器的相位是頻率的積分，白噪 → 相位
> random walk → $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$（[P2] Eq.(8), p.792，見 [lc_vs_ring](/06_design_insights/lc_vs_ring)）；
> 延遲線的誤差**每個週期都被參考邊緣重新歸零**，噪聲只加一次、不累積。代價是輸出 jitter
> 直接繼承參考時脈的 jitter（沒有 high-pass 去濾它），而且沒有頻率自由度——所以 PI-CDR 的
> 「追頻」全靠第 5 步的積分路徑在數位域累加相位碼。

## 第 4 步：JTOL(f) = (UI − TJ_eye)/|1 − H(f)| 與 mask 的 −40／−20 dB/dec 段

[pll_noise_budget](/06_design_insights/pll_noise_budget) 已經把 **jitter transfer**（$\lvert H_{lp}\rvert^2$）
與 **jitter tolerance**（由誤差轉移 $1-H_{lp}=H_{hp}$ 決定）分清楚：CDR 追不上的那部分輸入 jitter
$\phi_{err}=(1-H)\phi_{data}$ 才吃眼圖。給定眼圖裕度 $\text{UI}-\text{TJ}_{eye}$，可容忍的單頻正弦
輸入 jitter 是

$$
\boxed{\ \text{JTOL}_{pp}(f)=\frac{\text{UI}-\text{TJ}_{eye}}{\lvert1-H(f)\rvert}\ }
$$

> ⚠️ **慣例旗標（peak vs peak-to-peak，差 2×）**：業界 JTOL mask 以**峰峰**（UI pp）標示。取樣點在
> 眼中央、可左右各偏 $(\text{UI}-\text{TJ}_{eye})/2$，正弦誤差的峰值 $\le(\text{UI}-\text{TJ}_{eye})/2$
> ⇔ 峰峰 $\le\text{UI}-\text{TJ}_{eye}$——所以上式讀成 **peak-to-peak** 才與 mask 對得上；
> [pll_noise_budget](/06_design_insights/pll_noise_budget) 的同一式把它稱為 peak 幅度，數值相同、
> 讀法差 2×，引用時要說清楚是哪一種。

**mask 的三段從哪裡來**——把 type-II 二階環 $1-H_{lp}=H_{hp}(s)=\dfrac{s^2}{s^2+2\zeta\omega_ns+\omega_n^2}$
分段近似：

| 頻段 | $\lvert H_{hp}\rvert$ 近似 | JTOL 斜率 | 物理 |
|---|---|---|---|
| $f\ll f_z=f_n/(2\zeta)$ | $(f/f_n)^2$ | $-40$ dB/dec | 頻率積分器＋相位積分器：兩個積分追蹤慢擺動 |
| $f_z\ll f\ll2\zeta f_n$（$\zeta$ 大才明顯） | $f/(2\zeta f_n)$ | $-20$ dB/dec | 迴路零點：只剩比例路徑在追 |
| $f\gg f_n$ | $\to1$ | 平台 $\text{UI}-\text{TJ}_{eye}$ | 完全追不上，只剩靜態眼圖裕度 |

bang-bang 迴路還多一條 **slew-limited 的 $-20$ dB/dec 線**：峰峰 $A_{pp}$、頻率 $f$ 的正弦相位，
最大斜率是 $\pi A_{pp}f$；比例路徑每秒最多追 $(K_p/\text{UI})f_u$ UI，所以

$$
A_{pp}\le\frac{(K_p/\text{UI})\,f_u}{\pi f}\qquad(-20\ \text{dB/dec；Walker 2003、Lee–Kundert–Razavi 2004}).
$$

**這條線屬於「只有比例路徑」的迴路。** 用第 3 步的數字（$K_p=0.625$ ps、$N_{dec}=16$）：
$(K_p/\text{UI})f_u=0.015625\times1.5625\times10^9=2.44\times10^7$ UI/s，30 kHz 處
$A_{pp}\le2.44\times10^7/(\pi\times3\times10^4)=259$ UI（每次更新只取一個判斷、$\rho_T=0.5$ 時再減半為
$129.5$ UI）——**低於**第 5 步 SSC 需要的 $521$ UI。也就是說，第 3 步那顆一階迴路追不上 SSC。
第 5 步的積分（頻率）路徑用頻率暫存器記住「每次更新該走多少」，把這條**速度上限**拿掉，換成一條
**加速度上限**（$-40$ dB/dec，第 5 步推導）；有了它，表格第一列的 $-40$ dB/dec 段才存在。

**幾條線怎麼組合**：線性三段是 $1/\lvert H_{hp}\rvert=\lvert1+2\zeta\omega_n/s+\omega_n^2/s^2\rvert$ 的三項，
哪一項大就由哪一項主導；bang-bang 的大訊號極限（slew 線、加速度線）則是另一個**上限**，實際容忍度是
$\min(\text{線性值},\ \text{大訊號極限})$。這就是為什麼規格書的 JTOL 折線長那樣：**低頻 $-40$、中頻 $-20$、
高頻平台**——每一段對應迴路裡一個不同的機制。

> **worked example（mask 的線性樣板；站台值，與 pll_noise_budget 同一組數）**：UI $=40$ ps、$\sigma_t=447.9$ fs、
> $\text{TJ}_{eye}=2Q^{-1}(10^{-12})\sigma_t=2\times7.03\times0.4479$ ps $=6.30$ ps $=0.157$ UI，
> 裕度 $0.843$ UI；type-II、$f_n=1$ MHz、$\zeta=0.707$。

$$
\begin{aligned}
\text{JTOL}(10\ \text{kHz})&=\frac{0.843}{(10^4/10^6)^2}=\frac{0.843}{10^{-4}}=8.4\times10^{3}\ \text{UI},\\
\text{JTOL}(30\ \text{kHz})&=\frac{0.843}{9.0\times10^{-4}}=936\ \text{UI},\quad
\text{JTOL}(100\ \text{kHz})=84\ \text{UI},\quad
\text{JTOL}(1\ \text{MHz})=\frac{0.843}{0.707}=1.19\ \text{UI},\quad
\text{JTOL}(10\ \text{MHz})=0.84\ \text{UI}.
\end{aligned}
$$

10 kHz→100 kHz 恰好 $-40$ dB/dec（$8426\to84.3$，$100\times$）；$\zeta=0.707$ 時零點 $f_z=707$ kHz
幾乎貼著 $f_n$，$-20$ 段看不見；把 $\zeta$ 拉到 4（$f_z=125$ kHz）100 kHz→1 MHz 的斜率就變成
$-24$ dB/dec——這就是規格書中段 $-20$ dB/dec 的來源之一。

```python
import numpy as np
from simulations.common.pll_utils import H_highpass_mag2
UI, sigma_t, qinv = 40e-12, 447.9e-15, 7.03
TJ_eye = 2*qinv*sigma_t
margin_UI = 1 - TJ_eye/UI
print(round(TJ_eye*1e12, 2), round(TJ_eye/UI, 3), round(margin_UI, 3))
# -> 6.3 0.157 0.843
fn, zeta = 1e6, 0.707
for f in [1e4, 3e4, 1e5, 1e6, 1e7]:
    H_hp = np.sqrt(H_highpass_mag2(np.array([f]), fn, zeta)[0])   # amplitude |1-H_lp|
    print(f"{f:.0e}", f"{H_hp:.3e}", round(margin_UI/H_hp, 2))
# -> 1e+04 1.000e-04 8425.63
# -> 3e+04 9.000e-04 936.18
# -> 1e+05 1.000e-02 84.26
# -> 1e+06 7.072e-01 1.19
# -> 1e+07 1.000e+00 0.84
def jtol_slope(zeta, fa, fb):           # dB per decade of JTOL between fa and fb = 10 fa
    Ha, Hb = (np.sqrt(H_highpass_mag2(np.array([x]), fn, zeta)[0]) for x in (fa, fb))
    return float(20*np.log10((margin_UI/Hb)/(margin_UI/Ha)))
for zeta in (0.707, 4.0):
    print(zeta, [round(jtol_slope(zeta, fa, 10*fa), 1) for fa in (1e4, 1e5, 1e6)])
# -> 0.707 [-40.0, -37.0, -3.0]
# -> 4.0 [-37.9, -24.0, -16.0]
Kp, fu, rho_T = UI/64, 25e9/16, 0.5     # Step-3 loop: proportional path only
slew = (Kp/UI)*fu                       # UI/s when every update carries a decision
print(f"{slew:.3e}", round(slew/(np.pi*3e4), 1), round(rho_T*slew/(np.pi*3e4), 1), round(rho_T*slew/25e9*1e6))
# -> 2.441e+07 259.0 129.5 488
```

**Dimension check**：$\text{UI}-\text{TJ}_{eye}$ [UI] ÷ 無因次幅度轉移 $=$ [UI] ✓；slew 線
$[\text{UI/s}]/[\text{1/s}]=[\text{UI}]$ ✓。

## 第 5 步：SSC——CDR 必須追的三角 FM，521 UI 峰峰相位

**展頻時脈（SSC）** 為了把 EMI 能量攤開，故意把發送端時脈頻率以 $f_m\approx30$–$33$ kHz 的**三角波**
從名義值往下掃到 $-\delta$（down-spread，PCIe-style $\delta=0.5\%$；PCIe Base Spec，版本待查；外部
文獻，非本站 5 篇 PDF）。對接收端 CDR 而言這不是雜訊，是**一個必須追蹤的確定性 FM**——當 RX
的參考時脈沒有跟著展頻（separate-reference 架構）時尤其如此。

**逐步推導峰峰相位**。設位元率 $f_b$，頻率偏移相對中心值是振幅 $\pm\delta f_b/2$、週期 $T_m=1/f_m$
的三角波。相位（以 UI 計）是頻率偏移的積分；三角波在正半週的面積 $=\tfrac12\cdot\tfrac{T_m}{2}\cdot\tfrac{\delta f_b}{2}=\dfrac{\delta f_bT_m}{8}$，
這就是相位的峰峰值：

$$
\boxed{\ \Delta\phi_{pp}=\frac{\delta\,f_b\,T_m}{8}\ \text{UI}
=\frac{1}{4}\,T_m\,\Delta f_{pk}\ \text{cycles}\ }\qquad(\Delta f_{pk}=\delta f_{clk}/2\ \text{為時脈的峰值頻偏}).
$$

代入 $f_b=25$ Gb/s（半速率時脈 $f_{clk}=12.5$ GHz）、$\delta=0.005$、$f_m=30$ kHz（$T_m=33.3$ µs）：

$$
\Delta f_{pk}=\frac{0.005\times12.5\ \text{GHz}}{2}=31.25\ \text{MHz},\quad
\Delta\phi_{pp}=\tfrac14\times33.3\ \mu\text{s}\times31.25\ \text{MHz}=260\ \text{週期}
=260\times80\ \text{ps}=20.8\ \text{ns}=521\ \text{UI}.
$$

- **Dimension check**：$[\text{s}]\times[\text{1/s}]=$ 無因次（週期數）✓；一個 12.5 GHz 週期 $=2$ UI ✓。
- **這是五百多個 UI 的相位擺動**，比任何 RJ 大四個量級。30 kHz 的容忍度必須 $\gt521$ UI，而判斷要用
  第 4 步的 $\min(\text{線性值},\ \text{大訊號極限})$：type-II、$f_n=1$ MHz 樣板的線性值是 $936$ UI
  （10 kHz 為 $8.4\times10^3$ UI），但**只有比例路徑**時 slew 線只給 $259$ UI ✗——$936$ UI 要有積分路徑
  才拿得到（本步最後三點）。
- **殘餘誤差有多大**：三角 FM 的每一段是**頻率斜坡**＝相位拋物線 $\phi_{in}=\tfrac12at^2$，
  $a=\delta f_b/(T_m/2)=7.5\times10^{12}$ UI/s²。對 type-II 二階環，$E(s)=H_{hp}(s)\cdot a/s^3$ 的終值
  $e_{ss}=a/\omega_n^2=7.5\times10^{12}/(2\pi\times10^6)^2=0.19$ UI——斜坡每 $T_m/2$ 換一次方向，
  誤差是 $\pm0.19$ UI 的方波（峰峰 0.38 UI）。頻域交叉檢查：逐段拋物線的**基頻**峰峰值不是 521 UI，
  而是 $521\times32/\pi^3=538$ UI（三角波基頻 $8/\pi^2$ 再積分一次），乘上
  $\lvert H_{hp}(30\ \text{kHz})\rvert=9.0\times10^{-4}$ 得 $0.48$ UI pp $=0.38\times4/\pi$，正是方波的基頻 ✓。這 0.19 UI 要從
  0.843 UI 的裕度裡扣——**SSC 是 CDR 預算裡一項不小的 DJ**。（注意這是**線性 PD** 樣板的結果：
  bang-bang PD 在 $\pm0.56$ ps 就飽和，$0.19$ UI 的誤差會要求平均輸出 $K_{bb}\cdot0.19\ \text{UI}=13.5\gg1$，
  不可能出現；bang-bang 迴路自己的 SSC 殘餘見最後一點。）
- **一階迴路（type-I）不行**：同樣 1 MHz 頻寬的一階環 $\lvert1-H\rvert=f/\sqrt{f^2+f_{BW}^2}=0.030$
  @30 kHz → JTOL 只有 $28$ UI $\ll521$；更根本的是 type-I 對 5000 ppm 的頻率偏移有**靜態相位誤差**
  $\Delta f/(2\pi f_{BW})=0.005\times25\times10^9/(2\pi\times10^6)=19.9$ UI，直接失鎖。
- **在 bang-bang PI 迴路裡誰來追**：第 3 步算過比例路徑的追頻上限 $977$ ppm（$N_{dec}=16$；每次更新
  單一判斷時 $488$ ppm）$\lt5000$ ppm，等價地第 4 步的 slew 線 $259$ UI $\lt521$ UI——比例路徑追不動
  SSC；**追 SSC 是積分（頻率）路徑的工作**：
  $\phi[k+1]=\phi[k]+K_p\text{sign}(e)+\omega[k]$、$\omega[k+1]=\omega[k]+K_i\text{sign}(e)$，
  頻率暫存器 $\omega$ 把「每次更新該走幾分之一個 LSB」記住，讓 PD 回到只處理 jitter。這就是
  數位 CDR 幾乎都是 type-II 的原因。
- **積分路徑把速度上限換成加速度上限**：$\omega$ 每次更新最多改變 $K_i$（隨機資料平均 $\rho_TK_i$），
  所以相位加速度的上限是 $a_{max}=\rho_T(K_i/\text{UI})f_u^2$（單位：[UI/更新²]×[更新/s]² $=$ UI/s² ✓）。
  峰峰 $A_{pp}$ 的正弦相位最大加速度是 $2\pi^2f^2A_{pp}$，得 $A_{pp}\le a_{max}/(2\pi^2f^2)$（$-40$ dB/dec）。
  取 $K_i=K_p/1024=0.61$ fs/更新²（第 3 步的迴路加上這條積分路徑）：$a_{max}=1.86\times10^{13}$ UI/s²。
  (i) SSC 斜坡 $a=7.5\times10^{12}$ UI/s² 只用掉 $40\%$ ✓（追 SSC 的最低要求是 $K_i\gt0.25$ fs/更新²）；
  (ii) 30 kHz 的加速度線是 $1048$ UI $\gt521$ UI ✓；(iii) 把它寫成樣板的低頻形式
  $(\text{UI}-\text{TJ}_{eye})\,f_{n,eq}^2/f^2$，得 $f_{n,eq}=\sqrt{a_{max}/(2\pi^2\times0.843)}=1.06$ MHz。
  **這就是第 3 步的迴路與第 4–5 步 $f_n=1$ MHz 樣板的關係**：樣板是這顆 bang-bang 迴路**大訊號**
  $-40$ dB/dec 線的等效寫法（$936$ UI 對 $1048$ UI），不是它的小訊號轉移函數——小訊號是
  $f_n=5.8$ MHz、$\zeta=11.9$（比例路徑頻寬 $2\zeta f_n=138$ MHz），線性值在 30 kHz 高達 $3.2\times10^4$ UI，
  所以真正卡住的是加速度線。反過來，要讓小訊號響應就是 1 MHz／0.707，$K_p$ 得縮到 $6.4$ fs
  $\approx$ LSB/98，那顆迴路的 slew 線在 30 kHz 只剩幾個 UI。
- **bang-bang 迴路的 SSC 殘餘**：追斜坡時頻率暫存器要以 $a$ 的速率變化，PD 的平均輸出必須是
  $\rho_T\operatorname{erf}(\Delta t/\sqrt2\sigma_j)=\rho_T\,a/a_{max}$，所以平均誤差
  $\Delta t=\sqrt2\,\sigma_j\operatorname{erf}^{-1}(a/a_{max})=0.24$ ps（只算 $\sigma_j$；把 hunting 併入
  $\sigma_j$ 後模擬量到 $0.38$ ps）——是 **ps 等級**，不是線性樣板的 $0.19$ UI $=7.6$ ps。

```python
import numpy as np
from simulations.common.pll_utils import H_highpass_mag2
fb, UI = 25e9, 40e-12         # bit rate, UI
delta, fm = 0.005, 30e3       # -0.5 % down-spread, 30 kHz triangle (PCIe-style)
Tm = 1/fm
pp_cycles = 0.25*Tm*(delta*12.5e9/2)   # half-rate 12.5 GHz clock: +-31.25 MHz around centre
pp_UI = delta*fb*Tm/8
print(round(pp_cycles, 1), round(pp_UI, 1))
# -> 260.4 520.8
fn, zeta = 1e6, 0.707
margin_UI = 1 - 2*7.03*447.9e-15/UI    # 0.843 UI eye margin (Step 4)
a = (delta*fb)/(Tm/2)                  # phase acceleration during each ramp, UI/s^2
e_ss = a/(2*np.pi*fn)**2
H30 = np.sqrt(H_highpass_mag2(np.array([fm]), fn, zeta)[0])
pp_fund = pp_UI*32/np.pi**3            # fundamental (pp) of the piecewise-parabolic phase, not its pp
print(round(pp_fund, 1), f"{a:.2e}", round(e_ss, 3), round(pp_fund*H30, 3), round(margin_UI/H30, 1))
# -> 537.5 7.50e+12 0.19 0.484 936.2
fbw1 = 1e6                             # first-order (type-I) loop with the same bandwidth
H1 = fm/np.sqrt(fm**2 + fbw1**2)
print(round(margin_UI/H1, 1), round(delta*fb/(2*np.pi*fbw1), 1))
# -> 28.1 19.9
from scipy.special import erfinv
Kp, fu, rho_T = UI/64, fb/16, 0.5      # Step-3 loop (N_dec = 16) plus an integral path
K_bb = np.sqrt(2/np.pi)/447.9e-15
Ki = Kp/1024                           # s per update^2
a_max = rho_T*(Ki/UI)*fu**2            # UI/s^2: acceleration limit of the frequency register
print(f"{Ki*1e15:.4f}", f"{a_max:.3e}", round(a/a_max, 3), round(a_max/(2*np.pi**2*fm**2), 1),
      round(a*UI/(rho_T*fu**2)*1e15, 3))
# -> 0.6104 1.863e+13 0.403 1048.5 0.246
fn_eq = np.sqrt(a_max/(2*np.pi**2*margin_UI))            # large-signal equivalent of the template
fn_ss = np.sqrt(Ki*K_bb*rho_T)*fu/(2*np.pi)              # small-signal natural frequency
zeta_ss = Kp*K_bb*rho_T/(2*np.sqrt(Ki*K_bb*rho_T))
H_ss = np.sqrt(H_highpass_mag2(np.array([fm]), fn_ss, zeta_ss)[0])
print(round(fn_eq/1e6, 3), round(fn_ss/1e6, 2), round(zeta_ss, 1), round(2*zeta_ss*fn_ss/1e6, 1),
      f"{margin_UI/H_ss:.2e}")
# -> 1.058 5.8 11.9 138.4 3.17e+04
Kp_lin = 2*zeta*2*np.pi*fn/(K_bb*rho_T*fu)               # K_p whose small-signal loop IS 1 MHz / 0.707
print(round(Kp_lin*1e15, 2), round(Kp/Kp_lin, 1), round((Kp_lin/UI)*fu/(np.pi*fm), 2),
      round(0.19*UI*K_bb, 1), round(np.sqrt(2)*447.9e-15*erfinv(a/a_max)*1e12, 3))
# -> 6.38 97.9 2.65 13.5 0.237
```

## 數值驗證：lab_45 的 Monte-Carlo 與時域模擬 {#numerical-check}

前五步的每個公式都是線性化或漸近線；`simulations/lab_45_bb_cdr.py` 用行為級模型把它們各檢查一次。
模型與本頁完全同一組數：25 Gb/s、UI $=40$ ps、$\sigma_j=447.9$ fs、$K_p=\text{UI}/64$、$N_{dec}=16$
（$f_u=1.5625$ GHz）、每次更新取一個 Alexander 判斷（$\rho_T=0.5$）、$K_i=K_p/1024$；通過與否的判準是
「確定性追蹤誤差的峰值 $\le(\text{UI}-\text{TJ}_{eye})/2$」，也就是第 4 步的峰峰裕度 $0.843$ UI。

![六格圖：(a) Alexander 三個取樣點在時脈早與時脈晚兩種情況下的時序圖；(b) Monte-Carlo 的相位偵測器平均輸出對靜態偏移，與 erf 理論及 K_bb 切線重合；(c) 一階 bang-bang 迴路的 hunting，無雜訊時峰峰 1 與 5 個 K_p，有 jitter 時 rms 0.81 K_p；(d) 正弦 jitter 容忍度對頻率，只有比例路徑的模擬點沿 slew 線，比例加積分的模擬點在低頻沿加速度線、中頻沿 slew 線、高頻為平台，並標出 SSC 需要的 521 UI；(e) SSC 三角調變下只有比例路徑的迴路誤差發散到數千 UI，比例加積分保持在裕度內；(f) 比例加積分迴路追 SSC 的誤差放大圖，平均誤差約正負 0.37 ps](/figures/bb_cdr.png)

**怎麼讀這張圖**

- **(a) 三個取樣點**：轉態在 $t=0$。時脈早（藍）時三個取樣點整體左移，$E_k$ 落在轉態前、讀到舊位元
  （$E_k=D_{k-1}$）；時脈晚（紅）時 $E_k$ 落在轉態後、讀到新位元（$E_k=D_k$）。這就是第 1 步的真值表。
- **(b) PD 特性**：把真值表原樣套在隨機 NRZ 資料上（邊緣加 $\sigma_j$ 的高斯 jitter），只統計有轉態的
  位元，原點斜率／$K_{bb}=0.99$；對**全部**位元平均則是 $0.49\,K_{bb}$——轉態密度（量到 $0.50$）就是
  第 3 步 $f_{BW}$ 公式裡的 $\rho_T$。
- **(c) hunting**：無雜訊、延遲 $D=0,1,2$ 的極限環峰峰值正好 $1,3,5$ 個 $K_p$（$(2D+1)K_p$）。有 jitter
  時不再是整齊的極限環，而是被雜訊打散的隨機遊走：線性化給 $\sigma_{hunt}=\sqrt{K_p/(2K_{bb})}=419$ fs
  （由 $\sigma^2$ 的遞迴式 $2K_p\rho_TK_{bb}\sigma^2=K_p^2\rho_T$ 得到，與 $\rho_T$ 無關），模擬量到 $509$ fs
  （比值 $1.22$）。差距正是第 3 步的誠實聲明：$K_p\approx\sigma_j$ 時 erf 已彎，每次更新的有效增益只有
  $0.38$（線性化 $0.557$），有效頻寬 $94$ MHz 而非 $138$ MHz。
- **(d) 正弦 jitter 容忍度**：只有比例路徑（藍方塊）整條貼著 slew 線；30 kHz 量到 $126$ UI，是 $\rho_T$ slew 線
  $129.5$ UI 的 $0.97$ 倍（略低，因為隨機的轉態數讓 slew 本身有起伏，迴路必須留一點餘裕）；改成 16 個判斷
  多數決則量到 $262$ UI，是 $259$ UI 的 $1.01$ 倍。兩者都低於紫色星號的 $521$ UI。加上積分路徑（紅圓點）
  後，低頻改沿加速度線：30 kHz 量到 $972$ UI（加速度線 $1048$ UI 的 $0.93$ 倍；線性樣板 $936$ UI），
  中頻回到 slew 線，高頻進入平台——三段分別是加速度、slew、靜態裕度。
- **(d) 的平台低於 0.843 UI**：100 MHz 量到 $0.54$ UI。大振幅的高頻正弦 jitter 把 PD 推到飽和、有效增益
  下降，恢復時脈自己多了一份慢速漂移，吃掉一部分裕度；公式的 $\text{UI}-\text{TJ}_{eye}$ 是不含這份
  漂移的上限。
- **(e)(f) SSC**：只有比例路徑的迴路在第一個斜坡就失鎖，誤差累積到約 $5.9\times10^3$ UI；加上積分路徑後
  峰值誤差 $0.08$ UI（$3.1$ ps），斜坡上的平均誤差 $0.38$ ps，方向隨斜坡反轉——與第 5 步
  $\sqrt2\sigma\operatorname{erf}^{-1}(a/a_{max})$ 的預測一致（$\sigma$ 取含 hunting 的有效值）。

```python
import numpy as np
from simulations.lab_45_bb_cdr import (alexander_mc, limit_cycle, hunting_noisy, sj_tolerance, bb_loop,
    ssc_phase, KP, KP_UI, KI_UI, K_BB, SIGMA_J, RHO_T, FU, UI, MARGIN_UI, N_DEC)
rng = np.random.default_rng(45)
d0 = 0.1*SIGMA_J                       # (b) literal Alexander truth table on random NRZ data
(ap, tp, rho), (am, tm, _) = alexander_mc(+d0, 4_000_000, rng), alexander_mc(-d0, 4_000_000, rng)
print(round((tp - tm)/(2*d0)/K_BB, 2), round((ap - am)/(2*d0)/K_BB, 2), round(rho, 2))
# -> 0.99 0.49 0.5
phi = hunting_noisy(1_000_000, rng)[5000:]          # (c) first-order loop, sigma_j present
g_eff = KP**2*RHO_T/(2*phi.var())
print([float(np.ptp(limit_cycle(D)[200:])) for D in (0, 1, 2)], round(phi.std()*1e15),
      round(np.sqrt(KP/(2*K_BB))*1e15), round(g_eff, 2), round(g_eff*FU/(2*np.pi)/1e6))
# -> [1.0, 3.0, 5.0] 509 419 0.38 94
f = 30e3                                            # (d) sinusoidal-jitter tolerance at 30 kHz, UI pp
s1, sv = RHO_T*KP_UI*FU/(np.pi*f), KP_UI*FU/(np.pi*f)
acc = RHO_T*KI_UI*FU**2/(2*np.pi**2*f**2)
j1 = sj_tolerance(f, 0.0, s1 + MARGIN_UI, rng, n_amp=64, span=0.2)
jv = sj_tolerance(f, 0.0, sv + MARGIN_UI, rng, vote=N_DEC, n_amp=64, span=0.2)
j2 = sj_tolerance(f, KI_UI, acc + MARGIN_UI, rng, n_amp=64, span=0.3)
jh = sj_tolerance(1e8, 0.0, MARGIN_UI, rng, n_amp=64, span=0.3)   # far above the loop bandwidth
print(round(j1), round(j1/s1, 2), round(jv), round(jv/sv, 2), round(j2), round(j2/acc, 2), round(jh, 2))
# -> 126 0.97 262 1.01 972 0.93 0.54
n, per = int(3*FU/f), int(FU/f)                     # (e) SSC: -0.5 %, 30 kHz triangle, 3 periods
worst, tr = bb_loop(lambda k: np.repeat(ssc_phase(k)[:, None], 2, axis=1), n, 2,
                    np.array([0.0, KI_UI]), rng, eval_from=0, trace=True)
tau = np.mod(np.arange(n), per)/per                 # 0.15-0.45: settled part of the up-ramp
up = (tau > 0.15) & (tau < 0.45) & (np.arange(n) > per)
print(round(worst[0]), round(worst[1], 2), round(worst[1]*UI*1e12, 1), round(tr[up, 1].mean()*UI*1e12, 2))
# -> 5927 0.08 3.1 0.38
```

（完整腳本另外掃了 10 kHz–100 MHz 共 13 個頻點並畫出上圖；亂數序列不同，數字與上面相差在
Monte-Carlo 起伏之內，例如比例＋積分迴路 30 kHz 為 $985$ UI。）

**限制（誠實聲明）**

- 這是相位域的**行為級**模型，不是電晶體級：PI 理想（無 INL/DNL）、取樣器無 metastability、
  資料無 ISI，隨機 jitter 只有逐次獨立的白色高斯 $\sigma_j$。
- 容忍度以「追蹤誤差峰值不超過 $(\text{UI}-\text{TJ}_{eye})/2$」判定，不是真的數 $10^{-12}$ 的 BER；
  每個頻點只跑 3 個 jitter 週期（至少 $3\times10^4$ 次更新），振幅格點間距約 $3\%$，高頻平台的數值
  會隨觀察時間略降。
- JTOL 與 SSC 兩個實驗取迴路延遲 $D=0$；實際 pipeline 延遲會放大 hunting（$(2D+1)K_p$）並壓低
  積分路徑可用的 $K_i$。
- 多數決只在 30 kHz 一個點檢查 slew 上限；它的小訊號增益不是 $\rho_TK_{bb}$，本頁沒有分析。
- SSC 由 $-0.5\%$ 理想三角波產生，起點頻偏為零；沒有模擬頻率擷取（acquisition）。

## 互動探索器：自己拉 σ_j、PI 位元與 N_dec {#interactive-explorer}

前面五步的每個量都是 $\sigma_j$、$b$、$N_{dec}$ 的函數；下面的元件把它們接在一起，讓你一次動一個旋鈕，同時看三張圖和六張讀數卡：

1. **PD 特性**：$\langle e\rangle=\operatorname{erf}(\Delta t/\sqrt2\sigma_j)$ 與原點切線 $K_{bb}\Delta t$（綠色虛線，在 $\pm\sigma_j\sqrt{\pi/2}$ 打到 $\pm1$）。橫軸固定在 $\pm3$ ps，所以拉 $\sigma_j$ 時曲線會真的變陡或變平；紅色小方塊是一個 PI 步伐 $K_p$ 的寬度。
2. **時域 hunting**：本頁數值驗證的行為級模型（每次更新一個 Alexander 判斷、$\rho_T=0.5$、固定種子、延遲 $D=0$），再疊上你設定的正弦 jitter，取整段模擬中誤差最大處附近的 200 次更新來畫。色帶是 $K_p$ 寬；黃色虛線是 $\pm(\text{UI}-\text{TJ}_{eye})/2$。
3. **JTOL 圖**：線性曲線、slew 線、（開積分路徑時的）加速度線、合成後採用的容忍度，以及你的操作點（圓點＝通過、叉＝失敗；菱形是 SSC 的 $521$ UI @ 30 kHz 需求）。

圖中採用的容忍度把第 4–5 步的說法寫成一條式子：

$$
\text{JTOL}(f)=\min\Big(\text{JTOL}_{lin}(f),\ \max\big(A_{slew}(f),\ A_{acc}(f),\ \text{UI}-\text{TJ}_{eye}\big)\Big),
$$

其中 $A_{slew}=\rho_T(K_p/\text{UI})f_u/(\pi f)$、$A_{acc}=\rho_T(K_i/\text{UI})f_u^2/(2\pi^2f^2)$（只有比例路徑時 $A_{acc}=0$，$K_i=K_p/1024$），$\text{UI}-\text{TJ}_{eye}$ 是迴路完全追不上時剩下的平台；$\text{JTOL}_{lin}$ 在只有比例路徑時是一階 $\text{margin}/\lvert1-H\rvert$（$f_{BW}$ 用第 3 步的 $K_pK_{bb}\rho_Tf_u/2\pi$），有積分路徑時是 type-II，
$f_n=\sqrt{K_iK_{bb}\rho_T}\,f_u/2\pi$、$\zeta=K_pK_{bb}\rho_T/\big(2\sqrt{K_iK_{bb}\rho_T}\big)$（第 5 步最後幾點用的小訊號公式）。
**SSC 追得上嗎**：有積分路徑時看 $a_{ssc}=7.5\times10^{12}$ UI/s² 是否不超過 $a_{max}$（卡片顯示 $a/a_{max}$）；只有比例路徑時看 slew 速率（ppm）是否大於 SSC 的 $5000$ ppm。預設值就是本頁的 worked example，按「還原本頁預設」即可回來：

<BbCdrExplorer />

**可以試的幾件事**

- **預設值對帳**：$\sigma_j=447.9$ fs 時 $K_{bb}=1.781\times10^{12}$ s$^{-1}$、$71.3$ 每 UI，6-bit PI 的 $K_p=0.625$ ps，$N_{dec}=16$ 的 $f_{BW}=138.4$ MHz，hunting 的線性化 rms $419$ fs，30 kHz 的 JTOL 是加速度線 $1048$ UI，$a/a_{max}=0.403$——全部與第 2–5 步一致。
- **關掉積分路徑**：30 kHz 的 JTOL 掉到 slew 線 $129.5$ UI，SSC 卡片變成「否」（$488$ ppm 對 $5000$ ppm），操作點從圓點變叉，時域圖的誤差一路發散。
- **把 PI 位元往 4 拉**：$K_p$ 變大、$K_p/\sigma_j$ 更超過 1（預設的 $6$ bit 就已經大於 1，警告列一開始就在）——erf 已彎，線性化的 $K_{bb}$、$f_{BW}$ 偏樂觀；時域圖的色帶（$K_p$ 寬）比雜訊還寬，hunting 變成確定性的來回跳。往 8 拉則 $K_p$ 縮到雜訊以下，警告消失，色帶縮進抖動裡。
- **把 $N_{dec}$ 往 1 拉**：$f_u$ 變大，$f_{BW}$ 與 slew 線同比上升（$N_{dec}=1$ 的名義 $f_{BW}=2.2$ GHz 是第 3 步說「無意義」的那個值）；往 64 拉則兩者同比下降，JTOL 與 SSC 卡片隨之翻成失敗。
- **把 $\sigma_j$ 拉大**：$K_{bb}$ 變小、PD 曲線變平、線性區變寬；但 $\text{TJ}_{eye}=2\times7.03\,\sigma_j$ 吃掉裕度，高頻平台下降。這就是「ISF 算出的 $\sigma_t$ 同時決定增益與裕度」。

**限制**：容忍度曲線是解析模型，時域面板是行為級模擬，兩者在通過／失敗邊界附近會差幾個百分點（頁面實驗室量到 $0.93$–$1.01$ 倍）；模擬長度設上限（600000 次更新），低頻或 $N_{dec}$ 很小時只涵蓋不到一個 jitter 週期，面板會標出；其餘假設同上一節的限制清單（理想 PI、無 ISI、白色高斯 $\sigma_j$、$D=0$）。

<NumericQuiz
  prompt="把探索器調成 σ_j = 300 fs、7-bit PI、N_dec = 8、比例＋積分（K_i = K_p/1024）、正弦 jitter 頻率 300 kHz。用上式取 JTOL（此處線性值遠大於大訊號線），300 kHz 的 JTOL 是多少 UI 峰峰？"
  answer={20.97}
  tol={0.05}
  unit="UI pp"
  hint="先算 K_p = UI/2^b 與 f_u = 25 Gb/s ÷ N_dec；slew 線與加速度線各算一個，取較大者（眼圖裕度只是更高頻的平台）。"
  solutionNote="slew 線 12.95 UI、加速度線 20.97 UI，取較大者——300 kHz 在這組設定下由積分路徑的加速度上限決定。"
/>

<details>
<summary><strong>解答與 Python 驗證</strong>（σ_j = 300 fs、7-bit、N_dec = 8、300 kHz）</summary>

**(a) 迴路參數。** $K_p=\text{UI}/2^7=40\ \text{ps}/128=0.3125$ ps，$f_u=f_b/N_{dec}=25\ \text{Gb/s}/8=3.125$ GHz，
$K_{bb}=\sqrt{2/\pi}/\sigma_j=2.660\times10^{12}$ s$^{-1}$（$106.4$ 每 UI）。

**(b) 兩條大訊號線**（第 4–5 步，$\rho_T=0.5$、$K_i=K_p/1024$）：

$$
A_{slew}=\frac{\rho_T(K_p/\text{UI})f_u}{\pi f}=12.95\ \text{UI},\qquad
A_{acc}=\frac{\rho_T(K_i/\text{UI})f_u^2}{2\pi^2f^2}=20.97\ \text{UI}.
$$

**(c) 取值。** 眼圖裕度 $\text{UI}-\text{TJ}_{eye}=1-2\times7.03\times0.300/40=0.8945$ UI 遠小於兩條線；線性小訊號值（$f_n=10.02$ MHz、$\zeta=10.3$）是 $1172$ UI，也遠大於大訊號線，所以
$\text{JTOL}=\max(12.95,\ 20.97,\ 0.8945)=20.97$ UI 峰峰（加速度線主導）。

**Dimension check**：$[\text{UI/s}]/[\text{1/s}]=[\text{UI}]$ 與 $[\text{UI/s}^2]/[\text{1/s}^2]=[\text{UI}]$ ✓。

```python
import numpy as np
from simulations.common.pll_utils import H_highpass_mag2
fb, UI, rho_T, qinv = 25e9, 40e-12, 0.5, 7.03
sigma, b, Ndec, f = 0.300e-12, 7, 8, 300e3       # quiz setting: P + I with K_i = K_p/1024
Kp = UI/2**b
fu = fb/Ndec
K_bb = np.sqrt(2/np.pi)/sigma
print(round(Kp*1e12, 4), f"{fu:.4e}", f"{K_bb:.3e}", round(K_bb*UI, 1))
# -> 0.3125 3.1250e+09 2.660e+12 106.4
margin = 1 - 2*qinv*sigma/UI
slew = rho_T*(Kp/UI)*fu/(np.pi*f)                 # UI pp, proportional path
acc = rho_T*(Kp/1024/UI)*fu**2/(2*np.pi**2*f**2)  # UI pp, integral path
print(round(margin, 4), round(slew, 2), round(acc, 2))
# -> 0.8945 12.95 20.97
g_p, g_i = Kp*K_bb*rho_T, Kp/1024*K_bb*rho_T      # small-signal gains per update
fn, zeta = np.sqrt(g_i)*fu/(2*np.pi), g_p/(2*np.sqrt(g_i))
lin = margin/np.sqrt(H_highpass_mag2(np.array([f]), fn, zeta)[0])
print(round(fn/1e6, 2), round(zeta, 2), round(lin))
# -> 10.02 10.31 1172
print(round(max(slew, acc, margin), 2), round(min(lin, max(slew, acc, margin)), 2))
# -> 20.97 20.97
```

</details>

## 設計旋鈕清單

| 旋鈕 | 影響 | 取捨 |
|---|---|---|
| VCO/參考的 $\sigma_t$（ISF：$\Gamma_{rms}/q_{max}$） | $K_{bb}=\sqrt{2/\pi}/\sigma_j$ → 迴路增益與 $f_{BW}$ | 越乾淨迴路越快、線性區越窄；$\sigma_j\lesssim K_p$ 時進入 hunting 主導 |
| PI 位元數 $b$ | $\Delta\phi_{PI}=\text{UI}/2^b$：hunting DJ $(2D+1)K_p$、量化 rms $/\sqrt{12}$ | $b\uparrow$ 步小、DJ 小，但每步能追的頻偏也小，PI 線性度變難 |
| 更新率 $f_u=f_b/N_{dec}$ | $f_{BW}\propto f_u$、slew $\propto f_u$ | $N_{dec}\uparrow$ 省功率／降延遲負擔，犧牲頻寬與追頻 |
| 迴路延遲 $D$ | hunting 峰峰 $(2D+1)K_p$ | pipeline 深度 vs 時序收斂 |
| 積分路徑 $K_i$ | 追 SSC／頻偏；加速度上限 $a_{max}=\rho_T(K_i/\text{UI})f_u^2$ 決定 $-40$ dB/dec 段 | 太大 → peaking、穩定裕度差、hunting 變大 |
| $\zeta$（零點位置 $f_z=f_n/2\zeta$） | $-20$ dB/dec 段長度、jitter peaking | 級聯多顆 CDR 時 peaking dB 相加（見 pll_noise_budget） |

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 高斯 $\sigma_j$、線性化 $K_{bb}$ | $K_p\lesssim\sigma_j$、誤差 $\lesssim\sigma_j$ | $K_p\gg\sigma_j$：hunting 主導、頻寬由 $K_p f_u$ 決定；大誤差進入 slew-limited |
| 連續時間迴路近似 | $f_{BW}\ll f_u$（$K_pK_{bb}\rho_T\ll1$） | 每次更新增益 $\gtrsim1$：要用離散模型（$N_{dec}=1$ 的例子） |
| JTOL 用幅度轉移 $\lvert1-H\rvert$ | 單頻正弦、小訊號線性迴路 | 大訊號：只有比例路徑用 slew 線 $A_{pp}\le(K_p/\text{UI})f_u/(\pi f)$，有積分路徑用加速度線 $a_{max}/(2\pi^2f^2)$；峰峰 vs 峰值讀法差 2× |
| $\text{TJ}_{eye}$ 只含 RJ | 無 ISI/DJ 的乾淨眼 | 真實鏈路要把 ISI、DCD、SSC 殘餘 0.19 UI、hunting $(2D+1)K_p$ 都放進 $\text{TJ}_{eye}$ |
| SSC 需由 CDR 追 | separate-reference 架構 | common-clock 架構 RX PLL 同步展頻，CDR 只看殘餘 |
| $\rho_T=0.5$ | scrambled／編碼資料 | 長 run length：PD 失明、有效 $f_{BW}$ 下降 |

## 重點回顧

- Alexander PD 只輸出 $\text{sign}(\Delta t)$（有轉態時）；高斯 jitter 把它抹成
  $\langle e\rangle=\operatorname{erf}(\Delta t/\sqrt2\sigma_j)$，線性化增益 $K_{bb}=\sqrt{2/\pi}/\sigma_j$。
- 站台值：$\sigma_t=447.9$ fs → $K_{bb}=1.78\times10^{12}$ s$^{-1}=71.3$/UI；線性區僅 $\pm0.56$ ps。
  **ISF 算出的 $\sigma_t$ 決定 bang-bang CDR 的增益與頻寬。**
- PI：$\text{UI}/2^b$（6-bit → 0.625 ps）；一階 BB 更新 $\phi[k+1]=\phi[k]+K_p\text{sign}(e)$；
  hunting 峰峰 $(2D+1)K_p$ 是 DJ；線性化 $f_{BW}=K_pK_{bb}\rho_Tf_u/2\pi$（$N_{dec}=16$ → 比例路徑
  小訊號 138 MHz；Monte-Carlo 有效值 94 MHz）。
- $\text{JTOL}_{pp}(f)=(\text{UI}-\text{TJ}_{eye})/\lvert1-H(f)\rvert$：$-40$（雙積分）／$-20$
  （零點或 slew：$A_{pp}\le(K_p/\text{UI})f_u/\pi f$）／平台。站台值：$6.30$ ps $=0.157$ UI →
  $84/1.19/0.84$ UI @ 100 kHz/1 MHz/10 MHz。
- SSC（$-0.5\%$、30 kHz、25 Gb/s）：$\Delta\phi_{pp}=\delta f_bT_m/8=521$ UI（12.5 GHz 時脈 260 週）；
  線性 type-II $f_n=1$ MHz 樣板殘餘 $\pm0.19$ UI、JTOL(30 kHz)$=936$ UI；一階環 28 UI、靜態誤差 19.9 UI ✗。
- 第 3 步的 bang-bang 迴路**只有比例路徑**時，30 kHz 的 slew 線只有 $259$ UI（單一判斷 $129.5$ UI）
  $\lt521$ UI ✗；加上積分路徑（$K_i=K_p/1024$）後換成加速度線 $1048$ UI ✓，等效於 $f_n\approx1$ MHz 的樣板
  ——$936$ UI 只有靠積分路徑才拿得到。模擬：$126$／$262$／$972$ UI。
- DLL/PI 沒有振盪器 → jitter 不累積（Maneatis 1996），但也不濾參考、不追頻——追頻靠積分路徑。

## 延伸閱讀

- CDR 黑盒子直覺與 UI/eye/BER：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- transfer vs tolerance、JTOL worked example 原出處：[pll_noise_budget](/06_design_insights/pll_noise_budget)
- 兩條轉移函數：[lab_13_pll_cdr_transfer](/04_simulation_labs/lab_13_pll_cdr_transfer)
- TJ@BER 與 DJ 記帳：[dj_dual_dirac](/06_design_insights/dj_dual_dirac)
- 累積 jitter $\kappa\sqrt{\Delta t}$（DLL 側欄的對照）：[lc_vs_ring](/06_design_insights/lc_vs_ring)
- 外部文獻（非本站 5 篇 PDF）：J. D. H. Alexander, "Clock Recovery from Random Binary Signals,"
  *Electron. Lett.*, vol. 11, no. 22, pp. 541–542, Oct. 1975；J. Lee, K. S. Kundert, and B. Razavi,
  "Analysis and Modeling of Bang-Bang Clock and Data Recovery Circuits," *IEEE J. Solid-State Circuits*,
  vol. 39, no. 9, pp. 1571–1580, Sep. 2004；R. C. Walker, "Designing Bang-Bang PLLs for Clock and Data
  Recovery in Serial Data Transmission Systems," in *Phase-Locking in High-Performance Systems*,
  B. Razavi, Ed., IEEE Press, 2003；J. G. Maneatis, *IEEE J. Solid-State Circuits*, vol. 31, no. 11,
  pp. 1723–1732, Nov. 1996；PCI Express Base Specification（SSC 30–33 kHz、$-0.5\%$ down-spread；版本待查）。
- 本頁的 Monte-Carlo 與時域模擬腳本：`simulations/lab_45_bb_cdr.py`（圖 `bb_cdr.png`）。
