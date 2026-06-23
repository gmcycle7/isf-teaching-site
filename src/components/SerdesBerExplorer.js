import React, {useState} from 'react';

// Interactive SerDes RJ -> BER bathtub explorer. Adjust rms jitter sigma_t and
// the UI; see the BER bathtub and the eye opening at BER = 1e-12.
// BER(t) = 1/2[Q((UI/2 - t)/sigma) + Q((UI/2 + t)/sigma)],  Q(x)=1/2 erfc(x/sqrt2).

const W = 520, H = 220, PAD = 34;
const LOGMIN = -18; // BER floor for plotting

// Numerical Recipes erfcc approximation (~1e-7 accuracy).
function erfc(x) {
  const z = Math.abs(x);
  const t = 1 / (1 + 0.5 * z);
  const ans = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 +
    t * (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 +
    t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
  return x >= 0 ? ans : 2 - ans;
}
const Q = (x) => 0.5 * erfc(x / Math.SQRT2);

function Slider({label, value, unit, min, max, step, onChange, fmt}) {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.3rem 0'}}>
      <label style={{flex: '0 0 6rem', fontSize: '0.9rem'}}>{label}</label>
      <input type="range" min={min} max={max} step={step} value={value}
             onChange={(e) => onChange(parseFloat(e.target.value))} style={{flex: 1}} />
      <span style={{flex: '0 0 5rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
        {fmt ? fmt(value) : value} {unit}
      </span>
    </div>
  );
}

export default function SerdesBerExplorer() {
  const [sigma_ps, setSigma] = useState(4.0); // rms RJ [ps]
  const [ui_ps, setUI] = useState(100.0);     // UI [ps]

  const sigma = sigma_ps, ui = ui_ps; // work in ps
  const N = 240;
  const ber = (t) => Math.max(0.5 * (Q((ui / 2 - t) / sigma) + Q((ui / 2 + t) / sigma)), 1e-300);

  const pts = [];
  let openL = null, openR = null;
  for (let i = 0; i <= N; i++) {
    const t = -ui / 2 + (ui * i) / N;        // sampling offset [ps]
    const b = ber(t);
    pts.push([t, b]);
    if (b < 1e-12) { if (openL === null) openL = t; openR = t; }
  }
  const opening = openL !== null ? (openR - openL) : 0; // ps at BER<1e-12
  const openingUI = opening / ui;

  const X = (t) => PAD + ((t + ui / 2) / ui) * (W - 2 * PAD);
  const Y = (b) => {
    const l = Math.max(Math.log10(b), LOGMIN);
    return PAD + (1 - (l - LOGMIN) / (0 - LOGMIN)) * (H - 2 * PAD);
  };
  const poly = pts.map(([t, b]) => `${X(t).toFixed(1)},${Y(b).toFixed(1)}`).join(' ');
  const y12 = Y(1e-12);

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
      <div style={{fontWeight: 600, marginBottom: '0.4rem'}}>SerDes jitter→BER bathtub 探索器（RJ-only）</div>
      <svg viewBox={`0 0 ${W} ${H}`} style={{width: '100%', height: 'auto', background: 'var(--ifm-background-color)', borderRadius: '6px'}}>
        <line x1={PAD} y1={H - PAD} x2={W - PAD} y2={H - PAD} stroke={axis} strokeWidth="1" />
        <line x1={PAD} y1={PAD} x2={PAD} y2={H - PAD} stroke={axis} strokeWidth="1" />
        <line x1={PAD} y1={y12} x2={W - PAD} y2={y12} stroke="var(--ifm-color-danger, #e5534b)" strokeWidth="1" strokeDasharray="4 3" />
        <text x={W - PAD} y={y12 - 4} fontSize="10" fill="var(--ifm-color-danger, #e5534b)" textAnchor="end">BER = 10⁻¹²</text>
        <polyline points={poly} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2" />
        <text x={(W) / 2} y={H - 6} fontSize="11" fill={axis} textAnchor="middle">sampling offset [UI: −0.5 … +0.5]</text>
        <text x={PAD + 4} y={PAD - 6} fontSize="10" fill={axis}>BER (log)</text>
      </svg>
      <Slider label="rms RJ σ_t" value={sigma_ps} unit="ps" min={0.5} max={20} step={0.5} onChange={setSigma} fmt={(v) => v.toFixed(1)} />
      <Slider label="UI (1/鮑率)" value={ui_ps} unit="ps" min={20} max={400} step={5} onChange={setUI} fmt={(v) => v.toFixed(0)} />
      <div style={{display: 'flex', gap: '0.8rem', marginTop: '0.6rem', flexWrap: 'wrap'}}>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>eye 開口 @ 1e-12</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>{(openingUI * 100).toFixed(1)}%</div>
          <div style={{fontSize: '0.78rem'}}>UI（{opening.toFixed(1)} ps）</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>σ_t / UI</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>{(sigma_ps / ui_ps * 100).toFixed(1)}%</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>中心 BER</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>{ber(0).toExponential(1)}</div>
        </div>
      </div>
      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.6rem'}}>
        σ_t 就是把 oscillator phase noise 積分得到的 rms jitter（見
        [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)、[lab_12](/04_simulation_labs/lab_12_serdes_eye_ber)）。
        RJ-only toy model（無 ISI/DJ）。
      </div>
    </div>
  );
}
