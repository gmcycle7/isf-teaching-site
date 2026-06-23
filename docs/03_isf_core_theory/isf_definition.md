---
title: ISF 的定義
description: 從 current impulse 到 charge、到 state 擾動、投影到 phase direction，嚴謹定義無因次的 Γ(ω₀τ)，並推導 ideal LC 的 Γ(θ)=−sin θ。
---

# ISF 的定義

> **前置閱讀**：[oscillator_phase](/02_foundations/oscillator_phase)（limit cycle 與 excess phase 的幾何）、[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)（切向相位 vs 徑向振幅的分解）、[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)（電荷→電壓→相位的操作型鏈條）。

這頁回答一個聽起來簡單、其實很深的問題：**ISF（Impulse Sensitivity Function，脈衝敏感度函數）到底是什麼東西？它是一個 function，但它的「自變數」是什麼、「值」代表什麼、單位是什麼、為什麼是週期的、為什麼每個 node 和每個 noise source 各有一個？**

ISF 是 Hajimiri–Lee 1998 年 LTV（Linear Time-Variant，線性時變）相位雜訊理論的核心物件。它的操作型定義是：在波形相位 $\omega_0\tau$ 的時刻注入一坨電荷 $\Delta q$，造成的**永久相位偏移** $\Delta\phi$ 為（[P1] from Eq.(10)-(11), p.182）：

$$
\Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q
$$

把它寫成脈衝響應就是 [P1] Eq.(10), p.182：

$$
h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau)
$$

> **物理直覺（先講結論）**：振盪器穩態時，狀態點沿著一條封閉軌跡（limit cycle，極限環）一圈一圈轉。你拿一根手指（current impulse）去戳它一下——戳出去的位移可以拆成「沿軌跡切向」與「垂直軌跡徑向」兩個分量。**切向**那一份改變的是「轉到哪裡了」，也就是**相位**，而且因為相位沒有恢復力，這份偏移**永遠留著**；**徑向**那一份改變的是振幅，會被振盪器的 amplitude restoring（振幅恢復）機制慢慢拉回、不留痕跡。$\Gamma(\omega_0\tau)$ 就是「在相位 $\omega_0\tau$ 戳一單位電荷，有多少變成永久相位」的那個**敏感度權重**。它不是雜訊本身，是把雜訊翻譯成相位的「轉換係數」。

完整的「電荷→電壓→相位」逐步推導在 [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)。本頁聚焦在「$\Gamma$ 是什麼」與「$\Gamma$ 的性質」，並把 ideal LC 的 $\Gamma(\theta)=-\sin\theta$ 從幾何**親手算出來**。

## 第 1 步：從 impulse 到 state 擾動（複習關鍵物理）

把前一頁的鏈條快速串一遍，因為定義 $\Gamma$ 必須站在這條鏈上：

1. **current impulse → charge**：很窄的電流脈衝沉積電荷 $\Delta q=\int i(t)\,dt$。單位 $[\text{A}]\cdot[\text{s}]=[\text{C}]$ ✓。
2. **charge → voltage step**：節點電容 $C_{node}$ 上電壓瞬跳 $\Delta V=\Delta q/C_{node}$（[P1] Eq.(9), p.182）。單位 $[\text{C}]/[\text{F}]=[\text{V}]$ ✓。
3. **voltage step → state perturbation**：在 LC 中，電流脈衝只能瞬間改**電容電壓**（電感電流不能瞬變），所以擾動是 state-space 裡一個**沿電壓軸的水平位移**。

到這裡，狀態被推離 limit cycle 一點點。關鍵問題是：這個位移有多少變成**相位**？

## 第 2 步：投影到 phase direction

把振盪器狀態畫成 2-D 向量 $\mathbf{z}=(v,w)$，其中 $v$ 是電容電壓、$w$ 正比於電感電流。穩態軌跡是一個封閉環，狀態以角速度 $\omega_0$ 沿環移動。定義環上的**相位** $\theta=\omega_0 t$ 為「轉到哪個角度」。

一個沿電壓軸的小位移 $\Delta\mathbf{z}=(\Delta V,0)$ 打在環上某一點。把這個位移分解到該點的**切向**（phase direction，相位方向，即 $\partial\mathbf{z}/\partial\theta$ 的方向）與**法向**（amplitude direction，振幅方向）：

