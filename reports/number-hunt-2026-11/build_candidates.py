#!/usr/bin/env python3
"""Merge candidate numbers for units with no working phone.

Inputs (all in this folder): targets.csv, cnes_raw.json, history_phones.json,
optional cnpj_raw.json and osm_raw.json, plus the call-pilot dashboard-data.json
(path argument) so numbers already dialled are not queued again.

Sources, highest confidence first:
  cnes      phone in the unit's CNES record (Ministry open-data API)
  cnpj      phone of the CNPJ in the CNES record (Receita Federal via BrasilAPI)
  history   a number SoroJá published for this unit in an earlier version
  osm       OpenStreetMap health facility within 1 km with a similar name
  repair    rule-based fix of a dead number (missing mobile 9, wrong DDD for the town)

Outputs: candidates.csv (one row per unit x number) and queue-candidates.json
(SoroJá Automático queue format; only numbers never dialled before).
"""
import csv, json, math, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = {"no_phone", "failed", "not_dialed"}
DEAD = {"incorrect", "cannot_complete", "changed"}  # carrier says the number doesn't exist / changed


def digits(s):
    d = re.sub(r"\D", "", str(s or ""))
    if d.startswith("55") and len(d) in (12, 13):
        d = d[2:]
    return d[1:] if d.startswith("0") and len(d) in (11, 12) else d


# Area codes in use in Brazil (Anatel). Anything else cannot be dialled.
DDDS = set("11 12 13 14 15 16 17 18 19 21 22 24 27 28 31 32 33 34 35 37 38 41 42 43 44 45 46 47 "
           "48 49 51 53 54 55 61 62 63 64 65 66 67 68 69 71 73 74 75 77 79 81 82 83 84 85 86 87 "
           "88 89 91 92 93 94 95 96 97 98 99".split())


def valid(d):
    if len(d) == 11 and d.startswith("0800"):
        return True
    return d[:2] in DDDS and ((len(d) == 10 and d[2] in "2345") or (len(d) == 11 and d[2] == "9"))


def raw_fmt(d):
    if d.startswith("0800"):
        return f"0800 {d[4:7]} {d[7:]}"
    return f"({d[:2]}) {d[2:-4]}-{d[-4:]}"


def parse_free(raw, ddd_guess):
    """Turn a free-text registry phone into dialable numbers, with a note on any repair.

    Handles numbers from before the 8-digit landline change (7 local digits: a leading 3
    was added) and numbers written without the area code."""
    out, last = [], ""
    for piece in re.split(r"[/;,]| e | ou ", raw or ""):
        d = re.sub(r"\D", "", piece)
        if not d:
            continue
        if d.startswith("0800") and len(d) == 11:
            out.append((d, "")); continue
        trunk = d.startswith("0") and not d.startswith(("0800", "0300")) and len(d) >= 10
        if trunk:  # trunk zero(s) before the area code: 0 92 6634663; Receita pads to 0095 6231044
            d = d.lstrip("0")
        m = None if trunk else re.match(r"\s*\(?\s*0?(\d{2})\s*\)", piece)
        if trunk:
            ddd, local = d[:2], d[2:]
        elif m:
            ddd, local = m.group(1), d[len(d) - len(re.sub(r"\D", "", piece[m.end():])):]
        elif len(d) in (10, 11):
            ddd, local = d[:2], d[2:]
        else:
            ddd, local = last or ddd_guess, d
        if not ddd:
            continue
        note = "" if trunk or m or len(d) in (10, 11) or last else f"sem DDD; DDD {ddd} do município"
        if ddd not in DDDS and ddd_guess:
            note = (note + "; " if note else "") + f"DDD {ddd} não existe, usado {ddd_guess} do município"
            ddd = ddd_guess
        last = ddd
        if len(local) == 7:
            local, note = "3" + local, (note + "; " if note else "") + "número antigo de 7 dígitos, +3 na frente"
        elif len(local) == 8 and local[0] in "6789":
            local, note = "9" + local, (note + "; " if note else "") + "celular sem o 9"
        out.append((ddd + local, note))
    return out


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    stop = {"de", "da", "do", "das", "dos", "e", "hospital", "municipal", "unidade", "mista",
            "saude", "regional", "estadual", "pronto", "socorro", "upa", "ltda", "s", "a"}
    return {w for w in s.split() if w not in stop and len(w) > 2}


def hist_norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def km(a, b, c, d):
    r = math.pi / 180
    return 6371 * 2 * math.asin(math.sqrt(math.sin((c - a) * r / 2) ** 2 +
           math.cos(a * r) * math.cos(c * r) * math.sin((d - b) * r / 2) ** 2))


def load(name, default):
    p = HERE / name
    return json.load(open(p)) if p.exists() else default


