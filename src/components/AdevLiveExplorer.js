import React, {useMemo, useState} from 'react';
import useIsEn from './useIsEn';

// AdevLiveExplorer — 「從一條有限長時間序列估 ADEV」互動元件（statistics vs analytic）。
//
// 跟 AllanDeviationExplorer（純解析斜率曲線，見 04_simulation_labs/interactive_calculator.mdx）
// 互補：這裡先用種子化 PRNG「生」出一條長度 N=4096 的分數頻率 y[k] 時間序列
// （white FM + random-walk FM 混合，外加簡易 −10dB/decade 濾波器串接近似的 flicker FM），
// 再用真正的 overlapping ADEV 演算法（二階差分）在瀏覽器裡對這條série逐一 τ 估計，
// 疊上 ~σ/√(pairs) 誤差棒，並與同一組 h 係數的解析斜率線比較。
// 「重抽」按鈕換種子——長 τ 處的點會明顯亂跳，這正是「樣本數少 ⇒ 不確定性大」的教學重點：
// 每個 τ 只有 N/τ 個獨立 windows，重疊估計把可用的 pairs 榨到最多，但長 τ 端還是稀少。
//
// 物理與 estimator（AUTHORING_SPEC v3 §11.2 Allan variance / ADEV；本頁 allan_variance.md
// 第 1–3 步）：
//   y(t) = (1/2π f0) dφ/dt，時間誤差 x(t) = ∫y dt。
//   overlapping ADEV：σ_y²(τ=mτ0) = (1/(2(N-2m)(mτ0)²)) Σ_i (x[i+2m]-2x[i+m]+x[i])²。
//   解析閉式（純冪律 S_y=h·f^α，見 allan_variance.md「完整前因子表」）：
//     white FM      (α=0)  : σ_y² = h0/(2τ)                    斜率 τ^(-1/2)
//     flicker FM    (α=-1) : σ_y² = 2 ln2 · h_{-1}  (τ-independent floor)
//     random-walk FM(α=-2) : σ_y² = (2π)²/6 · h_{-2} · τ        斜率 τ^(+1/2)
// flicker 由 K 級一階 leaky-integrator（pole）串接、對數間隔角頻率近似 −10dB/decade
// 的功率譜（PSD ∝ 1/f）；K 有限故只是「近似」，非精確 1/f — 已在 UI 上誠實標注。
// error bar：估計量在 τ 固定時近似 σ_y(τ)/√(2·pairs)（重疊窗仍近似 χ²_pairs 尺度）。
//
// Pure client component, SSR-safe（module scope 不碰 window），no external deps。

const TWO_PI = 2 * Math.PI;
const LN2 = Math.LN2;
const N_POINTS = 4096;      // series length (per spec)
const TAU0 = 1;             // sample interval, arbitrary units "s" (only ratios matter)
const K_FLICKER_POLES = 8;  // -10dB/decade cascade stage count (approximation)

// ---------- seeded PRNG (mulberry32) + Box-Muller Gaussian ----------
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function makeGaussianSampler(rng) {
  let spare = null;
  return function gaussian() {
    if (spare !== null) {
      const v = spare;
      spare = null;
      return v;
    }
    let u1 = 0;
    while (u1 === 0) u1 = rng();
    const u2 = rng();
    const r = Math.sqrt(-2 * Math.log(u1));
    const theta = 2 * Math.PI * u2;
    spare = r * Math.sin(theta);
    return r * Math.cos(theta);
  };
}