$$
\Delta\mathbf{z}=\underbrace{(\Delta\mathbf{z}\cdot\hat{\mathbf{t}})}_{\text{切向→相位}}\hat{\mathbf{t}}+\underbrace{(\Delta\mathbf{z}\cdot\hat{\mathbf{n}})}_{\text{法向→振幅（會衰減）}}\hat{\mathbf{n}}.
$$

- **用到的數學**：把擾動向量投影到 limit cycle 的單位切向量 $\hat{\mathbf{t}}$。這是嚴謹版本背後 PPV（perturbation projection vector，擾動投影向量）／Floquet 理論的雛形（**PPV/adjoint/Floquet 不在下載的 5 篇 PDF 內，屬 Demir 等外部文獻**，見 [effective_isf](/03_isf_core_theory/effective_isf)）。
- **為何只留切向**：法向分量改變的是「離環多遠」＝振幅；穩定振盪一定有 amplitude restoring 把它拉回（見 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)）。切向分量改變的是「環上的角度」＝相位，相位是中性方向、無恢復力，所以**永久保留並累積**（claim C2，[P1] Sec. III-A）。

切向投影量除以「沿環走一單位相位對應多少 state 位移」，就把 $\Delta V$ 換算成 $\Delta\theta=\Delta\phi$。整個換算只跟「你打在環的哪個角度」有關——這就是 $\Gamma$ 只是 $\omega_0\tau$ 的函數的原因。

## 第 3 步：把比例 normalize 成無因次的 $\Gamma$

把第 1–2 步串起來：$\Delta\phi\propto\Delta V=\Delta q/C_{node}$，比例係數只跟注入相位有關。Hajimiri–Lee 用節點最大電荷擺幅 $q_{max}=C_{node}V_{max}$ normalize，定義無因次函數 $\Gamma(\omega_0\tau)$：

$$
\boxed{\ \Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q\ }
$$

- **$\Gamma$ 為何無因次**：$\Delta\phi$ 是 rad（無因次），$\Delta q/q_{max}$ 是電荷比（無因次），所以 $\Gamma$ 必為無因次。**Dimension check**：$[\text{rad}]=\Gamma\cdot[\text{C}]/[\text{C}]\Rightarrow\Gamma$ 無因次 ✓。
- **為何 normalize 用 $q_{max}$**：讓 $\Gamma$ 只描述「波形哪裡敏感」的**形狀**，與振幅絕對大小脫鉤；實際相位偏移大小由 $\Delta q/q_{max}$（注入電荷相對訊號電荷的比例）決定。這也直接給出 design 結論 C3：phase noise $\propto\Gamma_{rms}^2/q_{max}^2$，要壓低就「加大 $q_{max}$、壓小 $\Gamma_{rms}$」（[P1] Eq.(21)）。

## $\Gamma$ 的五個必記性質

| 性質 | 說明 | 為什麼 |
|---|---|---|
| **無因次** | 沒有單位 | 由 dimension check（上面）保證 |
| **$2\pi$ 週期** | $\Gamma(x+2\pi)=\Gamma(x)$ | 自變數是「波形相位」，波形本身 $2\pi$ 週期 |
| **不是 noise 本身** | 是「相位敏感度」權重函數 | noise 是 $i_n(\tau)$；$\Gamma$ 是把 $i_n$ 翻成 $\phi$ 的 kernel |
| **由 large-signal periodic operating point 決定** | 要知道完整的週期穩態波形（含 hard-switching）才能定出 $\Gamma$ | 投影方向 $\hat{\mathbf{t}}$ 沿著 limit cycle 變，是大訊號軌跡的幾何（[P1] assumptions） |
| **每個 node／每個 noise source 各有一個** | 不同注入點、不同 device 看到的 $\Gamma$ 不同 | 投影方向與該節點電容、該源注入位置有關 |

> **「不是 noise 本身」最常被誤解。** $\Gamma$ 是電路結構與波形決定的**確定性週期函數**，跟 noise 多大、是白噪還是 flicker 完全無關。換個 noise source（換 $i_n$）不會改 $\Gamma$，但會改最後的 $\phi$。換個注入節點（換投影幾何）才會改 $\Gamma$。

## 親手推導：ideal LC 的 $\Gamma(\theta)=-\sin\theta$

理論不能只說漂亮話，這裡用**無耗損並聯 LC**把 $\Gamma$ 整條算出來，作為全站的 reference 波形。

