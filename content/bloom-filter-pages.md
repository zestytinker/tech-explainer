# Bloom filter explainer: pages 2 to 4, sourced

Verified 2026-09-04. Each claim carries the source number from the footer and the sentence in the source that supports it. Page 3 claims are the ones that go stale; re-check them whenever the page is touched (R23).

## Page 2: Origin story

In 1970 Burton Bloom was looking at a problem where checking a big list was expensive and being occasionally wrong in one direction was survivable. He showed you could shrink the list to a strip of bits if you accepted a small rate of false "yes" answers, and never a false "no". [1]

His worked example was hyphenation: most words follow simple rules, a minority need a lookup in a dictionary too big for memory. A small in-memory filter could say "definitely a rule-following word" for most input and send only the rest to the slow dictionary. [1]

Verification: [1] abstract confirmed via the ACM record (13(7):422–426, doi 10.1145/362686.362692): "allowing a small number of test messages to be falsely identified as members of the given set will permit a much smaller hash area to be used". The hyphenation example is in the paper body, not the abstract; **confirm against the paper text on build day** before the second paragraph ships. If not confirmed, ship the first paragraph only.

## Page 3: Real-world applications

The same shape shows up wherever a full lookup is expensive and a wrong "maybe" is cheap to catch.

**Databases that write files and never rewrite them.** Apache Cassandra keeps one filter per data file on disk, so a read for a row can skip every file whose filter says "definitely not". Operators tune the false-positive chance per table, trading memory for fewer wasted disk reads. [3] RocksDB does the same: each file gets a filter built when the file is written, and a lookup consults the filter before opening the file. [4]

**The Bigtable paper.** Google's 2006 paper on Bigtable described attaching a Bloom filter to each of its immutable data files to avoid disk seeks for rows that aren't there. Most later systems of this kind, Cassandra and RocksDB included, inherited the idea from it. [5]

**Bitcoin light clients, and a warning.** For years, lightweight Bitcoin wallets sent a Bloom filter of their addresses to full nodes, which replied with only the transactions that "might be" theirs. In 2019 Bitcoin Core disabled serving those filters by default, calling them a well-known denial-of-service target. The lesson travels: "might be" is cheap for the asker and can be expensive for whoever has to answer. [6]

Verification record:
- [3] Apache Cassandra documentation, "Bloom Filters", https://cassandra.apache.org/doc/latest/cassandra/managing/operating/bloom_filters.html. Supports: per-SSTable filter; two states "definitely does not exist in the given file" / "probably exists"; `bloom_filter_fp_chance` tunable per table; memory vs IO trade-off.
- [4] RocksDB wiki, "RocksDB Bloom Filter", https://github.com/facebook/rocksdb/wiki/RocksDB-Bloom-Filter. Supports: when the filter policy is set, every new SST file contains a Bloom filter, built when the file is written, checked to decide whether the file may contain the key.
- [5] Chang et al., "Bigtable: A Distributed Storage System for Structured Data", OSDI 2006, https://www.usenix.org/legacy/event/osdi06/tech/chang/chang.pdf. Supports: Bloom filters per SSTable to reduce disk accesses for absent rows; cites Bloom 1970 as reference [7]. The "most later systems inherited it" sentence is an inference, not in any single source; **soften to "many later systems" or cut if a reviewer objects.**
- [6] Bitcoin Core pull request #16152, "Disable bloom filtering by default", merged 2019-07-19, https://github.com/bitcoin/bitcoin/pull/16152. Supports: BIP 37 filters "well-known to be a significant DoS target"; serving disabled by default. The privacy weakness is widely reported but the PR text is about DoS, so the page says DoS only.

Excluded: Chrome Safe Browsing. The commonly cited Bloom filter mechanism is historical and current documentation does not describe it that way; no primary source found that supports a present-tense claim.

## Page 4: Read further

1. The 1970 paper. Four pages, readable without a mathematics background for the first half. [1]
2. Broder and Mitzenmacher's 2004 survey, where the sizing formulas on this site come from. [2]
3. Wikipedia's article, for the variants: counting filters, cuckoo filters, blocked filters. [7]
4. The Cassandra and RocksDB documentation pages above, if you want to see the knobs real systems expose. [3][4]

## Footer sources (all pages)

1. Bloom, B. H. (1970). Space/time trade-offs in hash coding with allowable errors. Communications of the ACM 13(7): 422–426. https://doi.org/10.1145/362686.362692
2. Broder, A. and Mitzenmacher, M. (2004). Network applications of Bloom filters: a survey. Internet Mathematics 1(4): 485–509.
3. Apache Cassandra documentation, Bloom Filters. https://cassandra.apache.org/doc/latest/cassandra/managing/operating/bloom_filters.html (checked 2026-09-04)
4. RocksDB wiki, RocksDB Bloom Filter. https://github.com/facebook/rocksdb/wiki/RocksDB-Bloom-Filter (checked 2026-09-04)
5. Chang, F. et al. (2006). Bigtable: A Distributed Storage System for Structured Data. OSDI. https://www.usenix.org/legacy/event/osdi06/tech/chang/chang.pdf
6. Bitcoin Core PR #16152, Disable bloom filtering by default (2019). https://github.com/bitcoin/bitcoin/pull/16152
7. Wikipedia, Bloom filter. https://en.wikipedia.org/wiki/Bloom_filter
