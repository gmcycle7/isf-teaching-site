---
title: 擴散常數字典：κ、D、線寬、ADEV、1/f² 係數是同一個數字
description: 以相位方差成長率 κ²=Γrms²·Si/(2qmax²)（[P2] Eq.11/12）為主角，逐步推導它換上五件衣服——ring jitter 常數 κ、相位擴散常數 D（兩種慣例）、Lorentzian 3-dB 線寬 κ²/(2π)、1/f² phase PSD 係數 2κ²、white-FM Allan deviation κ/(2πf₀√τ)——並把每個 factor-of-2 慣例（單邊/雙邊、Var=D|t| vs 2D|t|、SSB /2 vs /4）逐一對帳，用 lab_23 一次模擬五路驗證，canonical κ²=0.125 rad²/s。
---

# 擴散常數字典：κ、D、線寬、ADEV、1/f² 係數是同一個數字

> 先備：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) · [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) · [allan_variance](/02_foundations/allan_variance) ｜ 接下來：[capstone_lc_end_to_end](/03_isf_core_theory/capstone_lc_end_to_end)

同一顆自由振盪器的白噪相位擴散，在五個不同社群的嘴裡是五個「不同」的數字：

- **ring / jitter 圈**（[P2]）講 $\kappa$：「累積 jitter 常數多少 $\sqrt{\text{s}}$？」
- **理論物理 / Demir 圈**講 $D$：「phase diffusion constant 多少 $\text{rad}^2/\text{s}$？」
- **雷射 / 頻譜圈**講 **linewidth**：「3-dB 線寬多少 Hz？」
- **RF / IC 圈**講 $\mathcal{L}$：「$1/f^2$ 裙邊在 1 MHz offset 是多少 dBc/Hz？」
- **時鐘 / 計量圈**講 **ADEV**：「$\sigma_y(\tau)$ 的 white-FM 段在 $\tau=1$ s 是多少？」

這頁要證明：**這五個數字是同一個物理量換了五件衣服**，並給出完整、每一個
factor-of-2 都對帳過的換算鏈。40 年來我看過最多的振盪器規格錯誤，不是算錯
$\Gamma_{rms}$、不是量錯 PSD，而是**在這五件衣服之間換裝時掉了一個 2**。
所以本頁的每一步都會明講：這個 2 來自哪個慣例（單邊/雙邊？$\mathrm{Var}=D|t|$ 還是
$2D|t|$？SSB $/2$ 還是 $/4$？），並在文末用 `lab_23` **一次模擬、五路萃取**同一個數字來驗收。

> **物理直覺（先講結論）**：白噪把相位推成隨機漫步（Wiener process，維納過程），
> 漫步只有**一個**自由參數——「方差每秒長多快」。我們把它記作
> $\kappa^2\equiv d\,\mathrm{Var}[\Delta\phi]/dt$（單位 $\text{rad}^2/\text{s}$）。
> 你之後量到的一切——jitter 怎麼隨 $\sqrt{\Delta t}$ 長、載波多胖、裙邊多高、
> 時鐘多穩——都只是這**一個速率**投影到不同儀器上的影子。字典的功能：給你任何
> 一件衣服的數字，馬上換出其他四件。

---

## 第 0 步：主角只有一個——相位方差成長率 κ²

一切從 [P1] Eq.(11), p.182 的相位積分開始（推導見
[convolution_derivation](/03_isf_core_theory/convolution_derivation)）：

$$
\phi(t)=\frac{1}{q_{max}}\int_{0}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau .
$$

其中 $\phi$ 是 excess phase（rad）、$\Gamma$ 是 ISF（無因次）、$q_{max}$ 是節點最大
電荷擺幅（C）、$i_n$ 是 noise 電流（A）。我們要算 $\mathrm{Var}[\phi(t)]$，逐步來。

**第 (i) 步：白噪的自相關——第一個 factor-of-2（單邊 PSD 記帳）。**
電路慣例中 $S_i\equiv\overline{i_n^2}/\Delta f$ 是**單邊** PSD（單位 $\text{A}^2/\text{Hz}$，
只對 $f\ge0$ 定義；datasheet 與 [P1][P2] 都是這個）。單邊 PSD 還原自相關要走
Wiener–Khinchin（見 [stochastic_noise_basics](/02_foundations/stochastic_noise_basics)）：

$$
R_i(\tau)=\int_0^{\infty}S_i\cos(2\pi f\tau)\,df=\frac{S_i}{2}\,\delta(\tau).
$$

那個 $\tfrac12$ 不是物理，是「把雙邊功率折到單邊」的記帳：同一總功率，單邊密度是
雙邊的 2 倍，所以還原 $\delta$ 強度時要除回來。**這是本頁第一個、也是最容易被忘記的 2。**

**第 (ii) 步：方差 = 雙重積分 + delta 收縮。**

$$
\mathrm{Var}[\phi(t)]=\frac{1}{q_{max}^2}\int_0^t\!\!\int_0^t\Gamma(\omega_0\tau_1)\Gamma(\omega_0\tau_2)\,\underbrace{\frac{S_i}{2}\delta(\tau_1-\tau_2)}_{R_i}\,d\tau_1 d\tau_2
=\frac{S_i}{2q_{max}^2}\int_0^t\Gamma^2(\omega_0\tau)\,d\tau .
$$

**第 (iii) 步：$\Gamma^2$ 的時間平均 = $\Gamma_{rms}^2$。** 只要觀察時間跨很多週期
（$t\gg T=1/f_0$），$\Gamma^2$ 的振盪平均掉、只剩它的均方值：

$$
\int_0^t\Gamma^2(\omega_0\tau)\,d\tau\;\xrightarrow[t\gg T]{}\;\Gamma_{rms}^2\,t .
$$

