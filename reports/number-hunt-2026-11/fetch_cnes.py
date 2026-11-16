#!/usr/bin/env python3
"""Fetch the CNES open-data record for every target unit -> cnes_raw.json (gitignored).

Targets = status no_phone, failed or not_dialed in targets.csv.
"""
import csv, json, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
API = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos/{}"
rows = list(csv.DictReader(open(HERE / "targets.csv")))
cnes = sorted({r["cnes"] for r in rows
               if r["status"] in ("no_phone", "failed", "not_dialed") and r["cnes"].isdigit()})


def get(c):
    err = ""
    for a in range(3):
        try:
            with urllib.request.urlopen(API.format(c), timeout=30) as r:
                return c, json.load(r)
        except Exception as e:
            err = str(e); time.sleep(2 + a * 3)
    return c, {"error": err}


with ThreadPoolExecutor(6) as ex:
    res = dict(ex.map(get, cnes))
json.dump(res, open(HERE / "cnes_raw.json", "w"), ensure_ascii=False)
print(len(cnes), "fetched;", sum("error" in v for v in res.values()), "errors")
