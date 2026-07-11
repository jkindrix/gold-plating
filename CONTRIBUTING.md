# Contributing

This repo catalogs ways to over-engineer things. Contributing to it should be
lightly over-engineered too — but only lightly, because the honest amount of
process for a prose repo is *some*, not *maximal*. (That distinction is the
whole project.)

## Writing an entry

1. Copy [`_template.md`](./_template.md) to `entries/<slug>.md`.
2. Fill in the axis-grouped catalog. Group items under the nine axes from
   [`axes.md`](./axes.md), in canonical order. **Omit axes that don't apply** —
   forcing an axis onto a subject that lacks it is a form of invention, and
   invention breaks the Prime Rule.
3. Tag every item with **Effort** (`[low|med|high]`) and **Bit-factor**
   (`⚖️` worth it / `🎭` theater).
4. Delete the `ENTRY CHECKLIST` comment once you've satisfied it.
5. End with the **Coda** — the sincere, high-leverage subset. This is mandatory.

## The two rules

- **Prime Rule:** every catalogued item must be real — something practitioners
  actually do in earnest at scale. If you can't point at prior art, cut it.
- **Coda Invariant:** every entry ends sincere. Funny is not enough; the reader
  must leave more capable.

## Before you open a PR

Run the same checks CI runs (Python 3.9+, no dependencies):

```sh
python3 scripts/lint-entries.py   # your entry against the structural contract
python3 scripts/test-linter.py    # the linter against its adversarial fixtures
```

The linter enforces the invariants that can be checked mechanically —
frontmatter, canonical axis order, tagged items, the Coda, a sources section,
and that every local citation resolves *inside the repo*. That last check is
what keeps the self-referential flagship honest: a citation can't rot without
failing CI. Local links must be plain relative paths (a `#fragment` is fine);
reference-style links aren't parsed. External links aren't fetched on the
required path — `scripts/check-links.py` sweeps those on a weekly schedule.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`,
`fix:`, `docs:`, `chore:`, etc. It's overkill for a repo this size, which is
exactly why it's here.
