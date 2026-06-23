---
title: 波形斜率與相位敏感度
description: 為什麼在波形斜率小（接近波峰）的相位注入 noise 比較危險，而快 transition（陡 ZC）有幫助——從 ISF 與斜率的反比關係看起。
---

# 波形斜率與相位敏感度

> **先備**：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)（$\Delta\phi=\Gamma\,\Delta q/q_{max}$ 操作定義與 $q_{max}=CV_{max}$）、[lti_vs_ltv](/02_foundations/lti_vs_ltv)（為何同 impulse、不同相位、不同效果）｜ **接下來**：[symmetry](/06_design_insights/symmetry)、[tank_swing](/06_design_insights/tank_swing)

這頁回答一個非常實用、layout 與 bias 階段就用得到的問題：**同樣一坨 noise 電荷，
在波形的哪個相位注入最傷？** 直覺上你可能以為「波峰最高、最敏感」——剛好相反。
**ISF 大小大致與波形斜率成反比**：斜率小（接近波峰）的地方 $|\Gamma|$ 大、最容易被推出相位誤差；
斜率大（ZC，zero crossing，過零點）的地方反而把 noise 多半轉成振幅、被拉回。

> **物理直覺（先講結論）**：相位是「沿著 limit cycle 切線方向跑得多快」。在波峰，狀態點
> 走得「慢、平」（$dV/dt\approx0$），你橫推一下，它在時間軸上要花很久才走回原位——**等效於
> 很大的相位偏移**。在 ZC，狀態點正「全速通過」（$dV/dt$ 最大），同樣橫推一下，很快就被
> 帶回軌道，**幾乎不留相位**（多半變成可衰減的振幅擾動）。所以「斜率小的相位」才是危險區。

## 第 1 步：ISF 與斜率的反比關係

回到 impulse→phase 的操作定義（[P1] Eq.(10)–(11), p.182）：

$$
\Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q
$$

一坨電荷 $\Delta q$ 造成電壓跳變 $\Delta V=\Delta q/C$（[P1] Eq.(9)）。把這個電壓跳變翻譯成
「時間軸上的提前／延後」：波形在該點以斜率 $\dot V=dV/dt$ 通過，要把電壓抬高 $\Delta V$，
等效於把波形在時間上平移

$$
\Delta t\approx\frac{\Delta V}{\dot V}=\frac{\Delta q}{C\,\dot V}.
$$

- **單位檢查**：$[\text{V}]/[\text{V/s}]=[\text{s}]$ ✓。
- 換成相位 $\Delta\phi=\omega_0\Delta t$：

$$
\Delta\phi=\omega_0\frac{\Delta q}{C\,\dot V}\quad\Rightarrow\quad \Gamma\propto\frac{1}{\dot V}.
$$

**逐步代數：把這個「平移近似」和 ISF 操作定義對齊，看 $\Gamma$ 究竟正比於什麼。**
把上式的 $\Delta\phi$ 與操作定義 $\Delta\phi=\Gamma\,\Delta q/q_{max}$ 兩個表達式令相等：

$$
\begin{aligned}
\frac{\Gamma}{q_{max}}\,\Delta q&=\omega_0\,\frac{\Delta q}{C\,\dot V} \\[4pt]
\Gamma&=\frac{q_{max}\,\omega_0}{C\,\dot V}
\qquad(\text{兩邊同消 }\Delta q) \\[4pt]
\Gamma&=\frac{(C\,V_{max})\,\omega_0}{C\,\dot V}=\frac{\omega_0\,V_{max}}{\dot V}
\qquad(\text{代入 }q_{max}=C\,V_{max}) \\[4pt]
&=\frac{V_{max}}{\dot V/\omega_0}=\frac{V_{max}}{dV/d\theta}\qquad(\dot V=\omega_0\,dV/d\theta).
\end{aligned}
$$

