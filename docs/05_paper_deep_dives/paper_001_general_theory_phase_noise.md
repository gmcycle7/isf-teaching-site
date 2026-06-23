---
title: "[P1] A General Theory of Phase Noise in Electrical Oscillators"
description: Hajimiri–Lee 1998 精讀：ISF、q_max normalization、1/f² 與 1/f³ phase noise、三條設計法則。
---

# A General Theory of Phase Noise in Electrical Oscillators

> **先備知識（建議先讀）**：[oscillator_phase](/02_foundations/oscillator_phase)（limit cycle 與 excess phase 的幾何）→ [lti_vs_ltv](/02_foundations/lti_vs_ltv)（為何振盪器是 LTV、不是 LTI）→ [stochastic_noise_basics](/02_foundations/stochastic_noise_basics)（white／flicker noise PSD）。這頁是全站的**地基**，其餘四篇 deep-dive 都建立在它之上。

這是整個課程的**地基**。它第一次把「振盪器對 noise 的反應」正確地建模成
**LTV（linear time-variant，線性時變）** 系統，引入了 **ISF（Impulse Sensitivity
Function，脈衝敏感度函數）** $\Gamma(\omega_0\tau)$，並用它一口氣推出 1/f²、1/f³
phase noise 的封閉式與三條沿用至今的設計法則。後面四篇論文（[P2][P3][P4]）全建立在這頁的
觀念上。

## Citation

> **[P1]** A. Hajimiri and T. H. Lee, *"A General Theory of Phase Noise in Electrical
> Oscillators,"* IEEE J. Solid-State Circuits, vol. 33, no. 2, pp. 179–194, Feb. 1998.
> （檔案 `general.pdf`，paper_001）

## One-sentence contribution

振盪器對 noise 不是 LTI 而是 **LTV**：同一顆 noise 脈衝在波形不同相位注入會造成不同的相位
偏移，這個「相位敏感度」就是 ISF $\Gamma(\omega_0\tau)$；用它能把任意 noise 推導成
phase noise，並得到 $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$ 的設計法則（claim C1, C3）。

## Why this paper matters

在 [P1] 之前，工程界主要用 **Leeson 模型**（1966，半經驗式）——它能畫出 1/f³、1/f²、平坦
三段斜率，卻說不清楚「為什麼 1/f³ 的轉折點不等於 device 的 1/f corner」「為什麼某些波形
比較不會把 flicker noise 上轉成 close-in phase noise」。[P1] 給出物理答案：

- **LTV 而非 LTI**（claim C1）：振盪器是 autonomous（自主）系統，沒有絕對時間參考。一個
  noise 脈衝打在波峰幾乎只改振幅，打在 zero-crossing（過零點）幾乎全變相位。所以「同一個
  脈衝、不同注入時刻、不同效果」——這就是時變。LTI 的卷積 $h(t-\tau)$ 抓不到這件事。
- **相位會永久累積、振幅會被拉回**（claim C2）：振盪器有 amplitude restoring（振幅恢復）
  機制把振幅擾動拉回 limit cycle，但相位**沒有恢復力**，每一次踢都永久留下。phase noise
  就住在這個「會累積的相位」裡。
- **把上面兩點量化成一個函數 $\Gamma$**，於是 phase noise 不再靠擬合，而是能從波形與 noise
  PSD **算出來**，並指出設計旋鈕。

它也把 Leeson、cyclostationary noise（週期穩態雜訊）都收成自己的特例（claim C9）。

## Main assumptions

照 paper_metadata（paper_001.assumptions）：

1. **noise 是小擾動**——相位反應可線性化（要求 $\Delta q\ll q_{max}$）。
2. **振幅擾動會衰減**（穩定 limit cycle），只有相位永久留下，所以「只追蹤相位」就夠。
3. **ISF 已知、週期、且與頻率無關**——$\Gamma$ 是 $2\pi$ 週期函數，只由 steady-state 波形決定。
4. **hard-switching／大訊號週期穩態**定義 ISF——$\Gamma$ 是在那個穩態軌跡上量到的敏感度。

> **物理直覺**：把振盪器狀態畫在 2-D 平面，穩態沿 limit cycle 轉圈。一顆電流脈衝把狀態點
> 推一下；**沿環的切向分量**變成相位（永久留），**離環的徑向分量**變成振幅（被拉回）。
> 同一個脈衝在不同相位踢，切向／徑向比例不同——把這比例整理成只跟注入相位有關的週期函數，
> 就是 ISF。完整幾何見 [oscillator_phase](/02_foundations/oscillator_phase)。