**設定**：理想 LC 的狀態做等速圓周（諧振），寫成

$$
\mathbf{z}(\theta)=A\,(\cos\theta,\ \sin\theta),\qquad \theta=\omega_0 t,
$$

其中第一分量 $v=A\cos\theta$ 是電容電壓（輸出波形 $\propto\cos\theta$）。

**Step A — 注入造成的 state 位移**：電流脈衝只改電容電壓，$\Delta v=\Delta q/C$，所以

$$
\Delta\mathbf{z}=(\Delta v,\,0)=\Big(\tfrac{\Delta q}{C},\,0\Big).
$$

**Step B — 投影到切向**。沿環的切向量

$$
\frac{\partial\mathbf{z}}{\partial\theta}=A\,(-\sin\theta,\ \cos\theta),\qquad \left|\frac{\partial\mathbf{z}}{\partial\theta}\right|=A.
$$

相位增量 $\Delta\theta$ 滿足「切向位移 ＝ 切向速度 × 相位增量」：把 $\Delta\mathbf{z}$ 點乘單位切向量、再除以 $|\partial\mathbf{z}/\partial\theta|$：

$$
\Delta\phi=\Delta\theta=\frac{\Delta\mathbf{z}\cdot(\partial\mathbf{z}/\partial\theta)}{|\partial\mathbf{z}/\partial\theta|^2}=\frac{(\Delta v,0)\cdot A(-\sin\theta,\cos\theta)}{A^2}=\frac{-A\sin\theta\,\Delta v}{A^2}=\frac{-\sin\theta}{A}\,\Delta v.
$$

**逐步代數（把上式的每個等號拆開，不跳步）**：

$$
\begin{aligned}
\text{分子（內積）}&:\ (\Delta v,\,0)\cdot A(-\sin\theta,\ \cos\theta)
=\Delta v\cdot(-A\sin\theta)+0\cdot(A\cos\theta)=-A\sin\theta\,\Delta v,\\
\text{分母}&:\ \left|\frac{\partial\mathbf{z}}{\partial\theta}\right|^2=\big(A(-\sin\theta)\big)^2+\big(A\cos\theta\big)^2=A^2(\sin^2\theta+\cos^2\theta)=A^2,\\
\text{相除}&:\ \Delta\phi=\frac{-A\sin\theta\,\Delta v}{A^2}=\frac{-\sin\theta}{A}\,\Delta v.
\end{aligned}
$$

- **為何要除以 $|\partial\mathbf z/\partial\theta|^2$ 而不是 $|\partial\mathbf z/\partial\theta|$**：先點乘單位切向量 $\hat{\mathbf t}=\dfrac{\partial\mathbf z/\partial\theta}{|\partial\mathbf z/\partial\theta|}$ 得「切向位移長度」，再除以「沿環走一單位 $\theta$ 對應的弧長 $|\partial\mathbf z/\partial\theta|$」換成 $\Delta\theta$；兩個 $|\partial\mathbf z/\partial\theta|$ 合起來就是分母的平方。
- **$\sin^2\theta+\cos^2\theta=1$** 是這裡讓分母乾淨收成 $A^2$ 的關鍵恆等式（圓周運動的等速性）。

**Step C — 代入 $\Delta v=\Delta q/C$**：

$$
\Delta\phi=\frac{-\sin\theta}{A}\cdot\frac{\Delta q}{C}=\frac{-\sin\theta}{AC}\,\Delta q.
$$

**Step D — 認出 $q_{max}$**：節點最大電荷擺幅 $q_{max}=C\,V_{max}=C A$。代入：

$$
\Delta\phi=\frac{-\sin\theta}{q_{max}}\,\Delta q\quad\Longrightarrow\quad\boxed{\ \Gamma(\theta)=-\sin\theta\ }
$$

正好對上定義 $\Delta\phi=\Gamma(\theta)\,\Delta q/q_{max}$。**Dimension check**：$\Gamma=-\sin\theta$ 無因次 ✓；$\Delta q/q_{max}$ 無因次 ✓；$\Delta\phi$ rad ✓。

**怎麼讀這個 $-\sin\theta$**（對上 [P1] Fig. 4 的直覺，p.181）：

