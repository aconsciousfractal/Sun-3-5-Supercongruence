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
| Sun_3_5_Supercongruence.tex | `e481172cc59def29ef32a925627912c8eb99f393c1ac4da6fdf797b669c8e1a9` |
| Sun_3_5_Supercongruence.pdf | `7219e00b24e06a58101b7058fb0e927b6d255584ad4e1b45bb5cd3d570b5879f` |

Run `python -B scripts/build_pdf.py` from the repository root. This writes into
the ignored paper/build directory, leaving the delivered PDF unchanged. See
[REPRODUCE](../REPRODUCE.md) for the explicit update operation.

Byte-identical reproduction is a property of the recorded engine, installed
package versions and fonts. A different TeX installation may produce a visually
equivalent PDF with different bytes. A file digest is an identity check, not a
mathematical or editorial review.

The recorded PDF was also rebuilt from the extracted source archive using the
same installed engine and packages; its SHA-256 was identical to the delivered
PDF above. All 14 rendered pages were visually inspected.
