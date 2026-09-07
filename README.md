# Tech explainer

A fun tooling for explaining hard tech concepts.

**Live:** https://zestytinker.github.io/tech-explainer/
**First explainer:** https://zestytinker.github.io/tech-explainer/bloom-filter/

## What this is

Most explanations of a hard idea hand you a definition and hope it sticks. This site does the opposite: you build a working, tiny version of the thing in a few clicks, then break it on purpose and work out why it broke. The Bloom filter is the first concept, chosen because it fails in a specific, visible way that a reader can cause themselves in about twenty seconds.

Two audiences. A curious generalist with a little software knowledge, who will never read the paper. And a reviewer who opens a URL, clicks around for a minute, and forms a judgment.

Two rules the whole project runs on:

- Nothing is shown as finished without its check. Every requirement in [the spec](docs/phase-1-spec.md) is paired with a check, and the results of each run are written into the commit that made the change.
- Nothing factual is published without its source. Every claim on a page carries a numbered link to a primary source. Claims that could not be sourced were removed, not softened.

## How to play with it

**The landing.** A single box. Type a concept and press Enter. Every answer is decided on your device against a fixed list of 207 tech concepts baked into the page; nothing you type is sent anywhere, and the page works with the network off. Three things can happen:

- a built concept (`bloom filter`, or its plural, or an alias) opens its explainer;
- a concept on the list without an explainer yet says so plainly and offers what does exist;
- anything else says it isn't supported and offers the same.

No input can leave you stuck, which is the point.

**The explainer.** Five pages, moved through with the step buttons under the title or Prev/Next at the bottom.

1. **Why** — the hook: a signup form that says "taken" faster than any real list could be searched.
2. **How** — the playground. This is the part to actually use:
   - Press **Seed 8 words**. Eight words go in, and each lights three bulbs on a strip of 24.
   - Press **Suggest a word**. It picks a word that was never added but whose three bulbs happen to all be lit already.
   - Press **Check**. It says *Might be in the set*. That is a false positive, and you caused it.
   - Now hover (or tap) the word chips. Each lights the three bulbs it set. Find the words that lit the three bulbs your query checked. That is the whole idea: the filter never stored a single word, only which bulbs are on, so it cannot tell your word's bulbs from anyone else's.
   - Type a word of your own and check it. When it says *Definitely not*, the message names a bulb that was dark. A dark bulb is proof, because nothing ever lit it.
   - Keep adding words and watch the strip fill. By fifteen words most made-up words come back *Might be*; by twenty-four almost everything does. That is the trade being made, not a bug.
   - The single yellow button is always the next thing worth doing.
3. **Origin story** — Burton Bloom, 1970, and the hyphenation problem that produced the idea.
4. **Real-world applications** — Cassandra, RocksDB, the Bigtable paper, and Bitcoin's cautionary version.
5. **Read further** — the paper, the survey, the docs.

## Repository

| Path | What it is |
|---|---|
| `index.html` | The landing. One file, the full 207-concept list embedded. |
| `bloom-filter/index.html` | The explainer. One file: filter, five pages, embedded font and word list. |
| `docs/phase-1-spec.md` | The spec. Goals, decisions log, every requirement with its check, the facts rule, open questions. |
| `content/allowlist.py` | The 207 concepts with aliases and a Wikipedia title each. Source of truth for the landing. |
| `content/bloom-filter-pages.md` | The prose for pages 1 and 3 to 5, with the sentence in each source that supports each claim. |
| `checks/verify_allowlist.py` | Dev check: every allowlist entry resolves to a real, non-disambiguation Wikipedia article. |
| `designs/` | Eight low-fidelity layout explorations with rationale, trade-off and checks each. |
| `preview/` | Styling preview from before the build. Superseded by the live pages. |

Both pages are single files with no external requests: no CDN, no analytics, no cookies, no storage. Fredoka is subsetted and embedded under the SIL Open Font License (`font/OFL.txt`). The suggest dictionary is 3,096 SCOWL words.

## Running it locally

```
git clone https://github.com/zestytinker/tech-explainer.git
cd tech-explainer
python3 -m http.server 8000     # then open http://localhost:8000
```

Opening `bloom-filter/index.html` straight from disk works too; only the root landing needs a server, because `bloom-filter/` has to resolve to a directory index.

Before any deploy, run the one check that needs the network:

```
python3 checks/verify_allowlist.py
```

It writes `checks/allowlist-verified.csv`. Any entry that comes back missing or as a disambiguation page is deleted from `content/allowlist.py`, not explained away.

## Ideas to extend

- **Let readers request a concept.**
  An unsupported search could become a signal instead of a dead end: count how many different readers ask for each concept, and when an unsupported one becomes popular, build it and add it to the bank.

- **Check whether a concept suits the format.**
  Not every idea has a tiny breakable version. An LLM pass at authoring time could ask what the reader would build and what breaking it looks like, and refuse the rest. A judgment call, so it belongs in the pipeline with a human deciding, never at runtime.

- **Use an LLM to police the facts rule, not to write the facts.**
  Claims already carry a source and a supporting sentence, so CI can fetch each source and flag drift. The LLM is the auditor, never the author; a generated claim with a generated citation is the exact failure the rule exists to prevent.

- **Data cleaning and cache popular knowledge.**
  Once the pipeline opens Wikipedia and a few other trusted data sources, it could clean the pages (ignoring advertisements and irrelevant blocks) so it reads the main content of the popular pages more efficiently, and cache that in a database of our own, so fact checks and authoring do not depend on a third party being up or unchanged. The natural next step is a small knowledge graph over those pages, concept to concept, refreshed on a schedule so drift shows up as a diff rather than a surprise.

- **Enable further customization.**
  Make the number of bulbs adjustable, and the scrambles per word (how many bulbs each word lights), for readers who want to go further. Growing the strip shows false positives fading; adding scrambles shows the strip filling faster. Both are fixed today on purpose, so the first visit stays one idea.
