import React, {useMemo, useState} from 'react';
import useIsEn from './useIsEn';

// CoupledQvcoExplorer — live explorer for the mutually injecting ([P3] Eq.(30)/(34))
// Adler pair derived on this page (docs/06_design_insights/quadrature_and_coupled_
// oscillators.md, Section 4, "Numerical verification" = simulations/lab_42_coupled_qvco.py).
// Same averaged equations and sign conventions as lab_42; nothing is reinvented:
//
//   coupling-path phase phi_c = 90 deg (aligned with the ISF fundamental, sin phi_c = 1)
//   psi = theta_A - theta_B          (I/Q phase difference)
//   w_L = m w0 / (2 Q)               (half lock range; [P3] Eq.(35) with I_c = m I_core,
//                                     I_core = q_max w0 / Q)
//   dpsi/dt = Dw0 - 2 w_L sin(phi_c) cos(psi)  ->  Dw0 - 2 w_L cos(psi)
//   steady state  cos(psi*) = Dw0/(2 w_L)  ->  psi* = -90 deg + delta,
//   Dphi_IQ = delta = asin( (Q/m) (Dw0/w0) )   (exact)
//                   ~ (Q/m) (Dw0/w0)           (small-mismatch / page's order-of-magnitude form)
//   lock exists iff |Dw0/w0| <= m/Q
//   lock time constant: linearize about psi*: d(psi - psi*)/dt = -2 w_L cos(delta) (psi - psi*)
//        -> tau_lock = 1/(2 w_L cos delta); the page quotes the small-delta value 1/(2 w_L).
//   unlocked (|Dw0| > 2 w_L): psi slips at the mean beat rate sqrt(Dw0^2 - (2 w_L)^2) (rad/s).
//
// Defaults (m=0.3, Q=10, Dw0/w0 = 0.1 %, f0 = 5 GHz) reproduce the page's worked example:
// w_L = 4.7124e8 rad/s (75.0 MHz), Dphi_IQ exact 1.9102 deg, linear 1.9099 deg,
// tau_lock = 1/(2 w_L) = 1.061 ns = 5.3 cycles, unlock limit m/Q = 3.0 %.
//
// Pure client component, SSR-safe: all math runs inside useMemo (render time only),
// no window/document access, no external deps, inline SVG.

const F0 = 5e9;                 // Hz, canonical carrier
const W0 = 2 * Math.PI * F0;    // rad/s
const RAD2DEG = 180 / Math.PI;

