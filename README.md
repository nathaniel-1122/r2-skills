# R² Media — Claude Skills

This repository holds R² Media's custom **Claude Code skills**. Right now the
main one is **`source-casting`** — it researches and ranks interview sources for
a story and produces a CSV you import straight into Cockpit.

A "skill" is just an instruction file that teaches Claude how to do one of our
workflows the same way every time. You don't run code — you talk to Claude, and
the skill kicks in.

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

### One-time setup (copy/paste, one block at a time)

Open the **Terminal** app. Copy each block below, paste it in, press Return, let
it finish before doing the next one.

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

**Step 3 — link the skill into Claude (this is the important one):**

```
ln -s ~/r2-skills/.claude/skills/source-casting ~/.claude/skills/source-casting
```

That `ln -s` command makes a **shortcut** (a "symlink"). It tells Claude: "the
source-casting skill lives inside the r2-skills folder." Because it's a shortcut
and not a copy, whenever you update the repo (see below) Claude instantly uses
the new version — you never re-install.

**Step 4 — check it worked:**

```
ls -l ~/.claude/skills/source-casting
```

You should see a line with an arrow `->` pointing at the r2-skills folder. If you
see that arrow, you're done.

> If Step 3 says "File exists," you may already have an old copy. Stop and message
> Nathaniel rather than deleting anything — we don't want to wipe a real skill.

---

## How to use it

Open Claude Code in any project and just ask in plain English, e.g.:

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

- **Claude doesn't seem to know the skill:** confirm Step 4 above shows the arrow.
  If not, re-run Step 3.
- **You're not getting recent improvements:** run `git pull` in `~/r2-skills`.
- **Anything destructive or confusing:** stop and message Nathaniel. Never delete
  the `~/.claude/skills/source-casting` link or the `~/r2-skills` folder on a
  hunch — ask first.

---

## What's in this repo (for reference)

```
.claude/skills/source-casting/SKILL.md   ← the skill itself (plain-English instructions)
check-skill-names.py                     ← a guardrail script that checks skill folders are named correctly
_archive/                                ← older versions of the skill, kept for reference only (not active)
README.md                                ← this file
```
