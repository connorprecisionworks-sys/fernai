---
name: packet
description: Build a study packet from the teacher's own materials - slides, study guide, past problem sets, graded work - as a single self-contained HTML file built around active recall. Use when the user has a test or quiz coming, asks for study notes, a study guide, flashcards, review material, or says they don't know what to study.
argument-hint: [course + what it covers, e.g. "chem 240 midterm, ch 1-7"]
---

# Packet

Target: $ARGUMENTS

Builds a study packet the student will actually finish. The output is a single
self-contained HTML file: mostly questions, answers hidden, keyboard-driven,
built from **their teacher's materials** rather than from generic knowledge.

Two rules govern everything here:

1. **Recall, not review.** Rereading notes feels like studying and isn't. The
   packet is a stack of questions. Any prose that isn't answering a question
   has to justify its existence.
2. **It has to hold attention for 20 minutes.** One card on screen at a time.
   Nothing that looks like a textbook page. If it scrolls like a wall, it
   failed and they'll close it.

## Step 1 — Get the teacher's materials

This is what makes the packet worth anything. Generic notes on "titration" are
worthless; notes built from the professor's slide deck and the questions they
already got wrong are not.

Gather, in priority order:

1. **The study guide or exam blueprint**, if one exists. This is the answer key
   to what matters. Everything else is guessing.
2. **Their graded work** — problem sets, quizzes, labs with scores. The
   questions they lost points on are the highest-value cards in the packet, by
   a wide margin. Get the actual returned work, not just the score.
3. **Lecture slides / posted notes** for the covered range.
4. **Past exams or practice exams**, if posted.
5. **The syllabus** — tells you the grade weighting and often the topic list.

Where to get them:

- **Canvas** — use the `canvas` skill's browser mode. Useful pages:
  `/courses/<id>/files`, `/courses/<id>/pages`, `/courses/<id>/modules`, and
  `/courses/<id>/assignments/syllabus`. Graded work with feedback is under
  `/courses/<id>/grades` → click into the submission.
  **Never open a quiz or timed exam page** — some are single-attempt.
- **Ask them to drop files in.** Fastest path if they already have the PDFs or
  slides. Say exactly what would help most: "the study guide and your last
  graded problem set."
- If they have nothing, say so plainly before building: "Without the slides or
  a study guide, this is my best guess at a standard CHEM 240 midterm — it'll
  be decent but not targeted. Worth 2 minutes to grab the slide deck first?"

Never invent a fact, a formula, a date, or a citation. If a slide is unreadable
or you're unsure, mark the card `[CHECK THIS]` rather than guessing.

## Step 2 — Find where the points are actually leaking

Before writing a single card, work out what they're bad at. Sources:

- Wrong answers on returned work — the single best signal
- Topics with the most lecture time or the most study-guide real estate
- Anything the professor repeated or flagged
- Their own answer to: "what do you feel worst about?"

Rank topics. Say the ranking out loud to them in one or two lines, then build
the packet weighted to the top of it. A packet with equal coverage of
everything is a packet that wastes their 20 minutes.

## Step 3 — Build the cards

**Card types**, in rough order of value:

- **Recall** — "What does an increase in temperature do to Ke, and why?"
- **Worked problem** — the kind that will be on the exam, with a full solution
  including the reasoning for each step, not just the algebra
- **Discrimination** — "SN1 or SN2? Tertiary substrate, polar protic solvent."
  These catch the confusions that lose the most points
- **Their actual mistake** — reproduce a question they got wrong, with what
  went wrong and the correction. Mark these clearly; they're the priority
- **Fact/formula** — the smallest category. Only what must be memorized

**Writing rules:**

- One idea per card. If the answer has three parts, it's three cards.
- Answers are short. Three lines, not a paragraph.
- Every worked problem shows *why*, including why the obvious wrong approach is
  wrong.
- Use the professor's notation and vocabulary, not the textbook's, when they
  differ. The exam will use the professor's.

**Sizing:**

- **Core set: 12–18 cards.** This is the 20-minute version. Weighted hard
  toward their weak topics.
- **Full set: 30–45 cards.** The hour version.
- Beyond ~45 the packet becomes a thing they abandon. If the material is
  bigger than that, build two packets and say so.

## Step 4 — The file

Single self-contained HTML — inline CSS and JS, no CDN, no external assets so
it works offline. Save it somewhere obvious and tell them the path.

Required behavior:

- **One card at a time.** Big question, generous whitespace, nothing else on
  screen.
- **Space or click reveals the answer.** Arrow keys / `J`/`K` move.
- **After reveal: "got it" / "missed it."** Missed cards return later in the
  session. This loop is the whole point — it's spaced repetition compressed
  into 20 minutes.
- **Progress indicator** — "7 / 16" and a thin bar. People finish things with
  visible progress and abandon things without it.
- **Mode toggle at the top: `20 min` / `full`.** Defaults to 20 min. The
  20-minute mode serves only the core set.
- **A "brain dump" panel** at the end: every formula, date, and definition on
  one screen, the thing they'd want to scribble down the second the exam
  starts.
- **Ends with a score** — "you missed 4: [topics]" — and names what to do
  next with the specific 20 minutes remaining.

Style it dark, high contrast, big type (18px+ body, 24px+ questions). It gets
read on a laptop at 11pm.

**Do not use localStorage or sessionStorage** — keep state in memory. Say
plainly that closing the tab loses progress.

## Step 5 — Hand it off

Tell them, in about four lines:

- Where the file is and that it opens in any browser
- What the core set is weighted toward, and why — name the topics
- The honest floor: "20 minutes covers X and Y, which is where you're actually
  losing points. The other two topics need another 40."
- What it *doesn't* cover, if you cut something

Then offer the follow-up that fits — usually `/tutor` on whichever topic they
miss the most, or `/cram` if the exam is imminent.

## When the exam is in a few hours

Skip the polish. Cut to 10 cards on the single highest-value topic, plus the
brain dump. Say what you cut. Then hand off to `/cram`, which is built for the
clock.
