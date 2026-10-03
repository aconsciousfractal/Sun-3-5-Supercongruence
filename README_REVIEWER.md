# Reading and verification path

Start with the main theorem in the [paper](paper/Sun_3_5_Supercongruence.pdf),
then use the [claim map](docs/CLAIM_MAP.md) to follow its dependencies.

The two branches are logically separate. The finite invariant proves the
inert branch from Sun's published modulo-p theorem. The split proof develops
the modular periods, their geometry, the polynomial degree bound and the CM
specialisation. The relation to the Franel sum appears only after both
evaluations. Read the direct p=5 check as part of the main theorem.

For a close proof reading, focus on:

1. The two resonant coefficients of the finite invariant, and the proof that
   a nonsingular zero is exactly double.
2. Holomorphy of the period identities at every cusp before using a finite
   coefficient bound; the same issue for the Hecke quotients.
3. Integral polynomial coefficients, the bound floor(m/2), and the degree-p
   endpoint that converts formal agreement to a finite polynomial congruence.
4. Both CM parity classes, the character and determinant factors, and the
   choice of an embedding where the displayed root is a unit.

The [source comparison](docs/SOURCE_COMPARISON.md) distinguishes imported
results from arguments proved here. In particular, the stronger modulo-p³
theorem in Beukers is not applied outside its hypotheses.

Run the commands in [REPRODUCE](REPRODUCE.md). The supplied evidence consists
of exact finite certificates and regression records, not a formal verification
of the entire paper. The [evidence guide](docs/EVIDENCE.md) explains which
finite checks close an identity only together with a proved degree/valence bound.
