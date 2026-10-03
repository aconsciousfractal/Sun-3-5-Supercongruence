# Source roles and literature comparison

The article proves the statement printed as Conjecture 3.5 in Sun's 2022 paper.
This identifies the target without asserting that this is its first proof.
The following comparison records a bounded search and targeted primary-source
reading on 2026-10-03; it is not an exhaustive priority determination.

## Sources used in the proof

| Source | Exact role | Boundary |
| --- | --- | --- |
| Z.-H. Sun, *Supercongruences involving Apéry-like numbers and binomial coefficients*, AIMS Mathematics 7(2) (2022), 2729–2781, [DOI 10.3934/math.2022153](https://doi.org/10.3934/math.2022153), [publisher PDF](https://www.aimspress.com/aimspress-data/math/2022/2/PDF/math-07-02-153.pdf) | Conjecture 3.5, printed p.2742, is the target. Theorem 3.5 and its proof, p.2739, supply the inert mod-p input for p>5. Definitions and recurrences are on pp.2729–2730. | Theorem 3.5 and Conjecture 3.5 are different statements. The article proves its own recurrences in Appendix B, lifts the inert congruence to p², and treats p=5 separately. |
| F. Beukers, *Supercongruences using modular forms*, [arXiv:2403.03301v3](https://arxiv.org/abs/2403.03301v3), 16 June 2025 | Lemma 3.7, pp.17–18, and §5 provide the modular-polynomial method; §9.15, p.33, records the Franel model and parameter 1/50. | The character must extend to the Atkin–Lehner group and be trivial on the base group. The stronger p³ theorem has additional hypotheses; it is not applied to these examples. The present article proves the required weaker p² construction. |
| J. Rouse and J. J. Webb, *On spaces of modular forms spanned by eta-quotients*, [arXiv:1311.1460v3](https://arxiv.org/abs/1311.1460v3), 14 November 2014 | Eta modularity criterion and cusp-order formula, p.2. | The transformation conditions alone do not establish cusp holomorphy. The article lists and checks the cusp data. |
| [NIST DLMF §23.18](https://dlmf.nist.gov/23.18), equations 23.18.5–23.18.7 | Eta transformation and Dedekind-sum phases. | The displayed transformation in the article is for determinant-one integral matrices. Determinant-three and determinant-six transformations are derived by composition. |

The characteristic-zero valence bound used for the finite certificates is
classical. The article gives the reduction from level six to the level-one
valence formula by a coset product. Its use is distinct from a general
congruence version of Sturm's theorem.

## Nearby results screened

Matching the target requires the same a_n, denominator 54, sign, modulus p²,
both prime branches and full domain p>3. A related Franel or three-binomial
evaluation alone does not supply the missing transformation to that sum.

| Work | Observation from the screened text | Reading limit |
| --- | --- | --- |
| Sun, *Congruences for sums involving Franel numbers*, IJNT 14(1) (2018), 123–142, [author PDF](https://maths.hytc.edu.cn/__local/3/45/77/77F7497DDFD531E8688ED13C0D0_262306C8_24EB4.pdf) | Theorem 2.2 (author PDF p.6) evaluates the denominator-50 Franel sum modulo p. Conjecture 3.5 (p.16) states its full p² evaluation for p>5, proved in the present Corollary 6.1. | Both statements were read directly. This is the antecedent conjecture for the Franel corollary, distinct from Sun's 2022 Conjecture 3.5 for the denominator-54 sum. The 2018 conjecture is not an imported theorem. |
| Sun–Ye, *Supercongruences via Beukers' method*, preprint [arXiv:2408.09776v4](https://arxiv.org/abs/2408.09776v4), 19 September 2024, 59 pages | Targeted screening of this preprint did not identify the exact denominator-54 or denominator-50 theorem. | Not a complete theorem-by-theorem review. This version is not assumed equivalent to the journal article below. |
| Sun–Ye, *Supercongruences Involving Products of Three Binomial Coefficients via Beukers' Method*, Results in Mathematics 80 (2025), article 143, [DOI 10.1007/s00025-025-02451-0](https://doi.org/10.1007/s00025-025-02451-0) | Publisher metadata identify this journal title and publication date, 24 June 2025. | The journal version of record remains unread; subscription preview and failed author-copy retrieval. No theorem-level exclusion of overlap is inferred from the preprint screening. This work is not a premise of the proof. |
| G.-S. Mao, *On Some Congruence Conjectures Involving Binary Quadratic Forms*, PRIMS 61 (2025),611–625, [DOI 10.4171/PRIMS/61-4-1](https://doi.org/10.4171/PRIMS/61-4-1), [publisher full text](https://ems.press/content/serial-article-files/51742) | The introduction discusses an established denominator-108 three-binomial supercongruence and further refinements. | Introduction and target searches were screened; this does not establish a bridge to the original denominator-54 sum. |
| G.-S. Mao, *Proof of Some Conjectural Congruences Involving Binomial Coefficients and Apéry-like Numbers*, Front. Math.21 (2026),341–368, [DOI 10.1007/s11464-024-0146-x](https://doi.org/10.1007/s11464-024-0146-x), [author-posted preprint](https://www.researchgate.net/publication/359579007_PROOF_OF_SOME_CONJECTURAL_CONGRUENCES_INVOLVING_BINOMIAL_COEFFICIENTS_AND_APERY-LIKE_NUMBERS) | Preprint Theorem 1.2 proves both p² branches for the different W_n sum with denominator −12. Theorems 1.4 and 1.6 treat S_n/16 and G_n(x). | Targeted theorem inventory in the author-uploaded preprint; journal version of record unread (publisher access restriction/HEP retrieval timeout). No byte-equivalence assumed. |
| Z.-H. Sun, *Congruences involving the products of three binomial coefficients*, RNT 12 (2026),68, [DOI 10.1007/s40993-026-00749-8](https://doi.org/10.1007/s40993-026-00749-8) | Publisher abstract concerns weighted three-binomial variants. | Full text unread: subscription preview and CAPTCHA on the official author attachment. The abstract cannot exclude an overlapping theorem. |
| Li–Sun, *Weighted bilinear identities and supercongruences for Apéry-like polynomials*, [arXiv:2609.28098v1](https://arxiv.org/abs/2609.28098v1) | Initial definitions and target searches concern different polynomial families and weighted squared sums. | Targeted screening only. |
| Z.-H. Sun, *Identities and congruences involving orthogonal polynomials and Apéry-like numbers*, [arXiv:2609.29910v1](https://arxiv.org/html/2609.29910v1) | Theorem 4.8 involves weighted a_n² sums with denominators 9 and 81; Theorem 4.6 involves weighted f_n². Theorem 2.1 gives a nearby quadratic endpoint telescoping identity for recurrence sequences. | Full HTML available, targeted theorem reading. No exact denominator-54/50 claim identified. The nearby quadratic identity is a reason to avoid a broad novelty claim for quadratic-invariant methods. |

No proof of the exact full target was identified in the material screened.
Unread journal versions, Sun's broader corpus and book, and the absence of an
exhaustive citation-database search prevent an absence-of-prior-work claim.
These are attribution and editorial-assessment limits, not premises silently
used in the mathematical proof. Third-party full texts are linked, not bundled.