- **每一步用到什麼**：第 1→2 行純代數（消 $\Delta q$）；第 2→3 行用 $q_{max}=C V_{max}$（電容定義，
  $C$ 自動約掉——這就是為什麼 ISF **與節點電容無關**，只跟波形形狀有關）；第 3→4 行把
  時間斜率換成相位斜率 $\dot V=\omega_0\,dV/d\theta$（鏈鎖律）。
- **結果的意義**：$\Gamma=V_{max}\big/(dV/d\theta)$ ——ISF **正比於 $V_{max}$、反比於波形對相位的斜率** $dV/d\theta$。
- **代正弦驗證**：$V=V_{max}\cos\theta\Rightarrow dV/d\theta=-V_{max}\sin\theta$，故
  $\Gamma=V_{max}/(-V_{max}\sin\theta)=-1/\sin\theta$。這個「$1/\sin$」是平移近似的產物，在斜率→0（波峰）處發散；
  嚴格的 LTV 投影給的是有界的 $\Gamma=-\sin\theta$（波峰處 $\Gamma=0$）。**兩者都說「斜率小 → 危險」，
  但發散與否不同**——平移近似只在斜率不為 0 的區間定性可用，定量請以 $\Gamma=-\sin\theta$ 為準。
- **dimension check**：$[\text{V}]/[\text{V}]=$ 無因次 ✓（$\Gamma$ 必須無因次）；中間式
  $\dfrac{[\text{C}]\cdot[\text{rad/s}]}{[\text{F}]\cdot[\text{V/s}]}=\dfrac{[\text{C}][\text{s}^{-1}]}{[\text{C/V}][\text{V/s}]}
  =\dfrac{[\text{C}][\text{s}^{-1}]}{[\text{C}][\text{s}^{-1}]}=$ 無因次 ✓（rad 不計入因次）。

- **結論**：ISF 大小**反比於瞬時斜率** $\dot V$。斜率大→$|\Gamma|$ 小（不敏感）；斜率小→$|\Gamma|$ 大（敏感）。
- 對理想正弦 $V=\cos\theta$，$\dot V\propto-\sin\theta$，所以 $\Gamma(\theta)\propto1/\sin\theta$ 的這個
  「平移」近似只在斜率不為 0 時成立；嚴格的 LC ISF 是 $\Gamma(\theta)=-\sin\theta$（在波峰 $\theta=0$
  處 $\Gamma=0$，在 ZC $\theta=\pi/2$ 處 $|\Gamma|$ 最大）。

> **這裡有一個常見的方向混淆，要說清楚**：上面「$\Delta t=\Delta V/\dot V$」的平移圖像，
> 講的是「波形被電壓擾動後，過零時刻（threshold crossing）移動多少」——那是 **threshold-crossing
> 敏感度**，斜率大時 timing 反而穩（這也是「快 transition 有幫助」的另一個角度）。
> 而 $\Gamma=-\sin\theta$ 講的是 **excess phase 敏感度**：它在波峰為 0、在 ZC 最大。
> 兩者看似矛盾，其實是不同問題：threshold crossing 問「邊緣何時穿過閾值」，excess phase 問
> 「limit cycle 切向被推多少」。**本頁與全站的 design rule 一律以 [P1] 的 ISF $\Gamma$（excess phase）為準**：
> $|\Gamma|$ 在 ZC（高斜率穿越點）最大、在波峰最小。這正是下圖要呈現的。

## 第 2 步：用 LC 波形與 ISF 對照圖看「哪裡危險」

下圖把理想 LC 的波形 $V(\theta)=\cos\theta$ 與其 ISF $\Gamma(\theta)=-\sin\theta$ 疊在一起：

![LC 波形與其 ISF](/figures/lc_waveform_and_isf.png)

怎麼讀這張圖：

- **波峰／波谷**（$\theta=0,\pi$，$V$ 極值、$dV/d\theta=0$）：$\Gamma=0$。在這裡注入電荷 → 純振幅擾動 → 被
  amplitude restoration（振幅恢復）拉回 → **幾乎不留相位**。這是「安全」相位。
