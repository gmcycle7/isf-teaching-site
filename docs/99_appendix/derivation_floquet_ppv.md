---
title: Floquet / adjoint / PPV：ISF 的嚴格基礎
description: 從週期係數線性系統的 Floquet 理論，到 monodromy 矩陣與 Floquet 指數、第一主向量 v1(t)、adjoint（伴隨）系統與 PPV，逐步證明 ϕ̇=v1ᵀ(t)B(t)ξ(t)，並對應到 ISF Γ/q_max。明標屬外部文獻，不在下載的 5 篇 PDF 內。
---

# Floquet / adjoint / PPV：ISF 的嚴格基礎

> **先備／See also**：[isf_definition](/03_isf_core_theory/isf_definition)（ISF 的直覺定義、「投影到切向」）、[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)（相位/振幅擾動的幾何圖像）、[lti_vs_ltv](/02_foundations/lti_vs_ltv)（為何振盪器是 LTV）｜**接下來**：[ltv_htm](/99_appendix/ltv_htm)（同一個 ISF 的 HTM 面孔）、[derivation_leeson](/99_appendix/derivation_leeson)（經驗模型對照）

[P1] 用「物理直覺 + impulse 模擬」把 ISF（Impulse Sensitivity Function，脈衝敏感度函數）引出來：戳一下、看相位永久偏移多少、整理成週期函數 $\Gamma(\omega_0\tau)$。這條路非常好懂，也是本站主線（見 [isf_definition](/03_isf_core_theory/isf_definition)）。但它有一個說不清楚的地方：「投影到切向（phase direction）」到底是什麼數學物件？為什麼那個方向對應「零恢復力、永久累積」？這頁就是補上這塊**嚴格的數學地基**。

> **誠實聲明（請先讀）**：本頁的 **Floquet theory（弗洛凱理論）、monodromy matrix（單值矩陣）、adjoint method（伴隨法）、PPV（Perturbation Projection Vector，擾動投影向量）** 全部屬於**外部文獻**，**不在本站下載的 5 篇 PDF 內**。主要來源是
> **[E2] A. Demir, A. Mehrotra, and J. Roychowdhury, "Phase Noise in Oscillators: A Unifying Theory and Numerical Methods for Characterization," IEEE Trans. Circuits Syst. I, vol. 47, no. 5, pp. 655–674, May 2000**，以及
> **[E3] F. X. Kärtner, "Analysis of White and $f^{-\alpha}$ Noise in Oscillators," Int. J. Circuit Theory Appl., vol. 18, pp. 485–519, 1990**。
> 卷期/頁碼/DOI **已用網路查證**（[E2] DOI 10.1109/81.847872、[E3] DOI 10.1002/cta.4490180505）。本頁公式記號（$v_1,B,\xi$、Floquet 指數符號慣例）依原文慣例，屬背景框架說明。本頁只提供「為什麼 ISF 是嚴格物件」的數學直覺與骨架，不取代原文。

這頁要回答三個問題：

1. 振盪器在 limit cycle（極限環）附近的擾動，遵守什麼樣的線性方程？
2. 那個方程的解結構長怎樣（Floquet）？為什麼一定有一個「零指數、永久不衰減」的方向？
3. 把任意擾動投影到那個方向，怎麼得到 $\dot\phi=v_1^T(t)B(t)\xi(t)$，又怎麼對回 ISF 的 $\Gamma/q_{max}$？

> **物理直覺（先講結論）**：自治振盪器（autonomous oscillator，沒有外部時脈、自己決定相位的振盪器）有一個與生俱來的對稱性——**時間平移不變**。你把整條解往後挪一點點時間，它還是一個合法的解。這個「沿著軌跡挪一點」的方向，就是**相位方向**；因為沒有任何力把它拉回某個「正確的時刻」，沿這方向的擾動**永遠留著**。Floquet 理論把這句話寫成「**有一個 Floquet 指數恰為 0**」，而 PPV $v_1(t)$ 就是「如何把任意一腳踢，換算成沿這方向挪了多少」的權重向量。ISF 不過是 PPV 在「電荷注入到某個節點電容」這個特定踢法下的標量化版本。

## 第 0 步：把振盪器寫成狀態方程

任何振盪器（LC、ring、Colpitts…）都可以寫成一組一階常微分方程（state-space form）：

$$
\dot{\mathbf{x}}(t)=\mathbf{f}\big(\mathbf{x}(t)\big),\qquad \mathbf{x}\in\mathbb{R}^{N}.
$$

- $\mathbf{x}$ 是狀態向量（例如 $(v_C,\,i_L)$：電容電壓、電感電流），$N$ 是狀態維度。
- $\mathbf{f}$ 是電路的非線性向量場（device 特性 + KCL/KVL）。
- **自治（autonomous）**：$\mathbf{f}$ 不顯含 $t$——這正是「振盪器自己決定頻率與相位」的數學特徵。

穩態時存在一個**週期解** $\mathbf{x}_s(t)=\mathbf{x}_s(t+T)$，$T=1/f_0$，它在狀態空間畫出 limit cycle。

- **單位檢查**：$[\dot{\mathbf{x}}]=[\mathbf{x}]/\text{s}$，$[\mathbf{f}]=[\mathbf{x}]/\text{s}$ ✓（兩邊都是「狀態的時間變化率」）。

注入 noise/擾動時，方程多一項：

$$
\dot{\mathbf{x}}(t)=\mathbf{f}\big(\mathbf{x}(t)\big)+B(t)\,\boldsymbol{\xi}(t).
$$

- $\boldsymbol{\xi}(t)$ 是擾動源向量（例如各 noise 電流 $i_n$）。
- $B(t)$ 是**注入/耦合矩陣**：把擾動「打到哪些狀態、打多重」。對「電流注入節點電容」這種情形，$B$ 的對應列大致是 $1/C_{node}$（把電流換成 $\dot v$）。
- **單位檢查**：$[B\boldsymbol\xi]$ 必須是 $[\mathbf{x}]/\text{s}$。若 $\xi$ 是電流（A）、對應狀態是電容電壓（V），則該列 $\sim 1/C$（$[\text{A}]/[\text{F}]=[\text{A}]\cdot[\text{V/C}]=[\text{V/s}]$）✓。

> 對照 [P1] 的語言：第 0 步的 $B(t)\boldsymbol\xi(t)$ 就是「noise 電流經節點電容變成 $\dot v$」那一步（[P1] Eq.(9), p.181 的 $\Delta V=\Delta q/C_{node}$ 的微分版）。