## Key equations

下面挑 [P1] 最關鍵的幾條（Eq.(1) 與 Eq.(9)–(24)）。每條的 LaTeX **逐字**取自規範第 3 節，
含 `[P1] Eq.(n) page` 引用；常數不自行更動。

### Eq.(1)：輸出分解（phase noise 住在哪裡）

**Original formula**（[P1] Eq.(1), p.181）：

$$
V_{out}(t)=A(t)\,f\!\big(\omega_0 t+\phi(t)\big)
$$

**Meaning**：任何振盪器的輸出都能拆成「瞬時振幅 $A(t)$」乘上「週期波形 $f$ 在
$\omega_0 t+\phi(t)$ 取值」。$f$ 是 steady-state 波形（不一定是 sin）。**phase noise
就住在 excess phase（多餘相位）$\phi(t)$**，amplitude noise 住在 $A(t)$。

**Step-by-step**：理想振盪是 $f(\omega_0 t)$；noise 進來後，振幅被擾動成 $A(t)$、相位多了
$\phi(t)$。因為振幅有恢復力（假設 2），$A(t)\to A_0$，所以分析 phase noise 時可把 $A(t)$
當常數，只追 $\phi(t)$。這一步把問題從「2-D 狀態」縮成「1-D 相位」。

### Eq.(9)：charge → voltage step（noise 的物理入口）

**Original formula**（[P1] Eq.(9), p.182）：

$$
\Delta V=\frac{\Delta q}{C_{node}}
$$

**Meaning**：一顆電流脈衝在節點電容上沉積電荷 $\Delta q=\int i\,dt$，瞬間把節點電壓抬一步
$\Delta V$。這是 noise 進入振盪器狀態的**物理入口**。

**Dimension check**：$[\text{C}]/[\text{F}]=[\text{C}]/[\text{C/V}]=[\text{V}]$ ✓。

### Eq.(10)–(11)：ISF 與 LTV phase response（核心）

**Original formula**（[P1] Eq.(10), p.182，excess-phase impulse response）：

$$
h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau)
$$

**Original formula**（[P1] Eq.(11), p.182，卷積式）：

$$
\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau
$$

**Meaning**：$\Gamma(\omega_0\tau)$ 是無因次、$2\pi$ 週期的 ISF；$q_{max}=C_{node}V_{max}$
是節點最大電荷擺幅。**$u(t-\tau)$（unit step）很關鍵**：相位步階一旦造成就永久保持（相位無
恢復力），所以脈衝響應帶一個階梯而不是衰減項。Eq.(11) 是對所有過去 noise 的疊加積分。

**Step-by-step derivation**（逐步、不跳步）：

$$
\begin{aligned}
&\text{(i) 電流脈衝沉積電荷：}\quad \Delta q=\int i_n(\tau)\,d\tau \\
&\text{(ii) 電荷抬高電壓（Eq.9）：}\quad \Delta V=\frac{\Delta q}{C_{node}} \\
&\text{(iii) 投影到 limit cycle 切向，得相位步階：}\quad \Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q \\
&\text{(iv) 步階永久保持，寫成脈衝響應：}\quad h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau) \\
&\text{(v) 對任意}i_n\text{線性疊加（卷積）：}\quad \phi(t)=\int_{-\infty}^{\infty} h_\phi(t,\tau)\,i_n(\tau)\,d\tau=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau
\end{aligned}
$$

**$\Gamma$ 為何無因次**：$\Delta\phi$ 是 rad（無因次），$\Delta q/q_{max}$ 也無因次，所以
$\Gamma$ 必須無因次 ✓。注意 $h_\phi$ 依賴**絕對注入時刻 $\tau$**（透過 $\Gamma(\omega_0\tau)$）
而非只依賴 $t-\tau$——這正是 **LTV** 的指紋（claim C1）。完整逐步推導在
[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) 與
[convolution_derivation](/03_isf_core_theory/convolution_derivation)。

**Numerical example（例 A）**：$q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$、$f_0=5$ GHz。

$$
\Delta\phi=\frac{0.5\times(1\times10^{-15})}{1\times10^{-12}}=5\times10^{-4}\ \text{rad}\;(\approx0.0286^\circ),\quad \Delta t=\frac{\Delta\phi}{2\pi f_0}=15.9\ \text{fs}.
$$

