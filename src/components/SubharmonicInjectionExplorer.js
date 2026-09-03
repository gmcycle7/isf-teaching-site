import React, {useMemo, useState} from 'react';
import useIsEn from './useIsEn';

// SubharmonicInjectionExplorer — live explorer for the ILCM (×N subharmonic
// injection locking) results derived on this page (docs/06_design_insights/
// subharmonic_injection.md, Sections 2-4). All formulas below are copied
// verbatim from that page; nothing is reinvented here.
//
//   I_k        = (2 q_inj / T_inj) |sinc(k f_ref τ_p)|            (§2 step 5)
//   Δω_L       = (q_inj/q_max) |Γ|_max / (N T0) · |sinc(f0 τ_p)|  (§2 step 3, finite-pulse §2 step 5)
//   β          = -q_inj Γ̃'(θ_ss) = (q_inj/q_max)·slope·|sinc(f0 τ_p)|  (§3, slope=1 at the
//                used lock point for BOTH presets: LC cosθ_ss=1 at center, ring flank h/w=1)
//   H_ref(z)   = β / (1-(1-β)z^-1),  H_osc(z) = (1-z^-1) / (1-(1-β)z^-1)   (§4.1, z=e^{j2πfT_inj})
//   S_out(f)   = |H_ref|² N² S_ref(f) + |H_osc|² S_osc(f),  S_osc = 2κ²/ω²  (§4.1)
//   f_c        ≈ β f_ref / 2π                                    (§4.2)
//   σ_out²     = κ² N T0 (1-β+β²/2) / (β(2-β))                    (§4.3, boxed closed form)
//   spur₁      = 20 log10(Δf0/f_ref)                              (§4.4)
//
// Canonical constants held fixed (site-wide, [diffusion_dictionary]):
//   f0 = 5 GHz, κ² = 0.125 rad²/s.
// ISF presets (§3 "ring vs LC" table):
//   LC:   Γ=-sinθ, q_max=1 pC,  |Γ|_max=1,        slope at lock =1 (cosθ_ss=1 @ center)
//   ring: [P2] App.B triangular toy, N_st=17, η=0.75, f'=ηN_st/π, q_max=10 fC (lab_32),
//         |Γ|_max=1/f', slope on flank h/w=1 (constant)
// Sliders default to the page's headline worked example: N=20, τ_p=10 ps (=0.05·T0),
// q_inj/q_max=0.05 (q_inj=50 fC @ LC), reference floor -160 dBc/Hz — this reproduces
// the page's Section 6 script output exactly (I_N=24.90 μA, Δf_L=1.981 MHz,
// β=0.0498, f_c=2.085 MHz, σ_t=2.228 fs, self platform -150.9 dBc/Hz, reference
// in-band -134.0 dBc/Hz, spur(100 kHz)=-67.96 dBc; verified in node against the
// page's own `simulations/fig_subharmonic_injection.py`/§6 numbers).
//
// Pure client component, SSR-safe: all math runs inside useMemo (render/hydration
// only), no window/document access, no external deps, inline SVG.

const F0 = 5e9;        // Hz, canonical
const T0 = 1 / F0;     // s
const KAPPA2 = 0.125;  // rad^2/s, canonical (diffusion_dictionary)
const TWO_PI = 2 * Math.PI;

const ETA = 0.75, N_ST = 17;
const F_PRIME = (ETA * N_ST) / Math.PI;

const PRESETS = {
  lc: {qmax: 1e-12, gmax: 1.0},
  ring: {qmax: 1e-14, gmax: 1 / F_PRIME},
};

function sinc(x) {
  if (x === 0) return 1;
  const px = Math.PI * x;
  return Math.sin(px) / px;
}

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
      <span style={{flex: '0 0 8.5rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
        <b>{fmt ? fmt(value) : value}</b> {unit}
      </span>
    </div>
  );
}