## 第 1 步：在 limit cycle 附近線性化 → 週期係數線性系統

小擾動下寫 $\mathbf{x}(t)=\mathbf{x}_s(t)+\Delta\mathbf{x}(t)$，對 $\mathbf{f}$ 做一階泰勒展開：

$$
\dot{\mathbf{x}}_s+\dot{\Delta\mathbf{x}}=\mathbf{f}(\mathbf{x}_s)+\underbrace{\frac{\partial\mathbf{f}}{\partial\mathbf{x}}\bigg|_{\mathbf{x}_s(t)}}_{\equiv\,A(t)}\Delta\mathbf{x}+B(t)\boldsymbol\xi(t)+O(\Delta\mathbf{x}^2).
$$

因為 $\dot{\mathbf{x}}_s=\mathbf{f}(\mathbf{x}_s)$（穩態自己滿足無擾動方程），兩邊相消，得到**擾動的線性方程**：

$$
\dot{\Delta\mathbf{x}}(t)=A(t)\,\Delta\mathbf{x}(t)+B(t)\,\boldsymbol\xi(t),\qquad A(t)\equiv\frac{\partial\mathbf{f}}{\partial\mathbf{x}}\bigg|_{\mathbf{x}_s(t)}.
$$

- **關鍵觀察**：$A(t)=A(t+T)$ 是**週期係數矩陣**（因為它在週期軌跡 $\mathbf{x}_s(t)$ 上取值）。這就是為什麼振盪器擾動是 **LTV（線性時變）**而不是 LTI——它的「系統矩陣」隨時間週期變化，正好對應 [P1] 反覆強調的 LTV 本質（見 [lti_vs_ltv](/02_foundations/lti_vs_ltv)）。
- **用到的數學**：Jacobian 線性化；丟掉 $O(\Delta\mathbf{x}^2)$ 即「小擾動/小噪」假設，與 [P1] 的小訊號假設一致。
- **單位檢查**：$A$ 的單位是 $1/\text{s}$（$\partial\dot{\mathbf x}/\partial\mathbf x$），$A\,\Delta\mathbf x$ 是 $[\mathbf x]/\text{s}$ ✓。

齊次部分（先關掉 $\boldsymbol\xi$）是

$$
\dot{\Delta\mathbf{x}}=A(t)\,\Delta\mathbf{x},\qquad A(t+T)=A(t).
$$

這正是 **Floquet 理論**研究的對象：**週期係數的線性常微分方程**。

## 第 2 步：Floquet 理論 — 解結構與 monodromy 矩陣

對線性系統 $\dot{\Delta\mathbf x}=A(t)\Delta\mathbf x$，定義**狀態轉移矩陣**（state transition matrix）$\Phi(t,t_0)$：它把 $t_0$ 時刻的擾動映到 $t$ 時刻，$\Delta\mathbf x(t)=\Phi(t,t_0)\Delta\mathbf x(t_0)$，且 $\Phi(t_0,t_0)=I$。

把它推進**整整一個週期**，得到 **monodromy matrix（單值矩陣）**：

$$
M\equiv\Phi(t_0+T,\,t_0).
$$

- **物理意義**：$M$ 回答「一個擾動轉一圈後變成什麼」。它的特徵值 $\mu_i$ 叫 **Floquet multipliers（弗洛凱乘子）**，描述擾動每轉一圈被放大/縮小的倍率。
- **單位檢查**：$\Phi$、$M$ 都是無因次的線性映射（狀態到狀態） ✓。

**Floquet 定理**說：齊次解可寫成

$$
\Delta\mathbf{x}(t)=\sum_{i=1}^{N} c_i\,\mathbf{u}_i(t)\,e^{\lambda_i t},\qquad \mathbf{u}_i(t)=\mathbf{u}_i(t+T),
$$

其中 $\mathbf{u}_i(t)$ 是**週期**的 Floquet 特徵向量、$\lambda_i$ 是 **Floquet exponents（弗洛凱指數）**，與乘子的關係是

$$
\mu_i=e^{\lambda_i T}\quad\Longleftrightarrow\quad \lambda_i=\frac{1}{T}\ln\mu_i.
$$

- **怎麼讀 $\lambda_i$**：$\mathrm{Re}\,\lambda_i<0$ → 該方向的擾動**衰減**（穩定，例如振幅方向）；$\mathrm{Re}\,\lambda_i=0$ → **中性、不衰減**（相位方向）；$\mathrm{Re}\,\lambda_i>0$ → 發散（穩定 limit cycle 不該有）。
- **單位檢查**：$[\lambda_i]=1/\text{s}$，$[\lambda_i T]$ 無因次（指數要無因次） ✓。

## 第 3 步：為什麼一定有一個 $\lambda=0$ 的方向（相位方向）

這是整套理論的樞紐，而且可以**親手證**。把穩態解對時間微分：對 $\dot{\mathbf x}_s=\mathbf f(\mathbf x_s)$ 兩邊再對 $t$ 微分（鏈鎖律）：

$$
\frac{d}{dt}\dot{\mathbf x}_s=\frac{\partial\mathbf f}{\partial\mathbf x}\bigg|_{\mathbf x_s}\dot{\mathbf x}_s
\quad\Longrightarrow\quad
\frac{d}{dt}\big(\dot{\mathbf x}_s\big)=A(t)\,\dot{\mathbf x}_s.
$$

換句話說，**$\dot{\mathbf x}_s(t)$ 本身就是齊次擾動方程 $\dot{\Delta\mathbf x}=A(t)\Delta\mathbf x$ 的一個解**！而且 $\dot{\mathbf x}_s(t)=\dot{\mathbf x}_s(t+T)$ 是**週期**的——它沒有任何指數成長/衰減因子，等於 $e^{\lambda t}$ 中 $\lambda=0$。

- **結論**：limit cycle 的**切向量** $\dot{\mathbf x}_s(t)$ 對應的 Floquet 指數恰為 $\lambda_1=0$。把它記為第一主向量
  

$$
\mathbf{u}_1(t)\propto\dot{\mathbf x}_s(t),\qquad \lambda_1=0.
$$

