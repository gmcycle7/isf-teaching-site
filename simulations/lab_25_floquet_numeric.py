"""
lab_25_floquet_numeric.py

Goal
----
Turn the Floquet / adjoint / PPV prose of
docs/99_appendix/derivation_floquet_ppv.md into NUMBERS on a toy oscillator:
the van der Pol oscillator (mu = 0.2, near-harmonic, unit frequency),

    x'' - mu (1 - x^2) x' + x = 0
    state s = (x, y),  x' = y,  y' = mu (1 - x^2) y - x
    Jacobian A(t) = [[0, 1], [-2 mu x y - 1, mu (1 - x^2)]]  along the cycle.

Four numeric steps (matching the page section):
  1. Find the limit cycle and its period T (settle + Poincare section x=0,
     y>0, Newton-refined crossings).  Expect T ~ 2*pi*(1 + mu^2/16).
  2. Integrate the fundamental matrix dPhi/dt = A(t) Phi over one period
     -> monodromy M = Phi(T).  Eigenvalues (Floquet multipliers):
     mu1 ~ 1.0 exactly (phase direction, lambda1 = 0) and |mu2| < 1
     (amplitude direction, lambda2 = ln(mu2)/T ~ -mu from averaging).
     Cross-check det M = exp( int_0^T tr A dt )  (Abel/Liouville).
  3. Integrate the ADJOINT system p' = -A(t)^T p BACKWARD over one period,
     starting from the left eigenvector of M with eigenvalue 1.  Backward,
     the unwanted 1/mu2 mode decays, so the periodic left vector v1(t)
     survives.  Normalize so v1(t) . xdot_s(t) = 1 for all t; the constancy
     of that inner product (adjoint invariant) is printed as a check.
  4. ISF: the component of v1 along the kicked state axis IS Gamma/q_max.
     We kick the y axis (the SAME axis lab_15_nonlinear_isf.py kicks with
     impulse_dy), so Gamma_ppv(theta)/q_max = omega0 * v1_y(theta).
     Overlay with (a) the brute-force impulse-response ISF from lab_15's
     extract_vdp_isf and (b) the harmonic-limit -sin(theta)/(omega0*A);
     print the RMS mismatches (small).

Bonus checks:
  * One adjoint solve gives the ISF for EVERY injection axis: v1_x predicts
    Gamma_x-kick ~ +cos(theta)/A without any new impulse sweep.
  * De-normalizing with q_max,toy = max|y| gives a dimensionless Gamma with
    peak ~ 1 and Gamma_rms ~ 1/sqrt(2) -- the canonical true-LC value.

All quantities are in normalized (dimensionless) units: time in units where
the harmonic-limit frequency is 1 rad/s; states dimensionless. Pedagogical
toy model, not transistor-level.

Figure
------
  static/figures/floquet_ppv_numeric.png

Run
---
    PYTHONPATH=. python simulations/lab_25_floquet_numeric.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                          # sibling lab modules
sys.path.insert(0, os.path.join(_HERE, "common"))  # shared utilities

import numpy as np

MU = 0.2  # van der Pol nonlinearity (near-harmonic)


# ---------------------------------------------------------------------------
# vdP dynamics: scalar RK4 (fast inner loops, same integrator style as lab_15)
# ---------------------------------------------------------------------------
def vdp_deriv(x, y, mu=MU):
    """State derivative of x'' - mu (1 - x^2) x' + x = 0 as (x', y')."""
    return y, mu * (1.0 - x * x) * y - x


def vdp_jacobian(x, y, mu=MU):
    """Jacobian A = d f / d s along the trajectory (2x2, units 1/s~)."""
    return np.array([[0.0, 1.0],
                     [-2.0 * mu * x * y - 1.0, mu * (1.0 - x * x)]])


