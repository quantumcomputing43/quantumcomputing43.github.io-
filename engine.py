"""Nuisance-aware Fisher information engine."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.linalg import pinvh

PARAMETER_NAMES = ("ln_C", "ln_Kd", "ln_g", "Gamma_0", "eta")

@dataclass(frozen=True)
class FisherAudit:
    matrix: np.ndarray
    eigenvalues: np.ndarray
    rank: int
    condition_number: float
    psd: bool
    covariance: np.ndarray
    relative_sigma_C: float

class FisherEngine:
    def __init__(self, probability_models, step: float = 1e-5, svd_tol: float = 1e-10):
        if callable(probability_models):
            probability_models = [probability_models]
        self.probability_models = list(probability_models)
        self.step = float(step)
        self.svd_tol = float(svd_tol)

    @staticmethod
    def _validate(p):
        p = np.asarray(p, dtype=float)
        if p.ndim != 1 or p.size < 2:
            raise ValueError("Each probability model must return a 1-D outcome vector")
        if np.any(p < 0) or not np.isclose(p.sum(), 1.0, atol=1e-9):
            raise ValueError(f"Invalid probability vector: {p}")
        return p

    def probabilities(self, theta):
        return [self._validate(m(np.asarray(theta, dtype=float))) for m in self.probability_models]

    def fisher(self, theta, weights=None):
        theta = np.asarray(theta, dtype=float)
        if weights is None:
            weights = np.ones(len(self.probability_models))
        weights = np.asarray(weights, dtype=float)
        if weights.shape != (len(self.probability_models),) or np.any(weights < 0):
            raise ValueError("weights must match number of probability models and be non-negative")
        F = np.zeros((theta.size, theta.size))
        for w, model in zip(weights, self.probability_models):
            p0 = self._validate(model(theta))
            J = np.empty((p0.size, theta.size))
            for j in range(theta.size):
                # Absolute finite-difference scale avoids huge steps for log(C),
                # while preserving a relative perturbation of the parameter.
                h = self.step * max(1.0, abs(theta[j]))
                e = np.zeros_like(theta); e[j] = h
                J[:, j] = (self._validate(model(theta + e)) - self._validate(model(theta - e))) / (2*h)
            F += w * np.einsum("ki,k,kj->ij", J, 1.0/np.maximum(p0, 1e-300), J)
        return 0.5*(F + F.T)

    def audit(self, theta, N=1.0, prior=None, weights=None):
        F = float(N) * self.fisher(theta, weights=weights)
        if prior is not None:
            prior = np.asarray(prior, dtype=float)
            if prior.shape != F.shape:
                raise ValueError("prior must have the same shape as the Fisher matrix")
            F = F + prior
        F = 0.5*(F + F.T)
        evals = np.linalg.eigvalsh(F)
        scale = max(1.0, np.max(np.abs(evals)))
        rank = int(np.sum(evals > self.svd_tol*scale))
        pos = evals[evals > self.svd_tol*scale]
        cond = float(pos.max()/pos.min()) if pos.size else np.inf
        cov = pinvh(F, rtol=self.svd_tol)
        rel_sigma_C = float(np.sqrt(max(cov[0,0], 0.0)))
        return FisherAudit(F, evals, rank, cond, bool(np.min(evals) >= -1e-10*scale), cov, rel_sigma_C)
