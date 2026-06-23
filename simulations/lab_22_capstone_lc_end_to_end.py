"""
lab_22_capstone_lc_end_to_end.py

Goal
----
Thread the whole ISF phase-noise main spine in ONE pass for the ideal LC,
reusing the EXISTING common utilities (no re-implemented physics):

    Gamma(theta) = -sin(theta)        [isf_utils.gamma_lc_ideal]
      -> Gamma_rms = 1/sqrt(2)        [isf_utils.gamma_rms]
      -> S_phi(f) = Gamma_rms^2/q_max^2 * S_i/(2 pi f)^2     (1/f^2 skirt)
      -> Lorentzian D = Gamma_rms^2/(2 q_max^2) * S_i,  Df_3dB = D/pi
      -> sigma_t  = integrate L(f) over a band   [noise_utils.integrate_rms_jitter]
      -> BER bathtub                              [serdes_utils.ber_bathtub]

This is the executable companion to
docs/03_isf_core_theory/capstone_lc_end_to_end.md. Every printed intermediate
carries a checkable `# -> expected value` comment so scripts/verify_examples.py
covers the entire chain when the same snippet is embedded in the doc.

Canonical numbers (AUTHORING_SPEC sec. 8 / 11.2):
    q_max = 1 pC,  S_i = 1e-24 A^2/Hz,  f0 = 5 GHz,  Gamma_rms^2 = 0.5 (true LC).

Convention note (factor of 2): we use the clean time-domain phase PSD
    S_phi = Gamma_rms^2/q_max^2 * S_i/(2 pi f)^2,   L(f) ~= 0.5 * S_phi,
matching capstone station 5's S_phi form and station 6's Lorentzian D. The
jitter integration in station 7 is driven, as in the doc, by the canonical
"datasheet" anchor L(1 MHz) = -100 dBc/Hz (1/f^2), so sigma_t = 447.9 fs.

Run
---
    PYTHONPATH=. python simulations/lab_22_capstone_lc_end_to_end.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np

from isf_utils import gamma_lc_ideal, gamma_rms
from noise_utils import integrate_rms_jitter, leeson_one_over_f2
from serdes_utils import ber_bathtub


def main():
    print("[lab_22] ideal-LC capstone: Gamma -> Gamma_rms -> S_phi -> "
          "Lorentzian -> sigma_t -> BER")

    # ---- canonical inputs -------------------------------------------------
    q_max = 1e-12          # node max charge swing [C]  (= 1 pC)
    S_i = 1e-24            # one-sided white current PSD [A^2/Hz]
    f0 = 5e9               # oscillation frequency [Hz] (5 GHz)

    # ---- station 3+4: Gamma(theta) = -sin(theta) -> Gamma_rms -------------
    theta = np.linspace(0.0, 2 * np.pi, 4001, endpoint=True)
    gamma = gamma_lc_ideal(theta)                 # = -sin(theta)
    Grms = gamma_rms(theta, gamma)                # = 1/sqrt(2)
    Grms2 = Grms ** 2
    print("Gamma_rms      =", round(float(Grms), 4), "   # -> 0.7071")
    print("Gamma_rms^2    =", round(float(Grms2), 4), "   # -> 0.5")

    # ---- station 5: phase PSD S_phi(f) (clean time-domain 1/f^2 skirt) ----
    # S_phi(f) = Gamma_rms^2/q_max^2 * S_i/(2 pi f)^2
    df = 1e6               # evaluate the skirt at 1 MHz offset
    S_phi_1MHz = Grms2 / q_max ** 2 * S_i / (2 * np.pi * df) ** 2
    print("S_phi(1MHz)    =", "{:.4e}".format(S_phi_1MHz),
          "rad^2/Hz   # -> 1.2665e-14")
    # corresponding SSB L(f) ~= 0.5*S_phi  (time-domain clean convention).
    # This clean /2 form sits 3 dB above the [P1] Eq.(21) /4 SSB form
    # (capstone station 5 reports -145 dBc/Hz via the /4 convention).
    L_1MHz = 10 * np.log10(0.5 * S_phi_1MHz)
    print("L(1MHz) clean  =", round(float(L_1MHz), 2),
          "dBc/Hz   # -> -141.98")

    # ---- station 6: Lorentzian diffusion D and 3-dB linewidth -------------
    # D = Gamma_rms^2/(2 q_max^2) * S_i ;  Df_3dB = D/pi
    D = Grms2 / (2 * q_max ** 2) * S_i
    df_3dB = D / np.pi
    print("D (diffusion)  =", round(float(D), 4),
          "rad^2/s   # -> 0.25")
    print("Df_3dB (FWHM)  =", round(float(df_3dB), 4),
          "Hz   # -> 0.0796")

    # ---- station 7: integrate L(f) over a band -> rms jitter --------------
    # Use the canonical datasheet anchor (example C): L(1MHz)=-100 dBc/Hz,
    # 1/f^2 skirt, integrate 1 MHz -> 100 MHz, via the SHARED integrator.
    f = np.logspace(6, 8, 20001)                  # 1 MHz .. 100 MHz
    L_band = leeson_one_over_f2(f, L_ref_dbc=-100.0, f_ref=1e6)
    sigma_t, sigma_phi = integrate_rms_jitter(f, L_band, f0=f0,
                                              fmin=1e6, fmax=100e6)
    print("sigma_phi      =", "{:.4e}".format(sigma_phi),
          "rad   # -> 1.407e-02")
    print("sigma_t        =", "{:.4e}".format(sigma_t),
          "s   # -> 4.479e-13")
    print("sigma_t [fs]   =", round(float(sigma_t * 1e15), 1),
          "fs   # -> 447.9")

    # ---- station 8: sigma_t -> BER bathtub --------------------------------
    ui = 100e-12           # 10 Gb/s -> UI = 100 ps
    # BER at the eye center (t = 0) and the floor it sets
    ber_center = float(ber_bathtub(np.array([0.0]), sigma_t, ui)[0])
    # at center: BER = Q(UI/2/sigma_t); UI/2/sigma_t = 50ps/447.9fs ~ 111.6
    # -> astronomically small; report -log10 so the chain stays checkable.
    print("UI/2 / sigma_t =", round(float((ui / 2) / sigma_t), 1),
          "   # -> 111.6")
    # RJ peak-to-peak budget for BER=1e-12: Q^-1(1e-12)~7.03, pp=2*7.03*sigma_t
    rj_pp = 2 * 7.03 * sigma_t
    eye_closure = rj_pp / ui
    print("RJ_pp [ps]     =", round(float(rj_pp * 1e12), 3),
          "ps   # -> 6.297")
    print("eye closure    =", round(float(eye_closure * 100), 2),
          "% UI   # -> 6.3")
    # sanity: center BER is effectively zero for this tiny sigma_t
    print("BER(center)    =", "{:.1e}".format(ber_center),
          "   # -> 1.0e-300")

    print("[lab_22] done: state -> ISF -> S_phi -> linewidth -> "
          "jitter -> BER, one pass.")


if __name__ == "__main__":
    main()
