# The Universal Axes of Over-Engineering

A wide range of subjects can be gold-plated along some subset of the same nine recurring axes — and naming the axes that *don't* apply is part of an entry's honesty. This document defines them once; every entry in the series organizes its catalog under these headings and links here rather than re-explaining them. Two subjects as different as a Git repository and a cup of coffee turn out to over-engineer along identical dimensions — which is the quiet thesis of the whole project: over-engineering is domain mastery made visible by applying a general maximalist toolkit to a specific object.

An entry need not populate all nine. A subject with no meaningful provenance story simply omits that axis. But the axis order is fixed, so a reader who knows the skeleton can navigate any entry.

---

## 1. Governance

**The maximalist question: who is allowed to change it, and under what conditions may a change land?**

The rules layer. Gates, approvals, allowlists, required checks, protected states. On a repo this is branch protection and code owners; on a home network it's who gets the admin password and what changes require a change-window; on a recipe it's "no one alters the house dial-in without a documented cupping." Governance is the axis that most obviously signals seriousness disproportionate to stakes, which makes it the funniest and often the first one people reach for.

## 2. Reproducibility

**The maximalist question: can I reproduce the exact result deterministically, from nothing, every time?**

Pinning, environments, lockfiles, versioned inputs, documented tolerances. The pursuit of "it works on my machine" becoming "it works on any machine, forever." A recipe specified to the gram, second, and degree. A dev environment rebuilt bit-identical from a declarative spec. The enemy is drift; the tool is determinism.

## 3. Automation

**The maximalist question: what manual step can I remove?**

Every human touch is a defect to be eliminated. CI pipelines, scheduled jobs, bots, controllers, and machines that do the thing so a person never has to. The temperature-controlled kettle that removes the human from the water; the workflow that labels, assigns, and merges without a keystroke. Taken to its limit, automation aspires to a system that runs the whole subject unattended.

## 4. Observability

**The maximalist question: what am I currently eyeballing that I could instead measure?**

Instrumentation, metrics, logs, traces, dashboards, and the replacement of intuition with data. The refractometer instead of taste; the scale and shot timer instead of "looks about right"; the SLO dashboard for an app with three users. Observability is where over-engineering becomes quantified, and quantification is where a hobby becomes a discipline.

## 5. Provenance

**The maximalist question: can I prove where it came from and exactly what happened to it?**

Auditability, signatures, attestations, chain-of-custody, immutable logs. The cryptographically signed commit; the software bill of materials; the bean's origin, roast date, and rest time logged before it ever touches the grinder. Provenance answers "trust me" with "verify me," which is almost always more than the situation requires and precisely the point.

## 6. Resilience

**The maximalist question: what is my backup, and what happens when the primary fails?**

Redundancy, failover, backups, disaster recovery, graceful degradation. The second grinder in the cupboard; the 3-2-1 backup rule for a photo library; the documented runbook for when the home server dies at 2 a.m. Resilience treats every single point of failure as an affront, whether or not failure would matter.

## 7. Optimization

**The maximalist question: what do I tune with measurement instead of vibes?**

Performance work, parameter sweeps, controlled experiments, and squeezing the last few percent of quality or speed out of a system that was fine. Pressure profiling a shot; A/B testing a build cache; periodizing a training block. Optimization is the axis that consumes infinite time by design — there is always another percent — which is why the coda exists to call it off.

## 8. Aesthetics

**The maximalist question: how does the presentation signal that this is taken seriously?**

Polish, branding, layout, ceremony, and the visible craft that communicates intent before any content is examined. Latte art and a laid-out station; a repo's badges, social preview, and immaculate README; a dashboard that is beautiful before it is useful. Aesthetics is over-engineering's outward face — often the first thing seen and the last thing needed.

## 9. Meta

**The maximalist question: how do I over-engineer the process of over-engineering?**

Process about the process. The logbook of every attempt; the conventional-commit standard and its enforcement; the metrics program that measures the improvement program. Meta is the recursive axis, and the most self-aware entries turn it on themselves — the repo that gold-plates its own governance, the training log that tracks the discipline of keeping the training log. It is where the series is most honest about what it is.

---

## Two tags every catalog item carries

Alongside these axes, individual items are tagged on two dimensions so a reader can navigate by appetite:

- **Effort** — `[low]` (a file, a setting, a few minutes), `[med]` (a tool or workflow to wire in), `[high]` (real integration work).
- **Bit-factor** — `⚖️` (genuinely worth it even at small scale), `🎭` (pure theater at this scale; adopt it for the bit, not the benefit). Most items live somewhere on the spectrum between; the tag marks which pole they lean toward.

The two tags are orthogonal: a `[low] 🎭` item is cheap theater (add it for fun), while a `[high] ⚖️` item is expensive but real (adopt it if you mean it).
