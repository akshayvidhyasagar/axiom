# AXIOM Knowledge Base Rules

> These rules apply to every session, every change, forever. They are non-negotiable.

---

## The Second Brain Model

The AXIOM wiki is a living second brain:

1. Raw material lands in `raw/` (papers, findings, docs, links)
2. Antigravity compiles it into structured `wiki/concepts/` pages with cross-links
3. Obsidian surfaces the graph — Akshay navigates it visually
4. Canonical docs (`ARCHITECTURE`, `CHANGELOG`, `DECISIONS`, `PRD`) stay in sync with reality

The wiki is NOT documentation. It is **compiled knowledge** — concepts distilled from sources, linked to each other, and grounded in AXIOM's implementation. If a wiki page could belong to any project, it is too generic.

---

## Documentation Hierarchy

1. **`docs/PRD.md`** — Source of truth for what to build and in what order
2. **`docs/ARCHITECTURE.md`** — Source of truth for system structure and dependencies
3. **`docs/DECISIONS.md`** — Source of truth for why things are the way they are
4. **`docs/CHANGELOG.md`** — Chronological record of all changes

---

## Mandatory Session Protocol

### On Session START (every session, no exceptions)

1. Read `docs/PRD.md` — identify the current active phase
2. Read `docs/ARCHITECTURE.md` — load the current module map into context
3. Check `docs/CHANGELOG.md` — read the last 3 entries to understand recent changes
4. If the user's task touches a concept in `wiki/concepts/`, read that page before proceeding
5. Run GitNexus to verify understanding of any file about to be edited

### On Session END (every session, no exceptions)

Append to `docs/CHANGELOG.md`:

```
## [YYYY-MM-DD] <Category>

### Code Changes
- <what changed> in `<file>` — <one-line reason>

### Architecture Changes (if any)
- <what structural change was made>

### Wiki Changes (if any)
- WikiCompile: <created/updated> `<page>.md` — <one-line summary>

### Decisions (if any)
- ADR-00N: <decision title> — see docs/DECISIONS.md
```

Never skip this step. Never batch multiple sessions into one entry. Date must be accurate.

---

## Canonical File Maintenance

### CHANGELOG.md
- **Append only.** Never edit past entries.
- One entry per session minimum if any file was touched.
- If nothing changed (read-only session), no entry needed.

### ARCHITECTURE.md
Rebuild the affected section whenever:
- A new file is created anywhere in the repo
- A file is deleted or moved
- A new import relationship is established between modules
- A module's purpose changes

Update: directory tree, Module Dependencies table, Data Flow diagram, "Current State" section.

### DECISIONS.md
Add a new ADR whenever:
- One implementation approach is chosen over a plausible alternative
- Something in scope is decided against
- A constraint is discovered (data availability, Qlib limitation, performance)
- A previous ADR's consequences become visible

### PRD.md
- Check phase checkbox immediately when completed: `- [x] Phase N`
- Add in-progress notes: `- [ ] Phase N *(in progress — <what's done>)*`
- Never change acceptance criteria without flagging as PRD amendment in CHANGELOG

### README.md
- Update benchmark table immediately when any phase produces new metrics
- Never leave TBD values once real numbers exist
- Keep build phases checklist in sync with PRD.md

---

## Commit Convention

Every git commit touching canonical files must use:

```
wiki: ingest <source>
fix: <description> in <file>
arch: <what changed> in ARCHITECTURE.md
prd: <what changed> in PRD
adr: ADR-00N <title>
feat: <feature> in <module>
chore: CHANGELOG + ARCHITECTURE sync
```

**Never commit canonical docs in the same commit as code changes** — separate them for a clean audit trail.

---

## Knowledge Rules

### R1: No undocumented architectural decisions
Every choice that affects system structure, data flow, or methodology must be logged as an ADR.

### R2: PRD phases are the only roadmap
Do not start work on a phase until the previous phase's acceptance criteria are met.

### R3: Benchmark table integrity
Never fill benchmark table values with prototype results. Only Qlib-pipeline outputs from committed code are valid.

### R4: Wiki pages are LLM-compiled
Wiki concept pages may be edited manually, but edits will be overwritten on next compilation unless `raw/` source material is updated.

### R5: Point-in-time discipline is non-negotiable
Any data source must document its PIT boundary. Any backtest violating PIT is invalid. See ADR-005.

### R6: Factor validation before inclusion
No custom factor enters the model without passing IC ≥ 0.02 validation.

### R7: Keep the changelog current
Every session that modifies code or documentation must append a CHANGELOG entry before committing.
