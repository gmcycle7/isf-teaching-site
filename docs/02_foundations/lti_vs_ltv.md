---
title: LTI vs LTV — 振盪器對 noise 的敏感度是週期時變的
description: 從 LTI 的 h(t-τ) 到 LTV 的 h(t,τ)；為何振盪器對 noise 的敏感度是週期時變、同一個 impulse 注在不同波形位置得到不同 phase shift；ISF 本質就是週期時變敏感度。
---

# LTI vs LTV — 振盪器對 noise 的敏感度是週期時變的

> 先備：[oscillator_phase](/02_foundations/oscillator_phase) · [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) ｜ 接下來：[從 impulse 到 phase shift 的推導](/03_isf_core_theory/impulse_to_phase_shift)

訊號與系統課教我們用脈衝響應 $h(t)$ 與卷積描述線性系統。但那套是 **LTI（Linear
Time-Invariant，線性非時變）** 的故事。Hajimiri–Lee 在 [P1] 最關鍵的洞見是：

> **振盪器對 noise 的相位響應不是 LTI，而是 LTV（Linear Time-Variant，線性時變）。**

這一頁說清楚 LTI 與 LTV 差在哪、為什麼振盪器一定是 LTV、以及為什麼這個差別正好就是
**ISF（Impulse Sensitivity Function，脈衝敏感度函數）** 的存在理由。

> **物理直覺（先講結論）**：LTI 系統「不看現在幾點」——同一個脈衝，今天打跟明天打，
> 反應形狀一模一樣，只是時間平移。振盪器不是這樣：因為它的狀態在 limit cycle 上**不停
> 轉動**，同一顆 noise 電流注在「波峰」跟注在「零交越」會得到**完全不同**的相位偏移。
> 系統對輸入的敏感度本身**隨時間（隨注入相位）週期變化**——這就是「週期時變敏感度」，
> 把它整理成一個 $2\pi$ 週期、無因次的函數，就是 ISF $\Gamma(\omega_0\tau)$。

## 1. 複習：LTI 的 $h(t-\tau)$

線性非時變系統有兩個性質：**線性**（疊加成立）與**時不變**（輸入延遲 $\Delta$，輸出也只是
延遲 $\Delta$、形狀不變）。時不變的後果是它的脈衝響應**只依賴時間差** $t-\tau$：

$$
y(t)=\int_{-\infty}^{\infty}h(t-\tau)\,x(\tau)\,d\tau\qquad\text{（LTI 卷積）}.
$$

- **為何只看 $t-\tau$**：在 $\tau_1$ 注入單位脈衝得到 $h(t-\tau_1)$，在 $\tau_2$ 注入得到
  $h(t-\tau_2)$——**同一個形狀，只是平移**。系統不在乎「絕對時刻 $\tau$」，只在乎「過了多久」。
- **單位檢查**：卷積核 $h$ 的維度由輸出／輸入決定；這裡重點是「形狀不變」而非數值。
- **這就是大學學的那套**：RLC 濾波器、放大器小訊號等效——只要工作點固定，都是 LTI。

## 2. 振盪器：脈衝響應變成 $h(t,\tau)$，多了一個自變數

振盪器**沒有固定工作點**——它的狀態在 limit cycle 上不停移動（見
[oscillator_phase](/02_foundations/oscillator_phase)）。所以「此刻系統對擾動多敏感」會隨
狀態（也就是隨注入相位 $\omega_0\tau$）改變。脈衝響應因此**同時依賴兩個時間**：

$$
\boxed{\;h_\phi(t,\tau)\neq h_\phi(t-\tau)\;}\qquad\text{（LTV：依賴絕對注入時刻}\tau\text{，不只}t-\tau\text{）}.
$$

[P1] 寫出的 excess-phase 脈衝響應正是這個形式（[P1] Eq.(10), p.182）：

$$
h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau).
$$

把它拆開看，剛好把 LTV 的兩個自變數分給兩個因子，意義清楚：

- **階高（step height）$\dfrac{\Gamma(\omega_0\tau)}{q_{max}}$**：只依賴**注入相位 $\omega_0\tau$**。
  這是「時變」的部分——同樣大小的脈衝，注入相位不同，跳的高度不同。
- **時間形狀 $u(t-\tau)$**：一個 unit step（單位階梯），只依賴 $t-\tau$。它編碼「相位偏移
  一旦發生就**永久保持**」（相位沒有恢復力，見
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)）。

