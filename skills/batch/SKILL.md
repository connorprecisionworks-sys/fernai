---
name: batch
description: Work through everything at once - draft every upcoming assignment in parallel, gathering what's needed from Canvas first and asking the student only for what genuinely can't be found. Use when they say draft everything, do all my assignments, knock out my work, catch me up, handle my week, or ask for several deliverables in one message.
argument-hint: [optional: "just the writing", "only what's overdue", a course name]
---

# Batch

Scope: $ARGUMENTS

The student asked for everything. Give them everything — started, in parallel,
without a negotiation first.

## Two rules govern this whole skill

**Drafts go in files, never in the chat.** Write each one to
`~/Desktop/fern-drafts/<COURSE> - <assignment>.md` as it finishes. Never print
a draft body, an outline, or a memo into the terminal — six drafts pasted into
a chat window is unreadable, unsavable, and the exact wall of text this toolkit
exists to prevent. The chat shows progress and questions only.

**Act. Do not offer.** "Draft my assignments" is the instruction, not a request
for a plan to draft them. Never reply with what you *could* do, never ask
whether to proceed, never tell them to run `/draft`. Say what you're starting,
then start.

The only questions you may ask are ones where **the work genuinely cannot
continue** without the answer, and only after you have tried to find it
yourself. Every avoidable question is a failure of this skill.

## Step 1 — Build the work list, silently

From `~/.claude/fern/snapshot.json`, take everything not `submitted` or
`graded`, due within ~10 days or already overdue. Sort by due date.

Split into three buckets:

- **Draftable** — writing, labs, memos, discussion posts, responses, proposals.
  A draft saves real time.
- **Not draftable** — problem sets, quizzes, exams, click-through modules.
  Drafting is meaningless. Say so in one line and move on; don't spawn an agent.
- **Skip** — worth few points in a class already above 90, and due more than a
  week out.

## Step 2 — Find the inputs yourself, before asking for anything

Every snapshot assignment carries a `prompt` field with the instructions Canvas
had. **Read it.** This is the single biggest source of unnecessary questions —
the prompt is nearly always already there.

If `prompt` is empty for something you're drafting, **go and get it** — do not
ask permission to look. "Tell me to pull it from Canvas myself" is not a
question, it is a task you were already given. Try, in order:

1. Open the assignment's `url` and read the page (`canvas` skill, browser mode)
2. Check the course syllabus page and Files for the assignment sheet
3. Look at how the same series was set up — Lab 2 usually mirrors Lab 1

Only after all three come up dry does it become a question for the student.

**What is genuinely worth asking for:** their own data (lab measurements,
observations, interview notes), a personal position where the assignment
demands one, a file that only exists on their laptop, and a format choice.
Nothing else.

**What is not worth asking:** anything on Canvas, anything you can infer from a
sibling assignment, or their "preference" on things you should just decide.
Structure a lab report the standard way and let them change it.

## Step 3 — Fan out

Spawn one subagent per draftable item, all at once, using the Task tool. Each
gets: the assignment title, course, due date, point value, the full prompt
text, the rubric if you have one, and any student input already collected.

Tell each subagent to follow the `draft` skill — including its integrity
handoff, which is not optional — and to return the finished draft plus a list
of anything it genuinely could not proceed without.

While they run, say once what's in flight. One line per item, no commentary:

    Drafting 4 in parallel.

      BIOL 201  Lab 1 writeup          50 pts   overdue
      ENGL 205  Memo assignment        60 pts   Fri
      HIST 110  Reading response 3     15 pts   Wed
      BIOL 201  Discussion board wk3   10 pts   Mon

    Skipping: CHEM PS3, MATH HW2, Quiz 1 — problem sets, nothing to draft.

## Step 4 — One question at a time

Collect every question the subagents raise, drop the duplicates, drop anything
you can still answer yourself. Then ask what remains **one at a time**, never
as a list. A wall of questions is the thing this skill exists to prevent.

Use exactly this shape:

    [1/3]  BIOL 201 · Lab 1: Microscopy writeup · due Aug 7

           Your microscopy observations — what you saw at 40x, 100x and
           400x. Rough notes are fine.

    ❯

When they answer: acknowledge in **one word or two**, then immediately show the
next question. No "great, thanks, that helps." Just:

    ✓ got it

    [2/3]  ENGL 205 · Memo assignment · due Fri Aug 14
    ...

For anything with a small set of sensible answers, offer numbers rather than
open text — it is faster to press 2 than to type a sentence:

    [3/3]  CHEM 240 · Midterm study material · Aug 22

           How do you want it?

             1  Flash cards      question on one side, answer hidden
             2  Practice quiz    timed, scored, tells you what you missed
             3  Study packet     both, plus a one-page brain dump
             4  Summary sheet    just the notes, no self-testing

    ❯ 2

If an answer is missing or they say "skip", draft it anyway with a clearly
marked `[YOUR DATA HERE — I couldn't find this]` placeholder. A draft with one
hole beats no draft.

## Step 5 — Deliver

The files are already written (see the rule at the top). All that goes in the
chat is the manifest — no prose, no draft content, no tables:

    Done. ~/Desktop/fern-drafts/

      BIOL 201 - Lab 1 writeup.md          4 pages   your data slotted in
      ENGL 205 - Memo assignment.md        1 page    2 spots need your call
      HIST 110 - Reading response 3.md     500 wds   ready
      BIOL 201 - Discussion wk3.md         150 wds   ready

    Every one needs a rewrite pass in your own words before you submit —
    each file says so at the bottom.

    Start with the BIOL lab. It's the 50 pts and it's already overdue.

Then stop. One closing line naming what to open first. No summary of what you
did, no offer of further help.
