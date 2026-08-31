import React, {useState} from 'react';
import useIsEn from './useIsEn';

// "畫波形 → 看 ISF 與 phase noise" sandbox.
//
// Waveform model: phase-warped, soft-clipped sine V(θ), θ ∈ [0, 2π), 512 pts.
//   A = rise/fall slope ratio f'_rise/f'_fall at the zero crossings
//       (implemented as warp slopes r1 = sqrt(A), r2 = 1/sqrt(A));
//   s = squareness: V = tanh(k·sin u)/tanh(k), k = 6s (s=0 → exact sine);
//   d = duty: V > 0 for θ ∈ (0, 2πd).
// The warp u(θ) is piecewise quadratic (u' is a piecewise-linear "tent"), so
// u(2π) = 2π exactly and the waveform is exactly periodic.
//
// ISF: [P2]-Appendix-style SLOPE APPROXIMATION, per-edge normalized:
//   Γ(θ) = −V'(θ)/f'²_max,edge   (rising / falling edge each normalized by its
//   own maximum slope). This is what makes rise/fall asymmetry produce c0 ≠ 0
//   — the flicker-upconversion knob of [P1] Eq.(24). NOT an exact PPV; a
//   single global max-slope normalization would force c0 ≡ 0 (∮V'dθ = 0).
//
// Numbers cross-checked against a python implementation of the same formulas
// (512-pt grid, central differences, rectangle-rule Fourier sums):
//   sine anchor (A=1, s=0, d=0.5, qmax=1 pC):
//     Γrms = 0.7071, |c1| = 1.0000, c0 ≈ 0, corner = 0,
//     L(1 MHz) = −145.0 dBc/Hz  ([P1] Eq.(21), SSB /4, Si = 1e-24 A²/Hz).
//   A=2, s=0.5, d=0.5 → c0 = 0.104, corner = 218 kHz;
//   A=5, s=0.5, d=0.5 → c0 = 0.328, corner = 600 kHz, Γrms = 0.300.
// Pure client component, SSR-safe (no window access at module scope).

const TWO_PI = 2 * Math.PI;
const NPTS = 512;
const W = 520;          // SVG width (viewBox units)
const PH = 150;         // plot height
const PADX = 30, PADY = 20;

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

// waveform + ISF + Fourier, all on a 512-point grid
function computeAll(A, s, d) {
  const r1 = Math.sqrt(A);
  const r2 = 1 / Math.sqrt(A);
  const thf = TWO_PI * d;                              // fall zero crossing
  const mh = (4 * Math.PI / thf - r1 - r2) / 2;        // mid warp slope, high half
  const ml = (4 * Math.PI / (TWO_PI - thf) - r1 - r2) / 2; // low half
  const tha = thf / 2;
  const thc = thf + (TWO_PI - thf) / 2;
  const uTha = tha * (r1 + mh) / 2;
  const uThf = uTha + (thf - tha) * (mh + r2) / 2;     // = π by construction
  const uThc = uThf + (thc - thf) * (r2 + ml) / 2;
  const uOf = (t) => {
    if (t <= tha) return r1 * t + (mh - r1) * t * t / (2 * tha);
    if (t <= thf) {
      const x = t - tha, L = thf - tha;
      return uTha + mh * x + (r2 - mh) * x * x / (2 * L);
    }
    if (t <= thc) {
      const x = t - thf, L = thc - thf;
      return uThf + r2 * x + (ml - r2) * x * x / (2 * L);
    }
    const x = t - thc, L = TWO_PI - thc;
    return uThc + ml * x + (r1 - ml) * x * x / (2 * L);
  };
  const k = 6 * s;
  const tk = k >= 1e-6 ? Math.tanh(k) : 1;
  const clip = (x) => (k < 1e-6 ? x : Math.tanh(k * x) / tk);

  const th = new Array(NPTS), V = new Array(NPTS);
  for (let i = 0; i < NPTS; i++) {
    th[i] = TWO_PI * i / NPTS;
    V[i] = clip(Math.sin(uOf(th[i])));
  }
  // periodic central difference dV/dθ
  const dth = TWO_PI / NPTS;
  const Vp = new Array(NPTS);
  for (let i = 0; i < NPTS; i++) {
    Vp[i] = (V[(i + 1) % NPTS] - V[(i - 1 + NPTS) % NPTS]) / (2 * dth);
  }
  // per-edge max slopes
  let Mr = 0, Mf = 0;
  for (let i = 0; i < NPTS; i++) {
    if (Vp[i] > Mr) Mr = Vp[i];
    if (-Vp[i] > Mf) Mf = -Vp[i];
  }
  // slope-approximation ISF, each edge normalized by its own max slope
  const gam = Vp.map((v) => (v > 0 ? -v / (Mr * Mr) : -v / (Mf * Mf)));
  // Γrms and Fourier magnitudes c0..c5 (Γ = c0/2 + Σ c_n cos(nθ+θ_n))
  let g2 = 0, sum0 = 0;
  for (let i = 0; i < NPTS; i++) { g2 += gam[i] * gam[i]; sum0 += gam[i]; }
  const grms = Math.sqrt(g2 / NPTS);
  const c0 = (dth / Math.PI) * sum0;
  const cn = [Math.abs(c0)];
  for (let n = 1; n <= 5; n++) {
    let a = 0, b = 0;
    for (let i = 0; i < NPTS; i++) {
      a += gam[i] * Math.cos(n * th[i]);
      b += gam[i] * Math.sin(n * th[i]);
    }
    cn.push(Math.hypot((dth / Math.PI) * a, (dth / Math.PI) * b));
  }
  return {V, gam, grms, c0, cn, Mr, Mf};
}

