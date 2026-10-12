---
name: dreamina-cli
description: Use Dreamina CLI to generate images or videos for QUANTUM33 only when the user explicitly requests generation. Use for CLI help, account-credit checks, prompt preparation, submission tracking, and safe local setup.
---

# Dreamina CLI — QUANTUM33 integration

## Scope and isolation
- This skill is an optional creative tool for producing explanatory visuals/videos. It is not part of the scientific evidence pipeline and must never be treated as evidence for a scientific claim.
- Keep Dreamina outputs and tasks separate from the miRNA-21, BHD/Axion, Quran, and Simulation Matrix scientific result records. Do not place generated media into research data directories unless the user explicitly asks.
- Do not change the Bounty Tours workflow or contract as part of Dreamina setup.
- The skill file documents use; it does not install the CLI, authenticate an account, or connect a remote GitHub runner.

## Safe first-use workflow
1. Inspect the environment first: `command -v dreamina`, then `dreamina -h`.
2. For any intended operation, inspect its current help first, e.g. `dreamina user_credit -h` or `dreamina text2video -h`. CLI help is authoritative because flags/models may change.
3. If not installed, show the user the official install command and ask them to run it in the terminal they want Codex to use:
   `curl -fsSL https://jimeng.jianying.com/cli | bash`
4. Authentication is user-controlled. If needed, ask the user to run `dreamina login` (or `dreamina login --headless` in a supported terminal) and complete the provider's authorization themselves. Never ask them to paste passwords, cookies, tokens, credential JSON, or session files into chat or commit them.
5. Before generation, run `dreamina user_credit` and report the available balance. Generation may consume credits. Do not submit any paid/credit-consuming generation task without explicit user approval of the prompt and estimated usage.
6. After approval, run the relevant command using the exact current help syntax. For asynchronous jobs, retain the submit/task ID and query the existing task before considering any retry. Never blindly resubmit a timed-out job.
7. Report the real task status and result path. A command being accepted is not proof that the video finished successfully.

## Security rules
- Never store credentials, cookies, login responses, tokens, or generated private media in Git.
- Do not add Dreamina secrets to GitHub Actions or repository files. Do not run credit-consuming generation automatically in CI.
- Do not download or execute third-party code as a substitute for the provider's documented CLI without user review.
- Prefer a local Codex terminal where the user can authenticate and inspect outputs. A GitHub-hosted runner is a separate environment and will not inherit a local login.
- Use neutral, scientifically accurate prompts. Label illustrative/synthetic visuals as illustrative; never present AI-generated scenes as experimental evidence.

## Typical read-only checks
```bash
command -v dreamina
dreamina -h
dreamina user_credit
dreamina list_task
```

Official setup/reference: https://dreamina.capcut.com/tools/dreamina-cli
