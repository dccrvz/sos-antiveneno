#!/usr/bin/env python3
"""Write number-hunt.html: the number hunt dashboard, on the same layout as the call dashboard.

Reads targets.csv (status of every unit's official numbers after the first dialer run),
candidates.csv (numbers found elsewhere) and the dashboard's brazil-map.json, and fills
hunt-template.html. Read-only: nothing here touches app/hospitals.json.

Usage: python3 build_page.py PATH/TO/brazil-map.json [PATH/TO/dashboard-data.json]

With the dashboard data, each candidate also carries the result of the hunt run's own call
to it (latest attempt whose source is the number hunt), so the page shows what was found.
"""
import csv, datetime, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEAD = {"incorrect", "cannot_complete", "changed"}
STATUS = {"human": "answer", "reached": "reach", "failed": "fail", "no_phone": "nophone", "not_dialed": "none"}

hunt = {}  # digits -> (at, category) of the latest hunt-run call
calls = "2026-11-15T17:33:40-03:00"
if len(sys.argv) > 2:
    dash = json.load(open(sys.argv[2]))
    calls = dash["latestEvent"]
    for a in dash["attempts"]:
        if a.get("hunt") and (a["number"] not in hunt or a["at"] > hunt[a["number"]][0]):
            hunt[a["number"]] = (a["at"], a["category"])
loaded = json.load(open(HERE / "loaded-queue-2026-11-15.json"))["numbers"]

cands = {}
for c in csv.DictReader(open(HERE / "candidates.csv")):
    cands.setdefault((c["cnes"], c["hospital_name"]), []).append(
        [c["candidate"], c["source"], c["detail"], c["already_dialled"], hunt.get(c["digits"], ("", ""))[1]])

units = []
for r in csv.DictReader(open(HERE / "targets.csv")):
    cats = [p.rsplit(":", 1)[1] for p in r["number_results"].split("; ") if p]
    dead = r["status"] == "failed" and bool(cats) and all(c in DEAD for c in cats)
    units.append([r["state"], r["city"], r["hospital_name"], r["cnes"], r["phones"],
                  STATUS[r["status"]], r["number_results"], int(dead),
                  round(float(r["lat"]), 5), round(float(r["lng"]), 5), int(r["geocode_tier"] or 0),
                  cands.get((r["cnes"], r["hospital_name"]), [])])

data = {"generated": datetime.date.today().isoformat(), "calls": calls, "loaded": "2026-11-15",
        "loadedNumbers": len(loaded), "dialled": sum(n in hunt for n in loaded),
        "humans": sum(hunt[n][1] == "human" for n in loaded if n in hunt),
        "runFirst": "2026-11-16", "runLast": "2026-12-02", "perDay": 99,
        "queued": len(json.load(open(HERE / "queue-candidates.json"))["candidates"]),
        "fields": ["uf", "city", "name", "cnes", "phones", "before", "res", "dead", "lat", "lng", "tier", "c"],
        "units": units}
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
html = (HERE / "hunt-template.html").read_text()
html = html.replace("__MAP__", Path(sys.argv[1]).read_text()).replace("__DATA__", payload)
(HERE / "number-hunt.html").write_text(html)
print(len(units), "units,", sum(1 for u in units if u[-1]), "with candidates,", data["dialled"], "dialled,",
      data["humans"], "answered by a person,", len(html), "bytes")