- 在**波峰**注入（$\theta=0$，輸出 $v=A\cos\theta$ 最大）：$\Gamma(0)=0$。手指沿電壓軸戳，方向幾乎與軌跡**垂直**（純徑向）→ 只改振幅、幾乎不改相位。振幅擾動會被拉回，所以這一戳「沒留下永久痕跡」。
- 在**zero crossing**注入（$\theta=\pi/2$，$v=0$、波形斜率最大）：$|\Gamma|=1$（最大）。手指沿電壓軸戳，方向幾乎與軌跡**相切**（純切向）→ 幾乎全部變成永久相位跳變。
- 介於之間：切向／徑向按 $-\sin\theta$ 連續分配。

這正是 **LTV 的本質**：同一個 $\Delta q$，注入時刻不同（$\theta$ 不同），效果完全不同。LTI 系統不會有這種「看你何時打」的行為。詳見 [lti_vs_ltv](/02_foundations/lti_vs_ltv)。

## 對應圖

**(1) LC 波形與其 ISF**：上排是 $v(t)=A\cos\theta$ 與 $\Gamma(\theta)=-\sin\theta$ 對齊畫（峰對零、零交越對峰）；下排示範 $\Delta\phi$ 與 $\Delta q$ 在小電荷時線性、且 zero-crossing 注入＝純相位跳。

![LC 波形與其 ISF：Γ=−sinθ，峰注入只改振幅、零交越注入給最大相位](/figures/lc_waveform_and_isf.png)

對應公式 $\Gamma_{LC}(\theta)=-\sin\theta$、$\Delta\phi=\Gamma\,\Delta q/q_{max}$；來源 [P1] Figs. 4, 6, 7(a)；script `simulations/lab_02_lc_toy_model.py`（`main`），參數 $f_0=1$、$f_s=8000$、$\mu=0.3$、$\Delta q/q_{max}\in[-0.05,0.05]$。**這是 pedagogical toy model，非 transistor-level。**

**(2) 數值法「眼見為憑」量出 $\Gamma$**：在不同相位注入小電荷、量持續相位偏移、反推 ISF，與解析 $-\sin\theta$ 幾乎重合（最大誤差約 0.001）：

![數值萃取的 ISF 與理論 −sin(θ) 對照](/figures/isf_impulse_sweep_sinusoidal.png)

來源：[P1] ISF 定義之驗證；script `simulations/lab_04_impulse_sweep.py`（`fig_isf_sweep`），$\Delta q/q_{max}=10^{-3}$、48 個相位點。詳見 [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep)。**toy model。**

## 數值例子（建立手感）

> **例 A**：$q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$、$f_0=5$ GHz。

取 $\Gamma=0.5$（注意理想 LC 的 $|\Gamma|$ 最大才到 1，$\Gamma=0.5$ 對應 $-\sin\theta=0.5$，即 $\theta\approx-30^\circ$ 附近的中等敏感相位）：

$$
\Delta\phi=\frac{\Gamma\,\Delta q}{q_{max}}=\frac{0.5\times(1\times10^{-15}\,\text{C})}{1\times10^{-12}\,\text{C}}=5\times10^{-4}\ \text{rad}\approx0.0286^\circ.
$$

換成 timing error（$\Delta t=\Delta\phi/(2\pi f_0)$）：

$$
\Delta t=\frac{5\times10^{-4}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}\approx1.59\times10^{-14}\ \text{s}=15.9\ \text{fs}.
$$

**Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。**手感**：1 fC（約 6240 個電子）在中等敏感相位只踢出 ~16 fs；單顆很小，但 noise 持續踢、會被積分累積（見下一頁）。

```python
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
import numpy as np

# ideal LC ISF：Γ(θ) = -sin(θ)
theta = np.array([0.0, np.pi/2])          # 峰、零交越
print(gamma_lc_ideal(theta))              # -> [ 0. -1.]  峰處 0、零交越 |Γ|=1

dphi = impulse_to_phase_step(delta_q=1e-15, gamma_value=0.5, qmax=1e-12)
print(dphi, "rad")                        # -> 0.0005 rad
```

（函式庫：`simulations/common/isf_utils.py`。）

## 各 paper 的 ISF 定義比較表

同一個 $\Gamma$ 在不同論文裡扮演不同角色，但核心物件一致：

