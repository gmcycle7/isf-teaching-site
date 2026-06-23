---
title: Oscillator phase 是什麼？
description: 用 state trajectory 與 limit cycle 解釋振盪器的相位：為何振盪器沒有絕對時間基準、phase 擾動沿切線累積、amplitude 擾動沿徑向被拉回，以及這如何變成 phase noise 與 jitter。
---

# Oscillator phase 是什麼？

> 先備：[統一符號表](/00_overview/notation) · [學習路徑](/00_overview/learning_path) ｜ 接下來：[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)

在談 ISF（Impulse Sensitivity Function，脈衝敏感度函數）之前，必須先把一件事講清楚：
**振盪器的「相位（phase）」到底是什麼物理量，它跟「振幅（amplitude）」差在哪裡，
為什麼一個會永久殘留、一個會被自動修正。** 這一頁就回答這個問題。它是整個 ISF 理論的
地基——後面 [從 impulse 到 phase shift 的推導](/03_isf_core_theory/impulse_to_phase_shift)
能成立，全靠這裡建立的幾何直覺。

> **物理直覺（先講結論）**：把振盪器的狀態畫在 2-D 平面上，穩態時它沿著一條閉合的環
> （limit cycle，極限環）不停轉圈。一個 noise 脈衝把狀態點推離這條環。推離的位移可以分成
> 兩個方向：**沿著環的切線方向 = 相位擾動**，**垂直於環指向圓心的徑向方向 = 振幅擾動**。
> 振盪器有「振幅恢復力」會把徑向偏差慢慢拉回環上；但**沒有任何力**會修正切線方向的偏差，
> 因為振盪器根本沒有「現在幾點」的絕對參考。於是相位誤差一次次累積，這就是 phase noise
> 與 timing jitter 的根源。

## 第 1 步：用 state trajectory 描述振盪器

任何振盪器都可以用幾個「狀態變數（state variables）」完整描述。最典型的 LC 振盪器有兩個
能量儲存元件：電容（存電壓）與電感（存電流），所以它的狀態是一個 2-D 向量

$$
\mathbf{z}(t)=\big(x(t),\,y(t)\big),
$$

其中我們可以取 $x$ = 電容電壓（normalized）、$y$ = 正比於電感電流的量（normalized）。
隨時間演化，$\mathbf{z}(t)$ 在這個「狀態平面（state plane）」上畫出一條軌跡，叫
**state trajectory（狀態軌跡）**。

- **用到的物理**：能量在電容與電感之間來回振盪——電壓最大時電流為零（能量全在電容），
  電壓為零時電流最大（能量全在電感）。這正是一個圓在 $x$–$y$ 平面上轉動的圖像。
- **單位檢查**：兩軸都先 normalize 成無因次（除以各自的最大擺幅），半徑 $r=\sqrt{x^2+y^2}$
  代表「振盪的總能量大小」，相位角 $\theta=\arctan(y/x)$ 代表「現在轉到哪裡」。
- **為何用 2-D**：訊號與系統課學過，二階系統的自由響應就是平面上的軌跡。理想無損 LC 是
  邊界穩定（marginally stable）的，軌跡是一個半徑固定的圓。

本站的 toy model（[lab_01](/04_simulation_labs/numerical_feeling) 用到的
`oscillator_models.py`）用一個正規化的 2-D 方程來產生這條軌跡（**這是 pedagogical toy
model，非 transistor-level**）：

$$
\begin{aligned}
\frac{dx}{dt}&=-\omega_0\,y+\mu\,(1-r^2)\,x,\\
\frac{dy}{dt}&=\ \ \omega_0\,x+\mu\,(1-r^2)\,y,\qquad r^2=x^2+y^2.
\end{aligned}
$$

第一項 $\pm\omega_0$ 就是純旋轉（理想 LC）；第二項 $\mu(1-r^2)$ 是 Van der Pol 式的
**振幅恢復項**：當 $r>1$ 它把能量抽掉、當 $r<1$ 它補能量，把軌跡推回單位圓。
$\mu=0$ 退化成無損 LC（純旋轉），$\mu>0$ 模擬真實振盪器一定要有的 AGC／device 非線性。

