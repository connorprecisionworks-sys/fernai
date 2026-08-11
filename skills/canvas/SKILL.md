---
name: canvas
description: Pull assignments, due dates, and grades out of the student's Canvas account by reading it in their already-logged-in browser, then save a snapshot the other school skills can use. Use when the user mentions Canvas, asks to sync or refresh their assignments, says "what's due", "pull my homework", "check my grades", or wants a plan built from their real coursework.
argument-hint: [optional: "grades only", "one course", or a course name]
---

# Canvas

Request: $ARGUMENTS

Reads Canvas through the student's own logged-in browser. No API token, no
password, nothing stored but a local JSON file of their coursework.

## Fast path — check for dev mode first

If `~/.claude/fern/credentials.json` exists, the student opted into API
mode. Just run the script and skip everything below — it's 3 seconds instead
of a minute:

```bash
fern sync
```

Then jump to **Report back**. If it errors, fall through to browser mode and
mention the error once.

Don't suggest setting up dev mode unprompted. Browser mode is the default for
a reason. `/canvas-dev` exists if they ask.

## Before anything

Invoke the `claude-in-chrome` skill first — the browser tools require it.

Then `tabs_context_mcp` to see open tabs. If Canvas is already open, note the
school's Canvas domain from the URL (`<school>.instructure.com`, or a custom
domain like `canvas.school.edu`). If not, ask the student for their Canvas URL
once and remember it in the snapshot file.

If the browser tools aren't available or Chrome isn't connected, skip straight
to **Fallback B** at the bottom. Don't stall.

## Pull order

Open **one new tab** and reuse it. Read pages with `read_page`, not
screenshots — it's faster and you need the text.

**1. `/grades`** — the global grades page.
One page, every active course, current grade. This also gives you the course
list and course IDs from the links. Start here; it's the cheapest call.

**2. `/courses/<id>/assignments`** for each active course.
Titles, due dates, point values, and usually submission status. Group by
"Upcoming" vs "Past" as Canvas presents it.

**3. `/courses/<id>/grades`** for each active course — only if the student
asked for grades, or if you need submission status the assignments page didn't
show. This has per-assignment scores, what's ungraded, and what's missing.

If the student named one course, do only that course. Don't crawl everything
when they asked about one thing.

**Also worth grabbing when relevant:** `/courses/<id>/assignments/syllabus`
has the schedule and grading breakdown — useful for `/plan-week`, and it tells
you what percentage of the grade each category is worth.

## Rules for reading

- **Don't hardcode expectations about layout.** Canvas installs vary and
  schools customize them. Read the page and interpret what's there.
- **Don't click anything that submits, deletes, or unenrolls.** Read-only.
  Navigation and reading only.
- **Never open a quiz or timed exam page.** Some are single-attempt and
  opening one starts the clock. If a link looks like a quiz, skip it and note
  it as unread.
- If a page needs a login, tell the student to log in and say when they're
  done. Don't attempt to enter credentials.
- Watch for concluded/past-term courses in the list and exclude them.
- Close the tab when finished.

## Save the snapshot

Write to `~/.claude/fern/snapshot.json`:

```json
{
  "pulled_at": "2026-08-10T21:45:00-04:00",
  "canvas_url": "https://school.instructure.com",
  "courses": [
    {
      "id": "12345",
      "name": "BIOL 201",
      "current_grade": "88.4%",
      "assignments": [
        {
          "title": "Lab 4 Report",
          "due": "2026-08-14T23:59:00-04:00",
          "points": 50,
          "status": "not_submitted",
          "score": null,
          "url": "https://school.instructure.com/courses/12345/assignments/98765"
        }
      ]
    }
  ],
  "unread": ["Quiz 3 (skipped — timed quiz)"]
}
```

`status` is one of: `not_submitted`, `submitted`, `graded`, `missing`, `late`,
`unknown`. Use `unknown` rather than guessing.

Run `date -Iseconds` for `pulled_at`. Create the directory if needed.

## Report back

Short. Not the whole JSON.

```
Pulled 5 courses, 23 assignments.

OVERDUE (2)
  BIOL 201 — Lab 3 Report        was due Aug 7    50 pts   missing
  HIST 110 — Reading response 4  was due Aug 8    10 pts   missing

DUE THIS WEEK (4)
  CHEM 240 — Problem set 5       Wed 11:59pm      40 pts
  ...

GRADES
  BIOL 201  88.4%   CHEM 240  91.0%   HIST 110  76.2%  <- lowest
```

Then one line: what looks most urgent, and offer `/triage` to rank it or
`/plan-week` to schedule it.

If something's overdue, say it plainly and first. Don't bury it.

## Fallback A — no browser tools, but they have the Canvas calendar feed

Canvas gives every student a personal calendar feed URL: **Calendar → Calendar
Feed** (bottom right), a link ending in `.ics`. Ask them to paste it. Fetch it
and parse due dates and titles.

Gives you dates and names only — no points, no grades, no submission status.
Fill those fields with `null` / `unknown` and say so in the report. It's still
enough for `/triage` and `/plan-week` to work.

## Fallback B — paste

Ask them to open Canvas, select the assignments page (or the dashboard "Coming
Up" list), copy, and paste it in. Messy paste is fine — parse it into the same
snapshot format.

This always works and takes 30 seconds. Offer it immediately rather than
fighting a broken browser connection.

## Refreshing

If `snapshot.json` exists and is under ~6 hours old, use it and say when it
was pulled rather than re-scraping. Otherwise re-pull. If the student says
"refresh" or "resync," always re-pull regardless of age.
