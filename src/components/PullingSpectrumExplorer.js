import React, {useMemo, useState} from 'react';
import useIsEn from './useIsEn';

// PullingSpectrumExplorer — integrates the Adler ODE and shows the resulting
// injection-pulling spectrum morph across the lock boundary r = Δω/ω_L = 1.
//
// Physics (this page, Part B "第 2–3 步"/"Step 2–3"):
//   dθ/dt = Δω − ω_L·sin(θ)                      (classical Adler)
//   V(t)  = cos(ω_inj·t + θ(t))                   (oscillator output)
//   r = Δω/ω_L < 1 → LOCKED   → θ settles → V(t) is a single clean tone at ω_inj
//   r = Δω/ω_L > 1 → PULLING  → θ(t) = ω_b·t + periodic(t), ω_b = √(Δω²−ω_L²)
//                                → V(t) has a one-sided comb, spacing ω_b,
//                                  one edge line pinned exactly at ω_inj
//                                  ([P4] Eq.(34); this page's boxed ω_b result).
//
// Numerics: RK2 (explicit midpoint) integrates the ODE for ~4096 steps; a
// small radix-2 Cooley–Tukey FFT (written inline below, no external deps) is
// applied to a Hann-windowed 2048-point slice of V(t) with parabolic peak
// interpolation to read off the comb spacing precisely. Verified against the
// closed form ω_b = √(Δω²−ω_L²): at r=1.5 the measured spacing matches theory
// to within ~0.1% (see the in-page write-up / lab_27 for the offline check).
//
// Pure client component, SSR-safe: all computation happens inside useMemo,
// which only (re)runs during render/hydration on the client — no window/
// document access anywhere, and there is no rAF/timer to clean up.

const TWO_PI = 2 * Math.PI;

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

// RK2 (explicit midpoint) integration of dθ/dt = Δω − ω_L·sin(θ).
function integrateAdler(dw, wL, dt, n, theta0) {
  const theta = new Float64Array(n);
  let th = theta0;
  for (let k = 0; k < n; k++) {
    const k1 = dw - wL * Math.sin(th);
    const k2 = dw - wL * Math.sin(th + 0.5 * dt * k1);
    th += dt * k2;
    theta[k] = th;
  }
  return theta;
}

// Inline radix-2 Cooley–Tukey FFT. Input arrays (re, im) of length n (power
// of 2) are transformed in place; returns nothing (caller reads re/im back).
function fftRadix2(re, im) {
  const n = re.length;
  // bit-reversal permutation
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      let t = re[i]; re[i] = re[j]; re[j] = t;
      t = im[i]; im[i] = im[j]; im[j] = t;
    }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = -TWO_PI / len;
    const wRe = Math.cos(ang), wIm = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let curRe = 1, curIm = 0;
      for (let j = 0; j < len / 2; j++) {
        const uRe = re[i + j], uIm = im[i + j];
        const vRe = re[i + j + len / 2] * curRe - im[i + j + len / 2] * curIm;
        const vIm = re[i + j + len / 2] * curIm + im[i + j + len / 2] * curRe;
        re[i + j] = uRe + vRe; im[i + j] = uIm + vIm;
        re[i + j + len / 2] = uRe - vRe; im[i + j + len / 2] = uIm - vIm;
        const nextRe = curRe * wRe - curIm * wIm;
        const nextIm = curRe * wIm + curIm * wRe;
        curRe = nextRe; curIm = nextIm;
      }
    }
  }
}

function hann(n) {
  const w = new Float64Array(n);
  for (let i = 0; i < n; i++) w[i] = 0.5 * (1 - Math.cos((TWO_PI * i) / (n - 1)));
  return w;
}

// Parabolic interpolation of a peak at integer bin i in array mag.
function parabolicPeak(mag, i) {
  if (i <= 0 || i >= mag.length - 1) return i;
  const a = mag[i - 1], b = mag[i], c = mag[i + 1];
  const denom = a - 2 * b + c;
  if (denom === 0) return i;
  return i + 0.5 * (a - c) / denom;
}

const N_STEPS = 4096;   // RK2 integration steps
const N_FFT = 2048;     // FFT window length (power of 2)
const DT = 0.02;        // normalized time step (ω_L = 1 units)
const OMEGA_INJ = 8.0;  // carrier, well above the Adler dynamics (normalized)

