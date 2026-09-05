from __future__ import annotations
import json
from dataclasses import asdict
from ..fisher.engine import FisherAudit

def audit_to_json(audit: FisherAudit) -> str:
    d = asdict(audit)
    for k, v in list(d.items()):
        if hasattr(v, "tolist"): d[k] = v.tolist()
    return json.dumps(d, indent=2)
