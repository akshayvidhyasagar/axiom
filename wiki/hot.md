---
type: meta
title: "Hot Cache"
updated: 2026-05-26
---

# Recent Context

## Last Updated
2026-05-26 — Terminology normalization to "agent" across all configs, docs, and skills.

## Current State
- AXIOM Knowledge System is fully operational and protocol-hardened.
- All session protocols (START/END) are encoded in `AGENTS.md` and `rules/axiom-kb.md` with unified "agent" branding.
- Stale `.antigravity/` references in docs and configurations have been successfully updated to `.agent/` to match actual filesystem structure.
- Hard limits for UI components, icon libraries, and theming are enforced in `rules/agent-limits.md`.
- Standard environment resolves Node/NPX v22.22.2 and v24.10.0 successfully.

## Key Known Issues
- `qmd` execution in agent shell is blocked by macOS `Operation not permitted`, but confirmed working in user terminal.
- Obsidian Local REST API may report offline if Obsidian is closed.
- Sync verification fallback appended `[obsidian-sync: offline]` to log.md.

## Active Threads
- Ready to move into Phase 1: AlphaAXIOM factor library.
- Need to ingest baseline Alpha158 metrics as specified in `docs/PRD.md`.
- Ensure all new frontend tasks follow the Blocks-First workflow.

## Recent Changes
- Standardised internal terminology across the codebase: replaced accidental `Antigravity` and `Claude` references with `agent`/`Agent` in configs, docs, rules, and custom `.agent/` skill definitions.
- Renamed internal `.antigravity/skills/` paths to `.agent/skills/` in rules and behavior guidelines to align with disk realities.
