# AXIOM — AlphaAXIOM Trading System

**Agent:** Antigravity
**Mode:** B (GitHub/Repo) + E (Research)
**Owner:** Akshay Vidhyasagar
**Purpose:** Quantitative alpha research — factor generation, regime detection, model routing, portfolio construction, execution simulation

---

## Session Protocol

### START (every session, no exceptions — execute all 7 steps before touching any file)

1. **Git state check**

   ```bash
   git log --oneline -5
   git status
   ```

   If there are uncommitted changes from a previous session, commit them first:

   ```bash
   git add -A && git commit -m "chore: uncommitted changes from previous session"
   ```

2. **Read wiki/hot.md** — 500-word context cache. This is the primary bootstrap. Read fully before anything else.

3. **Read docs/PRD.md** — identify the active phase, its acceptance criteria, and which checkboxes are complete vs pending.

4. **Read docs/CHANGELOG.md last 3 entries** — understand what changed recently and what was left incomplete.

5. **Run GitNexus on active phase directory**

   ```bash
   gitnexus analyze <active-phase-dir>/
   ```

   If Phase 0: `gitnexus analyze .` (whole repo — no code yet)
   Report the import graph and any structural issues before proceeding.

6. **Query wiki for relevant concepts**
   If the task touches any concept (regime, factors, signals, portfolio, execution):

   ```bash
   $QMD wiki/ "<concept keyword>"
   ```

   Then read the returned pages. Maximum 5 pages per query.

7. **Check Obsidian sync** (if Local REST API is online)

   ```bash
   curl -sk -H "Authorization: Bearer $OBSIDIAN_KEY" "https://127.0.0.1:27124/vault/wiki/hot.md" | head -30
   ```

   Confirm Obsidian and filesystem are in sync. If they diverge, filesystem is canonical.

### END (every session where any file was touched — all 5 steps mandatory)

1. **Overwrite wiki/hot.md completely**
   - Under 500 words
   - Sections: Last Updated, Current State, Key Known Issues, Active Threads, Recent Changes
   - Reflect actual current state — not aspirational

2. **Append to docs/CHANGELOG.md**
   Format:

   ```
   ## [YYYY-MM-DD] — <session summary in one line>
   - <bullet per meaningful change>
   ```

   Never edit past entries.

3. **Append to wiki/log.md at TOP**
   Format: `## [YYYY-MM-DD] <operation type> | <title>`
   Operation types: ingest | query | lint | migration | arch | feat | fix | chore

4. **Update wiki/index.md** if any wiki pages were created, modified, or deleted.

5. **Commit**

   ```bash
   git add -A
   git commit -m "<type>: <description>"
   ```

   Use commit convention from ANTIGRAVITY.md. Canonical doc changes in separate commits from code.

---

## Engineering Principles

These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding
*Don't assume. Don't hide confusion. Surface tradeoffs.*

- **State assumptions explicitly.** If uncertain, ask.
- **Present alternatives.** If multiple interpretations exist, present them — don't pick silently.
- **Push back for simplicity.** If a simpler approach exists, say so.
- **Stop on ambiguity.** If something is unclear, name what's confusing. Ask.

### 2. Simplicity First
*Minimum code that solves the problem. Nothing speculative.*

- **No gold-plating.** No features beyond what was asked.
- **No premature abstraction.** No abstractions for single-use code.
- **No unnecessary flexibility.** No "configurability" that wasn't requested.
- **Sane error handling.** No error handling for impossible scenarios.
- **Conciseness.** If you write 200 lines and it could be 50, rewrite it.
- **Seniority Test.** "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
*Touch only what you must. Clean up only your own mess.*

- **Stay in scope.** Don't "improve" adjacent code, comments, or formatting.
- **Respect established code.** Don't refactor things that aren't broken.
- **Match style.** Match existing style, even if you'd do it differently.
- **Mention dead code.** If you notice unrelated dead code, mention it — don't delete it.
- **Orphan management.** Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead code unless asked.
- **The Traceability Test.** Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
*Define success criteria. Loop until verified.*

- **Verifiable goals.**
  - "Add validation" → "Write tests for invalid inputs, then make them pass"
  - "Fix the bug" → "Write a test that reproduces it, then make it pass"
  - "Refactor X" → "Ensure tests pass before and after"
