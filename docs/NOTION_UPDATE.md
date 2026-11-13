# Notion update — SoroJá project page (pending)

The Notion connector was down on 2026-11-13, so nothing was written to Notion. Paste this
into the SoroJá hub page (link in the local `CLAUDE.md`), following the kit template
`dccrvz/project-kit/docs/NOTION_PROJECT_PAGE.md`.

## Properties

| Property      | Value                                              |
| ------------- | -------------------------------------------------- |
| Slug          | `soroja`                                           |
| Type          | own                                                |
| Status        | active                                             |
| Repo          | https://github.com/educrvz/sos-antiveneno (public) |
| Production    | https://soroja.com.br                              |
| Deploy target | Vercel project `soroja`, auto-deploy from `main`   |
| Vault         | DC Cruz — SoroJá (to be created)                   |
| Owner         | Edu                                                |
| Last change   | 2026-11-13                                         |

## Links

- Runbook: https://github.com/educrvz/sos-antiveneno/blob/main/docs/RUNBOOK.md
- Context: https://github.com/educrvz/sos-antiveneno/blob/main/docs/CONTEXT.md
- Change log: https://github.com/educrvz/sos-antiveneno/blob/main/PROGRESS.md
- Decisions: https://github.com/educrvz/sos-antiveneno/tree/main/docs/decisions
- Local folder: `~/Documents/03 Software & AI/SoroJá`

## Maintenance log rows (newest first)

| Date       | What changed                                                                                             | Who (+ AI tool)   | Deployed | Commit       |
| ---------- | -------------------------------------------------------------------------------------------------------- | ----------------- | -------- | ------------ |
| 2026-11-13 | Adopted into project-kit: CONTEXT, RUNBOOK, ADRs, PROGRESS, check.sh, registry                           | Edu + Claude Code | no       | see PROGRESS |
| 2026-11-13 | Public-corrections finding: 18/20 verified reports confirmed; 81% federal/state divergence (PR/ES/PE/RN) | Edu + Claude Code | no       | see PROGRESS |
| 2026-11-13 | Phone validation (n=50): 12% strict failure, 48% unconfirmed; 24-unit call list                          | Edu + Claude Code | no       | see PROGRESS |

## Open issues

- [ ] Create the "DC Cruz — SoroJá" vault and move the secrets listed in RUNBOOK into it.
- [ ] Call the 24 units in `reports/phone-validation-2026-11/call_list.csv`.
- [ ] The two task-level Notion updates in `reports/*-2026-11/NOTION_UPDATE.md` are also
      still pending.