![limit cycle 的相位/振幅分解：切向箭頭（沿環、phase 方向）對應 Floquet 指數 $\lambda_1=0$（中性、永久不衰減）；徑向箭頭（離環、amplitude 方向）對應 $\mathrm{Re}\,\lambda_{i\ge2}<0$（有恢復力、被拉回）。](/figures/limit_cycle_phase_amplitude.png)

> **怎麼讀這張圖**：圖中沿 limit cycle 的**切向箭頭**就是本步剛證出的 $\mathbf u_1(t)\propto\dot{\mathbf x}_s(t)$——它對應 $\lambda_1=0$，所以這方向的擾動既不放大也不衰減，**永久累積成相位**；**徑向箭頭**（amplitude 方向）對應 $\mathrm{Re}\,\lambda_{i\ge2}<0$，擾動被恢復力拉回 limit cycle。這正是 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 那張幾何圖的嚴格 Floquet 版本（同一張 `limit_cycle_phase_amplitude.png`，lab_01 `fig_limit_cycle`，pedagogical toy model，2-D state 示意）。

- **物理意義**：$\dot{\mathbf x}_s$ 就是「沿著軌跡走」的方向。沿這方向挪 = 在時間上平移 = **改變相位**。$\lambda_1=0$ 數學上保證「相位擾動既不放大也不衰減，永久保留」——這正是 [P1] 用 unit step $u(t-\tau)$ 表達的「相位步階永久不消」（[P1] Eq.(10), p.182），以及 [isf_definition](/03_isf_core_theory/isf_definition) 第 2 步「切向＝中性方向、無恢復力」那句話的嚴格根據。
- **其他方向**：剩下的 $\lambda_2,\dots$（振幅與更快衰減模態）$\mathrm{Re}\,\lambda_i<0$，擾動會被拉回 limit cycle——這就是「振幅擾動會衰減」（[P4] Fig. 5, p.2126 的 amplitude decay function，見 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)）的嚴格版。

> **這一步就是 ISF「投影到切向」的全部祕密**：本站 [isf_definition](/03_isf_core_theory/isf_definition) 親手把擾動點乘 $\partial\mathbf z/\partial\theta$；而 $\partial\mathbf z/\partial\theta\propto\dot{\mathbf x}_s$，正是 $\lambda_1=0$ 的 Floquet 主向量。直覺與嚴格在此完全對上。

## 第 4 步：adjoint（伴隨）系統與「左特徵向量」$v_1(t)$

問題來了：$\mathbf{u}_1(t)$ 告訴我們「相位方向**長怎樣**」，但要把任意一腳踢 $B(t)\boldsymbol\xi(t)$ **投影**到相位方向，我們需要的是它的**對偶（dual）**——一個能「萃取出相位分量」的**左向量**。這就是 **adjoint（伴隨）系統**登場的地方。

定義原系統的伴隨（adjoint）方程：

$$
\dot{\mathbf{p}}(t)=-A^{T}(t)\,\mathbf{p}(t).
$$

- **為什麼是 $-A^T$**：考慮內積 $\langle\mathbf p,\Delta\mathbf x\rangle=\mathbf p^T\Delta\mathbf x$，用乘積律
  

$$
\frac{d}{dt}\big(\mathbf p^T\Delta\mathbf x\big)=\dot{\mathbf p}^T\Delta\mathbf x+\mathbf p^T\dot{\Delta\mathbf x}
  =(-A^T\mathbf p)^T\Delta\mathbf x+\mathbf p^T(A\,\Delta\mathbf x)
  =-\mathbf p^TA\,\Delta\mathbf x+\mathbf p^TA\,\Delta\mathbf x=0.
$$

  所以選 $\dot{\mathbf p}=-A^T\mathbf p$ 讓內積 $\mathbf p^T\Delta\mathbf x$ **守恆**——這正是我們要的「投影後不被系統演化破壞」的性質。
- **單位檢查**：$[-A^T\mathbf p]=[\mathbf p]/\text{s}$ ✓（與 $\dot{\mathbf p}$ 一致）。

伴隨系統也有 Floquet 結構，其週期解中對應 $\lambda=0$ 的那一條，記為 **$v_1(t)$**——它就是原系統 $\mathbf u_1(t)$ 的**對偶（左 Floquet 向量）**。**$v_1(t)$ 就是 PPV（Perturbation Projection Vector）**。標準的歸一化是「PPV 與相位方向對齊且尺度為 1」：

$$
v_1^{T}(t)\,\dot{\mathbf x}_s(t)=1\qquad\text{（對所有 }t\text{；歸一化慣例）}.
$$

- **直覺**：$\mathbf u_1\propto\dot{\mathbf x}_s$ 是「相位方向的箭頭」；$v_1$ 是「量這個箭頭分量的尺」。兩者用上式校準成「沿軌跡走一單位時間 = 相位前進一單位」。
- **adjoint 的實務價值**：解一次伴隨系統的週期解，就**一次拿到整條 $v_1(t)$**（即整條 ISF）；不必像 [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep) 那樣「一個相位一個相位地打 impulse」暴力掃。商用 RF 模擬器的 PSS + Pnoise 內部正是用這類 adjoint/Floquet 流程。
- **註（背景）**：$v_1(t)$ 的歸一化慣例（$v_1^T\dot{\mathbf x}_s=1$）與 $\lambda$ 符號依 [E2] Demir 2000（pp.655–674, DOI 10.1109/81.847872）；citation 已查證，內部記號屬外部框架。

## 第 5 步：投影 → 證明 $\dot\phi=v_1^T(t)B(t)\boldsymbol\xi(t)$

現在把第 4 步的「尺」用在帶擾動的方程上。Demir 等人證明：在 limit cycle 附近，狀態可寫成「沿軌跡的相位偏移 + 一個衰減的軌道偏差」：

$$
\mathbf{x}(t)=\mathbf{x}_s\big(t+\alpha(t)\big)+\mathbf{y}(t),
$$

其中 $\alpha(t)$ 是**時間域的相位偏移**（單位 s）、$\mathbf y(t)$ 是會衰減的軌道偏差分量（落在 $\mathrm{Re}\,\lambda<0$ 的子空間）。把它代回 $\dot{\mathbf x}=\mathbf f(\mathbf x)+B\boldsymbol\xi$，用 $v_1$ 投影掉會衰減的 $\mathbf y$（因為 $v_1^T$ 與那些方向「正交」——這是左/右 Floquet 向量的雙正交性 biorthogonality），只剩相位分量存活，得到一階相位方程：