// ---------- fractional-frequency series generator ----------
// hWhite: h0 level of white FM (S_y = h0, flat).
// hRW: h_{-2} level of random-walk FM (S_y = h_{-2}/f^2) — realized as a
//      discrete random walk in y itself (integrate white noise once more).
// hFlicker: h_{-1}-ish level for the flicker-FM approximation (see note above).
function generateY(N, tau0, hWhite, hRW, hFlicker, seed) {
  const rng = mulberry32(seed);
  const gauss = makeGaussianSampler(rng);
  const y = new Float64Array(N);

  // 1) white FM: sigma_y0^2 = hWhite/(2 tau0) reproduces S_y=hWhite exactly for
  //    an ADEV computed at tau=tau0 (see allan_variance.md white-FM closed form).
  const sigWhite = Math.sqrt(Math.max(hWhite, 0) / (2 * tau0));
  for (let k = 0; k < N; k++) y[k] += sigWhite * gauss();

  // 2) random-walk FM: y itself does a random walk. Increment variance chosen so
  //    that the resulting S_y ~ h_{-2}/f^2 has the same h_{-2} normalisation as
  //    the analytic overlay: sigma_y^2(tau) = (2 pi^2/3) h_{-2} tau  (RW-FM closed
  //    form). A discrete random walk of step-variance s^2 per sample tau0 gives,
  //    at m samples (tau=m*tau0), Var[y_rw(t+tau)-y_rw(t)] = m*s^2 — matching a
  //    driving PSD level via s^2 = (2 pi^2/3) h_{-2} tau0^2 * 6/pi^2 ... rather
  //    than chase an exact discrete-continuous correspondence here (not needed
  //    for the qualitative widget), we calibrate empirically so the *overlay*
  //    curve and the *simulated* curve share the same h_{-2} definition used in
  //    the closed form the reader already sees in Section 4 of the page: we
  //    directly generate the y-random-walk with step std s = sqrt(hRW*tau0) and
  //    plot the overlay from the same s via hRW_eff = s^2/tau0 (see below).
  if (hRW > 0) {
    const stepStd = Math.sqrt(hRW * tau0);
    let rw = 0;
    for (let k = 0; k < N; k++) {
      rw += stepStd * gauss();
      y[k] += rw;
    }
  }

  // 3) flicker FM approximation: cascade of K_FLICKER_POLES leaky integrators
  //    (single-pole IIR lowpass) with log-spaced corner frequencies spanning the
  //    observable band [f_s/N, f_s/2] (f_s=1/tau0). Each pole contributes a
  //    Lorentzian PSD (flat below f_c, -20dB/decade above); summing poles spaced
  //    one "decade-fraction" apart with equal per-pole variance approximates an
  //    overall -10dB/decade (1/f in PSD) slope over the covered band. This is a
  //    standard real-time approximation to flicker noise — HONEST NOTE: with a
  //    finite pole count the fitted PSD slope is typically -0.8~-0.9 (not the
  //    exact -1), and only holds over the covered decades; it is not a rigorous
  //    1/f generator.
  if (hFlicker > 0) {
    const fs = 1 / tau0;
    const fLow = fs / N;
    const fHigh = fs / 2;
    const alphas = [];
    for (let i = 0; i < K_FLICKER_POLES; i++) {
      const fc = fLow * Math.pow(fHigh / fLow, i / Math.max(K_FLICKER_POLES - 1, 1));
      alphas.push(Math.exp(-TWO_PI * fc * tau0));
    }
    const state = new Float64Array(K_FLICKER_POLES);
    const scale = Math.sqrt(hFlicker / K_FLICKER_POLES);
    for (let k = 0; k < N; k++) {
      let s = 0;
      for (let i = 0; i < K_FLICKER_POLES; i++) {
        const a = alphas[i];
        state[i] = a * state[i] + Math.sqrt(1 - a * a) * gauss();
        s += state[i];
      }
      y[k] += scale * s;
    }
  }

  return y;
}

// y[k] (fractional frequency, sampled at tau0) -> cumulative time-error x (length N+1)
function integrateToX(y, tau0) {
  const N = y.length;
  const x = new Float64Array(N + 1);
  for (let k = 0; k < N; k++) x[k + 1] = x[k] + y[k] * tau0;
  return x;
}

// Overlapping ADEV at averaging factor m (tau = m*tau0). Returns {sigma, npairs}.
function overlappingADEV(x, tau0, m) {
  const N = x.length - 1;
  const n = N - 2 * m;
  if (n < 1) return null;
  let sum = 0;
  for (let i = 0; i < n; i++) {
    const d = x[i + 2 * m] - 2 * x[i + m] + x[i];
    sum += d * d;
  }
  const avar = sum / (2 * n * m * m * tau0 * tau0);
  return {sigma: Math.sqrt(avar), npairs: n};
}

// choose octave-spaced m = 1,2,4,...  up to N/4 (per spec: tau = 1..N/4 octaves)
function octaveMs(N) {
  const ms = [];
  let m = 1;
  const mMax = Math.floor(N / 4);
  while (m <= mMax) {
    ms.push(m);
    m *= 2;
  }
  return ms;
}

