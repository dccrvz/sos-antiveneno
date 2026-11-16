#!/usr/bin/env python3
"""Map units without a working phone number.

Joins the published app/hospitals.json with the Android call-pilot results
(dashboard-data.json, outside the repo) and writes targets.csv: one row per
unit with its phone status.

Status per number = category of its latest attempt:
  human            -> answered by a person
  ivr/voicemail/unclear -> reached, not confirmed
  everything else  -> failed (carrier announcement, network, blocked, ...)
Status per unit = best status among its numbers, or no_phone / not_dialed.

Usage: python3 build_targets.py PATH/TO/dashboard-data.json
"""
import csv, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REACHED = {"ivr", "voicemail", "unclear"}
RANK = {"human": 0, "reached": 1, "failed": 2, "not_dialed": 3}


def digits(s):
    d = re.sub(r"\D", "", s or "")
    return d[1:] if d.startswith("0") and len(d) in (11, 12) else d


def main(dash_path):
    units = json.load(open(ROOT / "app" / "hospitals.json"))
    dash = json.load(open(dash_path))
    latest = {}  # number -> (at, category)
    for a in dash["attempts"]:
        n = digits(a["number"])
        if n not in latest or a["at"] > latest[n][0]:
            latest[n] = (a["at"], a["category"], a.get("id", ""))

    def num_status(n):
        if n not in latest:
            return "not_dialed"
        c = latest[n][1]
        return "human" if c == "human" else "reached" if c in REACHED else "failed"

    rows = []
    for u in units:
        nums = [digits(p) for p in u["phones"] if digits(p)]
        if not nums:
            status, detail = "no_phone", ""
        else:
            sts = [num_status(n) for n in nums]
            status = min(sts, key=RANK.get)
            detail = "; ".join(
                f"{n}:{latest[n][1] if n in latest else 'not_dialed'}" for n in nums
            )
        rows.append({
            "state": u["state"], "city": u["city"], "hospital_name": u["hospital_name"],
            "cnes": u["cnes"], "phones": " | ".join(u["phones"]), "status": status,
            "number_results": detail, "lat": u["lat"], "lng": u["lng"],
            "geocode_tier": u["geocode_tier"], "address": u["address"],
        })
    with open(HERE / "targets.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(len(rows), Counter(r["status"] for r in rows))


if __name__ == "__main__":
    main(sys.argv[1])
