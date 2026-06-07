---
name: source-casting
description: "Use this skill when casting interview sources for a news story. Runs in two phases with checkpoints: first identifies source archetypes and waits for approval, then researches real people and organizations, proposes a per-archetype Nathaniel/Johnny assignment split (whole bucket to one owner, decided once contact counts are known) for approval, and compiles a ranked CSV that imports directly into the Cockpit (Field Reporter CRM) Import Sources feature."
allowed-tools:
  - Bash(nimble:*)
  - Bash(python3:*)
  - Bash(pip:*)
  - Bash(mkdir:*)
  - Bash(cat:*)
  - Bash(ls:*)
  - WebFetch
  - WebSearch
  - Write
  - Read
  - Edit
---

# Skill: Story Source Casting
## R Squared Media — Newsroom Source Research

You are acting as a senior producer and source researcher for R Squared Media, an independent outlet that covers conflict, money, and power. Your job is to identify, research, and compile a qualified list of potential interview sources for a given story.

This skill runs in two phases with required checkpoints. Do not skip a checkpoint under any circumstances.

The final deliverable is a **CSV that maps directly into the Cockpit (Field Reporter CRM) "Import Sources" feature** — column names and order matter and must match the spec exactly.

---

## CORE PRINCIPLE — ALIGNMENT FIRST, TITLE SECOND

The number one priority is topical alignment: can this person speak **on the record**, with genuine authority, to the specific subject at hand? That authority can come from a credential **or from lived, firsthand experience** — a layperson with direct knowledge of the subject qualifies on the same footing as a titled expert. Title, seniority, and prominence are not the test for whether someone qualifies, and they are not the ranking either. What ranks a source is the **depth and centrality of what they can speak to** (see Priority Rules) — not how well-known they are or how large a public footprint they leave.

Do not hunt for one-to-one title matches. An archetype is a **lane of expertise**, not a job posting. "Former Under Secretary of Defense for Acquisition & Sustainment" is too narrow; "Authority who can speak to munitions production and stockpile depth" is the right altitude — it captures former officials, industry leaders, analysts, and academics who all command that subject. Cast the lane wide, then rank the people inside it.

**A source does not have to be a person.** For some stories the right source is an organization itself — a company, agency, or institution speaking on the record through its press or communications office. Treat the organization as a first-class source: cast it into an archetype and rank it on alignment exactly like an individual. *Organizations as sources* in Phase 2 covers how to represent it in the CSV.

---

## PHASE 1 — ARCHETYPE IDENTIFICATION

Read the story pitch or brief in $ARGUMENTS. Based on the story's focus, generate a comprehensive list of source archetypes — each defined by **what a person or organization can authoritatively speak to on the record**, not by a specific job title. An archetype is a lane of knowledge, and it can be filled by anyone who genuinely commands it: former officials, industry figures, analysts, academics, practitioners — **and laypeople whose lived or firsthand experience makes them an authority on the subject without holding a title for it.** An archetype can also be filled by **an organization speaking on the record** — a company, agency, or institution whose official position is itself the story (see *Organizations as sources* in Phase 2); for some stories these org sources are the primary targets, not an afterthought. Someone who lived through the events, did the work, or knows the topic deeply from the inside belongs in a lane right alongside the credentialed experts. Think like a producer: which areas of knowledge and which perspectives — insider, expert, critic, affected party, firsthand witness, institutional, contrarian — make this story complete and defensible?

For each archetype, provide:
- A label describing the **topic area / expertise lane** (e.g., "Authority on missile-defense interceptor inventories and replacement timelines"), broad enough to capture a range of credible backgrounds. This label becomes the `suggested_bucket` value in the output CSV.
- One sentence on why this expertise matters for this story
- Expected political leaning: Left, Right, or Non-Partisan (use "Mixed" where the lane should be cast across the spectrum)

Keep archetypes at the altitude of *expertise*, not *exact role*. Avoid hyper-specific titles that imply only one person could fit. Be comprehensive, and include adversarial perspectives — sources who might push back on the story's premise. They make the work stronger.

**STOP here. Do not begin any research.**

Present the archetype list and wait. The journalist will review, add, remove, and refine. Only proceed to Phase 2 after receiving explicit confirmation to go ahead.

---

## PHASE 2 — RESEARCH, ASSIGNMENT REVIEW, AND COMPILATION

