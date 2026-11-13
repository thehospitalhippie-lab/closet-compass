# Yeha backlog

Work top-down. One item per night. Move finished items to **Done** with the date.

## Next up

1. **(Blocked 2026-11-09: ccnash.org and www.tn.gov must be added to the session's allowed network domains.) Upgrade Christ Church Nashville to `official`.** Find the church's own ministry page (ccnash.org) and confirm the phone, email and how donations work.
2. **Middle TN leads to verify and add:** Empower Tennessee (center for independent living, Nashville); FiftyForward senior centers (ask about equipment); Williamson County senior services; Rutherford County / Murfreesboro church closets; Sumner County (Hendersonville, Gallatin); Wilson County (Lebanon); Montgomery County (Clarksville); Maury County (Columbia); Lions Clubs of Middle TN.
3. **Guide: "Where to donate a hospital bed in Nashville."** Needs at least 3 verified Middle TN places that take beds. Cover pickup and what to ask.
4. **East TN leads:** Hope Medical Equipment Ministry (Knoxville area, a third-party list gives 865-202-9022; verify); Disability Resource Center (Knoxville); Tri-Cities church closets (Johnson City, Kingsport, Bristol).
5. **West TN leads:** Church Health (Memphis), whose donation program a third-party list mentions (verify); Memphis Center for Independent Living; Jackson Center for Independent Living.
6. **Southeast TN leads:** Tri-State Resource & Advocacy (Chattanooga CIL); closets in Cleveland TN. Confirm that Goodwill HELPs is still running, and its current rules.
7. **Statewide:** MDA equipment program; VA equipment for veterans (Tennessee Valley Healthcare System, Memphis VA, Mountain Home VA); the Area Agencies on Aging & Disability, as referral sources.
8. **Guide: "Medicare and hospital beds: rent vs. own, in plain English."** Cite CMS only.
9. **Guide: "Questions to ask a loan closet" (printable checklist).**
10. **Guide: "How to start a medical equipment loan closet at your church."** Supply side; likely to earn links.
11. **City pages**, each only once the area has 4+ verified listings: Nashville, Knoxville, Chattanooga, Memphis.
12. **Guide: "Medical equipment for veterans in Tennessee."**

- Lead (2026-11-09): AARP article says five regional Tennessee technology access centers lend equipment incl. hospital beds (East TN Technology Access Center, Knoxville); find each center's own page.
- Lead (2026-11-09): Empower Tennessee shows no equipment loan in searches; call/ask before listing. Hope Medical Equipment Ministry: a seniorsmobility.org list says free loans, location unknown; find its own page.
- Lead (2026-11-11): Knoxville Office on Aging reportedly runs loan closets (resource-guide mention); find the city/county page.
- Check (2026-11-11): a search summary says Mid-South ACT (Memphis) does not accept medical equipment donations, but our listing says accepts_donations "yes". Re-verify on Mid-South ACT's own site and correct.
- Lead (2026-11-13): DDA Innovation Centers (wheelchair seating; Arlington, Nashville, Greeneville) reportedly went to online-only applications Nov 1, 2026; verify on tn.gov and consider a short note in the borrowing guide's "No loan closet near you?" section.
- Lead: a third-party 2023 list mentions a Tennessee church parish closet with hospital beds ("Church of Incarnation"); find the church's own page.

## Site to-dos (need Micaiah)

- **Network access for nightly runs (blocking since 2026-11-09):** the scheduled task's environment can't reach source sites (ccnash.org, www.tn.gov, medicare.gov, newschannel5.com, ettac.org, states.aarp.org all fail). Allow these domains, or switch the environment's network policy to full access, so Yeha can verify sources.

- **Google AdSense (optional):** needs a custom domain first. The after-a-death guide never shows ads.
- Amazon Associates tag → `config.json` `amazon_tag` (Micaiah signs up; it needs her tax info)
- Starter Deck link → `config.json` `starter_deck_url` and `starter_deck_name`
- Custom domain (optional, about $12/yr) → `config.json` `custom_domain` and `site_url`, then set the domain in the GitHub Pages settings
- Google Search Console verification code → `config.json` `search_console_verification`

## Done

- 2026-11-05: Launched the site: home, Tennessee directory (10 listings), borrowing guide, after-a-death guide, About, Disclosures and Suggest pages.
- Lead (2026-11-09): TTAP's five regional technology access centers each lend devices (tn.gov TTAP page); fetch the tn.gov page for names/phones once www.tn.gov is allowed, then add the centers not yet listed.
