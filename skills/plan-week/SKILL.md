---
name: plan-week
description: Build a realistic weekly schedule around classes, work, and deadlines - one that survives contact with an actual week. Use when the user wants a study schedule, a weekly plan, help with time management, asks how to fit everything in, or is setting up a new semester.
argument-hint: [your classes, work hours, and what's due this week]
---

# Plan Week

Input: $ARGUMENTS

**Check `~/.claude/canvas/snapshot.json` first** — if it's there, that's the
deadline list, and the syllabus data tells you what each thing is worth. Refresh
with the `canvas` skill if it's stale. If it doesn't exist and they use Canvas,
offer `/canvas`. Then ask what Canvas doesn't know: work shifts, practice,
commute, non-Canvas classes.

Most student schedules fail for one reason: they're built for an idealized
person with no friction. This one is built with slack in it.

## Step 1 — Fixed blocks first

Get everything that cannot move:

- Classes, labs, discussion sections
- Job / practice / rehearsal / commitments
- Commute
- Sleep — 8 hours, blocked, non-negotiable. Do not let them plan on 5.
- Meals — yes, actually block them

What's left is the real budget. Say the number out loud: *"You have 23 workable
hours this week."* Students consistently believe they have double what they do,
and every bad plan starts there.

## Step 2 — Subtract friction

Multiply the remaining hours by **0.7**. That's the honest number.

The other 30% is transitions, restarting after interruptions, the thing that
takes longer than expected, and being a human. Planning at 100% capacity
guarantees failure by Wednesday and makes them feel like the failure is theirs.

## Step 3 — Match work to energy

Ask when they actually focus well. Then:

- **Peak hours** → the hardest thing. Problem sets, writing, new material.
  Protect these ruthlessly and never spend them on email or busywork.
- **Medium hours** → reading, review, revision
- **Dead hours** → admin, printing, formatting, submitting, flashcards on the
  bus

The most common mistake is spending peak hours on easy tasks because they feel
productive, then hitting the hard thing at 11pm with nothing left.

## Step 4 — Place the work

Rules for placement:

- **Deep work in 90-minute blocks**, ideally 2/day max. More than that isn't
  real.
- **Right after class** is the highest-return study time in the week — the
  material is still warm. Use the gaps between classes for this.
- **Reading gets a block, not "whenever."** Unscheduled reading never happens.
- **Start big things early in the week.** Anything needing a draft, feedback,
  office hours, or a library book must begin Monday or Tuesday.
- **Leave Friday afternoon and one weekend block empty.** That's the buffer
  everything overflows into. A plan with no buffer is a plan with one bad day
  of life left in it.
- **Batch similar work.** All reading together, all problem sets together.
  Context switching costs more than students think.

## Step 5 — Checkpoints

- **Sunday, 15 min:** plan the week. Look at deadlines two weeks out, not one.
- **Wednesday, 5 min:** is this working? Move what slipped now, not Friday.
- **Friday:** what's actually done, what rolls over.

## Output

A day-by-day grid with named blocks and specific tasks:

```
MON
  9–10:30   CHEM lecture
  10:45–12  [PEAK] Chem problem set 4 — through Q6
  12–1      lunch
  ...
```

Not "study." Every block names the actual task and where to stop.

Then, below the grid, three lines:

- **Total planned work hours** vs. what's needed for the deadlines
- **The buffer blocks** — labeled, so they know what to sacrifice first
- **The one thing that must happen this week**, even if everything else slips

## If it doesn't fit

Say so immediately and clearly. Do not compress sleep, do not shrink task
estimates, do not produce a fantasy grid to be encouraging.

Instead: name what gets dropped, what gets done at 70%, and what's worth an
extension request. A true "this doesn't fit, here's the least-bad version" is
more useful than an optimistic schedule that collapses Tuesday.
