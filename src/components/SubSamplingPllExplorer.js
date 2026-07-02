import React, {useState} from 'react';

// Classic charge-pump PLL vs sub-sampling PLL in-band floor explorer.
// Same illustrative (示意) math as docs/06_design_insights/sampling_pll.md:
//   classic : ref -> L_ref + 20logN ; CP -> i_n^2/(I_cp/2piN)^2 ; divider floor + 20logN
//   SSPLL   : ref -> L_ref + 20logN (unavoidable) ; gm -> i_n^2/(gm*A)^2 ;
//             sampler kT/C folded into f_ref/2 -> 2kT/(Cs*f_ref)/A^2
// All L in SSB dBc/Hz with L = (1/2) S_phi. Pure client component, SSR-safe.

const TWO_PI = 2 * Math.PI;
const KT = 1.380649e-23 * 300; // J (T = 300 K)
const F_REF = 100e6;           // Hz, fixed reference
const L_DIV_FLOOR = -160;      // dBc/Hz divider output floor (fixed, illustrative)

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

function padd(...Ls) {
  return 10 * Math.log10(Ls.reduce((s, L) => s + Math.pow(10, L / 10), 0));
}

// dB axis for the bar chart
const L_MIN = -200, L_MAX = -100, X0 = 150, X1 = 600;
function xOf(L) {
  const t = (Math.min(Math.max(L, L_MIN), L_MAX) - L_MIN) / (L_MAX - L_MIN);
  return X0 + t * (X1 - X0);
}

function BarGroup({title, rows, yTop}) {
  const h = 15, gap = 8;
  return (
    <g>
      <text x={8} y={yTop} fontSize="12" fontWeight="700" fill="var(--ifm-font-color-base)">{title}</text>
      {rows.map(([label, L, color, bold], i) => {
        const y = yTop + 8 + i * (h + gap);
        return (
          <g key={label}>
            <text x={142} y={y + h - 4} fontSize="11" textAnchor="end"
                  fontWeight={bold ? 700 : 400} fill="var(--ifm-font-color-base)">{label}</text>
            <rect x={X0} y={y} width={Math.max(xOf(L) - X0, 1.5)} height={h}
                  fill={color} opacity={bold ? 0.95 : 0.75} rx="2" />
            <text x={xOf(L) + 5} y={y + h - 4} fontSize="11"
                  fontWeight={bold ? 700 : 400} fill="var(--ifm-font-color-base)">
              {L.toFixed(1)}
            </text>
          </g>
        );
      })}
    </g>
  );
}

