---
title: Leeson 模型推導與 ISF 對照
description: 從 tank 熱雜訊、feedback、品質因數 Q 出發逐步建立 Leeson 經驗相位雜訊模型，再與 [P1] Eq.(21),(23),(24) 的 ISF 結果逐項對照（Q↔Γrms/qmax、F 經驗 vs ISF 物理、1/f³ corner），再用 [P1] Sec.III-F Eq.(28)–(29) 示範 ISF 一般式如何收斂回 LTI 特例（含 Craninckx–Steyaert 2× 差），並嵌入 Leeson vs ISF 疊圖。明標 Leeson 1966 不在下載的 5 篇 PDF 內。
---

# Leeson 模型推導與 ISF 對照

> **先備／See also**：[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)（$Q$ 的能量定義、tank 為何整形 $1/f^2$）、[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)（$4kTR$ 熱雜訊與 PSD 基礎）、[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（ISF 版 $1/f^2$ 推導）｜**接下來**：[symmetry](/06_design_insights/symmetry)（用 $c_0$ 對稱性壓 $1/f^3$ corner）、[references](/99_appendix/references)（外部文獻 [E1]）

在 Hajimiri–Lee 的 ISF 理論（[P1], 1998）出現之前，工程師估振盪器相位雜訊靠的是 **Leeson 模型**（1966）。它是一條**半經驗（semi-empirical）**公式：物理骨架（tank 濾波 + 回授）是對的，但裡面塞了一個「不知道從哪來、要靠量測 fit」的雜訊因子 $F$。這頁把 Leeson 從頭推一遍，然後**逐項**對回 ISF 的封閉式——你會看到 ISF 理論「解釋了 Leeson 為什麼長那樣，並把那個神祕的 $F$ 換成可計算的物理量」。

> **誠實聲明（請先讀）**：**Leeson 模型來自 [E1] D. B. Leeson, "A Simple Model of Feedback Oscillator Noise Spectrum," Proc. IEEE, vol. 54, no. 2, pp. 329–330, Feb. 1966**，**不在本站下載的 5 篇 PDF 內**。本頁只憑標準文獻知識做背景與對照；卷期/頁碼/DOI **已用網路查證**（DOI 10.1109/PROC.1966.4682）；$F$（noise figure）本就是 Leeson 模型的**經驗擬合參數**（依實作而異），非固定常數。相對地，本頁右半的 ISF 公式（[P1] Eqs.(21),(23),(24)）是 5 篇 PDF 內、已核的權威式。

這頁要回答：

1. Leeson 式的每一項（floor、$1/f^2$、$1/f^3$）物理上從哪來？
2. 為什麼斜率是 $1/f^2$ 與 $1/f^3$，corner 在哪？
3. Leeson 的 $Q$、$F$、$\omega_{1/f^3}$ 對應 ISF 的哪些量？哪些是 ISF 講得更清楚的？
4. [P1] 自己怎麼證明「既有 LTI 模型是 ISF 的簡化特例」（Sec.III-F Eq.(28)–(29)）？那個著名的 2× 差從哪來？

> **物理直覺（先講結論）**：Leeson 把振盪器想成「一個被熱雜訊持續餵食、又被高 $Q$ tank 窄帶濾波的回授系統」。三件事疊起來：(1) 放大器/tank 注入一塊**白色雜訊地板**（$2FkT/P_s$）；(2) 因為是**自治振盪器**，載波附近的相位擾動沒有恢復力，閉迴路把雜訊乘上 $(\omega_0/2Q\Delta\omega)^2$ 的「相位積分」轉移函數，生出 $1/f^2$ 裙帶；(3) device 的 $1/f$ flicker 雜訊再被往上搬一階，生出最靠近載波的 $1/f^3$。ISF 理論講的是**同三段**，只是把 $1/2Q$ 換成 $\Gamma_{rms}/q_{max}$、把 $F$ 換成可由 $\Gamma_{eff}$ 算出的物理量。

## 完整公式（先擺出，再逐步推）

Leeson 模型（規範 10.2，**外部文獻、非 5 篇 PDF**）：

$$
\mathcal{L}(\Delta\omega)=10\log_{10}\!\left[\frac{2FkT}{P_s}\left(1+\Big(\frac{\omega_0}{2Q\,\Delta\omega}\Big)^2\right)\left(1+\frac{\omega_{1/f^3}}{\lvert\Delta\omega\rvert}\right)\right]
$$

符號：$F$＝放大器**雜訊因子**（noise figure，經驗量、無因次）；$k$＝Boltzmann 常數（J/K）；$T$＝溫度（K）；$P_s$＝振盪訊號功率（W）；$Q$＝tank 品質因數（quality factor，無因次）；$\omega_0$＝載波角頻率（rad/s）；$\Delta\omega$＝offset 角頻率（rad/s）；$\omega_{1/f^3}$＝flicker corner（rad/s）。

下面把方括號裡的三個因子一個一個推出來。

## 第 1 步：tank 熱雜訊 — 雜訊地板 $2FkT/P_s$

把振盪器看成「放大器 + 諧振 tank 的回授環」。環裡的熱雜訊源頭是 tank 的損耗電阻 $R$（並聯等效），它的單邊熱雜訊電壓 PSD（Johnson–Nyquist）：

$$
\frac{\overline{v_n^2}}{\Delta f}=4kTR.
$$

- **用到的物理**：電阻熱雜訊 $4kTR$（標準結果，見 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)）。
- **單位檢查**：$[kT]=\text{J}=\text{V·C}$，$[kTR]=\text{V·C·}\Omega=\text{V}^2\text{·s}=\text{V}^2/\text{Hz}$ ✓。

