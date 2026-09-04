# Tech explainer

Build a tiny version of a hard tech idea, then break it.

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

## Adding a second explainer

By design this costs one folder and one line. Give the concept a path in `content/allowlist.py`, add `<concept>/index.html`, done. Nothing in the existing explainer needs editing, and the landing picks it up automatically. Keep the five-page skeleton and the numbered sources footer so the checks stay reusable.

## Ideas to extend

Rough order of value, with the honest cost of each.

**Let readers request a concept.** Today an unsupported search is a dead end with a polite message. It could be a signal instead: a "request this" button that records what people actually want, feeding the queue for what to build next. The catch is that this is the first thing here that needs a backend, or at least a form service, and with it come spam, moderation, and a privacy promise that currently reads "nothing you type is sent anywhere". That sentence would have to change, and it should change loudly rather than quietly.

**Check whether a concept suits this format at all.** Not every idea has a tiny breakable version. A Bloom filter does; "eventual consistency" might not. Before a concept enters the queue, an LLM pass could ask whether there is a playground in it, what the reader would build, and what breaking it would look like, and refuse the ones with no good answer. This is a judgment call, so it belongs in the authoring pipeline with a human deciding, not at runtime in front of a reader.

**Use an LLM to police the facts rule, not to write the facts.** Each page's claims already carry a source and the supporting sentence. That structure is machine-checkable: fetch each source, ask whether it still supports the claim, and flag drift. This is most valuable for the "used by system X" claims, which go stale silently, and it would run as scheduled CI rather than in the browser. Worth stating plainly: the LLM would be the auditor, never the author. A generated claim with a generated citation is exactly the failure mode the facts rule exists to prevent, so any such pipeline needs a human sign-off before publish and a record of what was checked and when.

**Cache popular concepts.** If explainers are ever produced with help from a model, the expensive part is the drafting and the sourcing, not the serving. Those outputs are static once verified, so they should be generated once, reviewed, committed as plain HTML, and served from the CDN like everything else here. The cache is the repository. That keeps the current property worth protecting: a reader gets bytes, not an inference call, and the page behaves identically offline and forever.

**Smaller things.** A third message on the landing for ambiguous prefixes like "hash", which today falls to "not supported" (open question OQ-20 in the spec). A size control on the filter, so the reader can watch false positives disappear as the strip grows. And the reader test that has not been run yet, which is the only thing that will actually tell us whether the bulbs teach what they are supposed to teach.

## Status

Built and deployed. Five checks still need a human or a machine this repo has not had access to, listed in section 11b of the spec: the hash vectors in Firefox and Safari, the timed reader test, the console on the live URL, the Wikipedia pass over the allowlist, and re-opening the page 4 links on deploy day.