$$
\dot{\alpha}(t)=v_1^{T}\big(t+\alpha(t)\big)\,B(t)\,\boldsymbol\xi(t)\;\approx\;v_1^{T}(t)\,B(t)\,\boldsymbol\xi(t).
$$

把時間相位 $\alpha$ 換成弧度相位 $\phi=\omega_0\alpha$（或直接定義 $\phi$ 為無因次相位），得到本頁的招牌結果：

$$
\boxed{\ \dot{\phi}(t)=v_1^{T}(t)\,B(t)\,\boldsymbol\xi(t)\ }
$$

- **逐項意義**：$\boldsymbol\xi(t)$ 是 raw 擾動（noise 電流）；$B(t)$ 把它打進狀態空間（經節點電容）；$v_1^T(t)$ 把結果投影到相位方向、萃取出「這一腳踢貢獻多少相位變化率」。
- **為什麼是 $\dot\phi$（變化率）而不是 $\phi$**：因為相位是中性方向（$\lambda_1=0$），每一瞬間的踢都「原封不動」累加進相位——所以擾動直接給的是 $\dot\phi$，要拿 $\phi$ 得對時間積分。這與 [P1] Eq.(11) 的積分形式（[convolution_derivation](/03_isf_core_theory/convolution_derivation)）一模一樣：
  

$$
\phi(t)=\int_{-\infty}^{t}v_1^{T}(\tau)\,B(\tau)\,\boldsymbol\xi(\tau)\,d\tau.
$$

- **單位檢查**：$\dot\phi$ 是 rad/s。右邊 $v_1^TB\boldsymbol\xi$：取 noise 為電流（A）、$B$ 那列 $\sim1/C$（V/C 經 A 變 V/s... 細節依歸一化），整體調成 rad/s。確切量綱依 $v_1$ 的歸一化（是否含 $1/q_{max}$）而定（依 [E2] 慣例）——見下一步對應。

## 第 6 步：對應回 ISF — $\Gamma/q_{max}$ 是 PPV 的標量化

把第 5 步窄化到 [P1] 的具體情境：**單一 noise 電流 $i_n(t)$ 注入單一節點電容 $C_{node}$**。此時：

- $\boldsymbol\xi(t)\to i_n(t)$（純量）。
- $B(t)\to \mathbf b$（一個常向量，只有「注入節點對應的電容狀態」那一格非零，值 $\sim 1/C_{node}$，把電流變成 $\dot v$）。
- $v_1^T(t)\,\mathbf b$ 是一個**純量的週期函數**——它**就是** $\Gamma(\omega_0 t)/q_{max}$。

於是

$$
\dot\phi(t)=\big[v_1^{T}(t)\,\mathbf b\big]\,i_n(t)\;\equiv\;\frac{\Gamma(\omega_0 t)}{q_{max}}\,i_n(t)
\quad\Longrightarrow\quad
\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau.
$$

右式正是 [P1] Eq.(11), p.182。對照得到**嚴格對應**：

$$
\boxed{\ \frac{\Gamma(\omega_0\tau)}{q_{max}}=v_1^{T}(\tau)\,\mathbf b=\big(\text{PPV 在注入節點上的分量}\big)\ }
$$

等價地，把 $q_{max}$ normalization 顯式拉出來，ISF 就是「**PPV 在該節點的分量乘上 $q_{max}$**」（呼應作者規範 10.2：ISF $=q_{max}\cdot$（PPV 在注入節點的分量））：

$$
\Gamma(\omega_0\tau)=q_{max}\cdot\big(v_1(\tau)\text{ 在注入節點電容狀態上的分量}\big).
$$

- **為什麼 $\Gamma$ 無因次而 PPV 有單位**：PPV $v_1$ 帶單位（取決於狀態的物理量），但乘上 $q_{max}=C_{node}V_{max}$（C）後剛好抵消，把它變成無因次的「形狀函數」——這就是 [P1] 用 $q_{max}$ normalize 的深層理由（見 [isf_definition](/03_isf_core_theory/isf_definition) 第 3 步）。
- **為什麼 $\Gamma$ 是 $2\pi$ 週期**：$v_1(t)$ 是 Floquet 週期向量（週期 $T$），代入 $\omega_0\tau$ 後週期變 $2\pi$ ✓。
- **為什麼「每個 node／每個 noise source 各有一個 ISF」**：因為每個注入點對應不同的 $\mathbf b$，投影出不同的純量 $v_1^T\mathbf b$ ✓。這把 [isf_definition](/03_isf_core_theory/isf_definition) 那條性質從「直覺」升級成「$B$ 的列選擇」。

## 三套語言對照表

同一件事，三種抽象層級：

| 概念 | [P1] 直覺語言（本站主線） | Floquet/PPV 嚴格語言（本頁，外部文獻） | 對應關係 |
|---|---|---|---|
| 相位方向 | limit cycle 的切向 $\partial\mathbf z/\partial\theta$ | $\lambda_1=0$ 的 Floquet 主向量 $\mathbf u_1\propto\dot{\mathbf x}_s$ | 同一方向 |
| 「相位不衰減」 | 相位無恢復力、unit step $u(t-\tau)$ | Floquet 指數 $\lambda_1=0$（中性） | $\lambda_1=0\Leftrightarrow$ 永久保留 |
| 投影權重 | 「轉換比例」$\Gamma/q_{max}$ | PPV $v_1(t)$ 的節點分量 | $\Gamma/q_{max}=v_1^T\mathbf b$ |
| 相位響應 | $\phi=\tfrac{1}{q_{max}}\int\Gamma\,i_n\,d\tau$ | $\dot\phi=v_1^TB\boldsymbol\xi$（積分） | 同一式 |
| 萃取方法 | 一相一相打 impulse（lab_04 暴力法） | 解 adjoint 週期解一次拿整條 | adjoint 高效得多 |
| 振幅衰減 | amplitude restoring | $\mathrm{Re}\,\lambda_{i\ge2}<0$ 子空間 | 嚴格化「振幅被拉回」 |

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 存在穩定 limit cycle | Floquet 結構成立，$\lambda_1=0$ 唯一中性方向 | 多重極限環/混沌時 PPV 不唯一或不存在 |
| 小擾動（線性化有效） | $\dot\phi=v_1^TB\boldsymbol\xi$ 一階成立 | 大注入 → 需保留 $\alpha$ 的非線性相位方程（Demir 完整式） |
| 擾動為加性 $B\boldsymbol\xi$ | 投影乾淨、$\Gamma_{eff}$ 可吸收 cyclostationary（見 [effective_isf](/03_isf_core_theory/effective_isf)） | 強乘性/狀態相依噪需更完整模型 |
| 單一節點電流注入 | $\Gamma/q_{max}=v_1^T\mathbf b$ 純量化成立 | 多節點/分散注入要保留向量形式 $v_1^TB$ |

