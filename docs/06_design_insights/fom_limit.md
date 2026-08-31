---
title: FOM 的理論天花板
description: 從 [P1] Eq.(21) 與 [P2] Eq.(23) 推導「任何拓樸的 FOM 都可寫成 173.8 − 10log10(F_eff) dB（300 K）」；驗證參考常數 173.8 對應 1·kT（不是 2kT）、ring 天花板 168.3 dB、LC 天花板隨 Q 上升，並量化好的 LC 發表設計與 ring 各距天花板幾 dB。
---

import NumericQuiz from "@site/src/components/NumericQuiz";

# FOM 的理論天花板

> **先備**：[tank_swing](/06_design_insights/tank_swing)（FOM 定義與 phase-noise × power 取捨）、[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（[P1] Eq.(21) 與 factor-of-2 慣例）、[lc_vs_ring](/06_design_insights/lc_vs_ring)（[P2] Eq.(23) ring FOM、$-91$ dBc/Hz 例）｜**接下來**：[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)、[pll_noise_budget](/06_design_insights/pll_noise_budget)

這頁回答三個所有 VCO 設計者遲早會問的問題：

1. **FOM（figure of merit，振盪器品質指標）有沒有物理上限？** 上限是多少、由什麼決定？
2. 文獻上最好的 LC 設計 FOM 在 190 dB 上下——**它們離天花板還有幾 dB？**
3. **ring oscillator 為什麼天生落後 LC 約 25 dB？** 落後的每一 dB 是誰吃掉的？

> **物理直覺（先講結論）**：FOM 的構造刻意把 $(f_0/\Delta f)^2$ 與功率 $P$ **完全消掉**，
> 剩下的只有兩個東西：一個是**大自然的價目表** $kT$（1 Hz 頻寬內的熱雜訊能量 vs 1 mW），
> 在 300 K 折合 **173.8 dB**；另一個是**拓樸雜訊因子** $F_{eff}$——你的電路把 $kT$ 放大
> （ring：$F_{eff}\ge3.6$，天花板 168.3 dB）或用高 $Q$ 儲能把它**比下去**
> （LC：$F_{eff}\propto 1/Q^2$，天花板隨 $Q$ 每十倍升 20 dB）。
> 所以**沒有單一魔術數字**：天花板是一個「家族」，家族成員由你允許 $F_{eff}$ 裡放什麼物理決定。

## 第 0 步：FOM 的定義與正負號慣例

本頁採用**正值慣例**（越大越好，survey 表格最常見）：

$$
\mathrm{FOM}\;=\;-\mathcal{L}(\Delta f)\;+\;20\log_{10}\!\left(\frac{f_0}{\Delta f}\right)\;-\;10\log_{10}\!\left(\frac{P}{1\ \text{mW}}\right)\qquad[\text{dB}]
$$

- $\mathcal{L}(\Delta f)$：offset $\Delta f$ 處的 SSB phase noise，單位 dBc/Hz（負數，故 $-\mathcal{L}$ 為正）。
- $f_0$：載波頻率 [Hz]；$\Delta f$：offset 頻率 [Hz]；$P$：**總 DC 功耗** [W]，以 1 mW 歸一化。
- **與 [tank_swing](/06_design_insights/tank_swing) 的對照**：該頁寫的是
  $\mathrm{FOM}'=\mathcal{L}-20\log_{10}(f_0/\Delta f)+10\log_{10}(P/1\text{mW})$——**正負號相反的同一個量**
  （$\mathrm{FOM}=-\mathrm{FOM}'$，該慣例下越負越好）。兩種寫法文獻都有；本頁用正值慣例，
  數值上例如 ring 例的 $\mathrm{FOM}=165.0$ dB 就是該頁慣例的 $\mathrm{FOM}'=-165.0$ dB。
- **隱藏的參考單位**：$\mathcal{L}$ 的「per Hz」其實是「1 Hz 量測頻寬內的 sideband 功率 ÷ 載波功率」。
  把這個 $B_{ref}=1$ Hz 寫出來，FOM 的 log 引數才嚴格無因次；FOM 的完整參考基準是
  「**1 Hz 頻寬、1 mW 功率**」。下一步會看到這件事不是學究——它正好讓 $kT$ 乾淨現身。
- **Dimension check**：三項各是無因次比值的 $10\log_{10}$（$\mathcal{L}_{lin}B_{ref}$、$(f_0/\Delta f)^2$、$P/P_{ref}$）→ dB ✓。

## 第 1 步：參考常數——173.8 dB 是 $1\cdot kT$，不是 $2kT$

假設某拓樸在 $1/f^2$（白噪）區的 phase noise 可以整理成下面這個**萬用形**（下兩步會證明
ring 與 LC 都可以）：

$$
\mathcal{L}_{lin}(\Delta f)\;=\;F_{eff}\cdot\frac{kT}{P}\cdot\left(\frac{f_0}{\Delta f}\right)^2\qquad\left[\tfrac{1}{\text{Hz}}\right]
$$

其中 $F_{eff}$ 是無因次的**拓樸雜訊因子**（這條式子就是它的定義）。
**單位檢查**：$\dfrac{kT}{P}=\dfrac{[\text{J}]}{[\text{W}]}=[\text{s}]=\dfrac{1}{[\text{Hz}]}$，
乘無因次的 $F_{eff}(f_0/\Delta f)^2$ 後正是 $\mathcal{L}_{lin}$ 需要的 per-Hz ✓。代入 FOM 定義，逐步約分：

$$
\begin{aligned}
\mathrm{FOM}
&=-10\log_{10}\!\left(F_{eff}\,\frac{kT\,B_{ref}}{P}\Big(\frac{f_0}{\Delta f}\Big)^{2}\right)
 +10\log_{10}\!\left(\Big(\frac{f_0}{\Delta f}\Big)^{2}\right)
 -10\log_{10}\!\left(\frac{P}{P_{ref}}\right)\\[4pt]
&=-10\log_{10}\!\left(F_{eff}\cdot\frac{kT\,B_{ref}}{P}\cdot\frac{P}{P_{ref}}\right)
 \qquad\text{（兩個 }(f_0/\Delta f)^{2}\text{ 項相消）}\\[4pt]
&=\underbrace{-10\log_{10}\!\left(\frac{kT\,B_{ref}}{P_{ref}}\right)}_{\equiv\,C_{ref}(T)\text{，只跟溫度有關}}\;-\;10\log_{10}F_{eff}.
\end{aligned}
$$

- **每一步用到什麼**：第 1→2 行，$(f_0/\Delta f)^2$ 在 $-\mathcal{L}$ 與 $+20\log_{10}(f_0/\Delta f)$
  之間**精確相消**；第 2→3 行，$P$ 在 $kT/P$ 與 $P/P_{ref}$ 之間**精確相消**。
  這兩個相消**就是 FOM 被發明的目的**（把「$\mathcal{L}\times P\approx$ 常數」的取捨歸一化掉，
  見 [tank_swing](/06_design_insights/tank_swing) 第 4 步）。
- **Dimension check**：$\dfrac{kT\,B_{ref}}{P_{ref}}=\dfrac{[\text{J}][\text{Hz}]}{[\text{W}]}=\dfrac{[\text{W}]}{[\text{W}]}$ 無因次 ✓——
  第 0 步藏的 $B_{ref}=1$ Hz 在這裡剛好把 $kT$ 的量綱補齊。
- **物理意義**：$kT\cdot(1\ \text{Hz})$ 是 1 Hz 頻寬內電阻能交出的熱雜訊可用功率
  （$kT\approx4.14\times10^{-21}$ J @ 300 K）；$C_{ref}$ 就是「**1 mW 比熱雜訊地板大幾個 dB**」。

數值（$k=1.380649\times10^{-23}$ J/K，$T=300$ K）：$kT=4.142\times10^{-21}$ J，
$kT\cdot1\,\text{Hz}/1\,\text{mW}=4.142\times10^{-18}$，$C_{ref}=-10\log_{10}(4.142\times10^{-18})=173.83$ dB。

$$
\boxed{\;\mathrm{FOM}\;=\;173.8\ \text{dB}\;-\;10\log_{10}F_{eff}\qquad(T=300\ \text{K})\;}
$$

> ⚠️ **記憶陷阱（本站算過，別背錯）**：快速筆記常把這個常數寫成「$-10\log_{10}(2kT/1\text{mW})=173.8$」——
> **錯**。$2kT$ 配對的是 $170.8$ dB；$173.8$ dB 配對的是 $1\cdot kT$。
> **本頁的推導自然落在 $1\cdot kT$**：因為 [P2] Eq.(23) 印出來的就是 $kT/P$ 形式（第 2 步），
> 而 LC 的歸約（第 3 步）把所有 2 與 4 都收進 $F_{eff}$。**所有 factor-of-2 慣例
> （SSB 的 /4 vs 時域的 /2）都住在 $F_{eff}$ 裡、只挪動 FOM 共 3.01 dB；$C_{ref}$ 本身是無慣例的。**

```python
import numpy as np
kB, T = 1.380649e-23, 300.0
print(round(-10*np.log10(kB*T*1.0/1e-3), 2))   # -> 173.83
print(round(-10*np.log10(2*kB*T/1e-3), 2))     # -> 170.82 （2kT 的配對值，常被誤記成 173.8）
print(round(10*np.log10(kB*290.0/1e-3), 2))    # -> -173.98 （即 RF 圈著名的 -174 dBm/Hz 熱雜訊地板）
```

- 順帶收穫：$kT$ 用 $T_0=290$ K（IEEE 雜訊指數的參考溫度，源自 Friis 1944，**外部文獻，非本站 5 篇 PDF**，
  完整引用見頁尾）換算成 dBm/Hz 就是著名的 **$-174$ dBm/Hz**；300 K 給 $-173.83$，兩者都四捨五入成 $-174$。
- 溫度效應：$C_{ref}$ 每升溫 10 K 降約 $0.14$ dB（$C_{ref}(310\,\text{K})-C_{ref}(300\,\text{K})=-0.142$ dB）——
  比較不同溫度量的 FOM 時要記得這條斜率。

## 第 2 步：ring——[P2] Eq.(23) 一步歸約，天花板 168.3 dB

[P2] Eq.(23), p.796（已對照原始 PDF 核實，前置係數 $8/(3\eta)$）本身**已經是萬用形**：

$$
\mathcal{L}_{lin}\{\Delta f\}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{V_{char}}\cdot\left(\frac{f_0}{\Delta f}\right)^{2}
\;\;\Longrightarrow\;\;
F_{eff}^{ring}=\frac{8}{3\eta}\cdot\frac{V_{DD}}{V_{char}}
$$

- $\eta$：級延遲比例常數（[P2] Eq.(14)，$\approx1$，無因次）；$V_{DD}$：supply 電壓 [V]；
  $V_{char}=\Delta V/\gamma$：device 的特徵電壓 [V]（$\Delta V$ = gate overdrive [V]、$\gamma$ = 通道熱雜訊係數，無因次）。
- **單位檢查**：$F_{eff}^{ring}$ 是（無因次）×（V/V）= 無因次 ✓；整條 $\mathcal{L}_{lin}$ 的單位由 $kT/P=[\text{s}]$ 提供 per-Hz ✓。
- **為什麼 $P$ 會自然出現**：[P2] Eq.(21) 給 $P=2\eta N V_{DD}q_{max}f_0$——功率把 $N$、$q_{max}$、$f_0$
  全部吸收，這正是 [lc_vs_ring](/06_design_insights/lc_vs_ring) 講的 **N-independence** 在 FOM 語言下的樣子。

**天花板**：$V_{char}=\Delta V/\gamma$，而 overdrive 受 supply 限制 $\Delta V\le V_{DD}/2$（$V_T=0$ 時取等號），所以

$$
\frac{V_{DD}}{V_{char}}=\gamma\,\frac{V_{DD}}{\Delta V}\;\ge\;2\gamma
\;\;\Longrightarrow\;\;
F_{eff}^{ring}\;\ge\;\frac{16\gamma}{3\eta}
$$

這就是 [P2] Eq.(25), p.796 的下限。取長通道 $\gamma=2/3$、$\eta=1$：$F_{eff,min}^{ring}=32/9=3.556$，
$10\log_{10}(3.556)=5.51$ dB，

$$
\mathrm{FOM}_{max}^{ring}=173.83-5.51=168.32\ \text{dB}\quad(300\ \text{K})
$$

**本站 ring worked example 的驗證**（[lc_vs_ring](/06_design_insights/lc_vs_ring) 例 1：
$\mathcal{L}=-91.0$ dBc/Hz @ 1 MHz、$f_0=5$ GHz、$P=1$ mW、$V_{DD}/V_{char}=3$）：

$$
\mathrm{FOM}=91.0+20\log_{10}(5000)-0=91.0+73.98=165.0\ \text{dB}
$$

```python
import numpy as np
kB, f0, df = 1.380649e-23, 5e9, 1e6
Cref = -10*np.log10(kB*300/1e-3)
Feff_ring = 8/3 * 3                              # [P2] Eq.(23)：(8/(3η))·(V_DD/V_char)，η=1、V_DD/V_char=3
print(round(Cref - 10*np.log10(Feff_ring), 2))   # -> 164.8 （F_eff 路徑，kT 用 300 K 精確值）
print(round(91.0 + 20*np.log10(f0/df) - 0.0, 2)) # -> 164.98 （直接由該頁 -91.0 dBc/Hz、P=1 mW）
Feff_min = 16*(2/3)/3                            # [P2] Eq.(25)：V_T=0 下限，γ=2/3
print(round(Cref - 10*np.log10(Feff_min), 2))    # -> 168.32 （ring 天花板）
```

- **兩條路差 0.2 dB 的來源（誠實記帳）**：$F_{eff}$ 路徑用精確 $kT(300\,\text{K})=4.142\times10^{-21}$ J
  得 $164.80$；[lc_vs_ring](/06_design_insights/lc_vs_ring) 的鏈用了四捨五入的 $kT=4.0\times10^{-21}$ J
  （那其實是 $290$ K 的值）得 $\mathcal{L}=-91.0$、$\mathrm{FOM}=165.0$。兩者在 $kT$ 取值一致時**逐位相等**
  （`simulations/fig_fom_limit.py` 印出 identity check $=0.00$）。本頁引用時一律寫「$\approx165$ dB」。
- 這個例子離 ring 天花板只有 $168.32-164.80=3.52$ dB（正好是 $V_{DD}/V_{char}=3$ vs 下限 $2\gamma=4/3$
  的比值 $2.25\to3.52$ dB）——**ring 的萬用形幾乎沒有揮灑空間**，這是重點。
- **適用/失效**：single-ended CMOS inverter ring、白噪、long-channel $\gamma=2/3$。短通道 $\gamma$ 更大
  → 天花板**更低**（$\gamma=1$ 時 $16\gamma/3=5.33\to166.6$ dB）；flicker、supply/substrate 耦合都只會再往下扣。

## 第 3 步：LC——從 [P1] Eq.(21) 推 $F_{eff}=\dfrac{F\,\Gamma_{rms}^2}{2Q^2\,\eta_P}$

LC 沒有現成的 $kT/P$ 形式，要自己走。從 [P1] Eq.(21), p.185（SSB、分母 $4\Delta\omega^2$ 慣例）出發：

$$
\mathcal{L}_{lin}\{\Delta\omega\}=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}
$$

