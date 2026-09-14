---
title: "[P2] Jitter and Phase Noise in Ring Oscillators"
description: Hajimiri–Limotyrakis–Lee 1999 精讀：accumulated jitter、Γrms∝N^(-3/2)、N-independence（已核實）、symmetry 與 Fig.17。
---

# Jitter and Phase Noise in Ring Oscillators

> **先備知識（建議先讀）**：先把 [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)（ISF、$\Gamma_{rms}^2/q_{max}^2$、symmetry 法則）讀懂——本頁所有結論都是 [P1] 的 ISF 套到 ring。jitter 的時域／頻域語言見 [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)。

[P2] 把 [P1] 的 ISF 框架**套到 ring oscillator（環形振盪器）**。它回答三個非常實際的問題：
（1）自由振盪的 ring 的 long-term jitter 怎麼隨時間長大？（2）級數 $N$ 對 phase noise 有什麼
影響？（3）為什麼波形對稱性能壓低 close-in noise？答案分別是 $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$、
$\Gamma_{rms}\propto N^{-3/2}$（與「固定功率與頻率下幾乎與 $N$ 無關」），以及 Fig. 17 的對稱性實驗。

## Citation

> **[P2]** A. Hajimiri, S. Limotyrakis, and T. H. Lee, *"Jitter and Phase Noise in Ring
> Oscillators,"* IEEE J. Solid-State Circuits, vol. 34, no. 6, pp. 790–804, Jun. 1999.
> （檔案 `jitter_ring.pdf`，paper_002）

## One-sentence contribution

把 [P1] 的 ISF 用到 ring oscillator，得到 jitter 與 phase noise 的封閉式、
$\Gamma_{rms}\propto N^{-3/2}$ 的 scaling、以及「固定 $f_0$ 與功率時 single-ended ring 的
phase noise／jitter 幾乎與級數 $N$ 無關」這個反直覺結論（claim C7, C8）。

## Why this paper matters

LC 振盪器要電感，面積大、不好整合；**ring oscillator 全用反相器、面積小、好整合、調頻範圍寬**，
是 PLL／CDR 裡最常見的 VCO。但 ring 的 phase noise 通常比 LC 差很多——[P2] 用 ISF 解釋
**為什麼**，並給出可操作的設計法則：

- 它把 ring 的 jitter 連到**和 phase noise 同一個 $\Gamma_{rms}^2/q_{max}^2$ 比例**（claim C6），
  讓「時域 jitter」與「頻域 phase noise」在 ISF 框架下統一。
- 它澄清一個常被誤解的問題：「ring 級數 $N$ 加多會不會比較好？」答案在固定功率與頻率的約束下
  是「**幾乎沒差**」（claim C7）——多了級數、$\Gamma_{rms}$ 變小，但每級擺幅也變小、device 變多，
  彼此抵消。
- 它用實測（Fig. 17）證實 [P1] 的 symmetry 法則：把控制電壓調到讓上升／下降對稱的點，phase
  noise 出現**極小值**（claim C4）。

## Main assumptions

照 paper_metadata（paper_002.assumptions）：

1. 與 [P1] 相同的 LTV／ISF 小擾動假設。
2. 每級 device noise 為白噪（加上用 symmetry 處理的 1/f 成分）。
3. 各級相同；延遲與 noise 在每次 transition 獨立相加。

> **物理直覺**：ring 的能量幾乎全集中在 transition（邊緣翻轉）那一瞬間注入，所以它的 ISF
> 不像 LC 的平滑 $-\sin$，而是**集中在 transition 的尖峰**（[P2] Fig. 5）。哪裡敏感、哪裡踢
> 一下最傷相位，就在那些尖峰上。級數越多、單一 transition 佔整個週期的比例越小，rms ISF 越小。

## Key equations

### Eq.(8)：accumulated jitter（隨機漫步指紋）

**Original formula**（[P2] Eq.(8), p.792；κ 由 Eq.(12), p.793）：

$$
\sigma_{\Delta t}=\kappa\sqrt{\Delta t}
$$

**Meaning**：自由振盪器相隔 $\Delta t$ 的兩個邊緣，其時間誤差的標準差**正比於
$\sqrt{\Delta t}$**——這是「沒有絕對時間參考」的振盪器的**隨機漫步（random walk）指紋**
（claim C6）。$\kappa$ 是每顆 device 的比例常數，單位 $\sqrt{\text{s}}$。

**Step-by-step derivation**：每次 transition 注入一筆獨立、零均值、變異數 $\sigma_{step}^2$
的時間擾動。經過 $\Delta t$ 共約 $M=\Delta t/T$ 次 transition，獨立量相加變異數相加：

$$
\begin{aligned}
\sigma_{\Delta t}^2 &= M\,\sigma_{step}^2 = \frac{\Delta t}{T}\,\sigma_{step}^2 \\
\Rightarrow\quad \sigma_{\Delta t} &= \underbrace{\frac{\sigma_{step}}{\sqrt{T}}}_{\equiv\,\kappa}\sqrt{\Delta t}=\kappa\sqrt{\Delta t}.
\end{aligned}
$$

**Dimension check**：$\kappa$ 是 $\sqrt{\text{s}}$，$\sqrt{\Delta t}$ 是 $\sqrt{\text{s}}$，
相乘得 $\text{s}$ ✓。對照 [P1] 的頻域：$\sigma_{\Delta t}\propto\sqrt{\Delta t}$ 對應頻域的
1/f² phase noise（兩者是同一件事的時域／頻域兩面）。

**Numerical example**：toy ring 設 per-edge $\sigma_{step}=50$ fs（見
`ring_oscillator_timing_noise_accumulation.png` 參數）。隔 $\Delta t=1$ µs（$f_0=5$ GHz
下約 5000 個週期）的累積 jitter：先求 $\kappa$。若 $T=200$ ps，
$\kappa=50\text{fs}/\sqrt{200\text{ps}}=50\times10^{-15}/\sqrt{2\times10^{-10}}=3.54\times10^{-9}\ \sqrt{\text{s}}$，
故 $\sigma_{\Delta t}=3.54\times10^{-9}\times\sqrt{10^{-6}}=3.54\ \text{ps}$。手感：隔越久、偏越多，但只以 $\sqrt{\Delta t}$ 慢慢長。

**Python verification**：

```python
import numpy as np
from simulations.common.oscillator_models import accumulated_jitter_curve

# toy 隨機漫步：每個 edge 加一筆 50 fs 的獨立 timing 擾動
lags, sigma = accumulated_jitter_curve(f0=5e9, sigma_edge=50e-15, max_lag_periods=500, n_trials=2000)
# 期望 sigma(lag) ~ sigma_edge * sqrt(lag) -> log-log 斜率 0.5
slope = np.polyfit(np.log(lags[1:]), np.log(sigma[1:]), 1)[0]
print(round(slope, 2))  # -> 0.50
```

完整 toy 推導在 [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
（**pedagogical toy model，非 transistor-level**）。

### Eq.(11)–(12)：jitter 常數 κ 與 ISF 的關係（已核實 ✓）

**Original formula**（[P2] Eq.(11)–(12), p.793，比例關係）：

$$
\kappa^2\;\propto\;\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}
$$

**Meaning**：jitter 比例常數 $\kappa$ 由**和 phase noise 一模一樣的 $\Gamma_{rms}^2/q_{max}^2$
比例**決定（claim C6）。這把時域 jitter 與頻域 phase noise 綁在同一個 ISF 量上：壓低 phase
noise 的旋鈕同時壓低 jitter。

> **已核實（v11 重看 PDF 更正）**：[P2] Eq.(12), p.793 印刷式為 $\kappa=\dfrac{\Gamma_{rms}}{q_{max}\,\omega_0}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$——分母**含 $\omega_0$**，單位 $\sqrt{\text{s}}$，是 Eq.(8) $\sigma_{\Delta T}=\kappa\sqrt{\Delta T}$ 的**時間版** jitter 常數 $\kappa_t$（由 Eq.(10) $\sigma_{\Delta\phi}=\omega_0\sigma_{\Delta T}$ 與 Eq.(11) $\sigma_{\Delta\phi}^2=\Gamma_{rms}^2(\overline{i_n^2}/\Delta f)\,\Delta T/(2q_{max}^2)$ 合成；對照原始 PDF 渲染逐字確認）。本站 [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) 的 $\kappa_\phi=\dfrac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$（rad/$\sqrt{\text{s}}$）是同一件事的**相位版**：$\kappa_\phi=\omega_0\kappa_t$，數值上 $\kappa_t=\kappa_\phi/(2\pi f_0)$。v4–v5 曾把「Eq.(12) 無 $\omega_0$」當作已核實，v11 更正；本站所有數字不變。
> 兩版都與 phase noise 共用同一個 $\Gamma_{rms}^2/q_{max}^2$ 比例（claim C6）。

