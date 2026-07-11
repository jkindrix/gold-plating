#!/usr/bin/env python3
"""Gold-Plating entry linter.

Enforces the structural contract that keeps the catalog honest and consistent:

  1. The entry opens with a YAML frontmatter block.
  2. The template's ENTRY CHECKLIST comment is removed (the entry was filled in).
  3. Axis headings are well-formed: each is one of the nine known axes, carries
     its canonical number (Governance=1 ... Meta=9), is not duplicated, and the
     axes present appear in canonical order. At least one axis is required.
  4. Every catalog item in an axis section is bold-led (- **Name** ...) and
     carries an Effort tag and a Bit-factor tag.
  5. The Coda is present and is the last section, except that a single
     "Prior art & sources" section may follow it.
  6. A "Prior art & sources" section is present (the Prime Rule, made structural).
  7. Every local file citation resolves to a real path.

The citation check (6) is what stops the self-referential flagship from citing a
file that isn't there. It guarantees citation *resolution* and structure — not
the semantic truth of the prose. That is a deliberately modest promise: it
prevents citation rot, not misstatement, and the project says so rather than
overselling the word.

Numbers reflect an axis's fixed identity, not its sequence: omitting an axis
skips its number, it does not renumber the rest.

No third-party dependencies — deliberately, so there is nothing to pin or lock.
Exit status is non-zero if any entry violates the contract. The adversarial
fixture suite in scripts/test-linter.py checks that each rule actually fires.
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
AXIS_INDEX = {name: i for i, name in enumerate(AXES)}

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
NUM_HEADING_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
CODA_RE = re.compile(r"(?i)^#{1,3}\s+.*\bcoda\b")
SOURCES_RE = re.compile(r"(?i)^##\s+(prior art|sources|references)\b")


def lint_entry(path: str) -> list[str]:
    errs: list[str] = []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()

    # 1. frontmatter present
    if not lines or lines[0].strip() != "---" or "---" not in [l.strip() for l in lines[1:]]:
        errs.append("missing YAML frontmatter (file must open with a --- ... --- block)")

    # 2. template checklist removed
    if "ENTRY CHECKLIST" in text:
        errs.append("template ENTRY CHECKLIST comment is still present — satisfy and delete it")

    # 3. axis headings: known, canonically numbered, unique, ordered, >= 1
    seen: list[str] = []
    axis_positions: list[tuple[int, int, str]] = []  # (line_no, canonical_index, name)
    for i, ln in enumerate(lines):
        m = NUM_HEADING_RE.match(ln)
        if not m:
            continue
        num, name = int(m.group(1)), m.group(2).strip()
        if name not in AXIS_INDEX:
            errs.append(f"unknown axis heading '## {num}. {name}' (must be one of the nine axes)")
            continue
        canonical = AXIS_INDEX[name] + 1
        if num != canonical:
            errs.append(f"axis '{name}' is numbered {num} but its canonical number is {canonical}")
        if name in seen:
            errs.append(f"duplicate axis heading: {name}")
        seen.append(name)
        axis_positions.append((i, AXIS_INDEX[name], name))
    if not seen:
        errs.append("no axis sections found (an entry needs at least one axis)")
    canonical_order = [idx for _, idx, _ in axis_positions]
    if canonical_order != sorted(canonical_order):
        errs.append("axis sections out of canonical order: "
                    + " -> ".join(n for _, _, n in axis_positions))

    # 4/5. coda present, and last except for an optional trailing Sources section
    coda_line = next((i for i, ln in enumerate(lines) if CODA_RE.match(ln)), None)
    if coda_line is None:
        errs.append("no Coda section found (the Coda Invariant is mandatory)")
    else:
        for ln in lines[coda_line + 1:]:
            if re.match(r"^#{1,2}\s+\S", ln):
                if not SOURCES_RE.match(ln):
                    errs.append("the Coda must be the last section "
                                "(only a Prior-art/Sources section may follow it)")
                break

    # 6. a Prior-art/Sources section is present (the Prime Rule, made structural)
    if not any(SOURCES_RE.match(ln) for ln in lines):
        errs.append("missing a 'Prior art & sources' section")

    # 4. catalog items in axis sections are bold-led and tagged
    if axis_positions:
        start = axis_positions[0][0]
        end = coda_line if coda_line is not None else len(lines)
        for ln in lines[start:end]:
            if not ln.startswith("- "):
                continue
            if not ln.startswith("- **"):
                errs.append(f"catalog item must be bold-led (- **Name** ...): {ln.strip()[:70]}")
                continue
            has_effort = re.search(r"\[(low|med|high)\]", ln)
            has_bit = ("⚖️" in ln) or ("🎭" in ln)
            if not (has_effort and has_bit):
                want = []
                if not has_effort:
                    want.append("Effort [low|med|high]")
                if not has_bit:
                    want.append("Bit-factor ⚖️|🎭")
                errs.append("catalog item missing " + " and ".join(want) + f": {ln.strip()[:70]}")

    # 6. local citations resolve
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
