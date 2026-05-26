# AXIOM — Changelog

All notable changes to this project are documented in this file.  
Format: `[YYYY-MM-DD] Category — Description`

---

## [2026-05-26] Feat — Audited MCP Servers and Skills and Wrote Individual Protocols

- Audited all 6 MCP servers and 30 custom agent skills configured in the Axiom workspace.
- Wrote detailed individual protocols for all components to `rules/skill-protocols.md` and `.agent/rules/skill-protocols.md`.
- Formulated 4 multi-step combination workflows (Feature Build, Hard Bug, Quant Research & Ingest, Refactoring & Code Deepening).
- Verified header counts match skills count on disk with zero grouping violations or placeholder strings.

---

## [2026-05-26] Fix — Unified and Generalized Terminology to 'agent' across configs, docs, and skills

- Normalized internal references to "Antigravity" and "Claude" to "agent"/"Agent" across all rules (`rules/agent-limits.md`, `rules/mcp-policy.md`, `rules/axiom-kb.md`), documentation (`AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/ONBOARDING.md`, `README.md`), and custom skills.
- Generalised file references to target `AGENTS.md` (canonical filename) instead of the obsolete `ANTIGRAVITY.md`.
- Corrected documentation paths to correctly point to `.agent/skills/` instead of the non-existent `.antigravity/skills/` directory on disk.
- Overwrote `wiki/hot.md` to capture recent cache updates.

---

## [2026-05-26] Fix — Repair Broken Obsidian and GitNexus MCP Configurations

- Replaced wrapper-based launch commands in both repository `mcp_config.json` and global `~/.gemini/config/mcp_config.json` with direct execution commands (`npx -y obsidian-mcp` and `npx -y gitnexus mcp`).
- Configured direct launch for `obsidian` using standard `obsidian-mcp` package and absolute vault path `/Users/akshayvidhyasagar/AXIOM`.
- Removed stale `.antigravity/scripts/` wrapper directory tree reference from `AGENTS.md` and `docs/ARCHITECTURE.md` repository diagrams.

---

## [2026-05-04] Scaffolding — AXIOM Knowledge System

### Created
- `docs/PRD.md` — Product requirements with 7 phased build plan, all phases unchecked
- `docs/ARCHITECTURE.md` — System architecture, module map, dependency table
- `docs/DECISIONS.md` — ADR-001 through ADR-006
- `docs/CHANGELOG.md` — This file
- `wiki/INDEX.md` — Obsidian vault entry point with concept page table
- `wiki/.meta/last_compiled` — Wiki compilation timestamp
- `wiki/concepts/qlib-alpha158.md` — Qlib Alpha158 baseline factor set
- `wiki/concepts/regime-detection.md` — HMM regime detection concept
- `wiki/concepts/factor-scoring.md` — Factor IC/ICIR scoring methodology
- `wiki/concepts/polygon-data-layer.md` — Data layer architecture (renamed: covers all data sources)
- `rules/axiom-kb.md` — Antigravity knowledge-base rules
- `skills/llm-wiki-compiler/SKILL.md` — LLM Wiki Compiler skill definition
- `raw/.gitkeep` — Wiki ingestion drop zone
- `README.md` — Project README with architecture, benchmark table, methodology

### Modified
- `ANTIGRAVITY.md` — Optimized with AXIOM-specific context and knowledge system references

### Architectural Decisions Added
- ADR-005: Point-in-time data discipline for all backtests
- ADR-006: Threshold-based signal selection, not rank-based top-N

---

## [2026-05-04] WikiCompile — compiled 4 pages (4 new, 0 updated)

- `wiki/concepts/qlib-alpha158.md` — Alpha158 baseline factor set documentation
- `wiki/concepts/regime-detection.md` — HMM regime detection with validation criteria
- `wiki/concepts/factor-scoring.md` — IC/ICIR factor validation methodology
- `wiki/concepts/polygon-data-layer.md` — Data layer architecture (all free sources)
- `wiki/INDEX.md` — updated with all 4 concept pages
- `wiki/.meta/last_compiled` — set to `2026-05-04T12:08:00+08:00`
- `raw/` — scanned, empty (no new materials to ingest)

---

## [2026-05-04] Maintenance — Permanent Knowledge System Protocol

### Code Changes
- Updated `rules/axiom-kb.md` — encoded full Second Brain maintenance protocol (session start/end, canonical file rules, commit convention)
- Updated `skills/llm-wiki-compiler/SKILL.md` — enhanced with new page template, quality rules, orphan detection, graph hygiene
- Updated `ANTIGRAVITY.md` — added permanent session protocol, commit convention, manual steps for Akshay
- Updated `.gitignore` — added `.gitnexus` to ignored paths

---

## [2026-05-04] Maintenance — Behavioral Guidelines Integration

### Code Changes
- Updated `ANTIGRAVITY.md` — Integrated Karpathy-style behavioral guidelines for reducing common LLM coding mistakes (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution).
- Updated `ANTIGRAVITY.md` — Added step to Session START protocol to strictly follow these guidelines.

---

## [2026-05-05] Maintenance — Protocol Hardening & System Verification

### Code Changes
- Updated `ANTIGRAVITY.md` — Expanded Session START to 7 steps, END to 5 steps. Encoded GitNexus Decision Protocol, Continuous Wiki Maintenance, and Skill Invocation Rules.
- Updated `rules/axiom-kb.md` — Added Session Invariants (non-negotiable START/END routines).
- Updated `docs/ARCHITECTURE.md` — Synchronized repository tree with current wiki structure and claude-obsidian skills.
- Updated `.gitignore` — Added logic to track core Obsidian config while ignoring volatile cache/workspace files.
- Removed legacy artifacts (`llm-wiki-compiler`, `last_compiled.md`) and auto-generated root clutter.

### Infrastructure
- Verified `qmd` global installation.
- Synchronized `.obsidian/plugins` and configurations.

---

## [2026-05-25] Maintenance — Shadcn Blocks-First Protocol Integration

### Code Changes
- Updated `ANTIGRAVITY.md` — Codified the Shadcn Blocks-First Protocol, added aesthetic constraints for Obsidian Dark, and updated repository structure/canonical file rules.
- Updated `rules/mcp-policy.md` — Replaced basic registry policy with a detailed 6-step blocks-first workflow and explicit forbidden rules.
- Updated `docs/ONBOARDING.md` — Expanded the Design System section with the mandatory blocks-first frontend workflow.
- Updated `rules/agent-limits.md` — Added non-negotiable frontend restrictions (mandatory registry searches, no third-party registries, Geist theme variables, Lucide icons only).
- Updated `docs/ARCHITECTURE.md` — Added Frontend Stack section documenting the Vite, Tailwind CSS v4, and shadcn/ui configuration.
- Updated `rules/axiom-kb.md` — Added Shadcn Blocks-First Protocol under Knowledge Rules (R8), integrated shadcn MCP tools under Tooling, and documented file rules.

