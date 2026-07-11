#!/usr/bin/env python3
"""Gold-Plating entry linter.

Enforces the structural contract that keeps the catalog honest and consistent.
Each rule reports a stable diagnostic code (tested one-for-one by the
adversarial suite in scripts/test-linter.py):

  frontmatter        entry opens with a contiguous, closed YAML block
  frontmatter-field  frontmatter carries date (ISO yyyy-mm-dd), author, context
  checklist          the template's ENTRY CHECKLIST comment was removed
  axis-unknown       every numbered ## heading is one of the nine axes
  axis-number        each axis keeps its canonical number (Governance=1 … Meta=9)
  axis-duplicate     no axis appears twice
  axis-order         axes present appear in canonical order
  axes-missing       at least one axis section exists
  axis-empty         every axis section contains at least one catalog item
  item-format        catalog items are bold-led (- **Name** …)
  item-untagged      each item carries an Effort tag and a Bit-factor tag
  coda-missing       the Coda exists (the Coda Invariant)
  coda-not-last      nothing follows the Coda except one Sources section
  sources-missing    a "Prior art & sources" section exists (the Prime Rule,
                     made structural)
  sources-misplaced  the Sources section comes after the Coda, and nothing
                     follows it
  citation-missing   every local file citation resolves to a real path
  citation-escape    local citations stay inside the repository

The citation checks guarantee *resolution and containment*, not the semantic
truth of the prose — a deliberately modest promise: they prevent citation rot,
not misstatement, and the project says so rather than overselling the word.

Axis numbers reflect a fixed identity, not a sequence: omitting an axis skips
its number, it does not renumber the rest.

Local links must use plain relative paths (optionally with a #fragment). That
is the supported subset — reference-style links and exotic destinations are
not parsed. External http(s) links are not fetched here; scripts/check-links.py
covers those on a schedule, off the required path.

No third-party dependencies — deliberately, so there is nothing to pin or lock.
Exit status is non-zero if any entry violates the contract. Requires Python 3.9+.
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
HEADING_RE = re.compile(r"^#{1,2}\s+\S")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_FIELDS = ("date", "author", "context")


def check_frontmatter(lines: list[str]) -> tuple[list[tuple[str, str]], int]:
    """Validate the frontmatter block; return (diagnostics, body_start_line)."""
    errs: list[tuple[str, str]] = []
    if not lines or lines[0].strip() != "---":
        errs.append(("frontmatter", "file must open with a --- frontmatter block"))
        return errs, 0
    close = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close = i
            break
        if HEADING_RE.match(lines[i]):  # body content before the block closed
            break
    if close is None:
        errs.append(("frontmatter", "frontmatter block is never closed with ---"))
        return errs, 0
    fields = {}
    for ln in lines[1:close]:
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", ln)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    for f in REQUIRED_FIELDS:
        if not fields.get(f):
            errs.append(("frontmatter-field", f"frontmatter is missing required field '{f}'"))
    if fields.get("date") and not DATE_RE.match(fields["date"]):
        errs.append(("frontmatter-field", f"date '{fields['date']}' is not ISO yyyy-mm-dd"))
    return errs, close + 1


def lint_entry(path: str) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()

    fm_errs, body_start = check_frontmatter(lines)
    errs.extend(fm_errs)

    if "ENTRY CHECKLIST" in text:
        errs.append(("checklist", "template ENTRY CHECKLIST comment is still present"))

    # --- axis headings: known, canonically numbered, unique, ordered, >= 1
    seen: list[str] = []
    axis_positions: list[tuple[int, int, str]] = []  # (line_no, canonical_idx, name)
    for i in range(body_start, len(lines)):
        m = NUM_HEADING_RE.match(lines[i])
        if not m:
            continue
        num, name = int(m.group(1)), m.group(2).strip()
        if name not in AXIS_INDEX:
            errs.append(("axis-unknown", f"'## {num}. {name}' is not one of the nine axes"))
            continue
        canonical = AXIS_INDEX[name] + 1
        if num != canonical:
            errs.append(("axis-number",
                         f"axis '{name}' is numbered {num}; canonical is {canonical}"))
        if name in seen:
            errs.append(("axis-duplicate", f"duplicate axis heading: {name}"))
        seen.append(name)
        axis_positions.append((i, AXIS_INDEX[name], name))
    if not seen:
        errs.append(("axes-missing", "no axis sections found (need at least one)"))
    canonical_order = [idx for _, idx, _ in axis_positions]
    if canonical_order != sorted(canonical_order):
        errs.append(("axis-order", "axis sections out of canonical order: "
                     + " -> ".join(n for _, _, n in axis_positions)))

    # --- coda: present; after it, only one Sources section, and nothing after that
    coda_line = next((i for i in range(body_start, len(lines)) if CODA_RE.match(lines[i])), None)
    sources_lines = [i for i in range(body_start, len(lines)) if SOURCES_RE.match(lines[i])]
    if coda_line is None:
        errs.append(("coda-missing", "no Coda section found (the Coda Invariant is mandatory)"))
    else:
        sources_after = None
        for i in range(coda_line + 1, len(lines)):
            if not HEADING_RE.match(lines[i]):
                continue
            if SOURCES_RE.match(lines[i]) and sources_after is None:
                sources_after = i
            else:
                code = "sources-misplaced" if sources_after is not None else "coda-not-last"
                errs.append((code, f"unexpected section after the "
                             f"{'Sources' if sources_after is not None else 'Coda'}: "
                             f"{lines[i].strip()[:60]}"))
                break

    # --- sources: present, and after the coda
    if not sources_lines:
        errs.append(("sources-missing", "missing a 'Prior art & sources' section"))
    elif coda_line is not None and all(i < coda_line for i in sources_lines):
        errs.append(("sources-misplaced", "'Prior art & sources' must follow the Coda"))

    # --- catalog items: bold-led, tagged, and every axis section non-empty
    boundaries = [i for i, _, _ in axis_positions]
    stop_lines = [i for i in (coda_line, (sources_lines[0] if sources_lines else None))
                  if i is not None]
    hard_stop = min(stop_lines) if stop_lines else len(lines)
    for n, start in enumerate(boundaries):
        end = min(boundaries[n + 1] if n + 1 < len(boundaries) else len(lines), hard_stop)
        items = 0
        for ln in lines[start:end]:
            if not ln.startswith("- "):
                continue
            items += 1
            if not ln.startswith("- **"):
                errs.append(("item-format",
                             f"catalog item must be bold-led (- **Name** …): {ln.strip()[:60]}"))
                continue
            has_effort = re.search(r"\[(low|med|high)\]", ln)
            has_bit = ("⚖️" in ln) or ("🎭" in ln)
            if not (has_effort and has_bit):
                want = [w for w, ok in (("Effort [low|med|high]", has_effort),
                                        ("Bit-factor ⚖️|🎭", has_bit)) if not ok]
                errs.append(("item-untagged",
                             "catalog item missing " + " and ".join(want)
                             + f": {ln.strip()[:60]}"))
        if items == 0:
            errs.append(("axis-empty",
                         f"axis '{axis_positions[n][2]}' has no catalog items"))

    # --- local citations: resolve, and stay inside the repository
    base = os.path.dirname(os.path.abspath(path))
    repo_root = os.path.realpath(REPO)
    for target in LINK_RE.findall(text):
        cleaned = target.split("#", 1)[0].strip()
        if not cleaned or cleaned.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = os.path.realpath(os.path.join(base, cleaned))
        if not resolved.startswith(repo_root + os.sep):
            errs.append(("citation-escape",
                         f"citation leaves the repository: {target}"))
        elif not os.path.exists(resolved):
            errs.append(("citation-missing", f"citation points at a missing path: {target}"))

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
            for code, msg in errs:
                print(f"  - [{code}] {msg}")
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
