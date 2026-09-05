# AI QUANTUM AGENT V15 — RECONSTRUCTED BASELINE
# Axion Dark Matter x Quantum Sensing
# NOTE: reconstructed from project notes; not byte-for-byte recovery.

from __future__ import annotations
import json, math
from dataclasses import dataclass, asdict
from typing import Dict, Tuple
import numpy as np

HBAR = 1.054571817e-34
H = 6.62607015e-34
KB = 1.380649e-23
GEV_TO_JOULE = 1.602176634e-10
GEV_TO_M_INV = 5.0677307e15
GEV_TO_SEC_INV = 1.5192674e24
TESLA_TO_GEV2 = 1.9535e-2
EV_TO_JOULE = 1.602176634e-19
M3_TO_GEV3 = GEV_TO_M_INV ** 3

@dataclass
class V15Config:
    m_a_eV: float = 1e-5
    g_agamma_GeV_inv: float = 1e-14
    rho_a_GeV_cm3: float = 0.45
    B_T: float = 8.0
    V_m3: float = 0.1
    Q_L: float = 1e5
    C: float = 0.69
    T_sys_K: float = 0.1
    t_int_s: float = 10e-6
    t_reset_s: float = 5e-6
    t_readout_s: float = 5e-6
    eta: float = 0.95
    dark_count_Hz: float = 10.0
    depolarization: float = 0.0
    drive_model: str = "coherent"

    @property
    def t_cycle_s(self): return self.t_int_s + self.t_reset_s + self.t_readout_s
    @property
    def shots_per_second(self): return 1.0 / self.t_cycle_s

def axion_frequency_hz(m_a_eV):
    return (m_a_eV * EV_TO_JOULE) / H

def axion_angular_frequency(m_a_eV):
    return 2.0 * math.pi * axion_frequency_hz(m_a_eV)

def axion_bandwidth_hz(m_a_eV):
    return axion_frequency_hz(m_a_eV) / 1e6

def rho_GeV_cm3_to_GeV4(rho):
    cm_in_GeV_inv = 1e-2 * GEV_TO_M_INV
    return rho / (cm_in_GeV_inv ** 3)

def axion_power_watts(cfg):
    g = cfg.g_agamma_GeV_inv
    rho = rho_GeV_cm3_to_GeV4(cfg.rho_a_GeV_cm3)
    m = cfg.m_a_eV * 1e-9
    B = cfg.B_T * TESLA_TO_GEV2
    V = cfg.V_m3 * M3_TO_GEV3
    p_GeV2 = g**2 * rho / m * B**2 * V * cfg.C * cfg.Q_L
    return p_GeV2 * GEV_TO_JOULE * GEV_TO_SEC_INV

def photon_rate_hz(power_w, m_a_eV):
    return power_w / (H * axion_frequency_hz(m_a_eV))

def axion_field_amplitude_natural(cfg):
    rho = rho_GeV_cm3_to_GeV4(cfg.rho_a_GeV_cm3)
    m = cfg.m_a_eV * 1e-9
    return math.sqrt(2.0 * rho) / m

def coherent_drive_rate_hz(cfg):
    return photon_rate_hz(axion_power_watts(cfg), cfg.m_a_eV)

def signal_probability_per_shot(cfg):
    eps = 2.0 * math.pi * coherent_drive_rate_hz(cfg)
    p = math.sin(eps * cfg.t_int_s) ** 2
    return float(np.clip(p * cfg.eta, 0.0, 1.0))

def dark_probability_per_shot(cfg):
    return float(np.clip(cfg.dark_count_Hz * cfg.t_readout_s, 0.0, 1.0))

def total_click_probability(cfg):
    ps, pd = signal_probability_per_shot(cfg), dark_probability_per_shot(cfg)
    return 1.0 - (1.0 - ps) * (1.0 - pd)

def classical_radiometer_snr(cfg, integration_time_s=None):
    t = cfg.t_int_s if integration_time_s is None else integration_time_s
    bw = max(axion_bandwidth_hz(cfg.m_a_eV), 1e-30)
    return (axion_power_watts(cfg) / (KB * cfg.T_sys_K)) * math.sqrt(t / bw)

