# Claims and evidence

The article's proofs establish the general statements. The companion reproduces
the finite certificates and bounded checks identified below. Stable TeX labels
are supplied because pagination may change in later editions.

| Result | Manuscript locator | Evidence and limits |
| --- | --- | --- |
| Sun Conjecture 3.5, original sum, sign, both branches, all primes p>3 | Theorem 1.1 (`thm:main`), §§2 and 6 | Assembly of the proofs below; `prime_regression.json` tests all 301 primes from 5 to 1999, not all primes. |
| Differential identity theta I(Y)=2YLY | Lemma 2.1 (`lem:differential`) | Product-rule proof; optional `symbolic.py` checks the formal identity. |
| Finite invariant I(U)=0 mod p², including degrees p and 2p | Proposition 2.2 (`prop:finite-invariant`) | Exact resonance formulas and p-divisibility proof; 88 polynomial regressions through p=199 in `invariant_certificates.json`. |
| Lifting a mod-p zero at tD(t) a unit | Theorem 2.3 (`thm:lift`) | Multiplicity proof using deg U<p and the third-order operator. The nonsingularity hypothesis is essential; the companion includes a singular negative control. |
| Inert branch and exceptional p=5 | End of §2 (`eq:inert-result`, `eq:discriminants`) | Sun's mod-p theorem is an explicit imported premise for p>5; five summands settle p=5 directly. |
| P1/P2 and both modular periods | Proposition 3.1 and Theorem 3.2 (`prop:P`, `thm:periods`) | Analytic modularity and cusp holomorphy plus four exact residual vectors through q⁸. `eta_certificates.json` recomputes them by two coefficient algorithms, with extra terms through q²⁰ as regression. |
| Extended-group characters, rational parameters, divisors and CM values | Lemmas 4.1, 4.2, 4.4; Proposition 4.3 | Eta transformation and divisor proofs; E1/E2 finite coefficients, multiplier clearing and strict valence bounds 242>240, 329>312. Appendix A gives the data without requiring software. |
| Integral Hecke polynomial, coefficient degree bounds and weak p² congruence | Lemma 5.1 (`lem:Hecke-core`) | General orbit, cusp and integrality proof. `modular_polynomials.json` reconstructs eight finite examples (653 integer coefficients), not a substitute for the general proof. |
| Degree-p endpoint and finite specialization | Lemma 5.2 and Theorem 5.3 (`lem:endpoint`, `thm:specialization`) | Endpoint binomial congruence removes the possible tᵖ term; specialization evaluates finite polynomials, not an infinite series at a p-adic unit. |
| Split primes in both parity classes | §6.1–6.3 (`eq:CM-even` through `eq:trace`) | Determinant-one and determinant-three matrices, character signs, exact CM roots and a chosen unit embedding. Both classes have fixed companion controls, even with a short requested prime range. |
| Franel evaluation and bridge as a consequence | Corollary 6.1 (`cor:Franel`) | The Franel evaluation is Sun's 2018 Conjecture 3.5. Independent evaluations of the two sums give the bridge; p>5 is necessary for denominator 50. |
| Recurrences of the binomially defined sequences | Appendix B (`eq:telescoping-a`, `eq:telescoping-f`) | Exact telescoping proof with explicit summation endpoints; direct-definition comparisons. |

Finite computations certify modular identities only after the manuscript's
space, holomorphy and valence hypotheses are established. No numerical search,
test count or file hash establishes mathematical novelty or the all-prime
conclusion by itself. See [source roles](SOURCE_COMPARISON.md),
[limits](KNOWN_LIMITS.md) and [reproduction](../REPRODUCE.md).