**結果（本頁主角）**：

$$
\boxed{\ \mathrm{Var}[\Delta\phi(t)]=\kappa^2\,|t|,\qquad \kappa^2\equiv\frac{\Gamma_{rms}^2}{2\,q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}\ \ [\text{rad}^2/\text{s}]\ }
$$

這**逐字**就是 **[P2] Eq.(11), p.793**（單一白噪源、$\Delta T=nT$ 或 $nT/2$ 時的
phase jitter：$\sigma_{\Delta\phi}^2=\frac{\Gamma_{rms}^2}{2q_{max}^2}\frac{\overline{i_n^2}}{\Delta f}\Delta T$，已核實）。

- **物理意義**：$\kappa^2$ 是「相位方差每秒長多少 $\text{rad}^2$」。它就是隨機漫步的
  **步伐速率**——之後五件衣服全部只由它決定。
- **單位檢查**：$[\Gamma_{rms}^2]=1$；$[S_i]=\text{A}^2/\text{Hz}=\text{A}^2\text{s}$；
  $[q_{max}^2]=\text{C}^2=\text{A}^2\text{s}^2$。相除得
  $\text{A}^2\text{s}/(\text{A}^2\text{s}^2)=1/\text{s}$，rad 無因次，故 $\text{rad}^2/\text{s}$ ✓。
- **canonical 數值**（例 B 的數字，全站一致）：$\Gamma_{rms}=0.5$、$q_{max}=1$ pC、
  $S_i=10^{-24}\ \text{A}^2/\text{Hz}$：

$$
\kappa^2=\frac{0.25}{2\times(10^{-12})^2}\times10^{-24}=\frac{0.25}{2}=0.125\ \text{rad}^2/\text{s}.
$$

  真・理想 LC（$\Gamma_{rms}=1/\sqrt2$，見 [rms_isf](/03_isf_core_theory/rms_isf)）則是
  $\kappa^2=0.25\ \text{rad}^2/\text{s}$——正好 2 倍，因為 $\Gamma_{rms}^2$ 差 2 倍。
- **適用條件**：白噪、平穩、單一源、$t\gg T$、LTV 小訊號。flicker（$1/f$）源**不適用**——
  它的方差長得比線性快（對應 $1/f^3$ 裙邊與 ADEV floor，見
  [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)）。

---

## 衣服一：κ —— ring / jitter 圈的講法（[P2]）

[P2] Eq.(8), p.792 把自由振盪器的累積 jitter 寫成隨機漫步：

$$
\sigma=\kappa\sqrt{\Delta t}.
$$

把第 0 步的結果開根號，$\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$，比例常數正是
**[P2] Eq.(12), p.793（已核實）**：

$$
\boxed{\ \kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\frac{1}{2}\cdot\frac{\overline{i_n^2}}{\Delta f}}\ \ [\text{rad}/\sqrt{\text{s}}]\ }
$$

> **κ 的單位陷阱（誠實註記，已核實）**：[P2] 的內文把 Eq.(8) 講成 **timing** jitter
> $\sigma_{\Delta t}$，但印出來的 Eq.(12) **沒有 $\omega_0$**（對照原始 PDF 逐字確認），
> 量綱是 $\text{rad}/\sqrt{\text{s}}$——所以 Eq.(12) 的 $\kappa$ 其實是**相位版**常數，
> 與 Eq.(10), p.793 定義的 phase jitter（$\sigma_{\Delta\phi}=2\pi\sigma_{\Delta t}/T=\omega_0\sigma_{\Delta t}$）
> 和 Eq.(11) 完全自洽。要講**時間版**就除以 $\omega_0$：
> $\sigma_{\Delta t}=\kappa_t\sqrt{\Delta t}$、$\kappa_t=\kappa/\omega_0=\kappa/(2\pi f_0)$，
> 單位 $\sqrt{\text{s}}$。
> 全站他頁（如 [paper_002 深讀](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)）寫
> $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$、$\kappa$ 單位 $\sqrt{\text{s}}$ 時，指的就是這個
> $\kappa_t$。兩者只差一個 $\omega_0$，物理相同。

- **與 κ² 的關係**：$\kappa=\sqrt{\kappa^2}$——衣服一就是主角本人開根號。
- **單位檢查**：$\dfrac{1}{\text{C}}\cdot\sqrt{\text{A}^2\text{s}}=\dfrac{\text{A}\sqrt{\text{s}}}{\text{A}\,\text{s}}=\dfrac{1}{\sqrt{\text{s}}}$ ✓（rad 無因次）；
  $\kappa_t$：$(1/\sqrt{\text{s}})/(1/\text{s})=\sqrt{\text{s}}$ ✓。
- **canonical 數值**：$\kappa=\sqrt{0.125}=0.354\ \text{rad}/\sqrt{\text{s}}$。掛上 $f_0=5$ GHz：
  $\kappa_t=0.354/(2\pi\times5\times10^9)=1.125\times10^{-11}\ \sqrt{\text{s}}$。
  隔 $\Delta t=1\ \mu\text{s}$ 量兩個 edge：
  $\sigma_{\Delta t}=1.125\times10^{-11}\times\sqrt{10^{-6}}=1.13\times10^{-14}\ \text{s}\approx11.3$ fs。
  **dimension check**：$\sqrt{\text{s}}\times\sqrt{\text{s}}=\text{s}$ ✓。

```python
import numpy as np
gamma_rms, qmax, Si, f0 = 0.5, 1e-12, 1e-24, 5e9
kappa = gamma_rms / qmax * np.sqrt(0.5 * Si)        # [P2] Eq.(12)
print(round(kappa, 4))  # -> 0.3536
print(f"{kappa/(2*np.pi*f0)*np.sqrt(1e-6)*1e15:.2f}")  # -> 11.25 fs（積分 1 µs）
```

