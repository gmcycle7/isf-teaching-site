#!/usr/bin/env python3
"""
run_all_sims.py — run every simulation lab and regenerate all figures.

Usage:
    python scripts/run_all_sims.py

Each lab script is executed in its own subprocess so a failure in one does not
abort the rest. A summary table is printed at the end, and the contents of
static/figures/ are listed.
"""
import os
import subprocess
import sys
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
SIM_DIR = os.path.join(PROJECT_ROOT, "simulations")
FIG_DIR = os.path.join(PROJECT_ROOT, "static", "figures")


def main():
    scripts = sorted(glob.glob(os.path.join(SIM_DIR, "lab_*.py")) +
                     glob.glob(os.path.join(SIM_DIR, "fig_*.py")))
    if not scripts:
        print("No lab scripts found in", SIM_DIR)
        return 1

    print("=" * 70)
    print("Running ISF simulation labs")
    print("=" * 70)

    results = []
    for s in scripts:
        name = os.path.basename(s)
        print(f"\n>>> {name}")
        proc = subprocess.run([sys.executable, s], capture_output=True, text=True)
        ok = proc.returncode == 0
        if proc.stdout:
            print(proc.stdout.rstrip())
        if not ok:
            print("    !!! FAILED !!!")
            print(proc.stderr.rstrip())
        results.append((name, ok))

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    n_ok = 0
    for name, ok in results:
        status = "OK  " if ok else "FAIL"
        if ok:
            n_ok += 1
        print(f"  [{status}] {name}")
    print(f"\n  {n_ok}/{len(results)} labs succeeded")

    figs = sorted(glob.glob(os.path.join(FIG_DIR, "*.png")))
    print(f"\n  {len(figs)} figures in static/figures/:")
    for f in figs:
        print("    -", os.path.basename(f))

    return 0 if n_ok == len(results) else 2


if __name__ == "__main__":
    sys.exit(main())
