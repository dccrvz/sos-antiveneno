# Progress — SoroJá

Dated log of every change, newest first. Each entry says what changed, why, which checks
ran, whether it was deployed, and what is still open. Format: see `AGENTS.md`.

## 2026-11-15 — Number hunt run loaded on the Samsung; source scoring (Edu + Claude Code)

On Edu's request the Android dialer (separate pilot, not in this repo) now calls number-hunt
candidates first: 1,602 never-dialled numbers added to its queue, retries of rejected numbers
turned off (≈1% answered), and a one-time window reset so 16/11 is day 1 of 17 (last day 02/12,
99/day). Installed over the 09/11 build with the same key; read back on the phone: window
2026-11-16→2026-12-02, goal enabled, alarm 16/11 09:00. Parser fixes before loading: trunk zeros,
Receita's padded area codes and impossible area codes (all 1,602 dial-shape checked). New
`score_sources.py` rates sources and repair tricks by human-answer rate, crediting every source of a
number from the frozen `loaded-queue-2026-11-15.json` (what the phone actually got). Google Places approved
but blocked: billing is disabled on the Maps project (`fetch_places.py` ready, resumable).
Checks: app Java tests (RunWindow 28, Schedule 7, PhoneRules, RandomOrder, Recovery, Dual,
AudioHealth) pass; unchanged rebuild byte-identical to the installed APK before editing; scorer
tested on synthetic results. Deployed: phone only, no site change. Notion: done.

## 2026-11-15 — Number hunt: candidates for units with no working phone (Edu + Claude Code)

Analysis only; no app or data change. New `reports/number-hunt-2026-11/`. Joined `app/hospitals.json`
with the call dashboard (15/11 17:33): 1,543 of 2,279 units have no working number (176 with none
published, 923 where the carrier says every number doesn't exist, 431 other failures, 13 not
dialled). Sourced candidates from CNES (incl. old 7-digit landlines + leading 3, missing area
codes), Receita Federal CNPJ via BrasilAPI, earlier SoroJá versions in git (matched on CNES + name, so shared CNES codes never mix units), OpenStreetMap and
rule-based repair of dead numbers: 1,139 units now have a candidate; 1,588 never-dialled numbers in
`queue-candidates.json` (dialer queue format). 139 candidates are shared office numbers, marked.
Raw API dumps gitignored. Map: private artifact "SoroJá Number Hunt". Checks: script syntax,
`git diff --check`. Deployed: no. Open: load the queue on the Samsung; Google Places (≈US$ 50);
SAMU/state outreach; how confirmed numbers show on the site. Notion: done (page "Number Hunt —
finding numbers for units with none that work" under the SoroJá hub).

## 2026-11-14 — Repo transferred to dccrvz/sos-antiveneno (Edu + Claude Code)

Edu decided to move SoroJá under the D.C. Cruz org for funding (FAPESP PIPE opens
2026-11-16). On his yes, the repo was transferred with `gh api POST .../transfer`:
`dccrvz/sos-antiveneno`, still public, same repo ID 76060342; `educrvz/sos-antiveneno`
301-redirects there. Pre-checks: dccrvz is an org with Edu as owner; no name clash;
no Actions secrets, variables, webhooks or deploy keys; Vercel project `soroja` has no
env vars or deploy hooks. Local remote now `git@github.com:dccrvz/sos-antiveneno.git`.
Repo links updated in the site footer, privacy and terms pages (CACHE_NAME → v35),
PRIVACY/TERMS, AGENTS, docs and Apps Script comments. ADR 0005 supersedes ADR 0004.
project-kit registry updated (dccrvz/project-kit 572c55c).
Checks: prettier on changed files, `git diff --check`.
Deployed: yes. The Vercel GitHub app was installed on dccrvz (only `sos-antiveneno`) and
`vercel git connect` linked project `soroja` to `dccrvz/sos-antiveneno` (prod branch
`main`); this commit was pushed to confirm auto-deploy to soroja.com.br.
Open items: mint a new
fine-grained PAT (resource owner dccrvz) for the Apps Script and set script properties
`GITHUB_TOKEN` + `GITHUB_REPO=dccrvz/sos-antiveneno`. Never create a repo named
`sos-antiveneno` on educrvz. Notion: done (task page log, Projects row).

## 2026-11-13 — Adopted into the project-kit standard (project-kit adopt-project)

Canonical folder: `~/Documents/03 Software & AI/SoroJá` → repo https://github.com/educrvz/sos-antiveneno.
Other copies found (not the live home, marked with STALE_COPY.md):

- `~/Documents/Codex/2026-10-13/task/soroja-fix`: 38% identical, 0 files only there, 0 changed and newer there
- `~/Documents/Codex/2026-08-14/https-github-com-educrvz-sos-antiveneno/work/sos-antiveneno`: 35% identical, 0 files only there, 0 changed and newer there
  Added: .env.example, GEMINI.md, PROGRESS.md, docs/CONTEXT.md, docs/ISSUE_TEMPLATE.md, docs/RUNBOOK.md, docs/decisions/0001-one-project-home.md, docs/decisions/README.md, docs/decisions/_TEMPLATE.md, scripts/check.sh.

Merged: .gitignore (+19 rules); AGENTS.md (kit rules appended; SoroJá rules take precedence).

Also in this change (Claude Code, project-home adoption session):

- `scripts/check.sh` runs the same checks as `.github/workflows/ci.yml` (canonicalizer
  self-test, pytest, dataset validation, app-contract freshness, prettier on tracked
  files). No separate `check.yml` was added: `ci.yml` already gates `main`. Result: pass.
- Filled `docs/CONTEXT.md` and `docs/RUNBOOK.md` (deploy, rollback, refresh, secrets by
  name), added ADRs 0002 (public repo) and 0003 (layered data), reconstructed the history
  below from git, and wrote `docs/NOTION_UPDATE.md`.
- `.gitignore`: kit rules merged, but `build/` is NOT ignored (pipeline outputs are
  tracked); `reports/**/cnes_raw.json` ignored (CNES dumps contain staff e-mails).
- Committed today's November reports: `reports/phone-validation-2026-11/` (without
  `cnes_raw.json`) and `reports/public-corrections-2026-11/`.
