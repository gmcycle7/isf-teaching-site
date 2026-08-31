---
title: 時脈鏈雜訊記帳：×N、÷N、PLL、buffer 一頁查表
description: 四條時脈鏈記帳規則的嚴格推導——×N 倍頻 +20logN（φ_out=Nφ_in）、÷N 除頻 −20logN（edge-picking）、過 PLL（reference ×N² 且低通、VCO 高通）、buffer/divider 的加成雜訊床（功率相加）——加上一條 100 MHz → ×50 PLL → 5 GHz → ÷2 → 2.5 GHz → buffer 的完整 worked chain：每級在 100 kHz 與 10 MHz 的 L、最終 27.6 fs 積分 jitter、以及 brick-wall 記帳 vs 完整 type-II 整形的誠實對照。
---

import NumericQuiz from "@site/src/components/NumericQuiz";

# 時脈鏈雜訊記帳：×N、÷N、PLL、buffer 一頁查表

> **先備**：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)（$S_\phi$、$\mathcal{L}$、phase↔time 換算）、[pll_noise_budget](/06_design_insights/pll_noise_budget)（$\lvert H_{lp}\rvert^2,\lvert H_{hp}\rvert^2$ 與五源預算——本頁直接沿用、**不重推**）、[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（VCO 那條 $-148$ dBc/Hz 從哪來）｜ **接下來**：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)、[exercises](/06_design_insights/exercises)

真實系統裡沒有「一顆振盪器直接用」這回事：參考晶體被 PLL 倍頻上去、再被除頻器分下來、
一路又過好幾級 buffer 才到取樣器。系統工程師每天的問題是：**給我源頭的 $\mathcal{L}(f)$，
時脈樹（clock tree）每一個節點的 $\mathcal{L}(f)$ 是多少？最後那個 clock 的積分 jitter 是多少？**
好消息是：整條鏈的記帳只需要**四條規則**。這頁把四條規則各自**逐步推導**（不跳步、帶單位、
給失效條件），然後用一條完整的 worked chain 把它們串起來算到底。

> **物理直覺（先講結論）**：時脈鏈上發生在相位身上的事，只有兩種——
> **(1) 確定性的相位縮放**：×N 把相位乘 $N$（$+20\log_{10}N$ dB）、÷N 把相位除 $N$
> （$-20\log_{10}N$ dB）、PLL 在 in-band 對 reference 做 ×N 並低通、對 VCO 高通。
> 縮放作用在**整條曲線**上，offset 軸不動。
> **(2) 加成的獨立雜訊**：buffer 與 divider 自己的雜訊床（floor），與輸入相位不相關，
> **功率相加**（絕不是 dB 相加）。
> 另外有一個漂亮的**守恆量**：理想 ×N/÷N 下，**以秒計的時間抖動 $\sigma_t$ 完全不變**——
> 變的只是「同一個秒數誤差佔一個週期的角度比例」。

## 第 0 步：一頁查表（先給結論，推導在後）

| 元件 | 相位關係 | $\mathcal{L}(f)$ 記帳 | 主要失效條件 |
|---|---|---|---|
| 理想 ×N 倍頻 | $\phi_{out}=N\,\phi_{in}$ | $\mathcal{L}+20\log_{10}N$（整條曲線平移） | 小角近似（$\sigma_\phi\times N$ 變大）、offset 接近 $f_{ref}/2$ |
| 理想 ÷N 除頻 | $\phi_{out}=\phi_{in}/N$ | $\mathcal{L}-20\log_{10}N$ | 取樣摺疊（offset 接近 $f_{out}/2$）、divider 自身床 |
| 過 PLL（×N） | in-band 跟 ref、out-of-band 跟 VCO | $N^2S_{ref}\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$ | 純二階 loop 的 ref 尾巴（本頁第 6 步實算） |
| buffer / divider 床 | $\phi_{out}=\phi_{in}+\phi_{add}$ | $10\log_{10}\big(10^{\mathcal{L}_{in}/10}+10^{\mathcal{L}_{buf}/10}\big)$ | 相關雜訊（共 supply/bias）時不能直接功率相加 |

**慣例聲明（factor-of-2 紀律，全頁一致）**：本頁所有 $\mathcal{L}$ 都是 **SSB（單邊帶）dBc/Hz**，
與 $S_\phi$ 的換算用小角近似 $\mathcal{L}=\tfrac12 S_\phi$（規範公式 16；`noise_utils` 同一慣例）。
worked chain 的 VCO 錨點 $-148$ dBc/Hz @ 1 MHz 是站內 canonical 例 B，用 [P1] Eq.(21), p.185 的
**「/4」SSB 記帳**；乾淨時域推導的「/2」版本會給 $-145$（差 3 dB 的著名慣例之爭，見
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)）。本頁四條規則本身
（$\pm20\log_{10}N$、功率相加）都是**比值運算**：只要輸入輸出用同一個慣例，/2 或 /4 都會對消，
規則的數字不受慣例影響——這是為什麼記帳規則可以放心查表。

## 規則 1：理想 ×N 倍頻 —— 為什麼是 $+20\log_{10}N$

**第 1 步（把訊號寫成相位的函數）。** 用 [P1] Eq.(1), p.181 的分解，取正弦波形：

$$
V_{in}(t)=\cos\big(\Phi_{in}(t)\big),\qquad \Phi_{in}(t)=\omega_{ref}\,t+\phi_{in}(t)
$$

$\Phi_{in}$ 是**總相位**（rad），$\phi_{in}$ 是 excess phase（rad），$\omega_{ref}=2\pi f_{ref}$（rad/s）。

