# Exact evidence and its mathematical role

The files in evidence/ are recomputed by the core verifier. They use integers,
fractions and finite series arithmetic, without floating-point acceptance.

| File | Role | What it does not establish alone |
|---|---|---|
| eta_certificates.json | Direct period identities P1/P2; eta geometry, cusp orders and E1/E2 coefficient certificates | Modularity and holomorphy must first be proved in the paper; only then does the valence bound close the identities |
| prime_regression.json | Original binomial definitions, endpoint congruences and branch sums for the stated prime window | A uniform theorem for untested primes |
| invariant_certificates.json | Exact coefficients, two resonances and nonsingular/singular controls in a bounded window | The general lifting argument without the written proof |
| modular_polynomials.json | Eight exact finite reconstructions, degree/coefficient checks and CM controls | The all-prime degree theorem or all-prime specialisation |
| verification_summary.json | Bounds, counts and explicitly requested check modes | Mathematical review or publication status |

The 36 sufficient coefficient slots for the four weight-8 period identities
are q⁰ through q⁸. The verifier also carries extra precision and parameter
mutations. For E1/E2 the written proof gives the strict valence inequalities
242>240 and 329>312. Those bounds are separate from the arbitrary prime
regression limit 1999.

EVIDENCE_SHA256.txt covers the code, tests, verification configuration and these
five files. The paper/prose are excluded from that digest to avoid a circular
identity. The full delivered tree is instead covered by MANIFEST_SHA256.txt.

Version 0.1.2 evidence-inventory SHA-256 (the hash of EVIDENCE_SHA256.txt itself):

```text
a8bb62720842b534d6d92927c0ac628f33d922eb07d95d642a86d4c8efb63214
```

The core record contains 301 primes (148 split, 153 inert), 398 comparisons
with original binomial definitions, 602 endpoint checks, 88 invariant
polynomials and eight Hecke polynomials with 653 integer coefficients.
Optional symbolic mode checks 15 formal identities; it is intentionally absent
from the five-file core inventory and must be requested explicitly.