---

## 衣服二：D —— 擴散常數的兩種慣例（本頁的對帳核心）

「diffusion constant $D$」在文獻裡有**兩種定義**，差一個 2。這一節就是規格書
（規範 11.2）與 [P2] Eq.(11) 的**正面對帳**——任務只有一個：講清楚 $\kappa^2$
在每種慣例下等於什麼。

**慣例甲（rate 慣例）**：直接把 $D$ 定成方差成長率——

$$
\mathrm{Var}[\Delta\phi(t)]=D_{\text{甲}}\,|t|\quad\Longrightarrow\quad \kappa^2=D_{\text{甲}}.
$$

**慣例乙（Demir／雷射慣例，[E2] Demir 2000 與雷射線寬文獻的寫法）**：模仿布朗運動
$\langle x^2\rangle=2Dt$，把 2 寫在外面——

$$
\mathrm{Var}[\Delta\phi(t)]=2D_{\text{乙}}\,|t|\quad\Longrightarrow\quad \kappa^2=2D_{\text{乙}},\qquad D_{\text{乙}}=\frac{\kappa^2}{2}.
$$

兩者只是**命名**不同，物理（方差長多快）一樣。用 ISF 物理量寫出來：

$$
D_{\text{甲}}=\frac{\Gamma_{rms}^2}{2q_{max}^2}\frac{\overline{i_n^2}}{\Delta f}=0.125\ \text{rad}^2/\text{s},\qquad
D_{\text{乙}}=\frac{\Gamma_{rms}^2}{4q_{max}^2}\frac{\overline{i_n^2}}{\Delta f}=0.0625\ \text{rad}^2/\text{s}\quad(\text{canonical}).
$$

