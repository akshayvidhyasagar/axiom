# Usage Matrix

| Component | Type | Purpose | Currently Used? | Reference(s) | Classification |
|-----------|------|---------|-----------------|--------------|----------------|
| gitnexus | MCP Server | Structural analysis of imports and dependencies via `gitnexus analyze` | ✅ (used in session protocol) | `AGENTS.md` steps 5, `rules/mcp-policy.md` | Essential |
| obsidian | MCP Server | Local REST API for Obsidian vault front‑matter patches | ✅ (used in session protocol) | `AGENTS.md` step 7, `rules/mcp-policy.md` | Essential |
| github | MCP Server | Read GitHub issues, PRs, repo metadata | ⚪ (not invoked in current workflow) | None observed | Underused |
| sequential-thinking | MCP Server | Multi‑step reasoning for complex design tasks | ⚪ (no recent usage) | None observed | Underused |
| airweave | MCP Server | Semantic search across external sources for research assistance | ⚪ (rarely used) | None observed | Underused |
| wiki (skill) | Skill | Core wiki operations (ingest, query, lint, fold) | ✅ (core to workflow) | `AGENTS.md`, many sessions | Essential |
| utils/save | Skill | Save current answer as permanent wiki page | ✅ (used via `/save`) | `AGENTS.md` utilities | Essential |
| utils/canvas | Skill | Create/update Obsidian canvas maps | ✅ (used via `/canvas`) | `AGENTS.md` utilities | Essential |
| research/autoresearch | Skill | Autonomous research loop (search, fetch, ingest) | ✅ (used for concept expansion) | `AGENTS.md` research | Essential |
| obsidian/obsidian-markdown | Skill | Interaction with Obsidian markdown via REST API | ✅ (used for front‑matter patches) | `rules/mcp-policy.md` | Essential |
| gitnexus/gitnexus-cli | Skill | Wrapper for `gitnexus` CLI commands | ✅ (used in protocol) | `AGENTS.md` step 5 | Essential |
| gitnexus/gitnexus-debugging | Skill | Debugging guidance for `gitnexus` usage | ⚪ (no observed calls) | None | Underused |
| gitnexus/gitnexus-exploring | Skill | Exploratory usage of `gitnexus` features | ⚪ (no observed calls) | None | Underused |
| gitnexus/gitnexus-guide | Skill | Reference guide for `gitnexus` | ⚪ (no observed calls) | None | Underused |
| gitnexus/gitnexus-impact-analysis | Skill | Impact analysis of changes using `gitnexus` | ⚪ (no observed calls) | None | Underused |
| gitnexus/gitnexus-refactoring | Skill | Refactoring assistance via `gitnexus` | ⚪ (no observed calls) | None | Underused |
| interrupt | Skill | Session interrupt handling protocol | ✅ (used when session ends mid‑task) | `AGENTS.md` interrupt section | Essential |
| mattpocock/* (caveman, diagnose, grill‑me, etc.) | Skill Set | Development utilities for debugging, triage, prototyping, etc. | ⚪ (rarely invoked) | None | Underused |
| shadcn UI blocks & components | MCP Tools (search, view, install, audit) | Front‑end component/library management | ✅ (required for any UI work) | `AGENTS.md` frontend protocol | Essential |

*✅ – observed usage in repository or protocol*\
*⚪ – not observed in current workflows*
