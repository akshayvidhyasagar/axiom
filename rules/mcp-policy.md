# MCP Usage Policy

This file defines when each MCP may be invoked, what operations are permitted, and what is forbidden.
Read this before using any MCP tool. Do not improvise MCP behavior from training defaults.

***

## GitNexus

**Trigger:** Before editing any module file, adding a dependency, completing a phase, or any time structure feels uncertain.
See ANTIGRAVITY.md → GitNexus Decision Protocol for full trigger table.

**Permitted:**
- `gitnexus analyze <path>` — read-only structural analysis
- Import graph inspection
- Circular dependency detection

**Forbidden:**
- Do not use GitNexus output to make architectural decisions without filing an ADR if a circular dep or unexpected coupling is found
- Do not skip GitNexus on phase completion gate — it is mandatory

***

## Obsidian (Local REST API)

**Trigger:** When Obsidian is open and Local REST API is confirmed online (Step 7 of START protocol).
Use for frontmatter patches only — do not rewrite full files via API when filesystem write is available.

**Permitted:**
- `GET /vault/<path>` — read any file in the vault
- `PATCH /vault/<path>` with `Target-Type: frontmatter` — patch individual frontmatter fields (status, updated, tags)
- Sync verification at session start

**Forbidden:**
- Do not use the API to write full file content if the filesystem is directly accessible — use filesystem writes instead
- Do not use the API when offline fallback has triggered (`[obsidian-sync: offline]` in log.md)
- Never write to `.raw/` via API or any other method

***

## GitHub MCP

**Trigger:** Only when task explicitly requires reading GitHub context unavailable locally — open issues, PR descriptions, review comments, CI status.

**Permitted (read only):**
- Read issues and issue comments
- Read PR descriptions, review threads, CI check status
- Read repo metadata (labels, milestones)

**Forbidden:**
- Do not create, edit, or close issues or PRs via GitHub MCP
- Do not push commits, create branches, or merge PRs via GitHub MCP
- All commits must go through plain `git` CLI following the commit convention in ANTIGRAVITY.md
- Do not use GitHub MCP as a substitute for local `git log`, `git status`, or `git diff`

**Default:** When in doubt, use local git. GitHub MCP is supplementary context only.

***

## Sequential Thinking

**Trigger:** Only for tasks with genuine multi-step reasoning complexity — architectural decisions, debugging a non-obvious failure, designing a new module, evaluating competing approaches.

**Permitted:**
- Multi-step reasoning chains for complex design or debugging tasks
- Structured decomposition of ambiguous requirements before coding

**Forbidden:**
- Do not invoke for routine tasks: file edits, wiki updates, commit operations, simple bug fixes
- Do not use Sequential Thinking as a substitute for asking Akshay when the blocker is a missing decision, not a reasoning gap
- Do not let Sequential Thinking output bypass the "Stop on ambiguity — ask" rule in Engineering Principles

**Signal to invoke:** If the task has more than 3 interdependent unknowns and all of them are resolvable through reasoning alone (not through asking Akshay), invoke Sequential Thinking.

***

## Airweave

**Trigger:** When searching for prior context across ingested sources, past research, or cross-document synthesis that `qmd wiki/ "<query>"` cannot resolve from the local wiki alone.

**Permitted:**
- Semantic search across indexed sources
- Cross-document retrieval to inform wiki ingest or autoresearch
- Surfacing prior findings before starting a new research task

**Forbidden:**
- Do not use Airweave as a substitute for reading hot.md, index.md, or local wiki pages — local wiki is always checked first
- Do not ingest Airweave results directly into wiki without running the full ingest procedure (`skills/wiki-ingest/SKILL.md`)
- Do not treat Airweave results as canonical — they are retrieval hints, not ground truth

**Read order when Airweave is invoked:**
1. `qmd wiki/ "<query>"` first — check local wiki
2. If local wiki is insufficient, query Airweave
3. Synthesize both before acting

***

## General MCP Rules (all tools)

- Prefer local filesystem and CLI over MCP when both can accomplish the task
- If an MCP call fails, log the failure in wiki/log.md and fall back to the non-MCP equivalent
- Never chain multiple MCP calls without checking intermediate results
- MCP tool usage does not replace the START/END/INTERRUPT protocol — all session rules still apply regardless of which tools are used

***

## shadcn/ui (Registry & Component Management)

**Trigger:** Mandatory for all frontend UI development. Use before adding any new visual component, layout primitive, or block.

**Permitted:**
- `shadcn add <component>` — Installing verified components from the registry
- `shadcn add <block>` — Composing full UI blocks (Sidebars, Settings, Forms)
- Theme inspection via registry search

**Forbidden:**
- Do not create custom UI components from scratch if a shadcn equivalent exists
- Do not manually edit files in `components/ui/` unless strictly necessary for the obsidian theme override
- Do not use Tailwind utility classes for high-level layouts (cards, dialogs) when a shadcn component is available

**Design Standard:** All components must follow the **Obsidian Dark** theme variables defined in `src/index.css`.
