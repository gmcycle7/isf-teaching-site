"""
lab_15_nonlinear_isf.py

Goal
----
The ISF is NOT always -sin(theta): it is set by the oscillator's large-signal
waveform. For a near-harmonic oscillator (small nonlinearity) the ISF is close
to a sinusoid; for a strongly nonlinear (relaxation) oscillator the waveform
distorts and so does the ISF. We use the van der Pol oscillator:

    x'' - mu (1 - x^2) x' + x = 0     (state: dx/dt = y, dy/dt = mu(1-x^2)y - x)

small mu  -> near-sinusoidal,   large mu -> relaxation (sharp transitions).

We extract the ISF numerically by injecting a small impulse on the velocity
state at many phases and measuring the persistent time-shift of the steady
state (Delta phi = -omega0 * Delta t).

Figure
------
  static/figures/nonlinear_oscillator_isf.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from plot_utils import savefig


def simulate_vdp(mu, t_end, fs, x0=2.0, y0=0.0, impulse_time=None, impulse_dy=0.0):
    dt = 1.0 / fs
    n = int(round(t_end * fs))
    x = np.empty(n); y = np.empty(n)
    xi, yi = float(x0), float(y0)
    imp = int(round(impulse_time * fs)) if impulse_time is not None else -1

    def deriv(xx, yy):
        return yy, mu * (1 - xx * xx) * yy - xx

    for k in range(n):
        x[k] = xi; y[k] = yi
        if k == imp:
            yi += impulse_dy
        k1x, k1y = deriv(xi, yi)
        k2x, k2y = deriv(xi + 0.5 * dt * k1x, yi + 0.5 * dt * k1y)
        k3x, k3y = deriv(xi + 0.5 * dt * k2x, yi + 0.5 * dt * k2y)
        k4x, k4y = deriv(xi + dt * k3x, yi + dt * k3y)
        xi += dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        yi += dt / 6 * (k1y + 2 * k2y + 2 * k3y + k4y)
    t = np.arange(n) * dt
    return t, x, y


def rising_zero_crossings(t, x):
    s = x < 0
    idx = np.where(s[:-1] & ~s[1:])[0]  # - to + crossings
    out = []
    for i in idx:
        x0, x1 = x[i], x[i + 1]
        out.append(t[i] + (t[i + 1] - t[i]) * (0 - x0) / (x1 - x0))
    return np.array(out)


def measure_period(mu, fs, t_end, t_settle):
    t, x, y = simulate_vdp(mu, t_end, fs)
    zc = rising_zero_crossings(t, x)
    zc = zc[zc > t_settle]
    return float(np.median(np.diff(zc))), zc[0]


def extract_vdp_isf(mu, fs=400.0, n_points=36, dq=0.02):
    # 1) estimate period and a settle time scaled to it
    T, _ = measure_period(mu, fs, t_end=220.0, t_settle=80.0)
    t_settle = max(60.0, 10 * T)
    t_late = t_settle + 6 * T
    t_end = t_late + 4 * T              # generous tail
    w0 = 2 * np.pi / T

    # reference run
    t_ref, xr, yr = simulate_vdp(mu, t_end, fs)
    zr = rising_zero_crossings(t_ref, xr)
    t0 = zr[zr > t_settle][0]
    zr_late = zr[zr > t_late]
    if len(zr_late) == 0:
        raise RuntimeError("reference late crossing not found")
    zr_late = zr_late[0]

    thetas = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
    isf = np.zeros(n_points)
    for i, th in enumerate(thetas):
        t_inj = t0 + (th / (2 * np.pi)) * T + T  # one period after t0, at phase th
        t_p, xp, yp = simulate_vdp(mu, t_end, fs, impulse_time=t_inj, impulse_dy=dq)
        zp = rising_zero_crossings(t_p, xp)
        zp = zp[zp > t_late]
        if len(zp) == 0:
            isf[i] = np.nan; continue
        dt_shift = (zp[0] - zr_late + T / 2) % T - T / 2   # wrap to [-T/2, T/2]
        isf[i] = -w0 * dt_shift / dq
    return thetas, isf, T


def main():
    print("[lab_15] nonlinear (van der Pol) ISF extraction ...")
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8))

    # (a) waveforms over one period
    ax = axes[0]
    for mu, c in zip([0.1, 1.0, 3.0], ["tab:blue", "tab:orange", "tab:red"]):
        t, x, y = simulate_vdp(mu, 120.0, 400.0)
        zc = rising_zero_crossings(t, x); zc = zc[zc > 60]
        T = np.median(np.diff(zc)); t0 = zc[0]
        m = (t >= t0) & (t <= t0 + T)
        ax.plot((t[m] - t0) / T, x[m], color=c, label=fr"$\mu$={mu}")
    ax.set_xlabel("phase within one period")
    ax.set_ylabel("$x(t)$")
    ax.set_title("(a) van der Pol 波形：μ 越大越偏離正弦（relaxation）")
    ax.legend(fontsize=8)

    # (b) extracted ISFs
    ax = axes[1]
    for mu, c in zip([0.1, 3.0], ["tab:blue", "tab:red"]):
        th, isf, T = extract_vdp_isf(mu)
        good = np.isfinite(isf)
        isf = isf / np.nanmax(np.abs(isf))
        if mu == 0.1:
            # self-check for the "small mu -> -sin" claim: the normalized ISF
            # of a near-harmonic oscillator should track -sin(theta).
            ref = -np.sin(th)
            err = float(np.sqrt(np.nanmean((isf[good] - ref[good]) ** 2)))
            print("rms_err vs -sin:", round(err, 3))  # -> < 0.1
        ax.plot(th[good] / (2 * np.pi), isf[good], "o-", ms=3, color=c,
                label=fr"extracted ISF, $\mu$={mu}")
    xg = np.linspace(0, 1, 200)
    ax.plot(xg, np.sin(2 * np.pi * xg), "k--", lw=1, label=r"sinusoid 參考")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel("injection phase")
    ax.set_ylabel("normalized ISF")
    ax.set_title("(b) ISF 隨大訊號波形改變：大 μ 明顯非正弦")
    ax.legend(fontsize=8)
    savefig(fig, "nonlinear_oscillator_isf.png")


if __name__ == "__main__":
    main()