**Python verification**：

```python
from simulations.common.isf_utils import impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error

dphi = impulse_to_phase_step(delta_q=1e-15, gamma_value=0.5, qmax=1e-12)
dt   = phase_to_time_error(dphi, f0=5e9)
print(dphi, "rad", dt*1e15, "fs")   # -> 0.0005 rad  15.92 fs
```

### Eq.(12)–(13)：ISF 傅立葉級數與分諧波

**Original formula**（[P1] Eq.(12), p.183）：

$$
\Gamma(\omega_0\tau)=\frac{c_0}{2}+\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)
$$

**Original formula**（[P1] Eq.(13), p.183）：

$$
\phi(t)=\frac{1}{q_{max}}\!\left[\frac{c_0}{2}\!\int_{-\infty}^{t}\!i_n\,d\tau+\sum_{n=1}^{\infty}c_n\!\int_{-\infty}^{t}\!i_n\cos(n\omega_0\tau+\theta_n)\,d\tau\right]
$$

**Meaning**：把 ISF 展成傅立葉級數，每個諧波係數 $c_n$ 告訴你「振盪器把 $n\omega_0$ 附近的
noise 搬到 carrier 的能力」。$c_0$（DC 項，ISF 的 DC **值**是 $c_0/2$）特別重要——它是把
device 的低頻 1/f noise 上轉成 close-in 1/f³ phase noise 的**唯一**通道（見 Eq.(23)–(24)）。

**Step-by-step**：把 Eq.(12) 代進 Eq.(11)，逐項展開就是 Eq.(13)。物理上這是一張
**頻率搬移圖**（[P1] Fig. 8）：$n\omega_0$ 附近的 noise 被第 $n$ 諧波 down-convert 到
baseband 的慢相位調變。完整推導與符號陷阱（$c_0$ vs $c_0/2$）見
[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)。

### Eq.(20)：Parseval / rms ISF

**Original formula**（[P1] Eq.(20), p.185）：

$$
\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}|\Gamma(x)|^2dx=2\,\Gamma_{rms}^2
$$

**Meaning**：把所有諧波能量加起來（Parseval）就是 $2\Gamma_{rms}^2$。這條讓 Eq.(19)
的「對所有諧波求和」收成一個漂亮的 $\Gamma_{rms}^2$。

**Step-by-step**：對 Eq.(12) 兩邊平方、在一個週期 $[0,2\pi]$ 積分、用三角函數正交性（不同
諧波的交叉項積分為 0）即得。詳見 [rms_isf](/03_isf_core_theory/rms_isf)。

### Eq.(21)：1/f² phase noise（招牌結果）

**Original formula**（[P1] Eq.(21), p.185）：

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)
$$

**Meaning**：白噪電流源造成的 SSB phase noise，在 1/f² 區（$-20$ dB/dec）。**phase noise
正比 $\Gamma_{rms}^2/q_{max}^2$**（claim C3）——這就是三條設計法則裡最重要的一條：拉大
$q_{max}$、壓小 $\Gamma_{rms}$。

**Step-by-step**：先由 Eq.(16)/(17) 得單音注入的相位調變（$\propto c_n/\Delta\omega$），
再由 Eq.(18) 得單邊功率，對白噪在所有諧波上求和（Eq.(19)）並用 Eq.(20) 收成 $\Gamma_{rms}^2$。

**Numerical example（例 B）**：$f_0=5$ GHz、$\Delta f=1$ MHz、$q_{max}=1$ pC、
$\Gamma_{rms}=0.5$、$S_i=10^{-24}$ A²/Hz。$\Delta\omega=2\pi\times10^6=6.283\times10^6$
rad/s，$\Delta\omega^2=3.948\times10^{13}$。

$$
\mathcal{L}=10\log_{10}\!\left(\frac{0.25}{10^{-24}}\cdot\frac{10^{-24}}{4\times3.948\times10^{13}}\right)=10\log_{10}(1.583\times10^{-15})=-148.0\ \text{dBc/Hz}.
$$

這是**單一白噪源的理想值**；真實電路有多個源、cyclostationary、flicker，會更高。完整逐步與
著名的 factor-of-2（SSB 記帳慣例）討論見
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

### Eq.(22)–(24)：flicker 上轉與 1/f³ corner

**Original formula**（[P1] Eq.(22), p.185，device flicker）：