## 與哪些 paper／公式對應

- **本站主線（5 篇 PDF 內）**：投影到切向、$\Gamma$ 無因次/週期、$\phi=\tfrac{1}{q_{max}}\int\Gamma\,i_n\,d\tau$ —— [P1] Eqs.(10),(11), p.182（見 [isf_definition](/03_isf_core_theory/isf_definition)、[convolution_derivation](/03_isf_core_theory/convolution_derivation)）。
- **cyclostationary 接口**：把 $\Gamma\to\Gamma_{eff}=\Gamma\alpha$ 即可，與本頁 $v_1$ 投影框架相容 —— [P1] Eqs.(25)–(27), p.186（見 [effective_isf](/03_isf_core_theory/effective_isf)）。
- **本頁全部嚴格機制屬外部文獻、不在 5 篇 PDF 內**：[E2] Demir–Mehrotra–Roychowdhury 2000（PPV、$\dot\phi=v_1^TB\boldsymbol\xi$）、[E3] Kärtner 1990（白噪/$f^{-\alpha}$ 擾動分析）。正式 citation 卷期/頁碼/DOI **已查證**，詳見 [references](/99_appendix/references)（[E2]、[E3]）。

## 數值驗證：親手算 monodromy 與 PPV

前面六步全是定理與散文。老工程師的習慣是：**定理沒變成數字之前，先不要相信自己真的懂了**。這一節我們拿一顆 van der Pol 振盪器（$\mu=0.2$，近諧波、單位頻率——與 [lab_15](/04_simulation_labs/lab_15_nonlinear_isf) 同一顆 toy）把本頁每一個數學物件——limit cycle、$T$、monodromy $M$、Floquet multipliers、adjoint 週期解 $v_1(t)$、PPV→ISF——**逐一算出數字**，最後把 adjoint 算出的 ISF 與「一個相位一個相位打脈衝」的暴力法（lab_15 的方法）疊在同一張圖上。完整 script：`simulations/lab_25_floquet_numeric.py`。

> **誠實聲明**：這是 **pedagogical toy model**（非 transistor-level）；全部使用**正規化（無因次）單位**——時間單位取「諧波極限角頻率 $=1$ rad/s」的那個秒，狀態 $x,y$ 無因次。下面凡寫 s 與 rad/s 都指這套正規化單位。Floquet/adjoint 演算法本身依 [E2] Demir 2000 的框架（外部文獻，非本站 5 篇 PDF）。

### 模型與 Jacobian（一次寫清楚，後面四步共用）

van der Pol 方程 $\ddot x-\mu(1-x^2)\dot x+x=0$ 寫成第 0 步的 state form：

$$
\dot{\mathbf x}=\mathbf f(\mathbf x)=\begin{pmatrix}y\\ \mu(1-x^2)\,y-x\end{pmatrix},\qquad \mathbf x=(x,y),\ \ \mu=0.2 .
$$

第 1 步需要的 Jacobian，逐項微分（$f_2=\mu(1-x^2)y-x$）：$\partial f_2/\partial x=-2\mu xy-1$、$\partial f_2/\partial y=\mu(1-x^2)$，所以

$$
A(t)=\frac{\partial\mathbf f}{\partial\mathbf x}\bigg|_{\mathbf x_s(t)}
=\begin{pmatrix}0 & 1\\ -2\mu x_s y_s-1 & \mu(1-x_s^2)\end{pmatrix},
\qquad A(t+T)=A(t).
$$

- **單位檢查**：正規化下 $[x]=[y]=$ 無因次、$[t]=$ s，故 $[A]=1/\text{s}$ ✓（第 1 步的一般結論）。
- 選 $\mu=0.2$ 的理由：夠小 → 波形近正弦、ISF 應接近 $-\sin$（可對照直覺）；又不為零 → Floquet 結構非退化（$\vert\mu_2\vert$ 明顯小於 1）。

### 數值步驟 1：找 limit cycle 與週期 $T$

**方法**：從 $(2,0)$ 出發用 RK4（步長 $10^{-3}$ s）積 300 s——暫態以 $e^{-\mu t}$ 衰減，$\mu t=60$ 已到機器精度；然後取 Poincaré 截面「$x=0$、$y>0$（$x$ 的上升零交越）」，用 Newton 步 $\Delta t=-x/\dot x=-x/y$ 把落點修到 $\vert x\vert<10^{-13}$；連續 5 次回到截面取平均得 $T$。

```python
import numpy as np
from simulations.lab_25_floquet_numeric import find_limit_cycle, monodromy

s0, T = find_limit_cycle()            # 步驟 1：settle + Poincaré 截面 + Newton
print(round(T, 4))                    # -> 6.2989
print(round(2 * np.pi / T, 4))        # -> 0.9975

M, states, hf = monodromy(s0, T)      # 步驟 2：dPhi/dt = A(t)Phi 積一圈
mults = np.sort(np.linalg.eigvals(M).real)[::-1]
print(round(float(mults[0]), 6), round(float(mults[1]), 4))  # -> 1.0 0.2828
print(round(float(np.log(mults[1]) / T), 4))                 # -> -0.2005
print(round(float(np.linalg.det(M)), 6))                     # -> 0.282827
tr = 0.2 * (1 - states[:, 0] ** 2)    # tr A = mu(1 - x^2)
print(round(float(np.exp(np.trapezoid(tr, dx=hf))), 6))      # -> 0.282827
```

**結果與交叉檢查**：$T=6.2989$ s、$\omega_0=2\pi/T=0.9975$ rad/s。Lindstedt–Poincaré 微擾展開給 van der Pol 的標準結果 $T=2\pi\,(1+\mu^2/16+O(\mu^4))$（外部文獻，非本站 5 篇 PDF：A. H. Nayfeh, *Perturbation Methods*, Wiley, New York, 1973）：代入 $\mu=0.2$ 得 $2\pi\times1.0025=6.2989$ s——與數值**四位小數一致**；等價地 $\omega_0\approx1-\mu^2/16=0.9975$ ✓。振幅 $A=\max\vert x_s\vert=2.0004$（諧波極限的著名結果 $A\to2$）。

