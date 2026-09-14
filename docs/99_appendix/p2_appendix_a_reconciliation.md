---
title: "[P2] Appendix A 逐字對帳：時域自相關路與 Khinchin 路"
description: "[P2] Appendix A「Relationship Between Jitter and Phase Noise」（p.802–803）逐字轉錄＋逐因子對帳：白噪時域自相關路 Eq.(40)–(44) 與自相關＋Khinchin 路 Eq.(45)–(51)，逐步對照 jitter_kernels 頁第 3、4 步的推導，並誠實列出兩條路各自跳過與寫全之處，附 Python 兩路數值重演同一個 κ²ΔT。"
---

# [P2] Appendix A 逐字對帳：時域自相關路與 Khinchin 路

> 先備：[jitter_kernels](/02_foundations/jitter_kernels)（第 0–4 步：唯一慣例宣告、edge=相位取樣、三個核的推導、白噪 FM 封閉式）｜ 接下來：回到 [jitter_kernels](/02_foundations/jitter_kernels) 第 5 步（flicker $1/f^3$ 封閉式）· [allan_variance](/02_foundations/allan_variance)

> 本頁是 [jitter_kernels](/02_foundations/jitter_kernels) 第 3、4 步推導的**論文原生出處**：把 [P2] Appendix A 逐字轉錄下來，跟 jitter_kernels 頁自己的推導逐項對照、逐因子對帳。**以下「該頁」一律指 [jitter_kernels](/02_foundations/jitter_kernels) 主頁**；本頁只做逐字轉錄與對帳，不重新推導——所有公式、數值與程式碼都與 jitter_kernels 頁第 0–4 步共用同一套 canonical 參數與符號。

第 3、4 步是本站自己的推導；其實 [P2] 在 **Appendix A "Relationship Between
Jitter and Phase Noise"** 把同一件事**用兩條路各走了一遍**——它**起於 p.802 右欄、
收於 p.803 左欄**（p.803 右欄起是 Appendix B 的非對稱邊沿推導，別搞混）：
Eq.(40)–(44) 是白噪時域路（＝該頁 4.2）、Eq.(45)–(49) 是自相關＋Khinchin 路
（＝該頁路 A），末尾附兩條實用推論 Eq.(50)/(51)（＝該頁 4.5 與 4.4 的一週期版）。
主文 p.793 明說 Eq.(11) 的出處就是這裡（"As shown in Appendix A, for
$\Delta T\gg T$ or $\Delta T=nT$…"，緊接著給出
$\sigma_{\Delta\phi}^2=\frac{\Gamma_{rms}^2\cdot\overline{i_n^2}/\Delta f}{2q_{max}^2}\Delta T$）。
以下逐字轉錄自 p.802–803 的 PDF 渲染頁（放大核對），照排如實——包括印刷滑失。

## A.1 白噪時域路：Eq.(40)–(44)（p.802 右欄）

phase jitter 的定義（原文："The phase jitter is"）：

$$
\sigma_{\Delta\phi}^2=E\{\Delta\phi^2\}=E\big\{[\phi(t+\Delta T)-\phi(t)]^2\big\}
\qquad(\text{[P2] Eq.(40), p.802})
$$

其中（把 [P1] 的 ISF 相位積分限截到觀測窗）：

$$
\Delta\phi=\int_0^{\Delta T}\frac{\Gamma(\omega_0\tau)}{q_{max}}\,i(\tau)\,d\tau.
\qquad(\text{Eq.(41)})
$$

平方、期望與積分交換：

$$
\sigma_{\Delta\phi}^2=\frac{1}{q_{max}^2}\int_0^{\Delta T}\!\!\int_0^{\Delta T}
\Gamma(\omega_0\tau_1)\,\Gamma(\omega_0\tau_2)\cdot E[i(\tau_1)i(\tau_2)]\,d\tau_1\,d\tau_2.
\qquad(\text{Eq.(42)})
$$

白噪電流的自相關原文明寫為
$R_{ii}(t_1,t_2)=(1/2)\big(\overline{i_n^2}/\Delta f\big)\delta(t_1-t_2)$，
代入後雙重積分塌成單重：