export default function PullingSpectrumExplorer() {
  const isEn = useIsEn();
  const [rRatio, setRRatio] = useState(1.5); // Δω/ω_L, swept 0..3
  const [fftLen, setFftLen] = useState(2048); // 1024 or 2048

  const WL = 1.0;

  const result = useMemo(() => {
    const dw = rRatio * WL;
    const nfft = fftLen;
    const theta = integrateAdler(dw, WL, DT, N_STEPS, -1.2);
    // Use the last nfft samples so the transient has settled out.
    const start = N_STEPS - nfft;
    const win = hann(nfft);
    const re = new Float64Array(nfft);
    const im = new Float64Array(nfft);
    for (let k = 0; k < nfft; k++) {
      const t = (start + k) * DT;
      const V = Math.cos(OMEGA_INJ * t + theta[start + k]);
      re[k] = V * win[k];
      im[k] = 0;
    }
    fftRadix2(re, im);
    const half = nfft / 2;
    const mag = new Float64Array(half);
    for (let k = 0; k < half; k++) mag[k] = re[k] * re[k] + im[k] * im[k];
    const dOmega = TWO_PI / (nfft * DT); // angular-frequency bin spacing

    // Find local-maxima peaks above a small threshold relative to the max.
    let maxMag = 0;
    for (let k = 0; k < half; k++) if (mag[k] > maxMag) maxMag = mag[k];
    const thresh = maxMag * 1e-5;
    const peaks = [];
    for (let k = 2; k < half - 2; k++) {
      if (mag[k] > thresh && mag[k] > mag[k - 1] && mag[k] >= mag[k + 1]) {
        peaks.push(k);
      }
    }
    // Keep the strongest few, sorted by frequency, with parabolic refinement.
    peaks.sort((a, b) => mag[b] - mag[a]);
    const top = peaks.slice(0, 8).sort((a, b) => a - b);
    const peakFreqs = top.map((i) => parabolicPeak(mag, i) * dOmega);
    const peakMagsDb = top.map((i) => 10 * Math.log10(mag[i] / (maxMag || 1)));

    const spacings = [];
    for (let i = 1; i < peakFreqs.length; i++) spacings.push(peakFreqs[i] - peakFreqs[i - 1]);
    spacings.sort((a, b) => a - b);
    const medianSpacing = spacings.length
      ? spacings[Math.floor(spacings.length / 2)]
      : null;

    const locked = rRatio < 1;
    const wbTheory = locked ? 0 : Math.sqrt(Math.max(dw * dw - WL * WL, 0));
    const errPct = (!locked && medianSpacing !== null && wbTheory > 1e-9)
      ? Math.abs(medianSpacing - wbTheory) / wbTheory * 100
      : null;

    // Downsample the magnitude spectrum for plotting (avoid 1024/2048 SVG points).
    const plotN = 240;
    const plotMagDb = new Float64Array(plotN);
    const plotOmega = new Float64Array(plotN);
    for (let p = 0; p < plotN; p++) {
      const k = Math.min(half - 1, Math.round((p / (plotN - 1)) * (half - 1)));
      plotMagDb[p] = 10 * Math.log10(Math.max(mag[k], maxMag * 1e-8) / (maxMag || 1));
      plotOmega[p] = k * dOmega;
    }

    return {
      dw, locked, wbTheory, medianSpacing, errPct,
      peakFreqs, peakMagsDb, plotMagDb, plotOmega, dOmega, half,
    };
  }, [rRatio, fftLen]);

  const {dw, locked, wbTheory, medianSpacing, errPct, peakFreqs, peakMagsDb, plotMagDb, plotOmega} = result;

  // ---- inline SVG spectrum plot ----
  const svg = useMemo(() => {
    const W = 460, H = 240;
    const padL = 40, padR = 14, padT = 16, padB = 30;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;
    const omegaMax = OMEGA_INJ + Math.max(dw, WL) * 1.6 + 1;
    const omegaMin = Math.max(0, OMEGA_INJ - Math.max(dw, WL) * 0.4);
    const dbMin = -60, dbMax = 2;
    const xOf = (w) => padL + ((w - omegaMin) / (omegaMax - omegaMin)) * plotW;
    const yOf = (db) => padT + plotH * (1 - (Math.max(db, dbMin) - dbMin) / (dbMax - dbMin));
    let d = '';
    for (let i = 0; i < plotOmega.length; i++) {
      const x = xOf(plotOmega[i]);
      const y = yOf(plotMagDb[i]);
      d += (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1) + ' ';
    }
    const injX = xOf(OMEGA_INJ);
    const peakMarks = peakFreqs.map((f, i) => ({x: xOf(f), y: yOf(peakMagsDb[i]), f}));
    return {W, H, padL, padR, padT, padB, plotW, plotH, d, injX, peakMarks, xOf, yOf, omegaMin, omegaMax};
  }, [plotOmega, plotMagDb, dw, peakFreqs, peakMagsDb]);

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
  const stateColor = locked ? 'var(--ifm-color-success)' : 'var(--ifm-color-danger)';
  const statusCard = {...card, border: `2px solid ${stateColor}`};
  const stroke = 'var(--ifm-color-emphasis-700)';
  const gridCol = 'var(--ifm-color-emphasis-300)';
  const curveCol = 'var(--ifm-color-primary)';
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
          ? 'Injection-pulling spectrum explorer (RK2 Adler integration → FFT)'
          : 'Injection pulling 頻譜互動探索器（RK2 積分 Adler → FFT）'}
      </div>

      <Row label={isEn ? 'Δω / ω_L (r)' : 'Δω / ω_L（r）'} value={rRatio} unit="" min={0.1} max={3.0} step={0.01}
           onChange={setRRatio} fmt={(v) => v.toFixed(2)} />

      <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.35rem 0', flexWrap: 'wrap'}}>
        <label style={{flex: '0 1 11rem', fontSize: '0.9rem'}}>{isEn ? 'FFT length' : 'FFT 點數'}</label>
        <button type="button" style={fftLen === 1024 ? btnActive : btn} onClick={() => setFftLen(1024)}>1024</button>
        <button type="button" style={fftLen === 2048 ? btnActive : btn} onClick={() => setFftLen(2048)}>2048</button>
      </div>

      <div style={out}>
        <div style={statusCard}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>{isEn ? 'state' : '狀態'}</div>
          <div style={{fontSize: '1.15rem', fontWeight: 800, color: stateColor}}>
            {locked ? (isEn ? 'LOCKED — single tone' : 'LOCKED — 單一純音') : (isEn ? 'PULLING — comb' : 'PULLING — 梳狀頻譜')}
          </div>
          <div style={{fontSize: '0.78rem'}}>{locked ? 'r < 1' : 'r > 1'}</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>ω_b {isEn ? '(theory)' : '（理論）'}</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>
            {locked ? '—' : wbTheory.toFixed(4)}
          </div>
          <div style={{fontSize: '0.8rem'}}>√(Δω²−ω_L²)</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>ω_b {isEn ? '(measured, FFT)' : '（量測，FFT）'}</div>
          <div style={{fontSize: '1.2rem', fontWeight: 700}}>
            {locked || medianSpacing === null ? '—' : medianSpacing.toFixed(4)}
          </div>
          <div style={{fontSize: '0.8rem'}}>
            {locked || errPct === null ? '' : `${isEn ? 'error' : '誤差'} ${errPct.toFixed(2)}%`}
          </div>
        </div>
      </div>

      <div style={{marginTop: '0.9rem'}}>
        <svg viewBox={`0 0 ${svg.W} ${svg.H}`} width="100%"
             style={{maxWidth: `${svg.W}px`, display: 'block'}}
             role="img"
             aria-label="One-sided pulling spectrum comb, magnitude in dB vs angular frequency">
          <rect x={svg.padL} y={svg.padT} width={svg.plotW} height={svg.plotH}
                fill="none" stroke={gridCol} strokeWidth="1" />
          {/* injection frequency marker */}
          <line x1={svg.injX} y1={svg.padT} x2={svg.injX} y2={svg.padT + svg.plotH}
                stroke="var(--ifm-color-danger)" strokeWidth="1.4" strokeDasharray="5 4" opacity="0.75" />
          <text x={svg.injX + 3} y={svg.padT + 11} fontSize="10" fill="var(--ifm-color-danger)">ω_inj</text>

          <path d={svg.d} fill="none" stroke={curveCol} strokeWidth="1.8" />

          {/* peak markers with parabolic-refined frequency */}
          {svg.peakMarks.map((m, i) => (
            <circle key={i} cx={m.x} cy={m.y} r="3" fill="var(--ifm-color-emphasis-800)" />
          ))}

          <text x={svg.padL} y={svg.H - 8} fontSize="10" fill={stroke}>
            {svg.omegaMin.toFixed(1)}
          </text>
          <text x={svg.padL + svg.plotW} y={svg.H - 8} fontSize="10" fill={stroke} textAnchor="end">
            {svg.omegaMax.toFixed(1)}
          </text>
          <text x={svg.padL + svg.plotW / 2} y={svg.H - 8} fontSize="10" fill={stroke} textAnchor="middle">
            ω [rad/s, normalized]
          </text>
          <text x={6} y={svg.padT + 8} fontSize="10" fill={stroke}>0 dB</text>
          <text x={6} y={svg.padT + svg.plotH} fontSize="10" fill={stroke}>−60 dB</text>
        </svg>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.78, marginTop: '0.6rem', lineHeight: 1.6}}>
        {isEn ? (
          <>
            Reading the plot: the red dashed line is the injection frequency ω_inj. Slide
            <b> r = Δω/ω_L</b> below 1 and the spectrum collapses to a single clean line at
            ω_inj — the oscillator is <b>locked</b> onto the injection, θ(t) has settled to a
            constant, so V(t) = cos(ω_inj t + θ_ss) is a pure tone. Push <b>r</b> above 1 and a
            <b> one-sided comb</b> appears, spaced by ω_b = √(Δω²−ω_L²), with one edge line pinned
            exactly at ω_inj — this is the closed form derived in Part B above ([P4] Eq.(34)).
            The "ω_b (measured, FFT)" readout takes the median spacing between the strongest comb
            lines (with parabolic sub-bin interpolation) and compares it to the theoretical
            closed form live.
          </>
        ) : (
          <>
            讀圖：紅色虛線是注入頻率 ω_inj。把 <b>r = Δω/ω_L</b> 滑到 1 以下，頻譜會收成
            ω_inj 上的一根乾淨純音——振盪器<b>鎖定</b>在注入上，θ(t) 已沉降成常數，
            所以 V(t) = cos(ω_inj t + θ_ss) 是純音。把 <b>r</b> 推過 1，會冒出<b>單邊梳</b>，
            間距 ω_b = √(Δω²−ω_L²)，其中一端的梳齒恰好貼在 ω_inj 上——這正是上方 Part B
            推導出的閉式解（[P4] Eq.(34)）。「ω_b（量測，FFT）」讀數取最強幾根梳齒間距的中位數
            （用拋物線次頻段內插提高精度），即時與理論閉式比對。
          </>
        )}
      </div>
      <div style={{fontSize: '0.74rem', opacity: 0.62, marginTop: '0.5rem', lineHeight: 1.5}}>
        {isEn
          ? `Model: RK2 (midpoint) integration of dθ/dt = Δω − ω_L·sin(θ) for ${N_STEPS} steps (dt = ${DT}, ω_L = 1 normalized), Hann-windowed FFT of V(t) = cos(ω_inj t + θ(t)) over the last ${'{1024 or 2048}'}-point window (radix-2 Cooley–Tukey, written inline, no external deps), peak positions refined with parabolic interpolation. Offline verification (Node/Python, same algorithm): at r = 1.5 the measured comb spacing matches √(Δω²−ω_L²) to within ≈0.1% using the 2048-point FFT — see the write-up in Part B and lab_27 for the reference numbers.`
          : `模型：RK2（中點法）積分 dθ/dt = Δω − ω_L·sin(θ) 共 ${N_STEPS} 步（dt = ${DT}，ω_L=1 正規化），對 V(t) = cos(ω_inj t + θ(t)) 取最後 ${'{1024 或 2048}'} 點做 Hann 窗 FFT（radix-2 Cooley–Tukey，本檔內建、無外部套件），峰值位置以拋物線內插細修。離線核對（Node/Python，同一套演算法）：在 r = 1.5 時，用 2048 點 FFT 量到的梳距與 √(Δω²−ω_L²) 誤差 ≈0.1% ——參見上方 Part B 正文與 lab_27 的參考數字。`}
      </div>
    </div>
  );
}
