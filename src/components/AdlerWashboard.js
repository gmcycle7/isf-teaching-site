import React, {useEffect, useRef, useState} from 'react';
import useIsEn from './useIsEn';

// AdlerWashboard — tilted-washboard potential animation for the Adler equation.
//
// Physics (mechanical analogy of the classical Adler equation derived on this
// page, "第 0 步"/"Step 0" above): overdamped motion of a ball in the tilted
// periodic potential
//   U(θ) = −Δω·θ − ω_L·cos(θ)                     (tilted washboard)
// gives, since overdamped dynamics obey dθ/dt = −dU/dθ,
//   dθ/dt = Δω − ω_L·sin(θ)                        (classical Adler, this page's boxed result)
// Let r = Δω/ω_L (normalized detuning):
//   r < 1  → U(θ) has local minima (wells) → ball settles → LOCKED
//   r > 1  → U(θ) is monotonically tilted, no wells → ball rolls forever,
//            with period = one beat T_b = 2π/ω_b, ω_b = √(Δω²−ω_L²) (Part B of this page)
// Noise is added as a random walk kick each frame on dθ/dt; when noise is large
// enough near r≈1 it can kick the ball out of a well early ("cycle slip"),
// counted live in the readout.
//
// Pure client component, SSR-safe (no window/document access at module scope
// or in the render path — only inside the rAF effect, which never runs during
// SSR because effects don't execute on the server). No external deps; the
// washboard + ball are drawn with inline SVG. Cleans up its rAF on unmount.

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

// U(θ) = −Δω·θ − ω_L·cos(θ), normalized so ω_L sets the corrugation depth.
function potential(theta, dw, wL) {
  return -dw * theta - wL * Math.cos(theta);
}

