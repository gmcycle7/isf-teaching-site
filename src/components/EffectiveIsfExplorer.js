import React, {useState} from 'react';
import useIsEn from './useIsEn';

// EffectiveIsfExplorer — Γ×α 對齊 explorer（cyclostationary 閘控）。
//
// Fixed ISF: Gamma(x) = -sin(x) (ideal LC, [P1] derivation). The device's
// noise-modulating function (NMF) alpha(x) is a raised-cosine-ish window
// (same family as simulations/lab_14_cyclostationary_isf.py::nmf_window,
// generalized with a "floor" so alpha in [floor,1] instead of [0,1]):
//
//   raised(x) = 0.5*(1+cos(pi*clip(d/(width/2), -1, 1))),  d = wrapped(x-center)
//   alpha(x)  = floor + (1-floor)*raised(x)
//
// Gamma_eff(x) = Gamma(x)*alpha(x). Sliders: center theta_c (0..360 deg),
// width (10..100% of period -> width_rad = widthFrac*2*pi, matching lab_14's
// width=pi <=> widthFrac=0.5 convention), floor (0..0.5).
//
// Readouts: Gamma_eff,rms (trapezoidal numeric integral, same convention as
// simulations/common/isf_utils.py::gamma_rms), c0_eff (DC Fourier coefficient,
// c0_eff = (1/pi) * integral of Gamma_eff dx, matching
// compute_fourier_coefficients's a0 = (1/pi) int f dx convention -> DC value
// = c0/2), and L-degradation vs the site's canonical stationary example B
// (Gamma_rms=0.5, [P1] Eq.(21)): 10*log10(Gamma_eff_rms^2 / 0.5^2) dB. This
// ratio is independent of the well-known /2 vs /4 SSB-accounting constant in
// Eq.(21) (see white_noise_to_phase_noise.md "factor-of-2" note) because that
// constant is common to numerator and denominator and cancels in a ratio.
//
// Anchor numbers reproduced at width=50% (i.e. lab_14's width=pi), floor=0:
//   stationary Gamma_rms = 0.707
//   center=90 deg (zero crossing, |Gamma|=1, "bad")   -> Gamma_eff,rms ~ 0.395
//   center=0 deg  (peak, Gamma=0, "good"/Colpitts-like) -> Gamma_eff,rms ~ 0.177
// (verified in node; see simulations/lab_14_cyclostationary_isf.py for the
// Python reference that produced the same 0.707/0.395/0.177 triple.)
//
// Pure client component, SSR-safe (no window access at module scope), no
// external deps, inline SVG.

const TWO_PI = 2 * Math.PI;
const DEG = Math.PI / 180;
const N = 361; // sample points around [0, 2*pi]

function wrapPi(d) {
  // wrap an angle difference to (-pi, pi]
  return Math.atan2(Math.sin(d), Math.cos(d));
}

function gammaLc(x) {
  return -Math.sin(x);
}

function alphaWindow(x, centerRad, widthFrac, floor) {
  const width = widthFrac * TWO_PI;
  const d = wrapPi(x - centerRad);
  const clipped = Math.max(-1, Math.min(1, d / (width / 2)));
  const raised = 0.5 * (1 + Math.cos(Math.PI * clipped)); // in [0,1]
  return floor + (1 - floor) * raised;
}

// trapezoidal rms over a uniformly sampled [0, 2*pi] closed interval
function trapzRms(xs, ys) {
  let s = 0;
  for (let i = 0; i < xs.length - 1; i++) {
    s += 0.5 * (ys[i] * ys[i] + ys[i + 1] * ys[i + 1]) * (xs[i + 1] - xs[i]);
  }
  return Math.sqrt(s / TWO_PI);
}

// DC Fourier coefficient c0 = (1/pi) * integral_0^{2pi} f(x) dx  (so DC value = c0/2)
function trapzC0(xs, ys) {
  let s = 0;
  for (let i = 0; i < xs.length - 1; i++) {
    s += 0.5 * (ys[i] + ys[i + 1]) * (xs[i + 1] - xs[i]);
  }
  return s / Math.PI;
}

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