- **單位檢查**：$[T]=$ s、$[\omega_0]=$ rad/s ✓；rad 是無因次記帳單位。

### 數值步驟 2：fundamental matrix 一圈 → monodromy $M$ 與 multipliers

**方法**：把第 2 步的定義直接照抄成數值問題——沿著剛找到的 cycle 同時積分「狀態 + fundamental matrix」：

$$
\frac{d\Phi}{dt}=A(t)\,\Phi,\qquad \Phi(0)=I_2,\qquad M=\Phi(T),
$$

RK4、一個週期 12000 步（$A(t)$ 在每個 RK4 stage 直接用當下的 $\mathbf x_s$ 代入 Jacobian，不需要 $A(t)$ 的解析式）。

**結果**（上面同一個 code block 印出）：

$$
\mu_1=1.000000,\qquad \mu_2=0.2828,
$$

$$
\lambda_1=\frac{\ln\mu_1}{T}=1.5\times10^{-13}\ \text{1/s}\approx0,\qquad
\lambda_2=\frac{\ln\mu_2}{T}=-0.2005\ \text{1/s}.
$$

三件事值得看三遍：

1. **$\mu_1=1$ 不是我們放進去的，是算出來的**。程式從頭到尾沒有告訴它「有一個相位方向」；$\mu_1$ 偏離 1 的量（$\sim10^{-13}$）同時是第 3 步定理（切向 $\Rightarrow\lambda_1=0$）的數值證據，也是「cycle 找得夠準、$T$ 量得夠準」的自我診斷——若 settle 不足或 $T$ 錯了，$\mu_1$ 會立刻偏離 1。
2. **$\lambda_2\approx-\mu$ 有解析對照**。用標準 averaging（Krylov–Bogoliubov；同上 Nayfeh 1973，外部文獻）：慢變振幅方程 $\dot a=g(a)=\tfrac{\mu}{2}a\,(1-a^2/4)$，在 $a=2$ 線性化：$g'(a)=\tfrac{\mu}{2}(1-3a^2/4)$，$g'(2)=\tfrac{\mu}{2}(1-3)=-\mu$。所以一階預測 $\lambda_2=-\mu=-0.2$，數值 $-0.2005$（差 0.25%，$O(\mu^3)$ 修正）✓。振幅擾動時間常數 $\tau_{amp}=1/\vert\lambda_2\vert=4.99$ s $\approx1/\mu$——這正是 [P4] Fig. 5, p.2126 的 amplitude decay function $d=e^{-t/\tau_0}$（LC 振盪器 $\tau_0=2Q/\omega_0$）在這顆 toy 上的 Floquet 嚴格版。
3. **Abel–Liouville 交叉檢查**。行列式恆等式 $\det M=\exp\!\big(\int_0^T\operatorname{tr}A\,dt\big)$，而 $\operatorname{tr}A=\mu(1-x_s^2)$：左邊 $\mu_1\mu_2=0.282827$、右邊沿 cycle 數值積分後取指數 $=0.282827$——**六位小數一致**。兩條完全獨立的計算路徑（特徵值 vs 跡的積分）互相咬合，integrator 沒有偷走任何東西。

- **單位檢查**：$\Phi,M,\mu_i$ 無因次（狀態→狀態的映射）✓；$[\lambda_i]=1/\text{s}$，$\lambda_iT$ 無因次才能放進指數 ✓。

### 數值步驟 3：adjoint 往回積 → 週期左向量 $v_1(t)$

**為什麼要「往回」積**：先把第 4 步的守恆式變成 map。對所有初始擾動 $\Delta\mathbf x(0)$，$\mathbf p(T)^T\Delta\mathbf x(T)=\mathbf p(0)^T\Delta\mathbf x(0)$ 且 $\Delta\mathbf x(T)=M\Delta\mathbf x(0)$，所以 $M^T\mathbf p(T)=\mathbf p(0)$——adjoint 的「一圈 map」是 $M^{-T}$，特徵值是 $1/\mu_i$：即 $1$ 與 $1/0.2828=3.54$。**正著積**，那個 3.54 模態每圈把數值雜質放大 3.54 倍，很快淹沒 $v_1$；**倒著積**，它每圈衰減 0.2828 倍，積分自動「自我清洗」收斂到週期解 $v_1(t)$——這正是 [E2] Demir 2000 的 backward-adjoint 數值流程（外部文獻）。我們從 $M^T$ 的特徵值 $=1$ 左特徵向量出發、沿 cycle 倒積一圈：

$$
\dot{\mathbf p}=-A^T(t)\,\mathbf p\quad(\text{從 }t=T\text{ 積回 }t=0).
$$

```python
import numpy as np
from simulations.common.isf_utils import gamma_rms
from simulations.lab_25_floquet_numeric import ppv_pipeline

res = ppv_pipeline()                       # 步驟 1-3 一次做完
print("{:.1e}".format(res["const_err"]))   # -> 2.2e-14
print("{:.1e}".format(res["per_err"]))     # -> 9.5e-13

theta = res["theta"]
g = res["omega0"] * res["v1"][:, 1]        # 步驟 4：Gamma/qmax = w0 * v1_y
print(round(float(np.max(np.abs(g))), 4))  # -> 0.5011
print(round(res["qmax_toy"], 4))           # -> 2.0442
print(round(float(gamma_rms(theta, res["qmax_toy"] * g)), 4))   # -> 0.7258
gn = g / np.max(np.abs(g))
print(round(float(np.sqrt(np.mean((gn + np.sin(theta)) ** 2))), 4))  # -> 0.0555
```

**兩個機器精度級的檢查**：

- **週期性**：$\Vert\mathbf p(0)-\mathbf p(T)\Vert/\Vert\mathbf p(T)\Vert=9.5\times10^{-13}$——倒積一圈確實回到自己（左 Floquet 向量、$\lambda=0$）。
- **歸一化恆定**（第 4 步的內積守恆定理）：$\mathbf p(t)^T\dot{\mathbf x}_s(t)$ 沿整圈的最大相對偏差 $=2.2\times10^{-14}$。這個內積**理論上一個常數都不能動**；數值只剩捨入誤差。除以這個常數就完成歸一化 $v_1^T(t)\,\dot{\mathbf x}_s(t)=1$（對所有 $t$）。

