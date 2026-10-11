# Bounty Tours preflight audit

This is a separate, read-only technical preflight for the Bounty Tours candidate. It is deliberately isolated from the scientific miRNA-21 and BHD projects.

## Run

```bash
python bounty_tours/preflight_check.py
```

The script uses only the Python standard library. It probes DNS, verified TLS, and HTTPS for `bounty-tours.com` and `www.bounty-tours.com`, then prints a JSON report with an overall technical status. Preserve the complete output with the run timestamp.

## Decision rules

- **Technical PASS:** at least one host resolves, verified TLS succeeds, and the HTTPS GET succeeds after normal redirects.
- **Technical FAIL:** neither host completes all three checks. HTTP error responses are recorded as failures, not treated as successful homepage responses.
- **HOLD_RESEARCH:** evidence is incomplete or ambiguous.
- **Commercial PASS:** requires a separate human-confirmed contact and explicit authorization; technical reachability cannot establish demand or consent.

## Safety

The script makes read-only network requests. It does not modify DNS/hosting, use credentials, submit forms, or send email. It does not prove that the company is currently operating. No company outreach is authorized by this repository change.

The frozen contract is `bounty_tours/CONTRACT_V1.json`. The live result remains `NOT_RUN` until the script is executed in a network-enabled environment and its output is preserved.
