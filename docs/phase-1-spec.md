# Phase 1 spec: explainers site, Bloom filter first

Status: draft v6.2, step buttons, 2026-09-04. Nothing here is built. Lines added in the audit are marked (v5).

Vocabulary used throughout: **explainer** is one concept's page (v1 has one: Bloom filter). **Playground** is the interactive part of an explainer, the strip of bulbs and its boxes. **Site** is the thing at the GitHub Pages URL that will eventually hold several explainers.

## 1. Goals

1. A reader causes a false positive themselves and can say why it happened.
2. A reviewer opening the URL cold can try every path in under 60 seconds with no instructions.
3. Every factual claim on the page traces to a source that meets the facts rule (section 8).
4. The Bloom filter explainer is the first of several. v1 ships one, but its structure must not need rework when the second concept arrives.

## 2. Users

- **Reader**: curious generalist with a little software knowledge. Will never read the paper. Wants to poke something and have it click.
- **Reviewer**: opens a URL, clicks around for a minute, forms a judgment. May be on a phone.
- **Future author** (you, later): adds a second explainer without touching the first.

## 3. Non-goals for v1

- No backend, no accounts, no live LLM calls from the browser, no custom domain.
- One explainer ships in v1. The Bloom filter is the first concept the site supports, not the only one it will ever support. Structure for more (section 4b), build only one.
- No explanation sentence written by the page, no raw hash numbers shown. Decided: the bulbs carry the whole explanation.
- No size or hash-count controls for the reader. Decided: 24 bulbs, 3 hashes, fixed.
- (v5) No LLM step anywhere in v1 (D31), so the original "any LLM step must be previewable offline" constraint is satisfied vacuously.
- (v5) No analytics, cookies, or storage of any kind. Reload clears everything. Nothing about a reader leaves their device (D32).

## 4. Constraints

- 2 hours total build time.
- Static hosting on GitHub Pages. No build step, no external JS.
- Must work on first load with sample data present via one click.
- Deterministic in the browser: same word gives the same bulbs on every machine, every visit. No `Math.random` anywhere in the filter path.
- Plain words, playfulness only in visuals. Decided.
- (v5) Browser baseline: current Chrome, Firefox, Safari and their mobile versions. No IE, no polyfills.
- (v5) Size budget: each HTML file under 150 KB uncompressed, allowlist and dictionary included. One file, one request per page.
- (v5) "No build step" means nothing runs at deploy. Generators that emit committed files (allowlist.py writing allowlist.js, the seed-pattern script) are dev checks, and their output is committed.

### 4b. Scalability constraints (new, from your review)

The cheapest form of "scalable" that fits in 2 hours is a file layout and a set of conventions, not shared code. Proposed:

- Each explainer lives in its own folder: `/tech-explainer/bloom-filter/index.html`. The site root `/tech-explainer/index.html` is the search landing (D27).
- Each explainer folder carries its own `checks/` with the deploy checklist, hash vectors, and reader test. Site-level checks (landing, allowlist) live in `/checks/`. (v5)
- Each explainer has the same skeleton in the same order (link back to the landing, title, one framing sentence, playground, prose sections, numbered sources footer), so the second one is a copy with the middle swapped. Design 1 is the reference layout; design 8 is its variant.
- No shared JS or CSS library in v1. Duplication across two explainers is acceptable; a framework built for one is not.
- Sources footer format is identical across explainers so R12's check is reusable verbatim.
- The landing's concept list (D28) is the single registry. Nothing else on the site needs to know a second explainer exists.

## 5. Decision rights

- **You decide**: anything that changes scope, cost, the URL, hosting, or reverses a line marked Decided below.
- **I decide**: implementation details inside those lines (hash function, colors, layout, wording of microcopy), provided each stays within a Decided line and I log the choice.
- **Rule for anything unclear**: I stop and ask you. No guessing, no "reasonable default" silently applied mid-build. Defaults exist only in this document, where you can see them.

## 6. Decisions log

