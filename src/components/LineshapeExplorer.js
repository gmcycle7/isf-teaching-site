import React, {useMemo, useState} from 'react';
import useIsEn from './useIsEn';

// LineshapeExplorer — same-L(f_ref) lineshape explorer with RBW smearing.
//
// Lets the reader pick a single-point spec L(f_ref) at f_ref = 10 kHz, a
// dominant near-carrier noise "color" (white FM -> Lorentzian, per
// lorentzian_linewidth.md; or flicker FM -> near-Gaussian frozen-log line,
// per beyond_lorentzian.md Part A), and a spectrum-analyzer RBW, then shows
// both the *true* lineshape and the RBW-convolved *measured* curve on the
// same axes. Point of the widget: one L(f_ref) number does not fix the
// linewidth (noise color does), and a too-wide RBW smears the flattening
// away entirely.
//
// Physics (site v5 mapping, time-domain /2 convention throughout):
//   White FM (lorentzian_linewidth.md step 5):
//     unilateral S_phi(df) = 4D/(2*pi*df)^2  =>  D = S_phi*(2*pi*f_ref)^2/4
//     Lorentzian: S(df) prop to D/(D^2+(2*pi*df)^2), FWHM = D/pi.
//   Flicker FM (beyond_lorentzian.md Part A, steps 2-4):
//     S_phi(f) = b_-3/f^3  =>  b_-3 = S_phi * f_ref^3 (reading the fit off
//     the single spec point, as the page does for its worked example).
//     Var[Dphi(tau)] = 4 pi^2 b_-3 tau^2 [ln(1/(2 pi f_l tau)) + 3/2 - gammaE]
//       (needs a low-frequency cutoff f_l; we use the page's lab_29 value
//       f_l = 1/32 Hz -- an observation-time artifact, not a device
//       parameter, and the log dependence is deliberately weak).
//     Freeze the log at the memory time tau* where Var(tau*) = 2 (i.e.
//     E(tau*) = e^-1), then use the page's Gaussian-envelope engineering
//     approximation S(df) prop to exp(-2 pi^2 sigma_tau^2 df^2) with
//     sigma_tau = 1/(2 pi sqrt(b_-3 L*)), giving
//     FWHM = 2 sqrt(2 ln2) sqrt(b_-3 L*). The page is explicit that this
//     frozen-log Gaussian is an approximation (~2% off the exact numeric
//     Fourier transform in its own lab_29 example) -- we relabel it
//     "近似" / "approx." throughout rather than claim it is exact.
// RBW smearing: convolve the (peak-normalized) true lineshape with a
// Gaussian RBW kernel of FWHM = RBW on a 512-point linear frequency grid,
// discrete direct convolution (no FFT dependency). This is what a swept
// spectrum analyzer with Gaussian-like resolution bandwidth does to a line
// narrower than or comparable to the RBW.
//
// Pure client component, SSR-safe (no window/document access), no external
// deps. Locale-aware chrome via useIsEn; the physics/labels below are
// written bilingually inline (this widget is embedded on both zh and en
// pages, matching the ImpulseAnimation pattern).

const TWO_PI = 2 * Math.PI;
const GAMMA_E = 0.5772156649015329;
const N_GRID = 512;
const F_REF = 10e3;      // Hz, fixed per spec (matches beyond_lorentzian's -71 dBc/Hz@10kHz anchor)
const F_L = 1 / 32;      // Hz, lab_29's low-frequency cutoff (32 s record -> f_l = 1/T)

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

// --- physics helpers -------------------------------------------------

// White FM: unilateral S_phi = 4D/dw^2 at f_ref -> D; Lorentzian S(df) prop
// to D/(D^2+dw^2); FWHM = D/pi. (lorentzian_linewidth.md step 5, step 3)
function whiteLineshape(Sphi_at_fref, fref) {
  const dw = TWO_PI * fref;
  const D = (Sphi_at_fref * dw * dw) / 4;
  const fwhm = D / Math.PI;
  return {
    D, fwhm,
    curve: (df) => {
      const w = TWO_PI * df;
      return D / (D * D + w * w);
    },
  };
}

