---
name: triage
description: Turn a pile of assignments into a ranked do-this-next list. Use when the user is overwhelmed, has many deadlines, asks what to work on first, says they're behind, drowning, don't know where to start, or dumps a list of homework at you.
argument-hint: [paste your assignments, or say "ask me"]
---

# Triage

Input: $ARGUMENTS

Goal: in under five minutes of the student's time, produce one ranked list
where the top item is unambiguously the right thing to open right now.

## Step 1 — Get the data (fast)

**Check `~/.claude/fern/snapshot.json` first.** If it exists, that's the
assignment list — use it and skip the interview. Mention when it was pulled;
if it's more than a day old, run the `canvas` skill to refresh. If the file
doesn't exist and they have Canvas, offer `/canvas` — it takes about a minute
and beats typing everything out.

Canvas won't know about everything (reading, group work, job shifts,
non-Canvas classes), so always ask: "anything not in Canvas?"

If they pasted a list, use it. If not, ask for a brain dump in one message:
every assignment, exam, and obligation, however messy. Do not interview them
item by item — that's the thing they're too overwhelmed to do.

For each item you need four fields. Infer what you can, ask only for what's
missing and actually load-bearing:

- **Due** — when
- **Weight** — % of grade, or high/med/low
- **Effort** — hours remaining, their estimate
- **Done** — % complete

If they can't estimate effort, ask: "if you sat down right now with no
distractions, how long?" Then multiply by 1.5. Students underestimate.

## Step 2 — Score

Sort by this, in order:

1. **Hard blockers first.** Anything with a hard cutoff in <24h that isn't
   done. Portal closes, exam happens, group deadline others depend on. These
   jump the queue regardless of weight.
2. **Points per hour.** `(weight × remaining work) ÷ hours needed`. A 25%
   paper barely started beats a 5% quiz you'd ace anyway.
3. **Unblocks other people or other work.** Group work you owe, lab data
   someone needs, a reading required for tomorrow's problem set.
4. **Cheap wins.** Anything worth points that takes under 20 minutes. Do these
   in the gaps, not in prime focus time.
5. **Slow burners.** Things that need calendar time, not clock time — drafts
   that need to sit, reading that needs days, office hours that only exist on
   Tuesday. Start these early even though they're not urgent.

## Step 3 — Reality check the math

Add up the hours. Compare to actual hours available before each deadline
(subtract sleep, class, work, commute — be honest, not aspirational).

If it doesn't fit, say so directly. Do not produce a plan that requires a
28-hour day. Then give the triage options, ranked:

- What to deliberately do at 70% instead of 100% (name the specific item and
  what "70%" means for it)
- What's worth emailing for an extension — with the actual expected value
  ("this is 30% of your grade and you have 4 hours; a 2-day extension is worth
  more than anything else you could do tonight")
- What to strategically skip and eat the loss on — compute the grade cost so
  it's a decision, not a failure

## Output format

Plain lines, no code fences, no tables — this gets read in a terminal. **A
blank line between every group.** Density is what makes triage unreadable, and
an unread plan is the same as no plan.

    NOW
      45m   CHEM 240 PS3 — due tomorrow 11:59pm, 40 pts, not started

    NEXT
      20m   CHEM lab safety module — missing since Aug 7, click-through

    THIS WEEK
      Thu   MATH HW2 + Quiz 1, HIST reading response
      Fri   ENGL memo — 60 pts, the big one
      Sat   BIOL Lab 2

    SKIP
      HIST term paper proposal — not due till Aug 29, costs nothing to wait

**Time goes at the front of the line, never the end.** A terminal wraps long
lines, and a trailing "— 45m" orphans onto its own row where it reads as
noise. Keep each item under about 65 characters so it never wraps at all.

Two or three items per group, maximum, and **at most four groups**. If a group
needs six items you are listing rather than triaging — merge them into one line
and move on. NOW should hold exactly one thing.

**Estimate honestly but not perfectionistically.** Time to done and submitted
at a solid B, not polished: a lab writeup is 45 minutes, a discussion post is
15, a problem set you follow is an hour. Inflated estimates are why students
bounce off plans.

Then one line: **what tonight actually costs** — NOW plus NEXT only, which
should land in the 2–4 hour range. Never report a total for the week; it is
demoralising and it is not a number anyone acts on. If the week genuinely does
not fit, say so in one sentence and name what gets cut.

Then: **the single next physical action** — not "start the essay" but "open a
doc and write the thesis sentence." The first action must be small enough that
refusing it feels silly.

Stop there. No pep talk.
