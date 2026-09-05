"""Binary Ramsey-like qubit readout driven by dipolar shift/dephasing."""
from __future__ import annotations
import numpy as np
from ..transduction.dipolar import DipolarMagneticModel

def make_binary_probability_model(*, model: DipolarMagneticModel, t_int_s: float, readout_reference_rad_s: float = 0.0):
    if t_int_s <= 0:
        raise ValueError("t_int_s must be positive")
    def probabilities(theta):
        ln_c, ln_kd, ln_g, gamma0, eta = map(float, theta)
        if gamma0 < 0 or not (0 < eta < 1):
            raise ValueError("Require Gamma_0 >= 0 and 0 < eta < 1")
        q = model.parameters(ln_c, ln_kd, ln_g, gamma0)
        phase = (q["delta_omega_rad_s"] - readout_reference_rad_s) * t_int_s
        coherence = np.exp(-q["Gamma_phi_s"] * t_int_s) * np.cos(phase)
        p_ideal = 0.5 * (1.0 + coherence)
        p1 = eta*p_ideal + (1.0-eta)*0.5
        p1 = float(np.clip(p1, 1e-15, 1-1e-15))
        return np.array([1.0-p1, p1])
    return probabilities
