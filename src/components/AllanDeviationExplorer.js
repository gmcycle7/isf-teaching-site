import React, {useState, useMemo} from 'react';

// Interactive Allan-deviation explorer.
//
// Lets the reader pick a dominant FM noise type (white FM / flicker FM /
// random-walk FM) and a level, then plots sigma_y(tau) vs tau on log-log
// inline SVG, annotating the canonical slope tau^(-1/2), tau^0, tau^(+1/2).
// An optional mix slider blends the chosen dominant type with the other two so
// the reader can watch the composite curve bend through the three regions.
//
// Physics (one-sided fractional-frequency PSD S_y(f) = h_alpha * f^alpha,
// standard time-and-frequency convention, IEEE Std 1139; see also the v3
// AUTHORING_SPEC section 11.2 slope table):
//   white FM       alpha= 0 : S_y = h0          -> sigma_y^2 = h0 / (2 tau)
//                                                  -> sigma_y ~ tau^(-1/2)
//   flicker FM     alpha=-1 : S_y = h_{-1} / f   -> sigma_y^2 = 2 ln2 * h_{-1}
//                                                  -> sigma_y ~ tau^0 (floor)
//   random-walk FM alpha=-2 : S_y = h_{-2} / f^2 -> sigma_y^2 = (2pi)^2/6 * h_{-2} * tau
//                                                  -> sigma_y ~ tau^(+1/2)
// These closed forms are the textbook integrals of
//   sigma_y^2(tau) = 2 \int_0^inf S_y(f) sin^4(pi f tau) / (pi f tau)^2 df
// (the same transfer kernel quoted in the spec). They are exact for these
// pure power-law processes. Pure client component, SSR-safe (no window at
// module scope; all geometry computed from constants).

const TWO_PI = 2 * Math.PI;
const LN2 = Math.LN2;

// Allan-variance coefficients: sigma_y^2(tau) = K(type) * h * tau^p.
//   p = exponent of tau in the *variance*; deviation slope = p/2.
const NOISE_TYPES = {
  whiteFM: {
    label: 'White FM（白頻雜訊）',
    short: 'White FM',
    alpha: 0,
    // sigma_y^2 = (h0/2) * tau^(-1)
    K: (h) => h / 2,
    p: -1,
    slopeLabel: 'τ⁻¹ᐟ²', // tau^(-1/2)
    slopeText: 'σ_y ∝ τ^(−1/2)',
    note: 'thermal / shot 白噪 → 1/f² 相位雜訊 → 頻率 random walk-free，sigma_y 隨 τ 下降。',
  },
  flickerFM: {
    label: 'Flicker FM（閃爍頻雜訊）',
    short: 'Flicker FM',
    alpha: -1,
    // sigma_y^2 = 2 ln2 * h_{-1} * tau^0
    K: (h) => 2 * LN2 * h,
    p: 0,
    slopeLabel: 'τ⁰', // tau^0
    slopeText: 'σ_y ∝ τ^0（floor）',
    note: '1/f device noise 上轉 → 1/f³ 相位雜訊 → ADEV 平台（flicker floor），與 τ 無關。',
  },
  rwFM: {
    label: 'Random-walk FM（隨機漫步頻雜訊）',
    short: 'RW FM',
    alpha: -2,
    // sigma_y^2 = (2pi)^2/6 * h_{-2} * tau
    K: (h) => (TWO_PI * TWO_PI / 6) * h,
    p: 1,
    slopeLabel: 'τ⁺¹ᐟ²', // tau^(+1/2)
    slopeText: 'σ_y ∝ τ^(+1/2)',
    note: '環境/溫度漂移等 → 頻率本身 random walk → ADEV 隨 τ 上升（長期不穩定）。',
  },
};

const TYPE_ORDER = ['whiteFM', 'flickerFM', 'rwFM'];

// variance contribution of one pure type at a given tau, level h.
function varOf(typeKey, h, tau) {
  const t = NOISE_TYPES[typeKey];
  return t.K(h) * Math.pow(tau, t.p);
}

