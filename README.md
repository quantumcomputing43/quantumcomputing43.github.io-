# QuantumBiomarker Framework

## Baseline: miRNA-21 dipolar magnetic shift/dephasing

This repository starts the simulation branch of the Quantum Biomarker project.
The current model is an **effective, experimentally testable baseline**, not a
claim that miRNA-21 has a particular magnetic moment or that cancer can be
detected from this model alone.

### Parameter vector

`theta = (ln C, ln Kd, ln g, Gamma_0, eta)`

- `C`, `Kd`: mol/L
- `g`: angular-frequency coupling scale, rad/s
- `Gamma_0`: s^-1
- `eta`: readout efficiency, 0 < eta < 1

### Baseline transduction

`f = C/(C+Kd)`

`delta_omega = g f`

`Gamma_phi = Gamma_0 + g^2 tau_c f(1-f)`

The stochastic dephasing term is a variance-times-correlation-time effective
model. `tau_c` must be replaced/validated against experimental dynamics.

### Run

```bash
python scripts/run_baseline.py
pytest -q
```

The next physics-critical task is to replace the effective `g` mapping with an
experimentally justified geometry/material model and independently validate the
correlation time, magnetic moment/source spectrum, and readout model.
