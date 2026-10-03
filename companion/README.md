# Exact companion

From the repository root, run:

```console
python scripts/verify.py
python -O scripts/verify.py --expected evidence
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
```

The default command checks primes from 5 through 1999 and prints one JSON
summary. It computes evidence in an operating-system temporary directory and
removes that directory when finished. It does not update frozen evidence or
write bytecode caches. `--bound N` changes the inclusive prime regression bound;
N must be an integer at least 7. The invariant regression uses the smaller of N
and 199. Both split CM classes also receive fixed controls at 7 and 13, even
when N is smaller than 13. The modular-polynomial windows are fixed independently
of N.

To retain a replay, supply a new or empty directory:

```console
python scripts/verify.py --out /path/to/new-replay --expected evidence
```

`--out` never overwrites an existing nonempty directory. `--expected` compares
independently computed results with the fixed evidence inventory and fails on
changed, missing or extra files. It rejects duplicate JSON keys and nonfinite
numbers. Formatting and line endings do not affect the comparison; integer,
Boolean and floating-point representations are distinguished. The generated
and expected directories must be distinct. A failed command may leave an
incomplete explicit output directory; its files do not constitute a successful
replay. Successful completion returns exit code 0 and a `status: PASS` summary.

The core uses only the Python standard library: integers and `fractions.Fraction`,
with no floating-point acceptance checks. It was exercised with Python 3.14.
All acceptance conditions raise exceptions and remain active under `-O`.

## What is verified

| Check | Exact extent | Mathematical role |
| --- | --- | --- |
| Eta expansions | Six series through q^20, product and logarithmic-derivative engines | Supplies reproducible coefficients. |
| P1 and P2 | Four period identities through q^20; q^0 through q^8 suffice for the paper's weight-8, index-12 argument | Finite certificates together with the paper's modularity and holomorphy proof. |
| E1 and E2 | Residuals through q^20; clearing monomials, cusp orders, weights and bounds 242>240 and 329>312 | Finite certificates together with the paper's geometry and valence proof. |
| Characters and CM geometry | Exact Dedekind-sum phases, character valuations, CM factorizations | Arithmetic checks accompanying the transformation and CM arguments. |
| Period definitions | Binomial definitions and recurrence through n=60; composed eta period through q^60; rational parameter transport | Bounded independent regressions of the normalized periods. |
| Prime conclusions | Every prime 5<=p<=N; raw sum, Franel sum for p>5, transport, two endpoint congruences | Bounded regressions of the theorem and its companion. |
| Original definitions | Both binomial sums for 0<=n<min(N,199) | Checks recurrence coefficients against original definitions. |
| CM matrices | Every split prime in the prime window, plus fixed p=7 and p=13 controls | Exact determinant, coset, image, quadratic root, trace and norm certificates. |
| Invariant | Both recurrences at all primes 5<=p<=min(N,199), including both exact resonances | Bounded regression of the polynomial invariant proof. |
| Singular point | Franel p=11, t=8: D=0 modulo11, U=0 modulo11, U=44 modulo121 | Demonstrates necessity of nonsingularity in the lifting argument. |
| Hecke polynomials | Raw p=5,7,11,13,19,31; Franel p=7,13; stated finite q windows | Exact finite reconstructions; lower-coefficient divisibility, weak identity and split CM factors. |

The default prime window contains 301 primes: 148 split and 153 inert. It gives
398 original-definition comparisons and 602 endpoint checks. The invariant
window contains 88 polynomials. The eight Hecke reconstructions contain 653
stored integer coefficients. These counts describe finite runs. They do not
prove assertions for all primes. The general proof, integrality, holomorphy,
degree bounds and lawful specialization remain mathematical arguments in the
paper. The eta coefficient certificates obtain their proof role precisely
because those hypotheses and the valence bound are established there.

The tests change period parameters and eta coefficients, shorten required
certificate windows, change CM signs and determinant factors in both classes,
corrupt Hecke coefficients, corrupt invariant coefficients and resonances,
and attack the prime domain and frozen-evidence reader. One Hecke corruption
is invisible modulo p^2 and is caught by the exact CM quadratic factor check.

## Paper trace

The following are the stable labels in `paper/Sun_3_5_Supercongruence.tex`.
They identify the mathematical hypotheses accompanying each executable check.