## 第 2 步：limit cycle（極限環）是什麼

當 $\mu>0$，不管從哪裡出發（例如從半徑 $1.7$ 起跳），軌跡最後都會收斂到同一條閉合曲線
——這條**吸引子**就是 **limit cycle（極限環）**：

- **定義**：limit cycle 是相平面上一條孤立的、週期性的閉合軌跡，鄰近的軌跡會被吸引到它
  （穩定極限環）或被它排斥。穩態振盪 = 沿 limit cycle 等速繞圈，週期 $T=1/f_0$。
- **為何振盪器一定有 limit cycle**：要有穩定、振幅固定的振盪，必須有一個機制把振幅鎖在
  某個值。線性系統做不到（不是衰減就是發散），所以**所有真實振盪器都是非線性的**，而那個
  非線性恰恰造出 limit cycle。這點在 [LTI vs LTV](/02_foundations/lti_vs_ltv) 會再用到。
- **單位檢查**：繞一圈相位前進 $2\pi$ rad，花時間 $T$，所以角速度 $\omega_0=2\pi/T=2\pi f_0$
  rad/s ✓。

下圖就是 toy model 模擬出的 limit cycle：黑色虛線是穩態的單位圓，藍線是從環外
（半徑 $1.7$）起跳、被振幅恢復項一圈圈拉回環上的軌跡。圖上標了在操作點處的兩個擾動方向。

![Limit cycle 上的 phase（切向）與 amplitude（徑向）擾動](/figures/limit_cycle_phase_amplitude.png)

**這張圖怎麼解讀**：

- 黑色虛線圓 = limit cycle（穩態軌跡）。狀態點以 $\omega_0$ 等角速度沿它逆時針轉。
- 綠色箭頭（切線方向）= **phase 擾動 $\Delta\phi$**：沿著環移動，相當於「提早或延後到達
  某個相位」。沒有恢復力，會**持續累積**。
- 紅色箭頭（徑向方向）= **amplitude 擾動 $\Delta A$**：把狀態點推離或推進環，被振幅恢復項
  **慢慢拉回**。
- 藍線示範了徑向擾動的命運：從半徑 1.7 起跳，幾圈內就鬆弛回單位圓——徑向資訊被「忘掉」。

**對應公式**：把擾動向量 $\delta\mathbf{z}$ 投影到 limit cycle 在該點的切線單位向量
$\hat{\mathbf{t}}$（相位方向）與徑向單位向量 $\hat{\mathbf{r}}$（振幅方向）：

$$
\delta\mathbf{z}=\underbrace{(\delta\mathbf{z}\cdot\hat{\mathbf{t}})}_{\to\ \Delta\phi}\hat{\mathbf{t}}+\underbrace{(\delta\mathbf{z}\cdot\hat{\mathbf{r}})}_{\to\ \Delta A}\hat{\mathbf{r}}.
$$

切向分量決定相位偏移，徑向分量決定振幅偏移。**ISF 就是「單位注入電荷在某個注入相位下，
切向分量佔多少」的那個比例函數**（正式定義見
[從 impulse 到 phase shift 的推導](/03_isf_core_theory/impulse_to_phase_shift)）。

## 第 3 步：為什麼振盪器沒有絕對時間基準

這是整個理論最關鍵、卻最常被忽略的一句話：

> **自治振盪器（autonomous oscillator）的微分方程不含時間 $t$ 的顯式項。**

意思是，方程只認得「狀態 $\mathbf{z}$」，不認得「現在是幾點」。數學上的後果是：若
$\mathbf{z}(t)$ 是一個解，那麼把時間平移任意常數 $\Delta\tau$ 後的 $\mathbf{z}(t-\Delta\tau)$
**也是一個完全合法、能量相同、波形相同的解**。

