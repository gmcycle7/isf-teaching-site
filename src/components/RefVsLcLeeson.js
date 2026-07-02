import React, {useState} from 'react';

// Interactive comparison of the Leeson shaping term for a crystal reference
// (extreme-Q LC) vs an on-chip LC oscillator.
// Model: L(df) = 10log10( 2*F*kT/Ps * (1 + (f0/(2*Q*df))^2 ) )  [Leeson, external]
// Thermal-only, no 1/f^3 flicker, same F and Ps for both — isolates the
// (f0/2Q df)^2 term. kT at 300 K. Pure client component, SSR-safe.

const KT = 4.142e-21; // J, k*T at 300 K
const LOG_F_MIN = 0;  // 1 Hz
const LOG_F_MAX = 8;  // 100 MHz

function leesonDb(f0, Q, F_dB, Ps_mW, df) {
  const pre = 2 * Math.pow(10, F_dB / 10) * KT / (Ps_mW * 1e-3);
  const shape = 1 + Math.pow(f0 / (2 * Q * df), 2);
  return 10 * Math.log10(pre * shape);
}

function fmtHz(f) {
  if (f >= 1e6) return (f / 1e6).toFixed(f >= 1e7 ? 0 : 1) + ' MHz';
  if (f >= 1e3) return (f / 1e3).toFixed(f >= 1e4 ? 0 : 1) + ' kHz';
  return f.toFixed(0) + ' Hz';
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

export default function RefVsLcLeeson() {
  const [fx_MHz, setFx] = useState(100);   // crystal f0 [MHz]
  const [logQx, setLogQx] = useState(4.7); // crystal Q = 10^logQx  (~5e4)
  const [fl_GHz, setFl] = useState(5.0);   // LC f0 [GHz]
  const [Ql, setQl] = useState(10);        // LC Q
  const [F_dB, setF] = useState(10);       // noise factor, both
  const [Ps_mW, setPs] = useState(1.0);    // signal power, both
  const [logDf, setLogDf] = useState(3);   // marker offset = 10^logDf [Hz]
  const [refer, setRefer] = useState(true);// refer crystal to LC carrier (+20logN)

  const fx = fx_MHz * 1e6;
  const Qx = Math.pow(10, logQx);
  const fl = fl_GHz * 1e9;
  const N = fl / fx;
  const multDb = 20 * Math.log10(N);
  const dfMark = Math.pow(10, logDf);

  const Lx = (df) => leesonDb(fx, Qx, F_dB, Ps_mW, df) + (refer ? multDb : 0);
  const Ll = (df) => leesonDb(fl, Ql, F_dB, Ps_mW, df);

  // --- SVG geometry ---
  const W = 680, H = 380;
  const x0 = 55, x1 = 662, y0 = 16, y1 = 330;
  const L_TOP = -20, L_BOT = -190;
  const xOf = (lg) => x0 + ((lg - LOG_F_MIN) / (LOG_F_MAX - LOG_F_MIN)) * (x1 - x0);
  const yOf = (L) => {
    const Lc = Math.max(Math.min(L, L_TOP), L_BOT);
    return y0 + ((L_TOP - Lc) / (L_TOP - L_BOT)) * (y1 - y0);
  };
  const curve = (fn) => {
    const pts = [];
    const nPts = 97;
    for (let i = 0; i <= nPts; i++) {
      const lg = LOG_F_MIN + (i / nPts) * (LOG_F_MAX - LOG_F_MIN);
      pts.push(`${xOf(lg).toFixed(1)},${yOf(fn(Math.pow(10, lg))).toFixed(1)}`);
    }
    return pts.join(' ');
  };

  const decLabels = ['1', '10', '100', '1k', '10k', '100k', '1M', '10M', '100M'];
  const gridV = [];
  for (let d = 0; d <= 8; d++) {
    gridV.push(
      <g key={'v' + d}>
        <line x1={xOf(d)} y1={y0} x2={xOf(d)} y2={y1}
              stroke="var(--ifm-color-emphasis-300)" strokeWidth="0.5" />
        <text x={xOf(d)} y={y1 + 14} textAnchor="middle" fontSize="10"
              fill="currentColor" opacity="0.75">{decLabels[d]}</text>
      </g>
    );
  }
  const gridH = [];
  for (let L = -180; L <= -20; L += 20) {
    gridH.push(
      <g key={'h' + L}>
        <line x1={x0} y1={yOf(L)} x2={x1} y2={yOf(L)}
              stroke="var(--ifm-color-emphasis-300)" strokeWidth="0.5" />
        <text x={x0 - 6} y={yOf(L) + 3.5} textAnchor="end" fontSize="10"
              fill="currentColor" opacity="0.75">{L}</text>
      </g>
    );
  }

  // Leeson corners f0/2Q (draw if inside plot range)
  const cornerX = fx / (2 * Qx);
  const cornerL = fl / (2 * Ql);
  const cornerMark = (fc, color, label) => {
    const lg = Math.log10(fc);
    if (lg < LOG_F_MIN || lg > LOG_F_MAX) return null;
    return (
      <g>
        <line x1={xOf(lg)} y1={y0} x2={xOf(lg)} y2={y1}
              stroke={color} strokeWidth="1" strokeDasharray="3,4" opacity="0.6" />
        <text x={xOf(lg) + 3} y={y0 + 11} fontSize="9.5" fill={color}>{label}</text>
      </g>
    );
  };

  const LxMark = Lx(dfMark);
  const LlMark = Ll(dfMark);

  const cXtal = 'var(--ifm-color-primary)';
  const cLc = 'var(--ifm-color-danger, #e5484d)';

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px', padding: '1rem 1.1rem', margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.6rem 0.8rem', textAlign: 'center',
  };

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        參考源（crystal）vs on-chip LC：Leeson 整形項互動比較
      </div>
      <Row label="crystal f₀" value={fx_MHz} unit="MHz" min={10} max={200} step={5}
           onChange={setFx} fmt={(v) => v.toFixed(0)} />
      <Row label="crystal Q = 10^x" value={logQx} unit={'(Q≈' + Math.round(Qx).toLocaleString('en-US') + ')'}
           min={4} max={6} step={0.05} onChange={setLogQx} fmt={(v) => v.toFixed(2)} />
      <Row label="LC f₀" value={fl_GHz} unit="GHz" min={1} max={20} step={0.5}
           onChange={setFl} fmt={(v) => v.toFixed(1)} />
      <Row label="LC Q" value={Ql} unit="" min={5} max={30} step={1}
           onChange={setQl} fmt={(v) => v.toFixed(0)} />
      <Row label="noise factor F（兩者同）" value={F_dB} unit="dB" min={0} max={20} step={1}
           onChange={setF} fmt={(v) => v.toFixed(0)} />
      <Row label="P_s（兩者同）" value={Ps_mW} unit="mW" min={0.1} max={10} step={0.1}
           onChange={setPs} fmt={(v) => v.toFixed(1)} />
      <Row label="讀值 offset = 10^x" value={logDf} unit={'(' + fmtHz(dfMark) + ')'}
           min={0} max={8} step={0.1} onChange={setLogDf} fmt={(v) => v.toFixed(1)} />
      <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', margin: '0.4rem 0', flexWrap: 'wrap'}}>
        <label style={{fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.4rem'}}>
          <input type="checkbox" checked={refer} onChange={(e) => setRefer(e.target.checked)} />
          把 crystal 折算到 LC 載波（×N，+{multDb.toFixed(1)} dB，N={N.toFixed(1)}）
        </label>
      </div>

      <div style={{overflowX: 'auto'}}>
        <svg viewBox={`0 0 ${W} ${H}`} style={{width: '100%', minWidth: '320px', color: 'var(--ifm-font-color-base)'}}
             xmlns="http://www.w3.org/2000/svg" role="img"
             aria-label="Leeson shaping comparison: crystal vs on-chip LC">
          {gridV}
          {gridH}
          {cornerMark(cornerX, cXtal, 'f₀/2Q (xtal)')}
          {cornerMark(cornerL, cLc, 'f₀/2Q (LC)')}
          <polyline points={curve(Lx)} fill="none" stroke={cXtal} strokeWidth="2.2" />
          <polyline points={curve(Ll)} fill="none" stroke={cLc} strokeWidth="2.2" />
          <line x1={xOf(logDf)} y1={y0} x2={xOf(logDf)} y2={y1}
                stroke="currentColor" strokeWidth="1" strokeDasharray="2,3" opacity="0.5" />
          <circle cx={xOf(logDf)} cy={yOf(LxMark)} r="4" fill={cXtal} />
          <circle cx={xOf(logDf)} cy={yOf(LlMark)} r="4" fill={cLc} />
          <text x={x1 - 4} y={y1 + 14} textAnchor="end" fontSize="10"
                fill="currentColor" opacity="0.75">offset Δf (Hz)</text>
          <text x={x0 + 6} y={y0 + 12} fontSize="10" fill="currentColor" opacity="0.75">
            L(Δf) [dBc/Hz]
          </text>
          <g>
            <rect x={x1 - 168} y={y0 + 6} width="162" height="36" rx="4"
                  fill="var(--ifm-background-surface-color)"
                  stroke="var(--ifm-color-emphasis-300)" strokeWidth="0.5" />
            <line x1={x1 - 160} y1={y0 + 18} x2={x1 - 138} y2={y0 + 18} stroke={cXtal} strokeWidth="2.2" />
            <text x={x1 - 133} y={y0 + 21.5} fontSize="10" fill="currentColor">
              crystal{refer ? '（折算 ×N）' : ''}
            </text>
            <line x1={x1 - 160} y1={y0 + 32} x2={x1 - 138} y2={y0 + 32} stroke={cLc} strokeWidth="2.2" />
            <text x={x1 - 133} y={y0 + 35.5} fontSize="10" fill="currentColor">on-chip LC</text>
          </g>
        </svg>
      </div>

      <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.4rem'}}>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>crystal @ {fmtHz(dfMark)}{refer ? '（折算後）' : ''}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700, color: cXtal}}>{LxMark.toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>dBc/Hz</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>LC @ {fmtHz(dfMark)}</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700, color: cLc}}>{LlMark.toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>dBc/Hz</div>
        </div>
        <div style={{...card}}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>crystal 優勢（LC − crystal）</div>
          <div style={{fontSize: '1.25rem', fontWeight: 700}}>{(LlMark - LxMark).toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>dB</div>
        </div>
      </div>
      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem'}}>
        模型：Leeson（外部文獻 [E1]，thermal-only）L = 10·log₁₀[2F·kT/P_s·(1+(f₀/2QΔf)²)]，
        T = 300 K，兩顆振盪器共用同一組 F、P_s 以隔離 (f₀/2QΔf)² 項；未含 1/f³ flicker
        與 sustaining amp 的實際雜訊，故為理想下限（illustrative）。crystal 折算 ×N 即
        +20·log₁₀N（時脈鏈規則 1）。預設值對應本頁 worked block：Q=50,000@100 MHz vs
        Q=10@5 GHz，1 kHz 處折算後差 ≈ 71 dB。
      </div>
    </div>
  );
}
