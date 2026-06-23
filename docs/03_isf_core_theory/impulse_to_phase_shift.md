---
title: 從 impulse 到 phase shift 的推導
description: 從 Δq = ∫i dt 一路推到 Δφ = Γ(ω₀τ)·Δq/q_max，逐步、帶單位、附數值。
---

# 從 impulse 到 phase shift 的推導

> **先備**：[oscillator_phase](/02_foundations/oscillator_phase)（limit cycle 與相位／振幅幾何）、[lti_vs_ltv](/02_foundations/lti_vs_ltv)（為何振盪器對 noise 是 LTV） ｜ **接下來**：[isf_definition](/03_isf_core_theory/isf_definition)（嚴謹 ISF 定義與多節點）→ [convolution_derivation](/03_isf_core_theory/convolution_derivation)（對任意 noise 做卷積疊加）

這頁回答一個非常具體的問題：**一個 current impulse（電流脈衝）注進振盪器的某個節點，
會讓振盪器的相位偏移多少？** 答案就是 ISF 理論的操作型定義：

$$
\Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q
$$

我們不直接背這條，而是從電容的 $q=Cv$ 一步步推出來，每一步都說明用了什麼物理、
什麼近似、單位是什麼、怎麼做 dimension check。

> **物理直覺（先講結論）**：noise 電流先變成節點上的一坨**電荷** $\Delta q$；這坨電荷
> 把振盪器的瞬時狀態推離原本軌跡一點點；這「一點點」有多少**轉成相位**、多少轉成振幅，
> 取決於你在**波形的哪個相位**踢它——這個「轉換比例」就是 ISF $\Gamma$。在波形斜率大的
> 地方踢，相位被推得多；在波峰踢，幾乎只改振幅。

## 第 1 步：current impulse 變成 charge

電流對時間積分就是電荷。一個很窄、很短的電流脈衝 $i(t)$ 注入節點，沉積的總電荷是

$$
\Delta q=\int i(t)\,dt .
$$

- **用到的物理**：電荷守恆／電流定義 $i=dq/dt$。
- **單位檢查**：$[\text{A}]\cdot[\text{s}]=[\text{C}]$ ✓（安培乘秒等於庫侖）。
- **為何合理**：脈衝寬度遠小於週期 $T$ 時，可視為「瞬間」把 $\Delta q$ 倒進節點。

## 第 2 步：charge 變成 voltage 步階

節點上有總電容 $C_{node}$。瞬間多出的電荷會讓節點電壓**瞬間跳一步**（[P1] Eq.(9), p.181）：

$$
\Delta V=\frac{\Delta q}{C_{node}} .
$$

- **用到的物理**：電容關係 $q=Cv$，對小變化取微分 $\Delta q=C\,\Delta V$。
- **單位檢查**：$[\text{C}]/[\text{F}]=[\text{C}]/[\text{C/V}]=[\text{V}]$ ✓。
- **關鍵觀察**：在並聯 LC 中，電流脈衝只改**電容電壓**（瞬間），不改**電感電流**
  （電感電流不能瞬變）。所以 state-space 裡這是一個**沿電壓軸的水平跳變**。

## 第 3 步：voltage 步階推離 limit cycle，但只有「切向分量」變成相位

把振盪器狀態畫在 2-D 平面（例如橫軸=電容電壓 $v$、縱軸=正比於電感電流的 $w$）。穩態時
狀態沿著 **limit cycle**（極限環）轉圈。第 2 步的電壓跳變把狀態點推到旁邊：

- 推離環的**徑向分量** → 改變**振幅** $A$。但振盪器有 amplitude restoring（振幅恢復）機制，
  這部分**會被慢慢拉回**，不會永久殘留。
- 沿著環的**切向分量** → 改變**相位** $\phi$。相位**沒有**恢復力，這部分**永久留著**。

同一個 $\Delta V$ 在不同相位 $\tau$ 踢，切向／徑向的分配比例不同。把「$\Delta V$ 轉成
$\Delta\phi$ 的比例」整理成一個只跟注入相位有關的週期函數，就是 ISF：