| 來源 | 符號／物件 | 脈絡 | 與本站 $\Gamma$ 的關係 | 信心 |
|---|---|---|---|---|
| **[P1]** Hajimiri–Lee 1998 | $\Gamma(\omega_0\tau)$ | phase noise（LTV impulse response） | **本站定義的原始出處**，Eq.(10),(11) | high（公式已核） |
| **[P2]** Hajimiri–Limotyrakis–Lee 1999 | $\Gamma(\omega_0\tau)$ | ring oscillator 的 jitter／phase noise | 同一個 $\Gamma$；強調 $\Gamma_{rms}\propto N^{-3/4}$ scaling（[P2] Eq.(16), p.794） | high（敘述與 scaling 皆已核實） |
| **[P3]** Hong–Hajimiri 2019 Part I | $\Gamma(\theta+\phi)$ | injection locking／pulling（廣義 Adler） | **同一個 $\Gamma$**，搬到注入脈絡：$\frac{d\phi}{dt}=\Delta\omega-\frac{1}{q_{max}}\langle\Gamma(\theta+\phi)\,i_{inj}(\theta)\rangle$（[P3] Eq.(30), p.2113；本站 $\Gamma$ 取與 [P3] 相反符號慣例，故平均項前為 $-$，數值等價） | high（已對照原始 PDF） |
| **[P4]** Hong–Hajimiri 2019 Part II | $\Lambda(\phi)$（APF） | amplitude modulation（振幅域） | **振幅版**：把 impulse 投影到**徑向**而非切向；單位 $\text{A}^{-1}$；ideal LC 中 ISF 與 APF 正交（quadrature，[P4] Eq.(26), p.2128） | ✓（APF=[P4] Eq.(19)、Fig. 5, p.2126，已核實） |
| **[P5]** Hajimiri–Heald 1998 | — | sense amplifier | **與 ISF 無關**（sense amplifier 論文，誠實標明 mislabeled） | high（明顯離題） |

> **記法陷阱**：[P3] 寫成 $\Gamma(\theta+\phi)$ 是把「注入波形相位 $\theta$」與「振盪器自身 excess phase $\phi$」相加當自變數——本質仍是同一個 $\Gamma$，只是 argument 換成「相對相位」。[P4] 的 APF $\Lambda$ 是**振幅**敏感度，與 $\Gamma$（相位敏感度）互補；在 ideal LC 兩者正交（一個 $\propto\sin$、一個 $\propto\cos$）。詳見 [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2)。
>
> **已核實**：[P3] 廣義 Adler（Eq.30/33, p.2113–2114）與 [P4] APF（Eq.25/26, p.2128）已對照原始 PDF；詳見 paper_003 / paper_004 deep-dive。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 小訊號 $\Delta q\ll q_{max}$ | 切向投影線性，$\Gamma$ 與 $\Delta q$ 無關 | 大注入 → 非線性、AM–PM、$\Gamma$ 本身被改變 |
| 穩定 limit cycle（振幅擾動衰減） | 只需追蹤相位 | 無穩定環或強 AM–PM 時 phase-only 模型不成立 |
| 已知大訊號週期穩態波形 | 能定出 $\Gamma$ 的形狀 | 不知波形就不知投影方向；要靠 transient／adjoint 萃取 |
| 脈衝遠窄於週期 $T$ | 可視為瞬間注入 | 寬脈衝要用 Eq.(11) 積分形式（見下頁） |

## Worked examples 數值例題

格式照規範第 10.4：題目 → 逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證。

### 例題 1：$\Gamma=-\sin$ 在 $\theta=0,\pi/4,\pi/2$ 的值與對應 $\Delta\phi$

> **題目**：理想 LC 的 $\Gamma(\theta)=-\sin\theta$。在三個相位 $\theta=0$（波峰）、$\theta=\pi/4$（半途）、$\theta=\pi/2$（zero crossing）各注入同一坨電荷，注入電荷比固定為 $\Delta q/q_{max}=10^{-3}$。求各處的 $\Gamma$ 與相位步階 $\Delta\phi=\Gamma\cdot\Delta q/q_{max}$。

**逐步代入**：先算 $\Gamma$，再乘上 $\Delta q/q_{max}=10^{-3}$。