export default function SubharmonicInjectionExplorer() {
  const isEn = useIsEn();
  const [N, setN] = useState(20);
  const [tauFrac, setTauFrac] = useState(0.05);   // τ_p / T0
  const [ratio, setRatio] = useState(0.05);        // q_inj / q_max
  const [lref, setLref] = useState(-160);          // dBc/Hz, assumed white reference floor
  const [preset, setPreset] = useState('lc');

  const calc = useMemo(() => {
    const P = PRESETS[preset];
    const fref = F0 / N;
    const Tinj = N * T0;
    const qinj = ratio * P.qmax;
    const sTau = Math.abs(sinc(tauFrac)); // = |sinc(f0 τ_p)| since f0 τ_p = τ_p/T0 = tauFrac
    const IN = (2 * qinj / Tinj) * sTau;
    const dwL = (ratio * P.gmax / Tinj) * sTau;
    const dfL = dwL / TWO_PI;
    const beta = ratio * sTau;
    const stable = beta > 0 && beta < 2;
    const kE = beta > 0 && beta < 1 ? -1 / Math.log(1 - beta) : NaN;
    const fc = (beta * fref) / (TWO_PI * (1 - beta));
    const sw2 = KAPPA2 * Tinj;
    const varAvg = (sw2 * (1 - beta + (beta * beta) / 2)) / (beta * (2 - beta));
    const sigmaOutRad = Math.sqrt(Math.max(varAvg, 0));
    const sigmaOutFs = (sigmaOutRad / (TWO_PI * F0)) * 1e15;
    const selfPlatform = (2 * KAPPA2 * Tinj * Tinj) / (beta * beta); // rad^2/Hz
    const Lself = 10 * Math.log10(selfPlatform / 2);
    const Sref = 2 * Math.pow(10, lref / 10); // rad^2/Hz
    const sigPsi2 = (Sref * fref) / 2;
    const LrefOut = lref + 20 * Math.log10(N);
    const varRef = (beta * N * N * sigPsi2) / (2 - beta);
    const sigmaRefFs = (Math.sqrt(Math.max(varRef, 0)) / (TWO_PI * F0)) * 1e15;
    const bOpt = Math.sqrt(sw2 / (N * N * sigPsi2));
    const qinjOptFc = bOpt * P.qmax * 1e15;
    const spur100k = 20 * Math.log10(1e5 / fref);

    // --- harmonic comb: I_k vs k, k-th line uses sinc(k f_ref τ_p) = sinc(k·tauFrac/N) ---
    const kMax = Math.min(64, Math.max(12, 2 * N));
    const comb = [];
    for (let k = 1; k <= kMax; k++) {
      const s = Math.abs(sinc((k * tauFrac) / N));
      comb.push({k, I: (2 * qinj / Tinj) * s});
    }

    // --- S_out(f): log-spaced f from just below f_c to the Nyquist f_ref/2 ---
    const xMin = Math.max(fc * 0.05, 1);
    const xMax = fref * 0.5;
    const NPTS = 140;
    const spec = [];
    const logXmin = Math.log10(xMin), logXmax = Math.log10(xMax);
    for (let i = 0; i < NPTS; i++) {
      const logf = logXmin + (i / (NPTS - 1)) * (logXmax - logXmin);
      const f = Math.pow(10, logf);
      const x = TWO_PI * f * Tinj;
      const cosx = Math.cos(x), sinx = Math.sin(x);
      const denomRe = 1 - (1 - beta) * cosx;
      const denomIm = (1 - beta) * sinx;
      const denom2 = denomRe * denomRe + denomIm * denomIm;
      const Href2 = (beta * beta) / denom2;
      const Hosc2 = (2 - 2 * cosx) / denom2;
      const SoscFree = (2 * KAPPA2) / ((TWO_PI * f) * (TWO_PI * f));
      const Sself = Hosc2 * SoscFree;
      const Srefout = Href2 * N * N * Sref;
      const Stotal = Sself + Srefout;
      spec.push({
        logf, f,
        Lself: 10 * Math.log10(Sself / 2),
        Lrefout: 10 * Math.log10(Srefout / 2),
        Ltotal: 10 * Math.log10(Stotal / 2),
      });
    }

    return {
      fref, Tinj, qinj, IN, dwL, dfL, beta, stable, kE, fc, sigmaOutRad, sigmaOutFs,
      selfPlatform, Lself, Sref, LrefOut, sigmaRefFs, bOpt, qinjOptFc, spur100k,
      comb, kMax, spec, logXmin, logXmax, qmax: P.qmax,
    };
  }, [N, tauFrac, ratio, lref, preset]);

  const {
    fref, Tinj, qinj, IN, dfL, beta, kE, fc, sigmaOutFs, Lself, LrefOut, sigmaRefFs,
    bOpt, qinjOptFc, spur100k, comb, kMax, spec, logXmin, logXmax,
  } = calc;

  // ---- comb plot geometry ----
  const combSvg = useMemo(() => {
    const W = 460, H = 210, padL = 40, padR = 12, padT = 16, padB = 28;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const maxI = Math.max(...comb.map((d) => d.I), 1e-30) * 1e6; // μA
    const xOf = (k) => padL + ((k - 0.5) / kMax) * plotW;
    const barW = Math.max(1.2, (plotW / kMax) * 0.68);
    const yOf = (uA) => padT + plotH * (1 - uA / (maxI * 1.12));
    const bars = comb.map((d) => {
      const uA = d.I * 1e6;
      const y = yOf(uA);
      return {k: d.k, x: xOf(d.k) - barW / 2, y, h: padT + plotH - y, isN: d.k === N};
    });
    const nX = xOf(N);
    return {W, H, padL, padR, padT, padB, plotW, plotH, bars, nX, maxI, barW};
  }, [comb, kMax, N]);

  // ---- S_out spectrum plot geometry ----
  const specSvg = useMemo(() => {
    const W = 460, H = 240, padL = 46, padR = 12, padT = 16, padB = 30;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const allDb = [];
    spec.forEach((p) => { allDb.push(p.Lself, p.Lrefout, p.Ltotal); });
    let dMin = Math.min(...allDb), dMax = Math.max(...allDb);
    if (!isFinite(dMin) || !isFinite(dMax) || dMax - dMin < 5) { dMin = -180; dMax = -60; }
    dMin -= 6; dMax += 6;
    const xOf = (logf) => padL + ((logf - logXmin) / (logXmax - logXmin)) * plotW;
    const yOf = (db) => padT + plotH * (1 - (Math.max(Math.min(db, dMax), dMin) - dMin) / (dMax - dMin));
    const pathOf = (key) => spec.map((p, i) => (i === 0 ? 'M' : 'L') + xOf(p.logf).toFixed(1) + ',' + yOf(p[key]).toFixed(1) + ' ').join('');
    const fcX = xOf(Math.log10(Math.max(fc, Math.pow(10, logXmin))));
    return {
      W, H, padL, padR, padT, padB, plotW, plotH,
      dSelf: pathOf('Lself'), dRef: pathOf('Lrefout'), dTotal: pathOf('Ltotal'),
      fcX, dMin, dMax, xOf, yOf,
    };
  }, [spec, logXmin, logXmax, fc]);

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 8.5rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.55rem 0.7rem', textAlign: 'center',
  };
  const cardsRow = {display: 'flex', gap: '0.7rem', flexWrap: 'wrap', marginTop: '0.7rem'};
  const cardLabel = {fontSize: '0.75rem', opacity: 0.72};
  const cardVal = {fontSize: '1.1rem', fontWeight: 700};
  const panelsRow = {display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-start', marginTop: '0.8rem'};
  const panel = {flex: '1 1 21rem', minWidth: '260px'};
  const axisColor = 'var(--ifm-color-emphasis-400)';
  const btn = {
    padding: '0.3rem 0.8rem', borderRadius: '6px', cursor: 'pointer',
    border: '1px solid var(--ifm-color-emphasis-300)',
    background: 'var(--ifm-background-surface-color)',
    color: 'var(--ifm-font-color-base)', fontSize: '0.82rem',
  };
  const btnActive = {...btn, background: 'var(--ifm-color-primary)', color: '#fff', border: '1px solid var(--ifm-color-primary)', fontWeight: 700};

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Subharmonic injection (ILCM ×N) explorer — lock range, β, and discrete-time noise shaping'
          : 'Subharmonic injection（ILCM ×N）互動探索器 —— lock range、β 與離散時間雜訊整形'}
      </div>

      <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0', flexWrap: 'wrap'}}>
        <label style={{flex: '0 1 11rem', fontSize: '0.9rem'}}>
          {isEn ? 'ISF preset' : 'ISF 預設'}
        </label>
        <button type="button" style={preset === 'lc' ? btnActive : btn}
                aria-label={isEn ? 'ideal LC ISF, Γ=-sinθ' : 'ideal LC ISF，Γ=−sinθ'}
                onClick={() => setPreset('lc')}>
          LC (Γ=−sinθ)
        </button>
        <button type="button" style={preset === 'ring' ? btnActive : btn}
                aria-label={isEn ? '[P2]-style triangular ring ISF' : '[P2] 三角 ring ISF'}
                onClick={() => setPreset('ring')}>
          {isEn ? 'ring ([P2] triangular)' : 'ring（[P2] 三角）'}
        </button>
      </div>

      <Row label={isEn ? 'N (multiplication ratio)' : 'N（倍頻比）'} value={N} unit="" min={2} max={32} step={1}
           ariaLabel={isEn ? 'multiplication ratio N' : '倍頻比 N'}
           onChange={(v) => setN(Math.round(v))} fmt={(v) => v.toFixed(0)} />
      <Row label={isEn ? 'τ_p / T0 (pulse width)' : 'τ_p / T0（脈衝寬度）'} value={tauFrac} unit="" min={0.02} max={0.5} step={0.005}
           ariaLabel={isEn ? 'pulse width as a fraction of T0' : '脈衝寬度佔 T0 的比例'}
           onChange={setTauFrac} fmt={(v) => v.toFixed(3)} />
      <Row label="q_inj / q_max" value={ratio} unit="" min={0.005} max={0.2} step={0.001}
           ariaLabel="q_inj over q_max"
           onChange={setRatio} fmt={(v) => v.toFixed(3)} />
      <Row label={isEn ? 'reference floor L_ref' : '參考噪聲底 L_ref'} value={lref} unit="dBc/Hz" min={-180} max={-120} step={1}
           ariaLabel={isEn ? 'assumed white reference phase noise floor' : '假設的白色參考相位雜訊底'}
           onChange={setLref} fmt={(v) => v.toFixed(0)} />

      <div style={cardsRow}>
        <div style={card}>
          <div style={cardLabel}>f_ref = f0/N</div>
          <div style={cardVal}>{(fref / 1e6).toFixed(1)}</div>
          <div style={{fontSize: '0.75rem'}}>MHz{' '}({(Tinj * 1e9).toFixed(2)} ns)</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>q_inj</div>
          <div style={cardVal}>{(qinj * 1e15).toFixed(2)}</div>
          <div style={{fontSize: '0.75rem'}}>fC</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>I_N</div>
          <div style={cardVal}>{(IN * 1e6).toFixed(2)}</div>
          <div style={{fontSize: '0.75rem'}}>μA</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>Δf_L</div>
          <div style={cardVal}>{dfL >= 1e6 ? (dfL / 1e6).toFixed(3) + ' MHz' : (dfL / 1e3).toFixed(2) + ' kHz'}</div>
          <div style={{fontSize: '0.75rem'}}>{isEn ? 'half lock range' : '半 lock range'}</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>β</div>
          <div style={cardVal}>{beta.toFixed(4)}</div>
          <div style={{fontSize: '0.75rem'}}>≈1/β = {isFinite(kE) ? kE.toFixed(1) : '—'} {isEn ? 'pulses to 1/e' : '次注入到 1/e'}</div>
        </div>
      </div>

      <div style={panelsRow}>
        <div style={panel}>
          <div style={{fontSize: '0.82rem', opacity: 0.75, marginBottom: '0.25rem'}}>
            {isEn ? `Injection harmonic comb |I_k|, k-th line at k=N=${N} highlighted` : `注入諧波梳 |I_k|，第 k=N=${N} 根高亮`}
          </div>
          <svg viewBox={`0 0 ${combSvg.W} ${combSvg.H}`} width="100%" role="img"
               style={{maxWidth: `${combSvg.W}px`, display: 'block', background: 'var(--ifm-background-color)', borderRadius: '6px'}}
               aria-label={isEn
                 ? `Bar chart of injection current harmonic amplitudes versus harmonic index k, with the N-th harmonic (used for locking) highlighted`
                 : `注入電流諧波振幅對諧波序號 k 的長條圖，鎖定用到的第 N 根高亮`}>
            <rect x={combSvg.padL} y={combSvg.padT} width={combSvg.plotW} height={combSvg.plotH}
                  fill="none" stroke={axisColor} strokeWidth="1" />
            {combSvg.bars.map((b) => (
              <rect key={b.k} x={b.x} y={b.y} width={combSvg.barW} height={Math.max(b.h, 0.6)}
                    fill={b.isN ? 'var(--ifm-color-primary)' : 'var(--ifm-color-emphasis-500)'}
                    opacity={b.isN ? 1 : 0.68} />
            ))}
            <line x1={combSvg.nX} y1={combSvg.padT} x2={combSvg.nX} y2={combSvg.padT + combSvg.plotH}
                  stroke="var(--ifm-color-primary)" strokeWidth="1" strokeDasharray="4 3" opacity="0.55" />
            <text x={combSvg.nX + 3} y={combSvg.padT + 11} fontSize="10" fill="var(--ifm-color-primary)">k=N</text>
            <text x={combSvg.padL} y={combSvg.H - 8} fontSize="10" fill={axisColor}>k=1</text>
            <text x={combSvg.padL + combSvg.plotW} y={combSvg.H - 8} fontSize="10" fill={axisColor} textAnchor="end">k={kMax}</text>
            <text x={combSvg.padL + combSvg.plotW / 2} y={combSvg.H - 8} fontSize="10" fill={axisColor} textAnchor="middle">
              {isEn ? 'harmonic index k' : '諧波序號 k'}
            </text>
            <text x={6} y={combSvg.padT + 8} fontSize="10" fill={axisColor}>μA</text>
          </svg>
          <div style={{fontSize: '0.72rem', opacity: 0.68, marginTop: '0.3rem'}}>
            {isEn
              ? `A pure-sine injection has only k=1; for N=${N}≥2 the k=N line — the one that actually locks the loop — is exactly zero.`
              : `純正弦注入只有 k=1；N=${N}≥2 時真正用來鎖定的 k=N 那一根恰好為零。`}
          </div>
        </div>

        <div style={panel}>
          <div style={{fontSize: '0.82rem', opacity: 0.75, marginBottom: '0.25rem'}}>
            {isEn ? 'S_out(f): self-noise shaped by |H_osc|², reference ×N²|H_ref|², and total' : 'S_out(f)：自身雜訊經 |H_osc|² 整形、參考 ×N²|H_ref|²、以及總和'}
          </div>
          <svg viewBox={`0 0 ${specSvg.W} ${specSvg.H}`} width="100%" role="img"
               style={{maxWidth: `${specSvg.W}px`, display: 'block', background: 'var(--ifm-background-color)', borderRadius: '6px'}}
               aria-label={isEn
                 ? 'Output phase noise spectrum in dBc/Hz versus log frequency, showing the self-noise shaped component, the reference-shaped component, and their sum, with the noise corner marked'
                 : '輸出相位雜訊頻譜（dBc/Hz）對 log 頻率，顯示自身雜訊整形分量、參考整形分量與總和，並標出雜訊轉折點'}>
            <rect x={specSvg.padL} y={specSvg.padT} width={specSvg.plotW} height={specSvg.plotH}
                  fill="none" stroke={axisColor} strokeWidth="1" />
            <line x1={specSvg.fcX} y1={specSvg.padT} x2={specSvg.fcX} y2={specSvg.padT + specSvg.plotH}
                  stroke="var(--ifm-color-danger)" strokeWidth="1.2" strokeDasharray="5 4" opacity="0.7" />
            <text x={specSvg.fcX + 3} y={specSvg.padT + 11} fontSize="10" fill="var(--ifm-color-danger)">f_c</text>
            <path d={specSvg.dSelf} fill="none" stroke="var(--ifm-color-emphasis-700)" strokeWidth="1.6" strokeDasharray="6 3" />
            <path d={specSvg.dRef} fill="none" stroke="var(--ifm-color-danger)" strokeWidth="1.6" strokeDasharray="2 2" />
            <path d={specSvg.dTotal} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2" />
            <text x={specSvg.padL} y={specSvg.H - 8} fontSize="10" fill={axisColor}>
              {(Math.pow(10, logXmin) / 1e3).toFixed(1)} kHz
            </text>
            <text x={specSvg.padL + specSvg.plotW} y={specSvg.H - 8} fontSize="10" fill={axisColor} textAnchor="end">
              {(fref / 2 / 1e6).toFixed(1)} MHz (f_ref/2)
            </text>
            <text x={6} y={specSvg.padT + 8} fontSize="10" fill={axisColor}>{specSvg.dMax.toFixed(0)}</text>
            <text x={6} y={specSvg.padT + specSvg.plotH} fontSize="10" fill={axisColor}>{specSvg.dMin.toFixed(0)}</text>
          </svg>
          <div style={{display: 'flex', gap: '0.9rem', flexWrap: 'wrap', fontSize: '0.72rem', marginTop: '0.25rem'}}>
            <span><span style={{color: 'var(--ifm-color-emphasis-700)'}}>▬ ▬</span> {isEn ? 'self ×|H_osc|²' : '自身 ×|H_osc|²'}</span>
            <span><span style={{color: 'var(--ifm-color-danger)'}}>····</span> {isEn ? 'ref ×N²|H_ref|²' : '參考 ×N²|H_ref|²'}</span>
            <span><span style={{color: 'var(--ifm-color-primary)'}}>▬</span> {isEn ? 'total S_out' : '總和 S_out'}</span>
          </div>
        </div>
      </div>

      <div style={cardsRow}>
        <div style={card}>
          <div style={cardLabel}>f_c ≈ βf_ref/2π</div>
          <div style={cardVal}>{(fc / 1e6).toFixed(3)}</div>
          <div style={{fontSize: '0.75rem'}}>MHz</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'self platform' : '自身平台'}</div>
          <div style={cardVal}>{Lself.toFixed(1)}</div>
          <div style={{fontSize: '0.75rem'}}>dBc/Hz</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'ref in-band (×N²)' : '參考 in-band（×N²）'}</div>
          <div style={cardVal}>{LrefOut.toFixed(1)}</div>
          <div style={{fontSize: '0.75rem'}}>dBc/Hz</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>σ_out (§4.3)</div>
          <div style={cardVal}>{sigmaOutFs.toFixed(3)}</div>
          <div style={{fontSize: '0.75rem'}}>fs {isEn ? '(self only)' : '（僅自身）'}</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>σ_ref,out</div>
          <div style={cardVal}>{sigmaRefFs.toFixed(2)}</div>
          <div style={{fontSize: '0.75rem'}}>fs</div>
        </div>
      </div>

      <div style={cardsRow}>
        <div style={card}>
          <div style={cardLabel}>β_opt (§5.4)</div>
          <div style={cardVal}>{bOpt.toFixed(4)}</div>
          <div style={{fontSize: '0.75rem'}}>{isEn ? 'q_inj,opt' : '對應 q_inj,opt'} {qinjOptFc.toFixed(2)} fC</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>spur₁ @ Δf0=100 kHz</div>
          <div style={cardVal}>{spur100k.toFixed(2)}</div>
          <div style={{fontSize: '0.75rem'}}>dBc {isEn ? '(§4.4, illustrative)' : '（§4.4，示範用）'}</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'stability' : '穩定性'}</div>
          <div style={{...cardVal, color: calc.stable ? 'var(--ifm-color-success)' : 'var(--ifm-color-danger)'}}>
            0{'<'}β{'<'}2
          </div>
          <div style={{fontSize: '0.75rem'}}>{calc.stable ? 'OK' : (isEn ? 'unstable!' : '不穩定！')}</div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.78, marginTop: '0.7rem', lineHeight: 1.6}}>
        {isEn ? (
          <>
            Formulas (verbatim from this page): injection harmonic I_k = (2q_inj/T_inj)|sinc(k f_ref τ_p)| (§2 step 5);
            lock range Δω_L = (q_inj/q_max)|Γ|_max/(N T0)·|sinc(f0 τ_p)| (§2 step 3 + step 5); realignment
            β = -q_inj Γ̃'(θ_ss), evaluated at the zero-detuning lock point where the slope is 1 for both presets
            (LC: cosθ_ss=1 at the peak; ring: the triangular flank has h/w=1 — §3, "ring vs LC"), so β = (q_inj/q_max)|sinc(f0 τ_p)|
            regardless of preset; discrete-time noise shaping H_ref(z)=β/(1-(1-β)z⁻¹), H_osc(z)=(1-z⁻¹)/(1-(1-β)z⁻¹),
            S_out=N²|H_ref|²S_ref+|H_osc|²S_osc with S_osc=2κ²/ω² (§4.1); corner f_c≈βf_ref/2π (§4.2); output jitter closed
            form σ_out²=κ²NT0(1-β+β²/2)/(β(2-β)) (§4.3, boxed, MC-verified to 0.999 on the page); reference spur
            spur₁=20log₁₀(Δf0/f_ref) shown here for the page's illustrative Δf0=100 kHz (§4.4, independent of β).
            κ²=0.125 rad²/s and f0=5 GHz are the site canonical values, held fixed; only q_max and |Γ|_max change with
            the ISF preset (LC: q_max=1 pC, |Γ|_max=1; ring: [P2] App.B triangular toy, N_st=17, η=0.75, q_max=10 fC
            (lab_32), |Γ|_max=1/f'). Defaults (N=20, τ_p=10 ps, q_inj/q_max=0.05, L_ref=-160 dBc/Hz, LC preset)
            reproduce the page's headline worked example exactly. Sliders assume zero detuning (lock point at the
            ISF's peak/flank centre); the sinc pulse-average correction is exact for the LC's pure -sinθ but only a
            first-order approximation for the ring's finite-width triangular flank (§5.1's own caveat) — treat the
            ring numbers as qualitative. Phase-only, weak-injection pedagogical toy, same as the rest of this page.
          </>
        ) : (
          <>
            公式（逐字取自本頁）：注入諧波 I_k = (2q_inj/T_inj)|sinc(k f_ref τ_p)|（§2 第 5 步）；
            lock range Δω_L = (q_inj/q_max)|Γ|_max/(N T0)·|sinc(f0 τ_p)|（§2 第 3、5 步）；
            realignment β = −q_inj Γ̃'(θ_ss)，在零失諧鎖定點（斜率兩種預設都是 1：LC 波峰 cosθ_ss=1、
            ring 三角 flank h/w=1，見 §3「ring vs LC」）算出，故 β=(q_inj/q_max)|sinc(f0 τ_p)|，與 ISF 預設無關；
            離散時間雜訊整形 H_ref(z)=β/(1−(1−β)z⁻¹)、H_osc(z)=(1−z⁻¹)/(1−(1−β)z⁻¹)，
            S_out=N²|H_ref|²S_ref+|H_osc|²S_osc，S_osc=2κ²/ω²（§4.1）；轉折點 f_c≈βf_ref/2π（§4.2）；
            輸出 jitter 閉式 σ_out²=κ²NT0(1−β+β²/2)/(β(2−β))（§4.3 boxed 公式，頁面 MC 驗證到 0.999）；
            reference spur spur₁=20log₁₀(Δf0/f_ref) 此處用頁面示範的 Δf0=100 kHz（§4.4，與 β 無關）。
            κ²=0.125 rad²/s、f0=5 GHz 是全站 canonical 值，固定不變；只有 q_max 與 |Γ|_max 隨 ISF 預設改變
            （LC：q_max=1 pC、|Γ|_max=1；ring：[P2] 附錄 B 三角 toy，N_st=17、η=0.75、q_max=10 fC（lab_32）、
            |Γ|_max=1/f'）。預設值（N=20、τ_p=10 ps、q_inj/q_max=0.05、L_ref=−160 dBc/Hz、LC 預設）
            精確重現本頁開場的 worked example。滑桿假設零失諧（鎖定點在 ISF 波峰／flank 中心）；
            sinc 脈衝平均修正對 LC 的純 −sinθ 是精確的，對 ring 的有限寬三角 flank 只是一階近似
            （§5.1 自己的但書）——ring 的數字請當作定性參考。與本頁其餘部分一樣，是 phase-only、弱注入的
            pedagogical toy model。
          </>
        )}
      </div>
    </div>
  );
}