export default function AllanDeviationExplorer() {
  const [domType, setDomType] = useState('whiteFM'); // dominant noise type
  const [logLevel, setLogLevel] = useState(-20);     // dominant h = 10^logLevel
  const [mix, setMix] = useState(0);                 // 0..1 amount of the other two

  // tau axis: 1 ms .. 1000 s, 7 decades.
  const tauMin = 1e-3, tauMax = 1e3;
  const nPts = 120;

  const {curve, pureCurve, slopeRef, hDom, hMix} = useMemo(() => {
    const hDom = Math.pow(10, logLevel);
    // Mixed contributions: the two non-dominant types each get a fraction of
    // the dominant level, scaled by `mix`. We anchor them so that at the geometric
    // centre of the tau axis (tau = 1 s here, since sqrt(1e-3 * 1e3) = 1) their
    // variance equals mix * (dominant variance at tau = 1 s). This keeps the
    // blend visually meaningful across types with different units.
    const tauAnchor = Math.sqrt(tauMin * tauMax); // = 1 s
    const domVarAnchor = varOf(domType, hDom, tauAnchor);
    const hMix = {};
    TYPE_ORDER.forEach((k) => {
      if (k === domType) { hMix[k] = 0; return; }
      const t = NOISE_TYPES[k];
      const Kk = t.K(1) * Math.pow(tauAnchor, t.p); // var per unit h at anchor
      hMix[k] = Kk > 0 ? (mix * domVarAnchor) / Kk : 0;
    });

    const logTauMin = Math.log10(tauMin), logTauMax = Math.log10(tauMax);
    const curve = [], pureCurve = [];
    for (let i = 0; i < nPts; i++) {
      const lt = logTauMin + (logTauMax - logTauMin) * (i / (nPts - 1));
      const tau = Math.pow(10, lt);
      // pure dominant
      const vPure = varOf(domType, hDom, tau);
      pureCurve.push({tau, sig: Math.sqrt(Math.max(vPure, 0))});
      // mixed = dominant + scaled others (variances add: independent processes)
      let vMix = vPure;
      TYPE_ORDER.forEach((k) => {
        if (k === domType) return;
        vMix += varOf(k, hMix[k], tau);
      });
      curve.push({tau, sig: Math.sqrt(Math.max(vMix, 0))});
    }
    // a reference point on the pure curve at tau = 1 s for the slope annotation
    const slopeRef = pureCurve[Math.floor(nPts / 2)];
    return {curve, pureCurve, slopeRef, hDom, hMix};
  }, [domType, logLevel, mix]);

  // --- plot geometry (log-log) ---
  const W = 560, H = 360;
  const m = {l: 64, r: 18, t: 28, b: 46};
  const pw = W - m.l - m.r, ph = H - m.t - m.b;

  // x range = tau decades; y range computed from the data (with padding).
  const xLogMin = Math.log10(tauMin), xLogMax = Math.log10(tauMax);
  const allSig = curve.concat(pureCurve).map((d) => d.sig).filter((s) => s > 0 && isFinite(s));
  const yDataMin = Math.min.apply(null, allSig);
  const yDataMax = Math.max.apply(null, allSig);
  // snap to decades for clean gridlines
  const yLogMin = Math.floor(Math.log10(yDataMin) - 0.05);
  const yLogMax = Math.ceil(Math.log10(yDataMax) + 0.05);

  const xPix = (tau) => m.l + ((Math.log10(tau) - xLogMin) / (xLogMax - xLogMin)) * pw;
  const yPix = (sig) => m.t + (1 - (Math.log10(sig) - yLogMin) / (yLogMax - yLogMin)) * ph;

  const pathFrom = (pts) =>
    pts
      .filter((d) => d.sig > 0 && isFinite(d.sig))
      .map((d, i) => `${i === 0 ? 'M' : 'L'}${xPix(d.tau).toFixed(2)},${yPix(d.sig).toFixed(2)}`)
      .join(' ');

  const xTicks = [];
  for (let e = Math.ceil(xLogMin); e <= Math.floor(xLogMax); e++) xTicks.push(e);
  const yTicks = [];
  for (let e = yLogMin; e <= yLogMax; e++) yTicks.push(e);

  const fmtPow = (e) => {
    const supers = {'-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³',
      4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹'};
    return '10' + String(e).split('').map((c) => supers[c] || c).join('');
  };

  const dom = NOISE_TYPES[domType];

  // slope-annotation segment: draw a short reference line of the exact canonical
  // slope p/2 (in log-log) through slopeRef so the reader can eyeball it.
  const slopeSeg = useMemo(() => {
    if (!slopeRef || !(slopeRef.sig > 0)) return null;
    const halfDec = 0.8; // half-length of the reference segment, in tau-decades
    const lt0 = Math.log10(slopeRef.tau);
    const slope = dom.p / 2; // d(log sigma)/d(log tau)
    const lt1 = lt0 - halfDec, lt2 = lt0 + halfDec;
    const ls0 = Math.log10(slopeRef.sig);
    const ls1 = ls0 + slope * (lt1 - lt0);
    const ls2 = ls0 + slope * (lt2 - lt0);
    return {
      x1: xPix(Math.pow(10, lt1)), y1: yPix(Math.pow(10, ls1)),
      x2: xPix(Math.pow(10, lt2)), y2: yPix(Math.pow(10, ls2)),
      lx: xPix(Math.pow(10, lt2)), ly: yPix(Math.pow(10, ls2)),
    };
  }, [slopeRef, domType, yLogMin, yLogMax]);

  // --- styles (match PhaseNoiseCalculator: CSS vars for light/dark) ---
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

  const axisColor = 'var(--ifm-color-emphasis-600)';
  const gridColor = 'var(--ifm-color-emphasis-200)';
  const textColor = 'var(--ifm-font-color-base)';
  const pureColor = 'var(--ifm-color-primary)';
  const mixColor = 'var(--ifm-color-emphasis-700)';

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        Allan deviation σ_y(τ) 互動探索器
      </div>

      <div style={{fontSize: '0.85rem', marginBottom: '0.2rem'}}>主導 FM 雜訊類型：</div>
      <div style={btnRow}>
        {TYPE_ORDER.map((k) => (
          <button key={k} style={btn(domType === k)} onClick={() => setDomType(k)}>
            {NOISE_TYPES[k].label}
          </button>
        ))}
      </div>

      <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0'}}>
        <label style={{flex: '0 0 11rem', fontSize: '0.9rem'}}>level h = 10^x</label>
        <input type="range" min={-26} max={-14} step={0.1} value={logLevel}
               onChange={(e) => setLogLevel(parseFloat(e.target.value))}
               style={{flex: '1 1 auto'}} />
        <span style={{flex: '0 0 9rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
          <b>{hDom.toExponential(1)}</b> {dom.alpha === 0 ? '(1)' : ''}
        </span>
      </div>

      <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0'}}>
        <label style={{flex: '0 0 11rem', fontSize: '0.9rem'}}>mix（混入另兩型）</label>
        <input type="range" min={0} max={1} step={0.01} value={mix}
               onChange={(e) => setMix(parseFloat(e.target.value))}
               style={{flex: '1 1 auto'}} />
        <span style={{flex: '0 0 9rem', textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
          <b>{(mix * 100).toFixed(0)}</b> %
        </span>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{maxWidth: `${W}px`, display: 'block', margin: '0.6rem auto 0'}}
           role="img" aria-label="Allan deviation versus averaging time on log-log axes">
        {/* gridlines + x ticks */}
        {xTicks.map((e) => (
          <g key={`x${e}`}>
            <line x1={xPix(Math.pow(10, e))} y1={m.t} x2={xPix(Math.pow(10, e))} y2={m.t + ph}
                  stroke={gridColor} strokeWidth="1" />
            <text x={xPix(Math.pow(10, e))} y={m.t + ph + 16} fill={textColor}
                  fontSize="11" textAnchor="middle">{fmtPow(e)}</text>
          </g>
        ))}
        {/* gridlines + y ticks */}
        {yTicks.map((e) => (
          <g key={`y${e}`}>
            <line x1={m.l} y1={yPix(Math.pow(10, e))} x2={m.l + pw} y2={yPix(Math.pow(10, e))}
                  stroke={gridColor} strokeWidth="1" />
            <text x={m.l - 8} y={yPix(Math.pow(10, e)) + 4} fill={textColor}
                  fontSize="11" textAnchor="end">{fmtPow(e)}</text>
          </g>
        ))}
        {/* axis frame */}
        <rect x={m.l} y={m.t} width={pw} height={ph} fill="none" stroke={axisColor} strokeWidth="1.2" />
        {/* axis labels */}
        <text x={m.l + pw / 2} y={H - 8} fill={textColor} fontSize="12" textAnchor="middle">
          averaging time τ (s)
        </text>
        <text x={14} y={m.t + ph / 2} fill={textColor} fontSize="12" textAnchor="middle"
              transform={`rotate(-90 14 ${m.t + ph / 2})`}>
          Allan deviation σ_y(τ)
        </text>

        {/* mixed curve (drawn first, underneath) */}
        {mix > 0 && (
          <path d={pathFrom(curve)} fill="none" stroke={mixColor} strokeWidth="1.6"
                strokeDasharray="5 4" opacity="0.85" />
        )}
        {/* pure dominant curve */}
        <path d={pathFrom(pureCurve)} fill="none" stroke={pureColor} strokeWidth="2.4" />

        {/* slope reference segment + label */}
        {slopeSeg && (
          <g>
            <line x1={slopeSeg.x1} y1={slopeSeg.y1} x2={slopeSeg.x2} y2={slopeSeg.y2}
                  stroke={textColor} strokeWidth="1.4" strokeDasharray="2 3" opacity="0.7" />
            <circle cx={xPix(slopeRef.tau)} cy={yPix(slopeRef.sig)} r="3.2" fill={pureColor} />
            <text x={slopeSeg.lx + 6} y={slopeSeg.ly + 2} fill={textColor}
                  fontSize="13" fontWeight="700">{dom.slopeLabel}</text>
          </g>
        )}

        {/* legend */}
        <g>
          <line x1={m.l + 10} y1={m.t + 12} x2={m.l + 34} y2={m.t + 12} stroke={pureColor} strokeWidth="2.4" />
          <text x={m.l + 40} y={m.t + 16} fill={textColor} fontSize="11">{dom.short}（純）</text>
          {mix > 0 && (
            <>
              <line x1={m.l + 130} y1={m.t + 12} x2={m.l + 154} y2={m.t + 12}
                    stroke={mixColor} strokeWidth="1.6" strokeDasharray="5 4" />
              <text x={m.l + 160} y={m.t + 16} fill={textColor} fontSize="11">mixed（三型相加）</text>
            </>
          )}
        </g>
      </svg>

      <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem'}}>
        <div style={{flex: '1 1 9rem', background: 'var(--ifm-background-color)',
          border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
          padding: '0.6rem 0.8rem', textAlign: 'center'}}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>canonical slope</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{dom.slopeText}</div>
        </div>
        <div style={{flex: '2 1 16rem', background: 'var(--ifm-background-color)',
          border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
          padding: '0.6rem 0.8rem'}}>
          <div style={{fontSize: '0.82rem', lineHeight: 1.45}}>{dom.note}</div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem', lineHeight: 1.5}}>
        模型：純冪律 FM 過程，S_y(f) = h·f^α（α = 0 / −1 / −2 對應 white / flicker / RW FM）。
        Allan 變異數閉式：σ_y² = h/(2τ)（white）、2 ln2·h（flicker）、(2π)²/6·h·τ（RW），
        各為 σ_y²(τ) = 2∫₀^∞ S_y(f)·sin⁴(πfτ)/(πfτ)² df 對純冪律的精確積分結果
        （IEEE Std 1139；對應 AUTHORING_SPEC 11.2 與 lab_19）。mix 滑桿把另兩型以變異數相加方式混入
        （獨立過程變異數可加），可看出複合曲線在三段斜率間彎折。獨立樣本、無 dead-time 假設。
      </div>
    </div>
  );
}
