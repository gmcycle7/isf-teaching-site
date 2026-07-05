import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// useIsEn — tiny shared hook so interactive widgets can switch their
// hard-coded UI chrome strings (buttons/labels/captions/feedback) to English
// when the site is being viewed under the "en" locale, while keeping
// zh-Hant as the default. This does NOT translate per-page prop content
// (prompts/hints passed in from MDX) — that is translated at the page level
// via i18n/en/... markdown/mdx files.
//
// Implementation: useDocusaurusContext().i18n.currentLocale is the correct,
// SSR-safe API for this — it comes from Docusaurus's own i18n config
// (docusaurus.config.js: i18n.locales = ['zh-Hant', 'en']) rather than
// string-matching the URL, so it works regardless of baseUrl
// (/isf-teaching-site/) and trailing-slash/query-string edge cases.
// SSR-safe: no window/document access; useDocusaurusContext works
// identically during server render and client hydration.
export default function useIsEn() {
  const {i18n} = useDocusaurusContext();
  return i18n.currentLocale === 'en';
}
