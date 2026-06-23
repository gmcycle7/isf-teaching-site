import React, {useState, useMemo} from 'react';

// Interactive injection-locking explorer (Adler / ISF picture).
//
// Physics (all from [P3] B. Hong & A. Hajimiri, JSSC 2019, Part I):
//   Lock (half-)range  ω_L = ½ · I_inj · |Γ̃_1|            [P3] Eq.(35)
//   Adler phase-error dynamics  dθ/dt = Δω − ω_L·sin(θ)    (Adler, 外部文獻)
//   where θ = phase difference between oscillator and injection,
//   and the steady-state pulling term is  Ω(θ) = ω_L·sin(θ).
//
//   LOCKED   when |Δω| ≤ ω_L  → a stable fixed point sin(θ*) = Δω/ω_L exists.
//   UNLOCKED when |Δω| > ω_L  → phase slips; the residual beat / pulling
//   frequency is  Ω_beat = √(Δω² − ω_L²).
//
// Pure client component, SSR-safe (no window access at module scope),
// no external deps — the cone / Ω(θ) curve is drawn with inline SVG.

const TWO_PI = 2 * Math.PI;

function Row({label, value, unit, min, max, step, onChange, fmt}) {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0'}}>
      <label style={{flex: '0 0 12rem', fontSize: '0.9rem'}}>{label}</label>
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

export default function InjectionLockingExplorer() {
  // Injection current — arbitrary units (the ISF normalization absorbs q_max).
  const [Iinj, setIinj] = useState(2.0);
  // Detuning Δω = ω0 − ω_inj, in arbitrary rad/s (same units as ω_L).
  const [dw, setDw] = useState(0.4);
  // |Γ̃_1| — normalized ISF fundamental (dimensionless).
  const [G1, setG1] = useState(0.5);

  const physics = useMemo(() => {
    // [P3] Eq.(35): ω_L = ½ · I_inj · |Γ̃_1|
    const wL = 0.5 * Iinj * G1;
    const adw = Math.abs(dw);
    const locked = adw <= wL;
    // Steady-state phase error: sin(θ*) = Δω / ω_L (only valid when locked).
    let thetaStar = null;
    if (locked && wL > 0) {
      thetaStar = Math.asin(Math.max(-1, Math.min(1, dw / wL))); // rad, in [−π/2, π/2]
    }
    // Beat / pulling frequency when unlocked: Ω_beat = √(Δω² − ω_L²).
    const beat = locked ? 0 : Math.sqrt(adw * adw - wL * wL);
    return {wL, adw, locked, thetaStar, beat};
  }, [Iinj, dw, G1]);

  const {wL, adw, locked, thetaStar, beat} = physics;

  // ---- inline SVG: Ω(θ) = ω_L·sin(θ) over θ∈[0,2π], with the Δω level line ----
  const svg = useMemo(() => {
    const W = 460, H = 240;
    const padL = 44, padR = 16, padT = 18, padB = 30;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;
    // Vertical scale: cover both the sine envelope (±ω_L) and the Δω line.
    const yMax = Math.max(wL, adw, 1e-9) * 1.15;
    const xOf = (theta) => padL + (theta / TWO_PI) * plotW;       // θ: 0..2π
    const yOf = (val) => padT + plotH * (1 - (val + yMax) / (2 * yMax)); // val: −yMax..+yMax

    // Ω(θ) = ω_L·sin(θ) sampled curve.
    const N = 120;
    let d = '';
    for (let i = 0; i <= N; i++) {
      const th = (i / N) * TWO_PI;
      const v = wL * Math.sin(th);
      d += (i === 0 ? 'M' : 'L') + xOf(th).toFixed(1) + ',' + yOf(v).toFixed(1) + ' ';
    }
    const yZero = yOf(0);
    const yDw = yOf(dw);          // the Δω level line (signed)
    const yLockTop = yOf(wL);     // +ω_L envelope
    const yLockBot = yOf(-wL);    // −ω_L envelope

    // Intersection markers: where ω_L·sin(θ) = Δω (the locked fixed points).
    const marks = [];
    if (locked && wL > 0) {
      const a = thetaStar;                 // stable: dΩ/dθ = ω_L·cos(θ) > 0
      const b = Math.PI - thetaStar;       // unstable
      const wrap = (x) => ((x % TWO_PI) + TWO_PI) % TWO_PI;
      marks.push({theta: wrap(a), stable: true});
      marks.push({theta: wrap(b), stable: false});
    }
    return {W, H, padL, padR, padT, padB, plotW, plotH, d, yZero, yDw,
            yLockTop, yLockBot, xOf, yOf, marks, yMax};
  }, [wL, adw, dw, locked, thetaStar]);

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const out = {display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem'};
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.6rem 0.8rem', textAlign: 'center',
  };

  const lockColor = locked ? 'var(--ifm-color-success)' : 'var(--ifm-color-danger)';
  const statusCard = {...card, border: `2px solid ${lockColor}`};

  // Color helpers using CSS vars (fall back gracefully in either theme).
  const stroke = 'var(--ifm-color-emphasis-700)';
  const grid = 'var(--ifm-color-emphasis-300)';
  const curveCol = 'var(--ifm-color-primary)';

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        Injection Locking 互動探索器（注入鎖定，外部訊號把振盪器頻率拉到自己身上）
      </div>

      <Row label="I_inj（注入電流，arb.）" value={Iinj} unit="a.u." min={0} max={5} step={0.05}
           onChange={setIinj} fmt={(v) => v.toFixed(2)} />
      <Row label="Δω = ω₀ − ω_inj（detuning）" value={dw} unit="rad/s" min={-2} max={2} step={0.01}
           onChange={setDw} fmt={(v) => v.toFixed(2)} />
      <Row label="|Γ̃₁|（normalized ISF 基頻）" value={G1} unit="" min={0} max={1.5} step={0.01}
           onChange={setG1} fmt={(v) => v.toFixed(2)} />

      <div style={out}>
        <div style={statusCard}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>狀態</div>
          <div style={{fontSize: '1.3rem', fontWeight: 800, color: lockColor}}>
            {locked ? 'LOCKED' : 'UNLOCKED'}
          </div>
          <div style={{fontSize: '0.78rem'}}>|Δω| {locked ? '≤' : '>'} ω_L</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>lock range ω_L — [P3] Eq.(35)</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{wL.toFixed(3)}</div>
          <div style={{fontSize: '0.8rem'}}>rad/s</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>
            {locked ? 'phase error θ*' : 'beat Ω_beat'}
          </div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>
            {locked
              ? (thetaStar === null ? '—' : (thetaStar * 180 / Math.PI).toFixed(1))
              : beat.toFixed(3)}
          </div>
          <div style={{fontSize: '0.8rem'}}>{locked ? 'deg' : 'rad/s'}</div>
        </div>
      </div>

      {/* lock cone / Ω(θ) = ω_L·sin(θ) curve with the Δω level line */}
      <div style={{marginTop: '0.9rem'}}>
        <svg viewBox={`0 0 ${svg.W} ${svg.H}`} width="100%"
             style={{maxWidth: `${svg.W}px`, display: 'block'}}
             role="img"
             aria-label="Ω(θ) = ω_L·sin(θ) 與 Δω 水平線；交點為鎖定固定點">
          {/* plot frame */}
          <rect x={svg.padL} y={svg.padT} width={svg.plotW} height={svg.plotH}
                fill="none" stroke={grid} strokeWidth="1" />
          {/* zero axis */}
          <line x1={svg.padL} y1={svg.yZero} x2={svg.padL + svg.plotW} y2={svg.yZero}
                stroke={grid} strokeWidth="1" strokeDasharray="2 3" />

          {/* ±ω_L lock envelope (the "cone" half-width) */}
          <line x1={svg.padL} y1={svg.yLockTop} x2={svg.padL + svg.plotW} y2={svg.yLockTop}
                stroke="var(--ifm-color-success)" strokeWidth="1" strokeDasharray="5 4" opacity="0.7" />
          <line x1={svg.padL} y1={svg.yLockBot} x2={svg.padL + svg.plotW} y2={svg.yLockBot}
                stroke="var(--ifm-color-success)" strokeWidth="1" strokeDasharray="5 4" opacity="0.7" />

          {/* Ω(θ) = ω_L·sin(θ) */}
          <path d={svg.d} fill="none" stroke={curveCol} strokeWidth="2.2" />

          {/* Δω level line */}
          <line x1={svg.padL} y1={svg.yDw} x2={svg.padL + svg.plotW} y2={svg.yDw}
                stroke={lockColor} strokeWidth="2" />

          {/* fixed-point markers (locked only) */}
          {svg.marks.map((m, i) => (
            <circle key={i} cx={svg.xOf(m.theta)} cy={svg.yOf(dw)} r={m.stable ? 5 : 4}
                    fill={m.stable ? 'var(--ifm-color-success)' : 'none'}
                    stroke={m.stable ? 'var(--ifm-color-success)' : stroke}
                    strokeWidth="1.6" />
          ))}

          {/* axis labels */}
          <text x={svg.padL} y={svg.H - 8} fontSize="11" fill={stroke}>0</text>
          <text x={svg.padL + svg.plotW / 2 - 6} y={svg.H - 8} fontSize="11" fill={stroke}>π</text>
          <text x={svg.padL + svg.plotW - 12} y={svg.H - 8} fontSize="11" fill={stroke}>2π</text>
          <text x={svg.padL + svg.plotW / 2 - 8} y={svg.padT - 5} fontSize="11" fill={stroke}>θ</text>
          <text x={6} y={svg.yOf(wL) + 4} fontSize="10" fill="var(--ifm-color-success)">+ω_L</text>
          <text x={6} y={svg.yOf(-wL) + 4} fontSize="10" fill="var(--ifm-color-success)">−ω_L</text>
          <text x={svg.padL + svg.plotW - 30} y={svg.yDw - 4} fontSize="10" fill={lockColor}>Δω</text>
        </svg>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.78, marginTop: '0.6rem', lineHeight: 1.5}}>
        讀圖：藍色曲線 Ω(θ)=ω_L·sin(θ) 是「振盪器能提供的最大頻率牽引」；
        水平線是要克服的失諧 Δω。<b>只要 Δω 落在 ±ω_L 包絡內</b>，
        曲線與水平線就有交點（穩定固定點 = 實心綠點，θ*∈[−90°,+90°]；
        另一交點為不穩定），系統<b>鎖定</b>，相位差停在 θ* 不再漂移。
        一旦 |Δω| {'>'} ω_L 交點消失，相位持續滑動，殘餘拍頻 Ω_beat=√(Δω²−ω_L²)。
      </div>
      <div style={{fontSize: '0.74rem', opacity: 0.62, marginTop: '0.5rem', lineHeight: 1.5}}>
        公式：lock range ω_L = ½·I_inj·|Γ̃₁|（[P3] Eq.(35)）；
        相位動態 dθ/dt = Δω − ω_L·sin(θ)（Adler 方程，外部文獻，非本站 5 篇 PDF）；
        鎖定條件 |Δω| ≤ ω_L；拍頻 Ω_beat = √(Δω² − ω_L²)。單位：ω_L、Δω、Ω_beat 同為 rad/s，
        |Γ̃₁| 無因次，I_inj 為任意單位（normalization 已吸收 q_max）。
      </div>
    </div>
  );
}