// Flicker FM: read b_-3 off the single spec point (beyond_lorentzian step 2:
// b_-3 = S_phi * f^3), solve for the memory time tau* where Var(tau*)=2
// (E(tau*)=e^-1) via bisection, freeze L* there, then use the page's
// Gaussian frozen-log engineering approximation for the lineshape and FWHM
// (beyond_lorentzian.md step 4).
function flickerLineshape(Sphi_at_fref, fref, fl) {
  const b3 = Sphi_at_fref * Math.pow(fref, 3);

  const varAt = (tau) => {
    const x = TWO_PI * fl * tau;
    if (x <= 0 || x >= 1) return NaN;
    const bracket = Math.log(1 / x) + 1.5 - GAMMA_E;
    return 4 * Math.PI * Math.PI * b3 * tau * tau * bracket;
  };

  // bisection for varAt(tau) = 2, tau in (tiny, 1/(2*pi*fl)) so x in (0,1)
  let lo = 1e-12;
  let hi = 0.999 / (TWO_PI * fl);
  let flo = varAt(lo) - 2;
  for (let i = 0; i < 200; i++) {
    const mid = (lo + hi) / 2;
    const fm = varAt(mid) - 2;
    if ((fm > 0) === (flo > 0)) { lo = mid; flo = fm; } else { hi = mid; }
  }
  const tauStar = (lo + hi) / 2;
  const Lstar = Math.log(1 / (TWO_PI * fl * tauStar)) + 1.5 - GAMMA_E;

  const sigmaTau = 1 / (TWO_PI * Math.sqrt(b3 * Lstar));
  const fwhm = 2 * Math.sqrt(2 * Math.LN2) * Math.sqrt(b3 * Lstar);

  return {
    b3, Lstar, tauStar, sigmaTau, fwhm,
    curve: (df) => Math.exp(-2 * Math.PI * Math.PI * sigmaTau * sigmaTau * df * df),
  };
}

// Build a linear frequency grid spanning +/- span around the carrier, and
// evaluate a normalized (peak = 1) true-lineshape curve on it.
function buildGrid(fwhmForSpan, nPts) {
  const span = Math.max(30 * fwhmForSpan, 5); // Hz; guard tiny fwhm
  const df = (2 * span) / (nPts - 1);
  const freqs = new Array(nPts);
  for (let i = 0; i < nPts; i++) freqs[i] = -span + i * df;
  return {freqs, df, span};
}

// Gaussian RBW kernel of FWHM = rbwHz on a grid spacing df, odd length so
// convolution stays centered exactly (avoids the half-bin index bug of
// even-length kernels).
function gaussKernel(rbwHz, df) {
  const sigma = rbwHz / (2 * Math.sqrt(2 * Math.LN2));
  const half = Math.max(1, Math.round((4 * sigma) / df));
  const M = 2 * half + 1;
  const k = new Array(M);
  let sum = 0;
  for (let i = 0; i < M; i++) {
    const x = (i - half) * df;
    const v = Math.exp(-0.5 * (x / sigma) * (x / sigma));
    k[i] = v;
    sum += v;
  }
  for (let i = 0; i < M; i++) k[i] /= sum;
  return k;
}

// Direct discrete convolution, "same" length output, zero-padded edges.
function convolveSame(sig, kernel) {
  const N = sig.length;
  const M = kernel.length;
  const half = (M - 1) / 2;
  const out = new Array(N).fill(0);
  for (let i = 0; i < N; i++) {
    let acc = 0;
    for (let j = 0; j < M; j++) {
      const idx = i + (j - half);
      if (idx >= 0 && idx < N) acc += sig[idx] * kernel[j];
    }
    out[i] = acc;
  }
  return out;
}

// FWHM of a peak-normalized curve on a uniform grid, via linear
// interpolation at the half-max crossings either side of the peak.
function fwhmOfCurve(freqs, curve) {
  let iPeak = 0;
  let peak = -Infinity;
  for (let i = 0; i < curve.length; i++) {
    if (curve[i] > peak) { peak = curve[i]; iPeak = i; }
  }
  if (!(peak > 0)) return NaN;
  const half = peak / 2;
  let iL = 0;
  for (let i = iPeak; i > 0; i--) { if (curve[i] < half) { iL = i; break; } }
  let iR = curve.length - 1;
  for (let i = iPeak; i < curve.length - 1; i++) { if (curve[i] < half) { iR = i; break; } }
  if (iL >= iPeak || iR <= iPeak || curve[iL + 1] === curve[iL] || curve[iR] === curve[iR - 1]) {
    return NaN; // curve too flat / RBW so wide it never crosses half-max within the grid
  }
  const fL = freqs[iL] + ((half - curve[iL]) / (curve[iL + 1] - curve[iL])) * (freqs[iL + 1] - freqs[iL]);
  const fR = freqs[iR - 1] + ((half - curve[iR - 1]) / (curve[iR] - curve[iR - 1])) * (freqs[iR] - freqs[iR - 1]);
  return fR - fL;
}