- **單位檢查**：歸一化條件 $v_1^T\dot{\mathbf x}_s=1$（無因次）給出 $[v_1]=\text{s}/[\mathbf x]$；於是一腳踢 $\Delta\mathbf x$ 換得的**時間相位** $\Delta\alpha=v_1^T\Delta\mathbf x$ 單位是 s ✓（第 5 步 $\alpha(t)$ 的單位）。

### 數值步驟 4：$v_1$ 的分量就是 ISF——疊圖對決

第 6 步說 $\Gamma(\omega_0\tau)/q_{max}=v_1^T\mathbf b$。這顆 toy 我們把脈衝踢在 $y$ 軸上（**與 lab_15 的 `impulse_dy` 完全同一個踢法**，$\mathbf b=\hat{\mathbf e}_y$），於是

$$
\frac{\Gamma(\theta)}{q_{max}}=\omega_0\,v_{1,y}(\theta),\qquad \theta=\omega_0 t\ (\text{自 }x\text{ 的上升零交越起算}).
$$

- **那個 $\omega_0$ 是單位換算，不是新物理**：$v_1$ 給的是「每單位 $\Delta q$ 換多少**秒**」（$\Delta\alpha$，s），乘 $\omega_0$ 才變「多少 **rad**」（$\Delta\phi=\omega_0\Delta\alpha$）。這正是本站在 [P2] Eq.(8), p.792（$\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$，相位 jitter）與 Eq.(12), p.793（$\kappa$ 表達式**不含** $\omega_0$）反覆強調的「時間域 vs 弧度域記帳」同一顆因子——在哪個域工作、何時乘 $\omega_0$，必須每次寫明。
- **單位檢查**：$[\omega_0 v_{1,y}]=(\text{rad/s})\times(\text{s}/[\Delta q])=\text{rad}/[\Delta q]$ ✓——正是 [P1] Eq.(10), p.182 中 $\Gamma/q_{max}$ 的單位（每單位電荷的相位）。

**諧波極限的解析對照**（$\mu\to0$ 時該長什麼樣）：純諧波 $x=A\sin\theta$、$y=\dot x=\omega_0A\cos\theta$，相位可寫 $\theta=\operatorname{atan2}(u,v)$，$u=\omega_0x$、$v=y$。用 $\partial\,\mathrm{atan2}/\partial v=-u/(u^2+v^2)$ 與 $\partial\,\mathrm{atan2}/\partial u=+v/(u^2+v^2)$，其中 $u^2+v^2=\omega_0^2A^2$：

$$
\frac{\Gamma_y(\theta)}{q_{max}}=\frac{\partial\theta}{\partial y}
=\frac{-\omega_0A\sin\theta}{\omega_0^2A^2}=-\frac{\sin\theta}{\omega_0A},
\qquad
\frac{\Gamma_x(\theta)}{q_{max}}=\frac{\partial\theta}{\partial x}
=\omega_0\cdot\frac{\omega_0A\cos\theta}{\omega_0^2A^2}=+\frac{\cos\theta}{A}.
$$

峰值預測 $1/(\omega_0A)=1/(0.9975\times2.0004)=0.5011$——數值峰值正是 $0.5011$ ✓。

```python
import numpy as np
from simulations.lab_15_nonlinear_isf import extract_vdp_isf
from simulations.lab_25_floquet_numeric import ppv_isf, extract_isf_impulse_axis

theta, g_ppv, res = ppv_isf()              # adjoint 一次解
th15, isf15, T15 = extract_vdp_isf(0.2)    # lab_15 暴力法：36 個相位打脈衝
rms = np.sqrt(np.mean((np.interp(th15, theta, g_ppv) - isf15) ** 2))
print(round(float(rms), 4))                # -> 0.0016

g_ppv_x = res["omega0"] * res["v1"][:, 0]  # 同一條 v1 的 x 分量
thx, isfx = extract_isf_impulse_axis(res["s0"], res["T"], axis=0)
rms_x = np.sqrt(np.mean((np.interp(thx, theta, g_ppv_x) - isfx) ** 2))
print(round(float(rms_x), 4))              # -> 0.0023
```

![lab_25 數值驗證：(a) van der Pol μ=0.2 的 limit cycle 與切向（λ₁=0 方向）；(b) 一次 adjoint 解得到的週期左向量 v₁ 兩個分量＝兩個注入軸的 ISF，x 軸踢法用獨立脈衝掃描實測驗證；(c) PPV 算出的 ISF（線）與 lab_15 打脈衝法（紅圈）疊圖，rms 差 0.0016。](/figures/floquet_ppv_numeric.png)

**怎麼讀這張圖**（script：`simulations/lab_25_floquet_numeric.py`，圖 `floquet_ppv_numeric.png`）：

- **(a)**：灰線是暫態（$e^{\lambda_2 t}$ 被吸進 limit cycle——$\mathrm{Re}\,\lambda_2<0$ 的可視化）；藍圈是 $\mathbf x_s(t)$；紅箭頭是切向 $\dot{\mathbf x}_s$，即 $\lambda_1=0$ 的 Floquet 主向量 $\mathbf u_1$。
- **(b)**：**一次** adjoint 解給出整條 $v_1(t)$，它的**兩個分量同時是兩個注入軸的 ISF**——藍線（踢 $y$）貼著 $-\sin\theta/(\omega_0A)$；橘線（踢 $x$）與諧波極限 $+\cos\theta/A$（點線）有肉眼可見的偏差。這個偏差是真的物理（$\mu=0.2$ 的波形失真），不是數值誤差——證據：橘方塊是**另外做的獨立脈衝掃描**（踢 $x$ 軸、18 個相位），與橘線 rms 差只有 $0.0023$。第 4 步說的「解一次 adjoint、所有注入點的 ISF 全拿到」在此成為算出來的事實：$x$ 軸的 ISF 我們**沒有**重新解 adjoint，只是把同一條 $v_1$ 換一個分量讀出來。
- **(c)**：招牌疊圖。藍線 = $\omega_0v_{1,y}$（adjoint 法）；紅圈 = lab_15 的打脈衝法（36 個相位、$\Delta q=0.02$）；黑虛線 = $-\sin\theta/(\omega_0A)$。**PPV vs 脈衝的 raw rms 差 $=0.0016$**（峰值的 0.3%）；歸一化後與 $-\sin\theta$ 的 rms 差 $=0.0555$——後者比前者大 30 倍，說明「偏離 $-\sin$」的部分是 $O(\mu)$ 波形失真的真實物理（兩種方法**一致地**量到它），不是誤差。

