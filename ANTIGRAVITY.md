# AXIOM — AlphaAXIOM Trading System
**Agent:** Antigravity
**Mode:** B (GitHub/Repo) + E (Research)
**Owner:** Akshay Vidhyasagar
**Purpose:** Quantitative alpha research — factor generation, regime detection, model routing, portfolio construction, execution simulation

---

## Session Protocol

### START (every session, no exceptions)
1. Read `wiki/hot.md` — 500-word context cache, costs ~500 tokens
2. Read `docs/PRD.md` — identify active phase and any changed checkboxes
3. Read last 3 entries of `docs/CHANGELOG.md` — what changed recently
4. If the task touches a concept in `wiki/`, read that concept page before proceeding
5. If the task touches a module, run GitNexus on it to verify current structure

### END (every session where any file was touched)
1. Overwrite `wiki/hot.md` completely — keep under 500 words, reflect current state
2. Append to `docs/CHANGELOG.md` — one entry, accurate date, no batching
3. Append to `wiki/log.md` — one entry at TOP, operation type + what changed

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

1. Open Obsidian → Open Folder as Vault → select `AXIOM/` (the repo root, not wiki/)
2. Install community plugins: Dataview, Templater, Obsidian Git, Local REST API
3. CSS snippet vault-colors.css — already enabled at `.obsidian/snippets/`
4. Set graph view group colors per `skills/WIKI.md` Section 7
5. Install Obsidian Web Clipper → configure save path to `.raw/`
6. After any wiki compile: check graph view for orphan nodes, report them
7. Phase sign-off: say "mark Phase N complete" — Antigravity handles all file updates
8. Copy Local REST API key into a local `.env` file — never commit it