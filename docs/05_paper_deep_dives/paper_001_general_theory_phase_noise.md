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
| Fig. 20–22 | 189–190 | 注入實驗：sideband $\propto I^2$、$-20$ dB/dec、對稱 vs 不對稱節點 | 見下方 Sec. V 一節 |
| Fig. 23–24 | 190–191 | 232／115 MHz ring 的 $\mathcal{L}(\Delta f)$ 量測（1/f³ 與 1/f² 段分明） | 見下方 Sec. V 一節 |

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

## 論文自己的端到端矽驗證（Sec. V）

> **這一節要回答什麼**：本站的數值鏈（例 B 的 $-148.0$ dBc/Hz）用的是乾淨的教學數字；
> 同一條「process 資料 → $C_{node}$ → $q_{max}$ → $\overline{i_n^2}/\Delta f$ →
> $\Gamma_{rms}^2$ → Eq.(21) → $\mathcal{L}$」管線，[P1] Sec. V（pp.189–191）在**真矽**上
> 用八個實驗驗證過，預測與量測差 0.2–0.7 dB，而且輸入全是**事前可得**的量（process 參數、
> 幾何、擺幅、萃取的 ISF），不是事後擬合。下面先鳥瞰八個實驗，再把數字最完整的一條鏈逐步重演。

八個實驗一覽（數字逐字取自 [P1] pp.189–191）：

| # | 實驗 | 驗證什麼 | 論文結果 |
|---|---|---|---|
| 1 | 5 級 5.4 MHz CMOS ring，正弦電流注入掃幅度（$f_m=100$ kHz、$f_0+f_m=5.5$ MHz、$2f_0+f_m=10.9$ MHz、$3f_0+f_m=16.3$ MHz） | Eq.(18) 的電流→sideband 線性 | 上下 sideband 相等（量測精度 0.2 dB 內）；最佳擬合斜率 19.8 dB/decade vs 預測 20（Fig. 20） |
| 2 | 同 ring，20 µA (rms)，掃 $f_m$ | Eq.(18) 的 $1/\Delta\omega$ 相依 | 四組注入頻率全部 $-20$ dB/decade（Fig. 21） |
| 3 | 5 級 ring，其中一級加 extra pulldown NMOS 製造不對稱，注入 20 µA (rms) | 低頻上轉由 $c_0$（波形對稱性）決定 | 打在不對稱節點 sideband 大 7 dB；對稱節點幾乎不變（Fig. 22） |
| 4 | **5 級 232 MHz single-ended ring（2-µm、5-V CMOS）** | Eq.(21) + Eq.(24) 全鏈預測 | 預測 $-114.7$ vs 量測 $-114.5$ dBc/Hz @ 500 kHz；corner 預測 75 vs 量測 80 kHz（Fig. 23） |
| 5 | 11 級 115 MHz ring（同一顆 die） | 同上，換 $N$ 與元件尺寸 | 預測 $-122.1$ vs 量測 $-122.5$ dBc/Hz @ 500 kHz；corner 預測 43 vs 量測 45 kHz（Fig. 24） |
| 6 | 7 級 current-starved ring（$f_0$ 定在 60／50 MHz），控制電壓獨立調 rise/fall | 對稱性只該動 1/f³、不動 1/f²（Eq.(24)、Eq.(30)） | 調對稱大幅壓 1/f³ 段、1/f² 段幾乎不變；存在最佳對稱點（Fig. 25／26） |
| 7 | 4 級 differential 200 MHz ring（0.5-µm） | Eq.(21)；「half-circuit 對稱才算數」 | 預測 $-103.2$ vs 量測 $-103.9$ dBc/Hz @ 1 MHz；差動對稱仍有明顯 1/f³ 段（Fig. 27） |
| 8 | Bipolar Colpitts 100 MHz，掃 $n=C_1/(C_1+C_2)$（$C_{eq}$ 固定） | cyclostationary／$\Gamma_{eff}$ 的導通角效應 | 存在最佳導通角，$n\approx0.2$ 相位雜訊最低——經典 Colpitts 經驗法則的理論根據（Fig. 28） |

