#!/usr/bin/env python3
"""Guardrail: verify every skill folder's name matches its SKILL.md `name:` frontmatter.

This catches the copy-paste mistake where a SKILL.md is duplicated from another
skill and the body/frontmatter is never updated (e.g. a folder named
`source-casting` whose SKILL.md still says `name: frontend-design`).

Usage:  python3 check-skill-names.py
Exit:   0 = all good, 1 = at least one mismatch (and prints the offenders).
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKILLS_GLOB = os.path.join(ROOT, ".claude", "skills", "*", "SKILL.md")


def frontmatter_name(path):
    """Return the `name:` value from the YAML frontmatter, or None."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    for line in m.group(1).splitlines():
        nm = re.match(r"\s*name:\s*(.+?)\s*$", line)
        if nm:
            return nm.group(1).strip().strip('"').strip("'")
    return None


def main():
    paths = sorted(glob.glob(SKILLS_GLOB))
    if not paths:
        print("No skills found under .claude/skills/*/SKILL.md")
        return 0

    problems = []
    for path in paths:
        folder = os.path.basename(os.path.dirname(path))
        name = frontmatter_name(path)
        if name is None:
            problems.append((folder, "<no name in frontmatter>"))
        elif name != folder:
            problems.append((folder, name))

    if problems:
        print("MISMATCH — skill folder name != SKILL.md `name:`")
        for folder, name in problems:
            print("  folder '{}'  ->  name '{}'".format(folder, name))
        print("\nFix the frontmatter (or the folder name) so they match.")
        return 1

    print("OK — all {} skill(s) have matching folder and frontmatter names.".format(len(paths)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
