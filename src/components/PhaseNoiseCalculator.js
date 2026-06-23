import React, {useState} from 'react';

// Interactive ISF phase-noise / jitter calculator.
// Uses Hajimiri-Lee Eq.(21) for L at a chosen offset, and a 1/f^2-skirt closed
// form for integrated rms jitter (same math as lab_08). Pure client component,
// SSR-safe (no window access at module scope).

const TWO_PI = 2 * Math.PI;

function Row({label, value, unit, min, max, step, onChange, fmt}) {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0'}}>
      <label style={{flex: '0 0 11rem', fontSize: '0.9rem'}}>{label}</label>
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

export default function PhaseNoiseCalculator() {
  const [qmax_pC, setQ] = useState(1.0);      // pC
  const [Grms, setG] = useState(0.5);         // dimensionless
  const [logSi, setLogSi] = useState(-24);    // S_i = 10^logSi  [A^2/Hz]
  const [f0_GHz, setF0] = useState(5.0);      // GHz
  const [fref_MHz, setFref] = useState(1.0);  // offset for L [MHz]
  const [f1_MHz, setF1] = useState(1.0);      // integ lower [MHz]
  const [f2_MHz, setF2] = useState(100.0);    // integ upper [MHz]

  // --- physics ---
  const qmax = qmax_pC * 1e-12;
  const Si = Math.pow(10, logSi);
  const f0 = f0_GHz * 1e9;
  const fref = fref_MHz * 1e6;
  const dw = TWO_PI * fref;
  // Eq.(21): L = 10log10[ (Grms^2/qmax^2) * Si / (4 dw^2) ]   (Si = i^2/df)
  const Llin = (Grms * Grms / (qmax * qmax)) * Si / (4 * dw * dw);
  const L_dbc = 10 * Math.log10(Llin);

  // 1/f^2 skirt anchored at (fref, L_dbc): sigma_phi^2 = 2 Lref f_ref^2 (1/f1 - 1/f2)
  const f1 = f1_MHz * 1e6, f2 = Math.max(f2_MHz * 1e6, f1_MHz * 1e6 * 1.0001);
  const Lref_lin = Math.pow(10, L_dbc / 10);
  const sigPhi2 = 2 * Lref_lin * fref * fref * (1 / f1 - 1 / f2);
  const sigPhi = Math.sqrt(Math.max(sigPhi2, 0));
  const sigT = sigPhi / (TWO_PI * f0);

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const out = {
    display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem',
  };
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.6rem 0.8rem', textAlign: 'center',
  };

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        ISF 相位雜訊 / jitter 互動計算器
      </div>
      <Row label="q_max" value={qmax_pC} unit="pC" min={0.1} max={10} step={0.1}
           onChange={setQ} fmt={(v) => v.toFixed(1)} />
      <Row label="Γ_rms" value={Grms} unit="" min={0.05} max={1.5} step={0.01}
           onChange={setG} fmt={(v) => v.toFixed(2)} />
      <Row label="S_i = 10^x" value={logSi} unit="A²/Hz (log)" min={-26} max={-20} step={0.1}
           onChange={setLogSi} fmt={(v) => v.toFixed(1)} />
      <Row label="f₀" value={f0_GHz} unit="GHz" min={0.5} max={30} step={0.5}
           onChange={setF0} fmt={(v) => v.toFixed(1)} />
      <Row label="offset (for L)" value={fref_MHz} unit="MHz" min={0.1} max={50} step={0.1}
           onChange={setFref} fmt={(v) => v.toFixed(1)} />
      <Row label="integrate from f₁" value={f1_MHz} unit="MHz" min={0.01} max={50} step={0.01}
           onChange={setF1} fmt={(v) => v.toFixed(2)} />
      <Row label="integrate to f₂" value={f2_MHz} unit="MHz" min={1} max={1000} step={1}
           onChange={setF2} fmt={(v) => v.toFixed(0)} />

      <div style={out}>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>L(offset) — Eq.(21)</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{L_dbc.toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>dBc/Hz</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>σ_φ ({f1_MHz}–{f2_MHz} MHz)</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{(sigPhi * 1e3).toFixed(2)}</div>
          <div style={{fontSize: '0.8rem'}}>mrad</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>σ_t (rms jitter)</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{(sigT * 1e15).toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>fs</div>
        </div>
      </div>
      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem'}}>
        模型：單一白噪源、1/f² skirt（toy）。L = 10·log₁₀[Γ_rms²/q_max² · S_i/(4Δω²)]；
        σ_t = √(2·L_lin·f_ref²·(1/f₁−1/f₂)) / (2π f₀)。對應 lab_06 / lab_08。
      </div>
    </div>
  );
}
