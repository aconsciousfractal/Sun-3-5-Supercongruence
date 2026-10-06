# Revision 0.1.3 — 6 October 2026

The manuscript was revised after comments from Zhi-Hong Sun. The main theorem,
its domain, and the Franel corollary are unchanged.

## Changes

- Use `G_p(1/54)` and `F_p(1/50)` throughout, with the sign
  `(-1)^((p-1)/2)` written explicitly. Remove the auxiliary names for these
  quantities and for the two coefficient sequences; define the generating
  functions directly from the binomial sums.
- State `p > 3` explicitly in Theorem 5.3 and explain which first coefficient
  is used in its degree-p comparison.
- Credit the coefficient-comparison mechanism in the proof of Beukers'
  Theorem 6.1, while retaining the separate proof here at modulus p².
- Acknowledge Sun's comments, retain the full AI-use disclosure, and update
  the README, version, citation metadata, build record and inventories.

## Review and checks

The author-side AI review covered the complete manuscript and companion,
including the two resonant invariant coefficients, the nonsingular lifting
hypothesis, the exceptional prime 5, modularity before coefficient comparison,
cusp orders, characters, integral Hecke coefficients, the degree-p endpoint,
both CM parity cases, and finite specialization. No invalidating mathematical
error was identified in this review. This is not independent specialist
refereeing or proof-assistant verification.

The unchanged core replay passed normally and with Python `-O`: 301 primes
from 5 through 1999, 398 comparisons with the binomial definitions, 602 endpoint
checks, 88 invariant polynomials, and eight exact Hecke reconstructions with
653 integer coefficients. All 14 tests passed in both modes. The optional
15 symbolic identities also passed in both modes. The printed coefficient
tables were compared with the recomputed evidence.

Additional review checks verified both Appendix B telescoping identities as
rational identities and recomputed both sums directly from binomial definitions
for the 77 primes from 5 through 401. These separately written checks were
performed by the same AI reviewer with access to the proof; they do not confer
independent-review status. The finite prime tests are consistency checks, not
proofs for all primes. The general arguments remain in the manuscript.

The companion code, tests and five frozen evidence files are byte-for-byte
unchanged. The evidence-inventory digest changes because it includes VERSION.
The scope and unresolved bibliographic limits in [SOURCE_COMPARISON](SOURCE_COMPARISON.md)
and [KNOWN_LIMITS](KNOWN_LIMITS.md) remain in force.
