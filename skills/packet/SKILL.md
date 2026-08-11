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

### Math, and anything else that needs real notation

Do not render formulas as plain text — `[[1,2],[3,4]]` is unreadable and the
student won't trust it. No MathJax or KaTeX either; the file must work offline.
Build the notation yourself:

- **Matrices and vectors** — an HTML `<table>` wrapped in a span with square
  brackets drawn as CSS pseudo-elements:
  ```css
  .m{display:inline-block;position:relative;padding:.34em .62em}
  .m::before,.m::after{content:"";position:absolute;top:0;bottom:0;
    width:.34em;border:2px solid currentColor}
  .m::before{left:0;border-right:0}   /* [ */
  .m::after {right:0;border-left:0}   /* ] */
  ```
  For augmented matrices, add a dashed `border-left` to the last column's cells.
  Label vectors (`v₁ = [...]`) rather than running three brackets together.
- **Fractions** — a flex column with a `border-bottom` on the numerator.
- **Symbols** — Unicode covers almost everything: λ ⁻¹ ᵀ ℝ ⇒ ≠ ≤ ∈ ∅ × · ᵢ ₙ.
- **Diagrams** — inline SVG, hand-written. Span as a shaded plane, eigenvectors
  as arrows that keep vs. change direction, three line-pair sketches for
  one/none/infinite solutions. A 200-byte SVG explains "dependent" better than
  a paragraph does.

**Bug that will bite you:** a `<table>` inside a `<p>` is invalid HTML. The
browser silently closes the paragraph early and the bracket spans collapse into
garbage. Use `<div>` for any block that might contain a matrix. Render the page
and look at it before handing it over.

### Stepped solutions for anything procedural

For math, physics, or any worked problem, one reveal is not enough — the whole
value is seeing where the reasoning turns. Break the solution into 3–5 steps
revealed one at a time, so the student can try, peek at step 1, try again.

Each step gets a short title naming the *move*, not the arithmetic: "Kill the
entries below the first pivot" beats "Step 1". End with the answer, then a
verification line ("check it in the original second equation") — the checking
habit is worth as much as the method.

Add a separate amber **"why"** step wherever there's a trap: why the order
reverses in `(AB)ᵀ`, why the obvious wrong approach fails, why the shortcut is
legal. That's the step people remember.

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