$$
\sigma_{\Delta\phi}^2=\frac12\,\frac{\overline{i_n^2}/\Delta f}{q_{max}^2}
\int_0^{\Delta T}\Gamma^2(\omega_0\tau)\,d\tau
\qquad(\text{Eq.(43)})
$$

$$
\sigma_{\Delta\phi}^2=\frac12\,\frac{\overline{i_n^2}/\Delta f}{q_{max}^2}\,
\Gamma_{rms}^2\,\Delta T
\quad\text{for}\quad\Delta T\gg T\ \text{or}\ \Delta T=mT.
\qquad(\text{Eq.(44)})
$$

**Eq.(44) 字面就是主文 Eq.(11)**（p.793，僅排版不同），其係數
$\tfrac12\,(\overline{i_n^2}/\Delta f)\,\Gamma_{rms}^2/q_{max}^2$ 正是該頁 4.2 的
$\kappa^2$（$S_i\equiv\overline{i_n^2}/\Delta f$）——論文的時域路與 4.2
**一個符號都不差**。

## A.2 自相關＋Khinchin 路：Eq.(45)–(51)（p.803 左欄）

論文接著換第二條路——開頭明說 timing jitter 是時間不確定度的標準差：

$$
\sigma_{\Delta\phi}^2=\frac{1}{\omega_0^2}E\big\{[\phi(t+\Delta T)-\phi(t)]^2\big\}
=\frac{E[\phi^2(t)]}{\omega_0^2}+\frac{[\phi^2(t+\Delta T)]}{\omega_0^2}
-\frac{E[\phi(t)\phi(t+\Delta T)]}{\omega_0^2}
\qquad(\text{Eq.(45)，照排如此})
$$

$$
R_\phi(\tau)=E[\phi(t)\phi(t+\Delta T)]
\qquad(\text{Eq.(46)，照排如此})
$$

$$
\sigma_{\Delta\phi}^2=\frac{2}{\omega_0^2}\big[R_\phi(0)-R_\phi(\Delta T)\big].
\qquad(\text{Eq.(47)})
$$

$$
R_\phi(\tau)=\int_{-\infty}^{\infty}S_\phi(f)\,e^{j2\pi f\tau}\,df
\qquad(\text{Eq.(48)，Khinchin 定理})
$$

$$
\sigma_{\Delta\phi}^2=\frac{8}{\omega_0^2}\int_0^{\infty}S_\phi(f)\sin^2(\pi f\tau)\,df.
\qquad(\text{Eq.(49)})
$$

以及兩條白噪（$1/f^2$ 區）限定的實用推論——Eq.(50) 由主文 (6)+(12) 組合而得、
Eq.(51) 再 "based on (8)"（即 $\sigma=\kappa\sqrt T$）接上；**都不是**由積分 (49) 而得：

$$
\kappa=\frac{\Delta f}{f_0}\cdot10^{-\mathcal{L}\{\Delta f\}/20}
\qquad(\text{Eq.(50)})
$$

$$
\sigma_{CTC}=\frac{f}{f_0^{1.5}}\cdot10^{-\mathcal{L}\{\Delta f\}/20}.
\qquad(\text{Eq.(51)，照排如此})
$$

**照排聲明（渲染放大核對；符號重載與排印滑失都如實列出）**：

1. **$\sigma_{\Delta\phi}^2$ 一符兩用**：Eq.(40)–(44) 的 LHS 是**相位** jitter（rad²）；
   Eq.(45) 起 LHS 印的還是 $\sigma_{\Delta\phi}^2$，卻多了 $1/\omega_0^2$、原文也明說是
   timing jitter——實為 $\sigma_{\Delta T}^2=\sigma_{\Delta\phi}^2/\omega_0^2$（s²，
   即 Eq.(10) 的換算）。該頁把 $\sigma_{\Delta\phi}$ 與 $\sigma_{\Delta t}$ 分開命名，
   就是為了拆掉這顆地雷。
2. **Eq.(45) 展開行漏了兩個記號**：中項漏印 $E$、交叉項漏印係數 2（$[a-b]^2$ 的
   交叉項是 $2ab$；平穩下前兩項合為 $2R_\phi(0)$，要落到 Eq.(47) 交叉項非
   $2R_\phi(\Delta T)$ 不可）。Eq.(47) 本身印刷正確——滑失沒有傳染下去。