def rk4_state(x, y, dt, mu=MU):
    k1x, k1y = vdp_deriv(x, y, mu)
    k2x, k2y = vdp_deriv(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, mu)
    k3x, k3y = vdp_deriv(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, mu)
    k4x, k4y = vdp_deriv(x + dt * k3x, y + dt * k3y, mu)
    return (x + dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x),
            y + dt / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y))


def _newton_to_section(x, y, dt_max=0.1):
    """Newton-refine onto the Poincare section x = 0 (x' = y != 0 there)."""
    for _ in range(20):
        if abs(x) < 1e-13:
            break
        step = -x / y                      # since dx/dt = y near the section
        step = max(-dt_max, min(dt_max, step))
        x, y = rk4_state(x, y, step)
    return x, y


# ---------------------------------------------------------------------------
# Step 1: limit cycle + period T
# ---------------------------------------------------------------------------
def find_limit_cycle(t_settle=300.0, dt=1e-3, n_periods_avg=5):
    """Settle onto the cycle, then measure T from Newton-refined rising
    zero crossings of x (Poincare section x=0, y>0).

    Returns (s0, T): s0 = (0, y0) on the section, T = period.
    """
    # -- settle: transients decay like exp(-mu t); mu*t_settle = 60 >> 1
    x, y = 2.0, 0.0
    for _ in range(int(round(t_settle / dt))):
        x, y = rk4_state(x, y, dt)
    # -- walk to the next rising zero crossing of x, then Newton-refine
    while True:
        xn, yn = rk4_state(x, y, dt)
        if x < 0.0 <= xn and yn > 0.0:
            x, y = _newton_to_section(xn, yn)
            break
        x, y = xn, yn
    s_start = (x, y)
    # -- accumulate n_periods_avg full returns to the section
    t_acc = 0.0
    crossings = 0
    while crossings < n_periods_avg:
        xn, yn = rk4_state(x, y, dt)
        t_acc += dt
        if x < 0.0 <= xn and yn > 0.0:
            crossings += 1
        x, y = xn, yn
    # Newton back onto the section (state is one grid step past crossing #n)
    for _ in range(20):
        if abs(x) < 1e-13:
            break
        step = -x / y
        x, y = rk4_state(x, y, step)
        t_acc += step
    T = t_acc / n_periods_avg
    s0 = (x, y)          # most-settled section point: x ~ 0, y = y0 > 0
    return s0, T


# ---------------------------------------------------------------------------
# Step 2: fundamental matrix -> monodromy M
# ---------------------------------------------------------------------------
def monodromy(s0, T, nf=12000, mu=MU):
    """Integrate the augmented system (state s, fundamental matrix Phi):

        s'   = f(s),   Phi' = A(s(t)) Phi,   Phi(0) = I

    with RK4 over one period.  Returns (M, states, hf) where
    M = Phi(T) is the monodromy matrix and states[k] is s(k*hf), hf = T/nf.
    """
    hf = T / nf

    def aug(s, P):
        x, y = s
        fx = np.array(vdp_deriv(x, y, mu))
        return fx, vdp_jacobian(x, y, mu) @ P

    s = np.array(s0, dtype=float)
    P = np.eye(2)
    states = np.empty((nf + 1, 2))
    states[0] = s
    for k in range(nf):
        k1s, k1P = aug(s, P)
        k2s, k2P = aug(s + 0.5 * hf * k1s, P + 0.5 * hf * k1P)
        k3s, k3P = aug(s + 0.5 * hf * k2s, P + 0.5 * hf * k2P)
        k4s, k4P = aug(s + hf * k3s, P + hf * k3P)
        s = s + hf / 6.0 * (k1s + 2 * k2s + 2 * k3s + k4s)
        P = P + hf / 6.0 * (k1P + 2 * k2P + 2 * k3P + k4P)
        states[k + 1] = s
    return P, states, hf


