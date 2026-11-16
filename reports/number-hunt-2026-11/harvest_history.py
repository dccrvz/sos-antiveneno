#!/usr/bin/env python3
"""Collect every phone ever published for each unit in git history of app/hospitals.json.

Keyed by (cnes, normalized hospital name) so shared CNES codes don't mix units.
Writes history_phones.json: {key: {digits: first_commit_date}}.
"""
import json, re, subprocess, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def digits(s):
    d = re.sub(r"\D", "", s or "")
    return d[1:] if d.startswith("0") and len(d) in (11, 12) else d


out = {}
for path in ("app/hospitals.json", "hospitals.json"):
    log = subprocess.run(["git", "log", "--format=%H %as", "--", path], cwd=ROOT,
                         capture_output=True, text=True).stdout.split("\n")
    for line in filter(None, log):
        sha, date = line.split()
        blob = subprocess.run(["git", "show", f"{sha}:{path}"], cwd=ROOT,
                              capture_output=True, text=True).stdout
        try:
            data = json.loads(blob)
        except ValueError:
            continue
        rows = data if isinstance(data, list) else data.get("hospitals", [])
        for u in rows:
            key = f"{u.get('cnes','')}|{norm(u.get('hospital_name') or u.get('name'))}"
            phones = u.get("phones") or u.get("phone") or []
            if isinstance(phones, str):
                phones = re.split(r"[/;,]", phones)
            for p in phones:
                d = digits(p)
                if len(d) >= 10:
                    prev = out.setdefault(key, {}).get(d)
                    if prev is None or date < prev:
                        out[key][d] = date
json.dump(out, open(HERE / "history_phones.json", "w"), ensure_ascii=False, indent=0)
print(len(out), "units;", sum(len(v) for v in out.values()), "unit-number pairs")
