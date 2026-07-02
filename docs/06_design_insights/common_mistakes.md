---
title: 常見錯誤陳列室：12 個真實地雷
description: 12 個 phase-noise / jitter 工作中真實、可驗證的常見錯誤——κ² 誤當 D、SSB /4 與 /2 混用、單邊譜塞錯 jitter 核、ΔV/斜率直覺推反 ISF、corner 混淆、8/(3γ) 錯記、積分忘 ×2、把 1/f² 發散當物理、DJ_pp 誤入 TJ 公式、RBW 抹平 close-in、÷2 以為秒數減半、對 flicker 用 √N——每條附物理解釋、正確版與站內出處。
---

# 常見錯誤陳列室：12 個真實地雷

> 先備：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) · [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) ｜ 接下來：[exercises](/06_design_insights/exercises) · [cheat_sheet](/00_overview/cheat_sheet)

這一頁不教新公式。它陳列 12 個在 phase noise / jitter 工作裡**真的會犯、犯了就是
2 倍、3 dB 或 $\sqrt2$** 的錯誤——其中好幾個是本站自己在撰寫與審校過程中踩過、
再用模擬裁決修正的（我們把修正紀錄誠實留在各頁）。每一條都是同一個格式：

**❌ 錯誤講法/做法 → 💥 為什麼錯（物理）→ ✅ 正確版 → 📍 站內出處**。

40 年的經驗談：這行最貴的錯不是不會推導，而是**慣例換裝時掉了一個 2**、
或**把 LTI 直覺硬套在 LTV 系統上**。先看總表，再逐條拆。

