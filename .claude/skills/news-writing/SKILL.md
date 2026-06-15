---
name: news-writing
description: The craft and quality standard for writing and editing a news story or research note. Defines structure (lede, nut graf, inverted pyramid), the anti-AI-slop banned list, headline rules, the editor self-pass, and the quality bar a piece must clear before submission. Use whenever drafting or editing any article. This is the generic craft layer; crypto-news-domain layers domain judgment on top of it, and verifiable-claims supplies the number format it relies on.
source: OCCA (internal)
installed: 2026-06-07
---

# News writing

This skill is the craft. `verifiable-claims` governs the numbers and
`crypto-news-domain` governs what they mean; this one governs how the
piece is built and how it reads. A story can be perfectly accurate and
still be unpublishable because it reads like generated filler. This
skill is what keeps that from happening.

You are both writer and editor. Draft, then turn on the editor and cut.
The editor is the more important half.

## 1. Order of work

Do these in order. They do not reorder.

1. **Verify first.** Gather data with tools, build the
   `<!--occa:claims-->` block per `verifiable-claims`. The block exists
   before the prose does.
2. **Write from the block.** Every factual sentence rests on something
   you verified. If a sentence states a fact you cannot point to in the
   block or a tool result, it does not get written.
3. **Edit against this skill.** Run the anti-slop pass and the editor
   pass below before you submit. The first draft is never the one you
   ship.

The hard rule: no factual sentence without a source behind it. A
sentence of analysis or interpretation is allowed, but it must read as
clearly your read of the data, not as a smuggled fact.

**Corroboration.** A routine fact from a primary source needs that one
source. A claim that is contested, surprising, market-moving, or rests
on an unnamed source needs at least two independent sources before it
ships — independent meaning neither derives from the other (two articles
citing the same tweet are one source, not two). No second source? Then
the claim does not run as fact: either cut it, or report the dispute
itself with explicit attribution ("X claims..., unconfirmed"). A rumor
is verified or knocked down — it is never repeated as fact.

## 2. Structure

**Lede.** Lead with the news or the sharpest finding. Never open with
broad context ("In the rapidly evolving world of..."). The first
sentence states what happened and why it is worth a reader's time.

**Nut graf.** By the second or third paragraph, one sentence states why
this story matters now. If you cannot write that sentence, you do not
have a story yet.

**Inverted pyramid.** Most important fact first, then descending. A
reader who stops after two paragraphs should still have the core. Detail
and nuance come after, not before.

**One idea per paragraph.** Each paragraph advances the argument. Apply
the reshuffle test: if you can swap two body paragraphs without breaking
the piece, you have written a list, not an argument. Fix the structure.

## 3. The anti-slop pass

These are the statistical fingerprints of generated text. Cut them. They
are signals, not proof, but in your own draft they are almost always
worth removing.

**Banned vocabulary (always cut):** delve, leverage, robust, seamless,
utilize, paradigm, cutting-edge, game-changer, deep dive, unpack,
harness, best practices, thought leadership. Replace with the plain
word or rewrite the sentence.

**Cut in clusters (fine alone, slop in groups):** navigate, foster,
elevate, unleash, empower, bolster, ecosystem, myriad, plethora,
transformative.

**Sentence patterns to delete:**

- Contrastive frame: "It's not X, it's Y" / "No X. No Y. Just Z."
- Rhetorical opener: "What does this mean for builders?" / "Why should
  you care?" If you know the answer, state it.
- Engagement hook: "The catch?" / "But here's the thing." / "The best
  part?"
- "Let's" transition: "Let's explore," "Let's dive in," "Let's break
  this down."
- Hedge stack: "could potentially eventually." Each hedge cancels the
  next and leaves no claim.
- Generic closer: "only time will tell," "the future looks bright," "one
  thing is certain." Delete the last paragraph if it does this.
- Confidence calibration: "it's worth noting," "interestingly,"
  "notably," "importantly." Let the fact carry its own weight.

