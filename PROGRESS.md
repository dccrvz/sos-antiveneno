# Progress — SoroJá

Dated log of every change, newest first. Each entry says what changed, why, which checks
ran, whether it was deployed, and what is still open. Format: see `AGENTS.md`.

## 2026-11-22 — FAPESP PIPE branch: main merged again, twice (Claude Code)

Routine: resolved PROGRESS.md conflicts on PR #56, keeping both sides. Checks: prettier,
`git diff --check`. Deployed: no. Open: old PR commit 5d36545 still shows the removed budget
estimates (Edu's call). Notion: pending.

## 2026-11-22 — Evening extraction, window reset on the phone, new radio hours (Edu + Claude Code)

Second extraction of the day, on Edu's request: the 99 calls of 22/11 (all number-hunt candidates,
no technical errors, 4 answered by a person). Hunt so far: 693 of 1,602 candidates dialled, 45
answered (36 with no sign of being another place), 909 left. In this repo: `source_scores.*` and
`number-hunt.html` rebuilt. Outside the repo, on the dialer phone, at Edu's request: the run window
now starts 2026-11-23 (last day still 2026-12-02) so the app's per-day list starts fresh, with the
queue and call journal untouched; airplane mode now runs 21:00-06:59 instead of 19:00-07:59; and an
SMS "call me" from Edu's number, read by the Mac over the cable, starts a call of the separate
Companion prototype during radio hours.
Checks: official totals unchanged in the rebuilt data (2,343 numbers, 272 answered); on the phone,
window values, foreground service and the exact alarm for 23/11 09:00 read back after the app
restarted; night script on the phone identical to the Mac copy; real SMS inbox read over adb.
Deployed: validacao.soroja.com.br republished on Edu's instruction to push the data (Vercel
`soroja-validacao`; live check: HTTP 200, noindex header, latestEvent 2026-11-22T17:33, audioPath
null); private Number Hunt artifact updated. Site `soroja.com.br` and `app/hospitals.json` untouched.
Unverified: the app's home screen was not opened to see the empty list; the new airplane hours are
only proven at the next 21:00 and 07:00. Open: Edu's call on re-reading the 50 skipped calls and on
how a candidate becomes a published number. Notion: done (call diary, operations page, status page).

## 2026-11-22 — Number hunt: first results, page and scores updated (Edu + Claude Code)

Edu plugged in the Samsung and asked for the new calls to be extracted and shown. Pulled the 594
attempts of 16–21/11 over USB (99 a day, no technical errors, phone journal hash-checked), all of
them number-hunt candidates. Transcribed locally and reviewed: 41 answered by a person (6.9%), in
40 units; about 9 of those were another office (city hall, health secretariat, a company), so an
answer is not a confirmed unit. By source: OpenStreetMap 6/36, CNES 20/249, CNPJ 16/308. 1,008
candidates left; the window ends 02/12. In this repo: `source_scores.*` rerun; `build_page.py` now
takes the dashboard data and `hunt-template.html` shows each candidate's call result, with a new
"Answered, unconfirmed" state for the 32 units where a person answered and did not say it was
another place. The 9 numbers answered by another office are listed in `answered-elsewhere.json` and
count as not working (a stop-time review caught that the first version counted all 41 as found). Outside the repo (dialer pilot): the call
dashboard got an "Origem dos números" switch, so candidates show without changing the official
totals (2,343 numbers, 272 answered: unchanged); a bug in the manual-review filter was fixed. It
had been hiding connected calls with real speech from the reading list; 50 such calls in earlier
batches were never read and may raise the 272.
Checks: official totals recomputed from the rebuilt data match 15/11; both pages rendered headless
(1280 px, origin switch, state filter, reset; no console errors, no overflow); prettier on the
changed docs. Deployed: no. `app/hospitals.json` untouched; validacao.soroja.com.br and the private
Number Hunt artifact not republished (waiting for Edu). Open: Edu's call on re-reading the 50
skipped calls, on republishing, and on how a candidate becomes a published number. Notion: done
(call diary, operations page, Number Hunt page, Call Center status page).

