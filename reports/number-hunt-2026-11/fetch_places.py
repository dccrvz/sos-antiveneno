#!/usr/bin/env python3
"""Google Places (New) Text Search for every target unit, asking for the phone field.

One request per unit: "<name>, <city>, <UF>, Brasil", biased 25 km around the pin.
Field mask is limited to what we need. Cost is the Text Search Enterprise SKU (phone
fields), roughly US$ 35 per 1,000 requests. Resume-safe: units already in
places_raw.json (gitignored) are skipped.

Usage: python3 fetch_places.py [--limit N]
"""
import csv, json, os, subprocess, sys, time, urllib.error, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "places_raw.json"
URL = "https://places.googleapis.com/v1/places:searchText"
MASK = ("places.id,places.displayName,places.formattedAddress,places.location,"
        "places.primaryType,places.nationalPhoneNumber,places.internationalPhoneNumber,"
        "places.businessStatus")


def key():
    if os.environ.get("GOOGLE_MAPS_API_KEY"):
        return os.environ["GOOGLE_MAPS_API_KEY"]
    user = subprocess.check_output(["whoami"]).decode().strip()
    return subprocess.check_output(["security", "find-generic-password", "-s",
                                    "google_maps_api_key", "-a", user, "-w"]).decode().strip()


def search(k, body):
    req = urllib.request.Request(URL, method="POST", data=json.dumps(body).encode(), headers={
        "Content-Type": "application/json", "X-Goog-Api-Key": k, "X-Goog-FieldMask": MASK})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"error": raw}


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    done = json.load(open(OUT)) if OUT.exists() else {}
    rows = [r for r in csv.DictReader(open(HERE / "targets.csv"))
            if r["status"] in ("no_phone", "failed", "not_dialed")]
    k, n = key(), 0
    for r in rows:
        uid = f"{r['cnes']}|{r['hospital_name']}"
        if uid in done:
            continue
        if limit is not None and n >= limit:
            break
        body = {"textQuery": f"{r['hospital_name']}, {r['city']}, {r['state']}, Brasil",
                "languageCode": "pt-BR", "regionCode": "BR", "maxResultCount": 3}
        if r["lat"]:
            body["locationBias"] = {"circle": {"center": {"latitude": float(r["lat"]),
                                    "longitude": float(r["lng"])}, "radius": 25000.0}}
        status, data = search(k, body)
        if status != 200:
            print("HTTP", status, json.dumps(data)[:400]); break
        done[uid] = data.get("places", [])
        n += 1
        if n % 100 == 0:
            json.dump(done, open(OUT, "w"), ensure_ascii=False); print(n, "done")
        time.sleep(0.12)
    json.dump(done, open(OUT, "w"), ensure_ascii=False)
    print(n, "requests this run;", len(done), "units total;",
          sum(1 for v in done.values() if any(p.get("nationalPhoneNumber") for p in v)), "with a phone")


if __name__ == "__main__":
    main()
