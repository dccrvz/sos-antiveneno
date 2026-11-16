#!/usr/bin/env python3
"""Write page-data.js for number-hunt.html from targets.csv + candidates.csv + the Brazil outline."""
import csv, json, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEAD = {"incorrect", "cannot_complete", "changed"}
outline = json.load(open(sys.argv[1]))  # dashboard brazil-map.json (paths + proj)
cands = {}
for c in csv.DictReader(open(HERE / "candidates.csv")):
    cands.setdefault((c["cnes"], c["hospital_name"]), []).append(
        [c["candidate"], c["source"], c["detail"], c["already_dialled"]])
units = []
for r in csv.DictReader(open(HERE / "targets.csv")):
    if r["status"] not in ("no_phone", "failed", "not_dialed"):
        continue
    kind = r["status"]
    if kind == "failed":
        cats = [p.rsplit(":", 1)[1] for p in r["number_results"].split("; ") if p]
        kind = "dead" if all(c in DEAD for c in cats) else "failed"
    units.append({
        "uf": r["state"], "city": r["city"], "name": r["hospital_name"], "cnes": r["cnes"],
        "phones": r["phones"], "kind": kind, "res": r["number_results"],
        "lat": float(r["lat"]) if r["lat"] else None, "lng": float(r["lng"]) if r["lng"] else None,
        "c": cands.get((r["cnes"], r["hospital_name"]), []),
    })
src = Counter(c[1] for u in units for c in u["c"])
meta = {"generated": "2026-11-15", "calls_snapshot": "2026-11-15 17:33",
        "total_units": 2279, "kinds": Counter(u["kind"] for u in units),
        "with_cand": sum(1 for u in units if u["c"]), "sources": src,
        "new_numbers": len(json.load(open(HERE / "queue-candidates.json"))["candidates"])}
js = ("window.HUNT=" + json.dumps({"meta": meta, "units": units,
      "map": {"viewBox": outline["viewBox"], "paths": outline["paths"], "proj": outline["proj"]}},
      ensure_ascii=False, separators=(",", ":")) + ";\n")
(HERE / "page-data.js").write_text(js)
print(len(units), "units;", meta)
