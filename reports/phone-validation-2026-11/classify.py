#!/usr/bin/env python3
"""Final classification (valid / suspect / invalid / missing) + Wilson 95% CI.

Rules (per listed phone):
  valid   = well-formed, DDD matches the municipality, and corroborated by an
            independent source (CNES last-8 digits, CNES with a dropped digit,
            or a non-MS directory / official page).
  suspect = well-formed but not corroborated (CNES lists another number or
            none, nothing found on the web), or DDD inconsistent with the city.
  invalid = cannot connect as listed (malformed, or wrong DDD for the city
            while the same subscriber number is listed elsewhere with the
            correct DDD).
  missing = unit has no phone listed.
Unit-level: OK if >= 1 valid phone; otherwise the unit's worst-best status.
The MS/PESA list is NOT counted as corroboration (it is SoroJá's own source).
"""
import csv, math
from collections import Counter, defaultdict
from pathlib import Path
OUT = Path(__file__).resolve().parent

# Manual evidence from web checks on 2026-11-13, keyed by listed digits.
MANUAL = {
 "9734156240": ("valid", "listed 3415-6240 also in cidadesdomeubrasil.com.br (CNES-derived directory); current CNES shows a mobile"),
 "5121021000": ("valid", "benditoguia.com.br lists (51) 2102-1000; CNES 2102-1060 is same PBX range"),
 "4432847200": ("invalid", "Marechal Cândido Rondon uses DDD 45; vymaps lists +55 45 3284-7200 -> dialing (44) misroutes"),
 "71987473089": ("suspect", "DDD 71 (Salvador) for a Jequié unit (DDD 73); CNES lists (73) 4103-0025"),
 "1155133132": ("suspect", "contradicted by 2 official sources: CNES (11) 5511-6410 and SMS-SP page 5812-4688"),
 "1837044255": ("suspect", "CNES (18) 3704-4155 differs by one digit - possible transcription error"),
 "4335271022": None,
}
NOTES_MISSING = {
 "5982146": "CNES record disabled (motivo 08) and points to Pari-Cachoeira PEF; listing may be the wrong establishment",
 "2312123": "CNES has (94) 3785-1287 - easy fix candidate",
 "": "row has no CNES, no address and no phone in the published data",
}

def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (max(0, c-h), min(1, c+h))

rows = list(csv.DictReader(open(OUT/"cnes_compare.csv")))
for r in rows:
    m, st = r["cnes_match"], r["offline_status"]
    if st == "missing":
        r["status"], r["evidence"] = "missing", NOTES_MISSING.get(r["cnes"], "no phone listed")
        if r["cnes_phone_raw"]: r["evidence"] += f"; CNES phone: {r['cnes_phone_raw']}"
    elif st == "invalid":
        r["status"], r["evidence"] = "invalid", r["offline_reason"]
    elif r["digits"] in MANUAL and MANUAL[r["digits"]]:
        r["status"], r["evidence"] = MANUAL[r["digits"]]
    elif m == "exact":
        r["status"], r["evidence"] = "valid", f"matches CNES ({r['cnes_phone_raw']}, upd {r['cnes_updated']})"
    elif m == "partial7":
        r["status"], r["evidence"] = "valid", f"matches CNES with dropped leading digit ({r['cnes_phone_raw']})"
    elif m == "cnes_no_phone":
        r["status"], r["evidence"] = "suspect", "CNES has no phone; no independent web source found"
    else:
        r["status"], r["evidence"] = "suspect", f"CNES lists {r['cnes_phone_raw']} (upd {r['cnes_updated']}); no independent web corroboration found"
    if r["cnes_name"] and r["cnes"] == "2086336":
        r["evidence"] += "; NB CNES name is 'Hospital Infantil Menino Jesus' (name differs from listing)"
    if r["cnes"] == "4051165":
        r["evidence"] += "; CNES itself has DDD 45 (wrong for Assis Chateaubriand, DDD 44)"

cols = ["sample_idx","uf","city","cnes","hospital_name","phone","digits","kind","status","evidence",
        "offline_status","offline_reason","cnes_match","cnes_phone_raw","cnes_updated","cnes_name","cnes_municipio"]
with open(OUT/"phone_validation_sample50.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

rank = {"valid":0,"suspect":1,"invalid":2,"missing":3}
units = defaultdict(list)
for r in rows: units[r["sample_idx"]].append(r)
ustat = {}
for k, rs in units.items():
    ustat[k] = (rs[0]["uf"], min((r["status"] for r in rs), key=rank.get))
n = len(ustat)
uc = Counter(s for _, s in ustat.values())
pc = Counter(r["status"] for r in rows if r["status"] != "missing")
lines = [f"units n={n}: " + ", ".join(f"{s}={uc[s]}" for s in rank)]
for label, bad in [("strict (missing+invalid)", {"missing","invalid"}),
                   ("broad (not confirmed: missing+invalid+suspect)", {"missing","invalid","suspect"})]:
    k = sum(uc[s] for s in bad); lo, hi = wilson(k, n)
    lines.append(f"failure {label}: {k}/{n} = {k/n:.0%} (Wilson 95% CI {lo:.0%}-{hi:.0%})")
np_ = sum(pc.values())
lines.append(f"phones n={np_}: " + ", ".join(f"{s}={pc[s]}" for s in ("valid","suspect","invalid")))
k = pc["suspect"]+pc["invalid"]; lo, hi = wilson(k, np_)
lines.append(f"phone-level not confirmed: {k}/{np_} = {k/np_:.0%} (CI {lo:.0%}-{hi:.0%})")
byuf = defaultdict(Counter)
for uf, s in ustat.values(): byuf[uf][s] += 1
with open(OUT/"by_uf.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["uf","units","valid","suspect","invalid","missing","not_confirmed_pct"])
    for uf in sorted(byuf):
        c = byuf[uf]; t = sum(c.values())
        w.writerow([uf,t,c["valid"],c["suspect"],c["invalid"],c["missing"],round(100*(t-c["valid"])/t)])
open(OUT/"summary.txt","w").write("\n".join(lines)+"\n")
print("\n".join(lines))