### 全鏈重演：第四個實驗（5 級、232 MHz、2-µm 5-V CMOS）

這是全論文數字最完整的一條鏈——每個輸入都印在 p.190 上，我們逐步代回去。

**Step 0 — 論文的 process／幾何輸入**（[P1] p.190，逐字轉錄）：

| 量 | 值 | 單位 |
|---|---|---|
| gate oxide 厚度 $t_{ox}$ | 25 | nm |
| $V_{TN}$ | 0.6 | V |
| $V_{TP}$ | 0.53 | V |
| $(W/L)_N$ | 3 µm ／ 2 µm | — |
| $(W/L)_P$ | 5 µm ／ 2 µm | — |
| lateral diffusion $L_d$ | 0.1 | µm（故 $L_{\text{eff}}=2-2\times0.1=1.8$ µm） |
| 每節點總電容 $C_{total}$（含 parasitic，由 process＋幾何算出） | 35.7 | fF |
| 量測方式 | delay-based | —（Fig. 23 可見分明的 1/f³ 與 1/f² 段） |

**Step 1 — $q_{max}$**：5-V process，節點擺幅 $V_{swing}=5$ V：

$$
q_{max}=C_{total}\,V_{swing}=35.7\ \text{fF}\times5\ \text{V}=178.5\ \text{fC}
$$

論文取整為 **179 fC**。Dimension check：F × V = C ✓（fF × V = fC）。

**Step 2 — transition 點的 noise PSD**：ring 的（有效）ISF 集中在 transition（本站
[lc_vs_ring](/06_design_insights/lc_vs_ring) 與 [P2]），所以論文只在「輸出過 $V_{DD}/2$
的那一瞬」評 noise；該點 NMOS 與 PMOS **同時導通**，兩者的電流噪聲功率相加（p.190）：

$$
\left(\overline{i_n^2}/\Delta f\right)_{NMOS}=4kT\gamma\mu_nC_{ox}(W/L_{\text{eff}})_N(V_{DD}/2-V_{TN})=4.44\times10^{-24}\ \text{A}^2/\text{Hz}
$$

$$
\left(\overline{i_n^2}/\Delta f\right)_{PMOS}=2.19\times10^{-24}\ \text{A}^2/\text{Hz}
$$

（這是 $4kT\gamma g_{d0}$ 形式的 channel thermal noise，偏壓點取在 $V_{DD}/2$；$\mu_n$、
$\gamma$ 的個別數值論文未列出，上面兩個 PSD 是論文直接給的結果。）每級合計：

$$
\overline{i_n^2}/\Delta f=(4.44+2.19)\times10^{-24}=6.63\times10^{-24}\ \text{A}^2/\text{Hz}
$$

（數值手感：本站 canonical 的 $S_i=10^{-24}$ A²/Hz 與這顆 2-µm 真矽的 $6.63\times10^{-24}$
同一個量級。）

**Step 3 — $\Gamma_{rms}^2$**：論文用附錄的方法對 ring 算出

$$
\Gamma_{rms}^2\approx\frac{16}{N^3}=\frac{16}{125}=0.128
$$

（無因次 ✓。）這正是 [P2] Eq.(16) 的前身：$\Gamma_{rms}^2=\dfrac{2\pi^2}{3\eta^3}\dfrac{1}{N^3}$，
代 $\eta\approx0.75$ 得 $\approx15.6/N^3\approx16/N^3$——1998 與 1999 兩篇互相咬合。
順帶一提 $\Gamma_{rms}=\sqrt{0.128}=0.358$，與本站代表值 0.5 同量級、比 true-LC 的
$1/\sqrt2\approx0.707$ 小。

