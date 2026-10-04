import React, {useMemo, useState} from 'react';
import useIsEn from './useIsEn';

// BbCdrExplorer — live explorer for the bang-bang CDR page
// (docs/06_design_insights/cdr_bang_bang_jtol.md). Every formula is the page's own;
// the time-domain panel re-implements, line for line, the behavioural model of
// simulations/lab_45_bb_cdr.py (functions bb_loop / sj_tolerance), with one fixed seed.
//
//   PD characteristic   <e>(dt) = erf(dt / (sqrt2 sigma_j))                 (Step 2)
//   K_bb                = sqrt(2/pi) / sigma_j      [1/s];  K_bb*UI per UI   (Step 2)
//   PI step             K_p = UI / 2^b                                       (Step 3)
//   hunting             DJ_pp = (2D+1) K_p  (D = 0 here);  sigma_hunt = sqrt(K_p / (2 K_bb))
//   proportional BW     f_BW = rho_T K_p K_bb f_u / (2 pi),  f_u = f_b / N_dec  (Step 3)
//   eye margin          UI - TJ_eye,  TJ_eye = 2 * 7.03 * sigma_j            (Step 4)
//   slew line           rho_T (K_p/UI) f_u / (pi f)           [UI pp]        (Step 4)
//   acceleration line   rho_T (K_i/UI) f_u^2 / (2 pi^2 f^2)   [UI pp]        (Step 5), K_i = K_p/1024
//   linear JTOL         margin / |1 - H(f)|: first order (P only) or type-II with
//                       f_n = sqrt(K_i K_bb rho_T) f_u / 2pi, zeta = K_p K_bb rho_T / (2 sqrt(K_i K_bb rho_T))
//   JTOL used here      min( linear , max( large-signal lines , margin ) )   (Step 4 "min(linear, large-signal)")
//   SSC (-0.5 %, 30 kHz triangle, 25 Gb/s): a = delta f_b / (T_m/2) = 7.5e12 UI/s^2,
//                       peak velocity delta f_b = 5000 ppm of f_b             (Step 5)
//
// Defaults reproduce the page: sigma_j = 447.9 fs -> K_bb = 1.781e12 1/s = 71.3 per UI,
// 6-bit PI -> K_p = 0.625 ps, N_dec = 16, f = 30 kHz, 521 UI pp, integral path on.
//
// Pure client component, SSR-safe (all maths inside useMemo), no external deps, inline SVG.

const FB = 25e9;            // bit rate [b/s]
const UI = 40e-12;          // [s]
const RHO_T = 0.5;          // transition density of scrambled data
const QINV = 7.03;          // Q^-1(1e-12)
const KI_DIV = 1024;        // K_i = K_p / 1024 (page, Step 5)
const SSC_DELTA = 0.005;    // -0.5 % down-spread
const SSC_FM = 30e3;        // Hz
const SSC_PP_UI = (SSC_DELTA * FB) / SSC_FM / 8;   // 520.83 UI
const MAX_STEPS = 600000;   // cap on simulated updates (keeps a slider drag responsive)
const SEED = 45;
const WIN = 200;            // updates shown in the time-domain panel
const F_LO = 1e4, F_HI = 1e8;
const Y_LO = 0.2, Y_HI = 5e4;
const N_DEC_LIST = [1, 2, 4, 8, 16, 32, 64];

const DEFAULTS = {
  sigmaFs: 447.9, bits: 6, nDecIdx: 4,
  logF: Math.log10(30e3), logA: Math.log10(SSC_PP_UI), integral: true,
};

// ---- numerics --------------------------------------------------------------
function erf(x) {      // Abramowitz-Stegun 7.1.26 (abs. error < 1.5e-7), enough for drawing
  const s = x < 0 ? -1 : 1;
  const ax = Math.abs(x);
  const t = 1 / (1 + 0.3275911 * ax);
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-ax * ax);
  return s * y;
}

function makeRng(seed) {   // mulberry32 + cached Box-Muller
  let a = seed >>> 0;
  let spare = null;
  const u = () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const g = () => {
    if (spare !== null) { const s = spare; spare = null; return s; }
    let u1 = u(); if (u1 < 1e-300) u1 = 1e-300;
    const r = Math.sqrt(-2 * Math.log(u1));
    const th = 2 * Math.PI * u();
    spare = r * Math.sin(th);
    return r * Math.cos(th);
  };
  return {u, g};
}

// ---- the analytic model (everything the readout cards show) ------------------
export function cdrModel({sigmaFs, bits, nDec, logF, logA, integral}) {
  const sigma = sigmaFs * 1e-15;
  const Kp = UI / Math.pow(2, bits);
  const KpUI = Kp / UI;
  const fu = FB / nDec;
  const Kbb = Math.sqrt(2 / Math.PI) / sigma;
  const KbbUI = Kbb * UI;
  const gp = Kp * Kbb * RHO_T;                          // gain per update (dimensionless)
  const fbw = (gp * fu) / (2 * Math.PI);
  const Ki = integral ? Kp / KI_DIV : 0;
  const KiUI = Ki / UI;
  const gi = Ki * Kbb * RHO_T;
  const slew = RHO_T * KpUI * fu;                       // UI/s
  const accMax = integral ? RHO_T * KiUI * fu * fu : 0; // UI/s^2
  const TJ = 2 * QINV * sigma;
  const margin = 1 - TJ / UI;                           // UI pp
  const sigmaHunt = Math.sqrt(Kp / (2 * Kbb));
  const fn = integral ? (Math.sqrt(gi) * fu) / (2 * Math.PI) : NaN;
  const zeta = integral ? gp / (2 * Math.sqrt(gi)) : NaN;

  const linearAt = (f) => {
    if (!integral) return (margin * Math.sqrt(f * f + fbw * fbw)) / f;
    const w = 2 * Math.PI * f, wn = 2 * Math.PI * fn;
    const hp2 = Math.pow(w, 4) / (Math.pow(wn * wn - w * w, 2) + Math.pow(2 * zeta * wn * w, 2));
    return margin / Math.sqrt(hp2);
  };
  const slewAt = (f) => slew / (Math.PI * f);
  const accAt = (f) => (integral ? accMax / (2 * Math.PI * Math.PI * f * f) : 0);
  const effAt = (f) => Math.min(linearAt(f), Math.max(slewAt(f), accAt(f), margin));

  const f = Math.pow(10, logF);
  const A = Math.pow(10, logA);
  const jtol = effAt(f);
  const pass = A <= jtol;
  const limitName = Math.max(slewAt(f), accAt(f)) >= margin
    ? (accAt(f) > slewAt(f) ? 'acc' : 'slew') : 'plateau';

  // SSC: P only must follow the 5000 ppm peak velocity; P+I only needs a <= a_max
  const sscVel = SSC_DELTA * FB;                        // UI/s
  const sscAcc = sscVel / (1 / SSC_FM / 2);             // UI/s^2
  const sscTracks = integral ? sscAcc <= accMax : slew >= sscVel;
  const sscRatio = integral ? sscAcc / accMax : sscVel / slew;
  const slewPpm = (slew / FB) * 1e6;

  return {
    sigma, Kp, KpUI, fu, Kbb, KbbUI, gp, fbw, Ki, KiUI, gi, slew, accMax, TJ, margin,
    sigmaHunt, fn, zeta, f, A, jtol, pass, limitName, sscTracks, sscRatio, sscAcc, sscVel,
    slewPpm, linearAt, slewAt, accAt, effAt, linRange: sigma * Math.sqrt(Math.PI / 2),
  };
}

