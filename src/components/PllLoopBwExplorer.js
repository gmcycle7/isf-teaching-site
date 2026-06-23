import React, {useState, useMemo} from 'react';

// Interactive PLL loop-bandwidth explorer.
//
// A type-II 2nd-order PLL referred to the OUTPUT phase low-pass-filters the
// reference path and high-pass-filters the VCO path (see pll_utils.py /
// lab_20). The closed-loop output phase-noise PSD is
//
//   S_out(f) = S_ref(f) * |H_lp|^2 + S_vco(f) * |H_hp|^2          (spec 10.2)
//
// with the normalized power transfers (w = 2*pi*f, wn = 2*pi*f_n, zeta):
//
//   |H_lp|^2 = ((2 zeta wn w)^2 + wn^4) / ((wn^2 - w^2)^2 + (2 zeta wn w)^2)
//   |H_hp|^2 = w^4 / ((wn^2 - w^2)^2 + (2 zeta wn w)^2)
//
// Reference noise modeled as a flat (white) in-band floor; the free-running VCO
// as a 1/f^2 skirt anchored at 1 MHz. Integrated rms jitter (spec formula 19):
//
//   sigma_t = (1 / 2 pi f0) * sqrt( integral S_out df )
//
// Moving the loop BW f_n trades in-band reference noise (grows with f_n) against
// out-of-band VCO noise (shrinks with f_n) -> there is an OPTIMAL f_n that
// minimizes integrated jitter. Pure client component, SSR-safe, no plotting
// libs (inline SVG). Pedagogical toy model, not a specific silicon loop.

const TWO_PI = 2 * Math.PI;
const ZETA = 0.707;        // damping (maximally-flat-ish, fixed)
const F_ANCHOR = 1e6;      // 1 MHz anchor for both noise levels [Hz]
const F_LO = 1e3;          // integration / plot band lower edge [Hz]
const F_HI = 1e9;          // integration / plot band upper edge [Hz]
const NPTS = 400;          // log-spaced points across the band
const NSWEEP = 160;        // f_n grid for the optimum search

// ---- transfer functions (power), exactly pll_utils.py ----
function Hlp2(f, fn, zeta) {
  const w = TWO_PI * f, wn = TWO_PI * fn;
  const num = (2 * zeta * wn * w) ** 2 + wn ** 4;
  const den = (wn * wn - w * w) ** 2 + (2 * zeta * wn * w) ** 2;
  return num / den;
}
function Hhp2(f, fn, zeta) {
  const w = TWO_PI * f, wn = TWO_PI * fn;
  const num = w ** 4;
  const den = (wn * wn - w * w) ** 2 + (2 * zeta * wn * w) ** 2;
  return num / den;
}

// log-spaced offset-frequency grid (shared by plot + integration)
function logGrid(fLo, fHi, n) {
  const out = new Array(n);
  const a = Math.log10(fLo), b = Math.log10(fHi);
  for (let i = 0; i < n; i++) out[i] = Math.pow(10, a + (b - a) * (i / (n - 1)));
  return out;
}

// trapezoidal integral of S over linear f given a (log-spaced) grid
function integrate(fGrid, S) {
  let acc = 0;
  for (let i = 1; i < fGrid.length; i++) {
    acc += 0.5 * (S[i] + S[i - 1]) * (fGrid[i] - fGrid[i - 1]);
  }
  return acc;
}