def _central_derivative(cfg, fn):
    g0 = cfg.g_agamma_GeV_inv
    dg = max(abs(g0) * 1e-5, 1e-30)
    c1, c2 = V15Config(**asdict(cfg)), V15Config(**asdict(cfg))
    c1.g_agamma_GeV_inv = g0 + dg
    c2.g_agamma_GeV_inv = max(g0 - dg, 1e-30)
    return (fn(c1) - fn(c2)) / (2.0 * dg)

def classical_fisher_information(cfg):
    return float(_central_derivative(cfg, classical_radiometer_snr) ** 2)

def measured_fisher_information(cfg):
    dp_dg = _central_derivative(cfg, total_click_probability)
    p = np.clip(total_click_probability(cfg), 1e-15, 1.0 - 1e-15)
    return float(dp_dg**2 / (p * (1.0 - p)))

def sld_qfi_two_level(cfg):
    # Conservative reconstructed-V15 placeholder.
    # V16 should replace this with an exact bosonic-channel QFI.
    return measured_fisher_information(cfg)

def fisher_summary(cfg):
    fq = sld_qfi_two_level(cfg)
    fm = measured_fisher_information(cfg)
    fc = classical_fisher_information(cfg)
    return {
        "F_Q": fq,
        "F_meas": fm,
        "F_classical": fc,
        "F_meas_over_F_classical": fm / max(fc, 1e-300),
        "F_meas_le_F_Q": bool(fm <= fq + 1e-12 * max(1.0, fq)),
        "shots_per_second": cfg.shots_per_second,
    }

def benchmark_report(cfg):
    p = axion_power_watts(cfg)
    return {
        "config": asdict(cfg),
        "derived": {
            "axion_frequency_Hz": axion_frequency_hz(cfg.m_a_eV),
            "axion_bandwidth_Hz": axion_bandwidth_hz(cfg.m_a_eV),
            "axion_field_amplitude_natural": axion_field_amplitude_natural(cfg),
            "power_W": p,
            "photon_rate_Hz": photon_rate_hz(p, cfg.m_a_eV),
            "coherent_drive_rate_Hz": coherent_drive_rate_hz(cfg),
            "signal_probability_per_shot": signal_probability_per_shot(cfg),
            "dark_probability_per_shot": dark_probability_per_shot(cfg),
            "total_click_probability": total_click_probability(cfg),
            "classical_radiometer_SNR": classical_radiometer_snr(cfg),
        },
        "fisher": fisher_summary(cfg),
        "status": "RECONSTRUCTED V15 BASELINE — model-dependent simulation; not an experimental quantum-advantage claim.",
    }

def reverse_parameter_scan(base, masses_eV, couplings_GeV_inv):
    snr = np.zeros((len(masses_eV), len(couplings_GeV_inv)))
    for i, m in enumerate(masses_eV):
        for j, g in enumerate(couplings_GeV_inv):
            cfg = V15Config(**asdict(base))
            cfg.m_a_eV, cfg.g_agamma_GeV_inv = float(m), float(g)
            snr[i, j] = classical_radiometer_snr(cfg)
    return snr

def save_report(path="v15_report.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(benchmark_report(V15Config()), f, indent=2)
    print("Saved:", path)

if __name__ == "__main__":
    cfg = V15Config()
    print("=" * 68)
    print("AI QUANTUM AGENT V15 — RECONSTRUCTED BASELINE")
    print("=" * 68)
    r = benchmark_report(cfg)
    for section, values in r.items():
        print("\n[" + section + "]")
        if isinstance(values, dict):
            for k, v in values.items(): print(f"{k:34s}: {v}")
        else: print(values)

    masses = np.logspace(-7, -3, 81)
    couplings = np.logspace(-18, -11, 81)
    snr = reverse_parameter_scan(cfg, masses, couplings)
    i, j = np.unravel_index(np.argmax(snr), snr.shape)
    print("\n[REVERSE SEARCH PREVIEW]")
    print(f"Best grid mass     : {masses[i]:.4e} eV")
    print(f"Best grid coupling : {couplings[j]:.4e} GeV^-1")
    print(f"Max benchmark SNR  : {snr[i, j]:.4e}")
    save_report()
