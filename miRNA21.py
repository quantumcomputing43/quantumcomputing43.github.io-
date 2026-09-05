"""Biophysical baseline for miRNA-21 binding/occupancy.

This module deliberately separates biochemical binding from quantum transduction.
The binding law is a baseline Langmuir model; Kd and concentration are explicit
parameters so their confounding can be tested rather than hidden.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class MiRNA21BindingModel:
    """Minimal 1:1 binding model.

    Concentration and Kd are in mol/L.  C_ref is only a numerical reference
    scale for the log-parameterization and cancels from the physical occupancy.
    """
    c_ref_M: float = 5e-9
    name: str = "miRNA-21"

    def occupancy(self, concentration_M: float | np.ndarray, kd_M: float | np.ndarray) -> np.ndarray:
        c = np.asarray(concentration_M, dtype=float)
        kd = np.asarray(kd_M, dtype=float)
        if np.any(c <= 0) or np.any(kd <= 0):
            raise ValueError("concentration and Kd must be strictly positive")
        return c / (c + kd)

    def bound_fraction_from_logs(self, ln_c: float, ln_kd: float) -> float:
        return float(self.occupancy(np.exp(ln_c), np.exp(ln_kd)))
