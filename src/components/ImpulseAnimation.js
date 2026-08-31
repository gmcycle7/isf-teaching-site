import React, {useEffect, useRef, useState} from 'react';
import useIsEn from './useIsEn';

// ImpulseAnimation — 「在 limit cycle 上打一下看相位」核心概念動畫。
//
// Ideal LC toy model：state z(θ) = (sinθ, cosθ)，橫軸 ∝ 電感電流、縱軸 = 電容電壓，
// dot 以等角速度 ω 沿 unit circle 順時針轉（θ=0 在頂端 = 電壓波峰）。
// 按「注入！」後，等 dot 轉到 θ_inj 時沿「垂直電壓軸」打一個 ΔV kick（大小 ∝ Δq/q_max），
// 並把 kick 分解成：
//   切向分量（橘）→ 永久相位偏移 Δφ = Γ(θ_inj)·Δq/q_max，Γ(θ) = −sinθ
//   徑向分量（灰）→ 振幅擾動，以指數鬆弛（時間常數 ~0.55 圈，~2 圈內衰減 97%）拉回環上
// 淡色 ghost 為未受擾參考，讓永久 lag/lead 看得見。
// 對應 [P1] Hajimiri–Lee 1998, Eqs.(10),(11), p.182 與本頁 Γ_LC(θ)=−sinθ 推導。
// 純教學 toy model，非 transistor-level。SSR-safe（module scope 不碰 window）。

const TWO_PI = 2 * Math.PI;
const DEG = Math.PI / 180;
const T_ORBIT = 6;                // 動畫一圈秒數（純視覺時間尺度）
const OMEGA = TWO_PI / T_ORBIT;   // 動畫角速度 rad/s
const TAU_AMP = 0.55 * T_ORBIT;   // 徑向（振幅）鬆弛時間常數 ≈ 0.55 圈
const ARROW_FADE = 2 * T_ORBIT;   // kick 箭頭殘留 ~2 圈後淡出
const CX = 230, CY = 200, RPX = 150;   // viewBox 460×400，circle 半徑 150
const GAIN = 1.6;                 // 箭頭視覺放大倍率（三支同倍率，分解幾何仍正確）
const COL_TAN = '#ff8c00';        // 切向（永久相位）
const COL_KICK = '#4098ff';       // ΔV kick

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

function Arrow({x1, y1, x2, y2, color, opacity = 1, width = 2.4}) {
  const dx = x2 - x1, dy = y2 - y1;
  const len = Math.hypot(dx, dy);
  if (len < 2) return null;
  const ux = dx / len, uy = dy / len;
  const hs = Math.min(9, 3 + len * 0.3);
  const bx = x2 - ux * hs, by = y2 - uy * hs;
  const px = -uy, py = ux;
  return (
    <g opacity={opacity}>
      <line x1={x1} y1={y1} x2={bx} y2={by} stroke={color} strokeWidth={width} />
      <polygon
        points={`${x2},${y2} ${bx + px * hs * 0.5},${by + py * hs * 0.5} ${bx - px * hs * 0.5},${by - py * hs * 0.5}`}
        fill={color}
      />
    </g>
  );
}