export default function AdlerWashboard() {
  const isEn = useIsEn();
  const [running, setRunning] = useState(true);
  const [rRatio, setRRatio] = useState(0.6);     // Δω/ω_L ∈ [0, 1.5], ω_L fixed = 1
  const [noiseAmp, setNoiseAmp] = useState(0.0); // noise strength (dθ/dt random-walk kick scale)
  const [, setTick] = useState(0);

  const rRef = useRef(0.6);
  const noiseRef = useRef(0.0);
  const runningRef = useRef(true);
  // theta: ball phase; slips: cycle-slip counter; settled: whether ball has
  // come to rest in a well (locked case); lastBeatT / beatPeriod: measured
  // period between successive 2π crossings while rolling (unlocked case).
  const simRef = useRef({
    theta: -1.4, omega: 0, slips: 0, settled: false,
    lastCrossTime: null, beatPeriod: null, elapsed: 0, crossAccum: 0,
  });

  useEffect(() => { rRef.current = rRatio; }, [rRatio]);
  useEffect(() => { noiseRef.current = noiseAmp; }, [noiseAmp]);

  const WL = 1.0; // fixed lock-range scale; rRatio sweeps Δω/ω_L

  useEffect(() => {
    let raf;
    let last = null;
    const step = (now) => {
      if (last === null) last = now;
      let dtReal = (now - last) / 1000;
      last = now;
      dtReal = Math.min(dtReal, 0.05);
      if (runningRef.current && dtReal > 0) {
        const s = simRef.current;
        const dw = rRef.current * WL;
        // Sub-step the ODE for stability at larger dw/noise.
        const sub = 4;
        const dt = dtReal / sub;
        for (let i = 0; i < sub; i++) {
          // dθ/dt = Δω − ω_L sin(θ) + noise(t)   (Adler + white-ish drive)
          const kick = noiseRef.current > 0
            ? noiseRef.current * (Math.random() + Math.random() + Math.random() - 1.5) * Math.sqrt(dt) * 6
            : 0;
          const drift = dw - WL * Math.sin(s.theta);
          const prevTheta = s.theta;
          s.theta += drift * dt + kick;
          s.omega = drift + kick / dt;
          s.elapsed += dt;

          // Cycle-slip / beat detection: count each full 2π traversal.
          const prevWrapped = Math.floor(prevTheta / (2 * Math.PI));
          const nowWrapped = Math.floor(s.theta / (2 * Math.PI));
          if (nowWrapped !== prevWrapped) {
            const crossed = Math.abs(nowWrapped - prevWrapped);
            s.slips += crossed;
            if (s.lastCrossTime !== null) {
              s.beatPeriod = s.elapsed - s.lastCrossTime;
            }
            s.lastCrossTime = s.elapsed;
          }
        }
        // Settling detection for the locked case: small residual velocity.
        s.settled = rRef.current < 1 && Math.abs(s.omega) < 0.01 && noiseRef.current < 0.02;
        setTick((t) => (t + 1) % 1e9);
      }
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf); // cleanup rAF on unmount
  }, []);

  const toggleRun = () => {
    runningRef.current = !runningRef.current;
    setRunning(runningRef.current);
  };
  const reset = () => {
    simRef.current = {
      theta: -1.4, omega: 0, slips: 0, settled: false,
      lastCrossTime: null, beatPeriod: null, elapsed: 0, crossAccum: 0,
    };
    setTick((t) => t + 1);
  };

  const s = simRef.current;
  const dw = rRatio * WL;
  const locked = rRatio < 1;
  const thetaWrapped = s.theta - 2 * Math.PI * Math.floor(s.theta / (2 * Math.PI) + 0.5); // wrap to [-π, π]
  // Theoretical stable well center (only meaningful if locked): sinθ*=Δω/ω_L
  const thetaStar = locked ? Math.asin(Math.max(-1, Math.min(1, dw / WL))) : null;
  const wbTheory = locked ? null : Math.sqrt(Math.max(dw * dw - WL * WL, 0));
  const TbTheory = wbTheory && wbTheory > 1e-9 ? (2 * Math.PI) / wbTheory : null;

  // ---- draw U(θ) over a window of θ centered on the ball, plus the ball itself ----
  const svg = React.useMemo(() => {
    const W = 460, H = 260;
    const padL = 44, padR = 16, padT = 18, padB = 30;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;
    const span = 4 * Math.PI; // show ~2 periods total, ball roughly centered
    const thetaMin = s.theta - span / 2;
    const thetaMax = s.theta + span / 2;
    const N = 160;
    const us = [];
    for (let i = 0; i <= N; i++) {
      const th = thetaMin + (i / N) * (thetaMax - thetaMin);
      us.push(potential(th, dw, WL));
    }
    const uMin = Math.min(...us);
    const uMax = Math.max(...us);
    const uSpan = Math.max(uMax - uMin, 1e-6);
    const xOf = (th) => padL + ((th - thetaMin) / (thetaMax - thetaMin)) * plotW;
    const yOf = (u) => padT + plotH * (1 - (u - uMin) / uSpan);
    let d = '';
    for (let i = 0; i <= N; i++) {
      const th = thetaMin + (i / N) * (thetaMax - thetaMin);
      const u = potential(th, dw, WL);
      d += (i === 0 ? 'M' : 'L') + xOf(th).toFixed(1) + ',' + yOf(u).toFixed(1) + ' ';
    }
    const ballX = xOf(s.theta);
    const ballY = yOf(potential(s.theta, dw, WL));
    // tick marks every π
    const ticks = [];
    const kStart = Math.ceil(thetaMin / Math.PI);
    const kEnd = Math.floor(thetaMax / Math.PI);
    for (let k = kStart; k <= kEnd; k++) {
      const th = k * Math.PI;
      ticks.push({x: xOf(th), label: `${k}π`});
    }
    return {W, H, padL, padR, padT, padB, plotW, plotH, d, ballX, ballY, ticks};
  }, [s.theta, dw]);

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const btn = {
    padding: '0.35rem 1.0rem', borderRadius: '6px', cursor: 'pointer',
    border: '1px solid var(--ifm-color-emphasis-300)',
    background: 'var(--ifm-background-surface-color)',
    color: 'var(--ifm-font-color-base)', fontSize: '0.9rem',
  };
  const btnPrimary = {
    ...btn, background: 'var(--ifm-color-primary)', color: '#fff',
    border: '1px solid var(--ifm-color-primary)', fontWeight: 700,
  };
  const out = {display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem'};
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.6rem 0.8rem', textAlign: 'center',
  };
  const stateColor = locked
    ? (s.settled ? 'var(--ifm-color-success)' : 'var(--ifm-color-warning)')
    : 'var(--ifm-color-danger)';
  const statusCard = {...card, border: `2px solid ${stateColor}`};

  const stroke = 'var(--ifm-color-emphasis-700)';
  const curveCol = 'var(--ifm-color-primary)';
  const gridCol = 'var(--ifm-color-emphasis-300)';

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Adler tilted-washboard animation (mechanical analogy: a ball rolling in U(θ) = −Δω·θ − ω_L·cos θ)'
          : 'Adler 傾斜洗衣板動畫（機械類比：一顆球在 U(θ) = −Δω·θ − ω_L·cos θ 裡滾動）'}
      </div>

      <Row label={isEn ? 'Δω / ω_L (r)' : 'Δω / ω_L（r）'} value={rRatio} unit="" min={0} max={1.5} step={0.01}
           onChange={setRRatio} fmt={(v) => v.toFixed(2)} />
      <Row label={isEn ? 'noise strength' : '雜訊強度'} value={noiseAmp} unit="" min={0} max={0.6} step={0.01}
           onChange={setNoiseAmp} fmt={(v) => v.toFixed(2)} />

      <div style={out}>
        <div style={statusCard}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>{isEn ? 'state' : '狀態'}</div>
          <div style={{fontSize: '1.15rem', fontWeight: 800, color: stateColor}}>
            {locked
              ? (isEn ? (s.settled ? 'LOCKED (settled)' : 'LOCKED (settling…)') : (s.settled ? 'LOCKED（已定住）' : 'LOCKED（沉降中）'))
              : (isEn ? 'PULLING (rolling)' : 'PULLING（持續滾動）')}
          </div>
          <div style={{fontSize: '0.78rem'}}>{locked ? 'r < 1' : 'r > 1'}</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>
            {locked ? (isEn ? 'well center θ*' : '井心 θ*') : (isEn ? 'beat period T_b (theory)' : '拍週期 T_b（理論）')}
          </div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>
            {locked
              ? (thetaStar === null ? '—' : (thetaStar * 180 / Math.PI).toFixed(1))
              : (TbTheory === null ? '—' : TbTheory.toFixed(2))}
          </div>
          <div style={{fontSize: '0.8rem'}}>{locked ? 'deg' : '1/ω_L units'}</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>
            {locked ? (isEn ? 'cycle slips' : 'cycle slip 次數') : (isEn ? 'measured beat period' : '量測拍週期')}
          </div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>
            {locked ? s.slips : (s.beatPeriod === null ? '—' : s.beatPeriod.toFixed(2))}
          </div>
          <div style={{fontSize: '0.8rem'}}>{locked ? (isEn ? 'count' : '次') : '1/ω_L units'}</div>
        </div>
      </div>

      <div style={{marginTop: '0.9rem'}}>
        <svg viewBox={`0 0 ${svg.W} ${svg.H}`} width="100%"
             style={{maxWidth: `${svg.W}px`, display: 'block'}}
             role="img"
             aria-label="Tilted washboard potential U(theta) with a rolling/settling ball">
          <rect x={svg.padL} y={svg.padT} width={svg.plotW} height={svg.plotH}
                fill="none" stroke={gridCol} strokeWidth="1" />
          {svg.ticks.map((tk, i) => (
            <g key={i}>
              <line x1={tk.x} y1={svg.padT} x2={tk.x} y2={svg.padT + svg.plotH}
                    stroke={gridCol} strokeWidth="1" strokeDasharray="2 3" opacity="0.6" />
              <text x={tk.x} y={svg.H - 8} fontSize="10" fill={stroke} textAnchor="middle">{tk.label}</text>
            </g>
          ))}
          <path d={svg.d} fill="none" stroke={curveCol} strokeWidth="2.4" />
          {/* the ball */}
          <circle cx={svg.ballX} cy={svg.ballY} r="7"
                  fill={stateColor} stroke="var(--ifm-background-surface-color)" strokeWidth="1.5" />
          <text x={svg.padL + svg.plotW / 2} y={svg.padT - 5} fontSize="11" fill={stroke} textAnchor="middle">
            U(θ) = −Δω·θ − ω_L·cos θ
          </text>
        </svg>
      </div>

      <div style={{display: 'flex', gap: '0.6rem', flexWrap: 'wrap', margin: '0.6rem 0'}}>
        <button type="button" style={btnPrimary} onClick={toggleRun}>
          {running ? (isEn ? 'Pause' : '暫停') : (isEn ? 'Play' : '播放')}
        </button>
        <button type="button" style={btn} onClick={reset}>{isEn ? 'Reset' : '重設'}</button>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.78, marginTop: '0.4rem', lineHeight: 1.6}}>
        {isEn ? (
          <>
            Reading the animation: the curve is the tilted washboard potential U(θ); the ball's
            horizontal position is the Adler phase θ, and it always rolls "downhill" (dθ/dt = −dU/dθ
            = Δω − ω_L sin θ, this page's boxed classical Adler equation). At <b>r = Δω/ω_L {'<'} 1</b> the
            tilt is gentle enough that U(θ) still has local wells — the ball settles into one and
            stops: that is <b>lock</b>. At <b>r {'>'} 1</b> the tilt has washed the wells out entirely —
            the ball rolls forever, one full 2π "slip" per beat period T_b = 2π/ω_b
            (ω_b = √(Δω²−ω_L²), derived in Part B below). Turning up "noise strength" adds a
            random-walk kick to dθ/dt each frame; near r ≈ 1 an unlucky kick can shove the ball out of
            a shallowing well before it would otherwise settle — each such escape is one
            <b> cycle slip</b>, counted live above.
          </>
        ) : (
          <>
            讀圖：曲線是傾斜洗衣板位能 U(θ)；球的水平位置就是 Adler 相位 θ，球永遠往「下坡」滾
            （dθ/dt = −dU/dθ = Δω − ω_L sin θ，本頁上方推導的經典 Adler 方程）。當 <b>r = Δω/ω_L {'<'} 1</b>
            時傾斜還不夠猛，U(θ) 仍有局部井——球掉進井裡就停住，這就是<b>鎖定</b>。當 <b>r {'>'} 1</b>
            時傾斜已經把井填平，球永不停止地滾，每滾完一整圈 2π 就是一拍，拍週期
            T_b = 2π/ω_b（ω_b = √(Δω²−ω_L²)，下方 Part B 逐步推導）。把「雜訊強度」調高會在每一幀對
            dθ/dt 加一個隨機漫步的踢動；在 r ≈ 1 附近，運氣不好的一踢可能把球從變淺的井裡踢出去——
            這種提前逃逸就是一次 <b>cycle slip</b>，即時計數顯示在上方。
          </>
        )}
      </div>
      <div style={{fontSize: '0.74rem', opacity: 0.62, marginTop: '0.5rem', lineHeight: 1.5}}>
        {isEn
          ? 'Model: pedagogical mechanical analogy (overdamped particle in a periodic tilted potential), not a literal circuit. ω_L fixed at 1 (normalized units); Δω = r·ω_L. Numerical integration: explicit Euler sub-stepped 4× per frame for stability; noise is a scaled sum-of-uniforms random-walk term (not exact Gaussian white noise, but statistically close for this illustration).'
          : '模型：教學用機械類比（過阻尼粒子在週期性傾斜位能中運動），非電路的逐項對應。ω_L 固定為 1（正規化單位）；Δω = r·ω_L。數值積分：顯式 Euler，每幀切成 4 個子步以求穩定；雜訊是縮放過的均勻分布疊加隨機漫步項（非精確高斯白噪，但用於本示意在統計上已足夠接近）。'}
      </div>
    </div>
  );
}