**Structural tells to fix:**

- Vague attribution: "experts say," "studies show," "research suggests"
  with no name. Name the source or cut the claim.
- Synonym cycling: rotating developers / engineers / builders /
  practitioners in one passage. Repeat the right word instead.
- Significance inflation: "pivotal moment," "watershed," "marks a turning
  point" on a routine event. State what happened; let the reader judge.
- Real/actual inflation: "real utility," "genuine demand" with no stated
  contrast. Drop the intensifier, add the specific.

**Deterministic limits (these get checked, not argued):**

- Em dashes: at most 1 per 1,000 words. Use periods, commas, colons.
- Vary sentence length. If most sentences are 15 to 25 words, add short
  ones (3 to 8) and let one run long. Fragments are allowed.
- Vary paragraph length. Not every paragraph is three to five sentences.
  One-sentence paragraphs are allowed for a single hard point.

## 4. Headlines

Accurate first, then sharp. Never clickbait.

- **Specific over vague.** If the headline could sit on ten other
  stories, it is too vague. Put the number, the name, or the finding in
  it.
- **Active voice.** Subject does the action. "Solana fees climbed 40%,"
  not "A 40% climb was seen in Solana fees."
- **Sentence case**, not Title Case. Spell out one through nine, digits
  for 10 and up.
- **Under ~70 characters** where possible.
- **No hype verbs:** no "revolutionize," "skyrocket," "explode," "soar."
  Report the move in plain words and let the number do the work.

## 5. The editor pass

Before you submit, stop being the writer and read as a demanding editor.
Two layers, in order. If either fails, revise and read again. Do this up
to three times.

**Layer 1, integrity:**

- Is there a factual sentence with no source behind it? Cut or source it.
- Is any number in the prose missing from the `<!--occa:claims-->` block?
- Is any attribution unnamed?
- Is any contested, surprising, or single-source claim presented as
  settled fact without a second independent source?
- Does any claim state causation where the data only shows correlation?

**Layer 2, prose:**

- Run the section 3 banned list. Remove every hit.
- Is there a lede and a nut graf? Is the structure inverted pyramid?
- Are the verbs strong, or is it "serves as / features / boasts" filler?
- Does every paragraph add information, or is some of it restating?

Say what you changed. If a pass finds nothing, say the draft is clean.

## 6. Voice

The banned list removes bad writing. It does not supply a voice. Voice
comes from the house examples appended to this skill and from these
principles:

- **Be concrete.** Numbers, names, dates, specific protocols. Specifics
  are the difference between writing and filler.
- **Have a position.** State what the data plausibly means and what would
  confirm or refute it. Flat neutrality reads as generated.
- **Report dramatic numbers flatly.** A 77% surge gets the same even tone
  as a 2% drift. The restraint is the voice. (See `crypto-news-domain`.)
- **Earn emphasis.** Do not tell the reader something is interesting.
  Make it interesting and let them notice.

> House voice exemplars: to be added. Paste two to three Crypoch articles
> that represent the target voice (and one that does not, labeled as the
> anti-example). Until then, the four principles above are the standard.

## 7. The quality bar

A piece clears the bar only if it passes all six. The first four are
mechanical checks; the last two are editorial judgment. Score every
piece so quality is tracked over time, not felt.

| Dimension | Check | Pass |
|---|---|---|
| Sourcing | every factual sentence has a verified claim behind it | 100% |
| Attribution | count of unnamed "experts say" | 0 |
| Anti-slop | banned-list hits, by severity | 0 always-cut, ≤ 2 cluster |
| Readability | em dashes per 1,000 words; sentence-length variety | em dashes ≤ 1; varied |
| Newsworthiness | is it large, sustained, or divergent (per crypto-news-domain)? | yes to at least one |
| Clarity | lede present, nut graf present, inverted pyramid | all three |

A piece that fails any mechanical check goes back automatically. A piece
that fails an editorial check goes back to the editor pass.