function TraceSvg({xs, ys1, ys2, label1, label2, color1, color2, ymin, ymax, height}) {
  const W = 560, H = height || 130, PAD_L = 34, PAD_R = 10, PAD_T = 10, PAD_B = 18;
  const X = (u) => PAD_L + (u / TWO_PI) * (W - PAD_L - PAD_R);
  const Y = (v) => H - PAD_B - ((v - ymin) / (ymax - ymin)) * (H - PAD_T - PAD_B);
  const poly1 = xs.map((x, i) => `${X(x).toFixed(1)},${Y(ys1[i]).toFixed(1)}`).join(' ');
  const poly2 = ys2 ? xs.map((x, i) => `${X(x).toFixed(1)},${Y(ys2[i]).toFixed(1)}`).join(' ') : null;
  const zeroY = Y(0);
  const axis = 'var(--ifm-color-emphasis-400)';
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{width: '100%', height: 'auto', display: 'block',
         background: 'var(--ifm-background-color)', borderRadius: '6px', marginBottom: '0.35rem'}}>
      <line x1={PAD_L} y1={zeroY} x2={W - PAD_R} y2={zeroY} stroke={axis} strokeWidth="1" />
      <line x1={PAD_L} y1={PAD_T} x2={PAD_L} y2={H - PAD_B} stroke={axis} strokeWidth="1" />
      {[0, 0.25, 0.5, 0.75, 1].map((f) => (
        <text key={f} x={X(f * TWO_PI)} y={H - 4} fontSize="9" fill={axis} textAnchor="middle">
          {f === 0 ? '0' : f === 1 ? '2π' : `${f}·2π`}
        </text>
      ))}
      <polyline points={poly1} fill="none" stroke={color1} strokeWidth="2" />
      {poly2 && <polyline points={poly2} fill="none" stroke={color2} strokeWidth="2" />}
      <text x={PAD_L + 4} y={PAD_T + 10} fontSize="10" fill={color1}>{label1}</text>
      {label2 && <text x={PAD_L + 4} y={PAD_T + 22} fontSize="10" fill={color2}>{label2}</text>}
    </svg>
  );
}

