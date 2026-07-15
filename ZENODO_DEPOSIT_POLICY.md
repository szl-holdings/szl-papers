# Zenodo deposit policy

The canonical Thesis v8 publication already exists as version DOI
[`10.5281/zenodo.21184984`](https://doi.org/10.5281/zenodo.21184984) under concept DOI
[`10.5281/zenodo.20567256`](https://doi.org/10.5281/zenodo.20567256).

Do **not** publish a GitHub release with Zenodo auto-mint enabled in an attempt to update that
record. A GitHub-triggered deposit creates a new Zenodo record; `.zenodo.json` supplies metadata
but cannot select and update an existing DOI. The root `.zenodo.json` is retained only as
human-readable reference metadata.

To update Thesis v8, use the owner's authenticated Zenodo session or API to create a new version
under the existing concept. To publish P1 or P2, first confirm that no paper-specific record exists,
then create or reserve exactly one concept for that paper and update that same record/version after
arXiv assigns an identifier. Never reuse the umbrella Ouroboros concept DOI as a paper DOI.

Before any deposit:

1. compare normalized title, author/ORCID, abstract, and content hash against the public estate;
2. confirm whether the object is a new work, a new version, or a supplement;
3. preserve the appropriate Zenodo relation rather than asserting `isIdenticalTo` without
   byte/content identity;
4. upload the exact reviewed PDF/source bundle and record its hash;
5. add the eventual arXiv identifier to that same Zenodo record instead of creating a duplicate.
