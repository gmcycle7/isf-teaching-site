#!/usr/bin/env node
// Validate one or more .md/.mdx files the way Docusaurus 3 compiles them (MDX + GFM + math).
// Usage: node scripts/validate_mdx.mjs <file> [<file> ...]   (exit 1 on any failure)
import { compile } from '@mdx-js/mdx'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import { readFile } from 'node:fs/promises'

let bad = 0
for (const f of process.argv.slice(2)) {
  try {
    let src = await readFile(f, 'utf8')
    src = src.replace(/^---\n[\s\S]*?\n---\n/, '') // strip front matter
    src = src.replace(/[ \t]*\{#[A-Za-z0-9_-]+\}[ \t]*$/gm, '') // Docusaurus explicit heading ids {#id} are not MDX expressions
    await compile(src, { remarkPlugins: [remarkGfm, remarkMath], format: 'mdx' })
    console.log('OK   ' + f)
  } catch (e) {
    bad++
    console.log('FAIL ' + f + '\n     ' + String(e.message || e).split('\n')[0])
  }
}
process.exit(bad ? 1 : 0)
