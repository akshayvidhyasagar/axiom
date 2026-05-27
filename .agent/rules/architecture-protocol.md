# Architecture & Refactoring Protocol

---
purpose: Guidelines for system modularity, interface design, blast radius analysis, and coordinated refactoring
when_to_use: When changing interfaces, splitting modules, resolving circular dependencies, or running architectural audits
when_not_to_use: For trivial syntax fixes, simple bug patches, or documentation-only runs
companion_protocols: "[[core-agent-rules.md]], [[mcp-usage-protocol.md]]"
relevant_mcps: gitnexus
relevant_skills: "/improve-codebase-architecture, gitnexus-refactoring, gitnexus-impact-analysis, gitnexus-exploring"
---

This protocol outlines how to maintain design integrity, analyze architectural coupling, perform safe large-scale refactorings, and document system boundaries.

---

## 1. Modularity & Interface Design Principles
- **Deep Modules**: Prefer modules that provide rich functionality behind simple interfaces. Avoid creating "shallow" modules that add boilerplate or wrapping without real abstraction.
- **High Cohesion & Low Coupling**: Keep related logic together within a module. Minimize inter-module dependencies and strictly prevent circular imports.
- **Architectural Checkpoints**:
  1. Always run `gitnexus analyze` before finalizing module splits or additions.
  2. If the tool detects circular dependencies, you must resolve them before proceeding.
  3. Non-trivial modular changes or new libraries must be backed by an ADR in `docs/DECISIONS.md`.

---

## 2. Coordinated Refactoring & Renames
- **Blast Radius Analysis**: Before modifying any public class, function, or database schema, you must map out all callers. Do not guess the impact.
- **Rename Protocols**:
  - Always run a GitNexus rename dry-run preview (`gitnexus_rename` with preview) before executing.
  - Review all affected references across files to ensure semantic consistency.
  - Never split or rename symbols while tests are failing. Always refactor in a GREEN state.

---

## 3. Refactoring & Code Deepening Recipe
1. **gitnexus-impact-analysis** - Trace upstream call chains and blast radius of the target changes.
2. **/improve-codebase-architecture** - Scan for shallow interfaces or structural weaknesses.
3. **/grill-with-docs** - Interview the user if interface boundaries or glossary normalizations require alignment.
4. **gitnexus-refactoring** - Apply coordinated dry-run renames/splits, review the diff, then execute.

---

## 4. Architecture Skills Reference Catalog

This catalog details the specific commands, triggers, expected outputs, and operational parameters for architecture and refactoring skills.

### Covered Skills & Tools
- `/improve-codebase-architecture` (Structural optimization analysis and HTML cards UI view)
- `gitnexus-exploring` (Read-only visual module mapping and cohesion auditing)
- `gitnexus-impact-analysis` (Assess public symbol change blast radius)
- `gitnexus-refactoring` (Coordinated multi-file symbol splits and renames)

### Triggers & Usage
- **Modularity Audits**: Invoke `/improve-codebase-architecture` when modules are shallow, tightly coupled, or duplicated code is detected.
- **Dependency Inquiries**: Invoke `gitnexus-exploring` to visualize dependency maps or look for circular import paths.
- **Change Planning**: Invoke `gitnexus-impact-analysis` before changing a public API or signature.
- **Executing Refactors**: Invoke `gitnexus-refactoring` to perform coordinated renames or extract modules.

### Expected Output & Artifacts
- **Cohesion Report**: Cohesion scores, coupling factors, and target improvement lists.
- **Blast Radius Summary**: List of all affected source files and lines requiring adjustments.
- **Refactoring Diff**: A preview dry-run showing exact token replacements before execution.
- **Wiki Entry**: Updated glossary or architecture description documented via `/save` into the wiki.

### Failure Modes & Remediation
- **Stale Analyzer Index**: If GitNexus misses new modules, run the indexing command (`gitnexus analyze`) to rebuild the graph.
- **Breaking Structural Regression**: If a split breaks dependencies, revert changes immediately, return to a green test baseline, and refine the plan.
- **Insufficient Test Seams**: If a module lacks integration tests, flag the risk, construct mock-based harnesses, and verify basic behavior before refactoring.