放大器自己也加雜訊，整體用一個**雜訊因子 $F$**（noise figure，把「實際總雜訊」對「只有輸入熱雜訊」的倍率打包成一個數）概括。把雜訊功率對載波功率 $P_s$ 正規化，得到**載波附近的相位雜訊地板**：

$$
\mathcal{L}_{\text{floor}}=\frac{2FkT}{P_s}.
$$

- **$F$ 是 Leeson 的「經驗逃生口」**：它把所有沒被顯式建模的雜訊（放大器、轉換損耗、cyclostationary 效應…）塞進一個量測 fit 的數字。**這正是 ISF 後來要取代的對象**（見第 5 步對照）。
- **那個 2 哪來**：屬 Leeson 模型的記帳慣例（並非唯一寫法，依文獻而異）。物理上其實有**兩步、方向相反**的因子：(1) **AM/PM 等分**——熱雜訊同時擾動振幅與相位，相位只分到一半功率（$\times\tfrac12$）；(2) **單邊帶（SSB）記帳**把雙邊功率折算成單邊（$\times2$）。兩者相抵後，最「乾淨」的地板寫法其實是 $FkT/P_s$；本式寫成 $2FkT/P_s$，是把 SSB 慣例**顯式留在前置常數**、而未把 AM/PM 的 $\tfrac12$ 併進 $F$ 的版本。這與 [P1] Eq.(21) 的 $4\Delta\omega^2$ vs 時域 $2\Delta\omega^2$ 同屬 SSB／雙邊記帳差異（見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 的 factor-of-2 討論）。（$F$ 為經驗擬合參數，前置常數依文獻略異——這正是 ISF 後來用 $\Gamma_{rms}/q_{max}$ 取代的對象。）
- **單位檢查**：$[2FkT/P_s]=\text{J}/\text{W}=\text{J}/(\text{J/s})=\text{s}=1/\text{Hz}$ ✓（$\mathcal{L}$ 是每赫茲的相對功率，dBc/**Hz**）。

## 第 2 步：高 $Q$ tank 的窄帶濾波 → $1/f^2$ 裙帶

tank 是一個窄帶濾波器。在載波附近 offset $\Delta\omega$ 處，並聯 RLC 的相位/振幅響應斜率由 $Q$ 決定。標準結果：tank 對 offset $\Delta\omega$ 的（半功率）轉移可寫成

$$
\left|H(\Delta\omega)\right|^2\;\propto\;\left(\frac{\omega_0}{2Q\,\Delta\omega}\right)^2\qquad(\Delta\omega\ll\omega_0/2Q).
$$

- **$Q$ 的物理**：$Q=\omega_0/\Delta\omega_{3dB}$＝「諧振多尖」＝每週期儲能/耗能比 $\times2\pi$。$Q$ 越高，tank 帶寬越窄、相位斜率越陡，對 offset 雜訊抑制越強。
- **為何是 $1/\Delta\omega^2$（即 $-20$ dB/dec）**：自治振盪器的相位是**中性方向**（無恢復力，呼應 [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv) 的 $\lambda_1=0$）。閉迴路相當於對相位擾動做了一次**積分**，頻域上是 $\times 1/\Delta\omega$；功率再平方就是 $1/\Delta\omega^2$。這就是相位雜訊在中頻段必為 $1/f^2$、斜率 $-20$ dB/dec 的根本原因——**與 ISF 給的 $1/\Delta\omega^2$ 同源**（[P1] Eq.(21)）。
- **單位檢查**：$\omega_0/(2Q\Delta\omega)$ 無因次（rad/s ÷ rad/s）✓，整個轉移無因次。

把第 1、2 步相乘（地板 × tank 整形），方括號出現前兩項：

$$
\mathcal{L}_{1/f^2+\text{floor}}=\frac{2FkT}{P_s}\left(1+\Big(\frac{\omega_0}{2Q\,\Delta\omega}\Big)^2\right).
$$

- 「$1+$」裡的 $1$ 是**白雜訊地板**（遠 offset 主導，平坦）；$(\omega_0/2Q\Delta\omega)^2$ 是 **$1/f^2$ 裙帶**（近 offset 主導）。兩者相等處就是 $1/f^2\to$ floor 的轉角，$\Delta\omega\approx\omega_0/2Q$。

## 第 3 步：device flicker → $1/f^3$ 最近載波段

device 的低頻 $1/f$（flicker）雜訊會被振盪器的非線性「上轉（upconvert）」到載波附近，再經第 2 步的相位積分，變成比 $1/f^2$ 更陡的 $1/f^3$。Leeson 用一個乘性因子把它接上：

$$
\left(1+\frac{\omega_{1/f^3}}{\lvert\Delta\omega\rvert}\right).
$$

- 當 $\Delta\omega\gg\omega_{1/f^3}$：此因子 $\approx1$，看不到 flicker，剩 $1/f^2$ 與 floor。
- 當 $\Delta\omega\ll\omega_{1/f^3}$：此因子 $\approx\omega_{1/f^3}/\lvert\Delta\omega\rvert\propto1/\Delta\omega$，**再乘上**第 2 步的 $1/\Delta\omega^2$ → 總共 $1/\Delta\omega^3$，即 **$1/f^3$、$-30$ dB/dec**。
- **$\omega_{1/f^3}$ 是「相位雜訊的 flicker corner」**，**不是** device 自己的 $1/f$ corner。Leeson 沒說清楚它由什麼決定——**這正是 ISF 補上的關鍵物理**（第 5 步、[P1] Eq.(24)）。
- **單位檢查**：$\omega_{1/f^3}/\lvert\Delta\omega\rvert$ 無因次 ✓。

三項乘起來，就是開頭那條完整 Leeson 式。三段斜率：**floor（平）→ $1/f^2$（$-20$ dB/dec）→ $1/f^3$（$-30$ dB/dec）**，由遠到近。

```mermaid
flowchart LR
  N["熱雜訊 4kTR + 放大器 (打包成 F)"] --> FL["地板 2FkT/Ps"]
  FL --> TK["× tank 整形 (1+(ω0/2QΔω)^2)"]
  TK --> FK["× flicker 上轉 (1+ω_1f3/|Δω|)"]
  FK --> L["L(Δω): floor → 1/f^2 → 1/f^3"]
```

## 第 4 步：Leeson vs ISF 疊圖

把 Leeson 式與 ISF 結果（[P1] Eqs.(21),(23),(24)）畫在同一張 log–log 上，三段（$1/f^3$、$1/f^2$、floor）會**重疊**——兩個模型描述同一條曲線，只是參數的物理意義不同：

![Leeson 模型與 ISF 結果疊圖：兩者共享 1/f³、1/f²、noise floor 三段](/figures/leeson_vs_isf_overlay.png)

- **對應公式**：左半 Leeson 開頭那條（外部文獻）；右半 [P1] Eq.(21)（$1/f^2$）、Eq.(23)（$1/f^3$）、Eq.(24)（$1/f^3$ corner）。
- **script / function**：`simulations/lab_16_leeson_vs_isf.py`（`main`），對應規範 10.1 表的 `leeson_vs_isf_overlay.png`（lab_16）。**這是 pedagogical toy model，非 transistor-level**；Leeson 曲線用 `simulations/common/noise_utils.py` 的 `leeson_one_over_f2` 等函式繪示意 1/f² 段，三段拼接的常數為教學示意值。
- **怎麼讀**：兩條線在中頻段 $1/f^2$ 完全平行（斜率都 $-20$ dB/dec，因為都來自「相位積分 $1/\Delta\omega^2$」）；近載波都翻成 $1/f^3$；遠端都壓到 floor。差異只在「corner 落在哪、絕對位準多高」——而那由參數對應決定，見下節。
- **註**：疊圖中 Leeson 段的 $F,Q,\omega_{1/f^3}$ 與 ISF 段的 $\Gamma_{rms},q_{max},c_0,\omega_{1/f}$ 為**教學示意值**（lab_16 參數），用來展示三段斜率重疊，非特定電路量測。

## 第 5 步：逐項對照（Leeson ↔ ISF）

這是本頁的重點。把兩個模型的對應項擺在一起：

| 段 | Leeson（經驗，[E1] 1966，非 5 篇 PDF） | ISF（[P1] 1998，5 篇 PDF 內） | 對應關係與「ISF 講得更清楚」之處 |
|---|---|---|---|
| **$1/f^2$ 整形** | $\Big(\dfrac{\omega_0}{2Q\,\Delta\omega}\Big)^2$ | $\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{1}{\Delta\omega^2}$（[P1] Eq.(21)） | 都給 $1/\Delta\omega^2$。Leeson 的 $\dfrac{1}{2Q}$ ↔ ISF 的 $\dfrac{\Gamma_{rms}}{q_{max}}\times$（含載波/雜訊功率正規化）。**$Q$↔$\Gamma_{rms}/q_{max}$**：高 $Q$＝低 $\Gamma_{rms}/q_{max}$＝低相位雜訊。 |
| **雜訊源/位準** | $\dfrac{2FkT}{P_s}$，$F$ 經驗 fit | $\dfrac{\overline{i_n^2}/\Delta f}{4}$ 配 $\Gamma_{eff}$（含 cyclostationary） | **$F$ 經驗 vs ISF 物理**：Leeson 的 $F$ 是「量了才知道」；ISF 把它拆成可算的 device 雜訊 PSD × $\Gamma_{eff}$，連 cyclostationary 閘控都進得來（見 [effective_isf](/03_isf_core_theory/effective_isf)）。 |
| **$1/f^3$ corner** | $\omega_{1/f^3}$（Leeson 沒說它由什麼定） | $\Delta\omega_{1/f^3}=\omega_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}\approx\omega_{1/f}\Big(\dfrac{c_0}{c_1}\Big)^2$（[P1] Eq.(24)） | **ISF 的招牌洞見**：$1/f^3$ corner **不等於** device 的 $1/f$ corner $\omega_{1/f}$，而被 $(c_0/\Gamma_{rms})^2$ 縮放。**波形對稱 → $c_0\to0$ → corner 被推到遠低於 $\omega_{1/f}$**。Leeson 完全看不到這條設計槓桿。 |

關鍵對照展開：

**(a) $Q\leftrightarrow\Gamma_{rms}/q_{max}$。** 兩者都是「把雜訊轉成相位裙帶的效率」。Leeson 說「$Q$ 越高越好」；ISF 說「$\Gamma_{rms}/q_{max}$ 越小越好」。但 ISF 更一般：它對**沒有高 $Q$ tank 的 ring oscillator** 也成立（ring 沒有 $Q$ 可言，但有 $\Gamma_{rms},q_{max}$，見 [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)）。這是 ISF 超越 Leeson 的第一點。

**(b) $F$ 經驗 vs ISF 物理。** Leeson 的 $F$ 是黑盒：你得先做出振盪器、量了相位雜訊、反推 $F$，才能用模型「預測」——這其實是事後配適，不是預測。ISF 把同一塊位準寫成 $\dfrac{\overline{i_n^2}/\Delta f}{4q_{max}^2}\Gamma_{rms}^2$（[P1] Eq.(21)），每個量都能從 device 模型與波形**事前算出**，還能透過 $\Gamma_{eff}=\Gamma\cdot\alpha$ 把 cyclostationary（device 在某些相位才漏雜訊）算進去——這正是為什麼 Colpitts 的「實效 $F$」比 Leeson 樸素估計低很多（見 [effective_isf](/03_isf_core_theory/effective_isf)）。

**(c) $1/f^3$ corner。** Leeson 直接把 $\omega_{1/f^3}$ 當輸入參數，等於承認「我不知道它從哪來」。早期工程界甚至誤以為它就等於 device 的 $1/f$ corner。ISF 的 [P1] Eq.(24) 一錘定音：$\Delta\omega_{1/f^3}=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$——它由 **ISF 的 DC 係數 $c_0$**（波形對稱性）決定。**讓波形上升/下降對稱 → $c_0\to0$ → $1/f^3$ corner 大幅下移 → 近載波相位雜訊大降**。這是 Leeson 完全給不出的設計法則，也是 [P2] 用對稱性壓 ring 相位雜訊的理論依據（見 [symmetry](/06_design_insights/symmetry)、[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)）。

## 第 6 步：[P1] 自己的收斂——Sec.III-F「既有模型是簡化特例」（Eq.(28)–(29)）

前五步是「Leeson 對 ISF」的**外部對照**。[P1] 自己在 Sec.III-F（p.187）也做了一次**內部收斂**：把 ISF 一般式 Eq.(19) 加上 LTI 模型的全部簡化假設，看它退化成什麼。這一段是本頁最有說服力的證據——**兩個模型不只是「曲線重疊」，而是同一條公式的特例關係**。

**(1) LTI 假設在 ISF 語言裡等於什麼。** [P1] p.187 列出 LTI 模型（其文獻 [3] 與 [8]）的四個假設：線性非時變、所有雜訊源 stationary、只有 $\omega_0$ 附近的雜訊重要、無雜訊波形是完美弦波。用 ISF 的傅立葉級數（[P1] Eq.(12)）翻譯：**丟掉 $c_1$ 以外的所有項，並令 $c_1=1$**（[P1] p.187 原文設定；已對照渲染頁核實）。這正是理想 LC 的 ISF（[lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model)、[capstone](/03_isf_core_theory/capstone_lc_end_to_end)）：

$$
\Gamma(\theta)=-\sin\theta=\cos\!\big(\theta+\tfrac{\pi}{2}\big)\;\Rightarrow\;c_0=0,\quad c_1=1,\quad c_{n\ge2}=0,\quad \Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta=\tfrac12 .
$$

Parseval（[P1] Eq.(20)）自洽：$\sum c_n^2=c_1^2=1=2\Gamma_{rms}^2$ ✓，故 $\Gamma_{rms}=1/\sqrt2\approx0.707$（本站「true LC」值；代表值 $0.5$ 是刻意保守的教學值，見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)）。$c_0=0$ 順便說明：**理想弦波 LC 沒有 $1/f^3$ 上轉**——LTI 模型看不到 $\omega_{1/f^3}$ 由什麼決定，根子就在它把 $c_0$ 也一起丟掉了。

**(2) 注入 tank 並聯電阻的熱雜訊（[P1] Eq.(28), p.187）。** 考慮 [P1] Fig. 2 的 RLC 振盪器，只算 tank 並聯電阻 $R_p$ 這一個雜訊源：

$$
\frac{\overline{i_n^2}}{\Delta f}=\frac{4kT}{R_p},\qquad q_{max}=C\cdot V_{max}.
$$

- $4kT/R_p$：第 1 步 $4kTR$ 的 Norton 電流版（單邊 PSD，A²/Hz）。
- $q_{max}=CV_{max}$：tank 電容上的最大電荷擺幅——這就是全站 $q_{max}=C\cdot V_{max}$ 定義的論文出處，也是 LTI 變數（$C$、$V_{max}$）與 ISF 變數（$q_{max}$）之間的「翻譯字典」。

**(3) 代入 Eq.(19) 得 Eq.(29)。** [P1] Eq.(19)（白噪求和式，p.185）：

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\overline{i_n^2}/\Delta f\;\sum_{n=0}^{\infty}c_n^2}{8\,q_{max}^2\,\Delta\omega^2}\right).
$$

代 $\sum c_n^2=c_1^2=1$、$\overline{i_n^2}/\Delta f=4kT/R_p$、$q_{max}=CV_{max}$：

$$
\begin{aligned}
\mathcal{L}\{\Delta\omega\}
&=10\log_{10}\!\left(\frac{4kT/R_p}{8\,C^2V_{max}^2\,\Delta\omega^2}\right)
=10\log_{10}\!\left(\frac{kT}{2\,R_p\,C^2V_{max}^2\,\Delta\omega^2}\right)\\
&=10\log_{10}\!\left[\frac12\cdot\frac{kT}{V_{max}^2}\cdot\frac{1}{R_p\,(C\omega_0)^2}\cdot\Big(\frac{\omega_0}{\Delta\omega}\Big)^2\right].
\end{aligned}
$$

最後一行就是 **[P1] Eq.(29), p.187**（已對照渲染頁逐字核實）——只是把 $C^2\Delta\omega^2$ 改寫成 $(C\omega_0)^2(\Delta\omega/\omega_0)^2$，好讓「tank 導納 $C\omega_0$」與「相對 offset $\omega_0/\Delta\omega$」分開看。

- **單位檢查**：$[kT/V_{max}^2]=\text{J/V}^2=\text{C/V}=\text{F}$；$[1/(R_p(C\omega_0)^2)]=1/(\Omega\cdot\text{S}^2)=\Omega$；$\text{F}\cdot\Omega=\text{s}=1/\text{Hz}$ ✓；$(\omega_0/\Delta\omega)^2$ 無因次 ✓。
- **物理**：$1/\Delta\omega^2$（相位積分）、$\propto1/R_p$（$R_p$ 越大＝$Q$ 越高＝雜訊電流越小）、$\propto1/(CV_{max})^2=1/q_{max}^2$（電荷擺幅越大越好）——第 5 步表格的每一格在這條式子裡都有對應。

**(4) 數值（沿用 [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) 的 5 GHz tank）**：$L=1$ nH、$C=1.013$ pF、$R_p=314\ \Omega$、$T=300$ K（$Q=\omega_0R_pC\approx10$）、取 $V_{max}=1$ V、$\Delta f=1$ MHz。

- $kT=1.380649\times10^{-23}\times300=4.142\times10^{-21}$ J；$\tfrac12\,kT/V_{max}^2=2.071\times10^{-21}$ F。
- $C\omega_0=1.013\times10^{-12}\times3.1416\times10^{10}=3.182\times10^{-2}$ S；$R_p(C\omega_0)^2=314\times1.0128\times10^{-3}=0.3180$ S，倒數 $=3.145\ \Omega$。
- $(\omega_0/\Delta\omega)^2=(5\times10^9/10^6)^2=2.5\times10^7$。
- 乘起來：$2.071\times10^{-21}\times3.145\times2.5\times10^7=1.628\times10^{-13}$（單位 F·Ω = s ✓）→ $\mathcal{L}=10\log_{10}(1.628\times10^{-13})=-127.9$ dBc/Hz。
- **用 Eq.(21) 重算必得同值**（$\Gamma_{rms}^2=\tfrac12$、$q_{max}=CV_{max}=1.013$ pC、$S_i=4kT/R_p=5.276\times10^{-23}$ A²/Hz）：$\dfrac{0.5}{(1.013\times10^{-12})^2}\cdot\dfrac{5.276\times10^{-23}}{4\,(2\pi\times10^6)^2}=1.628\times10^{-13}$ ✓。
- **對照 canonical 例 B 的 $-148.0$ dBc/Hz**（$S_i=10^{-24}$ A²/Hz、$\Gamma_{rms}=0.5$、$q_{max}=1$ pC）：這裡 $S_i$ 大 52.8 倍（$+17.2$ dB）、$\Gamma_{rms}^2$ 大 2 倍（$+3.0$ dB）、$q_{max}^2$ 大 $1.013^2$ 倍（$-0.1$ dB）：$-148.0+17.2+3.0-0.1=-127.9$ ✓。

**(5) Craninckx–Steyaert 的 2×，與本站 factor-of-2 的真身。** [P1] p.187 接著指出：其文獻 [8]（J. Craninckx and M. Steyaert, "Low-noise voltage controlled oscillators using enhanced LC-tanks," IEEE Trans. Circuits Syst. II, vol. 42, no. 12, pp. 794–804, Dec. 1995；**外部文獻，非本站 5 篇 PDF**；[P1] 參考文獻表印作 pp. 794–904，應為 804 之誤植）假設振幅與相位對 $\mathcal{L}_{total}$ 的貢獻相等，因此 [8] 的結果**恰為 Eq.(29) 的兩倍**。換句話說，Eq.(19)→(29) 這條鏈**只計了相位那一半**；LTI 模型的 $\mathcal{L}_{total}$（[P1] Eq.(2), p.180 的量測定義，含 AM）把振幅雜訊也算了進去。

本站再自己做一個對照（非論文原文，可用下方 Python 重跑）：把 [P1] p.181 的 Leeson 型 Eq.(6) 取 $F=1$，用 $Q=\omega_0R_pC$、$P_s=V_{max}^2/(2R_p)$ 換算：

$$
\frac{2kT}{P_s}\Big(\frac{\omega_0}{2Q\,\Delta\omega}\Big)^2=\frac{4kTR_p}{V_{max}^2}\cdot\frac{\omega_0^2}{4\,\omega_0^2R_p^2C^2\,\Delta\omega^2}=\frac{kT}{R_p\,C^2V_{max}^2\,\Delta\omega^2}=2\times\big[\text{Eq.(29)}\big].
$$

所以在 [P1] 自己的記帳裡，**Eq.(6) 取 $F=1$ 也比 Eq.(29) 高 3 dB**（$-124.9$ vs $-127.9$ dBc/Hz）——即使 [P1] 在 Eq.(6) 下方已註明其 $\tfrac12$ 來自略去振幅雜訊。這個 2 跟 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) factor-of-2 註記的「時域乾淨 $/2$ vs Eq.(21) 的 $/4$」是同一個 2（canonical 例 B 的 $-145$ vs $-148$ dBc/Hz），也是文獻上著名的小爭議所在。本站誠實列出、**不裁決**哪個常數「對」：**scaling（$\propto1/(R_pC^2V_{max}^2\Delta\omega^2)$）與 $-20$ dB/dec 斜率是物理，這個 2 是 AM/PM 與 SSB 記帳慣例**。

**(6) 與第 5 步 $F$/$Q$ 對映收尾。** 由上式，Eq.(29) $=\tfrac12\cdot\tfrac{2kT}{P_s}\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$，即

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left[\frac{kT}{P_s}\Big(\frac{\omega_0}{2Q\,\Delta\omega}\Big)^2\right]
$$

（理想弦波 LC、僅 tank $R_p$ 熱雜訊）。

- 這就是 Leeson 式的 $1/f^2$ 項，**而且前置常數正好落在第 1 步說的「最乾淨寫法」$FkT/P_s$、$F=1$**；若硬套本頁開頭的 $2FkT/P_s$ 寫法，等價於 $F=\tfrac12$。[P1] p.187 的原話是 (29) 配上 (24) 就得到 (6)——差別全在 $F$ 吸收了多少記帳常數。
- **$Q\leftrightarrow\Gamma_{rms}/q_{max}$ 的顯式等式**：ISF 側 $\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4}=\dfrac12\cdot\dfrac{4kT/R_p}{4C^2V_{max}^2}=\dfrac{kT}{2R_pC^2V_{max}^2}$；Leeson 側 $\dfrac{kT}{P_s}\cdot\dfrac{\omega_0^2}{4Q^2}=\dfrac{2kTR_p}{V_{max}^2}\cdot\dfrac{1}{4R_p^2C^2}=\dfrac{kT}{2R_pC^2V_{max}^2}$——兩邊逐字相等 ✓。這把第 5 步 (a) 的「$1/2Q\leftrightarrow\Gamma_{rms}/q_{max}$（含正規化）」寫成了可核對的等式。
- **ISF 版的 $F$ 不再是黑盒**：對任何真實 ISF，$F$ 的角色由 $\sum c_n^2=2\Gamma_{rms}^2$（相對理想 LC 的 $c_1^2=1$）與 $\Gamma_{eff}$（cyclostationary）接手；$\omega_{1/f^3}$ 由 Eq.(24) 的 $c_0^2/(2\Gamma_{rms}^2)$ 接手。[P1] p.187 明說其一般化方法能用 ISF 的 $c_n$ 與 device 的 $\omega_{1/f}$ **算出** Eq.(3) 的擬合參數 $F$ 與 $\Delta\omega_{1/f^3}$——這句話就是第 5 步表格三列的論文原始出處。

Python 驗證（`# ->` 為實跑輸出）：

```python
import numpy as np
from simulations.common.isf_utils import gamma_rms, compute_fourier_coefficients
# (1) 理想 LC 的 ISF Γ(θ) = -sin θ：只有 c1，且 c1 = 1（[P1] p.187 的 LTI 設定）
theta = np.linspace(0, 2*np.pi, 4097)          # 含端點，供梯形積分
gam = -np.sin(theta)
c0, _, _, c, _ = compute_fourier_coefficients(theta, gam, 3)   # c[n] = c_n
Grms = gamma_rms(theta, gam)
print(round(float(c0), 4), round(float(c[1]), 4), round(float(c[2]), 4), round(float(Grms), 4))
# -> 0.0 1.0 0.0 0.7071   (c0, c1, c2, Γrms；Parseval：c1² = 1 = 2Γrms²)
# (2) [P1] Eq.(28)：tank_Q 頁的 5 GHz tank（L=1 nH、C=1.013 pF、Rp=314 Ω、T=300 K），Vmax = 1 V
k, T = 1.380649e-23, 300.0
f0, C, Rp, Vmax = 5e9, 1.013e-12, 314.0, 1.0
w0 = 2*np.pi*f0
Q  = w0*Rp*C
Si = 4*k*T/Rp            # A²/Hz
qmax = C*Vmax            # C
dw = 2*np.pi*1e6         # Δω @ 1 MHz
print(round(Q, 3), f"{Si:.3e}", f"{qmax:.3e}")
# -> 9.993 5.276e-23 1.013e-12   (Q、i_n²/Δf [A²/Hz]、q_max [C])
# (3) [P1] Eq.(29) vs Eq.(19)（只留 c1）vs Eq.(21)（Γrms² = 1/2）——三者必須同值
L29 = 0.5*k*T/Vmax**2 / (Rp*(C*w0)**2) * (w0/dw)**2
L19 = Si*c[1]**2 / (8*qmax**2*dw**2)
L21 = Grms**2/qmax**2 * Si/(4*dw**2)
print(round(10*np.log10(L29), 2), round(10*np.log10(L19), 2), round(10*np.log10(L21), 2))
# -> -127.88 -127.88 -127.88   (dBc/Hz @ 1 MHz)
# (4) Leeson 形式對照：[P1] Eq.(6) 取 F = 1，以及收尾式 (kT/Ps)(ω0/2QΔω)²
Ps = Vmax**2/(2*Rp)
L6 = 2*k*T/Ps * (w0/(2*Q*dw))**2
L29_leeson = k*T/Ps * (w0/(2*Q*dw))**2
print(round(10*np.log10(L6), 2), round(L6/L29, 4), round(L29_leeson/L29, 4))
# -> -124.87 2.0 1.0   (Eq.(6)|F=1 比 Eq.(29) 高 3 dB＝正好 2×；Eq.(29) ≡ (kT/Ps)(ω0/2QΔω)²)
```

> **適用條件**：Eq.(29) 只在四個 LTI 假設全部成立時才是等式（理想弦波、只有 $c_1$、stationary 雜訊、只算 $\omega_0$ 附近）。ring oscillator（$c_{n\ge2}\neq0$、$\Gamma_{rms}\propto N^{-3/2}$）、非對稱波形（$c_0\neq0$ → $1/f^3$）、cyclostationary 元件雜訊（$\Gamma_{eff}=\Gamma\alpha$）都會讓它失效——此時回到 Eq.(19)/(21)，用真實的 $c_n$ 與 $\Gamma_{eff}$，$F$ 就自動被算出來而不是被 fit 出來。

## 數值例子（建立手感）

> **例（$1/f^3$ corner 對照）**：取 device $1/f$ corner $f_{1/f}=1$ MHz（$\omega_{1/f}=2\pi\times10^6$ rad/s）。比較「對稱」與「不對稱」波形的相位雜訊 $1/f^3$ corner。

ISF 的 [P1] Eq.(24)：$\Delta\omega_{1/f^3}=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$，取 $\Gamma_{rms}=0.5$。

- **不對稱波形**（大 $c_0$，設 $c_0=0.4$）：
  

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{(0.4)^2}{2(0.5)^2}=\omega_{1/f}\cdot\frac{0.16}{0.5}=0.32\,\omega_{1/f}.
$$

  即 $f_{1/f^3}\approx0.32\times1\ \text{MHz}=320$ kHz——$1/f^3$ 裙帶延伸到離載波很遠。
- **對稱波形**（小 $c_0$，設 $c_0=0.04$，小 10 倍）：
  

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{(0.04)^2}{2(0.5)^2}=\omega_{1/f}\cdot\frac{0.0016}{0.5}=3.2\times10^{-3}\,\omega_{1/f}.
$$

  即 $f_{1/f^3}\approx3.2$ kHz——corner 下移 **100 倍**（因為 $c_0$ 平方、降 10 倍 → corner 降 100 倍）。

- **Dimension check**：$c_0^2/\Gamma_{rms}^2$ 無因次，$\omega_{1/f}\times$無因次 $=$ rad/s ✓。
- **手感**：Leeson 把 $\omega_{1/f^3}$ 當「天生固定」；ISF 告訴你它是**設計者能用對稱性壓兩個數量級**的旋鈕。這就是 ISF 的實戰價值。

一行 Python 驗證（corner 比值）：

```python
import numpy as np
from simulations.common.isf_utils import gamma_rms
# 對稱 vs 不對稱波形的 1/f^3 corner 比值 = (c0_asym/c0_sym)^2
c0_asym, c0_sym, Gamma_rms = 0.4, 0.04, 0.5
w1f = 2*np.pi*1e6
corner_asym = w1f * c0_asym**2 / (2*Gamma_rms**2)
corner_sym  = w1f * c0_sym**2  / (2*Gamma_rms**2)
print(corner_asym/(2*np.pi)/1e3, "kHz ;", corner_sym/(2*np.pi)/1e3, "kHz")
# -> ~320.0 kHz ; ~3.2 kHz   (對稱波形把 1/f^3 corner 壓低 100 倍)
```

（`gamma_rms` 等函式庫見 `simulations/common/isf_utils.py`；本例直接用 [P1] Eq.(24) 手算 corner。）

## 適用與失效條件

| 條件 | Leeson 成立時 | 失效時會怎樣 |
|---|---|---|
| 有高 $Q$ 諧振 tank | $(\omega_0/2Q\Delta\omega)^2$ 整形準 | ring 等無 $Q$ 拓樸不適用 → 改用 ISF 的 $\Gamma_{rms}/q_{max}$ |
| $F$ 可由量測 fit | 可事後配適曲線 | 想**事前預測**或拆解物理 → 必須用 ISF（$F$ 是黑盒） |
| $\omega_{1/f^3}$ 已知 | $1/f^3$ 段對得上 | 想知道 corner 由什麼決定/如何壓 → ISF Eq.(24)（$c_0$、對稱性） |
| 線性/弱非線性、加性雜訊 | 三段模型夠用 | 強 cyclostationary → ISF 的 $\Gamma_{eff}=\Gamma\alpha$ 才算得準 |
| 理想弦波 LC、僅 tank $R_p$ 熱雜訊（第 6 步） | [P1] Eq.(29) 就是 Leeson 的 $1/f^2$ 項：$\tfrac{kT}{P_s}(\tfrac{\omega_0}{2Q\Delta\omega})^2$（$F=1$ 於 $FkT/P_s$ 寫法） | $c_{n\ge2}\neq0$、$c_0\neq0$、cyclostationary → 回到 Eq.(19)/(21)，$F$ 由 $2\Gamma_{rms,eff}^2$ 與 $c_0$ 算出而非 fit |

## 與哪些 paper／公式對應

- **Leeson 模型本身**：[E1] D. B. Leeson, Proc. IEEE 54(2):329–330, Feb. 1966 —— **不在下載的 5 篇 PDF 內**；卷期/DOI 已查證（10.1109/PROC.1966.4682，見 [references](/99_appendix/references) 的 [E1]）；本式為標準 Leeson 形式（$F$ 為經驗 noise factor，前置常數依文獻略異）。
- **ISF 對照式（5 篇 PDF 內、已核）**：$1/f^2$ [P1] Eq.(21), p.185；$1/f^3$ [P1] Eq.(23), p.185；$1/f^3$ corner [P1] Eq.(24), p.185；device flicker [P1] Eq.(22), p.185。
- **cyclostationary（解釋「實效 $F$」）**：[P1] Eqs.(25)–(27), p.186（見 [effective_isf](/03_isf_core_theory/effective_isf)）。
- **[P1] 內部收斂（第 6 步）**：Sec.III-F Eq.(28)–(29), p.187（$c_1=1$、$4kT/R_p$、$q_{max}=CV_{max}$）；Leeson 型 Eq.(3), p.180 與 Eq.(6), p.181；量測定義 $\mathcal{L}_{total}$ Eq.(2), p.180；其文獻 [8] Craninckx–Steyaert, IEEE TCAS-II 42(12):794–804, Dec. 1995（**外部文獻，非本站 5 篇 PDF**）。
- **疊圖**：`/figures/leeson_vs_isf_overlay.png`，`simulations/lab_16_leeson_vs_isf.py`（規範 10.1，lab_16）。

## 重點回顧

- Leeson（1966，**外部、非 5 篇 PDF**）＝半經驗三段式：$\mathcal{L}=10\log_{10}\!\big[\tfrac{2FkT}{P_s}(1+(\tfrac{\omega_0}{2Q\Delta\omega})^2)(1+\tfrac{\omega_{1/f^3}}{\lvert\Delta\omega\rvert})\big]$。
- 三段：白雜訊 **floor**（$2FkT/P_s$）→ tank 整形的 **$1/f^2$**（$-20$ dB/dec，源自相位積分 $1/\Delta\omega^2$）→ flicker 上轉的 **$1/f^3$**（$-30$ dB/dec）。
- **逐項對照**：$Q\leftrightarrow\Gamma_{rms}/q_{max}$（高 $Q$＝低 $\Gamma_{rms}/q_{max}$）；$F$ 經驗黑盒 ↔ ISF 可算的 $\overline{i_n^2}\cdot\Gamma_{eff}$（含 cyclostationary）；$\omega_{1/f^3}$ 神祕參數 ↔ [P1] Eq.(24) 由 $c_0$（對稱性）決定。
- **ISF 的三大超越**：(1) 對無 $Q$ 的 ring 也成立；(2) 事前可算、不靠 fit；(3) 把 $1/f^3$ corner 變成可用對稱性壓兩個數量級的設計旋鈕。
- 兩模型在 log–log 疊圖上三段重疊（`leeson_vs_isf_overlay.png`）——同一條曲線、不同物理語言。
- **[P1] 自己的收斂（Sec.III-F）**：LTI 假設 ⇔ 只留 $c_1=1$（$\Gamma=-\sin\theta$、$\Gamma_{rms}=1/\sqrt2$）；代 $4kT/R_p$、$q_{max}=CV_{max}$ 進 Eq.(19) 得 Eq.(29) $=\tfrac{kT}{P_s}(\tfrac{\omega_0}{2Q\Delta\omega})^2$——Leeson 的 $1/f^2$ 項是 ISF 的特例（5 GHz、$Q=10$、$V_{max}=1$ V 例：$-127.9$ dBc/Hz @ 1 MHz）；[8] Craninckx–Steyaert（外部）因 AM/PM 等量計入而大 2×，與本站 factor-of-2 是同一個 2。

## 延伸閱讀

- $1/f^2$ 白噪推導（ISF 版）：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- $1/f^3$ flicker 上轉與 corner：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- 對稱性如何壓 $c_0$：[symmetry](/06_design_insights/symmetry)
- 「實效 $F$」與 cyclostationary：[effective_isf](/03_isf_core_theory/effective_isf)
- PSD / phase noise / jitter 基礎：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- 嚴格基礎（PPV/Floquet）：[derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)
- 完整文獻與外部 citation（[E1]）：[references](/99_appendix/references)