**第 2 步（理想倍頻器＝無記憶非線性＋帶通）。** 任何無記憶非線性 $g(\cdot)$ 作用在
$\cos\Phi$ 上，因為 $g(\cos\Phi)$ 對 $\Phi$ 是 $2\pi$ 週期函數，可展開成對 $\Phi$ 的傅立葉級數：

$$
g\big(\cos\Phi(t)\big)=\sum_{k=0}^{\infty}a_k\cos\big(k\,\Phi(t)+\theta_k\big)
$$

關鍵在引數：每一項都是「**瞬時總相位的整數倍** $k\Phi(t)$」——無記憶元件沒有時間概念，
只能對「當下的相位」動作，所以 excess phase 被**原封不動**地帶著走。

**第 3 步（帶通取第 $N$ 諧波）。** 以 $N f_{ref}$ 為中心的帶通濾波器取 $k=N$ 那一項：

$$
V_{out}(t)\propto\cos\big(N\Phi_{in}(t)\big)=\cos\big(N\omega_{ref}\,t+N\phi_{in}(t)\big)
\quad\Longrightarrow\quad \boxed{\ \phi_{out}(t)=N\,\phi_{in}(t)\ }
$$

這是**逐時刻**成立的恆等式——$\phi_{in}$ 的每一個頻率成分都被乘 $N$，沒有任何頻率選擇性。

**第 4 步（換成 PSD 與 dB）。** 相位乘 $N$（幅度），功率譜密度乘 $N^2$：

$$
S_{\phi,out}(f)=N^2\,S_{\phi,in}(f)\ \ [\text{rad}^2/\text{Hz}],\qquad
\mathcal{L}_{out}(f)=\mathcal{L}_{in}(f)+20\log_{10}N\ \ [\text{dBc/Hz}]
$$

第二式用了 $\mathcal{L}=\tfrac12 S_\phi$——輸入輸出**同一慣例**，$\tfrac12$ 對消，所以
$+20\log_{10}N$ 與 /2-vs-/4 慣例無關。$N=50$ 時 $+20\log_{10}50=+33.98$ dB $\approx+34$ dB。

- **物理意義**：倍頻**不創造雜訊**。它把「同一個絕對時間抖動」放大成 $N$ 倍的**角度**——
  輸出一個週期只有輸入的 $1/N$ 長，同樣的秒數誤差佔輸出週期的比例是 $N$ 倍。
- **offset 軸不動（常見錯誤）**：被乘 $N$ 的是**相位幅度**，不是相位起伏的節奏。
  $\mathcal{L}$ 曲線整條**垂直上移** $20\log_{10}N$，水平軸（offset $f$）完全不變。
- **Dimension check**：$N$ 無因次、$\phi$ 為 rad、$S_\phi$ 為 rad²/Hz、$20\log_{10}N$ 為 dB ✓。
- **時間抖動守恆**：$\Delta t_{out}=\dfrac{\phi_{out}}{2\pi N f_{ref}}=\dfrac{N\phi_{in}}{2\pi N f_{ref}}
  =\dfrac{\phi_{in}}{2\pi f_{ref}}=\Delta t_{in}$——以秒計的 edge 誤差**不變**（後面第 5 步用數值驗證）。

**失效條件**：(1) **小角近似**——$\sigma_{\phi,out}=N\sigma_{\phi,in}$，$N$ 大時（例如
$N=1000$，$+60$ dB）可能逼近 1 rad，$\mathcal{L}\approx\tfrac12 S_\phi$ 崩潰，載波能量重新分佈
成 Lorentzian（線寬擴散常數 $D$ 放大 $N^2$ 倍，見
[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)）；(2) **邊帶重疊**——offset 接近
$f_{ref}/2$ 時第 $N\pm1$ 諧波的裙帶混進帶通；(3) 真實倍頻器有自己的加成床（規則 4）。

## 規則 2：理想 ÷N 除頻 —— $-20\log_{10}N$ 的嚴格出處

[quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators) 頁在
÷2 產生 I/Q 那節直接引用了 $\mathcal{L}_{out}=\mathcal{L}_{in}-20\log_{10}N$；**這裡是那條式子的
嚴格推導之家**，兩頁數字一致（÷2 即 $-6.02$ dB）。

**第 1 步（輸入 edge 的時刻）。** 輸入第 $k$ 個上升過零點 $t_k$ 由總相位定義：
$\Phi_{in}(t_k)=2\pi k$。代入 $\Phi_{in}=\omega_{ref}t+\phi_{in}(t)$ 解出：

$$
t_k=k\,T_{ref}-\frac{\phi_{in}(t_k)}{\omega_{ref}}
\qquad\Longrightarrow\qquad
\delta t_k=-\frac{\phi_{in}(kT_{ref})}{\omega_{ref}}
$$

第二式用了「$\phi$ 慢變」（offset $\ll f_{ref}$）把 $\phi_{in}(t_k)$ 換成 $\phi_{in}(kT_{ref})$。
**Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。

**第 2 步（除頻器只丟 edge、不搬 edge）。** 理想 ÷N 是個 edge-picking 機器：每 $N$ 個輸入
edge 輸出一個，而且輸出 edge 的時刻**就是**被選中的那個輸入 edge 的時刻。所以絕對時間誤差
$\delta t$ **原封不動**傳到輸出：

$$
\delta t^{(out)}_m=\delta t_{mN}
$$