## 2026-11-19 — FAPESP PIPE branch: main merged, budget estimates removed (Claude Code)

Merged main into PR #56 twice (PROGRESS.md conflicts only, both sides kept). To follow the new
no-budget-figures rule, removed the illustrative budget table from `OUTLINE.md` §4.10 and the
estimate in `GAPS.md` D.1; they now point to the Notion budget page. FAPESP's published call caps
and scholarship rates stay, with sources. Checks: prettier, `git diff --check`. Deployed: no.
Open: the earlier PR commit 5d36545 still carries the removed estimates on the public PR branch;
removing them needs a history rewrite, which is Edu's call. Notion: pending.

## 2026-11-19 — No budget figures in GitHub (Edu + Claude Code)

Edu's rule: budget and funding figures may live locally and in Notion, never in GitHub. Checked every
tracked file and the whole git history for the amounts: none found, in files or in any pushed commit.
Trimmed the entry below so it no longer describes the budget's make-up, and added the rule to
`AGENTS.md`. The earlier wording of that entry remains in commit e54dc29; it carries no amounts.
Checks: `git grep` and `git log -S` for the figures, prettier, `git diff --check`. Deployed: no app
change. Notion: pending.

## 2026-11-19 — Budget moved to one internal page; figures removed from materials (Edu + Claude Code)

Edu asked for a single place that explains the budget, a critical look at the 09/11 figure and
three routes, and for no outward material to carry any amount. New internal Notion page under
"3 · Patrocínio institucional / ESG": "Orçamento SoroJá 2027 — análise crítica e três rotas
(interno)". It holds the history, the analysis and three routes. Amounts and findings stay on that
page only: this repo is public.
Removed from materials: the one-pager artifact (ask box, annual budget, quotas; now "value and
format agreed in conversation") and the Notion proposal draft (budget table, per-month and
per-hospital lines, quotas, budget notes; the assumptions were moved to the budget page). The deck
had no budget figures since 11/11; the status page and press pitch never had any.
Checks: route totals recomputed by hand; one-pager rendered headless and still fits one A4 sheet;
proposal draft re-fetched, no "R$" left. Deployed: no app change. Not done: decision logs (sponsorship
page, task page, hub) keep the figures as internal history in Notion; the estimates are unconfirmed.
Notion: done (the budget page itself and the proposal draft).

## 2026-11-19 — Status page images from the deck; press pitch draft (Edu + Claude Code)

