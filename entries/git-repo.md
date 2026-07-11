---
date: 2026-07-10
author: Justin Kindrix
context: A standalone catalog of ways to over-engineer a Git repository and the forge it lives on. Organized by the universal axes. Every item is something teams do in earnest at scale; the humor is aiming all of it at a repository that does not need it. Ends with a sincere high-leverage subset. This is also the repo's own flagship — where an item is enabled here, it cites the real file that implements it.
---

# Gold-Plating a Git Repo

A Git repository is, at rest, a folder with a `.git` directory in it. You could run a serious software project out of one with nothing but `git commit` and a shared remote, and people did, for years, happily.

You could also treat that folder the way a Fortune 100 platform team treats the system of record for a regulated product: gate every change behind reviewers and machine checks, sign every commit, generate cryptographic provenance for every build, measure your own delivery performance against an industry framework, and enforce all of it with a second layer of automation that exists only to make sure the first layer is obeyed. None of it is fake. All of it ships in real organizations. Most of it is gloriously unnecessary for a personal repo, which is what makes it worth cataloging.

Effort tags: `[low]` file/setting/minutes · `[med]` a tool or workflow to wire in · `[high]` real integration work.
Bit-factor tags: `⚖️` genuinely worth it even here · `🎭` theater at this scale, adopt for the bit.

> **How this entry stays honest.** Some items below are *enabled in this very repo* and cite the real file that implements them — those citations are checked by [`../scripts/lint-entries.py`](../scripts/lint-entries.py), so if one rots, the build fails. The rest are catalogued but not enabled here, and say so. Where this repo declines a step, it admits it rather than pretending — an entry about over-engineering a repo would be a poor place to fudge.

---

## 1. Governance

*Who is allowed to change it, and under what conditions may a change land?*

