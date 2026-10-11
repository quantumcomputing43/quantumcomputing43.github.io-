#!/usr/bin/env python3
"""Read-only DNS/TLS/HTTPS preflight for Bounty Tours.

This tool performs network reads only. It does not change DNS, hosting, accounts,
or send messages. A successful transport check does not prove business activity.
"""
from __future__ import annotations

import json
import socket
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

DOMAINS = ("bounty-tours.com", "www.bounty-tours.com")
TIMEOUT_SECONDS = 8


def check_dns(host: str) -> dict:
    try:
        rows = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        addresses = sorted({row[4][0] for row in rows})
        return {"status": "PASS" if addresses else "FAIL", "addresses": addresses}
    except socket.gaierror as exc:
        return {"status": "FAIL", "error": str(exc), "addresses": []}
    except Exception as exc:  # preserve unexpected environment/network failures
        return {"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}


def check_tls(host: str) -> dict:
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, 443), timeout=TIMEOUT_SECONDS) as raw:
            with context.wrap_socket(raw, server_hostname=host) as conn:
                cert = conn.getpeercert()
                return {
                    "status": "PASS",
                    "tls_version": conn.version(),
                    "cipher": conn.cipher()[0] if conn.cipher() else None,
                    "certificate_subject": cert.get("subject", []),
                    "certificate_not_after": cert.get("notAfter"),
                }
    except Exception as exc:
        return {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}


def check_https(host: str) -> dict:
    request = urllib.request.Request(
        f"https://{host}/",
        headers={"User-Agent": "Q33-read-only-preflight/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return {
                "status": "PASS",
                "http_status": response.status,
                "final_url": response.geturl(),
                "content_type": response.headers.get("Content-Type"),
            }
    except urllib.error.HTTPError as exc:
        # An HTTP response proves the server answered, but not that the site works.
        return {
            "status": "HTTP_RESPONSE",
            "http_status": exc.code,
            "final_url": exc.geturl(),
            "error": str(exc),
        }
    except Exception as exc:
        return {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}


def audit_domain(host: str) -> dict:
    dns = check_dns(host)
    # Only probe TLS/HTTPS when DNS resolves; avoid redundant failures.
    if dns.get("status") == "PASS":
        tls = check_tls(host)
        https = check_https(host)
    else:
        tls = {"status": "BLOCKED", "reason": "DNS did not resolve"}
        https = {"status": "BLOCKED", "reason": "DNS did not resolve"}
    return {"domain": host, "dns": dns, "tls": tls, "https": https}


def main() -> int:
    report = {
        "audit": "BOUNTY_TOURS_READ_ONLY_PREFLIGHT_V1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "network_mutations": False,
        "messages_sent": False,
        "interpretation_limit": (
            "Transport checks do not establish company operating status, ownership, "
            "commercial demand, or permission to contact."
        ),
        "domains": [audit_domain(host) for host in DOMAINS],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if any(
        item["dns"].get("status") == "PASS" for item in report["domains"]
    ) else 2


if __name__ == "__main__":
    sys.exit(main())
