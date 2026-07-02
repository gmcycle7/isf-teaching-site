import React, {useId, useState} from 'react';

// Reusable instant-feedback numeric quiz（即時回饋數值小測驗）。
// Props:
//   prompt       題目文字（純文字，可含 unicode 如 Γ、×10⁻¹²；不做數學渲染）
//   answer       正確數值（number）
//   tol          相對容許誤差（default 0.05 = ±5%）
//   unit         答案單位字串（例如 "fs"、"dBc/Hz"）
//   hint         提示（答錯 1 次後顯示）
//   solutionNote 解說（答對或按「顯示答案」後顯示）
// 純 client component、SSR-safe（module scope 不碰 window）。

function parseNumber(raw) {
  if (typeof raw !== 'string') return NaN;
  const cleaned = raw
    .trim()
    .replace(/[−–—]/g, '-') // unicode minus/dash → ASCII '-'
    .replace(/,/g, '');
  if (cleaned === '') return NaN;
  const v = Number(cleaned);
  return Number.isFinite(v) ? v : NaN;
}

export default function NumericQuiz({
  prompt,
  answer,
  tol = 0.05,
  unit = '',
  hint = '',
  solutionNote = '',
}) {
  const inputId = useId();
  const [raw, setRaw] = useState('');
  const [status, setStatus] = useState('idle'); // idle | correct | wrong | invalid | revealed
  const [wrongTries, setWrongTries] = useState(0);

  const check = () => {
    if (status === 'revealed') return;
    const v = parseNumber(raw);
    if (Number.isNaN(v)) {
      setStatus('invalid');
      return;
    }
    const scale = Math.max(Math.abs(answer), Number.MIN_VALUE);
    if (Math.abs(v - answer) / scale <= tol) {
      setStatus('correct');
    } else {
      setStatus('wrong');
      setWrongTries((t) => t + 1);
    }
  };

  const reveal = () => {
    setStatus('revealed');
  };

  const done = status === 'correct' || status === 'revealed';
  const showHint = hint && wrongTries >= 1 && !done;

  let feedback = null;
  let feedbackColor = 'var(--ifm-color-emphasis-700)';
  if (status === 'correct') {
    feedback =
      wrongTries === 0
        ? '✓ 一次就答對，非常漂亮！'
        : '✓ 答對了——修正得很好，繼續保持！';
    feedbackColor = 'var(--ifm-color-success)';
  } else if (status === 'wrong') {
    feedback =
      wrongTries <= 1
        ? '✗ 還差一點——檢查一下單位與 10 的冪次，再試一次！'
        : '✗ 尚未命中。別氣餒，可以參考提示，或按「顯示答案」。';
    feedbackColor = 'var(--ifm-color-danger)';
  } else if (status === 'invalid') {
    feedback = '請輸入數字（可用科學記號，例如 15.9、1.6e-14 或 -148）。';
    feedbackColor = 'var(--ifm-color-warning-darkest, var(--ifm-color-emphasis-700))';
  } else if (status === 'revealed') {
    feedback = `參考答案：${answer} ${unit}`.trim() + '。看懂後建議再展開下方完整解答對照。';
    feedbackColor = 'var(--ifm-color-emphasis-800)';
  }

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px',
    padding: '0.9rem 1.1rem',
    margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const btn = {
    padding: '0.35rem 0.9rem',
    borderRadius: '6px',
    border: '1px solid var(--ifm-color-emphasis-400)',
    background: 'var(--ifm-background-surface-color)',
    color: 'var(--ifm-font-color-base)',
    cursor: done ? 'default' : 'pointer',
    fontSize: '0.9rem',
  };

  return (
    <div style={box}>
      <div style={{fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.95rem'}}>
        小測驗（先自己算，再檢查）
      </div>
      <label htmlFor={inputId} style={{display: 'block', fontSize: '0.9rem', marginBottom: '0.5rem'}}>
        {prompt}
      </label>
      <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap'}}>
        <input
          id={inputId}
          type="text"
          inputMode="decimal"
          value={raw}
          disabled={done}
          placeholder="輸入數值"
          aria-label={`作答欄位${unit ? `（單位 ${unit}）` : ''}`}
          onChange={(e) => {
            setRaw(e.target.value);
            if (status === 'wrong' || status === 'invalid') setStatus('idle');
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter') check();
          }}
          style={{
            flex: '1 1 8rem',
            maxWidth: '12rem',
            padding: '0.35rem 0.6rem',
            borderRadius: '6px',
            border: '1px solid var(--ifm-color-emphasis-400)',
            background: 'var(--ifm-background-surface-color)',
            color: 'var(--ifm-font-color-base)',
            fontVariantNumeric: 'tabular-nums',
          }}
        />
        <span style={{flex: '0 0 auto', fontSize: '0.9rem', opacity: 0.85}}>{unit}</span>
        <button type="button" onClick={check} disabled={done} style={btn}>
          檢查
        </button>
        <button type="button" onClick={reveal} disabled={done} style={{...btn, opacity: done ? 0.6 : 0.85}}>
          顯示答案
        </button>
      </div>
      <div role="status" aria-live="polite" style={{minHeight: '1.2rem', marginTop: '0.55rem'}}>
        {feedback && (
          <div style={{fontSize: '0.88rem', fontWeight: 600, color: feedbackColor}}>{feedback}</div>
        )}
        {showHint && (
          <div style={{fontSize: '0.85rem', marginTop: '0.3rem', color: 'var(--ifm-color-emphasis-700)'}}>
            提示：{hint}
          </div>
        )}
        {done && solutionNote && (
          <div style={{fontSize: '0.85rem', marginTop: '0.3rem', color: 'var(--ifm-color-emphasis-700)'}}>
            {solutionNote}
          </div>
        )}
      </div>
      <div style={{fontSize: '0.75rem', opacity: 0.65, marginTop: '0.4rem'}}>
        判定：相對誤差 ±{Math.round(tol * 100)}% 內算對；可用科學記號輸入。
      </div>
    </div>
  );
}