3. **$\tau$ 與 $\Delta T$ 混用**：Eq.(46) LHS 寫 $R_\phi(\tau)$、RHS 用 $\Delta T$；
   Eq.(49) 的核寫 $\sin^2(\pi f\tau)$，這個 $\tau$ 就是延遲 $\Delta T$。
4. **Eq.(51) 分子印作 $f$**：由 Eq.(50) 的 $\kappa$（時間版）乘 $\sqrt T=f_0^{-0.5}$
   得 $\sigma_{CTC}=\kappa\sqrt T$，分子應是 offset 頻率 $\Delta f$——印刷把
   $\Delta$ 吃掉了（「對應的 paper / 公式」節的轉錄已同步標注）。
5. Eq.(48) 的積分限 $\int_{-\infty}^{\infty}$ 宣告了此處 $S_\phi$ 是**雙邊**譜——
   全文唯一洩漏慣例的地方，Eq.(49) 的 8 因此內建一顆記帳的 2（見下表）。

## A.3 逐步對照：論文的兩條路 ↔ 該頁的推導

| [P2] | 那一步在做什麼 | 該頁對應 | 因子對帳（對第 0 步表） |
|---|---|---|---|
| Eq.(40) | 定義相位 jitter | 第 2 步的一階差分 $P_k(N)$（相位語言） | — |
| Eq.(41) | $\Delta\phi$＝ISF 加權的窗積分 | 4.2 引用的 [P1] Eq.(11)（積分限改成窗） | — |
| Eq.(42) | 平方展開成雙重積分＋$E[i(\tau_1)i(\tau_2)]$ | 4.2 第一行（代入自相關前的一般式） | 對任意（非白）自相關都成立 |
| Eq.(43) | 白噪 $R_{ii}=\tfrac12(\overline{i_n^2}/\Delta f)\delta$ 塌成單重積分 | 4.2 的 $R_i(\tau)=\tfrac{S_i}{2}\delta(\tau)$ | **同一顆 $\tfrac12$**：單邊 PSD ↔ 雙邊平坦位準 |
| Eq.(44) | $\int\Gamma^2\to\Gamma_{rms}^2\Delta T$（$\Delta T\gg T$ 或 $=mT$） | 4.2 括號註「整數週期精確」＋4.3 的 $\kappa^2NT$ | Eq.(44)＝主文 Eq.(11)＝$\kappa^2\Delta T$ |
| Eq.(45)–(47) | WSS 展開：差的變異數 $=2[R_\phi(0)-R_\phi(\Delta T)]$ | 路 A 第 1 步（同式） | **Eq.(47) 的 2**＝「差的變異數」的 2 |
| Eq.(48) | Khinchin 定理（雙邊譜、$\int_{-\infty}^{\infty}$） | 路 A 第 2 步（單邊 cos 版） | $S_\phi^{DS}=S_\phi/2$ |
| Eq.(49) | $\dfrac{8}{\omega_0^2}\displaystyle\int_0^\infty S_\phi^{DS}\sin^2(\pi f\tau)\,df$ | 核 (b) 的 $\dfrac{1}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\,4\sin^2 df$ | **8＝2（雙邊→單邊）×4（差分核）**，$1/\omega_0^2$＝相位→時間——第 0 步表第二欄字面重現 |
| Eq.(50) | 由主文 (6)+(12) 讀出 $\kappa\leftarrow\mathcal{L}$ | 4.5（負指數＝「低於載波 dB 數」讀法，v5 註） | 吃 $/2$ 慣例的 $\mathcal{L}$ |
| Eq.(51) | $\sigma_{CTC}=\kappa\sqrt T$（一週期版） | 4.4 末註（相鄰差定義再乘 $\sqrt2$） | 印刷分子 $f$ 應讀 $\Delta f$ |

## A.4 誰跳過了什麼（兩個方向都記帳）

**[P2] 跳過、該頁補上的**：

- **平穩性的 rigor gap**：Eq.(45)–(47) 需要 $R_\phi(0)$ 有限；自由振盪器的 $\phi$
  是隨機漫步，$R_\phi(0)$ 發散（正是該頁路 A 開頭的坦白）。差
  $R_\phi(0)-R_\phi(\Delta T)$ 有限、結論不受影響，但嚴格化要走該頁**路 B**
  （只要求 $\nu=\dot\phi$ 平穩）——論文沒有處理這一步。
