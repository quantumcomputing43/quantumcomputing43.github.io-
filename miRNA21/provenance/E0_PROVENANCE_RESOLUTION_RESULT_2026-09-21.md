# E0 Provenance Resolution — Result
DATE: 2026-09-21
PROJECT_ID: MIRNA21_FORENSIC_AUDIT
CASE_ID: MIRNA21_REPRESENTATION_INFORMATION_RETENTION

## Scope executed
Library-first search plus accessible GitHub history/trees/commits for:
- exact R8D frozen artifact
- R8D dimensions and feature order
- PLS coefficients/transformation lineage
- executable V1 mapping
- exact R8D null implementation
- historical V5 executable

## Findings

### R8D
Library records confirm the conceptual identity:
"frozen multi-task PLS 8D representation using PAM50 + miR-21 task information."

However, no authoritative artifact containing the exact 8D coefficients, feature order, dimensions, version/hash, and transformation lineage was recovered.

The historical GitHub repository contains miRNA21.py, engine.py, dipolar.py, identifiability artifacts, and an archived website ZIP in older commits, but the accessible repository metadata does not establish the exact R8D transform. The historical miRNA21.py is a Langmuir binding baseline, not the R8D implementation.

Therefore R8D provenance remains BLOCKED.

### V1 executable/mapping
The V1 master explicitly requires dimensions and mapping to be derived from registered frozen representation artifacts and says STOP if provenance cannot be resolved.

No provenance-complete V1 executable or synthetic latent-to-molecular feature mapping was recovered.

Therefore V1 execution remains BLOCKED.

### R8D null
Current records contain two descriptions that must not be silently conflated:
1. "randomized/shuffled 8D null control" in representation summaries.
2. label permutation within TRAIN only in the V1 master.

The V1 master is the current contract, but because the frozen R8D executable/mapping itself is missing, the complete executable null pipeline cannot yet be validated end-to-end.

### V5
Historical V5 result records are recovered, but the exact historical V5 executable source is not. No reconstructed executable is promoted.

Therefore V5 historical reproduction remains BLOCKED.

## Decision
E0 = FAIL TO UNBLOCK / INCONCLUSIVE-BLOCKED.

This is a provenance result, not a scientific failure of R8D.

## Matrix consequence
Do NOT escalate to Level 10/100/.../1M scientific simulation.

The next justified operation is targeted artifact recovery only:
- inspect recoverable historical archive/package contents if binary access becomes available;
- inspect Library for any separately stored transform/model artifact;
- inspect future repository history if additional refs become available.

No scientific parameters, dimensions, coefficients, null mechanism, or mapping may be invented to bypass this gate.
