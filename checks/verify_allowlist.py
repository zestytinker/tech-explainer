"""Dev check for D30/R17: every allowlist entry must resolve to a real Wikipedia article.
Run: python3 checks/verify_allowlist.py   (needs network; run on your machine, not in CI-less sandboxes)
Writes checks/allowlist-verified.csv. Entries marked missing or disambiguation are removed from the
allowlist before deploy, not shipped. The CSV is the source record for the 200 'X is a tech concept' claims.
"""
import json, csv, sys, urllib.parse, urllib.request, datetime, os
here = os.path.dirname(__file__)
entries = json.load(open(os.path.join(here, "..", "content", "allowlist.json")))
API = "https://en.wikipedia.org/w/api.php"
UA = {"User-Agent": "explainers-allowlist-check/1.0 (dev check; contact via repo)"}
rows, bad = [], 0
for i in range(0, len(entries), 50):
    batch = entries[i:i+50]
    q = {"action":"query","format":"json","redirects":1,"prop":"pageprops|info","inprop":"url",
         "titles":"|".join(e["wiki"] for e in batch)}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(q), headers=UA)
    data = json.load(urllib.request.urlopen(req, timeout=30))
    redirects = {r["from"]: r["to"] for r in data["query"].get("redirects", [])}
    norm = {n["from"]: n["to"] for n in data["query"].get("normalized", [])}
    pages = {p["title"]: p for p in data["query"]["pages"].values()}
    for e in batch:
        t = norm.get(e["wiki"], e["wiki"]); t = redirects.get(t, t)
        p = pages.get(t, {})
        if "missing" in p: status = "missing"
        elif "disambiguation" in p.get("pageprops", {}): status = "disambiguation"
        else: status = "ok"
        if status != "ok": bad += 1
        rows.append([e["name"], e["wiki"], t, status, p.get("fullurl",""), datetime.date.today().isoformat()])
with open(os.path.join(here, "allowlist-verified.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["name","requested_title","resolved_title","status","url","checked_on"]); w.writerows(rows)
print(f"{len(rows)} checked, {bad} not ok. See checks/allowlist-verified.csv")
sys.exit(1 if bad else 0)
