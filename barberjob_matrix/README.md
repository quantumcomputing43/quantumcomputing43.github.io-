# BarberJob Matrix — MVP 0.1

A separate, testable job-search workspace for an experienced barber seeking opportunities across Europe, the Gulf, and other countries.

## Scope of the first version
- Build a CV from a structured profile, without inventing missing qualifications.
- Keep a vetted company/role contact list with source and verification date.
- Score role fit using explicit, explainable criteria.
- Generate a personalized email draft for human review.
- Run Simulation Matrix tests on data quality, duplicate contacts, role fit, and message quality.
- Track applications and outcomes.

## Safety gates
- **No automatic bulk sending in MVP.** Drafts only; a human reviews and sends.
- Do not scrape behind logins, bypass platform restrictions, or use purchased/unverified personal contact lists.
- Prefer official careers pages and public recruitment contact channels; verify local rules before contacting a company.
- Keep CV/contact data private. Never commit a real CV, passport, phone number, home address, or email credentials to this public repository.
- Do not claim language fluency, certificates, visa status, or experience unless the profile supports it.
- Record opt-outs/do-not-contact entries and never contact them again.

## Quick start
Python 3.11+
```bash
cd barberjob_matrix
python -m pip install -e ".[dev]"
pytest
```

Create a private copy of `profile.template.json`, fill only accurate facts, then generate a CV draft:
```bash
python -m barberjob_matrix.cli --profile profile.json --output CV_draft.md
```
(The CLI is a planned next step; the tested core functions are in `src/barberjob_matrix/core.py`.)

## Initial project gates
1. **Profile integrity:** no unsupported claims; missing facts remain visibly marked.
2. **Contact integrity:** company, role, source URL, checked date, and contact basis are recorded.
3. **Simulation Matrix:** test duplicates, missing fields, irrelevant roles, bad email formats, and opt-out enforcement before any live outreach.
4. **Pilot:** review 10 manually verified opportunities and drafts before expanding.
5. **Scale:** increase only when quality checks pass; send rate is not a success metric by itself.

## Project layout
- `profile.template.json`: safe blank profile structure.
- `data/companies_template.csv`: company opportunity tracking columns.
- `src/barberjob_matrix/core.py`: deterministic CV/email draft and matching utilities.
- `tests/`: automated validity and adversarial tests.
- `.github/workflows/barberjob-matrix.yml`: scoped CI for this project folder.

## Status
Bootstrap branch created for review. No company list has been collected and no email has been sent.
