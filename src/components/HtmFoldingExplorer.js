import React, {useState, useMemo} from 'react';
import useIsEn from './useIsEn';

// HtmFoldingExplorer — interactive companion to docs/99_appendix/ltv_htm.md
// (the harmonic transfer matrix / band-folding picture of the ISF).
//
// Physics recap (spec 11.2, page Step 3/4/5):
//   A periodic-LTV oscillator does not keep an input noise band on the
//   diagonal like an LTI system does. A single input tone at f_in is folded
//   to |f_in - k*f0| at the phase output, with complex gain
//       H_0^(Gamma)   = c_tilde_0    = c0/2                       (k = 0, DC)
//       H_{+-k}^(Gamma) = c_tilde_{+-k} = (1/2) c_k e^{+-j theta_k}  (k >= 1)
//   so the |gain| of the fold from harmonic k is c0/2 (k=0) or c_k/2 (k>=1).
//   After the ISF-weighting stage the integrator contributes 1/(2*pi*Delta f)
//   (spec Step 5), giving the single-tone phase sideband amplitude
//       phi_p = I0 * c_k / (2 * q_max * Delta_omega)      ([P1] Eq.16/17).
//   This widget fixes I0/q_max = 1 (a normalized "unit-strength" tone) and
//   shows only the *shape* of the readout: the |c_k/2|^2 weighted energy and
//   the 1/(2*pi*Delta f) integrator gain, both as explicit numbers.
//
// The user drags f_in across 0..3 f0 and picks/edits an ISF Fourier series
// c0..c3 (three presets or free sliders). The widget finds every harmonic
// k*f0 within the displayed window (k = 0,1,2,3) and draws a folding arrow
// from f_in down to the corresponding baseband offset Delta f = |f_in-k f0|,
// with arrow height/label = |c_tilde_k|. The "closest" harmonic (the one
// that actually dominates the phase-noise readout at this f_in) is
// highlighted; a readout card sums the |c_k/2|^2-weighted contribution from
// all harmonics within the shown window (Sigma), matching the page's
// "baseband phase-noise contribution" language.
//
// Pure SVG, no chart lib, SSR-safe (no window/document access), locale-aware
// via useIsEn. Pedagogical toy model (illustrative), not transistor-level.

const PRESETS = {
  idealLC: {c0: 0, c1: 1.0, c2: 0, c3: 0},
  asymmetric: {c0: 0.5, c1: 1.0, c2: 0.35, c3: 0.18},
  squareish: {c0: 0, c1: 1.0, c2: 0, c3: 0.33},
};

function gammaTilde(k, c) {
  // c = {c0,c1,c2,c3}; returns |c_tilde_k| (real magnitude, phases theta_n
  // ignored here since only |gain| is drawn — matches the figure's arrows).
  if (k === 0) return c.c0 / 2;
  const cs = [c.c0, c.c1, c.c2, c.c3];
  const n = Math.abs(k);
  return n <= 3 ? cs[n] / 2 : 0;
}

function Row({label, value, unit, min, max, step, onChange, fmt}) {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.3rem 0', flexWrap: 'wrap'}}>
      <label style={{flex: '0 1 11rem', fontSize: '0.9rem'}}>{label}</label>
      <input
        type="range" min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{flex: '1 1 auto'}}
      />
      <span style={{flex: '0 0 7.5rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
        <b>{fmt ? fmt(value) : value}</b> {unit}
      </span>
    </div>
  );
}

const W = 560, H = 260, PAD_L = 40, PAD_R = 20, PAD_T = 46, PAD_B = 34;
const KMAX = 3; // window shown: 0 .. KMAX * f0

