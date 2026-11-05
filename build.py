#!/usr/bin/env python3
"""Build Closet Compass into docs/ for GitHub Pages.

Usage:
  python3 build.py                      # uses config.json
  python3 build.py --base-path ""       # local preview at site root
  python3 build.py --site-url https://user.github.io --base-path /closet-compass

Content lives in content/**/*.md with a simple front matter block:
---
title: ...
description: ...
path: /guides/some-slug/
kind: guide | page
eyebrow: ...
lede: ...
updated: 2026-11-05
---
Markdown body (Jinja macros allowed: amazon(), deck_box(), donate_list(), url()).
"""
import argparse
import os
import datetime as dt
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote_plus

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"

REGION_NAMES = {
    "middle": "Middle Tennessee (Nashville area)",
    "east": "East Tennessee (Knoxville & Tri-Cities)",
    "southeast": "Southeast Tennessee (Chattanooga)",
    "west": "West Tennessee (Memphis & Jackson)",
    "statewide": "Statewide programs",
}
REGION_SHORT = {
    "middle": "Middle TN",
    "east": "East TN",
    "southeast": "Southeast TN",
    "west": "West TN",
    "statewide": "Statewide",
}
REGION_BLURBS = {
    "middle": "Davidson, Williamson, Rutherford, Sumner, Wilson, Montgomery, Maury and surrounding counties.",
    "east": "Knoxville, the Tri-Cities and the mountain counties.",
    "southeast": "Chattanooga and the counties around it, some reaching into North Georgia.",
    "west": "Memphis, Jackson and the rest of West Tennessee.",
    "statewide": "Programs that serve people anywhere in Tennessee, often for a specific diagnosis or disability.",
}


def human_date(value):
    if not value:
        return ""
    if isinstance(value, str):
        value = dt.date.fromisoformat(value[:10])
    return value.strftime("%b %-d, %Y")


def telhref(phone):
    main = phone.split("(")[0]
    ext = ""
    m = re.search(r"ext\.?\s*(\d+)", main, re.I)
    if m:
        ext = "," + m.group(1)
        main = main[: m.start()]
    digits = re.sub(r"\D", "", main)
    return digits + ext


