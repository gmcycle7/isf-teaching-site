import React, {useState} from 'react';

// Interactive ISF Fourier explorer: adjust c0..c3 -> see Gamma(theta), Gamma_rms,
// and the 1/f^3 corner ratio c0^2/(2 Gamma_rms^2). Pure SVG, no chart lib.
// Convention (matches site): Gamma(theta) = c0/2 + sum_{n>=1} c_n cos(n theta).
// Gamma_rms^2 = (c0/2)^2 + 1/2 sum_{n>=1} c_n^2  (so sum_{n=0} c_n^2 = 2 Gamma_rms^2).

const W = 520, H = 200, PAD = 28;

function Slider({label, value, min, max, step, onChange}) {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.3rem 0'}}>
      <label style={{flex: '0 0 3.2rem', fontSize: '0.9rem'}}>{label}</label>
      <input type="range" min={min} max={max} step={step} value={value}
             onChange={(e) => onChange(parseFloat(e.target.value))} style={{flex: 1}} />
      <span style={{flex: '0 0 3.2rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
        {value.toFixed(2)}
      </span>
    </div>
  );
}

export default function IsfFourierExplorer() {
  const [c0, setC0] = useState(0.0);
  const [c1, setC1] = useState(1.0);
  const [c2, setC2] = useState(0.0);
  const [c3, setC3] = useState(0.0);

  const N = 200;
  const gamma = (th) => c0 / 2 + c1 * Math.cos(th) + c2 * Math.cos(2 * th) + c3 * Math.cos(3 * th);
  const pts = [];
  let ymax = 0.1;
  for (let i = 0; i <= N; i++) {
    const th = (2 * Math.PI * i) / N;
    const g = gamma(th);
    ymax = Math.max(ymax, Math.abs(g));
    pts.push([i / N, g]);
  }
  ymax *= 1.1;
  const X = (u) => PAD + u * (W - 2 * PAD);
  const Y = (g) => H / 2 - (g / ymax) * (H / 2 - PAD);
  const poly = pts.map(([u, g]) => `${X(u).toFixed(1)},${Y(g).toFixed(1)}`).join(' ');

  const grms2 = (c0 / 2) ** 2 + 0.5 * (c1 * c1 + c2 * c2 + c3 * c3);
  const grms = Math.sqrt(grms2);
  const cornerRatio = grms2 > 0 ? (c0 * c0) / (2 * grms2) : 0; // multiply by omega_1/f

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)', borderRadius: '8px',
    padding: '1rem 1.1rem', margin: '1rem 0', background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 8rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.5rem 0.7rem', textAlign: 'center',
  };
  const axis = 'var(--ifm-color-emphasis-400)';

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.4rem'}}>ISF 傅立葉探索器（調 c₀–c₃ 看 Γ(θ) 與 1/f³ corner）</div>
      <svg viewBox={`0 0 ${W} ${H}`} style={{width: '100%', height: 'auto', background: 'var(--ifm-background-color)', borderRadius: '6px'}}>
        <line x1={PAD} y1={H / 2} x2={W - PAD} y2={H / 2} stroke={axis} strokeWidth="1" />
        <line x1={PAD} y1={PAD} x2={PAD} y2={H - PAD} stroke={axis} strokeWidth="1" />
        <polyline points={poly} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2" />
        <text x={W - PAD} y={H / 2 + 14} fontSize="11" fill={axis} textAnchor="end">θ = 2π</text>
        <text x={PAD + 4} y={PAD + 4} fontSize="11" fill={axis}>Γ(θ)</text>
      </svg>
      <Slider label="c₀" value={c0} min={-1.5} max={1.5} step={0.05} onChange={setC0} />
      <Slider label="c₁" value={c1} min={0} max={1.5} step={0.05} onChange={setC1} />
      <Slider label="c₂" value={c2} min={-1} max={1} step={0.05} onChange={setC2} />
      <Slider label="c₃" value={c3} min={-1} max={1} step={0.05} onChange={setC3} />
      <div style={{display: 'flex', gap: '0.8rem', marginTop: '0.6rem', flexWrap: 'wrap'}}>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>Γ_rms</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>{grms.toFixed(3)}</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>Σcₙ² (=2Γ_rms²)</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>{(2 * grms2).toFixed(3)}</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>1/f³ corner / ω₁f = c₀²/(2Γ_rms²)</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>{cornerRatio.toFixed(3)}</div>
        </div>
      </div>
      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.6rem'}}>
        把 c₀→0（對稱波形）→ 1/f³ corner 趨近 0（close-in flicker 被抑制，[P1] Eq.24）。
        Γ_rms 決定 1/f² phase noise（[P1] Eq.21）。對應 [fourier](/03_isf_core_theory/fourier_series_of_isf)、[symmetry](/06_design_insights/symmetry)。
      </div>
    </div>
  );
}