**Step 4 — 代入 Eq.(21)（$N$ 個相同且不相關的源）**：$N$ 個不相關源功率相加，
$\overline{i_n^2}/\Delta f\to N\times6.63\times10^{-24}=3.315\times10^{-23}$ A²/Hz：

$$
\mathcal{L}\{\Delta f\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{N\,\overline{i_n^2}/\Delta f}{4\,(2\pi\Delta f)^2}\right)=10\log_{10}\!\left(\frac{0.128\times3.315\times10^{-23}}{(179\times10^{-15})^2\times4\times(2\pi)^2\times\Delta f^2}\right)
$$

分子 $=4.243\times10^{-24}$，分母 $=3.204\times10^{-26}\times157.9\times\Delta f^2=5.060\times10^{-24}\,\Delta f^2$，故

$$
\mathcal{L}\{\Delta f\}=10\log_{10}\!\left(\frac{0.84}{\Delta f^2}\right)
$$

與論文 p.190 印的 $10\log(0.84/\Delta f^2)$ 一致（我們重算得 0.839）。
**Dimension check**：$\dfrac{S_i}{q_{max}^2}$ 的單位是 $\dfrac{\text{A}^2/\text{Hz}}{\text{C}^2}=\dfrac{\text{A}^2\cdot\text{s}}{\text{A}^2\text{s}^2}=\text{Hz}$，
再除以 $(2\pi\Delta f)^2$ 的 Hz² 得 **1/Hz**——正是「每 Hz 的 sideband 功率相對
carrier」該有的因次 ✓。
（換句話說前係數 0.84 帶單位 Hz。）

**Step 5 — 預測 vs 量測**：代 $\Delta f=500$ kHz：

$$
\mathcal{L}=10\log_{10}\!\left(\frac{0.839\ \text{Hz}}{(5\times10^5\ \text{Hz})^2}\right)=10\log_{10}\!\left(3.35\times10^{-12}\ \text{Hz}^{-1}\right)=-114.7\ \text{dBc/Hz}
$$

論文量測 **$-114.5$ dBc/Hz**——差 0.2 dB。

> **factor-of-2／4 標記（每次出現都要講）**：分母的 **4** 是 [P1] Eq.(21) 的 **SSB 記帳**，
> 與本站例 B 的 $-148.0$ dBc/Hz 同一套慣例。若改用時域乾淨推導的 **/2** 記帳，同一組輸入會
> 預測 $-111.7$ dBc/Hz（高 3 dB），反而離量測 3.0 dB。這個實驗因此常被引用為 /4 版本的
> 經驗支持；不過 0.2 dB 的吻合同時吃 $\Gamma_{rms}$、$C_{total}$ 估計誤差，把它讀成
> 「量級與 scaling 對了」比讀成「一鎚定音裁決 factor-of-2」更穩健。詳見
> [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

**Step 6 — 1/f³ corner（Eq.(24) 兩邊同除 $2\pi$）**：同一顆 die 上的孤立 inverter
（輸入輸出短路）量到 device 1/f corner $f_{1/f}=250$ kHz；由萃取的 ISF 算出
$c_0^2/2\Gamma_{rms}^2=0.3$：

$$
f_{1/f^3}=f_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}=250\ \text{kHz}\times0.3=75\ \text{kHz}
$$

量測 **80 kHz**。這是 claim C5「1/f³ corner $\ne$ device 1/f corner」最直接的矽證據：
corner 從 250 kHz 被波形（部分）對稱性壓到 80 kHz。

**Python 驗證**（純代數重算，所有輸入取自 [P1] p.190–191）：

