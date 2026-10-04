#!/usr/bin/env node
// Validate one or more .md/.mdx files the way Docusaurus 3 compiles them (MDX + GFM + math).
// Usage: node scripts/validate_mdx.mjs [--quiet] <file> [<file> ...]   (exit 1 on any failure)
// --quiet prints only failures and a one-line summary (used in CI).
import { compile } from '@mdx-js/mdx'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import { readFile } from 'node:fs/promises'

const args = process.argv.slice(2)
const quiet = args.includes('--quiet')
const files = args.filter((a) => a !== '--quiet')
let bad = 0
for (const f of files) {
  try {
    let src = await readFile(f, 'utf8')
    src = src.replace(/^---\n[\s\S]*?\n---\n/, '') // strip front matter
    src = src.replace(/[ \t]*\{#[A-Za-z0-9_-]+\}[ \t]*$/gm, '') // Docusaurus explicit heading ids {#id} are not MDX expressions
    await compile(src, { remarkPlugins: [remarkGfm, remarkMath], format: 'mdx' })
    if (!quiet) console.log('OK   ' + f)
  } catch (e) {
    bad++
    console.log('FAIL ' + f + '\n     ' + String(e.message || e).split('\n')[0])
  }
}
if (quiet) console.log(`mdx: ${files.length} files compiled, ${bad} failed`)
process.exit(bad ? 1 : 0)
