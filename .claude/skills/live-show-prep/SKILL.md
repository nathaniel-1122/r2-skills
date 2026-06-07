---
name: live-show-prep
description: "Use this skill to prepare a live news show. Given a show's segment lineup (topic bullets, anchor clips, and viewer questions), it live-researches every story, fact-checks the numbers, and produces two host-ready PDFs in R²'s deep-dive field-guide format: (1) an extensive Research Brief to read beforehand, and (2) a one-glance Host Cheat Sheet for the desk. Triggers: 'prep the live show', 'make the host brief/cheat sheet', 'build the field guide for tonight's lineup', or pointing at Live Segment_*.txt files."
allowed-tools:
  - Bash(nimble:*)
  - Bash(bash:*)
  - Bash(./assets/render.sh:*)
  - Bash(chmod:*)
  - Bash(mkdir:*)
  - Bash(cp:*)
  - Bash(cat:*)
  - Bash(ls:*)
  - Bash(mdls:*)
  - Bash(qlmanage:*)
  - WebSearch
  - WebFetch
  - Write
  - Read
  - Edit
---

# Skill: Live Show Prep — Research Brief + Host Cheat Sheet
## R² Media — Newsroom Live-Show Desk Prep

You are acting as a senior producer briefing the host of R² Media's live news show.
Given tonight's lineup, your job is to teach the host the stories cold and hand them
two documents: a **Research Brief** they read beforehand, and a **Host Cheat Sheet**
they keep on the desk. Think *"what would be in front of someone briefing Bill Maher."*

The two deliverables are **PDFs in R²'s deep-dive field-guide format** — the same look
as the long-form Field Guides, with confidence-flagged stats and a "Do-Not-Say" panel.

---

## THE TWO DELIVERABLES

1. **Research Brief / Field Guide** (`… Research Brief.pdf`) — the read-through. Long,
   narrative, enough to talk ~30 minutes per segment. Per-chapter boxes, glossary, sources.
2. **Host Cheat Sheet** (`… Host Cheat Sheet.pdf`) — the desk reference. Dense, scannable:
   stat tables, the lines that land, rebuttals, lightning viewer-Q answers, Do-Not-Say.

Both are built from bundled templates so the format is identical every time. The
templates live in `assets/` next to this file:

- `assets/template-brief.html` — the Research Brief template (full house CSS + a worked example body).
- `assets/template-cheatsheet.html` — the Host Cheat Sheet template (same).
- `assets/render.sh` — renders an HTML file to a print-ready PDF (headless Chrome, embeds fonts).

> **The `<style>` block in each template IS the design system — keep it byte-for-byte.**
> The body of each template is a *worked example from a past show*. **Never ship that
> example content.** You keep the `<style>`, delete the example body, and rebuild the body
> from this show's research.

---

## CORE PRINCIPLES — READ BEFORE YOU START

1. **Research live; the date matters.** Shows cover current events that are usually *after*
   your training cutoff. Do **not** trust memory or the example template's facts — go find
   what is actually true as of the show date.
2. **Attribute everything; prefer ranges to false precision.** Every load-bearing number gets
   a **named source, a date, and a confidence flag** (`HIGH` / `MED` / `LOW`). Separate what is
   *confirmed* from what is *claimed*. If a dramatic stat doesn't survive checking, it goes in
   the **Do-Not-Say** panel with a defensible alternative — it does not go in the prose.
3. **The host has to defend it on air.** Write so a caller or guest can't catch them out. The
   safest framing beats the most dramatic one.
4. **Never overwrite existing files.** Give outputs clear, dated names. If a prior version
   exists, write alongside it — don't clobber it.

---

## PHASE 0 — INTAKE  ·  *(checkpoint)*

Read the show's lineup. It usually comes as **`Live Segment_*.txt`** files (one per segment,
plus often a "Questions" file with real viewer questions) in `$ARGUMENTS` or a folder the user
points at. Extract and list back to the user:

- Each **segment** and its core topics.
- The **anchor clips / chyrons** named in each segment (these are your must-cover beats).
- Every **viewer question** (each one must get answered in both documents).
- The **research clusters** you'll chase (group the topics into ~5–8 buckets).

**Checkpoint:** show this map and confirm the segment list + clusters before researching.

---

## PHASE 1 — LIVE RESEARCH

Research each cluster with live web tools. **Prefer Nimble** (`nimble search …`, or the Nimble
MCP tools) when `NIMBLE_API_KEY` is set; otherwise use **WebSearch / WebFetch**. (Check once:
`nimble --version` and a trial `nimble search`; if it returns `401 Unauthorized`, the key isn't
set — fall back to WebSearch and tell the user Nimble needs its key.)

For broad lineups, run clusters in **parallel research agents** (one per cluster) to stay fast.
Each cluster returns **dated, sourced facts, each with a HIGH/MED/LOW confidence rating**, and a
running list of **widely-repeated stats that DON'T hold up** (for the Do-Not-Say panel).

