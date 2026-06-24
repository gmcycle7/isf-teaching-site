#!/usr/bin/env bash
#
# deploy.sh — one-command redeploy of the ISF teaching site to GitHub Pages.
#
# It rebuilds the static site (with the project-page baseUrl /isf-teaching-site/)
# and force-pushes the built output to the `gh-pages` branch, which GitHub Pages
# serves. This needs only the `repo` token scope — NOT the `workflow` scope —
# so it works with the current `gh` login.
#
# Usage:
#     ./scripts/deploy.sh
#
# After it finishes, the live site updates once GitHub finishes its Pages build
# (typically 1–3 minutes):
#     https://gmcycle7.github.io/isf-teaching-site/
#
# NOTE: this publishes the *built site* to gh-pages. Commit your *source* changes
# to `main` separately (git add -A && git commit && git push origin main).

set -euo pipefail
cd "$(dirname "$0")/.."

REMOTE="$(git remote get-url origin)"
echo "==> Remote: ${REMOTE}"

echo "==> Building static site (Docusaurus, baseUrl /isf-teaching-site/) ..."
npm run build

echo "==> Publishing build/ to the gh-pages branch ..."
touch build/.nojekyll          # let GitHub Pages serve _-prefixed asset paths
(
  cd build
  rm -rf .git
  git init -q -b gh-pages
  git add -A
  git -c user.email="gmcycle7@gmail.com" -c user.name="gmcycle7" \
      commit -q -m "Deploy $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  git push -f -q "${REMOTE}" gh-pages:gh-pages
  rm -rf .git                  # keep build/ as a plain (gitignored) output dir
)

echo "==> Done. Live in ~1–3 min: https://gmcycle7.github.io/isf-teaching-site/"
echo "    (Check build status:  gh api repos/gmcycle7/isf-teaching-site/pages/builds/latest)"