$$
\Delta\phi=\underbrace{\big(\text{相位轉換比例}\big)}_{\text{只跟}\omega_0\tau\text{有關}}\times\Delta V .
$$

下圖把這個分解畫在 state plane 上。同一坨電荷造成的**水平** $\Delta V=\Delta q/C$
（電流只踢電容電壓軸，電感電流不能瞬變），被虛線分解成沿環的**切向分量**（綠，永久相位）
與離環的**徑向分量**（紅，會衰減）。在 zero-crossing 附近注入時水平踢幾乎全落在切向（相位被推得多）；
在 peak 附近注入時幾乎全落在徑向（只改振幅）。兩格左下角標出 $\Gamma(\theta)=-\sin\theta$ 的值——
**切向佔比恰好就是 $\Gamma(\theta)$**，這讓理想 LC 的 $\Gamma=-\sin\theta$ 變得幾何上不可避免
（$\Gamma=-\sin\theta$ 的代數推導見 [isf_definition](/03_isf_core_theory/isf_definition)）。

![理想 LC state plane 上的脈衝分解：同一個水平 ΔV=Δq/C 被虛線分解成切向（→Δφ，永久相位）與徑向（→ΔA，會衰減）兩分量；zero-crossing 附近幾乎全切向、peak 附近幾乎全徑向，切向佔比即 Γ(θ)=−sin θ。此為 ideal lossless LC 的 pedagogical 幾何圖，非 transistor-level。](/figures/impulse_phase_decomposition.png)

- **用到的數學**：把擾動向量投影到 limit cycle 的切線方向（phase direction）。
- **為何只留切向**：見 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)
  與 [oscillator_phase](/02_foundations/oscillator_phase)——振幅被 restoring 拉回，相位不會。

## 第 4 步：用 $q_{max}$ normalize，得到無因次的 ISF

把第 1～3 步串起來：$\Delta\phi\propto\Delta V=\Delta q/C_{node}$。Hajimiri–Lee 選擇用
節點的**最大電荷擺幅** $q_{max}=C_{node}V_{max}$ 來 normalize，把那個「相位轉換比例」
寫成無因次函數 $\Gamma(\omega_0\tau)$（[P1] Eq.(10)–(11), p.182）：

$$
\boxed{\ \Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q\ }
$$

- **為什麼要 $q_{max}$ normalization**：讓 $\Gamma$ 變成**無因次、與振幅大小無關**的「形狀」，
  只描述「波形哪裡敏感」。實際的相位偏移大小由 $\Delta q/q_{max}$（注入電荷相對訊號電荷的
  比例）決定。
- **$\Gamma$ 為何無因次**：$\Delta\phi$ 是 rad（無因次），$\Delta q/q_{max}$ 也是無因次，
  所以 $\Gamma$ 必須無因次。**Dimension check**：$[\text{rad}]=\Gamma\cdot[\text{C}]/[\text{C}]$
  $\Rightarrow\Gamma$ 無因次 ✓。
- **小訊號假設**：第 3 步把投影當成線性，要求 $\Delta q\ll q_{max}$（踢一下不能把振盪器踢翻）。
  [P1] Fig. 6 用實際 Colpitts 與 5 級 ring 證實了「$\Delta\phi$ 與 $\Delta q$ 在小電荷時成正比」。

## 對應的脈衝響應（為下一章鋪路）

因為相位步階**永久保持**，把它寫成脈衝響應就帶一個 unit step $u(t-\tau)$（[P1] Eq.(10)）：

$$
h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau).
$$

注意它依賴**絕對注入時刻 $\tau$**（透過 $\Gamma(\omega_0\tau)$），不是只依賴 $t-\tau$
——這正是 **LTV（線性時變）**的特徵，下一章 [convolution_derivation](/03_isf_core_theory/convolution_derivation)
會用它對任意 noise 電流做疊加。ISF 的完整定義與多節點討論見
[isf_definition](/03_isf_core_theory/isf_definition)。

