# AXIOM — Changelog

All notable changes to this project are documented in this file.  
Format: `[YYYY-MM-DD] Category — Description`

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