引入四條標準電路關係（每條先檢查單位）：

1. **雜訊源**：tank 損耗電阻 $R_p$ 的熱雜訊 $\overline{i_n^2}/\Delta f=4kT/R_p$
   （$[\text{J}]/[\Omega]=[\text{A}^2\text{s}]=[\text{A}^2/\text{Hz}]$ ✓；見
   [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)）。
   多個雜訊源時定義**噪聲因子** $F$（無因次）：把所有源經各自 $\Gamma_{eff}$ 加權後折算回 tank 源，
   $\overline{i_n^2}/\Delta f\big|_{tot}=F\cdot4kT/R_p$，$F\ge1$（tank 自己就貢獻 1）。
   理想 class-B cross-coupled（tail 理想濾波）$F=1+\gamma$——此值為**外部文獻**標準結果
   （Hegazi–Sjöland–Abidi 2001；Andreani et al. 2005，完整引用見頁尾），非 5 篇 PDF 內。
2. **電荷擺幅**：$q_{max}=C\,V_{max}$（$[\text{F}][\text{V}]=[\text{C}]$ ✓，[P1] 定義）。
3. **功率**：正弦擺幅 $V_{max}$ 打在 $R_p$ 上的平均耗散 $P_{tank}=V_{max}^2/(2R_p)$
   （$[\text{V}^2/\Omega]=[\text{W}]$ ✓）；總 DC 功耗 $P_{DC}=P_{tank}/\eta_P$，
   $\eta_P\le1$ 為功率效率（無因次）。