**第 3 步（把時間誤差摺回輸出載波的相位）。** 輸出載波 $\omega_{out}=\omega_{ref}/N$。輸出的
excess phase 由同一條相位定義反推（$\Phi_{out}(t'_m)=2\pi m$，$t'_m=mT_{out}+\delta t_m$）：

$$
\phi_{out}=-\,\omega_{out}\,\delta t^{(out)}
=\frac{\omega_{out}}{\omega_{ref}}\,\phi_{in}
\qquad\Longrightarrow\qquad
\boxed{\ \phi_{out}=\frac{\phi_{in}}{N}\ }
$$

**第 4 步（PSD 與 dB）。**

$$
S_{\phi,out}(f)=\frac{S_{\phi,in}(f)}{N^2},\qquad
\mathcal{L}_{out}(f)=\mathcal{L}_{in}(f)-20\log_{10}N
$$

÷2 即 $-20\log_{10}2=-6.02$ dB。**物理意義**：同一個秒數的抖動，攤在 $N$ 倍長的週期上，
角度小 $N$ 倍。與規則 1 完全對稱：×N 再 ÷N，$\mathcal{L}$ 回到原點，$\sigma_t$（秒）全程不變。

<NumericQuiz
  prompt="先自己算：理想 ÷2 除頻對 L(f) 的改變量 = ？（以 dB 作答，含負號）"
  answer={-6.02}
  tol={0.01}
  unit="dB"
  hint="ΔL = −20·log₁₀N，N=2。"
  solutionNote="−20·log₁₀(2) ≈ −6.02 dB（與規則 1 的 +20log₁₀N 完全對稱）。"
/>

**失效條件（兩個都重要）**：

1. **取樣摺疊（aliasing）**：$\phi_{out}$ 只在輸出 edge 的時刻有定義——這是一個以 $\sim f_{out}$
   取樣的系統。輸入相位雜訊中 offset 高於 $\sim f_{out}/2$ 的成分會**摺回**輸出頻帶；對平坦的
   寬頻 noise floor，除頻**賺不滿** $20\log_{10}N$（摺疊把功率疊回來）。乾淨的 $-20\log_{10}N$
   只對 offset $\ll f_{out}$ 的 close-in 雜訊成立。（外部文獻，非本站 5 篇 PDF；標準除頻器
   雜訊模型見本頁末 Egan。）
2. **divider 自身的床**：真實除頻器（CML latch、TSPC）有自己的加成床（規則 4），常常比
   「被除乾淨的訊號」高——除頻之後**輸出永遠不會好過 divider 自己的床**。

> **與 [P4] 的關係**：注入鎖定除頻器（ILFD）用 ISF 的第 2 諧波把 $2f_0$ 鎖到 $f_0$ 實作 ÷2
> （[P4]，Part II 的 frequency division，見
> [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)）。÷N 的相位記帳
> （$\phi/N$）對 ILFD 的載波路徑同樣成立；但 ILFD 靠近 lock range 邊緣時有自己的雜訊行為，
> 不在本頁的理想記帳內。

## 規則 3：過 PLL —— reference 走「×N＋低通」、VCO 走「高通」

PLL 是規則 1 的**閉迴路實作**：divider 把輸出拉回 $f_{ref}$ 比相，等於強迫「輸出相位
$=N\times$ 參考相位」——所以 reference 雜訊先吃 $+20\log_{10}N$（規則 1），**再**被閉環
低通 $\lvert H_{lp}\rvert^2$ 整形；VCO 自己的雜訊被高通 $\lvert H_{hp}\rvert^2$ 整形：

$$
S_{out}(f)=N^2\,S_{ref}(f)\,\lvert H_{lp}(f)\rvert^2+S_{vco}(f)\,\lvert H_{hp}(f)\rvert^2
\qquad[\text{rad}^2/\text{Hz}]
$$

兩條轉移函數（type-II 二階，$\omega_n,\zeta$）與完整五源預算已在
[pll_noise_budget](/06_design_insights/pll_noise_budget) 逐步推導並驗證，本頁**直接沿用不重推**
（該頁也含 charge-pump 床 $S_{cp}\lvert H_{lp}\rvert^2$；本頁 worked chain 為了聚焦四條規則，
把 CP 床併入「in-band 床」概念、數值上略去，標 illustrative）。查表用的 **brick-wall（磚牆）
記帳**是它的漸近版本：

- **in-band（$f\ll f_n$）**：$\lvert H_{lp}\rvert^2\to1$、$\lvert H_{hp}\rvert^2\to0$ ⇒
  $\mathcal{L}_{out}\approx\mathcal{L}_{ref}+20\log_{10}N$。
- **out-of-band（$f\gg f_n$）**：$\lvert H_{lp}\rvert^2\to0$、$\lvert H_{hp}\rvert^2\to1$ ⇒
  $\mathcal{L}_{out}\approx\mathcal{L}_{vco}$（VCO 自由跑的裙邊）。
- 切換點取 loop bandwidth $f_n$。

**Dimension check**：$S$ 皆 rad²/Hz、$N^2$ 與 $\lvert H\rvert^2$ 無因次 ✓。
brick-wall 版本好用但有一個著名的坑——**純二階 loop 的 reference 尾巴**，第 6 步用數值攤開。

## 規則 4：buffer / divider 的加成床 —— 功率相加，絕不是 dB 相加

**第 1 步（buffer 為什麼是「加成」）。** buffer 對 edge 做再生（regeneration）：輸入波形穿過
切換門檻的瞬間，buffer 內部 device 的雜訊電壓 $v_n$（V）疊在門檻上，把輸出 edge 推移

$$
\Delta t_{add}=\frac{v_n(t_k)}{SR}\qquad
\Big[\frac{\text{V}}{\text{V/s}}=\text{s}\Big]\ \checkmark
$$

（$SR$＝穿越門檻處的 slew rate，V/s。這與
[waveform_slope](/06_design_insights/waveform_slope) 的「斜率小處最敏感」是同一件事。）
$v_n$ 來自 buffer 自己的 device，與輸入時脈的相位**不相關**。

**第 2 步（不相關 ⇒ PSD 相加）。** 相位上這是純加法：

$$
\phi_{out}=\phi_{in}+\phi_{add}
\qquad\Longrightarrow\qquad
S_{\phi,out}(f)=S_{\phi,in}(f)+S_{buf}(f)
$$

（交叉項 $\langle\phi_{in}\phi_{add}\rangle=0$。）換成 dBc/Hz 就得到查表式——注意必須
**先轉線性、相加、再轉回 dB**：

$$
\boxed{\ \mathcal{L}_{out}(f)=10\log_{10}\Big(10^{\mathcal{L}_{in}(f)/10}+10^{\mathcal{L}_{buf}(f)/10}\Big)\ }
$$

兩個 $\mathcal{L}$ 都是同載波、同慣例的 SSB，$\mathcal{L}=\tfrac12 S_\phi$ 的 $\tfrac12$
在等式兩邊對消——所以直接用 $\mathcal{L}$ 記帳合法，與 /2-vs-/4 慣例無關。

**第 3 步（乘法 vs 加法——本頁最重要的分類）。**
規則 1–3 是**乘法**：把「進來的」相位整條縮放/整形，源頭乾淨、輸出就乾淨。
規則 4 是**加法**：buffer 加進**新的、獨立的**雜訊，**輸出永遠不會好過 buffer 自己的床**——
再乾淨的源頭過一級吵 buffer 就毀了。這就是「floor dominates」的意思。

**第 4 步（什麼時候床當家——dB 加法表）。** 設訊號比床高 $\Delta$ dB，代價是
$10\log_{10}(1+10^{-\Delta/10})$：

| $\Delta=\mathcal{L}_{in}-\mathcal{L}_{buf}$ | 輸出比 $\mathcal{L}_{in}$ 高 | 誰當家 |
|---|---|---|
| $+20$ dB（訊號高很多） | $+0.04$ dB | 床完全隱形 |
| $+10$ dB | $+0.41$ dB | 床開始可見 |
| $+6$ dB | $+0.97$ dB | — |
| $+3$ dB | $+1.76$ dB | — |
| $0$ dB（一樣高） | $+3.01$ dB | 各半 |
| $-10$ dB（訊號低於床） | 輸出 $\approx\mathcal{L}_{buf}+0.41$ | **床當家，輸出被鉗住** |

**第 5 步（平坦床 ⇒ 白 phase noise ⇒ 一條好記的 jitter 公式）。** 平坦的
$\mathcal{L}_{buf}$ 就是白相位雜訊，積分頻寬 $B$（Hz）內它自己貢獻的 rms jitter：

$$
\sigma_{t,add}=\frac{1}{2\pi f_0}\sqrt{2\cdot10^{\mathcal{L}_{buf}/10}\cdot B}
$$

（$2\times$ 是 $\mathcal{L}\to S_\phi$ 的小角換算，規範公式 16；再用規範公式 19 積分。）
數值：$\mathcal{L}_{buf}=-155$ dBc/Hz、$B\approx100$ MHz、$f_0=2.5$ GHz：
$\sigma_{t,add}=\sqrt{2\times3.16\times10^{-16}\times10^8}\,/(2\pi\times2.5\times10^9)
=2.51\times10^{-4}/1.571\times10^{10}=16.0$ fs。
**Dimension check**：$\sqrt{[\text{rad}^2/\text{Hz}]\cdot[\text{Hz}]}=[\text{rad}]$，
$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。（這個 16.0 fs 等下會在 worked chain 的分解裡
原封不動出現。）

<NumericQuiz
  prompt="先自己算：buffer 平坦床 L_buf=−155 dBc/Hz、積分頻寬 B=100 MHz、f₀=2.5 GHz 時 σ_t,add = ？（以 fs 作答）"
  answer={16.0}
  tol={0.02}
  unit="fs"
  hint="σ_t,add = √(2·10^(L_buf/10)·B) / (2π f₀)。"
  solutionNote="√(2×3.16×10⁻¹⁶×10⁸)/(2π×2.5×10⁹) ≈ 16.0 fs（這個數字會在下方 worked chain 的分解裡再次出現）。"
/>

四條規則的常數先用一個可核對的 Python 塊釘死（`# ->` 後面就是實跑輸出）：

```python
import numpy as np
print(round(20*np.log10(50), 2))   # -> 33.98
print(round(20*np.log10(2), 2))    # -> 6.02
print(round(10*np.log10(1 + 10**(-20/10)), 2))  # -> 0.04
print(round(10*np.log10(1 + 10**(-10/10)), 2))  # -> 0.41
print(round(10*np.log10(1 + 10**(-6/10)), 2))   # -> 0.97
print(round(10*np.log10(1 + 10**(-3/10)), 2))   # -> 1.76
print(round(10*np.log10(1 + 10**(0/10)), 2))    # -> 3.01
```

## 第 5 步：守恆量——理想 ×N/÷N 下 $\sigma_t$（秒）不變

把規則 1 與 2 的結論並排看：×N 時 $\phi\times N$ 而載波 $f_0\times N$；÷N 時 $\phi/N$ 而
$f_0/N$。代進 $\Delta t=\phi/(2\pi f_0)$（規範公式 17），兩個 $N$ 對消：

$$
\sigma_{t,out}=\frac{\sigma_{\phi,out}}{2\pi f_{0,out}}
=\frac{N^{\pm1}\,\sigma_{\phi,in}}{2\pi\,N^{\pm1} f_{0,in}}=\sigma_{t,in}
$$

**以秒計的時間抖動是理想倍頻／除頻的不變量。** 變差（或變好）的 $\mathcal{L}$ 只是
「同一個秒數誤差換算成角度」的匯率變了。這給你一個超好用的 sanity check：鏈上任何一段
「純 ×N/÷N、沒有加成床」的路徑，頭尾用**同一積分頻帶**算出來的 $\sigma_t$ 必須一樣。
用 worked chain 的數字驗證（5 GHz 那級 vs 理想 ÷2 後的 2.5 GHz，都不含 buffer）：

```python
import numpy as np
from simulations.common.noise_utils import integrate_rms_jitter
f = np.logspace(4, 8, 20001)
L5G = np.where(f <= 1e6, -126.02, -148.0 - 20*np.log10(f/1e6))
st5, _ = integrate_rms_jitter(f, L5G, f0=5e9, fmin=1e4, fmax=1e8)
st25, _ = integrate_rms_jitter(f, L5G - 6.02, f0=2.5e9, fmin=1e4, fmax=1e8)
print(round(st5*1e15, 1))    # -> 22.5
print(round(st25*1e15, 1))   # -> 22.5
```

兩個 22.5 fs 一模一樣——÷2 讓 $\mathcal{L}$ 好了 6 dB，卻**一顆 fs 都沒省**。
對 SerDes 這其實是壞消息的另一面：換算成 UI 時，$\sigma_t$ 不變而 UI 變長，
所以除頻後「佔 UI 的比例」確實變小——省的是**比例**，不是秒數。

## 第 6 步：worked chain——100 MHz → ×50 PLL → 5 GHz → ÷2 → 2.5 GHz → buffer

現在把四條規則串成一條真實形狀的鏈。所有數值是 representative／illustrative
（非特定矽製程），但與站內 canonical 完全一致。

```mermaid
flowchart LR
  REF["100 MHz 參考<br/>L = -160 dBc/Hz 床"] --> PLL["PLL ×50<br/>f_n = 1 MHz"]
  PLL --> OUT5["5 GHz<br/>in-band ref+34 dB<br/>out-of-band VCO"]
  OUT5 --> DIV["÷2<br/>-6.02 dB"]
  DIV --> OUT25["2.5 GHz"]
  OUT25 --> BUF["輸出 buffer<br/>床 -155 dBc/Hz"]
  BUF --> CLK["最終時脈"]
```

**參數表：**

| 量 | 值 | 單位 | 說明 |
|---|---|---|---|
| $f_{ref}$ | 100 | MHz | 參考頻率 |
| $\mathcal{L}_{ref}$ | $-160$（平坦床） | dBc/Hz | 乾淨參考的 far-out 床（illustrative；真實晶體 close-in 會翹，本頁只看 $\ge10$ kHz） |
| $N$ | 50 | — | $100\ \text{MHz}\to5\ \text{GHz}$ |
| $f_n,\ \zeta$ | 1 MHz、0.707 | Hz、— | type-II 二階 loop（沿用 [pll_noise_budget](/06_design_insights/pll_noise_budget)） |
| VCO | $\mathcal{L}(1\,\text{MHz})=-148$、$1/f^2$ | dBc/Hz | 站內 canonical 例 B（[P1] Eq.(21), p.185，/4 SSB 慣例） |
| ÷N | 2 | — | $5\to2.5$ GHz |
| $\mathcal{L}_{buf}$ | $-155$（平坦床） | dBc/Hz | 輸出 buffer 的加成床 |
| 積分頻帶 | $10^4$–$10^8$ | Hz | 最終 jitter 積分 |

### 6.1 每級的 $\mathcal{L}$：in-band 看 100 kHz、out-of-band 看 10 MHz

逐步手算（brick-wall 記帳）：

1. **參考**：平坦床 ⇒ 兩個 offset 都是 $-160.00$。
2. **PLL 輸出（5 GHz）**：
   - in-band（$100\ \text{kHz}\ll f_n$）：規則 3 ⇒ $-160+20\log_{10}50=-160+33.98=-126.02$。
   - out-of-band（$10\ \text{MHz}\gg f_n$）：VCO 自由跑，$1/f^2$ 由 1 MHz 錨點外推：
     $-148-20\log_{10}(10)= -168.00$。
3. **÷2（2.5 GHz）**：規則 2，整條 $-6.02$ dB ⇒ $-132.04$ 與 $-174.02$。
4. **輸出 buffer**：規則 4，與 $-155$ 床做功率相加：
   - 100 kHz：訊號 $-132.04$ 比床**高** 22.96 dB ⇒ 代價 $\approx0.02$ dB ⇒ $-132.02$（床隱形）。
   - 10 MHz：訊號 $-174.02$ 比床**低** 19 dB ⇒ **床當家** ⇒ $-154.95$（被鉗在 $-155$ 附近）。

| 節點 | 載波 | $\mathcal{L}$(100 kHz) [dBc/Hz] | $\mathcal{L}$(10 MHz) [dBc/Hz] | 當家的規則 |
|---|---|---|---|---|
| 參考 | 100 MHz | $-160.00$ | $-160.00$ | — |
| PLL ×50 輸出 | 5 GHz | $-126.02$ | $-168.00$ | 規則 3（in-band ref+34；out-of-band VCO） |
| ÷2 之後 | 2.5 GHz | $-132.04$ | $-174.02$ | 規則 2（$-6.02$） |
| ＋buffer（最終） | 2.5 GHz | $-132.02$ | $-154.95$ | 規則 4（10 MHz 處床當家） |

同一張表用可核對的 Python 釘死：

```python
import numpy as np
L_ref = -160.0
L_in = L_ref + 20*np.log10(50)               # 規則 1/3：in-band = ref + 20logN
print(round(L_in, 2))                        # -> -126.02
L_vco_10M = -148.0 - 20*np.log10(10e6/1e6)   # VCO 1/f²：由 1 MHz 錨點外推到 10 MHz
print(round(L_vco_10M, 2))                   # -> -168.0
div = -20*np.log10(2)                        # 規則 2
print(round(L_in + div, 2))                  # -> -132.04
print(round(L_vco_10M + div, 2))             # -> -174.02
def padd(*Ls): return 10*np.log10(sum(10**(L/10) for L in Ls))
print(round(padd(L_in + div, -155.0), 2))    # -> -132.02
print(round(padd(L_vco_10M + div, -155.0), 2))  # -> -154.95
```

### 6.2 最終 2.5 GHz 時脈的積分 jitter（10 kHz–100 MHz）

最終曲線的 brick-wall 模型：in-band 床 $-132.04$（到 $f_n=1$ MHz）、之後接被 ÷2 的 VCO 裙邊
（1 MHz 錨點 $-148-6.02=-154.02$、$1/f^2$），全程再與 $-155$ buffer 床功率相加。
用規範公式 18/19 手積（$\mathcal{L}\to S_\phi=2\times10^{\mathcal{L}/10}$）：

$$
\begin{aligned}
\text{in-band 床:}\quad
\sigma_{\phi,1}^2&=2\times10^{-13.204}\times(10^6-10^4)=1.250\times10^{-13}\times9.9\times10^5
=1.238\times10^{-7}\ \text{rad}^2,\\[2pt]
\text{VCO 裙邊:}\quad
\sigma_{\phi,2}^2&=2\times10^{-15.402}\,(10^6)^2\!\left(\frac{1}{10^6}-\frac{1}{10^8}\right)
=7.9\times10^{-10}\ \text{rad}^2,\\[2pt]
\text{buffer 床:}\quad
\sigma_{\phi,3}^2&=2\times10^{-15.5}\times(10^8-10^4)=6.32\times10^{-8}\ \text{rad}^2,\\[4pt]
\sigma_\phi&=\sqrt{1.238\times10^{-7}+7.9\times10^{-10}+6.32\times10^{-8}}
=4.33\times10^{-4}\ \text{rad},\\[2pt]
\sigma_t&=\frac{\sigma_\phi}{2\pi\times2.5\times10^9}=27.6\ \text{fs}.
\end{aligned}
$$

**Dimension check**：$[\text{rad}^2/\text{Hz}]\times[\text{Hz}]=[\text{rad}^2]$ ✓；
$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。用 `noise_utils` 驗證（同一慣例 $S_\phi=2\mathcal{L}$）：

```python
import numpy as np
from simulations.common.noise_utils import integrate_rms_jitter
f = np.logspace(4, 8, 20001)
L_core = np.where(f <= 1e6, -132.04, -154.02 - 20*np.log10(f/1e6))
L_tot = 10*np.log10(10**(L_core/10) + 10**(-155.0/10))
st, sp = integrate_rms_jitter(f, L_tot, f0=2.5e9, fmin=1e4, fmax=1e8)
print(round(st*1e15, 1))   # -> 27.6
print(round(sp*1e6, 1))    # -> 433.4
```

**誰貢獻了這 27.6 fs？**（`simulations/fig_clock_chain.py` 實跑分解，功率比）

| 來源 | 單獨 $\sigma_t$ | 佔 $\sigma_\phi^2$ 比例 |
|---|---|---|
| in-band 床（reference $\times N^2$） | 22.4 fs | 65.9 % |
| buffer 床 | 16.0 fs | 33.7 % |
| VCO 裙邊 | 1.78 fs | 0.42 % |
| **RSS 總和** | **27.6 fs** | 100 % |

> **這張表是本頁最重要的設計訊息**：這條鏈的 jitter 由「被 $\times N^2$ 抬高的 in-band 床」
> 與「不起眼的 buffer 床」平分天下；那顆漂亮的 $-148$ dBc/Hz VCO 幾乎**隱形**（0.42 %）。
> 花力氣再改善 VCO 是白工——記帳先做，力氣才花得對地方。
> （buffer 的 16.0 fs 正是規則 4 第 5 步那條公式的數字。）

### 6.3 對應模擬圖

**完整 script：`simulations/fig_clock_chain.py`**（跑法：專案根目錄下
`PYTHONPATH=. python3 simulations/fig_clock_chain.py`，會列印本頁所有 `# ->` 數字並產圖）。

![時脈鏈記帳：左＝各級 SSB phase noise（黑實線＝最終 2.5 GHz 時脈、紅虛線＝type-II 完整整形）；右＝最終時脈的累積 rms jitter（brick-wall 27.6 fs vs 整形 44.0 fs）](/figures/clock_chain_budget.png)

**如何解讀**：左圖藍線是 5 GHz 的 brick-wall（in-band $-126$ 平台＋1 MHz 後的 VCO 裙邊）、
綠線整條下移 6.02 dB（÷2）、橘點線是 $-155$ buffer 床、黑粗線是最終輸出——100 kHz 處
$-132.0$、10 MHz 處被床鉗在 $-154.9$。右圖是「從 10 kHz 積到 $f$」的累積 jitter：
in-band 床在 1 MHz 前就累積了 22 fs，之後 buffer 床慢慢把總數推到 27.6 fs；
紅虛線（完整 type-II 整形）在 $f_n$ 附近與之後持續高於 brick-wall——這就是下一步要攤開的坑。

## 第 7 步：誠實對照——brick-wall 查表 vs 完整 type-II 整形

brick-wall 是查表級近似。用
[pll_noise_budget](/06_design_insights/pll_noise_budget) 的 $\lvert H_{lp}\rvert^2$ 實際算
（`pll_utils`，$f_n=1$ MHz、$\zeta=0.707$），兩個 offset 的差異一目了然：

- **in-band（100 kHz）**：整形版 $-131.9$ vs brick-wall $-132.0$——只差 0.1 dB
  （$\lvert H_{lp}\rvert^2$ 在 $f_n/10$ 處的輕微 peaking）。查表**可靠** ✓。
- **out-of-band（10 MHz）**：整形版 $-148.0$ vs brick-wall $-154.9$——**差 7 dB**！

原因是 type-II 二階閉環的零點讓 $\lvert H_{lp}\rvert^2$ 在 $f\gg f_n$ 只以 $-20$ dB/dec 滾降
（$\lvert H_{lp}\rvert^2\approx(2\zeta f_n/f)^2$），所以被 $\times N^2$ 抬高的 reference 床有一條
**$-20$ dB/dec 的尾巴**漏到 out-of-band；而 VCO 裙邊**也是** $-20$ dB/dec——兩條線平行，
**差距是常數、永遠追不上**：

```python
import numpy as np
from simulations.common.pll_utils import H_lowpass_mag2
S_refN2 = 2 * 10**(-126.02/10)          # N²·S_ref（in-band 床的 S_phi）[rad²/Hz]
lp = H_lowpass_mag2(10e6, 1e6)          # |H_lp|² @ 10 MHz, fn = 1 MHz
L_refpath = 10*np.log10(0.5 * S_refN2 * lp)
print(round(L_refpath, 1))              # -> -143.0
print(round(L_refpath - (-168.0), 1))   # -> 25.0
```

reference 尾巴在 10 MHz 是 $-143.0$ dBc/Hz（5 GHz 載波），比 VCO 的 $-168$ **高 25 dB**——
且因兩者同斜率，這 25 dB 在**所有** out-of-band offset 都成立。查表那格
「out-of-band ＝ VCO」對純二階 loop 而言**根本到不了**。對積分 jitter 的後果
（`fig_clock_chain.py` 實跑）：

| 模型 | 最終 $\sigma_t$（10 kHz–100 MHz） |
|---|---|
| brick-wall 查表 | 27.6 fs |
| type-II 二階完整整形 | 44.0 fs（$+59\%$） |
| 二階＋第 3 極點 @ 3 MHz（illustrative） | 38.6 fs |

**怎麼修**：真實合成器正是為此在 loop filter 加**第三極點**（以及更高階的 post-filter），
把 ref 尾巴改成 $-40$ dB/dec 以上；上表第三列示範一顆 3 MHz 極點就把傷害砍掉三分之一
（極點位置與 loop 穩定性的取捨屬標準 PLL 文獻，外部文獻，非本站 5 篇 PDF）。

**再誠實一層**：這條鏈的 $f_n=1$ MHz 本來就**不是** jitter 最佳解——in-band 床（$-126$）與
VCO 裙邊的交叉點在 $79.6$ kHz，遠低於 1 MHz。用
[pll_noise_budget](/06_design_insights/pll_noise_budget) 的 U 形曲線方法對本鏈掃 $f_n$
（整形模型、第 3 極點跟隨在 $3f_n$）：最低點在 $f_n^\*\approx53$ kHz、$\sigma_t\approx19.6$ fs。
**查表記帳（本頁）告訴你每一級的帳；最佳化 loop（該頁）告訴你帳該怎麼改**——兩件事，別混。

## design knobs 清單

| 旋鈕 | 作用在哪條規則 | 怎麼調 |
|---|---|---|
| 除頻比 $N$（參考頻率） | 規則 1/3：in-band 床 $\propto N^2$ | 本鏈 65.9% 的 jitter 功率來自 ref$\times N^2$；用更高 $f_{ref}$ 降 $N$ 最有效 |
| buffer 床 $\mathcal{L}_{buf}$ | 規則 4 | 33.7% 來自一級 $-155$ 床；加大 buffer 電流/斜率（$\Delta t=v_n/SR$）壓床；級數越少越好 |
| ÷N 放哪裡 | 規則 2＋4 | ÷N 只除「它上游」的雜訊；放在吵源**之後**才享受 $-20\log_{10}N$，其下游 buffer 床照原值相加 |
| loop BW $f_n$ | 規則 3 | 本鏈最佳 $f_n^\*\approx53$ kHz（非 1 MHz）；交叉點 79.6 kHz 是第一手感 |
| loop 階數（第 3 極點） | 規則 3 | 純二階的 ref 尾巴與 VCO 平行（本例恆 $+25$ dB）；加高階極點才能讓 out-of-band 真的交給 VCO |
| VCO $\Gamma_{rms}/q_{max}$ | 規則 3 的 $S_{vco}$ | 本鏈 VCO 僅 0.42%——**先看記帳再決定要不要動它**（ISF 旋鈕見 [tank_swing](/06_design_insights/tank_swing)、[lc_vs_ring](/06_design_insights/lc_vs_ring)） |

## 與 SerDes 的關聯

最終 2.5 GHz 時脈的 $\sigma_t=27.6$ fs 直接餵進
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) 的 eye/BER 機器：
若這顆 clock 打 5 Gb/s 的 half-rate link（UI $=200$ ps），BER $=10^{-12}$（$Q^{-1}\approx7.03$，
站內 canonical）的 RJ 開銷是 $2\times7.03\times27.6\ \text{fs}=0.39$ ps $=0.19\%$ UI——很健康；
但注意時脈樹每多一級 buffer 就多一份規則 4 的床（功率相加），fan-out 大的樹光是 buffer
就能把預算吃光。free-running 段的累積 jitter（[P2] Eq.(8), p.792 的
$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$）一旦進入 PLL/CDR 的 loop 就被高通截斷——
這條鏈裡「誰 free-run、誰被鎖」決定哪些雜訊要積、哪些不用（同頁第 6 步）。

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 小角近似（$\sigma_\phi\ll1$ rad） | $\mathcal{L}=\tfrac12 S_\phi$、$\pm20\log_{10}N$ 查表成立 | 大 $N$ 倍頻後 $\sigma_\phi\times N$ 變大 → Lorentzian 重分佈（[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)） |
| offset $\ll f_{ref}/2$（×N）、$\ll f_{out}/2$（÷N） | 乾淨的 $\pm20\log_{10}N$ | 邊帶重疊／取樣摺疊，平坦床賺不滿 $-20\log_{10}N$ |
| 各級雜訊不相關 | 規則 4 功率相加 | 共用 supply/bias 的相關雜訊（如 PSIJ）要含交叉項，可能同相疊加 |
| brick-wall PLL 記帳 | in-band 查表誤差 $\sim0.1$ dB | 純二階 loop：ref 尾巴與 VCO 平行（本例恆差 25 dB），out-of-band 那格可錯 7 dB、$\sigma_t$ 低估 59% |
| 理想 edge-picking divider | $-20\log_{10}N$ | 真實 divider 自身床（規則 4）先當家；ILFD 近 lock-range 邊緣另計（[P4]） |

