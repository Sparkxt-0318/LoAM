
---

## TASK 3 — detectability literature — **COMPLETE**
Branch `claude/sources-detectability` · `136 passed` · no rows written

All five citations confirmed against Crossref. Availability checked via
Unpaywall. Two retrieval attempts each; **no paywall circumvented**.

| paper | status | outcome |
|---|---|---|
| von Haden et al. 2020, GCB 26:3759 | green OA | **RETRIEVED** and read (OSTI accepted manuscript) |
| Smith 2004, GCB 10:1878 | bronze OA | **403 from Wiley bot protection** — free to read, a browser will open it |
| Bradford et al. 2023, Geoderma 440:116719 | **gold OA** | **403** from ScienceDirect and DOAJ — openly licensed, a browser will open it |
| Saby et al. 2008, GCB 14:2432 | closed | no OA location |
| de Gruijter et al. 2016, Geoderma 265:120 | closed | no OA location |

**The one real find: von Haden Table 1 is stronger than what component 6
currently rests on.** Mean absolute percentage error in SOC stock, fixed depth
vs equivalent soil mass, under simulated ±2.5 cm compaction/expansion:
**ESM 0.2–1.1%, FD 2.1–23.2%.** Our `VC-BDC-001..004` carry 17 / 16.2 / 8 / 6%
from Fowler 2023 — von Haden's FD range brackets all four, from an independent
study with an explicit ESM comparison. Also supplies a citation for the
bulk-density-change mechanism (5–20% after land-use change, tillage, residue
addition) that our BDC rows currently assert uncited.

⚠️ **Table 1's column alignment was recovered from PDF text extraction and needs
visual confirmation against the typeset version before any number is tabled.**
The range is unambiguous; the mapping of values to bulk-density rows is not.

**Blockers, logged per rule 6:** Smith 2004 and Bradford 2023 are both *openly
readable* and both blocked by bot protection, not by a paywall. Two attempts
each (publisher + alternate legitimate host). **These are one browser click for
a human** — the highest-value five minutes available to the PI in this whole
handoff, since Bradford 2023 is the paper Potash et al. are answering and
therefore the other half of the argument D-037/D-038 position against.