4. **品質因數**：並聯 RLC 的 $Q=\omega_0 R_p C$（$[\text{s}^{-1}][\Omega][\text{F}]$，
   $\Omega\cdot\text{F}=\text{s}$ → 無因次 ✓）。

逐步代入（不跳步）：

$$
\begin{aligned}
\mathcal{L}_{lin}
&=\frac{\Gamma_{rms}^2}{(CV_{max})^2}\cdot\frac{F\cdot4kT/R_p}{4\Delta\omega^2}
 =\frac{F\,\Gamma_{rms}^2\,kT}{R_p\,C^2V_{max}^2\,\Delta\omega^2}
 &&\text{（代 1、2，約掉 }4\text{）}\\[4pt]
&=\frac{F\,\Gamma_{rms}^2\,kT}{R_p\,C^2\cdot 2P_{tank}R_p\cdot\Delta\omega^2}
 =\frac{F\,\Gamma_{rms}^2\,kT}{2P_{tank}\,(R_pC)^2\,\Delta\omega^2}
 &&\text{（代 3：}V_{max}^2=2P_{tank}R_p\text{）}\\[4pt]
&=\frac{F\,\Gamma_{rms}^2}{2Q^2}\cdot\frac{kT}{P_{tank}}\cdot\left(\frac{\omega_0}{\Delta\omega}\right)^{2}
 &&\text{（代 4：}R_pC=Q/\omega_0\text{）}
