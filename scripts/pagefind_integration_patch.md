# Pagefind integration — proposed patch (NOT applied)

Status: **prototype evaluation only**. This document describes the diffs needed to
switch the site's search from `@easyops-cn/docusaurus-search-local` to
[Pagefind](https://pagefind.app) (v1.5.2 tested). Nothing here has been applied to
`docusaurus.config.js` or `package.json` — see `unit-C1` eval report for the
measured numbers and the GO/NO-GO call.

Evaluated by running `npx --yes pagefind --site build --output-subdir _pagefind_eval`
against the existing `build/` (from the last deploy) and querying the result with
Pagefind's Node/browser API (`pagefind.js`'s `search()`/`options()`/`init()` exports,
run under Node 24 against a local static server so its internal `fetch()` calls
resolve). `build/_pagefind_eval` was deleted after measurement, per the task spec.

---

## 1. How indexing would work (postbuild hook, both locales in one pass)

Pagefind's CLI walks a directory of already-rendered HTML and derives per-page
language from each page's own `<html lang="…">` attribute — it does **not** need to
be told about Docusaurus locales at all. Since this site's `docusaurus build`
already emits both locales into one `build/` tree (root = zh-Hant at
`defaultLocale`, `/en/**` = English, per `docusaurus.config.js` lines 30-34, which
sets `htmlLang: 'en'` for the en locale and Docusaurus's own default for zh-Hant),
**a single `pagefind --site build` run after `docusaurus build` indexes both
locales together** in one index. This was confirmed directly in the prototype: the
CLI printed `Discovered 2 languages: zh-hant, en` and `Indexed 188 pages` (94 zh +
94 en) from one pass over the one `build/` directory. No per-locale build/run split
is needed.

### package.json diff (not applied)

```diff
   "scripts": {
     "docusaurus": "docusaurus",
     "start": "docusaurus start",
-    "build": "NODE_OPTIONS=--max-old-space-size=8192 docusaurus build",
+    "build": "NODE_OPTIONS=--max-old-space-size=8192 docusaurus build && pagefind --site build --output-subdir pagefind",
     "serve": "docusaurus serve",
     ...
   },
+  "devDependencies": {
+    "@docusaurus/module-type-aliases": "3.10.1",
+    "@docusaurus/types": "3.10.1",
+    "pagefind": "^1.5.2"
+  },
```

`pagefind` (the npm package) ships the `pagefind` CLI binary as its `bin` entry, so
`npx`/the local `node_modules/.bin/pagefind` resolves once it's a devDependency —
no separate download step needed at build time, no network access required for
users running `npm run build` (the platform binary is an npm `optionalDependency`
of the `pagefind` package, e.g. `@pagefind/darwin-arm64`, resolved by npm's normal
optional-dependency mechanism, same pattern as `esbuild`/`swc`).

Output is written to `build/pagefind/` (via `--output-subdir pagefind`, chosen to
avoid colliding with the existing `build/search/` directory that
`docusaurus-search-local` currently owns — that directory and
`build/search-index.json` / `build/en/search-index.json` would be retired once
`docusaurus-search-local` is removed from `themes` in step 3 below).

### docusaurus.config.js diff (not applied)

```diff
     themes: [
       '@docusaurus/theme-mermaid',
-      // Offline local search (no Algolia / no network). Builds a local index.
-      [
-        require.resolve('@easyops-cn/docusaurus-search-local'),
-        {
-          hashed: true,
-          indexDocs: true,
-          indexBlog: false,
-          docsRouteBasePath: '/',
-          language: ['en', 'zh'],
-          highlightSearchTermsOnTargetPage: true,
-        },
-      ],
     ],
```

Pagefind is not a Docusaurus theme/plugin — it runs as a postbuild CLI step (above)
and is wired into the UI via a swizzled component (step 2), so it needs no entry in
`themes`/`plugins` at all. Removing the `@easyops-cn/docusaurus-search-local` theme
entry also removes its build-time cost of writing `search-index.json` (13 MB zh +
12 MB en, see the eval report) and its `build/search/` route.

`static/.nojekyll` already exists (`build/.nojekyll` is present in the current
build), so GitHub Pages won't mangle the new `build/pagefind/` directory — Pagefind
writes only regular files under it, no leading-underscore paths.

---

## 2. How the UI would work (swizzle `SearchBar`)

`@easyops-cn/docusaurus-search-local` currently supplies its own `SearchBar`
implementation via the theme it registers. Removing it means the classic preset's
default (Algolia-shaped, but with no `algolia` config supplied) `SearchBar` swizzle
point becomes the thing to eject and replace:

```bash
npm run swizzle @docusaurus/theme-classic SearchBar -- --wrap
# or --eject if wrap doesn't give enough control over the trigger button
```

This writes `src/theme/SearchBar/index.js` (wrap) or a full `src/theme/SearchBar/`
(eject). The replacement component:

1. Is client-side only (`useEffect`, or `@docusaurus/BrowserOnly` wrapper) — Pagefind's
   `pagefind.js` uses `WebAssembly` + `fetch` and must never run during Docusaurus's
   Node-side SSR build pass.
2. Dynamically imports the built index's entry module:
   ```js
   const pagefind = await import(
     /* webpackIgnore: true */ 'https://REPLACE-WITH-SITE-ROOT/pagefind/pagefind.js'
   );
   ```
   or, simpler and what Pagefind's own docs recommend for a turnkey widget, mounts
   the prebuilt `PagefindUI` class that ships in the same output directory
   (`build/pagefind/pagefind-ui.js` / `pagefind-ui.css` — both were present and
   measured in the prototype's `_pagefind_eval` output: 120 KB JS + 16 KB CSS
   gzippable static assets, no separate npm install needed since they're emitted by
   the CLI, not imported from a package):
   ```js
   import('/pagefind/pagefind-ui.js').then(() => {
     new window.PagefindUI({ element: '#search-modal', showSubResults: true });
   });
   ```
3. Needs **no explicit per-locale wiring** for which index to search — Pagefind's
   `pagefind.js` calls `document.querySelector('html').getAttribute('lang')` itself
   (verified by reading the shipped `pagefind.js` source directly) and loads the
   matching language's index automatically, so the same swizzled component works
   unmodified on both `/` (zh-Hant) and `/en/**` (en) — matching how
   `docusaurus-search-local`'s `language: ['en', 'zh']` config behaves today, but
   without needing an explicit language list at all.
4. `useBaseUrl('/pagefind/pagefind-ui.js')` (or the `.css`) should be used instead
   of a hardcoded `/pagefind/...` path, since the site is not served from a root
   path in every deploy target this project has used (see project-state memory on
   deploy quirks) — a raw absolute path risks breaking under a `baseUrl` other than
   `/`.

`i18n/en/docusaurus-plugin-content-docs/current/` needs no changes for this step —
Pagefind indexes rendered HTML output, not source Markdown, so the swizzled
component (a `src/theme` file, not per-locale content) is shared by both locales
automatically. If `--eject` is used instead of `--wrap`, Docusaurus also expects a
translated copy of any UI strings the new component introduces
(`i18n/en/docusaurus-theme-classic/theme-classic.json` "unwritten" for a swizzled
component's own literals) — audit that file if the ejected SearchBar hardcodes new
UI text such as a placeholder or empty-state string.

---

## 3. Removing the retired plugin

Once the swizzle is verified against a real `npm run build`:

```diff
   "dependencies": {
     "@docusaurus/core": "3.10.1",
     "@docusaurus/preset-classic": "3.10.1",
     "@docusaurus/theme-mermaid": "3.10.1",
-    "@easyops-cn/docusaurus-search-local": "^0.55.2",
     "@mdx-js/react": "^3.0.0",
     ...
```

and delete the theme entry shown in the config diff in step 1.

---

## 4. What this prototype did NOT resolve — read before applying

The zh-hant query-quality results in the eval report (recall for common 2-character
technical compounds such as 雜訊/時脈/振盪器/積分 was far below their true page counts,
while other compounds such as 頻率/電荷/線寬/鎖相 over-matched relative to their true
counts — cross-checked against literal-substring ground truth computed directly
from the built HTML) point to a real Traditional-Chinese segmentation problem in
Pagefind, not a harness artifact (confirmed with a real local HTTP server, the
correct per-locale index explicitly selected, and English-language queries on the
same corpus behaving close to their ground truth as a control). **Applying this
patch as-is would ship a search box whose Chinese results are unreliable on this
site's own core vocabulary** — see the eval report for the full number set and the
GO/NO-GO recommendation before doing so.