$$
\overline{i_{n,1/f}^2}=\overline{i_n^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}
$$

**Original formula**（[P1] Eq.(23), p.185，1/f³ phase noise）：

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}\right)
$$

**Original formula**（[P1] Eq.(24), p.185，1/f³ corner）：

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2
$$

**Meaning**：device 的 1/f noise 只能透過 ISF 的 **DC 項 $c_0$** 上轉成 close-in 1/f³
phase noise（claim C4）。最反直覺、也最重要的一點（claim C5）：**1/f³ corner $\ne$ device
1/f corner**——它被 $(c_0/\Gamma_{rms})^2/2$ 縮放。若波形上下對稱、$c_0$ 很小，1/f³ corner
可以被推到遠低於 $\omega_{1/f}$。這就是「symmetry 設計法則」的數學根據。

**Step-by-step**：把 Eq.(22) 的 1/f noise 代進 Eq.(19)；因為只有 DC 係數 $c_0$ 對 baseband
有 DC 響應，求和只剩 $c_0^2$ 項，得 Eq.(23)（注意分母是 $8$ 不是 $4$）。令 Eq.(21) 的 1/f²
與 Eq.(23) 的 1/f³ 相等，解出交點頻率即 Eq.(24)。$c_0/c_1\approx \dfrac{c_0/\Gamma_{rms}}{\sqrt2}$
的近似來自「對稱波形以 $c_1$ 為主，$\Gamma_{rms}^2\approx c_1^2/2$」（即 $c_1\approx\sqrt2\,\Gamma_{rms}$，故 $c_0/c_1=(c_0/\Gamma_{rms})/\sqrt2$，與 $c_0^2/(2\Gamma_{rms}^2)=(c_0/c_1)^2$ 一致）。

**Numerical example**：若 $\omega_{1/f}=2\pi\times1$ MHz、且波形相當對稱使
$c_0/\Gamma_{rms}=0.1$，則 $\Delta\omega_{1/f^3}=\omega_{1/f}\times(0.1)^2/2=\omega_{1/f}\times5\times10^{-3}$，
即 1/f³ corner $\approx5$ kHz——遠低於 device 的 1 MHz
corner。對稱性把 close-in noise 推走了 200 倍頻率。完整推導見
[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)。

## Key figures

| 論文圖 | 頁 | 內容 | 本站對應 |
|---|---|---|---|
| Fig. 4 | 181 | 脈衝打在 peak vs zero-crossing 的 state-space 效果 | toy 重現於 lab_01／lab_02；見 `limit_cycle_phase_amplitude.png` |
| Fig. 6 | 182 | Colpitts 與 5 級 ring：excess phase vs 注入電荷（小電荷線性） | 佐證 $\Delta\phi\propto\Delta q$ 線性假設 |
| Fig. 7 | 183 | (a) LC、(b) ring 的波形與 ISF | toy 對照 `lc_vs_ring_isf_comparison.png` |
| Fig. 8 | 183 | $n\omega_0$ 附近 noise 搬到 carrier 的頻率搬移圖 | [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) |
| Fig. 12 | 185 | $\overline{i^2}/f$ 與 $\mathcal{L}(\Delta f)$：1/f³、1/f²、floor | flicker upconversion lab |

本站用 Python toy model 重畫了概念對照圖（**非 transistor-level**）：

![理想 LC 的 -sin ISF 與數值萃取對照](/figures/isf_impulse_sweep_sinusoidal.png)

## Design insights

[P1] 把 phase noise 設計濃縮成三個旋鈕（都直接讀自 Eq.(21) 與 Eq.(24)）：

1. **拉大 $q_{max}$**（節點電荷擺幅）：$\mathcal{L}\propto1/q_{max}^2$，每加倍 $q_{max}$
   就降 6 dB。加大電容、加大電壓擺幅、提高功率都往這走。
2. **壓小 $\Gamma_{rms}$**：讓 noise 注入的時刻盡量落在 ISF 小的地方。LC 的 $\Gamma=-\sin$
   在波峰為 0，所以「在波峰附近補能量」最不傷 phase noise。
3. **靠 symmetry 壓 $c_0$**：上升／下降對稱的波形 $c_0\approx0$，把 1/f³ corner（Eq.(24)）
   推到很低，close-in phase noise 大幅下降。這條在 [P2] 的 ring 實驗（Fig. 17）得到直接驗證。