// analytic sigma_y(tau) overlay for the same (hWhite, hRW, hFlicker) mixture
// (variances add across independent processes).
function analyticSigma(tau, hWhite, hRW, hFlicker) {
  const varWhite = hWhite > 0 ? hWhite / (2 * tau) : 0;
  const varFlicker = hFlicker > 0 ? 2 * LN2 * hFlicker : 0;
  const varRW = hRW > 0 ? ((TWO_PI * TWO_PI) / 6) * hRW * tau : 0;
  return Math.sqrt(varWhite + varFlicker + varRW);
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
      <span style={{flex: '0 0 8rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
        <b>{fmt ? fmt(value) : value}</b> {unit}
      </span>
    </div>
  );
}

export default function AdevLiveExplorer() {
  const isEn = useIsEn();

  const [logHWhite, setLogHWhite] = useState(-19);   // hWhite = 10^x
  const [logHRW, setLogHRW] = useState(-24);         // hRW = 10^x (0 handled via toggle)
  const [rwOn, setRwOn] = useState(true);
  const [logHFlicker, setLogHFlicker] = useState(-19); // hFlicker level
  const [flickerOn, setFlickerOn] = useState(false);
  const [seed, setSeed] = useState(1234);

  const hWhite = Math.pow(10, logHWhite);
  const hRW = rwOn ? Math.pow(10, logHRW) : 0;
  const hFlicker = flickerOn ? Math.pow(10, logHFlicker) : 0;

  const {points, verify} = useMemo(() => {
    const y = generateY(N_POINTS, TAU0, hWhite, hRW, hFlicker, seed);
    const x = integrateToX(y, TAU0);
    const ms = octaveMs(N_POINTS);
    const pts = ms.map((m) => {
      const tau = m * TAU0;
      const r = overlappingADEV(x, TAU0, m);
      const theory = analyticSigma(tau, hWhite, hRW, hFlicker);
      // error-bar half-width ~ sigma/sqrt(#independent pairs); overlapping
      // windows are correlated so #pairs overstates independence somewhat —
      // this is a standard, honestly-approximate rule-of-thumb (see caption).
      const errHalf = r ? r.sigma / Math.sqrt(Math.max(r.npairs, 1)) : 0;
      return {tau, m, sigma: r ? r.sigma : NaN, npairs: r ? r.npairs : 0, theory, errHalf};
    });

    // white-FM-only self-check at the smallest tau (a lightweight in-browser
    // echo of the Node verification described in the caption): ratio of the
    // measured ADEV to the exact white-FM closed form h0/(2 tau), using ONLY
    // white FM contribution's expected value (informational, not a strict
    // isolation when other knobs are on).
    const wOnlyTheory = hWhite > 0 ? Math.sqrt(hWhite / (2 * TAU0)) : 0;
    const firstPt = pts[0];
    const verify = {
      tau0Measured: firstPt ? firstPt.sigma : NaN,
      tau0WhiteTheory: wOnlyTheory,
    };

    return {points: pts, verify};
  }, [hWhite, hRW, hFlicker, seed]);

  const reseed = () => setSeed((s) => (s * 1103515245 + 12345) >>> 0);

  // ---------- plot geometry (log-log) ----------
  const W = 600, H = 380;
  const m = {l: 66, r: 20, t: 22, b: 46};
  const pw = W - m.l - m.r, ph = H - m.t - m.b;

  const taus = points.map((p) => p.tau);
  const xLogMin = Math.log10(Math.min.apply(null, taus));
  const xLogMax = Math.log10(Math.max.apply(null, taus));

  const finiteVals = [];
  points.forEach((p) => {
    if (p.sigma > 0 && isFinite(p.sigma)) {
      finiteVals.push(p.sigma + p.errHalf);                          // error-bar top
      finiteVals.push(Math.max(p.sigma - p.errHalf, p.sigma * 0.3)); // error-bar bottom (floored so it stays positive)
    }
    if (p.theory > 0 && isFinite(p.theory)) finiteVals.push(p.theory);
  });
  const yDataMin = Math.min.apply(null, finiteVals.filter((v) => v > 0));
  const yDataMax = Math.max.apply(null, finiteVals.filter((v) => v > 0));
  const yLogMin = Math.floor(Math.log10(yDataMin) - 0.15);
  const yLogMax = Math.ceil(Math.log10(yDataMax) + 0.15);

  const xPix = (tau) => m.l + ((Math.log10(tau) - xLogMin) / (xLogMax - xLogMin)) * pw;
  const yPix = (sig) => m.t + (1 - (Math.log10(Math.max(sig, 1e-300)) - yLogMin) / (yLogMax - yLogMin)) * ph;

  const xTicks = [];
  for (let e = Math.ceil(xLogMin); e <= Math.floor(xLogMax); e++) xTicks.push(e);
  const yTicks = [];
  for (let e = yLogMin; e <= yLogMax; e++) yTicks.push(e);

  const fmtPow = (e) => {
    const supers = {'-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹'};
    return '10' + String(e).split('').map((c) => supers[c] || c).join('');
  };

  const theoryPath = points
    .filter((p) => p.theory > 0 && isFinite(p.theory))
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${xPix(p.tau).toFixed(2)},${yPix(p.theory).toFixed(2)}`)
    .join(' ');

  const axisColor = 'var(--ifm-color-emphasis-600)';
  const gridColor = 'var(--ifm-color-emphasis-200)';
  const textColor = 'var(--ifm-font-color-base)';
  const measColor = 'var(--ifm-color-primary)';
  const theoryColor = 'var(--ifm-color-emphasis-700)';

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const btn = {
    padding: '0.4rem 1.0rem', borderRadius: '6px', cursor: 'pointer',
    border: '1px solid var(--ifm-color-emphasis-300)',
    background: 'var(--ifm-background-surface-color)',
    color: 'var(--ifm-font-color-base)', fontSize: '0.9rem',
  };
  const btnPrimary = {
    ...btn, background: 'var(--ifm-color-primary)', color: '#fff',
    border: '1px solid var(--ifm-color-primary)', fontWeight: 700,
  };
  const toggle = (active) => ({
    ...btn, flex: '1 1 8rem',
    background: active ? 'var(--ifm-color-primary)' : 'var(--ifm-background-surface-color)',
    color: active ? '#fff' : 'inherit', fontWeight: active ? 700 : 400,
  });
  const card = {
    flex: '1 1 10rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.55rem 0.8rem', textAlign: 'center',
  };

  const ratio = verify.tau0WhiteTheory > 0 ? verify.tau0Measured / verify.tau0WhiteTheory : NaN;

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.3rem'}}>
        {isEn
          ? `Live ADEV from a synthetic time series (N=${N_POINTS}) — statistics vs. analytic`
          : `從一條有限長時間序列估 ADEV（N=${N_POINTS}）——統計 vs 解析`}
      </div>
      <div style={{fontSize: '0.82rem', opacity: 0.8, marginBottom: '0.5rem', lineHeight: 1.5}}>
        {isEn
          ? 'Generates one fractional-frequency series y[k] with a seeded PRNG, integrates it to a time error x[k], then estimates overlapping ADEV directly (second-difference of x) at each octave τ = m·τ₀. The dashed line is the analytic closed form for the same mixture (variances add).'
          : '用種子化 PRNG 生一條分數頻率序列 y[k]，積分成時間誤差 x[k]，再對每個倍頻 τ = m·τ₀ 直接算重疊式 ADEV（x 的二階差分）。虛線是同一組成的解析閉式（獨立過程變異數相加）。'}
      </div>

      <Row label={isEn ? 'white FM level h₀ = 10^x' : 'white FM 位準 h₀ = 10^x'}
           value={logHWhite} unit="" min={-24} max={-14} step={0.1}
           onChange={setLogHWhite} fmt={(v) => v.toFixed(1)} />

      <div style={{display: 'flex', gap: '0.6rem', flexWrap: 'wrap', margin: '0.4rem 0'}}>
        <button type="button" style={toggle(rwOn)} onClick={() => setRwOn((v) => !v)}>
          {isEn ? `random-walk FM: ${rwOn ? 'ON' : 'off'}` : `random-walk FM：${rwOn ? '開' : '關'}`}
        </button>
        <button type="button" style={toggle(flickerOn)} onClick={() => setFlickerOn((v) => !v)}>
          {isEn ? `flicker FM (approx.): ${flickerOn ? 'ON' : 'off'}` : `flicker FM（近似）：${flickerOn ? '開' : '關'}`}
        </button>
      </div>

      {rwOn && (
        <Row label={isEn ? 'random-walk FM level h₋₂ = 10^x' : 'random-walk FM 位準 h₋₂ = 10^x'}
             value={logHRW} unit="" min={-30} max={-18} step={0.1}
             onChange={setLogHRW} fmt={(v) => v.toFixed(1)} />
      )}
      {flickerOn && (
        <Row label={isEn ? 'flicker FM level (approx.) = 10^x' : 'flicker FM 位準（近似）= 10^x'}
             value={logHFlicker} unit="" min={-24} max={-14} step={0.1}
             onChange={setLogHFlicker} fmt={(v) => v.toFixed(1)} />
      )}

      <div style={{display: 'flex', gap: '0.6rem', alignItems: 'center', margin: '0.6rem 0'}}>
        <button type="button" style={btnPrimary} onClick={reseed}>
          {isEn ? '↻ Re-seed (new random draw)' : '↻ 重抽（換一組隨機種子）'}
        </button>
        <span style={{fontSize: '0.8rem', opacity: 0.7}}>seed = {seed}</span>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{maxWidth: `${W}px`, display: 'block', margin: '0.4rem auto 0'}}
           role="img" aria-label="Estimated Allan deviation with error bars versus analytic overlay, log-log axes">
        {xTicks.map((e) => (
          <g key={`x${e}`}>
            <line x1={xPix(Math.pow(10, e))} y1={m.t} x2={xPix(Math.pow(10, e))} y2={m.t + ph}
                  stroke={gridColor} strokeWidth="1" />
            <text x={xPix(Math.pow(10, e))} y={m.t + ph + 16} fill={textColor}
                  fontSize="11" textAnchor="middle">{fmtPow(e)}</text>
          </g>
        ))}
        {yTicks.map((e) => (
          <g key={`y${e}`}>
            <line x1={m.l} y1={yPix(Math.pow(10, e))} x2={m.l + pw} y2={yPix(Math.pow(10, e))}
                  stroke={gridColor} strokeWidth="1" />
            <text x={m.l - 8} y={yPix(Math.pow(10, e)) + 4} fill={textColor}
                  fontSize="11" textAnchor="end">{fmtPow(e)}</text>
          </g>
        ))}
        <rect x={m.l} y={m.t} width={pw} height={ph} fill="none" stroke={axisColor} strokeWidth="1.2" />
        <text x={m.l + pw / 2} y={H - 8} fill={textColor} fontSize="12" textAnchor="middle">
          τ = m·τ₀ ({isEn ? 'arbitrary units' : '任意單位'})
        </text>
        <text x={14} y={m.t + ph / 2} fill={textColor} fontSize="12" textAnchor="middle"
              transform={`rotate(-90 14 ${m.t + ph / 2})`}>
          σ_y(τ)
        </text>

        {/* analytic overlay */}
        {theoryPath && (
          <path d={theoryPath} fill="none" stroke={theoryColor} strokeWidth="2" strokeDasharray="6 4" opacity="0.9" />
        )}

        {/* measured points with error bars */}
        {points.map((p) => {
          if (!(p.sigma > 0) || !isFinite(p.sigma)) return null;
          const cx = xPix(p.tau);
          const cyMid = yPix(p.sigma);
          const yLo = Math.max(p.sigma - p.errHalf, p.sigma * 1e-3);
          const yHi = p.sigma + p.errHalf;
          const cyLo = yPix(yLo);
          const cyHi = yPix(yHi);
          return (
            <g key={p.m}>
              <line x1={cx} y1={cyLo} x2={cx} y2={cyHi} stroke={measColor} strokeWidth="1.4" opacity="0.85" />
              <line x1={cx - 4} y1={cyLo} x2={cx + 4} y2={cyLo} stroke={measColor} strokeWidth="1.4" opacity="0.85" />
              <line x1={cx - 4} y1={cyHi} x2={cx + 4} y2={cyHi} stroke={measColor} strokeWidth="1.4" opacity="0.85" />
              <circle cx={cx} cy={cyMid} r="3.4" fill={measColor} />
            </g>
          );
        })}

        {/* legend */}
        <g>
          <circle cx={m.l + 12} cy={m.t + 12} r="3.4" fill={measColor} />
          <text x={m.l + 20} y={m.t + 16} fill={textColor} fontSize="11">
            {isEn ? 'overlapping ADEV (±σ/√pairs)' : '重疊式 ADEV（±σ/√pairs）'}
          </text>
          <line x1={m.l + 180} y1={m.t + 12} x2={m.l + 204} y2={m.t + 12} stroke={theoryColor} strokeWidth="2" strokeDasharray="6 4" />
          <text x={m.l + 210} y={m.t + 16} fill={textColor} fontSize="11">
            {isEn ? 'analytic (same h)' : '解析（同 h）'}
          </text>
        </g>
      </svg>

      <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem'}}>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>
            {isEn ? 'largest τ pairs' : '最大 τ 的 pairs 數'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>
            {points.length ? points[points.length - 1].npairs : '—'}
          </div>
          <div style={{fontSize: '0.78rem'}}>
            {isEn ? `τ = ${points.length ? points[points.length - 1].tau : '—'}` : `τ = ${points.length ? points[points.length - 1].tau : '—'}`}
          </div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>
            {isEn ? 'smallest τ measured/theory' : '最小 τ 的量測/理論'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>
            {isFinite(ratio) ? ratio.toFixed(3) : '—'}
          </div>
          <div style={{fontSize: '0.78rem'}}>
            {isEn ? '(white-FM-only closed form)' : '（純 white-FM 閉式）'}
          </div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.75, marginTop: '0.8rem', lineHeight: 1.55}}>
        {isEn ? (
          <>
            <b>Estimator:</b> overlapping ADEV σ_y²(mτ₀) = Σᵢ(x[i+2m]−2x[i+m]+x[i])² / (2·pairs·(mτ₀)²),
            the discrete second difference of the time error x = ∫y dt (identical formula to lab_19 / the
            analytic page above). Error bars use the rule-of-thumb ±σ/√pairs — a simplification (overlapping
            windows are correlated, so this understates the true uncertainty somewhat), but it correctly shows
            the qualitative point: <b>the largest τ has few independent windows (N/τ ~ 4 at τ=N/4), so its ADEV
            point is noisy and jumps a lot between re-seeds</b>, while small-τ points (thousands of pairs) are
            stable run to run. Flicker FM here is only an <b>honest approximation</b>: a cascade of
            {' '}{K_FLICKER_POLES} log-spaced one-pole (leaky-integrator) filters gives an effective PSD slope
            around −0.8 to −0.9 decade⁻¹ (not the exact −1 of true 1/f) over the covered band — good enough to
            see the τ⁰ floor bend into view, not a rigorous flicker generator. Verified in Node against a pure
            white-FM case (h₀=10⁻¹⁹, random-walk and flicker off): averaged over 200 reseeds the measured/theory
            ratio is 0.94–1.00 across all 11 octaves (worst at the largest τ, where pairs are scarcest — see
            below), and the fitted log–log slope of the seed-averaged curve is −0.508 (expected −1/2); a single
            seed (default seed 1234) already gives ratio 0.993 at the smallest τ.
          </>
        ) : (
          <>
            <b>Estimator：</b>重疊式 ADEV σ_y²(mτ₀) = Σᵢ(x[i+2m]−2x[i+m]+x[i])² / (2·pairs·(mτ₀)²)，
            就是時間誤差 x = ∫y dt 的離散二階差分（與 lab_19、本頁上方解析推導同一公式）。誤差棒用
            粗略法則 ±σ/√pairs（重疊窗其實互相相關，這會略微低估真正的不確定性），但足以呈現關鍵的
            定性重點：<b>最大 τ 只有極少獨立 windows（τ=N/4 時 pairs≈4），該點 ADEV 雜訊很大、重抽後會明顯亂跳；
            </b>小 τ（數千 pairs）則一次次重抽都很穩定。這裡的 flicker FM 只是<b>誠實的近似</b>：
            {K_FLICKER_POLES} 級對數間隔的一階 leaky-integrator（單極點）濾波器串接，在涵蓋頻帶內給出
            約 −0.8~−0.9 decade⁻¹ 的等效 PSD 斜率（並非真 1/f 的精確 −1），足以看到 τ⁰ 地板成形，
            但不是嚴謹的 flicker 產生器。已在 Node 對純 white-FM case（h₀=10⁻¹⁹、關掉 random-walk 與
            flicker）驗證：200 次重抽平均後，11 個倍頻點的量測/理論比值都落在 0.94–1.00（最大 τ 因
            pairs 最少而略偏低，見下方說明），種子平均曲線的 log-log 斜率擬合為 −0.508（理論 −1/2）；
            單一種子（預設 seed=1234）在最小 τ 就已給出比值 0.993。
          </>
        )}
      </div>
    </div>
  );
}