\end{aligned}
$$

$\omega_0/\Delta\omega=f_0/\Delta f$（$2\pi$ 上下相消），再把 $P_{tank}=\eta_P P_{DC}$ 換成總功耗，得萬用形與

$$
\boxed{\;F_{eff}^{LC}=\frac{F\,\Gamma_{rms}^2}{2\,Q^2\,\eta_P}\;}
$$

- **Dimension check（整條）**：$F_{eff}^{LC}$ 全由無因次量組成 ✓；$kT/P_{tank}=[\text{s}]$ 給 per-Hz ✓。
- **物理意義（本頁最重要的一句話）**：分母的 $Q^2$ 說明 LC 憑什麼打穿 173.8 dB「參考線」——
  諧振腔把訊號能量**無雜訊地儲存**起來，每瓦損耗只有 $R_p$ 一份 $kT$ 雜訊進帳；$Q$ 越高，
  「儲存的訊號 ÷ 買進的雜訊」越大，$F_{eff}\lt1$ 完全合法。**參考線不是 LC 的天花板；
  LC 的天花板由製程能給的 $Q$ 決定**（片上 spiral 電感在 GHz 頻段典型 $Q\approx8\sim15$）。
- **失效條件**：swing 大到波形失真（$\Gamma_{rms}$、$F$ 改變）、voltage-limited 後 $\eta_P$ 崩落、
  varactor/開關的損耗吃掉 $Q$、flicker 主導的 offset（萬用形只涵蓋 $1/f^2$ 區）。

**數值一致性驗證（把 canonical 例 B 反向工程成一顆 tank）**：例 B（$\Gamma_{rms}=0.5$、$q_{max}=1$ pC、
$S_i=10^{-24}$ A²/Hz、$f_0=5$ GHz → $\mathcal{L}=-148.0$ dBc/Hz @ 1 MHz）若把 $S_i$ 解讀成單一 tank 源、
假設 $V_{max}=1$ V，則 $R_p=4kT/S_i=16.6$ kΩ、$C=1$ pF、$Q=\omega_0R_pC=520.5$、$P_{tank}=30.2$ µW——
兩條路（Eq.(21) 直接算 vs $F_{eff}$ 萬用形）必須給同一個 $\mathcal{L}$：

```python
import numpy as np
kB, T, f0, df = 1.380649e-23, 300.0, 5e9, 1e6
grms, qmax, Si = 0.5, 1e-12, 1e-24
dw = 2*np.pi*df
L_direct = 10*np.log10(grms**2/qmax**2 * Si/(4*dw**2))    # [P1] Eq.(21)
Rp = 4*kB*T/Si; C = qmax/1.0; Q = 2*np.pi*f0*Rp*C; Pt = 1.0**2/(2*Rp)
Feff = 1.0*grms**2/(2*Q**2)                               # F=1、η_P=1
L_feff = 10*np.log10(Feff*(kB*T/Pt)*(f0/df)**2)
print(round(L_direct, 2), round(L_feff, 2))    # -> -148.0 -148.0 （兩條路逐位一致：代數鏈正確）
print(round(Q, 1), round(Pt*1e6, 2))           # -> 520.5 30.18 （Q≈520：晶片上不存在這種 tank）
FOM = -L_direct + 20*np.log10(f0/df) - 10*np.log10(Pt/1e-3)
print(round(FOM, 1))                           # -> 237.2
```

- **教學點（FOM 會抓包）**：例 B 的 $-148$ dBc/Hz 本身沒問題，但換算成 FOM 高達 **237 dB**，
  等價於 $Q\approx520$ 的 tank——立刻暴露「$S_i=10^{-24}$ A²/Hz 配 1 pC」是**刻意理想化的單源教學參數**，
  不是可實作的設計點。dBc/Hz 會騙人（沒講功率），FOM 不會。