**順手對回全站的 canonical 數字**：把 toy 的 $q_{max}$ 取為被踢節點的最大擺幅 $q_{max}^{\,toy}=\max\vert y_s\vert=2.0442$，去正規化的無因次 ISF $\Gamma=q_{max}^{\,toy}\cdot(\Gamma/q_{max})$ 的 rms 為 $\Gamma_{rms}=0.7258$——距真 LC 的 canonical 值 $1/\sqrt2=0.7071$（見 [rms_isf](/03_isf_core_theory/rms_isf)）只差 $+2.6\%$：近諧波振盪器的 ISF「幾乎就是」理想 LC 的 $-\sin$，偏差正是 $\mu$ 帶來的失真，與 [lab_15](/04_simulation_labs/lab_15_nonlinear_isf) 的教訓（大 $\mu$ 時 ISF 遠離 $-\sin$）銜接。

### 這一節到底證明了什麼

| 前六步的散文（定理） | 本節算出的數字 |
|---|---|
| 切向 $\Rightarrow\lambda_1=0$（第 3 步） | $\mu_1=1.000000$，$\vert\lambda_1\vert=1.5\times10^{-13}$ 1/s |
| 振幅方向衰減 $\mathrm{Re}\,\lambda_2<0$ | $\mu_2=0.2828$，$\lambda_2=-0.2005\approx-\mu$（averaging 預測 $-0.2$） |
| $\det M=\exp\int\operatorname{tr}A\,dt$（Liouville） | $0.282827$ vs $0.282827$（六位一致） |
| 內積 $\mathbf p^T\Delta\mathbf x$ 守恆（第 4 步） | $v_1^T\dot{\mathbf x}_s$ 恆定到 $2.2\times10^{-14}$ |
| $\Gamma/q_{max}=v_1^T\mathbf b$（第 6 步） | PPV vs 打脈衝 rms 差 $0.0016$（踢 $y$）、$0.0023$（踢 $x$） |
| 「解一次 adjoint 全拿」（第 4 步實務價值） | $x$ 軸 ISF 由同一條 $v_1$ 直接讀出，免重掃 |

一句話：**「PPV = ISF」在這顆 toy 上已經不是散文，是一個被算出來、可重跑驗證的事實。**[P1] 的打脈衝直覺法與 [E2] 的 adjoint 嚴格法，在同一顆振盪器上給出同一條曲線，差 0.3%。

**本節數值方法的適用與失效**（誠實條款）：固定步長 RK4 + Poincaré/Newton 對這顆近諧波 toy 綽綽有餘；若 $\mu\gg1$（relaxation，波形極陡）需要自適應步長與更小心的截面選擇；若系統維度高且 $\vert\mu_2\vert\to1$（衰減極慢，例如超高 $Q$），$M$ 的特徵向量分離變差、倒積收斂變慢——商用 shooting-PSS/Pnoise 引擎處理的正是這些工程細節。此外本 toy 為加性、單點注入；cyclostationary 調變請回 [effective_isf](/03_isf_core_theory/effective_isf)。

## 重點回顧

- 振盪器擾動在 limit cycle 附近 → **週期係數線性系統** $\dot{\Delta\mathbf x}=A(t)\Delta\mathbf x+B\boldsymbol\xi$，$A(t+T)=A(t)$——這就是 LTV 的根。
- **Floquet 定理**給出 $\Delta\mathbf x=\sum c_i\mathbf u_i(t)e^{\lambda_i t}$；monodromy 矩陣 $M=\Phi(t_0+T,t_0)$ 的特徵值決定每圈放大率，$\mu_i=e^{\lambda_iT}$。
- 切向量 $\dot{\mathbf x}_s$ 自動是齊次解 → **$\lambda_1=0$**（相位中性、永久不衰減）；振幅等其餘方向 $\mathrm{Re}\,\lambda<0$（衰減）。
- **adjoint 系統** $\dot{\mathbf p}=-A^T\mathbf p$ 讓 $\mathbf p^T\Delta\mathbf x$ 守恆；其 $\lambda=0$ 解就是 **PPV $v_1(t)$**。
- 投影得 $\boxed{\dot\phi=v_1^T(t)B(t)\boldsymbol\xi(t)}$；窄化到單節點電流注入 → $\Gamma/q_{max}=v_1^T\mathbf b$，即 **ISF 是 PPV 在注入節點的分量**（乘 $q_{max}$）。
- 全套 Floquet/adjoint/PPV **屬 Demir 2000、Kärtner 1990 外部文獻、不在 5 篇 PDF 內**；citation（卷期/頁碼/DOI）已查證，見 references。
- **數值驗證（lab_25，van der Pol $\mu=0.2$）**：$T=6.2989$、$\mu_1=1.000000$（$\lambda_1\approx0$）、$\mu_2=0.2828$（$\lambda_2=-0.2005\approx-\mu$）；$v_1^T\dot{\mathbf x}_s$ 恆定到 $2.2\times10^{-14}$；adjoint 算出的 ISF 與打脈衝法 rms 差 $0.0016$——「PPV = ISF」是**算出來的事實**，不只是散文。

## 延伸閱讀

- ISF 的直覺定義（本頁的「白話版」）：[isf_definition](/03_isf_core_theory/isf_definition)
- 操作型逐步推導：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)
- 對任意 noise 疊加（積分式）：[convolution_derivation](/03_isf_core_theory/convolution_derivation)
- cyclostationary 與 effective ISF（含 PPV/adjoint 背景）：[effective_isf](/03_isf_core_theory/effective_isf)
- LTV vs LTI 的本質差異：[lti_vs_ltv](/02_foundations/lti_vs_ltv)
- 非線性（van der Pol）振盪器的打脈衝 ISF 萃取（本頁數值驗證的對照組）：[lab_15_nonlinear_isf](/04_simulation_labs/lab_15_nonlinear_isf)；本頁數值驗證 script：`simulations/lab_25_floquet_numeric.py`
- 完整文獻與外部 citation（[E2]、[E3]）：[references](/99_appendix/references)
- 另一個推導附錄（經驗模型對照）：[derivation_leeson](/99_appendix/derivation_leeson)
