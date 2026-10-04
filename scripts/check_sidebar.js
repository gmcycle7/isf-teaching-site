#!/usr/bin/env node
// Every page under docs/ must be reachable from sidebars.js (pages have been orphaned before).
// Usage: node scripts/check_sidebar.js   (exit 1 if any doc id is missing)
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const sidebar = JSON.stringify(require(path.join(root, 'sidebars.js')));

function walk(dir) {
  return fs.readdirSync(dir, {withFileTypes: true}).flatMap((e) =>
    e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)],
  );
}

const docsDir = path.join(root, 'docs');
const ids = walk(docsDir)
  .filter((f) => /\.mdx?$/.test(f))
  .map((f) => path.relative(docsDir, f).split(path.sep).join('/').replace(/\.mdx?$/, ''));
const missing = ids.filter((id) => !sidebar.includes('"' + id + '"'));
console.log(`sidebar: ${ids.length} pages, ${missing.length} not in sidebars.js`);
missing.forEach((id) => console.log('MISSING', id));
process.exit(missing.length ? 1 : 0);
