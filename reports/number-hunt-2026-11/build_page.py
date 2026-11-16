#!/usr/bin/env python3
"""Write number-hunt.html: the number hunt dashboard, on the same layout as the call dashboard.

Reads targets.csv (status of every unit's official numbers after the first dialer run),
candidates.csv (numbers found elsewhere) and the dashboard's brazil-map.json, and fills
hunt-template.html. Read-only: nothing here touches app/hospitals.json.

Usage: python3 build_page.py PATH/TO/brazil-map.json
"""
import csv, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEAD = {"incorrect", "cannot_complete", "changed"}
STATUS = {"human": "answer", "reached": "reach", "failed": "fail", "no_phone": "nophone", "not_dialed": "none"}

cands = {}
for c in csv.DictReader(open(HERE / "candidates.csv")):
    cands.setdefault((c["cnes"], c["hospital_name"]), []).append(
        [c["candidate"], c["source"], c["detail"], c["already_dialled"]])

units = []
for r in csv.DictReader(open(HERE / "targets.csv")):
    cats = [p.rsplit(":", 1)[1] for p in r["number_results"].split("; ") if p]
    dead = r["status"] == "failed" and bool(cats) and all(c in DEAD for c in cats)
    units.append([r["state"], r["city"], r["hospital_name"], r["cnes"], r["phones"],
                  STATUS[r["status"]], r["number_results"], int(dead),
                  round(float(r["lat"]), 5), round(float(r["lng"]), 5), int(r["geocode_tier"] or 0),
                  cands.get((r["cnes"], r["hospital_name"]), [])])

data = {"generated": "2026-11-16", "calls": "2026-11-15T17:33:40-03:00", "loaded": "2026-11-15",
        "runFirst": "2026-11-16", "runLast": "2026-12-02", "perDay": 99,
        "queued": len(json.load(open(HERE / "queue-candidates.json"))["candidates"]),
        "fields": ["uf", "city", "name", "cnes", "phones", "before", "res", "dead", "lat", "lng", "tier", "c"],
        "units": units}
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
html = (HERE / "hunt-template.html").read_text()
html = html.replace("__MAP__", Path(sys.argv[1]).read_text()).replace("__DATA__", payload)
(HERE / "number-hunt.html").write_text(html)
print(len(units), "units,", sum(1 for u in units if u[-1]), "with candidates,", len(html), "bytes")
