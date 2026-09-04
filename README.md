# Explainers

Build a tiny version of a hard idea, then break it. First concept: the Bloom filter.

Status: spec and design phase. Nothing is deployed yet.

- `docs/phase-1-spec.md`: the spec. Every requirement has its check; every decision is logged.
- `designs/`: eight low-fidelity layout explorations with rationale, trade-off and checks each. `designs/README.md` has the comparison and recommendation.
- `preview/`: the neo-brutalist styling preview (static, no filter logic).
- `content/allowlist.py`: the ~200 concept allowlist for the landing search. `allowlist.json` is generated from it and committed.
- `checks/verify_allowlist.py`: dev check that every allowlist entry is a real Wikipedia article. Run on a machine with network access; commit the CSV it writes.

Rule for the whole project: nothing is shown as finished without its check, and nothing factual is published without its source.
