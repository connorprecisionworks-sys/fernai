# Back to School — Claude Skills for Students

Seven skills that turn Claude into something actually useful during a semester.
Install once, then type `/tutor`, `/triage`, `/cram` and go.

No fluff, no "as an AI language model." Each one is a procedure someone who's
good at that thing would actually follow.

| Command      | What it does |
|--------------|--------------|
| `/tutor`     | Diagnoses what you actually don't understand, then teaches that — by asking, not lecturing. |
| `/triage`    | Dumps of assignments in, one ranked do-this-next list out. Tells you when it doesn't fit. |
| `/draft`     | Gets you off the blank page: outline, then a draft you rewrite. Ships with an integrity handoff. |
| `/email`     | Emails to professors, TAs, advisors that get a yes. Extensions, grade reviews, rec letters. |
| `/learn`     | A brutal, project-first plan for learning a new skill on a deadline. |
| `/cram`      | Emergency exam prep. Triages material, drills you, quizzes you hard, tells you to sleep. |
| `/plan-week` | A weekly schedule with slack built in, so it survives past Tuesday. |

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

Pass your context on the same line:

```
/tutor eigenvectors, I get the definition but not why anyone cares
/triage    (then paste everything you owe)
/cram orgo midterm, 6 hours from now, ch 1-7, haven't started
/email need a 3-day extension on my BIOL 201 lab, prof is strict
/plan-week 4 classes, 15hr/wk job, two papers due Friday
```

Claude will also pull these up on its own when the conversation matches — you
don't have to remember the command.

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
│   ├── tutor/SKILL.md
│   ├── triage/SKILL.md
│   ├── draft/SKILL.md
│   ├── email/SKILL.md
│   ├── learn/SKILL.md
│   ├── cram/SKILL.md
│   └── plan-week/SKILL.md
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

- Subject-specific tutors (`/tutor-calc`, `/tutor-orgo`)
- `/read` — getting through dense assigned reading
- `/office-hours` — what to actually ask when you get there
- `/debug-my-grade` — where the points went and how to get them back

Keep the house style: short, direct, procedural. No motivational filler.

## License

MIT. Fork it, rename it, ship it.
