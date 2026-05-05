<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **AXIOM**. Use GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Run `gitnexus_impact({target: "symbolName", direction: "upstream", repo: "AXIOM"})` and report the blast radius.
- **MUST run `gitnexus_detect_changes({repo: "AXIOM"})` before committing.**
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk.
- Use `gitnexus_query({query: "concept", repo: "AXIOM"})` to find execution flows.
- Use `gitnexus_context({name: "symbolName", repo: "AXIOM"})` for full symbol context.

## Never Do

- NEVER edit a function/class/method without first running `gitnexus_impact`.
- NEVER ignore HIGH or CRITICAL risk warnings.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename`.
- NEVER commit without running `gitnexus_detect_changes()`.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/AXIOM/context` | Codebase overview, index freshness |
| `gitnexus://repo/AXIOM/clusters` | All functional areas |
| `gitnexus://repo/AXIOM/processes` | All execution flows |
| `gitnexus://repo/AXIOM/process/{name}` | Step-by-step execution trace |
<!-- gitnexus:end -->

---

# AXIOM — Permanent Agent Protocol

## Context & Memory
AXIOM uses the `claude-obsidian` skill suite for its knowledge base.
- Read `wiki/hot.md` for recent context.
- Use `/wiki-query` to search the knowledge base.
- Use `/save` to file new architectural decisions or synthesis.

## Session START (every session, no exceptions)

1. Read `docs/PRD.md` → identify current active phase
2. Read `docs/ARCHITECTURE.md` → load module map
3. Read `docs/CHANGELOG.md` → last 3 entries for recent context
4. If task touches a wiki concept → read that `wiki/concepts/` page first
5. Run GitNexus on any file about to be edited
6. **Follow Behavioral Guidelines:** Think before coding, favor simplicity, and perform surgical changes only.

## Session END (every session, no exceptions)

1. Append entry to `docs/CHANGELOG.md` (see `rules/axiom-kb.md` for format)
2. Update `docs/ARCHITECTURE.md` if any files were created/moved/deleted
3. Update `docs/PRD.md` checkboxes if phase progress was made
4. Run `gitnexus_detect_changes()` before committing

## Current State

| Directory | Status | Purpose |
|-----------|--------|---------|
| `core/` | PROTOTYPE | DCF + fundamentals scoring, macro regime |
| `scripts/` | PROTOTYPE | Backtest, report gen, usage examples |
| `data/` | ACTIVE | OHLCV sync, raw data storage |
| `factors/` | EMPTY | Phase 1: AlphaAXIOM factor library |
| `regime/` | EMPTY | Phase 2: HMM regime detection |
| `models/` | EMPTY | Phase 3: per-regime model configs |
| `portfolio/` | EMPTY | Phase 4: risk-parity + sector caps |
| `execution/` | EMPTY | Phase 5: Almgren-Chriss simulation |

## Key Documentation

| File | Purpose |
|------|---------|
| `docs/PRD.md` | Phased build plan — check phase status here |
| `docs/ARCHITECTURE.md` | Module map and dependencies |
| `docs/DECISIONS.md` | ADRs — always check before making architectural choices |
| `docs/CHANGELOG.md` | Session log — append-only |
| `wiki/index.md` | Knowledge vault entry point |
| `rules/axiom-kb.md` | Full maintenance rules (Second Brain protocol) |

---

## Behavioral Guidelines

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code. No "flexibility" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- **Ask yourself:** "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken. Match existing style.
- If you notice unrelated dead code, mention it - don't delete it.
- **Orphans:** Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead code unless asked.
- **The test:** Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
- Transform tasks into verifiable goals (e.g., "Write tests for invalid inputs, then make them pass").
- For multi-step tasks, state a brief plan:
  1. `[Step]` → verify: `[check]`
  2. `[Step]` → verify: `[check]`

---

## Commit Convention

```
wiki: ingest <source>          # wiki changes
fix: <desc> in <file>          # bug fixes
arch: <desc> in ARCHITECTURE   # architecture doc changes
prd: <desc> in PRD             # PRD changes
adr: ADR-00N <title>           # new decisions
feat: <feature> in <module>    # new features
chore: CHANGELOG sync          # maintenance
```

**Never commit canonical docs and code changes in the same commit.**

## Key Rules

1. Never fill benchmark table with prototype results
2. Point-in-time discipline is non-negotiable (ADR-005)
3. Factor validation IC ≥ 0.02 before inclusion (ADR-006)
4. Update CHANGELOG before every commit
5. Log architectural decisions as ADRs

## What Akshay Does Manually

- Open Obsidian → "Open folder as vault" → `AXIOM/`
- Review graph view after wiki compiles for orphans/hubs
- Drop raw materials into `raw/` then say "compile wiki"
- Confirm phase completion: "mark Phase N complete"
- Periodically review ADRs: "are past decisions still valid?"