- **用到的數學**：自治系統 $\dot{\mathbf{z}}=F(\mathbf{z})$ 對時間平移具有不變性
  （time-translation invariance）。沿 limit cycle 的位移對應的就是這個自由度。
- **物理意義**：振盪器沒有外部時鐘告訴它「該在哪個相位」。沿環滑動（= 改變相位）**不耗能、
  不被任何恢復力反對**。這就是為什麼相位是一個 **marginally stable（中性穩定）** 的自由度
  ——對應系統有一個 **零特徵值（Floquet exponent = 0）**。
- **對照振幅**：垂直於環的方向（振幅）對應**負特徵值**，所以擾動會指數衰減回環上。
  （嚴格的 Floquet／PPV 理論**不在下載的 5 篇 PDF 內**，屬 Demir 等外部文獻，
  本站只用幾何直覺；詳見 [effective_isf](/03_isf_core_theory/effective_isf) 的補充說明。）

一句話總結：**相位是振盪器唯一沒有恢復力的狀態方向**，所以 noise 對相位的影響是永久的、
會累積的；對振幅的影響是暫時的、會被吃掉的。

## 第 4 步：同一個 impulse，注入相位不同，效果完全不同

既然擾動會被分解成切向與徑向，那麼**在波形的哪個相位踢它**，就決定了切向／徑向的分配比例。
看純正弦波 $V(t)=\cos(\omega_0 t)$：

- 在**波峰（peak）**，$\theta=0$：狀態點在 $x$ 軸最右端，狀態速度（切線）是純 $y$ 方向。
  一個沿 $x$ 的電壓跳變幾乎全是**徑向**——只改振幅、幾乎不改相位。對應 $\Gamma\approx 0$。
- 在**零交越（zero crossing）**，$\theta=\pi/2$：狀態點在 $y$ 軸最上端，切線是純 $x$ 方向。
  同樣沿 $x$ 的電壓跳變幾乎全是**切向**——只改相位、幾乎不改振幅。對應 $|\Gamma|$ 最大。

下圖把這件事畫在時域波形上：

![同樣大小的 impulse，注入相位不同 → 效果完全不同](/figures/waveform_with_impulse_markers.png)

**這張圖怎麼解讀**：

- 藍色曲線 $V(t)=\cos(2\pi f_0 t)$ 是穩態波形。
- 紅色標記（波峰）：在這裡注入脈衝 → **只有 $\Delta A$、幾乎沒有 $\Delta\phi$**（$\Gamma\approx 0$）。
- 綠色標記（零交越，斜率最大處）：在這裡注入脈衝 → **最大 $\Delta\phi$、幾乎沒有 $\Delta A$**
  （$|\Gamma|$ 最大）。
- 結論：相位敏感度跟「波形此刻的斜率」高度相關——斜率大的地方，同一個電壓跳變等效於更大的
  時間（相位）位移。這就是 ISF 為理想 LC 長成 $\Gamma(\theta)=-\sin\theta$ 的幾何原因
  （正弦波在零交越斜率最大、在峰值斜率為零）。

**對應公式**（操作型 ISF 定義，[P1] Eq.(10)–(11), p.182；完整推導在下一章）：

$$
\Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q,\qquad \Gamma_{LC}(\theta)=-\sin\theta.
$$

「同 impulse、相位不同 → 效果不同」這個事實，正式名稱叫 **週期時變敏感度（periodically
time-varying sensitivity）**，是 [P1] 把振盪器當成 **LTV（線性時變）系統**的核心理由
（見 [LTI vs LTV](/02_foundations/lti_vs_ltv)）。

### 用真實函式產生這兩張圖

兩張圖都由 `simulations/lab_01_sinusoidal_oscillator.py` 產生。limit cycle 來自
`simulate_lc()` 的 RK4 積分（含振幅恢復），波形標記來自 `sinusoidal_oscillator()`：

