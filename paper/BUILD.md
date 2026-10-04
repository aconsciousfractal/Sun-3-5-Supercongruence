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
| Sun_3_5_Supercongruence.tex | `a97307ebb92843819c7d889879ecdc86c397d2b7a77f3291001a699d9e1b2b0b` |
| Sun_3_5_Supercongruence.pdf | `613e3274c232962ee801b6b0ccb5b49174ae0606fbb395e9422b02b19f302fab` |

Run `python -B scripts/build_pdf.py` from the repository root. This writes into
the ignored paper/build directory, leaving the delivered PDF unchanged. See
[REPRODUCE](../REPRODUCE.md) for the explicit update operation.

Byte-identical reproduction is a property of the recorded engine, installed
package versions and fonts. A different TeX installation may produce a visually
equivalent PDF with different bytes. A file digest is an identity check, not a
mathematical or editorial review.

Version 0.1.2 adds the manuscript AI-use disclosure. The three-pass build
completed without warnings. Pages 1--12 render identically to version 0.1.1;
the changed pages 13--14 were visually inspected. The mathematical source
is unchanged; only the disclosure, package version and inventory digest differ.
