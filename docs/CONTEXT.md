# SoroJá — context

> What this is and how it fits together. Keep it short and true; update it in the same
> commit whenever reality changes. Deep pipeline detail lives in
> [`PROCESS.md`](PROCESS.md); this file does not repeat it.

## In one paragraph

SoroJá (<https://soroja.com.br>, repo `sos-antiveneno`) is a free, open-source,
mobile-first web app that shows the nearest Brazilian hospitals that hold antivenom
(soro antiveneno/antipeçonhento) for snake, scorpion, spider and other venomous-animal
accidents. The Ministry of Health publishes these "PESA" reference units only as one PDF
per state; SoroJá extracts all 27 states, geocodes them, audits the result and serves it
as a static, offline-capable PWA. It started in April 2026 after the death of Bernardo
de Lima Mendes in Conchal/SP (the footer tribute must stay verbatim). It always tells the
user to call SAMU 192 / Bombeiros 193 and to confirm with the hospital or CIATox first.

## Client and people

| Role                             | Name                                       | Contact                    | Notes                                           |
| -------------------------------- | ------------------------------------------ | -------------------------- | ----------------------------------------------- |
| Owner / maintainer               | Edu (DC Cruz, GitHub `educrvz`)            | `contato.soroja@gmail.com` | Own public-interest product, no client contract |
| Public contributors              | Anyone, via issues/PRs and "Reportar erro" | GitHub                     | See [`CONTRIBUTING.md`](../CONTRIBUTING.md)     |
| Collaborators with deploy rights | None yet                                   |                            | Ask Edu before inviting anyone                  |

## Scope and contract

- Type: own product (public interest), not sold. No maintenance contract.
- Included: the public app, the data pipeline, the correction layers and the weekly
  Ministry-update check.
- Not included: telemedicine, clinical advice, real-time stock of antivenom.

## Architecture

- **Frontend:** vanilla HTML/CSS/JS in [`app/`](../app) (`index.html`, `sw.js` service
  worker with `CACHE_NAME`, `manifest.json`, Leaflet map). Geolocation stays on the
  device. Also hosts carrier dialing pages (`ligacoes-vivo.html`, `ligacoes-claro.html`,
  `call-list*.js`) used by the phone-verification effort.
- **Hosting:** Vercel project `soroja`, auto-deploys `main` from GitHub. Security headers
  and CSP in [`vercel.json`](../vercel.json).
- **Data pipeline:** Python in [`scripts/`](../scripts), orchestrated by
  `scripts/refresh_dataset.sh` (extract → merge → normalize → QA → geocode → classify →
  repair → reconcile → build `app/hospitals.json`). See [`PROCESS.md`](PROCESS.md).
- **Scheduled jobs (GitHub Actions):**
  - `check-ms-updates.yml`: daily 09:00 UTC, checks gov.br for newer state PDFs and
    opens an issue.
  - `rebuild-hospitals-on-override.yml`: on push of `data/*overrides*/notes/temporary`,
    rebuilds and commits `hospitals.json` (Vercel then redeploys).
  - `ci.yml`: canonicalizer self-test, pytest, dataset validation, prettier, security
    config tests. `scripts/check.sh` runs the same set locally.
- **Corrections intake:** Google Sheet with Apps Script ([`scripts/sheet/Code.gs`](../scripts/sheet/Code.gs))
  that commits `data/location_overrides.json` / `data/community_notes.json` to GitHub.
  Sheet IDs are private (local `CLAUDE.md`).

## Data

- **Official layer (canonical):** Ministry of Health PESA PDFs, one per UF, in
  `Docs Estado/{UF}_{YYYYMMDD}.pdf` (git-ignored, copyrighted). Extracted to
  `extracted/{UF}.json`; source dates and hashes in `data/source_dates.json` and
  `data/source_hashes.json`.
- **State lists (secondary):** some state health secretariats (SESA-PR, SES-ES, SES-PE,
  SESAP-RN, SES-RS, SESAU-AL, OuvERJ/RJ) publish their own lists. They differ a lot from
  the federal one (see findings). Verified official corrections live in a separate
  correction layer (`scripts/apply_official_state_corrections.py`), never folded into the
  extracts.
- **Community layers:** `data/location_overrides.json` (pin fixes, hides) and
  `data/community_notes.json` (alerts shown on cards), plus
  `data/official_temporary_units.json`. Traceable, reviewable, on top of official data.
- **Published:** `app/hospitals.json` and root `hospitals.json` (2,279 units on
  2026-11-13), owned by `scripts/build_app_hospitals_json.py`. Never edit by hand.
- **Personal data:** none in git. Reporter names, phones and raw report text stay in the
  private Control Sheet (LGPD-minimal). CNES API dumps with staff e-mails are git-ignored.

## Findings so far (November 2026)

- **Phone validation** ([`reports/phone-validation-2026-11/ACHADOS.md`](../reports/phone-validation-2026-11/ACHADOS.md)):
  random sample of 50 of 2,279 units (seed 20261113). Strict failure (missing or invalid
  number) 12% (6/50, Wilson 95% CI 6–24%); no independently confirmed number 48%
  (24/50, 35–61%). About half of all units (~1,100) would need a human call to confirm.
  24 units are queued in `call_list.csv`.
- **Public corrections** ([`reports/public-corrections-2026-11/ACHADO.md`](../reports/public-corrections-2026-11/ACHADO.md)):
  43 new public reports in 13 UFs; 35 of 2,279 published units (1.5%) reported; 18 of 20
  verified reports confirmed (90%). State and federal lists diverge for 231 of 285
  federal units (81%) in PR, ES, PE and RN.
- Earlier reconciliations: [`reports/pr_state_federal_reconciliation_2026-10-09.md`](../reports/pr_state_federal_reconciliation_2026-10-09.md),
  [`reports/pe_state_federal_reconciliation_2026-10-09.md`](../reports/pe_state_federal_reconciliation_2026-10-09.md).

## Integrations and accounts

| Service                          | Used for                                | Account / project                | Login lives in         |
| -------------------------------- | --------------------------------------- | -------------------------------- | ---------------------- |
| GitHub                           | Code, CI, issues                        | `dccrvz/sos-antiveneno` (public) | vault DC Cruz — SoroJá |
| Vercel                           | Hosting and deploys                     | project `soroja`                 | vault DC Cruz — SoroJá |
| Domain registrar (soroja.com.br) | DNS                                     | TODO: confirm registrar          | vault DC Cruz — SoroJá |
| Google Maps Platform             | Geocoding/Places during refreshes       | TODO: GCP project name           | vault DC Cruz — SoroJá |
| Google Sheets + Apps Script      | Overrides and error-report intake       | Edu's Google account             | vault DC Cruz — SoroJá |
| GoatCounter                      | Cookieless page counts (see PRIVACY.md) | TODO: site code                  | vault DC Cruz — SoroJá |
| Gmail `contato.soroja@gmail.com` | Public contact                          |                                  | vault DC Cruz — SoroJá |

## Where everything is

- Code: this repo (<https://github.com/dccrvz/sos-antiveneno>); local folder
  `~/Documents/03 Software & AI/SoroJá`
- Docs and history: SoroJá Notion hub (link in local `CLAUDE.md` and the project-kit
  registry)
- Production URL: <https://soroja.com.br> · Staging: Vercel preview deployments per branch
- Related, separate work (not in this repo): Android call-verification pilot
  (`educrvz/soroja-phone-verification`; Codex outputs under
  `~/Documents/Codex/2026-10-22/take-a-look-at-this-thread/outputs/`).
