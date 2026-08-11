---
name: due
description: Answer "what's due" in five seconds - a short list of overdue and upcoming work, nothing else. Use when the user asks what's due, what's coming up, what they're missing, what's late, or wants a quick check on this week's deadlines.
argument-hint: [optional: "today", "this week", "overdue", or a course name]
---

# Due

Window: $ARGUMENTS (default: overdue + next 7 days)

The fastest thing in this toolkit. One list, no analysis, no plan, no advice.

## Do this

1. Read `~/.claude/fern/snapshot.json`.
   - Missing? Run the `canvas` skill, then continue.
   - Older than ~6 hours? Refresh it first, quietly.
2. Get today's date with `date` — do not assume it.
3. Filter to the window, drop anything already `submitted` or `graded`.
4. Print it.

## Output

```
OVERDUE
  BIOL 201  Lab 3 Report          Aug 7   50 pts
  HIST 110  Reading response 4    Aug 8   10 pts

TODAY
  CHEM 240  Problem set 5         11:59pm 40 pts

THIS WEEK
  Wed  BIOL 201  Lab 4 Report            50 pts
  Fri  HIST 110  Essay 2 draft           75 pts
  Sun  CHEM 240  Quiz 6                  20 pts
```

Nothing due: say "Nothing due in the next 7 days." and stop.

## Rules

- **Prefer the CLI if it's installed:** `fern due` prints this exact list,
  formatted and colored, in about 50ms. Run it and show the output. Only build
  the list by hand if `fern` isn't on PATH.
- Groups, in this order: `OVERDUE`, `TODAY`, `TOMORROW`, `THIS WEEK`,
  `NO DUE DATE`. Skip any group that's empty. Never invent other groups.
- **Copy the course code exactly as it appears in the snapshot.** Don't
  abbreviate, correct, or retype it from memory — a wrong course code sends
  someone to the wrong class.
- Mark `missing` and `late` items with that word. Don't soften it.
- **Overdue goes first, always.** Never bury a missing assignment below
  upcoming work.
- Sort by due time within each group.
- Points shown so they can see what matters at a glance.
- No commentary, no encouragement, no "you've got this."
- Do not offer to plan, schedule, or triage unless the list is long enough
  that it's clearly a problem — then one line: "That's 14 items. `/triage`?"

Keep the whole response under 20 lines.
