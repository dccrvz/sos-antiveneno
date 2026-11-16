#!/usr/bin/env python3
"""Score each candidate source by what the dialer got when it called the number.

Reads the call dashboard (dashboard-data.json, rebuilt after each phone export) and the
frozen snapshot of what was loaded on the phone (loaded-queue-*.json). Attribution comes
only from that snapshot, so rebuilding candidates.csv later never changes the credit for
calls already made. A number found through several sources credits each of them.

Outcome per number = its latest attempt:
  human    a person answered (the only result that can confirm a unit)
  reached  menu, voicemail or unclear audio
  dead     carrier says the number doesn't exist / changed / can't complete
  failed   network, blocked, congestion, unavailable, technical

Writes source_scores.csv and source_scores.md. Usage:
  python3 score_sources.py PATH/TO/dashboard-data.json
"""
import csv, json, sys
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REACHED = {"ivr", "voicemail", "unclear"}
DEAD = {"incorrect", "cannot_complete", "changed"}


def outcome(cat):
    return "human" if cat == "human" else "reached" if cat in REACHED else "dead" if cat in DEAD else "failed"


def variant(source, detail):
    """Split a source by the repair it needed, so the report shows which tricks work."""
    d = detail.lower()
    tags = []
    if "secretaria/escritório" in d:
        tags.append("shared office line")
    if "7 dígitos" in d:
        tags.append("old 7-digit +3")
    if "sem ddd" in d:
        tags.append("area code added")
    if "não existe" in d and "ddd" in d:
        tags.append("bad area code replaced")
    if "celular sem o 9" in d:
        tags.append("mobile 9 added")
    if source == "repair" and "→" in detail:
        tags.append("town area code")
    return source + (" · " + ", ".join(tags) if tags else " · as published")


def main(dash_path):
    dash = json.load(open(dash_path))
    latest = {}
    for a in dash["attempts"]:
        if not a.get("source", "").startswith("Caça de números"):
            continue
        n = a["number"]
        if n not in latest or a["at"] > latest[n]["at"]:
            latest[n] = a
    # Each number is credited only by the first snapshot that loaded it, and only calls made
    # after that load count. A later load can add new numbers but never re-credits old ones.
    by_num = defaultdict(list)  # digits -> [(source, variant, unit key, unit status)]
    loaded_at = {}
    snaps = [json.load(open(p)) for p in HERE.glob("loaded-queue-*.json")]
    for snap in sorted(snaps, key=lambda x: datetime.fromisoformat(x["loaded"])):
        t = datetime.fromisoformat(snap["loaded"])
        for n, v in snap["numbers"].items():
            if n in loaded_at:
                continue
            loaded_at[n] = t
            by_num[n] = [(c["source"], c["variant"], tuple(c["unit"]), c["unit_status"]) for c in v["credits"]]
    latest = {n: a for n, a in latest.items()
              if n not in loaded_at or datetime.fromisoformat(a["at"]) >= loaded_at[n]}
    queued_nums = set(by_num)
    unknown = [n for n in latest if n not in by_num]
    if unknown:
        print(f"warning: {len(unknown)} hunt attempts have no loaded-queue snapshot entry")

    def table(keyfn):
        stats = defaultdict(lambda: {"queued": 0, "dialled": 0, **{o: 0 for o in ("human", "reached", "dead", "failed")}})
        for n in queued_nums:
            keys = {keyfn(x) for x in by_num.get(n, [])}
            for k in keys:
                stats[k]["queued"] += 1
                if n in latest:
                    stats[k]["dialled"] += 1
                    stats[k][outcome(latest[n]["category"])] += 1
        return stats

    by_source, by_variant = table(lambda x: x[0]), table(lambda x: x[1])
    by_status = table(lambda x: x[3])
    units_found = {x[2] for n, a in latest.items() if a["category"] == "human" for x in by_num.get(n, [])}

    rows = []
    for level, stats in (("source", by_source), ("variant", by_variant), ("unit status", by_status)):
        for k, s in sorted(stats.items(), key=lambda kv: -kv[1]["queued"]):
            d = s["dialled"] or 1
            rows.append({"level": level, "name": k, **s,
                         "human_pct": round(100 * s["human"] / d, 1) if s["dialled"] else "",
                         "reached_pct": round(100 * s["reached"] / d, 1) if s["dialled"] else "",
                         "dead_pct": round(100 * s["dead"] / d, 1) if s["dialled"] else ""})
    with open(HERE / "source_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader(); w.writerows(rows)

    lines = [f"# Number hunt: source scores ({dash.get('latestEvent','')[:16]})", "",
             f"{sum(n in latest for n in queued_nums)} of {len(queued_nums)} candidate numbers dialled. "
             f"{sum(latest[n]['category']=='human' for n in queued_nums if n in latest)} answered by a person, "
             f"covering {len(units_found)} units. A person answering is not yet a confirmed unit: "
             "check the recording before publishing.", "",
             "Human % is the share of dialled numbers a person answered. Previous baseline: "
             "11.6% on the first pass of official numbers, about 1% on retries.", ""]
    for level in ("source", "variant", "unit status"):
        lines += [f"## By {level}", "", "| Name | Queued | Dialled | Human | Human % | Reached % | Dead % |",
                  "|---|---:|---:|---:|---:|---:|---:|"]
        for r in rows:
            if r["level"] == level:
                lines.append(f"| {r['name']} | {r['queued']} | {r['dialled']} | {r['human']} | "
                             f"{r['human_pct']} | {r['reached_pct']} | {r['dead_pct']} |")
        lines.append("")
    (HERE / "source_scores.md").write_text("\n".join(lines))
    print("\n".join(lines[:4]))


if __name__ == "__main__":
    main(sys.argv[1])