設計面的整理見 [symmetry](/06_design_insights/symmetry) 與
[lc_vs_ring](/06_design_insights/lc_vs_ring)。

## Limitations

照 paper_metadata（paper_001.limitations）：

- 1/f³ 段歷史上靠經驗連結；本理論澄清它由 $c_0$ 決定，但**確切 $c_0$ 仍需萃取**。
- 實際電路的 $\Gamma$ 要靠 transient impulse 模擬或 adjoint/PSS 法萃取；封閉式是一階近似。
- **AM–PM 轉換與強非線性**沒被一階 phase-only 模型完全涵蓋（這正是 [P4] 用 APF 補的洞）。
- 嚴謹的數學地基（PPV／adjoint／Floquet）**不在這 5 篇 PDF**，屬外部文獻（claim C13），
  見 [effective_isf](/03_isf_core_theory/effective_isf)。

## Relationship to other papers

- **[P2]** 把這頁的 ISF 套到 ring oscillator：用同一個 $\Gamma_{rms}^2/q_{max}^2$ 比例導出
  jitter $\kappa$，並研究 $\Gamma_{rms}\propto N^{-3/4}$ scaling（claim C8）。
- **[P3]/[P4]** 把同一個 ISF 從「隨機 noise」延伸到「確定注入」：[P3] 用 $\Gamma$ 寫出廣義
  Adler 方程（claim C10），[P4] 補上振幅版的 APF（claim C11）。
- **[P5]** 與本頁**無關**（sense amplifier，claim C12）；唯一概念橋樑是 regeneration／正回授。
- **Leeson 模型** 是本理論的特例（claim C9）；Leeson 公式列在
  [equation_index](/01_paper_map/equation_index) 第 19 條，標為 reference（不在 5 篇 PDF）。

## 延伸閱讀 / 對應教學頁

這頁是「站在論文高度」的鳥瞰；下面五頁把 [P1] 的每一塊**逐步推到底**，建議照這個順序展開：

| 本頁的哪一塊 | 對應教學頁 | 那頁多給你什麼 |
|---|---|---|
| Eq.(10)–(13) ISF 與 LTV phase response | [isf_definition](/03_isf_core_theory/isf_definition) | ISF 的完整定義、$2\pi$ 週期性、無因次性的逐項建立 |
| Eq.(11) 卷積式 $\phi(t)=\frac{1}{q_{max}}\int\Gamma\,i_n\,d\tau$ | [convolution_derivation](/03_isf_core_theory/convolution_derivation) | 從 impulse response $h_\phi(t,\tau)$ 到疊加積分的不跳步推導，含 LTV 指紋 |
| Eq.(19)–(21) 白噪 $\to$ 1/f² phase noise | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) | down-conversion、factor-8 求和、著名 factor-of-2 SSB 記帳爭議 |
| Eq.(22)–(24) flicker 上轉與 1/f³ corner | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) | 為何只有 $c_0$ 能上轉、1/f³ corner $\ne$ device corner 的完整代數 |
| 三條設計法則裡的「靠 symmetry 壓 $c_0$」 | [symmetry](/06_design_insights/symmetry) | 對稱性如何決定 $c_0$、設計旋鈕、與 [P2] Fig. 17 的實驗對照 |

> **怎麼讀**：理論細節與數值手感都在 [03_isf_core_theory](/03_isf_core_theory/isf_definition)；想動手算回 [numerical_feeling](/04_simulation_labs/numerical_feeling)。本頁只負責把這些塊**串成一篇論文的故事**。

## What to remember

- **LTV，不是 LTI**：同一脈衝、不同注入相位、不同效果——這就是 ISF $\Gamma(\omega_0\tau)$。
- **相位累積、振幅被拉回**：phase noise 住在會累積的相位裡（Eq.(1)、Eq.(11) 的積分上限是 $t$）。
- **招牌公式**：$\mathcal{L}\propto\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{\Delta\omega^2}$（Eq.(21)）。
- **三條設計法則**：拉大 $q_{max}$、壓小 $\Gamma_{rms}$、靠 symmetry 壓 $c_0$。
- **1/f³ corner $\ne$ device 1/f corner**（Eq.(24)）——對稱性能把它推得很低。
- 核心推導全在 [03_isf_core_theory](/03_isf_core_theory/isf_definition)；數值手感在
  [numerical_feeling](/04_simulation_labs/numerical_feeling)。