| Evidence or argument | Exact paper labels |
| --- | --- |
| Period P1/P2, q certificates and normalization | `sec:periods`, `prop:P`, `eq:P1`, `eq:P2`, `thm:periods`, `eq:periods` |
| Original recurrence versus binomial definitions | `app:recurrences`, `eq:telescoping-a`, `eq:telescoping-f` |
| Eta cusp orders and valence closure | `app:certificates`, `eq:Ligozat`, `eq:cusp-orders`, `lem:E` |
| E1/E2 and rational parameter transport | `sec:geometry`, `eq:E1`, `eq:E2`, `prop:geometry`, `eq:t-rational` |
| Transformation phases, characters and normalizers | `lem:character`, `eq:characters` |
| CM polynomial factorizations and values | `lem:CM-point`, `eq:CM-point` |
| Differential invariant and formal covariance | `lem:differential`, `eq:Leibniz`, `prop:P` |
| Finite invariant, both resonances and singular control | `sec:invariant`, `prop:finite-invariant`, `eq:finite-invariant`, `eq:LU`, `eq:resonance-p`, `eq:resonance-2p`, `thm:lift`, `eq:lift`, `eq:discriminants` |
| The exceptional prime 5 | `sec:invariant`, direct calculation immediately after `eq:inert-result` |
| Hecke reconstruction, weak identity and endpoints | `sec:Hecke`, `lem:Hecke-core`, `eq:Hecke-product`, `eq:Hecke-core`, `lem:endpoint`, `eq:endpoint`, `thm:specialization`, `eq:finite-specialization`, `eq:K`, `eq:Q-boundary` |
| Both split CM classes, character sign, root, trace and norm | `sec:split`, `eq:CM-even`, `eq:CM-image-even`, `eq:root-even`, `eq:CM-odd`, `eq:CM-class`, `eq:CM-image-odd`, `eq:root-odd`, `eq:trace`, `eq:split-values` |
| Prime regressions, Franel companion and transport | `thm:main`, `eq:main`, `eq:inert-result`, `eq:split-values`, `cor:Franel`, `eq:Franel-value`, `eq:bridge-corollary` |

## Evidence format

Core replays produce exactly these five UTF-8 JSON files, each with
`schema_version: 1` and `status: PASS`:

| File | Contents |
| --- | --- |
| `eta_certificates.json` | Eta metadata and expansions, P1/P2 residuals, E1/E2 residuals and valence data, character phases, period regression and parameter-mutation witnesses. |
| `prime_regression.json` | Inclusive bound, counts, per-prime residues, exceptional p=5 addends, CM matrices and both fixed class controls. |
| `invariant_certificates.json` | Per-prime polynomial coefficient counts and exact resonances, and the singular-point control. |
| `modular_polynomials.json` | Eight integer coefficient arrays, reconstruction windows, weak-identity checks, CM factors, and sign/determinant controls. |
| `verification_summary.json` | Compact scope, bounds and counts. `symbolic_requested` is false and `symbolic_identity_count` is null in the core run. |

Fractions and very large resonance integers use exact decimal strings where
appropriate. Polynomial coefficient arrays list coefficients in ascending
degree. Hecke arrays list C_m(t) in ascending X-degree m, with each C_m in
ascending t-degree. Evidence contains no timestamps or machine paths.

## Optional formal algebra

Fifteen identities in formal indeterminates can also be checked explicitly:

```console
python -m pip install -r requirements-symbolic.txt
python scripts/verify.py --symbolic --out /path/to/new-symbolic-replay
```

This requires SymPy 1.14.0, with mpmath 1.3.0 pinned in the optional requirements.
An unavailable dependency or wrong SymPy version fails the requested run. The
default core never imports SymPy or claims to have run this step.

These identities cover theta I=2YLY, the weight-8 conversion, the W and bracket
covariance laws, extended-group normalizers and their squares, the CM
factorizations and roots, trace and highest resonance. A changed bracket
coefficient produces a nonzero symbolic residual. The symbolic replay adds
`symbolic_identities.json` and changes the summary's symbolic fields. To use
`--expected` with `--symbolic`, supply a frozen directory containing the full
six-file symbolic replay, rather than the five-file core evidence directory.
