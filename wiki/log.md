## [2026-05-26] feat | Audit MCP servers and skills and write protocols [obsidian-sync: offline]
- Audited all 6 MCP servers and 30 custom skills configured under `.agent/skills/`.
- Documented individual protocols for each component in `rules/skill-protocols.md` and `.agent/rules/skill-protocols.md` with zero grouping.
- Established 4 multi-step combination recipes and a summary table.
- Verified header counts match disk counts.

## [2026-05-26] fix | Unify terminology to "agent" and normalize paths [obsidian-sync: offline]
- Standardised internal terminology across the codebase: replaced accidental `Antigravity` and `Claude` references with `agent`/`Agent` in configs, docs, rules, and custom `.agent/` skill definitions.
- Renamed internal `.antigravity/skills/` paths to `.agent/skills/` in rules and behavior guidelines to align with disk realities.
- Updated `wiki/hot.md` to capture recent cache updates.

## [2026-05-26] fix | Repair Broken Obsidian and GitNexus MCP Configurations [obsidian-sync: offline]
- Replaced wrapper-based launch commands in both repository `mcp_config.json` and global `~/.gemini/config/mcp_config.json` with direct execution commands (`npx -y obsidian-mcp` and `npx -y gitnexus mcp`).
- Switched `obsidian` to `obsidian-mcp` via direct `npx` with absolute vault path `/Users/akshayvidhyasagar/AXIOM`.
- Removed stale `.antigravity/scripts/` wrapper directory tree reference from `AGENTS.md` and `docs/ARCHITECTURE.md`.

## [2026-05-25] arch | Shadcn Blocks-First Frontend Protocol Integration
- Codified Shadcn Blocks-First Frontend Protocol across AXIOM
- Added rules/agent-limits.md and rules/mcp-policy.md restrictions
- Updated docs/ARCHITECTURE.md, docs/ONBOARDING.md, and rules/axiom-kb.md

## [2026-05-05] arch | Protocol Hardening
- Encoded live tool gates (GitNexus analyze, qmd query) into session START/END
- Established Skill Invocation Rules and Continuous Wiki Maintenance protocol
- Cleaned root artifacts and synchronized Obsidian plugin state

## [2026-05-04] admin | System Migration
- Migrated knowledge system to `claude-obsidian` standard
- Normalized frontmatter across existing concepts
- Established hot.md and dashboard