## 重點回顧

- 四條規則：**×N 加 $20\log_{10}N$**（$\phi_{out}=N\phi_{in}$，offset 軸不動）；
  **÷N 減 $20\log_{10}N$**（edge-picking，時間誤差原封不動、角度除 $N$）；
  **PLL**＝reference 走 $N^2\lvert H_{lp}\rvert^2$、VCO 走 $\lvert H_{hp}\rvert^2$
  （轉移函數沿用 [pll_noise_budget](/06_design_insights/pll_noise_budget)）；
  **buffer/divider 床＝功率相加**，$\mathcal{L}_{out}=10\log_{10}(10^{\mathcal{L}_{in}/10}+10^{\mathcal{L}_{buf}/10})$。
- 守恆量：理想 ×N/÷N 下 **$\sigma_t$（秒）不變**（本例兩端都是 22.5 fs）；÷N 省的是「佔 UI 的比例」，不是秒。
- worked chain（100 MHz→×50→5 GHz→÷2→2.5 GHz→buffer）：100 kHz 處 $-160\to-126.02\to-132.04\to-132.02$；
  10 MHz 處 $-160\to-168.00\to-174.02\to-154.95$（床當家）。
- 最終積分 jitter（10 kHz–100 MHz）＝**27.6 fs**；分解＝ref$\times N^2$ 床 65.9%＋buffer 床 33.7%＋VCO 0.42%——
  **記帳先行，別盲目升級 VCO**。
