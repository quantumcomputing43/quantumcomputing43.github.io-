#!/usr/bin/env python3
import numpy as np
from quantum_biomarker.transduction.dipolar import DipolarMagneticModel
from quantum_biomarker.measurement.binary_sensor import make_binary_probability_model
from quantum_biomarker.fisher.engine import FisherEngine, PARAMETER_NAMES

# theta = (ln C, ln Kd, ln g, Gamma_0, eta)
theta = np.array([np.log(5e-9), np.log(10e-9), np.log(2*np.pi*1e5), 1e3, 0.92])
model = DipolarMagneticModel(dipolar_correlation_time_s=1e-6)

# Multiple interrogation times are essential: one binary probability is rank <= 1.
times = np.array([5, 10, 20, 40, 80]) * 1e-6
models = [make_binary_probability_model(model=model, t_int_s=t) for t in times]
engine = FisherEngine(models)
audit = engine.audit(theta, N=2e5)

print("Parameter order:", PARAMETER_NAMES)
print("Interrogation times (us):", times*1e6)
print("Per-setting probabilities:")
for t, m in zip(times, models): print(f"  {t*1e6:6.1f} us -> {m(theta)}")
print("Fisher matrix:\n", audit.matrix)
print("Eigenvalues:", audit.eigenvalues)
print("Rank:", audit.rank, "/ 5")
print("Condition number:", audit.condition_number)
print("PSD:", audit.psd)
print("Relative sigma(ln C) CRB:", audit.relative_sigma_C)
print("\nIMPORTANT: C and Kd enter only through C/(C+Kd) in this baseline, so ln C and ln Kd are structurally confounded. Full identifiability therefore requires an additional observable or independently calibrated Kd.")
