#!/usr/bin/env python3
"""Fetch OpenStreetMap health facilities in Brazil that carry a phone tag -> osm_raw.json (gitignored)."""
import json, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
Q = """[out:json][timeout:300];
area["ISO3166-1"="BR"][admin_level=2]->.br;
nwr["amenity"~"^(hospital|clinic|doctors)$"](area.br)[~"^(phone|contact:phone)$"~"."];
out center tags;"""
req = urllib.request.Request("https://overpass-api.de/api/interpreter",
                             data=urllib.parse.urlencode({"data": Q}).encode(),
                             headers={"User-Agent": "soroja-number-hunt/1.0"})
with urllib.request.urlopen(req, timeout=400) as r:
    data = json.load(r)
json.dump(data, open(HERE / "osm_raw.json", "w"), ensure_ascii=False)
print(len(data.get("elements", [])), "OSM facilities with phone")
