# 0003 — Official data first, corrections as traceable layers

- Date: 2026-05-14 (recorded 2026-11-13) · Status: Accepted · Decided by: Edu

## Context

The Ministry PESA PDFs are the only national source, but they contain wrong pins,
phones and closed units, and state lists often disagree with them. Silent edits would
make refreshes destroy fixes and make the data impossible to audit.

## Decision

The Ministry PESA extraction is the canonical layer. Location overrides, community
notes, official temporary units and verified state corrections are separate files
applied on top at build time. Every state promotion is gated by `scripts/refresh_diff.py`.

## Consequences

Refreshes keep community fixes; every published change can be traced to its source.
Overrides must never be keyed by a CNES shared by several facilities.
