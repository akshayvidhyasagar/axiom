# LLM Wiki Compiler

> Skill: Compile research materials into Obsidian-compatible wiki pages

## Trigger

User says: "compile wiki"

## Procedure

1. **Check timestamp:** Read `wiki/.meta/last_compiled` for the last compilation date.

2. **Scan ingestion zone:** List all files in `raw/` (papers, docs, findings, notes).
   - If `raw/` is empty or contains only `.gitkeep`, skip ingestion but still proceed to verification.
   - If new files exist since `last_compiled`, process them.

3. **Process new materials:** For each new file in `raw/`:
   - Extract key concepts, definitions, and relationships
   - Determine if a new concept page is needed or if an existing page should be updated
   - Generate/update wiki pages in `wiki/concepts/` using the template below

4. **Verify cross-links:** For every page in `wiki/concepts/`:
   - Ensure the `> Related:` header contains valid `[[wikilinks]]` to related concepts
   - Ensure no broken links exist (every `[[target]]` must have a corresponding `wiki/concepts/target.md`)
   - Ensure no absolute file paths or markdown-style links are used

5. **Update INDEX.md:** Verify `wiki/INDEX.md` contains a row for every concept page with:
   - Page name (as wikilink)
   - One-line summary
   - Relevant AXIOM phase number

6. **Update timestamp:** Write current ISO 8601 timestamp to `wiki/.meta/last_compiled`

7. **Log:** Append a WikiCompile entry to `docs/CHANGELOG.md`:
   ```
   ## [YYYY-MM-DD] WikiCompile — compiled N pages (M new, K updated)
   ```

## Concept Page Template

```markdown
# {Concept Name}

> Related: [[related-concept-1]], [[related-concept-2]]

## What It Is

{2-3 sentence definition}

## Role in AXIOM

{How this concept fits into the AXIOM architecture}

## Key Details

{Technical specifics, formulas, configuration}

## References

{Links to papers, documentation, source code}
```

## Constraints

- All internal links must use `[[wikilinks]]` format, never `[text](path)` format
- No absolute file paths in any wiki page
- Concept page filenames must be lowercase-kebab-case (e.g., `regime-detection.md`)
- Each page must have exactly one `> Related:` line as the first content after the title