- 誠實對照：純 type-II 二階 loop 的 ref 尾巴與 VCO 裙邊**平行**（本例恆 $+25$ dB），
  整形後 $\sigma_t=44.0$ fs（比查表高 59%）；加第 3 極點（3 MHz）→ 38.6 fs；
  本鏈 jitter 最佳 loop BW 其實是 $f_n^\*\approx53$ kHz（$\sigma_t\approx19.6$ fs）。
- 慣例紀律：規則全是比值/加法運算，/2-vs-/4 對消；唯一吃慣例的是 VCO 錨點
  （$-148$＝[P1] Eq.(21) 的 /4 SSB；時域 /2 給 $-145$）。

## 延伸閱讀

- PLL 轉移函數與五源預算（本頁規則 3 的完整推導處）：[pll_noise_budget](/06_design_insights/pll_noise_budget)、[lab_13_pll_cdr_transfer](/04_simulation_labs/lab_13_pll_cdr_transfer)
- ÷2 產生 quadrature 與 ILFD（引用本頁規則 2）：[quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators)、[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)
- 把 $\sigma_t$ 接到 eye/BER：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- 大 $N$ 倍頻後小角近似崩潰的去處：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- VCO 錨點 $-148$ dBc/Hz 的來源與 /2-vs-/4：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- 本頁模擬 script：`simulations/fig_clock_chain.py`

## 外部文獻（不在下載的 5 篇 PDF 內）

- **×N/÷N 的 $\pm20\log_{10}N$、divider 取樣摺疊、加成床**：標準頻率合成記帳
  （外部文獻，非本站 5 篇 PDF；任何 frequency-synthesis 教材皆有）。標準參考：
  W. F. Egan, *Frequency Synthesis by Phase Lock*, 2nd ed., Wiley, New York, 2000；
  B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, Upper Saddle River, NJ, 2012。
- 本站 5 篇 PDF 提供的是鏈上「源」的物理：[P1]（VCO 的 $\mathcal{L}$ 與 ISF）、
  [P2]（ring 的 $\kappa\sqrt{\Delta t}$ 累積）、[P3]/[P4]（注入鎖定與 ILFD 除頻機制）。