function Slider({label, value, unit, min, max, step, onChange, fmt}) {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.3rem 0'}}>
      <label style={{flex: '0 0 11rem', fontSize: '0.9rem'}}>{label}</label>
      <input type="range" min={min} max={max} step={step} value={value}
             onChange={(e) => onChange(parseFloat(e.target.value))} style={{flex: 1}} />
      <span style={{flex: '0 0 8rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
        <b>{fmt ? fmt(value) : value}</b> {unit}
      </span>
    </div>
  );
}

const W = 540, H = 250, PAD_L = 46, PAD_R = 14, PAD_T = 14, PAD_B = 32;
// PSD plot dynamic range (dBc/Hz-style decades on the log10 PSD axis)
const PSD_DECADES = 14;

export default function PllLoopBwExplorer() {
  const [fn_kHz, setFn] = useState(500);     // loop BW f_n [kHz]
  const [logSref, setLogSref] = useState(-12); // S_ref flat floor = 10^x [rad^2/Hz]
  const [logSvco, setLogSvco] = useState(-10); // S_vco @1MHz = 10^x [rad^2/Hz]
  const [f0_GHz, setF0] = useState(5.0);      // carrier (jitter scaling) [GHz]

  const fn = fn_kHz * 1e3;
  const Sref = Math.pow(10, logSref);          // flat reference floor
  const SvcoAnchor = Math.pow(10, logSvco);    // VCO 1/f^2 level at 1 MHz
  const f0 = f0_GHz * 1e9;

  // shared offset grid + source PSDs (independent of f_n)
  const {fGrid, SrefArr, SvcoArr} = useMemo(() => {
    const g = logGrid(F_LO, F_HI, NPTS);
    const sref = g.map(() => Sref);                         // white floor
    const svco = g.map((f) => SvcoAnchor * (F_ANCHOR / f) ** 2); // 1/f^2 skirt
    return {fGrid: g, SrefArr: sref, SvcoArr: svco};
  }, [Sref, SvcoAnchor]);

  // shaped output for the CURRENT f_n (for the spectrum plot)
  const {SrefSh, SvcoSh, Sout, crossIdx, sigT} = useMemo(() => {
    const sr = new Array(NPTS), sv = new Array(NPTS), so = new Array(NPTS);
    let ci = -1;
    for (let i = 0; i < NPTS; i++) {
      const lp = Hlp2(fGrid[i], fn, ZETA);
      const hp = Hhp2(fGrid[i], fn, ZETA);
      sr[i] = SrefArr[i] * lp;
      sv[i] = SvcoArr[i] * hp;
      so[i] = sr[i] + sv[i];
      // ref/VCO crossover: first index where shaped VCO overtakes shaped ref
      if (ci === -1 && i > 0 && (sr[i - 1] - sv[i - 1]) * (sr[i] - sv[i]) <= 0) ci = i;
    }
    const var_phi = integrate(fGrid, so);          // rad^2
    const st = Math.sqrt(Math.max(var_phi, 0)) / (TWO_PI * f0); // s
    return {SrefSh: sr, SvcoSh: sv, Sout: so, crossIdx: ci, sigT: st};
  }, [fGrid, SrefArr, SvcoArr, fn, f0]);

  // jitter vs f_n sweep + optimum (independent of carrier f0 for the MINIMIZER,
  // since f0 only scales every point by the same 1/(2 pi f0); we keep f0 in for
  // the absolute fs readout)
  const {fnSweep, jitterSweep, fnOpt, jitterOpt, jMin, jMax} = useMemo(() => {
    const fns = logGrid(1e3, 30e6, NSWEEP);  // 1 kHz .. 30 MHz loop BW
    const jit = new Array(NSWEEP);
    let bestVar = Infinity, bestFn = fns[0], lo = Infinity, hi = 0;
    for (let k = 0; k < NSWEEP; k++) {
      const fnk = fns[k];
      const so = new Array(NPTS);
      for (let i = 0; i < NPTS; i++) {
        so[i] = SrefArr[i] * Hlp2(fGrid[i], fnk, ZETA)
              + SvcoArr[i] * Hhp2(fGrid[i], fnk, ZETA);
      }
      const v = integrate(fGrid, so);                  // rad^2
      const st = Math.sqrt(Math.max(v, 0)) / (TWO_PI * f0); // s
      jit[k] = st;
      if (v < bestVar) { bestVar = v; bestFn = fnk; }
      if (st < lo) lo = st;
      if (st > hi) hi = st;
    }
    return {
      fnSweep: fns, jitterSweep: jit, fnOpt: bestFn,
      jitterOpt: Math.sqrt(Math.max(bestVar, 0)) / (TWO_PI * f0),
      jMin: lo, jMax: hi,
    };
  }, [fGrid, SrefArr, SvcoArr, f0]);

  // ---------- styles ----------
  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)', borderRadius: '8px',
    padding: '1rem 1.1rem', margin: '1rem 0', background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 8rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.55rem 0.75rem', textAlign: 'center',
  };
  const axis = 'var(--ifm-color-emphasis-400)';
  const grid = 'var(--ifm-color-emphasis-200)';
  const cRef = 'var(--ifm-color-primary)';
  const cVco = 'var(--ifm-color-warning, #d6a000)';
  const cOut = 'var(--ifm-color-danger, #e5534b)';

  // ---------- spectrum plot mapping (log f x-axis, log10 PSD y-axis) ----------
  const logFlo = Math.log10(F_LO), logFhi = Math.log10(F_HI);
  const Xf = (f) => PAD_L + (Math.log10(f) - logFlo) / (logFhi - logFlo) * (W - PAD_L - PAD_R);
  // anchor PSD top at the largest source level present, span PSD_DECADES down
  const psdTop = Math.ceil(Math.log10(Math.max(
    SrefArr.reduce((a, b) => Math.max(a, b), 0),
    SvcoArr.reduce((a, b) => Math.max(a, b), 0),
  )));
  const psdBot = psdTop - PSD_DECADES;
  const Yp = (S) => {
    const l = Math.min(Math.max(Math.log10(Math.max(S, 1e-300)), psdBot), psdTop);
    return PAD_T + (1 - (l - psdBot) / (psdTop - psdBot)) * (H - PAD_T - PAD_B);
  };
  const poly = (arr) => arr.map((S, i) => `${Xf(fGrid[i]).toFixed(1)},${Yp(S).toFixed(1)}`).join(' ');
  const fnX = Xf(Math.min(Math.max(fn, F_LO), F_HI));

  // x decade gridlines for spectrum
  const decades = [];
  for (let d = Math.ceil(logFlo); d <= Math.floor(logFhi); d++) decades.push(d);
  const decLabel = (d) => {
    const v = Math.pow(10, d);
    if (v >= 1e9) return `${v / 1e9}G`;
    if (v >= 1e6) return `${v / 1e6}M`;
    if (v >= 1e3) return `${v / 1e3}k`;
    return `${v}`;
  };

  // ---------- jitter-vs-f_n plot (log f_n x, linear jitter y) ----------
  const JW = 540, JH = 150, JPAD_L = 46, JPAD_R = 14, JPAD_T = 12, JPAD_B = 30;
  const logFnLo = Math.log10(fnSweep[0]), logFnHi = Math.log10(fnSweep[fnSweep.length - 1]);
  const Xfn = (f) => JPAD_L + (Math.log10(f) - logFnLo) / (logFnHi - logFnLo) * (JW - JPAD_L - JPAD_R);
  const jTop = jMax * 1.05, jBot = Math.max(jMin * 0.6, 0);
  const Yj = (j) => JPAD_T + (1 - (j - jBot) / (jTop - jBot + 1e-300)) * (JH - JPAD_T - JPAD_B);
  const jpoly = jitterSweep.map((j, i) => `${Xfn(fnSweep[i]).toFixed(1)},${Yj(j).toFixed(1)}`).join(' ');
  const optX = Xfn(fnOpt);
  const curX = Xfn(Math.min(Math.max(fn, fnSweep[0]), fnSweep[fnSweep.length - 1]));

  const fnDecades = [];
  for (let d = Math.ceil(logFnLo); d <= Math.floor(logFnHi); d++) fnDecades.push(d);

  const fmtHz = (v) => {
    if (v >= 1e6) return `${(v / 1e6).toFixed(v / 1e6 >= 10 ? 0 : 2)} MHz`;
    if (v >= 1e3) return `${(v / 1e3).toFixed(v / 1e3 >= 10 ? 0 : 1)} kHz`;
    return `${v.toFixed(0)} Hz`;
  };
  const crossF = crossIdx > 0 ? fGrid[crossIdx] : null;

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        PLL loop-bandwidth 探索器（最佳 loop BW）
      </div>

      {/* ---- output spectrum (log-log) ---- */}
      <svg viewBox={`0 0 ${W} ${H}`} style={{width: '100%', height: 'auto', background: 'var(--ifm-background-color)', borderRadius: '6px'}}>
        {decades.map((d) => (
          <g key={`xd${d}`}>
            <line x1={Xf(Math.pow(10, d))} y1={PAD_T} x2={Xf(Math.pow(10, d))} y2={H - PAD_B} stroke={grid} strokeWidth="1" />
            <text x={Xf(Math.pow(10, d))} y={H - PAD_B + 12} fontSize="9" fill={axis} textAnchor="middle">{decLabel(d)}</text>
          </g>
        ))}
        {/* axes */}
        <line x1={PAD_L} y1={H - PAD_B} x2={W - PAD_R} y2={H - PAD_B} stroke={axis} strokeWidth="1" />
        <line x1={PAD_L} y1={PAD_T} x2={PAD_L} y2={H - PAD_B} stroke={axis} strokeWidth="1" />
        {/* loop BW marker */}
        <line x1={fnX} y1={PAD_T} x2={fnX} y2={H - PAD_B} stroke={cOut} strokeWidth="1" strokeDasharray="2 3" opacity="0.7" />
        <text x={fnX + 3} y={PAD_T + 10} fontSize="9" fill={cOut}>f_n</text>
        {/* shaped sources (thin) + output (thick) */}
        <polyline points={poly(SrefSh)} fill="none" stroke={cRef} strokeWidth="1.2" opacity="0.8" />
        <polyline points={poly(SvcoSh)} fill="none" stroke={cVco} strokeWidth="1.2" opacity="0.8" />
        <polyline points={poly(Sout)} fill="none" stroke={cOut} strokeWidth="2.2" />
        {/* crossover dot */}
        {crossIdx > 0 && (
          <circle cx={Xf(fGrid[crossIdx])} cy={Yp(Sout[crossIdx])} r="3.5" fill={cOut} stroke="var(--ifm-background-color)" strokeWidth="1" />
        )}
        {/* labels */}
        <text x={PAD_L + 4} y={PAD_T + 10} fontSize="10" fill={axis}>S_out (rad²/Hz, log)</text>
        <text x={W - PAD_R} y={H - 4} fontSize="10" fill={axis} textAnchor="end">offset Δf [Hz, log]</text>
        <g fontSize="9.5">
          <text x={W - PAD_R - 4} y={PAD_T + 22} fill={cRef} textAnchor="end">ref·|H_lp|²</text>
          <text x={W - PAD_R - 4} y={PAD_T + 34} fill={cVco} textAnchor="end">vco·|H_hp|²</text>
          <text x={W - PAD_R - 4} y={PAD_T + 46} fill={cOut} textAnchor="end">S_out</text>
        </g>
      </svg>

      {/* ---- integrated jitter vs f_n ---- */}
      <svg viewBox={`0 0 ${JW} ${JH}`} style={{width: '100%', height: 'auto', background: 'var(--ifm-background-color)', borderRadius: '6px', marginTop: '0.5rem'}}>
        {fnDecades.map((d) => (
          <g key={`jxd${d}`}>
            <line x1={Xfn(Math.pow(10, d))} y1={JPAD_T} x2={Xfn(Math.pow(10, d))} y2={JH - JPAD_B} stroke={grid} strokeWidth="1" />
            <text x={Xfn(Math.pow(10, d))} y={JH - JPAD_B + 12} fontSize="9" fill={axis} textAnchor="middle">{decLabel(d)}</text>
          </g>
        ))}
        <line x1={JPAD_L} y1={JH - JPAD_B} x2={JW - JPAD_R} y2={JH - JPAD_B} stroke={axis} strokeWidth="1" />
        <line x1={JPAD_L} y1={JPAD_T} x2={JPAD_L} y2={JH - JPAD_B} stroke={axis} strokeWidth="1" />
        {/* optimum marker */}
        <line x1={optX} y1={JPAD_T} x2={optX} y2={JH - JPAD_B} stroke={cRef} strokeWidth="1.2" strokeDasharray="4 3" />
        <circle cx={optX} cy={Yj(jitterOpt)} r="4" fill={cRef} stroke="var(--ifm-background-color)" strokeWidth="1" />
        <text x={optX + 4} y={JPAD_T + 10} fontSize="9.5" fill={cRef}>最佳 f_n</text>
        {/* current f_n marker */}
        <line x1={curX} y1={JPAD_T} x2={curX} y2={JH - JPAD_B} stroke={cOut} strokeWidth="1" strokeDasharray="2 3" opacity="0.7" />
        <circle cx={curX} cy={Yj(sigT)} r="3" fill={cOut} />
        {/* curve */}
        <polyline points={jpoly} fill="none" stroke={cVco} strokeWidth="2" />
        <text x={JPAD_L + 4} y={JPAD_T + 10} fontSize="10" fill={axis}>σ_t (rms jitter) vs loop BW f_n</text>
        <text x={JW - JPAD_R} y={JH - 4} fontSize="10" fill={axis} textAnchor="end">loop BW f_n [Hz, log]</text>
      </svg>

      {/* ---- sliders ---- */}
      <div style={{marginTop: '0.6rem'}}>
        <Slider label="loop BW f_n" value={fn_kHz} unit="kHz" min={1} max={10000} step={1}
                onChange={setFn} fmt={(v) => (v >= 1000 ? `${(v / 1000).toFixed(2)} M` : v.toFixed(0))} />
        <Slider label="ref noise S_ref = 10^x" value={logSref} unit="rad²/Hz" min={-17} max={-11} step={0.1}
                onChange={setLogSref} fmt={(v) => v.toFixed(1)} />
        <Slider label="VCO noise S_vco@1MHz = 10^x" value={logSvco} unit="rad²/Hz" min={-13} max={-7} step={0.1}
                onChange={setLogSvco} fmt={(v) => v.toFixed(1)} />
        <Slider label="carrier f₀" value={f0_GHz} unit="GHz" min={0.5} max={30} step={0.5}
                onChange={setF0} fmt={(v) => v.toFixed(1)} />
      </div>

      {/* ---- readouts ---- */}
      <div style={{display: 'flex', gap: '0.8rem', marginTop: '0.7rem', flexWrap: 'wrap'}}>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>σ_t @ 目前 f_n</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>{(sigT * 1e15).toFixed(1)}</div>
          <div style={{fontSize: '0.78rem'}}>fs（f_n = {fmtHz(fn)}）</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>最佳 loop BW f_n*</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700, color: cRef}}>{fmtHz(fnOpt)}</div>
          <div style={{fontSize: '0.78rem'}}>σ_t,min = {(jitterOpt * 1e15).toFixed(1)} fs</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>ref/VCO 交越</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>{crossF ? fmtHz(crossF) : '—'}</div>
          <div style={{fontSize: '0.78rem'}}>shaped ref = shaped VCO</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.78rem', opacity: 0.7}}>離最佳值</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>
            {jitterOpt > 0 ? `${((sigT / jitterOpt - 1) * 100).toFixed(0)}%` : '—'}
          </div>
          <div style={{fontSize: '0.78rem'}}>σ_t 高於最小</div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.72, marginTop: '0.7rem'}}>
        模型：type-II 2nd-order PLL（ζ = {ZETA}），參考雜訊取平坦 floor、VCO 取 1/f²
        skirt（@1 MHz 錨定）。低頻被 loop 追蹤（|H_lp|²），高頻 VCO 被高通抑制（|H_hp|²）：
        S_out = S_ref·|H_lp|² + S_vco·|H_hp|²。積分頻段 1 kHz–1 GHz、σ_t = √(∫S_out df)/(2π f₀)
        （規範公式 19）。加大 f_n 會多收 in-band 參考雜訊、少收 out-of-band VCO 雜訊，故
        存在最小化積分 jitter 的最佳 f_n。對應 pll_utils / lab_13 / lab_20，pedagogical
        toy model（非特定 silicon loop）。
      </div>
    </div>
  );
}