export default function EffectiveIsfExplorer() {
  const isEn = useIsEn();
  const [centerDeg, setCenterDeg] = useState(90);   // theta_c, 0..360 deg
  const [widthPct, setWidthPct] = useState(50);     // width, 10..100 % of period
  const [floor, setFloor] = useState(0.0);          // 0..0.5

  // build sample grid [0, 2*pi]
  const xs = [];
  for (let i = 0; i < N; i++) xs.push((TWO_PI * i) / (N - 1));

  const centerRad = centerDeg * DEG;
  const widthFrac = widthPct / 100;

  const gamma = xs.map(gammaLc);
  const alpha = xs.map((x) => alphaWindow(x, centerRad, widthFrac, floor));
  const gammaEff = xs.map((x, i) => gamma[i] * alpha[i]);

  const grmsStationary = trapzRms(xs, gamma);           // ~0.7071
  const grmsEff = trapzRms(xs, gammaEff);
  const c0eff = trapzC0(xs, gammaEff);                  // DC Fourier coeff of Gamma_eff
  const dcValue = c0eff / 2;                              // <Gamma*alpha> average

  // L-degradation vs the site's canonical stationary example B (Gamma_rms=0.5, [P1] Eq.21).
  // Ratio-only -> independent of the well-known /2 vs /4 SSB convention (see
  // white_noise_to_phase_noise.md); only Gamma_rms^2 scaling survives the ratio.
  const GRMS_REF = 0.5;
  const lDeg = 10 * Math.log10((grmsEff * grmsEff) / (GRMS_REF * GRMS_REF));
  const lDegVsStationary = 20 * Math.log10(grmsEff / grmsStationary);

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.55rem 0.8rem', textAlign: 'center',
  };
  const out = {display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.7rem'};

  const presets = isEn
    ? [
        {label: 'Bad (zero crossing, θc=90°)', center: 90, width: 50, floor: 0},
        {label: 'Good (peak, θc=0°, Colpitts-like)', center: 0, width: 50, floor: 0},
      ]
    : [
        {label: '壞（zero crossing, θc=90°）', center: 90, width: 50, floor: 0},
        {label: '好（波峰, θc=0°, Colpitts-like）', center: 0, width: 50, floor: 0},
      ];

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Γ×α alignment explorer (cyclostationary gating)'
          : 'Γ×α 對齊 explorer（cyclostationary 閘控）'}
      </div>

      <TraceSvg xs={xs} ys1={gamma} ys2={alpha}
                label1="Γ(x) = −sin x" label2="α(x) (NMF window)"
                color1="var(--ifm-color-emphasis-700)" color2="#4098ff"
                ymin={-1.15} ymax={1.15} height={120} />
      <TraceSvg xs={xs} ys1={gammaEff}
                label1="Γ_eff(x) = Γ(x)·α(x)" color1="var(--ifm-color-primary)"
                ymin={-1.15} ymax={1.15} height={120} />

      <Row label={isEn ? 'Center phase θc' : '中心相位 θ_c'} value={centerDeg} unit="°" min={0} max={360} step={1}
           onChange={setCenterDeg} fmt={(v) => v.toFixed(0)} />
      <Row label={isEn ? 'Width (% of period)' : '寬度（% 週期）'} value={widthPct} unit="%" min={10} max={100} step={1}
           onChange={setWidthPct} fmt={(v) => v.toFixed(0)} />
      <Row label={isEn ? 'Floor' : '底值 floor'} value={floor} unit="" min={0} max={0.5} step={0.01}
           onChange={setFloor} fmt={(v) => v.toFixed(2)} />

      <div style={{display: 'flex', gap: '0.5rem', flexWrap: 'wrap', margin: '0.5rem 0'}}>
        {presets.map((p) => (
          <button key={p.label} type="button"
                  onClick={() => { setCenterDeg(p.center); setWidthPct(p.width); setFloor(p.floor); }}
                  style={{
                    padding: '0.3rem 0.7rem', borderRadius: '6px', cursor: 'pointer', fontSize: '0.82rem',
                    border: '1px solid var(--ifm-color-emphasis-300)',
                    background: 'var(--ifm-background-surface-color)', color: 'var(--ifm-font-color-base)',
                  }}>
            {p.label}
          </button>
        ))}
      </div>

      <div style={out}>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>Γ_eff,rms</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{grmsEff.toFixed(3)}</div>
          <div style={{fontSize: '0.75rem', opacity: 0.7}}>
            {isEn ? `stationary Γ_rms = ${grmsStationary.toFixed(3)}` : `stationary Γ_rms = ${grmsStationary.toFixed(3)}`}
          </div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>c₀_eff (DC×2)</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{c0eff.toFixed(4)}</div>
          <div style={{fontSize: '0.75rem', opacity: 0.7}}>
            {isEn ? `⟨Γα⟩ = ${dcValue.toFixed(4)}` : `⟨Γα⟩ = ${dcValue.toFixed(4)}`}
          </div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>
            {isEn ? 'L-degradation vs stationary' : 'L-degradation vs stationary'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{lDegVsStationary.toFixed(1)} dB</div>
          <div style={{fontSize: '0.75rem', opacity: 0.7}}>
            {isEn ? `vs Γ_rms=0.5 ref: ${lDeg.toFixed(1)} dB` : `vs 例B Γ_rms=0.5: ${lDeg.toFixed(1)} dB`}
          </div>
        </div>
      </div>

      <div style={{fontSize: '0.82rem', marginTop: '0.7rem', lineHeight: 1.7,
                   padding: '0.5rem 0.7rem', borderRadius: '6px',
                   background: 'var(--ifm-background-color)',
                   border: '1px solid var(--ifm-color-emphasis-200)'}}>
        {isEn ? (
          <>
            <b>The Colpitts aha:</b> drag θ_c to <b>90°</b> (device noisy right at the ISF zero
            crossing, where |Γ|=1) — Γ_eff,rms stays large (≈0.40 at width=50%, floor=0: the
            classic "bad" case). Now drag θ_c to <b>0°</b> (device noisy at the waveform peak,
            where Γ≈0, Colpitts-like) — Γ_eff,rms collapses to ≈0.18, a further ≈7 dB better than
            the zero-crossing case even though the noise amount (window width, floor) is
            identical. <b>Windowing at the ISF zero crossing hurts the most; windowing at the
            peak barely matters.</b> (Anchor check at width=50%, floor=0: stationary 0.707,
            zero-crossing 0.395, peak 0.177 — matching lab_14.)
          </>
        ) : (
          <>
            <b>Colpitts 的頓悟：</b>把 θ_c 拉到 <b>90°</b>（device 恰好在 ISF 的 zero crossing、
            |Γ|=1 最敏感處才吵）——Γ_eff,rms 仍然很大（width=50%、floor=0 時 ≈0.40，
            經典「壞」case）。再把 θ_c 拉到 <b>0°</b>（device 在波形波峰、Γ≈0 處才吵，
            像 Colpitts）——Γ_eff,rms 崩到 ≈0.18，比 zero-crossing 再省約 7 dB，即使「吵多少」
            （窗寬、floor）完全沒變。<b>在 ISF 零點附近開窗傷最重；在波峰開窗幾乎沒差。</b>
            （錨點核對：width=50%、floor=0 時 stationary 0.707、zero-crossing 0.395、
            peak 0.177 — 與 lab_14 吻合。）
          </>
        )}
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem'}}>
        {isEn ? (
          <>
            Model: Γ(x) = −sin x fixed (ideal LC). α(x) is a raised-cosine-ish window,
            α(x) = floor + (1−floor)·0.5[1+cos(π·clip(d/(width/2),−1,1))] with d the wrapped
            distance to center θ_c (same family as <code>nmf_window</code> in
            simulations/lab_14_cyclostationary_isf.py). Γ_eff = Γ·α; Γ_eff,rms and c0_eff are
            computed with the trapezoidal rule (361 samples over one period), matching
            simulations/common/isf_utils.py's gamma_rms/compute_fourier_coefficients
            conventions. L-degradation uses 10·log₁₀(Γ_eff,rms²/0.5²) dB referencing the site's
            canonical stationary example B (Γ_rms=0.5, [P1] Eq.21); this ratio is independent of
            the well-known /2-vs-/4 SSB-accounting constant in Eq.(21) since that constant
            cancels between numerator and denominator (see white_noise_to_phase_noise.md).
          </>
        ) : (
          <>
            模型：Γ(x) = −sin x 固定（ideal LC）。α(x) 是 raised-cosine-ish 窗，
            α(x) = floor + (1−floor)·0.5[1+cos(π·clip(d/(width/2),−1,1))]，d 為到中心 θ_c 的
            wrapped 距離（與 simulations/lab_14_cyclostationary_isf.py 的 <code>nmf_window</code>
            同一族）。Γ_eff = Γ·α；Γ_eff,rms 與 c0_eff 用梯形法（一週期 361 點）計算，
            與 simulations/common/isf_utils.py 的 gamma_rms/compute_fourier_coefficients 慣例一致。
            L-degradation 用 10·log₁₀(Γ_eff,rms²/0.5²) dB，對照本站 canonical stationary 例 B
            （Γ_rms=0.5，[P1] Eq.21）；此比值與 Eq.(21) 著名的 /2 對 /4 SSB 記帳常數無關，
            因為該常數在比值的分子分母間相消（見 white_noise_to_phase_noise.md）。
          </>
        )}
      </div>
    </div>
  );
}
