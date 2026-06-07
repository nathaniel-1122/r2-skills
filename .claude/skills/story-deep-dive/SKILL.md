---
name: story-deep-dive
description: "Use this skill to research a single story in depth and produce R²'s two-part deep-dive package: an illustrated Deep-Dive Field Guide (the 'teach-me' main read) and a Quick Dossier (the fast reference, with a Who-To-Interview list). Both are live-researched with numbered, hyperlinked sources, and designed to be genuinely engaging to read (strong signposting, badge-coded callouts, pulled-out stats). Length flexes to the story. Triggers: 'do a deep dive on X', 'build the field guide + dossier for [story]', 'research [topic] for an episode', 'make a story deep-dive'."
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

# Skill: Story Deep Dive — Field Guide + Quick Dossier
## R² Media — Newsroom Story Research Desk

You are acting as R² Media's senior story-research producer. Given a single story or
topic, you teach it cold and hand back two documents a host or producer uses to build an
episode and walk into interviews: a **Deep-Dive Field Guide** (the long "teach-me" read)
and a **Quick Dossier** (the fast, fact-dense reference). Both are **live-researched** and
every figure carries a **numbered, clickable source**.

---

## THE TWO DELIVERABLES

1. **Deep-Dive Field Guide** (`… (Field Guide).pdf`) — the illustrated, chaptered, explanatory
   read. Teaches the *why* and *how* so the host can follow the argument and ask sharp questions.
   Per-chapter signposting (a one-line **THE GIST**, badge-coded boxes), charts, pulled-out stat
   bands, pull quotes; numbered hyperlinked sources + appendix.
2. **Quick Dossier** (`… (Dossier).pdf`) — the terse, fast reference: a one-line thesis hero, a
   key-numbers strip, numbered sections (every fact bracket-sourced), and a **Who To Interview**
   card set (people, companies, orgs).

**Length flexes to the story.** Make each document as long as it needs to be to genuinely prepare
the reader — more chapters/sections or fewer. Completeness over page count; never pad to a length.

Both are built from bundled templates so the house format is identical every time. The
templates live in `assets/` next to this file:

- `assets/template-field-guide.html` — the Field Guide (full house CSS + a skeleton showing every component).
- `assets/template-dossier.html` — the Quick Dossier (same).
- `assets/render.sh` — renders an HTML file to a print-ready PDF (headless Chrome, embeds fonts).

> **Keep each template's `<style>` block byte-for-byte — it IS the design system.** The
> bodies are skeletons with `[bracketed placeholders]`. Build a story by keeping the
> `<style>`, deleting the placeholder body, and writing the real content from research.
> **Never ship placeholder text or example facts.**

---

## CORE PRINCIPLES — READ BEFORE YOU START

1. **Research live; verify every source.** These are reported documents. Use live web tools
   and trace **every** load-bearing number to a real, named source with a working link. Do
   not invent citations, quotes, or URLs. If you can't verify it, don't state it.
2. **Numbered, linked citations.** In the prose, hard claims get a bracketed superscript
   (`<sup class="c"><a href="#s7">7</a></sup>`) that links to a numbered **Sources** list at
   the end. Every `[n]` in the text must have a matching source entry, and vice-versa.
3. **Flag contested figures.** Where outlets disagree, use the most recent/authoritative
   figure and **say so on the page** — give the range and which measure you're using (e.g.,
   "Japan defense spend ≈2% of GDP on Tokyo's accounting vs ≈1.4% on SIPRI's calendar-year
   measure — say which"). The host must not get caught out.
4. **Teach, don't dump — and make it a pleasure to read.** The Field Guide makes the reader
   *fluent* (explain mechanisms and concepts), but lean on the design system — **THE GIST**
   one-liners, badge-coded boxes, pulled-out stat bands, pull quotes, sub-heads, sidebars — to
   chunk the text and keep an easily-distracted reader engaged *without* sacrificing rigor or
   detail. Vary the visual rhythm chapter to chapter. The Dossier is the opposite mode: terse,
   scannable, every line a fact.
