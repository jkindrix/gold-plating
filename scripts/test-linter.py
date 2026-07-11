#!/usr/bin/env python3
"""Adversarial tests for the entry linter.

Each broken fixture in tests/fixtures/ carries a specific defect, and the test
asserts the linter reports the *expected diagnostic code* — not merely that it
fails. A fixture that fails for the wrong reason is a test bug, and this suite
catches it. Fixtures named after false negatives found in external review are
regression tests: the linter once passed them.

Run: python3 scripts/test-linter.py   (requires Python 3.9+)
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "tests", "fixtures")

# The linter module has a hyphen in its name, so load it by path.
_spec = importlib.util.spec_from_file_location("linter", os.path.join(HERE, "lint-entries.py"))
assert _spec and _spec.loader, "could not load lint-entries.py"
linter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(linter)

# (fixture, expected diagnostic codes). Empty tuple = must pass clean.
CASES = [
    ("valid.md", ()),
    ("no-frontmatter.md", ("frontmatter",)),
    ("unclosed-frontmatter.md", ("frontmatter",)),          # regression: review probe E
    ("missing-frontmatter-field.md", ("frontmatter-field",)),
    ("bad-date.md", ("frontmatter-field",)),
    ("checklist-left-in.md", ("checklist",)),
    ("unknown-axis.md", ("axis-unknown",)),
    ("wrong-axis-number.md", ("axis-number",)),
    ("duplicate-axis.md", ("axis-duplicate",)),
    ("axes-out-of-order.md", ("axis-order",)),
    ("no-axes.md", ("axes-missing",)),
    ("empty-axis.md", ("axis-empty",)),                     # regression: review probe D
    ("untagged-item.md", ("item-untagged",)),
    ("non-bold-item.md", ("item-format",)),
    ("missing-coda.md", ("coda-missing",)),
    ("coda-not-last.md", ("coda-not-last",)),
    ("missing-sources.md", ("sources-missing",)),
    ("sources-before-coda.md", ("sources-misplaced",)),     # regression: review probe A
    ("appendix-after-sources.md", ("sources-misplaced",)),  # regression: review probe B
    ("broken-citation.md", ("citation-missing",)),
    ("escaping-citation.md", ("citation-escape",)),         # regression: review probe C
    ("multi-defect.md", ("item-untagged", "sources-missing")),
]


def main() -> int:
    wrong = 0
    for name, expected in CASES:
        errs = linter.lint_entry(os.path.join(FIXTURES, name))
        codes = {code for code, _ in errs}
        if not expected:
            ok = not errs
            detail = f"unexpected: {sorted(codes)}" if errs else "clean"
        else:
            ok = all(e in codes for e in expected)
            detail = f"got {sorted(codes)}, wanted {list(expected)}"
        if ok:
            print(f"ok    {name} ({detail if not expected else '+'.join(expected)})")
        else:
            wrong += 1
            print(f"WRONG {name}: {detail}")
    if wrong:
        print(f"\n{wrong} test(s) wrong")
        return 1
    print(f"\nall {len(CASES)} linter tests pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
