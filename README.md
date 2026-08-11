# Back to School — Claude Skills for Students

Eleven skills plus a CLI that turn Claude into something actually useful during a semester.
Install once, then type `/due`, `/triage`, `/cram` and go.

It reads your real Canvas assignments, so the plans are about your actual
coursework — not a list you had to type out.

No fluff, no "as an AI language model." Each one is a procedure someone who's
good at that thing would actually follow.

| Command      | What it does |
|--------------|--------------|
| `/canvas`    | Pulls your assignments, due dates, and grades out of Canvas via your logged-in browser. No token, no password. |
| `/canvas-dev`| Opt-in: direct Canvas API access with your own token. Faster, but you accept the risks. |
| `/packet`    | Builds a study packet from your teacher's slides and your graded work — active recall, not a wall of notes. |
| `/due`       | "What's due?" in five seconds. Overdue first, then the week. Nothing else. |
| `/triage`    | Your whole workload → one ranked do-this-next list. Tells you when it doesn't fit. |
| `/plan-week` | A weekly schedule with slack built in, so it survives past Tuesday. |
| `/tutor`     | Diagnoses what you actually don't understand, then teaches that — by asking, not lecturing. |
| `/cram`      | Emergency exam prep. Triages material, drills you, quizzes you hard, tells you to sleep. |
| `/draft`     | Gets you off the blank page: outline, then a draft you rewrite. Ships with an integrity handoff. |
| `/email`     | Emails to professors, TAs, advisors that get a yes. Extensions, grade reviews, rec letters. |
| `/learn`     | A brutal, project-first plan for learning a new skill on a deadline. |