| # | Decision | State |
|---|---|---|
| D1 | Concept: Bloom filter first. Site is structured for more (4b) | Decided |
| D2 | Check = dev-only checklist run before deploy (section 7) | Decided |
| D3 | The set is words the reader adds themselves | Decided |
| D4 | Page loads empty, with one "seed 8 words" button | Decided |
| D5 | False positive is found by free trying, plus a "suggest a word" button the page knows will collide | Decided |
| D6 | Filter shown as one strip of 24 bulbs, not a grid | Decided |
| D7 | On query: bulbs only, colored by the word that lit them. No sentence, no numbers | Decided |
| D8 | Hovering a word in the list lights its three bulbs | Decided |
| D9 | Verdict copy: "Definitely not in the set" / "Might be in the set" | Decided |
| D10 | Playfulness lives in visuals only, words stay plain | Decided |
| D11 | Word cap 24, add button disables at the cap, no saturation note | Decided |
| D12 | Accept that the strip saturates well before the cap (see numbers under R7) | Decided |
| D13 | Sources: primary preferred, textbooks and Wikipedia allowed, all linked | Decided |
| D14 | Input is lowercased and trimmed before hashing | Decided |
| D15 | Suggest button visible from the start, styled as a secondary action | Decided |
| D16 | A bulb shows the color of the first word that lit it; later words change nothing visible until hovered | Decided |
| D17 | After a query the three checked bulbs keep a ring until the next query | Decided |
| D18 | On touch, tap does what hover does and stays until the next tap | Decided |
| D19 | Querying a word that is in the set gets the same "Might be" as any other hit. The page never reveals true positives | Decided |
| D20 | Reset button always visible, no confirm dialog | Decided |
| D21 | Reversed 2026-09-04 by D40. Was: one origin paragraph only | Reversed |
| D22 | I write the code, single `index.html` per explainer; you name the repo | Decided |
| D23 | Strip wraps to two rows of 12 below 480 px | Decided |
| D24 | I pick the 8 seed words, verified by script (R8). You can veto | Decided |
| D25 | Cut order in section 10 | Decided |
| D26 | Site layout: landing at root, each explainer in its own folder | Decided |
| D27 | Landing is a search box. Free text, resolved on the reader's device against an allowlist of about 200 tech concepts shipped in the page. Focus shows built explainers plus a type-to-search prompt; typing shows matches. A match on a built name opens the explainer. An allowlisted name with no page gets "real concept, no explainer here yet" with the built ones offered. Anything else gets "not supported" with the same offer. No input can end in a dead state, nothing is fetched | Decided |
| D28 | The fixed list is the one place a new explainer registers itself: name, aliases, path. Adding a concept is one entry plus one folder | Decided |
| D29 | A full match on a concept name or alias opens the page as you type; partial matches only highlight until Enter or click | Default (OQ-11) |
| D30 | The allowlist is `content/allowlist.py`, 207 entries across 10 categories with aliases and a Wikipedia title each. Every entry must pass `checks/verify_allowlist.py` (R17) or it is removed. The legitimacy check you asked for runs here, author-side, once, and is recorded | Decided, list itself open to veto (OQ-12) |
| D31 | No live legitimacy or LLM check at runtime. The allowlist replaces it for the demo. Reversed on 2026-09-04 after weighing proxy, key and hosting costs | Decided |
| D32 | (v5) No analytics, no cookies, no localStorage. Reload resets the playground | Default |
| D33 | (v5) Input limits, both boxes: 1 to 20 characters after trim, any characters accepted including accents and emoji. Over-length input is refused with a quiet note, same as duplicates | Default |
| D34 | (v5) Word colors: a palette of 12 distinguishable colors, cycling after 12 words. Beyond 12 the color is not unique, and hover (D8) remains the reliable channel. Color is never the only channel: hover highlight and the query ring do not depend on it | Default (OQ-15) |
| D35 | (v5) Keyboard: Enter submits in both boxes, Tab reaches every button, focus is visible. Word chips are focusable so hover-highlight works from the keyboard | Default |
| D36 | (v5) The suggest dictionary is a fixed list of roughly 1,000 common English words embedded in the explainer. Its source and license are recorded in the sources footer | Default, source open (OQ-14) |
| D37 | Dropped 2026-09-04: no `404.html` in v1. A mistyped URL shows GitHub's default 404 | Dropped |
| D38 | (v5) Repository: MIT for code, CC BY 4.0 for prose and the allowlist | Default (OQ-16) |
| D39 | Repo `tech-explainer`, site title "Tech explainer". Explainer URL `<user>.github.io/tech-explainer/bloom-filter/` | Decided |
| D40 | The explainer is five pages in a fixed order: 1 Why (hook story), 2 How (playground), 3 Origin story, 4 Real-world applications, 5 Read further. Prev and Next move between them; on page 1 the Next button reads "Next: build it". The playground page is complete on its own; the reviewer path (R13) is one click from page 1, then never leaves page 2. Revised 2026-09-04 from four pages | Decided |
| D45 | Five step buttons sit under the title on every page, labelled "1. Why", "2. How", "3. Origin story", "4. Real-world applications", "5. Read further". The current page is filled black. Each jumps to its page; Prev/Next at the bottom stay | Decided |
| D44 | The hook story is a hypothetical (a signup form on an unnamed site), so it carries no factual claim and no source. Text is in `content/bloom-filter-pages.md` | Decided |
| D41 | The five pages are sections of one `index.html`, switched by URL hash (`#problem`, `#playground`, `#origin`, `#applications`, `#further`). Every page is deep-linkable and Prev/Next are instant | Default (OQ-18) |
| D42 | Page 3 content is final and sourced in `content/bloom-filter-pages.md` (Cassandra, RocksDB, Bigtable paper, Bitcoin Core PR #16152), verified 2026-09-04. Chrome Safe Browsing excluded, no primary source for a present-tense claim. R23 re-checks the four links on deploy day | Decided |
| D43 | Page 4 is a short list of links: the 1970 paper, the 2004 survey, the Wikipedia article, and the page 3 sources. Every link is also a source, so R12 covers it | Default |

## 7. Requirements, each with its check

The check column is the deploy checklist. Run it top to bottom before every push. A requirement without a passing check is not shown as finished.

| ID | Requirement | Check (dev, before deploy) |
|---|---|---|
| R1 | Page loads with an empty strip of 24 dark bulbs, an empty word list, an add box, a query box, "seed 8 words", "suggest a word", and reset | Open `index.html` from disk with network off. All seven elements visible above the fold at 1280 wide and at 375 wide |
| R2 | "Seed 8 words" adds a fixed list of 8 words in a fixed order. Repeat clicks do nothing | Click twice. Word list shows exactly 8. Bulb pattern matches the pattern recorded in `checks/seed-pattern.txt` |
| R3 | Adding a word lights exactly 3 bulbs (fewer if two hashes agree) and appends the word to the list with a distinct color | Add "penguin" to the seeded set. Count newly lit bulbs, 1 to 3. Word appears in list |
| R4 | Same word always gives the same bulbs, across reloads and browsers | Add "penguin" in Chrome, Firefox and Safari (or two of them). Bulb indices identical. Record them in `checks/hash-vectors.txt` |
| R5 | Input is lowercased and trimmed; empty input and duplicates are refused with a quiet note | Add " Cat ", then "cat". Second is refused. List shows "cat" once. Empty submit does nothing |
| R6 | Add button disables at 24 words | Seed, then add 16 more. Button disables at 24. Reset re-enables it |
| R7 | Query lights a ring on the 3 checked bulbs and shows the plain verdict. "Definitely not" iff at least one checked bulb is dark | Query "cat" after seeding (in set): Might be. Query a word whose ring includes a dark bulb: Definitely not |
| R8 | "Suggest a word" proposes a word not in the list whose 3 bulbs are all lit. If no such word exists in the built-in dictionary, the button is disabled with a note to add more words first | With 1 word added, button is disabled. With the 8 seeds, button proposes a word; querying it gives Might be; the word is not in the list |
| R9 | Hovering a word in the list highlights its 3 bulbs; on touch, tap toggles the same highlight | Hover each seed word, 3 bulbs highlight. On a phone or devtools touch emulation, tap works and persists until the next tap |
| R10 | A bulb lit by more than one word shows the first word's color; hovering any of its words highlights it | Find a shared bulb in the seed pattern (recorded in `checks/seed-pattern.txt`). Hover both words. Both highlight it |
| R11 | Reset returns to R1 state | Click reset after R6. Strip dark, list empty, add enabled |
| R12 | Every factual sentence on the page has a numbered source link in the footer that resolves | Open every footer link. Each loads. Each sentence's number matches a link. Zero unnumbered factual sentences (see section 8 for what counts) |
| R13 | A reviewer landing on page 1 can click through to the playground and complete seed, query, suggest, query, hover, reset in under 60 seconds with no instructions | Hand the URL to one person who has not seen it. Time them. Do not speak |
| R14 | Works on GitHub Pages at the project URL with no console errors | Open the live URL, open devtools console. Zero errors. Repeat R2 and R8 on the live page |
| R15 | Landing search per D27: focus shows built explainers plus a type prompt; matches appear while typing, built first; full match on a built name opens `/bloom-filter/`; an allowlisted name with no page gives "real concept, no explainer here yet" plus links to built ones; anything else gives "not supported" plus the same links. Works with network off | Focus empty box: built names and the prompt, nothing else. Type "bloom filter": page opens. Type "merkle tree", "hash map" (alias), "arrays" (plural): real-concept message plus a link to Bloom. Type gibberish, empty, 200 chars, an emoji: not supported plus the same link, zero console errors. Repeat everything with network off |
| R16 | Adding a second explainer means one allowlist entry gets a path and one folder is added, nothing else | Dry run: give a stub entry a path and add an empty `/second/index.html`. Dropdown and match update. Confirm nothing in `/bloom-filter/` was edited. Delete the stub |
| R17 | Every allowlist entry resolves to a real, non-disambiguation Wikipedia article | Run `checks/verify_allowlist.py` on your machine (the sandbox cannot reach Wikipedia). Zero not-ok rows. Commit `checks/allowlist-verified.csv` with the date. Any not-ok entry is deleted from the list before deploy |
| R18 | (v5) Both pages are keyboard operable and color is never the only channel (D34, D35) | Tab through the explainer with the mouse unplugged: seed, add, check, suggest, reset, every word chip. Enter submits. Focus ring visible. Grayscale the page (devtools rendering, or a screenshot desaturated): a query result is still readable from the ring and the verdict |
| R19 | (v5) Input limits per D33 in both boxes, and an empty check does nothing | Add a 21-character word: refused with a note. Add "café" and an emoji word: accepted, 3 bulbs. Submit an empty check: nothing changes |
| R20 | Dropped with D37 | |
| R22 | Prev/Next move through the five pages in order; Prev is absent on page 1 and Next on page 5; page 1's Next reads "Next: build it"; the step buttons under the title mark the current page and jump on click; the browser back button and a direct link to `#applications` both land on the right page | Click through 1 to 5 and back. Reload on `#origin` shows Origin story. Open `#further` in a fresh tab. Back button returns to the previous page, not out of the site |
| R23 | Every system named on page 3 links to that system's own documentation or the original paper, and the claim matches what that source says today | On deploy day, open each source and read the sentence that supports the claim. Record the URL and date in the commit message. A claim without a matching sentence is removed |
| R21 | (v5) Reload resets state; nothing is stored | Seed, reload. Strip is dark. Devtools: Application tab shows no cookies, no local or session storage for the origin |

Numbers behind D12, computed for 24 bulbs and 3 hashes from the standard occupancy estimate [2]:

| words | bulbs lit | made-up word says "Might be" |
|---|---|---|
| 8 | ~64% | ~26% |
| 12 | ~78% | ~48% |
| 15 | ~85% | ~62% |
| 24 | ~95% | ~87% |

These are expectations over random hash placement, not guarantees for the specific seed list. R2's recorded pattern is the actual behavior.

## 8. Facts rule

What counts as a factual claim: any sentence a reader could check against the world. That includes a number, a date, a name, a "this is used by", and a "this was invented because". A sentence describing what the playground does in front of the reader is not a claim and needs no source.

Source standard (D13): primary preferred, meaning the original paper or the maintaining organization's own documentation. Textbooks and Wikipedia are allowed. Blog posts, talks and secondary summaries are not, even when they are the thing that made the example famous. Every source is a link in the footer, numbered, and the number appears next to the sentence.

Verification cost is uneven and the page should be written knowing that. A number needs the formula and the arithmetic run (the table under R7 was regenerated by script, not recalled). A historical claim about the 1970 paper is stable and cheap. A "used by system X today" claim needs X's current documentation and goes stale silently; each one costs a lookup and is the first thing to cut under time pressure.

The 207 allowlist names are claims of the form "X is a tech concept". Their source is one Wikipedia article each, recorded in `checks/allowlist-verified.csv` by R17; the landing links to that file rather than listing 207 footnotes.

At deploy, R12 and R17 are the enforcement. If a sentence can't be sourced in time, the sentence is removed, not the check.

This rule applies identically to every future explainer. It is a site rule, not a Bloom filter rule.

## 9. Definition of done

Phase 1 is done when all of the following hold on the live GitHub Pages URL:

1. R1 through R23 pass, checked off in `bloom-filter/checks/deploy-checklist.md` with the date.
2. One person who has never seen the page (the same session as R13 is fine) hit a false positive, was asked "why did it say might be", and gave an answer that mentions the bulbs already being on from other words. Record their words verbatim in `bloom-filter/checks/reader-test.md`. One failed attempt is logged, not hidden.
3. Zero factual sentences without a footer number.
4. Total build time logged and under 2 hours, or the overrun is written down with what was cut.

## 10. Cut order when time runs out

Decided (D25). Deferred before the build started, 2026-09-04: the `checks/` folders. The checks in section 7 are still run before each push; results are recorded in the commit message instead of files. Folder is rebuilt from those records if time allows.

Cut from the bottom of this list first:

0. Page 4, Real-world applications (D42). Highest verification cost. If cut, Next goes from Origin story straight to Read further.
1. The landing's typeahead and dropdown (part of R15). Fall back to a plain list of built names with the same three messages on submit. The not-yet and not-supported states are never cut; a dead end on the front door fails goal 2.
2. Touch tap-to-highlight (D18). Reviewers on phones lose hover; everything else works.
3. The suggest button's "add more words first" state. Replace with the button simply doing nothing below 3 words.
4. The Origin story page. The hook page (D44) is never cut; it costs five minutes and is the reader's reason to click.
5. Distinct colors per word, replaced by one "on" color. This breaks D7 and needs your OK.

Never cut: R18 keyboard operability. (The 404 page was dropped from scope on 2026-09-04, not cut.)

Never cut: the false positive path (seed, query, suggest), the verdict asymmetry, R12.

(v6) Budget note, honest version: playground page about 70 min, the other four pages about 25 (page 3 was sourced and written ahead of the build on 2026-09-04), landing with typeahead about 25, deploy about 10. That is 130 minutes against 120; the cut order is still expected to be used.

## 11. Open questions

| ID | Question | Default if you say nothing |
|---|---|---|
| OQ-11 | "A match will open the page" while typing. Opening on every partial match would yank the reader away mid-keystroke, so I read it as: full match on a name or alias opens immediately, partial match highlights and waits for Enter | Full match opens, partial waits |
| OQ-12 | The 207 entries in `content/allowlist.py` are my draft. Categories, aliases and Wikipedia titles are all mine | Ship as drafted after R17 passes. Veto entries or categories |
| OQ-13 | Matching tolerance. Exact after lowercase and trim is cheapest; plurals and aliases are in the list; typo tolerance (one edit) costs another 10 minutes | Lowercase, trim, drop trailing s, aliases. No typo tolerance in v1 |
| OQ-14 | (v5) Source of the ~1,000 word suggest dictionary. Any word list carries a license and the footer has to say so | I pick a permissively licensed common-words list and record it. Veto |
| OQ-15 | (v5) 24 words but only about 12 colors humans can tell apart. Cycle after 12, or lower the word cap to 12, which would also reopen D11 | Cycle after 12, keep the cap |
| OQ-18 | Page switching: hash sections in one file (instant, one file, deep-linkable) or four HTML files (works with JS off, four files to keep in step) | Hash sections in one file |
| OQ-19 | Closed: page 3 written and sourced, see D42 | |
| OQ-16 | (v5) Repo license. MIT for code and CC BY 4.0 for prose and allowlist is the usual pair | As stated |
| OQ-17 | Closed 2026-09-04: repo is `tech-explainer`, site title "Tech explainer", URL `<user>.github.io/tech-explainer/`. Now D39 | |

OQ-1 through OQ-10 were accepted at their defaults on 2026-09-04 and are now Decided.

## 12. Sources

1. Bloom, Burton H. "Space/time trade-offs in hash coding with allowable errors." Communications of the ACM 13(7): 422–426, July 1970. https://doi.org/10.1145/362686.362692
2. Broder, Andrei, and Michael Mitzenmacher. "Network applications of Bloom filters: A survey." Internet Mathematics 1(4): 485–509, 2004. Source for the false-positive estimate (1 − e^(−kn/m))^k and the occupancy estimate 1 − (1 − 1/m)^(kn) used in section 7.

Both citations were confirmed against the ACM record and a secondary reference list on 2026-09-04. The section 7 table was regenerated by a 5-line script on the same date; the script should be committed under `bloom-filter/checks/` so R7's numbers can be re-run.
