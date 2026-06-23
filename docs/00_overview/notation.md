---
title: 統一符號表 Notation
description: 全站一致的符號、單位、與各論文之間的符號對照。
---

# 統一符號表 Notation

不同論文用不同符號寫同一件事，這頁把它們**統一**，往後所有章節都照這張表。
若你在某篇論文看到不同寫法，回到這裡對照即可。

> **怎麼用這頁**：先掃一遍混個臉熟；真正讀推導時，遇到不懂的符號回來查。
> 每個量都標了**單位**——做 dimension check（因次檢查）是抓錯最快的方法。

## 主要符號

| Symbol | Meaning（中文直覺） | Unit | Used in | Notes |
|---|---|---|---|---|
| $t$ | 時間 | s | all | — |
| $\tau$ | noise／impulse 的「注入時刻」 | s | [P1] | ISF 的自變數是注入相位 $\omega_0\tau$ |
| $T$ | 振盪週期 $T=1/f_0$ | s | all | — |
| $\omega_0$ | 振盪角頻率 $=2\pi f_0$ | rad/s | all | — |
| $f_0$ | 振盪頻率（carrier） | Hz | all | 例：5 GHz |
| $\phi(t)$ | excess phase（多餘相位，理想相位之外的偏差） | rad | [P1][P2] | phase noise／jitter 就住在這裡 |
| $\Delta\phi$ | 相位步階／相位誤差 | rad | all | 一次 impulse 造成的跳變 |
| $A(t)$ | 瞬時振幅 | V 或 normalized | [P1][P4] | 擾動會被拉回（見 [P4] APF） |
| $\Gamma(\omega_0\tau)$ | **ISF**，振盪器對 noise 的「相位敏感度」，無因次、$2\pi$ 週期 | — | [P1] | 不是 noise 本身，是權重函數 |
| $q_{max}$ | 節點最大電荷擺幅 $=C\cdot V_{max}$ | C | [P1] | normalize 用；越大 phase noise 越低 |
| $\Delta q$ | 注入電荷 $=\int i\,dt$ | C | [P1] | 例：1 fC |
| $i_n(t)$ | noise 電流 | A | [P1][P2] | 注入到節點的雜訊源 |
| $\overline{i_n^2}/\Delta f$ | 電流 noise 功率譜密度（單邊） | A²/Hz | [P1] | white：與頻率無關 |
| $S_i(f)$ | 電流 noise PSD | A²/Hz | all | 同上的另一寫法 |
| $S_\phi(f)$ | phase PSD（單邊） | rad²/Hz | all | 對 $f$ 積分得 $\sigma_\phi^2$ |
| $\mathcal{L}(\Delta f)$ | SSB phase noise（單邊帶相位雜訊） | dBc/Hz | all | $\approx\frac12 S_\phi$ |
| $\Delta f,\ \Delta\omega$ | offset 頻率（離 carrier 多遠） | Hz, rad/s | all | $\Delta\omega=2\pi\Delta f$ |
| $c_0$ | ISF 的 DC 傅立葉係數（DC 值 $=c_0/2$） | — | [P1] | 控制 1/f upconversion 的關鍵 |
| $c_n,\ \theta_n$ | ISF 第 $n$ 諧波的幅度／相位 | — | [P1] | 把 $n\omega_0$ 附近 noise 搬到 carrier |
| $\Gamma_{rms}$ | ISF 的 rms 值 | — | [P1][P2] | 決定 1/f² phase noise 大小 |
| $\Gamma_{eff}$ | effective ISF（含 cyclostationary） | — | [P1] | $\Gamma_{eff}=\Gamma\cdot\alpha$ |
| $\alpha(\omega_0 t)$ | noise-modulating function（NMF），device 何時在「漏雜訊」 | — | [P1] | $0\le\alpha\le1$，週期 |
| $\sigma_t$ | rms timing jitter | s | [P2] | SerDes 最在意這個 |
| $\sigma_\phi$ | rms phase | rad | all | $\sigma_t=\sigma_\phi/(2\pi f_0)$ |
| $\kappa$ | ring 累積 jitter 比例常數 | $\sqrt{\mathrm{s}}$ | [P2] | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ |
| $\omega_{1/f}$ | device 的 1/f noise corner | rad/s | [P1] | 注意：≠ phase noise 的 1/f³ corner |
| $N$ | ring oscillator 級數 | — | [P2] | $\Gamma_{rms}\propto N^{-3/4}$ |
| $Q$ | tank 品質因子 | — | [P1] | 出現在 Leeson 對照 |
| $\eta$ | ring 頻率／FOM 的比例常數 | — | [P2] | $f_0=1/(2N\tau_D)$ |

## jitter 的四種「方言」

很多人把 jitter 混為一談，其實量到的是不同東西：

| 名稱 | 定義 | 直覺 |
|---|---|---|
| **period jitter** | $T_k-T$（單一週期相對 nominal） | 這一拍多長／多短 |
| **cycle-to-cycle jitter** | $T_{k+1}-T_k$（相鄰兩拍差） | 拍與拍之間變化多快 |
| **accumulated / long-term jitter** | 相隔 $\Delta t$ 的兩 edge 誤差，$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ | 開環振盪器越跑越偏 |
| **random jitter (RJ)** | 高斯、無上界，用 $\sigma$ 描述 | SerDes BER 用它估 eye 閉合 |

詳見 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) 與
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

## 各論文符號對照（需要統一之處）

| 概念 | 本站符號 | 各論文寫法／備註 |
|---|---|---|
| ISF | $\Gamma(\omega_0\tau)$ | [P1][P2] 用 $\Gamma$；有些後續文獻用 $h$ 或 ISF |
| 最大電荷 | $q_{max}$ | [P1] $q_{max}=C_{node}V_{max}$；ring 中對應每級節點電荷 |
| offset 頻率 | $\Delta\omega$ 或 $\Delta f$ | [P1] 多用 $\Delta\omega$；datasheet 用 $\Delta f$（Hz） |
| 相位敏感度的振幅版 | （見 [P4]）APF $\tilde\Lambda$ | [P4] amplitude perturbation function；ideal LC 基波 $\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\angle0°$，與 ISF quadrature；$\tau_0=2Q/\omega_0$ |
| 有單位的 ISF | $\tilde\Gamma=\Gamma/q_{max}$ | [P3] Eq.(26)：Hong 用有單位版本（rad/C）；本站核心用無因次 $\Gamma$ |
| 相位方程（injection） | 廣義 Adler | [P3] Eq.(30),(33)：$\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$，$\Omega=\langle\tilde\Gamma\,i_{inj}\rangle$ |
| PPV / adjoint / Floquet | — | **不在這 5 篇 PDF**；屬 Demir 等外部文獻，見 [effective_isf](/03_isf_core_theory/effective_isf) |

> **符號陷阱**：$c_0$ 是傅立葉「係數」，而 ISF 的 DC**值**是 $c_0/2$（見 Eq.(12)）。
> 這個 factor 在算 1/f³ corner（Eq.(24)）時很容易出錯，後面章節會反覆提醒。
