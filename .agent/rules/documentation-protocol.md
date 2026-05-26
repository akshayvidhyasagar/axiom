# Documentation & Wiki Protocol

---
purpose: Guidelines for wiki indexing, ingestion delta checks, address counters, lint checks, fold rollups, and canvases
when_to_use: When writing wiki pages, updating logs, running index/lint checks, or organizing visual canvases
when_not_to_use: For coding implementations or standard command executions
companion_protocols: "[[core-agent-rules.md]], [[mcp-usage-protocol.md]]"
relevant_mcps: obsidian
relevant_skills: "wiki-ingest, wiki-query, wiki-lint, wiki-fold, /save, /canvas, obsidian-markdown"
---

This protocol outlines how to maintain the AXIOM wiki vault, write correct Obsidian markdown, allocate addresses, audit vault health, and visually map concepts.

---

## 1. Obsidian Flavored Markdown (OFM)
Ensure all pages use proper Obsidian syntax:
- **Wikilinks**: Use double brackets `[[Note Name]]` or `[[Note Name|Display Text]]`. Match filename exactly. No path names needed unless resolving duplicate filenames.
- **Embeds**: Prepend an exclamation mark `![[image.png]]` or `![[Note Name#Heading]]`.
- **Properties (YAML Frontmatter)**: Flat properties only. Dates must be `YYYY-MM-DD`. Lists use `- item` format. Quote wikilinks: `related: - "[[Other Note]]"`.
- **Callouts**: Format blockquotes using `> [!type] Title`. Supported types: `note`, `warning`, `failure`, `bug`, `example`, `question`, and custom `[!contradiction]` or `[!gap]`.

---

## 2. Ingest & Query Workflows

### Delta Tracking (`wiki-ingest`)
- Compare MD5 file hashes against `.raw/.manifest.json` before processing. Skip if unchanged unless re-ingest is forced.
- Record created/updated pages in the manifest after processing.

### DragonScale Address Counter (Mechanism 2)
- New non-meta pages created on or after **2026-04-23** must have an address in frontmatter (e.g. `address: c-000042`).
- Call `./scripts/allocate-address.sh` (atomic counter) to reserve. Never edit `.vault-meta/address-counter.txt` via Write/Edit tools.
- Map old paths to new paths in `address_map` during renames. Exclude index, fold, and legacy files.

### Query Modes (`wiki-query`)
- *Quick Mode*: Read `wiki/hot.md` and `wiki/index.md` only. No page openings.
- *Standard Mode*: Read hot cache, index, and 3-5 relevant pages. Cite with wikilinks.
- *Deep Mode*: Read hot cache, index, and all relevant pages across vault. File synthesis results back to vault.

---

## 3. Linting & Fold Rollups

### Vault Auditing (`wiki-lint`)
Run weekly or before phase transitions. Audits:
- Orphans, dead links, stale claims, frontmatter gaps, and index alignment.
- *Address validation*: Flag missing addresses on post-rollout files as errors.
- *Semantic Tiling*: Check duplicate similarity using local Ollama model (`tiling-check.py`). Map error bands (`>=0.90`) and review bands (`0.80-0.90`).

### Chronological Rollups (`wiki-fold`)
Roll up `2^k` entries in `wiki/log.md`:
- *Dry-run*: Stdout output only. Do not write files (avops PostToolUse hook triggers).
- *Commit*: Write page to `wiki/folds/{FOLD-ID}.md`, update `wiki/index.md` folds section, and append log.

---

## 4. Visual Canvases & Dashboards
- **Canvases**: Obsidian canvases are JSON visual maps. Calculate coordinates dynamically to prevent overlaps, using timestamp IDs to avoid collisions. Save to `wiki/canvases/`.
- **Dashboards**: Maintain `wiki/meta/dashboard.md` with Dataview code blocks to track seeds, activity, and open gaps.

---

## 5. Documentation Recipes

### Wiki Integration & Rollup Recipe
1. **/autoresearch** - Run search and fetch rounds on a quant concept.
2. **wiki-ingest** - Run manifest checks, create summaries/entities, and allocate addresses.
3. **wiki-lint** - Check vault links, address uniqueness, and run semantic tiling duplicate checks.
4. **wiki-fold** - Compile chronological rollups for the completed batch.

### Refactoring & Code Deepening Recipe
1. **gitnexus-impact-analysis** - Trace upstream call chains and blast radius.
2. **/improve-codebase-architecture** - Search for shallow modules and present HTML candidates card view.
3. **/grill-with-docs** - Interview user, update `CONTEXT.md` glossary, and write ADRs in `docs/DECISIONS.md`.
4. **gitnexus-refactoring** - Apply coordinated renames or splits, and run `gitnexus_detect_changes`.
