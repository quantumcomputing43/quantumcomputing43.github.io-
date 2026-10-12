# Dreamina CLI + Codex + GitHub — setup and audit

## Audit result (2026-10-12)

- The repository's default branch is `main`; the existing Bounty Tours preflight workflow is read-only and scoped to `bounty_tours/**`.
- No existing Dreamina CLI integration or Codex skill was found in the repository.
- `requirements.txt` contains only the existing Python scientific stack. Dreamina CLI is a separate external executable, not a Python dependency.
- The reconstructed Axion V15 script is explicitly marked as a model-dependent reconstructed baseline. Dreamina is only for illustrative media and must not be connected to scientific validation.
- To avoid disrupting active work, this integration is isolated on branch `integrate/dreamina-cli-codex-2026-10-12`. No existing files or workflows were modified.

## What this change provides

- A project-scoped Codex skill at `.agents/skills/dreamina-cli/SKILL.md`.
- This setup/audit guide.
- No credentials, tokens, generated media, or credit-consuming jobs are included.

## Install on the machine where Codex will run

The repo and the CLI are separate. Open this repository in the Codex environment that has a terminal, then run:

```bash
curl -fsSL https://jimeng.jianying.com/cli | bash
```

Open a fresh terminal if necessary, then check:

```bash
command -v dreamina
dreamina -h
dreamina user_credit
```

If `dreamina` is not on PATH, the documented default install location may be `~/.local/bin`; add that directory to PATH for the active shell if needed.

## Sign in safely

Run `dreamina login` in that same environment and complete authorization on Dreamina's official flow. Use `dreamina login --headless` only if the installed CLI help supports it and a suitable browser/QR flow is available.

Never commit authentication files or paste cookies, session JSON, or credentials into GitHub. A login on a phone/browser does not necessarily authenticate a separate Codex terminal or a GitHub Actions runner.

## First test (read-only)

1. Run `dreamina -h` and `dreamina user_credit`.
2. Confirm the account/credit output is understandable.
3. Run the relevant subcommand help, such as `dreamina text2video -h`.
4. Draft a short scientific-illustration prompt and show it for review.
5. Only after explicit approval, submit a generation request. All generation commands may consume account benefits/credits; verify balance and current pricing before each run.
6. For asynchronous tasks, query the existing submit ID before any retry.

## GitHub Actions policy

Do not add Dreamina generation to GitHub Actions yet. The CLI needs its own installation and account authorization, and generation may consume credits. A local login will not transfer to the hosted runner. Keep CI limited to non-secret documentation/lint checks until a separate secure automation design is reviewed and explicitly approved.

## Current status

- Repository audit: **PASS** (read-only review completed).
- Integration files: **added on the isolated branch**.
- CLI installed: **NOT VERIFIED** (GitHub API cannot install software in the user's Codex runtime).
- Dreamina login: **NOT VERIFIED**.
- Credits: **NOT CHECKED**.
- Video generation: **NOT RUN**.
- Main branch: **unchanged**.
