# SoroJá — runbook

> How to run, check, deploy, roll back and debug. Commands must be copy-pasteable.
> Dataset refresh detail lives in [`PROCESS.md`](PROCESS.md); this file links to it.

## First-time setup

```bash
git clone https://github.com/dccrvz/sos-antiveneno.git
cd sos-antiveneno
npm ci                       # prettier only
python3 -m pip install pytest pdfplumber
cp .env.example .env         # only needed for dataset refreshes (Google Maps key)
```

## Run locally

```bash
python3 -m http.server 8000 --directory app   # → http://localhost:8000
```

Geolocation needs `localhost` or HTTPS. The service worker caches aggressively: use a
private window or DevTools → Application → Unregister after changing app files.

## Test / pre-deploy check

```bash
./scripts/check.sh           # must pass before every push to main (CI runs the same set)
SKIP_FORMAT=1 ./scripts/check.sh   # skip prettier if node is not installed
```

Manual smoke test after app changes: open the app on a phone-width window, allow
location, confirm the nearest cards load, the map opens, and "Ligar" opens the dialer.

## Deploy

- Target: Vercel project `soroja` → <https://soroja.com.br>.
- How: push to `main`. CI runs; Vercel deploys `main` automatically. Branches get
  Vercel preview URLs.
- Any change to a precached app file must bump `CACHE_NAME` in `app/sw.js`.
- Data-only fixes (overrides, community notes) may arrive from the Google Sheet; the
  `rebuild-hospitals-on-override` workflow regenerates `hospitals.json` and commits it.
- After deploying, verify with a cache-busted request (not raw.githubusercontent.com):

```bash
curl -s "https://soroja.com.br/hospitals.json?cb=$(date +%s)" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))"
curl -s "https://soroja.com.br/sw.js?cb=$(date +%s)" | head -1
```

- Log it in `PROGRESS.md` (commit, result).

## Dataset refresh (new Ministry PDF)

Follow [`PROCESS.md`](PROCESS.md) (or the `pesa-refresh` Claude skill). Short form:
`python3 scripts/check_updates.py` → download PDF to `Docs Estado/` → extract to
`extracted/{UF}.new.json` → `python3 scripts/refresh_diff.py` and review every change
(pdfplumber drops rows; cross-check raw PDF text) → promote → `./scripts/refresh_dataset.sh`
→ validate → commit. The full refresh calls Google Maps APIs (costs money): do not run it
casually.

## Roll back

1. Fastest: Vercel dashboard → project `soroja` → Deployments → previous good deployment →
   "Promote to Production" (Instant Rollback).
2. Code/data: `git revert <bad-commit> && git push` → CI checks and Vercel redeploys.
3. A single sheet override: delete its row in the Overrides tab and republish (see
   PROCESS.md → overrides).
4. Clients keep the old service worker until `CACHE_NAME` changes; bump it in the fix.
   Write what happened in `PROGRESS.md`.

## Backups

- Git history is the backup of code, data layers and published JSON (public on GitHub,
  plus this local clone).
- Source PDFs: `Docs Estado/` locally only (git-ignored). TODO: decide an off-machine copy.
- Corrections Sheet: Google Drive version history.

## Logs and monitoring

- Deploy logs: Vercel dashboard → `soroja` → Deployments.
- CI and scheduled jobs: GitHub → Actions (`CI`, `check-ms-updates`, `rebuild-hospitals-on-override`).
- New Ministry PDFs: auto-opened GitHub issues from `check-ms-updates`.
- Public error reports: private Control Sheet (ID in local `CLAUDE.md`); triage with the
  `community-report` skill.
- Traffic: GoatCounter (aggregate, cookieless).

## Secrets inventory

Real values live only in the vault **DC Cruz — SoroJá** (to be created) and in local
`.env` / macOS Keychain / the provider's settings. Never in git.

| Key / item                    | What it is                                          | Where it is set                                      | Vault item             |
| ----------------------------- | --------------------------------------------------- | ---------------------------------------------------- | ---------------------- |
| `GOOGLE_MAPS_API_KEY`         | Geocoding + Places for dataset refreshes            | `.env` or Keychain service `google_maps_api_key`     | Google Maps API key    |
| `GITHUB_TOKEN` (Apps Script)  | Fine-grained PAT that commits overrides to the repo | Apps Script → Script properties (with `GITHUB_REPO`) | Apps Script GitHub PAT |
| GitHub org `dccrvz`           | Repo owner (Edu = org owner, account `educrvz`)     | github.com                                           | GitHub login           |
| Vercel account                | Hosting, domains, rollback                          | vercel.com                                           | Vercel login           |
| Domain registrar              | `soroja.com.br` DNS                                 | registrar                                            | Registrar login        |
| Google account (Sheets/Drive) | Overrides Sheet, Control Sheet, Apps Script         | google.com                                           | Google login           |
| `contato.soroja@gmail.com`    | Public contact mailbox                              | gmail.com                                            | Contact mailbox login  |
| GoatCounter                   | Analytics dashboard                                 | goatcounter.com                                      | GoatCounter login      |

## Common issues

| Symptom                               | Likely cause                            | Fix                                                                    |
| ------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------- |
| Users still see old data after deploy | Service worker cache                    | Bump `CACHE_NAME` in `app/sw.js`; verify with cache-busted curl        |
| CI "app contract is current" fails    | `app/hospitals.json` not rebuilt        | `python3 scripts/build_app_hospitals_json.py` and commit both JSONs    |
| Refresh drops hospitals               | pdfplumber table extraction lost rows   | `scripts/refresh_diff.py` + compare with raw PDF text before promoting |
| Override applied to the wrong unit    | Shared CNES (e.g. `2115786`)            | Fix in the source extract, never key overrides by a shared CNES        |
| Sheet "Publish" fails                 | Expired PAT or repo renamed/transferred | Rotate `GITHUB_TOKEN` / update `GITHUB_REPO` in Script properties      |
