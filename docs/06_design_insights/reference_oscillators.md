---
title: 參考源振盪器：crystal 與 MEMS 的 phase noise
description: 為什麼 crystal / MEMS 參考源是每條時脈鏈的 low-offset 錨——crystal 就是一顆 Q 高達 10⁴–10⁶ 的極端 LC tank，用本站 tank_Q 頁的 Q↔Γrms/qmax 橋一步步推出 close-in L 與 Lorentzian 線寬都 ∝1/Q²；一個可核對的 worked block（Q=50,000@100 MHz vs Q=10@5 GHz，同 offset Leeson 項差 ~105 dB、折算同載波後仍 ~71 dB）；XO/TCXO/OCXO/MEMS 的典型量級表（產業慣例，外部）；以及 aging/溫度（ppm 慢軸）與 phase noise（dBc/Hz 快軸）為何是兩條不同的 spec 軸。
---

import RefVsLcLeeson from "@site/src/components/RefVsLcLeeson";

# 參考源（crystal / MEMS）：時脈鏈的 low-offset 錨

> **先備**：[clock_chain_budget](/06_design_insights/clock_chain_budget)（規則 3：in-band $= N^2 S_{ref}\lvert H_{lp}\rvert^2$）、[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)（$Q$ 三寫法、$4kT/R_p$、$Q\leftrightarrow\Gamma_{rms}/q_{max}$ 橋——本頁的推導全部踩在它上面）、[derivation_leeson](/99_appendix/derivation_leeson)（$\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$ 整形項）｜ **接下來**：[pll_noise_budget](/06_design_insights/pll_noise_budget)、[fom_limit](/06_design_insights/fom_limit)

