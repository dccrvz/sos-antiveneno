# Repository Instructions for AI Agents

## Project Snapshot

SoroJa is a static, mobile-first emergency reference app for finding Brazilian
antivenom hospitals. The public app lives in `app/`; the data pipeline lives in
`scripts/`; source and manual data live in `extracted/` and `data/`; generated
artifacts live in `build/`, `reports/`, `app/hospitals.json`, and
`hospitals.json`.

Keep the app static-first and offline-capable. Browser geolocation must stay on
the user's device; do not send, log, store, or add analytics around precise user
location.

This file is the single repository instruction file for every AI agent (Codex,
Claude, others). Project strategy and decisions live in the SoroJá Notion hub;
a local, gitignored `CLAUDE.md` may only point here and hold non-public
operational IDs.

## Non-Negotiables

- Product name is SoroJá; repo name is `sos-antiveneno`. Do not rename either.
- The repository stays public and open source (decision 2026-08-03). Do not add
  a root `LICENSE` file without asking; the footer carries the open-source
  statement by design.
- Public contact is `contato.soroja@gmail.com`. Never restore personal WhatsApp
  links.
- Preserve the footer tribute to Bernardo de Lima Mendes verbatim; flag any PR
  that removes or rewords it.
- Never publish reporter names, phone numbers or raw report text (LGPD-minimal).
- Do not key overrides by CNES when the CNES is shared by several facilities
  (e.g. `2115786`, three MG units); fix those in the source extract instead.
- Bump `CACHE_NAME` in `app/sw.js` whenever any precached app file changes.
- Gate every state promotion with `scripts/refresh_diff.py`; pdfplumber table
  extraction silently drops rows, so cross-check against raw PDF text.
- Verify production with a cache-busted request to `https://soroja.com.br`,
  not `raw.githubusercontent.com`.

## Read First

- Start with `README.md` for the project shape.
- Read `docs/PROCESS.md` only for dataset refresh, geocoding, PESA PDF,
  generated artifact, override, or community-note work.
- Read `PRIVACY.md` and `TERMS.md` before changes involving privacy, emergency
  wording, medical-risk UX, third parties, geolocation, service workers, CSP,
  forms, or public data collection. If `SECURITY.md` exists, read it for the
  same work.
- Follow more local instructions if a future subdirectory adds its own
  `AGENTS.md`.

## Token Discipline

- Use `rg` and targeted file reads before opening large files.
- Avoid loading all of `app/hospitals.json`, `hospitals.json`, `build/*`,
  `reports/*`, large CSVs, or per-state JSONs unless the task requires it.
- Prefer schemas, scripts, tests, reports summaries, and small samples over
  full generated artifacts.
- Do not duplicate `docs/PROCESS.md` in new docs; link to it and add only the
  missing operational decision.

## Data Safety

- Ministry of Health PESA data is the canonical official layer.
- `data/location_overrides.json` and `data/community_notes.json` are traceable
  layers on top of official data; do not silently fold them into source
  extracts.
- Do not manually edit generated files when a script owns them. Regenerate via
  the pipeline or the specific builder script.
- Treat unexpected row-count, CNES, UF, source-date, coordinate, or
  publish-policy changes as blockers to investigate.
- Full refreshes can call Google Maps APIs. Do not run
  `./scripts/refresh_dataset.sh` casually; use it when dataset/public artifacts
  actually need regeneration.

## App and Content Rules

- Keep the app vanilla HTML/CSS/JS unless there is a strong reason to add a
  dependency.
- Preserve the current security posture in `vercel.json`, especially CSP,
  frame restrictions, referrer policy, and geolocation permissions.
- Do not add cookies, tracking pixels, analytics, or default PII collection.
- User-facing app copy should be pt-BR. Code, internal docs, comments, commit
  messages, and PR text should be en-US unless a local file clearly uses
  another language.
- Emergency guidance must remain conservative: tell users to call SAMU 192 or
  Bombeiros 193 and confirm with the hospital/CIATox before traveling.

## Validation