- **過零點 ZC**（$\theta=\pi/2,3\pi/2$，$V=0$、斜率最大）：$|\Gamma|$ **最大**。在這裡注入電荷 → 純相位跳變
  → 永久殘留。這是「危險」相位。
- 對照 [P1] Fig. 4：同一個 impulse 打在 peak 與打在 ZC，state-space 裡切向／徑向分配完全不同——
  這正是 oscillator 是 **LTV（線性時變）**系統的招牌（claim C1）。

> 這是 **pedagogical toy model（教學玩具，非 transistor-level）**：用理想正弦狀態的 LC。
> 真實 LC 因 tank loss 與非線性 transconductor，ISF 不會是完美的 $-\sin$，但「波峰安全、ZC 危險」
> 的定性結論成立。完整 script：`simulations/lab_02_lc_toy_model.py`。

## 第 3 步：為什麼「快 transition」幫助 ring oscillator

Ring oscillator（環形振盪器）的波形不是正弦，而是接近方波——大部分時間「壓在軌（rail）」，
只有在切換瞬間（transition）快速衝過 ZC。它的 ISF 因此**集中在 transition 附近**（[P2] Fig. 6, p.793；Fig. 5 顯示峰值/lobe 隨 N 變窄）：

- **rail 上（平頂）**：$\dot V\approx0$ 理論上應該很敏感——但 device 此時通常**沒在導通／沒在漏雜訊**
  （$\alpha\approx0$，見 [device_noise_mapping](/06_design_insights/device_noise_mapping)），所以 effective ISF 仍小。
- **transition 上**：$\dot V$ 最大→裸 $\Gamma$ 小；但 device 正全力切換、雜訊最大（$\alpha$ 大）。
- 兩者乘起來：ring 的 effective ISF $\Gamma_{eff}=\Gamma\cdot\alpha$ 能量集中在 transition。

**快 transition（陡邊緣）為什麼好**，有兩個互相加強的理由：

1. **縮短危險視窗**：transition 越快，device「全開、邊緣穿越」的時間視窗越窄，noise 被
   收集進相位的「曝光時間」越短 → $\Gamma_{rms}$ 下降（ring 的 $\Gamma_{rms}\propto N^{-3/4}$ 趨勢也與
   每級 transition 變陡有關，見 [lc_vs_ring](/06_design_insights/lc_vs_ring)）。
2. **提高 threshold-crossing 抗擾**：邊緣越陡，$\Delta t=\Delta V/\dot V$ 越小——同樣電壓 noise
   造成的 timing 抖動越小。這是 SerDes data path 上「快 slew rate → 小 jitter」的同一條道理
   （見 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)）。

## 數值例子（建立手感）

> 用 canonical 數值估「同一坨 $\Delta q$ 在 peak vs ZC 的相位差」。

取 $q_{max}=1$ pC、$\Delta q=1$ fC、$f_0=5$ GHz。理想 LC $\Gamma(\theta)=-\sin\theta$：

- **在 ZC**（$\theta=\pi/2$，$\Gamma=-1$，最大敏感）：

$$
\Delta\phi=\frac{|\Gamma|\,\Delta q}{q_{max}}=\frac{1\times10^{-15}}{10^{-12}}=10^{-3}\ \text{rad}\;\Rightarrow\;\Delta t=\frac{10^{-3}}{2\pi\cdot5\times10^9}=31.8\ \text{fs}.
$$

- **在波峰**（$\theta=0$，$\Gamma=0$）：$\Delta\phi=0$ rad，$\Delta t=0$（理想；真實有殘餘）。
- **在中間相位**（$\theta=\pi/6$，$\Gamma=-0.5$，即 canonical 例 A 的 $\Gamma=0.5$）：

$$
\Delta\phi=\frac{0.5\times10^{-15}}{10^{-12}}=5\times10^{-4}\ \text{rad}\;\Rightarrow\;\Delta t=15.9\ \text{fs}.
$$

- **手感**：同一坨 1 fC，在 ZC 造成 ~32 fs、在波峰造成 ~0 fs。**位置（相位）比大小更重要**——
  這就是為什麼 layout 時要避免讓大 noise 源（如尾電流源切換、supply ripple）耦合到「斜率小」的相位窗口。

