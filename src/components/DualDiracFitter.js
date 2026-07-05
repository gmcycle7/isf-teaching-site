import React, {useMemo, useState} from 'react';
import useIsEn from './useIsEn';

// DualDiracFitter — interactive dual-Dirac Q-scale fitter for dj_dual_dirac.md.
//
// Model (matches the page's Steps 4-7 and lab_31 exactly):
//   TJ = RJ + DJ,  RJ ~ N(0, sigma^2),  DJ = A_dj * sin(theta), theta ~ U[0,2pi)
//   (sinusoidal/supply-spur DJ, the arcsine "double-horn" distribution derived on the page).
// A seeded PRNG (mulberry32) draws N~20k (theta, rj) pairs once per parameter change to build
// the histogram + empirical CDF shown in panel (a)/(b) (illustrating what a real BERT/scope
// TIE histogram would show at achievable sample depth).
//
// The FIT itself, however, needs tail probabilities far deeper than any finite sample can
// resolve honestly (BER windows down to 1e-9 need >1e9 draws to see a single event). So — same
// approach as simulations/lab_31_dual_dirac.py — the tail T(x) = P(RJ+DJ > x) used for fitting
// is the semi-analytic phase-average of the Gaussian tail over the DJ sinusoid:
//   T(x) = (1/2pi) * integral_0^{2pi} Q((x - A_dj sin(theta))/sigma) dtheta
// This is exact (not Monte-Carlo noise), matches lab_31's method, and is what makes a clean
// two-fit-depth comparison possible. Verified in Node against the page's lab_31 numbers:
// windows [1e-8,1e-4]/[1e-10,1e-6]/[1e-14,1e-10] reproduce 3.07/3.16/3.27 ps for DJ_dd exactly
// as printed in dj_dual_dirac.md Step 8.
//
// Q(x) = erfc-based (Numerical Recipes approximation, same as SerdesBerExplorer.js).
// norminv(p) = Acklam's algorithm (rational-function approximation to the inverse normal CDF,
// relative error < 1.15e-9), used for the Q-scale vertical axis Q^{-1}(2T(x)).
// Pure client component, hooks only, SSR-safe (no window/document access).

const TWO_PI = 2 * Math.PI;

// ---- mulberry32 seeded PRNG (deterministic across SSR/client, no external deps) ----
function mulberry32(seed) {
  let a = seed | 0;
  return function () {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---- erfc (Numerical Recipes rational approximation, ~1e-7 accuracy) ----
function erfc(x) {
  const z = Math.abs(x);
  const t = 1 / (1 + 0.5 * z);
  const ans =
    t *
    Math.exp(
      -z * z -
        1.26551223 +
        t *
          (1.00002368 +
            t *
              (0.37409196 +
                t *
                  (0.09678418 +
                    t *
                      (-0.18628806 +
                        t *
                          (0.27886807 +
                            t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277))))))))
    );
  return x >= 0 ? ans : 2 - ans;
}
const Qfun = (x) => 0.5 * erfc(x / Math.SQRT2);