// ---- time-domain run: same update rule as lab_45_bb_cdr.bb_loop (vote = 1, D = 0) ----
export function runLoop({sigmaUI, KpUI, KiUI, fu, f, A}) {
  const per = fu / f;
  let nRamp = Math.floor(Math.max(per, 6000));
  let nSteps = Math.floor(Math.max(3 * per, 30000));
  let capped = false;
  if (nSteps > MAX_STEPS) {
    capped = true;
    nSteps = MAX_STEPS;
    nRamp = Math.min(nRamp, Math.floor(nSteps / 3));
  }
  const w = (2 * Math.PI * f) / fu;
  const rng = makeRng(SEED);
  const err = new Float32Array(nSteps);
  let phi = 0, om = 0, worst = 0, worstIdx = nRamp;
  for (let k = 0; k < nSteps; k++) {
    const env = k < nRamp ? 0.5 * (1 - Math.cos((Math.PI * k) / nRamp)) : 1;
    const x = env * Math.sin(w * k) * (A / 2);
    const e0 = x - phi;
    err[k] = e0;
    if (k >= nRamp) {
      const a = Math.abs(e0);
      if (a > worst) { worst = a; worstIdx = k; }
    }
    const errw = e0 - Math.round(e0);                   // PD only sees the error mod UI
    const n = rng.g() * sigmaUI;
    const mask = rng.u() < RHO_T ? 1 : 0;
    const v = errw + n;
    const e = (v > 0 ? 1 : v < 0 ? -1 : 0) * mask;
    phi += KpUI * e + om;
    om += KiUI * e;
  }
  return {err, worst, worstIdx, nRamp, nSteps, capped, covered: (nSteps - nRamp) / per};
}

// ---- small UI helpers ---------------------------------------------------------
function Row({label, value, unit, min, max, step, onChange, fmt, ariaLabel}) {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0', flexWrap: 'wrap'}}>
      <label style={{flex: '0 1 11rem', fontSize: '0.9rem'}}>{label}</label>
      <input
        type="range" min={min} max={max} step={step} value={value}
        aria-label={ariaLabel || label}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{flex: '1 1 auto'}}
      />
      <span style={{flex: '0 0 11.5rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
        <b>{fmt ? fmt(value) : value}</b> {unit}
      </span>
    </div>
  );
}

const fmtSci = (x, d = 3) => {
  if (!isFinite(x)) return '—';
  if (x === 0) return '0';
  const e = Math.floor(Math.log10(Math.abs(x)));
  const m = x / Math.pow(10, e);
  return `${m.toFixed(d - 1)}e${e}`;
};
const fmtF = (f) => (f >= 1e6 ? `${(f / 1e6).toPrecision(3)} MHz` : `${(f / 1e3).toPrecision(3)} kHz`);
const fmtUI = (x) => (x >= 100 ? x.toFixed(0) : x >= 10 ? x.toFixed(1) : x >= 1 ? x.toFixed(2) : x.toFixed(3));