| # | 地雷 | 錯多少 | 解藥頁 |
|---|---|---|---|
| 1 | 把 $\kappa^2$ 當 Demir 慣例的 $D$ | 線寬 $\times2$ | [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) |
| 2 | SSB $/4$ 與時域 $/2$ 混用（$-148$ vs $-145$） | 3 dB；反解 $\kappa$ 差 $\sqrt2$ | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) |
| 3 | 單邊 $S_\phi$ 塞進 8 係數 jitter 核 | 變異數 $\times2$、jitter $\times\sqrt2$ | [jitter_kernels](/02_foundations/jitter_kernels) |
| 4 | 用 $\Delta V/$斜率 直覺推 ISF 方向 | 符號反、峰值處假發散 | [lti_vs_ltv](/02_foundations/lti_vs_ltv) |
| 5 | 把 device $1/f$ corner 當 $1/f^3$ corner | 本例差 3–300 倍頻率 | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) |
| 6 | ring FOM 記成 $8/(3\gamma)$ | 1.76 dB（長通道） | [fom_limit](/06_design_insights/fom_limit) |
| 7 | dBc/Hz 積分忘 $\times2$ 或亂移 $f_1$ | $\sqrt2$；$f_1$ 每 decade $\sqrt{10}$ | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) |
| 8 | 把 $\Delta f\to0$ 發散當物理 | 定性錯（真實是 Lorentzian） | [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |
| 9 | $\mathrm{DJ}_{pp}$ 直接進 TJ 公式 | 本例悲觀 0.84 ps | [dj_dual_dirac](/06_design_insights/dj_dual_dirac) |
| 10 | RBW 太寬量 close-in | 本例偏高 2.5 dB（且可更糟） | [measurement_and_spurs](/06_design_insights/measurement_and_spurs) |
| 11 | ÷2 後以為 jitter（秒）也減半 | 秒數其實**一顆 fs 都沒變** | [clock_chain_budget](/06_design_insights/clock_chain_budget) |
| 12 | 對 flicker 用白噪 $\sqrt N$ 累積律 | $N=10$ 時低估 ~3 倍 | [jitter_kernels](/02_foundations/jitter_kernels) |

---

## 1. 把 κ² 當 D——線寬直接大 2 倍

**❌ 錯誤做法**：算出相位方差成長率
$\kappa^2=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$（[P2] Eq.(11)/(12), p.793），
把這個數字**直接**叫做 diffusion constant $D$，再套 Demir 慣例的線寬公式
$\Delta f_{3\mathrm{dB}}=D/\pi$。（本站 v3 規範曾犯此錯，v5 以 Monte-Carlo 裁決修正。）

**💥 為什麼錯**：文獻裡 $D$ 有兩種定義——rate 慣例 $\mathrm{Var}[\Delta\phi]=D\vert t\vert$
（此時 $D=\kappa^2$）與 Demir/雷射慣例 $\mathrm{Var}[\Delta\phi]=2D\vert t\vert$（此時
$D=\kappa^2/2$）。$\Delta f_{3\mathrm{dB}}=D/\pi$ 是**後者**的公式；把前者的值塞進去，
線寬多算 $2\times$。

**✅ 正確版**：先問對方的 $\mathrm{Var}$ 式子裡**有沒有那個 2**，再換裝。無歧義的寫法是
全部用 $\kappa^2$ 表達：

$$
\Delta f_{3\mathrm{dB}}=\frac{\kappa^2}{2\pi}\qquad[\text{Hz}]
$$

canonical 例 B（$\Gamma_{rms}=0.5$、$q_{max}=1$ pC、$S_i=10^{-24}$ A²/Hz）：
$\kappa^2=0.125$ rad²/s → 正確線寬 **19.9 mHz**；錯版給 39.8 mHz。lab_23 一次模擬四路萃取
（方差斜率 0.1252 rad²/s、線寬擬合 20.0 mHz）站在 19.9 mHz 這邊。
單位檢查：$\text{rad}^2/\text{s}\div2\pi=\text{Hz}$ ✓（rad 無因次）。

**📍 站內出處**：[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)（衣服二/三的
逐項對帳與 lab_23 裁決）、[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)。

## 2. −148 與 −145 混著用——SSB /4 vs 時域 /2 的 3 dB

**❌ 錯誤做法**：同一顆振盪器，一頁寫 $\mathcal{L}(1\,\text{MHz})=-148$ dBc/Hz、另一頁寫
$-145$，不標慣例就互相引用；或把 [P1] Eq.(21) 算出的 $/4$ 慣例數字，塞進吃 $/2$ 慣例的
反解公式 $\kappa=2\pi\Delta f\sqrt{\mathcal{L}_{lin}}$。

**💥 為什麼錯**：[P1] Eq.(21), p.185 用 SSB（single-sideband，單邊帶）記帳，分母是
$4\Delta\omega^2$（其求和版 Eq.(19) 對應 $8q_{max}^2\Delta\omega^2$）；小角 PM 的乾淨時域
推導給 $\mathcal{L}=\tfrac12S_\phi$，分母是
$2\Delta\omega^2$——兩者差 $10\log_{10}2\approx3$ dB，是文獻上著名的慣例之爭，**不是**誰算錯。

**✅ 正確版**：例 B 的兩張臉都要認得：$/4$ 給 $-148.0$、$/2$ 給 $-145.0$ dBc/Hz。
報數字**必標慣例**；反解 $\kappa$（[P2] Eq.(50), p.803 路線）吃的是 $/2$ 慣例——代
$-145$ 得 $\kappa=0.354$ rad/$\sqrt{\text{s}}$ ✓，誤代 $-148$ 只得 $0.25$（少 $\sqrt2$）。
scaling（$\Gamma_{rms}^2/q_{max}^2$、$-20$ dB/dec）兩種慣例完全相同。

**📍 站內出處**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
（factor-of-2 教學註記）、[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)（衣服四）、
[jitter_kernels](/02_foundations/jitter_kernels)（第 4.5 節的反解陷阱）。

## 3. 單邊/雙邊 PSD 塞錯 jitter 核——8 vs 4 的 √2

**❌ 錯誤做法**：從量測的 $\mathcal{L}$ 取單邊譜 $S_\phi=2\times10^{\mathcal{L}/10}$，
然後塞進文獻上寫成
$\sigma^2_{\Delta\phi}=\dfrac{8}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\sin^2(\pi f\tau)\,df$
的 period-jitter 公式（[P2] Eq.(49), p.803 的字面形）。

**💥 為什麼錯**：[P2] Eq.(48) 定義的 $R_\phi(\tau)=\int_{-\infty}^{\infty}S_\phi e^{j2\pi f\tau}df$
是**雙邊**譜；係數 8 的公式配雙邊譜。單邊譜（datasheet／$\mathcal{L}$ 換來的那條）本身已把
雙邊功率折成 2 倍密度，再配 8 係數就**重複計了一次 2**——變異數 $\times2$、jitter $\times\sqrt2$。

**✅ 正確版**：一種慣例走全程。單邊 $S_\phi$、$\int_0^\infty$ 時，N-period 核是

$$
\sigma_P^2(N)=\frac{1}{\omega_0^2}\int_0^\infty S_\phi(f)\,4\sin^2(\pi fNT)\,df
$$

（$8S_\phi^{DS}\sin^2=4S_\phi^{OS}\sin^2$，兩式數值相同）。canonical 白噪振盪器
（$\kappa^2=0.125$ rad²/s、$f_0=5$ GHz）：正確 $\sigma_P=0.1592$ fs；錯版 0.2251 fs。
lab_24 用三種記帳各算一次，三個都印 0.1592 fs。

**📍 站內出處**：[jitter_kernels](/02_foundations/jitter_kernels)（第 0 步對照表、
[P2] Eq.(48)/(49) 逐字核實註記、lab_24 Monte-Carlo）。

## 4. 用 ΔV/斜率 直覺推 ISF 方向——LTI 直覺在 LTV 系統上翻車

**❌ 錯誤做法**：套 comparator 的
$\Delta t=\Delta V/(\mathrm{d}V/\mathrm{d}t)$ 直覺，宣稱「注入正電荷把電壓推高，所以相位
一律超前（或一律落後）」；或由此推出「斜率越小越敏感，所以正弦振盪器在**波峰**最怕
noise」。（本站 lti_vs_ltv 頁早期版本就把方向寫反過，已修正。）

**💥 為什麼錯**：振盪器是 LTV（linear time-variant，線性時變）系統，$\Delta\phi$ 的正負
由電壓跳變在 limit cycle 上的**切向投影**決定，隨注入相位**變號**；而在波峰，$\Delta V$
幾乎全是徑向（振幅）分量，被振幅恢復力吃掉——真實敏感度是 **0**，不是 $1/$斜率 暗示的
無限大。

**✅ 正確版**：理想 LC（$V=V_{max}\cos\theta$）的 ISF 是 $\Gamma(\theta)=-\sin\theta$
（[P1] Sec. III；$\Delta\phi=\Gamma\,\Delta q/q_{max}$）。方向自查表：上升零交越
（$\theta=3\pi/2$）$\Gamma=+1$ → 相位**超前**；下降零交越（$\theta=\pi/2$）$\Gamma=-1$
→ 相位**落後**；波峰/波谷 $\Gamma=0$ → 純改振幅。數值手感（例 A）：1 fC 注入
$q_{max}=1$ pC、$f_0=5$ GHz，零交越 $\vert\Delta\phi\vert=10^{-3}$ rad $=31.8$ fs、
波峰 0 fs。1-D 波形平移檢查 $\delta=\Delta V/(\mathrm{d}V/\mathrm{d}t)$ **只在零交越**
與 ISF 一致，往波峰走就失效——那正是振幅通道接手的地方。

**📍 站內出處**：[lti_vs_ltv](/02_foundations/lti_vs_ltv)（方向表與投影論證）、
[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)、
[waveform_slope](/06_design_insights/waveform_slope)（斜率直覺**適用**的場合：受驅動的
threshold-crossing 電路）。

## 5. 把 device 的 1/f corner 當成 1/f³ corner

**❌ 錯誤講法**：「這顆電晶體 flicker corner 在 1 MHz，所以 phase noise 的 $1/f^3$ 段
也延伸到 offset 1 MHz。」

**💥 為什麼錯**：flicker 上轉的效率由 ISF 的 DC 係數 $c_0$ 決定，白噪段則由
$\Gamma_{rms}$ 決定——兩段交點（$1/f^3$ corner）因此被**波形對稱性**重新縮放，
不是 device corner 的複製品。[P1] 特別強調這推翻了「兩個 corner 相等」的舊迷思。

**✅ 正確版**：[P1] Eq.(24), p.185：

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2
$$

device corner 1 MHz、$\Gamma_{rms}=0.5$ 時：不對稱波形（$c_0=0.4$）→ corner
**320 kHz**；對稱化到 $c_0=0.04$ → **3.2 kHz**。同一顆 device，corner 差 100 倍——
$1/f^3$ corner 是**設計變數**（對稱性），不是製程常數。
單位檢查：頻率 × 無因次比例 = 頻率 ✓。

**📍 站內出處**：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
（例 E/F 就是這兩個數字）、[symmetry](/06_design_insights/symmetry)。

## 6. ring FOM 前置係數記成 8/(3γ)——γ 被算了兩次

**❌ 錯誤做法**：把 [P2] 的 ring 白噪 phase-noise 極限寫成
$\mathcal{L}=\dfrac{8}{3\gamma}\dfrac{kT}{P}\dfrac{V_{DD}}{V_{char}}\Big(\dfrac{f_0}{\Delta f}\Big)^2$
（分母放通道熱雜訊係數 $\gamma$）。

**💥 為什麼錯**：[P2] Eq.(23), p.796 的前置係數是 $8/(3\eta)$——$\eta$ 是**級延遲比例
常數**（[P2] Eq.(14)，$\approx1$，波形/延遲記帳），與雜訊無關；$\gamma$ 只透過
$V_{char}=\Delta V/\gamma$ 進入。寫成 $8/(3\gamma)$ 等於把 $\gamma$ 算兩次。

**✅ 正確版**：

$$
\mathcal{L}_{lin}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{V_{char}}\cdot\left(\frac{f_0}{\Delta f}\right)^{2},\qquad V_{char}=\frac{\Delta V}{\gamma}
$$

長通道 $\gamma=2/3$、$\eta=1$ 時，錯記法把雜訊多算 $10\log_{10}\!\big(4/(8/3)\big)=1.76$ dB；
更陰險的是 $\gamma=1$ 時兩式剛好重合，把錯誤藏起來。$V_T=0$ 的天花板
$F_{eff}\ge16\gamma/(3\eta)$（[P2] Eq.(25)）裡的 $\gamma$ 才是從 $V_{char}$ 一路帶出來的。
（本站規範 v3 已對照 [P2] 原始 PDF p.796 更正此係數。）

**📍 站內出處**：[fom_limit](/06_design_insights/fom_limit)（第 2 步含逐步推導與天花板）、
[paper_002 深讀](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)。

## 7. dBc/Hz 積分算 jitter：忘了 ×2，或積分範圍亂標

**❌ 錯誤做法**：算 rms jitter 時直接
$\sigma_\phi^2=\int10^{\mathcal{L}/10}df$（忘了 $S_\phi=2\times10^{\mathcal{L}/10}$ 的
$\times2$）；或不標積分頻帶就報「jitter = xx fs」，別人用不同 $f_1$ 對不上。

**💥 為什麼錯**：$\mathcal{L}\approx\tfrac12S_\phi$（小角 PM，每個 sideband 只拿一半功率），
少乘 2 → 變異數少一半、jitter 低 $\sqrt2$。而 $1/f^2$ 譜的積分被**下限 $f_1$ 主導**
（$\int_{f_1} df/f^2\propto1/f_1$）——$f_1$ 每降一個 decade，jitter 漲 $\sqrt{10}$。

**✅ 正確版**：四步鏈 $\mathcal{L}\xrightarrow{\times2,\ \text{de-dB}}S_\phi\xrightarrow{\int_{f_1}^{f_2}}\sigma_\phi^2\xrightarrow{\sqrt{\ }}\sigma_\phi\xrightarrow{\div\,2\pi f_0}\sigma_t$，且**永遠附上 $[f_1,f_2]$**。canonical 例 C
（5 GHz、$-100$ dBc/Hz@1 MHz、$1/f^2$、積 1–100 MHz）：正確 **447.9 fs**；
忘 $\times2$ → 316.7 fs；$f_1$ 移到 100 kHz → 1422.8 fs（$\times\sqrt{10}$）。
dimension check：$\text{rad}\div(\text{rad/s})=\text{s}$ ✓。

**📍 站內出處**：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)（例 C 逐步）、
[lab_08](/04_simulation_labs/lab_08_jitter_integration)。

