# Search-first landing (fixed local list)

Screens: landing.html, landing-typing.html, landing-notyet.html, landing-unsupported.html, explainer.html

## Rationale
The landing is one question and a search box, and every answer is decided on the reader's device against an allowlist of about 200 tech concepts shipped inside the page (content/allowlist.py). Focus shows the built explainers and a prompt to type. Typing shows matches, built first, and a full match on a built name opens the page. An allowlisted name with no page gets "real concept, no explainer here yet"; anything else gets "not supported"; both offer the built ones. No input can fail and nothing is fetched. The explainer is design 1.

## Main trade-off
Three extra states and a typeahead over 200 names, roughly 20 minutes of the 2 hours. Under the facts rule each of the 200 names is a small claim, so the list needs its own verification check (checks/verify_allowlist.py) and entries that fail it are dropped, not shipped. Matching tolerance (plurals, aliases, typos) is where the reviewer experience is decided and it is not free.

## Spec lines this design bends
None. Section 4b said conventions not shared code; this landing needs a small concept list in the page, which is the one place a second explainer must register itself (name, aliases, path).

## For a second concept
Good, list-driven. See checks.md for the dry run.
