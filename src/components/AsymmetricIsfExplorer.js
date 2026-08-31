import React, {useState} from 'react';
import useIsEn from './useIsEn';

// AsymmetricIsfExplorer — [P2] Appendix B closed-form explorer for the
// asymmetric triangular ring-oscillator ISF (Fig. 18, p.803).
//
// Verbatim closed forms (see docs/03_isf_core_theory/asymmetric_isf_closed_form.md):
//   Eq.(55): Gamma_rms^2 = (2*pi^2 / (3*eta^3)) * (1/N^3) * [4(1+A^3)/(1+A)^3]
//   Eq.(56): Gamma_dc    = (2*pi/eta^2) * (1/N^2) * (1-A)/(1+A)
//            c0 = 2*Gamma_dc  (DC Fourier coefficient, c0/2 = DC value)
//   Eq.(57): f_{1/f^3}   = f_{1/f} * (3/(2*eta*N)) * (1-A)^2/(1-A+A^2)
// where A = f'_rise/f'_fall (waveform asymmetry ratio, Eq.53) and eta ~= 1
// is the per-stage delay proportionality constant (Eq.14).
//
// Shape model (Fig.18, p.803): one positive triangular lobe (rising edge)
// of peak height 1/f'_rise and base width 2/f'_rise, one negative lobe
// (falling edge) of depth 1/f'_fall and base width 2/f'_fall -- unit-slope
// (+-1) sides. Peak heights come from the period constraint Eq.(54):
//   1/f'_rise = 2*pi / (eta*N*(1+A)),   1/f'_fall = A/f'_rise.
// Valid only when the two lobes do not overlap: N >= 2/eta (page's own
// "適用/失效條件" table). Sliders allow N,A,eta combinations that violate
// this; the widget flags it rather than silently drawing a wrong picture.
//
// Pedagogical toy model (linear-ramp triangular ISF), not transistor-level.
// Pure client component, SSR-safe (no window/document access), no external
// deps, inline SVG.

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

const TWO_PI = 2 * Math.PI;

function computeClosedForm(N, A, eta) {
  const grms2 = (2 * Math.PI * Math.PI / (3 * eta ** 3)) * (1 / (N ** 3)) * (4 * (1 + A ** 3) / (1 + A) ** 3);
  const grms = Math.sqrt(Math.max(grms2, 0));
  const gdc = (2 * Math.PI / (eta * eta)) * (1 / (N * N)) * (1 - A) / (1 + A);
  const c0 = 2 * gdc;
  // f_{1/f^3} = f_{1/f} * 3/(2 eta N) * (1-A)^2/(1-A+A^2)
  const cornerRatio = (3 / (2 * eta * N)) * ((1 - A) ** 2) / (1 - A + A * A);
  return {grms2, grms, gdc, c0, cornerRatio};
}

// Triangular Gamma(x) shape, x in [0, 2*pi): positive lobe (rising edge)
// placed at the start, negative lobe (falling edge) placed right after it.
function gammaShape(x, hRise, wRise, hFall, wFall) {
  // Positive lobe: triangle of base wRise centered so that it starts at 0.
  if (x < wRise) {
    const half = wRise / 2;
    const d = Math.abs(x - half);
    return hRise * (1 - d / half);
  }
  const x2 = x - wRise;
  if (x2 < wFall) {
    const half = wFall / 2;
    const d = Math.abs(x2 - half);
    return -hFall * (1 - d / half);
  }
  return 0;
}