function polyline(arr, ymax) {
  const pts = [];
  for (let i = 0; i < arr.length; i++) {
    const x = PADX + (i / (arr.length - 1)) * (W - 2 * PADX);
    const y = PH / 2 - (arr[i] / ymax) * (PH / 2 - PADY);
    pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
  }
  return pts.join(' ');
}

export default function IsfSandbox() {
  const isEn = useIsEn();
  const [A, setA] = useState(1.0);        // f'_rise / f'_fall
  const [sq, setSq] = useState(0.0);      // squareness 0..1
  const [duty, setDuty] = useState(0.5);  // 0.3..0.7
  const [f0GHz, setF0] = useState(5.0);   // GHz
  const [qmaxPC, setQ] = useState(1.0);   // pC

  const {V, gam, grms, c0, cn, Mr} = computeAll(A, sq, duty);

  // --- phase noise, [P1] Eq.(21) (SSB /4), Si = 1e-24 A²/Hz, offset 1 MHz ---
  const Si = 1e-24;
  const qmax = qmaxPC * 1e-12;
  const dw = TWO_PI * 1e6;
  const Llin = (grms * grms / (qmax * qmax)) * Si / (4 * dw * dw);
  const Ldbc = 10 * Math.log10(Llin);
  // --- 1/f³ corner, [P1] Eq.(24): Δf_corner = c0²/(2Γrms²)·f_1/f, f_1/f = 1 MHz ---
  const cornerKHz = (c0 * c0 / (2 * grms * grms)) * 1e6 / 1e3;
  // f0 only sets the time scale of one period (Eq.(21) at a fixed 1-MHz offset
  // has no explicit f0); also convert the steepest edge to a slew rate.
  const Tps = 1000 / f0GHz;                       // T = 1/f0 in ps
  const slewVns = Mr * TWO_PI * f0GHz;            // V'(θ)·ω0, amp = 1 V → V/ns

  // --- plot scalings ---
  const gmax = Math.max(0.1, ...gam.map(Math.abs)) * 1.12;
  const xZC = PADX + duty * (W - 2 * PADX);       // fall zero crossing
  const barMax = Math.max(1e-6, ...cn);
  const BH = 118, barW = 40;
  const slot = (W - 2 * PADX) / 6;

  const axis = 'var(--ifm-color-emphasis-400)';
  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)', borderRadius: '8px',
    padding: '1rem 1.1rem', margin: '1rem 0', background: 'var(--ifm-color-emphasis-100)',
  };
  const svgStyle = {
    width: '100%', height: 'auto', background: 'var(--ifm-background-color)',
    borderRadius: '6px', display: 'block',
  };
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.6rem 0.8rem', textAlign: 'center',
  };
  const small = {fontSize: '0.78rem', opacity: 0.7};

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'ISF sandbox: draw a waveform → see the ISF and phase noise'
          : 'ISF sandbox：畫波形 → 看 ISF 與 phase noise'}
      </div>

      <Row label={isEn ? 'Slope ratio A = f′rise/f′fall' : '斜率比 A = f′rise/f′fall'} value={A} unit="" min={0.2} max={5} step={0.05}
           onChange={setA} fmt={(v) => v.toFixed(2)} />
      <Row label={isEn ? 'Squareness (0=sine, 1=near-square)' : '方形度（0=正弦，1=近方波）'} value={sq} unit="" min={0} max={1} step={0.01}
           onChange={setSq} fmt={(v) => v.toFixed(2)} />
      <Row label={isEn ? 'Duty (fraction with V>0)' : 'duty（V＞0 佔比）'} value={duty} unit="" min={0.3} max={0.7} step={0.01}
           onChange={setDuty} fmt={(v) => v.toFixed(2)} />
      <Row label="f₀" value={f0GHz} unit="GHz" min={1} max={10} step={0.1}
           onChange={setF0} fmt={(v) => v.toFixed(1)} />
      <Row label="q_max" value={qmaxPC} unit="pC" min={0.2} max={3} step={0.05}
           onChange={setQ} fmt={(v) => v.toFixed(2)} />

      {/* waveform V(θ) */}
      <svg viewBox={`0 0 ${W} ${PH}`} role="img" aria-label="Waveform V(theta) over one period"
           style={{...svgStyle, marginTop: '0.6rem'}}>
        <line x1={PADX} y1={PH / 2} x2={W - PADX} y2={PH / 2} stroke={axis} strokeWidth="1" />
        <line x1={PADX} y1={PADY} x2={PADX} y2={PH - PADY} stroke={axis} strokeWidth="1" />
        <line x1={xZC} y1={PADY} x2={xZC} y2={PH - PADY} stroke={axis} strokeWidth="1" strokeDasharray="4 4" />
        <polyline points={polyline(V, 1.15)} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2" />
        <text x={PADX + 4} y={PADY + 2} fontSize="11" fill={axis}>{isEn ? 'V(θ) (normalized, amplitude 1)' : 'V(θ)（normalized，振幅 1）'}</text>
        <text x={W - PADX} y={PH / 2 + 14} fontSize="11" fill={axis} textAnchor="end">θ = 2π</text>
        <text x={xZC + 4} y={PH - PADY - 4} fontSize="10" fill={axis}>{isEn ? 'fall ZC' : 'fall ZC'}</text>
      </svg>
      <div style={{...small, margin: '0.15rem 0 0.5rem'}}>
        {isEn
          ? `One period T = 1/f₀ = ${Tps.toFixed(1)} ps; the steepest edge's slew ≈ (dV/dθ)·ω₀ = ${slewVns.toFixed(1)} V/ns (amplitude 1 V).`
          : `一個週期 T = 1/f₀ = ${Tps.toFixed(1)} ps；最陡 edge 的 slew ≈ (dV/dθ)·ω₀ = ${slewVns.toFixed(1)} V/ns（振幅 1 V）。`}
      </div>

      {/* ISF Γ(θ) */}
      <svg viewBox={`0 0 ${W} ${PH}`} role="img" aria-label="Slope-approximation ISF Gamma(theta) derived from the waveform"
           style={svgStyle}>
        <line x1={PADX} y1={PH / 2} x2={W - PADX} y2={PH / 2} stroke={axis} strokeWidth="1" />
        <line x1={PADX} y1={PADY} x2={PADX} y2={PH - PADY} stroke={axis} strokeWidth="1" />
        <line x1={xZC} y1={PADY} x2={xZC} y2={PH - PADY} stroke={axis} strokeWidth="1" strokeDasharray="4 4" />
        <polyline points={polyline(gam, gmax)} fill="none" stroke="var(--ifm-color-danger, #e5534b)" strokeWidth="2" />
        <text x={PADX + 4} y={PADY + 2} fontSize="11" fill={axis}>{isEn ? 'Γ(θ)  max = ' : 'Γ(θ)　max = '}{gmax === 0 ? '0' : (gmax / 1.12).toFixed(2)}</text>
        <text x={W - PADX} y={PH / 2 + 14} fontSize="11" fill={axis} textAnchor="end">θ = 2π</text>
      </svg>
      <div style={{...small, margin: '0.15rem 0 0.5rem'}}>
        {isEn ? (
          <>
            The ISF is a <b>slope approximation ([P2] Appendix approach), not an exact PPV</b>:
            Γ(θ) = −V′(θ)/f′²_max, with the rising and falling edges each normalized by their own
            maximum slope (a single global normalization would force c₀ to be identically 0).
          </>
        ) : (
          <>
            ISF 為 <b>slope 近似（[P2] Appendix 思路），非 exact PPV</b>：Γ(θ) = −V′(θ)/f′²_max，
            上升沿與下降沿各用自己的最大斜率歸一（單一全域歸一會讓 c₀ 恆為 0）。
          </>
        )}
      </div>

      {/* |c_n| bars */}
      <svg viewBox={`0 0 ${W} ${BH}`} role="img" aria-label="Fourier coefficient magnitudes c0 through c5 of the ISF"
           style={svgStyle}>
        <line x1={PADX} y1={BH - 18} x2={W - PADX} y2={BH - 18} stroke={axis} strokeWidth="1" />
        {cn.map((c, n) => {
          const h = (c / barMax) * (BH - 44);
          const x = PADX + n * slot + (slot - barW) / 2;
          const y = BH - 18 - h;
          return (
            <g key={n}>
              <rect x={x} y={y} width={barW} height={Math.max(h, 0.5)}
                    fill={n === 0 ? 'var(--ifm-color-danger, #e5534b)' : 'var(--ifm-color-primary)'}
                    opacity="0.85" rx="2" />
              <text x={x + barW / 2} y={y - 4} fontSize="10" fill={axis} textAnchor="middle">
                {c.toFixed(3)}
              </text>
              <text x={x + barW / 2} y={BH - 5} fontSize="11" fill={axis} textAnchor="middle">
                {'c' + String.fromCharCode(0x2080 + n)}
              </text>
            </g>
          );
        })}
      </svg>

      {/* readouts */}
      <div style={{display: 'flex', gap: '0.8rem', flexWrap: 'wrap', marginTop: '0.8rem'}}>
        <div style={card}>
          <div style={small}>Γ_rms</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{grms.toFixed(3)}</div>
        </div>
        <div style={card}>
          <div style={small}>{isEn ? 'c₀ (signed)' : 'c₀（含正負號）'}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{c0.toFixed(3)}</div>
        </div>
        <div style={card}>
          <div style={small}>L(1 MHz) — [P1] Eq.(21)</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{Ldbc.toFixed(1)}</div>
          <div style={small}>dBc/Hz</div>
        </div>
        <div style={card}>
          <div style={small}>1/f³ corner — [P1] Eq.(24)</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{cornerKHz.toFixed(1)}</div>
          <div style={small}>kHz</div>
        </div>
      </div>

      <div style={{...small, marginTop: '0.7rem'}}>
        {isEn ? (
          <>
            Model: 512-point numerical computation. L(1 MHz) uses [P1] Eq.(21) (SSB /4 convention)
            with a fixed S_i = 10⁻²⁴ A²/Hz; 1/f³ corner = c₀²/(2Γ_rms²)·f₁/f, f₁/f = 1 MHz ([P1]
            Eq.(24)). f₀ only rescales the time axis and the slew (at a fixed offset, Eq.(21) has
            no explicit f₀ dependence).
            <b> Anchor point (numerically verified)</b>: sine setting (A=1, squareness 0, duty 0.5,
            q_max=1 pC) → Γ_rms = 0.707, |c₁| = 1.000, c₀ ≈ 0, corner = 0, L(1 MHz) = −145.0 dBc/Hz
            (Example B's −148.0 dBc/Hz corresponds to Γ_rms = 0.5; 0.707 is 3.0 dB higher than 0.5).
          </>
        ) : (
          <>
            模型：512 點數值計算。L(1 MHz) 用 [P1] Eq.(21)（SSB /4 記帳），固定 S_i = 10⁻²⁴ A²/Hz；
            1/f³ corner = c₀²/(2Γ_rms²)·f₁/f，f₁/f = 1 MHz（[P1] Eq.(24)）。f₀ 只換算時間刻度與 slew
            （固定 offset 下 Eq.(21) 不顯含 f₀）。
            <b>錨點（已數值驗證）</b>：正弦設定（A=1、方形度 0、duty 0.5、q_max=1 pC）→
            Γ_rms = 0.707、|c₁| = 1.000、c₀ ≈ 0、corner = 0、L(1 MHz) = −145.0 dBc/Hz
            （例B 的 −148.0 dBc/Hz 對應 Γ_rms = 0.5；0.707 比 0.5 高 3.0 dB）。
          </>
        )}
      </div>
    </div>
  );
}
