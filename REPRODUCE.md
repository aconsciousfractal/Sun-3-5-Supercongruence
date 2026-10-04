# Reproduction

Run commands from the repository root. Core code requires Python 3.10 or newer,
the standard library and no network. The paper PDF is included.

## Exact companion

```text
python -B scripts/verify.py --expected evidence
python -B -O scripts/verify.py --expected evidence
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
python -B scripts/check_manifest.py
python -B scripts/check_manifest.py --evidence
```

The default regression window is all primes 5 through 1999. The invariant
polynomial regression is bounded by 199. Eta and modular-polynomial
certificates have their own stated fixed precisions. Running with a smaller
`--bound` changes the regression output and is not expected to match the
delivered default evidence.

The verifier uses a temporary directory unless `--out PATH` is explicitly
supplied. An output directory must be new or empty. The five JSON files are
independently recomputed; expected values are never fed into a calculation.
Missing, extra, changed or invalid JSON records fail the comparison.
See [companion documentation](companion/README.md) and [evidence roles](docs/EVIDENCE.md).

## Optional symbolic identities

```text
python -m pip install -r requirements-symbolic.txt
python -B scripts/verify.py --symbolic
python -B -O scripts/verify.py --symbolic
```

This explicitly requests the additional SymPy checks. A missing dependency
fails the command. A core PASS does not mean symbolic checks were requested.
The five-file core evidence directory excludes the optional sixth output;
do not combine `--symbolic` with `--expected evidence`.

## Paper

Use an existing pdflatex installation with the packages declared in the TeX
preamble. The build script does not install TeX or packages and disables
shell escape and MiKTeX package installation.

```text
python -B scripts/build_pdf.py
```

This writes the PDF and build_info.json into the ignored paper/build directory.
The delivered PDF is not overwritten. An author may explicitly use `--update`
after reviewing the rebuilt document; the distribution manifest must then be
refreshed intentionally.

The source suppresses volatile PDF dates and IDs; the builder fixes
SOURCE_DATE_EPOCH and performs three passes. Identical bytes are expected with
the same TeX engine, packages and fonts, not across every TeX distribution.
The recorded compiler and PDF digest are in [paper/BUILD.md](paper/BUILD.md).

## Inventories and source archive

EVIDENCE_SHA256.txt pins code, tests, verification configuration and exact
evidence. MANIFEST_SHA256.txt covers the complete delivered tree except itself.
Neither is a signed authenticity claim. Normal verification never rewrites them.
After deliberate reviewed edits, `scripts/check_manifest.py --write` and
`--write --evidence` are explicit authoring operations.

```text
python -B scripts/make_archive.py --output <existing-output-directory>/Sun-3-5-Supercongruence-0.1.2.zip
```

Replace the placeholder with an existing writable directory outside the repository;
quote the complete path if it contains spaces.
The destination must not already exist and must lie outside the repository.
The ZIP contains only the verified inventory, with deterministic entry metadata;
its payload bytes are rechecked and frozen before writing. It excludes Git state,
build outputs and caches. An extracted copy supports the
same commands without a Git checkout. Hosted CI is configured separately; its
presence is not evidence that a hosted run has occurred.