```python
import math

# [P1] Sec. V 第四個實驗：5 級 232 MHz single-ended ring（2-µm 5-V CMOS, p.190）
N       = 5              # 級數
qmax    = 179e-15        # C（= C_total 35.7 fF × V_swing 5 V）
Si_nmos = 4.44e-24       # A²/Hz（論文 p.190 給定，transition 點）
Si_pmos = 2.19e-24       # A²/Hz（論文 p.190 給定）
G2rms   = 16 / N**3      # Γ²_rms ≈ 16/N³（論文 p.190）

print(round(G2rms, 3))                            # -> 0.128
Si_total = N * (Si_nmos + Si_pmos)                # N 個不相關源功率相加
prefac = G2rms * Si_total / (4 * qmax**2 * (2*math.pi)**2)
print(round(prefac, 3))                           # -> 0.839 （論文印 0.84）

df = 500e3   # Hz
print(round(10*math.log10(prefac/df**2), 2))      # -> -114.74 （論文預測 -114.7；量測 -114.5）
print(round(10*math.log10(2*prefac/df**2), 2))    # -> -111.73 （若改用時域 /2 記帳，離量測 3 dB）
print(round(250e3*0.3/1e3, 1))                    # -> 75.0 （kHz，Eq.(24)；量測 80 kHz）

# 第五個實驗：11 級 115 MHz（同一顆 die；noise 隨 W 放大：NMOS×4/3、PMOS×6/5，L 相同）
N2, qmax2 = 11, 217e-15
Si_stage2 = Si_nmos*(4/3) + Si_pmos*(6/5)
prefac2 = (16/N2**3) * N2 * Si_stage2 / (4 * qmax2**2 * (2*math.pi)**2)
print(round(prefac2, 3))                          # -> 0.152 （論文印 0.152，逐位一致）
print(round(10*math.log10(prefac2/df**2), 2))     # -> -122.16 （論文預測 -122.1；量測 -122.5）
print(round(250e3*0.17/1e3, 1))                   # -> 42.5 （kHz，論文取 43；量測 45 kHz）

# 第七個實驗：4 級 differential 200 MHz（0.5-µm；q_max = 49 fF × 1.2 V = 58.8 fC）
prefac3 = (16/4**3) * 4 * 2.63e-23 / (4 * (58.8e-15)**2 * (2*math.pi)**2)
print(round(prefac3, 1))                          # -> 48.2 （論文印 48.1，尾數捨入差）
print(round(10*math.log10(prefac3/(1e6)**2), 2))  # -> -103.17 （論文預測 -103.2；量測 -103.9）
```

### 同一顆 die 的第二次驗證：11 級 115 MHz ring

第五個實驗換 $N$ 與元件尺寸重跑同一條鏈（[P1] p.190，數字逐字）：$(W/L)_N=4$ µm／2 µm、
$(W/L)_P=6$ µm／2 µm、每節點總電容 43.5 fF、$q_{max}=217$ fC（$=43.5\ \text{fF}\times5\ \text{V}$）。
論文說「以與前一實驗完全相同的方式計算」得 $\mathcal{L}\{\Delta f\}=10\log(0.152/\Delta f^2)$，
即 500 kHz 處 $-122.1$ dBc/Hz；量測 **$-122.5$ dBc/Hz**（差 0.4 dB）。
$c_0^2/2\Gamma_{rms}^2=0.17$ 預測 1/f³ corner 43 kHz、量測 **45 kHz**。
論文沒有列出 11 級元件的 PSD；上面 Python 以「noise 隨 $W$ 線性放大（$L$ 相同）」重算，
前係數得 **0.152**、與論文逐位一致——反推這正是論文的內部算法。

順手把 5 級 → 11 級的 7.4 dB 改善**在 Eq.(21) 內部**拆帳（用上面重算的兩個前係數
$10\log_{10}(0.839/0.152)=7.42$ dB）：

| 項 | 比值 | dB |
|---|---|---|
| $\Gamma_{rms}^2\times N=16/N^2$（$25\to121$） | $\times4.84$ 變小 | $-6.85$ |
| $q_{max}^2$（$179\to217$ fC） | $\times1.47$ 變大 | $-1.67$ |
| 每級 noise PSD（$6.63\to8.55\times10^{-24}$ A²/Hz） | $\times1.29$ 變大 | $+1.10$ |
| **合計** | | $-7.42$ ✓ |

