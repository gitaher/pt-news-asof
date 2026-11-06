from datetime import datetime, timedelta


def solve(x):
    cutoff = datetime.strptime(x["cutoff"], "%Y-%m-%dT%H:%M:%S%z")
    lower = cutoff - timedelta(hours=x["lookback_hours"])
    seen, ids = set(), []
    for r in sorted(x["articles"], key=lambda a: (a["available_at"], a["id"])):
        published = datetime.strptime(r["published_at"], "%Y-%m-%dT%H:%M:%S%z")
        available = datetime.strptime(r["available_at"], "%Y-%m-%dT%H:%M:%S%z")
        if published < lower or published > cutoff or available > cutoff:
            continue
        if not any(s in x["symbols"] for s in r["symbols"]) or r["canonical_id"] in seen:
            continue
        seen.add(r["canonical_id"])
        ids.append(r["id"])
    return {"selected_ids": ids}
