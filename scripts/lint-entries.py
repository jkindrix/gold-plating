#!/usr/bin/env python3
"""Gold-Plating entry linter.

Enforces the invariants that keep the catalog honest:

  1. The template's ENTRY CHECKLIST comment is removed (the entry was filled in).
  2. The entry ends with a Coda (the Coda Invariant).
  3. Axis headings appear in the canonical order (a subsequence of the nine).
  4. Every catalog item carries an Effort tag and a Bit-factor tag.
  5. Every local file citation resolves to a real path.

The citation check (5) is what stops the self-referential flagship from citing a
file that isn't there. It guarantees citation *resolution* and structure — not
the semantic truth of the prose. That is a deliberately modest promise: it
prevents citation rot, not misstatement, and the project says so rather than
overselling the word.

No third-party dependencies — deliberately, so there is nothing to pin or lock.
Exit status is non-zero if any entry violates an invariant.
"""
from __future__ import annotations

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(REPO, "entries")

AXES = [
    "Governance", "Reproducibility", "Automation", "Observability",
    "Provenance", "Resilience", "Optimization", "Aesthetics", "Meta",
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def lint_entry(path: str) -> list[str]:
    errs: list[str] = []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    # 1. template checklist removed
    if "ENTRY CHECKLIST" in text:
        errs.append("template ENTRY CHECKLIST comment is still present — satisfy and delete it")

    # 2. coda present
    if not re.search(r"(?mi)^#{1,3}\s+.*\bcoda\b", text):
        errs.append("no Coda section found (the Coda Invariant is mandatory)")

    # 3. axes present must appear in canonical order
    found = []
    for idx, axis in enumerate(AXES):
        m = re.search(rf"(?mi)^##\s*\d+\.\s*{re.escape(axis)}\b", text)
        if m:
            found.append((m.start(), idx, axis))
    by_position = sorted(found, key=lambda t: t[0])
    canonical_indices = [t[1] for t in by_position]
    if canonical_indices != sorted(canonical_indices):
        errs.append("axis headings are out of canonical order: "
                    + " -> ".join(t[2] for t in by_position))

    # 4. every catalog item in an axis section carries Effort + Bit-factor tags
    lines = text.splitlines()
    axis_heading = re.compile(r"(?i)^##\s*\d+\.\s*(" + "|".join(AXES) + r")\b")
    coda_heading = re.compile(r"(?i)^#{1,3}\s+.*\bcoda\b")
    axis_start = coda_start = None
    for i, ln in enumerate(lines):
        if axis_start is None and axis_heading.match(ln):
            axis_start = i
        if coda_heading.match(ln):
            coda_start = i
            break
    if axis_start is not None:
        end = coda_start if coda_start is not None else len(lines)
        for ln in lines[axis_start:end]:
            if ln.startswith("- **"):
                has_effort = re.search(r"\[(low|med|high)\]", ln)
                has_bit = ("⚖️" in ln) or ("🎭" in ln)
                if not (has_effort and has_bit):
                    want = []
                    if not has_effort:
                        want.append("Effort [low|med|high]")
                    if not has_bit:
                        want.append("Bit-factor ⚖️|🎭")
                    errs.append("catalog item missing " + " and ".join(want)
                                + f": {ln.strip()[:70]}")

    # 5. local citations resolve
    base = os.path.dirname(path)
    for target in LINK_RE.findall(text):
        cleaned = target.split("#", 1)[0].strip()
        if not cleaned or cleaned.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = os.path.normpath(os.path.join(base, cleaned))
        if not os.path.exists(resolved):
            errs.append(f"citation points at a missing path: {target}")

    return errs


def main() -> int:
    if not os.path.isdir(ENTRIES):
        print("no entries/ directory — nothing to lint")
        return 0

    files = sorted(f for f in os.listdir(ENTRIES) if f.endswith(".md"))
    problems = 0
    for name in files:
        errs = lint_entry(os.path.join(ENTRIES, name))
        if errs:
            problems += len(errs)
            print(f"FAIL entries/{name}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"ok   entries/{name}")

    if problems:
        print(f"\n{problems} problem(s) found")
        return 1
    label = "entry" if len(files) == 1 else "entries"
    print(f"\nall {len(files)} {label} pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
