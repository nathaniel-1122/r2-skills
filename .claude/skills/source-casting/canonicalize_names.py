#!/usr/bin/env python3
"""Canonicalize person-name spellings in a source-list CSV.

The same person often anchors several archetype buckets, and across rows their
name can drift ("Tom" vs "Thomas Karako", "Wilson" vs "Wilson C. Beaver").
Cockpit's importer dedupes on EXACT name, so variant spellings land as
duplicate contacts. This pass rewrites every row for one person to a single
canonical spelling (it does NOT merge rows — cross-listed people still get one
row per bucket; it just makes their `name` identical so the importer collapses
them cleanly).

Logic is kept deliberately in sync with the importer's name guard
(`_IMP_NICK` / `_impNameKey` in field-reporter-crm/index.html).

Usage:
    python3 canonicalize_names.py "Story — Source List — YYYY-MM-DD.csv"        # rewrite in place
    python3 canonicalize_names.py in.csv --out out.csv                          # write a copy
    python3 canonicalize_names.py in.csv --dry-run                              # report only, no write
"""
import csv
import sys
import argparse

# Nickname -> canonical root. Mirrors _IMP_NICK in the Cockpit importer; keep in sync.
NICK = {
    "tom": "thomas", "tommy": "thomas",
    "bill": "william", "will": "william", "willie": "william", "billy": "william",
    "bob": "robert", "bobby": "robert", "rob": "robert", "robbie": "robert",
    "dick": "richard", "rick": "richard", "rich": "richard", "richie": "richard",
    "jim": "james", "jimmy": "james", "jamie": "james",
    "joe": "joseph", "joey": "joseph",
    "mike": "michael", "mickey": "michael",
    "dave": "david",
    "dan": "daniel", "danny": "daniel",
    "chris": "christopher",
    "matt": "matthew",
    "greg": "gregory",
    "ben": "benjamin", "benji": "benjamin",
    "sam": "samuel", "sammy": "samuel",
    "alex": "alexander",
    "ed": "edward", "eddie": "edward", "ted": "edward", "teddy": "edward",
    "nate": "nathaniel", "nathan": "nathaniel",
    "nick": "nicholas",
    "steve": "steven", "stephen": "steven",
    "pat": "patrick",
    "andy": "andrew", "drew": "andrew",
    "jerry": "gerald",
    "fred": "frederick",
    "ken": "kenneth", "kenny": "kenneth",
    "larry": "lawrence",
    "ron": "ronald", "ronnie": "ronald",
    "tim": "timothy",
    "tony": "anthony",
    "jon": "jonathan", "jonny": "jonathan",
    "doug": "douglas",
    "charlie": "charles", "chuck": "charles",
    "frank": "francis",
    "hank": "henry",
}
SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v", "phd", "md", "esq"}
ORG_STOP = {"the", "inc", "llc", "ltd", "corp", "company", "co", "foundation",
            "institute", "institution", "center", "centre", "for", "of", "and", "a"}


def _canon_token(t):
    t = "".join(ch for ch in t.lower() if ch.isalpha())
    return NICK.get(t, t)


def name_key(name):
    """nickname-canonical first name + surname, ignoring middle names/initials/suffixes."""
    toks = []
    for raw in str(name or "").lower().replace(".", " ").replace(",", " ").split():
        t = "".join(ch for ch in raw if ch.isalpha())
        if t and t not in SUFFIXES:
            toks.append(t)
    if not toks:
        return ""
    if len(toks) == 1:
        return _canon_token(toks[0])
    return _canon_token(toks[0]) + "|" + toks[-1]


def org_key(org):
    cleaned = []
    skip = False
    out = []
    s = str(org or "").lower()
    # drop parenthetical acronyms like "(CSIS)"
    depth = 0
    buf = []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            buf.append(ch if (ch.isalnum() or ch == " ") else " ")
    toks = [t for t in "".join(buf).split() if t and t not in ORG_STOP]
    return " ".join(toks)


def _canonical_spelling(names):
    """Pick the fullest spelling: most name tokens, then longest string, then alphabetical."""
    return sorted(names, key=lambda n: (-len(n.split()), -len(n), n))[0]


def canonicalize(rows):
    """Rewrite each person's `name` to one canonical spelling across all their rows.

    Returns (changes, warnings):
      changes  -> list of (from_name, to_name, org)         names that were rewritten
      warnings -> list of (name_key, [(name, org), ...])    same person-key across DIFFERENT orgs
    """
    groups = {}   # (name_key, org_key) -> set of raw names
    bykey = {}    # name_key -> set of org_keys (to detect cross-org same-name)
    for r in rows:
        nk = name_key(r.get("name", ""))
        if not nk:
            continue
        ok = org_key(r.get("organization", ""))
        groups.setdefault((nk, ok), set()).add(r.get("name", "").strip())
        bykey.setdefault(nk, {}).setdefault(ok, set()).add(r.get("name", "").strip())

    canon = {}
    for (nk, ok), names in groups.items():
        canon[(nk, ok)] = _canonical_spelling([n for n in names if n])

    changes = []
    for r in rows:
        nk = name_key(r.get("name", ""))
        if not nk:
            continue
        ok = org_key(r.get("organization", ""))
        target = canon.get((nk, ok))
        cur = (r.get("name", "") or "").strip()
        if target and cur != target:
            changes.append((cur, target, r.get("organization", "")))
            r["name"] = target

    warnings = []
    for nk, orgs in bykey.items():
        if len(orgs) > 1:
            flat = []
            for ok, names in orgs.items():
                for n in names:
                    flat.append((n, ok))
            warnings.append((nk, flat))
    return changes, warnings


def main():
    ap = argparse.ArgumentParser(description="Canonicalize person-name spellings in a source-list CSV.")
    ap.add_argument("csv_path")
    ap.add_argument("--out", default=None, help="write to this path instead of in place")
    ap.add_argument("--dry-run", action="store_true", help="report only; do not write")
    args = ap.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    changes, warnings = canonicalize(rows)

    # de-dup the change report (a name may be rewritten many times)
    seen = set()
    uniq = []
    for frm, to, org in changes:
        k = (frm, to)
        if k not in seen:
            seen.add(k)
            uniq.append((frm, to, org))

    print(f"Canonicalizer: {len(rows)} rows, {len(uniq)} name spelling(s) unified.")
    for frm, to, org in uniq:
        print(f"  '{frm}'  ->  '{to}'   ({org})")
    if warnings:
        print(f"\n{len(warnings)} same-person key(s) appear under DIFFERENT orgs "
              f"— left separate; confirm same person vs. different people:")
        for nk, flat in warnings:
            shown = "; ".join(f"'{n}' @ {ok or '(no org)'}" for n, ok in flat)
            print(f"  [{nk}] {shown}")

    if args.dry_run:
        print("\n(dry run — nothing written)")
        return

    out_path = args.out or args.csv_path
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