## 數值例子（建立手感）

> **例 A**：$q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$、$f_0=5$ GHz。

**相位步階**：

$$
\Delta\phi=\frac{\Gamma\,\Delta q}{q_{max}}=\frac{0.5\times(1\times10^{-15}\,\text{C})}{1\times10^{-12}\,\text{C}}=5\times10^{-4}\ \text{rad}.
$$

換成度：$\Delta\phi=5\times10^{-4}\times\dfrac{180}{\pi}\approx0.0286^\circ$。

**換成 timing error**（用 $\Delta t=\Delta\phi/(2\pi f_0)$）：

$$
\Delta t=\frac{5\times10^{-4}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=\frac{5\times10^{-4}}{3.1416\times10^{10}}\ \text{s}\approx1.59\times10^{-14}\ \text{s}=15.9\ \text{fs}.
$$

- **Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓（注意 $2\pi f_0$ 的單位是 rad/s）。
- **手感**：在 5 GHz（週期 200 ps）下，一顆 1 fC 的電荷（約 6240 個電子）在最敏感相位
  也只造成 ~16 fs 的時間誤差。單顆很小——但 noise 是**持續**踢的，會積分累積（下一章）。

可用內建函式快速驗證：

```python
from simulations.common.isf_utils import impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error

dphi = impulse_to_phase_step(delta_q=1e-15, gamma_value=0.5, qmax=1e-12)
dt   = phase_to_time_error(dphi, f0=5e9)
print(dphi, "rad", dt*1e15, "fs")   # -> 0.0005 rad  15.92 fs
```

（完整 script：`simulations/common/isf_utils.py`、`simulations/common/noise_utils.py`。）

## 數值法「眼見為憑」：直接量 $\Gamma$

[lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep) 用模擬在不同相位注入小電荷、
量持續相位偏移，**反推出 ISF**，結果與理想 LC 的 $\Gamma(\theta)=-\sin\theta$ 幾乎完全吻合
（最大誤差約 0.001）：

![數值萃取的 ISF 與理論 -sin(θ) 對照](/figures/isf_impulse_sweep_sinusoidal.png)

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 小訊號 $\Delta q\ll q_{max}$ | $\Delta\phi$ 線性正比 $\Delta q$ | 大注入 → 非線性、AM–PM、ISF 本身被改變 |
| 振幅擾動會衰減 | 只需追蹤相位 | 高 AM–PM 或無穩定 limit cycle 時不成立 |
| 脈衝遠窄於週期 | 可視為瞬間注入 | 寬脈衝要用 Eq.(11) 積分形式 |
| 已知正確的 $\Gamma$ | 預測準確 | $\Gamma$ 要靠 transient/adjoint 模擬萃取（見 [effective_isf](/03_isf_core_theory/effective_isf)） |

## 重點回顧

- noise 電流 → 電荷 $\Delta q$ → 電壓跳變 $\Delta V=\Delta q/C$ → 經 ISF 投影成相位 $\Delta\phi$。
- $\Delta\phi=\Gamma(\omega_0\tau)\,\Delta q/q_{max}$；$\Gamma$ 無因次、$2\pi$ 週期、與注入相位有關。
- $q_{max}$ 把 $\Gamma$ normalize 成「形狀」；相位偏移大小由 $\Delta q/q_{max}$ 決定。
- 一顆 1 fC 在 5 GHz、$\Gamma=0.5$、$q_{max}=1$ pC 下 → 16 fs。
- 來源：[P1] Eq.(9) p.181、Eqs.(10),(11) p.182；驗證圖見 lab_04。

## 延伸閱讀

- 上一步的幾何：[oscillator_phase](/02_foundations/oscillator_phase)
- 嚴謹 ISF 定義與多節點：[isf_definition](/03_isf_core_theory/isf_definition)
- 對任意 noise 疊加：[convolution_derivation](/03_isf_core_theory/convolution_derivation)
- 數值手感總整理：[numerical_feeling](/04_simulation_labs/numerical_feeling)
