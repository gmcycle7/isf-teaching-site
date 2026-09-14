import React, {useState} from 'react';

// Interactive ISF phase-noise / jitter calculator.
// Uses Hajimiri-Lee Eq.(21) for L at a chosen offset, and a 1/f^2-skirt closed
// form for integrated rms jitter (same math as lab_08). Pure client component,
// SSR-safe (no window access at module scope).
//
// "Segment table" mode (measurement_and_spurs.md Sec.3.3): integrates a
// datasheet-style table of (f, L[dBc/Hz]) points using the piecewise
// log-log closed form -- same math as simulations/lab_35's docs-page sibling
// section, verified against np.trapezoid in that page's worked example.

const TWO_PI = 2 * Math.PI;

function Row({label, value, unit, min, max, step, onChange, fmt}) {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0', flexWrap: 'wrap'}}>
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

// Default worked-example table: measurement_and_spurs.md Sec.3.3 canonical
// 6-point datasheet table (f0 = 5 GHz), reproducing sigma_t = 8.45 ps over
// 12 kHz-20 MHz and 448.5 fs over 1-100 MHz.
const DEFAULT_TABLE = [
  {f: 1e3, L: -20.0},
  {f: 1e4, L: -50.0},
  {f: 1e5, L: -80.0},
  {f: 1e6, L: -100.0},
  {f: 1e7, L: -120.0},
  {f: 1e8, L: -139.6},
];

// Piecewise log-log closed-form integral of L(f) df across a table of
// (f, L[dBc/Hz]) points, clipped to [f1, f2]. Within each adjacent pair
// [fa,fb] the local slope exponent is m = log10(Lb_lin/La_lin)/log10(fb/fa)
// (m=-2 for a 1/f^2 segment, m=-3 for 1/f^3, m=0 for a flat floor), and
//   integral(L, f=fa..fb) = La_lin*fa/(m+1) * [(fb/fa)^(m+1) - 1]   (m != -1)
//   integral(L, f=fa..fb) = La_lin*fa*ln(fb/fa)                     (m == -1)
// A segment partially inside [f1,f2] is first clipped by re-evaluating L at
// the clipped endpoints along the same power law, then integrated with the
// clipped endpoint as the new anchor -- mathematically identical to
// re-deriving m from the clipped points (same power law).
function integrateTable(points, f1, f2) {
  const sorted = [...points].sort((a, b) => a.f - b.f);
  let total = 0;
  const detail = [];
  for (let i = 0; i < sorted.length - 1; i++) {
    const fa = sorted[i].f, La = sorted[i].L;
    const fb = sorted[i + 1].f, Lb = sorted[i + 1].L;
    if (!(fb > fa)) continue; // guard against non-increasing/duplicate f
    const segLo = Math.max(fa, f1);
    const segHi = Math.min(fb, f2);
    if (!(segHi > segLo)) continue;
    const LaLin = Math.pow(10, La / 10);
    const LbLin = Math.pow(10, Lb / 10);
    const m = Math.log10(LbLin / LaLin) / Math.log10(fb / fa);
    const Lval = (f) => 10 * Math.log10(LaLin * Math.pow(f / fa, m));
    const L1lin = Math.pow(10, Lval(segLo) / 10);
    let seg;
    if (Math.abs(m + 1) < 1e-9) {
      seg = L1lin * segLo * Math.log(segHi / segLo);
    } else {
      seg = (L1lin * segLo / (m + 1)) * (Math.pow(segHi / segLo, m + 1) - 1);
    }
    total += seg;
    detail.push({segLo, segHi, m, I: seg});
  }
  return {total, detail};
}

export default function PhaseNoiseCalculator() {
  const [mode, setMode] = useState('single');  // 'single' | 'table'
  const [qmax_pC, setQ] = useState(1.0);      // pC
  const [Grms, setG] = useState(0.5);         // dimensionless
  const [logSi, setLogSi] = useState(-24);    // S_i = 10^logSi  [A^2/Hz]
  const [f0_GHz, setF0] = useState(5.0);      // GHz
  const [fref_MHz, setFref] = useState(1.0);  // offset for L [MHz]
  const [f1_MHz, setF1] = useState(1.0);      // integ lower [MHz]
  const [f2_MHz, setF2] = useState(100.0);    // integ upper [MHz]

  // --- segment-table mode state (measurement_and_spurs.md Sec.3.3) ---
  const [table, setTable] = useState(DEFAULT_TABLE);
  const [f1_tbl_Hz, setF1Tbl] = useState(12e3);   // default: SONET/OC-192-style 12 kHz
  const [f2_tbl_Hz, setF2Tbl] = useState(20e6);   // default: 20 MHz
  const [f0_tbl_GHz, setF0Tbl] = useState(5.0);

  function updateTablePoint(idx, key, val) {
    const next = table.map((p, i) => (i === idx ? {...p, [key]: val} : p));
    setTable(next);
  }

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

  // --- segment-table mode: sigma_phi^2 = 2 * integral(L, df); sigma_t = sigma_phi/(2*pi*f0) ---
  const f0_tbl = f0_tbl_GHz * 1e9;
  const f2_tbl_clamped = Math.max(f2_tbl_Hz, f1_tbl_Hz * 1.0001);
  const {total: tblIntegral} = integrateTable(table, f1_tbl_Hz, f2_tbl_clamped);
  const sigPhiTbl = Math.sqrt(Math.max(2 * tblIntegral, 0));
  const sigTTbl = sigPhiTbl / (TWO_PI * f0_tbl);

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
  const modeBtn = (active) => ({
    padding: '0.3rem 0.8rem', borderRadius: '6px', fontSize: '0.85rem', cursor: 'pointer',
    border: active ? '1px solid var(--ifm-color-primary)' : '1px solid var(--ifm-color-emphasis-300)',
    background: active ? 'var(--ifm-color-primary)' : 'var(--ifm-background-color)',
    color: active ? 'white' : 'inherit', fontWeight: active ? 600 : 400,
  });
  const tblInput = {
    width: '6.5rem', fontSize: '0.85rem', padding: '0.15rem 0.35rem',
    border: '1px solid var(--ifm-color-emphasis-300)', borderRadius: '4px',
  };

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        ISF 相位雜訊 / jitter 互動計算器
      </div>
      <div style={{display: 'flex', gap: '0.5rem', marginBottom: '0.7rem'}}>
        <button type="button" style={modeBtn(mode === 'single')} onClick={() => setMode('single')}>
          單一 1/f² skirt
        </button>
        <button type="button" style={modeBtn(mode === 'table')} onClick={() => setMode('table')}>
          datasheet 分段表（6 點）
        </button>
      </div>

      {mode === 'single' && (
        <>
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
        </>
      )}

      {mode === 'table' && (
        <>
          <div style={{fontSize: '0.82rem', opacity: 0.85, marginBottom: '0.5rem'}}>
            對應 <code>measurement_and_spurs.md</code> §3.3：分段 log–log 閉式積分。
            預設值為該節 worked example（12 kHz–20 MHz → σ_t≈8.45 ps）；可自行編輯 6 個
            (f, L) 點與積分範圍。
          </div>
          <div style={{overflowX: 'auto'}}>
            <table style={{borderCollapse: 'collapse', fontSize: '0.82rem'}}>
              <thead>
                <tr>
                  <th style={{textAlign: 'left', padding: '0.2rem 0.6rem 0.2rem 0'}}>#</th>
                  <th style={{textAlign: 'left', padding: '0.2rem 0.6rem'}}>f [Hz]</th>
                  <th style={{textAlign: 'left', padding: '0.2rem 0.6rem'}}>L [dBc/Hz]</th>
                </tr>
              </thead>
              <tbody>
                {table.map((p, i) => (
                  <tr key={i}>
                    <td style={{padding: '0.2rem 0.6rem 0.2rem 0', opacity: 0.6}}>{i + 1}</td>
                    <td style={{padding: '0.2rem 0.6rem'}}>
                      <input type="number" style={tblInput} value={p.f}
                             onChange={(e) => updateTablePoint(i, 'f', parseFloat(e.target.value))} />
                    </td>
                    <td style={{padding: '0.2rem 0.6rem'}}>
                      <input type="number" style={tblInput} value={p.L}
                             onChange={(e) => updateTablePoint(i, 'L', parseFloat(e.target.value))} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.6rem 0', flexWrap: 'wrap'}}>
            <label style={{fontSize: '0.9rem'}}>積分下限 f₁ [Hz]</label>
            <input type="number" style={tblInput} value={f1_tbl_Hz}
                   onChange={(e) => setF1Tbl(parseFloat(e.target.value))} />
            <label style={{fontSize: '0.9rem'}}>積分上限 f₂ [Hz]</label>
            <input type="number" style={tblInput} value={f2_tbl_Hz}
                   onChange={(e) => setF2Tbl(parseFloat(e.target.value))} />
            <label style={{fontSize: '0.9rem'}}>f₀ [GHz]</label>
            <input type="number" style={tblInput} value={f0_tbl_GHz}
                   onChange={(e) => setF0Tbl(parseFloat(e.target.value))} />
            <button type="button" style={modeBtn(false)} onClick={() => {
              setTable(DEFAULT_TABLE); setF1Tbl(12e3); setF2Tbl(20e6); setF0Tbl(5.0);
            }}>
              重設為 worked example
            </button>
          </div>

          <div style={out}>
            <div style={card}>
              <div style={{fontSize: '0.8rem', opacity: 0.7}}>∫L df</div>
              <div style={{fontSize: '1.3rem', fontWeight: 700}}>{tblIntegral.toExponential(3)}</div>
              <div style={{fontSize: '0.8rem'}}>(linear·Hz)</div>
            </div>
            <div style={card}>
              <div style={{fontSize: '0.8rem', opacity: 0.7}}>σ_φ</div>
              <div style={{fontSize: '1.3rem', fontWeight: 700}}>{(sigPhiTbl * 1e3).toFixed(2)}</div>
              <div style={{fontSize: '0.8rem'}}>mrad</div>
            </div>
            <div style={card}>
              <div style={{fontSize: '0.8rem', opacity: 0.7}}>σ_t (rms jitter)</div>
              <div style={{fontSize: '1.3rem', fontWeight: 700}}>
                {sigTTbl * 1e12 >= 1 ? (sigTTbl * 1e12).toFixed(2) : (sigTTbl * 1e15).toFixed(1)}
              </div>
              <div style={{fontSize: '0.8rem'}}>{sigTTbl * 1e12 >= 1 ? 'ps' : 'fs'}</div>
            </div>
          </div>
          <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem'}}>
            分段 log–log 閉式：相鄰點 [f_a,f_b] 的斜率指數 m=log₁₀(L_b,lin/L_a,lin)/log₁₀(f_b/f_a)；
            ∫L df=L_a,lin·f_a/(m+1)·[(f_b/f_a)^(m+1)−1]（m≠−1，m=−1 時用 L_a,lin·f_a·ln(f_b/f_a)）；
            σ_φ²=2·Σ段積分、σ_t=σ_φ/(2π f₀)。與 <code>measurement_and_spurs.md</code> §3.3、
            <code>simulations/lab_35_xcorr_measurement.py</code> 頁面附近的手算數值同一組公式。
          </div>
        </>
      )}
    </div>
  );
}