- **State the plan.** For multi-step tasks, state a brief plan:
  1. [Step] → verify: [check]
  2. [Step] → verify: [check]
  3. [Step] → verify: [check]

---

## Project State

| Item | Value |
|------|-------|
| Active Phase | Phase 0 — Environment Setup |
| Qlib installed | No |
| Baseline metrics | TBD |
| Last commit | 3cca4f7 |
| Wiki pages | 4 concept stubs |

---

## Repo Structure

```
AXIOM/                       ← vault root (open this in Obsidian)
├── .obsidian/               ← Obsidian config — do not modify manually
│   └── snippets/
│       └── vault-colors.css
├── .raw/                    ← immutable — never write here
│   ├── papers/
│   ├── findings/
│   └── docs/
├── wiki/                    ← knowledge base
│   ├── hot.md               ← overwrite each session end (~500 words)
│   ├── index.md             ← master catalog — update on every ingest
│   ├── log.md               ← append-only, new entries at TOP
│   ├── modules/             ← one page per AXIOM module
│   ├── concepts/            ← quant concepts
│   ├── decisions/           ← ADR navigation (full text in docs/DECISIONS.md)
│   ├── papers/              ← research paper summaries
│   ├── gaps/                ← open questions, unresolved issues
│   ├── flows/               ← data flow diagrams
│   ├── sources/             ← one page per ingested raw source
│   └── meta/                ← dashboard, lint reports
├── docs/
│   ├── PRD.md               ← phase checkboxes — source of truth
│   ├── ARCHITECTURE.md      ← module map, dependency graph
│   ├── DECISIONS.md         ← ADR-001 through ADR-00N
│   └── CHANGELOG.md         ← append-only session log
├── factors/                 ← Phase 1
├── regime/                  ← Phase 2
├── models/                  ← Phase 3
├── portfolio/               ← Phase 4
├── execution/               ← Phase 5
├── backtest/
├── notebooks/
├── references/
├── data/
│   └── raw/
│       ├── options/
│       ├── ohlcv/
│       ├── short_interest/
│       └── earnings/
├── rules/axiom-kb.md        ← full rule set
└── skills/
    ├── WIKI.md                   ← claude-obsidian schema — read before any wiki op
    ├── wiki/SKILL.md
    ├── wiki-ingest/SKILL.md
    ├── wiki-query/SKILL.md
    ├── wiki-lint/SKILL.md
    ├── wiki-fold/SKILL.md
    ├── save/SKILL.md
    ├── autoresearch/SKILL.md
    ├── canvas/SKILL.md
    └── obsidian-markdown/SKILL.md
```

---

## Canonical File Rules

| File | Rule |
|------|------|
| `docs/PRD.md` | Update phase checkboxes immediately on completion. Never change acceptance criteria without a PRD amendment entry in CHANGELOG. |
| `docs/ARCHITECTURE.md` | Rebuild affected section on any file create/delete/move/rename. Update module dependency table. |
| `docs/DECISIONS.md` | Add ADR on every non-trivial implementation choice, discovered constraint, or rejected alternative. |
| `docs/CHANGELOG.md` | Append one entry per session. Never edit past entries. Accurate date always. |
| `wiki/hot.md` | Overwrite completely at session end. Keep under 500 words. Primary session bootstrap. |
| `wiki/log.md` | Append only. New entries at TOP. Format: `## [YYYY-MM-DD] operation \| title` |
| `wiki/index.md` | Update on every ingest and after any wiki restructure. |

---

## Wiki Operations

Read `skills/WIKI.md` before any wiki operation.

| Trigger | Operation | Skill |
|---------|-----------|-------|
| `ingest [file]` | Read source → create pages → update index + log | `skills/wiki-ingest/SKILL.md` |
| `what do I know about X` | hot.md → index → pages → synthesize | `skills/wiki-query/SKILL.md` |
| `lint wiki` | Auto-fix links/index; report orphans/gaps | `skills/wiki-lint/SKILL.md` |
| `/save` | File current answer as permanent wiki page | `skills/save/SKILL.md` |
| `/autoresearch [topic]` | Autonomous search → fetch → ingest loop | `skills/autoresearch/SKILL.md` |
| `/canvas` | Create/update Obsidian canvas map | `skills/canvas/SKILL.md` |
| `fold [page]` | Compress long page to summary | `skills/wiki-fold/SKILL.md` |

### Query read order (token budget)