export default function ImpulseAnimation() {
  const isEn = useIsEn();
  const [running, setRunning] = useState(true);
  const [thetaInjDeg, setThetaInjDeg] = useState(90);   // 注入相位（度）
  const [eps, setEps] = useState(0.15);                 // Δq/q_max
  const [lastInj, setLastInj] = useState(null);
  const [, setTick] = useState(0);

  const runningRef = useRef(true);
  const thetaInjRef = useRef(90);
  const epsRef = useRef(0.15);
  // 模擬狀態：thetaRef = 未受擾參考相位；phi = 累積永久相位偏移；amp = 徑向（振幅）擾動
  const simRef = useRef({thetaRef: 0, phi: 0, amp: 0, armed: false, trail: [], events: []});

  useEffect(() => { thetaInjRef.current = thetaInjDeg; }, [thetaInjDeg]);
  useEffect(() => { epsRef.current = eps; }, [eps]);

  useEffect(() => {
    let raf;
    let last = null;
    const step = (now) => {
      if (last === null) last = now;
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      if (runningRef.current && dt > 0) {
        const s = simRef.current;
        const prevA = s.thetaRef + s.phi;      // dot 目前的波形相位
        s.thetaRef += OMEGA * dt;
        s.amp *= Math.exp(-dt / TAU_AMP);      // 徑向擾動指數鬆弛（amplitude restoring）
        s.events.forEach((ev) => { ev.age += dt; });
        s.events = s.events.filter((ev) => ev.age < ARROW_FADE);
        // 已排定注入：dot 波形相位跨過 θ_inj 的瞬間開火
        if (s.armed) {
          const target = thetaInjRef.current * DEG;
          const gap = (((target - (prevA % TWO_PI)) % TWO_PI) + TWO_PI) % TWO_PI;
          if (gap <= OMEGA * dt) {
            const e = epsRef.current;
            const gamma = -Math.sin(target);              // Γ(θ) = −sinθ（ideal LC）
            s.phi += gamma * e;                           // 切向 → 永久相位偏移
            s.amp = Math.max(-0.6, Math.min(0.9, s.amp + e * Math.cos(target))); // 徑向 → 振幅擾動
            s.events.push({th: target, eps: e, age: 0});
            if (s.events.length > 3) s.events.shift();
            s.armed = false;
            setLastInj({deg: thetaInjRef.current, gamma, dphi: gamma * e});
          }
        }
        // 彗星尾
        const rr = 1 + s.amp;
        const a = s.thetaRef + s.phi;
        s.trail.push([CX + RPX * rr * Math.sin(a), CY - RPX * rr * Math.cos(a)]);
        if (s.trail.length > 150) s.trail.shift();
        setTick((t) => (t + 1) % 1e9);
      }
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);   // unmount 時清掉 rAF
  }, []);

  const toggleRun = () => {
    runningRef.current = !runningRef.current;
    setRunning(runningRef.current);
  };
  const inject = () => {
    simRef.current.armed = true;
    runningRef.current = true;   // 暫停中按注入 → 自動恢復轉動，轉到 θ_inj 開火
    setRunning(true);
    setTick((t) => t + 1);
  };
  const reset = () => {
    simRef.current = {thetaRef: 0, phi: 0, amp: 0, armed: false, trail: [], events: []};
    setLastInj(null);
    setTick((t) => t + 1);
  };

  // --- 由模擬狀態導出的繪圖量 ---
  const s = simRef.current;
  const thA = s.thetaRef + s.phi;
  const rr = 1 + s.amp;
  const dotX = CX + RPX * rr * Math.sin(thA);
  const dotY = CY - RPX * rr * Math.cos(thA);
  const gX = CX + RPX * Math.sin(s.thetaRef);
  const gY = CY - RPX * Math.cos(s.thetaRef);

  const injRad = thetaInjDeg * DEG;
  const gammaLive = -Math.sin(injRad);         // Γ(θ_inj) = −sin(θ_inj)
  const dphiLive = gammaLive * eps;            // 預測 Δφ = Γ·Δq/q_max

  // θ_inj 注入標記（circle 外側的小三角形，尖端指向注入點）
  const ox = Math.sin(injRad), oy = -Math.cos(injRad);   // SVG 外向單位向量
  const pxp = -oy, pyp = ox;
  const triTip = [CX + (RPX + 3) * ox, CY + (RPX + 3) * oy];
  const triB1 = [CX + (RPX + 14) * ox + 5.5 * pxp, CY + (RPX + 14) * oy + 5.5 * pyp];
  const triB2 = [CX + (RPX + 14) * ox - 5.5 * pxp, CY + (RPX + 14) * oy - 5.5 * pyp];

  // Δφ 弧：沿 circle 從 ghost 相位畫到 dot 相位，永久 lag/lead 一眼可見
  let arcPath = null;
  if (Math.abs(s.phi) > 0.004 && Math.abs(s.phi) < TWO_PI) {
    const sweep = s.phi > 0 ? 1 : 0;
    const large = Math.abs(s.phi) > Math.PI ? 1 : 0;
    const ex = CX + RPX * Math.sin(thA), ey = CY - RPX * Math.cos(thA);
    arcPath = `M ${gX} ${gY} A ${RPX} ${RPX} 0 ${large} ${sweep} ${ex} ${ey}`;
  }

  // 四個定位標籤
  const marks = isEn
    ? [
        {deg: 0, lines: ['θ=0° (peak)'], x: CX, y: 34, anchor: 'middle'},
        {deg: 90, lines: ['θ=90°', 'zero crossing (falling)'], x: CX + RPX + 8, y: CY - 4, anchor: 'start'},
        {deg: 180, lines: ['θ=180° (trough)'], x: CX, y: CY + RPX + 24, anchor: 'middle'},
        {deg: 270, lines: ['θ=270°', 'zero crossing (rising)'], x: CX - RPX - 8, y: CY - 4, anchor: 'end'},
      ]
    : [
        {deg: 0, lines: ['θ=0°（波峰）'], x: CX, y: 34, anchor: 'middle'},
        {deg: 90, lines: ['θ=90°', '零交越（降）'], x: CX + RPX + 8, y: CY - 4, anchor: 'start'},
        {deg: 180, lines: ['θ=180°（波谷）'], x: CX, y: CY + RPX + 24, anchor: 'middle'},
        {deg: 270, lines: ['θ=270°', '零交越（升）'], x: CX - RPX - 8, y: CY - 4, anchor: 'end'},
      ];

  // 注入事件的三支箭頭（kick／切向／徑向），錨在注入點
  const k = RPX * GAIN;
  const eventEls = s.events.map((ev, i) => {
    const sinT = Math.sin(ev.th), cosT = Math.cos(ev.th);
    const bx = CX + RPX * sinT, by = CY - RPX * cosT;
    const fade = Math.max(0, 1 - ev.age / ARROW_FADE);
    // 切向分量（state 座標）：(Δz·t̂)t̂ = (−ε sinθ)(cosθ, −sinθ)
    const tvx = -ev.eps * sinT * cosT;
    const tvy = ev.eps * sinT * sinT;
    // 徑向分量：(Δz·n̂)n̂ = (ε cosθ)(sinθ, cosθ)，長度隨鬆弛縮短
    const rmag = ev.eps * cosT * Math.exp(-ev.age / TAU_AMP);
    const rvx = rmag * sinT;
    const rvy = rmag * cosT;
    return (
      <g key={`${i}-${ev.th.toFixed(3)}`}>
        <Arrow x1={bx} y1={by} x2={bx + k * rvx} y2={by - k * rvy}
               color="var(--ifm-color-emphasis-600)" opacity={fade} width={2.2} />
        <Arrow x1={bx} y1={by} x2={bx + k * tvx} y2={by - k * tvy}
               color={COL_TAN} opacity={fade} width={2.8} />
        <Arrow x1={bx} y1={by} x2={bx} y2={by - ev.eps * k}
               color={COL_KICK} opacity={0.85 * fade} width={2.2} />
      </g>
    );
  });

  // --- 樣式 ---
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
  const card = {
    flex: '1 1 9rem', background: 'var(--ifm-background-color)',
    border: '1px solid var(--ifm-color-emphasis-200)', borderRadius: '6px',
    padding: '0.55rem 0.8rem', textAlign: 'center',
  };
  const legendItem = {display: 'inline-flex', alignItems: 'center', gap: '0.3rem', marginRight: '0.9rem'};
  const swatch = (c) => ({display: 'inline-block', width: '0.9em', height: '0.28em', background: c, borderRadius: '2px'});
  const dotSwatch = (c, o = 1) => ({display: 'inline-block', width: '0.7em', height: '0.7em', background: c, borderRadius: '50%', opacity: o});

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem'}}>
        {isEn
          ? 'Interactive "kick the limit cycle and watch the phase" animation (ideal LC toy model)'
          : 'Limit cycle 上「打一下看相位」互動動畫（ideal LC toy model）'}
      </div>

      <svg viewBox="0 0 460 400" role="img"
           aria-label="Limit cycle impulse injection animation"
           style={{width: '100%', height: 'auto', display: 'block', maxWidth: '560px', margin: '0 auto'}}>
        {/* 座標軸（虛線）＋ limit cycle */}
        <line x1={CX - RPX - 14} y1={CY} x2={CX + RPX + 14} y2={CY}
              stroke="var(--ifm-color-emphasis-300)" strokeWidth="1" strokeDasharray="4 4" />
        <line x1={CX} y1={CY - RPX - 14} x2={CX} y2={CY + RPX + 14}
              stroke="var(--ifm-color-emphasis-300)" strokeWidth="1" strokeDasharray="4 4" />
        <circle cx={CX} cy={CY} r={RPX} fill="var(--ifm-background-surface-color)"
                stroke="var(--ifm-color-emphasis-400)" strokeWidth="1.6" />

        {/* 四個相位定位刻度與標籤 */}
        {marks.map((m) => {
          const sn = Math.sin(m.deg * DEG), cs = Math.cos(m.deg * DEG);
          return (
            <g key={m.deg}>
              <line x1={CX + (RPX - 6) * sn} y1={CY - (RPX - 6) * cs}
                    x2={CX + (RPX + 6) * sn} y2={CY - (RPX + 6) * cs}
                    stroke="var(--ifm-color-emphasis-500)" strokeWidth="1.4" />
              {m.lines.map((txt, j) => (
                <text key={j} x={m.x} y={m.y + j * 14} textAnchor={m.anchor}
                      fontSize="11" fill="var(--ifm-color-emphasis-700)">{txt}</text>
              ))}
            </g>
          );
        })}

        {/* θ_inj 注入標記（三角形，尖端指向注入點；armed 時實心醒目） */}
        <polygon points={`${triTip[0]},${triTip[1]} ${triB1[0]},${triB1[1]} ${triB2[0]},${triB2[1]}`}
                 fill="var(--ifm-color-primary)" opacity={s.armed ? 1 : 0.55} />

        {/* Δφ 弧（ghost → dot 的永久 lag/lead） */}
        {arcPath && (
          <path d={arcPath} fill="none" stroke={COL_TAN} strokeWidth="5"
                strokeLinecap="round" opacity="0.85" />
        )}

        {/* 彗星尾 */}
        {s.trail.length > 1 && (
          <polyline points={s.trail.map((p) => p.join(',')).join(' ')}
                    fill="none" stroke="var(--ifm-color-primary)" strokeWidth="2" opacity="0.3" />
        )}

        {/* 半徑輔助線：中心→ghost（虛線）、中心→dot */}
        <line x1={CX} y1={CY} x2={gX} y2={gY}
              stroke="var(--ifm-color-emphasis-500)" strokeWidth="1" strokeDasharray="3 4" opacity="0.5" />
        <line x1={CX} y1={CY} x2={dotX} y2={dotY}
              stroke="var(--ifm-color-primary)" strokeWidth="1" opacity="0.35" />

        {/* 注入事件箭頭（徑向灰、切向橘、kick 藍） */}
        {eventEls}

        {/* ghost（未受擾參考，永遠在 unit circle 上） */}
        <circle cx={gX} cy={gY} r="7" fill="var(--ifm-color-emphasis-500)" opacity="0.45" />

        {/* 實際 dot（受擾：相位含 Δφ、半徑含衰減中的振幅擾動） */}
        <circle cx={dotX} cy={dotY} r="8" fill="var(--ifm-color-primary)"
                stroke="var(--ifm-background-surface-color)" strokeWidth="1.5" />
      </svg>

      {/* 圖例 */}
      <div style={{fontSize: '0.78rem', opacity: 0.85, margin: '0.5rem 0 0.6rem', lineHeight: 1.9}}>
        {isEn ? (
          <>
            <span style={legendItem}><span style={dotSwatch('var(--ifm-color-primary)')} />actual dot (perturbed)</span>
            <span style={legendItem}><span style={dotSwatch('var(--ifm-color-emphasis-500)', 0.45)} />ghost (unperturbed reference)</span>
            <span style={legendItem}><span style={{color: 'var(--ifm-color-primary)'}}>▲</span>θ_inj injection point</span>
            <span style={legendItem}><span style={swatch(COL_KICK)} />ΔV kick (along vertical voltage axis)</span>
            <span style={legendItem}><span style={swatch(COL_TAN)} />tangential component / Δφ arc (permanent)</span>
            <span style={legendItem}><span style={swatch('var(--ifm-color-emphasis-600)')} />radial component (amplitude, exponential relaxation)</span>
          </>
        ) : (
          <>
            <span style={legendItem}><span style={dotSwatch('var(--ifm-color-primary)')} />實際 dot（受擾）</span>
            <span style={legendItem}><span style={dotSwatch('var(--ifm-color-emphasis-500)', 0.45)} />ghost（未受擾參考）</span>
            <span style={legendItem}><span style={{color: 'var(--ifm-color-primary)'}}>▲</span>θ_inj 注入點</span>
            <span style={legendItem}><span style={swatch(COL_KICK)} />ΔV kick（沿垂直電壓軸）</span>
            <span style={legendItem}><span style={swatch(COL_TAN)} />切向分量／Δφ 弧（永久）</span>
            <span style={legendItem}><span style={swatch('var(--ifm-color-emphasis-600)')} />徑向分量（振幅，指數鬆弛）</span>
          </>
        )}
      </div>

      {/* 控制列 */}
      <Row label={isEn ? 'Injection phase θ_inj' : '注入相位 θ_inj'} value={thetaInjDeg} unit="°" min={0} max={360} step={1}
           onChange={setThetaInjDeg} fmt={(v) => v.toFixed(0)} />
      <Row label={isEn ? 'Charge ratio Δq/q_max' : '電荷比 Δq/q_max'} value={eps} unit="" min={0.02} max={0.3} step={0.01}
           onChange={setEps} fmt={(v) => v.toFixed(2)} />
      <div style={{display: 'flex', gap: '0.6rem', flexWrap: 'wrap', margin: '0.6rem 0'}}>
        <button type="button" style={btnPrimary} onClick={inject}>{isEn ? 'Inject!' : '注入！'}</button>
        <button type="button" style={btn} onClick={toggleRun}>{running ? (isEn ? 'Pause' : '暫停') : (isEn ? 'Play' : '播放')}</button>
        <button type="button" style={btn} onClick={reset}>{isEn ? 'Reset' : '重設'}</button>
      </div>
      <div role="status" aria-live="polite" style={{fontSize: '0.82rem', opacity: 0.8, minHeight: '1.3em'}}>
        {isEn
          ? (s.armed
              ? `Injection armed: Δq will fire when the dot reaches θ_inj = ${thetaInjDeg}° (Γ = ${gammaLive.toFixed(3)})`
              : lastInj
                ? `Last injection @ θ = ${lastInj.deg}°: Γ = ${lastInj.gamma.toFixed(3)}, Δφ = ${lastInj.dphi.toFixed(4)} rad (kept permanently)`
                : 'Click "Inject!" — a packet of charge Δq fires once the dot reaches θ_inj.')
          : (s.armed
              ? `已排定注入：等 dot 轉到 θ_inj = ${thetaInjDeg}° 時打入 Δq（Γ = ${gammaLive.toFixed(3)}）`
              : lastInj
                ? `上次注入 @ θ = ${lastInj.deg}°：Γ = ${lastInj.gamma.toFixed(3)}，Δφ = ${lastInj.dphi.toFixed(4)} rad（永久保留）`
                : '按「注入！」，dot 轉到 θ_inj 時會打入一坨電荷 Δq。')}
      </div>

      {/* 即時讀數 */}
      <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem'}}>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>Γ(θ_inj) = −sin(θ_inj)</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{gammaLive.toFixed(3)}</div>
          <div style={{fontSize: '0.8rem'}}>{isEn ? 'dimensionless' : '無因次'}</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>{isEn ? 'Δφ = Γ·Δq/q_max (this prediction)' : 'Δφ = Γ·Δq/q_max（本次預測）'}</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{dphiLive.toFixed(4)}</div>
          <div style={{fontSize: '0.8rem'}}>rad ({(dphiLive / DEG).toFixed(2)}°)</div>
        </div>
        <div style={card}>
          <div style={{fontSize: '0.8rem', opacity: 0.7}}>{isEn ? 'Accumulated Δφ (dot − ghost)' : '累積 Δφ（dot − ghost）'}</div>
          <div style={{fontSize: '1.3rem', fontWeight: 700}}>{s.phi.toFixed(4)}</div>
          <div style={{fontSize: '0.8rem'}}>rad ({(s.phi / DEG).toFixed(2)}°)</div>
        </div>
      </div>

      <div style={{fontSize: '0.78rem', opacity: 0.7, marginTop: '0.7rem'}}>
        {isEn ? (
          <>
            Model: the unit-circle limit cycle of an ideal LC (a pedagogical toy model, not
            transistor-level). Δφ = Γ(θ_inj)·Δq/q_max, Γ(θ) = −sinθ (derived in Steps A–D on this
            page; [P1] Eqs.(10),(11), p.182). Negative Δφ = phase lag, positive Δφ = phase lead.
            The radial (amplitude) component is shown relaxing exponentially with time constant
            ≈ 0.55 cycles (≈ 2.6% remaining after 2 cycles); all three arrows share the same 1.6×
            visual magnification, so the decomposition geometry stays correct.
          </>
        ) : (
          <>
            模型：ideal LC 的 unit-circle limit cycle（pedagogical toy model，非 transistor-level）。
            Δφ = Γ(θ_inj)·Δq/q_max、Γ(θ) = −sinθ（本頁 Step A–D 推導；[P1] Eqs.(10),(11), p.182）。
            負 Δφ = 相位落後（lag）、正 Δφ = 超前（lead）。徑向（振幅）分量以時間常數 ≈ 0.55 圈
            的指數鬆弛示意（2 圈後殘餘 ≈ 2.6%）；三支箭頭同以 1.6× 視覺放大，分解幾何仍正確。
          </>
        )}
      </div>
    </div>
  );
}