## 8. 把 L 在 Δf→0 的發散當物理——「近載波無限大」不存在

**❌ 錯誤講法**：「Eq.(21) 是 $1/\Delta\omega^2$，所以 offset 越小 phase noise 越大，
$\Delta f\to0$ 時功率無限大」；或拿著儀器在極小 offset 讀不到 $-20$ dB/dec 而懷疑量測壞了。

**💥 為什麼錯**：$1/\Delta\omega^2$ 來自**線性化**（小角近似），而 $\Delta f\to0$ 對應
長時間，相位隨機漫步早就走出 $\gg1$ rad——近似正好在那裡失效。真實載波譜是
**Lorentzian**：近載波轉平、峰值有限、總功率守恆（$=$ 載波功率）。

**✅ 正確版**：$1/f^2$ 只是 Lorentzian 在 $\Delta f\gg\Delta f_{3\mathrm{dB}}$ 的遠端漸近；
轉折在 $\Delta f_{3\mathrm{dB}}=\kappa^2/2\pi$。canonical 例 B：19.9 mHz（幾乎量不到，
所以工程上 $1/f^2$「看起來」一路到底）；datasheet 級 $-100$ dBc/Hz@1 MHz 的振盪器
則是 628 Hz——在低 offset 量測時真的看得到轉平。發散不是物理，是近似的失效訊號。

