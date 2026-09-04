# Checks for Search-first landing (fixed local list)

Run before this design is called finished. Each line is pass/fail.

- [ ] Focus the empty box: dropdown shows every built name and every recognised name, grouped, nothing else.
- [ ] Type each built name in full: page opens. Type a prefix: it highlights, Enter opens.
- [ ] Type five allowlisted names with no page, including one via an alias and one as a plural: real-concept message plus links to every built one. No dead end.
- [ ] Type gibberish, an empty string, 200 characters, an emoji: not supported message plus the same links. No console errors.
- [ ] Network off: all four behaviors identical, proving nothing is fetched.
- [ ] Second concept dry run: adding a concept is one entry in the list plus a folder. The dropdown and the not yet list update with no other edit.
- [ ] Explainer checks: same four as design 1.