1. `wiki/hot.md` (~500 tokens)
2. `wiki/index.md` (~1000 tokens)
3. `wiki/<domain>/_index.md` (~300 tokens)
4. Individual pages (100-300 tokens each, max 5 per query)

Run `qmd wiki/ "<query>"` before manually scanning pages.

### Wiki page frontmatter (required on every page)

```yaml
---
type: <concept|module|decision|paper|source|flow|gap|meta>
title: "Human-Readable Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - quant
  - axiom
status: <seed|developing|mature|evergreen>
related:
  - "[[Related Page]]"
sources: []
---
```

---

## Obsidian Setup

**Vault path:** `AXIOM/` — the entire repo is the vault root. wiki/ is a subfolder within it.
**Wikilinks:** `[[Page Name]]` format everywhere in wiki/ body text.
**CSS snippets:** `.obsidian/snippets/vault-colors.css` — already enabled.

**Required community plugins:**

- Dataview — powers wiki/meta/dashboard.md
- Templater — consistent page creation
- Obsidian Git — auto-commit every 15 minutes
- Local REST API — enables direct file read/write via curl

**REST API usage** (when MCP not available):

```bash
API="https://127.0.0.1:27124"
KEY="<your-api-key>"
# Read:
curl -sk -H "Authorization: Bearer $KEY" "$API/vault/wiki/hot.md"
# Patch frontmatter status:
curl -sk -X PATCH -H "Authorization: Bearer $KEY" \
  -H "Operation: replace" -H "Target-Type: frontmatter" \
  -H "Target: status" -H "Content-Type: application/json" \
  --data '"mature"' "$API/vault/wiki/concepts/regime-detection.md"
```

---

## Tooling

| Tool | Command | Purpose |
|------|---------|---------|
| qmd | `qmd wiki/ "<query>"` | Fast keyword search across wiki — use before manual scanning |
| GitNexus | `gitnexus analyze <path>` | Module import graph — run before editing any module |
| git | `git log --oneline -10` | Verify last 10 commits at session start |

---

## GitNexus Integration

Run GitNexus before editing any module to verify current structure. When a phase completes:

1. Run GitNexus on completed modules → get import graph
2. Create or update `wiki/modules/<module>.md` for each new module
3. Update `wiki/flows/` with any new data flow
4. Update `docs/ARCHITECTURE.md` module dependency table

---

## GitNexus Decision Protocol

GitNexus is the structural oracle. Consult it before making any architectural decision.

### When to run GitNexus

| Trigger | Command |
|---------|---------|
| Before editing any module file | `gitnexus analyze <module-dir>/` |
| Before adding a new import/dependency | `gitnexus analyze <file>` |
| Before a phase completes | `gitnexus analyze <phase-dir>/` |
| After any refactor | `gitnexus analyze .` |
| Any time structure feels uncertain | `gitnexus analyze .` |

### How to use the output

1. Read the import graph — identify all upstream and downstream dependencies of the file you're about to touch
2. If the change affects a downstream module, check its wiki page first: `$QMD wiki/ "<module name>"`
3. If no wiki page exists for an affected module, create a stub before making the change
4. If GitNexus reveals a circular dependency or unexpected coupling, file an ADR before proceeding:
   `docs/DECISIONS.md → ADR-00N: <issue title>`
5. After the change, re-run GitNexus to confirm the graph updated as expected

### Phase completion gate

Before marking any phase checkbox in docs/PRD.md as complete:

1. Run `gitnexus analyze <phase-dir>/` — import graph must be clean (no unresolved imports, no circular deps)
2. Run `lint wiki` — no orphan pages for modules in this phase
3. All acceptance criteria in PRD.md for this phase must be verifiably met
4. Only then: update PRD.md checkbox, create wiki/modules/ pages, update wiki/flows/, commit

---

## Continuous Wiki Maintenance

The wiki is a live system, not a documentation afterthought. Every substantive action has a wiki consequence.

### Automatic wiki triggers

| Action | Wiki consequence |
|--------|-----------------|
| New file created in any phase dir | Create `wiki/modules/<name>.md` stub |
| Function/class significantly changed | Update relevant `wiki/modules/<name>.md` |
| New concept encountered (algorithm, technique, data source) | Create `wiki/concepts/<name>.md` |
| Paper read or referenced | `ingest` it: create `wiki/papers/<name>.md` |
| Bug discovered | Add to `wiki/gaps/_index.md` |
| Bug resolved | Update gap entry, update relevant concept/module page |
| ADR written | Add navigation stub to `wiki/decisions/_index.md` |
| Phase completed | Full wiki/modules/ sweep for all modules in that phase |
| Any query answered | Consider `/save` if the answer has lasting value |

