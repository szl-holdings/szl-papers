# Hugging Face dataset cards sourced from this repository

HF upgrade plan P18 makes this repository the GitHub source for four Hugging Face
datasets. Each `datasets/<id>/README.md` is a **verbatim import** of the current Hub
card (read-only fetch; nothing was written to the Hub), so GitHub holds the card
before any mirror publishes it.

| Hub dataset | Card imported from Hub revision | sha256 of the imported card |
|---|---|---|
| [`SZLHOLDINGS/thesis-v18-formal-verification`](https://huggingface.co/datasets/SZLHOLDINGS/thesis-v18-formal-verification) | `9a08e0c1fccf410b447769091ebeb26885942f3c` | `7b138b57d39c0cbededd7d35a2ecb4467af440c5331b17a6b8cd3751a73bb469` |
| [`SZLHOLDINGS/ouroboros-arxiv-preprint`](https://huggingface.co/datasets/SZLHOLDINGS/ouroboros-arxiv-preprint) | `704753d8a0328762deb127bddf88867df275bcbf` | `14d993e94a98e5cb0370264c1533d25e38117e34890707a1aa6becbdeade8f8e` |
| [`SZLHOLDINGS/why-we-lead`](https://huggingface.co/datasets/SZLHOLDINGS/why-we-lead) | `51df5c36889742255e9bee91b156cde58ff99bb3` | `c58289fee591efa76df92c0294898923beb69705ee1d48c8a70ce24e8b88e1bd` |
| [`SZLHOLDINGS/thesis-corpus-v18`](https://huggingface.co/datasets/SZLHOLDINGS/thesis-corpus-v18) | `e24c1e718ffe0ee989da7230a922b0065035b1b0` | `f0f0334b4e0706ee786e62e6c928e17343d54f377dc87cc38b083ba2196b0f5e` |

## License conflict (owner decision required)

This repository's [`LICENSE`](../LICENSE) is **CC-BY-4.0**. All four Hub cards declare
`license: apache-2.0`. The cards are imported unchanged, so they still carry the Hub's
declaration. That declaration is recorded here as the Hub's current state. It is not a
licensing decision made by this repository.

No mirror may publish these cards until the owner decides one of the following:

- **Relicense the Hub datasets to CC-BY-4.0.** The cards are then re-rendered with
  `license: cc-by-4.0`.
- **Keep apache-2.0 for these datasets.** The repository then states that carve-out
  explicitly, per dataset.

## Lineage and writers (read 2026-09-29)

- The first Hub commits for `thesis-v18-formal-verification` and `ouroboros-arxiv-preprint` are
  local uploads from 2026-05-29 (arXiv preprint package, thesis figures). No committed workflow
  wrote them.
- `why-we-lead` links no source. Its card labels it a HISTORICAL Doctrine v7 snapshot. This
  repository is its LIKELY source.
- `thesis-corpus-v18` is also referenced by `szl-holdings/szl-kernels` (`scripts/forge.py`).
  Under plan D1 there is one writer per asset, so that path must move here or become a reader.
- Three cards were last edited on the Hub on 2026-09-28 in the "estate audit" Hub PRs.
  `why-we-lead` was not part of that audit. Its latest Hub commits are "card: HISTORICAL
  Doctrine v7 snapshot" (2026-08-28), then a license commit and a readiness-audit commit
  (2026-08-31).

## Publishing status

No workflow publishes these cards or payloads yet. Three things are missing:

1. the license decision above;
2. the org-level `reusable-hf-mirror.yml` in `szl-holdings/.github` (not yet present);
3. a Hugging Face credential in this repository: an `HF_TOKEN` scoped to these datasets,
   or a Trusted Publisher.