def parse_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.lstrip("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-path", default=None)
    ap.add_argument("--site-url", default=None)
    ap.add_argument("--relative", action="store_true", help="relative links (for previews hosted under an unknown path)")
    ap.add_argument("--out", default=None, help="output folder (default docs/)")
    args = ap.parse_args()
    global OUT
    if args.out:
        OUT = Path(args.out).resolve()

    site = json.loads((ROOT / "config.json").read_text())
    if args.base_path is not None:
        site["base_path"] = args.base_path
    if args.site_url is not None:
        site["site_url"] = args.site_url
    base = site.get("base_path", "").rstrip("/")

    listings = json.loads((ROOT / "data" / "listings.json").read_text())
    order = list(REGION_NAMES)
    listings.sort(key=lambda l: (order.index(l["region"]), l["name"].lower()))
    updated = max(l["last_checked"] for l in listings)
    region_counts = {}
    for l in listings:
        region_counts[l["region"]] = region_counts.get(l["region"], 0) + 1

    current = {"page": "/"}

    def url(path):
        if not args.relative:
            return f"{base}{path}"
        target, _, frag = path.partition("#")
        if target.endswith("/"):
            target += "index.html"
        page_dir = current["page"] if current["page"].endswith("/") else str(Path(current["page"]).parent) + "/"
        rel = os.path.relpath(target, page_dir)
        return rel + (("#" + frag) if frag else "")

    def canonical(path):
        return f"{site['site_url'].rstrip('/')}{base}{path}"

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    env.filters["human_date"] = human_date
    env.filters["telhref"] = telhref

    build_id = hashlib.sha1(dt.datetime.now().isoformat().encode()).hexdigest()[:8]

    # ---- helpers usable inside markdown content ----
    def amazon(query, label=None):
        tag = site.get("amazon_tag", "").strip()
        href = f"https://www.amazon.com/s?k={quote_plus(query)}" + (f"&tag={tag}" if tag else "")
        rel = "sponsored nofollow noopener" if tag else "nofollow noopener"
        return Markup(f'<a href="{href}" rel="{rel}">{label or query}</a>')

    def deck_box():
        link = site.get("starter_deck_url", "").strip()
        if not link:
            return Markup("")
        name = site.get("starter_deck_name") or "a conversation starter deck"
        return Markup(
            '<aside class="deck-box"><h3>Before the equipment arrives: have the talk</h3>'
            "<p>Talking about what someone wants near the end of life is easier with a little structure. "
            f'If that would help your family, <a href="{link}" rel="noopener">{name}</a> is made for exactly that conversation. '
            "(Closet Compass's owner made it, so this is a plug for our own product.)</p></aside>"
        )

    def donate_list():
        items = [l for l in listings if l.get("accepts_donations") == "yes"]
        lis = []
        for l in items:
            contact = l.get("phone") or l.get("email") or ""
            lis.append(
                f'<li><strong><a href="{url("/tennessee/")}#{l["id"]}">{l["name"]}</a></strong>'
                f' — {l["city"]}. {("Contact: <span class=\"nowrap\">" + contact + "</span>") if contact else ""}</li>'
            )
        return Markup('<ul class="mini-list">' + "".join(lis) + "</ul>")

    md_globals = dict(site=site, url=url, amazon=amazon, deck_box=deck_box, donate_list=donate_list,
                      listings=listings, region_names=REGION_NAMES)

    common = dict(site=site, url=url, canonical=canonical, build_id=build_id, updated_human=human_date(updated),
                  region_names=REGION_NAMES, region_short=REGION_SHORT, region_blurbs=REGION_BLURBS, region_counts=region_counts,
                  listings=listings)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "static", OUT / "static")
    (OUT / ".nojekyll").write_text("")

    pages_for_sitemap = []

    def write(path, html):
        target = OUT / path.lstrip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html)

    # Home
    recent = sorted(listings, key=lambda l: l["last_checked"], reverse=True)[:4]
    page = dict(path="/", title=site["site_name"], description=site["description"])
    current["page"] = "/"
    write("/", env.get_template("home.html").render(page=page, recent_listings=recent, **common))
    pages_for_sitemap.append(("/", updated))

    # Directory
    page = dict(path="/tennessee/", title="Medical equipment loan closets in Tennessee",
                description="Where to borrow wheelchairs, walkers, shower chairs, hospital beds and other medical equipment in Tennessee, free or low cost, and where to donate equipment. Every listing is sourced and dated.")
    items = []
    for i, l in enumerate(listings, 1):
        org = {"@type": "NGO", "name": l["name"]}
        if l.get("phone"):
            org["telephone"] = l["phone"]
        if l.get("website"):
            org["url"] = l["website"]
        if l.get("address"):
            org["address"] = l["address"]
        items.append({"@type": "ListItem", "position": i, "item": org})
    current["page"] = "/tennessee/"
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "name": page["title"], "itemListElement": items}
    write("/tennessee/", env.get_template("directory.html").render(page=page, itemlist_jsonld=json.dumps(itemlist), **common))
    pages_for_sitemap.append(("/tennessee/", updated))

    # Markdown pages
    md = markdown.Markdown(extensions=["extra", "sane_lists", "smarty"])
    for f in sorted((ROOT / "content").rglob("*.md")):
        meta, body = parse_front_matter(f.read_text())
        current["page"] = meta["path"]
        body = env.from_string(body).render(**md_globals)
        md.reset()
        html_body = md.convert(body)
        meta.setdefault("kind", "page")
        meta.setdefault("updated", updated)
        article = {
            "@context": "https://schema.org", "@type": "Article", "headline": meta["title"],
            "description": meta.get("description", ""), "dateModified": meta["updated"],
            "author": {"@type": "Organization", "name": site["site_name"]},
            "mainEntityOfPage": canonical(meta["path"]),
        }
        write(meta["path"], env.get_template("page.html").render(page=meta, body=html_body,
                                                                   article_jsonld=json.dumps(article), **common))
        pages_for_sitemap.append((meta["path"], meta["updated"]))

    # 404
    page = dict(path="/404.html", title="Page not found", description="This page could not be found.")
    current["page"] = "/"
    (OUT / "404.html").write_text(env.get_template("404.html").render(page=page, **common))

    # Sitemap + robots
    urls = "".join(f"<url><loc>{canonical(p)}</loc><lastmod>{d}</lastmod></url>" for p, d in pages_for_sitemap)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {canonical('/sitemap.xml')}\n")
    if site.get("custom_domain"):
        (OUT / "CNAME").write_text(site["custom_domain"].strip() + "\n")

    print(f"Built {len(pages_for_sitemap)} pages, {len(listings)} listings -> {OUT}")


if __name__ == "__main__":
    main()
