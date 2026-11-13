# 0004 — Repo stays under educrvz

- Date: 2026-11-13 · Status: Accepted · Decided by: Edu

## Context

The project-kit standard puts every project in the `dccrvz` org. Moving
`educrvz/sos-antiveneno` would require rewiring the Vercel project's Git link and the
Apps Script fine-grained token (scoped to this repo), with risk to production and to
the corrections Sheet.

## Decision

The repo stays at `educrvz/sos-antiveneno` (public, ADR 0002). It is registered in the
project-kit registry at this location as an exception to the `dccrvz` default.

## Consequences

No deploy or token rewiring is needed. Revisit with a new ADR if collaborators need
org-level access.
