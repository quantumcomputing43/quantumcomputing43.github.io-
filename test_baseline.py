import numpy as np
from quantum_biomarker.transduction.dipolar import DipolarMagneticModel
from quantum_biomarker.measurement.binary_sensor import make_binary_probability_model
from quantum_biomarker.fisher.engine import FisherEngine

def theta():
    return np.array([np.log(5e-9), np.log(1e-8), np.log(2*np.pi*1e5), 1e3, 0.92])

def test_probabilities_normalize():
    p = make_binary_probability_model(model=DipolarMagneticModel(), t_int_s=20e-6)(theta())
    assert np.all(p > 0) and np.isclose(p.sum(), 1.0)

def test_fisher_psd():
    models = [make_binary_probability_model(model=DipolarMagneticModel(), t_int_s=t) for t in [5e-6, 10e-6, 20e-6, 40e-6]]
    F = FisherEngine(models).fisher(theta())
    assert np.all(np.linalg.eigvalsh(F) >= -1e-8)

def test_c_kd_structural_confounding():
    models = [make_binary_probability_model(model=DipolarMagneticModel(), t_int_s=t) for t in [5e-6, 10e-6, 20e-6, 40e-6]]
    F = FisherEngine(models).fisher(theta())
    # The first two columns are opposite because f=C/(C+Kd) depends on ln(C/Kd).
    assert np.allclose(F[:, 0], -F[:, 1], rtol=1e-4, atol=1e-10)