export default function BbCdrExplorer() {
  const isEn = useIsEn();
  const [sigmaFs, setSigmaFs] = useState(DEFAULTS.sigmaFs);
  const [bits, setBits] = useState(DEFAULTS.bits);
  const [nDecIdx, setNDecIdx] = useState(DEFAULTS.nDecIdx);
  const [logF, setLogF] = useState(DEFAULTS.logF);
  const [logA, setLogA] = useState(DEFAULTS.logA);
  const [integral, setIntegral] = useState(DEFAULTS.integral);

  const nDec = N_DEC_LIST[nDecIdx];
  const m = useMemo(
    () => cdrModel({sigmaFs, bits, nDec, logF, logA, integral}),
    [sigmaFs, bits, nDec, logF, logA, integral],
  );

  const run = useMemo(
    () => runLoop({sigmaUI: m.sigma / UI, KpUI: m.KpUI, KiUI: m.KiUI, fu: m.fu, f: m.f, A: m.A}),
    [m.sigma, m.KpUI, m.KiUI, m.fu, m.f, m.A],
  );

  // ---------------- panel 1: PD characteristic ----------------
  const pdSvg = useMemo(() => {
    const W = 460, H = 250, padL = 44, padR = 12, padT = 16, padB = 34;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const XR = 3;                                       // +-3 ps, fixed so sigma_j visibly changes the curve
    const xOf = (ps) => padL + ((ps + XR) / (2 * XR)) * plotW;
    const yOf = (e) => padT + plotH * (1 - (e + 1.1) / 2.2);
    let dErf = '', dTan = '';
    const N = 121;
    for (let i = 0; i < N; i++) {
      const ps = -XR + (2 * XR * i) / (N - 1);
      const e = erf(ps / (Math.SQRT2 * (m.sigma * 1e12)));
      const t = Math.max(-1, Math.min(1, m.Kbb * ps * 1e-12));
      dErf += (i === 0 ? 'M' : 'L') + xOf(ps).toFixed(1) + ',' + yOf(e).toFixed(1) + ' ';
      dTan += (i === 0 ? 'M' : 'L') + xOf(ps).toFixed(1) + ',' + yOf(t).toFixed(1) + ' ';
    }
    const lr = m.linRange * 1e12;
    return {W, H, padL, padT, plotW, plotH, xOf, yOf, dErf, dTan, lr, XR};
  }, [m.sigma, m.Kbb, m.linRange]);

  // ---------------- panel 2: time-domain run ----------------
  const tdSvg = useMemo(() => {
    const W = 460, H = 250, padL = 44, padR = 12, padT = 16, padB = 34;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const start = Math.max(run.nRamp, Math.min(run.worstIdx - 60, run.nSteps - WIN));
    const end = Math.min(run.nSteps, start + WIN);
    const KpPs = m.Kp * 1e12;
    let lo = Infinity, hi = -Infinity;
    for (let k = start; k < end; k++) {
      const v = run.err[k] * 40;                       // UI -> ps (UI = 40 ps)
      if (v < lo) lo = v;
      if (v > hi) hi = v;
    }
    const minSpan = 3 * KpPs;                          // never zoom below three PI steps
    if (hi - lo < minSpan) {
      const c = 0.5 * (hi + lo);
      lo = c - minSpan / 2; hi = c + minSpan / 2;
    }
    const pad = 0.1 * (hi - lo);
    lo -= pad; hi += pad;
    const useUI = hi - lo > 400;
    const sc = useUI ? 1 / 40 : 1;                     // ps -> displayed unit
    const xOf = (i) => padL + (i / (WIN - 1)) * plotW;
    const yOf = (ps) => padT + plotH * (1 - (ps - lo) / (hi - lo));
    let d = '';
    for (let k = start; k < end; k++) {
      d += (k === start ? 'M' : 'L') + xOf(k - start).toFixed(1) + ',' + yOf(run.err[k] * 40).toFixed(1) + ' ';
    }
    const allowedPs = (m.margin / 2) * 40;
    const bandTop = Math.max(padT, yOf(KpPs / 2));     // band of one K_p around 0, clipped to the plot
    const bandBot = Math.min(padT + plotH, yOf(-KpPs / 2));
    return {W, H, padL, padT, plotW, plotH, xOf, yOf, d, lo, hi, sc, useUI, KpPs, allowedPs, start, bandTop, bandBot};
  }, [run, m.Kp, m.margin]);

  // ---------------- panel 3: JTOL chart ----------------
  const jSvg = useMemo(() => {
    const W = 460, H = 270, padL = 46, padR = 12, padT = 16, padB = 34;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const lx0 = Math.log10(F_LO), lx1 = Math.log10(F_HI);
    const ly0 = Math.log10(Y_LO), ly1 = Math.log10(Y_HI);
    const xOf = (f) => padL + ((Math.log10(f) - lx0) / (lx1 - lx0)) * plotW;
    const yOfRaw = (v) => padT + plotH * (1 - (Math.log10(v) - ly0) / (ly1 - ly0));
    const inRange = (v) => v >= Y_LO && v <= Y_HI;
    const mk = (fn) => {
      let d = '', pen = false;
      const N = 160;
      for (let i = 0; i < N; i++) {
        const f = Math.pow(10, lx0 + ((lx1 - lx0) * i) / (N - 1));
        const v = fn(f);
        if (!(v > 0) || !inRange(v)) { pen = false; continue; }
        d += (pen ? 'L' : 'M') + xOf(f).toFixed(1) + ',' + yOfRaw(v).toFixed(1) + ' ';
        pen = true;
      }
      return d;
    };
    const clampY = (v) => yOfRaw(Math.max(Y_LO, Math.min(Y_HI, v)));
    return {
      W, H, padL, padT, plotW, plotH, xOf, yOfRaw, clampY,
      dLin: mk(m.linearAt), dSlew: mk(m.slewAt), dAcc: m.accMax > 0 ? mk(m.accAt) : '',
      dEff: mk(m.effAt),
    };
  }, [m]);

  // ---------------- styles ----------------
  const axisColor = 'var(--ifm-color-emphasis-500)';
  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)', borderRadius: '8px',
    padding: '1rem 1.1rem', margin: '1rem 0', background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 9.5rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.55rem 0.7rem', textAlign: 'center',
  };
  const cardsRow = {display: 'flex', gap: '0.7rem', flexWrap: 'wrap', marginTop: '0.7rem'};
  const cardLabel = {fontSize: '0.75rem', opacity: 0.72};
  const cardVal = {fontSize: '1.1rem', fontWeight: 700, fontVariantNumeric: 'tabular-nums'};
  const cardSub = {fontSize: '0.72rem', opacity: 0.85};
  const panelsRow = {display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-start', marginTop: '0.8rem'};
  const panel = {flex: '1 1 21rem', minWidth: '260px'};
  const panelTitle = {fontSize: '0.82rem', opacity: 0.8, marginBottom: '0.25rem'};
  const svgStyle = (w) => ({maxWidth: `${w}px`, display: 'block', background: 'var(--ifm-background-color)', borderRadius: '6px'});
  const btn = {
    padding: '0.3rem 0.8rem', borderRadius: '6px', cursor: 'pointer',
    border: '1px solid var(--ifm-color-emphasis-300)',
    background: 'var(--ifm-background-surface-color)',
    color: 'var(--ifm-font-color-base)', fontSize: '0.82rem',
  };
  const btnActive = {...btn, background: 'var(--ifm-color-primary)', color: '#fff', border: '1px solid var(--ifm-color-primary)', fontWeight: 700};
  const okColor = 'var(--ifm-color-success)';
  const badColor = 'var(--ifm-color-danger)';

  const reset = () => {
    setSigmaFs(DEFAULTS.sigmaFs); setBits(DEFAULTS.bits); setNDecIdx(DEFAULTS.nDecIdx);
    setLogF(DEFAULTS.logF); setLogA(DEFAULTS.logA); setIntegral(DEFAULTS.integral);
  };

  const simOk = run.worst <= m.margin / 2;
  const limitText = {
    acc: isEn ? 'acceleration line' : '加速度線',
    slew: isEn ? 'slew line' : 'slew 線',
    plateau: isEn ? 'plateau (UI − TJ_eye)' : '平台 (UI − TJ_eye)',
  }[m.limitName];
  const linearMin = m.linearAt(m.f) < Math.max(m.slewAt(m.f), m.accAt(m.f), m.margin);
  const warnKp = m.Kp > m.sigma;
  const warnGain = m.gp >= 2;

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Bang-bang CDR explorer — K_bb, hunting, bandwidth, JTOL and SSC tracking'
          : 'Bang-bang CDR 互動探索器 —— K_bb、hunting、頻寬、JTOL 與 SSC 追蹤'}
      </div>

      <Row label={isEn ? 'RMS jitter σ_j' : 'RMS jitter σ_j'} value={sigmaFs} unit="fs" min={200} max={1500} step={0.1}
           ariaLabel={isEn ? 'rms jitter between data edge and clock in femtoseconds' : '資料邊緣與時脈之間的 rms jitter（fs）'}
           onChange={setSigmaFs} fmt={(v) => v.toFixed(1)} />
      <Row label={isEn ? 'PI resolution b' : 'PI 位元數 b'} value={bits} unit={`bit → ${(UI / Math.pow(2, bits) * 1e12).toFixed(3)} ps`}
           min={4} max={8} step={1}
           ariaLabel={isEn ? 'phase interpolator bits per unit interval' : '相位內插器每個 UI 的位元數'}
           onChange={(v) => setBits(Math.round(v))} fmt={(v) => v.toFixed(0)} />
      <Row label={isEn ? 'Decimation N_dec' : '降頻倍數 N_dec'} value={nDecIdx} unit={`→ f_u = ${(FB / nDec / 1e9).toPrecision(4)} GHz`}
           min={0} max={N_DEC_LIST.length - 1} step={1}
           ariaLabel={isEn ? 'decimation factor, one phase update every N_dec unit intervals' : '降頻倍數，每 N_dec 個 UI 更新一次相位'}
           onChange={(v) => setNDecIdx(Math.round(v))} fmt={(v) => String(N_DEC_LIST[Math.round(v)])} />
      <Row label={isEn ? 'Sinusoidal-jitter frequency' : '正弦 jitter 頻率'} value={logF} unit="" min={4} max={8} step="any"
           ariaLabel={isEn ? 'sinusoidal jitter frequency, logarithmic slider from 10 kHz to 100 MHz' : '正弦 jitter 頻率（對數滑桿，10 kHz 到 100 MHz）'}
           onChange={setLogF} fmt={(v) => fmtF(Math.pow(10, v))} />
      <Row label={isEn ? 'Sinusoidal-jitter amplitude' : '正弦 jitter 振幅'} value={logA} unit="UI pp" min={-0.5} max={3.5} step="any"
           ariaLabel={isEn ? 'sinusoidal jitter amplitude in unit intervals peak to peak, logarithmic slider' : '正弦 jitter 峰峰振幅（UI，對數滑桿）'}
           onChange={setLogA} fmt={(v) => fmtUI(Math.pow(10, v))} />
      <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0', flexWrap: 'wrap'}}>
        <label style={{flex: '0 1 11rem', fontSize: '0.9rem'}}>{isEn ? 'Integral path (K_i = K_p/1024)' : '積分路徑（K_i = K_p/1024）'}</label>
        <button type="button" style={integral ? btnActive : btn} aria-pressed={integral}
                aria-label={isEn ? 'integral path on' : '積分路徑開'} onClick={() => setIntegral(true)}>
          {isEn ? 'P + I' : '比例＋積分'}
        </button>
        <button type="button" style={!integral ? btnActive : btn} aria-pressed={!integral}
                aria-label={isEn ? 'integral path off, proportional only' : '積分路徑關，只有比例路徑'} onClick={() => setIntegral(false)}>
          {isEn ? 'P only' : '只有比例'}
        </button>
        <button type="button" style={btn}
                aria-label={isEn ? 'reset all controls to the page defaults' : '全部控制項還原為本頁預設值'} onClick={reset}>
          {isEn ? 'Reset to page values' : '還原本頁預設'}
        </button>
      </div>

      <div style={cardsRow}>
        <div style={card}>
          <div style={cardLabel}>K_bb = √(2/π)/σ_j</div>
          <div style={cardVal}>{fmtSci(m.Kbb, 4)} s⁻¹</div>
          <div style={cardSub}>= {m.KbbUI.toFixed(1)} {isEn ? 'per UI' : '每 UI'} · {isEn ? 'linear range' : '線性區'} ±{(m.linRange * 1e12).toFixed(3)} ps</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'hunting DJ pp, (2D+1)K_p' : 'hunting DJ 峰峰 (2D+1)K_p'}</div>
          <div style={cardVal}>{(m.Kp * 1e12).toFixed(3)} ps</div>
          <div style={cardSub}>D = 0 · D = 2: {(5 * m.Kp * 1e12).toFixed(3)} ps · σ_hunt = {(m.sigmaHunt * 1e15).toFixed(0)} fs</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'proportional-path BW f_BW' : '比例路徑頻寬 f_BW'}</div>
          <div style={cardVal}>{m.fbw >= 1e9 ? `${(m.fbw / 1e9).toFixed(2)} GHz` : `${(m.fbw / 1e6).toFixed(1)} MHz`}</div>
          <div style={cardSub}>K_pK_bbρ_T = {m.gp.toFixed(3)} {isEn ? 'per update' : '每次更新'}</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? `JTOL at ${fmtF(m.f)}` : `JTOL @ ${fmtF(m.f)}`}</div>
          <div style={{...cardVal, color: m.pass ? okColor : badColor}}>{fmtUI(m.jtol)} UI pp</div>
          <div style={cardSub}>
            {isEn ? 'applied' : '施加'} {fmtUI(m.A)} UI → {m.pass ? (isEn ? 'pass' : '通過') : (isEn ? 'FAIL' : '失敗')} ·{' '}
            {linearMin ? (isEn ? 'linear loop' : '線性迴路') : limitText}
          </div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'tracks SSC (−0.5 %, 30 kHz)?' : '追得上 SSC（−0.5 %、30 kHz）？'}</div>
          <div style={{...cardVal, color: m.sscTracks ? okColor : badColor}}>{m.sscTracks ? (isEn ? 'yes' : '是') : (isEn ? 'no' : '否')}</div>
          <div style={cardSub}>
            {integral
              ? `a/a_max = ${m.sscRatio.toFixed(3)}`
              : `${isEn ? 'slew' : 'slew'} ${m.slewPpm.toFixed(0)} ppm ${m.slewPpm >= 5000 ? '≥' : '<'} 5000 ppm`}
          </div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'eye margin UI − TJ_eye' : '眼圖裕度 UI − TJ_eye'}</div>
          <div style={cardVal}>{m.margin.toFixed(3)} UI</div>
          <div style={cardSub}>TJ_eye = 2·7.03·σ_j = {(m.TJ * 1e12).toFixed(2)} ps</div>
        </div>
      </div>

      {(warnKp || warnGain) && (
        <div role="note" style={{fontSize: '0.78rem', marginTop: '0.6rem', color: 'var(--ifm-color-warning-darkest, var(--ifm-color-emphasis-800))'}}>
          {warnKp && (isEn
            ? `K_p/σ_j = ${(m.Kp / m.sigma).toFixed(2)} > 1: the PI step exceeds the jitter, so the erf has already bent — hunting dominates and the linearised K_bb and f_BW are optimistic (the page's Monte-Carlo gives 94 MHz against the nominal 138 MHz at the default).`
            : `K_p/σ_j = ${(m.Kp / m.sigma).toFixed(2)} > 1：PI 步伐大於 jitter，erf 已彎，hunting 主導，線性化的 K_bb 與 f_BW 偏樂觀（本頁預設值的 Monte-Carlo 為 94 MHz，名義值 138 MHz）。`)}
          {warnKp && warnGain ? ' ' : ''}
          {warnGain && (isEn
            ? `K_pK_bbρ_T = ${m.gp.toFixed(2)} ≥ 2: the discrete loop is unstable.`
            : `K_pK_bbρ_T = ${m.gp.toFixed(2)} ≥ 2：離散迴路不穩定。`)}
        </div>
      )}

      <div style={panelsRow}>
        <div style={panel}>
          <div style={panelTitle}>
            {isEn ? '(1) PD characteristic ⟨e⟩ = erf(Δt/√2σ_j) and the tangent K_bb·Δt' : '(1) PD 特性 ⟨e⟩ = erf(Δt/√2σ_j) 與切線 K_bb·Δt'}
          </div>
          <svg viewBox={`0 0 ${pdSvg.W} ${pdSvg.H}`} width="100%" role="img" style={svgStyle(pdSvg.W)}
               aria-label={isEn
                 ? `Mean phase-detector output versus static timing offset from minus 3 to plus 3 picoseconds: an erf curve with rms jitter ${(m.sigma * 1e15).toFixed(0)} femtoseconds, its tangent at the origin with slope K_bb, and the PI step marked`
                 : `PD 平均輸出對靜態時間偏移（−3 到 +3 ps）：rms jitter ${(m.sigma * 1e15).toFixed(0)} fs 的 erf 曲線、原點的切線（斜率 K_bb）與 PI 步伐標示`}>
            <rect x={pdSvg.padL} y={pdSvg.padT} width={pdSvg.plotW} height={pdSvg.plotH} fill="none" stroke={axisColor} strokeWidth="1" />
            <line x1={pdSvg.padL} x2={pdSvg.padL + pdSvg.plotW} y1={pdSvg.yOf(0)} y2={pdSvg.yOf(0)} stroke={axisColor} strokeWidth="0.6" strokeDasharray="2 3" />
            <line x1={pdSvg.xOf(0)} x2={pdSvg.xOf(0)} y1={pdSvg.padT} y2={pdSvg.padT + pdSvg.plotH} stroke={axisColor} strokeWidth="0.6" strokeDasharray="2 3" />
            <line x1={pdSvg.padL} x2={pdSvg.padL + pdSvg.plotW} y1={pdSvg.yOf(1)} y2={pdSvg.yOf(1)} stroke={axisColor} strokeWidth="0.5" opacity="0.6" />
            <line x1={pdSvg.padL} x2={pdSvg.padL + pdSvg.plotW} y1={pdSvg.yOf(-1)} y2={pdSvg.yOf(-1)} stroke={axisColor} strokeWidth="0.5" opacity="0.6" />
            <path d={pdSvg.dTan} fill="none" stroke="var(--ifm-color-success)" strokeWidth="1.6" strokeDasharray="5 3" />
            <path d={pdSvg.dErf} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2.2" />
            {[-1, 1].map((s) => (
              <circle key={s} cx={pdSvg.xOf(s * pdSvg.lr)} cy={pdSvg.yOf(s)} r="3.2" fill="var(--ifm-color-success)" />
            ))}
            <rect x={pdSvg.xOf(-m.Kp * 0.5e12)} y={pdSvg.padT + pdSvg.plotH - 7} width={Math.max(1.5, pdSvg.xOf(m.Kp * 0.5e12) - pdSvg.xOf(-m.Kp * 0.5e12))} height="5"
                  fill="var(--ifm-color-danger)" opacity="0.85" />
            <text x={pdSvg.xOf(0)} y={pdSvg.padT + pdSvg.plotH - 10} fontSize="9" textAnchor="middle" fill="var(--ifm-color-danger)">K_p</text>
            {[-3, 0, 3].map((t) => (
              <text key={t} x={pdSvg.xOf(t)} y={pdSvg.H - 20} fontSize="10" textAnchor="middle" fill={axisColor}>{t}</text>
            ))}
            {[-1, 0, 1].map((t) => (
              <text key={t} x={pdSvg.padL - 5} y={pdSvg.yOf(t) + 3} fontSize="10" textAnchor="end" fill={axisColor}>{t}</text>
            ))}
            <text x={pdSvg.padL + pdSvg.plotW / 2} y={pdSvg.H - 6} fontSize="10" textAnchor="middle" fill={axisColor}>
              {isEn ? 'static offset Δt [ps] (clock early = positive)' : '靜態偏移 Δt [ps]（時脈早為正）'}
            </text>
            <text x={6} y={pdSvg.padT + 8} fontSize="10" fill={axisColor}>⟨e⟩</text>
          </svg>
          <div style={{display: 'flex', gap: '0.9rem', flexWrap: 'wrap', fontSize: '0.72rem', marginTop: '0.25rem'}}>
            <span><span style={{color: 'var(--ifm-color-primary)'}}>▬</span> erf</span>
            <span><span style={{color: 'var(--ifm-color-success)'}}>▬ ▬</span> {isEn ? 'tangent, hits ±1 at ±σ_j√(π/2) (dots)' : '切線，在 ±σ_j√(π/2) 打到 ±1（圓點）'}</span>
            <span><span style={{color: 'var(--ifm-color-danger)'}}>■</span> {isEn ? 'one PI step K_p' : '一個 PI 步伐 K_p'}</span>
          </div>
          <div style={{fontSize: '0.72rem', opacity: 0.68, marginTop: '0.3rem'}}>
            {isEn ? 'Transitions only; averaged over all bits the curve is scaled by ρ_T = 0.5.' : '只算有轉態的位元；對全部位元平均要再乘 ρ_T = 0.5。'}
          </div>
        </div>

        <div style={panel}>
          <div style={panelTitle}>
            {isEn ? `(2) Loop phase error, ${WIN} updates (seed ${SEED}) — the hunting` : `(2) 迴路相位誤差，${WIN} 次更新（種子 ${SEED}）—— hunting`}
          </div>
          <svg viewBox={`0 0 ${tdSvg.W} ${tdSvg.H}`} width="100%" role="img" style={svgStyle(tdSvg.W)}
               aria-label={isEn
                 ? `Simulated loop phase error versus update index for ${WIN} updates around the worst moment of the run, with a band one PI step wide around zero; the loop is ${integral ? 'proportional plus integral' : 'proportional only'}`
                 : `迴路相位誤差對更新序號（取整個模擬中最糟時刻附近的 ${WIN} 次更新），零點附近畫出一個 PI 步伐寬的色帶；迴路為${integral ? '比例加積分' : '只有比例路徑'}`}>
            <rect x={tdSvg.padL} y={tdSvg.padT} width={tdSvg.plotW} height={tdSvg.plotH} fill="none" stroke={axisColor} strokeWidth="1" />
            {tdSvg.bandBot > tdSvg.bandTop && (
              <rect x={tdSvg.padL} y={tdSvg.bandTop} width={tdSvg.plotW}
                    height={Math.max(1, tdSvg.bandBot - tdSvg.bandTop)}
                    fill="var(--ifm-color-danger)" opacity="0.14" />
            )}
            {tdSvg.lo < 0 && tdSvg.hi > 0 && (
              <line x1={tdSvg.padL} x2={tdSvg.padL + tdSvg.plotW} y1={tdSvg.yOf(0)} y2={tdSvg.yOf(0)} stroke={axisColor} strokeWidth="0.6" strokeDasharray="2 3" />
            )}
            {[tdSvg.allowedPs, -tdSvg.allowedPs].filter((v) => v > tdSvg.lo && v < tdSvg.hi).map((v) => (
              <line key={v} x1={tdSvg.padL} x2={tdSvg.padL + tdSvg.plotW} y1={tdSvg.yOf(v)} y2={tdSvg.yOf(v)}
                    stroke="var(--ifm-color-warning)" strokeWidth="1.2" strokeDasharray="5 3" />
            ))}
            <path d={tdSvg.d} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="1.3" strokeLinejoin="round" />
            <text x={tdSvg.padL - 5} y={tdSvg.padT + 8} fontSize="10" textAnchor="end" fill={axisColor}>{(tdSvg.hi * tdSvg.sc).toPrecision(3)}</text>
            <text x={tdSvg.padL - 5} y={tdSvg.padT + tdSvg.plotH} fontSize="10" textAnchor="end" fill={axisColor}>{(tdSvg.lo * tdSvg.sc).toPrecision(3)}</text>
            <text x={tdSvg.padL} y={tdSvg.H - 20} fontSize="10" fill={axisColor}>k = {tdSvg.start}</text>
            <text x={tdSvg.padL + tdSvg.plotW} y={tdSvg.H - 20} fontSize="10" textAnchor="end" fill={axisColor}>k = {tdSvg.start + WIN}</text>
            <text x={tdSvg.padL + tdSvg.plotW / 2} y={tdSvg.H - 6} fontSize="10" textAnchor="middle" fill={axisColor}>
              {isEn ? 'update index k' : '更新序號 k'}
            </text>
            <text x={6} y={tdSvg.padT + 8} fontSize="10" fill={axisColor}>{tdSvg.useUI ? 'UI' : 'ps'}</text>
          </svg>
          <div style={{display: 'flex', gap: '0.9rem', flexWrap: 'wrap', fontSize: '0.72rem', marginTop: '0.25rem'}}>
            <span><span style={{color: 'var(--ifm-color-danger)'}}>■</span> {isEn ? 'one K_p wide around 0' : '0 附近寬 K_p 的色帶'}</span>
            <span><span style={{color: 'var(--ifm-color-warning)'}}>▬ ▬</span> ±(UI − TJ_eye)/2</span>
          </div>
          <div style={{fontSize: '0.74rem', marginTop: '0.3rem', lineHeight: 1.5}}>
            {isEn ? 'Peak |error| over the run: ' : '整段模擬的最大 |誤差|：'}
            <b style={{color: simOk ? okColor : badColor}}>{fmtUI(run.worst)} UI</b>
            {isEn ? ` against the allowed ${fmtUI(m.margin / 2)} UI → ` : `，允許值 ${fmtUI(m.margin / 2)} UI → `}
            <b style={{color: simOk ? okColor : badColor}}>{simOk ? (isEn ? 'inside' : '在裕度內') : (isEn ? 'outside' : '超出裕度')}</b>
            {run.capped
              ? (isEn ? ` (run capped at ${run.nSteps} updates = ${run.covered.toFixed(2)} jitter periods)` : `（模擬上限 ${run.nSteps} 次更新，只涵蓋 ${run.covered.toFixed(2)} 個 jitter 週期）`)
              : ''}
          </div>
        </div>

        <div style={panel}>
          <div style={panelTitle}>
            {isEn ? '(3) JTOL: linear curve, slew line, acceleration line and the operating point' : '(3) JTOL：線性曲線、slew 線、加速度線與操作點'}
          </div>
          <svg viewBox={`0 0 ${jSvg.W} ${jSvg.H}`} width="100%" role="img" style={svgStyle(jSvg.W)}
               aria-label={isEn
                 ? `Log-log chart of tolerable sinusoidal jitter in unit intervals peak to peak versus jitter frequency from 10 kilohertz to 100 megahertz: the linear small-signal curve, the slew line, ${integral ? 'the acceleration line, ' : ''}the resulting tolerance, and the operating point at ${fmtF(m.f)} and ${fmtUI(m.A)} unit intervals, which ${m.pass ? 'passes' : 'fails'}`
                 : `可容忍正弦 jitter（UI 峰峰）對 jitter 頻率（10 kHz 到 100 MHz）的雙對數圖：線性小訊號曲線、slew 線、${integral ? '加速度線、' : ''}合成容忍度，以及 ${fmtF(m.f)}、${fmtUI(m.A)} UI 的操作點，結果為${m.pass ? '通過' : '失敗'}`}>
            <rect x={jSvg.padL} y={jSvg.padT} width={jSvg.plotW} height={jSvg.plotH} fill="none" stroke={axisColor} strokeWidth="1" />
            {[1, 10, 100, 1000, 10000].map((v) => (
              <g key={v}>
                <line x1={jSvg.padL} x2={jSvg.padL + jSvg.plotW} y1={jSvg.yOfRaw(v)} y2={jSvg.yOfRaw(v)} stroke={axisColor} strokeWidth="0.4" opacity="0.5" />
                <text x={jSvg.padL - 5} y={jSvg.yOfRaw(v) + 3} fontSize="10" textAnchor="end" fill={axisColor}>{v >= 1000 ? `${v / 1000}k` : v}</text>
              </g>
            ))}
            {[[1e4, '10k'], [1e5, '100k'], [1e6, '1M'], [1e7, '10M'], [1e8, '100M']].map(([f, t]) => (
              <g key={t}>
                <line x1={jSvg.xOf(f)} x2={jSvg.xOf(f)} y1={jSvg.padT} y2={jSvg.padT + jSvg.plotH} stroke={axisColor} strokeWidth="0.4" opacity="0.5" />
                <text x={jSvg.xOf(f)} y={jSvg.H - 20} fontSize="10" textAnchor="middle" fill={axisColor}>{t}</text>
              </g>
            ))}
            <line x1={jSvg.padL} x2={jSvg.padL + jSvg.plotW} y1={jSvg.clampY(m.margin)} y2={jSvg.clampY(m.margin)}
                  stroke={axisColor} strokeWidth="1" strokeDasharray="2 3" />
            <path d={jSvg.dLin} fill="none" stroke="var(--ifm-font-color-base)" strokeWidth="1" opacity="0.7" />
            <path d={jSvg.dSlew} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="1.3" strokeDasharray="6 3" />
            {jSvg.dAcc && <path d={jSvg.dAcc} fill="none" stroke="var(--ifm-color-danger)" strokeWidth="1.3" strokeDasharray="6 3" />}
            <path d={jSvg.dEff} fill="none" stroke="var(--ifm-color-success)" strokeWidth="2.6" opacity="0.9" />
            <line x1={jSvg.xOf(m.f)} x2={jSvg.xOf(m.f)} y1={jSvg.padT} y2={jSvg.padT + jSvg.plotH}
                  stroke={m.pass ? okColor : badColor} strokeWidth="0.8" opacity="0.5" strokeDasharray="3 3" />
            <polygon points={`${jSvg.xOf(SSC_FM)},${jSvg.clampY(SSC_PP_UI) - 6} ${jSvg.xOf(SSC_FM) + 5},${jSvg.clampY(SSC_PP_UI)} ${jSvg.xOf(SSC_FM)},${jSvg.clampY(SSC_PP_UI) + 6} ${jSvg.xOf(SSC_FM) - 5},${jSvg.clampY(SSC_PP_UI)}`}
                     fill="none" stroke="var(--ifm-color-info, var(--ifm-color-primary))" strokeWidth="1.6" />
            {m.pass
              ? <circle cx={jSvg.xOf(m.f)} cy={jSvg.clampY(m.A)} r="5.5" fill={okColor} stroke="var(--ifm-background-color)" strokeWidth="1.2" />
              : (
                <g stroke={badColor} strokeWidth="2.4" strokeLinecap="round">
                  <line x1={jSvg.xOf(m.f) - 5} y1={jSvg.clampY(m.A) - 5} x2={jSvg.xOf(m.f) + 5} y2={jSvg.clampY(m.A) + 5} />
                  <line x1={jSvg.xOf(m.f) - 5} y1={jSvg.clampY(m.A) + 5} x2={jSvg.xOf(m.f) + 5} y2={jSvg.clampY(m.A) - 5} />
                </g>
              )}
            <text x={jSvg.padL + jSvg.plotW / 2} y={jSvg.H - 6} fontSize="10" textAnchor="middle" fill={axisColor}>
              {isEn ? 'jitter frequency f [Hz]' : '正弦 jitter 頻率 f [Hz]'}
            </text>
            <text x={6} y={jSvg.padT + 8} fontSize="10" fill={axisColor}>UI pp</text>
          </svg>
          <div style={{display: 'flex', gap: '0.9rem', flexWrap: 'wrap', fontSize: '0.72rem', marginTop: '0.25rem'}}>
            <span><span style={{color: 'var(--ifm-font-color-base)'}}>▬</span> {isEn ? 'linear small-signal' : '線性小訊號'}</span>
            <span><span style={{color: 'var(--ifm-color-primary)'}}>▬ ▬</span> {isEn ? 'slew line (P path)' : 'slew 線（比例路徑）'}</span>
            {integral && <span><span style={{color: 'var(--ifm-color-danger)'}}>▬ ▬</span> {isEn ? 'acceleration line (I path)' : '加速度線（積分路徑）'}</span>}
            <span><span style={{color: 'var(--ifm-color-success)'}}>▬</span> {isEn ? 'JTOL used' : '採用的 JTOL'}</span>
            <span><span style={{color: 'var(--ifm-color-info, var(--ifm-color-primary))'}}>◇</span> {isEn ? 'SSC need, 521 UI @ 30 kHz' : 'SSC 需求 521 UI @ 30 kHz'}</span>
            <span>{isEn ? 'dots: plateau UI − TJ_eye' : '點線：平台 UI − TJ_eye'}</span>
          </div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.78, marginTop: '0.7rem', lineHeight: 1.6}}>
        {isEn ? (
          <>
            Formulas (all from this page): K_bb = √(2/π)/σ_j (Step 2); K_p = UI/2^b, f_u = f_b/N_dec, f_BW = ρ_T K_p K_bb f_u/2π and the
            (2D+1)K_p hunting limit cycle (Step 3, D = 0 here; σ_hunt = √(K_p/2K_bb) is the linearised rms from the Numerical-check section);
            margin = UI − TJ_eye with TJ_eye = 2·7.03·σ_j (Step 4); slew line ρ_T(K_p/UI)f_u/(πf) and acceleration line
            ρ_T(K_i/UI)f_u²/(2π²f²) with K_i = K_p/1024 (Steps 4–5). The tolerance drawn is min(linear, max(large-signal lines, margin)):
            the linear curve is the first-order |1−H| for P only, or the type-II one with f_n = √(K_iK_bbρ_T)·f_u/2π and
            ζ = K_pK_bbρ_T/(2√(K_iK_bbρ_T)) for P + I; the large-signal lines are the Step 4–5 limits, and the margin is the floor that
            remains when the loop cannot follow at all. SSC tracking: with the integral path a_ssc = δ·f_b/(T_m/2) = 7.5×10¹² UI/s² must not
            exceed a_max; proportional only, the slew rate must exceed the 5000 ppm peak frequency offset. Panel (2) is the page's own
            behavioural model (one Alexander decision per update, ρ_T = 0.5, white Gaussian σ_j, ideal PI, latency D = 0, fixed seed {SEED}),
            started with a raised-cosine ramp of the sinusoid, and shows the {WIN} updates around the largest error; its peak error is judged
            against (UI − TJ_eye)/2, as in the lab. Limits: pedagogical behavioural model, not transistor level; the linearised numbers are
            optimistic once K_p exceeds σ_j; near the pass/fail boundary the simulated verdict can differ from the analytic curve by the
            few-percent scatter seen in the lab (measured/line ≈ 0.93–1.01 on the page).
          </>
        ) : (
          <>
            公式（全部取自本頁）：K_bb = √(2/π)/σ_j（第 2 步）；K_p = UI/2^b、f_u = f_b/N_dec、f_BW = ρ_T K_p K_bb f_u/2π 與
            (2D+1)K_p 的 hunting 極限環（第 3 步，此處 D = 0；σ_hunt = √(K_p/2K_bb) 是數值驗證一節的線性化 rms）；
            裕度 = UI − TJ_eye，TJ_eye = 2·7.03·σ_j（第 4 步）；slew 線 ρ_T(K_p/UI)f_u/(πf)、加速度線
            ρ_T(K_i/UI)f_u²/(2π²f²)，K_i = K_p/1024（第 4–5 步）。圖中採用的容忍度是 min(線性值, max(大訊號線, 裕度))：
            線性曲線在只有比例路徑時是一階 |1−H|，有積分路徑時是 type-II，f_n = √(K_iK_bbρ_T)·f_u/2π、
            ζ = K_pK_bbρ_T/(2√(K_iK_bbρ_T))；大訊號線就是第 4–5 步的上限，裕度是迴路完全追不上時剩下的底。
            SSC 追蹤：有積分路徑時，a_ssc = δ·f_b/(T_m/2) = 7.5×10¹² UI/s² 不可超過 a_max；只有比例路徑時，slew 速率要大於 5000 ppm 的峰值頻偏。
            面板 (2) 就是本頁數值驗證的行為級模型（每次更新一個 Alexander 判斷、ρ_T = 0.5、白色高斯 σ_j、理想 PI、延遲 D = 0、固定種子 {SEED}），
            正弦以升餘弦斜坡啟動，畫出最大誤差附近的 {WIN} 次更新；峰值誤差與實驗室一樣對照 (UI − TJ_eye)/2。
            限制：這是 pedagogical 行為級模型，不是電晶體級；K_p 大於 σ_j 後線性化的數字偏樂觀；靠近通過／失敗邊界時，
            模擬判定與解析曲線可差實驗室裡那幾個百分點的散布（本頁量測／理論線 ≈ 0.93–1.01）。
          </>
        )}
      </div>
    </div>
  );
}