## 第 4 步：天花板是「家族」，不是一個數字

把三步合起來：**任何**拓樸只要白噪區能寫成萬用形，就有

$$
\mathrm{FOM}=173.8\ \text{dB}-10\log_{10}F_{eff}\qquad(300\ \text{K})
$$

這是**恆等式**（$F_{eff}$ 的定義使然）；「天花板」的內容全看你允許 $F_{eff}$ 裡放什麼物理：

| 家族成員 | $F_{eff}$ | $10\log_{10}F_{eff}$ | $\mathrm{FOM}_{max}$（300 K） | 來源／假設 |
|---|---|---|---|---|
| 參考線（$F_{eff}=1$） | $1$ | $0$ dB | $173.8$ dB | 定義；「sideband 密度 = 熱雜訊地板」 |
| ring 天花板 | $16\gamma/(3\eta)=3.56$ | $+5.5$ dB | $168.3$ dB | [P2] Eq.(25)：$V_T=0$、$\gamma=2/3$、$\eta=1$、白噪 |
| 本站 ring 例 | $8$ | $+9.0$ dB | $164.8$（$\approx165.0$）dB | [P2] Eq.(23)：$V_{DD}/V_{char}=3$；= $-91$ dBc/Hz 例 |
| LC 理想、$Q=10$ | $4.17\times10^{-3}$ | $-23.8$ dB | $197.6$ dB | [P1] Eq.(21)（SSB /4）＋$F=1+\gamma$、$\Gamma_{rms}^2=\tfrac12$、$\eta_P=1$ |
| 同上、時域 /2 慣例 | $8.33\times10^{-3}$ | $-20.8$ dB | $194.6$ dB | 同一物理、Leeson $2FkT$ 記帳（低 3.01 dB） |
| LC 理想、$Q=20$ | $1.04\times10^{-3}$ | $-29.8$ dB | $203.7$ dB | 同上（/4 慣例） |

```python
import numpy as np
Cref = -10*np.log10(1.380649e-23*300/1e-3)
gamma = 2/3
def fom_lc_ceiling(Q, F=1+gamma, grms2=0.5, eta_p=1.0):
    return Cref - 10*np.log10(F*grms2/(2*Q**2*eta_p))
print(round(fom_lc_ceiling(10), 2))                   # -> 197.63 （[P1] Eq.(21) SSB /4 慣例）
print(round(fom_lc_ceiling(10) - 10*np.log10(2), 2))  # -> 194.62 （時域 /2 慣例；同物理，低 3.01 dB）
print(round(fom_lc_ceiling(20), 2))                   # -> 203.65
```

<NumericQuiz
  prompt="先自己算：理想 LC、Q=20、F=1+γ（γ=2/3）、Γ_rms²=0.5、η_P=1 時的天花板 FOM_max = ？（300 K，[P1] /4 慣例；以 dB 作答）"
  answer={203.65}
  tol={0.01}
  unit="dB"
  hint="FOM_max = C_ref − 10log₁₀(F·Γ_rms²/(2Q²·η_P))，C_ref=173.83 dB。"
  solutionNote="F=5/3、Γ_rms²=0.5、Q=20 → 括號內 = (5/3×0.5)/(2×400) ≈ 1.042×10⁻³ → FOM_max ≈ 173.83+29.82 ≈ 203.65 dB。"
/>