- Markdown-only docs changes: `git diff --check -- <changed-files>`
- If `package.json` defines `format:check`, run `npm run format:check` for
  docs/config changes.
- Python pipeline or script changes: `python3 -m pytest scripts/tests/ -v`
- Published hospital JSON changes:
  - `python3 scripts/validate_hospitals_json.py app/hospitals.json`
  - `python3 scripts/rebuild_final_artifacts.py --check`
- Full dataset refresh or generated artifact rebuild:
  - `./scripts/refresh_dataset.sh`
  - `python3 scripts/validate_hospitals_json.py app/hospitals.json`
  - `python3 scripts/rebuild_final_artifacts.py --check`

If validation cannot be run, report the exact command and the blocker.

## Git

- Use the current branch unless the user asks for another one.
- Keep PRs narrow: one behavioral purpose, one reviewable scope.
- Use Conventional Commits when no stricter local convention exists, with a
  meaningful scope.
- Before pushing authored commits, verify the latest commit signature with
  `git log --show-signature -1`.

<!-- project-kit:start -->

> Merged from `dccrvz/project-kit` on 2026-11-13. Where a kit rule and a SoroJá rule
> above disagree, the SoroJá rule wins (e.g. the repo stays public, PRs stay narrow, and
> `CLAUDE.md` stays local-only because it holds private operational IDs).

## This folder is the one home of SoroJá

- Repo: https://github.com/dccrvz/sos-antiveneno · Notion: SoroJá hub (URL in the local `CLAUDE.md` and the project-kit registry; kept out of this public repo) · Secrets vault: DC Cruz — SoroJá
- Registry entry: `soroja` in `dccrvz/project-kit` → `projects.json`

## Before you change anything

1. Confirm this is the live copy: `.project-home.json` is here and its `repo` matches
   `git remote get-url origin`. If you find `STALE_COPY.md`, stop and go to the path it names.
2. Run `git pull`. Other people and other AI sessions also work here.
3. Read `docs/CONTEXT.md`, `docs/RUNBOOK.md` and the latest entries at the top of
   `PROGRESS.md`. Skim the titles in `docs/decisions/`.
4. Before you build something, search `PROGRESS.md` and the code. It may already exist.

## Rules

- **Never commit secrets.** Real values live only in the vault (DC Cruz — SoroJá) and in the local,
  git-ignored `.env`. If you need a new secret: add the key (no value) to `.env.example`,
  add a row to the secrets table in `docs/RUNBOOK.md`, and ask the human to store the value.
- Never put real client or personal data in git, tests, fixtures, logs, screenshots or issues.
- **Check before every deploy:** `./scripts/check.sh` must pass. Never deploy a red check.
- **Deploy and roll back only as `docs/RUNBOOK.md` describes.** Take a backup first when a
  change touches production data or the database schema.
- **Log every change.** Add a new entry to the top of `PROGRESS.md` (format below) in the
  same commit as the change, then push.
- **Keep the docs true.** When reality changes, update them in the same commit:
  `docs/CONTEXT.md` (what, who, architecture, data, integrations), `docs/RUNBOOK.md`
  (run, test, deploy, rollback, logs, secrets, common issues), and a new ADR in
  `docs/decisions/` for any lasting choice. Never rewrite an old ADR; supersede it.
- If the docs and the code disagree, trust the code, fix the docs and note it in PROGRESS.
- Ask the human first before anything irreversible or outward-facing: deleting data,
  production schema changes, messaging real customers, spending money, changing access.
- If the expected product behavior is unclear, ask. Do not invent it.
- Keep changes small. Commit messages say why. Code and commits in English; user-facing
  copy in the client's language.
- Notion: when the Notion connector works, copy the PROGRESS entry into the project's
  Notion maintenance log. If it does not, write `Notion: pending` in the entry.

## PROGRESS.md entry format (newest first)

```
## YYYY-MM-DD — short title (name + AI tool)
What changed and why. Checks run and their results.
Deployed: yes/no (commit, where). Rollback: how, if not the standard one.
Open items, risks, Notion: done/pending.
```

<!-- project-kit:end -->