每一條真實的時脈鏈——SoC、SerDes、取樣系統、射頻收發機——的最上游都坐著一顆
**參考源（reference oscillator，頻率參考振盪器）**：石英晶體振盪器（crystal oscillator）
或 MEMS 振盪器。系統設計者為它花的錢常常超過整顆 PLL，問題是：**為什麼？它到底買到了什麼、
買不到什麼？** 這頁用本站已建好的兩座橋回答：
[clock_chain_budget](/06_design_insights/clock_chain_budget) 的規則 3 說明**為什麼鏈上沒有任何
東西能替 reference 的 close-in 雜訊擦屁股**；
[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 的
$Q\leftrightarrow\Gamma_{rms}/q_{max}$ 橋說明**為什麼 crystal 的 close-in 雜訊天生就低幾個數量級**。

> **物理直覺（先講結論）**：crystal 不是什麼新物理——它就是一顆 **$Q$ 高到誇張的 LC tank**。
> 石英的機械共振等效成 $L$、$C$、$R$，$Q$ 常見 $10^4$ 到 $10^6$（產業慣例量級，外部），
> 而 on-chip spiral inductor 的 tank 只有 $Q\approx5$–$20$。同一套 Leeson／ISF 公式、
> 同一個 $\big(\tfrac{f_0}{2Q\Delta f}\big)^2$ 整形項，把 $Q$ 從 10 換成 $5\times10^4$，
> close-in phase noise 就掉 $\propto 1/Q^2$——幾十個 dB 不是靠聰明電路，是靠**共振器裡
> 儲存的巨大能量對上極小的每週期損耗**。時脈鏈的分工因此天生確定：**低 offset 聽 reference 的、
> 高 offset 聽 VCO 的**，PLL 只是把兩段縫起來的裁縫。

> **誠實聲明（請先讀）**：本站下載的 5 篇 PDF（[P1]–[P5]）**都沒有** crystal / MEMS 的內容。
> 本頁凡是接到 ISF 的地方都經由已核的 [P1] Eq.(21), p.185 與站內
> [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 的橋；
> Leeson 整形項屬 [E1] Leeson 1966（外部文獻，非本站 5 篇 PDF，見
> [references](/99_appendix/references)）；crystal 等效電路（BVD model）與 XO/TCXO/OCXO/MEMS
> 的典型數字屬**標準頻率控制工業知識（產業慣例，外部，非本站 5 篇 PDF）**，本頁只給
> order-of-magnitude 範圍、不杜撰特定論文引用，選型請以廠商 datasheet 為準。

## 第 1 步：為什麼 reference 是整條鏈的 low-offset 錨

[clock_chain_budget](/06_design_insights/clock_chain_budget) 的規則 3（PLL）說：

$$
S_{out}(f)=N^2\,S_{ref}(f)\,\lvert H_{lp}(f)\rvert^2+S_{vco}(f)\,\lvert H_{hp}(f)\rvert^2
$$

in-band（$f\ll f_n$，loop bandwidth 內）$\lvert H_{lp}\rvert^2\to1$：**輸出的 close-in 相位雜訊
就是 reference 的相位雜訊加 $20\log_{10}N$**，一個 dB 都跑不掉。再看鏈上其他元件能做什麼
（同頁規則 1、2、4）：×N、÷N 只做**縮放**（整條曲線平移，乾淨的進去才乾淨的出來）；
buffer 只會**加**自己的床（功率相加，只會更糟）。結論：

- **鏈上沒有任何東西能改善 reference 的 close-in 雜訊**。低 offset（loop BW 內）的品質，
  在你「買下那顆 reference」的瞬間就定案了。
- 該頁的 worked chain 是活生生的證據：最終 27.6 fs 積分 jitter 裡 **65.9 % 的功率來自
  被 $\times N^2$ 抬高的 reference in-band 床**，而那顆漂亮的 $-148$ dBc/Hz VCO 只佔 0.42 %。
- 反過來，far-out（loop BW 外）reference 完全無關——那裡 $\lvert H_{hp}\rvert^2\to1$，
  聽 VCO 的。**reference 是 low-offset 錨，不是全頻段救星**（第 4 步的 worked block
  會給這句話數字）。

> **例 1（把 reference 錨進 ×50 PLL——canonical 數字）**：一顆 100 MHz 低雜訊 XO 在
> 1 kHz offset 有 $\mathcal{L}=-150$ dBc/Hz（低雜訊 XO 等級，產業慣例量級，外部）。
> 鎖進 ×50 PLL 到 5 GHz，in-band 的 $\mathcal{L}(1\,\text{kHz})$ 是多少？
> 比 free-run 的 on-chip LC 好幾 dB？

**逐步代入（帶單位）**——in-band 用規則 3 的漸近式：

$$
\mathcal{L}_{out}(1\,\text{kHz})=-150+20\log_{10}50=-150+33.98=-116.02\ \text{dBc/Hz}.
$$

對照組：本站 canonical 例 B 的 5 GHz on-chip LC（$\mathcal{L}(1\,\text{MHz})=-148$、
$1/f^2$ 裙邊）free-run 外推到 1 kHz：$-148+20\log_{10}(10^6/10^3)=-148+60=-88$ dBc/Hz。
**鎖 reference 在 1 kHz 贏 28.0 dB**——這就是「買 reference」買到的東西。
兩條線交叉在 $25.2$ kHz（$-148-20\log_{10}(f/10^6)=-116.02$ 解出 $f$），
正是 [pll_noise_budget](/06_design_insights/pll_noise_budget) 「交叉點決定最佳 loop BW」
的第一手感。**Dimension check**：dB 加法 = 無因次比值相乘 ✓；
$20\log_{10}N$ 之 $N$ 無因次 ✓。一行 Python 驗證：

```python
import numpy as np
L_in = -150.0 + 20*np.log10(50)        # 規則 3 in-band：ref + 20logN
print(round(L_in, 2))                  # -> -116.02
L_lc = -148.0 - 20*np.log10(1e3/1e6)   # canonical LC 1/f² 裙邊外推到 1 kHz
print(round(L_lc, 1))                  # -> -88.0
print(round(L_lc - L_in, 1))           # -> 28.0
f_cross = 1e6 * 10**(-(L_in + 148.0)/20)
print(round(f_cross/1e3, 1))           # -> 25.2
```

## 第 2 步：crystal 就是一顆極端 $Q$ 的 LC tank

石英晶體是**機械**共振器：壓電效應（piezoelectricity，機械應變↔電場互相轉換）把石英片的
機械振動模態映成電埠上的等效電路——標準的 **BVD model（Butterworth–Van Dyke 等效電路，
外部教科書內容，非本站 5 篇 PDF）**：

- **motional branch（動生支路）**：$L_m$–$C_m$–$R_m$ 串聯，代表機械的質量－勁度－阻尼。
  量級（產業慣例）：$L_m\sim$ mH–H、$C_m\sim$ fF、$R_m\sim$ 十到百 $\Omega$。
- **$C_0$（靜態電容）**：電極與封裝的普通電容，pF 級，與 motional branch 並聯。

在 series resonance $\omega_s=1/\sqrt{L_mC_m}$ 附近，這就是一顆 LC tank，$Q$ 用
[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 的同一套定義
（串聯形式 $Q=\omega_s L_m/R_m$，或能量定義 $Q=\omega_0 E_{stored}/P_{diss}$——兩頁同一個 $Q$）：

$$
Q_{crystal}\sim10^4\ \text{到}\ 10^6\qquad\text{vs}\qquad Q_{on\text{-}chip\ LC}\sim5\text{–}20.
$$

（crystal $Q$ 範圍為產業慣例量級，外部；on-chip $Q$ 天花板見 tank_Q 頁第 5 步。）
$L_m\sim$ mH 對上 on-chip 的 nH——**差 6 個數量級的等效電感**配上更小的等效損耗，
這就是「巨大儲能對上極小損耗」的電路化身。振盪波形接近正弦，所以 pedagogical toy 的
ISF 仍是 $\Gamma\approx-\sin$、$\Gamma_{rms}=1/\sqrt2$（[rms_isf](/03_isf_core_theory/rms_isf)）——
**crystal 的優勢不是來自 ISF 形狀，而是全部從 $Q$（等價地：儲能 $E$ 與 $q_{max}$）進帳**。
下一步就把這句話變成公式。

## 第 3 步：用站內的 $Q\leftrightarrow\Gamma_{rms}/q_{max}$ 橋推 $1/Q^2$ scaling

[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 第 4 步 (c) 的橋：
Leeson 的 $\dfrac{1}{2Q}$ 與 ISF 的 $\dfrac{\Gamma_{rms}}{q_{max}}$ 是同一個「雜訊→相位」
轉換效率。現在把這座橋**從 [P1] Eq.(21) 一步步走一遍**（正弦 LC toy，只算 tank 熱雜訊，
active core 另計）：

**(1) 起點——[P1] Eq.(21), p.185（5 篇 PDF 內、已核）：**

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)
$$

**(2) 代入三個站內已推好的量**：$\Gamma_{rms}^2=\tfrac12$（$\Gamma=-\sin$ 的 rms，
[rms_isf](/03_isf_core_theory/rms_isf)）、$q_{max}=C\,V_p$（規範符號表）、
$\overline{i_n^2}/\Delta f=4kT/R_p$（tank 損耗的熱雜訊，tank_Q 頁第 3 步）：

$$
\mathcal{L}_{lin}=\frac{\tfrac12}{C^2V_p^2}\cdot\frac{4kT/R_p}{4\,\Delta\omega^2}
=\frac{kT}{2\,C^2V_p^2\,R_p\,\Delta\omega^2}.
$$

**(3) 用 $Q$ 換掉 $R_p$**（tank_Q 頁第 1 步：$R_p=Q/(\omega_0 C)$）：

$$
\mathcal{L}_{lin}=\frac{kT\,\omega_0 C}{2\,C^2V_p^2\,Q\,\Delta\omega^2}
=\frac{kT\,\omega_0}{2\,C V_p^2\,Q\,\Delta\omega^2}.
$$

**(4) 用儲能換掉 $CV_p^2$**（tank_Q 頁第 2 步：$E_{stored}=\tfrac12 CV_p^2$，
即 $CV_p^2=2E_{stored}$）：

$$
\boxed{\ \mathcal{L}_{lin}(\Delta\omega)=\frac{kT\,\omega_0}{4\,E_{stored}\,Q\,\Delta\omega^2}\ }
$$

**(5) 再用能量定義換成功率形式**（tank_Q 頁第 2 步：$P_{diss}=\omega_0E_{stored}/Q$，
即 $E_{stored}=Q\,P_{diss}/\omega_0$）：

$$
\mathcal{L}_{lin}(\Delta\omega)=\frac{kT}{P_{diss}}\left(\frac{\omega_0}{2Q\,\Delta\omega}\right)^2.
$$

這正是 **Leeson（[E1]，外部）在 $F=1$、thermal-only 時的 $1/f^2$ 段**——ISF 版與 Leeson 版
在這條鏈上精確會合（factor-of-2 的 SSB 記帳慣例照舊，見
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)；本頁全程用
[P1] Eq.(21) 的 /4 慣例）。

- **Dimension check（步驟 4 形式）**：$\dfrac{[\text{J}][\text{rad/s}]}{[\text{J}][\text{rad/s}]^2}=\dfrac{1}{[\text{1/s}]}=[\text{s}]=1/\text{Hz}$ ✓
  （$\mathcal{L}_{lin}$ 是 per-Hz 的功率比值）。
- **Dimension check（步驟 5 形式）**：$kT/P_{diss}=[\text{J}]/[\text{W}]=[\text{s}]=1/\text{Hz}$，
  括號平方無因次 ✓。

**三個立即的推論**（都被第 4 步與例 2 的數值接住）：

1. **close-in $\mathcal{L}\propto 1/Q^2$**（固定 $P_{diss}$）：$Q$ 乘 $10\Rightarrow-20$ dB。
   crystal 的 $Q$ 比 on-chip LC 高 $10^3$–$10^5$ 倍，光這一項就是 $-60$ 到 $-100$ dB 級。
2. **真正的槓桿是 $E_{stored}\cdot Q$ 乘積**（步驟 4 形式）——「儲多少能」×「漏得多慢」。
   同一個 $4kT$ 漲落對上越大的儲能水庫、越慢的洩漏，換到的相位就越小。這就是
   $Q\leftrightarrow\Gamma_{rms}/q_{max}$ 橋的能量讀法：**crystal 的有效
   $\Gamma_{rms}/q_{max}$（連同它看到的雜訊）比任何 on-chip LC 低好幾個數量級**，
   不是 ISF 形狀不同，而是分母 $q_{max}$（儲存電荷/能量）巨大、雜訊源（損耗）相對微小。
3. **Lorentzian 線寬也 $\propto1/Q^2$**：close-in 的 $1/f^2$ 裙邊對應相位擴散常數 $D$
   （單邊 $S_\phi=4D/\Delta\omega^2$，[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)），
   由步驟 5 讀出 $S_\phi=2\mathcal{L}_{lin}$：

$$
D=\frac{\Delta\omega^2 S_\phi}{4}=\frac{kT\,\omega_0^2}{8\,P_{diss}\,Q^2},\qquad
\Delta f_{3\mathrm{dB}}=\frac{D}{\pi}=\frac{kT\,\omega_0^2}{8\pi\,P_{diss}\,Q^2}\ \propto\ \frac{1}{Q^2}.
$$

**把數字放進去（crystal 到底儲了多少能）**——crystal：$f_0=100$ MHz、$Q=5\times10^4$、
驅動（耗散）功率 $P_{diss}=100\ \mu$W（典型 crystal drive level 量級，產業慣例，外部）；
on-chip LC：tank_Q 頁的 canonical 例（$C=1.013$ pF、$V_p=1$ V、$Q=10$、$f_0=5$ GHz）：

```python
import numpy as np
k, T = 1.380649e-23, 300.0
kT = k*T
f0x, Qx, Px = 100e6, 5e4, 100e-6      # crystal：100 MHz, Q=50k, drive 100 µW
w0x = 2*np.pi*f0x
Ex = Qx*Px/w0x                        # E = Q·P/ω0（tank_Q 第 2 步能量定義反解）
print(round(Ex*1e9, 2))               # -> 7.96
C, Vp, Ql = 1.013e-12, 1.0, 10.0      # on-chip LC（tank_Q canonical 例）
El = 0.5*C*Vp**2
w0l = 2*np.pi*5e9
Pl = w0l*El/Ql                        # LC 得耗掉的功率
print(round(El*1e12, 3))              # -> 0.507
print(round(Pl*1e3, 2))               # -> 1.59
print(round(10*np.log10((Ex*Qx)/(El*Ql)), 1))               # -> 79.0
print(round(10*np.log10((w0l/(El*Ql))/(w0x/(Ex*Qx))), 1))   # -> 95.9
print(round(10*np.log10(kT/Px), 1))   # -> -163.8
```

讀法：crystal 儲能 **7.96 nJ**，是 LC 的 0.507 pJ 的約 $1.6\times10^4$ 倍——而且耗的功率
還少 16 倍（0.1 mW vs 1.59 mW）。$E\cdot Q$ 乘積差 **79.0 dB**；再算上 $\omega_0$ 一次方，
**同一 offset 的 thermal-only $\mathcal{L}$ 差 95.9 dB**（幅度比 $\sqrt{3.9\times10^9}\approx6\times10^4$
——「有效 $\Gamma_{rms}/q_{max}$ 低了近 5 個數量級」就是這個意思）。
最後一行順便給出 crystal 在自己 Leeson corner 處的理想床 $kT/P_{diss}=-163.8$ dBc/Hz——
與真實低雜訊 XO 的 $-150\sim-160$ 級 floor（產業慣例）同一量級，多出來的差距屬
sustaining amplifier（維持振盪的放大器）的 noise factor 與 flicker（見失效條件）。

> **例 2（線寬 $\propto1/Q^2$——同兩顆振盪器）**：把上面兩組參數代入
> $\Delta f_{3\mathrm{dB}}=kT\omega_0^2/(8\pi P_{diss}Q^2)$，兩顆的 thermal-only
> Lorentzian 線寬各是多少？

**逐步代入（帶單位）**：

$$
\text{crystal}:\ \frac{4.14\times10^{-21}\times(6.28\times10^8)^2}{8\pi\times10^{-4}\times(5\times10^4)^2}
=2.6\times10^{-10}\ \text{Hz},\qquad
\text{LC}:\ 1.02\ \text{Hz}.
$$

差 $3.9\times10^9$ 倍（95.9 dB）——與上面的同 offset $\mathcal{L}$ 比值**完全同一個數字**
（兩者都 $\propto\omega_0^2/(PQ^2)$，這是自洽性檢查 ✓）。crystal 的 thermal-only 線寬
$10^{-10}$ Hz 級：**在任何可實現的量測時間內都量不到**——這就是「reference 的載波
幾乎是一根 delta」的定量版本。兩個數字都是 thermal-only 理想值（無 flicker、無
sustaining amp），標 illustrative。**Dimension check**：
$\dfrac{[\text{J}][\text{rad/s}]^2}{[\text{W}]}=[\text{J/s}]\cdot\dfrac{[\text{J}]}{[\text{W}]}\cdot\dfrac{1}{[\text{s}]}=[\text{1/s}]=[\text{Hz}]$ ✓。
一行 Python 驗證：

```python
import numpy as np
kT = 1.380649e-23*300.0
lw = lambda f0, Q, Ps: kT*(2*np.pi*f0)**2/(8*np.pi*Ps*Q**2)
print(f"{lw(100e6, 5e4, 100e-6):.2e}")   # -> 2.60e-10
print(round(lw(5e9, 10.0, 1.591e-3), 2)) # -> 1.02
print(round(10*np.log10(lw(5e9, 10.0, 1.591e-3)/lw(100e6, 5e4, 100e-6)), 1))  # -> 95.9
```

（LC 的 $D=\pi\times1.02\approx3.2$ rad²/s 屬本頁 illustrative 參數組，與
[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) 的 toy 參數組
$D=0.125\to39.8$ mHz 是不同輸入，公式相同。）

## 第 4 步：worked block——$Q=50{,}000$ @ 100 MHz vs $Q=10$ @ 5 GHz（可核對）

現在做本頁招牌的、完全可核對的比較：**同一個 offset $\Delta f$ 下，Leeson 整形項
$10\log_{10}\big[1+\big(\tfrac{f_0}{2Q\Delta f}\big)^2\big]$ 差多少？**
（[E1] 形式；只比整形項＝假設兩者同 $F$、同 $P_s$，這是刻意的隔離變因，誠實註記在下。）

先算兩顆的 **Leeson corner** $f_0/2Q$（整形項從 $1/f^2$ 轉平的地方）：

$$
\text{crystal}:\ \frac{10^8}{2\times5\times10^4}=1000\ \text{Hz},\qquad
\text{LC}:\ \frac{5\times10^9}{2\times10}=2.5\times10^8\ \text{Hz}=250\ \text{MHz}.
$$

crystal 的整形項在 1 kHz 以外就**沒了**（轉平）；LC 的整形項一路 $1/f^2$ 到 250 MHz——
**LC 在整個實用 offset 範圍內都在被 $\big(\tfrac{f_0}{2Q\Delta f}\big)^2$ 懲罰**。逐 offset 算：

| offset $\Delta f$ | crystal 項 [dB] | LC 項 [dB] | 差（同 offset、各自載波） | 折算同載波（$-33.98$） |
|---|---|---|---|---|
| 1 kHz | $3.01$ | $107.96$ | $104.95$ dB | $70.97$ dB |
| 100 kHz | $0.00$ | $67.96$ | $67.96$ dB | $33.98$ dB |
| 1 MHz | $0.00$ | $47.96$ | $47.96$ dB | $13.98$ dB |

- **第 4 欄**：同 offset、同 $F$、同 $P_s$ 下的裸差。1 kHz 處 $104.95$ dB
  （漸近比 $\big(\tfrac{2.5\times10^8}{10^3}\big)^2=6.25\times10^{10}=108.0$ dB，
  crystal 在自己 corner 上少了 $3$ dB 的 $1+1$）。
- **第 5 欄（誠實的比法）**：100 MHz 和 5 GHz 載波不同，公平比較要把 crystal ×50
  折到 5 GHz，付 $+20\log_{10}50=33.98$ dB（[clock_chain_budget](/06_design_insights/clock_chain_budget)
  規則 1）。**折算後 1 kHz 仍贏 71.0 dB**；但注意優勢隨 offset 縮水
  （100 kHz 剩 34 dB、1 MHz 剩 14 dB），到了兩條 $1/f^2$ 與 floor 的交界之外，
  被 ×50 抬高的 crystal **floor** 反而會輸給 LC 的遠端裙邊——這正是第 1 步說的
  「reference 是 low-offset 錨，不是全頻段救星」，也是 PLL loop BW 存在的理由。
- **Dimension check**：$\dfrac{f_0}{2Q\Delta f}=\dfrac{[\text{Hz}]}{[\text{Hz}]}$ 無因次 ✓；
  dB 差 = 比值 ✓。

```python
import numpy as np
f0x, Qx = 100e6, 5e4    # crystal：100 MHz、Q = 50,000
f0l, Ql = 5e9, 10.0     # on-chip LC：5 GHz、Q = 10
term = lambda f0, Q, df: 10*np.log10(1 + (f0/(2*Q*df))**2)
print(round(f0x/(2*Qx), 0))                               # -> 1000.0
print(round(f0l/(2*Ql)/1e6, 0))                           # -> 250.0
print(round(term(f0x, Qx, 1e3), 2))                       # -> 3.01
print(round(term(f0l, Ql, 1e3), 2))                       # -> 107.96
print(round(term(f0l, Ql, 1e3) - term(f0x, Qx, 1e3), 2))  # -> 104.95
print(round(term(f0l, Ql, 1e5) - term(f0x, Qx, 1e5), 2))  # -> 67.96
print(round(term(f0l, Ql, 1e6) - term(f0x, Qx, 1e6), 2))  # -> 47.96
print(round(20*np.log10(f0l/f0x), 2))                     # -> 33.98
```

**誠實註記**：(1) 只比整形項＝假設同 $F$、同 $P_s$；真實 crystal 驅動功率（$\sim0.1$ mW）
低於典型 LC tank 耗散（$\sim1.6$ mW），把功率也算進去會把 108 dB 修成第 3 步的 95.9 dB
（$108.0-10\log_{10}(1.59\,\text{mW}/0.1\,\text{mW})=95.9$，兩種算法自洽 ✓）。
(2) thermal-only：真實 crystal 的 close-in 實測常被 sustaining amp 的 $1/f^3$ 主宰、
floor 被 buffer 限制，本表是「共振器物理給的下限」。(3) $Q=5\times10^4$ @ 100 MHz
是保守取值（100 MHz 常用 overtone 切型，$Q$ 可更高；產業慣例量級，外部）。

下面的互動元件就是這個 worked block 的通用版——拉 $Q$、$f_0$、offset，
看兩條 Leeson 曲線與折算 ×N 後的差距：

<RefVsLcLeeson />

## 第 5 步：典型數字表——XO / TCXO / OCXO / MEMS

> **本表全部是產業慣例的 order-of-magnitude 範圍（外部文獻，非本站 5 篇 PDF）**：
> 不同廠牌、切型、頻率、年代差異很大；同一等級內高低配可差 20 dB。本表只建立
> 「哪個量級住在哪一層」的手感，**選型一律以 datasheet 的 L(f) 曲線與 stability 表為準**，
> 本站不杜撰特定型號或論文數字。

| 等級 | 典型輸出頻率 | 頻率 vs 溫度（慢軸） | $\mathcal{L}(1\,\text{kHz})$ 量級 | far-out floor 量級 | 一句話定位 |
|---|---|---|---|---|---|
| **XO**（plain crystal osc.） | 10–100 MHz | $\pm10\ldots\pm100$ ppm | $-135\ldots-155$ dBc/Hz | $-150\ldots-165$ dBc/Hz | 最便宜的高 $Q$；低雜訊 100 MHz 級可到 $-150$ dBc/Hz @ 1 kHz |
| **TCXO**（溫度補償 XO） | 10–50 MHz | $\pm0.1\ldots\pm2$ ppm | 與同級 XO 相近 | $-150\ldots-160$ dBc/Hz | 補償網路修的是**慢軸**（ppm），幾乎不動 $\mathcal{L}(f)$；部分設計 close-in 反而略差 |
| **OCXO**（恆溫 XO） | 5–100 MHz | $\pm10^{-4}\ldots\pm10^{-2}$ ppm | $-150\ldots-165$ dBc/Hz | $-155\ldots-170$ dBc/Hz | close-in 之王（1–10 Hz offset 都有規格）；代價是瓦級加熱功耗與體積 |
| **MEMS oscillator** | 1–700 MHz（PLL 合成） | $\pm0.05\ldots\pm20$ ppm 依等級 | $-120\ldots-145$ dBc/Hz | $-140\ldots-155$ dBc/Hz | 矽共振器 + fractional-N PLL；贏在抗震/可靠度/可程式化，phase noise 通常讓給石英 |

三個讀表要點：

1. **XO→TCXO→OCXO 的階梯主要是「慢軸」（ppm）的階梯**，$\mathcal{L}(f)$ 的差距集中在
   close-in（OCXO 用更高 $Q$ 的切型、更講究的 sustaining amp 與恆溫把 1 Hz–1 kHz 段壓低）。
2. floor 段（$\ge10$ kHz）各等級都擠在 $-150\sim-170$ dBc/Hz——floor 由
   sustaining amp／output buffer 決定（$kT/P$ 級，見第 3 步的 $-163.8$），**不是** $Q$ 決定；
   $Q$ 買到的是 corner 以內的 $1/Q^2$。
3. MEMS 的 $\mathcal{L}$ 欄要小心讀：它的輸出頻率是 PLL 合成的，in-band 形狀由
   PLL（$N^2$ 床 + charge pump）決定、不直接是共振器的 Leeson 裙邊——下一步展開。

## 第 6 步：MEMS——$f\cdot Q$ 乘積上限與「倍頻稅」

MEMS（microelectromechanical systems，微機電）振盪器把石英換成矽的機械共振器
（真空封裝、$Q\sim10^4$–$10^5$ 量級），再用 fractional-N PLL 把 MHz 級的共振頻率
合成到使用者要的輸出。兩件物理決定它的 phase noise 定位（皆產業慣例／材料物理量級，外部）：

**(a) $f\cdot Q$ 乘積上限。** 對給定材料與損耗機制（聲子散射 Akhiezer damping、
thermoelastic damping、anchor loss 等），共振頻率與 $Q$ 的**乘積**有量級上限——
石英與矽在室溫都在 $f\cdot Q\sim10^{13}$ Hz 量級（產業慣例；精確值依切型/模態/溫度而異，
本站不給假精度）。**這條上限把 $Q$ 和 $f_0$ 綁成蹺蹺板**：$f_0$ 拉高，$Q$ 就 $\propto1/f_0$
掉下來。

**(b) 「倍頻稅」下的最佳分工。** 若 $f\cdot Q$ 固定，Leeson corner 變成

$$
\frac{f_0}{2Q}=\frac{f_0^2}{2\,(f\cdot Q)}\ \propto\ f_0^2,
$$

共振器自己的 close-in 整形項 $\big(\tfrac{f_0}{2Q\Delta f}\big)^2\propto f_0^4$；把它 ×N 折到
固定的輸出載波 $f_{out}$ 再付 $20\log_{10}(f_{out}/f_0)$，淨 close-in

$$
\mathcal{L}_{out,\ close\text{-}in}\ \propto\ f_0^4\cdot\Big(\frac{f_{out}}{f_0}\Big)^2=f_0^2\,f_{out}^2
$$

——**共振器頻率每降 10 倍，輸出端 close-in 淨賺 20 dB**（同 $f\cdot Q$、同 $F$、同 $P$）。
這就是為什麼參考源都住在 10–100 MHz 而不是直接做 GHz 共振器；也是為什麼 MEMS
（與石英一樣受 $f\cdot Q$ 綁架）選擇 MHz 級共振器＋PLL 合成的架構。數值驗證：

```python
import numpy as np
fQ, fout = 1e13, 5e9    # f·Q 乘積固定（量級，產業慣例）、輸出 5 GHz
rel = lambda f0: 20*np.log10(f0/(2*(fQ/f0))) + 20*np.log10(fout/f0)
print(round(rel(10e6), 2))               # -> 67.96
print(round(rel(100e6), 2))              # -> 87.96
print(round(rel(100e6) - rel(10e6), 2))  # -> 20.0
```

（$rel$＝corner 值＋倍頻稅的相對 dB；10 MHz/$Q=10^6$ 比 100 MHz/$Q=10^5$ 淨好 20.0 dB ✓
$f_0^2$ 律。當然 $f_0$ 也不能無限降：$N=f_{out}/f_0$ 變大使 in-band 床 $\propto N^2$ 上抬、
divider/PLL 床與 flicker 也會接手——實務最佳點就落在幾十 MHz，與市場上的 reference
頻率一致。）

**MEMS 的記帳後果**：輸出端 in-band 由 fractional-N PLL 的 $N^2$ 床＋量化雜訊決定、
out-of-band 由內建 VCO 決定——**共振器的極高 $Q$ 主要買到「頻率穩定度與 close-in 錨」，
不是整條曲線**。所以第 5 步表裡 MEMS 的 $\mathcal{L}(1\,\text{kHz})$ 通常比同級石英 XO 高
（它是 PLL 床，不是共振器裙邊），但對很多應用（乙太網、USB、感測）足夠，換到的是
抗震動/衝擊、壽命、尺寸與任意頻率可程式化（產業慣例定位，外部）。

## 第 7 步：aging／溫度 vs phase noise——兩條不同的 spec 軸

datasheet 上的「stability ±25 ppm」和「$-150$ dBc/Hz @ 1 kHz」**講的是兩件幾乎正交的事**，
混用是系統設計最常見的選型錯誤之一：

| | **快軸：spectral purity（相位雜訊）** | **慢軸：frequency stability（頻率準確度/穩定度）** |
|---|---|---|
| 量什麼 | $\mathcal{L}(\Delta f)$、積分 jitter | $\Delta f/f_0$ 對溫度、時間、電壓的漂移 |
| 單位 | dBc/Hz、fs | ppm、ppb |
| 時間尺度 | offset $\ge1$ Hz（亞秒級起伏） | 秒—年（溫度循環、aging） |
| 物理來源 | tank 熱雜訊（$kT\omega_0/4EQ\Delta\omega^2$）、amp 的 $F$ 與 flicker | 切型的溫度係數、應力鬆弛、電極/封裝污染遷移（aging，產業慣例定性） |
| 誰能修 | 換更高 $Q$/更大 $P$/更乾淨 amp；**鏈上修不了**（第 1 步） | 補償（TCXO）、恆溫（OCXO）、校準/馴服（GPS-disciplined） |
| 對系統的傷 | eye 閉合、BER、ADC SNR（快 jitter） | 頻率偏出接收窗、PLL/CDR pull-in 失敗、時間戳漂移 |

- **oven 和補償網路不動 $\mathcal{L}(f)$**：OCXO 的恆溫爐把「小時—天」尺度的漂移壓掉，
  對 1 kHz offset 的裙邊毫無作用（那裡的物理是第 3 步的 $kT/(E\cdot Q)$）；反過來，
  再乾淨的 buffer 也救不了 aging。**兩軸各自用各自的手段、各自付各自的錢。**
- aging 量級（產業慣例）：XO/TCXO 首年 $\sim\pm(0.5\ldots5)$ ppm/year；OCXO 可到
  ppb/day–ppb/year 級。它是**確定性慢漂**，不是隨機相位雜訊。
- **兩軸的橋是 Allan deviation**（[allan_variance](/02_foundations/allan_variance)）：
  短 $\tau$ 段（white/flicker PM/FM）對應 $\mathcal{L}(f)$ 的各段斜率，長 $\tau$ 端的
  上翹（random-walk FM、drift $\propto\tau^{+1}$）就是溫度與 aging 進場的地方——
  一張 ADEV 圖同時看得到兩條軸的交棒點。這也是為什麼 reference 的 datasheet 常常
  同時給 $\mathcal{L}(f)$ 表、ADEV 表與 aging 表：**三張表三個時間尺度，缺一不可**。

## design knobs 清單（怎麼選/用一顆 reference）

| 旋鈕 | 作用在哪裡 | 代價／限制 |
|---|---|---|
| reference 等級（XO→TCXO→OCXO） | 直接搬 low-offset 錨（第 1 步：in-band $=\mathcal{L}_{ref}+20\log_{10}N$，鏈上無解藥） | 錢、功耗（OCXO 爐瓦級）、體積；TCXO/OCXO 主要買慢軸 |
| reference 頻率 $f_{ref}$（降 $N$） | in-band 床 $\propto N^2$（[clock_chain_budget](/06_design_insights/clock_chain_budget) 規則 3） | $f\cdot Q$ 蹺蹺板：共振器 close-in $\propto f_0^2 f_{out}^2$（第 6 步），最佳點在幾十 MHz |
| drive level $P_{diss}$ | $\mathcal{L}\propto1/P$（第 3 步步驟 5） | crystal 過驅 → 非線性、應力、aging 加速（產業慣例）；datasheet 有 max drive 規格 |
| loop bandwidth $f_n$ | 決定「聽 reference 到哪、交給 VCO 從哪」（交叉點法，例 1 的 25.2 kHz） | 完整取捨見 [pll_noise_budget](/06_design_insights/pll_noise_budget)（U 形曲線） |
| 輸出 buffer／扇出 | floor 由它鉗住（規則 4 功率相加） | 再好的 OCXO 過一級吵 buffer 就毀（[clock_chain_budget](/06_design_insights/clock_chain_budget) 第 4 規則） |
| 石英 vs MEMS | phase noise vs 抗震/可靠度/可程式化的取捨（第 6 步） | MEMS in-band 是 PLL 床；石英怕振動（vibration sensitivity，產業慣例） |

## 與 SerDes 的關聯

- TX PLL 的 in-band（loop BW 內）就是 reference $+20\log_{10}N$——reference 的 close-in
  決定 TX 時脈在 CDR tracking 頻寬**邊緣**的殘餘 jitter；完全在 CDR 頻寬內的部分會被
  接收端追掉（[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)），
  所以 SerDes 對 reference 的 $\mathcal{L}(10\,\text{Hz})$ 相對寬容、對
  10 kHz–數 MHz 的「交接帶」敏感——恰好是例 1 交叉點（25.2 kHz）附近的戰場。
- 無 CDR 追蹤的系統（ADC/DAC 取樣、雷達）沒這個豁免：aperture jitter 從低 offset 一路積上來，
  reference 的 close-in 直接進 SNR（[adc_aperture_jitter](/06_design_insights/adc_aperture_jitter)）。
- 慢軸也咬人：reference 的 ppm 偏移吃掉 CDR 的 pull-in/tracking range 與
  SSC（spread-spectrum clocking）預算——這是第 7 步「兩條軸」在 SerDes 的具體化身。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| thermal-only、$F=1$ 理想化（第 3、4 步） | $1/Q^2$、$E\cdot Q$ scaling 乾淨成立 | 實測 close-in 常被 sustaining amp 的 flicker（$1/f^3$）主宰、floor 被 buffer 鉗住——本頁數字是**共振器物理下限** |
| series resonance 附近的 BVD 等效 | crystal ≈ 一顆極端 $Q$ 的 LC，tank_Q 全套適用 | 遠離共振、overtone/spurious 模態、$C_0$ 並聯路徑主導時，單一 LC 模型失效 |
| drive level 在 datasheet 範圍 | $\mathcal{L}\propto1/P$ 適用 | 過驅：非線性、activity dip、aging 加速；欠驅：起振裕度差（產業慣例） |
| 小角近似、$\Delta f$ 遠大於線寬 | $\mathcal{L}=\tfrac12S_\phi$、Leeson $1/f^2$ 裙邊 | 極近載波轉 Lorentzian（crystal 線寬 $10^{-10}$ Hz 級，實務永遠量不到這區；[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)） |
| 量測本底夠低 | datasheet 曲線可信 | 量低雜訊 reference 必須 cross-correlation，否則量到的是儀器（[measurement_and_spurs](/06_design_insights/measurement_and_spurs)） |
| MEMS：看系統輸出 | in-band=PLL 床、共振器買 close-in 錨與穩定度 | 把 MEMS 輸出當「裸共振器 Leeson 裙邊」讀會全錯（第 6 步） |

## 重點回顧

- **reference 是 low-offset 錨**：in-band $\mathcal{L}_{out}=\mathcal{L}_{ref}+20\log_{10}N$
  （[clock_chain_budget](/06_design_insights/clock_chain_budget) 規則 3），鏈上任何元件都
  救不了它的 close-in；worked chain 裡 65.9 % 的 jitter 功率來自 ref$\times N^2$ 床。
- **crystal＝極端 $Q$ 的 LC**（BVD：$L_m\sim$ mH、$C_m\sim$ fF、$Q\sim10^4$–$10^6$，
  產業慣例量級）；ISF 形狀照舊（$\Gamma\approx-\sin$、$\Gamma_{rms}=1/\sqrt2$），
  優勢全從 $Q$（儲能對損耗）進帳。
- **站內橋推出的 scaling**：[P1] Eq.(21) ＋ $4kT/R_p$ ＋ $Q$ 定義 ⇒
  $\mathcal{L}_{lin}=\dfrac{kT\,\omega_0}{4E_{stored}Q\,\Delta\omega^2}=\dfrac{kT}{P_{diss}}\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$；
  close-in $\mathcal{L}$ 與 Lorentzian 線寬皆 $\propto1/Q^2$；真正槓桿是 $E\cdot Q$ 乘積
  （crystal 例：7.96 nJ vs 0.507 pJ，$E\cdot Q$ 差 79.0 dB、同 offset $\mathcal{L}$ 差 95.9 dB）。
- **worked block**：$Q=5\times10^4$@100 MHz vs $Q=10$@5 GHz——corner 1 kHz vs 250 MHz；
  同 offset Leeson 項差 104.95 dB（1 kHz）、67.96 dB（100 kHz）；折算同載波（$-33.98$）
  後仍贏 71.0／34.0 dB，但優勢隨 offset 縮水——far-out 要交還給 VCO。
- 典型量級（產業慣例，外部）：XO floor $-150\ldots-165$、OCXO close-in 之王、
  TCXO/OCXO 的階梯主要在**慢軸**（ppm）；floor 由 amp/buffer（$kT/P$ 級）而非 $Q$ 決定。
- **MEMS**：$f\cdot Q\sim10^{13}$ Hz 量級蹺蹺板 ⇒ 輸出端 close-in $\propto f_0^2f_{out}^2$
  （共振器頻率降 10 倍淨賺 20 dB）⇒ MHz 共振器＋fractional-N PLL 的架構；in-band 是
  PLL 床，買的是穩定度、抗震與可程式化。
- **兩條 spec 軸**：dBc/Hz（快軸，$Q$/$P$/amp 決定，鏈上修不了）與 ppm（慢軸，
  補償/恆溫/馴服可修）；橋是 ADEV（[allan_variance](/02_foundations/allan_variance)）。
- 來源紀律：[P1] Eq.(21)（5 篇 PDF 內、已核）＋站內 tank_Q 橋；Leeson 整形＝[E1]（外部）；
  crystal/MEMS 等效電路與典型數字＝產業慣例 order-of-magnitude（外部，非本站 5 篇 PDF，
  不杜撰引用）。

## 延伸閱讀

- $Q$ 三寫法、$4kT/R_p$、$Q\leftrightarrow\Gamma_{rms}/q_{max}$ 橋（本頁推導的地基）：[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)
- 四條時脈鏈記帳規則與 worked chain（65.9 % 來自 ref 床的那條）：[clock_chain_budget](/06_design_insights/clock_chain_budget)
- phase noise × power 的理論天花板（另一個「還剩幾 dB」的視角）：[fom_limit](/06_design_insights/fom_limit)
- Leeson 模型全推導與 ISF 對照表：[derivation_leeson](/99_appendix/derivation_leeson)
- 最佳 loop BW 的 U 形取捨（例 1 交叉點的完整版）：[pll_noise_budget](/06_design_insights/pll_noise_budget)
- 慢軸/快軸的橋——ADEV 斜率表：[allan_variance](/02_foundations/allan_variance)
- 極近載波的 Lorentzian 與擴散常數 $D$：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)、[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
- 量低雜訊 reference 為何要 cross-correlation：[measurement_and_spurs](/06_design_insights/measurement_and_spurs)

## 外部文獻（不在下載的 5 篇 PDF 內）

- **Leeson 整形項**：[E1] D. B. Leeson, *"A Simple Model of Feedback Oscillator Noise
  Spectrum,"* Proc. IEEE, vol. 54, no. 2, pp. 329–330, Feb. 1966（已在
  [references](/99_appendix/references) 查證卷期/DOI）。
- **crystal BVD 等效電路、$Q$／drive level／aging／$f\cdot Q$ 乘積、XO/TCXO/OCXO/MEMS
  典型數字**：標準頻率控制（frequency control）工業知識與教科書內容——本頁一律標
  **產業慣例、order-of-magnitude**，不引用特定論文或型號以免杜撰；工程上請以
  廠商 datasheet 與 IEEE Int. Frequency Control Symposium 系列文獻為準（領域名稱，
  非特定篇目引用）。
- 本站 5 篇 PDF 提供的是把這一切接回 ISF 的鑰匙：[P1] Eq.(21), p.185（$\Gamma_{rms}/q_{max}$
  與 $1/f^2$）；[P2]–[P4] 與本頁無直接關係。
