#!/usr/bin/env python3
"""Compare listed phones with CNES phones (last-8 / last-7 digit match) and municipality."""
import csv, json, re, sys, unicodedata
from pathlib import Path
OUT = Path(__file__).resolve().parent
ibge = {str(m["municipio-id"])[:6]: m["municipio-nome"] for m in json.load(open(sys.argv[1]))}
cn = json.load(open(OUT/"cnes_raw.json"))
norm = lambda s: unicodedata.normalize("NFKD", s or "").encode("ascii","ignore").decode().lower().strip()

def cnes_tokens(raw):
    if not raw: return []
    toks, prev = [], ""
    for part in re.split(r"[/;,]|\s+e\s+", raw):
        d = re.sub(r"\D", "", part)
        if not d: continue
        if len(d) <= 4 and prev:  # suffix shorthand e.g. 6832351188/ 1366
            d = prev[:-len(d)] + d
        toks.append(d); prev = d
    return toks

rows = list(csv.DictReader(open(OUT/"offline_checks.csv")))
for r in rows:
    rec = cn.get(r["cnes"], {})
    raw = rec.get("numero_telefone_estabelecimento")
    toks = cnes_tokens(raw)
    r["cnes_phone_raw"] = raw or ""
    r["cnes_updated"] = rec.get("data_atualizacao") or ""
    r["cnes_name"] = rec.get("nome_fantasia") or ""
    mun = ibge.get(str(rec.get("codigo_municipio") or ""), "")
    r["cnes_municipio"] = mun
    r["cnes_city_matches"] = "" if not mun else ("yes" if norm(mun).replace("'", "") .startswith(norm(r["city"]).replace("'", "")[:8]) else "NO")
    r["cnes_disabled_code"] = rec.get("codigo_motivo_desabilitacao_estabelecimento") or ""
    d = r["digits"]
    if not d: m = ""
    elif not toks: m = "cnes_no_phone"
    elif any(t[-8:] == d[-8:] for t in toks): m = "exact"
    elif any(len(t) >= 7 and d.endswith(t[-7:]) for t in toks): m = "partial7"
    else: m = "differs"
    r["cnes_match"] = m
with open(OUT/"cnes_compare.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
from collections import Counter
print(Counter(r["cnes_match"] for r in rows))
for r in rows:
    if r["cnes_match"] not in ("exact",) or r["cnes_city_matches"]=="NO":
        print(r["uf"], r["city"], "|", r["hospital_name"][:40], "|", r["phone"], "|", r["cnes_phone_raw"], "|", r["cnes_match"], r["cnes_municipio"], r["cnes_city_matches"])