> **與規範 11.2／[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 的對帳（重要；v5 已依本頁修正）**：
> 規範 11.2 **v3 版**曾寫 $D=\Gamma_{rms}^2 S_i/(2q_{max}^2)$（canonical $D=0.125$、真 LC $0.25$）
> ——這個**數值**正是 $\kappa^2$，也就是**慣例甲**的 $D$（方差成長率本人）。但規範同一段
> 又寫 $\mathrm{Var}[\Delta\phi]=2D|t|$（慣例乙的方差式）。兩句話**不能同時成立**：
> 若 $D=0.125$ 且 $\mathrm{Var}=2D|t|$，方差就得每秒長 $0.25\ \text{rad}^2$，
> 與 [P2] Eq.(11)（每秒 $0.125\ \text{rad}^2$）矛盾。
> **模擬裁決**（`lab_23`，圖 (a)）：用 canonical 常數合成 ISF 加權白噪相位，量到
> $\mathrm{Var}[\Delta\phi(\tau)]/\tau=0.1252\ \text{rad}^2/\text{s}$——落在 $\kappa^2\tau$ 線上、
> **不在** $2\times0.125\,\tau$ 線上。結論：**$D=0.125$ 這個 canonical 值是對的，但它是
> 慣例甲的 $D$（$=\kappa^2$）；配它的方差式應為 $\mathrm{Var}=D|t|$**。若堅持用慣例乙的
> $\mathrm{Var}=2D|t|$，則 $D$ 要改讀 $0.0625$。這不影響任何 scaling，只影響下一節線寬的
> 絕對值（見衣服三的誠實註記）。

- **單位**：兩種 $D$ 都是 $\text{rad}^2/\text{s}$（等效 $1/\text{s}$）✓。
- **一句話字典**：$\kappa^2=D_{\text{甲}}=2D_{\text{乙}}$。報 $D$ 給別人時，**先問對方的
  $\mathrm{Var}$ 式子裡有沒有那個 2**。

---

## 衣服三：Lorentzian 3-dB 線寬

[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 已推過整條機制
（高斯特徵函數 → 指數自相關 → Wiener–Khinchin → Lorentzian，屬 [E2] Demir 2000
外部文獻）。這裡只做「把 $\kappa^2$ 代進去」的最後一哩，每步帶單位：

**第 (i) 步：失憶包絡。** 載波自相關的包絡是
$\langle\cos\Delta\phi\rangle=e^{-\frac12\mathrm{Var}[\Delta\phi(\tau)]}$（高斯特徵函數）。
代入主角 $\mathrm{Var}=\kappa^2|\tau|$：

$$
R_x(\tau)=\frac12\cos(\omega_0\tau)\,e^{-\kappa^2|\tau|/2}.
$$

（用慣例乙寫就是熟悉的 $e^{-D_{\text{乙}}|\tau|}$——同一條指數。）

**第 (ii) 步：雙邊指數 → Lorentzian。** $e^{-a|\tau|}$ 的傅立葉變換是
$2a/(a^2+\Omega^2)$，半高發生在 $\Omega=\pm a$。這裡 $a=\kappa^2/2$（單位 $1/\text{s}$），
所以繞載波的半高**半**寬（HWHM）是 $\Delta\omega_{\text{HWHM}}=\kappa^2/2$ rad/s，
半高**全**寬（FWHM）是它的兩倍：

$$
\Delta\omega_{3\mathrm{dB}}=\kappa^2\ \text{rad/s}\quad\Longrightarrow\quad
\boxed{\ \Delta f_{3\mathrm{dB}}=\frac{\kappa^2}{2\pi}=\frac{D_{\text{乙}}}{\pi}=\frac{D_{\text{甲}}}{2\pi}=\frac{\Gamma_{rms}^2}{4\pi\,q_{max}^2}\frac{\overline{i_n^2}}{\Delta f}\ \ [\text{Hz}]\ }
$$

- **單位檢查**：$[\kappa^2/2\pi]=(1/\text{s})/1=\text{Hz}$ ✓。
- **canonical 數值**：$\Delta f_{3\mathrm{dB}}=0.125/(2\pi)=19.9$ mHz（代表值
  $\Gamma_{rms}=0.5$）；真・理想 LC（$\kappa^2=0.25$）則 $39.8$ mHz。
  `lab_23` 直接量合成載波的頻譜：Lorentzian 擬合給 **20.0 mHz**、半高直讀給
  **20.3 mHz**（圖 (b)），與 $\kappa^2/2\pi=19.9$ mHz 吻合。
- **外部交叉檢查**（標準結果）：白色**頻率**雜訊單邊 PSD 為 $S_\nu^0$（$\text{Hz}^2/\text{Hz}$）
  時，線寬 $\Delta f_{3\mathrm{dB}}=\pi S_\nu^0$。由衣服四將得 $S_\nu^0=\kappa^2/(2\pi^2)$，
  代入：$\pi\cdot\kappa^2/(2\pi^2)=\kappa^2/(2\pi)$ ✓ 同一答案。（此關係式屬外部文獻，
  非本站 5 篇 PDF：G. Di Domenico, S. Schilt, and P. Thomann, "Simple approach to the
  relation between laser frequency noise and laser line shape," Applied Optics,
  vol. 49, no. 25, pp. 4801–4807, 2010。）

> **誠實對帳（線寬數值 ×2 註記；v5 已修正）**：
> [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 例 2 與
> [capstone_lc_end_to_end](/03_isf_core_theory/capstone_lc_end_to_end) 站⑥**v3 版曾**引用
> $\Delta f_{3\mathrm{dB}}=D/\pi$ 搭配 $D=0.125$／$0.25$，得 **40 mHz／80 mHz**
> （例 1 同法得 1257 Hz）。依本頁對帳：那個 $D$ 值是**慣例甲**（$=\kappa^2$），而
> $D/\pi$ 是**慣例乙**的公式——甲值塞進乙式，線寬大了 $2\times$。嚴格推導與 `lab_23`
> 實測都給 $\kappa^2/(2\pi)$：**19.9 mHz（代表值）／39.8 mHz（真 LC）／628 Hz
> （$-100$ dBc/Hz@1MHz 錨點）**。注意 `lab_18` 的模擬本身沒有錯——它從頭到尾用
> 慣例乙（增量方差 $2D\,dt$ 配 $\Delta f=D/\pi$），錯不在 Lorentzian 機制，只在
> 「ISF 量 → $D$」那一步的慣例混用。scaling（$\propto\Gamma_{rms}^2 S_i/q_{max}^2$）
> 完全不受影響。**v5 已依本頁裁決完成修正**：規範 11.2 改為 $D=\Gamma_{rms}^2S_i/(4q_{max}^2)=\kappa^2/2$；
> lorentzian_linewidth 例 1/例 2 → 628 Hz／20 mHz；capstone 站⑥ → 40 mHz（HWHM 20 mHz）；
> lab_22 同步更新。本頁的 MC 裁決（$0.1252$ rad²/s、$20.0$ mHz）就是修正依據。

---

## 衣服四：1/f² phase PSD 係數與 $\mathcal{L}$

**第 (i) 步：$\dot\phi$ 是白的。** 主角說方差每秒長 $\kappa^2$，等價於
$\dot\phi$ 的自相關 $R_{\dot\phi}(\tau)=\kappa^2\delta(\tau)$。它的**雙邊** PSD 是
$\kappa^2$、**單邊** PSD 是 $2\kappa^2$（單位 $\text{rad}^2/\text{s}^2/\text{Hz}=\text{rad}^2/\text{s}$）。
**第二個 factor-of-2：單邊 vs 雙邊**，跟第 0 步那個 $S_i/2$ 是同一家人。

**第 (ii) 步：積分器除 $\Delta\omega^2$。** $\phi=\int\dot\phi$，PSD 除以
$|j\Delta\omega|^2$：

$$
\boxed{\ S_\phi(f)=\frac{2\kappa^2}{(2\pi f)^2}\ \ [\text{rad}^2/\text{Hz}]\ \ (\text{單邊})\ }\qquad
S_\phi^{\text{雙邊}}(f)=\frac{\kappa^2}{(2\pi f)^2}.
$$

寫成 $S_\phi=b_{-2}/f^2$ 的係數形：$b_{-2}=\kappa^2/(2\pi^2)$（單位 $\text{rad}^2\cdot\text{Hz}$）。
這條正是 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
的時域乾淨版 $S_\phi=\Gamma_{rms}^2S_i/(q_{max}^2\Delta\omega^2)$——代
$\kappa^2=\Gamma_{rms}^2S_i/(2q_{max}^2)$ 即得，完全一致 ✓。

**第 (iii) 步：$\mathcal{L}$——第三個 factor-of-2（SSB /2 vs /4，全站已明講）。**

$$
\mathcal{L}_{/2}(\Delta f)=\frac{S_\phi}{2}=\frac{\kappa^2}{\Delta\omega^2}
\qquad\text{vs}\qquad
\mathcal{L}_{\text{[P1] Eq.(21)}}(\Delta f)=\frac{\kappa^2}{2\,\Delta\omega^2}.
$$

前者是小角 PM 的乾淨結果（規範 Eq.16），後者是 [P1] Eq.(21), p.185 的 SSB $/4$
記帳（$\Gamma_{rms}^2S_i/(4q_{max}^2\Delta\omega^2)$），兩者差 3 dB——這就是全站
$-145$ vs $-148$ dBc/Hz 並存、各自有註的那件事（見
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 的
factor-of-2 教學註記）。它也是 Lorentzian 遠端尾巴：衣服三的歸一化 Lorentzian
在 $\Delta f\gg\Delta f_{3\mathrm{dB}}$ 時 $\to\kappa^2/\Delta\omega^2=\mathcal{L}_{/2}$ ✓。

- **canonical 數值**（$\Delta f=1$ MHz，$\Delta\omega=6.283\times10^6$ rad/s、
  $\Delta\omega^2=3.948\times10^{13}$）：
  $\mathcal{L}_{/2}=0.125/3.948\times10^{13}=3.17\times10^{-15}\Rightarrow-145.0$ dBc/Hz；
  $\mathcal{L}_{/4}=1.58\times10^{-15}\Rightarrow-148.0$ dBc/Hz——**正是**例 B 的招牌數字 ✓。
  $b_{-2}=0.125/(2\pi^2)=6.33\times10^{-3}\ \text{rad}^2\cdot\text{Hz}$。
- **單位檢查**：$[2\kappa^2/\Delta\omega^2]=(1/\text{s})/(1/\text{s}^2)=\text{s}=1/\text{Hz}$，
  掛上 rad² 得 $\text{rad}^2/\text{Hz}$ ✓。
- **反向查字典**（量到裙邊 → 主角）：$\kappa^2=\mathcal{L}_{/2}\cdot\Delta\omega^2$。
  例：datasheet 級的 $-100$ dBc/Hz@1MHz（例 C 錨點）給
  $\kappa^2=10^{-10}\times3.948\times10^{13}=3.95\times10^{3}\ \text{rad}^2/\text{s}$，
  線寬 $\kappa^2/2\pi=628$ Hz、$\kappa_t=\sqrt{3948}/(2\pi\cdot5\times10^9)=2.0\times10^{-9}\sqrt{\text{s}}$
  （1 µs 累積 2 ps）——一個數字，整本字典跟著出來。

---

## 衣服五：white-FM Allan deviation

[allan_variance](/02_foundations/allan_variance) 第 1 步給了轉接頭
$S_y=(f^2/f_0^2)S_\phi$。代入衣服四：

$$
S_y(f)=\frac{f^2}{f_0^2}\cdot\frac{2\kappa^2}{(2\pi f)^2}=\frac{\kappa^2}{2\pi^2 f_0^2}\equiv h_0\quad(\text{白色 FM，與 }f\text{ 無關})\ [\text{1/Hz}].
$$

順帶把衣服三用到的頻率雜訊 PSD 也拿到了：$S_\nu^0=f_0^2\,h_0=\kappa^2/(2\pi^2)$
（$\text{Hz}^2/\text{Hz}$）——跟 $b_{-2}$ 同一個數，巧合嗎？不是：$S_\nu=f^2S_\phi$
對 $1/f^2$ 裙邊本來就是常數。

white FM 的 ADEV 閉式（[allan_variance](/02_foundations/allan_variance) 第 3 步的核
積分結果，標準頻率計量結果，IEEE Std 1139）：$\sigma_y^2(\tau)=h_0/(2\tau)$，故

$$
\boxed{\ \sigma_y(\tau)=\sqrt{\frac{h_0}{2\tau}}=\frac{\kappa}{2\pi f_0\,\sqrt{\tau}}=\frac{\kappa_t}{\sqrt{\tau}}\ }
$$

- **單位檢查**：$[\kappa/(2\pi f_0\sqrt\tau)]=\dfrac{1/\sqrt{\text{s}}}{(1/\text{s})\cdot\sqrt{\text{s}}}=\dfrac{\text{s}}{\text{s}}=1$ ✓（$\sigma_y$ 無因次）。
- **canonical 數值**（$f_0=5$ GHz）：$h_0=0.125/(2\pi^2\times(5\times10^9)^2)=2.53\times10^{-22}\ /\text{Hz}$；
  $\sigma_y(1\,\text{s})=1.13\times10^{-11}$、$\sigma_y(1\,\text{ms})=3.56\times10^{-10}$。
  **交叉檢查**：[allan_variance](/02_foundations/allan_variance) 例 2 用 $-100$ dBc/Hz
  得 $\sigma_y(1\,\text{ms})=6.3\times10^{-8}$；我們的 $-145$ dBc/Hz 低 45 dB，
  $\sigma_y$ 應低 $\sqrt{10^{4.5}}=178$ 倍：$6.3\times10^{-8}/178=3.5\times10^{-10}$ ✓ 對上。
- **字典閉環（最漂亮的一步）**：把 ADEV 乘回 $\tau$ 得時間版的漂移
  $\tau\,\sigma_y(\tau)=\kappa_t\sqrt{\tau}$——**正是衣服一的累積 timing jitter**
  $\sigma_{\Delta t}=\kappa_t\sqrt{\Delta t}$。五件衣服繞一圈回到起點，字典自洽 ✓。

---

## 字典總表（一眼換裝）

主角：$\kappa^2=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$。
canonical 行用 $\Gamma_{rms}=0.5$、$q_{max}=1$ pC、$S_i=10^{-24}\ \text{A}^2/\text{Hz}$、
$f_0=5$ GHz（真・理想 LC 把 $\kappa^2$ 換成 $0.25$：線寬、$h_0$、$\mathcal{L}$ 線性跟著 ×2，
$\kappa$ 類 ×$\sqrt2$）。

| 衣服 | 用 $\kappa^2$ 寫 | 單位 | canonical 值 | 誰在講 | 出處 |
|---|---|---|---|---|---|
| 方差成長率（主角） | $\mathrm{Var}[\Delta\phi]=\kappa^2\vert t\vert$ | $\text{rad}^2/\text{s}$ | $0.125$ | 理論 | [P2] Eq.(11) p.793 |
| ① $\kappa$（相位） | $\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$ | $\text{rad}/\sqrt{\text{s}}$ | $0.354$ | ring/jitter | [P2] Eq.(8) p.792, Eq.(12) p.793 |
| ① $\kappa_t$（時間） | $\kappa_t=\kappa/(2\pi f_0)$ | $\sqrt{\text{s}}$ | $1.13\times10^{-11}$ | ring/jitter | [P2] Eq.(10) p.793 換算 |
| ② $D$（慣例甲） | $D_{\text{甲}}=\kappa^2$（$\mathrm{Var}=D\vert t\vert$） | $\text{rad}^2/\text{s}$ | $0.125$ | rate 慣例（v3 規範曾誤標此值為 $D$） | 對帳見衣服二 |
| ② $D$（慣例乙） | $D_{\text{乙}}=\kappa^2/2$（$\mathrm{Var}=2D\vert t\vert$） | $\text{rad}^2/\text{s}$ | $0.0625$ | Demir/雷射；**本站規範 11.2（v5）** | [E2] Demir 2000 |
| ③ 3-dB 線寬 | $\Delta f_{3\mathrm{dB}}=\kappa^2/(2\pi)$ | Hz | $19.9$ mHz | 雷射/頻譜 | 衣服三；[E2] |
| ④ $S_\phi$ 係數 | $S_\phi=2\kappa^2/(2\pi f)^2$（單邊） | $\text{rad}^2/\text{Hz}$ | $b_{-2}=6.33\times10^{-3}$ | RF/IC | [P1] Eq.(21) p.185（$/4$ 版） |
| ④ $\mathcal{L}$@1MHz | $\mathcal{L}_{/2}=\kappa^2/\Delta\omega^2$；$\mathcal{L}_{/4}=\kappa^2/2\Delta\omega^2$ | dBc/Hz | $-145.0$／$-148.0$ | RF/IC | 規範 Eq.16；[P1] Eq.(21) |
| ⑤ white-FM ADEV | $\sigma_y(\tau)=\kappa/(2\pi f_0\sqrt{\tau})$ | — | $1.13\times10^{-11}$@1s | 時鐘/計量 | [E1] Allan 1966；IEEE 1139 |

換裝口訣：**「開根號穿①、除以 2 穿乙②、除 $2\pi$ 穿③、乘 2 除 $\Delta\omega^2$ 穿④、
除 $\omega_0$ 再除 $\sqrt\tau$ 穿⑤。」** 每個 2 的出處：①→無、②→$\mathrm{Var}$ 定義、
③→FWHM 是全寬（HWHM×2）、④→單邊 PSD（另有 SSB $/2$ vs $/4$ 的 3 dB）、⑤→Allan 定義的 $\tfrac12$
被 white-FM 核積分吃成 $h_0/2\tau$。

---

## 對應模擬圖（lab_23：一次模擬、五路萃取）

`simulations/lab_23_diffusion_dictionary.py` 用 [P1] Eq.(11) 的離散版合成**一段**
ISF 加權白噪相位（$\Gamma=-\sqrt2\,\Gamma_{rms}\sin\theta$、$\Gamma_{rms}=0.5$、
$q_{max}=1$ pC、$S_i=10^{-24}\ \text{A}^2/\text{Hz}$ 全部用真值；載波用正規化
$f_0^{\text{sim}}=16$ Hz——線寬**不吃 $f_0$**，只有 ADEV 吃，其 $f_0$ 縮放在模擬內
自我驗證後再解析換到 5 GHz），總長 $131072$ s，然後**四路獨立**萃取同一個 $\kappa^2$：

![同一個 κ²=0.125 rad²/s 的四件量測衣服：相位方差斜率、Lorentzian 線寬、white-FM ADEV、1/f² phase PSD](/figures/diffusion_dictionary.png)

| 項目 | 值 | 說明 |
|---|---|---|
| 模型 | toy / illustrative（非 transistor-level） | [P1] Eq.(11) 離散積分，Wiener 相位 |
| $\Gamma_{rms},q_{max},S_i$ | $0.5$、$1$ pC、$10^{-24}\ \text{A}^2/\text{Hz}$ | canonical 例 B 真值 |
| 理論 $\kappa^2$ | $0.125\ \text{rad}^2/\text{s}$ | [P2] Eq.(11)/(12) |
| (a) 方差斜率 | $0.1252$ | 落在 $\kappa^2\tau$，**不在** $2\times0.125\,\tau$（紅點線被否證） |
| (b) 線寬 | 擬合 $20.0$ mHz、半高直讀 $20.3$ mHz | 理論 $\kappa^2/2\pi=19.9$ mHz |
| (c) ADEV | $\hat\kappa^2=0.1254$；斜率 $-1/2$ | $\sigma_y=\kappa/(2\pi f_0^{\text{sim}}\sqrt\tau)$ |
| (d) $S_\phi$ | $\hat\kappa^2=0.1254$ | 平台 $S_\phi(2\pi f)^2/2$ |

**如何解讀**：(a) 藍點（量測方差）貼黑虛線 $\kappa^2\tau$、紅點線（若規範的
$\mathrm{Var}=2D|t|$ 配 $D=0.125$ 成立該走的線）整條高 2 倍——這就是衣服二對帳的
模擬裁決。(b) 載波近端轉平、半高全寬 20 mHz；同一個 $\kappa^2$。(c) ADEV 一條
$-1/2$ 斜率直線，水平截距還原 $\kappa$。(d) $1/f^2$ 裙邊的係數還原 $2\kappa^2$（單邊）。
**四個儀器、一個數字。**

核心 Python（完整 script：`simulations/lab_23_diffusion_dictionary.py`；
ADEV 估計式逐字沿用 `lab_19_allan.py` 的 `overlapping_adev`；跑法
`PYTHONPATH=. python3 simulations/lab_23_diffusion_dictionary.py`）：

```python
import numpy as np
from simulations.common.noise_utils import white_noise

GAMMA_RMS, QMAX, SI, F0_REAL = 0.5, 1e-12, 1e-24, 5e9
KAPPA2 = GAMMA_RMS**2 * SI / (2 * QMAX**2)      # [P2] Eq.(11)/(12)
print(f"{KAPPA2:.4f}")  # -> 0.1250

FS, N, F0_SIM = 64.0, 2**23, 16.0
t = np.arange(N) / FS
gamma = -np.sqrt(2.0) * GAMMA_RMS * np.sin(2 * np.pi * F0_SIM * t)  # rms=0.5
i_n = white_noise(N, SI, FS, np.random.default_rng(23))   # 單邊 PSD = SI
phi = np.cumsum(gamma * i_n / FS / QMAX)                  # [P1] Eq.(11) 離散版

# (a) 方差斜率 -> kappa^2（同時否證 2*0.125*t；全 script 對多個 lag 取中位數得 0.1252）
m = 640                                                    # tau = 10 s
print(f"{np.mean((phi[m:] - phi[:-m])**2) / (m / FS):.4f}")  # -> 0.1251

# (b) Lorentzian 線寬：1/S 對 offset^2 線性擬合 -> FWHM = 2*sqrt(c0/c1)
#     （見完整 script；擬合 20.03 mHz、半高直讀 20.26 mHz）
print(f"{KAPPA2 / (2 * np.pi) * 1e3:.2f}")  # -> 19.89 mHz 理論

# (c)(d) ADEV 與 S_phi 萃取（見完整 script）
#     qhat_ADEV = 0.1254 ; qhat_Sphi = 0.1254

# 換到 canonical 5 GHz 的整本字典
dw = 2 * np.pi * 1e6
print(f"{10*np.log10(KAPPA2/dw**2):.1f}")        # -> -145.0 dBc/Hz (/2)
print(f"{10*np.log10(KAPPA2/(2*dw**2)):.1f}")    # -> -148.0 dBc/Hz ([P1] /4)
print(f"{np.sqrt(KAPPA2):.4f}")                  # -> 0.3536 rad/sqrt(s)
print(f"{np.sqrt(KAPPA2)/(2*np.pi*F0_REAL):.4e}")  # -> 1.1254e-11 sqrt(s)
print(f"{np.sqrt(KAPPA2/(4*np.pi**2*F0_REAL**2)/1.0):.3e}")  # -> 1.125e-11 ADEV@1s
print(f"{KAPPA2/(2*np.pi**2):.3e}")              # -> 6.333e-03（b₋₂ 係數）
```

---

## 一條 canonical 例子貫穿五件衣服

> **例（嚴格格式：題目 → 逐步代入帶單位 → 結果 → dimension check → 一行 Python）**：
> $\Gamma_{rms}=0.5$、$q_{max}=1$ pC、$S_i=10^{-24}\ \text{A}^2/\text{Hz}$、$f_0=5$ GHz。
> 求 (1) $\kappa$ 與 1 µs 累積 jitter、(2) 兩種 $D$、(3) 線寬、(4) $\mathcal{L}(1\text{MHz})$
> 兩種慣例、(5) $\sigma_y(1\,\text{s})$。

1. **主角**：$\kappa^2=\dfrac{0.25}{2\times10^{-24}}\times10^{-24}=0.125\ \text{rad}^2/\text{s}$。
2. **衣服一**：$\kappa=\sqrt{0.125}=0.354\ \text{rad}/\sqrt{\text{s}}$；
   $\kappa_t=0.354/(2\pi\cdot5\times10^9)=1.13\times10^{-11}\ \sqrt{\text{s}}$；
   $\sigma_{\Delta t}(1\,\mu\text{s})=1.13\times10^{-11}\sqrt{10^{-6}}=11.3$ fs。
3. **衣服二**：$D_{\text{甲}}=0.125$、$D_{\text{乙}}=0.0625\ \text{rad}^2/\text{s}$。
4. **衣服三**：$\Delta f_{3\mathrm{dB}}=0.125/(2\pi)=19.9$ mHz。
5. **衣服四**：$\mathcal{L}_{/2}=0.125/3.948\times10^{13}=3.17\times10^{-15}\Rightarrow-145.0$ dBc/Hz；
   $\mathcal{L}_{/4}=-148.0$ dBc/Hz。
6. **衣服五**：$h_0=0.125/(2\pi^2\cdot2.5\times10^{19})=2.53\times10^{-22}\ /\text{Hz}$；
   $\sigma_y(1\,\text{s})=\sqrt{2.53\times10^{-22}/2}=1.13\times10^{-11}$。

**Dimension check 串**：$\text{rad}^2/\text{s}\to\sqrt{\ }\to\text{rad}/\sqrt{\text{s}}\to\div\,\omega_0\to\sqrt{\text{s}}\to\times\sqrt{\Delta t}\to\text{s}$ ✓；
$\text{rad}^2/\text{s}\div2\pi=\text{Hz}$ ✓；
$\text{rad}^2/\text{s}\div(\text{rad/s})^2=\text{rad}^2\cdot\text{s}=\text{rad}^2/\text{Hz}$ ✓。

```python
import numpy as np
k2 = 0.5**2 * 1e-24 / (2 * 1e-12**2); dw = 2*np.pi*1e6; f0 = 5e9
print(round(k2,4), round(k2/(2*np.pi)*1e3,1), round(10*np.log10(k2/dw**2),1),
      f"{np.sqrt(k2)/(2*np.pi*f0):.2e}")  # -> 0.125 19.9 -145.0 1.13e-11
```

---

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 白噪主導（white FM 段） | 五件衣服一個 $\kappa^2$ 互換 | flicker 段：$\mathrm{Var}$ 非線性成長、ADEV 出 floor、線型非純 Lorentzian，字典失效（每件衣服各自要 $1/f^3$ 版本） |
| $t\gg T$、多週期平均 | $\Gamma^2\to\Gamma_{rms}^2$ | 短於一週期時方差有 cyclostationary 漣波（lab_23 用 overlapping 平均消掉） |
| 單一（或不相關疊加）噪源 | $\kappa^2$ 各源相加 | 相關源（supply/substrate）：$\sigma\propto\Delta t$（[P2] Eq.(9)），不是 $\sqrt{\Delta t}$ |
| 小角 / 線性化（衣服四） | $\mathcal{L}\approx S_\phi/2$ | 近載波 $\Delta f\lesssim\Delta f_{3\mathrm{dB}}$：$1/f^2$ 假發散，要用衣服三的 Lorentzian |
| 自由振盪（無迴路） | 純隨機漫步 | 進 PLL 後低頻被高通掉：$\mathrm{Var}$ 飽和、ADEV 轉彎（見 [pll_noise_budget](/06_design_insights/pll_noise_budget)） |
| 報告他人數據 | 先問清楚慣例 | 沒對帳就換裝 → 典型 ×2（$\mathrm{Var}$ 定義）或 3 dB（SSB $/2$ vs $/4$）錯誤 |

## 與哪些 paper／公式對應

- **[P2] Eq.(8), p.792**（$\sigma=\kappa\sqrt{\Delta t}$）、**Eq.(10), p.793**（phase jitter 定義）、
  **Eq.(11), p.793**（$\sigma_{\Delta\phi}^2=\Gamma_{rms}^2S_i\Delta T/(2q_{max}^2)$，主角本人，已核實）、
  **Eq.(12), p.793**（$\kappa=(\Gamma_{rms}/q_{max})\sqrt{S_i/2}$，無 $\omega_0$，已核實）。
- **[P1] Eq.(11), p.182**（相位積分，第 0 步起點）、**Eq.(21), p.185**（衣服四的 SSB $/4$ 版）。
- **外部文獻（非本站 5 篇 PDF）**：[E2] A. Demir, A. Mehrotra, J. Roychowdhury, IEEE TCAS-I,
  vol. 47, no. 5, pp. 655–674, May 2000（衣服二乙慣例與衣服三機制）；[E1] D. W. Allan,
  Proc. IEEE, vol. 54, no. 2, pp. 221–230, Feb. 1966 與 IEEE Std 1139（衣服五）；
  G. Di Domenico, S. Schilt, P. Thomann, Applied Optics, vol. 49, no. 25, pp. 4801–4807,
  2010（$\Delta f_{3\mathrm{dB}}=\pi S_\nu^0$ 交叉檢查）。
- 站內：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（$/2$ vs $/4$）、
  [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)（衣服三機制）、
  [allan_variance](/02_foundations/allan_variance)（衣服五積分核）、
  [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)（衣服一的 toy 版）。

## 重點回顧

- 白噪相位擴散只有**一個**自由參數：$\kappa^2=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$
  （[P2] Eq.(11)/(12)；canonical $0.125\ \text{rad}^2/\text{s}$、真 LC $0.25$）。
- 五件衣服：$\kappa=\sqrt{\kappa^2}$（rad/√s；時間版 $\kappa_t=\kappa/\omega_0$）、
  $D_{\text{甲}}=\kappa^2$／$D_{\text{乙}}=\kappa^2/2$、$\Delta f_{3\mathrm{dB}}=\kappa^2/2\pi=19.9$ mHz、
  $S_\phi=2\kappa^2/\Delta\omega^2$（$\mathcal{L}$：$-145.0$ ($/2$)／$-148.0$ ($/4$) dBc/Hz@1MHz）、
  $\sigma_y=\kappa/(2\pi f_0\sqrt\tau)=1.13\times10^{-11}$@1s(5 GHz)。閉環：$\tau\sigma_y(\tau)=\kappa_t\sqrt\tau$ 回到累積 jitter。
- **三個 factor-of-2 家族**：單邊/雙邊 PSD（$S_i/2$、$2\kappa^2$）、$\mathrm{Var}=D|t|$ vs $2D|t|$
  （$\kappa^2=D_{\text{甲}}=2D_{\text{乙}}$）、SSB $/2$ vs $/4$（3 dB）。換裝前先對帳。
- 規範 11.2 v3 版的 $D=0.125$ 其實是**慣例甲之值（$=\kappa^2$）**；配 $\mathrm{Var}=2D|t|$ 或 $\Delta f=D/\pi$
  會多算 2 倍——lab_23 實測方差斜率 $0.1252$、線寬 $20.0$ mHz 裁決之。**v5 已全站修正**（規範 11.2 改 $/(4q_{max}^2)$；lorentzian／capstone／lab_22 數值同步更新）。
- lab_23：一次模擬、四路萃取（$0.1252$／$0.1258$／$0.1254$／$0.1254$）同一個 $0.125$——
  **四個儀器、一個數字、五件衣服**。

## 延伸閱讀

- 衣服三的完整機制（特徵函數 → Lorentzian）：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- 衣服五的完整推導（$\sin^4$ 核與斜率表）：[allan_variance](/02_foundations/allan_variance)
- 衣服四的上游（$1/f^2$ 與 $/2$ vs $/4$）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- 頻域 ↔ 時域 jitter 總表：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- 把整本字典用在一顆理想 LC 上：[capstone_lc_end_to_end](/03_isf_core_theory/capstone_lc_end_to_end)
- 衣服一的 toy 隨機漫步：[lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
- 外部文獻完整 citation：[references](/99_appendix/references)