## 把斜率轉成 design knobs（清單）

| Knob | 怎麼做 | 機制 | 代價／註記 |
|---|---|---|---|
| 提高 transition slew rate | 加大 delay cell 驅動、降負載電容 | 縮短危險視窗、降 $\Gamma_{rms}$、降 threshold jitter | 更大電流→功耗↑ |
| 把大 noise 源挪離敏感相位 | 尾電流切換、charge injection 對準波峰/低 $\alpha$ 窗口 | 在 $\vert \Gamma_{eff}\vert $ 小的相位注入 | 需要 timing 規劃 |
| 加大 swing（提高 $\dot V$） | 大 tank swing（LC）、full-rail（ring） | 高斜率→低 threshold 敏感度，同時提 $q_{max}$ | 受 headroom 限制（見 [tank_swing](/06_design_insights/tank_swing)） |
| 避免波形「平頂」期間 device 仍導通 | 讓 device 在低 $\Gamma$ 相位才導通 | cyclostationary $\alpha$ 與 $\Gamma$ 錯開 | 需 effective ISF 分析 |

## 適用與失效條件

| 條件 | 成立時 | 失效時 |
|---|---|---|
| 小擾動、線性投影 | $\Gamma\propto1/\dot V$ 近似有效 | 強非線性、大注入時 ISF 自身會變 |
| 斜率不為 0 | $\Delta t=\Delta V/\dot V$ 有定義 | 純波峰（$\dot V=0$）要用 $\Gamma=0$ 的極限（純振幅） |
| 振幅擾動會衰減 | 可只追蹤相位 | 高 AM–PM 時波峰注入也會殘留相位 |

## Worked examples 數值例題

以下兩題把「同一坨 $\Delta q$、注入在 slope 大／小處，$\Delta\phi$ 差多少」用具體 $\Gamma$ 值算清楚，
沿用 canonical $q_{max}=1$ pC、$\Delta q=1$ fC、$f_0=5$ GHz、理想 LC $\Gamma(\theta)=-\sin\theta$。

> **例 1（slope 大處 vs slope 小處，同一 $\Delta q$ 的 $\Delta\phi$ 比值）**
> 在 ZC（$\theta=\pi/2$，slope 最大，$|\Gamma|=1$）與在「靠近波峰」（$\theta=\pi/6=30^\circ$，slope 小，
> $|\Gamma|=\sin(\pi/6)=0.5$）各注入同一坨 $\Delta q=1$ fC。求兩處 $\Delta\phi$ 與其比值。

**逐步代入（帶單位）**，用 $\Delta\phi=\dfrac{|\Gamma|\,\Delta q}{q_{max}}$：

$$
\begin{aligned}
\Delta\phi_{ZC}&=\frac{|{-}\sin(\pi/2)|\cdot\Delta q}{q_{max}}=\frac{1\times(1\times10^{-15}\,\text{C})}{1\times10^{-12}\,\text{C}}=1\times10^{-3}\ \text{rad}, \\[4pt]
\Delta\phi_{30^\circ}&=\frac{|{-}\sin(\pi/6)|\cdot\Delta q}{q_{max}}=\frac{0.5\times10^{-15}}{10^{-12}}=5\times10^{-4}\ \text{rad}, \\[4pt]
\frac{\Delta\phi_{ZC}}{\Delta\phi_{30^\circ}}&=\frac{|\Gamma(\pi/2)|}{|\Gamma(\pi/6)|}=\frac{1}{0.5}=2.
\end{aligned}
$$

- **結果**：slope 大處（ZC）的相位偏移是 slope 小處（$30^\circ$）的 **2 倍**——因為 $\Gamma$ 值正好相差 2 倍。
  注意這裡 ZC 是 $|\Gamma|$ 最大、最危險的相位。
