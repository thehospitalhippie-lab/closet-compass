#!/usr/bin/env python3
"""Quality gate for Closet Compass. Run after build.py; exits non-zero on problems.

Checks:
- every listing has the required fields, a valid region, at least one http(s) source,
  a valid ISO last_checked date that isn't in the future, and a unique id
- no listing invents contact info without a source (phone/email/website need >= 1 source)
- every built HTML page has a <title>, a meta description and an <h1>
- every internal link (href starting with base path or "/") resolves to a built file
"""
import datetime as dt
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
REGIONS = {"middle", "east", "southeast", "west", "statewide"}
REQUIRED = ["id", "name", "region", "city", "offers", "equipment", "serves", "cost",
            "accepts_donations", "confidence", "sources", "last_checked"]

problems = []


def check_listings():
    listings = json.loads((ROOT / "data" / "listings.json").read_text())
    seen = set()
    today = dt.date.today()
    for l in listings:
        lid = l.get("id", "?")
        for k in REQUIRED:
            if k not in l or l[k] in (None, "", []):
                problems.append(f"listing {lid}: missing {k}")
        if lid in seen:
            problems.append(f"listing {lid}: duplicate id")
        seen.add(lid)
        if l.get("region") not in REGIONS:
            problems.append(f"listing {lid}: bad region {l.get('region')}")
        if l.get("confidence") not in {"official", "news", "directory"}:
            problems.append(f"listing {lid}: bad confidence {l.get('confidence')}")
        if l.get("accepts_donations") not in {"yes", "no", "ask"}:
            problems.append(f"listing {lid}: accepts_donations must be yes/no/ask")
        srcs = l.get("sources") or []
        if not all(isinstance(s, dict) and str(s.get("url", "")).startswith("http") and s.get("title") for s in srcs):
            problems.append(f"listing {lid}: every source needs a title and an http(s) url")
        try:
            d = dt.date.fromisoformat(l.get("last_checked", ""))
            if d > today:
                problems.append(f"listing {lid}: last_checked is in the future")
        except ValueError:
            problems.append(f"listing {lid}: last_checked must be YYYY-MM-DD")
    return listings


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.has_title, self.has_desc, self.h1 = [], False, False, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append(a.get("href", ""))
        if tag == "script" and a.get("src"):
            self.links.append(a["src"])
        if tag == "title":
            self.has_title = True
        if tag == "meta" and a.get("name") == "description" and a.get("content"):
            self.has_desc = True
        if tag == "h1":
            self.h1 += 1


def check_site():
    if not OUT.exists():
        problems.append("docs/ not built — run python3 build.py first")
        return
    base = json.loads((ROOT / "config.json").read_text()).get("base_path", "").rstrip("/")
    # The build may have been run with --base-path; detect it from the home page stylesheet link.
    home = (OUT / "index.html").read_text()
    m = re.search(r'href="([^"]*)/static/style\.css', home)
    if m:
        base = m.group(1)
    for page in OUT.rglob("*.html"):
        p = PageParser()
        p.feed(page.read_text())
        rel = page.relative_to(OUT)
        if not p.has_title:
            problems.append(f"{rel}: missing <title>")
        if not p.has_desc:
            problems.append(f"{rel}: missing meta description")
        if p.h1 != 1:
            problems.append(f"{rel}: expected exactly one <h1>, found {p.h1}")
        for href in p.links:
            if href.startswith(("http", "mailto:", "tel:", "#")):
                continue
            path = href.split("#")[0].split("?")[0]
            if base and path.startswith(base):
                path = path[len(base):]
            if not path.startswith("/"):
                problems.append(f"{rel}: relative link {href} (use url())")
                continue
            target = OUT / path.lstrip("/")
            if path.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                problems.append(f"{rel}: broken internal link {href}")


if __name__ == "__main__":
    listings = check_listings()
    check_site()
    if problems:
        print("CHECK FAILED:")
        for x in problems:
            print(" -", x)
        sys.exit(1)
    print(f"CHECK OK: {len(listings)} listings, site links and pages look good.")
