---
title: "注入鎖定除頻（ILFD）：M:N 次諧波鎖定與設計"
description: "把 [P4] Eq.(28)–(30), p.2129 的 M:N 次諧波鎖定數學獨立成一頁教學：為何用注入鎖定除頻（ILFD）而非靜態除頻器、lock range ω_L=½I_inj|Γ̃_N| 如何由 ISF 第 N 諧波扛起、半波對稱 ISF 為何鎖不住 ÷2（payoff）、lab_37 的數值驗證、如何靠不對稱／單端拓樸與 tail 注入創造 c₂、除頻器（吃 ISF 諧波）與倍頻器（要吃注入諧波）的對偶，以及除頻輸出 −20log₁₀N 記帳如何與鎖定振盪器自身的雜訊整形銜接。"
---

import NumericQuiz from "@site/src/components/NumericQuiz";

# 注入鎖定除頻（ILFD）：M:N 次諧波鎖定與設計

> **先備**：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)（[P4] Eq.(28)–(30), p.2129 的完整逐步推導原始出處，本頁只做教學摘要與延伸）、[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（ISF 的 Fourier 係數與對稱性，本頁 payoff 的骨架）｜**接下來**：[subharmonic_injection](/06_design_insights/subharmonic_injection)（倍頻／次諧波注入的對偶篇）、[injection_locking_noise](/06_design_insights/injection_locking_noise)（鎖定振盪器的雜訊整形機制，本頁最後一節會借用它的框架）

> **這頁要回答什麼**：
> 1. 為什麼要用**注入鎖定除頻**（injection-locked frequency divider，ILFD），而不是數位除頻器？
> 2. ÷$N$ 的 lock range 公式怎麼來、由 ISF 的**哪一個諧波**決定？
> 3. 為什麼**差動、半波對稱**的振盪器天生鎖不住 ÷2？設計上怎麼繞過去？
> 4. 除頻輸出的相位雜訊要怎麼記帳——是乾淨的 $-20\log_{10}N$，還是別的東西？

> **物理直覺（先講結論）**：ILFD 不是「除法電路」，是一顆**本來就跑在 $f_0=f_{inj}/N$ 的振盪器**，
> 靠注入電流在每個振盪週期偷偷「拉」一下相位，把它鎖死在輸入的 $1/N$ 上。拉多用力，取決於振盪器
> 自己的 ISF 在**第 $N$ 諧波**上有多少內容——這正是本站 [P1] Eq.(12) 傅立葉展開第一次真正「被
> 拿來當設計旋鈕」的地方：**ISF 諧波不只決定雜訊怎麼折回載波，也決定除頻器鎖不鎖得住**。

---

## 為什麼用注入鎖定除頻，而不是靜態除頻器

高速本地振盪器鏈（例如 mm-wave PLL 前級除頻）常在兩條路線之間選：

1. **靜態數位除頻器**（CML latch、TSPC/D-flip-flop 鏈；[quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators)
   的 ÷2 一節已介紹過這條路）：每一級都要在輸入的**全速率**下正確 toggle，動態功耗量級隨輸入頻率
   上升，而且要求製程在該頻率下仍有足夠的開關裕度——輸入頻率越接近製程極限，功耗與可靠度代價
   越大。
2. **ILFD**（本頁主角）：本質上是一顆**自己跑在 $f_0$**（而非 $f_{inj}$）的振盪器，只需要一根遠比自身
   振幅小的注入電流「拉住」相位，不需要在 $f_{inj}$ 那麼高的速率下做邏輯翻轉——只需要在自己天生的
   $f_0$ 速率下振盪、以及讓注入路徑能耐受 $f_{inj}$（通常只是一個電容或小電晶體的窗口，不必整級
   toggle）。這讓 ILFD 在**輸入頻率逼近製程極限**時，通常比靜態除頻器省功耗、能推得更高——這是它
   在 mm-wave PLL 前級很受歡迎的原因。

> **誠實標註**：以上是類比／RF 電路設計的常識性權衡（**外部文獻，非本站 5 篇 PDF 的定量結果**）；
> [P4] 全篇沒有給出 ILFD vs. 靜態除頻器的功耗數字比較，這裡只提供定性理由。量化比較需查個別
> 製程／拓樸的論文（TODO：待查證）。本頁接下來要精讀的是 [P4] 給出的**嚴格數學**：ILFD 到底
> 鎖不鎖得住、鎖多寬。

---

## M:N 廣義平均方程：ISF 的第 $N$ 諧波怎麼被「電到」

[P3] 的廣義 Adler 方程只處理注入頻率 $\omega_{inj}\approx\omega_0$（基頻鎖定）。[P4] Sec. IV
（Eq.(28)–(30), p.2129，本站已對照原文核實，見 [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)
的完整逐步版本）把它推廣到**任意有理數頻率比**：鎖定時 $M\omega_{inj}=N\omega_{osc}$
（$M,N$ 為互質正整數）。**ILFD** 是 $M=1$ 的特例（輸出 $=\omega_{inj}/N$，除頻）；$N=1$ 則是
injection-locked frequency multiplier（乘頻）。以下把推導壓縮成三步，完整版請見 [paper_004]。

**第 1 步（重新定義相對相位，Eq.(28)）**：

$$
\varphi(t)\equiv\frac{M}{N}\,\omega_{inj}t+\theta(t)
$$

$\varphi$ 是振盪器總相位 [rad]、$\theta$ 是相對注入時鐘的慢變相位 [rad]。÷2 ILFD 取 $M=1,N=2$：
注入 $\omega_{inj}\approx2\omega_0$，振盪器跑在 $\omega_{inj}/2$。

**第 2 步（在 $NT_{inj}$ 窗上時間同步平均，Eq.(29)）**：

$$
\frac{d\theta}{dt}=\omega_0-\frac{M}{N}\omega_{inj}+\frac{1}{NT_{inj}}\int_{NT_{inj}}\tilde\Gamma\!\left(\frac{M}{N}\omega_{inj}t+\theta\right)i_{inj}(t)\,dt
$$

窗取 $NT_{inj}$（不是 $T_{inj}$）是因為：窗內注入波形走 $N$ 整圈，ISF 引數前進
$(M/N)\omega_{inj}\cdot NT_{inj}=2\pi M$、走 $M$ 整圈——兩者都是整數圈，平均才乾淨。

**第 3 步（逐項平均，只有共振諧波存活，得 Eq.(30)）**：取 $M=1$、正弦注入
$i_{inj}=I_{inj}\cos(\omega_{inj}t)$，把 $\tilde\Gamma$ 展成 phasor Fourier 級數
（對應 [P1] Eq.(12)：$\vert\tilde\Gamma_n\vert=c_n/q_{max}$，單位 rad/C）。逐項乘積化和差後，
**除了 $n=N$ 的差頻項**（頻率恰為 0），其餘每一項在 $NT_{inj}$ 窗上都走整數圈、平均精確歸零
——這是**恆等式**，不是「近似很小」（下面 lab_37 數值驗證到 $10^{-15}$）。存活的唯一一項：

$$
\Omega(\theta)=\frac{1}{2}\,I_{inj}\,\vert\tilde\Gamma_N\vert\cos\!\big(N\theta+\angle\tilde\Gamma_N\big)
$$

**讀法**：振盪器的 ISF 只有**第 $N$ 諧波** $\vert\tilde\Gamma_N\vert$ 對 $N$ 次超諧波注入有反應——
不是基波 $\vert\tilde\Gamma_1\vert$，也不是其他諧波。÷2 用 $\vert\tilde\Gamma_2\vert$（即 $c_2$）、
÷3 用 $\vert\tilde\Gamma_3\vert$（即 $c_3$）。

---

## Lock range：$\omega_L=\tfrac12 I_{inj}\vert\tilde\Gamma_N\vert$ —— ISF 第 $N$ 諧波扛起鎖定

鎖定 $\Leftrightarrow d\theta/dt=0$ 有穩定解 $\Leftrightarrow\vert\Delta\omega\vert\le\max_\theta\Omega(\theta)$
（$\Delta\omega\equiv\omega_{inj}/N-\omega_0$，輸出頻率軸）。[P4] p.2130 原文："which can be calculated
from (30) to be $\omega_L=I_{inj}\vert\tilde\Gamma_N\vert/2$"：

$$
\omega_L=\frac{1}{2}\,I_{inj}\,\vert\tilde\Gamma_N\vert=\frac{I_{inj}\,c_N}{2\,q_{max}}
$$

三個立刻可讀的物理（[P4] p.2129–2130，已核實）：

1. **除頻比 $N$ 不直接出現在公式裡**——它只決定「用哪一個諧波 $c_N$」；÷2、÷3 的 lock range 落在
   **同一條** $f_L\propto c_N$ 直線上（見下面 lab_37 圖 (b)）。
2. $\omega_L$ 以**輸出頻率軸**計；換到注入頻率軸，可鎖的 $\omega_{inj}$ 窗寬是 $2N\omega_L$。
3. $\Omega(\theta)$ 週期 $2\pi/N$ ⟹ 有 **$N$ 個相距 $2\pi/N$、彼此不可分辨的穩定鎖定相位**——
   ÷$N$ 輸出天生有 $N$ 個可能的相位起點（output phase ambiguity），做多相時鐘要另行處理。

> **例（÷2 ILFD：10 GHz 進、5 GHz 出，canonical 數值，重演自 [paper_004]）**：
> $f_0=5$ GHz、$q_{max}=1$ pC、$I_{inj}=0.5$ mA 正弦注入在 $f_{inj}\approx10$ GHz、$c_2=0.5$。
>
> 1. $\vert\tilde\Gamma_2\vert=c_2/q_{max}=0.5/10^{-12}=5\times10^{11}$ rad/C。
> 2. $\omega_L=\tfrac12 I_{inj}\vert\tilde\Gamma_2\vert=\tfrac12(5\times10^{-4}\,\text{A})(5\times10^{11}\,\text{rad/C})=1.25\times10^{8}$ rad/s。
> 3. $f_L=\omega_L/2\pi=19.9$ MHz（只有 $f_0$ 的 $0.40\%$）；注入頻率軸可鎖窗寬 $2Nf_L=79.6$ MHz。
> 4. dimension check：A $\times$ rad/C $=$ rad/s ✓。弱注入檢查：$I_{max}:=\omega_0 q_{max}=31.4$ mA
>    （[P4] footnote 11, p.2130），$I_{inj}/I_{max}=1.6\%$ ⟹ 一階線性模型適用。
>
> 一行 Python：`0.5*0.5e-3*0.5/1e-12` → $1.25\times10^{8}$。

<NumericQuiz
  prompt="先自己算：同一顆振盪器換成 ÷3（N=3, c_3=0.2, I_inj=0.5 mA, q_max=1 pC）。用 ω_L=I_inj·c_N/(2·q_max) 算半鎖定範圍 f_L（MHz，四捨五入到小數點後兩位）？"
  answer={7.96}
  tol={0.05}
  unit="MHz"
  hint="ω_L = I_inj·c_N/(2·q_max)；f_L = ω_L/(2π)。"
  solutionNote="ω_L = 0.5×(5×10⁻⁴ A)×(0.2/10⁻¹² C) = 5×10⁷ rad/s → f_L = 5×10⁷/(2π) ≈ 7.96 MHz（與 lab_37 的理論值、以及數值 sweep 的量測/理論比值 1.000 一致）。"
/>

---

## 半波對稱的 ISF 不能 ÷2（payoff）

回看 [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) 第 7 步的對稱表：
**半波對稱** $\Gamma(x+\pi)=-\Gamma(x)$ ⟹ 偶次諧波 $c_2=c_4=\dots=0$。代進
$\omega_L=I_{inj}c_2/(2q_{max})$：÷2 的 lock range **恆等於零**——一階內，$I_{inj}$ 加多大都沒用，
$2f_0$ 注入就是鎖不上。

這正是**同一張對稱表在兩個地方講反話**：在 phase-noise 那邊（[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)）
是好消息——$2\omega_0$ 附近的雜訊不折回載波；在 ILFD 這邊卻是壞消息——**對稱是雙面刃**。理想差動
LC VCO 的差動輸出節點正是這種情況（$c_2\approx0$）。設計上的出路是**換注入節點**：ISF 是「每個
注入節點各一條」的（同 [P1]），差動輸出對稱，但某些內部節點天生不對稱——下一節細講。

---

## 數值驗證：lab_37（未平均 ODE 掃頻 + 諧波地圖）

lab_37 用**未平均**的瞬時方程直接積分（若拿已平均的 Eq.(30) 驗證 Eq.(30) 就是循環論證）：

$$
\frac{d\theta}{dt}=\Big(\omega_0-\frac{\omega_{inj}}{N}\Big)+\tilde\Gamma\!\Big(\frac{\omega_{inj}}{N}t+\theta\Big)\,I_{inj}\cos(\omega_{inj}t)
$$

ISF 用 3 諧波 toy（**pedagogical toy，非 transistor-level**）：
$\tilde\Gamma(x)=-\big(c_1\sin x+c_2\sin2x+c_3\sin3x\big)/q_{max}$。

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

**如何解讀**（完整 script：`simulations/lab_37_ilfd_lock.py`，runtime ≈ 19 s；完整逐圖說明見
[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) 該節）：

- **(a)**：鎖定＝平均漂移率 0 的平台，平台半寬正好 $\omega_L$；紅色 $c_2=0$（半波對稱）的曲線是一條
  過原點的直線（漂移＝失諧）——**任何失諧都不鎖**，0/61 網格點鎖定。
- **(b)**：$N=2$ 與 $N=3$ 的量測點落在**同一條**理論直線 $f_L=I_{inj}c_N/(4\pi q_{max})$ 上（$N$
  只挑諧波、不進公式）。
- **(c)**：Eq.(29) 的平均積分逐 $\theta$ 數值算出，與 Eq.(30) 閉式重疊；$N=2$ 週期 $\pi$、$N=3$
  週期 $2\pi/3$，肉眼可見 $2\pi/N$ 簡併。

---

## 設計筆記：怎麼創造 $c_2$，讓 ÷2 鎖得住

「半波對稱不能 ÷2」不是判死刑，是**指出要換注入節點**。兩條路：

1. **打破半波對稱本身**：半波對稱 $\Gamma(x+\pi)=-\Gamma(x)$ 需要「上升半週期」與「下降半週期」在
   波形上互為鏡像的反相版本——**差動、推挽（push-pull）**節點天生滿足這個條件（兩個互補的
   switching 事件、極性相反、間隔半週期）。**單端（single-ended）**節點通常不滿足：一個週期裡
   往往只有**一次**主要的敏感事件（例如 [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)
   (c) 節推的 CMOS ring inverter stage：ISF 集中在單一個 transition 窗，不是兩個互為鏡像的窗），
   或者上升沿與下降沿的斜率、時機本來就不對稱（同一頁 (b) 節的 Colpitts）。這類拓樸的 ISF
   **不會**自動滿足 $\Gamma(x+\pi)=-\Gamma(x)$，$c_2$ 天生非零——這正是「不對稱／單端拓樸較容易
   ÷2」的機制來源。
2. **換到本來就不對稱的節點——tail injection at $2f_0$**：差動 LC VCO 的差動輸出對稱、$c_2\approx0$，
   但 [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies) (a) 節已經算出
   **tail 節點的有效 ISF** 富含 $c_2$：因為 switching pair 把 tail 電流「翻」兩次，tail 節點電壓
   本來就擺在 $2\omega_0$，$\Gamma_{tail}(\theta)=\tfrac{c_0}{2}+c_{1,res}\cos\theta+c_2\cos2\theta$
   在該頁的 illustrative 模型裡取 $c_2=0.55$——比 tank 的 $c_1=1,c_2=0$ 大得多的 $c_2$ 內容。
   [P4] 的 ÷2 實驗正是把 $2f_0$ 打進 differential LC 的 **tail**（Fig. 11(a)(b) caption、Fig. 12(d)，
   p.2130–2131，已核實）——與本站 [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)
   獨立算出的「tail 是 $c_2$ 的來源」完全對得上：那一頁講的是 tail **噪聲**經 $c_2$ 折回，這一頁講
   的是同一個 $c_2$ 也能拿來**主動注入鎖定**——一體兩面。

> **設計旋鈕摘要**：
> 1. 想要 $\div2$ 鎖得住 → 找一個**不受差動對稱保護**的節點注入（tail、單端輔助節點）。
> 2. 該節點若同時也是 $c_2$ 折回噪聲的來源（如 tail），代表你在「借用同一個弱點」——注入鎖定用它
>    幫忙除頻，但平常運轉時它也在把 $2\omega_0$ 噪聲折回；tail filter（見 [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)）
>    平常要濾掉的頻率，恰好就是你要打進去鎖定用的頻率——兩者要分時或分頻段設計，不能互相打架。
> 3. 單端拓樸（ring inverter、Colpitts）本來就有非零 $c_2$，做 ÷2 ILFD 相對省事，但要注意它們的
>    $\Gamma_{rms}$、$c_0$ 特性（[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)
>    (b)(c) 節）也一併帶進來，不是只挑 $c_2$ 那一項。

---

## 對偶：除頻靠 ISF 諧波，倍頻要靠注入諧波

[P4] Eq.(28) 的 $M:N$ 一般形式其實描述兩種鏡像關係，本站只完整核實、推導了 $M=1$（除頻）那一半；
把 $M,N$ 對調角色，就能看出對偶：

| | ÷$N$（ILFD，本頁，$M=1$） | ×$M$（injection-locked multiplier，$N=1$） |
|---|---|---|
| 鎖定條件 | $M=1\Rightarrow\omega_{osc}=\omega_{inj}/N$ | $N=1\Rightarrow\omega_{osc}=M\,\omega_{inj}$ |
| **誰要供出諧波** | **振盪器的 ISF** 供出第 $N$ 諧波 $\vert\tilde\Gamma_N\vert$；注入本身只需基頻 $\cos(\omega_{inj}t)$ | **注入波形**要供出自己的第 $M$ 諧波；ISF 只需基頻 $\vert\tilde\Gamma_1\vert$ |
| 落地方式 | 正弦電流直接注入即可（$N$ 次內容全部來自 ISF 的傅立葉展開） | 純正弦沒有 $M\ge2$ 次諧波，實務上得靠**振盪器內部混頻**自己產生——[P4] footnote 10, p.2129 明說這**不在** Eq.(28)–(30) 這套框架內（部分由其引文 [25] 處理） |
| lock range 公式 | $\omega_L=\tfrac12 I_{inj}\vert\tilde\Gamma_N\vert$（本頁 Eq.(30)，已核實） | 依賴內部混頻增益，沒有本頁這種封閉形式（超出本站已核實範圍） |

**一句話對偶**：**除頻器把工作外包給振盪器自己的頻譜內容（ISF 諧波）；倍頻器則需要注入訊號自己
先有高次諧波**——而「讓一個正弦波長出諧波」正是 [subharmonic_injection](/06_design_insights/subharmonic_injection)
要處理的問題（次諧波注入／倍頻器怎麼在實務中生出所需的 $M$ 次諧波驅動）。兩頁的公式骨架同一套
（[P4] Eq.(28)），差別只在「諧波內容住在哪一邊」。

---

## 雜訊記帳：除頻的 $-20\log_{10}N$ 與鎖定振盪器自身的雜訊整形

[clock_chain_budget](/06_design_insights/clock_chain_budget) 規則 2 嚴格推導了**理想 ÷$N$**
（edge-picking，除頻器只丟 edge、不搬 edge）的相位記帳：$\phi_{out}=\phi_{in}/N\Rightarrow
\mathcal{L}_{out}=\mathcal{L}_{in}-20\log_{10}N$。那一頁的「與 [P4] 的關係」欄位已經指出：
**÷$N$ 的相位記帳（$\phi/N$）對 ILFD 的載波路徑同樣成立**——原因就在本頁 Eq.(28)：$M=1$ 時
$\varphi(t)=\omega_{inj}t/N+\theta(t)$，$\theta$ 是鎖定範圍內有界的慢變量，所以**確定性的載波
頻率關係** $\omega_{out}=\omega_{inj}/N$ 本身就是精確的 $1/N$ 縮放——這與 clock_chain_budget
規則 2 的 $\phi_{out}=\phi_{in}/N$ 是同一件事，只是這裡的「除頻器」是一整顆被鎖定的振盪器，不是
邏輯閘。

但 ILFD **不是**單純的 edge-picking 機器，它是**鎖定振盪器**，所以還有 clock_chain_budget 那條
callout 誠實留白的部分：「ILFD 靠近 lock range 邊緣時有自己的雜訊行為」。這一半要接
[injection_locking_noise](/06_design_insights/injection_locking_noise) 的框架：那一頁對基頻鎖定
（$M=N=1$）證明了鎖定振盪器的自身雜訊被**高通**整形，corner 定義為
$\omega_c\equiv-\Omega'(\theta_{ss})$（lock characteristic 在穩定點的斜率）。把同一個定義套用到
本頁的 $M:N$ 版 $\Omega(\theta)=\tfrac12 I_{inj}\vert\tilde\Gamma_N\vert\cos(N\theta+\angle\tilde\Gamma_N)$：

$$
\Omega'(\theta)=-N\,\omega_L\sin\!\big(N\theta+\angle\tilde\Gamma_N\big)
\quad\Longrightarrow\quad
\omega_c=\big\vert\Omega'(\theta_{ss})\big\vert=N\,\omega_L\sqrt{1-\Big(\frac{\Delta\omega}{\omega_L}\Big)^{2}}=N\sqrt{\omega_L^2-\Delta\omega^2}
$$

（用了鎖定條件 $\cos(N\theta_{ss}+\angle\tilde\Gamma_N)=\Delta\omega/\omega_L$。dimension check：
$\omega_L$ 為 rad/s、$N$ 無因次 ⟹ $\omega_c$ 為 rad/s ✓。）**這個 $\omega_c$ 恰好就是 [P4]
Eq.(32) 已核實的 pull-in frequency $\omega_p=N\sqrt{\omega_L^2-\Delta\omega^2}$**——不是巧合，
是同一件事：injection_locking_noise 建立的「雜訊 corner＝lock characteristic 的恢復力」這條
一般原理，套進 M:N 版的 $\Omega(\theta)$，自動就得到論文自己核實過的暫態時間常數。

**把兩段接起來的設計圖像**：

- **偏移頻率 $\ll\omega_c$**（迴路頻寬內）：$\theta$ 緊跟著注入源動、載波路徑的 $\phi_{out}=\phi_{in}/N$
  記帳成立——輸出繼承的是**注入源（上游 $f_{inj}$ 時鐘）**的相位雜訊，量級上呼應
  clock_chain_budget 規則 2 的 $-20\log_{10}N$ 直覺（把「$-20\log_{10}N$」想成「載波確定性地
  被除以 $N$」，而不是「除頻器把雜訊主動壓低」）。
- **偏移頻率 $\gg\omega_c$**（迴路頻寬外）：$\theta$ 跟不上，ILFD **自己**的自由跑相位雜訊
  （它自己的 $\Gamma_{rms}/q_{max}$，[P1] Eq.(21) 的老公式）透過高通 $S_n/(\omega_c^2+\omega^2)$
  主導輸出——這時 $-20\log_{10}N$ 不適用，輸出雜訊由 ILFD 這顆振盪器本身的品質決定。
- 越靠近 lock range 邊緣（$\Delta\omega\to\omega_L$），$\omega_c\to0$，高通 corner 往低頻退、
  抑制頻寬萎縮——這與 clock_chain_budget 規則 4「divider 自身的床」是同一個誠實提醒：真實 ILFD
  一樣有自己的雜訊底，除頻之後**輸出不會好過 ILFD 自己在該偏移頻率的雜訊行為**。

---

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 弱注入 $I_{inj}\ll I_{max}=\omega_0 q_{max}$（[P4] footnote 11, p.2130） | 一階平均、$\omega_L$ 公式成立 | 強注入：需 APF 修正（Eq.(27) 分母）與振幅動態，一階公式失準 |
| $\omega_L\ll\omega_0$ | 平均（Eq.(29)）成立 | 失諧太大或平均窗內振盪器動態太快：平均失效 |
| $M=1$（本頁只做除頻方向） | Eq.(30) 的閉式成立 | $M\neq1$（倍頻）需注入訊號自己的第 $M$ 諧波，正弦注入沒有——[P4] footnote 10 明說不在框架內，見上方對偶表 |
| 「$c_2=0$ 不能 ÷2」 | 一階結論 | 更高階混頻仍可能留下極小殘餘 lock range（在 lab_37 偵測底線之下） |
| 雜訊記帳的高通/低通部分 | 標準注入鎖定雜訊理論（[injection_locking_noise](/06_design_insights/injection_locking_noise)） | **不在 5 篇 PDF 內**（Kurokawa 1973；[P4] p.2130 指向其參考文獻 [29, Ch. 7]）；本頁把 $\omega_c$ 的一般定義套用到 M:N 版，數值上與 [P4] 已核實的 Eq.(32) 吻合 |

## 重點回顧

- **ILFD 是被鎖定的振盪器，不是邏輯除頻器**：靠注入電流把相位鎖在 $\omega_{inj}/N$，不需要在
  $f_{inj}$ 全速率下切換邏輯，這是它在高頻前級省功耗的定性理由。
- **鎖定的數學**（[P4] Eq.(28)–(30), p.2129，已核實）：時間同步平均在 $NT_{inj}$ 窗上只留下 ISF
  的第 $N$ 諧波，得 $\Omega(\theta)=\tfrac12 I_{inj}\vert\tilde\Gamma_N\vert\cos(N\theta+\angle\tilde\Gamma_N)$，
  lock range $\omega_L=\tfrac12 I_{inj}\vert\tilde\Gamma_N\vert=I_{inj}c_N/(2q_{max})$——除頻比
  $N$ 只挑諧波，不進公式；$N$ 個相距 $2\pi/N$ 的鎖定相位彼此不可分辨。
- **Payoff**：半波對稱 $\Rightarrow c_2=c_4=\dots=0\Rightarrow$ ÷2/÷4 lock range 一階恆為零——
  差動輸出節點鎖不住 ÷2；出路是換到不對稱節點（tail、單端輔助節點）注入。
- **lab_37**：未平均 ODE 直接驗證平均恆等式到 $10^{-15}$、量測 lock range 與理論比值 1.00–1.03、
  $c_2=0$ 時 0/61 網格點鎖定、$2\pi/N$ 簡併肉眼可見。
- **設計上創造 $c_2$**：打破半波對稱（單端／不對稱拓樸天生非零 $c_2$）或換注入節點（差動 LC VCO
  的 tail 天生富含 $c_2$，與 tail 噪聲折回是同一個機制的兩面）。
- **對偶**：除頻（$M=1$）靠振盪器自己的 ISF 諧波；倍頻（$N=1$）要靠注入訊號自己的諧波——正弦
  注入沒有，需內部混頻，不在本框架內（見 [subharmonic_injection](/06_design_insights/subharmonic_injection)）。
- **雜訊**：載波路徑的 $\phi_{out}=\phi_{in}/N$ 記帳對 ILFD 成立（呼應 clock_chain_budget 規則 2
  的 $-20\log_{10}N$）；但迴路頻寬 $\omega_c=N\sqrt{\omega_L^2-\Delta\omega^2}$（恰為 [P4] Eq.(32)
  的 pull-in frequency）之外，輸出雜訊由 ILFD 自身的自由跑相位雜訊高通整形決定，不是單純的
  $-20\log_{10}N$。

## 延伸閱讀

- 完整逐步推導與實驗證據：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)
  （[P4] Eq.(28)–(30), p.2129；$\omega_L$ p.2130；暫態 Eq.(31)–(34), p.2130；實驗 Fig. 11–12, p.2130–2131）
- ISF 傅立葉展開與對稱性表（本頁 payoff 的骨架）：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- ÷2 產生 quadrature 的第一次登場、與靜態除頻器的對照：[quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators)
- 三種真實拓樸的 ISF 諧波（本頁「怎麼創造 $c_2$」的數字來源）：[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)
- ÷$N$ 相位記帳 $-20\log_{10}N$ 的嚴格出處：[clock_chain_budget](/06_design_insights/clock_chain_budget) 規則 2
- 鎖定振盪器自身雜訊的高通整形（本頁最後一節借用的框架）：[injection_locking_noise](/06_design_insights/injection_locking_noise)
- 對偶的另一半——次諧波注入／倍頻器：[subharmonic_injection](/06_design_insights/subharmonic_injection)
