"""Dipolar magnetic shift + dephasing baseline.

Effective model:
    f = C/(C+Kd)
    δω = g f
    Gamma_phi = Gamma_0 + (g^2 tau_c) f(1-f)

The second term is the standard motional-narrowing-style variance-times-
correlation-time ansatz for stochastic occupancy fluctuations.  Here g is an
angular-frequency scale (rad/s) and tau_c is fixed by the experimental model.
This is an effective baseline, not a claim about the microscopic magnetic
moment of miRNA-21.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from ..biology.miRNA21 import MiRNA21BindingModel

@dataclass(frozen=True)
class DipolarMagneticModel:
    binding: MiRNA21BindingModel = MiRNA21BindingModel()
    dipolar_correlation_time_s: float = 1e-6
    omega_sensor_rad_s: float = 2*np.pi*5e6

    def parameters(self, ln_c: float, ln_kd: float, ln_g: float, gamma0_s: float):
        if gamma0_s < 0:
            raise ValueError("Gamma_0 must be non-negative")
        c, kd, g = np.exp(ln_c), np.exp(ln_kd), np.exp(ln_g)
        f = float(self.binding.occupancy(c, kd))
        delta_omega = g * f
        gamma_dip = (g*g) * self.dipolar_correlation_time_s * f * (1.0-f)
        gamma_phi = gamma0_s + gamma_dip
        return {"C_M": c, "Kd_M": kd, "g_rad_s": g, "bound_fraction": f,
                "delta_omega_rad_s": delta_omega, "gamma_dip_s": gamma_dip,
                "Gamma_phi_s": gamma_phi}
