# 0002 — Public, open-source repository

- Date: 2026-08-03 (recorded 2026-11-13) · Status: Accepted · Decided by: Edu

## Context

SoroJá is a public-interest emergency tool built on public Ministry of Health data.
Trust, auditability and outside corrections (doctors, secretariats, the public) matter
more than secrecy. The project-kit default is a private repo in the `dccrvz` org.

## Decision

The repo stays public and open source under the name `sos-antiveneno`. No root `LICENSE`
file is added without asking; the footer carries the open-source statement. This
overrides the kit's "private repo" default for this project.

## Consequences

No secrets, private IDs or personal data may ever reach git: private operational IDs
live in the gitignored `CLAUDE.md`, the Notion URL stays out of the repo, and CNES raw
dumps (staff e-mails) are git-ignored. Any move to `dccrvz` must keep the repo public.
