---
type: meta
title: "Hot Cache"
updated: 2026-05-26
---

# Recent Context

## Last Updated
2026-05-26 — Audited all configured MCP servers and 30 agent skills, and wrote comprehensive protocols to rules/skill-protocols.md.

## Current State
- All 6 MCP servers and 30 skills under `.agent/skills/` have been mapped, verified, and documented individually.
- The protocols have been verified to have exactly 36 level-3 headers with zero grouping violations and zero placeholder text.
- A summary matrix and 4 multi-step combination workflows have been added.
- Workspaces and rules are fully synced.

## Key Known Issues
- Obsidian Local REST API may report offline if Obsidian is closed; sync fallback is active.

## Active Threads
- Ready for quant trading Phase 1 (AlphaAXIOM factor library) or Phase 2 (regime detection) feature development using the newly documented combination recipes.

## Recent Changes
- Re-wrote `rules/skill-protocols.md` from scratch to cover every skill individually with concrete, Axiom-specific triggers, workflows, expected outputs, and combinations.
- Saved a duplicate copy to `.agent/rules/skill-protocols.md` to satisfy project configurations.
- Verified header counts match SKILL.md counts on disk.
