#!/usr/bin/env python3
"""Fetch the CNES record (MS open-data API) for each sampled unit -> cnes_raw.json."""
import csv, json, time, urllib.request
from pathlib import Path
OUT = Path(__file__).resolve().parent
API = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos/{}"
cnes = sorted({r["cnes"] for r in csv.DictReader(open(OUT/"offline_checks.csv")) if r["cnes"].isdigit()})
res = {}
for c in cnes:
    for attempt in range(3):
        try:
            with urllib.request.urlopen(API.format(c), timeout=30) as r:
                res[c] = json.load(r); break
        except Exception as e:
            res[c] = {"error": str(e)}; time.sleep(2)
    time.sleep(0.3)
json.dump(res, open(OUT/"cnes_raw.json","w"), ensure_ascii=False, indent=1)
print(len(res), sum("error" in v for v in res.values()))