```python
from oscillator_models import simulate_lc, sinusoidal_oscillator
import numpy as np

# (1) limit cycle：從環外 (x0=1.7) 起跳，被 mu>0 的振幅恢復項拉回單位圓
t, x, y = simulate_lc(f0=1.0, t_end=3.0, fs=4000.0, mu=0.6, x0=1.7, y0=0.0)

# (2) 純正弦波 + peak / zero-crossing 標記
tt = np.arange(int(2.0 * 4000.0)) / 4000.0
v  = sinusoidal_oscillator(tt, f0=1.0, amp=1.0)   # V = cos(2*pi*f0*t)
# peak  : theta=0      -> 只改振幅   (Gamma ~ 0)
# zero  : theta=pi/2 (t=0.25 T) -> 只改相位 (|Gamma| max)
```

完整 script：`simulations/lab_01_sinusoidal_oscillator.py`
（核心模型 `simulations/common/oscillator_models.py`）。

**參數表**：

| 參數 | 符號 | 圖 (limit cycle) | 圖 (impulse markers) | 單位 |
|---|---|---|---|---|
| 振盪頻率 | $f_0$ | 1.0（normalized） | 1.0（normalized） | Hz |
| 取樣率 | $f_s$ | 4000 | 4000 | Hz |
| 振幅恢復強度 | $\mu$ | 0.6 | —（純正弦） | — |
| 起始狀態 | $(x_0,y_0)$ | $(1.7,\,0)$ | — | normalized |
| 波形振幅 | $A$ | 1（穩態半徑） | 1.0 | normalized |

> **toy model 警告**：這兩張圖都是 pedagogical toy model，用一個正規化的 2-D Van der Pol
> 式系統重現「相位 vs 振幅」的**機制**，不是 transistor-level 的真實電路數值。它對應
> [P1] Fig. 4（impulse 注在 peak vs zero crossing、state-space limit cycle）與 Sec. III-A
> 的概念，但常數與波形是教學用的。

## 第 5 步：amplitude error 被拉回、phase error 累積 → phase noise / jitter

把前面四步串起來，看 noise 持續踢的長期後果：

1. **振幅誤差（amplitude error）**：每次 noise 把狀態推離環一點點（徑向），振幅恢復項在
   幾個時間常數內把它拉回。它對輸出的影響是有界、會衰減的——所以振幅雜訊通常被自然抑制
   （詳見 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)）。
2. **相位誤差（phase error）**：每次 noise 把狀態沿環推一點點（切向），**沒有恢復力**，
   這個 $\Delta\phi$ 永久留著。下一次 noise 又加一個 $\Delta\phi$……相位做的是一個
   **random walk（隨機漫步）**。

把這個隨機漫步寫成連續形式，就是下一章的 LTV 卷積（[P1] Eq.(11), p.182）：

$$
\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau.
$$

積分上限是 $t$（系統有**記憶**），所以過去所有 noise 的相位貢獻全部累加——這就是相位誤差
累積的數學原因，也是 phase noise／jitter 的本質。

### phase noise 與 timing jitter 的關係

同一件事（相位的隨機抖動）有兩種看法，只差一個換算常數 $2\pi f_0$：

- **phase noise（相位雜訊）**：在**頻域**看。把相位起伏的功率譜畫出來，就是
  $S_\phi(f)$（rad²/Hz），或工程上常用的單邊帶（SSB）$\mathcal{L}(\Delta f)$（dBc/Hz）。
  累積相位的隨機漫步在頻域呈現為靠近載波的 $1/f^2$ 裙擺。
- **timing jitter（時間抖動）**：在**時域**看。把相位誤差換成「邊緣（edge）跨越零點的
  時間誤差」，用 $\Delta t=\Delta\phi/(2\pi f_0)$ 換算。

換算公式（規範第 3 節 Eq.17、Eq.19）：

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0},\qquad \sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{1}{2\pi f_0}\sqrt{\int_{f_1}^{f_2}S_\phi(f)\,df}.
$$

- **Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓（注意 $2\pi f_0$ 的單位是
  rad/s，不是 Hz）。
