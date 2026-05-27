# AXIOM Knowledge Base Rules

> [!IMPORTANT]
> The AXIOM rules and protocols system has been refactored into a modular, layered structure to optimize context usage and prevent token bloat. 
> 
> Do not refer to this file for active operational rules. Instead, consult the new modular protocol files under `.agent/rules/`:

## New Protocol Architecture

### 1. Always-Active Core Rules
- **Core Agent Rules**: [.agent/rules/core-agent-rules.md](file:///.agent/rules/core-agent-rules.md) (terminology, write boundaries, limits, commit conventions).
- **Protocol Router**: [.agent/rules/protocol-router.md](file:///.agent/rules/protocol-router.md) (trigger conditions, scenario-to-protocol dispatch tables).

### 2. Execution Protocols (On-Demand)
- **Planning Protocol**: [.agent/rules/planning-protocol.md](file:///.agent/rules/planning-protocol.md) (design planning, PRDs, ticketing breakdowns).
- **Debugging Protocol**: [.agent/rules/debugging-protocol.md](file:///.agent/rules/debugging-protocol.md) (bug isolation loops, TDD, instrumentations, profiling).
- **Architecture Protocol**: [.agent/rules/architecture-protocol.md](file:///.agent/rules/architecture-protocol.md) (refactoring methodology, renames, module splits, structural analysis).
- **Research Protocol**: [.agent/rules/research-protocol.md](file:///.agent/rules/research-protocol.md) (web searches, fetches, autonomous research loops).
- **Documentation Protocol**: [.agent/rules/documentation-protocol.md](file:///.agent/rules/documentation-protocol.md) (wiki notes, index cataloging, visual canvases).

### 3. Tool & Skill Protocols (On-Demand)
- **MCP Usage Protocol**: [.agent/rules/mcp-usage-protocol.md](file:///.agent/rules/mcp-usage-protocol.md) (permitted/forbidden rules for GitHub, Obsidian API, GitNexus, shadcn).
- **Skills & MCP Index**: [.agent/rules/skills-mcp-index.md](file:///.agent/rules/skills-mcp-index.md) (concise reference table mapping all thematic skills to canonical protocol files).
