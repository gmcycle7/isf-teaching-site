// @ts-check
// Docusaurus 3 configuration for the ISF teaching site.
// remark-math@6 / rehype-katex@7 are ESM-only, so we load them with a dynamic
// import() inside an async config factory (the documented Docusaurus 3 pattern).
// KaTeX CSS is self-hosted from static/katex/ for fully offline math rendering.

const {themes} = require('prism-react-renderer');

/** @returns {Promise<import('@docusaurus/types').Config>} */
module.exports = async function createConfig() {
  const math = (await import('remark-math')).default;
  const katex = (await import('rehype-katex')).default;

  return {
    title: 'ISF & Oscillator Phase Noise',
    tagline: 'From Paper to Design Intuition — 從論文到設計直覺',
    favicon: 'img/favicon.ico',

    // Project page on GitHub Pages: https://gmcycle7.github.io/isf-teaching-site/
    url: 'https://gmcycle7.github.io',
    baseUrl: '/isf-teaching-site/',

    organizationName: 'gmcycle7',
    projectName: 'isf-teaching-site',

    onBrokenLinks: 'warn',
    onBrokenMarkdownLinks: 'warn',
    onBrokenAnchors: 'warn',

    i18n: {
      defaultLocale: 'zh-Hant',
      locales: ['zh-Hant'],
    },

    markdown: {
      mermaid: true,
    },
    themes: [
      '@docusaurus/theme-mermaid',
      // Offline local search (no Algolia / no network). Builds a local index.
      [
        require.resolve('@easyops-cn/docusaurus-search-local'),
        {
          hashed: true,
          indexDocs: true,
          indexBlog: false,
          docsRouteBasePath: '/',
          language: ['en', 'zh'],
          highlightSearchTermsOnTargetPage: true,
        },
      ],
    ],

    presets: [
      [
        'classic',
        /** @type {import('@docusaurus/preset-classic').Options} */
        ({
          docs: {
            path: 'docs',
            routeBasePath: '/', // serve docs at the site root
            // Keep the numeric folder prefixes (00_, 01_, ...) in doc IDs and
            // URLs so the sidebar and all internal /02_foundations/... links resolve.
            numberPrefixParser: false,
            sidebarPath: require.resolve('./sidebars.js'),
            remarkPlugins: [math],
            rehypePlugins: [katex],
            showLastUpdateTime: false,
          },
          blog: false,
          theme: {
            // KaTeX CSS is bundled through webpack (not a static <link>), so it
            // works at any baseUrl — e.g. a GitHub Pages project page /REPO/ —
            // and stays fully offline (fonts are emitted as hashed assets).
            customCss: [
              require.resolve('./src/css/custom.css'),
              require.resolve('katex/dist/katex.min.css'),
            ],
          },
        }),
      ],
    ],

    themeConfig:
      /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
      ({
        colorMode: {
          defaultMode: 'light',
          respectPrefersColorScheme: true,
        },
        navbar: {
          title: 'ISF Teaching Site',
          items: [
            {
              type: 'docSidebar',
              sidebarId: 'mainSidebar',
              position: 'left',
              label: '課程目錄',
            },
            {to: '/00_overview/build_report', label: 'Build Report', position: 'right'},
            {to: '/99_appendix/references', label: 'References', position: 'right'},
          ],
        },
        footer: {
          style: 'dark',
          copyright:
            'ISF Teaching Site — 教學用途。所有論文版權屬原作者。Built with Docusaurus.',
        },
        prism: {
          theme: themes.github,
          darkTheme: themes.dracula,
          additionalLanguages: ['python', 'bash', 'json', 'latex'],
        },
        tableOfContents: {
          minHeadingLevel: 2,
          maxHeadingLevel: 4,
        },
      }),
  };
};
