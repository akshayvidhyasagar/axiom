# Skills Architecture Protocol

This file details protocols for architecture‑related skills.

## Covered Skills
- `improve-codebase-architecture`
- `gitnexus-refactoring`
- `gitnexus-impact-analysis`
- `gitnexus-debugging`
- `gitnexus-exploring`

## Purpose
Guide systematic refactoring, interface deepening, and impact analysis to improve codebase maintainability and testability.

## Trigger Phrases
- User invokes `/improve-codebase-architecture` when modules are shallow or tightly coupled.
- User runs `/gitnexus-refactoring` to rename or split symbols.
- User calls `/gitnexus-impact-analysis` before making breaking changes.
- User uses `/gitnexus-debugging` for bug‑related structural changes.
- User runs `/gitnexus-exploring` to explore architecture.

## Workflow Overview
1. **Analyze Structure** – Run `gitnexus-exploring` to get cohesion scores and module maps.
2. **Identify Refactor Targets** – Highlight shallow interfaces, high coupling, or duplicated logic.
3. **Impact Assessment** – Use `gitnexus-impact-analysis` to assess blast radius.
4. **Plan Refactor** – Draft a step‑by‑step plan with minimal risk.
5. **Execute Refactor** – Apply `gitnexus-refactoring` with dry‑run then apply.
6. **Validate** – Run test suite, ensure no regressions, and verify impact report.
7. **Document** – Record rationale and changes via `save` into the wiki.

## Expected Output
- Architecture analysis report.
- Refactoring plan with ordered actions.
- Impact analysis summary.
- Updated codebase with passing tests.
- Wiki entry documenting the refactor.

## Failure Modes
- Stale GitNexus index – rebuild with `gitnexus-cli`.
- Refactor introduces breaking changes – abort, revert, and re‑analyse.
- Insufficient test coverage – warn and suggest adding tests.

## Combinations
- Often paired with `debugging-protocol.md` when fixing bugs while refactoring.
- May invoke `knowledgebase-protocol.md` for design references.