function qvcoCalc(m, Q, detune, psi0Deg) {
  const wL = (m * W0) / (2 * Q);              // rad/s
  const dw0 = detune * W0;                    // rad/s
  const arg = dw0 / (2 * wL);                 // = (Q/m) detune
  const locked = Math.abs(arg) <= 1;
  const deltaExact = locked ? Math.asin(arg) : NaN;   // rad
  const deltaLin = arg;                               // rad
  const tauNom = 1 / (2 * wL);                        // s
  const tauExact = locked ? 1 / (2 * wL * Math.cos(deltaExact)) : NaN;
  const beat = locked ? 0 : Math.sqrt(dw0 * dw0 - 4 * wL * wL); // rad/s
  // trajectory in tau = wL t:  dpsi/dtau = r - 2 cos(psi), r = Dw0/wL
  const r = dw0 / wL;
  const f = (p) => r - 2 * Math.cos(p);
  const nSteps = 700;
  const tauEnd = 3.5;                          // = 7 nominal time constants (7/(2 wL))
  const h = tauEnd / nSteps;
  let p = (psi0Deg * Math.PI) / 180;
  const traj = [{t: 0, psi: p}];
  for (let i = 0; i < nSteps; i++) {
    const k1 = f(p);
    const k2 = f(p + 0.5 * h * k1);
    const k3 = f(p + 0.5 * h * k2);
    const k4 = f(p + h * k3);
    p += (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4);
    traj.push({t: ((i + 1) * h) / wL, psi: p});
  }
  return {
    wL, dw0, arg, locked, deltaExact, deltaLin, tauNom, tauExact, beat,
    tauEnd: tauEnd / wL, traj,
    cyclesNom: tauNom * F0, cyclesExact: tauExact * F0,
    limit: m / Q,
    psiStar: locked ? -Math.PI / 2 + deltaExact : NaN,
  };
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

const wrapDeg = (d) => ((((d + 180) % 360) + 360) % 360) - 180;
const fmtDeg = (d) => (Math.abs(d) < 10 ? d.toFixed(4) : d.toFixed(2));

export default function CoupledQvcoExplorer() {
  const isEn = useIsEn();
  const [m, setM] = useState(0.3);
  const [Q, setQ] = useState(10);
  const [detPct, setDetPct] = useState(0.1);   // percent
  const [psi0, setPsi0] = useState(60);        // deg

  const detune = detPct / 100;
  const c = useMemo(() => qvcoCalc(m, Q, detune, psi0), [m, Q, detune, psi0]);

  // ---------- plot 1: psi(t) ----------
  const trajSvg = useMemo(() => {
    const W = 460, H = 240, padL = 46, padR = 12, padT = 22, padB = 34;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const tMax = c.tauEnd;
    const xOf = (t) => padL + (t / tMax) * plotW;
    const yOf = (deg) => padT + plotH * (1 - (deg + 180) / 360);
    let d = '';
    let prev = null;
    c.traj.forEach((pt, i) => {
      const w = wrapDeg(pt.psi * RAD2DEG);
      const x = xOf(pt.t).toFixed(1), y = yOf(w).toFixed(1);
      if (i === 0 || (prev !== null && Math.abs(w - prev) > 180)) d += 'M' + x + ',' + y + ' ';
      else d += 'L' + x + ',' + y + ' ';
      prev = w;
    });
    return {W, H, padL, padR, padT, padB, plotW, plotH, d, xOf, yOf, tMax};
  }, [c]);

  // ---------- plot 2: Dphi_IQ vs m ----------
  const errSvg = useMemo(() => {
    const W = 460, H = 240, padL = 46, padR = 12, padT = 22, padB = 34;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const mMin = 0.05, mMax = 1;
    const yLo = 0.01, yHi = 100;                    // deg
    const lx0 = Math.log10(mMin), lx1 = Math.log10(mMax);
    const ly0 = Math.log10(yLo), ly1 = Math.log10(yHi);
    const xOf = (mm) => padL + ((Math.log10(mm) - lx0) / (lx1 - lx0)) * plotW;
    const yOf = (deg) => padT + plotH * (1 - (Math.log10(Math.min(Math.max(deg, yLo), yHi)) - ly0) / (ly1 - ly0));
    const g = Q * detune;                           // asin argument = g/m
    let dEx = '', dLin = '';
    if (g > 0) {
      const N = 120;
      let startedEx = false, startedLin = false;
      for (let i = 0; i < N; i++) {
        const mm = Math.pow(10, lx0 + (i / (N - 1)) * (lx1 - lx0));
        const a = g / mm;
        const lin = a * RAD2DEG;
        if (lin <= yHi) {
          dLin += (startedLin ? 'L' : 'M') + xOf(mm).toFixed(1) + ',' + yOf(lin).toFixed(1) + ' ';
          startedLin = true;
        }
        if (a <= 1) {
          const ex = Math.asin(a) * RAD2DEG;
          dEx += (startedEx ? 'L' : 'M') + xOf(mm).toFixed(1) + ',' + yOf(ex).toFixed(1) + ' ';
          startedEx = true;
        }
      }
      // close the exact curve exactly at the unlock edge (asin(1) = 90 deg)
      if (g >= mMin && g <= mMax) dEx += 'L' + xOf(g).toFixed(1) + ',' + yOf(90).toFixed(1) + ' ';
    }
    const unlockX = g >= mMin && g <= mMax ? xOf(g) : null;
    const curY = c.locked && g > 0 ? yOf(c.deltaExact * RAD2DEG) : null;
    return {W, H, padL, padR, padT, padB, plotW, plotH, dEx, dLin, xOf, yOf, unlockX, curY, g};
  }, [Q, detune, c]);

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
  const cardSub = {fontSize: '0.75rem'};
  const panelsRow = {display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-start', marginTop: '0.8rem'};
  const panel = {flex: '1 1 21rem', minWidth: '260px'};
  const axisColor = 'var(--ifm-color-emphasis-500)';
  const gridColor = 'var(--ifm-color-emphasis-200)';
  const plotBg = {display: 'block', background: 'var(--ifm-background-color)', borderRadius: '6px'};
  const capStyle = {fontSize: '0.82rem', opacity: 0.75, marginBottom: '0.25rem'};

  const T = trajSvg, E = errSvg;
  const okColor = 'var(--ifm-color-success)';
  const badColor = 'var(--ifm-color-danger)';

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Coupled QVCO explorer — mutually injecting Adler pair: lock-in trajectory and I/Q phase error'
          : '耦合 QVCO 互動探索器 —— 互注入 Adler 對：鎖定軌跡與 I/Q 相位誤差'}
      </div>

      <Row label={isEn ? 'coupling factor m' : '耦合係數 m'} value={m} unit="" min={0.05} max={1} step={0.05}
           ariaLabel={isEn ? 'coupling factor m = I_c over I_core' : '耦合係數 m = I_c / I_core'}
           onChange={setM} fmt={(v) => v.toFixed(2)} />
      <Row label={isEn ? 'tank Q' : 'tank Q'} value={Q} unit="" min={5} max={30} step={1}
           ariaLabel={isEn ? 'tank quality factor Q' : 'tank 品質因數 Q'}
           onChange={(v) => setQ(Math.round(v))} fmt={(v) => v.toFixed(0)} />
      <Row label={isEn ? 'mismatch Δω0/ω0' : '失諧 Δω0/ω0'} value={detPct} unit="%" min={0} max={1} step={0.01}
           ariaLabel={isEn ? 'tank frequency mismatch in percent' : 'tank 頻率失諧（百分比）'}
           onChange={setDetPct} fmt={(v) => v.toFixed(2)} />
      <Row label={isEn ? 'initial phase ψ0' : '初始相位差 ψ0'} value={psi0} unit="°" min={-180} max={180} step={1}
           ariaLabel={isEn ? 'initial I/Q phase difference psi zero in degrees' : '初始 I/Q 相位差 ψ0（度）'}
           onChange={setPsi0} fmt={(v) => v.toFixed(0)} />

      <div style={cardsRow}>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'Δφ_IQ exact: asin[(Q/m)Δω0/ω0]' : 'Δφ_IQ 精確：asin[(Q/m)Δω0/ω0]'}</div>
          <div style={{...cardVal, color: c.locked ? undefined : badColor}}>
            {c.locked ? fmtDeg(c.deltaExact * RAD2DEG) : '—'}
          </div>
          <div style={cardSub}>{isEn ? 'deg' : '度'}</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'Δφ_IQ approx: (Q/m)Δω0/ω0' : 'Δφ_IQ 近似：(Q/m)Δω0/ω0'}</div>
          <div style={cardVal}>{fmtDeg(c.deltaLin * RAD2DEG)}</div>
          <div style={cardSub}>
            {isEn ? 'deg' : '度'}
            {c.locked && c.deltaExact > 0
              ? ` · ${(100 * (c.deltaLin - c.deltaExact) / c.deltaExact).toFixed(2)} % ${isEn ? 'vs exact' : '相對精確'}`
              : ''}
          </div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'lock time constant 1/(2ω_L)' : '鎖定時間常數 1/(2ω_L)'}</div>
          <div style={cardVal}>{(c.tauNom * 1e9).toFixed(3)}</div>
          <div style={cardSub}>
            ns · {c.cyclesNom.toFixed(1)} {isEn ? 'cycles' : '週期'}
            {c.locked ? ` · ${isEn ? 'with cosδ:' : '含 cosδ：'} ${(c.tauExact * 1e9).toFixed(3)} ns` : ''}
          </div>
        </div>
        <div style={card}>
          <div style={cardLabel}>{isEn ? 'lock exists?' : '是否有鎖定解？'}</div>
          <div style={{...cardVal, color: c.locked ? okColor : badColor}}>
            {c.locked ? (isEn ? 'Yes' : '有') : (isEn ? 'No (slips)' : '無（滑相）')}
          </div>
          <div style={cardSub}>
            {isEn ? 'limit' : '界限'} Δω0/ω0 ≤ m/Q = {(100 * c.limit).toFixed(2)} %
            {!c.locked ? ` · ${isEn ? 'beat' : '拍頻'} ${(c.beat / (2 * Math.PI) / 1e6).toFixed(1)} MHz` : ''}
          </div>
        </div>
        <div style={card}>
          <div style={cardLabel}>f_L = ω_L/2π = m f0/(2Q)</div>
          <div style={cardVal}>{(c.wL / (2 * Math.PI) / 1e6).toFixed(1)}</div>
          <div style={cardSub}>MHz (f0 = 5 GHz)</div>
        </div>
      </div>

      <div style={panelsRow}>
        <div style={panel}>
          <div style={capStyle}>
            {isEn
              ? 'ψ(t) = θ_A − θ_B (wrapped to ±180°): converges to −90° + Δφ_IQ'
              : 'ψ(t) = θ_A − θ_B（折到 ±180°）：收斂到 −90° + Δφ_IQ'}
          </div>
          <svg viewBox={`0 0 ${T.W} ${T.H}`} width="100%" role="img" style={{maxWidth: `${T.W}px`, ...plotBg}}
               aria-label={isEn
                 ? `Phase difference psi in degrees versus time in nanoseconds for the mutually injecting Adler pair. ${c.locked ? `It converges to ${(c.psiStar * RAD2DEG).toFixed(2)} degrees with a lock time constant of ${(c.tauNom * 1e9).toFixed(3)} nanoseconds.` : 'There is no lock, so psi slips continuously.'}`
                 : `互注入 Adler 對的相位差 ψ（度）對時間（奈秒）。${c.locked ? `收斂到 ${(c.psiStar * RAD2DEG).toFixed(2)} 度，鎖定時間常數 ${(c.tauNom * 1e9).toFixed(3)} 奈秒。` : '無鎖定解，ψ 持續滑相。'}`}>
            {[-180, -90, 0, 90, 180].map((v) => (
              <g key={v}>
                <line x1={T.padL} x2={T.padL + T.plotW} y1={T.yOf(v)} y2={T.yOf(v)} stroke={gridColor} strokeWidth="1" />
                <text x={T.padL - 4} y={T.yOf(v) + 3} fontSize="10" fill={axisColor} textAnchor="end">{v}</text>
              </g>
            ))}
            <rect x={T.padL} y={T.padT} width={T.plotW} height={T.plotH} fill="none" stroke={axisColor} strokeWidth="1" />
            {c.locked && (
              <g>
                <line x1={T.padL} x2={T.padL + T.plotW} y1={T.yOf(c.psiStar * RAD2DEG)} y2={T.yOf(c.psiStar * RAD2DEG)}
                      stroke="var(--ifm-color-danger)" strokeWidth="1.2" strokeDasharray="3 3" />
                <text x={T.padL + T.plotW - 3} y={T.yOf(c.psiStar * RAD2DEG) - 4} fontSize="10"
                      fill="var(--ifm-color-danger)" textAnchor="end">
                  ψ* = −90° + {(c.deltaExact * RAD2DEG).toFixed(2)}°
                </text>
                <line x1={T.xOf(c.tauNom)} x2={T.xOf(c.tauNom)} y1={T.padT} y2={T.padT + T.plotH}
                      stroke="var(--ifm-color-primary)" strokeWidth="1" strokeDasharray="4 3" opacity="0.7" />
                <text x={T.xOf(c.tauNom) + 3} y={T.padT + 11} fontSize="10" fill="var(--ifm-color-primary)">
                  1/(2ω_L)
                </text>
              </g>
            )}
            <path d={T.d} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2" />
            <text x={T.padL} y={T.H - 18} fontSize="10" fill={axisColor}>0</text>
            <text x={T.padL + T.plotW} y={T.H - 18} fontSize="10" fill={axisColor} textAnchor="end">
              {(T.tMax * 1e9).toFixed(1)} ns
            </text>
            <text x={T.padL + T.plotW / 2} y={T.H - 5} fontSize="10" fill={axisColor} textAnchor="middle">
              {isEn ? 't [ns] (window = 7 × 1/(2ω_L))' : 't [ns]（視窗 = 7 × 1/(2ω_L)）'}
            </text>
            <text x={T.padL} y={11} fontSize="10" fill={axisColor}>ψ [°]</text>
          </svg>
        </div>

        <div style={panel}>
          <div style={capStyle}>
            {isEn
              ? 'Δφ_IQ versus m at the current Q and mismatch (log–log)'
              : '目前 Q 與失諧下，Δφ_IQ 對 m（log–log）'}
          </div>
          <svg viewBox={`0 0 ${E.W} ${E.H}`} width="100%" role="img" style={{maxWidth: `${E.W}px`, ...plotBg}}
               aria-label={isEn
                 ? `I/Q phase error in degrees versus coupling factor m on log axes, exact arcsine curve and small-mismatch linear approximation. ${c.locked ? `The current point m = ${m.toFixed(2)} gives ${(c.deltaExact * RAD2DEG).toFixed(2)} degrees.` : `The current m = ${m.toFixed(2)} is below the unlock limit, so there is no lock.`}`
                 : `I/Q 相位誤差（度）對耦合係數 m 的雙對數圖，含精確 arcsin 曲線與小失諧線性近似。${c.locked ? `目前 m = ${m.toFixed(2)} 給 ${(c.deltaExact * RAD2DEG).toFixed(2)} 度。` : `目前 m = ${m.toFixed(2)} 低於失鎖界，無鎖定解。`}`}>
            {[0.01, 0.1, 1, 10, 100].map((v) => (
              <g key={v}>
                <line x1={E.padL} x2={E.padL + E.plotW} y1={E.yOf(v)} y2={E.yOf(v)} stroke={gridColor} strokeWidth="1" />
                <text x={E.padL - 4} y={E.yOf(v) + 3} fontSize="10" fill={axisColor} textAnchor="end">{v}</text>
              </g>
            ))}
            {[0.05, 0.1, 0.2, 0.5, 1].map((v) => (
              <g key={v}>
                <line x1={E.xOf(v)} x2={E.xOf(v)} y1={E.padT} y2={E.padT + E.plotH} stroke={gridColor} strokeWidth="1" />
                <text x={E.xOf(v)} y={E.padT + E.plotH + 12} fontSize="10" fill={axisColor} textAnchor="middle">{v}</text>
              </g>
            ))}
            <rect x={E.padL} y={E.padT} width={E.plotW} height={E.plotH} fill="none" stroke={axisColor} strokeWidth="1" />
            {E.unlockX !== null && (
              <g>
                <rect x={E.padL} y={E.padT} width={E.unlockX - E.padL} height={E.plotH}
                      fill="var(--ifm-color-danger)" opacity="0.08" />
                <line x1={E.unlockX} x2={E.unlockX} y1={E.padT} y2={E.padT + E.plotH}
                      stroke="var(--ifm-color-danger)" strokeWidth="1.2" strokeDasharray="5 4" opacity="0.8" />
                <text x={E.unlockX + 3} y={E.padT + 11} fontSize="10" fill="var(--ifm-color-danger)">
                  {isEn ? `unlock: m < ${E.g.toFixed(2)}` : `失鎖：m < ${E.g.toFixed(2)}`}
                </text>
              </g>
            )}
            {E.dLin && <path d={E.dLin} fill="none" stroke="var(--ifm-color-emphasis-700)" strokeWidth="1.4" strokeDasharray="5 3" />}
            {E.dEx && <path d={E.dEx} fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2" />}
            {E.curY !== null && (
              <g>
                <circle cx={E.xOf(m)} cy={E.curY} r="5.5" fill="var(--ifm-color-danger)" stroke="var(--ifm-background-color)" strokeWidth="1.5" />
                <text x={E.xOf(m) + 8} y={E.curY - 7} fontSize="10" fill="var(--ifm-color-danger)">
                  {fmtDeg(c.deltaExact * RAD2DEG)}°
                </text>
              </g>
            )}
            {!c.locked && (
              <g>
                <path d={`M${E.xOf(m) - 6},${E.padT + 2} L${E.xOf(m) + 6},${E.padT + 2} L${E.xOf(m)},${E.padT + 13} Z`}
                      fill="var(--ifm-color-danger)" />
                <text x={E.xOf(m) + 9} y={E.padT + 12} fontSize="10" fill="var(--ifm-color-danger)">
                  {isEn ? 'current m: no lock' : '目前 m：無鎖定解'}
                </text>
              </g>
            )}
            {E.g === 0 && (
              <text x={E.padL + E.plotW / 2} y={E.padT + E.plotH / 2} fontSize="11" fill={axisColor} textAnchor="middle">
                {isEn ? 'mismatch = 0: Δφ_IQ = 0 for every m (ψ* = −90° exactly)' : '失諧 = 0：任何 m 下 Δφ_IQ = 0（ψ* 恰為 −90°）'}
              </text>
            )}
            <text x={E.padL + E.plotW / 2} y={E.H - 5} fontSize="10" fill={axisColor} textAnchor="middle">
              {isEn ? 'coupling factor m = I_c / I_core' : '耦合係數 m = I_c / I_core'}
            </text>
            <text x={E.padL} y={11} fontSize="10" fill={axisColor}>Δφ_IQ [°]</text>
          </svg>
          <div style={{display: 'flex', gap: '0.9rem', flexWrap: 'wrap', fontSize: '0.72rem', marginTop: '0.25rem'}}>
            <span><span style={{color: 'var(--ifm-color-primary)'}}>▬</span> {isEn ? 'exact asin' : '精確 asin'}</span>
            <span><span style={{color: 'var(--ifm-color-emphasis-700)'}}>▬ ▬</span> {isEn ? 'linear (Q/m)Δω0/ω0' : '線性 (Q/m)Δω0/ω0'}</span>
            <span><span style={{color: 'var(--ifm-color-danger)'}}>●</span> {isEn ? 'current setting' : '目前設定'}</span>
          </div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.78, marginTop: '0.7rem', lineHeight: 1.6}}>
        {isEn ? (
          <>
            Equations (same averaged pair as lab_42, coupling aligned with the ISF fundamental, φ_c = 90°):
            dψ/dt = Δω0 − 2ω_L cos ψ, ω_L = mω0/(2Q) ([P3] Eq.(35)), steady state sin δ = Δω0/(2ω_L) = (Q/m)Δω0/ω0, δ = Δφ_IQ.
            The lock time constant is the linearization 1/(2ω_L cos δ) (the page quotes the small-δ value 1/(2ω_L)); near the unlock limit it grows without bound.
            f0 = 5 GHz fixed. Toy phase-only model; it says nothing about phase noise or the frequency pull that lowers the effective Q.
          </>
        ) : (
          <>
            方程式（與 lab_42 相同的平均後互注入對；耦合與 ISF 基波對齊，φ_c = 90°）：
            dψ/dt = Δω0 − 2ω_L cos ψ，ω_L = mω0/(2Q)（[P3] Eq.(35)），穩態 sin δ = Δω0/(2ω_L) = (Q/m)Δω0/ω0，δ = Δφ_IQ。
            鎖定時間常數取線性化的 1/(2ω_L cos δ)（頁面引用的是小 δ 的 1/(2ω_L)）；越接近失鎖界越發散。
            f0 固定 5 GHz。這是只含相位的 toy model，不涉及 phase noise，也不含「拉頻降低有效 Q」。
          </>
        )}
      </div>
    </div>
  );
}