Edu found the status page's app image weak. Version 2 of the artifact
(https://claude.ai/artifact/CGfvQw4mrvsqov5if9kXwF) now uses the sponsorship deck's images: the two
real app screens, the night-road photo in a "4h+" card, six press logos and the top of the validation
dashboard. Footer notes that the road photos are AI-generated and why the logos appear. Also drafted
the press pitch in pt-BR as a Notion page under Outreach ("Pauta de imprensa — telefones oficiais dos
hospitais de soro (rascunho)"), with decisions to make before sending and what not to use yet.
Checks: headless render at 1280 and 400 px with the images in place, no horizontal overflow, no
console errors. Deployed: no app change. Nothing sent to anyone. Unverified: the live artifact itself
was not opened after publishing; the old `cover.jpg` and `app-list.png` remain as unused files in it.
Open: Edu's review of the page and the pitch; who gets the story first and whether to warn the
Ministry and secretariats beforehand. Notion: done (sponsorship task page; a "Situação do projeto —
19/11/2026" section at the top of the SoroJá hub; a 19/11 entry in the decision log of
"3 · Patrocínio institucional / ESG").

## 2026-11-19 — Sendable project status page, no budget figure (Edu + Claude Code)

Edu does not want an amount in any material yet; he wants one visual piece to send when someone asks,
showing the work done. New private artifact "SoroJá: onde estamos" (pt-BR):
https://claude.ai/artifact/CGfvQw4mrvsqov5if9kXwF. Sections: origin, the site today, 2026 timeline,
"12 em cada 100", a Brazil map with one dot per hospital coloured by call result, SIH/SINAN/CNES
findings, number hunt in progress, what is missing, ways to support (sponsorship with value agreed in
conversation, support with one state in evidence while the project stays national, institutional
support, introductions and press) and the independence rules. No budget, quotas or price per hospital.
Edu also decided: a press story on the phone findings is worth doing; state-based support is acceptable.
Checks: figures recomputed from `dashboard-data.json` (snapshot 15/11 17:33): 272 / 498 / 1,573 of 2,343
numbers match the dashboard; map has 2,087 hospitals, 1,344 with no working number (dashboard header
says 1,346 of 2,089, used in the text). Headless render at 1280 and 400 px: no horizontal overflow.
Deployed: no app change; artifact is private until Edu shares it. Unverified: the two images were
copied from the one-pager artifact and not seen in the local render. Open: Edu's review of the text,
especially the SIH/SINAN/CNES box; the old one-pager still shows the 09/11 budget figure; no export since 15/11, so
no number-hunt results yet; press pitch not drafted. Notion: done (sponsorship task page).

## 2026-11-19 — Sponsorship proposal review: advice only (Claude Code)

No app, data, deck or Notion change. Read the Notion proposal draft, sponsorship decisions, sponsor
radar, outreach plan and number hunt page, plus the call dashboard data (snapshot 15/11 17:33), and
gave Edu suggestions: per-state quotas priced per hospital, cold emails opened with the
target's own numbers, name-matching the 272 human-answer recordings, an emergency sheet per site as
counterpart, support letters from warm contacts, early source scoring of the number-hunt run.
Commit e3666f1 named by the progress guard is from an earlier session, not this one.
Checks: none needed (read-only). Deployed: no. Unverified: no export after 15/11 exists on this Mac,
so the run started 16/11 was not seen; the "zero human answers in PA, AM, RO, RR, AC" cut may be a
carrier artifact. Open: draft still says "about 2 thousand numbers" and links `educrvz`; the amount
to ask; whether to allow state quotas. Next step: Edu's choice between the per-state packs and the
name match. Notion: pending.

## 2026-11-15 — FAPESP PIPE Phase 1 outline and gaps (Claude Code)

Added `docs/funding/fapesp-pipe/OUTLINE.md` and `GAPS.md`. The outline gives the deadline and
checklist, the call rules with source URLs, a proposed research question (a per-unit reliability
score plus accessibility by antivenom type), pre-proposal drafts within the SAGe character limits,
and an outline with a draft paragraph for each of the 12 Anexo 1 sections. GAPS lists the company,
team, letters, budget, research question and IP items, each marked blocking or nice-to-have.
Main finding: the date 2026-11-16 is the launch of the **PIPE Jornada 8th call ("Geral")**, whose
text is not published yet. Regular PIPE Phase 1 is continuous flow (9 months, ≤R$ 300k). The
previous Jornada general call allowed 12 months and ≤R$ 500k.
Sources: fapesp.br/pipe, /pipe/normas, /pipejornada, /pipe/jornada-tecnologica-2026-fase-1 and the
Anexo 1 template. Gemini was not used: the inputs were small enough to read here.
Checks: `git diff --check`, prettier on the new files.
Deployed: no (docs only). Nothing was submitted and no one was contacted.
Open items:

- `reports/hospital-value-2026-11/` (cited) is still uncommitted in the main checkout.
- The two deep-research files disagree on whether NT 127/2026 uses the terms PEACA/PEASA.
- Notion: pending.

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

## 2026-11-15 — Analysis: SIH venom admissions vs the published list (Edu + Claude Code)

Analysis only; no app, data or process change. Read 36 months of SIH-RD (2023-07 to 2026-06,
972 files, 43.0M admissions), kept venom admissions only (T63.x / X20–X29; non-identifying
fields; raw files deleted). 65,401 venom admissions, 387 in-hospital deaths; 82.5% in a listed
unit (RS 59%, RJ 64% lowest). 180 listed hospitals admit patients but had zero bite admissions;
19 unlisted CNES codes are listed units filing under another code; 69 hospitals with ≥10 bite
admissions are in towns without a listed unit (towns matched by pin location + name, after name-only matching gave false gaps). Report: `reports/sih-admissions-2026-11/`.
Checks: prettier, `git diff --check`, CSVs free of e-mail addresses. Deployed: no.
Open: Edu's decisions on the Notion page. Notion: done ("SIH hospital admissions for venomous
bites vs the published list — analysis (2026-11-15)" under "improve data quality").

## 2026-11-15 — Analysis: open data sources and CNES pin cross-check (Edu + Claude Code)

Analysis only; no app, data or process change. Reviewed the Brazil Open Data Index (144
sources) for SoroJá: CNES, IBGE boundaries, SINAN and SIH are the useful ones. Pilot with a
read-only `scripts/check_cnes_pins.py` (+ tests) in `reports/cnes-pin-check-2026-11/`: 1,764 of
2,279 pins within 1 km of CNES; 200 more than 5 km off; 6 live pins outside their own town
(worst: Barão de Grajaú/MA, 345 km, tier 1); 19 units carry another facility's CNES code.
`.gitignore` covers the cached IBGE meshes. Checks: pytest suite (70 passed), prettier,
`git diff --check`. Deployed: no. Open: Edu's decisions listed on the Notion page (pins, CNES
codes, whether to adopt the checks). Notion: done (page "Open data sources and CNES pin
cross-check — analysis (2026-11-15)" under "improve data quality").

## 2026-11-15 — Sponsorship deck and one-pager: phone check at 100% (Edu + Claude Code)

The call dashboard snapshot from 15/11 17:33 shows the whole dialer base done: 2,343 of 2,343
numbers dialled (2,566 calls including retests, across 2,089 hospitals). Results: 272 (11.6%) answered
by a person, 498 reached but not confirmed, 1,573 failed. In 1,346 of 2,089 hospitals, no number reached
anyone. Updated the deck "SoroJá 2027 — Proposta de patrocínio": slide 7 now says all 2,343 numbers;
slide 8 has a new dashboard screenshot and São Paulo map, SP 68/91/117, data to 15/11. Updated the
"Resumo SoroJá 2027" one-pager: the call band and the source line. The "12 em cada 100" headline still
holds. Checks: figures recomputed from `dashboard-data.json` match the dashboard header; the one-pager
still fits one A4 sheet in a headless render. Deployed: no app change. On Edu's yes, validacao.soroja.com.br was
republished with the 15/11 snapshot (Vercel `soroja-validacao`, dpl_9oUCwnWTuxTikuybLML5CU5h3E9f); live
check: HTTP 200, noindex header, latestEvent 2026-11-15T17:33, audioPath null. Notion: pending.

## 2026-11-15 — Research: what makes a PEA special, and better data sources (Edu + Claude Code)

New `reports/hospital-value-2026-11/FINDINGS.md`. Read NT Conjunta 127/2026 (PEA definition,
PEACA/PEASA, minimum requirements, states own the list). Profiled all 2,252 published CNES codes via
the CNES API: 77% general hospitals, 88% 24h; 107 deactivated or missing. Compared SINAN 2024 microdata
by municipality: 91% of antivenom cases fall in a listed municipality; 154 municipalities with ≥5 cases
have no listed unit (incl. Bento Gonçalves/RS); 206 listed municipalities had zero. RJ state list
(OuvERJ) matches federal 33/33. No app or data change. Checks: `git diff --check`.
Deployed: no. Open: LAI request for SIES/SI-PNI per-unit data; re-verify the 107 CNES-inactive units.
Notion: pending.

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
