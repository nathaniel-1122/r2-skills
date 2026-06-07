# R² Media — Claude Skills

This repository holds R² Media's custom **Claude Code skills**. There are three:

- **`source-casting`** — researches and ranks interview sources for a story and
  produces a CSV you import straight into Cockpit.
- **`live-show-prep`** — preps a live show: it live-researches tonight's lineup,
  fact-checks the numbers, and produces two host-ready PDFs — a long **Research
  Brief** to read beforehand and a one-page **Host Cheat Sheet** for the desk.
- **`story-deep-dive`** — researches one story in depth and produces the two-part
  package: a **Deep-Dive Field Guide** (the "teach-me" main read) and a **Quick Dossier**
  (the fast reference, with a Who-To-Interview list), both with numbered, clickable sources.
  Length flexes to the story.

A "skill" is just an instruction file that teaches Claude how to do one of our
workflows the same way every time. You don't run code — you talk to Claude, and
the skill kicks in. All three skills live in this one repo, so you clone it **once**
and link each skill you want.

---

## For Johnny — getting the skill on your machine

This is a one-time setup. After it's done, you just talk to Claude normally and
the skill is there. You'll need three things first:

1. **Claude Code** installed and working on your Mac.
2. **Git** installed. (On a Mac, open the **Terminal** app and type `git --version`
   then hit Return. If it asks to install developer tools, click **Install** and
   wait. If it prints a version number, you're set.)
3. **Access to this GitHub repo.** Ask Nathaniel to add your GitHub account to
   `nathaniel-1122/r2-skills` so you can clone it.

### Check first — am I already set up?

Before doing anything, open the **Terminal** app and paste this **whole block** in
at once, then press Return. It only *looks* at your machine — it changes nothing —
and tells you what's already in place and what's missing:

```
echo "Checking your r2-skills setup…"; echo
command -v git >/dev/null 2>&1 && echo "✅ git is installed" || echo "❌ git is NOT installed  → do Step 1's note about git"
[ -d ~/r2-skills/.git ] && echo "✅ repo is cloned at ~/r2-skills" || echo "❌ repo not cloned  → do Step 1"
[ -d ~/.claude/skills ] && echo "✅ Claude skills folder exists" || echo "❌ skills folder missing  → do Step 2"
for s in source-casting live-show-prep story-deep-dive; do
  L=$(readlink ~/.claude/skills/$s 2>/dev/null)
  if [ "$L" = "$HOME/r2-skills/.claude/skills/$s" ]; then echo "✅ '$s' is linked into Claude"
  elif [ -n "$L" ]; then echo "⚠️  '$s' linked, but to the wrong place ($L)  → message Nathaniel"
  elif [ -e ~/.claude/skills/$s ]; then echo "⚠️  '$s' is a copy, not a link  → message Nathaniel"
  else echo "❌ '$s' is not linked  → do Step 3"; fi
done
for d in ~/.claude/skills/*/; do
  f="${d}SKILL.md"; [ -f "$f" ] || continue
  fold=$(basename "$d")
  nm=$(grep -m1 '^name:' "$f" | sed 's/^name:[[:space:]]*//;s/[[:space:]]*$//;s/"//g')
  [ -n "$nm" ] && [ "$nm" != "$fold" ] && echo "⚠️  folder '$fold' actually holds a skill named '$nm' — mixed-up file  → message Nathaniel"
done
echo
ok=1; for s in source-casting live-show-prep story-deep-dive; do [ -f "$(readlink ~/.claude/skills/$s 2>/dev/null)/SKILL.md" ] || ok=0; done
if [ "$ok" = 1 ]; then
  echo "🎉 ALL SET — all three skills are installed. Nothing to do. (To get the newest versions, run 'cd ~/r2-skills && git pull'.)"
else
  echo "➡️  NOT fully set up — do the steps below for anything marked ❌, then run this check again."
fi
```

- If it says **🎉 ALL SET**, stop — you're done. Don't re-run the setup steps.
- If it says **➡️ NOT fully set up**, do only the steps marked **❌** below, then
  paste this check again to confirm.
- Any **⚠️** line means something's half-there — don't try to fix it yourself,
  just message Nathaniel.

### One-time setup (copy/paste, one block at a time)

Only do the steps the check flagged with **❌**. Copy each block below, paste it
in, press Return, let it finish before doing the next one.

**Step 1 — download the repo to your home folder:**

```
cd ~
git clone https://github.com/nathaniel-1122/r2-skills.git
```

If it asks you to sign in to GitHub, do so. When it finishes you'll have a folder
called `r2-skills` in your home folder.

**Step 2 — make sure your Claude skills folder exists:**

```
mkdir -p ~/.claude/skills
```

**Step 3 — link the skills into Claude (this is the important one):**

```
ln -s ~/r2-skills/.claude/skills/source-casting ~/.claude/skills/source-casting
ln -s ~/r2-skills/.claude/skills/live-show-prep  ~/.claude/skills/live-show-prep
ln -s ~/r2-skills/.claude/skills/story-deep-dive ~/.claude/skills/story-deep-dive
```

Those `ln -s` commands each make a **shortcut** (a "symlink"). They tell Claude:
"these skills live inside the r2-skills folder." Because they're shortcuts and not
copies, whenever you update the repo (see below) Claude instantly uses the new
version — you never re-install. (Want only one skill? Just run the line for the one
you want.)

**Step 4 — confirm it worked:** paste the **"Check first"** block from above again.
It should now say **🎉 ALL SET**.

> If Step 3 says "File exists," you may already have an old copy. Stop and message
> Nathaniel rather than deleting anything — we don't want to wipe a real skill.

---

## How to use `source-casting`

**Which folder to open first.** The skill works in *any* folder (it's installed
globally), but it **saves the finished CSV into whatever folder you have open** —
so pick where you want the file to land:

- **Don't** run it inside the **`field-reporter-crm`** folder — that's the Cockpit
  app's code; story files shouldn't go there.
- **Do** use a neutral, non-code folder. Your **home folder** is fine, or make a
  dedicated one (e.g. a folder called `source-lists`) so every story's CSV
  collects in one place. Use the folder picker (bottom-left in Claude) to switch.

Then just ask in plain English, e.g.:

> "Cast sources for this story: *[paste your pitch or brief]*"

or type the slash command:

```
/source-casting
```

Claude runs it in two phases, stopping for your approval each time:

1. **Archetypes** — it proposes the *types* of sources the story needs. You add,
   cut, and refine. It waits for your OK.
2. **Research + assignment** — it finds real people, then shows an **assignment
   table**: each source type, how many people it found, a one-line note on how
   you'd reach them, and who it suggests handles each bucket (you or Nathaniel) —
   plus a running headcount per person. You rebalance by just saying so ("give me
   the think-tank bucket," "Johnny takes all the press ones"). It re-prints the
   table after every change. When you approve, it writes the **CSV**.

Then in Cockpit, open a story → **Import Sources** → paste or upload that CSV.

**Important:** talking to the skill *while it's running* only steers that one
story. It does **not** change the skill itself. To change the skill permanently
(for every future story), see the next section.

---

## How to use `live-show-prep`

This one preps a live show. You give it the show's **segment lineup** — the little
text files with each segment's topic bullets, the on-screen clips/chyrons, and the
viewer questions (the `Live Segment_*.txt` files) — and it hands back two PDFs:

- a long **Research Brief** to read before air, and
- a one-page **Host Cheat Sheet** for the desk (key stats, punchy lines, rebuttals,
  quick answers to the viewer questions, and a "Do-Not-Say" list of numbers that
  don't hold up).

**Which folder to open first.** Like the other skill, it saves the finished files
into whatever folder you have open — so open the folder where your show files live
(or where you want the PDFs to land), using the folder picker (bottom-left in Claude).

Then just ask in plain English, e.g.:

> "Prep tonight's live show from these segment files."

or point it at the folder, or type the slash command:

```
/live-show-prep
```

It works in checkpoints, stopping for your OK along the way:

1. **Intake** — it reads the lineup and lists back the segments, the must-cover clips,
   and every viewer question, plus the research buckets it'll chase. You confirm.
2. **Live research + fact-check** — it researches each story with live web data
   (it'll use **Nimble** if your `NIMBLE_API_KEY` is set, otherwise normal web
   search), then shows you the headline findings and the **Do-Not-Say** list before
   writing. You catch anything off.
3. **Write + render** — it builds both documents in our house field-guide format and
   renders them to PDF (with the fonts baked in, so they print anywhere). The editable
   `.html` sources land next to the PDFs.

**Good to know:**

- **Research is live**, so the facts reflect the show date — not Claude's memory. Every
  number carries a source and a confidence flag; shaky stats get quarantined, not stated.
- It needs **Google Chrome** installed (that's what turns the pages into PDFs) and an
  internet connection the first time it renders (to fetch the fonts).
- Want the text bigger/smaller or a different look? Just ask — or tell Nathaniel and
  he'll tweak the template once for everyone.

---

## How to use `story-deep-dive`

This one researches a **single story** in depth and hands back the two-part package we
use to build an episode:

- a **Deep-Dive Field Guide** — the illustrated "teach-me" read (chapters, charts,
  key terms, "questions to ask" boxes), and
- a **Quick Dossier** — the fast, fact-dense reference, ending with a **Who-To-Interview** list.

Both come out as PDFs with **numbered, clickable sources** — every figure traces to a real link,
and each is **as long as the story needs** (no fixed page count).

**Which folder to open first.** It saves the finished files into whatever folder you have open,
so open the folder where you want them to land (e.g. a `story-research` folder), using the folder
picker (bottom-left in Claude).

Then just ask in plain English, e.g.:

> "Do a deep dive on *[your story or topic]*."

or type the slash command:

```
/story-deep-dive
```

It works in checkpoints, stopping for your OK:

1. **Outline** — it pitches the story's core idea (the "reframe"), the chapter list for the Field
   Guide, and the Dossier's sections. You shape it.
2. **Research + fact-check** — it researches live (using **Nimble** if your key is set, otherwise
   normal web search), builds a numbered source list, and flags any contested numbers before
   writing. You catch anything off.
3. **Write + render** — it writes both documents in our house deep-dive format and renders them to
   PDF (fonts baked in). The editable `.html` sources land next to the PDFs.

**Good to know:**

- **Every number is sourced and linked.** Where outlets disagree, it uses the most authoritative
  figure and **flags the discrepancy on the page**, so you don't get caught out on camera.
- Like the other skills, it needs **Google Chrome** (to make the PDFs) and an internet connection
  the first time it renders (to fetch the fonts).
- Setting up **Nimble** (next section) makes the research better — recommended.

---

## Turning on Nimble research (recommended for `live-show-prep` and `story-deep-dive`)

Both research skills (`live-show-prep` and `story-deep-dive`) do their homework with
**Nimble**, our web-research tool. It's **optional** — without a key they just use
ordinary web search — but with it the research is better, so it's worth two minutes.
This is a **one-time** setup per Mac.

> 🔒 **Never put this key in this repo, in a story file, or in a shared chat.** It
> lives only on your own Mac, in a hidden settings file in your home folder.

**Step 1 — get your key.** Ask Nathaniel for your **Nimble API key**. It's a long
string of letters and numbers (it looks like `af2799…3fde`).

**Step 2 — save it on your Mac.** Open the **Terminal** app, then paste the line
below **with your real key in place of `paste-your-key-here`**, and press Return:

```
echo 'export NIMBLE_API_KEY="paste-your-key-here"' >> ~/.zshrc
```

> Already have a `NIMBLE_API_KEY` line from before? Don't add a second one — you'd end
> up with two and they fight. Open `~/.zshrc` in a text editor and replace the old
> value, or just message Nathaniel and he'll sort it.

**Step 3 — open a brand-new Terminal window.** This matters: the change only takes
effect in Terminal windows you open *after* Step 2. In the new window, paste this check:

```
[ -n "$NIMBLE_API_KEY" ] && echo "✅ key is set" || echo "❌ not set — redo Step 2, then open a NEW Terminal"
nimble search --query "test" 2>&1 | head -5
```

- See **✅ key is set** followed by some `{ "results": … }` text? You're done — Nimble
  is on, and `live-show-prep` will use it automatically.
- Says **401**? The key didn't load — redo Step 2 and be sure to open a **new** Terminal.
- Mentions `search_depth 'fast' … not enabled`? **Ignore it** — it's harmless; the skill
  uses the standard setting.
- Says **`nimble: command not found`**? The Nimble tool isn't installed on your Mac yet —
  the skill will just use regular web search (totally fine). Ask Nathaniel if you want the
  full Nimble setup.

---

## Keeping it up to date

Nathaniel improves the skill over time. To pull his latest changes:

```
cd ~/r2-skills
git pull
```

That's it. Because of the shortcut you made in setup, Claude immediately uses the
new version — nothing else to do. Do this every so often, or whenever Nathaniel
says "I updated the skill."

---

## Want a change to the skill?

Two ways:

- **Easy (recommended):** just tell Nathaniel what you want different. He edits
  the skill, commits, and pushes; you run `git pull` and you have it.
- **Yourself:** the skill is the file
  `~/r2-skills/.claude/skills/source-casting/SKILL.md`. You can open it in any
  text editor and read it — it's plain English. If you edit it and want others to
  get your change, you'd `git pull`, then commit and push:

  ```
  cd ~/r2-skills
  git pull
  git add -A
  git commit -m "describe what you changed"
  git push
  ```

  When in doubt, take the easy path and let Nathaniel handle the commit.

---

## If something looks wrong

- **Claude doesn't seem to know the skill:** run the **"Check first"** block. Do
  whatever it marks ❌ (usually re-run Step 3).
- **You're not getting recent improvements:** run `git pull` in `~/r2-skills`.
- **Anything destructive or confusing:** stop and message Nathaniel. Never delete
  the `~/.claude/skills/source-casting` link or the `~/r2-skills` folder on a
  hunch — ask first.

---

## What's in this repo (for reference)

```
.claude/skills/source-casting/SKILL.md   ← the source-casting skill (plain-English instructions)
.claude/skills/live-show-prep/SKILL.md   ← the live-show-prep skill
.claude/skills/live-show-prep/assets/    ← its design templates (brief + cheat sheet) and render.sh
.claude/skills/story-deep-dive/SKILL.md  ← the story-deep-dive skill
.claude/skills/story-deep-dive/assets/   ← its templates (field guide + dossier) and render.sh
check-skill-names.py                     ← a guardrail script that checks skill folders are named correctly
_archive/                                ← older versions, kept for reference only (not active)
README.md                                ← this file
```
