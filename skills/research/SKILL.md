---
name: research
description: Find and vet real sources for a paper, then save them as a research file the draft skill can build from. Use when the user needs sources, citations, references, background reading, or says they have to write about a topic and don't know where to start. Also for fact-checking claims already in a draft.
argument-hint: [topic or thesis + how many sources you need]
---

# Research

Topic: $ARGUMENTS

Produces a vetted source file, not a pile of links. The output is an artifact —
`/draft` reads it, so research and writing stop being two disconnected jobs.

The failure this prevents: a student pastes five URLs into a paper, half are
blogs, one is a citation of a citation, and the professor notices.

## Step 1 — Pin the question first

Ask, in one message, only what you can't infer from the assignment prompt in
their coursework:

- How many sources, and does the assignment restrict the kind? (peer-reviewed
  only, primary sources, no websites — this is usually in the prompt, read it)
- Citation style — APA, MLA, Chicago, CSE
- Their angle, if they have one. A search for "climate change" returns
  everything; "why did the 1970s consensus shift" returns something usable.

If they have no angle, that's the actual problem. Give three specific arguable
angles and have them pick one before searching. A paper without a thesis can't
be researched, only browsed.

## Step 2 — Search in layers, not one pass

Run several searches from **different angles** — the same query reworded
returns the same page. Vary the axis:

- **Terminology** — the academic term and the plain-language term produce
  different results ("myocardial infarction" vs "heart attack")
- **Position** — search for the counterargument explicitly. A paper that only
  cites its own side is the most common way to lose points on an argument essay
- **Time** — the foundational work and the last two years are different
  searches
- **Venue** — Google Scholar, their library databases, government and NGO data,
  the primary document itself

Prefer their university library's databases when they have access — a source
behind a paywall they can actually reach beats an open blog.

## Step 3 — Grade every source before it goes in the file

For each candidate, record a tier. Be blunt; this is the part that saves them.

- **A — citable anywhere.** Peer-reviewed, primary source, government dataset,
  or a book from an academic press.
- **B — usable with attribution.** Reputable journalism, an established
  organisation's report, a textbook.
- **C — background only.** Wikipedia, blogs, course notes. Useful for finding
  A-tier sources through their references; **never cite these directly**.
- **D — do not use.** Content farms, SEO pages, AI-generated summaries, any
  page whose author you cannot identify.

Say out loud why each B or C is not an A. And check the **date** — a 2011
source on anything technological is a liability unless they're doing history.

**Never invent a source.** No fabricated DOIs, page numbers, author names, or
quotes. If you cannot open the actual page, mark it `[UNVERIFIED — open this
before citing]`. A hallucinated citation is worse than no citation: it is
detectable, and it looks like deliberate fraud rather than laziness.

## Step 4 — Write the artifact

Save to `~/Desktop/fern-research/<COURSE> - <topic>.md`:

    # <topic> — research for <COURSE> <assignment>
    Thesis: <the arguable sentence this is all supporting>
    Style: APA   ·   Needed: 6 sources   ·   Found: 7 (5 A, 2 B)

    ## Sources

    ### A1 — <full citation in the required style>
    URL / DOI
    What it argues: <one line>
    Use it for: <the specific claim in the paper this supports>
    Key quote (p. 14): "<exact text>"
    Counterpoint: <if it complicates their thesis, say so here>

    ### B1 — ...

    ## The other side
    <2–3 lines: the strongest argument against the thesis, and which source
    makes it. Every argument paper needs this and most students skip it.>

    ## Gaps
    <what you could not find, and where to look next — the library, a
    specific database, their professor's office hours>

## Step 5 — Hand off

Four lines, no more:

- Where the file is
- How many of each tier, and whether that meets the requirement
- The one source they should actually read in full, and why it's the one
- `/draft` next — it will pull this file in automatically

Then stop.

## Fact-checking mode

If they hand you an existing draft instead of a topic, invert the job: pull
every factual claim and every citation out, verify each one, and return only
the failures — the unsupported claims, the sources that don't say what the
draft implies, the citations that don't resolve. Sorted by how badly each would
hurt if a professor checked it. Don't list what passed.