- **Branch protection / rulesets** `[low] ⚖️` — Forbid direct pushes to the default branch; require pull requests. Modern forges layer *rulesets* on top: pattern-matched targets, stacked rules, priorities. On a solo repo you are the only person you're protecting the branch from, which is either pointless or profound depending on your mood. *(Catalogued; activates when this repo is published to a forge — a ruleset can't be expressed as a committed file.)*
- **Required status checks** `[low] ⚖️` — A change cannot merge until named checks pass. Here, the honest one is the entry linter — a PR that breaks a citation cannot land. *(Enabled in spirit via [`../.github/workflows/lint.yml`](../.github/workflows/lint.yml); enforced as a *required* gate only once branch protection is configured on the forge.)*
- **CODEOWNERS** `[low] 🎭` — Auto-request reviewers by path. This repo ships a [`../CODEOWNERS`](../CODEOWNERS) that assigns every path to a single maintainer, so it dutifully requests review from the author on the author's own pull requests. Pure ceremony, enabled precisely so this line isn't lying.
- **Required reviews with a minimum count** `[low] 🎭` — Demand N approvals before merge. N=2 on a one-person repo is a koan.
- **Required signed commits** `[med] ⚖️` — Reject any commit without a valid GPG/SSH signature (see Provenance for the signing itself). *(Catalogued; enforcement is a forge-side rule, not committed here.)*
- **Linear history required** `[low] ⚖️` — Ban merge commits; force squash or rebase so the graph stays a line. Genuinely nice; genuinely unnecessary at this size.
- **Merge queue** `[high] 🎭` — Serialize merges and re-run checks against the *combined* queued result so two individually-green PRs can't merge into a broken state. Requires more than one PR in flight, more than one contributor, and a straight face. The platonic over-engineering item.
- **Tag & release protection** `[low] ⚖️` — Restrict who may create or move `v*` tags so releases can't be forged or clobbered.
- **PR template as a soft gate** `[low] ⚖️` — Not enforcement, but a checklist every PR inherits. This repo ships one: [`../.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md).

## 2. Reproducibility

*Can I reproduce the exact result deterministically, every time?*

- **Pinned CI action versions** `[low] ⚖️` — Reference actions by immutable commit SHA rather than a movable tag, so a supply-chain compromise of a tag can't silently change your build. *(Enabled here: [`../.github/workflows/lint.yml`](../.github/workflows/lint.yml) pins both actions to full commit SHAs, tag kept as a comment for humans. This item spent its first days as an admitted gap; the correction landed when the pin did.)*
- **Zero-dependency tooling** `[low] ⚖️` — The strongest reproducibility move is having nothing to reproduce. The entry linter is deliberately pure-standard-library Python, so there is no lockfile to pin and no dependency to drift. Sometimes the over-engineered choice is the austere one.
- **Devcontainer / declarative dev environment** `[med] 🎭` — Ship a `devcontainer.json` or a Nix flake so any contributor gets a bit-identical toolchain. For a repo whose toolchain is "a Python interpreter you already have," this is a spacesuit for a walk to the mailbox.
- **Reproducible builds** `[high] 🎭` — Byte-identical outputs from identical inputs, verifiable by a third party. Meaningful for a compiler or a distro; there is no build here to make reproducible, which is itself the honest note.

## 3. Automation

*What manual step can I remove?*

- **CI on every push and PR** `[low] ⚖️` — The baseline. This repo commits a workflow ([`../.github/workflows/lint.yml`](../.github/workflows/lint.yml)) that runs the entry linter and its test suite on every push and pull request once the repo is hosted on a forge — and the same checks run locally with two commands in the meantime.
- **Structured issue forms** `[low] ⚖️` — Replace the free-text issue box with a typed form. This repo ships one for proposing new subjects: [`../.github/ISSUE_TEMPLATE/new-entry.yml`](../.github/ISSUE_TEMPLATE/new-entry.yml). It even makes the proposer do the Prime-Rule check themselves.
- **Bots: labeler, stale, welcome, release-drafter** `[med] 🎭` — Auto-label PRs by path, auto-close inactive issues, greet first-timers, continuously draft the next release's notes. A full bot fleet tending a repo that gets a commit a week is a beautiful thing to behold.
- **semantic-release** `[med] 🎭` — Parse commit messages, compute the next version, tag, generate a changelog, and publish — all with no human touching a version number. Requires the discipline of Conventional Commits (see Meta) and a release cadence this repo does not have.
- **Scheduled maintenance workflows** `[low] 🎭` — Nightly cron jobs: dependency-drift checks, docs link-checkers, "is the pinned language still supported?" watchers. Robots doing rounds in an empty building.

## 4. Observability

*What am I eyeballing that I could measure?*

- **CI analytics / flaky-test tracking** `[med] 🎭` — Dashboards of build duration, failure rate, and flaky tests over time. This repo's "test suite" is one linter that runs in under a second, so the dashboard would be a single flat line, lovingly rendered.
- **DORA metrics** `[high] 🎭` — Compute the DORA software-delivery metrics from the forge's API and chart them: deployment frequency, change lead time, change-fail rate, failed-deployment recovery time, and — since the framework grew from its original four keys to five — deployment rework rate. An industry framework for measuring elite delivery performance, pointed at a markdown repo maintained by one person for fun. Peak axis. (That the metric count itself moved is a live reminder of what this whole entry signs up to maintain.)
- **Repository insights over time** `[low] 🎭` — Snapshot traffic, clones, and contributor stats into a tracked artifact so you can chart the popularity of a repo about over-engineering repos. Recursion is a kind of telemetry.

*(This axis is nearly all `🎭` here — a prose repo has almost nothing worth instrumenting, and pretending otherwise would be invention. Named honestly, then mostly declined.)*

## 5. Provenance

*Can I prove where it came from and what happened to it?*

- **Signed commits** `[med] ⚖️` — Sign every commit with a GPG or SSH key so history carries verifiable authorship. Legitimately good practice; the "Verified" badge is also just satisfying. *(Enabled here: every commit in this repo is GPG-signed with an rsa4096 key, verifiable via `git log --show-signature`. This line was itself corrected the moment signing turned on — the entry cannot stay true otherwise.)*
- **Signed tags** `[low] ⚖️` — Sign release tags so a tag's authenticity is cryptographically checkable, not just its name.
- **Citation-integrity checking** `[med] ⚖️` — This entry cites real files to back its claims about the repo. [`../scripts/lint-entries.py`](../scripts/lint-entries.py) verifies, on every push, that every cited path resolves — plus that each catalog item is tagged and the coda is present. It guarantees citation *resolution and structure*, not the semantic truth of the prose: it stops the document from citing a file that isn't there, which is citation rot, not misstatement. A deliberately modest guarantee, honestly named — and still the one place this repo's over-engineering earns its keep.
- **SBOM generation** `[med] 🎭` — Emit a Software Bill of Materials cataloging every dependency of a build. There is no build and there are no dependencies, so the SBOM would certify a void. Beautiful, empty.
- **SLSA build provenance / signed attestations** `[high] 🎭` — Cryptographically signed statements about how an artifact was built, verifiable by consumers. A supply-chain-security capstone with no supply chain beneath it here.

## 6. Resilience

*What is my backup, and what happens when the primary fails?*

- **Push mirrors** `[low] ⚖️` — Automatically mirror the repo to a second forge so one provider's outage or account action can't strand you. Cheap, genuinely sensible, faintly paranoid — the good kind.
- **3-2-1 backups of the repo** `[med] 🎭` — Three copies, two media, one offsite, for a repository that is already fully distributed across every clone by design. Belt, suspenders, and a second belt.
- **A documented disaster-recovery runbook** `[med] 🎭` — Step-by-step instructions for restoring the project after catastrophe, for a project whose catastrophe-recovery procedure is `git clone`.

## 7. Optimization

*What do I tune with measurement instead of vibes?*

- **CI caching** `[low] 🎭` — Cache dependencies and build outputs to shave seconds off a pipeline. This one already runs in about a second, so the cache would optimize a rounding error.
- **Job matrices** `[low] 🎭` — Fan the linter across three operating systems and four language versions to prove a citation-checker behaves identically everywhere. Rigor as performance art.
- **Concurrency / auto-cancel of superseded runs** `[low] 🎭` — Cancel in-flight CI when a newer commit arrives, saving compute. Meaningful at a thousand PRs a day; here it saves a second that was free.
- **Path-filtered CI** `[low] ⚖️` — Skip the workflow entirely on changes that can't affect it. Real savings on a heavy suite — with one documented trap: a *required* status check that gets path-filtered away is left "pending," which can block the pull request forever. This repo's suite runs in about a second, so it runs on everything; the optimization would have cost more in edge cases than it saved in compute.

## 8. Aesthetics

*How does the presentation signal that this is taken seriously?*

- **A crafted README** `[low] ⚖️` — The front door. This repo's [`../README.md`](../README.md) opens with the thesis and no throat-clearing, because presentation is the first argument a reader hears. Genuinely worth the effort; also the most visible over-engineering there is.
- **Status badges** `[low] 🎭` — A row of shields — build passing, license, coverage, "made with love" — across the top of the README. Each is one honest signal and a small dopamine tile. A dozen of them is a merit-badge sash.
- **Social preview image** `[low] 🎭` — A custom Open Graph card so the repo unfurls handsomely when linked. Dressing the repo for a party it may never be invited to.
- **A clean commit graph** `[med] 🎭` — Curating history via rebase so the graph reads like prose. Somewhere between craftsmanship and topiary.

## 9. Meta

*How do I over-engineer the process of over-engineering?*

- **Conventional Commits** `[low] ⚖️` — A grammar for commit messages (`feat:`, `fix:`, `docs:`) that machines can parse into changelogs and version bumps. This repo asks for it in [`../CONTRIBUTING.md`](../CONTRIBUTING.md). Overkill for the volume, which is why it's here — and genuinely enabling if automation (see semantic-release) is ever switched on.
- **The entry template as enforced process** `[low] ⚖️` — Every catalog is minted from [`../_template.md`](../_template.md), whose checklist encodes the two rules so they survive contact with a deadline. Process about the process, made mandatory.
- **A shared framework document** `[low] ⚖️` — The nine axes live once in [`../axes.md`](../axes.md) and every entry reuses them, so the vocabulary can't fork. Standardizing the abstraction is itself the meta move.
- **The repo enforcing its own content rules** `[med] ⚖️` — [`../scripts/lint-entries.py`](../scripts/lint-entries.py) is a machine that checks the writing obeys the writing's own rules. A governance layer whose sole citizen is the repository that wrote it. This is the axis where the whole project's premise is most nakedly on display, and — fittingly — the axis where its over-engineering is realest.
- **Architecture Decision Records** `[low] 🎭` — A numbered, immutable log of every non-trivial decision and its rationale. Superb for a system a team will maintain for a decade; for a personal catalog it is a diary that has read too much RFC 2119.

---

## The Coda — if you actually adopted a fraction of this

Drop the bit. On a repository you genuinely care about — one other people will read, use, or depend on — the moves that earn their keep, in priority order:

1. **Branch protection + required CI + a real test/lint gate.** One rule (no direct pushes to main) plus one honest check that must pass. This single pairing shuts the door on the whole "how did *that* get in" class of incident and costs an afternoon.
2. **Signed commits and signed tags.** Cheap, permanent, and the one provenance step that matters before you have artifacts to attest. Turn it on once and forget it.
3. **A crafted README and a PR/issue template.** The highest-leverage aesthetics-and-governance combo: it shapes every future contribution and every first impression, and it's all just files.
4. **Conventional Commits, but only if you'll automate off them.** The discipline is worthless as decoration and valuable as fuel — adopt it the day you wire up changelog/version automation, not before.
5. **Push mirrors** if the repo is important and lives on a platform that could lock you out. The one resilience item that isn't redundant with Git's own distribution.

Everything above the coda is available when the ambition — or the bit — calls for it. Everything in the coda is worth doing the next time you start something you mean to keep.

## Prior art & sources

Sources mapped to the catalog claims they back, tagged by kind. The handful of items with no row (mirrors, curated history, badges, and other everyday forge conveniences) rest on documented platform features and common practice you can confirm in any forge's settings page.

- **Branch protection, rulesets, required reviews & checks** — [GitHub: about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [available ruleset rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) `[official-docs]`
- **CODEOWNERS auto-review** — [GitHub: about code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) `[official-docs]`
- **Merge queue** — [GitHub: managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) `[official-docs]`
- **Signed commits** — [GitHub: commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification), [Pro Git: Signing Your Work](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work) `[official-docs]`
- **SLSA build provenance** — [SLSA provenance spec](https://slsa.dev/spec/v1.0/provenance), [actions/attest-build-provenance](https://github.com/actions/attest-build-provenance) `[official-docs]`
- **SBOM generation** — [Syft (SPDX / CycloneDX)](https://github.com/anchore/syft) `[official-docs]`
- **Sigstore / cosign signing** — [Sigstore cosign quickstart](https://docs.sigstore.dev/quickstart/quickstart-cosign/) `[official-docs]`
- **Dependabot** — [GitHub: Dependabot security updates](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates) `[official-docs]`
- **CodeQL code scanning** — [GitHub: about code scanning with CodeQL](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql) `[official-docs]`
- **OpenSSF Scorecard** — [scorecard.dev](https://scorecard.dev/) `[official-docs]`
- **Conventional Commits & semantic-release** — [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), [semantic-release commit-analyzer](https://github.com/semantic-release/commit-analyzer) `[standard]`
- **DORA metrics (now five)** — [dora.dev metrics guide](https://dora.dev/guides/dora-metrics-four-keys/) `[official-docs]`
- **Architecture Decision Records** — [Nygard, "Documenting Architecture Decisions" (2011)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), [adr.github.io](https://adr.github.io/) `[practice]`
