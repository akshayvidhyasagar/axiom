<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **AXIOM**. Use GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream", repo: "AXIOM"})` and report the blast radius to the user.
- **MUST run `gitnexus_detect_changes({repo: "AXIOM"})` before committing** to verify changes only affect expected symbols.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding.
- Use `gitnexus_query({query: "concept", repo: "AXIOM"})` to find execution flows instead of grepping.
- Use `gitnexus_context({name: "symbolName", repo: "AXIOM"})` for full symbol context.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename`.
- NEVER commit changes without running `gitnexus_detect_changes()`.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/AXIOM/context` | Codebase overview, index freshness |
| `gitnexus://repo/AXIOM/clusters` | All functional areas |
| `gitnexus://repo/AXIOM/processes` | All execution flows |
| `gitnexus://repo/AXIOM/process/{name}` | Step-by-step execution trace |
<!-- gitnexus:end -->

---

# AXIOM — Project Context

## What This Is

**AXIOM** (Adaptive Cross-regime Intelligent Order Management) is a regime-aware, multi-signal equity strategy extending Microsoft Qlib with alternative data factors, heterogeneous model routing, and realistic execution simulation.

## Current State

The repo contains a **working prototype** (`core/`) using `defeatbeta-api` + FRED. This prototype is NOT the target system — it will be superseded by the Qlib-based architecture once Phase 0 begins.

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

## Documentation

| Document | Purpose |
|----------|---------|
| `docs/PRD.md` | Phased build plan — all phases currently unchecked |
| `docs/ARCHITECTURE.md` | System architecture and module dependencies |
| `docs/DECISIONS.md` | Architectural Decision Records (ADR-001 through ADR-006) |
| `docs/CHANGELOG.md` | Chronological change log |
| `wiki/INDEX.md` | Obsidian knowledge vault entry point |
| `rules/axiom-kb.md` | Knowledge base maintenance rules |

## Key Rules

1. **Never fill benchmark table with prototype results** — only Qlib-pipeline outputs are valid
2. **Point-in-time discipline is non-negotiable** — see ADR-005
3. **Factor validation before inclusion** — IC ≥ 0.02 threshold, see ADR-006
4. **Update `docs/CHANGELOG.md` before every commit**
5. **Log architectural decisions as ADRs** in `docs/DECISIONS.md`