# Sun's supercongruence for an Apéry-like sequence

**Oleksiy Babanskyy**

Manuscript and exact-arithmetic companion, version **0.1.3**.

This revision simplifies notation following comments from Zhi-Hong Sun,
states the prime hypothesis explicitly in the finite-specialization theorem,
and clarifies the attribution of its endpoint argument. The conclusions,
companion code and computational results are unchanged.

For
$$
a_n=\sum_{j=0}^{n}\binom{n}{j}^{2}\binom{2j}{j},
\qquad G_p(1/54)=\sum_{n=0}^{p-1}\frac{\binom{2n}{n}a_n}{54^n},
$$
the paper proves, for every prime $p>3$,
$$
(-1)^{(p-1)/2}G_p(1/54)\equiv
\begin{cases}
4x^2-2p \pmod{p^2},&p=x^2+3y^2\equiv1\pmod3,\\
0 \pmod{p^2},&p\equiv2\pmod3.
\end{cases}
$$
This is the congruence stated as Conjecture 3.5 in
[Zhi-Hong Sun, AIMS Mathematics 7 (2022), p.2742](https://doi.org/10.3934/math.2022153).

The inert branch follows from an exact finite differential invariant and a
double-root lifting argument. The split branch follows from eta periods,
an integral modular polynomial, a degree bound and finite CM specialisation.
The companion Franel sum at 1/50 is evaluated for $p>5$, as conjectured in
[Sun's 2018 paper, Conjecture 3.5](https://maths.hytc.edu.cn/__local/3/45/77/77F7497DDFD531E8688ED13C0D0_262306C8_24EB4.pdf).
The relation between the two sums is then a corollary. The original sum at
$p=5$ is handled directly.

- [Paper PDF](paper/Sun_3_5_Supercongruence.pdf) and [standalone TeX](paper/Sun_3_5_Supercongruence.tex)
- [Reading path](README_REVIEWER.md) and [reproduction](REPRODUCE.md)
- [Claim and evidence map](docs/CLAIM_MAP.md)
- [Sources and attribution](docs/SOURCE_COMPARISON.md), [scope and limits](docs/KNOWN_LIMITS.md)
- [Revision 0.1.3 and review scope](docs/REVISION_NOTES.md)

From the repository root, with Python 3.10 or newer:

```text
python -B scripts/verify.py --expected evidence
python -B -O scripts/verify.py --expected evidence
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
python -B scripts/check_manifest.py
python -B scripts/check_manifest.py --evidence
```

The core replay needs only the Python standard library and no network. It
recomputes exact certificates and bounded regressions before comparing the
five delivered JSON files. It does not infer a theorem from a finite prime
window. Optional symbolic checks and the existing-pdflatex build are described
in REPRODUCE.

The work has not undergone full independent specialist refereeing. No claim of
bibliographic priority is made. See [AI assistance](AI_USE.md).
Code, data and documentation use [MIT](LICENSE); the manuscript uses
[CC BY 4.0](LICENSE_MANUSCRIPT.md). See [licence scope](LICENSE_SCOPE.md)
and [citation metadata](CITATION.cff).

## Companion identity

The package is identified by VERSION and EVIDENCE_SHA256.txt, whose SHA-256 is
printed in the paper and recorded in [the evidence guide](docs/EVIDENCE.md).
That evidence identity excludes the paper and prose that cite it. The full
distribution is covered separately by MANIFEST_SHA256.txt.

Companion repository:
[aconsciousfractal/Sun-3-5-Supercongruence](https://github.com/aconsciousfractal/Sun-3-5-Supercongruence).
The package version identifies this distribution; it does not denote a journal
version of record.
