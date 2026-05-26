# Core Agent Rules

---
purpose: Permanent always-on rules, limits, and conventions for the AXIOM workspace
when_to_use: Always active in agent context
when_not_to_use: Never deactivated
companion_protocols: "[[protocol-router.md]]"
---

These rules govern every session, every file change, and every git commit. They are non-negotiable and optimized for token limits and high signal.

---

## 1. Terminology & Communication
- **Standardized Naming**: Always refer to yourself as the **agent** or **Agent**. Never use obsolete brandings ("Antigravity", "Claude").
- **Language**: Use clean, technical prose. For token conservation, user commands may activate the `/caveman` skill (terse fragment style), but code and error logs must remain exact.

---

## 2. Hard Boundaries & Write Limits
- **Raw Data Directory (`.raw/`, `data/raw/`)**: Completely immutable. Never write, modify, or delete files in these folders.
- **Append-Only Files**: Never edit past entries in `docs/CHANGELOG.md` or `wiki/log.md`.
- **PRD Sign-Off Gate**: Do not check a phase checkbox in `docs/PRD.md` as complete without:
  1. Running `gitnexus analyze <phase-dir>/` and confirming a clean import graph (no circular deps).
  2. Running `lint wiki` and resolving all orphan pages for modules in that phase.
  3. Verifying all acceptance criteria in `docs/PRD.md` are met.
- **Wiki Deletions**: Never delete a wiki page without first removing all inbound `[[wikilinks]]` and deleting its entry in `wiki/index.md`.
- **Theme Overrides**: Never use hardcoded hex values in UI components. All styling overrides must reference variables in `src/index.css` (Obsidian Dark palette).

---

## 3. Git Commit Conventions
- **Audit Separation**: Never commit canonical documentation (e.g. `docs/`, `wiki/`, `rules/`) in the same commit as code changes. Commit them separately.
- **Commit Message Format**: Follow this exact convention:
  ```
  wiki: ingest <source-title>
  wiki: lint — N fixes
  arch: <change> in ARCHITECTURE.md
  prd: phase N marked complete
  adr: ADR-00N <title>
  feat: <feature> in <module path>
  fix: <description> in <file>
  chore: CHANGELOG + hot.md sync
  ```

---

## 4. Key File Integrity
- **`docs/PRD.md`**: Source of truth for active phases. Update immediately when complete.
- **`docs/ARCHITECTURE.md`**: Rebuild diagrams and tables on any file creation, move, or dependency change.
- **`docs/DECISIONS.md`**: Add an Architecture Decision Record (ADR) on any non-trivial choice or rejected alternative.
- **`docs/CHANGELOG.md`**: Append one summary entry per session if any file was touched.
- **`wiki/hot.md`**: Overwrite completely at session end. Keep under 500 words.
- **`wiki/log.md`**: Chronological record. New entries must be prepended at the TOP.
- **`wiki/index.md`**: Master catalog updated on every ingest or restructure.