# ---------------------------------------------------------------------------
# Step 3: adjoint backward -> periodic left vector v1(t) (the PPV)
# ---------------------------------------------------------------------------
def adjoint_ppv(M, states, T, mu=MU):
    """Integrate p' = -A(t)^T p BACKWARD from t=T to t=0 with RK4 on a grid
    of nc = nf/2 steps (stage values of A taken from the stored fine states).
    Start from the left eigenvector of M with eigenvalue ~ 1, so p(t) is the
    periodic Floquet left vector; backward integration is self-correcting
    because the unwanted adjoint mode (multiplier 1/mu2 > 1) decays backward.

    Normalize so v1(t) . xdot_s(t) = 1 for all t.

    Returns (theta, v1, const_err, per_err):
      theta[j] = omega0 * t_j in [0, 2*pi];  v1[j] = v1(t_j)  (nc+1 rows);
      const_err = max_t | p.xdot_s / mean - 1 |  BEFORE normalization
                  (the adjoint invariant -- should be ~ machine level);
      per_err   = |p(0) - p(T)| / |p(T)|  (periodicity of the left vector).
    """
    nf = len(states) - 1
    nc = nf // 2
    h = T / nc

    # left eigenvector of M for the multiplier closest to 1:  M^T v = v
    w, V = np.linalg.eig(M.T)
    i1 = int(np.argmin(np.abs(w - 1.0)))
    p = np.real(V[:, i1]).astype(float)
    p_end = p.copy()

    ps = np.empty((nc + 1, 2))
    ps[nc] = p
    for j in range(nc, 0, -1):
        A0 = vdp_jacobian(*states[2 * j], mu)       # t_j
        Am = vdp_jacobian(*states[2 * j - 1], mu)   # t_j - h/2
        A1 = vdp_jacobian(*states[2 * j - 2], mu)   # t_j - h
        k1 = -A0.T @ p
        k2 = -Am.T @ (p - 0.5 * h * k1)
        k3 = -Am.T @ (p - 0.5 * h * k2)
        k4 = -A1.T @ (p - h * k3)
        p = p - h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        ps[j - 1] = p
    per_err = float(np.linalg.norm(ps[0] - p_end) / np.linalg.norm(p_end))

    # adjoint invariant: c(t) = p(t) . xdot_s(t) must be CONSTANT in t
    xdot = np.array([vdp_deriv(*states[2 * j], mu) for j in range(nc + 1)])
    c = np.einsum("ij,ij->i", ps, xdot)
    c_mean = float(np.mean(c))
    const_err = float(np.max(np.abs(c / c_mean - 1.0)))
    v1 = ps / c_mean                     # now v1 . xdot_s = 1 for all t
    theta = np.linspace(0.0, 2.0 * np.pi, nc + 1)
    return theta, v1, const_err, per_err


def ppv_pipeline(nf=12000, mu=MU):
    """Steps 1-3 in one call. Returns a dict with everything the page uses."""
    s0, T = find_limit_cycle()
    omega0 = 2.0 * np.pi / T
    M, states, hf = monodromy(s0, T, nf=nf, mu=mu)
    mults = np.sort(np.linalg.eigvals(M).real)[::-1]   # real for this toy
    theta, v1, const_err, per_err = adjoint_ppv(M, states, T, mu=mu)
    amp_x = float(np.max(np.abs(states[:, 0])))        # amplitude of x
    qmax_toy = float(np.max(np.abs(states[:, 1])))     # swing of kicked state y
    # Liouville / Abel cross-check: det M = exp( int tr A dt )
    tr = mu * (1.0 - states[:, 0] ** 2)                # tr A = mu (1 - x^2)
    detM_liouville = float(np.exp(np.trapezoid(tr, dx=hf)))
    return dict(s0=s0, T=T, omega0=omega0, M=M, mults=mults, states=states,
                theta=theta, v1=v1, const_err=const_err, per_err=per_err,
                amp_x=amp_x, qmax_toy=qmax_toy, detM_liouville=detM_liouville)