Cover, per the lineup: the spine of each story (who/what/when, with dates), the load-bearing
numbers, the "why it matters to a US viewer" hook, and a sourced answer to **every** viewer
question.

---

## PHASE 2 — ADVERSARIAL FACT-CHECK  ·  *(checkpoint)*

Take the ~10–15 most dramatic / load-bearing stats and verify each against a second independent
source. Assign final confidence. Build the **Do-Not-Say list**: the figure that circulates, why
it fails, and the defensible thing to say instead. Anchor on ranges where the truth is genuinely
uncertain or classified.

**Checkpoint:** present a short findings summary + the Do-Not-Say list before writing. This is
where the user catches anything off.

---

## PHASE 3 — WRITE THE RESEARCH BRIEF

Copy `assets/template-brief.html` to the output folder, **keep its `<style>` verbatim**, and
rebuild the body. Structure (each chapter carries the boxed components shown in the template):

- **Cover** — kicker, masthead, a big title, an italic dek, a meta line with the confidence key.
- **One-paragraph opener** ("if you read nothing else") with a drop cap.
- **How-to-use** box + **confidence note** box + a two-column **road map** (table of contents).
- **Parts & chapters.** Group into Part I / Part II (one per segment). Each chapter:
  `What you'll learn` → narrative prose → `Key terms` and/or `Misconception / Gotcha` boxes →
  `Takeaways` recap → `Host lines you can say on air` → `Audience question, answered` (drawn
  from the real viewer questions). Use **stat cards** and the **data-viz bar** for the headline numbers.
- **Glossary** + **Sources & where the numbers come from** (named institutions, with the
  confidence discipline spelled out).
- Page numbers render automatically in the footer (CSS `@page`), suppressed on the cover.

Box CSS classes available (see template): `.box.learn`, `.box.terms`, `.box.gotcha`, `.box.take`,
`.box.lines`, `.box.aq`; `.chip.c-high/.c-med/.c-low`; `.stats/.stat`; `.viz/.bar`; `table`.

Length: aim for a thorough read-through (the example runs ~30 pages at large, easy-on-the-eyes type).

---

## PHASE 4 — WRITE THE HOST CHEAT SHEET

Copy `assets/template-cheatsheet.html`, keep its `<style>`, rebuild the body. Sections:

- **Through-line** (the one idea, said once up top) — the dark banner.
- Per-segment **key-number tables** (`.num` rows: label + value + confidence chip).
- An **event timeline** (`.tl`) for any breaking story with dates.
- **Names & players** glossary-in-brief.
- **The lines that land** (`.line`) — punchy host quotes.
- **If a guest/caller says X → you say Y** (`.xy`) — rebuttals.
- **Viewer Q&A — lightning answers** (`.qa`) — one line per viewer question.
- **⛔ Do-Not-Say (failed fact-check)** (`.dns`) — the quarantined stats + the safe alternative.

Keep it dense and scannable; it's a glance tool, not a read.

---

## PHASE 5 — RENDER & DELIVER

Make the script runnable once: `chmod +x assets/render.sh`. Then render each file:

```
bash "<skill>/assets/render.sh" "<output folder>/… Research Brief.html"
bash "<skill>/assets/render.sh" "<output folder>/… Host Cheat Sheet.html"
```

`render.sh` finds Chrome, gives fonts time to load, and embeds them so the PDF is portable.
**Verify before handing off:** check page counts (`mdls -name kMDItemNumberOfPages -raw file.pdf`)
and eyeball page 1 (`qlmanage -t -s 1400 -o /tmp "file.pdf"`) to confirm fonts loaded, the boxes
and bars render, and nothing is clipped. Keep the `.html` sources next to the PDFs for edits.

Deliver the two PDFs with a short note: what each is, the headline findings, and the one or two
"moving" numbers worth a refresh if the show is days out.

---

## DESIGN SYSTEM (for reference; it lives in the template `<style>`)

- **Type:** *Newsreader* (body, made for long-form news), *Fraunces* (display/headlines/numerals),
  *IBM Plex Sans* (labels, tables, chips). Loaded from Google Fonts; embedded at render.
- **Palette:** warm paper, ink near-black, R² red accent, navy / amber / green for box types;
  green = HIGH, amber = MED, grey = LOW confidence chips.
- **Print:** US Letter, comfortable measure, generous leading, page-break-safe boxes, footer page numbers.

If the host wants the type bigger/smaller, change the `body { font-size }` in the template `<style>`
(and scale headings/tables proportionally), then re-render.

---

## GUARDRAILS — DON'T

- Don't ship the template's example content, or any fact from it, without re-verifying it live.
- Don't state a contested figure flat — attribute it, or move it to Do-Not-Say.
- Don't overwrite an existing brief/cheat sheet — write a clearly-named new file.
- Don't claim Nimble was used if it 401'd — say which tool actually sourced the facts.
