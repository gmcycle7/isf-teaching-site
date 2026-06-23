#!/usr/bin/env python3
"""
verify_examples.py — run every Python example in docs/ that states an expected
answer (a `# -> ...` comment) and check the printed output matches.

A block is "checkable" if it contains at least one `# -> ...` comment with a
number. Each expected number must appear in the block's stdout within a 5%
relative tolerance (or exactly for integers/strings).

Usage:
    python scripts/verify_examples.py [--verbose]
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NUM = re.compile(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?')
EXP_NUM = re.compile(r'(?<![A-Za-z0-9_.^])-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![A-Za-z0-9])')
# A block "uses a real API" if it imports from the project's simulations package
# (e.g. `from simulations.common.isf_utils import ...`). Such a block with NO
# `# ->` expected number is unchecked: a silently-broken call (wrong kwargs,
# missing args) would never be caught — exactly how the old
# accumulated_jitter_curve example hid its breakage.
IMPORTS_API = re.compile(r'^\s*(?:from|import)\s+simulations\b', re.M)


def _f(t):
    try:
        v=float(t)
        return None if (abs(v)<1e-30 and v!=0) else v
    except ValueError:
        return None


def nums(s):
    out = []
    for tok in NUM.findall(s):
        try:
            v = float(tok)
            if abs(v) < 1e-30 and v != 0:
                continue
            out.append(v)
        except ValueError:
            pass
    return out


def close(a, b, rel=0.05, absol=1e-12):
    if a == b:
        return True
    if abs(a - b) <= absol:
        return True
    denom = max(abs(a), abs(b))
    return denom > 0 and abs(a - b) / denom <= rel


def python_blocks(text):
    return re.findall(r'```python\n(.*?)```', text, re.S)


def _answer_prefix(s):
    """Marker convention is ``# -> <answer> [explanation]``. Keep only the answer
    part: stop at the first '(' / '（' or CJK character, so numbers living inside
    an explanatory parenthetical or comment (e.g. the "2" in "2*Gamma_rms^2", or
    "遠小於 447.9 fs") are NOT mistaken for expected outputs."""
    out = []
    for ch in s:
        if ch in '(（《「' or '一' <= ch <= '鿿':
            break
        out.append(ch)
    return ''.join(out)


def expected_from(code):
    exp = []
    for m in re.finditer(r'#\s*->\s*(.*)', code):
        prefix = _answer_prefix(m.group(1))
        ns = [float(t) for t in EXP_NUM.findall(prefix) if _f(t) is not None]
        if ns:
            exp.append((m.group(1).strip(), ns))
    return exp


def uses_api(code):
    return bool(IMPORTS_API.search(code))


def run_block(code):
    with tempfile.NamedTemporaryFile("w", suffix=".py", dir=ROOT, delete=False) as f:
        f.write(code)
        path = f.name
    try:
        env = dict(os.environ, PYTHONPATH=ROOT)
        p = subprocess.run([sys.executable, path], cwd=ROOT, env=env,
                           capture_output=True, text=True, timeout=120)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    finally:
        os.unlink(path)


def main():
    verbose = "--verbose" in sys.argv
    pages = sorted(glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True) +
                   glob.glob(os.path.join(ROOT, "docs", "**", "*.mdx"), recursive=True))
    total = passed = mismatch = errored = needs_ctx = 0
    fails = []
    unchecked_api = []  # (rel, block#) — imports a real API but has no `# ->`
    for p in pages:
        rel = os.path.relpath(p, ROOT)
        text = open(p, encoding="utf-8").read()
        for i, code in enumerate(python_blocks(text)):
            exp = expected_from(code)
            if not exp:
                # No expected number: if it nonetheless imports a real API
                # (simulations.*), flag it as unchecked so a silently-broken
                # call can't hide here.
                if uses_api(code):
                    unchecked_api.append((rel, i + 1))
                continue
            total += 1
            rc, out, err = run_block(code)
            if rc != 0:
                # distinguish "uses undefined name from previous block" from real error
                if re.search(r"NameError|is not defined", err):
                    needs_ctx += 1
                    if verbose:
                        print(f"  [ctx ] {rel} block#{i+1}: not self-contained ({err.strip().splitlines()[-1][:70]})")
                else:
                    errored += 1
                    fails.append((rel, i + 1, "ERROR", err.strip().splitlines()[-1][:120] if err.strip() else "rc!=0"))
                continue
            got = nums(out)
            ok = True
            missing = []
            for raw, ens in exp:
                for e in ens:
                    if not any(close(e, g) for g in got):
                        ok = False
                        missing.append(e)
            if ok:
                passed += 1
            else:
                mismatch += 1
                fails.append((rel, i + 1, "MISMATCH",
                              f"expected {missing} not in output {got[:8]}"))

    print("=" * 70)
    print("Example answer verification")
    print("=" * 70)
    print(f"checkable blocks (with '# ->' numbers): {total}")
    print(f"  PASSED (numbers match)   : {passed}")
    print(f"  MISMATCH (wrong number)  : {mismatch}")
    print(f"  ERROR (real failure)     : {errored}")
    print(f"  not self-contained (ctx) : {needs_ctx}")
    print(f"unchecked-but-uses-API blocks : {len(unchecked_api)}")
    if fails:
        print("\n-- FAILURES --")
        for rel, b, kind, detail in fails:
            print(f"  [{kind}] {rel} block#{b}: {detail}")
    if unchecked_api:
        print("\n-- UNCHECKED-BUT-USES-API "
              "(imports simulations.* but has no '# ->' number) --")
        for rel, b in unchecked_api:
            print(f"  [unchecked] {rel} block#{b}")
    return 1 if (mismatch or errored) else 0


if __name__ == "__main__":
    sys.exit(main())