# ---------------------------------------------------------------------------
# Brute-force impulse ISF on EITHER state axis (lab_15's method, but starting
# from the converged section state s0 so reference crossings need no settle)
# ---------------------------------------------------------------------------
def extract_isf_impulse_axis(s0, T, axis=1, n_points=18, dq=0.02, dt=2.5e-3):
    """Kick state axis `axis` (0=x, 1=y) with a small impulse dq at n_points
    phases; measure the persistent shift of a late rising zero crossing of x
    against an unkicked reference run (same integrator, same dt, so the
    integrator's own period bias cancels).  Gamma/q_max = -w0*dt_shift/dq,
    exactly the lab_15 sign convention."""
    w0 = 2.0 * np.pi / T
    t_late, t_end = 12.0 * T, 15.0 * T
    n = int(round(t_end / dt))

    def run(k_inj=-1):
        x, y = s0
        xs = np.empty(n + 1)
        xs[0] = x
        for k in range(n):
            if k == k_inj:
                if axis == 0:
                    x += dq
                else:
                    y += dq
            x, y = rk4_state(x, y, dt)
            xs[k + 1] = x
        return xs

    def first_late_zc(xs):
        neg = xs < 0
        idx = np.where(neg[:-1] & ~neg[1:])[0]     # rising (- to +) crossings
        for i in idx:
            tc = i * dt + dt * (0.0 - xs[i]) / (xs[i + 1] - xs[i])
            if tc > t_late:
                return tc
        raise RuntimeError("no late zero crossing found")

    z_ref = first_late_zc(run())
    thetas = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    isf = np.empty(n_points)
    for i, th in enumerate(thetas):
        t_inj = T + (th / (2.0 * np.pi)) * T       # one full period in, phase th
        z_p = first_late_zc(run(int(round(t_inj / dt))))
        dt_shift = (z_p - z_ref + T / 2.0) % T - T / 2.0   # wrap to [-T/2, T/2]
        isf[i] = -w0 * dt_shift / dq
    return thetas, isf


# ---------------------------------------------------------------------------
# Step 4 helper: PPV-based ISF on the lab_15 kick axis (y)
# ---------------------------------------------------------------------------
def ppv_isf(res=None):
    """Gamma/q_max from the PPV:  omega0 * v1_y(theta)  (rad per unit kick
    on the y axis -- the same axis lab_15's impulse_dy kicks).
    Returns (theta, gamma_over_qmax, res)."""
    if res is None:
        res = ppv_pipeline()
    return res["theta"], res["omega0"] * res["v1"][:, 1], res