### Lint schedule

Run `lint wiki` every 10 ingest operations or at the start of every new phase, whichever comes first.
After lint: commit with `wiki: lint — N fixes`.

### Hot.md discipline

hot.md is overwritten, never appended. It must answer these questions at all times:

- What phase are we in and what is the next concrete step?
- What are the 2-3 most important open issues?
- What changed in the last session?
- What should the next session start with?

If hot.md cannot answer all four, it is incomplete — rewrite it.

### Obsidian sync via Local REST API

When Obsidian is open and Local REST API is active, use it to patch frontmatter without rewriting entire files:

```bash
# Mark a concept page as mature
curl -sk -X PATCH -H "Authorization: Bearer $OBSIDIAN_KEY" \
  -H "Operation: replace" -H "Target-Type: frontmatter" \
  -H "Target: status" -H "Content-Type: application/json" \
  --data '"mature"' "https://127.0.0.1:27124/vault/wiki/concepts/<page>.md"

# Update the updated date on any wiki page
curl -sk -X PATCH -H "Authorization: Bearer $OBSIDIAN_KEY" \
  -H "Operation: replace" -H "Target-Type: frontmatter" \
  -H "Target: updated" -H "Content-Type: application/json" \
  --data '"2026-05-05"' "https://127.0.0.1:27124/vault/wiki/concepts/<page>.md"
```

Always patch frontmatter via API when Obsidian is open — avoids file conflicts from Obsidian's own write cache.

---

## Skill Invocation Rules

Before executing any wiki operation, read the corresponding SKILL.md. Do not improvise wiki operations from memory.

### Mandatory reads by trigger

| User says | Read first | Then execute |
|-----------|-----------|--------------|
| "ingest [anything]" | `skills/wiki-ingest/SKILL.md` | Full ingest procedure |
| "what do I know about X" | `skills/wiki-query/SKILL.md` | Query procedure |
| "lint wiki" | `skills/wiki-lint/SKILL.md` | Lint procedure |
| "/save" | `skills/save/SKILL.md` | Save procedure |
| "/autoresearch [topic]" | `skills/autoresearch/SKILL.md` | Full autonomous loop |
| "/canvas" | `skills/canvas/SKILL.md` | Canvas creation |
| "fold [page]" | `skills/wiki-fold/SKILL.md` | Fold procedure |
| Any wiki op | `skills/WIKI.md` | Schema reference |

### Autoresearch usage

`/autoresearch` runs a full autonomous loop: web search → fetch → synthesize → ingest → update wiki. Use it when:

- A new technique or algorithm is referenced that has no wiki page
- A concept page is at "seed" status and needs development
- Akshay asks "research X" with no specific source

Always confirm the autoresearch plan before executing — it can generate many pages. Cap at 5 pages per run unless Akshay explicitly approves more.

### Canvas usage

Use `/canvas` to create visual maps when:

- A new phase begins (architecture overview canvas)
- A complex data flow needs visualization
- Akshay asks for a system overview

Save canvases to `wiki/meta/<name>.canvas`.

---

## Commit Convention

```
wiki: ingest <source-title>
wiki: lint — N fixes
arch: <change> in ARCHITECTURE.md
prd: phase N marked complete
adr: ADR-00N <title>
feat: <feature> in <module path>
fix: <description> in <file>
chore: CHANGELOG + hot.md sync
```

Canonical doc changes in separate commits from code changes. Never batch wiki + code in one commit.

---

## Cross-Project Access (Vellanthra, Polymatic)

Add to those projects' ANTIGRAVITY.md:

```
## AXIOM Wiki
Path: ~/path/to/AXIOM/wiki/
Read order: hot.md → index.md → domain _index.md → individual pages
Do NOT read for general coding questions unrelated to AXIOM concepts.
```

---

## Akshay's Manual Responsibilities

1. Install Obsidian Web Clipper → configure save path to `.raw/`
2. After any wiki compile: check graph view for orphan nodes, report them
3. Phase sign-off: say "mark Phase N complete" — Antigravity handles all file updates