- **隨機漫步特徵**：相位 random walk 在時域對應 **accumulated jitter（累積抖動）**
  $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$（[P2] Eq.(8), p.792；κ 由 Eq.(12), p.793）——量測間隔越長、累積誤差
  的 rms 越大，正是「沒有絕對時間基準」的指紋。詳見
  [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)。

## 數值例子（建立手感）

用規範第 8 節的 canonical 數值，把上面的幾何落地成數字。

> **例 A**：$q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$、$f_0=5$ GHz。

一顆 $\Delta q=1$ fC 的電荷脈衝注在 $\Gamma=0.5$ 的相位（介於 peak 與 zero crossing 之間）：

$$
\Delta\phi=\frac{\Gamma\,\Delta q}{q_{max}}=\frac{0.5\times(1\times10^{-15}\,\text{C})}{1\times10^{-12}\,\text{C}}=5\times10^{-4}\ \text{rad}\;(\approx0.0286^\circ),
$$

換成 timing error：

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0}=\frac{5\times10^{-4}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}\approx1.59\times10^{-14}\ \text{s}=15.9\ \text{fs}.
$$

- **手感**：在 5 GHz（週期 200 ps）下，一顆 1 fC（約 6240 個電子）的電荷在中等敏感相位
  只造成 ~16 fs 的時間誤差。**單顆很小，但相位沒有恢復力，noise 持續踢就會積分累積**——
  這正是第 5 步講的 random walk。
- 若同樣 1 fC 注在波峰（$\Gamma\approx 0$），$\Delta\phi\approx 0$、$\Delta t\approx 0$：
  能量幾乎全進振幅，幾個時間常數後被恢復項吃掉，對相位無永久影響。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 存在穩定 limit cycle | 振幅擾動會衰減、只需追蹤相位 | 無穩定環（如未起振或多模）時整套幾何不適用 |
| 小訊號 $\Delta q\ll q_{max}$ | 切向投影可線性化，$\Delta\phi\propto\Delta q$ | 大注入 → 非線性、AM–PM、$\Gamma$ 本身被改變 |
| 自治振盪（無外部時鐘） | 相位是中性穩定自由度、會累積 | 鎖相／injection-locked 時相位被外部拉住（見 [P3]） |
| 脈衝遠窄於週期 $T$ | 可視為瞬間電壓跳變 | 寬脈衝要用 Eq.(11) 積分形式 |

## 重點回顧

- 振盪器狀態畫在 2-D 平面上沿 **limit cycle** 等速繞圈；相位 = 沿環的角位置。
- 自治振盪器**沒有絕對時間基準**（方程不含顯式 $t$）→ 沿環滑動不耗能、不被恢復力反對。
- 擾動分解：**切向 = phase 擾動（永久累積）**、**徑向 = amplitude 擾動（被恢復力拉回）**。
- 同一個 impulse 在 peak（$\Gamma\approx 0$）vs zero crossing（$|\Gamma|$ 最大）效果天差地遠
  → 週期時變敏感度 → ISF。
- 累積的相位 random walk 在頻域 = **phase noise** $\mathcal{L}(\Delta f)$，在時域 =
  **timing jitter** $\sigma_t=\sigma_\phi/(2\pi f_0)$。
- 例 A：1 fC @ $\Gamma=0.5$、$q_{max}=1$ pC、5 GHz → $\Delta\phi=5\times10^{-4}$ rad → 15.9 fs。
- 來源：[P1] Fig. 4、Sec. III-A；toy model 出自 lab_01。

## 延伸閱讀

- 下一步——把幾何變成公式：[從 impulse 到 phase shift 的推導](/03_isf_core_theory/impulse_to_phase_shift)
- 為何相位雜訊重要、振幅雜訊被抑制：[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)
- 週期時變敏感度的本質：[LTI vs LTV](/02_foundations/lti_vs_ltv)
- 全站符號與單位：[統一符號表 Notation](/00_overview/notation)
- 數值換算練習：[數值手感 Numerical Feeling](/04_simulation_labs/numerical_feeling)
