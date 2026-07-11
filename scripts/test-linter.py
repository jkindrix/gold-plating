#!/usr/bin/env python3
"""Adversarial tests for the entry linter.

Each fixture in tests/fixtures/ is either valid or carries exactly one defect.
We assert lint_entry() passes the valid one and fails each broken one, so the
linter's green result on real entries means something. Dependency-free.

Run: python3 scripts/test-linter.py
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

# (fixture filename, should_pass)
CASES = [
    ("valid.md", True),
    ("no-frontmatter.md", False),
    ("checklist-left-in.md", False),
    ("unknown-axis.md", False),
    ("wrong-axis-number.md", False),
    ("duplicate-axis.md", False),
    ("axes-out-of-order.md", False),
    ("no-axes.md", False),
    ("untagged-item.md", False),
    ("non-bold-item.md", False),
    ("missing-coda.md", False),
    ("coda-not-last.md", False),
    ("missing-sources.md", False),
]


def main() -> int:
    wrong = 0
    for name, should_pass in CASES:
        errs = linter.lint_entry(os.path.join(FIXTURES, name))
        passed = not errs
        if passed != should_pass:
            wrong += 1
            want = "pass" if should_pass else "fail"
            print(f"WRONG {name}: expected {want}, got {errs or 'pass'}")
        else:
            print(f"ok    {name} ({'passes' if passed else 'fails'} as intended)")
    if wrong:
        print(f"\n{wrong} test(s) wrong")
        return 1
    print(f"\nall {len(CASES)} linter tests pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