### Eq.(14)：ring 頻率與級數

**Original formula**（[P2] Eq.(14), p.794）：

$$
f_0=\frac{1}{2N\tau_D}
$$

**Meaning**：$N$ 級、每級延遲 $\tau_D$ 的 ring，振盪頻率為此式。**因子 2** 來自訊號每個週期
要繞 ring **兩圈**（一圈反相、再一圈才回到同相）才完成一個完整週期。

**Dimension check**：$1/(N\cdot\text{s})=\text{Hz}$ ✓（$N$ 無因次）。

**Numerical example**：要做 $f_0=5$ GHz 的 5 級 ring，每級延遲
$\tau_D=1/(2\times5\times5\times10^9)=2\times10^{-11}\ \text{s}=20$ ps。級數加倍到 $N=10$
又要維持 5 GHz，每級延遲就得砍半到 10 ps——這正是「固定頻率時 $N$↑ 必須讓每級更快、擺幅更
小」的由來，連到下面的 N-independence。

### Eq.(16)：rms ISF 隨級數的 scaling（v7 已重核 ✓）

**Original formula**（[P2] Eq.(16), p.794，根號只蓋常數項）：

$$
\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}}\;\dfrac{1}{N^{1.5}}
$$

其中 $\eta$ 是頻率比例常數（Eq.(14)–(15)：$\hat t_D=\eta/f_{max}$、$2\pi=2N\eta/f_{max}$）；
$\eta=0.75$ 時 $\sqrt{2\pi^2/(3\times0.75^3)}\approx3.95\approx4$，即 $\Gamma_{rms}\approx4/N^{1.5}$，
就是 [P2] Fig. 8 的實線——根號只含常數，$1/N^{1.5}$ 在根號外。

**Meaning**：**$\Gamma_{rms}\propto N^{-3/2}$**（即 $\Gamma_{rms}^2\propto N^{-3}$）。
直覺：級數越多，每個 transition 在 $2\pi$ 週期裡佔的「敏感時間窗」越窄、尖峰越矮，rms 自然變小。