export default function AsymmetricIsfExplorer() {
  const isEn = useIsEn();
  const [N, setN] = useState(5);
  const [A, setA] = useState(3);
  const [f1f, setF1f] = useState(1.0); // MHz
  const [eta, setEta] = useState(1.0);

  const {grms2, grms, gdc, c0, cornerRatio} = computeClosedForm(N, A, eta);
  const cornerMHz = f1f * cornerRatio;
  const cornerP1MHz = 2 * cornerMHz; // [P1] Eq.(24) convention flag (=2x)

  const overlapOk = N >= 2 / eta;

  // --- ISF shape geometry (Fig.18 unit-slope lobes) ---
  const hRise = TWO_PI / (eta * N * (1 + A));
  const hFall = hRise * A;
  const wRise = 2 * hRise;
  const wFall = 2 * hFall;

  const W = 460, H = 200, PAD = 34;
  const xs = [];
  const NS = 400;
  for (let i = 0; i <= NS; i++) xs.push((i / NS) * TWO_PI);
  const ys = xs.map((x) => gammaShape(x, hRise, wRise, hFall, wFall));
  const yMaxAbs = Math.max(hRise, hFall, 0.05) * 1.15;
  const X = (x) => PAD + (x / TWO_PI) * (W - 2 * PAD);
  const Y = (y) => H / 2 - (y / yMaxAbs) * (H / 2 - PAD * 0.5);
  const poly = xs.map((x, i) => `${X(x).toFixed(1)},${Y(ys[i]).toFixed(1)}`).join(' ');
  const gdcY = Y(gdc);

  // --- mini corner-vs-A curve (Fig.17-style V), at current N, eta ---
  const AW = 300, AH = 140, APAD = 30;
  const logAmin = Math.log10(0.2), logAmax = Math.log10(5);
  const aPts = [];
  const NAC = 120;
  for (let i = 0; i <= NAC; i++) {
    const la = logAmin + (i / NAC) * (logAmax - logAmin);
    const a = Math.pow(10, la);
    const ratio = (3 / (2 * eta * N)) * ((1 - a) ** 2) / (1 - a + a * a);
    aPts.push([la, ratio]);
  }
  const maxRatio = Math.max(...aPts.map((p) => p[1]), cornerRatio) * 1.1 || 1;
  const AX = (la) => APAD + ((la - logAmin) / (logAmax - logAmin)) * (AW - 2 * APAD);
  const AY = (r) => AH - APAD * 0.6 - (r / maxRatio) * (AH - APAD * 1.1);
  const aPoly = aPts.map(([la, r]) => `${AX(la).toFixed(1)},${AY(r).toFixed(1)}`).join(' ');
  const curLogA = Math.log10(A);
  const curX = AX(Math.max(logAmin, Math.min(logAmax, curLogA)));
  const curY = AY(cornerRatio);

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.6rem 0.8rem', textAlign: 'center',
  };
  const axisColor = 'var(--ifm-color-emphasis-400)';
  const panelsRow = {display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-start'};
  const panel = {flex: '1 1 20rem', minWidth: '260px'};

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Asymmetric triangular ISF explorer ([P2] Appendix B, Eqs. 52–57)'
          : '非對稱三角 ISF 探索器（[P2] 附錄 B, Eq.52–57）'}
      </div>

      <Row label="N (級數 stages)" value={N} unit="" min={3} max={15} step={1}
           onChange={(v) => setN(Math.round(v))} fmt={(v) => v.toFixed(0)} />
      <Row label="A = f'rise/f'fall" value={A} unit="" min={0.2} max={5} step={0.05}
           onChange={setA} fmt={(v) => v.toFixed(2)} />
      <Row label="f_{1/f} (device corner)" value={f1f} unit="MHz" min={0.1} max={10} step={0.1}
           onChange={setF1f} fmt={(v) => v.toFixed(1)} />
      <Row label="η (stage-delay const.)" value={eta} unit="" min={0.5} max={1.5} step={0.05}
           onChange={setEta} fmt={(v) => v.toFixed(2)} />

      {!overlapOk && (
        <div role="status" aria-live="polite" style={{
          fontSize: '0.8rem', color: 'var(--ifm-color-danger)', margin: '0.4rem 0',
          border: '1px solid var(--ifm-color-danger)', borderRadius: '6px', padding: '0.4rem 0.6rem',
        }}>
          {isEn
            ? `Warning: lobes overlap here (need N ≥ 2/η = ${(2 / eta).toFixed(2)}). The triangular model's non-overlap assumption is violated — shape and closed forms are outside their validity range.`
            : `警告：目前兩葉重疊（需 N ≥ 2/η = ${(2 / eta).toFixed(2)}）。三角模型「兩葉不重疊」的前提已失效，此處的形狀與閉式解已超出適用範圍。`}
        </div>
      )}

      <div style={panelsRow}>
        <div style={panel}>
          <div style={{fontSize: '0.82rem', opacity: 0.75, marginBottom: '0.25rem'}}>
            {isEn ? 'Γ(x) — Fig. 18 triangular lobes' : 'Γ(x) — Fig.18 三角葉形狀'}
          </div>
          <svg viewBox={`0 0 ${W} ${H}`} role="img"
               aria-label="Asymmetric triangular ISF shape"
               style={{width: '100%', height: 'auto', background: 'var(--ifm-background-color)', borderRadius: '6px'}}>
            <line x1={PAD} y1={H / 2} x2={W - PAD} y2={H / 2} stroke={axisColor} strokeWidth="1" />
            <line x1={PAD} y1={PAD * 0.3} x2={PAD} y2={H - PAD * 0.3} stroke={axisColor} strokeWidth="1" />
            <line x1={PAD} y1={gdcY} x2={W - PAD} y2={gdcY}
                  stroke="var(--ifm-color-primary)" strokeWidth="1" strokeDasharray="4 3" opacity="0.6" />
            <polyline points={poly} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2" />
            <text x={W - PAD} y={H / 2 + 16} fontSize="10.5" fill={axisColor} textAnchor="end">x = 2π</text>
            <text x={PAD} y={PAD * 0.3 - 4} fontSize="10.5" fill={axisColor}>Γ(x)</text>
            <text x={W - PAD} y={gdcY - 4} fontSize="10" fill="var(--ifm-color-primary)" textAnchor="end">
              Γ_dc = {gdc.toFixed(3)}
            </text>
          </svg>
        </div>

        <div style={panel}>
          <div style={{fontSize: '0.82rem', opacity: 0.75, marginBottom: '0.25rem'}}>
            {isEn ? 'corner / f_{1/f} vs A (log-A, Fig.17-style V)' : 'corner / f_{1/f} 對 A（log 軸，Fig.17 式 V 形谷）'}
          </div>
          <svg viewBox={`0 0 ${AW} ${AH}`} role="img"
               aria-label="1/f^3 corner ratio versus asymmetry A"
               style={{width: '100%', height: 'auto', background: 'var(--ifm-background-color)', borderRadius: '6px'}}>
            <line x1={APAD} y1={AH - APAD * 0.6} x2={AW - APAD} y2={AH - APAD * 0.6} stroke={axisColor} strokeWidth="1" />
            <line x1={APAD} y1={APAD * 0.4} x2={APAD} y2={AH - APAD * 0.6} stroke={axisColor} strokeWidth="1" />
            <polyline points={aPoly} fill="none" stroke="var(--ifm-color-emphasis-600)" strokeWidth="2" />
            <line x1={curX} y1={AH - APAD * 0.6} x2={curX} y2={curY}
                  stroke="var(--ifm-color-primary)" strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />
            <circle cx={curX} cy={curY} r="4.5" fill="var(--ifm-color-primary)" />
            <text x={APAD} y={AH - APAD * 0.6 + 14} fontSize="10" fill={axisColor}>A=0.2</text>
            <text x={AW - APAD} y={AH - APAD * 0.6 + 14} fontSize="10" fill={axisColor} textAnchor="end">A=5</text>
            <text x={(APAD + AW - APAD) / 2} y={AH - APAD * 0.6 + 14} fontSize="10" fill={axisColor} textAnchor="middle">A=1</text>
          </svg>
        </div>
      </div>

      <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem'}}>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>Γ_rms — Eq.(55)</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{grms.toFixed(4)}</div>
          <div style={{fontSize: '0.8rem'}}>{isEn ? 'dimensionless' : '無因次'}</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>c₀ = 2Γ_dc — Eq.(56)</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{c0.toFixed(4)}</div>
          <div style={{fontSize: '0.8rem'}}>{isEn ? 'dimensionless' : '無因次'}</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>f_{'{1/f³}'} — Eq.(57)</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{(cornerMHz * 1000).toFixed(2)}</div>
          <div style={{fontSize: '0.8rem'}}>kHz</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>
            {isEn ? '[P1] Eq.(24) convention (=2×)' : '[P1] Eq.(24) 慣例（=2×）'}
          </div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{(cornerP1MHz * 1000).toFixed(2)}</div>
          <div style={{fontSize: '0.8rem'}}>kHz</div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem'}}>
        {isEn ? (
          <>
            Closed forms ([P2] App. B, verbatim): Γ_rms² = (2π²/3η³)(1/N³)[4(1+A³)/(1+A)³]
            (Eq.55); Γ_dc = (2π/η²N²)(1−A)/(1+A), c₀ = 2Γ_dc (Eq.56); f_{'{1/f³}'} = f_{'{1/f}'}·
            (3/2ηN)·(1−A)²/(1−A+A²) (Eq.57). Sanity anchors: A=1 → c₀=0, corner=0 (exact
            symmetric-lobe cancellation); N=5, A=3, η=1, f_{'{1/f}'}=1&nbsp;MHz → Γ_rms=0.3035,
            c₀=−0.2513, corner=171.43&nbsp;kHz ([P2] Eq.57) / 342.86&nbsp;kHz ([P1] Eq.24
            convention). Pedagogical triangular toy model (linear-ramp edges, unit slope),
            valid only for N ≥ 2/η (non-overlapping lobes); see{' '}
            <a href="/03_isf_core_theory/asymmetric_isf_closed_form">asymmetric_isf_closed_form</a>.
          </>
        ) : (
          <>
            閉式（[P2] 附錄 B，逐字）：Γ_rms² = (2π²/3η³)(1/N³)[4(1+A³)/(1+A)³]（Eq.55）；
            Γ_dc = (2π/η²N²)(1−A)/(1+A)，c₀ = 2Γ_dc（Eq.56）；
            f_{'{1/f³}'} = f_{'{1/f}'}·(3/2ηN)·(1−A)²/(1−A+A²)（Eq.57）。
            健全性錨點：A=1 → c₀=0、corner=0（正負葉精確相消）；
            N=5、A=3、η=1、f_{'{1/f}'}=1&nbsp;MHz → Γ_rms=0.3035、c₀=−0.2513、
            corner=171.43&nbsp;kHz（[P2] Eq.57）／342.86&nbsp;kHz（[P1] Eq.24 慣例）。
            Pedagogical 三角 toy model（線性斜坡邊緣、單位斜率），僅在 N ≥ 2/η（兩葉不重疊）時適用；
            見 <a href="/03_isf_core_theory/asymmetric_isf_closed_form">asymmetric_isf_closed_form</a>。
          </>
        )}
      </div>
    </div>
  );
}