注意這**不是**免費午餐：級數變多、$f_0$ 也從 232 掉到 115 MHz；[P2] Eq.(23), p.796 之後
證明**固定總功率、固定 $f_0$** 時 single-ended ring 的白噪 phase noise 與 $N$ 無關。
詳見 [paper_002](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)。

### 換製程、換架構的第三次驗證：4 級 differential 200 MHz（0.5-µm）

第七個實驗（[P1] p.191）：tail 電流 108 µA、每個差動節點總電容 $C_{total}=49$ fF、
$V_{swing}=1.2$ V，故 $q_{max}=58.8$ fC（論文原文印作「58.8 fF」——因次上
$49\ \text{fF}\times1.2\ \text{V}$ 只能是 fC，這是論文的排版筆誤，我們照實轉錄並標記）。
每節點總 channel noise $(\overline{i_n^2}/\Delta f)_{total}=2.63\times10^{-23}$ A²/Hz，
$N=4$ 代入同一條鏈得 $\mathcal{L}\{\Delta f\}=10\log(48.1/\Delta f^2)$（我們重算得 48.2，
尾數捨入差），1 MHz 處預測 $-103.2$、量測 **$-103.9$ dBc/Hz**（差 0.7 dB）。

同一實驗還有一個對稱性教訓：雖然**差動訊號**完美對稱，每個 **half-circuit** 的單端波形並
不對稱，所以 Fig. 27 仍有明顯的 1/f³ 段——「差動救不了 $c_0$，重要的是 half-circuit 對稱」
（呼應 p.188 與 [symmetry](/06_design_insights/symmetry)）。

### 這組實驗告訴我們什麼（適用與失效條件）

- **預測是 a-priori 的**：三條全鏈（232 MHz／115 MHz／200 MHz differential）誤差
  0.2／0.4／0.7 dB，輸入只有 process 參數、幾何、$V_{swing}$ 與萃取的 ISF。
  本站例 B 的 toy 鏈（$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、$S_i=10^{-24}$ A²/Hz
  → $-148.0$ dBc/Hz @ 1 MHz，SSB /4 記帳）走的就是同一條管線，只是換成乾淨數字。
- **適用**：noise 集中在 transition 的近似（single-ended CMOS ring 成立）；
  $\Gamma_{rms}^2\approx16/N^3$ 是「相同 inverter、標準上升下降」ring 的專用近似
  （對應 [P2] 的 $\eta\approx0.75$）；各級 noise 不相關（不相關才可功率相加）。
- **失效**：波形不對稱時（實驗 3／6／7）close-in 由 $c_0$ 的 1/f³ 主導，Eq.(21) 只管
  1/f² 段；很近 carrier 處線性化失效（見
  [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)）；有強 spur 或
  injection pulling 時另計（[P3]／[P4]）。
- **因次**：每個 $10\log_{10}$ 的引數都是 1/Hz——dBc/Hz 的正字標記。

## Limitations

照 paper_metadata（paper_001.limitations）：

- 1/f³ 段歷史上靠經驗連結；本理論澄清它由 $c_0$ 決定，但**確切 $c_0$ 仍需萃取**。
- 實際電路的 $\Gamma$ 要靠 transient impulse 模擬或 adjoint/PSS 法萃取；封閉式是一階近似。
- **AM–PM 轉換與強非線性**沒被一階 phase-only 模型完全涵蓋（這正是 [P4] 用 APF 補的洞）。
- 嚴謹的數學地基（PPV／adjoint／Floquet）**不在這 5 篇 PDF**，屬外部文獻（claim C13），
  見 [effective_isf](/03_isf_core_theory/effective_isf)。

## Relationship to other papers

- **[P2]** 把這頁的 ISF 套到 ring oscillator：用同一個 $\Gamma_{rms}^2/q_{max}^2$ 比例導出
  jitter $\kappa$，並研究 $\Gamma_{rms}\propto N^{-3/2}$ scaling（claim C8）。
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