export default function HtmFoldingExplorer() {
  const isEn = useIsEn();
  const [fInFrac, setFInFrac] = useState(1.10); // f_in in units of f0, range [0, KMAX]
  const [preset, setPreset] = useState('asymmetric');
  const [c0, setC0] = useState(PRESETS.asymmetric.c0);
  const [c1, setC1] = useState(PRESETS.asymmetric.c1);
  const [c2, setC2] = useState(PRESETS.asymmetric.c2);
  const [c3, setC3] = useState(PRESETS.asymmetric.c3);

  const applyPreset = (name) => {
    const p = PRESETS[name];
    setPreset(name);
    setC0(p.c0); setC1(p.c1); setC2(p.c2); setC3(p.c3);
  };
  const c = {c0, c1, c2, c3};

  // ---- folding geometry: which harmonics k=0..KMAX fold f_in to baseband? ----
  const folds = useMemo(() => {
    const out = [];
    for (let k = 0; k <= KMAX; k++) {
      const df = Math.abs(fInFrac - k); // in units of f0
      const gain = gammaTilde(k, c);
      out.push({k, df, gain});
    }
    // closest harmonic = the one that dominates the phase-noise readout
    let closest = out[0];
    for (const f of out) if (f.df < closest.df) closest = f;
    return {list: out, closest};
  }, [fInFrac, c0, c1, c2, c3]); // eslint-disable-line react-hooks/exhaustive-deps

  // Sigma readout: sum of |c_k/2|^2 over harmonics "close enough" to matter.
  // We call a harmonic "relevant" when its baseband offset Delta f is within
  // 0.5 f0 of the smallest Delta f present (i.e. it is a plausible dominant
  // term at this f_in, not just numerically nonzero at huge offset).
  const relevantWindow = 0.5; // in units of f0, tunable "how close counts"
  const relevant = folds.list.filter((f) => f.df <= folds.closest.df + relevantWindow);
  const sigma = relevant.reduce((acc, f) => acc + f.gain * f.gain, 0);

  // ---- SVG mapping ----
  const X = (fFrac) => PAD_L + (fFrac / KMAX) * (W - PAD_L - PAD_R);
  const maxGain = Math.max(0.05, ...folds.list.map((f) => f.gain), 0.6);
  const Y = (g) => H - PAD_B - (g / maxGain) * (H - PAD_T - PAD_B);
  const y0 = H - PAD_B;

  const axis = 'var(--ifm-color-emphasis-400)';
  const grid = 'var(--ifm-color-emphasis-200)';
  const cIn = 'var(--ifm-color-primary)';
  const cDim = 'var(--ifm-color-emphasis-500)';
  const cHi = 'var(--ifm-color-danger, #e5534b)';

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)', borderRadius: '8px',
    padding: '1rem 1.1rem', margin: '1rem 0', background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 8rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.55rem 0.75rem', textAlign: 'center',
  };
  const btn = {
    padding: '0.3rem 0.75rem', borderRadius: '6px', cursor: 'pointer',
    border: '1px solid var(--ifm-color-emphasis-300)',
    background: 'var(--ifm-background-surface-color)',
    color: 'var(--ifm-font-color-base)', fontSize: '0.82rem',
  };
  const btnActive = {
    ...btn, background: 'var(--ifm-color-primary)', color: '#fff',
    border: '1px solid var(--ifm-color-primary)', fontWeight: 700,
  };

  const fmtF = (v) => `${v.toFixed(2)} f₀`;
  const df0 = folds.closest.df; // dimensionless (units of f0)

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'HTM band-folding explorer: drag the input tone, watch it fold to baseband'
          : 'HTM 頻帶折疊探索器：拖動輸入單音，看它折回 baseband'}
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} role="img"
           aria-label="HTM band folding diagram"
           style={{width: '100%', height: 'auto', background: 'var(--ifm-background-color)', borderRadius: '6px'}}>
        {/* harmonic gridlines + labels */}
        {Array.from({length: KMAX + 1}, (_, k) => k).map((k) => (
          <g key={`g${k}`}>
            <line x1={X(k)} y1={PAD_T} x2={X(k)} y2={y0} stroke={grid} strokeWidth="1" strokeDasharray={k === 0 ? undefined : '3 3'} />
            <text x={X(k)} y={y0 + 16} fontSize="10.5" fill={axis} textAnchor="middle">
              {k === 0 ? 'DC' : (k === 1 ? 'f₀' : `${k}f₀`)}
            </text>
          </g>
        ))}
        {/* frequency axis */}
        <line x1={PAD_L} y1={y0} x2={W - PAD_R} y2={y0} stroke={axis} strokeWidth="1.2" />
        <text x={W - PAD_R} y={y0 + 30} fontSize="10" fill={axis} textAnchor="end">
          {isEn ? 'frequency axis (units of f₀)' : '頻率軸（單位 f₀）'}
        </text>

        {/* input tone marker (tall vertical bar) */}
        <line x1={X(fInFrac)} y1={PAD_T - 8} x2={X(fInFrac)} y2={y0} stroke={cIn} strokeWidth="2.6" />
        <text x={X(fInFrac)} y={PAD_T - 12} fontSize="11.5" fill={cIn} fontWeight="700" textAnchor="middle">
          {isEn ? `f_in = ${fInFrac.toFixed(2)} f₀` : `f_in = ${fInFrac.toFixed(2)} f₀`}
        </text>

        {/* folding arrows: from input tone down to each harmonic's baseband image */}
        {folds.list.map(({k, df, gain}) => {
          if (gain < 1e-4) return null;
          const isClosest = k === folds.closest.k;
          const col = isClosest ? cHi : cDim;
          const x1 = X(fInFrac), x2 = X(k);
          const yTop = PAD_T + 6;
          const ybar = Y(gain);
          const midX = (x1 + x2) / 2;
          const midY = Math.min(yTop, ybar) - 14;
          return (
            <g key={`f${k}`}>
              <path d={`M ${x1} ${yTop} Q ${midX} ${midY} ${x2} ${ybar}`}
                    fill="none" stroke={col} strokeWidth={isClosest ? 2.2 : 1.4}
                    strokeDasharray={isClosest ? undefined : '4 3'} opacity={isClosest ? 0.95 : 0.55}
                    markerEnd="url(#arrowhead)" />
              {/* baseband bar at |f_in - k f0| plotted as a bar sitting at x=k, height=gain */}
              <rect x={X(k) - 7} y={ybar} width="14" height={y0 - ybar}
                    fill={col} opacity={isClosest ? 0.9 : 0.4} rx="2" />
              <text x={X(k)} y={ybar - 5} fontSize="10" fill={col} textAnchor="middle" fontWeight={isClosest ? 700 : 400}>
                {k === 0 ? `|c̃₀|=${gain.toFixed(3)}` : `|c̃${k}|=${gain.toFixed(3)}`}
              </text>
            </g>
          );
        })}
        <defs>
          <marker id="arrowhead" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 0, 7 3.5, 0 7" fill={cHi} />
          </marker>
        </defs>

        <text x={PAD_L} y={20} fontSize="10.5" fill={axis}>
          {isEn ? 'bar height / label = HTM fold gain |c̃ₖ|  (DC = c₀/2, k≥1 = cₖ/2)' : '長條高度／標籤 = HTM 折疊增益 |c̃ₖ|（DC=c₀/2，k≥1 為 cₖ/2）'}
        </text>
      </svg>

      {/* ---- controls: f_in slider ---- */}
      <Row label={isEn ? 'input tone f_in' : '輸入單音 f_in'} value={fInFrac} unit="× f₀" min={0} max={KMAX} step={0.01}
           onChange={setFInFrac} fmt={fmtF} />

      {/* ---- ISF preset buttons ---- */}
      <div style={{display: 'flex', gap: '0.5rem', flexWrap: 'wrap', margin: '0.6rem 0 0.3rem'}}>
        <span style={{fontSize: '0.85rem', opacity: 0.75, marginRight: '0.2rem'}}>
          {isEn ? 'ISF preset:' : 'ISF 預設：'}
        </span>
        <button type="button" style={preset === 'idealLC' ? btnActive : btn} onClick={() => applyPreset('idealLC')}>
          {isEn ? 'ideal LC (Γ=−sinθ)' : 'ideal LC（Γ=−sinθ）'}
        </button>
        <button type="button" style={preset === 'asymmetric' ? btnActive : btn} onClick={() => applyPreset('asymmetric')}>
          {isEn ? 'asymmetric' : 'asymmetric（不對稱）'}
        </button>
        <button type="button" style={preset === 'squareish' ? btnActive : btn} onClick={() => applyPreset('squareish')}>
          {isEn ? 'square-ish' : 'square-ish（方波狀）'}
        </button>
      </div>

      {/* ---- fine-tune sliders (editable regardless of preset) ---- */}
      <Row label="c₀ (DC term)" value={c0} unit="" min={-1} max={1.5} step={0.01}
           onChange={(v) => { setC0(v); setPreset('custom'); }} fmt={(v) => v.toFixed(2)} />
      <Row label="c₁" value={c1} unit="" min={0} max={1.5} step={0.01}
           onChange={(v) => { setC1(v); setPreset('custom'); }} fmt={(v) => v.toFixed(2)} />
      <Row label="c₂" value={c2} unit="" min={-1} max={1} step={0.01}
           onChange={(v) => { setC2(v); setPreset('custom'); }} fmt={(v) => v.toFixed(2)} />
      <Row label="c₃" value={c3} unit="" min={-1} max={1} step={0.01}
           onChange={(v) => { setC3(v); setPreset('custom'); }} fmt={(v) => v.toFixed(2)} />

      {/* ---- readouts ---- */}
      <div style={{display: 'flex', gap: '0.8rem', marginTop: '0.8rem', flexWrap: 'wrap'}}>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>
            {isEn ? 'dominant harmonic k*' : '主導諧波 k*'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700, color: cHi}}>
            {folds.closest.k === 0 ? 'DC' : `k = ${folds.closest.k}`}
          </div>
          <div style={{fontSize: '0.78rem'}}>
            {isEn ? `nearest to f_in` : `離 f_in 最近`}
          </div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>
            {isEn ? 'baseband offset Δf' : 'baseband 偏移 Δf'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{df0.toFixed(3)}</div>
          <div style={{fontSize: '0.78rem'}}>× f₀ = |f_in − k*·f₀|</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>
            {isEn ? 'fold gain |c̃_k*|' : '折疊增益 |c̃_k*|'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{folds.closest.gain.toFixed(3)}</div>
          <div style={{fontSize: '0.78rem'}}>
            {folds.closest.k === 0 ? 'c₀/2' : `c${folds.closest.k}/2`}
          </div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>
            {isEn ? 'Σ |cₖ/2|² (relevant terms)' : 'Σ |cₖ/2|²（相關項）'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{sigma.toFixed(4)}</div>
          <div style={{fontSize: '0.78rem'}}>
            {isEn ? 'baseband PN weight' : 'baseband 相位雜訊權重'}
          </div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>
            {isEn ? 'integrator 1/Δω (∝ 1/Δf)' : '積分器 1/Δω（∝ 1/Δf）'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>
            {df0 > 1e-4 ? (1 / (2 * Math.PI * df0)).toExponential(2) : '∞'}
          </div>
          <div style={{fontSize: '0.78rem'}}>
            {isEn ? '(units of 1/f₀, unit I₀/q_max)' : '（單位 1/f₀，取 I₀/q_max=1）'}
          </div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.72, marginTop: '0.8rem', lineHeight: 1.7}}>
        {isEn ? (
          <>
            Model: drag <code>f_in</code> across 0–3 f₀; the widget finds the nearest harmonic
            k·f₀ (k = 0..3) and draws the folding arrow that lands at baseband offset
            Δf = |f_in − k f₀|, with gain |c̃_k| = c₀/2 (k=0) or c_k/2 (k≥1) — exactly
            H_k^(Γ) from Step 4 of this page. A tone parked right on a harmonic
            (Δf → 0) folds straight to DC with the full gain c_k/2, and the readout
            integrator 1/(2π Δf) blows up there (the [P1] Eq.16/17 sideband
            φ_p = I₀ c_k/(2 q_max Δω), shown here with I₀/q_max normalized to 1).
            Anchor case: pick <b>ideal LC</b> (only c₁ ≠ 0) — only tones near f₀ fold
            at all; every other harmonic band has zero gain, so Σ|c_k/2|² collapses to
            the single c₁/2 = 0.5 term. This is a pedagogical toy model (illustrative),
            not a transistor-level extraction; see{' '}
            <a href="/99_appendix/ltv_htm">ltv_htm</a> Steps 3–5 for the full derivation.
          </>
        ) : (
          <>
            模型：拖動 <code>f_in</code>（0–3 f₀），小工具會找出最近的諧波 k·f₀（k=0..3），
            畫出折疊到 baseband 偏移 Δf = |f_in − k f₀| 的箭頭，增益 |c̃_k| = c₀/2（k=0）
            或 c_k/2（k≥1）——正是本頁 Step 4 的 H_k^(Γ)。單音停在諧波正上方
            （Δf→0）時會整段折到 DC、拿到全部增益 c_k/2，讀數的積分器 1/(2π Δf) 在那裡發散
            （對應 [P1] Eq.16/17 的 sideband φ_p = I₀c_k/(2q_max Δω)，這裡把 I₀/q_max 正規化為 1）。
            錨點案例：選 <b>ideal LC</b>（只有 c₁≠0）——只有 f₀ 附近的單音會折疊，其餘諧波
            band 增益皆為零，Σ|c_k/2|² 收斂成單一 c₁/2=0.5 項。這是 pedagogical toy model
            （illustrative），非 transistor-level 萃取；完整推導見{' '}
            <a href="/99_appendix/ltv_htm">ltv_htm</a> 第 3–5 步。
          </>
        )}
      </div>
    </div>
  );
}
