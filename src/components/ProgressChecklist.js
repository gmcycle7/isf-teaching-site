import React, {useEffect, useState} from 'react';
import Link from '@docusaurus/Link';

// localStorage-persisted course progress checklist.
// Props: items = [{id, label, href}]
// - Renders a card with a checkbox list (labels are clickable links),
//   a progress bar, an "N/M 完成" readout, and a 全部清除 (clear all) button.
// - Persists to localStorage key "isf-progress-v1".
// - SSR-safe: never touches window/localStorage during render; state is
//   hydrated from localStorage in useEffect after mount, so the server and
//   the first client render agree (all unchecked), avoiding hydration
//   mismatch.
// - Links use @docusaurus/Link (framework alias, no extra dependency) so
//   hrefs like "/02_foundations/..." get the site baseUrl
//   (/isf-teaching-site/) prepended automatically and work on GitHub Pages.

const STORAGE_KEY = 'isf-progress-v1';

function readStore() {
  if (typeof window === 'undefined') return {};
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return parsed && typeof parsed === 'object' && !Array.isArray(parsed)
      ? parsed
      : {};
  } catch (e) {
    return {};
  }
}

function writeStore(state) {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    // localStorage unavailable (private mode / quota) — degrade silently,
    // the in-memory state still works for this page view.
  }
}

export default function ProgressChecklist({items = []}) {
  const [checked, setChecked] = useState({});

  // Hydrate from localStorage after mount (SSR guard).
  useEffect(() => {
    setChecked(readStore());
  }, []);

  const toggle = (id) => {
    setChecked((prev) => {
      const next = {...prev};
      if (next[id]) {
        delete next[id];
      } else {
        next[id] = true;
      }
      writeStore(next);
      return next;
    });
  };

  const clearAll = () => {
    setChecked({});
    writeStore({});
  };

  const doneCount = items.reduce((n, it) => n + (checked[it.id] ? 1 : 0), 0);
  const total = items.length;
  const pct = total > 0 ? (100 * doneCount) / total : 0;

  const box = {
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px',
    padding: '1rem 1.1rem',
    margin: '1rem 0',
    background: 'var(--ifm-color-emphasis-100)',
  };
  const headerRow = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '0.6rem',
    flexWrap: 'wrap',
    marginBottom: '0.55rem',
  };
  const barOuter = {
    height: '0.55rem',
    borderRadius: '999px',
    background: 'var(--ifm-color-emphasis-200)',
    overflow: 'hidden',
  };
  const barInner = {
    height: '100%',
    width: pct + '%',
    borderRadius: '999px',
    background: 'var(--ifm-color-primary)',
    transition: 'width 0.25s ease',
  };
  const clearBtn = {
    flex: '0 0 auto',
    fontSize: '0.8rem',
    padding: '0.25rem 0.7rem',
    borderRadius: '6px',
    border: '1px solid var(--ifm-color-emphasis-300)',
    background: 'var(--ifm-background-surface-color)',
    color: 'var(--ifm-font-color-base)',
    cursor: 'pointer',
  };

  return (
    <div style={box}>
      <div style={headerRow}>
        <div style={{fontWeight: 600, flex: '0 1 auto'}}>課程進度 Progress</div>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            flexWrap: 'wrap',
          }}
        >
          <span
            style={{
              fontSize: '0.85rem',
              fontVariantNumeric: 'tabular-nums',
              opacity: 0.85,
            }}
          >
            <b>{doneCount}</b>/{total} 完成
          </span>
          <button type="button" style={clearBtn} onClick={clearAll}>
            全部清除
          </button>
        </div>
      </div>

      <div
        style={barOuter}
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={total}
        aria-valuenow={doneCount}
        aria-label={'課程進度 ' + doneCount + '/' + total}
      >
        <div style={barInner} />
      </div>

      <ul style={{listStyle: 'none', padding: 0, margin: '0.7rem 0 0'}}>
        {items.map((it) => {
          const done = !!checked[it.id];
          return (
            <li
              key={it.id}
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.55rem',
                padding: '0.22rem 0',
                flexWrap: 'wrap',
              }}
            >
              <input
                type="checkbox"
                id={'isf-progress-' + it.id}
                checked={done}
                onChange={() => toggle(it.id)}
                style={{
                  flex: '0 0 auto',
                  marginTop: '0.28rem',
                  cursor: 'pointer',
                }}
                aria-label={it.label}
              />
              <span style={{flex: '1 1 14rem', fontSize: '0.92rem'}}>
                {it.href ? (
                  <Link
                    to={it.href}
                    style={{
                      textDecoration: done ? 'line-through' : 'none',
                      opacity: done ? 0.6 : 1,
                    }}
                  >
                    {it.label}
                  </Link>
                ) : (
                  <span
                    style={{
                      textDecoration: done ? 'line-through' : 'none',
                      opacity: done ? 0.6 : 1,
                    }}
                  >
                    {it.label}
                  </span>
                )}
              </span>
            </li>
          );
        })}
      </ul>

      <div style={{fontSize: '0.75rem', opacity: 0.65, marginTop: '0.55rem'}}>
        進度存在瀏覽器 localStorage（key <code>isf-progress-v1</code>），
        只在這台裝置、這個瀏覽器有效。
      </div>
    </div>
  );
}
