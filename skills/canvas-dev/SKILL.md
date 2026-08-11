---
name: canvas-dev
description: Opt-in developer mode - set up direct Canvas API access with a personal access token stored locally, for students who want faster and more complete syncs than browser reading. Use when the user asks about the Canvas API, wants a token-based setup, developer mode, faster sync, or wants to check, test, or remove a saved Canvas token.
argument-hint: [setup | sync | due | status | revoke]
---

# Canvas Dev Mode

Action: $ARGUMENTS

Direct Canvas API access. Faster and more complete than browser reading, but
it means a token sits on this machine. **This is opt-in and the student
accepts the risk.** Default everyone to `/canvas` (browser) unless they ask
for this specifically.

CLI: `fern` (installed by `install.sh` to `~/.local/bin/fern`).
If `fern` isn't on PATH, run it directly from the repo: `./bin/fern`.

## Show the tradeoff first

If they haven't already decided, one short comparison, then let them pick:

|                | `/canvas` (browser)      | `/canvas-dev` (API)        |
|----------------|--------------------------|----------------------------|
| Setup          | none                     | make a token, ~2 min       |
| Speed          | ~1 min                   | ~3 sec                     |
| Data           | what's on the page       | everything, exact          |
| Stored secret  | none                     | a token on this machine    |
| School policy  | always fine              | **check yours**            |

If they don't have a concrete reason for the API, tell them to use `/canvas`.
Don't upsell this.

## Setup

Walk them through it, don't do it silently:

**1. Make the token.**
Canvas → Account → Settings → **"+ New Access Token"**.
- Purpose: something identifiable like `claude-school-skills`
- **Set an expiry date.** End of semester. Insist on this — it's the one
  control that limits the blast radius if the token ever leaks.
- Canvas shows the token **once**. Copy it.

**2. Run setup.** `fern` prints the risk notice and requires the student
to type `I ACCEPT` before it saves anything:

```bash
fern setup
```

It prompts for the Canvas URL and reads the token with hidden input.

**Never put the token in a command line argument** — argv is visible to other
processes via `ps` and lands in shell history. Let it prompt. If it must be
scripted, pipe it through the `CANVAS_TOKEN` environment variable.

**Never print, echo, log, or repeat the token back to the student.** If they
paste a token into the chat, tell them to revoke it in Canvas and make a new
one — it's now in a conversation log.

**3. It self-tests** on success and prints the connected account name.

## Commands

```bash
fern setup              # guided setup (requires typing "I ACCEPT")
fern sync               # fetch everything -> snapshot.json
fern sync --course chem # one course only
fern due                # overdue + next 7 days, straight in the terminal
fern status             # what's configured (never shows the token)
fern test               # is the token still good
fern revoke             # delete the local token
fern revoke --all       # ...and the coursework snapshot
```

`fern sync` writes `~/.claude/fern/snapshot.json` in the same format the browser
path produces, so `/due`, `/triage`, `/plan-week`, and `/cram` work identically
either way. The only difference is `"source": "api"`.

## What fern does and doesn't do

- **GET requests only.** It cannot submit, delete, or change anything.
- Token at `~/.claude/fern/credentials.json`, mode `0600`, unencrypted.
- Stdlib Python only, single file. No dependencies, no network calls anywhere but their
  own Canvas.
- Nothing is uploaded. Everything stays on their machine.

The token itself is *not* read-only, though — it's a full-access credential.
Say that plainly if they ask.

## Troubleshooting

- **401** — token wrong, expired, or revoked. Make a new one, run setup again.
- **403** — school has API tokens disabled, or a rate limit. This is common,
  and it's not fixable from here. Fall back to `/canvas`.
- **No token option in Canvas settings** — the school turned it off. Same
  answer: use `/canvas`.
- **Missing assignments** — the course may be unpublished, concluded, or the
  assignment has no due date. `fern sync` only includes active enrollments.

## Revoking

```bash
fern revoke
```

Then tell them the part people forget: **deleting the local file does not
invalidate the token.** They must also delete it in Canvas at
Account → Settings → Approved Integrations. Say this every time.

Good moments to bring this up unprompted: end of semester, if they mention
losing the laptop, or if they mention sharing the machine.