// ---- Acklam's algorithm: inverse standard-normal CDF norminv(p) ----
// Peter J. Acklam's rational approximation; |relative error| < 1.15e-9 over (0,1).
function norminv(p) {
  if (p <= 0) return -Infinity;
  if (p >= 1) return Infinity;
  const a = [
    -3.969683028665376e1, 2.209460984245205e2, -2.759285104469687e2,
    1.383577518672690e2, -3.066479806614716e1, 2.506628277459239e0,
  ];
  const b = [
    -5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2,
    6.680131188771972e1, -1.328068155288572e1,
  ];
  const c = [
    -7.784894002430293e-3, -3.223964580411365e-1, -2.400758277161838e0,
    -2.549732539343734e0, 4.374664141464968e0, 2.938163982698783e0,
  ];
  const d = [7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996e0, 3.754408661907416e0];
  const plow = 0.02425, phigh = 1 - plow;
  let q, r;
  if (p < plow) {
    q = Math.sqrt(-2 * Math.log(p));
    return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
      ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
  } else if (p <= phigh) {
    q = p - 0.5;
    r = q * q;
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q /
      (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
  }
  q = Math.sqrt(-2 * Math.log(1 - p));
  return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
    ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
}

// Semi-analytic right tail T(x) = P(A sin(theta) + N(0,sigma^2) > x), theta ~ U[0,2pi).
function tailSemiAnalytic(x, A, sigma, nTheta = 360) {
  let sum = 0;
  for (let i = 0; i < nTheta; i++) {
    const theta = (TWO_PI * i) / nTheta;
    sum += Qfun((x - A * Math.sin(theta)) / sigma);
  }
  return sum / nTheta;
}

// Invert T(x) = pTarget by bisection (T is strictly decreasing in x).
function invertTail(pTarget, A, sigma) {
  let lo = -A - 12 * sigma, hi = A + 12 * sigma;
  for (let it = 0; it < 60; it++) {
    const mid = 0.5 * (lo + hi);
    if (tailSemiAnalytic(mid, A, sigma) > pTarget) lo = mid;
    else hi = mid;
  }
  return 0.5 * (lo + hi);
}

// Ordinary least-squares line fit y = slope*x + intercept.
function fitLine(xs, ys) {
  const n = xs.length;
  let sx = 0, sy = 0, sxx = 0, sxy = 0;
  for (let i = 0; i < n; i++) {
    sx += xs[i]; sy += ys[i]; sxx += xs[i] * xs[i]; sxy += xs[i] * ys[i];
  }
  const denom = n * sxx - sx * sx;
  const slope = denom !== 0 ? (n * sxy - sx * sy) / denom : NaN;
  const intercept = (sy - slope * sx) / n;
  return {slope, intercept};
}

// Dual-Dirac Q-scale fit over a decade window [pDeep, pShallow] of one-sided tail probability.
// Returns extracted sigma_fit and DJ_dd = 2*mu, plus the (x,y) points used (for plotting).
function fitDualDirac(A, sigma, pDeep, pShallow, nPoints = 24) {
  const logLo = Math.log10(pDeep), logHi = Math.log10(pShallow);
  const xs = [], ys = [];
  for (let i = 0; i < nPoints; i++) {
    const logp = logLo + ((logHi - logLo) * i) / (nPoints - 1);
    const p = Math.pow(10, logp);
    const twop = 2 * p;
    if (twop >= 1) continue;
    const x = invertTail(p, A, sigma);
    const y = norminv(1 - twop); // Q^{-1}(2T(x))
    xs.push(x); ys.push(y);
  }
  const {slope, intercept} = fitLine(xs, ys);
  const sigma_fit = 1 / slope;
  const mu_fit = -intercept / slope;
  return {sigma_fit, mu_fit, dj_dd: 2 * mu_fit, xs, ys};
}

// Synthesize N (theta, rj) draws with a fixed seed -> TJ samples, for the illustrative
// histogram/CDF only (NOT used for the fit itself; see file header).
function synthSamples(N, A, sigma, seed) {
  const rng = mulberry32(seed);
  const out = new Float64Array(N);
  for (let i = 0; i < N; i++) {
    const theta = rng() * TWO_PI;
    const dj = A * Math.sin(theta);
    // Box-Muller for the Gaussian RJ component
    let u = 0, v = 0;
    while (u === 0) u = rng();
    while (v === 0) v = rng();
    const rj = Math.sqrt(-2 * Math.log(u)) * Math.cos(TWO_PI * v) * sigma;
    out[i] = dj + rj;
  }
  return out;
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

const N_SAMPLES = 20000;
const SEED = 20260702;
const Q_INV_1E12 = 7.034; // Q^-1(1e-12), see dj_dual_dirac.md Step 3

// Fit-depth presets: BER decade window [deep, shallow] used for the Q-scale straight-line fit.
const FIT_PRESETS = [
  {key: 'shallow', pDeep: 1e-6, pShallow: 1e-3, labelZh: '淺：1e-3 .. 1e-6', labelEn: 'shallow: 1e-3 .. 1e-6'},
  {key: 'deep', pDeep: 1e-9, pShallow: 1e-6, labelZh: '深：1e-6 .. 1e-9', labelEn: 'deep: 1e-6 .. 1e-9'},
];

export default function DualDiracFitter() {
  const isEn = useIsEn();
  const [sigma_ps, setSigmaPs] = useState(1.0);     // true RJ sigma [ps], slider 0.5..2
  const [A_ps, setAPs] = useState(2.0);              // sinusoidal DJ amplitude [ps], slider 0..4
  const [presetIdx, setPresetIdx] = useState(1);     // which fit-depth window is "active" for the headline readout

  const sigma = sigma_ps * 1e-12;
  const A = A_ps * 1e-12;
  const DJ_pp = 2 * A_ps; // ps

  // Illustrative samples for histogram + empirical CDF (seeded, deterministic; not used for fit).
  const samples = useMemo(() => synthSamples(N_SAMPLES, A, sigma, SEED), [A, sigma]);

  // Fits at both preset depths (always compute both so the "compare fit depth" lesson is visible).
  const fits = useMemo(
    () => FIT_PRESETS.map((preset) => ({
      preset,
      ...fitDualDirac(A, sigma, preset.pDeep, preset.pShallow, 24),
    })),
    [A, sigma]
  );
  const activeFit = fits[presetIdx];

  // TJ@1e-12 extrapolation for each fit depth: TJ = DJ_dd + 2*Qinv(1e-12)*sigma_fit
  const tjAt1e12 = fits.map((f) => f.dj_dd + 2 * Q_INV_1E12 * f.sigma_fit);

  // ---- histogram (panel a) ----
  const HB = 60;
  const histMax = Math.max(A_ps * 1.3 + sigma_ps * 5, sigma_ps * 6, 1);
  const histMin = -histMax;
  const bins = useMemo(() => {
    const counts = new Array(HB).fill(0);
    const w = (histMax - histMin) / HB;
    for (let i = 0; i < samples.length; i++) {
      const v = samples[i] * 1e12; // ps
      let b = Math.floor((v - histMin) / w);
      if (b < 0) b = 0; else if (b >= HB) b = HB - 1;
      counts[b]++;
    }
    const peak = Math.max(...counts, 1);
    return {counts, peak, w};
  }, [samples, histMin, histMax]);

  // ---- Q-scale plot (panel b) ----
  const QW = 420, QH = 230, QPAD_L = 40, QPAD_R = 12, QPAD_T = 10, QPAD_B = 30;
  const xDomain = [-(A_ps + sigma_ps * 5.5), A_ps + sigma_ps * 5.5];
  const yDomain = [0, 8.2];
  const qx = (x_ps) => QPAD_L + ((x_ps - xDomain[0]) / (xDomain[1] - xDomain[0])) * (QW - QPAD_L - QPAD_R);
  const qy = (y) => QH - QPAD_B - (y / yDomain[1]) * (QH - QPAD_T - QPAD_B);

  // "true" curve: Q^{-1}(2*T_semi_analytic(x)) sampled densely, to show the honest tail shape.
  const trueCurve = useMemo(() => {
    const pts = [];
    const n = 160;
    for (let i = 0; i <= n; i++) {
      const x_ps = xDomain[0] + ((xDomain[1] - xDomain[0]) * i) / n;
      const x = x_ps * 1e-12;
      const t = tailSemiAnalytic(x, A, sigma);
      const twot = 2 * t;
      if (twot <= 0 || twot >= 1) continue;
      const y = norminv(1 - twot);
      if (y >= 0 && y <= yDomain[1] + 1) pts.push([x_ps, y]);
    }
    return pts;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [A, sigma]);

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 9.5rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.55rem 0.8rem', textAlign: 'center',
  };
  const btn = (active) => ({
    padding: '0.3rem 0.8rem', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem',
    border: active ? '1px solid var(--ifm-color-primary)' : '1px solid var(--ifm-color-emphasis-300)',
    background: active ? 'var(--ifm-color-primary)' : 'var(--ifm-background-surface-color)',
    color: active ? '#fff' : 'var(--ifm-font-color-base)', fontWeight: active ? 700 : 400,
  });
  const svgWrap = {width: '100%', height: 'auto', display: 'block'};
  const axisColor = 'var(--ifm-color-emphasis-400)';

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Dual-Dirac Q-scale fitter — extract DJ_δδ and σ_fit, compare fit depths'
          : 'Dual-Dirac Q-scale 擬合器 — 萃取 DJ_δδ 與 σ_fit，比較擬合深度'}
      </div>

      <Row
        label={isEn ? 'RJ σ (true)' : 'RJ σ（真實）'} value={sigma_ps} unit="ps" min={0.5} max={2} step={0.05}
        onChange={setSigmaPs} fmt={(v) => v.toFixed(2)}
      />
      <Row
        label={isEn ? 'Sinusoidal DJ amplitude A' : '弦波 DJ 幅度 A'} value={A_ps} unit="ps" min={0} max={4} step={0.1}
        onChange={setAPs} fmt={(v) => v.toFixed(1)}
      />

      <div style={{display: 'flex', gap: '1.4rem', flexWrap: 'wrap', marginTop: '0.6rem'}}>
        {/* Panel (a): histogram */}
        <div style={{flex: '1 1 20rem', minWidth: '16rem'}}>
          <div style={{fontSize: '0.8rem', opacity: 0.75, marginBottom: '0.2rem'}}>
            {isEn
              ? `(a) TJ histogram (N=${N_SAMPLES.toLocaleString()}, seeded) — double horn + Gaussian smear`
              : `(a) TJ 直方圖（N=${N_SAMPLES.toLocaleString()}，seeded）— 雙角＋高斯抹圓`}
          </div>
          <svg viewBox={`0 0 ${QW} 150`} style={svgWrap}>
            <line x1={QPAD_L} y1={140} x2={QW - QPAD_R} y2={140} stroke={axisColor} strokeWidth="1" />
            {bins.counts.map((c, i) => {
              const bw = (QW - QPAD_L - QPAD_R) / HB;
              const x = QPAD_L + i * bw;
              const h = (c / bins.peak) * 120;
              return (
                <rect key={i} x={x} y={140 - h} width={Math.max(bw - 0.5, 0.5)} height={h}
                      fill="var(--ifm-color-primary)" opacity="0.55" />
              );
            })}
            <text x={QPAD_L} y={149} fontSize="9" fill={axisColor}>{histMin.toFixed(0)} ps</text>
            <text x={QW - QPAD_R} y={149} fontSize="9" fill={axisColor} textAnchor="end">{histMax.toFixed(0)} ps</text>
            <text x={(QPAD_L + QW - QPAD_R) / 2} y={149} fontSize="9" fill={axisColor} textAnchor="middle">
              {isEn ? 'TJ (ps)' : 'TJ（ps）'}
            </text>
          </svg>
        </div>

        {/* Panel (b): Q-scale bathtub tail */}
        <div style={{flex: '1 1 22rem', minWidth: '18rem'}}>
          <div style={{fontSize: '0.8rem', opacity: 0.75, marginBottom: '0.2rem'}}>
            {isEn ? '(b) Q-scale bathtub tail — drag the fit-region buttons below' : '(b) Q-scale bathtub 尾巴 — 用下方按鈕拖動擬合區'}
          </div>
          <svg viewBox={`0 0 ${QW} ${QH}`} style={svgWrap}>
            <line x1={QPAD_L} y1={QH - QPAD_B} x2={QW - QPAD_R} y2={QH - QPAD_B} stroke={axisColor} strokeWidth="1" />
            <line x1={QPAD_L} y1={QPAD_T} x2={QPAD_L} y2={QH - QPAD_B} stroke={axisColor} strokeWidth="1" />
            {/* horizontal gridlines at Q^-1 for BER decades 1e-3, 1e-6, 1e-9, 1e-12 */}
            {[3.09, 4.75, 6.11, 7.034].map((yv, i) => (
              <g key={i}>
                <line x1={QPAD_L} y1={qy(yv)} x2={QW - QPAD_R} y2={qy(yv)} stroke={axisColor} strokeWidth="0.5" strokeDasharray="2 3" opacity="0.5" />
                <text x={QW - QPAD_R} y={qy(yv) - 2} fontSize="8" fill={axisColor} textAnchor="end">
                  {['1e-3', '1e-6', '1e-9', '1e-12'][i]}
                </text>
              </g>
            ))}
            {/* true honest tail curve */}
            <polyline
              points={trueCurve.map(([x, y]) => `${qx(x).toFixed(1)},${qy(y).toFixed(1)}`).join(' ')}
              fill="none" stroke="var(--ifm-color-emphasis-700)" strokeWidth="2"
            />
            {/* both fit lines, active one bold */}
            {fits.map((f, i) => {
              const x0 = xDomain[0], x1 = xDomain[1];
              const y0 = f.slope * (x0 * 1e-12) + f.intercept;
              const y1 = f.slope * (x1 * 1e-12) + f.intercept;
              const active = i === presetIdx;
              return (
                <line key={i}
                      x1={qx(x0)} y1={qy(Math.max(0, Math.min(yDomain[1], y0)))}
                      x2={qx(x1)} y2={qy(Math.max(0, Math.min(yDomain[1], y1)))}
                      stroke={i === 0 ? '#e07b39' : 'var(--ifm-color-primary)'}
                      strokeWidth={active ? 2.6 : 1.4}
                      strokeDasharray={active ? '0' : '5 4'}
                      opacity={active ? 0.95 : 0.55}
                />
              );
            })}
            {/* fit-window sample points for the active fit */}
            {activeFit.xs.map((x, i) => (
              <circle key={i} cx={qx(x * 1e12)} cy={qy(activeFit.ys[i])} r="2.2"
                      fill={presetIdx === 0 ? '#e07b39' : 'var(--ifm-color-primary)'} opacity="0.85" />
            ))}
            <text x={(QPAD_L + QW - QPAD_R) / 2} y={QH - 4} fontSize="9" fill={axisColor} textAnchor="middle">
              {isEn ? 'x (ps)' : 'x（ps）'}
            </text>
            <text x={QPAD_L + 2} y={QPAD_T + 8} fontSize="9" fill={axisColor}>Q⁻¹(2T)</text>
          </svg>
        </div>
      </div>

      <div style={{display: 'flex', gap: '0.5rem', flexWrap: 'wrap', margin: '0.5rem 0 0.3rem'}}>
        {FIT_PRESETS.map((p, i) => (
          <button key={p.key} type="button" style={btn(i === presetIdx)} onClick={() => setPresetIdx(i)}>
            {isEn ? p.labelEn : p.labelZh}
          </button>
        ))}
      </div>
      <div style={{fontSize: '0.78rem', opacity: 0.85, lineHeight: 1.7}}>
        {isEn ? (
          <>
            <span style={{color: '#e07b39', fontWeight: 700}}>―</span> shallow fit region (orange)
            <span style={{color: 'var(--ifm-color-primary)', fontWeight: 700}}>―</span> deep fit region (blue)
            <span style={{color: 'var(--ifm-color-emphasis-700)', fontWeight: 700}}>―</span> true tail (semi-analytic,
            exact — same method as lab_31; the bold line is the currently-selected fit depth).
          </>
        ) : (
          <>
            <span style={{color: '#e07b39', fontWeight: 700}}>―</span> 淺擬合區（橘）
            <span style={{color: 'var(--ifm-color-primary)', fontWeight: 700}}>―</span> 深擬合區（藍）
            <span style={{color: 'var(--ifm-color-emphasis-700)', fontWeight: 700}}>―</span> 真實尾巴（半解析、精確——
            與 lab_31 同法；粗線＝目前選取的擬合深度）。
          </>
        )}
      </div>

      {/* Readouts */}
      <div style={{display: 'flex', gap: '0.8rem', flexWrap: 'wrap', marginTop: '0.9rem'}}>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>{isEn ? 'DJ_δδ (fitted)' : 'DJ_δδ（擬合）'}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{activeFit.dj_dd > 0 ? (activeFit.dj_dd * 1e12).toFixed(2) : '0.00'}</div>
          <div style={{fontSize: '0.78rem'}}>ps</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>DJ_pp {isEn ? '(true)' : '（真實）'}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{DJ_pp.toFixed(2)}</div>
          <div style={{fontSize: '0.78rem'}}>ps</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>{isEn ? 'Δ = DJ_pp − DJ_δδ' : 'Δ = DJ_pp − DJ_δδ'}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700, color: 'var(--ifm-color-primary)'}}>
            {(DJ_pp - activeFit.dj_dd * 1e12).toFixed(2)}
          </div>
          <div style={{fontSize: '0.78rem'}}>ps</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>σ_fit / σ_true</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>
            {(activeFit.sigma_fit * 1e12).toFixed(2)} / {sigma_ps.toFixed(2)}
          </div>
          <div style={{fontSize: '0.78rem'}}>ps</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>TJ@10⁻¹² {isEn ? '(extrapolated)' : '（外插）'}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{(tjAt1e12[presetIdx] * 1e12).toFixed(2)}</div>
          <div style={{fontSize: '0.78rem'}}>ps</div>
        </div>
      </div>

      <div style={{fontSize: '0.8rem', marginTop: '0.7rem', lineHeight: 1.75, background: 'var(--ifm-background-color)',
                    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px', padding: '0.55rem 0.8rem'}}>
        {isEn ? (
          <>
            <b>Shallow</b> ([10⁻³, 10⁻⁶]): DJ_δδ = {(fits[0].dj_dd * 1e12).toFixed(2)} ps, σ_fit = {(fits[0].sigma_fit * 1e12).toFixed(2)} ps, TJ@10⁻¹² = {(tjAt1e12[0] * 1e12).toFixed(2)} ps.{' '}
            <b>Deep</b> ([10⁻⁶, 10⁻⁹]): DJ_δδ = {(fits[1].dj_dd * 1e12).toFixed(2)} ps, σ_fit = {(fits[1].sigma_fit * 1e12).toFixed(2)} ps, TJ@10⁻¹² = {(tjAt1e12[1] * 1e12).toFixed(2)} ps.
            The lesson: <b>DJ_δδ &lt; DJ_pp always</b>, and the deeper fit pulls DJ_δδ closer to (but never past) DJ_pp — because the deep tail is dominated by the sinusoid's turning points, where nearly all of the DJ probability mass actually sits.
          </>
        ) : (
          <>
            <b>淺</b>（[10⁻³, 10⁻⁶]）：DJ_δδ = {(fits[0].dj_dd * 1e12).toFixed(2)} ps、σ_fit = {(fits[0].sigma_fit * 1e12).toFixed(2)} ps、TJ@10⁻¹² = {(tjAt1e12[0] * 1e12).toFixed(2)} ps。{' '}
            <b>深</b>（[10⁻⁶, 10⁻⁹]）：DJ_δδ = {(fits[1].dj_dd * 1e12).toFixed(2)} ps、σ_fit = {(fits[1].sigma_fit * 1e12).toFixed(2)} ps、TJ@10⁻¹² = {(tjAt1e12[1] * 1e12).toFixed(2)} ps。
            教訓：<b>DJ_δδ 恆小於 DJ_pp</b>，且擬合越深，DJ_δδ 越逼近（但不超過）DJ_pp——因為深尾巴主要由弦波的轉折點主導，
            那裡才是 DJ 機率質量真正集中的地方。
          </>
        )}
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem'}}>
        {isEn ? (
          <>
            Model: RJ ~ N(0, σ²) ⊛ sinusoidal DJ = A·sin(θ), θ ~ U[0, 2π) (arcsine "double horn"; see this page's
            Step 2). Histogram/CDF panel uses N = {N_SAMPLES.toLocaleString()} seeded samples (mulberry32) purely for
            illustration; the fit itself uses the semi-analytic tail T(x) = ⟨Q((x−A sinθ)/σ)⟩_θ (same method as
            <code> simulations/lab_31_dual_dirac.py</code>), since BER windows this deep cannot be resolved honestly
            from any finite sample. Q(x) via the Numerical Recipes erfc approximation; Q⁻¹ via Acklam's rational
            approximation to the inverse normal CDF. Pedagogical toy model — real links superpose ISI+DCD+PJ and ISI
            is data-correlated (this page's Step 8 / Applicability table).
          </>
        ) : (
          <>
            模型：RJ ~ N(0, σ²) ⊛ 弦波 DJ = A·sin(θ)，θ ~ U[0, 2π)（arcsine「雙角」分布；見本頁第 2 步）。
            直方圖／CDF 面板用 N = {N_SAMPLES.toLocaleString()} 筆 seeded 樣本（mulberry32）純示意；擬合本身用半解析尾巴
            T(x) = ⟨Q((x−A sinθ)/σ)⟩_θ（與 <code>simulations/lab_31_dual_dirac.py</code> 同法），因為這麼深的 BER 窗口
            任何有限樣本都無法誠實估計。Q(x) 用 Numerical Recipes 的 erfc 近似；Q⁻¹ 用 Acklam 對反常態 CDF 的有理函數近似。
            Pedagogical toy model——真實鏈路是 ISI+DCD+PJ 疊加、且 ISI 與資料相關（見本頁第 8 步／適用條件表）。
          </>
        )}
      </div>
    </div>
  );
}
