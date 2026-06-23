"""
lab_12_serdes_eye_ber.py

Goal
----
Make the oscillator -> SerDes link explicit: an rms timing jitter sigma_t (which
came from integrating the clock's phase noise) closes the data eye and sets the
bit-error rate. Plot the eye diagram and the BER "bathtub".

Model
-----
  10 Gb/s NRZ (UI = 100 ps). Sampling clock has random jitter sigma_t.
  BER(t) = 1/2[Q((UI/2 - t)/sigma_t) + Q((UI/2 + t)/sigma_t)]  (RJ only).

Figure
------
  static/figures/serdes_eye_ber_bathtub.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from serdes_utils import eye_traces, ber_bathtub
from plot_utils import savefig

RNG = np.random.default_rng(12)


def main():
    print("[lab_12] SerDes eye diagram + BER bathtub ...")
    ui = 100e-12       # 10 Gb/s -> 100 ps UI
    sigma_t = 4e-12    # 4 ps rms RJ (e.g. from an integrated 5 GHz clock)

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8))

    # (a) eye diagram
    ax = axes[0]
    t, traces = eye_traces(sigma_t, ui, n_traces=300, rng=RNG)
    for tr in traces:
        ax.plot(t, tr, color="tab:blue", alpha=0.05, lw=1.0)
    ax.set_xlabel("time [UI]")
    ax.set_ylabel("amplitude")
    ax.set_title(fr"(a) Eye diagram，RJ $\sigma_t$={sigma_t*1e12:.0f} ps，UI={ui*1e12:.0f} ps")
    ax.set_xlim(-1, 1)

    # (b) BER bathtub
    ax = axes[1]
    toff = np.linspace(-ui / 2 * 0.98, ui / 2 * 0.98, 400)
    for st, c in zip([2e-12, 4e-12, 8e-12], ["tab:green", "tab:orange", "tab:red"]):
        ber = ber_bathtub(toff, st, ui)
        ax.semilogy(toff / ui, ber, color=c, label=fr"$\sigma_t$={st*1e12:.0f} ps")
    ax.axhline(1e-12, color="gray", ls="--", lw=1, label="BER = $10^{-12}$")
    ax.set_xlabel("sampling offset [UI]")
    ax.set_ylabel("BER")
    ax.set_title("(b) BER bathtub：jitter 越大，可用取樣窗（eye）越窄")
    ax.set_ylim(1e-18, 1)
    ax.legend(fontsize=8)
    savefig(fig, "serdes_eye_ber_bathtub.png")


if __name__ == "__main__":
    main()