- **慣例不聲明**：$S_\phi$ 單邊還是雙邊，全文沒有一句話；只有 Eq.(48) 的積分限
  洩底。該頁第 0 步的三欄表就是把這件事攤開（v5 正是靠這個積分限反推，才把
  「文獻 8 係數版」對上單邊 $4\sin^2$ 核）。
- **兩條路在論文裡沒有互鎖**：Eq.(44) 停在時域、Eq.(49) 停在頻域；論文從未把
  白噪譜代入 (49) 驗證會回到 (44)。該頁 4.1 的
  $\int_0^\infty\sin^2(ax)/x^2\,dx=\pi a/2$ ＋ 4.3 的代入就是補上的閉環
  （下方 code 把兩路各算一遍，同一個數）。
- flicker $1/f^3$ 的時域封閉式（第 5 步的 log 式）與 c2c 的 $16\sin^4$ 核
  （核 (c)；Eq.(51) 只是一週期版）論文都沒有給。

**該頁帶過、[P2] 寫全的**：

- **Eq.(42) 的一般雙重積分**：該頁 4.2 直接跳「白噪 δ 相關 ⇒ 單重積分」；論文把
  $\Gamma(\omega_0\tau_1)\Gamma(\omega_0\tau_2)\,E[i(\tau_1)i(\tau_2)]$ 的一般式
  明寫出來——那是任何色噪自相關都能接的起點，白噪只是特例。
- **成立條件印在式子裡**：Eq.(44) 的 "for $\Delta T\gg T$ or $\Delta T=mT$" 把
  「$\int\Gamma^2$ 換 $\Gamma_{rms}^2\Delta T$ 何時精確」印在等號旁；該頁 4.2 只在
  括號裡帶過。短或非整數 $\Delta T$ 時有 $O(T/\Delta T)$ 級的 $\Gamma^2$ 漣漪殘差。

## A.5 兩路重演白噪 FM 變異數（# -> 可驗證）

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal

F0, T = 5e9, 2e-10
W0 = 2 * np.pi * F0
QMAX, SI, GRMS = 1e-12, 1e-24, 0.5      # canonical 參數
N = 100
DT = N * T                              # ΔT = mT（Eq.(44) 的成立條件）

# 路線一：[P2] Appendix A 時域自相關路——Eq.(42) 代 R_ii=(S_i/2)δ 塌成 Eq.(43)
tau = np.linspace(0.0, DT, 200 * N + 1)
gam = np.sqrt(2.0) * GRMS * gamma_lc_ideal(W0 * tau)     # Γrms=0.5 的 LC 形 ISF
var_43 = 0.5 * SI / QMAX**2 * np.trapezoid(gam**2, tau)  # Eq.(43) 數值積分
var_44 = 0.5 * SI / QMAX**2 * GRMS**2 * DT               # Eq.(44) ＝主文 Eq.(11)
print(f"{var_43:.4e}")            # -> 2.5000e-09 rad^2（Eq.(43)，σ²_Δφ @ N=100）
print(f"{var_43/var_44:.4f}")     # -> 1.0000（ΔT=mT 時 ∫Γ² 精確 = Γrms²ΔT）

# 路線二：該頁核路——單邊 S_φ=2κ²/(2πf)² 乘 4sin²(πfΔT) 核
kappa2 = GRMS**2 / QMAX**2 * SI / 2                      # κ²=Γrms²S_i/(2q_max²)
print(f"{kappa2:.4f}")            # -> 0.1250 rad^2/s（與 Eq.(44) 前置常數同一顆）
x = np.linspace(1e-8, 1e4, 4_000_001)                    # x = fΔT
core = np.trapezoid(np.sin(np.pi * x)**2 / x**2, x) + 0.5 / x[-1]  # 尾巴 sin²→1/2
var_kernel = 2 * kappa2 * DT / np.pi**2 * core           # = κ²ΔT（4.3 節解析值）
print(f"{var_kernel/var_43:.4f}") # -> 1.0000（頻域核 = Appendix A 自相關路，同一數）

