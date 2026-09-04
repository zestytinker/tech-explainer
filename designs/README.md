# Design explorations: Bloom filter explainer

Eight low-fidelity layouts. Each folder has the screens as HTML, a README with rationale, trade-off and the spec lines it bends, and a checks.md. Wireframes are deliberately grey; the only color is the bulbs, because the bulbs are the subject. The playground in every screen is static, not functional, so these compare layout and not behavior.

Every design was generated from one script (`gen_designs.py`) so the strip, word list and boxes are identical across them and the differences you see are the differences that matter.

## Comparison

"How hard to verify" counts the factual sentences the layout invites and rates the cost of sourcing them under the facts rule (section 8 of the spec). "Hit" is my estimate of how many generalists leave able to say why the false positive happened; it is a judgment, and the reader test in the definition of done is what actually measures it.

| # | Design | Prose | Claims | Hard to verify | 60 s path | Hit on goal 1 | Second concept | Build in 2 h |
|---|---|---|---|---|---|---|---|---|
| 1 | [Single scroll, playground first](01-single-scroll-playground-first/README.md) | 1 para | 2 | Low | Yes | Medium | Good | Fits |
| 2 | [Stepped six-part page](02-stepped-six-part/README.md) | 6 sections | 10 | High | No | High | Medium | Over |
| 3 | [Search-first landing (fixed local list)](03-search-first-landing/README.md) | 1 para | 2 | Low | Yes | Medium | Good, list-driven | Fits, +15 min |
| 4 | [Catalog landing with tags](04-catalog-landing/README.md) | 1 para | 2 | Low | Yes | Medium | Good at 3+ | Slightly over |
| 5 | [Bouncer-style playful](05-bouncer-playful/README.md) | 1 para + metaphor | 2 | Low | Yes | Medium, risk of wrong model | Good | Over (art) |
| 6 | [Reference style, prose first](06-reference-style/README.md) | 7 sections | 18 | Very high | No | Low for generalists | Best | Over |
| 7 | [Playground only](07-playground-only/README.md) | hidden | 2 | Lowest | Yes, if they click | Medium | Weak (no landing) | Fits easily |
| 8 | [Guided tour beside the playground](08-guided-tour/README.md) | 1 para + 5 prompts | 2 | Low | Yes (skippable) | High | Good, prompts per concept | Borderline (+20 min) |

## Observations

- Verification cost tracks prose almost linearly. Designs 2 and 6 are the only ones that reach double-digit claims, and both do it in a "where it's used today" section. That section is where the facts rule bites, because those claims go stale silently.
- Design 4 is a landing for a site that does not exist yet. Design 3 was in the same bucket until it was rebuilt around a fixed list where no input can fail; that turns the search box from theatre into a real front door, at the cost of three extra states.
- Design 5 is the argument for D9 and D10. Written down it sounds like a nice metaphor; drawn, the bouncer plainly "remembers" things, and that is the one wrong idea the page must not plant.
- Designs 1, 7 and 8 are the same explainer at three levels of scaffolding: none, one sentence, five prompts. The spec's recorded risk (bulbs-only may leave generalists with a light show and no insight) is what separates them.

## Recommendation

Take design 1 as the explainer, and the revised design 3 as the landing (your call on 2026-09-04: free text, decided on device against a fixed list, no input can fail). Design 1 is inside every Decided line and carries exactly two claims. Design 3's landing costs about 15 minutes more than a card list and buys a front door that already behaves like a site with many concepts.

Take design 8 as the second one to develop. It is design 1 plus a skippable side panel, so the two share almost all of their code, and it directly hedges the one risk the spec logged against D7. The reader test in the definition of done can then be run once per design with one person each, and the verbatim answers decide which ships.

Not taken further: 2 and 6 (prose-first, over budget, expensive to verify), 4 (a catalog is right at concept three, not today), 5 (breaks D9 and D10 for a metaphor that teaches the wrong model), 7 (drops the one framing sentence and the landing, and the empty-on-load state gives a cold reviewer nothing to grab).

## What is still a guess

The "Hit" column. Nothing here has been shown to a reader. The two designs taken forward are chosen so that the first reader test compares them directly.
