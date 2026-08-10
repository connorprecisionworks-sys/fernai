# Back to School — Claude Skills for Students

Nine skills that turn Claude into something actually useful during a semester.
Install once, then type `/due`, `/triage`, `/cram` and go.

It reads your real Canvas assignments, so the plans are about your actual
coursework — not a list you had to type out.

No fluff, no "as an AI language model." Each one is a procedure someone who's
good at that thing would actually follow.

| Command      | What it does |
|--------------|--------------|
| `/canvas`    | Pulls your assignments, due dates, and grades out of Canvas via your logged-in browser. No token, no password. |
| `/due`       | "What's due?" in five seconds. Overdue first, then the week. Nothing else. |
| `/triage`    | Your whole workload → one ranked do-this-next list. Tells you when it doesn't fit. |
| `/plan-week` | A weekly schedule with slack built in, so it survives past Tuesday. |
| `/tutor`     | Diagnoses what you actually don't understand, then teaches that — by asking, not lecturing. |
| `/cram`      | Emergency exam prep. Triages material, drills you, quizzes you hard, tells you to sleep. |
| `/draft`     | Gets you off the blank page: outline, then a draft you rewrite. Ships with an integrity handoff. |
| `/email`     | Emails to professors, TAs, advisors that get a yes. Extensions, grade reviews, rec letters. |
| `/learn`     | A brutal, project-first plan for learning a new skill on a deadline. |

## Install

### Option A — copy the skills (simplest, gives you clean `/tutor`)

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/back-to-school-skills.git
cd back-to-school-skills
./install.sh
```

Restart Claude Code. Type `/` and they're there.

Manual version, if you'd rather see what's happening:

```bash
cp -R skills/* ~/.claude/skills/
```

### Option B — install as a plugin

```
/plugin marketplace add YOUR-GITHUB-USERNAME/back-to-school-skills
/plugin install back-to-school@back-to-school-skills
```

Commands are namespaced this way: `/back-to-school:tutor`.

### Option C — one skill only

Copy the folder you want:

```bash
cp -R skills/cram ~/.claude/skills/
```

### Not using Claude Code?

Every skill is just a markdown file. Open `skills/<name>/SKILL.md`, paste the
body into any chat with Claude (or another model), add your specifics, go.

## Usage

Start of semester, run once:

```
/canvas
```

It opens a tab in your browser, reads the Canvas you're already logged into,
and saves everything to `~/.claude/canvas/snapshot.json`. After that:

```
/due                    what's overdue and what's this week
/triage                 ranked plan from your real assignments
/plan-week              a schedule built around your real deadlines
/canvas refresh         resync after new stuff gets posted
```

Everything else takes context on the same line:

```
/tutor eigenvectors, I get the definition but not why anyone cares
/cram orgo midterm, 6 hours from now, ch 1-7, haven't started
/email need a 3-day extension on my BIOL 201 lab, prof is strict
/learn react, 6 weeks, ~8hrs a week, want to ship a real app
```

Claude will also pull these up on its own when the conversation matches — you
don't have to remember the command.

## How the Canvas part works

**No API token. No password. No credentials anywhere.**

`/canvas` drives the Chrome you're already signed into, opens your Canvas
pages, and reads them the way you would. It touches four pages:

| Page | What it gets |
|------|--------------|
| `/grades` | every course + your current grade, in one shot |
| `/courses/<id>/assignments` | titles, due dates, point values |
| `/courses/<id>/grades` | scores, what's ungraded, what's missing |
| `/courses/<id>/assignments/syllabus` | schedule and grade weighting |

It's read-only. It won't submit, delete, or unenroll anything, and it will
**never open a quiz or timed exam page** — some are single-attempt and opening
one starts your clock.

Requires the [Claude in Chrome](https://www.anthropic.com/claude/chrome)
extension. Two fallbacks if you don't have it or it breaks:

- **Calendar feed** — Canvas → Calendar → "Calendar Feed" (bottom right) gives
  you a personal `.ics` URL. Paste it. Gets due dates and titles, no grades.
- **Paste** — copy your assignments page and paste it in. Always works, takes
  30 seconds.

Your snapshot lives at `~/.claude/canvas/snapshot.json` on your own machine.
Nothing is uploaded anywhere. Delete the file and it's gone.

Other LMS? The `canvas` skill is a page-reading procedure, not Canvas-specific
code — point it at Blackboard, Moodle, or Brightspace and it mostly works. PRs
welcome for proper versions.

## A note on `/draft`

`/draft` produces drafts, and every draft it produces ends with a required
handoff block: verify the citations, rewrite it in your own words, check your
syllabus. Submitting AI text as your own is an integrity violation at most
schools and it reads as AI to anyone who knows your writing.

The point of the skill is momentum and structure. The words should end up
being yours. `/draft` is at its best reviewing *your* rewrite against the
rubric — do that part.

## Repo layout

```
back-to-school-skills/
├── skills/
│   ├── canvas/SKILL.md      <- pulls data, writes the snapshot
│   ├── due/SKILL.md
│   ├── triage/SKILL.md
│   ├── plan-week/SKILL.md
│   ├── tutor/SKILL.md
│   ├── cram/SKILL.md
│   ├── draft/SKILL.md
│   ├── email/SKILL.md
│   └── learn/SKILL.md
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── install.sh
└── LICENSE
```

## Making your own

A skill is a folder with a `SKILL.md` in it. Frontmatter, then instructions:

```markdown
---
name: my-skill
description: What it does and when Claude should reach for it.
argument-hint: [what to pass in]
---

Instructions. Use $ARGUMENTS for whatever the user typed after the command.
```

Drop it in `~/.claude/skills/my-skill/` and it's a `/my-skill` command. The
`description` is what Claude reads to decide whether to auto-trigger it, so
write it as *when to use this*, not *what this is*.

## Contributing

PRs welcome, especially:

- Blackboard / Moodle / Brightspace versions of `/canvas`
- Subject-specific tutors (`/tutor-calc`, `/tutor-orgo`)
- `/read` — getting through dense assigned reading
- `/office-hours` — what to actually ask when you get there
- `/grade-check` — where the points went and what's still recoverable

Keep the house style: short, direct, procedural. No motivational filler.

## License

MIT. Fork it, rename it, ship it.