- **單位檢查 / dimension**：$\Gamma$ 無因次、$q_{max}$ 單位 C、$u$ 無因次，所以
  $h_\phi$ 的單位是 $\mathrm{C^{-1}}$；對電流（A）卷積後 $\int h_\phi\,i\,d\tau$ 得
  $\mathrm{C^{-1}\cdot A\cdot s}=\mathrm{C^{-1}\cdot C}=$ 無因次 = rad ✓。
- **為何是 $\Gamma(\omega_0\tau)$ 而不是 $\Gamma(\tau)$**：敏感度隨「波形相位」週期變化，
  週期是 $2\pi$（每轉一圈 limit cycle 回到相同敏感度）。所以 $\Gamma$ 的自變數是相位
  $\omega_0\tau$，且 $\Gamma$ 是 $2\pi$ 週期函數——這就是「**週期時變**敏感度」。

## 3. 為什麼同一個 impulse 在不同位置得到不同 phase shift

把第 2 步的 step height 套到操作型 ISF 定義（[P1] Eq.(11) 的脈衝極限）：

$$
\Delta\phi(\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q.
$$

固定 $\Delta q$、掃注入相位 $\theta=\omega_0\tau$，$\Delta\phi$ 就照著 $\Gamma(\theta)$ 的形狀
起伏。對理想 LC，$\Gamma(\theta)=-\sin\theta$：

| 注入相位 $\theta$ | 波形位置 | $\Gamma(\theta)=-\sin\theta$ | 結果 |
|---|---|---|---|
| $0$ | 波峰（斜率 0） | $0$ | $\Delta\phi=0$，純改振幅 |
| $\pi/2$ | 下降零交越（斜率最負） | $-1$ | $\vert \Delta\phi\vert $ 最大 |
| $\pi$ | 波谷（斜率 0） | $0$ | $\Delta\phi=0$，純改振幅 |
| $3\pi/2$ | 上升零交越（斜率最正） | $+1$ | $\vert \Delta\phi\vert $ 最大、反向 |

- **物理原因（接 oscillator_phase 第 4 步）**：相位偏移大小取決於電壓跳變**投影到 limit
  cycle 切線方向**的分量。零交越時狀態速度（切線）正好沿著電壓軸，固定的 $\Delta V$ 幾乎
  全部變成切向位移 → $\Delta\phi$ 最大；波峰時切線垂直於電壓軸，$\Delta V$ 幾乎全是徑向
  （純振幅）→ $\Delta\phi\approx 0$。切向分量 $\propto\sin\theta$，故對正弦波 $\Gamma(\theta)=-\sin\theta$。
- **這就是 LTV 的指紋**：若振盪器是 LTI，$\Delta\phi$ 應該與 $\tau$ 無關（只看 $t-\tau$）——
  但實際上 $\Delta\phi(\tau)$ 週期起伏。**敏感度本身隨時間變 = time-variant**。

把 LTI 與 LTV 並排看最清楚：

| | LTI | LTV（振盪器相位） |
|---|---|---|
| 脈衝響應 | $h(t-\tau)$（只看時間差） | $h_\phi(t,\tau)=\dfrac{\Gamma(\omega_0\tau)}{q_{max}}u(t-\tau)$ |
| 換注入時刻 $\tau$ | 形狀不變，只平移 | **階高隨 $\omega_0\tau$ 改變** |
| 敏感度 | 與絕對時刻無關 | **$2\pi$ 週期時變**（= ISF） |
| 卷積 | $\int h(t-\tau)x\,d\tau$ | $\dfrac{1}{q_{max}}\displaystyle\int_{-\infty}^{t}\Gamma(\omega_0\tau)i_n(\tau)\,d\tau$ |

右下角那個 LTV 卷積就是 [P1] Eq.(11), p.182——下一章
[convolution_derivation](/03_isf_core_theory/convolution_derivation) 會用它把任意 noise 電流
疊加成 $\phi(t)$。

## 4. 對照圖：LTI 形狀不變 vs LTV 階高隨相位變

下圖上半是一個 LTI 系統（簡單一階衰減）的脈衝響應：在 $\tau=0.3,\,0.9,\,1.5$ 注入，
得到**同一個形狀、只是平移**。下半是振盪器的 LTV 相位響應 $h_\phi(t,\tau)$：在不同注入
相位 $\tau$，**階梯高度 $\Gamma(\omega_0\tau)=-\sin(2\pi\tau)$ 跟著改變**（甚至變號）。

![LTI 形狀不變 vs LTV 階高隨注入相位改變](/figures/lti_vs_ltv_impulse_response.png)

**這張圖怎麼解讀**：

- **上半（LTI）**：三條曲線疊起來形狀一模一樣，只是起點平移——「系統不看絕對時刻」。
- **下半（LTV）**：三條都是階梯（$u(t-\tau)$，永久保持），但**階高不同**：$\tau=0$ 時
  $\Gamma=-\sin 0=0$（注在波峰，階高 0、無相位偏移）；$\tau=0.25$ 時 $\Gamma=-\sin(\pi/2)=-1$
  （注在零交越，階高最大、負向）；$\tau=0.5$ 時 $\Gamma=-\sin(\pi)=0$（注在波谷，階高 0）。
- **訊息**：LTV 的「形狀」固定（都是階梯，因相位無恢復力），但「強度」週期時變——這正是 ISF。

下面這張是把 step height 對注入相位連續掃出來的結果（[lab_04](/04_simulation_labs/numerical_feeling)
的相位掃描），等於把上表那一欄畫成連續曲線，數值與理論 $-\sin\theta$ 幾乎重合：

![持續相位偏移隨注入相位變化（LC limit-cycle 模型）](/figures/sinusoidal_impulse_phase_sweep.png)

**這張圖怎麼解讀**：橫軸是注入相位 $\theta/2\pi$（一個週期），縱軸是注入後**持續保留**的
$\Delta\phi$（固定 $\Delta q/q_{max}=10^{-3}$）。藍點是數值模擬、黑虛線是
$\Delta\phi=-\sin\theta\cdot\Delta q/q_{max}$。**$\Delta\phi$ 隨注入相位週期起伏**就是 LTV 的
眼見為憑；它正比於 ISF，所以這張掃描圖本質上就是「量出來的 $\Gamma(\theta)$」。

### 用真實函式產生這兩張圖

兩張圖都由 `simulations/lab_04_impulse_sweep.py` 產生。LTV 對照圖用解析 ISF
$\Gamma(\theta)=-\sin(2\pi f_0\tau)$ 設定階高；相位掃描圖用 `extract_isf_by_injection()`
在 limit-cycle 模型上真的注入小電荷、量持續相位偏移：

```python
import numpy as np
from oscillator_models import extract_isf_by_injection

# (1) LTV 對照：階高 = ISF(注入相位)，時間形狀都是 u(t - tau)
f0 = 1.0
for tau in [0.0, 0.25, 0.5]:
    gamma = -np.sin(2 * np.pi * f0 * tau)   # ISF at injection phase
    # h_phi(t, tau) = gamma * u(t - tau)    -> 階高隨 tau 改變，形狀(階梯)不變

# (2) 相位掃描：數值反推 ISF，對比解析 -sin(theta)
theta, g_num, g_ana = extract_isf_by_injection(
    f0=1.0, fs=8000.0, n_inject_periods=6, settle_periods=4,
    dq_over_qmax=1e-3, n_points=48, mu=0.3)
# g_num ≈ g_ana = -sin(theta)，最大誤差約 0.001
```

完整 script：`simulations/lab_04_impulse_sweep.py`
（核心模型 `simulations/common/oscillator_models.py` 的 `extract_isf_by_injection`、`simulate_lc`）。

**參數表**：

| 參數 | 符號 | LTV 對照圖 | 相位掃描圖 | 單位 |
|---|---|---|---|---|
| 振盪頻率 | $f_0$ | 1.0（normalized） | 1.0（normalized） | Hz |
| 取樣率 | $f_s$ | 2000 | 8000 | Hz |
| 注入相位 | $\tau$ | $\{0,\,0.25,\,0.5\}$ 週期 | 掃 48 點遍歷一週期 | — |
| 相對注入電荷 | $\Delta q/q_{max}$ | （示意階高） | $10^{-3}$（小訊號） | — |
| 沉降週期數 | — | — | 4 | — |
| 振幅恢復強度 | $\mu$ | —（解析階高） | 0.3 | — |

> **toy model 警告**：兩張圖都是 pedagogical toy model，非 transistor-level。LTV 圖用解析
> $-\sin$ 設定階高；掃描圖用一個正規化 2-D limit-cycle 模型重現「敏感度週期時變」的**機制**，
> 數值是教學用的。對應 [P1] Eqs.(10),(11) 與 Sec. III、Fig. 4。

## 5. 為什麼非得用 LTV——LTI 模型錯在哪

歷史上早期把振盪器 noise 當 LTI（如把雜訊直接乘上 tank 的轉移函數）會漏掉兩件事，正是
LTV／ISF 才補得起來的：

1. **頻率轉換（frequency translation）**：因為敏感度 $\Gamma(\omega_0\tau)$ 本身是週期的
   （含 $\omega_0$ 的諧波），它會把 $0,\,\omega_0,\,2\omega_0,\dots$ 附近的 noise **混頻**搬到
   載波旁邊。LTI 不會混頻，因此無法解釋為何 device 在 DC 與在 $n\omega_0$ 的 noise 都會出現在
   close-in 相位雜訊裡。這由 ISF 的傅立葉係數 $c_n$ 描述（[P1] Eq.(12)–(13), p.183）。
2. **$1/f$ 上轉成 $1/f^3$**：device 的低頻 $1/f$ noise 之所以能搬到載波附近，靠的是 ISF 的
   **DC 係數 $c_0$**（[P1] Eq.(23)），純 LTI 觀點解釋不了。波形對稱 → $c_0$ 小 → $1/f^3$ 角
   被壓低（[P1] Eq.(24)）。

換句話說，**LTV 不是把問題複雜化，而是因為振盪器物理上就是時變的**；強行套 LTI 會在定性上
就漏掉混頻與 $1/f$ 上轉這兩個真實現象。

## 數值例子（建立手感）

> **例 A 的 LTV 版**：$q_{max}=1$ pC、$\Delta q=1$ fC、$f_0=5$ GHz，比較注在零交越
> （$\Gamma=-1$）與注在峰值（$\Gamma=0$）。

**零交越**（$\theta=\pi/2$，$\Gamma=-\sin(\pi/2)=-1$）：

$$
|\Delta\phi|=\frac{|\Gamma|\,\Delta q}{q_{max}}=\frac{1\times(1\times10^{-15})}{1\times10^{-12}}=1\times10^{-3}\ \text{rad}\ \Rightarrow\ \Delta t=\frac{10^{-3}}{2\pi\times5\times10^{9}}\approx31.8\ \text{fs}.
$$

**峰值**（$\theta=0$，$\Gamma=0$）：$\Delta\phi=0$ rad、$\Delta t=0$ fs。

- **Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。
- **手感**：同一顆 1 fC，因為敏感度週期時變，注入相位差 $90^\circ$ 就讓相位偏移從 31.8 fs 變成 0。
  **這個「隨相位變」的比例，整理出來就是 ISF**——LTV 的全部精神就在這一句。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 小訊號（線性化） | 響應對 $\Delta q$ 線性、可定義 $h_\phi(t,\tau)$ | 大注入 → 真正非線性，連 LTV 線性疊加都不夠 |
| 穩態週期軌跡存在 | $\Gamma$ 是良好定義的 $2\pi$ 週期函數 | 未起振／chirp／調頻時 $\Gamma$ 不再固定週期 |
| 已知正確 $\Gamma$ | LTV 卷積可預測 $\phi(t)$ | $\Gamma$ 要靠 transient/adjoint 模擬萃取（見 [effective_isf](/03_isf_core_theory/effective_isf)） |
| 相位無恢復力 | 用 $u(t-\tau)$（永久階梯）合理 | 強 injection-locking 時相位被外力拉住（[P3]） |

## 重點回顧

- **LTI**：$h(t-\tau)$，只看時間差，換注入時刻只是平移、形狀不變。
- **LTV**：$h_\phi(t,\tau)=\dfrac{\Gamma(\omega_0\tau)}{q_{max}}u(t-\tau)$——**階高隨注入相位
  $\omega_0\tau$ 週期變化**，時間形狀（階梯）固定。
- 振盪器一定是 LTV：狀態沿 limit cycle 移動 → 敏感度隨相位變 → 同 impulse 不同位置 → 不同 $\Delta\phi$。
- **ISF $\Gamma(\omega_0\tau)$ 的本質就是「週期時變敏感度」**；理想 LC 為 $-\sin\theta$。
- LTV 才解釋得了**頻率轉換**（$c_n$ 混頻）與 **$1/f\to1/f^3$ 上轉**（$c_0$），LTI 漏掉這兩者。
- 例 A：1 fC 注零交越 → 31.8 fs；注波峰 → 0 fs（敏感度週期時變的直接後果）。
- 來源：[P1] Eq.(10), Eq.(11), Sec. III；數值與圖出自 lab_04。

## 延伸閱讀

- 幾何起點：[oscillator_phase](/02_foundations/oscillator_phase)
- 為何相位累積、振幅衰減：[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)
- 把 LTV 變成完整推導：[從 impulse 到 phase shift 的推導](/03_isf_core_theory/impulse_to_phase_shift)
- 用 LTV 卷積疊加任意 noise：[convolution_derivation](/03_isf_core_theory/convolution_derivation)
- $c_n$ 混頻與頻率轉換：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- 對應的數值實驗：[數值手感 Numerical Feeling](/04_simulation_labs/numerical_feeling)