def main():
    import matplotlib.pyplot as plt
    from plot_utils import savefig
    from isf_utils import gamma_rms
    from lab_15_nonlinear_isf import extract_vdp_isf  # brute-force reference

    print("[lab_25] Floquet / monodromy / adjoint PPV on van der Pol "
          f"(mu={MU}) ...")

    # ---- Step 1: limit cycle + period ------------------------------------
    res = ppv_pipeline()
    T, omega0 = res["T"], res["omega0"]
    print("T       =", round(T, 4))        # -> 6.2989 (2*pi*(1+mu^2/16)=6.2989)
    print("omega0  =", round(omega0, 4))   # -> 0.9975 (1 - mu^2/16 = 0.9975)
    closure = float(np.linalg.norm(res["states"][-1] - res["states"][0]))
    print("cycle closure |s(T)-s(0)| =", "{:.1e}".format(closure))

    # ---- Step 2: monodromy + Floquet multipliers -------------------------
    mu1, mu2 = res["mults"]
    print("mu1     =", round(float(mu1), 6))   # -> 1.0 (phase direction)
    print("mu2     =", round(float(mu2), 4))   # -> 0.2828 (amplitude, |mu2|<1)
    print("lambda1 =", "{:.1e}".format(np.log(mu1) / T), "1/s~")
    print("lambda2 =", round(float(np.log(mu2) / T), 4))  # -> -0.2005 (~ -mu)
    print("det M   =", round(float(mu1 * mu2), 6),
          "; Liouville exp(int trA dt) =", round(res["detM_liouville"], 6))

    # ---- Step 3: adjoint backward -> v1(t), normalization constancy ------
    print("adjoint periodicity |p(0)-p(T)|/|p(T)| =",
          "{:.1e}".format(res["per_err"]))
    print("normalization constancy max|v1.xdot_s - 1| =",
          "{:.1e}".format(res["const_err"]))

    # ---- Step 4: ISF overlay ---------------------------------------------
    theta, g_ppv, _ = ppv_isf(res)          # Gamma/q_max, y-axis kick
    g_ppv_x = omega0 * res["v1"][:, 0]      # bonus: x-axis kick, no re-sweep
    amp, qmax_toy = res["amp_x"], res["qmax_toy"]

    print("A (max|x|) =", round(amp, 4))   # -> 2.0004 (harmonic limit 2)
    print("peak |Gamma_ppv/qmax| =", round(float(np.max(np.abs(g_ppv))), 4))
    # -> 0.5011 (harmonic limit 1/(omega0*A) = 0.5011)
    print("q_max,toy = max|y| =", round(qmax_toy, 4))   # -> 2.0442

    # de-normalized Gamma = q_max * (Gamma/q_max): true-LC canonical checks
    g_dimless = qmax_toy * g_ppv
    print("Gamma_rms (dimensionless) =",
          round(float(gamma_rms(theta, g_dimless)), 4))
    # -> 0.7258 (near-harmonic: close to true-LC 1/sqrt(2)=0.7071, +2.6%)

    # brute-force impulse ISF, lab_15 method (36 phases, dq=0.02 on y)
    th15, isf15, T15 = extract_vdp_isf(MU)
    print("lab_15 T =", round(T15, 4))      # -> 6.2989 (same cycle)
    g_on_15 = np.interp(th15, theta, g_ppv)
    rms_imp = float(np.sqrt(np.mean((g_on_15 - isf15) ** 2)))
    print("rms mismatch PPV vs impulse (raw) =", round(rms_imp, 4))
    # -> 0.0016 (small: adjoint and brute force agree)

    # harmonic-limit reference -sin(theta): compare normalized shapes
    g_norm = g_ppv / np.max(np.abs(g_ppv))
    rms_sin = float(np.sqrt(np.mean((g_norm - (-np.sin(theta))) ** 2)))
    print("rms mismatch PPV vs -sin(theta) (normalized) =", round(rms_sin, 4))
    # -> 0.0555 (small: O(mu) waveform distortion away from pure -sin)

    # bonus: the SAME v1 predicts the ISF of the OTHER axis (kick on x),
    # with no new adjoint solve -- verify by a fresh impulse sweep on x
    thx, isfx = extract_isf_impulse_axis(res["s0"], T, axis=0)
    rms_x = float(np.sqrt(np.mean((np.interp(thx, theta, g_ppv_x)
                                   - isfx) ** 2)))
    print("rms mismatch PPV vs impulse on x-axis =", round(rms_x, 4))
    # -> 0.0023 (one adjoint solve covers every injection axis)

    # ---- figure -----------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.6))

    # (a) limit cycle + tangent (u1) arrows + transient
    ax = axes[0]
    xt, yt = 0.2, 0.0
    tr_x, tr_y = [xt], [yt]
    for _ in range(int(60.0 / 2e-3)):
        xt, yt = rk4_state(xt, yt, 2e-3)
        tr_x.append(xt); tr_y.append(yt)
    ax.plot(tr_x, tr_y, color="0.75", lw=0.8, label="暫態（被吸進 limit cycle）")
    st = res["states"]
    ax.plot(st[:, 0], st[:, 1], color="tab:blue", lw=2.2,
            label="limit cycle $x_s(t)$")
    for j in np.linspace(0, len(st) - 1, 8, dtype=int)[:-1]:
        fx, fy = vdp_deriv(st[j, 0], st[j, 1])
        nrm = np.hypot(fx, fy)
        ax.annotate("", xy=(st[j, 0] + 0.45 * fx / nrm,
                            st[j, 1] + 0.45 * fy / nrm),
                    xytext=(st[j, 0], st[j, 1]),
                    arrowprops=dict(arrowstyle="->", color="tab:red", lw=1.4))
    ax.plot([], [], color="tab:red", lw=1.4,
            label=r"切向 $\dot{x}_s\ (\lambda_1=0)$")
    ax.set_xlabel("$x$（無因次）"); ax.set_ylabel(r"$y=\dot{x}$（無因次）")
    ax.set_title(f"(a) van der Pol μ={MU}：limit cycle\n"
                 f"T={T:.4f}, μ₁={mu1:.6f}, μ₂={mu2:.4f}")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_aspect("equal", adjustable="datalim")

    # (b) periodic left vector v1(theta): both components + harmonic refs
    ax = axes[1]
    frac = theta / (2 * np.pi)
    ax.plot(frac, omega0 * res["v1"][:, 1], color="tab:blue",
            label=r"$\omega_0 v_{1,y}$（踢 $y$ 軸的 $\Gamma/q_{max}$）")
    ax.plot(frac, g_ppv_x, color="tab:orange",
            label=r"$\omega_0 v_{1,x}$（踢 $x$ 軸的 $\Gamma/q_{max}$）")
    ax.plot(thx / (2 * np.pi), isfx, "s", ms=4, color="tab:orange", mfc="none",
            label=r"打脈衝實測（踢 $x$ 軸）")
    ax.plot(frac, -np.sin(theta) / (omega0 * amp), "k--", lw=1.1,
            label=r"諧波極限 $-\sin\theta/(\omega_0 A)$")
    ax.plot(frac, np.cos(theta) / amp, "k:", lw=1.1,
            label=r"諧波極限 $+\cos\theta/A$")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"$\theta/2\pi$（自 $x$ 上升零交越起算）")
    ax.set_ylabel(r"$\Gamma/q_{max}$（rad／單位 $\Delta q$，正規化）")
    ax.set_title("(b) 一次 adjoint 解 → 每個注入軸的 ISF\n"
                 f"歸一化恆定誤差 {res['const_err']:.1e}，"
                 f"x 軸 rms 差 {rms_x:.4f}")
    ax.legend(fontsize=7.5)

    # (c) the punchline overlay: PPV vs impulse vs -sin
    ax = axes[2]
    ax.plot(frac, g_ppv, color="tab:blue", lw=2.0,
            label=r"PPV：$\omega_0 v_{1,y}(\theta)$（adjoint 一次解）")
    good = np.isfinite(isf15)
    ax.plot(th15[good] / (2 * np.pi), isf15[good], "o", ms=4.5,
            color="tab:red", mfc="none",
            label="打脈衝法（lab_15，36 個相位）")
    ax.plot(frac, -np.sin(theta) / (omega0 * amp), "k--", lw=1.1,
            label=r"$-\sin\theta/(\omega_0 A)$")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"注入相位 $\theta/2\pi$（自 $x$ 上升零交越起算）")
    ax.set_ylabel(r"$\Gamma/q_{max}$（rad／單位 $\Delta q$，正規化）")
    ax.set_title("(c) PPV = ISF：兩種方法疊在一起\n"
                 f"rms 差 {rms_imp:.4f}（vs 脈衝）,"
                 f" {rms_sin:.4f}（vs $-\\sin$, 歸一）")
    ax.legend(fontsize=8, loc="upper right")

    savefig(fig, "floquet_ppv_numeric.png")


if __name__ == "__main__":
    main()