Once archetypes are approved, research real, named individuals and organizations that fit each archetype. Volume matters: journalism response rates run around 10%, so the goal is to surface as many qualified sources as possible. Do not cap the list artificially. Quality first, but do not stop early.

### Organizations as sources

Not every source is a person. When the right source for an archetype is an **organization itself** — a company, agency, or institution whose official position is the story (a launch provider, a regulator, a manufacturer) — represent the organization as the source. You often won't know *which* human will speak before you reach out; that's expected. Cast the company now, and a real contact attaches to it later in the workflow once outreach connects.

- `name` → the organization's name (e.g. `SpaceX`, `NASA`, `Rocket Lab`).
- `role_title` → a **placeholder for the entry point** you'll actually reach: `Press Office` (or `Media Relations` / `Communications`). It's a stand-in — once a real person at the org picks up the story, their name and title replace the placeholder.
- `organization` → the same organization (or its parent/division if that differs).
- Contact path follows the normal rules: press email in `notes`, media-inquiry **web form URL** in `source_url` (fold-in rule), org website in `source_url` only if nothing more direct exists.
- `is_press` → `y` (you're entering through the comms desk). But an org-as-source is still **ranked on alignment** like any other source — it can be Priority A. Do **not** auto-demote it just because it routes through a press office; `is_press` here marks the *contact path*, not the source's value.

Rule of thumb: if you'd reach out to "the company" before you know which human will speak, cast the company. The placeholder gets a face later.

### Research Tools — Nimble vs. built-in fetch

Nimble is **not always required.** Use the lightest tool that returns reliable data, and escalate to Nimble only when the lighter tool fails or the target resists it.

1. **Discovering who exists** — searching for people/orgs that fit an archetype: use **Nimble search**. It gives the broadest open-web coverage for finding candidates. (Built-in **WebSearch** is a fine fallback for a quick one-off lookup.)

2. **Reading a specific URL you already have:**
   - **Static, public, cooperative page** — government bio, university faculty page, think-tank profile, personal site, Substack, blog: try **built-in WebFetch first.** It's faster and lighter.
   - **JS-heavy, paywalled, or bot-protected** — LinkedIn, X/Twitter, major news paywalls, anything behind a login/consent wall: go **straight to Nimble.** WebFetch will come back empty or blocked.
   - **WebFetch returned empty, truncated, or blocked:** escalate that one URL to **Nimble.**

3. **Bulk or structured extraction** — pulling the same fields across many profiles, or scraping a directory/roster: use **Nimble extract.** Don't loop WebFetch over many pages.

Rule of thumb: **WebFetch for a handful of friendly pages; Nimble for search, hostile pages, and scale.**

For each source, populate every field below. Leave a cell blank rather than guess. Flag anything uncertain in the `notes` field.

### Output Columns (CSV header — exact names, exact order)

The header row must be, verbatim:

```
priority,suggested_bucket,name,role_title,organization,email,phone,linkedin,source_url,confidence,why_relevant,is_press,story,location,political_leaning,assigned_to,notes,links
```

The first sixteen columns are read by Cockpit's importer. `notes` and `links` are also imported (notes → the contact's Notes field; links → the contact's link list). Keep URLs out of `notes` — every URL belongs in `links`.

| # | Column | Instructions |
|---|--------|-------------|
| 1 | `priority` | **A**, **B**, or **C** — see Priority Rules. (A = highest.) |
| 2 | `suggested_bucket` | The approved archetype label from Phase 1. The importer groups and files sources by this. |
| 3 | `name` | Full name. **Use one canonical spelling per person across every bucket they appear in** — the same individual must have an identical `name` string in all rows (never "Tom" in one bucket and "Thomas" in another, or "Wilson" vs "Wilson C."). Pick their fullest real name and reuse it verbatim. Cockpit's importer dedupes on **exact** name, so variant spellings land as duplicate contacts. A canonicalizer pass enforces this at the end (see Output Format). **When the source is an organization itself, put the org's name here — e.g. `SpaceX` — per *Organizations as sources*.** |
| 4 | `role_title` | Current or most recent relevant position. **For an organization-as-source, use a placeholder entry point — `Press Office` / `Media Relations` — to be replaced by a real contact's name and title later in the workflow.** |
| 5 | `organization` | Primary employer or affiliation. |
| 6 | `email` | Direct email if findable. If unavailable, leave blank. Do not construct from naming patterns unless the org format is confirmed on their website. |
| 7 | `phone` | Only if publicly listed on a professional profile. Do not attempt to find personal phones. |
| 8 | `linkedin` | Full profile URL. |
| 9 | `source_url` | Where you found this person / their best single direct link. **Fold-in rules:** if there is no direct personal URL, put the org media-inquiry **Online Form URL** here. If there is no personal/direct URL at all, you may put the **Organization Website** here; otherwise drop the org website. (Reference links and social profiles do NOT go here — they go in `links`.) |
| 10 | `confidence` | A float **0.0–1.0** reflecting how much source evidence was found for this contact. See Confidence Rubric. |
| 11 | `why_relevant` | 1–2 sentences on their specific relevance to this story. (The importer surfaces this as the contact's context note.) |
| 12 | `is_press` | Truthy (`y` / `yes` / `true` / `1`) if this is a press / media-relations contact rather than an individual source — **also `y` for an organization-as-source reached via its comms desk.** Blank or `n` otherwise. This flags the **contact path, not the source's value**: an `is_press = y` row can still be Priority A. |
| 13 | `story` | **Leave blank.** The CRM assigns the story at import time. |
| 14 | `location` | City and State/Country. |
| 15 | `political_leaning` | One of: **Left / Center-Left / Non-Partisan / Center-Right / Right / Unknown** — inferred from research. (Cockpit collapses Center-Left→Left, Center-Right→Right, Unknown→Non-Partisan on import; emit the precise value anyway.) |
| 16 | `assigned_to` | **Nathaniel** or **Johnny** — assigned **per archetype** at the Assignment Checkpoint (whole bucket → one owner). See Assignment Logic. |
| 17 | `notes` | **Prose only — no URLs.** Sensitivities, known positions, preferred contact channel, and anything needing manual verification. When `is_press = y`, record the press/media-relations contact name and email here. Lands in the contact's Notes field in Cockpit. |
| 18 | `links` | **All URLs except `linkedin`/`source_url`.** Credibility evidence (media appearances, published work, op-eds, cited research, testimony) and social profiles (X, Instagram, Substack). Format each as `Label: URL`, separated by semicolons — e.g. `Op-ed (Foreign Affairs): https://… ; Senate testimony: https://… ; X: https://… ; Substack: https://…`. Lands in the contact's link list in Cockpit. |

### Confidence Rubric (column 10)

- **0.90–1.00** — Identity certain; direct email or confirmed contact path; multiple corroborating public profiles or published work.
- **0.70–0.89** — Identity and current role confirmed; reachable via org/press; solid corroborating public record.
- **0.50–0.69** — Identity confirmed but sparse corroboration or only an indirect contact path.
- **below 0.50** — Tentative match or thin evidence; must be manually verified (say so in `notes`).

Round to two decimals.

Confidence measures **how sure we are this is a real, reachable person** — it is *not* a measure of their worth. A hidden-gem source with a thin public trail can legitimately be **Priority A with a modest confidence score** at the same time; rank them high for what they can speak to, and use confidence (plus a `notes` flag) to tell the journalist what still needs verifying.

### Assignment Logic (column 16)

Sources are split between **Nathaniel** and **Johnny** **by archetype, not by individual person** — every contact in a given archetype is owned by the same person. This keeps outreach simple: whoever owns an archetype runs one consistent outreach approach across the whole bucket, and either person can take **several archetypes at once** when their outreach looks alike (same channel, same framing, same kind of ask).

Assignment is decided at the **Assignment Checkpoint below, after research is finished** — when the real count of contacts in each archetype is known, so the journalists can see the size and shape of each bucket before claiming it.

You propose a starting lean for them to react to, not a final answer:
- **Nathaniel** — institutional sources, officials, think-tank voices, on-record named experts.
- **Johnny** — press contacts, spokespeople, connectors, background sources.
- (`is_press = y` archetypes almost always go to Johnny.)
- **Organization-as-source** buckets (a company/agency reached through its press office) can go to **either** owner — assign by whose outreach they resemble, not automatically to Johnny.

The journalists make the final call.

### ASSIGNMENT CHECKPOINT — STOP before writing the CSV

After research is complete and before you generate the final CSV, present an **archetype assignment table** and wait — the same present-and-wait pattern used for archetypes in Phase 1.

For each archetype, show:
- the archetype label,
- **how many contacts it holds**, with a priority breakdown (e.g. `6 — 2A / 3B / 1C`),
- a one-line **outreach note** — *how* you reach that bucket and *what* you ask (channel + kind of ask). This is the batching signal: buckets whose notes read alike should be claimed by the same owner so they run one consistent outreach. Keep it short and comparable.
- the **proposed owner** (Nathaniel or Johnny).

Order the table so archetypes with **similar outreach sit next to each other**, making it easy to claim a group in one go.

Below the table, always print a **volume tally** — the running total of people assigned to each owner — so the split can be balanced by workload, not just by topic:

```
Assigned so far —  Nathaniel: 9   ·   Johnny: 11   ·   Unassigned: 0   (20 total)
```

Worked example of the table + tally (story: munitions stockpile depth):

| Archetype | Count | Outreach note | Owner |
|---|---|---|---|
| Authority on interceptor inventories & replacement timelines | 5 — 2A/2B/1C | Direct email to personal/academic address; cold pitch for on-record expert interview | Nathaniel |
| Former defense-acquisition officials | 4 — 3A/1B | Direct email + LinkedIn DM; reference their tenure, ask on-record or background | Nathaniel |
| Think-tank analysts (CSIS, Hudson) | 4 — 1A/3B | Email via institute press contact; quick reaction quote on stockpile numbers | Johnny |
| Defense-prime media relations (Raytheon, Lockheed) | 3 — press | Corporate press desk / web form; formal media inquiry, expect slow + gatekept | Johnny |
| Frontline veterans / armorers (firsthand resupply) | 3 — 1A/2B | Warm approach via X DM or referral; sensitive, trust-first, lived-experience interview | Johnny |

```
Assigned so far —  Nathaniel: 9   ·   Johnny: 10   ·   Unassigned: 0   (19 total)
```

**Reassigning is conversational — the journalists just say it in chat.** Examples: "give the think-tank bucket to me," "flip defense-prime and think-tank," "buckets 1, 2 and 5 are mine," "Johnny takes all the press buckets, I take the rest." Whole buckets only — one archetype goes entirely to one owner.

**After every change, re-print the full table AND the updated volume tally, then wait again.** Never apply a reassignment silently and never jump to the CSV off an un-reprinted table — the journalists confirm against the numbers they can see, and the tally is how they manage each person's volume.

Once approved, write that owner into `assigned_to` for **every contact in the archetype** (whole bucket → one owner; no per-person exceptions).

**Only generate the CSV after the archetype assignment is approved.**

---

## PRIORITY RULES

Priority ranks sources who have **already cleared the alignment bar** — everyone on the list can speak credibly and on the record to the topic. Priority orders them by **how much their perspective advances the story**: the depth and directness of their topical authority and how central their angle is to the core of the piece. It is **not** a measure of résumé prestige, media presence, or public profile. A source who has never been interviewed, published, or profiled can be Priority A if their firsthand command of the subject is central to the story — these obscure, hidden-gem sources are exactly who we want, and a thin digital footprint is never a reason to rank someone down. Judge priority on the substance of what they can speak to. When two sources contribute roughly equally, the one with deeper or more direct knowledge ranks higher; when genuinely unsure, rank lower.

**Priority A** — Deep, direct authority on a perspective that is central to the story.
- A person with deep firsthand experience at the heart of the story — they lived it, ran it, built it, or witnessed it directly
- A practitioner or operator with hands-on command of the subject
- A recognized authority — academic, analyst, former official, or industry figure — whose expertise is directly central to the story
- A journalist or author who has done significant original work on this exact topic
- A layperson whose unique firsthand knowledge is more central to the story than any credentialed expert's
- An organization whose **official, on-record position** is itself central to the story (represented per *Organizations as sources*) — ranked on the centrality of that position, not demoted for being institutional

**Priority B** — Strong, relevant knowledge, but a step removed from the core of the story.
- Solid topical command, but their experience sits adjacent to the central events (advised on it, studied it, worked near it) rather than at the center
- An analyst, academic, or researcher with real depth on the beat, in a supporting rather than central role
- Someone with direct experience of a narrower slice of the story

**Priority C** — A valid perspective on a narrower or more peripheral angle.
- Adds useful context or one specific angle, but not depth across the core subject
- Relevant standing with limited or narrow experience of the story
- A genuine background voice whose contribution is one piece of the picture

---

## CONTACT INFO APPROACH

Gather what exists publicly. Never fabricate or guess.

- Direct email on org website or public profile: put it in `email`.
- Personal email on personal site or Substack: put it in `email`.
- No individual email but a press/media-relations contact exists: set `is_press = y`, and record the press contact name/email in `notes`. Still include the individual's name and LinkedIn so the journalist can reach them directly.
- Only a web form: put the form URL in `source_url` (per the fold-in rule) and note it in `notes`.
- Phone: only include if publicly listed on a professional profile page.
- Reference links and social profiles: put every URL in `links` (labeled), never in `notes`.

---

## OUTPUT FORMAT

Deliver as a **CSV file** (RFC-4180 quoting) written with Python's `csv` module.

- First row is the exact header listed above (18 columns, in that order).
- One row per source.
- Any field containing a comma, quote, or newline must be quoted properly — the `csv` module handles this; do not hand-roll the CSV.
- Sort: `priority` (A first), then `suggested_bucket` alphabetically, then `name` alphabetically within each bucket.
- Leave `story` blank in every row.

Filename: `[Story Title] — Source List — [YYYY-MM-DD].csv`

### Canonicalize names before handing off

The same person frequently anchors several buckets, and their `name` can drift across rows ("Tom" vs "Thomas Karako"). Cockpit dedupes on **exact** name, so drift creates duplicate contacts. After writing the CSV, run the canonicalizer to force one spelling per person:

```
python3 ~/.claude/skills/source-casting/canonicalize_names.py "[Story Title] — Source List — [YYYY-MM-DD].csv"
```

It rewrites same-person name variants to a single spelling **in place** (it does not merge or drop rows — cross-listed people still get one row per bucket) and prints a report. **Read the report before handing off:**
- Unified spellings are safe — that's the point.
- Any **"same person key under DIFFERENT orgs"** warnings are judgment calls: usually one person who changed jobs (correctly left as separate rows), occasionally two different people. Confirm each, and fix the CSV by hand if a warning is actually wrong.

Add `--dry-run` to preview the report without writing. (The nickname/normalization logic mirrors Cockpit's importer guard, so the two agree.)

**Organization-as-source rows** are handled too: an org name in `name` is deduped like any other and isn't nickname-expanded in the normal case (`SpaceX` stays `SpaceX`). Skim the report for any org name that got unexpectedly rewritten (rare — e.g. an org whose first word is a common nickname) and fix it by hand.

After writing and canonicalizing the file, tell the journalist they can paste its contents (or upload the file) into Cockpit → a story's **Import Sources** modal, where they pick the keepers and file them into buckets.

---

## NIMBLE USAGE LOGGING (after handoff)

Nimble bills by credit, and this skill is where almost all Nimble usage happens. After the CSV is handed off, log the run's credit spend to Cockpit so its **API Spend** card (Dashboard) and **Nimble** card (Admin) stay current.

The Nimble CLI doesn't report a running balance, so don't guess credits. Instead:

1. **Report the run's Nimble footprint** to the journalist — roughly how many Nimble operations you ran, broken down by kind. E.g. *"This run used Nimble for ~18 searches and 4 extracts."* (Count your actual `nimble search` / `nimble extract` / `nimble map` calls; built-in WebFetch/WebSearch don't cost Nimble credits.)
2. **Ask for the credits spent** — the authoritative number is in the journalist's Nimble dashboard (Usage). Ask them to read it off, or to give the delta since the last run. If they'd rather skip, that's fine — they can log it later via Cockpit's in-app **"+ Log"** button on the Admin → Nimble card.
3. **Log it** with the helper (uses `COCKPIT_URL` + `NIMBLE_LOG_SECRET` from the shell env; it's best-effort and never breaks the run):

```
python3 ~/.claude/skills/source-casting/log_nimble_usage.py <credits> "<story> — N searches, M extracts"
```

Example: `python3 ~/.claude/skills/source-casting/log_nimble_usage.py 120 "Munitions stockpile — 18 searches, 4 extracts"`

If `COCKPIT_URL` / `NIMBLE_LOG_SECRET` aren't set, the helper says so and exits cleanly — tell the journalist to set them (or use the in-app form) and move on.

---

## ACCURACY RULES

- Never fabricate a name, title, affiliation, contact detail, quote, or link.
- If uncertain about a specific fact, leave the cell blank and flag it in `notes`.
- Do not construct email addresses from naming conventions unless the format is confirmed on the org website.
- Do not infer phone numbers or social profiles — only include what you have actually found.
- "Verify this" in `notes` is a feature, not a weakness.
