# Gold-Plating

*Opportunity catalogs for over-engineering anything — exhaustively, affectionately, and honestly.*

---

**Gold-plating** is the software-engineering term for adding effort or sophistication beyond what a task warrants. This project takes that as an invitation rather than a warning. Each entry picks a subject — a Git repo, a cup of coffee, a pile of laundry — and catalogs the *complete* professional-grade surface for over-engineering it: every gate, every automation, every measurement, every provenance ritual that a serious practitioner might apply at industrial scale, aimed squarely at something that does not remotely need it.

The joke is the scale mismatch. The value is that the joke is a complete education. Read the coffee entry and you'll come out understanding extraction yield, water chemistry, and refractometry — you just arrived through the funny door.

## The two rules that keep it honest

**1. The Prime Rule — everything must be real.**
Every item in every catalog is something practitioners actually do at scale. The humor lives entirely in the *scale mismatch*, never in fabricated absurdity. The moment an entry invents overkill, it stops being a reference and becomes a listicle. If you can't point to someone who does this in earnest, it doesn't go in.

**2. The Coda Invariant — every entry ends sincere.**
Each catalog closes with the high-leverage subset: "if you actually adopted a fraction of this, do these." The bit earns its place by also being useful. An entry that is only funny has failed; an entry that is funny *and* leaves you genuinely more capable has succeeded.

## The universal axes

A wide range of subjects can be over-engineered along some subset of the same nine recurring axes — governance, reproducibility, automation, observability, provenance, resilience, optimization, aesthetics, and meta. Not every axis fits every subject, and naming the ones that *don't* apply is part of an entry's honesty. The axes are defined once in [`axes.md`](./axes.md) and reused by every entry, so the catalogs stay comparable and each new entry has a skeleton to fill rather than a blank page.

## How an entry is structured

Every entry follows [`_template.md`](./_template.md): a framing of the subject, an axis-grouped catalog with effort and "bit-factor" tags, and the mandatory sincere coda. Structural identity across entries is a feature — it makes the catalogs legible and makes the axes comparable across wildly different subjects. Each entry is *narratively* self-contained: it assumes you've read nothing else here.

## This repo gold-plates itself

The flagship demonstration of the project is the repo you are reading. **Gold-Plating over-engineers its own infrastructure**, and every feature it turns on is simultaneously a live, verifiable example in the [Gold-Plating a Git Repo](./entries/git-repo.md) entry. The container is the content. Where the repo enables a governance rule, a template, or a check, the corresponding catalog item cites the real file that implements it.

To keep that self-reference from quietly rotting, every citation points at an actual file in this repo, and a continuous-integration check ([`scripts/lint-entries.py`](./scripts/lint-entries.py), run by [`.github/workflows/lint.yml`](./.github/workflows/lint.yml)) fails the build if a cited path goes missing, a catalog item loses its tags, or an entry drops its coda. It guarantees citation *resolution* and structure — not the truth of the prose — which is a modest promise, kept honestly, and the point.

## Index

*The catalog grows here. Each entry is self-contained and stands alone.*

| Entry | Subject | Status |
|-------|---------|--------|
| [Gold-Plating a Git Repo](./entries/git-repo.md) | A version-controlled repository and its forge | Draft — the self-referential flagship |

<!-- Index note: a flat table is honest at this size. Past ~15 entries, group it
     by domain or generate it from entry frontmatter — but not before, since
     pre-building for a scale you don't have is itself ungrounded gold-plating. -->


## License

Dual-licensed, because this repo is both prose and code:

- **Prose and catalog content** (everything in `entries/`, the `.md` documents, this README) — [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Quote it, translate it, remix it, write your own entries in this format — just keep the attribution.
- **Code and configuration** (scripts, workflows, templates, config) — [MIT](./LICENSE).

Attribution is deliberate: the framework here — the nine axes, the Prime Rule and Coda Invariant, the tag system — is the original work, and keeping its provenance attached is, fittingly, axis #5.
