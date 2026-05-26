---
type: meta
title: "Hot Cache"
updated: 2026-05-26
---

# Recent Context

## Last Updated
2026-05-26 — Fix broken Obsidian and GitNexus MCP configurations.

## Current State
- AXIOM Knowledge System is fully operational and protocol-hardened.
- All session protocols (START/END) are encoded in `AGENTS.md` and `rules/axiom-kb.md`.
- Obsidian and GitNexus MCP configurations have been repaired, bypassing the non-existent `.antigravity/scripts/` wrapper scripts in favor of direct execution commands (`npx -y obsidian-mcp` and `npx -y gitnexus mcp`).
- Standard environment resolves Node/NPX v22.22.2 and v24.10.0 successfully.
- Hard limits for UI components, icon libraries, and theming are enforced in `rules/agent-limits.md`.

## Key Known Issues
- `qmd` execution in agent shell is blocked by macOS `Operation not permitted`, but confirmed working in user terminal.
- Obsidian Local REST API may report offline if Obsidian is closed.
- Sync verification fallback appended `[obsidian-sync: offline]` to log.md.

## Active Threads
- Ready to move into Phase 1: AlphaAXIOM factor library.
- Need to ingest baseline Alpha158 metrics as specified in `docs/PRD.md`.
- Ensure all new frontend tasks follow the Blocks-First workflow.

## Recent Changes
- Fixed local `mcp_config.json` and global `~/.gemini/config/mcp_config.json` to launch `gitnexus` and `obsidian` MCP servers directly using direct `npx` commands.
- Removed obsolete `mcp-wrapper.js` and `airweave-wrapper.js` from `AGENTS.md` and `docs/ARCHITECTURE.md` repository tree diagrams.