def main(dash_path):
    rows = list(csv.DictReader(open(HERE / "targets.csv")))
    cnes_count = Counter(r["cnes"] for r in rows)
    cnes = load("cnes_raw.json", {})
    cnpj = load("cnpj_raw.json", {})
    hist = load("history_phones.json", {})
    osm = load("osm_raw.json", {}).get("elements", [])
    dash = json.load(open(dash_path))
    dialled = {}
    for a in dash["attempts"]:
        n = digits(a["number"])
        if n not in dialled or a["at"] > dialled[n][0]:
            dialled[n] = (a["at"], a["category"])

    # Town DDD = most common DDD among numbers that reached someone in that town.
    town_ddd = defaultdict(Counter)
    for r in rows:
        for part in filter(None, r["number_results"].split("; ")):
            n, cat = part.rsplit(":", 1)
            if cat in ("human", "ivr", "voicemail", "unclear"):
                town_ddd[(r["state"], r["city"])][n[:2]] += 1
    with_ddd = []
    for r in rows:
        nums = [p.split(":")[0] for p in r["number_results"].split("; ") if p]
        if nums and r["lat"]:
            with_ddd.append((float(r["lat"]), float(r["lng"]), nums[0][:2]))

    def ddd_for(r):
        best = town_ddd.get((r["state"], r["city"]))
        if best:
            return best.most_common(1)[0][0]
        if not r["lat"]:
            return ""
        lat, lng = float(r["lat"]), float(r["lng"])
        return min(with_ddd, key=lambda x: (x[0] - lat) ** 2 + (x[1] - lng) ** 2)[2]

    osm_pts = []
    for e in osm:
        t = e.get("tags", {})
        lat = e.get("lat") or e.get("center", {}).get("lat")
        lon = e.get("lon") or e.get("center", {}).get("lon")
        ph = t.get("phone") or t.get("contact:phone") or ""
        if lat and ph:
            osm_pts.append((lat, lon, norm(t.get("name", "")), ph, e["type"][0] + str(e["id"])))

    out = []
    for r in rows:
        if r["status"] not in TARGET:
            continue
        published = {p.split(":")[0] for p in r["number_results"].split("; ") if p}
        found = {}  # digits -> (source, detail)

        def add(d, src, detail):
            if valid(d) and d not in published and d not in found:
                found[d] = (src, detail)

        rec = cnes.get(r["cnes"], {})
        guess = ddd_for(r)
        for d, note in parse_free(rec.get("numero_telefone_estabelecimento"), guess):
            add(d, "cnes", f"CNES {r['cnes']}" + (f" ({note})" if note else ""))
        cj = cnpj.get(rec.get("numero_cnpj") or rec.get("numero_cnpj_entidade") or "", {})
        for k in ("ddd_telefone_1", "ddd_telefone_2"):
            for d, note in parse_free(cj.get(k) or "", guess):
                add(d, "cnpj", f"CNPJ {cj.get('cnpj','')} {(cj.get('razao_social') or '')[:40]}" + (f" ({note})" if note else ""))
        # Same key as harvest_history.py. Fall back to CNES alone only when no other
        # current unit shares the code (shared CNES codes must not mix units).
        hkey = f"{r['cnes']}|{hist_norm(r['hospital_name'])}"
        hkeys = [hkey] if hkey in hist else (
            [k for k in hist if r["cnes"] and k.split("|")[0] == r["cnes"]]
            if cnes_count[r["cnes"]] == 1 else [])
        for hk in hkeys:
            for d, date in hist[hk].items():
                add(d, "history", f"publicado em versão de {date}")
        if r["lat"]:
            lat, lng, nm = float(r["lat"]), float(r["lng"]), norm(r["hospital_name"])
            for (a, b, on, ph, oid) in osm_pts:
                if abs(a - lat) < 0.02 and abs(b - lng) < 0.02 and km(lat, lng, a, b) <= 1 and (nm & on or not nm):
                    for d, note in parse_free(ph.replace("+55", ""), guess):
                        add(d, "osm", f"OSM {oid}" + (f" ({note})" if note else ""))
        # Rule-based repairs of numbers the carrier said don't exist.
        for part in filter(None, r["number_results"].split("; ")):
            n, cat = part.rsplit(":", 1)
            if cat not in DEAD:
                continue
            if len(n) == 10 and n[2] in "6789":
                add(n[:2] + "9" + n[2:], "repair", f"celular sem o 9: {n}")
            ddd = ddd_for(r)
            if ddd:
                if ddd != n[:2]:
                    add(ddd + n[2:], "repair", f"DDD {n[:2]}→{ddd} (DDD da cidade)")
        for d, (src, detail) in found.items():
            prev = dialled.get(d)
            out.append({
                "state": r["state"], "city": r["city"], "hospital_name": r["hospital_name"],
                "cnes": r["cnes"], "unit_status": r["status"], "candidate": raw_fmt(d),
                "digits": d, "source": src, "detail": detail,
                "already_dialled": prev[1] if prev else "",
            })
    shared = Counter(c["digits"] for c in out)
    for c in out:
        if shared[c["digits"]] >= 3:
            c["detail"] += f" · mesmo número em {shared[c['digits']]} unidades (secretaria/escritório, não linha direta)"
    order = {"cnes": 0, "cnpj": 1, "history": 2, "osm": 3, "repair": 4}
    out.sort(key=lambda x: (x["state"], x["city"], x["hospital_name"], order[x["source"]]))
    with open(HERE / "candidates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        w.writeheader(); w.writerows(out)
    seen, queue = set(), []
    for c in sorted(out, key=lambda x: order[x["source"]]):
        if c["already_dialled"] or c["digits"] in seen:
            continue
        seen.add(c["digits"])
        queue.append({"unit": c["hospital_name"], "cnes": c["cnes"], "city": c["city"],
                      "state": c["state"], "number": c["digits"], "raw": c["candidate"],
                      "extension": "", "source": f"Caça de números · {c['source']} · {c['detail']}",
                      "referenceOnly": False, "incomplete": False})
    json.dump({"source": "SoroJá number hunt 2026-11 (candidates never dialled)",
               "created": "2026-11-15", "candidates": queue},
              open(HERE / "queue-candidates.json", "w"), ensure_ascii=False, indent=1)
    units = {(c["cnes"], c["hospital_name"]) for c in out}
    print(len(out), "candidates;", len(units), "units with ≥1 candidate;", len(queue), "new numbers to dial")
    print("by source:", Counter(c["source"] for c in out))
    print("by unit status:", Counter(r["unit_status"] for r in {(c["cnes"], c["hospital_name"]): c for c in out}.values()))
    print("already dialled:", Counter(c["already_dialled"] for c in out if c["already_dialled"]))


if __name__ == "__main__":
    main(sys.argv[1])