export default function SubSamplingPllExplorer() {
  const [N, setN] = useState(50);         // divide ratio (f0 = N * 100 MHz)
  const [Lref, setLref] = useState(-160); // reference floor dBc/Hz @ 100 MHz
  const [icpMA, setIcp] = useState(1.0);  // CP current, mA
  const [inPA, setIn] = useState(4.0);    // noise current, pA/rtHz (CP and gm)
  const [gmMS, setGm] = useState(5.0);    // gm stage, mS
  const [ampV, setAmp] = useState(0.5);   // sampled VCO amplitude, V
  const [csFF, setCs] = useState(100);    // sampling cap, fF

  // --- physics (same as page's worked block) ---
  const Icp = icpMA * 1e-3;
  const Si = Math.pow(inPA * 1e-12, 2);            // A^2/Hz
  const Kcp = Icp / TWO_PI;                        // A/rad @ PFD input
  const Kss = gmMS * 1e-3 * ampV;                  // A/rad @ output phase
  const LrefOut = Lref + 20 * Math.log10(N);       // ref x N^2
  const LcpOut = 10 * Math.log10(0.5 * (Si / (Kcp * Kcp)) * N * N);
  const LdivOut = L_DIV_FLOOR + 20 * Math.log10(N);
  const Lclassic = padd(LrefOut, LcpOut, LdivOut);
  const LgmSS = 10 * Math.log10(0.5 * Si / (Kss * Kss));
  const Lsmp = 10 * Math.log10(0.5 * (2 * KT / (csFF * 1e-15 * F_REF)) / (ampV * ampV));
  const Lss = padd(LrefOut, LgmSS, Lsmp);
  const suppDb = LcpOut - LgmSS;                   // CP -> gm suppression
  const gainDb = Lclassic - Lss;                   // total in-band improvement

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

  const cRef = '#5b84c4', cFront = '#dd8452', cAdd = '#55a868';
  const g1 = [
    ['ref ×N²', LrefOut, cRef, false],
    ['CP (×N²)', LcpOut, cFront, false],
    ['divider ×N²', LdivOut, cAdd, false],
    ['總和', Lclassic, 'var(--ifm-color-primary)', true],
  ];
  const g2 = [
    ['ref ×N²', LrefOut, cRef, false],
    ['gm (÷K_PD²)', LgmSS, cFront, false],
    ['sampler kT/C', Lsmp, cAdd, false],
    ['總和', Lss, 'var(--ifm-color-primary)', true],
  ];
  const ticks = [-200, -180, -160, -140, -120, -100];
  const axisY = 232;

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        經典 CP-PLL vs sub-sampling PLL：in-band 地板互動比較（示意模型）
      </div>
      <Row label="N（f₀ = N×100 MHz）" value={N} unit={`→ ${(N * 0.1).toFixed(1)} GHz`}
           min={10} max={200} step={5} onChange={setN} fmt={(v) => v.toFixed(0)} />
      <Row label="L_ref 參考床" value={Lref} unit="dBc/Hz" min={-170} max={-140} step={1}
           onChange={setLref} fmt={(v) => v.toFixed(0)} />
      <Row label="I_cp（經典 CP）" value={icpMA} unit="mA" min={0.1} max={10} step={0.1}
           onChange={setIcp} fmt={(v) => v.toFixed(1)} />
      <Row label="i_n（CP 與 gm 同值）" value={inPA} unit="pA/√Hz" min={1} max={20} step={0.5}
           onChange={setIn} fmt={(v) => v.toFixed(1)} />
      <Row label="g_m（SSPD 後級）" value={gmMS} unit="mS" min={1} max={20} step={0.5}
           onChange={setGm} fmt={(v) => v.toFixed(1)} />
      <Row label="A（被取樣振幅）" value={ampV} unit="V" min={0.1} max={1} step={0.05}
           onChange={setAmp} fmt={(v) => v.toFixed(2)} />
      <Row label="C_s（取樣電容）" value={csFF} unit="fF" min={20} max={500} step={10}
           onChange={setCs} fmt={(v) => v.toFixed(0)} />

      <div style={out}>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>經典 in-band 地板</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{Lclassic.toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>dBc/Hz</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>sub-sampling 地板</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{Lss.toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>dBc/Hz</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>CP→gm 抑制（K_PD²）</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{suppDb.toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>dB</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>in-band 改善</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{gainDb.toFixed(1)}</div>
          <div style={{fontSize: '0.8rem'}}>dB</div>
        </div>
      </div>

      <svg viewBox="0 0 640 252" style={{width: '100%', height: 'auto', marginTop: '0.8rem'}}
           role="img" aria-label="in-band noise contributions bar chart">
        {ticks.map((t) => (
          <g key={t}>
            <line x1={xOf(t)} y1={16} x2={xOf(t)} y2={axisY - 14}
                  stroke="var(--ifm-color-emphasis-300)" strokeWidth="1" strokeDasharray="3,3" />
            <text x={xOf(t)} y={axisY} fontSize="10" textAnchor="middle"
                  fill="var(--ifm-font-color-base)" opacity="0.7">{t}</text>
          </g>
        ))}
        <BarGroup title="經典 CP-PLL" rows={g1} yTop={22} />
        <BarGroup title="sub-sampling PLL" rows={g2} yTop={126} />
        <text x={(X0 + X1) / 2} y={axisY + 14} fontSize="11" textAnchor="middle"
              fill="var(--ifm-font-color-base)" opacity="0.75">
          in-band 相位雜訊貢獻 [dBc/Hz]（換到 f₀ 輸出，deep in-band，SSB）
        </text>
      </svg>

      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.5rem'}}>
        示意模型（非特定製程）：f_ref 固定 100 MHz；divider 自身床固定 −160 dBc/Hz（再 ×N²）；
        K_cp = I_cp/2π（對 PFD 輸入相位）、K_SS = g_m·A（對輸出相位，取樣在過零點）；
        sampler 項 = 2kT/(C_s·f_ref)/A²（kT/C 摺進 ±f_ref/2）。ref ×N² 兩邊都在——
        sub-sampling 只移除 divider/CP 那兩項。對應 sampling_pll 頁的 worked example。
      </div>
    </div>
  );
}
