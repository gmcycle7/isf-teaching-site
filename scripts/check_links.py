#!/usr/bin/env python3
"""check_links.py — check all EXTERNAL links in docs/ (HEAD, then GET fallback).

Network-dependent, so this is a standalone opt-in tool (not part of the build gate).
Usage: python scripts/check_links.py [--timeout 10]
"""
import glob, os, re, ssl, sys, urllib.request
try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _CTX = ssl.create_default_context()

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TIMEOUT = float(sys.argv[sys.argv.index("--timeout") + 1]) if "--timeout" in sys.argv else 10.0
URL = re.compile(r'https?://[^\s\)\]\}>"\'`）】」]+')

def check(url):
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "Mozilla/5.0 (link-checker)"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=_CTX) as r:
            return r.status
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 429):   # HEAD-hostile hosts: try GET
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=TIMEOUT, context=_CTX) as r:
                    return r.status
            except Exception as e2:
                return f"GET-fail: {e2}"
        return e.code
    except Exception as e:
        return f"fail: {e}"

def main():
    urls = {}
    for p in glob.glob(os.path.join(ROOT, "docs", "**", "*.md*"), recursive=True):
        for u in URL.findall(open(p, encoding="utf-8").read()):
            u = u.rstrip('.,;:')
            if 'localhost' in u or '127.0.0.1' in u:
                continue
            urls.setdefault(u, []).append(os.path.relpath(p, ROOT))
    print(f"checking {len(urls)} unique external links ...")
    bad = []
    for i, (u, pages) in enumerate(sorted(urls.items())):
        st = check(u)
        ok = isinstance(st, int) and st < 400
        if not ok:
            bad.append((u, st, pages[0]))
            print(f"  [BAD {st}] {u}   (e.g. {pages[0]})")
    print(f"\n{len(urls) - len(bad)}/{len(urls)} OK, {len(bad)} bad")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