5. **Never overwrite existing files.** Name outputs clearly; write alongside any prior version.

---

## PHASE 0 — INTAKE & OUTLINE  ·  *(checkpoint)*

Take the story/topic from `$ARGUMENTS` (a pitch, a title, or a paragraph). Establish and show back:

- The **thesis / reframe** — the one idea that makes the story click (one sentence).
- The **series + tags** — Desk-Reported vs Field/Road; topic tags (e.g., *Conflict + Money*).
- A **chapter outline** for the Field Guide (usually **6–9 chapters**: why it matters → core
  mechanism → the numbers → the players → the debate → where it's going).
- The **Dossier section list** (Executive Summary → Why This Matters Now → How We Got Here →
  mechanism → players → debate → scale → risks → what to watch).

**Checkpoint:** confirm the thesis and the outline before researching.

---

## PHASE 1 — DEEP LIVE RESEARCH

Research with live web tools. **Prefer Nimble** (`nimble search …`) when `NIMBLE_API_KEY` is
set; otherwise WebSearch / WebFetch. (Quick check: `nimble --version` + a trial `nimble search`;
on `401` the key isn't set — fall back and say so. Note the account may not have the `fast`
tier — use default depth.)

Gather, building a **numbered source list as you go** (each entry: outlet/author, title, date, URL):

- The **narrative arc** and the mechanism — enough to teach each chapter.
- Every **load-bearing number**, each tied to a specific source. Prefer primary sources and
  named institutions (CSIS, SIPRI, government filings, company releases, major outlets).
- The **key players** — states, companies, individuals — and what each controls.
- The **live debate** — the strongest case on each side; the genuinely contested figures.
- **Interview targets** — real, reachable people/orgs who can speak to this on the record.

For big topics, run **parallel research agents** (one per chapter/cluster) to stay fast; each
returns sourced facts + links.

---

## PHASE 2 — FACT-CHECK & FLAG  ·  *(checkpoint)*

Verify the dramatic / load-bearing figures against a second source. Where they diverge, pick the
authoritative one and write the **flag** you'll put on the page. Confirm every link resolves
(note any that are paywalled or block fetchers — they still count, just flag them).

**Checkpoint:** present the outline + headline findings + the numbered source list before writing.

---

## PHASE 3 — WRITE THE FIELD GUIDE

Copy `assets/template-field-guide.html`, **keep its `<style>`**, rebuild the body:

- **Cover** (`.cover`) — wordmark + series pill, kicker, big title, italic dek, topic tags, a
  **reading-map** pill row (chapter count, sources count, the payoff), and the compiled/sourced line.
- **The one-sentence version** — the dark **`.bigidea`** band ("if you read nothing else").
- **How to use this guide** (`.howto`) → **The route** TOC (`.toc`, numbered).
- **Chapters** (`<section class="chap">`) — each opens with `.chap-open` (a big ghost numeral, a
  `Chapter N` kicker, the title, and a one-line **`.gist` THE GIST** band), then a
  `What you'll learn` box → explanatory narrative **with inline citations**, paced with
  `.statband` (a big pulled-out number), `.pull` (a pull quote), `.viz` charts, `h4.sub`
  sub-heads, and the occasional `.aside` sidebar → `Key terms` / `Misconception / Gotcha` boxes →
  `Takeaways` → **`Questions to ask`** (the sharp interview questions the chapter sets up).
  Chapters start on a new page automatically.
- **Glossary** + a numbered **Sources** appendix (`<li id="s1">…<a href>`). Footer page numbers
  render automatically; the cover stays clean.

Components (see template): boxes `.box.learn / .terms / .gotcha / .take / .ask` (each carries a
colored `.badge` glyph — ◎ § ! ✓ ?); `.bigidea`, `.gist`, `.statband`, `.pull`, `.aside`,
`.stats/.stat`, `.viz/.bar`, `table`; citations `<sup class="c"><a href="#sN">N</a></sup>` →
`.sources ol li[id]`. Keep the badge glyphs and box classes as-is — they're the learnable system.

---

## PHASE 4 — WRITE THE QUICK DOSSIER

Copy `assets/template-dossier.html`, keep its `<style>`, rebuild the body:

- Masthead (wordmark + series pill) + kicker + big title + tags.
- **The story in one line** — the dark `.oneline` hero.
- A **key-numbers strip** (`.keynums`) — 3–4 of the most important figures up top, for instant scanning.
- A one-line **how-to-read** note, then **numbered sections** (`h2.sec` with a red number badge):
  Executive Summary as cited bullets → Why This Matters Now → How We Got Here → mechanism →
  players → debate → scale → risks → what to watch. Terse, every number bracket-cited.
- **Who To Interview** — `.icards` grouped People / Companies / Organizations, each with a one-line why.
- A numbered **Sources** list. Keep the dossier's facts and citations **consistent with the Field
  Guide** (reuse the same source set).

---

## PHASE 5 — RENDER & DELIVER

`chmod +x assets/render.sh` once, then render each file:

```
bash "<skill>/assets/render.sh" "<out>/[NN — Title] (Field Guide).html"
bash "<skill>/assets/render.sh" "<out>/[NN — Title] (Dossier).html"
```

**Verify before handing off:** page counts (`mdls -name kMDItemNumberOfPages -raw file.pdf`),
eyeball page 1 (`qlmanage -t -s 1400 -o /tmp "file.pdf"`) to confirm fonts loaded, boxes/charts
render, and nothing is clipped, and spot-check that a couple of source links are real. Keep the
`.html` sources next to the PDFs. Deliver with a short note: the thesis, the 2–3 headline numbers
(and any contested-figure flags), and the interview shortlist.

---

## DESIGN SYSTEM (lives in the template `<style>`)

The design goal: a **premium intelligence-briefing / explanatory-magazine** feel that is genuinely
engaging and easy to read — strong signposting and scannable entry points for an easily-distracted
reader — while staying serious, credible, and detail-dense. The signposting is a *learnable system*,
so keep it consistent:

- **Type:** *Newsreader* (body), *Fraunces* (display/headlines/numerals), *IBM Plex Sans*
  (labels, tables, citations). Loaded from Google Fonts; embedded at render.
- **Palette:** warm paper, near-black ink, R² red accent; the **box taxonomy is colored and
  badge-coded** so the eye sorts the page: navy ◎ *what you'll learn*, teal § *key terms*, red !
  *gotcha*, green ✓ *takeaways*, amber ? *questions to ask*. Don't recolor or relabel these.
- **Rhythm tools** (use them to vary the pace and re-grab attention): `.bigidea` dark lead band,
  `.gist` chapter one-liners, `.statband` big pulled-out numbers, `.pull` pull quotes, `.aside`
  sidebars, the `.viz` bar chart, and oversized ghost chapter numerals.
- **Print:** US Letter, footer page numbers, page-break-safe boxes, new-page chapter starts.

If you need the type bigger/smaller, change `body { font-size }` in the template `<style>` and
scale headings proportionally, then re-render. To redesign the look itself, use the **frontend-design**
skill — but keep the badge taxonomy and box classes stable so the system stays learnable.

---

## GUARDRAILS — DON'T

- Don't invent sources, links, quotes, or numbers. Every figure traces to a real, named source.
- Don't leave an orphan citation — every `[n]` maps to a source entry and every source is cited.
- Don't state a contested figure flat — give the range, name the measure, flag it on the page.
- Don't ship the template's placeholder/skeleton text or example facts.
- Don't overwrite an existing guide/dossier — write a clearly-named new file.
