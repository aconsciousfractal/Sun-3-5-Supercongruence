# Manuscript build

The delivered standalone PDF was built with **MiKTeX-pdfTeX 4.23 (MiKTeX 25.12)**,
using three pdflatex passes, shell escape disabled and automatic package
installation disabled. The final log contains no warnings, overfull boxes,
underfull boxes or unresolved references. The PDF has 14 A4 pages.

The source suppresses volatile dates and trailer IDs. The builder sets
`SOURCE_DATE_EPOCH=1790985600` (2026-10-03 UTC), `FORCE_SOURCE_DATE=1` and `TZ=UTC`.
The required packages are declared in the preamble: fontenc, lmodern, microtype,
geometry, amsmath, amssymb, amsthm, booktabs, array and hyperref.

| Artifact | SHA-256 |
| --- | --- |
| Sun_3_5_Supercongruence.tex | `cb4b8bd8b2c5d4251a7f8bd2865d9a053a8ce3b717ac2385cfc894d830d5d1da` |
| Sun_3_5_Supercongruence.pdf | `ba64bf6f7a8a14e64fe9a25d168566740b906811308f64f5f0b1280b9db2dd94` |

Run `python -B scripts/build_pdf.py` from the repository root. This writes into
the ignored paper/build directory, leaving the delivered PDF unchanged. See
[REPRODUCE](../REPRODUCE.md) for the explicit update operation.

Byte-identical reproduction is a property of the recorded engine, installed
package versions and fonts. A different TeX installation may produce a visually
equivalent PDF with different bytes. A file digest is an identity check, not a
mathematical or editorial review.

Version 0.1.3 simplifies notation and clarifies the finite-specialization
hypothesis and attribution; see [revision notes](../docs/REVISION_NOTES.md).
The three-pass build completed without warnings. All 14 pages were visually
reviewed, including the coefficient tables, acknowledgments, AI disclosure
and compact bibliography. Printed coefficient tables agree with the fresh
exact replay. The theorem statements and companion computations are unchanged.