> **Factor-of-2 紀律（哪個 2、哪個慣例）**：本站在
> [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 記錄過：同一組例 B 參數，
> [P1] Eq.(21) 的 SSB「/4」給 $-148.0$ dBc/Hz，時域乾淨推導的「/2」給 $-145.0$ dBc/Hz。
> 在 FOM 語言裡這顆 2 **整顆搬進 $F_{eff}$**：/2 慣例的 $F_{eff}$ 是 /4 慣例的兩倍、FOM 低
> $10\log_{10}2=3.01$ dB（上表兩列）。Leeson 的 $2FkT/P_s$ 形（見
> [derivation_leeson](/99_appendix/derivation_leeson)）化簡成 $F_{eff}=F/(2Q^2)$，屬 /2 那一族——
> 與本頁 [P1] 推導的 $F\Gamma_{rms}^2/(2Q^2)=F/(4Q^2)$（$\Gamma_{rms}^2=\tfrac12$）正好差這顆 2 ✓。
> **量測的 FOM 沒有這個問題**（儀器量到什麼就是什麼）；這 3 dB 只影響「理論天花板」的標定，
> 所以上表把兩種慣例都列出來。
> 另注意 $\Gamma_{rms}^2=\tfrac12$ 是 true-LC（$\Gamma=-\sin\theta$）的**代表值**而非硬下限——
> 波形工程（class-F 等）動的正是這一項與 $F$、$\eta_P$。

![FOM 天花板家族：(a) 各 F_eff 對溫度的天花板線；(b) 300 K 下 LC 天花板 vs Q、ring 天花板與參考線](/figures/fom_limit.png)

- **script**：`simulations/fig_fom_limit.py`（跑法 `PYTHONPATH=. python3 simulations/fig_fom_limit.py`，
  會把本頁全部關鍵數字印出來並存圖）。
- **參數**：$k=1.380649\times10^{-23}$ J/K；ring：$\eta=1$、$\gamma=2/3$、$V_{DD}/V_{char}\in\{2\gamma,3\}$；
  LC：$F=1+\gamma$、$\Gamma_{rms}^2=\tfrac12$、$\eta_P=1$、$Q\in[2,100]$。
- **如何解讀**：(a) 每條線是一個 $F_{eff}$ 的天花板對溫度 $T$ 的走勢（斜率 $\approx-0.14$ dB/10 K）；
  (b) 綠線是 LC 理想天花板 vs $Q$（實線 /4、虛線 /2 慣例），水平線由上而下是參考線 173.8、
  ring 天花板 168.3、本站 ring 例 164.8。**圖上刻意不放發表設計散點**——本站 5 篇 PDF 內沒有
  可核實的 per-design FOM 數據，畫線不畫點是誠實的做法（紫點與綠方塊是本頁自己算的例子）。

## 距離天花板還有幾 dB？

- **好的發表 LC 設計**：survey 表格常見的優秀值在 $188\sim195$ dB（量級敘述；對應
  $F_{eff}\approx0.008\sim0.03$，可由本頁 bound family 反推，如下面例 2 的 $189$ dB → $Q\approx5.7$
  等效點）。對照它們自己的 $Q$ 天花板（$Q=10\sim15$ → $197.6\sim201.2$ dB，/4 慣例），
  **典型距離約 $5\sim10$ dB**——被 $\eta_P\lt1$、tail 與 bias 雜訊（$F\gt1+\gamma$）、
  varactor/開關損耗（有效 $Q$ 下降）、佈局寄生分掉。換句話說：**LC 這題已經被解到離物理極限
  一隻手掌的距離**，剩下的 dB 一顆比一顆貴。
- **Colpitts vs LC-tank（Andreani et al., JSSC 2005；外部文獻，非本站 5 篇 PDF，完整引用見頁尾）**：
  該文對 CMOS Colpitts 與 differential LC-tank 給出封閉式雜訊因子並用實作驗證，著名結論是
  **CMOS 下 LC-tank 的 phase-noise 表現至少與 Colpitts 一樣好**——Colpitts 的 cyclostationary
  優勢（電流脈衝對準 ISF 波谷；本站
  [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies) 例 2 估約 7 dB 的
  $\Gamma_{eff,rms}^2$ 壓低）被其偏壓效率與起振裕度的代價抵銷。兩種拓樸都在**同一條 LC 天花板家族**下
  （都含 $1+\gamma$ 一族的 $F$ 與 $1/Q^2$），沒有誰能繞過 $Q$ 這道牆。
- **ring**：本站例距 ring 天花板僅 $3.5$ dB——ring 的萬用形裡**沒有 $Q$ 可以買**，
  天花板本身（168.3 dB）就比 LC 的低了約 30 dB。

**ring 落後 LC 的 dB 記帳**（拿本站 ring 例 164.8 dB 對 LC $Q=10$ 理想天花板 197.63 dB，
差 $32.83$ dB，`fig_fom_limit.py` 驗證分解逐項相加**精確等於**總差）：

| 項目 | 比值 | dB | 物理 |
|---|---|---|---|
| 無儲能 vs $2Q^2$（$Q=10$） | $200$ | $23.0$ | LC 的高 $Q$ 儲能把 $kT$ 比下去；ring 每週期把能量全數丟掉重充 |
| $V_{DD}/V_{char}=3$ | $3$ | $4.8$ | overdrive／headroom：$V_{char}$ 越小雜訊放大越多 |
| 前置係數 $8/3$ | $8/3$ | $4.3$ | ring 波形／transition 記帳（[P2] Eq.(23) 的 $8/(3\eta)$） |
| LC 波形項 $(1+\gamma)\Gamma_{rms}^2$ | $5/6$ | $0.8$ | LC 自己的 $F$ 與 $-\sin$ ISF 只收回一點點 |
| **合計** | $1920$ | $32.8$ | $=197.63-164.80$ ✓ |

實際發表的 LC 沒拿滿理想天花板（還掉 $5\sim10$ dB），所以**實務上觀察到的差距約 25 dB**
——與「好的 LC $\approx190$、好的 ring $\approx165$」互相印證。結論：ring 落後**不是設計不努力**，
是 $Q$（23 dB 那一項）加上 $V_{char}$／波形（約 9 dB）的結構性差距；ring 的買點在面積、調諧範圍、
多相位（見 [lc_vs_ring](/06_design_insights/lc_vs_ring)）。

## Worked examples 數值例題

> **例 1（把本站 ring 例換算成 FOM，並對天花板定位）**
> 給定 [lc_vs_ring](/06_design_insights/lc_vs_ring) 例 1：$\mathcal{L}=-91.0$ dBc/Hz @ $\Delta f=1$ MHz、
> $f_0=5$ GHz、$P=1$ mW。求 FOM 與距 ring 天花板的距離。

**逐步代入（帶單位）**：

$$
\begin{aligned}
20\log_{10}\!\left(\frac{f_0}{\Delta f}\right)&=20\log_{10}\!\left(\frac{5\times10^9\ \text{Hz}}{10^6\ \text{Hz}}\right)=20\log_{10}(5000)=73.98\ \text{dB},\\[4pt]
10\log_{10}\!\left(\frac{P}{1\ \text{mW}}\right)&=10\log_{10}(1)=0\ \text{dB},\\[4pt]
\mathrm{FOM}&=-(-91.0)+73.98-0=164.98\approx165.0\ \text{dB}.
\end{aligned}
$$

- **結果**：$\mathrm{FOM}\approx165$ dB；距 ring 天花板 $168.3$ dB 約 $3.5$ dB
  （全部來自 $V_{DD}/V_{char}=3$ vs 下限 $2\gamma=4/3$），距參考線 $173.8$ dB 為 $9.0$ dB（$F_{eff}=8$）。
- **Dimension check**：三項皆無因次比值的 log → dB ✓（$f_0/\Delta f$：Hz/Hz；$P/1$ mW：W/W）。
- **一行 Python 驗證**：

```python
import numpy as np
print(round(91.0 + 20*np.log10(5e9/1e6) - 10*np.log10(1e-3/1e-3), 2))   # -> 164.98
```

> **例 2（設計反推：從量測 FOM 讀出「等效 $Q$」）**
> 一顆 $f_0=5$ GHz 的 LC VCO 燒 $P=10$ mW，量到 $\mathcal{L}(1\ \text{MHz})=-125$ dBc/Hz。
> 求 FOM、隱含的 $F_{eff}$，以及在 $F=2$、$\Gamma_{rms}^2=\tfrac12$、$\eta_P=0.5$（實際一點的損耗假設）下
> 隱含的 tank $Q$。

**逐步代入（帶單位）**：

$$
\begin{aligned}
\mathrm{FOM}&=125+20\log_{10}(5000)-10\log_{10}(10)=125+73.98-10=188.98\ \text{dB},\\[4pt]
F_{eff}&=10^{(C_{ref}-\mathrm{FOM})/10}=10^{(173.83-188.98)/10}=10^{-1.515}=0.0305,\\[4pt]
Q&=\sqrt{\frac{F\,\Gamma_{rms}^2}{2\,F_{eff}\,\eta_P}}
  =\sqrt{\frac{2\times0.5}{2\times0.0305\times0.5}}=\sqrt{32.7}=5.72 .
\end{aligned}
$$

- **結果**：$\mathrm{FOM}=189.0$ dB——「好設計」量級；隱含 $Q\approx5.7$，片上完全合理。
  若製程能給 $Q=10$（理想天花板 $197.6$ dB，/4 慣例），這顆設計離自己的天花板約 $8.7$ dB
  ——下一步該查的是 $\eta_P$（class 效率）、tail 雜訊（$F$）與 varactor 損耗，而不是再堆電流。
- **Dimension check**：$F_{eff}$ 無因次（dB 差 ÷10 後取冪）✓；根號內全無因次 → $Q$ 無因次 ✓。
- **一行 Python 驗證**：

```python
import numpy as np
Cref = -10*np.log10(1.380649e-23*300/1e-3)
FOM = 125.0 + 20*np.log10(5e9/1e6) - 10*np.log10(10e-3/1e-3)
print(round(FOM, 2))                           # -> 188.98
Feff = 10**((Cref - FOM)/10)
print(round(Feff, 4))                          # -> 0.0305
print(round(np.sqrt(2*0.5/(2*Feff*0.5)), 2))   # -> 5.72 （隱含 Q；F=2、Γrms²=0.5、η_P=0.5）
```

## design knobs：什麼動得了 FOM、什麼動不了

| Knob | 動哪一項 | 效果 | 註記 |
|---|---|---|---|
| 提高 tank $Q$ | $F_{eff}^{LC}\propto1/Q^2$ | $+20$ dB／$Q$ 每十倍（$Q$ 加倍 $+6$ dB） | **唯一的大槓桿**；受製程電感/varactor 限制 |
| 提高功率效率 $\eta_P$（class-B→C/D/F） | $1/\eta_P$ | 最多幾 dB | swing 波形與導通角工程 |
| 壓 $F$（tail filter、對稱、bias 乾淨） | $F\to1+\gamma$ | 幾 dB | Hegazi 2001（外部文獻）一族的技巧 |
| 波形／ISF 工程 | $\Gamma_{rms}^2$ | $1\sim2$ dB 量級 | class-F、諧波整形 |
| **加功率 $P$** | — | **0 dB** | FOM 對 $P$ 已歸一化；只降 $\mathcal{L}$ 不升 FOM |
| **ring 加級數 $N$** | — | **0 dB** | [P2] N-independence；$N$ 不在 Eq.(23) 裡 |
| 降溫 | $C_{ref}(T)$ | $+0.14$ dB／$-10$ K | 通常不是你能選的 |
| ring 的 $V_{DD}/V_{char}$ | $F_{eff}^{ring}$ | 至多到 $2\gamma$ 下限（差 $\sim3.5$ dB） | 之後就撞 [P2] Eq.(25) 天花板 |

## 與 SerDes 的關聯

FOM 天花板直接換算成「**一個功率預算內買得到的最低 jitter**」。例 C
（[lab_08](/04_simulation_labs/lab_08_jitter_integration)：$f_0=5$ GHz、$-100$ dBc/Hz @ 1 MHz、
$1/f^2$、積分 1–100 MHz）給 $\sigma_t=447.9$ fs；同法之下 $\sigma_t\propto10^{\Delta\mathcal{L}/20}$，
所以 1 mW 的 165-dB-FOM ring（$-91$ dBc/Hz，比例 C 高 9 dB）給：

```python
print(round(447.9 * 10**((100.0-91.0)/20), 1))   # -> 1262.4 （fs；同積分帶寬、1/f² 斜率的縮放）
```

約 $1.26$ ps rms——對 $\ge56$ Gb/s 的 SerDes UI 是不可用的量級，這就是為什麼高速 SerDes 的
LC-PLL＋（必要時）ring 只敢放在 PLL 帶寬內被抑制的位置
（見 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)、
[pll_noise_budget](/06_design_insights/pll_noise_budget)）。

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| offset 落在 $1/f^2$ 白噪區 | 萬用形與 $\mathrm{FOM}=173.8-10\log_{10}F_{eff}$ 成立 | $1/f^3$ 區（flicker）或 floor 區：FOM 隨 $\Delta f$ 改變，比較無意義 |
| $P$ = 總 DC 功耗 | 跨設計公平比較 | 只報 core 功耗（漏掉 buffer/bias）會虛胖 FOM |
| $T=300$ K | 常數 $173.83$ dB | 其他溫度用 $C_{ref}(T)$（$-0.14$ dB/10 K） |
| 理論值標明 /2 或 /4 慣例 | 天花板可互相對表（差 $3.01$ dB） | 混用慣例會生出幽靈 3 dB |
| 小擾動 LTV（[P1] 框架） | $F_{eff}$ 是常數 | 大注入、injection pulling（見 [P3]/[P4] 頁）另議 |
| 只看 FOM | 功率—雜訊取捨歸一化 | 面積、調諧範圍（FOM$_T$ 變體另計）、supply pushing、良率都不在裡面 |