function fmtHz(hz) {
  if (!isFinite(hz)) return '—';
  if (hz >= 1e3) return `${(hz / 1e3).toFixed(hz >= 1e4 ? 1 : 2)} k`;
  return `${hz.toFixed(hz >= 100 ? 0 : 1)} `;
}

export default function LineshapeExplorer() {
  const isEn = useIsEn();
  const [L_dbc, setLdbc] = useState(-71.0);           // dBc/Hz @ f_ref, time-domain /2 convention
  const [noiseType, setNoiseType] = useState('white'); // 'white' | 'flicker'
  const [logRbw, setLogRbw] = useState(2.0);          // RBW = 10^logRbw Hz, slider is log-uniform

  const rbw = Math.pow(10, logRbw);

  const {trueFwhm, apparentFwhm, freqs, trueCurve, measuredCurve, extra} = useMemo(() => {
    const Llin = Math.pow(10, L_dbc / 10);
    const Sphi = 2 * Llin; // time-domain /2 convention (site v5 standard), matches beyond_lorentzian's -71 dBc/Hz anchor

    const model = noiseType === 'white'
      ? whiteLineshape(Sphi, F_REF)
      : flickerLineshape(Sphi, F_REF, F_L);

    const spanFwhm = Math.max(model.fwhm, rbw); // make sure the grid covers whichever is wider
    const {freqs, df} = buildGrid(spanFwhm, N_GRID);

    const rawTrue = freqs.map(model.curve);
    const peakTrue = Math.max(...rawTrue);
    const trueCurve = rawTrue.map((v) => v / peakTrue);

    const kernel = gaussKernel(rbw, df);
    const rawMeasured = convolveSame(trueCurve, kernel);
    const peakMeasured = Math.max(...rawMeasured);
    const measuredCurve = rawMeasured.map((v) => v / peakMeasured);

    const trueFwhm = model.fwhm;
    const apparentFwhm = fwhmOfCurve(freqs, measuredCurve);

    return {trueFwhm, apparentFwhm, freqs, trueCurve, measuredCurve, extra: model};
  }, [L_dbc, noiseType, rbw]);

  // --- plot geometry ---
  const W = 600, H = 340;
  const m = {l: 54, r: 16, t: 20, b: 42};
  const pw = W - m.l - m.r, ph = H - m.t - m.b;
  const span = freqs.length ? freqs[freqs.length - 1] : 1;

  const xPix = (f) => m.l + ((f + span) / (2 * span)) * pw;
  const yPix = (v) => m.t + (1 - Math.max(v, 0)) * ph;

  const pathFrom = (curve) =>
    curve.map((v, i) => `${i === 0 ? 'M' : 'L'}${xPix(freqs[i]).toFixed(2)},${yPix(v).toFixed(2)}`).join(' ');

  const fmtFreqAxis = (f) => {
    const af = Math.abs(f);
    if (af >= 1000) return `${(f / 1000).toFixed(af >= 10000 ? 0 : 1)}k`;
    return `${f.toFixed(0)}`;
  };

  const xTickCount = 5;
  const xTicks = [];
  for (let i = 0; i < xTickCount; i++) {
    xTicks.push(-span + (2 * span * i) / (xTickCount - 1));
  }

  // --- styles (match established widget pattern) ---
  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const btnRow = {display: 'flex', gap: '0.4rem', flexWrap: 'wrap', margin: '0.4rem 0 0.8rem'};
  const btn = (active) => ({
    flex: '1 1 8rem', cursor: 'pointer',
    padding: '0.45rem 0.6rem', fontSize: '0.85rem', borderRadius: '6px',
    border: '1px solid var(--ifm-color-emphasis-300)',
    background: active ? 'var(--ifm-color-primary)' : 'var(--ifm-background-color)',
    color: active ? 'var(--ifm-color-primary-contrast-foreground, #fff)' : 'inherit',
    fontWeight: active ? 700 : 400,
  });
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.6rem 0.8rem', textAlign: 'center',
  };
  const axisColor = 'var(--ifm-color-emphasis-600)';
  const gridColor = 'var(--ifm-color-emphasis-200)';
  const textColor = 'var(--ifm-font-color-base)';
  const trueColor = 'var(--ifm-color-emphasis-600)';
  const measColor = 'var(--ifm-color-primary)';

  const smearedAway = isFinite(apparentFwhm) === false || (isFinite(trueFwhm) && apparentFwhm > 3 * trueFwhm);

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Lineshape explorer: same L(f_ref) spec, two noise colors, RBW smearing'
          : '線形 explorer：同一個 L(f_ref) 規格、兩種雜訊顏色、RBW 抹平'}
      </div>

      <div style={{fontSize: '0.85rem', marginBottom: '0.2rem'}}>
        {isEn ? 'Dominant near-carrier noise:' : '近載波主導雜訊：'}
      </div>
      <div style={btnRow}>
        <button type="button" style={btn(noiseType === 'white')} onClick={() => setNoiseType('white')}>
          {isEn ? 'White FM (Lorentzian)' : 'White FM（Lorentzian）'}
        </button>
        <button type="button" style={btn(noiseType === 'flicker')} onClick={() => setNoiseType('flicker')}>
          {isEn ? 'Flicker FM (near-Gaussian, approx.)' : 'Flicker FM（近高斯，近似）'}
        </button>
      </div>

      <Row
        label={isEn ? `L(${(F_REF / 1e3).toFixed(0)} kHz)` : `L(${(F_REF / 1e3).toFixed(0)} kHz)`}
        value={L_dbc} unit="dBc/Hz" min={-100} max={-60} step={0.5}
        onChange={setLdbc} fmt={(v) => v.toFixed(1)}
      />
      <Row
        label={isEn ? 'RBW (log)' : 'RBW（對數）'}
        value={logRbw} unit={`= ${fmtHz(rbw)}Hz`} min={0} max={4} step={0.02}
        onChange={setLogRbw} fmt={() => fmtHz(rbw)}
      />

      <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{maxWidth: `${W}px`, display: 'block', margin: '0.6rem auto 0'}}
           role="img" aria-label="True and RBW-convolved lineshape versus offset frequency">
        {xTicks.map((f, i) => (
          <g key={i}>
            <line x1={xPix(f)} y1={m.t} x2={xPix(f)} y2={m.t + ph} stroke={gridColor} strokeWidth="1" />
            <text x={xPix(f)} y={m.t + ph + 16} fill={textColor} fontSize="11" textAnchor="middle">
              {fmtFreqAxis(f)}
            </text>
          </g>
        ))}
        {[0, 0.5, 1].map((v) => (
          <g key={v}>
            <line x1={m.l} y1={yPix(v)} x2={m.l + pw} y2={yPix(v)} stroke={gridColor} strokeWidth="1" />
            <text x={m.l - 6} y={yPix(v) + 4} fill={textColor} fontSize="10" textAnchor="end">{v}</text>
          </g>
        ))}
        <rect x={m.l} y={m.t} width={pw} height={ph} fill="none" stroke={axisColor} strokeWidth="1.2" />
        <text x={m.l + pw / 2} y={H - 6} fill={textColor} fontSize="12" textAnchor="middle">
          {isEn ? 'offset from carrier Δf (Hz)' : '偏離載波 Δf（Hz）'}
        </text>
        <text x={14} y={m.t + ph / 2} fill={textColor} fontSize="12" textAnchor="middle"
              transform={`rotate(-90 14 ${m.t + ph / 2})`}>
          {isEn ? 'normalized power' : '歸一化功率'}
        </text>

        <path d={pathFrom(trueCurve)} fill="none" stroke={trueColor} strokeWidth="1.8" strokeDasharray="5 4" />
        <path d={pathFrom(measuredCurve)} fill="none" stroke={measColor} strokeWidth="2.4" />

        <g>
          <line x1={m.l + 8} y1={m.t + 12} x2={m.l + 30} y2={m.t + 12} stroke={trueColor} strokeWidth="1.8" strokeDasharray="5 4" />
          <text x={m.l + 36} y={m.t + 16} fill={textColor} fontSize="11">{isEn ? 'true lineshape' : '真實線形'}</text>
          <line x1={m.l + 140} y1={m.t + 12} x2={m.l + 162} y2={m.t + 12} stroke={measColor} strokeWidth="2.4" />
          <text x={m.l + 168} y={m.t + 16} fill={textColor} fontSize="11">
            {isEn ? 'measured (RBW-convolved)' : '量測（RBW 卷積後）'}
          </text>
        </g>
      </svg>

      <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem'}}>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>{isEn ? 'FWHM_true' : 'FWHM_true'}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{fmtHz(trueFwhm)}Hz</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>
            {isEn ? 'apparent width @ this RBW' : '目前 RBW 下的表觀寬度'}
          </div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>
            {isFinite(apparentFwhm) ? `${fmtHz(apparentFwhm)}Hz` : (isEn ? 'smeared flat' : '已抹平')}
          </div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>{isEn ? 'RBW' : 'RBW'}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{fmtHz(rbw)}Hz</div>
        </div>
      </div>

      {smearedAway && (
        <div role="status" aria-live="polite" style={{fontSize: '0.82rem', marginTop: '0.6rem', padding: '0.5rem 0.7rem',
          border: '1px dashed var(--ifm-color-emphasis-400)', borderRadius: '6px'}}>
          {isEn
            ? 'RBW ≫ FWHM_true: the flattening / near-Gaussian shoulder is smeared into the analyzer’s own resolution bell — you would read only a wide, featureless hump, not the true lineshape.'
            : 'RBW 遠大於 FWHM_true：轉平／近高斯肩部已經被儀器自己的解析度鐘形抹平——量到的只是一個寬而無特徵的鼓包，不是真實線形。'}
        </div>
      )}

      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem', lineHeight: 1.55}}>
        {isEn ? (
          <>
            Model: a single spec point, L at {(F_REF / 1e3).toFixed(0)} kHz (time-domain "/2"
            convention), is mapped to the near-carrier lineshape two ways. <b>White FM</b>
            (lorentzian_linewidth.md): unilateral S_phi = 4D / Delta-omega^2 fixes the phase
            diffusion constant D, giving an exact Lorentzian with FWHM = D/pi. <b>Flicker FM</b>
            (beyond_lorentzian.md Part A): b_-3 = S_phi times f_ref^3 fixes the 1/f^3 level; with
            a low-frequency cutoff f_l = 1/32 Hz (an observation-time artifact, not a device
            parameter — the page shows the dependence on f_l is only logarithmic), the frozen-log
            Gaussian-envelope approximation gives FWHM ≈ 2·sqrt(2 ln 2)·sqrt(b_-3 · L*) — an
            approximation the page itself quotes as roughly 2% off the exact numeric Fourier
            transform, not an exact result. Both curves are then convolved (direct 512-point
            discrete convolution, no FFT) with a Gaussian resolution-bandwidth kernel of FWHM =
            RBW to produce the "measured" trace. Toy/illustrative: real spectrum analyzers,
            cross-correlation instruments, and residual white-FM skirts (see beyond_lorentzian.md)
            all modify this picture further.
          </>
        ) : (
          <>
            模型：同一個規格點——{(F_REF / 1e3).toFixed(0)} kHz 處的 L（時域「/2」慣例）——用兩種方式映成近載波線形。
            <b>White FM</b>（lorentzian_linewidth.md）：單邊 S_phi = 4D / Delta-omega^2 定出相位擴散常數
            D，得到精確 Lorentzian，FWHM = D/π。<b>Flicker FM</b>（beyond_lorentzian.md Part A）：
            b_-3 = S_phi 乘 f_ref^3 定出 1/f^3 強度；配上低頻截止 f_l = 1/32 Hz
            （這是觀察時間的產物、不是元件參數——原頁指出對 f_l 只有對數弱依賴），
            用凍結 log 的高斯包絡近似得到 FWHM ≈ 2·sqrt(2 ln 2)·sqrt(b_-3 · L*)——
            原頁自己就標明這個近似與精確數值傅立葉變換差約 2%，不是精確解。兩條線再各自與
            FWHM = RBW 的高斯解析度核卷積（直接 512 點離散卷積，不用 FFT）得到「量測」曲線。
            Toy／illustrative：真實頻譜儀、cross-correlation 儀器、殘餘 white FM 裙邊
            （見 beyond_lorentzian.md）都會再改變這張圖。
          </>
        )}
      </div>
    </div>
  );
}
