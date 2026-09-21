"""Mechanical repository/provenance validator.

This script deliberately does not make scientific decisions. It checks that
required namespaces and explicit blocker documentation exist.
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

required = [
    ROOT / "README.md",
    ROOT / "provenance" / "MASTER_REPAIR_OPERATION_2026-09-21.md",
    ROOT / "provenance" / "V1_CONTRACT_REGISTRY.json",
    ROOT / "provenance" / "REPOSITORY_AUDIT_CHECKLIST.md",
    ROOT / "representations" / "R8D" / "README.md",
    ROOT / "simulations" / "V1" / "README.md",
    ROOT / "simulations" / "V3" / "README.md",
    ROOT / "simulations" / "V4" / "README.md",
    ROOT / "simulations" / "V5" / "README.md",
    ROOT / "validation" / "README.md",
]

missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    raise SystemExit("MISSING_REQUIRED_PATHS: " + ", ".join(missing))

registry = json.loads((ROOT / "provenance" / "V1_CONTRACT_REGISTRY.json").read_text())
if registry.get("execution_gate") != "CLOSED":
    raise SystemExit("INVALID_GATE: execution_gate must remain CLOSED until scientific blockers are resolved")

print("MECHANICAL_REPOSITORY_VALIDATION: PASS")
print("SCIENTIFIC_EXECUTION_GATE: CLOSED")
print("BLOCKED_CONTRACTS:", sum(c["state"] == "BLOCKED" for c in registry["contracts"]))
