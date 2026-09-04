# Tech explainer

Build a tiny version of a hard tech idea, then break it. Live at https://zestytinker.github.io/tech-explainer/ First concept: the Bloom filter.

Status: built, awaiting the live checks (see docs/phase-1-spec.md section 11b). Landing at `/`, explainer at `/bloom-filter/`.

- `docs/phase-1-spec.md`: the spec. Every requirement has its check; every decision is logged.
- `designs/`: eight low-fidelity layout explorations with rationale, trade-off and checks each. `designs/README.md` has the comparison and recommendation.
- `preview/`: the neo-brutalist styling preview (static, no filter logic).
- `content/allowlist.py`: the ~200 concept allowlist for the landing search. `allowlist.json` is generated from it and committed.
- `checks/verify_allowlist.py`: dev check that every allowlist entry is a real Wikipedia article. Run on a machine with network access; commit the CSV it writes.

Rule for the whole project: nothing is shown as finished without its check, and nothing factual is published without its source.
