# Number hunt (2026-11-15)

Candidate phone numbers for SoroJá units with no working number. Analysis only: nothing here
changes `app/hospitals.json`. A candidate is unverified until the Android dialer reaches a person
who confirms the unit.

## Run order

The call results live outside the repo (Android pilot dashboard):
`DASH=~/Documents/Codex/2026-10-22/take-a-look-at-this-thread/outputs/dashboard`

1. `python3 build_targets.py $DASH/dashboard-data.json` → `targets.csv` (status per unit)
2. `python3 fetch_cnes.py` → `cnes_raw.json` (gitignored; CNES records carry staff e-mails)
3. `python3 fetch_cnpj.py` → `cnpj_raw.json` (gitignored)
4. `python3 fetch_osm.py` → `osm_raw.json` (gitignored; same for `places_raw.json`)
5. `python3 harvest_history.py` → `history_phones.json`
6. `python3 build_candidates.py $DASH/dashboard-data.json` → `candidates.csv`, `queue-candidates.json`
7. `python3 build_page.py $DASH/brazil-map.json` → `number-hunt.html` (fills `hunt-template.html`, the call
   dashboard's layout: per-state comparison of official numbers against official + candidates)
8. After each phone export and dashboard rebuild: `python3 score_sources.py $DASH/dashboard-data.json`
   → `source_scores.md` / `.csv` (human-answer rate per source and per repair trick). Credit comes
   only from `loaded-queue-2026-11-15.json`, the frozen list of what was loaded on the phone with every
   source per number, so rebuilding `candidates.csv` later never changes past attribution. A new load
   on the phone gets its own `loaded-queue-<date>.json`; a number keeps the credit of the first load
   that contained it, and only calls after that load count.

Optional: `python3 fetch_places.py` (Google Places, ≈US$ 50; needs billing on the Maps project),
then rerun steps 6–7 and add the new numbers to the phone queue.

## Outputs

- `targets.csv`: all 2,279 units with status `human`, `reached`, `failed`, `no_phone` or `not_dialed`.
- `candidates.csv`: one row per unit and candidate, with source, reason and any earlier call result.
- `queue-candidates.json`: numbers never dialled before, each once, in the SoroJá Automático queue
  format (`unit, cnes, city, state, number, raw, extension, source, referenceOnly, incomplete`).
- `number-hunt.html`: self-contained dashboard (map with state zoom, before/after by state, candidate book),
  published as a private artifact. Light theme only.

Methods, findings and open decisions: Notion page "Number Hunt" under the SoroJá hub.