- Not copies, left unmarked: the Android call pilot (separate repo
  `educrvz/soroja-phone-verification` + Codex outputs), `~/Downloads/soroja_auditoria_para_edu (1)`
  (external audit letter, April 2026), `03 Software & AI/AI/Gemini/SoroJa` (early notes),
  LinkedIn copy folders, `Codex/2026-10-22/soroja-phone-validation` (QR images only).
- Repo stays at `educrvz/sos-antiveneno`: Edu decided not to move it to `dccrvz` (ADR 0004).
  Deployed: no app change (docs, check script, reports only). Notion: pending (connector down; see docs/NOTION_UPDATE.md).

## 2026-11-13 — Phone validation sample and public-corrections finding (Claude Code)

Two research sessions, outputs in `reports/phone-validation-2026-11/` and
`reports/public-corrections-2026-11/`. Phones: 12% strict failure, 48% without an
independently confirmed number (n=50); 24 units in `call_list.csv`. Corrections: 18/20
verified reports confirmed; 81% of federal units in PR/ES/PE/RN differ from state lists.
Deployed: no. Notion: pending.

## 2026-10 — Call verification and state reconciliations (git history)

Carrier dialing pages (`app/ligacoes-vivo.html`, `ligacoes-claro.html`) and sourced
alternative contacts for the call retry batch (3704f2a, 5c8c1a4). PR and PE
state-vs-federal reconciliations (reports dated 2026-10-09). Araruama pin fix, Rio
Paranaíba community alert. Privacy page discloses GoatCounter collection; BA/SP
2026-07-03 verification documented (#52). Separate Android call pilot built in Codex.

## 2026-08 to 2026-09 — RJ refresh, official corrections, repo stays public (git history)

RJ refreshed from the 2026-07-03 Ministry PDF; BA/SP 2026-07-03 verification. SES-RS
temporary unit attribution (#42), São Domingos pin (#45), Ministry PDF hash refresh
(#47), Pix donation option. 2026-08-03: decision to keep the repo public and open source
(ADR 0002).

## 2026-06 to 2026-07 — Hardening and contributor path (git history)

Security policy (#18), contributor guide (#13), external refresh hand-off docs (#22),
CI fix for the Ministry update checker (#8), manual-triage reconciliation (#11), tests
for the override validator, community notes always visible. July: 25-UF field-change
review against the 2026-07-03 PDFs.

## 2026-05 — Community notes and diff-aware refresh (git history)

Community notes per CNES (several MG/SP units), Secretaria-attributed notes,
`refresh_diff.py` diff-aware refresh to protect overrides (ADR 0003). An offline
pre-cache change was reverted (2026-05-10).

## 2026-04 — Launch (git history)

2026-04-12 data pipeline for the PESA PDFs; 2026-04-14 UI redesign for emergency use;
2026-04-19 Google geocoding pipeline rebuild, 2,137 units published; 2026-04-20
Google-Sheet overrides via Apps Script; 2026-04-21 external audit by a physician
(kept outside the repo); 2026-04-22 dark theme, per-card mini-maps, footer tribute.
The repo itself dates from a 2016 placeholder (3 commits).
