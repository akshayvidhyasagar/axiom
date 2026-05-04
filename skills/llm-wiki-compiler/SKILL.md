# LLM Wiki Compiler

> Skill: Compile research materials into Obsidian-compatible wiki pages

## Trigger

- User says: "compile wiki"
- A build phase is completed
- New files appear in `raw/`

## Procedure

1. **Check timestamp:** Read `wiki/.meta/last_compiled` for the last compilation date.

2. **Scan ingestion zone:** Find all files in `raw/` modified after that timestamp.
   - If `raw/` is empty or contains only `.gitkeep`, skip ingestion but still proceed to verification.
   - Subdirectories: `raw/papers/`, `raw/findings/`, `raw/docs/` — scan all.

3. **Process new materials:** For each new source file:
   a. Summarize the core concept
   b. Identify which `wiki/concepts/` page it belongs to (create if none exists)
   c. Add content under the correct heading — **do not overwrite existing content**, append or merge
   d. Add `[[wikilinks]]` to related pages
   e. Add backlinks on those related pages

4. **Check for orphans:** Pages with no incoming `[[wikilinks]]` from other pages — flag them with `> Status: Orphan — needs incoming links`

5. **Update INDEX.md:** Verify `wiki/INDEX.md` contains a row for every concept page with:
   - Page name (as `[[wikilink]]`)
   - One-line summary
   - Relevant AXIOM phase number

6. **Update timestamp:** Write current ISO 8601 timestamp to `wiki/.meta/last_compiled`

7. **Log:** Append WikiCompile entry to `docs/CHANGELOG.md`:
   ```
   ## [YYYY-MM-DD] WikiCompile — compiled N pages (M new, K updated)
   ```

## New Page Template

```markdown
# <Concept Name>

> Source: <raw/ file or external source>
> Related: [[concept-a]], [[concept-b]]
> Status: (remove this line when complete)

## What It Is

<2-3 sentence synthesis — not a copy of the source>

## Key Details

<Structured content — tables for comparisons, code blocks for formulas/pseudocode>

## AXIOM Relevance

**Module:** `<path/to/module.py>`
**Phase:** Phase N — <phase name>
**How it's used:** <specific implementation detail>

## Open Questions

- <anything unresolved>
```

## Wiki Page Quality Rules

- Every page **must** have `> Related: [[page1]], [[page2]]` at the top
- Every page **must** have an "AXIOM Relevance" section — how this concept maps to a specific module and phase
- No page should be a copy-paste of a source — it must be **synthesized and specific to AXIOM**
- Pages should link OUT generously; any concept mentioned that has its own page gets a `[[wikilink]]`
- Flag stubs with `> Status: Stub — needs expansion` at the top

## Obsidian Compatibility Rules

- All internal links **MUST** use `[[wikilinks]]` format — never `[text](path.md)`
- No absolute file paths anywhere in `wiki/`
- Filenames: lowercase, hyphenated (e.g., `regime-detection.md`) — Obsidian is case-sensitive
- `wiki/INDEX.md` is the vault entry point — every new page must be linked from it
- Use `##` headers inside pages, not `#` (the page title IS the H1 via the filename)
- Tables use standard markdown format (Obsidian renders them)
- Put formulas in code blocks — Obsidian doesn't render LaTeX by default

## Graph View Hygiene

After each compile, check for:
- **Isolated nodes** (orphans) — flag if any concept page has no connections
- **Hub pages** — `qlib-alpha158` and `factor-scoring` should be the most-linked pages
- **Missing links** — if two pages discuss the same concept but don't link each other, add the link