- **Dimension check**：$\dfrac{[\text{無因次}]\cdot[\text{C}]}{[\text{C}]}=[\text{rad}]$（無因次）✓；比值無因次 ✓。
- **一行 Python 驗證**：

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
g_zc = abs(gamma_lc_ideal(np.pi/2));  g_30 = abs(gamma_lc_ideal(np.pi/6))
d_zc = impulse_to_phase_step(1e-15, g_zc, 1e-12)
d_30 = impulse_to_phase_step(1e-15, g_30, 1e-12)
print(d_zc, d_30, d_zc/d_30)   # -> 0.001  0.0005  2.0
```

> **例 2（波峰幾乎免疫 + 換成 timing error 看手感）**
> 同一坨 $\Delta q=1$ fC 注入在「正波峰」（$\theta=0$，slope $=0$，$\Gamma=0$）。求 $\Delta\phi$ 與 $\Delta t$；
> 再和例 1 的 ZC 注入比，換成 $f_0=5$ GHz 的時間誤差。

**逐步代入（帶單位）**：

$$
\begin{aligned}
\Delta\phi_{peak}&=\frac{|{-}\sin 0|\cdot\Delta q}{q_{max}}=\frac{0\times10^{-15}}{10^{-12}}=0\ \text{rad}\;\Rightarrow\;\Delta t_{peak}=0\ \text{s}, \\[4pt]
\Delta t_{ZC}&=\frac{\Delta\phi_{ZC}}{2\pi f_0}=\frac{1\times10^{-3}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}
=\frac{10^{-3}}{3.1416\times10^{10}}\ \text{s}\approx3.18\times10^{-14}\ \text{s}=31.8\ \text{fs}.
\end{aligned}
$$

- **結果**：理想波峰注入 → $\Delta\phi=0$、$\Delta t=0$（純振幅擾動，被 amplitude restoration 拉回）；
  同樣大小的電荷在 ZC 注入 → 31.8 fs。**位置（相位）比大小更重要**：差別不是幾個 %，而是 0 對 32 fs。
- **Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓（$2\pi f_0$ 是 rad/s）。
- **一行 Python 驗證**：

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error
for th in (0.0, np.pi/2):
    dphi = impulse_to_phase_step(1e-15, abs(gamma_lc_ideal(th)), 1e-12)
    print(f"theta={th:.3f}: dphi={dphi:.1e} rad, dt={phase_to_time_error(dphi,5e9)*1e15:.1f} fs")
# theta=0.000: dphi=0.0e+00 rad, dt=0.0 fs ; theta=1.571: dphi=1.0e-03 rad, dt=31.8 fs
```

> 兩題皆 **pedagogical toy（理想 LC $-\sin$，非 transistor-level）**：真實波峰有殘餘 AM–PM，$\Delta t$ 不會嚴格為 0。

## 重點回顧

- ISF 大小大致**反比於波形斜率**：斜率小（波峰）→$|\Gamma|$ 大、危險；斜率大（ZC）→$|\Gamma|$ 小、安全。
- 理想 LC：$\Gamma=-\sin\theta$，波峰 $\Gamma=0$、ZC $|\Gamma|$ 最大（見圖）。
- 快 transition 兩重好處：縮短「危險視窗」降 $\Gamma_{rms}$、提高 threshold-crossing 抗擾降 timing jitter。
- 同一坨 1 fC：ZC 注入 ~32 fs、波峰注入 ~0 fs（5 GHz, $q_{max}=1$ pC）——**位置比大小更重要**。
- ring 的 effective ISF 集中在 transition；要把大 noise 源挪離 $|\Gamma_{eff}|$ 大的相位。

## 延伸閱讀

- impulse→phase 完整推導：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)
- LTV（為何同 impulse、不同相位、不同效果）：[lti_vs_ltv](/02_foundations/lti_vs_ltv)
- 對稱性與 $c_0$：[symmetry](/06_design_insights/symmetry)
- swing 與 $q_{max}$：[tank_swing](/06_design_insights/tank_swing)
- cyclostationary $\alpha$：[device_noise_mapping](/06_design_insights/device_noise_mapping)