**📍 站內出處**：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)（完整機制與
功率守恆）、[beyond_lorentzian](/03_isf_core_theory/beyond_lorentzian)、
[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)（衣服三）。

## 9. 把 DJ_pp 直接塞進 TJ 公式——該用 DJ_δδ

**❌ 錯誤做法**：量到（或算出）deterministic jitter 的實際 peak-to-peak 值
$\mathrm{DJ}_{pp}$，直接代入業界外插公式
$\mathrm{TJ}(\mathrm{BER})=\mathrm{DJ}+2Q^{-1}(\mathrm{BER})\,\sigma$。

**💥 為什麼錯**：dual-Dirac（雙 Dirac）模型的 $\mathrm{DJ}_{\delta\delta}$ 是**Q-scale
尾巴擬合出的模型參數**，數學上必然 $\le\mathrm{DJ}_{pp}$（DJ 分布靠近極值處只有有限
機率質量，深尾是「打了折的高斯」）；這個「故意低報」正是讓 BER 外插貼住真實尾巴的
機制。

**✅ 正確版**：$\mathrm{TJ}(\mathrm{BER})=\mathrm{DJ}_{\delta\delta}+2Q^{-1}(\mathrm{BER})\sigma$，
BER $=10^{-12}$ 時 $2Q^{-1}=14.07$。lab_31（弦波 DJ、$A=2$ ps、RJ $\sigma=1$ ps）：
$\mathrm{DJ}_{pp}=4.0$ ps 但擬合 $\mathrm{DJ}_{\delta\delta}=3.16$ ps；硬用
$\mathrm{DJ}_{pp}$ 得 TJ $=18.07$ ps，比精確 bathtub 的 17.23 ps **悲觀 0.84 ps**——
白白丟掉 margin。反方向也錯：$\mathrm{DJ}_{\delta\delta}$ 不是實體 peak-to-peak，別拿它
去畫波形極值。報告時註明擬合窗（lab_31：擬合窗越深 $\mathrm{DJ}_{\delta\delta}$ 越靠近
但不超過 $\mathrm{DJ}_{pp}$：3.07/3.16/3.27 ps）。