> **[P2] Eq.(16), p.794（v7 已重核：根號只蓋常數，$\Gamma_{rms}\propto N^{-3/2}$；正文
> $4/N^{1.5}$@$\eta=0.75$ 與 App.B Eq.(55) 三重驗證。v3 曾誤讀為 $N^{-3/4}$）**：
> 三重證據——(1) 正文（p.794，Eq.16 下一段）明寫「the $1/N^{1.5}$ dependence of $\Gamma_{rms}$」；
> (2) $\eta=0.75$ 數值錨：正文「solid line = $\Gamma_{rms}\approx4/N^{1.5}$, obtained from (16)
> for $\eta=0.75$」，且 $\sqrt{2\pi^2/(3\times0.75^3)}=3.95\approx4$ ✓（若 $N^{1.5}$ 在根號內
> 會得 $4/N^{0.75}$，與正文矛盾）；(3) App.B Eq.(52)+(54)（p.803）獨立代數：
> $\Gamma_{rms}^2=(1/3\pi)(1/f'_{rise})^3(1+A^3)$、$2\pi=\eta N(1+A)/f'_{rise}$，
> 代入整理得 $\Gamma_{rms}^2=(2\pi^2/3\eta^3)\cdot[4(1+A^3)/(1+A)^3]\cdot N^{-3}$；$A=1$ 時中括號
> 為 1，故 $\Gamma_{rms}^2\propto N^{-3}\Rightarrow\Gamma_{rms}\propto N^{-3/2}$ ✓。三者一致指向
> $N^{-3/2}$；並無「公式 vs 文字」不一致——是先前對根號範圍的誤讀。

### Eq.(23)：ring 白噪 phase noise FOM 與 N-independence（前置係數已更正為 8/(3η) 並核實）

**Original formula**（[P2] Eq.(23), p.796；$V_T=0$ 的下限為 Eq.(25)）：

$$
\mathcal{L}\{\Delta f\}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{V_{char}}\cdot\left(\frac{f_0}{\Delta f}\right)^2
\qquad\Big(\min_{V_T=0}:\ \frac{16\gamma}{3\eta}\cdot\frac{kT}{P}\cdot\frac{f_0^2}{\Delta f^2}\Big)
$$

其中 $\gamma$ 是 MOSFET 通道熱雜訊係數（長通道 $2/3$，短通道更大）、$V_{char}$ 是元件的
**characteristic voltage**（長通道 $\approx\Delta V/\gamma$），$P$ 是功率耗散（Eq.(21)：$P=2\eta N V_{DD}q_{max}f_0$），
每級雜訊由 Eq.(17),(18) $\overline{i_n^2}/\Delta f=4kT\gamma\mu C_{ox}(W/L)\Delta V$ 給出。

**Meaning**：ring 白噪 phase noise 收成一個 figure of merit——只看 $kT/P$、電壓比 $V_{DD}/V_{char}$
與 $(f_0/\Delta f)^2$。**關鍵結論（claim C7）：Eq.(23) 裡完全沒有 $N$——固定 $f_0$ 與功率 $P$ 時，
single-ended ring 的 phase noise 與級數 $N$ 無關。**

**為何與 $N$ 無關**：微觀上，$N$↑ 會降 $\Gamma_{rms}$（Eq.16）但同時降每級擺幅 $q_{max}$、又增加噪聲級數；
[P2] 證明這些效應在固定 $P$、$f_0$ 下剛好抵消，最後 Eq.(23) 不含 $N$。所以「ring 要不要多加級數」
不是靠 phase noise 決定，而看相位裕度、調頻範圍、面積、quadrature 需求等其他考量。

> **校訂註記（v3）**：[P2] Eq.(23) 的前置係數是 $8/(3\eta)$（$\eta$ 為級延遲比例常數 Eq.14，$\approx1$）；
> $\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入。（v2 曾誤改為 $8/(3\gamma)$ 並誤標「逐字核實」，v3 已對照原始 PDF p.796 更正。）
> $V_T=0$ 的下限亦由此修為 $16\gamma/(3\eta)$。$\gamma$（噪聲係數）與 $\eta$（頻率比例常數，Eq.14）是不同的量，勿混淆。

### Eq.(27)–(30)：短通道 velocity-saturation 電流／雜訊模型與 $V_{char}=E_cL/\gamma$（已核實 ✓）

**Original formulas**（[P2] Sec. V-A, p.796，對照原始 PDF 渲染頁逐字核實）：

短通道元件的汲極電流受 **velocity saturation（載子速度飽和，電場大到載子速度不再隨電場上升）** 支配（Eq.(27)）：

$$
I_D=\frac{\mu C_{ox}}{2}\,W\,E_c\,\Delta V
$$

其中 $E_c$ 是 **critical electric field（臨界電場）**，論文定義為「讓載子速度降到低場遷移率所預期值的一半」的電場強度。
把 Eq.(27) 併入 Eq.(17)，得短通道 MOS 的汲極電流雜訊（Eq.(28)）：

$$
\frac{\overline{i_n^2}}{\Delta f}=8kT\,\frac{\gamma I_D}{E_cL}
$$

振盪頻率（Eq.(29)，照排）：

$$
f_0=\frac{1}{2Nt_D}=\frac{1}{\eta N(t_r+t_f)}=\frac{\mu_{eff}W_{eff}C_{ox}\Delta V^2}{8\eta NLq_{max}}
$$

用 (28)、(29) 重走 Eq.(23)/(24) 的推導，論文說得到**同樣的** phase noise 與 jitter 式，只是 $V_{char}$ 換成（Eq.(30)）：

$$
V_{char}=\frac{E_cL}{\gamma}
$$

並註明結果比長通道大一個因子 $\gamma\Delta V/E_cL$（p.796），且原文逐字："Again, note the absence of any dependency on the number of stages."——**N-independence 在短通道分支不變**。

**Step-by-step derivation of Eq.(28)**（與本站由 Eq.(17) 推 Eq.(18) 同一招）：

1. Eq.(17)（p.795）：$\overline{i_n^2}/\Delta f=4kT\gamma g_{d0}=4kT\gamma\,\mu C_{ox}(W/L)\Delta V$。原文明說此式長、短通道皆適用，只要 $\gamma$ 取對（長通道 $2/3$，短通道「typically two to three times greater」）。
2. 由 Eq.(27) 解出 $\mu C_{ox}W\Delta V=2I_D/E_c$。
3. 代入：

$$
\frac{\overline{i_n^2}}{\Delta f}=4kT\gamma\cdot\frac{1}{L}\cdot\underbrace{\mu C_{ox}W\Delta V}_{=\,2I_D/E_c}=\frac{8kT\gamma I_D}{E_cL}\quad\checkmark
$$

**Dimension check**：$kT$ 是 J $=$ V·A·s，$I_D$ 是 A，$E_cL$ 是 (V/m)·m $=$ V；故 $8kT\gamma I_D/(E_cL)=$ V·A·s·A/V $=$ A²·s $=$ A²/Hz ✓。

**物理意義**：長通道時 $g_{d0}\propto(W/L)\Delta V$，雜訊隨 overdrive 線性升；速度飽和後電流只剩 $\Delta V$ 的一次方（Eq.(27)），等效 $g_{d0}=2I_D/(E_cL)$——雜訊**直接正比於電流、反比於 $E_cL$**。$E_cL$ 是一個「電壓」：載子在通道長 $L$ 上被推到飽和速度所需的電壓尺度；0.25 µm 製程取 $E_c\approx4\times10^6$ V/m 得 $E_cL=1.0$ V（[P2] p.799 對編號 3 振盪器用的數字）。

**Step-by-step derivation of Eq.(30)**（本站補推，順便看 $N$ 為何仍消掉）：

1. $N$ 個相同雜訊源、各注入一節點，總 phase noise 是 Eq.(6) 的 $N$ 倍；代 Eq.(16) 的 $\Gamma_{rms}^2=2\pi^2/(3\eta^3N^3)$ 與 Eq.(28)：

$$
\mathcal{L}\{\Delta f\}=N\cdot\frac{2\pi^2}{3\eta^3N^3}\cdot\frac{1}{8\pi^2\Delta f^2}\cdot\frac{8kT\gamma I_D/(E_cL)}{q_{max}^2}=\frac{2kT\gamma\,I_D}{3\eta^3N^2\,E_cL\,\Delta f^2\,q_{max}^2}
$$

> **慣例旗標**：[P2] Eq.(6)（p.792，逐字核實）的分母是 $8\pi^2f_{off}^2=2\Delta\omega^2$，即本站 [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) 的 $\mathcal{L}_{/2}=\kappa^2/\Delta\omega^2$ 家族——比 [P1] Eq.(21) 分母的 $4\Delta\omega^2$（$\mathcal{L}_{/4}$）**高 3 dB**。本節與下方「Measured validation」全部照 Eq.(6) 印刷式記帳，所以能與論文數字逐位吻合；若改用 [P1] Eq.(21)，每個絕對值都要 $-3$ dB，但所有 scaling 與 $N$-independence 不變。

2. **級延遲**：transition 期間由 $I_D$ 把節點充到 $q_{max}$，$t_r\approx t_f\approx q_{max}/I_D$，故 $f_0=1/(\eta N(t_r+t_f))\approx I_D/(2\eta Nq_{max})$——這是 Eq.(32)（差動，$I_{tail}$ 充電）的 single-ended 孿生式；解出 $I_D=2\eta Nq_{max}f_0$。
3. **功率**：Eq.(21) $P=2\eta NV_{DD}q_{max}f_0\Rightarrow q_{max}=P/(2\eta NV_{DD}f_0)$。
4. 代回步驟 1（先代 $I_D$、再代 $q_{max}$）：

$$
\mathcal{L}\{\Delta f\}=\frac{2kT\gamma\cdot2\eta Nq_{max}f_0}{3\eta^3N^2E_cL\Delta f^2q_{max}^2}=\frac{4kT\gamma f_0}{3\eta^2N\,E_cL\,\Delta f^2\,q_{max}}=\frac{4kT\gamma f_0\cdot2\eta NV_{DD}f_0}{3\eta^2N\,E_cL\,\Delta f^2\,P}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{E_cL/\gamma}\cdot\frac{f_0^2}{\Delta f^2}
$$

正是 Eq.(23) 配上 $V_{char}=E_cL/\gamma$（Eq.(30)）✓。**指數記帳**（固定 $P$、$f_0$）：$q_{max}\propto1/N$，而 $I_D=2\eta Nq_{max}f_0=P/V_{DD}$ 與 $N$ 無關；故 $N^{+1}\cdot N^{-3}\cdot N^{0}\cdot N^{+2}=N^0$（分別來自雜訊源數、$\Gamma_{rms}^2$、$S_i\propto I_D$、$1/q_{max}^2$）——與長通道分支完全相同的相消。

> **關於 Eq.(29) 的照排註記（本站判讀，待查證）**：p.796 印出的 Eq.(29) 末項與 Eq.(22)（p.795）**逐字相同**（$\mu_{eff}W_{eff}C_{ox}\Delta V^2/(8\eta NLq_{max})$，仍含 $\Delta V^2/L$）；若真的把這個末項連同 Eq.(28) 一起代入，前置係數會變成 $16/(3\eta)$ 而不是 Eq.(23) 印的 $8/(3\eta)$，也推不出 Eq.(30)。本站的推導只用 Eq.(29) 的前兩個等號（$f_0=1/(\eta N(t_r+t_f))$）加上 $t_r\approx q_{max}/I_D$，這條路同時重現印刷版 Eq.(23) 的 $8/(3\eta)$、Eq.(30) 的 $E_cL/\gamma$，以及 Table I 對編號 3 的 Pred.(23)（見下方）。把 Eq.(27) 代進去，短通道頻率應讀作 $f_0\approx\mu_{eff}W_{eff}C_{ox}E_c\Delta V/(4\eta Nq_{max})$（不含 $L$、$\Delta V$ 只有一次方）。無論取哪個寫法，只要 $I_D$ 用 Eq.(27)，$N$ 都消掉、Eq.(30) 不變。

**Numerical example（用論文編號 3 振盪器的數字，p.799）**：$E_c=4\times10^6$ V/m、$\gamma=2.5$、$L=0.25$ µm、transition 中點模擬電流 $I_D=3.47$ mA、$kT$ 取 $300$ K：

- Eq.(28)：$8\times4.14\times10^{-21}\times2.5\times3.47\times10^{-3}/(4\times10^6\times0.25\times10^{-6})=2.87\times10^{-22}$ A²/Hz（論文印 $2.87\times10^{-22}$ ✓）。
- Eq.(30)：$V_{char}=E_cL/\gamma=1.0/2.5=0.4$ V。
- **長／短通道劣化倍率**：論文只給因子 $\gamma\Delta V/E_cL$。若長通道取 $V_{char}=\Delta V/\gamma$ 且兩邊用同一個 $\gamma$，代數上比值是 $(\Delta V/\gamma)/(E_cL/\gamma)=\Delta V/(E_cL)$，沒有 $\gamma$；印刷因子裡多出的那個 $\gamma$ 本站讀作 $\gamma_S/\gamma_L$ 之比（待查證）——p.795 明說短通道 $\gamma$「typically two to three times greater」，實務上的差別主要來自 $\gamma$ 本身。取 $\Delta V=V_{DD}/2-V_T$、**假設** $V_T=0.5$ V（論文未印該 0.25 µm 製程的 $V_T$，待查證）得 $\Delta V=0.75$ V：長通道 $V_{char}=\Delta V/\gamma_L=0.75/(2/3)=1.125$ V、短通道 $0.4$ V，比值 $2.81$，即 **$+4.5$ dB**；而單看速度飽和（同 $\gamma$）比值只有 $0.75$（反而略好）——短通道真正扣分的是 $\gamma\approx2.5$ 而非 $E_c$。
- **慣例旗標**：本節沒有引入新的 2／4／SSB 因子；所有 SSB 記帳都在 Eq.(6)／(23) 裡（見上方旗標）。

**Python verification**：

```python
import numpy as np
k, T = 1.380649e-23, 300.0
kT = k*T                                   # J
Ec, L, gam_s, gam_l = 4e6, 0.25e-6, 2.5, 2/3   # [P2] p.799 numbers for oscillator #3; long-channel gamma = 2/3
ID = 3.47e-3                                # A, simulated mid-transition drain current (#3)
Si_28 = 8*kT*gam_s*ID/(Ec*L)                # [P2] Eq.(28)
Vchar_s = Ec*L/gam_s                        # [P2] Eq.(30)
print(f"{Si_28:.2e}")                       # -> 2.87e-22  A^2/Hz（論文印 2.87e-22）
print(round(Vchar_s, 3))                    # -> 0.4  V
# short vs long channel: paper prints the factor gamma*dV/(Ec*L) (p.796); the site reads it with two gammas
VT = 0.5                                    # V, ASSUMED (the paper does not print V_T for the 0.25 um process)
dV = 2.5/2 - VT                             # gate overdrive at mid-transition, [P2] p.795
Vchar_l = dV/gam_l
ratio = Vchar_l/Vchar_s                     # = (gam_s/gam_l)*dV/(Ec*L)
print(round(Vchar_l,3), round(ratio,2), round(10*np.log10(ratio),1))   # -> 1.125 2.81 4.5
print(round(dV/(Ec*L),2))                   # -> 0.75  same-gamma ratio dV/(Ec L)
# N-independence check: N x Eq.(6) with Eq.(16),(28) under P = 2*eta*N*VDD*qmax*f0 and f0 = ID/(2*eta*N*qmax)
def L_short(N, P=25e-3, f0=1.33e9, VDD=2.5, eta=0.75, df=1e6):
    qmax = P/(2*eta*N*VDD*f0); ID = 2*eta*N*qmax*f0
    G2 = 2*np.pi**2/(3*eta**3*N**3)
    Si = 8*kT*gam_s*ID/(Ec*L)
    return 10*np.log10(N*G2*Si/(8*np.pi**2*df**2*qmax**2))
Ls = [round(float(L_short(N)),2) for N in (3,5,7,11,19)]
L23 = 10*np.log10(8/(3*0.75)*kT/25e-3*2.5/Vchar_s*(1.33e9/1e6)**2)
print(Ls, round(L23,2))   # -> [-111.86, -111.86, -111.86, -111.86, -111.86] -111.86   dBc/Hz, N 從 3 到 19 完全一樣 = Eq.(23)
```

**適用與失效條件**：Eq.(27) 是完全速度飽和的一階模型（$\Delta V\gg E_cL$ 時才成立；編號 3 的 $\Delta V\approx0.75$ V 對 $E_cL=1.0$ V 其實只在過渡區，論文仍直接套用）；$\gamma$ 的值（2–3）本身是經驗數，且隨偏壓變；Eq.(28) 只算通道熱雜訊，不含閘極電阻、基板與 induced-gate noise。實測對照見下方「Measured validation」。

### Eq.(31)–(35)：差動 ring 的 phase noise——明含 $N$（已核實 ✓）

**Original formulas**（[P2] Sec. V-B, p.796，對照原始 PDF 渲染頁逐字核實）：

功率（Eq.(31)）與頻率（Eq.(32)）：

$$
P=N\,I_{tail}\,V_{DD}
\qquad\qquad
f_0=\frac{1}{2Nt_D}\approx\frac{1}{2\eta N t_r}\approx\frac{I_{tail}}{2\eta N q_{max}}
$$

每個 single-ended 節點的雜訊（Eq.(33)；差動電晶體＋負載電阻 $R_L$ 兩份，$V_{char}=(V_{GS}-V_T)/\gamma$
long-channel 平衡級、$E_cL/\gamma$ short-channel）：

$$
\frac{\overline{i_n^2}}{\Delta f}=\left(\frac{\overline{i_n^2}}{\Delta f}\right)_{N}+\left(\frac{\overline{i_n^2}}{\Delta f}\right)_{Load}=4kT\,I_{tail}\left(\frac{1}{V_{char}}+\frac{1}{R_L I_{tail}}\right)
$$

全環 $2N$ 個節點（每級兩個輸出），總 phase noise 是單源的 $2N$ 倍（p.796 原文："The phase noise
and jitter due to all $2N$ noise sources is $2N$ times the value given by (6) and (12)."——這個 2 是
**節點計數**，不是 SSB 慣例的 2）。配上 Eq.(16) 的 $\Gamma_{rms}$，收成（Eq.(34)/(35)，$\mathcal{L}$
即論文的 $L\{\Delta f\}$）：

$$
\mathcal{L}_{min}\{\Delta f\}=\frac{8}{3\eta}\cdot N\cdot\frac{kT}{P}\cdot\left(\frac{V_{DD}}{V_{char}}+\frac{V_{DD}}{R_L I_{tail}}\right)\cdot\frac{f_0^2}{\Delta f^2}
$$

$$
\kappa_{min}=\sqrt{\frac{8}{3\eta}}\cdot\sqrt{N\cdot\frac{kT}{P}\cdot\left(\frac{V_{DD}}{V_{char}}+\frac{V_{DD}}{R_L I_{tail}}\right)}
$$

原文明述兩式 "valid in both long- and short-channel regimes of operation with the right choice of
$V_{char}$"；bipolar 差動 ring 的 shot＋load noise（Eq.(36), p.797）併回**同兩式**，$V_{char}=4kT/q_e$。

**Meaning**：與 single-ended 的 Eq.(23) 只差兩處——**多了明含的 $N$**、括號多了負載那份
$V_{DD}/(R_L I_{tail})$。固定 $f_0$ 與 $P$ 下，差動 ring 的 phase noise **隨 $N$ 變差**
（$\Delta\mathcal{L}=10\log_{10}(N_2/N_1)$，jitter 則 $\kappa_{min}\propto\sqrt N$）——
N-independence 的失落另一半。

**Why the $N$ appears**（指數記帳，固定 $P$、$f_0$、固定 swing）：$P=NI_{tail}V_{DD}$ 是**靜態**
記帳（不像 Eq.(21) 綁著 $f_0$），固定 $P$ 逼 $I_{tail}\propto1/N$；Eq.(32) 再逼
$q_{max}=I_{tail}/(2\eta Nf_0)\propto1/N^2$（p.797 原文逐字："…reduce the swing, and hence
$q_{max}$, by a factor of $1/N^2$"）。於是
$2N\cdot\Gamma_{rms}^2\cdot S_i/q_{max}^2\propto N\cdot N^{-3}\cdot N^{-1}\cdot N^{4}=N^{+1}$。
完整逐項表與 worked example 見 [lc_vs_ring 第 2b 步](/06_design_insights/lc_vs_ring)。

> **[P2] 結論句（pp.796–797，逐字）**："Note that, in contrast with the single-ended ring oscillator,
> a differential oscillator does exhibit a phase noise and jitter dependency on the number of stages,
> with the phase noise degrading as the number of stages increases for a given frequency and power
> dissipation."

**Numerical example**：$f_0=5$ GHz、$\Delta f=1$ MHz、$kT=4.0\times10^{-21}$ J、$P=1$ mW、
$\eta\approx1$、$V_{DD}/V_{char}=3$、$V_{DD}/(R_LI_{tail})=2$（固定 swing）：$N=4$ 得
$-82.7$ dBc/Hz、$N=12$ 得 $-78.0$ dBc/Hz，$\Delta\mathcal{L}=10\log_{10}3=+4.77$ dB；
$\kappa_{min}$ 則 $\times\sqrt3\approx1.732$。（**慣例旗標（v11 更正）**：Eq.(34) 由 $2N\times$Eq.(6) 收成，而 [P2] Eq.(6), p.792 印刷式的分母 $8\pi^2f_{off}^2=2\Delta\omega^2$ 是本站的 $\mathcal{L}_{/2}$ 家族——比 [P1] Eq.(21) 分母 $4\Delta\omega^2$ 的 $/4$ SSB 家族**高 3 dB**。所以 $-82.7$／$-78.0$ dBc/Hz 這兩個絕對值是 **$/2$ 家族**的數字；換成 [P1] Eq.(21) 的記帳為 $-85.7$／$-81.0$ dBc/Hz。$\Delta\mathcal{L}$ 是相減，**兩種慣例相同**。）

**Python verification**：

```python
import numpy as np
def L_ring_diff(N, kT, P, f0, df, eta=1.0, vdd_vchar=3.0, vdd_swing=2.0):  # [P2] Eq.(34)
    return 10*np.log10(8/(3*eta) * N * (kT/P) * (vdd_vchar + vdd_swing) * (f0/df)**2)
L4  = L_ring_diff(4,  4.0e-21, 1e-3, 5e9, 1e6)
L12 = L_ring_diff(12, 4.0e-21, 1e-3, 5e9, 1e6)
print(round(L4,1), round(L12,1), round(L12-L4,2))   # -> -82.7 -78.0 4.77
# Eq.(34) = 2N x Eq.(6); Eq.(6) denominator 8*pi^2*f^2 = 2*dw^2 -> these are /2-family values; [P1] Eq.(21) /4 family is 3.01 dB lower
print(round(L4-10*np.log10(2),1), round(L12-10*np.log10(2),1))   # -> -85.7 -81.0
```

**設計一行話**：single-ended＝$N$-free（Eq.23）；差動＝**最少級數的贏**（Eq.34，每加倍 $+3.01$ dB）——
$N$ 由 phase margin／quadrature／多相位需求決定下限，別多加。tail 源近 $f_0$ 的雜訊「surprisingly」
不進 phase noise（p.796），進的是低頻（symmetry 路）與偶次諧波附近（可用 LC 濾）。

## Key figures

| 論文圖 | 頁 | 內容 | 本站對應 | 註 |
|---|---|---|---|---|
| Fig. 5 | 793 | 同頻、不同級數 $N$（3/5/15）的 ISF 疊圖 | scaling 直覺（$\Gamma_{rms}\propto N^{-3/2}$） | ✓ |
| Fig. 6 | 793 | single-ended ring 單級的近似波形與 ISF（能量集中在 transition） | toy 三角 ISF（lab_03） | ✓ |
| Fig. 8 | 794 | 不同級數 ring 的 rms ISF vs $N$，實線為 Eq.(16) 在 $\eta=0.75$ 時的 $\Gamma_{rms}\approx4/N^{1.5}$ | `lc_vs_ring_isf_comparison.png` 的 scaling 論證 | ✓ |
| Fig. 9 | 795 | **差動** ring 的 rms ISF vs $N$，三種約束情境（fixed power/fixed swing、fixed power/fixed $R_L$、fixed tail current/fixed $R_L$） | 差動 ring 沿用 Eq.(16) scaling 的實證（Eq.(34) 推導的前提） | ✓ |
| Fig. 12 / Tables I–III | 799–800 | 三種 ring 級電路（inverter-chain／current-starved／差動）與 26 顆實測 $\mathcal{L}(1\,\text{MHz})$ 對照 Eq.(6)/(23)/(34) | 「Measured validation」節（表格轉錄＋編號 3、12 重算） | ✓ |
| Fig. 16 | 802 | 編號 12 差動 ring 的 rms jitter vs $\Delta T$（log–log）：$\sqrt{\Delta T}$ 段擬合 $\kappa=6.18\times10^{-9}\ \sqrt{\text{s}}$，約 $10^{-8}$–$10^{-7}$ s 後轉 slope-1（$\zeta=2.5\times10^5$） | Eq.(8)/(12)/(35)/(50) 的實測閉環（Worked example 2） | ✓ |
| **Fig. 17** | 802 | phase noise vs symmetry（控制）電壓，在對稱點有**極小值** | symmetry 設計法則的直接實驗佐證 | ✓ |

**Fig. 17 是 symmetry 法則的鐵證**：把控制電壓掃過，調到 PMOS 上拉電流 = NMOS 下拉電流、
波形上下對稱的那一點，$c_0$ 被壓到最小、1/f³ 上轉被抑制，phase noise 出現一個**碗底**。這直接
驗證 [P1] Eq.(24)（claim C4）。

本站用 toy model 對照 LC（$-\sin$）與 ring（三角 ISF、峰隨 $N$ 變矮），**非 transistor-level**：

![LC 與 ring 的 ISF 對照（toy）](/figures/lc_vs_ring_isf_comparison.png)
![ring 累積 jitter 隨時間以 √Δt 長大（toy）](/figures/ring_oscillator_timing_noise_accumulation.png)

## Measured validation（Sec. VIII, pp.798–802）

[P2] 最被低估的一節：它用 **26 顆實作 ring**（三種拓樸、2 µm 5 V 與 0.25 µm 2.5 V 兩製程、115 MHz 到 5.5 GHz）
把 Eq.(6)／(23)／(34) 逐顆對照實測 $\mathcal{L}(1\,\text{MHz})$，並用 Fig. 16 對照 Eq.(8)／(12)／(35) 的 jitter。
量測系統（p.798）：HP 8563E、RDL NTS-1000A、HP E5500（phase noise）；Tektronix CSA 803A（jitter）。offset 固定 1 MHz 是為了量測動態範圍最大。
以下三張表由原始 PDF 渲染頁（pp.799–800）逐格轉錄；$W/L$ 單位 µm/µm，phase noise 單位 dBc/Hz @ 1 MHz offset。

> **誠實註記**：`extracted/raw_text/jitter_ring.txt` 的 OCR 把三張表與編號 3／12 範例的中間數字全部吃掉；本節的表格與論文印出的中間值（$2.87\times10^{-22}$、$179.5$ fC、$50.3$ fC、$4.14\times10^{-23}$、$8.28\times10^{-24}$、$4.97\times10^{-23}$、$-113.0$、$-95.5$、$-95.4$）皆改由渲染頁讀出，再以下方 Python **本站重算**——兩者逐位吻合者標 ✓，非逐字轉錄。
>
> **慣例旗標**：所有「Pred.(6)」欄與本站重算都用 [P2] Eq.(6) 的印刷式 $\mathcal{L}=\Gamma_{rms}^2/(8\pi^2\Delta f^2)\cdot(\overline{i_n^2}/\Delta f)/q_{max}^2$——分母 $8\pi^2\Delta f^2=2\Delta\omega^2$，是本站的 $\mathcal{L}_{/2}$ 家族，比 [P1] Eq.(21) 的 $4\Delta\omega^2$ 高 3 dB（見 Eq.(27)–(30) 節的旗標）。

### Table I（p.799）：inverter-chain ring（Fig. 12(a)，無調頻）

| Index | $N$ | NMOS $W/L$ | PMOS $W/L$ | $V_{DD}$ (V) | $I_{sup}$ (mA) | $f_0$ | Pred. (23) | Pred. (6) | Meas. |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 3/2 | 5/2 | 5.0 | 0.3 | 232 MHz | −119.9 | −117.7 | −118.5 |
| 2 | 11 | 4/2 | 6/2 | 5.0 | 0.5 | 115 MHz | −127.2 | −126.4 | −126.0 |
| 3 | 19 | 10/0.25 | 20/0.25 | 2.5 | 10 | 1.33 GHz | −111.8 | −113.0 | −111.5 |

編號 1、2 是 2 µm 5 V 製程（長通道，Eq.(18) 雜訊），編號 3 是 0.25 µm 2.5 V（短通道，Eq.(28) 雜訊）。兩種預測（FOM 式 Eq.(23) 與逐項的 $N\times$Eq.(6)）都落在實測 ±2 dB 內。

### Table II（p.799）：current-starved inverter-chain ring（Fig. 12(b)，全部 0.25 µm 2.5 V）

設計意圖是**固定頻率與功率、只掃 $N$**（用通道長調頻率、用寬度調功率）；Nbias 接 $V_{DD}$、Pbias 接 0 V。

| Index | $N$ | inv N/P $W/L$ | tail N/P $W/L$ | $I_{sup}$ (mA) | $f_0$ (MHz) | Pred. (23) | Pred. (6) | Meas. |
|---|---|---|---|---|---|---|---|---|
| 4 | 3 | 35/0.53, 70/0.53 | 28/0.53, 56/0.53 | 2.34 | 751 | −113.8 | −116.6 | −114.0 |
| 5 | 5 | 21/0.39, 42/0.39 | 23/0.39, 46/0.39 | 2.51 | 850 | −111.7 | −111.9 | −112.6 |
| 6 | 7 | 14/0.36, 28/0.36 | 36.8/0.36, 73.5/0.36 | 2.49 | 931 | −110.5 | −110.4 | −111.7 |
| 7 | 9 | 12.6/0.32, 25.2/0.32 | 28/0.32, 56/0.32 | 2.73 | 932 | −110.4 | −113.5 | −112.5 |
| 8 | 11 | 10.5/0.32, 21/0.32 | 146/0.32, 291/0.32 | 2.65 | 869 | −110.9 | −110.1 | −112.2 |
| 9 | 15 | 9.1/0.28, 18.2/0.28 | 146/0.28, 291/0.28 | 2.8 | 929 | −110.0 | −110.7 | −112.3 |
| 10 | 17 | 7.4/0.25, 12.6/0.25 | 25.2/0.28, 50.4/0.28 | 3.8 | 898 | −111.2 | −109.4 | −112.0 |
| 11 | 19 | 6.3/0.25, 12.6/0.25 | 56/0.25, 112/0.25 | 3.9 | 959 | −110.6 | −110.1 | −110.9 |

**這張表就是 claim C7（N-independence）的實測證據**：$N$ 從 3 到 19（$6.3\times$），實測 $\mathcal{L}$ 只在 $-114.0$ 到 $-110.9$ 之間；把每列用 Eq.(23) 的 $f_0^2/P$ 歸一到 900 MHz、6.25 mW 後全距只有 **3.2 dB**（本站重算，見下方 Python）——若只有 $\Gamma_{rms}^2\propto N^{-3}$ 在作用，$N=3\to19$ 該差 $10\log_{10}(19^3/3^3)=24.0$ dB。編號 4（3 級）略好，論文歸因於較低頻率與較長通道（$\gamma$ 較小）。編號 7 是 Fig. 17 對稱電壓實驗用的那顆。

### Table III（p.800）：differential ring（Fig. 12(c)，全部 0.25 µm 2.5 V，unsilicided poly $R_L$）

| Index | $N$ | $W/L$ | $R_L$ (Ω) | $I_{tail}$ (mA) | $P_{tot}$ (mW) | $f_{max}$ | Tuning | Pred. (34) | Pred. (6) | Meas. |
|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 4 | 4.2/0.25 | 2k | 1 | 10 | 2.81 GHz | 34% | −95.4 | −95.5 | −95.2 |
| 13 | 4 | 8.4/0.25 | 1k | 2 | 20 | 4.47 GHz | 42% | −95.1 | −94.0 | −94.3 |
| 14 | 4 | 16.8/0.25 | 500 | 4 | 40 | 3.89 GHz | 44% | −98.5 | −97.2 | −97.4 |
| 15 | 4 | 33.6/0.25 | 250 | 8 | 80 | 5.43 GHz | 25% | −98.7 | −99.6 | −98.5 |
| 16 | 4 | 8.4/0.25 | 2k | 1 | 10 | 2.87 GHz | 37% | −95.2 | −96.6 | −93.8 |
| 17 | 4 | 16.8/0.25 | 1k | 2 | 20 | 3.39 GHz | 45% | −96.7 | −97.9 | −96.8 |
| 18 | 4 | 33.6/0.25 | 500 | 4 | 40 | 5.33 GHz | 32% | −95.8 | −97.2 | −95.3 |
| 19 | 4 | 16.8/0.25 | 2k | 1 | 10 | 1.75 GHz | 73% | −99.5 | −97.5 | −95.2 |
| 20 | 4 | 33.6/0.25 | 1k | 2 | 20 | 2.24 GHz | 58% | −100.3 | −100.3 | −99.0 |
| 21 | 4 | 33.6/0.25 | 2k | 1 | 10 | 1.27 GHz | 67% | −104.4 | −101.8 | −100.2 |
| 22 | 4 | 67.2/0.25 | 1k | 2 | 20 | 1.19 GHz | 76% | −105.8 | −102.6 | −100.2 |
| 23 | 4 | 33.6/0.25 | 2k | 1 | 10 | 1.53 GHz | N/A | −100.6 | −98.9 | −97.3 |
| 24 | 6 | 13.4/0.25 | 3k | 0.67 | 10 | 859 MHz | 58% | −103.9 | −106.0 | −104.3 |
| 25 | 8 | 6.7/0.25 | 4k | 0.5 | 10 | 731 MHz | 74% | −104.1 | −106.3 | −106.2 |
| 26 | 12 | 4.2/0.25 | 6k | 0.33 | 10 | 447 MHz | 52% | −106.6 | −110.4 | −109.5 |

用 poly 電阻當負載的理由（p.799）：讓節點波形更接近 RC 步階響應、更對稱，壓 1/f 上轉（symmetry 法則的實作版）。
編號 12／24／25／26 四顆 **$P=10$ mW、$R_LI_{tail}=2$ V 固定**（fixed power／fixed swing，正是 Fig. 9 的「+」情境）：把實測歸一到 2.81 GHz 後為 $-95.2/-94.0/-94.5/-93.5$（$N=4/6/8/12$），Eq.(34) 預測 $+10\log_{10}(N/4)=0/1.8/3.0/4.8$ dB——**方向一致（差動 ring 越多級越差）**，但實測斜率較緩；這是 Eq.(34) 明含 $N$ 的實測面。

### Worked example 1：編號 3（單端，Eq.(28)→(6)→(23)；本站重算 ✓）

論文的算法（p.799）：transition 中點的模擬汲極電流 $I_D=3.47$ mA、$E_c=4\times10^6$ V/m、$\gamma=2.5$ 代 Eq.(28)；$C_{total}=71.8$ fF；每節點一個雜訊源，總 phase noise 是 Eq.(6) 的 $N$ 倍。

1. Eq.(28)：$\overline{i_n^2}/\Delta f=8kT\gamma I_D/(E_cL)=2.87\times10^{-22}$ A²/Hz（論文 ✓）。
2. $q_{max}=C_{total}V_{DD}=71.8\text{ fF}\times2.5\text{ V}=179.5$ fC（論文 ✓；full-swing 節點電荷）。
3. Eq.(16)：$\Gamma_{rms}^2=2\pi^2/(3\eta^3N^3)$，$N=19$；論文未印編號 3 用的 $\eta$，本站掃 $\eta=0.75$（Fig. 8 實線值）與 $0.9$（編號 12 用值）。
4. $N\times$Eq.(6)：$\mathcal{L}=N\Gamma_{rms}^2/(8\pi^2\Delta f^2)\cdot(\overline{i_n^2}/\Delta f)/q_{max}^2$；$\eta=0.75$ 得 $-113.1$ dBc/Hz（論文 $-113.0$，差 0.1 dB）。
5. Eq.(23)：$P=V_{DD}I_{sup}=25$ mW、$V_{char}=E_cL/\gamma=0.4$ V、$f_0=1.33$ GHz；$\eta=0.75$ 得 $-111.9$（論文 $-111.8$）。實測 $-111.5$。

**Dimension check**（步驟 4）：$\Gamma_{rms}^2$ 無因次；$1/(\text{Hz}^2)\times(\text{A}^2/\text{Hz})/\text{C}^2=\text{A}^2/(\text{Hz}^3\text{C}^2)=(\text{C}^2/\text{s}^2)\cdot\text{s}^3/\text{C}^2=\text{s}=1/\text{Hz}$ ✓（dBc/Hz 的「/Hz」）。

```python
import numpy as np
k, T = 1.380649e-23, 300.0; kT = k*T
# ---- oscillator #3 ([P2] Table I row 3, p.799): single-ended inverter chain, 0.25 um / 2.5 V
N, VDD, Isup, f0, df = 19, 2.5, 10e-3, 1.33e9, 1e6
Ec, Lch, gam, ID = 4e6, 0.25e-6, 2.5, 3.47e-3
Ctot = 71.8e-15
Si = 8*kT*gam*ID/(Ec*Lch)                       # Eq.(28)
qmax = Ctot*VDD                                 # full-swing node charge
print(f"{Si:.2e} {qmax*1e15:.1f}")             # -> 2.87e-22 179.5   A^2/Hz, fC（論文印 2.87e-22、179.5 fC）
def L6_times_N(N, Si, qmax, eta):               # N x Eq.(6), Gamma_rms from Eq.(16)
    G2 = 2*np.pi**2/(3*eta**3*N**3)
    return 10*np.log10(N*G2/(8*np.pi**2*df**2)*Si/qmax**2)
def L23(P, Vchar, eta):                         # Eq.(23), Vchar = Ec*L/gamma (Eq.30)
    return 10*np.log10(8/(3*eta)*kT/P*VDD/Vchar*(f0/df)**2)
Vchar = Ec*Lch/gam
for eta in (0.75, 0.9):
    print(eta, round(L6_times_N(N, Si, qmax, eta),1), round(L23(VDD*Isup, Vchar, eta),1))
# -> 0.75 -113.1 -111.9   （論文 Table I：Pred.(6) -113.0、Pred.(23) -111.8、Meas. -111.5）
# -> 0.9 -115.5 -112.7
```

### Worked example 2：編號 12（差動，Eq.(28)+(33)→(6)、Eq.(34)、jitter Eq.(12)/(35)；本站重算 ✓）

論文的算法（pp.800–801）：平衡態每節點 $C_{total}=41.6$ fF、模擬擺幅 $1.208$ V；差動對 NMOS 各流 $I_{tail}/2=0.5$ mA，雜訊用 Eq.(28)；負載電阻 $4kT/R_L$；$2N$ 個節點各一源；$\eta=0.9$。

1. $q_{max}=41.6\text{ fF}\times1.208\text{ V}=50.3$ fC（論文 ✓）。
2. NMOS：$8kT\gamma I_D/(E_cL)=4.14\times10^{-23}$；$R_L=2$ kΩ：$4kT/R_L=8.28\times10^{-24}$；總和 $4.97\times10^{-23}$ A²/Hz（三個都 ✓）。這就是 Eq.(33) 的兩份：$4kTI_{tail}(1/V_{char}+1/(R_LI_{tail}))$，$V_{char}=0.4$ V。
3. $2N\times$Eq.(6)（$N=4$、$\eta=0.9$）：$-95.5$ dBc/Hz（論文 ✓）。
4. Eq.(34)：$P=NV_{DD}I_{tail}=10$ mW、$V_{DD}/V_{char}=6.25$、$V_{DD}/(R_LI_{tail})=1.25$、$f_0=2.81$ GHz：$-95.4$（論文 ✓）。實測 $-95.2$。
5. **jitter**：p.801 印出 Fig. 16 的最佳擬合 $\kappa=6.18\times10^{-9}\ \sqrt{\text{s}}$，Eq.(12) 與 Eq.(35) 分別給 $5.95\times10^{-9}$ 與 $6.07\times10^{-9}\ \sqrt{\text{s}}$。本站重算：Eq.(35) 得 $6.07\times10^{-9}$ ✓；Eq.(12)（**照 p.793 印刷式**，分母含 $\omega_0$、$2N$ 個源的雜訊功率相加）得 $5.97\times10^{-9}$（與論文差 0.3%，在論文中間值取位範圍內，本站無法判定來自哪一步）；由實測 $-95.2$ dBc/Hz 用 Eq.(50)（p.803）$\kappa=(\Delta f/f_0)\sqrt{\mathcal{L}_{lin}}$ 反推 $6.18\times10^{-9}$——與 Fig. 16 的擬合**逐位吻合**，這是「頻域 phase noise ↔ 時域 jitter 同一個 $\Gamma_{rms}^2/q_{max}^2$」（claim C6）的實測閉環。**Dimension check**：$(\text{Hz}/\text{Hz})\cdot\sqrt{1/\text{Hz}}=\sqrt{\text{s}}$ ✓。Fig. 16（p.802）在約 $10^{-8}$–$10^{-7}$ s 之間轉成 slope-1（$\sigma\propto\Delta T$，圖上擬合 $\zeta=2.5\times10^5$），論文歸因於元件 1/f 雜訊（Sec. VI 末）。

> **慣例旗標（κ 的兩件衣服，全站一致）**：[P2] Eq.(12) 印刷式 $\kappa=\dfrac{\Gamma_{rms}}{q_{max}\omega_0}\sqrt{\tfrac12\dfrac{\overline{i_n^2}}{\Delta f}}$ 的分母含 $\omega_0$，單位 $\sqrt{\text{s}}$（時域 $\kappa_t$，配 Eq.(8) 的 $\sigma_{\Delta T}$）；本站 [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) 的 $\kappa_\phi^2=\Gamma_{rms}^2S_i/(2q_{max}^2)$ 是 Eq.(11) 的相位版（rad²/s）——同一個物理量，只差 Eq.(10) 的 $\omega_0$：$\kappa_t=\kappa_\phi/\omega_0$（本例 $\omega_0=2\pi\times2.81$ GHz）。本頁與字典頁自 v11 起同一種說法。

```python
import numpy as np
k, T = 1.380649e-23, 300.0; kT = k*T
# ---- oscillator #12 ([P2] Table III row 1, p.800): 4-stage differential, R_L = 2 kOhm, I_tail = 1 mA
N, VDD, Itail, RL, f0, df, eta = 4, 2.5, 1e-3, 2e3, 2.81e9, 1e6, 0.9
Ec, Lch, gam = 4e6, 0.25e-6, 2.5
Ctot, swing = 41.6e-15, 1.208
qmax = Ctot*swing
ID = Itail/2                                    # balanced: half the tail current
Si_N = 8*kT*gam*ID/(Ec*Lch)                     # Eq.(28), one differential-pair NMOS
Si_R = 4*kT/RL                                  # load resistor
Si = Si_N + Si_R
print(f"{qmax*1e15:.1f} {Si_N:.2e} {Si_R:.2e} {Si:.2e}")   # -> 50.3 4.14e-23 8.28e-24 4.97e-23   fC, A^2/Hz（論文印 50.3、4.14e-23、8.28e-24、4.97e-23）
G2 = 2*np.pi**2/(3*eta**3*N**3)                 # Eq.(16)
L6 = 10*np.log10(2*N*G2/(8*np.pi**2*df**2)*Si/qmax**2)     # 2N x Eq.(6)
P = N*VDD*Itail                                 # Eq.(31)
Vchar = Ec*Lch/gam                              # Eq.(30)
L34 = 10*np.log10(8/(3*eta)*N*kT/P*(VDD/Vchar + VDD/(RL*Itail))*(f0/df)**2)   # Eq.(34)
print(round(P*1e3,1), round(L6,1), round(L34,1))   # -> 10.0 -95.5 -95.4   mW, dBc/Hz（論文：-95.5、-95.4；Meas. -95.2）
# jitter: Eq.(12) as printed on p.793 carries omega_0 (kappa in sqrt(s)); 2N sources add in power
w0 = 2*np.pi*f0
k12 = np.sqrt(G2)/(qmax*w0)*np.sqrt(0.5*2*N*Si)
k35 = np.sqrt(8/(3*eta))*np.sqrt(N*kT/P*(VDD/Vchar + VDD/(RL*Itail)))          # Eq.(35)
k50 = df/f0*10**(-95.2/20)                       # Eq.(50) from the MEASURED -95.2 dBc/Hz
print(f"{k12:.2e} {k35:.2e} {k50:.2e}")          # -> 5.97e-09 6.07e-09 6.18e-09   sqrt(s)（論文 p.801：5.95e-9、6.07e-9；Fig.16 實測擬合 6.18e-9）
```

### 本站加值：把 Table II／III 歸一後看 $N$（本站重算）

```python
import numpy as np
# [P2] Table II (current-starved single-ended, all 0.25 um / 2.5 V, p.799): N -> (I_sup mA, f0 MHz, measured L(1 MHz) dBc/Hz)
tab2 = {3:(2.34,751,-114.0), 5:(2.51,850,-112.6), 7:(2.49,931,-111.7), 9:(2.73,932,-112.5),
        11:(2.65,869,-112.2), 15:(2.8,929,-112.3), 17:(3.8,898,-112.0), 19:(3.9,959,-110.9)}
# normalise each row to f0 = 900 MHz, P = 2.5 V x 2.5 mA = 6.25 mW with L ~ f0^2/P (Eq.23)
norm = np.array([L - 20*np.log10(f/900) + 10*np.log10(2.5*I/6.25) for N,(I,f,L) in tab2.items()])
print(round(norm.min(),1), round(norm.max(),1), round(norm.max()-norm.min(),1))   # -> -112.7 -109.5 3.2   dBc/Hz（N=3..19 歸一後全距僅 3.2 dB）
print(round(10*np.log10(19**3/3**3),1))   # -> 24.0  dB：若只有 Gamma_rms^2 ~ N^-3 在作用，N=3->19 該差這麼多
# [P2] Table III rows 12/24/25/26 (p.800): P = 10 mW and R_L*I_tail = 2 V for all four -> Eq.(34) bracket fixed
tab3 = {4:(2810,-95.4,-95.2), 6:(859,-103.9,-104.3), 8:(731,-104.1,-106.2), 12:(447,-106.6,-109.5)}  # N: (f_max MHz, Pred.(34), Meas.)
for N,(f,Lp,Lm) in tab3.items():
    s = 20*np.log10(2810/f)
    print(N, round(Lp+s,1), round(Lm+s,1), round(10*np.log10(N/4),1))
# -> 4 -95.4 -95.2 0.0
# -> 6 -93.6 -94.0 1.8
# -> 8 -92.4 -94.5 3.0
# -> 12 -90.6 -93.5 4.8   （N、Pred.(34) 歸一、Meas. 歸一、Eq.(34) 的 10log(N/4)；單位 dBc/Hz、dB）
```

**適用與失效條件（讀這三張表時）**：(i) 預測只算白噪（Eq.(6)/(23)/(34)），1 MHz offset 對這些 ring 已在 1/f² 區，所以吻合；close-in（1/f³）要看 Fig. 17 與 symmetry。(ii) Eq.(23)/(34) 假設對稱波形、忽略 supply／substrate 與 tail 源雜訊，故是**下限**（p.796），多數實測落在預測 ±2 dB 內，少數（Table III 低頻那幾顆，編號 19–23）實測比預測高 4–6 dB。(iii) $\eta$、$I_D$、$C_{total}$、擺幅都來自電路模擬，論文未全部印出（編號 3 的 $\eta$ 本站以 0.75 反推吻合）。(iv) jitter 的 $\sqrt{\Delta T}$ 段只到約 $10^{-8}$–$10^{-7}$ s，之後 1/f 接手成 slope-1；跨越該點的 SerDes 積分要用兩段式（見 [jitter_kernels](/02_foundations/jitter_kernels)）。

## Design insights

- **jitter 與 phase noise 同源**：壓低 $\Gamma_{rms}^2/q_{max}^2$ 同時降低兩者；別把 long-term
  jitter 與 close-in phase noise 當兩件事處理。
- **加級數不是 phase noise 的解藥**：single-ended 固定 $f_0$、$P$ 下 phase noise 近似與 $N$ 無關
  （結論已核實）；**差動 ring 更要少級**——Eq.(34) 明含 $N$，固定 $f_0$、$P$ 下每加倍級數
  $+3.01$ dB。加級數的真正理由是 quadrature／多相位輸出、調頻範圍、相位裕度。
- **對稱性是 close-in noise 的主旋鈕**：調 rise/fall 對稱（如 Fig. 17 的控制電壓）壓 $c_0$、
  推遠 1/f³ corner。差動 ring（differential）的對稱性通常比 single-ended 好。
- **transition 越陡越好**：能量集中在 transition，斜率越大、$q_{max}$ 越大、$\Gamma_{rms}$
  相對越小。

設計面整理見 [lc_vs_ring](/06_design_insights/lc_vs_ring) 與 [symmetry](/06_design_insights/symmetry)；
SerDes 觀點見 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

## Limitations

照 paper_metadata（paper_002.limitations）：

- toy／一階：短通道效應與細部 device noise 是近似的。
- **N-independence 結論**只對 **single-ended** ring、在固定功率、固定頻率與特定 noise 模型下成立（[P2] Sec.V, Eq.(23)/(25), p.796，已核實，claim C7）；差動 ring 反而明含 $N$（Eq.(34), p.796，已核實）。
- substrate／supply noise 是分開、定性處理的。

## Relationship to other papers

- **[P1]** 是地基：本頁的 jitter $\kappa$、$\Gamma_{rms}$、symmetry 全用 [P1] 的 ISF 與
  Eq.(21)/(24)。
- **[P3]/[P4]** 也用 ring 當載具（[P4] 的 ILFD/prescaler 就是 inverter-chain ring），把 ISF
  從 phase noise 延伸到 injection。
- **[P5]** 與本頁無關；但 latch-based／差動 ring 的起振也靠 cross-coupled 正回授（claim C12 的
  邊角橋樑）。

## 延伸閱讀 / 對應教學頁

| 本頁的哪一塊 | 對應教學頁 | 那頁多給你什麼 |
|---|---|---|
| LC（$-\sin$）vs ring（集中於 transition）的 ISF 對照、N-scaling 論證 | [lc_vs_ring](/06_design_insights/lc_vs_ring) | 兩種拓樸的 $\Gamma_{rms}$、$q_{max}$、phase noise 取捨整理成設計表 |
| Eq.(8) accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ 的隨機漫步 | [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model) | 可跑的 toy model：每 edge 加獨立擾動，log-log 斜率驗證 $\sqrt{\Delta t}$（**pedagogical toy，非 transistor-level**） |
| Fig. 17 對稱點的 phase noise 碗底、$c_0$ 與 1/f³ corner | [symmetry](/06_design_insights/symmetry) | rise/fall 對稱如何壓 $c_0$、differential vs single-ended、設計旋鈕 |

> **怎麼讀**：本頁是「論文怎麼把 [P1] 套到 ring」的故事；想動手看 jitter 怎麼以 $\sqrt{\Delta t}$ 長大，回 lab_03；想把結論變成拓樸選型，回 lc_vs_ring 與 symmetry。SerDes 觀點另見 [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

## What to remember

- **accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$**：自由振盪器的隨機漫步指紋（[P2] Eq.(8), p.792）。
- $\kappa$ 由**和 phase noise 同一個 $\Gamma_{rms}^2/q_{max}^2$** 決定（[P2] Eq.16/23，已核實）。
- **$\Gamma_{rms}\propto N^{-3/2}$**（[P2] Eq.(16), p.794，v7 已重核：根號只蓋常數，正文 $4/N^{1.5}$@$\eta=0.75$
  與 App.B Eq.(55) 三重驗證）；但固定 $f_0$、$P$ 下 phase noise
  **幾乎與 $N$ 無關**（[P2] Eq.(23) 無 $N$，claim C7，已核實）。
- **差動 ring 相反**：[P2] Eq.(34), p.796 明含 $N$（$q_{max}\propto1/N^2$，p.797 原文），固定 $f_0$、$P$
  下 phase noise 隨 $10\log_{10}N$ 惡化（$N=4\to12$ 為 $+4.77$ dB）；差動設計用最少必要級數。
- **Fig. 17**：對稱點 phase noise 有碗底——symmetry 法則的鐵證（claim C4）。
- **短通道分支**：[P2] Eq.(27)–(30), p.796 把 Eq.(23) 的 $V_{char}$ 換成 $E_cL/\gamma$（編號 3：$0.4$ V），N-independence 不變；**Sec. VIII 用 26 顆實作 ring 驗證**——編號 3 由 Eq.(28)→$N\times$Eq.(6) 重算得 $-113.1$（論文 $-113.0$、實測 $-111.5$）、編號 12 由 Eq.(34) 得 $-95.4$（實測 $-95.2$）、由實測 phase noise 反推 $\kappa=6.18\times10^{-9}\ \sqrt{\text{s}}$ 與 Fig. 16 擬合逐位吻合。
- ring 比 LC 好整合，但 phase noise 通常較差；本頁告訴你旋鈕在哪。
