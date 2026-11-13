#!/usr/bin/env python3
"""Reproducible 50-unit sample + offline phone checks (format, DDD vs UF).

Method: sort app/hospitals.json by (state, cnes, hospital_name), then
random.Random(SEED).sample(range(N), 50). Simple random sample without
replacement over all published units (including units with no phone).
"""
import csv, json, random, re, sys
from pathlib import Path

SEED = 20261113
N_SAMPLE = 50
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

DDD_BY_UF = {
 "AC":{68},"AL":{82},"AM":{92,97},"AP":{96},"BA":{71,73,74,75,77},"CE":{85,88},
 "DF":{61},"ES":{27,28},"GO":{61,62,64},"MA":{98,99},"MG":{31,32,33,34,35,37,38},
 "MS":{67},"MT":{65,66},"PA":{91,93,94},"PB":{83},"PE":{81,87},"PI":{86,89},
 "PR":{41,42,43,44,45,46},"RJ":{21,22,24},"RN":{84},"RO":{69},"RR":{95},
 "RS":{51,53,54,55},"SC":{47,48,49},"SE":{79},"SP":{11,12,13,14,15,16,17,18,19},
 "TO":{63},
}

def check(phone, uf):
    """Return (digits, ddd, kind, offline_status, reason)."""
    d = re.sub(r"\D", "", phone)
    if d.startswith("0800") and len(d) == 11:
        return d, "", "tollfree", "ok", "0800 toll-free"
    if d.startswith("0") and len(d) in (11, 12):
        d = d[1:]  # trunk prefix
    if len(d) not in (10, 11):
        return d, "", "?", "invalid", f"{len(d)} digits (expected 10/11 with DDD)"
    ddd, sub = int(d[:2]), d[2:]
    if len(sub) == 9:
        kind = "mobile"
        if sub[0] != "9":
            return d, ddd, kind, "invalid", "9-digit subscriber not starting with 9"
    else:
        kind = "landline" if sub[0] in "2345" else ("mobile_old" if sub[0] in "6789" else "?")
        if kind == "?":
            return d, ddd, kind, "invalid", "subscriber starts with 0/1"
        if kind == "mobile_old":
            return d, ddd, kind, "suspect", "8-digit mobile missing leading 9"
    if ddd not in DDD_BY_UF.get(uf, set()):
        return d, ddd, kind, "suspect", f"DDD {ddd} not used in {uf}"
    return d, ddd, kind, "ok", ""

def main():
    h = json.load(open(ROOT / "app/hospitals.json"))
    h.sort(key=lambda x: (x["state"], x.get("cnes") or "", x["hospital_name"]))
    idx = sorted(random.Random(SEED).sample(range(len(h)), N_SAMPLE))
    rows = []
    for i in idx:
        u = h[i]
        phones = u.get("phones") or []
        base = dict(sample_idx=i, uf=u["state"], city=u["city"], cnes=u.get("cnes") or "",
                    hospital_name=u["hospital_name"], n_phones=len(phones))
        if not phones:
            rows.append({**base, "phone": "", "digits": "", "ddd": "", "kind": "",
                         "offline_status": "missing", "offline_reason": "no phone listed"})
        for p in phones:
            d, ddd, kind, st, why = check(p, u["state"])
            rows.append({**base, "phone": p, "digits": d, "ddd": ddd, "kind": kind,
                         "offline_status": st, "offline_reason": why})
    with open(OUT / "offline_checks.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"population={len(h)} seed={SEED} units={len(idx)} phone_rows={len(rows)}")

if __name__ == "__main__":
    main()