**📍 站內出處**：[dj_dual_dirac](/06_design_insights/dj_dual_dirac)（第 6/7 步：推導＋
「低報是故意的」的證明）、[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

## 10. RBW 開太寬量 close-in——把 −30 dB/dec 的陡裙邊抹平

**❌ 錯誤做法**：用 spectrum analyzer 直接法量近載波 phase noise 時，為了掃得快，
在 offset 1 kHz 用 RBW（resolution bandwidth，解析頻寬）$=1$ kHz 級的濾波器讀
dBc/Hz；或用標稱 RBW（而非 ENBW）做 per-Hz 歸一。

**💥 為什麼錯**：dBc/Hz 讀數是「RBW 濾波器窗內的平均密度」。$1/f^3$ 區密度在一個
窗內變化數十 dB，平均值被靠載波那側主導——讀數偏高、陡裙邊被抹平；RBW 大到窗沿
碰到載波時，載波功率直接漏進來，read 到的是濾波器形狀不是 DUT。

**✅ 正確版**：close-in 量測讓 RBW $\ll\Delta f$（保守取 $\Delta f/10$ 以下）。誠實的
數值手感（對 $1/f^3$ 密度在窗內取平均、與 $\Delta f=1$ kHz 的真值比）：RBW $=1$ kHz
偏高 **2.5 dB**，RBW $=100$ Hz 只剩 0.02 dB（見文末 code；這還沒算載波洩漏，實況
只會更糟）。歸一到 per-Hz 用 **ENBW**（equivalent noise bandwidth，等效雜訊頻寬）
而非標稱 RBW，並記得 log 檢波的 $+2.5$ dB 修正（與上面窗平均那個 2.5 dB 是**不同機制**，
數值撞號純屬巧合）——此為標準頻譜儀量測常識（外部文獻，
非本站 5 篇 PDF；見 measurement 頁方法 A 所引 Keysight/Agilent AN-1303）。真正的
近載波轉平是 Lorentzian（錯誤 8），先排除 RBW 假象才能宣稱看到了它。

**📍 站內出處**：[measurement_and_spurs](/06_design_insights/measurement_and_spurs)
（方法 A 的 ENBW 歸一化、spur 判別的「改 RBW 重量」測試）。

## 11. ÷2 之後以為 jitter（秒）也減半——相位 dB 與絕對時間的混淆

**❌ 錯誤講法**：「除頻器 ÷2 讓 phase noise 好 6 dB，所以 rms jitter（fs）也小一半
（或小 $\sqrt2$）。」

**💥 為什麼錯**：理想除頻是 edge-picking（挑邊緣）——它**照搬**輸入 edge 的時間位置，
一顆 fs 都沒動。變的是「匯率」：同一個秒數誤差，攤在 $N$ 倍長的週期上，換算成的
**相位角**（rad）變小，$\mathcal{L}$ 才降 $20\log_{10}N$。

**✅ 正確版**：老老實實推一次。$\phi_{out}=\phi_{in}/N$（除頻的相位定義），所以
$\sigma_{\phi,out}=\sigma_{\phi,in}/N$（rad 確實變小）；但 $f_{0,out}=f_{0,in}/N$，代入
規範公式 17：

$$
\sigma_{t,out}=\frac{\sigma_{\phi,out}}{2\pi f_{0,out}}=\frac{\sigma_{\phi,in}/N}{2\pi f_{0,in}/N}=\frac{\sigma_{\phi,in}}{2\pi f_{0,in}}=\sigma_{t,in}
$$

兩個 $N$ 對消——**以秒計的 jitter 是理想 ×N/÷N 的不變量**。worked chain 實算
（5 GHz 級 ÷2 到 2.5 GHz、同積分頻帶）：22.5 fs → 22.5 fs，而 $\sigma_\phi$ 確實
減半（0.706 → 0.353 mrad）。÷2 省下的是「佔 UI 的比例」（UI 變長），不是秒數；
ADC aperture 或絕對時序預算看的是秒數，一點好處都沒拿到。
dimension check：$\text{rad}\div(\text{rad/s})=\text{s}$，與 $N$ 無關 ✓。

**📍 站內出處**：[clock_chain_budget](/06_design_insights/clock_chain_budget)（規則 2 與
第 5 步「守恆量」）、[adc_aperture_jitter](/06_design_insights/adc_aperture_jitter)。

## 12. 對 flicker 噪聲用白噪的 √N 累積律

**❌ 錯誤做法**：量了 period jitter $\sigma_P(1)$，用 $\sigma(N)=\sigma_P(1)\sqrt N$
外插 $N$ 個週期後的累積 jitter——不管譜長什麼樣。

**💥 為什麼錯**：$\sqrt N$ 律是白噪 FM 的隨機漫步性質（增量獨立，[P2] Eq.(8)）。
flicker（$1/f^3$）主導時相鄰增量**強相關**，成長律近似 $\propto N$（[P2] Eq.(9) 與
Fig. 4 的斜率 1 段）——用 $\sqrt N$ 外插會**系統性低估**長區間 jitter。

**✅ 正確版**：先看 $f\sim1/(2NT)$ 附近誰主導。白噪段：$\sigma_{\Delta\phi}=\kappa\sqrt{NT}$；
flicker 段：$\sigma^2_{\Delta\phi}=4\pi^2b_3(NT)^2\big[\tfrac32-\gamma_E-\ln(2\pi NTf_l)\big]$
（$\gamma_E=0.5772$ 為 Euler–Mascheroni 常數；幾乎 $\propto N$，且對數依賴低頻截止
$f_l$——報數字必附 $f_l$）。數值臉孔（lab_24，
$T=200$ ps、$f_l=100$ Hz）：$\sigma(N{=}10)/\sigma(N{=}1)$ 白噪 $=\sqrt{10}=3.16$、
flicker $=9.29$——差近 3 倍。快速體檢：白噪區才有 $\sigma_{c2c}=\sqrt2\,\sigma_P$；
這關係不成立就別用 $\sqrt N$。

**📍 站內出處**：[jitter_kernels](/02_foundations/jitter_kernels)（第 5 步 flicker 封閉式與
log-band caveat）、[lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)、
[allan_variance](/02_foundations/allan_variance)（同一件事的 ADEV 版：white FM
$\tau^{-1/2}$ vs flicker FM $\tau^0$）。

---

## 共同病根：三個 factor-of-2 家族 + 一個 LTI 慣性

12 條地雷裡有 7 條（1、2、3、7、9 的 $2Q^{-1}$、11、12）本質上是**記帳慣例**問題，
可歸成三家族（詳見 [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)）：

1. **單邊 vs 雙邊 PSD**：$S_i/2$ 的 $\delta$ 強度、$2\kappa^2$ 的單邊譜、jitter 核的 8 vs 4。
2. **$\mathrm{Var}=D\vert t\vert$ vs $2D\vert t\vert$**：$\kappa^2=D_{\text{甲}}=2D_{\text{乙}}$。
3. **SSB $/2$ vs $/4$**：$-145$ vs $-148$ 的 3 dB。

另外 4 條（4、5、8、部分 10）是**把 LTI／線性化直覺用到它失效的地方**：斜率直覺撞上
振幅恢復、device corner 直覺撞上 $c_0$ 上轉、$1/f^2$ 直線撞上隨機漫步的大角度、
窄帶密度直覺撞上寬 RBW 平均。防禦方法只有一個：**每個數字都問「這是哪個慣例？
近似在這裡還成立嗎？」**——然後用一行 Python 對帳。

## 一鍵對帳：本頁所有數字的驗證 code

以下把 12 條地雷中可一行驗證的數字全部重算一次（跑法：在專案根目錄
`PYTHONPATH=. python3 <此檔>`；錯誤 9 的 DJ 數字由 `simulations/lab_31_dual_dirac.py`
產生，見 [dj_dual_dirac](/06_design_insights/dj_dual_dirac)）：

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter

# --- 錯誤 1：κ² 誤當 D（線寬 2×）---
GRMS, QMAX, SI = 0.5, 1e-12, 1e-24
k2 = GRMS**2 * SI / (2 * QMAX**2)                 # [P2] Eq.(11)/(12)
print(round(k2, 3))                               # -> 0.125 （κ², rad²/s）
print(round(k2 / (2*np.pi) * 1e3, 1))             # -> 19.9 （正確 FWHM，mHz）
print(round(k2 / np.pi * 1e3, 1))                 # -> 39.8 （κ² 塞進 D/π 的 2× 錯值）

# --- 錯誤 2：SSB /4 vs 時域 /2（3 dB）---
dw = 2 * np.pi * 1e6
print(round(10*np.log10(GRMS**2/QMAX**2 * SI/(4*dw**2)), 1))  # -> -148.0 （[P1] Eq.(21) /4）
print(round(10*np.log10(GRMS**2/QMAX**2 * SI/(2*dw**2)), 1))  # -> -145.0 （時域 /2）

# --- 錯誤 3：單邊譜塞進 8 係數核（×√2）---
f0, T = 5e9, 2e-10
sigP = np.sqrt(k2 * T) / (2*np.pi*f0)
print(round(sigP*1e15, 4))                        # -> 0.1592 （正確 period jitter，fs）
print(round(sigP*np.sqrt(2)*1e15, 4))             # -> 0.2251 （×√2 錯值，fs）

# --- 錯誤 5：1/f³ corner ≠ device corner（Eq.24，device corner=1 MHz）---
print(round(1e6 * 0.4**2 / (2*GRMS**2) / 1e3, 1))   # -> 320.0 （c0=0.4，kHz）
print(round(1e6 * 0.04**2 / (2*GRMS**2) / 1e3, 1))  # -> 3.2 （c0=0.04，kHz）

# --- 錯誤 6：8/(3γ) vs 8/(3η)（γ=2/3、η=1）---
print(round(10*np.log10((8/(3*(2/3))) / (8/3)), 2))  # -> 1.76 （dB，錯記法多算的量）

# --- 錯誤 7：積分忘 ×2、或 f₁ 亂移 ---
f = np.logspace(3, 9, 400001)
L = leeson_one_over_f2(f, L_ref_dbc=-100.0, f_ref=1e6)
st, _ = integrate_rms_jitter(f, L, f0=5e9, fmin=1e6, fmax=1e8)
print(round(st*1e15, 1))                          # -> 447.9 （正確，fs；例 C）
print(round(st/np.sqrt(2)*1e15, 1))               # -> 316.7 （忘 ×2，fs）
st2, _ = integrate_rms_jitter(f, L, f0=5e9, fmin=1e5, fmax=1e8)
print(round(st2*1e15, 1))                         # -> 1422.8 （f₁ 移到 100 kHz，fs）

# --- 錯誤 10：RBW 對 1/f³ 裙邊在 offset=1 kHz 的讀數偏差 ---
d = 1e3
bias = lambda rbw: 10*np.log10(d**3/(2*rbw)*(1/(d-rbw/2)**2 - 1/(d+rbw/2)**2))
print(round(bias(1e3), 2))                        # -> 2.5 （RBW=1 kHz，dB 偏高）
print(round(bias(1e2), 2))                        # -> 0.02 （RBW=100 Hz，dB）

# --- 錯誤 11：÷2 之後 dB 好 6 dB、秒數不變 ---
f = np.logspace(4, 8, 20001)
L5G = np.where(f <= 1e6, -126.02, -148.0 - 20*np.log10(f/1e6))
st5, sp5 = integrate_rms_jitter(f, L5G, f0=5e9, fmin=1e4, fmax=1e8)
st25, sp25 = integrate_rms_jitter(f, L5G - 6.02, f0=2.5e9, fmin=1e4, fmax=1e8)
print(round(st5*1e15, 1), round(st25*1e15, 1))    # -> 22.5 22.5 （fs，除頻前後）
print(round(sp5/sp25, 2))                         # -> 2.0 （相位 rad 確實減半）

# --- 錯誤 12：flicker 的 N 成長律 ≈ N（不是 √N）---
gEM, fl = 0.5772156649, 100.0
br = lambda N: 1.5 - gEM - np.log(2*np.pi*N*T*fl)
print(round(10*np.sqrt(br(10)/br(1)), 2))         # -> 9.29 （白噪應為 √10=3.16）
```

（錯誤 10 的 `bias` 是「$1/f^3$ 密度在 RBW 窗內的平均 ÷ 窗中心真值」的解析式：
$\overline{S}=\frac{1}{\mathrm{RBW}}\int b/f^3\,df=\frac{b}{2\,\mathrm{RBW}}\big(f_{lo}^{-2}-f_{hi}^{-2}\big)$，
教學用 toy 計算，未含載波洩漏與檢波器效應。）

## 重點回顧

- 換慣例前先對帳：**單邊/雙邊**、**$\mathrm{Var}=D\vert t\vert$ vs $2D\vert t\vert$**、
  **SSB $/2$ vs $/4$**——三個 factor-of-2 家族包辦了大半地雷。
- ISF 的方向與大小來自 **limit-cycle 切向投影**，不是 $\Delta V/$斜率；波峰是振幅通道
  的地盤（$\Gamma=0$）。
- 兩個 corner 是兩回事：$1/f^3$ corner $=\omega_{1/f}\,c_0^2/(2\Gamma_{rms}^2)$，
  由對稱性可壓到遠低於 device corner（本例 $c_0=0.04$ 時低 300 倍：1 MHz → 3.2 kHz）。
- ring FOM 前置係數是 $8/(3\eta)$；$\gamma$ 只活在 $V_{char}=\Delta V/\gamma$ 裡。
- jitter 積分：$\times2$、標頻帶（$f_1$ 主導）、÷$2\pi f_0$；理想 ×N/÷N 之下
  **秒數不變**，變的只是 dB 匯率。
- $\Delta f\to0$ 的發散是線性化假象——真實譜是 Lorentzian，總功率守恆。
- TJ 外插吃 $\mathrm{DJ}_{\delta\delta}$（模型參數、故意低報），不吃 $\mathrm{DJ}_{pp}$。
- close-in 量測：RBW $\ll\Delta f$、用 ENBW 歸一，先排除儀器假象再談物理。
- flicker 主導時累積律 $\approx N$（非 $\sqrt N$），且對數依賴 $f_l$——報數字附條件。

## 延伸閱讀

- 全站 factor-of-2 對帳總表：[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
- $/4$ vs $/2$ 的完整推導：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- jitter 核與 [P2] Eq.(49) 逐字核實：[jitter_kernels](/02_foundations/jitter_kernels)
- $\mathcal{L}\to\sigma_t$ 四步鏈與例 C：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- 近載波真相：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- 時脈鏈記帳四規則：[clock_chain_budget](/06_design_insights/clock_chain_budget)
- 量測方法與 spur 判別：[measurement_and_spurs](/06_design_insights/measurement_and_spurs)
- 把觀念變手感的練習題：[exercises](/06_design_insights/exercises)
