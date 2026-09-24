# Tech explainer

A fun tooling for explaining hard tech concepts.

**Live:** https://zestytinker.github.io/tech-explainer/

## What this is

Most explanations of a hard idea hand you a definition and hope it sticks. This site does the opposite: you build a working, tiny version of the thing in a few clicks, then break it on purpose and work out why it broke. The Bloom filter is the first concept, chosen because it fails in a specific, visible way that a reader can cause themselves in about twenty seconds.

Who is the audience: A curious generalist with a little software knowledge, who will never read the paper.

Two rules the whole project runs on:

- Nothing is shown as finished without its check. Every requirement in [the spec](docs/phase-1-spec.md) is paired with a check, and the results of each run are written into the commit that made the change.
- Nothing factual is published without its source. Every claim on a page carries a numbered link to a primary source. Claims that could not be sourced were removed, not softened.

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
