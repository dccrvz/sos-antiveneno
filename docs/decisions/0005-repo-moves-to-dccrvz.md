# 0005 — Repo moves to the dccrvz org

- Date: 2026-11-14 · Status: Accepted · Decided by: Edu

## Context

ADR 0004 kept the repo under the personal `educrvz` account to avoid rewiring Vercel
and the Apps Script token. On 2026-11-14 Edu decided to put SoroJá under the D.C. Cruz
umbrella for funding (the FAPESP PIPE call opens 2026-11-16), which means the code
must live in the company's GitHub org, `dccrvz`.

## Decision

The repo was transferred to `dccrvz/sos-antiveneno` on 2026-11-14. It stays public and
open source (ADR 0002) and keeps its name. This supersedes ADR 0004.

## Consequences

- GitHub redirects `educrvz/sos-antiveneno` (web, git, API) to the new location. Never
  create a repo named `sos-antiveneno` on `educrvz`: it would break that redirect.
- The Vercel project `soroja` must be linked to `dccrvz/sos-antiveneno`, which needs the
  Vercel GitHub app installed on the `dccrvz` org.
- The Apps Script fine-grained PAT must have resource owner `dccrvz`, and the script
  property `GITHUB_REPO` must be `dccrvz/sos-antiveneno`.
- The project now follows the project-kit default (all projects in `dccrvz`).
