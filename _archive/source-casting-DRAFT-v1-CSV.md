# ARCHIVE — source-casting DRAFT v1 (first CSV rewrite)

> Reference only. This is the FIRST CSV draft Claude presented and the user reviewed,
> BEFORE the decision to split `links` out of `notes`. Kept for comparison against the
> final version. The ACTIVE skill is `.claude/skills/source-casting/SKILL.md`.
>
> Difference vs. the active baseline (v2): v1 has **17 columns** and consolidates
> Outreach Notes + Relevant Links + Other Social Profiles into a single `notes` cell
> (labeled OUTREACH/LINKS/SOCIAL). v2 splits URLs into a dedicated **`links`** column
> (18 columns total) so `notes` stays prose-only.

---

```markdown
---
name: source-casting
description: "Use this skill when casting interview sources for a news story. Runs in two phases with checkpoints: first identifies source archetypes and waits for approval, then researches real people using Nimble, proposes a Nathaniel/Johnny assignment split for approval, and compiles a ranked CSV that imports directly into the Cockpit (Field Reporter CRM) Import Sources feature."
allowed-tools:
  - Bash(nimble:*)
  - Bash(python3:*)
  - Bash(pip:*)
  - Bash(mkdir:*)
  - Bash(cat:*)
  - Bash(ls:*)
  - Write
  - Read
  - Edit
---

# Skill: Story Source Casting
## R Squared Media — Newsroom Source Research

[... full Phase 1 / Phase 2 body identical to active SKILL.md ...]

### Output Columns (CSV header — exact names, exact order)  [v1 = 17 cols]

priority,suggested_bucket,name,role_title,organization,email,phone,linkedin,source_url,confidence,why_relevant,is_press,story,location,political_leaning,assigned_to,notes

| 17 | notes | Consolidated research in one cell:
  `OUTREACH: <sensitivities, positions, channel, verify-flags> | LINKS: <op-eds, testimony, published work — URLs> | SOCIAL: <X / Instagram / Substack — URLs>`. Omit empty sections. |
```

> The full v1 prose (Confidence Rubric, Assignment Logic, Assignment Checkpoint,
> Priority Rules A/B/C, Contact Info Approach, Output Format, Accuracy Rules) is
> identical to the active SKILL.md EXCEPT for the single-`notes` column above.
> If you need the byte-exact v1, it is in the chat transcript where it was first presented.