# 對帳 [P2] Eq.(49)：8/ω₀² × 雙邊譜 S_φ^DS=κ²/(2πf)²，LHS 是時間版變異數
var_49 = 8 / W0**2 * (kappa2 * DT / 4 / np.pi**2) * core
print(f"{var_49/(kappa2*DT/W0**2):.4f}")   # -> 1.0000（8 = 2(雙邊→單邊)×4(核)）
print(f"{np.sqrt(var_49)*1e15:.2f} fs")    # -> 1.59 fs（σ_ΔT @ N=100 = √100×0.159 fs）
```

前兩個 print 走 [P2] Eq.(43)→(44)（時域自相關路），其餘四個走該頁核 (b) 與
Eq.(49) 的雙邊記帳版——**同一顆振盪器、兩條路、同一個數
$\kappa^2\Delta T=2.5\times10^{-9}\ \text{rad}^2$**。Appendix A 與該頁第 3/4 步
是同一個定理的兩份證明；差別只在論文把慣例藏在積分限裡、該頁把它印在第 0 步。

## 適用與失效條件

| 條件 | 兩條路（本頁）與該頁核路一致時 | 不一致 / 要小心時 |
|---|---|---|
| $\Delta T\gg T$ 或 $\Delta T=mT$（整數週期） | Eq.(44) 的 $\int\Gamma^2\to\Gamma_{rms}^2\Delta T$ 精確，與該頁 4.3 的 $\kappa^2NT$ 逐位吻合（A.5 code） | 短或非整數 $\Delta T$：$\Gamma^2$ 有 $O(T/\Delta T)$ 級漣漪殘差，Eq.(44) 只是近似 |
| $S_\phi$ 的慣例（單邊／雙邊）已知 | Eq.(49) 的 8＝2（雙邊→單邊）×4（差分核），可與該頁單邊 $4\sin^2$ 核精確對上（A.3 表） | 慣例不明時直接套 Eq.(49) 的「8」會與該頁單邊核差 2 倍（jitter 差 $\sqrt2$） |
| 只要相位增量／頻率雜訊 $\nu=\dot\phi$ 平穩 | 該頁路 B 的核公式對隨機漫步 $\phi$（$R_\phi(0)$ 發散）仍嚴格成立 | 若堅持論文 Eq.(45)–(47) 的 WSS 展開（要求 $R_\phi(0)$ 有限），需要額外的收斂論證（A.4） |
| 只算白噪 FM 的 $1/f^2$ 段 | Eq.(50)/(51) 可直接讀出 $\kappa$（吃時域 $/2$ 慣例的 $\mathcal{L}$） | flicker/其他色噪主導、或 $\mathcal{L}$ 記帳搞錯（$/2$ vs $/4$）：Eq.(50)/(51) 失效，需回到該頁第 5 步的 log 封閉式 |

## 重點回顧

- [P2] Appendix A 用**兩條獨立路**證同一件事：**A.1** 白噪時域自相關路（Eq.(40)–(44)，收斂到主文 Eq.(11)）、**A.2** 自相關＋Khinchin 路（Eq.(45)–(49)，另加兩條白噪特例推論 Eq.(50)/(51)）。
- **A.3** 逐步對照表把論文每一條式子釘回該頁對應的推導與慣例（哪個 2 屬於哪一步），**A.4** 誠實記帳兩邊各自跳過與寫全的地方（論文沒聲明 $S_\phi$ 慣例、沒把兩條路互鎖；該頁沒寫出 Eq.(42) 的一般雙重積分）。
- **A.5** 的 Python 把時域自相關路（Eq.(43)）與該頁的頻域核路各算一次，同一顆振盪器、同一個數 $\kappa^2\Delta T=2.5\times10^{-9}\ \text{rad}^2$（`# ->` 全部印 1.0000）。
- 論文本身有幾處**印刷滑失**（Eq.(45) 展開式漏 $E$ 與係數 2、Eq.(51) 分子印作 $f$ 應讀 $\Delta f$），本頁照排轉錄並在旁註明，不代論文修正。

## 延伸閱讀

- 三個核的第一原理推導與白噪/flicker 封閉式：[jitter_kernels](/02_foundations/jitter_kernels)
- PSD / phase noise / jitter 基礎：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- 隨機過程與平穩性基礎：[stochastic_noise_basics](/02_foundations/stochastic_noise_basics)
- Allan variance（另一種差分核）：[allan_variance](/02_foundations/allan_variance)
- 完整文獻列表：[references](/99_appendix/references)
