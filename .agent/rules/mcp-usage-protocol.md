# MCP Usage Protocol

---
purpose: Defines when each MCP server may be invoked, permitted operations, and forbidden actions
when_to_use: Before invoking any MCP server tool call
when_not_to_use: For local filesystem edits or plain CLI usage
companion_protocols: "[[core-agent-rules.md]], [[protocol-router.md]]"
---

This protocol outlines boundaries for using AXIOM's MCP servers. You must verify permitted actions before calling any external server.

---

## 1. GitNexus
- **Trigger**: Run before editing any module file, adding dependencies, or before phase completion.
- **Permitted**:
  - `gitnexus analyze <path>` — Read-only import graph and dependency analysis.
  - Blast radius and caller check (`gitnexus_impact`, `gitnexus_context`).
  - Coordinated symbol rename (`gitnexus_rename`) with preview dry-runs.
- **Forbidden**:
  - Do not make architectural changes without filing an ADR if GitNexus reveals circular dependencies.
  - Do not skip GitNexus analyze during Phase Completion Gates (PRD.md checkbox complete).

---

## 2. Obsidian (Local REST API)
- **Trigger**: Active when Obsidian is open and REST API is online.
- **Permitted**:
  - `GET /vault/<path>` — Read any vault file.
  - `PATCH /vault/<path>` (with `Target-Type: frontmatter`) — Patch status, updated, or tags properties.
- **Forbidden**:
  - Do not use the API to write full file content if local filesystem is directly writeable.
  - Do not use when connection is refused (append `[obsidian-sync: offline]` to log).

---

## 3. GitHub MCP
- **Trigger**: Interactive operations with GitHub tracker (issues, PR reviews, comments).
- **Permitted**:
  - Read issues, comments, PR files, and CI run states.
  - Create issues (`/to-issues` task breakdown) and comment triage updates.
- **Forbidden**:
  - Do not commit, branch, or merge pull requests via GitHub MCP.
  - Do not use GitHub MCP as a substitute for local `git log`, `git status`, or `git diff`. All local version control must go through terminal.

---

## 4. Sequential Thinking
- **Trigger**: Reasoning on design problems or bug isolation with >3 unknown variables.
- **Permitted**:
  - Multi-step chain-of-thought blocks for decomposing problems.
- **Forbidden**:
  - Do not invoke for simple fixes, edits, or routine tasks.
  - Do not bypass "Stop on ambiguity — ask" rule. Limit reasoning steps to 3-5 cycles.

---

## 5. Airweave
- **Trigger**: When local wiki searches (`qmd`) are thin and external semantic queries are required.
- **Permitted**:
  - Semantic search across indexed sources and cross-document retrieval.
- **Forbidden**:
  - Do not write Airweave search outputs directly to wiki without running the `wiki-ingest` pipeline.
  - Do not treat search output as canonical without validation.

---

## 6. shadcn / UI Blocks-First Protocol
Mandatory for all frontend development.
- **Tooling Sequence**:
  1. `search_items_in_registries` - Search `registry:block` first (dashboards, sidebars, charts), then `registry:ui` components.
  2. `view_items_in_registries` - Read code and dependencies.
  3. `get_item_examples_from_registries` - Review demo layouts.
  4. `get_add_command_for_items` - Generate installation command.
  5. Run command: `npx shadcn@latest add <item>`
  6. `get_audit_checklist` - Audit post-installation.
- **Aesthetic Constraints (Obsidian Dark)**:
  - Background: `#09090b` | Foreground: `#e4e4e7` | Accent: `#00d4ff` | Card: `#111113` | Border: `hsl(240 4% 14%)`.
  - Apply `.glass-panel` to cards, overlays, and floating frames.
- **Forbidden Patterns**:
  - ❌ Do not code layouts from scratch when shadcn blocks (`sidebar-01` to `sidebar-16`, `dashboard-01`, etc.) exist.
  - ❌ Do not use custom tables or dialogs when primitive registry elements exist.
  - ❌ Do not import non-Lucide icon sets (Lucide only).
  - ❌ Do not hardcode colors in components. Apply only theme CSS variables via `src/index.css`.