## Install

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/back-to-school-skills.git
cd back-to-school-skills
./install.sh
```

That copies the skills to `~/.claude/skills/` and puts the `bts` CLI on your
PATH. Restart Claude Code, type `/`, and they're there.

Manual version, if you'd rather see what's happening:

```bash
cp -R skills/* ~/.claude/skills/
install -m 755 bin/bts ~/.local/bin/bts
```

### Try it right now — no Canvas needed

```bash
bts demo     # loads a fake semester, dated relative to today
bts          # start chatting about it
```

The banner and the boxes show up on `bts`, `bts demo`, `bts setup` and
`bts doctor`. The data commands (`bts due`, `bts status`) skip the banner on
purpose — you run those twenty times a day.

**Not seeing colors?** Run `bts doctor`. Usual causes: output is piped or
redirected (colors auto-disable — override with `FORCE_COLOR=1`), `NO_COLOR`
is set in your shell, or `TERM=dumb`. It also checks whether `bts` and
`claude` are actually on your PATH.

You get five courses with real-looking grades, three overdue assignments, a
problem set due tomorrow and a midterm in eleven days. Clear it any time with
`bts revoke --all`.

### The CLI

Just run `bts`. It opens a chat:

```
❯ bts

  ✓ 5 courses, 22 assignments loaded
  Ask anything. /help for commands, /exit to quit.

❯ i have a chem midterm coming up and im behind, what do i do

  Midterm's Aug 21 — 11 days out, not a same-night cram. Bigger fires first:

  • PS3 (40 pts) due tomorrow 11:59pm, not started
  • PS2 already late — penalty grows the longer it sits, do it before PS3
  • Lab safety module (15 pts) missing — worth 20 min to check if late
    credit's still open before writing it off
  • Grade's 76.2% C — the problem sets are dragging it, not the midterm yet

  What's covered on the midterm, and is there a study guide posted? Once I
  know that I can build you a study packet targeting what you're weak on —
  20 min gets you the highest-yield topic, an hour covers the rest.
```

That's verbatim output, not a mockup.

It knows your actual courses, grades, and deadlines, and it remembers the
conversation. Inside the chat:

```
/due       show the assignment list      /new    fresh conversation
/packet    build a study packet          /help   commands
/sync      refresh from Canvas           /exit   quit
/status    what's configured
```

Any *other* slash command is handed straight to Claude, so `/tutor`,
`/triage`, `/plan-week`, `/cram`, `/draft`, `/email` and `/learn` all work
from inside the chat too.

Prefer one-shot? Every command also works directly:

```
bts ask "when is my chem midterm"
bts packet "chem 240 midterm, ch 1-7"
bts due                    # just the list, no chat
bts demo / sync / setup / status / revoke
```

**Chat needs the [`claude` CLI](https://claude.com/claude-code)** — it wraps
the one you already have, so there's no second API key and no extra cost.
Everything that isn't chat (`due`, `sync`, `status`) is pure stdlib Python and
works without it.

Output is colored and boxed on a terminal and degrades to clean plain text
when piped or when `NO_COLOR` is set — so `bts due | grep CHEM` works fine.

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

## Developer mode (`/canvas-dev`) — opt in, at your own risk

If you'd rather hit the Canvas API directly, you can. It's a real speed
difference and you get exact data instead of parsed pages:

|               | `/canvas` (default) | `/canvas-dev` |
|---------------|---------------------|---------------|
| Setup         | none                | make a token, ~2 min |
| Sync time     | ~1 min              | ~3 sec |
| Data          | what's on the page  | everything, exact |
| Stored secret | none                | a token on your machine |
| School policy | always fine         | **check yours** |

```bash
bts setup
```

A four-step wizard. It prints the risks and won't save anything until you type
`I ACCEPT`. Then:

```bash
bts sync                # -> snapshot.json, same format as browser mode
bts sync --course chem  # one course
bts due                 # the list, straight in your terminal
bts status              # what's configured (never prints the token)
bts test                # is the token still good
bts revoke              # delete the local token
bts revoke --all        # ...and the coursework snapshot
```

`/due`, `/triage`, `/plan-week` and `/cram` don't care which mode produced the
snapshot — they work the same either way.

**The deal you're accepting:**

- Your token lives at `~/.claude/canvas/credentials.json`, mode `0600`,
  **unencrypted**. Anyone who can read that file can act as you in Canvas.
- The script only ever sends `GET` requests — it can't submit, delete, or
  change anything. But the token itself is a full-access credential. Something
  else with it could.
- **Set an expiry date when you create the token.** End of semester. This is
  the single best thing you can do to limit the damage if it leaks.
- Lots of schools restrict or ban API tokens in their acceptable-use policy,
  and some disable them outright. Check yours. That's on you.
- `revoke` deletes the local copy — it does **not** invalidate the token.
  Also delete it in Canvas: Account → Settings → Approved Integrations.

Get a token at Canvas → Account → Settings → "+ New Access Token". Canvas
shows it once. Never paste it into a chat, a repo, or a command line argument
(`ps` and your shell history can see argv — let the script prompt you).

Stdlib Python only, no dependencies, one file. Read it before you run it:
[`bin/bts`](bin/bts).

## Why it doesn't just tell you to go study

The default failure mode of every study tool is handing back a block of time.
"Set aside 5 hours for the chem midterm" is useless — you already knew you
should study, and nobody volunteers for a 5-hour block.

So `bts` is built around two rules:

**Offer to make the thing, don't assign the time.** The answer to "I'm behind
in chem" is a study packet built from that professor's slides and the problem
sets you already lost points on — not a number of hours.

**Every estimate is two-tier, floor first.** "20 minutes gets you titrations,
which is where you're actually losing points. The other three topics need
another hour." The floor has to be real and under 30 minutes, and it has to
say honestly what it doesn't cover.

There's a working example in
[`examples/packet-math231-example.html`](examples/packet-math231-example.html) —
open it in a browser. Linear algebra, so it shows the math handling: matrices
drawn with CSS brackets, SVG diagrams for span and eigenvectors, and solutions
you step through one move at a time instead of one big reveal.

`/packet` is where this pays off. It builds a single self-contained HTML file:
one question on screen at a time, answers hidden until you commit, missed
cards come back, visible progress, and a brain-dump sheet at the end. Weighted
toward the questions you already got wrong, because those are worth more than
anything else you could review. It defaults to a 20-minute core set, with a
full set behind a toggle.

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
│   ├── packet/SKILL.md            <- builds the HTML study packets
│   ├── canvas/SKILL.md            <- browser mode, writes the snapshot
│   ├── canvas-dev/SKILL.md        <- opt-in API mode
│   ├── due/SKILL.md
│   ├── triage/SKILL.md
│   ├── plan-week/SKILL.md
│   ├── tutor/SKILL.md
│   ├── cram/SKILL.md
│   ├── draft/SKILL.md
│   ├── email/SKILL.md
│   └── learn/SKILL.md
├── bin/
│   └── bts                        <- the CLI
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