## 重點回顧

- $\mathrm{FOM}=-\mathcal{L}+20\log_{10}(f_0/\Delta f)-10\log_{10}(P/1\text{mW})$（本頁正值慣例；
  [tank_swing](/06_design_insights/tank_swing) 用其負值）。構造上 $(f_0/\Delta f)^2$ 與 $P$ 精確相消。
- **萬用歸約**：$\mathcal{L}_{lin}=F_{eff}(kT/P)(f_0/\Delta f)^2\Rightarrow\mathrm{FOM}=173.8-10\log_{10}F_{eff}$
  dB（300 K）。常數 $173.83=-10\log_{10}(kT\cdot1\text{Hz}/1\text{mW})$ 配 **1·kT**（$2kT$ 配 $170.8$，別背錯）；
  一切 factor-of-2 慣例都住在 $F_{eff}$（/2 vs /4 = 3.01 dB）。
- **ring**：$F_{eff}=(8/(3\eta))(V_{DD}/V_{char})\ge16\gamma/(3\eta)$（[P2] Eq.(23)/(25)）→ 天花板
  $168.3$ dB；本站 $-91$ dBc/Hz 例 = $165$ dB，離頂只剩 $3.5$ dB。
- **LC**：$F_{eff}=F\Gamma_{rms}^2/(2Q^2\eta_P)$（由 [P1] Eq.(21) 推出）→ 天花板隨 $Q$：$Q=10$ 給
  $197.6$ dB（/4）／$194.6$ dB（/2）。$Q$ 是唯一的大槓桿。