$$
\begin{aligned}
\theta=0:\quad &\Gamma=-\sin0=0, &\Delta\phi&=0\times10^{-3}=0\ \text{rad}.\\
\theta=\tfrac{\pi}{4}:\quad &\Gamma=-\sin\tfrac{\pi}{4}=-\tfrac{1}{\sqrt2}\approx-0.7071, &\Delta\phi&=-0.7071\times10^{-3}=-7.07\times10^{-4}\ \text{rad}.\\
\theta=\tfrac{\pi}{2}:\quad &\Gamma=-\sin\tfrac{\pi}{2}=-1, &\Delta\phi&=-1\times10^{-3}=-1.0\times10^{-3}\ \text{rad}.
\end{aligned}
$$

**結果**：同一坨電荷在波峰幾乎不改相位（$\Delta\phi=0$）、在 zero crossing 給最大相位步階（$|\Delta\phi|=1$ mrad），半途則介於兩者之間（$0.707$ mrad）。這就是 **LTV 的核心現象**：效果由「你何時打」決定。

**dimension check**：$\Gamma$ 無因次、$\Delta q/q_{max}$ 無因次 → $\Delta\phi$ 無因次（rad）✓。負號代表相位被往後推（落後），數量級由 $\Delta q/q_{max}$ 設定，與規範例 A 的 $5\times10^{-4}$ rad 同量級（例 A 用 $\Gamma=0.5$）。

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
theta = np.array([0.0, np.pi/4, np.pi/2])
g = gamma_lc_ideal(theta)                       # -> [ 0.    -0.7071 -1.    ]
dphi = impulse_to_phase_step(delta_q=1e-3, gamma_value=g, qmax=1.0)  # Δq/qmax = 1e-3
print(g)                                        # ISF 值
print(dphi)                                     # -> [ 0.  -7.07e-04  -1.0e-03 ] rad
```

### 例題 2：把 zero-crossing 注入換成 5 GHz 的 timing error

> **題目**：承例題 1 的 $\theta=\pi/2$（$|\Delta\phi|=1$ mrad），在 $f_0=5$ GHz 下換成 timing error $\Delta t=\Delta\phi/(2\pi f_0)$。

**逐步代入**：

$$
\Delta t=\frac{1\times10^{-3}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=\frac{10^{-3}}{3.1416\times10^{10}}\ \text{s}\approx3.18\times10^{-14}\ \text{s}=31.8\ \text{fs}.
$$

**結果**：最敏感相位、$\Delta q/q_{max}=10^{-3}$ 的單顆注入，在 5 GHz 給約 **31.8 fs** 的時間誤差（呼應 numerical_feeling 的「1 mrad ≈ 32 fs」記憶點）。

**dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓（$2\pi f_0$ 是 rad/s）。

```python
from simulations.common.noise_utils import phase_to_time_error
print(phase_to_time_error(1e-3, 5e9)*1e15, "fs")   # -> 31.83 fs
```

（函式庫：`simulations/common/isf_utils.py`、`simulations/common/noise_utils.py`。）

## 重點回顧

- $\Gamma(\omega_0\tau)$ ＝「在波形相位 $\omega_0\tau$ 注一單位電荷，有多少變成永久相位」的敏感度權重。
- 推導鏈：impulse → charge $\Delta q$ → voltage step $\Delta V$ → state 位移 → **投影到切向（phase direction）** → 永久相位 $\Delta\phi$。
- $\Gamma$ **無因次、$2\pi$ 週期、不是 noise 本身、由 large-signal periodic operating point 決定、每個 node／noise source 各有一個**。
- ideal LC：$\Gamma(\theta)=-\sin\theta$，峰注入 $\Gamma=0$（只改振幅）、零交越 $|\Gamma|=1$（最大相位）——這就是 LTV。
- 各 paper：[P1][P2] 用 $\Gamma$ 於 phase noise；[P3] 把同一 $\Gamma$ 用於 injection；[P4] 的 APF $\Lambda$ 是振幅版；[P5] 與 ISF 無關。
- 來源：[P1] Eqs.(10),(11)，p.182；驗證圖見 lab_02／lab_04。

## 延伸閱讀

- 操作型逐步推導：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)
- 對任意 noise 疊加（卷積式）：[convolution_derivation](/03_isf_core_theory/convolution_derivation)
- $\Gamma$ 的傅立葉級數與頻率搬移：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- cyclostationary 與 effective ISF（含 PPV/adjoint 外部文獻）：[effective_isf](/03_isf_core_theory/effective_isf)
- 相位 vs 振幅幾何：[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)、[oscillator_phase](/02_foundations/oscillator_phase)