- 好的發表 LC（$\approx190$ dB）離自己的 $Q$ 天花板約 $5\sim10$ dB；ring 落後 LC 約 25 dB，
  記帳：儲能 $2Q^2$（23 dB）＋ $V_{char}$／波形（$\sim9$ dB）。
- 天花板是**家族**不是魔術數字——引用任何「FOM 極限」時，先問它假設的 $F_{eff}$（$\gamma$、$Q$、
  $\eta_P$、慣例）是什麼。

## 延伸閱讀

- FOM 定義與 phase-noise × power 取捨：[tank_swing](/06_design_insights/tank_swing)
- [P1] Eq.(21) 推導與 /2 vs /4 慣例：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- [P2] ring FOM 與 N-independence：[lc_vs_ring](/06_design_insights/lc_vs_ring)、[paper_002 deep-dive](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)
- Leeson 的 $2FkT/P_s$ 與 ISF 對照：[derivation_leeson](/99_appendix/derivation_leeson)
- 拓樸層級的 $F$ 從哪來（tail、Colpitts 窄窗）：[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)
- FOM → jitter → BER 鏈：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)、[lab_08](/04_simulation_labs/lab_08_jitter_integration)
- 全站引用清單：[references](/99_appendix/references)

## 外部文獻（不在下載的 5 篇 PDF 內）

- **[E-Hegazi]** E. Hegazi, H. Sjöland, and A. A. Abidi, *"A Filtering Technique to Lower LC
  Oscillator Phase Noise,"* IEEE J. Solid-State Circuits, vol. 36, no. 12, pp. 1921–1930, Dec. 2001.
  （LC 噪聲因子下限 $F\to1+\gamma$ 與 tail filter；本站 [tank_swing](/06_design_insights/tank_swing)
  已引用並查證卷期/頁碼。）
- **[E-Andreani]** P. Andreani, X. Wang, L. Vandi, and A. Fard, *"A Study of Phase Noise in Colpitts
  and LC-Tank CMOS Oscillators,"* IEEE J. Solid-State Circuits, vol. 40, no. 5, pp. 1107–1118,
  May 2005.（Colpitts vs LC-tank 封閉式雜訊因子與量測比較；本站
  [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies) 已引用，
  DOI 10.1109/JSSC.2005.845991。本頁只取其摘要層級結論，未轉錄其內部公式。）
- **[E1] Leeson 1966**：D. B. Leeson, *"A Simple Model of Feedback Oscillator Noise Spectrum,"*
  Proc. IEEE, vol. 54, no. 2, pp. 329–330, Feb. 1966.（$2FkT/P_s$ 形；見
  [derivation_leeson](/99_appendix/derivation_leeson)。）
- **[E-Friis]** H. T. Friis, *"Noise Figures of Radio Receivers,"* Proc. IRE, vol. 32, no. 7,
  pp. 419–422, Jul. 1944.（$T_0=290$ K 雜訊參考溫度慣例的源頭；$-174$ dBm/Hz 即 $kT_0$ 換算。）
