# Skills Planning Protocol

This file contains the detailed protocol for all planning‑related skills.

## Covered Skills
- `grill-me`
- `grill-with-docs`
- `to-prd`
- `to-issues`
- `tdd`
- `prototype`
- `write-a-skill`

## Purpose
Guides the creation of implementation plans, PRDs, issue breakdowns, test‑driven development loops, and interactive design interviews.

## Trigger Phrases
- User invokes `/grill-me` or `/grill-with-docs`.
- User requests `/to-prd` or `/to-issues`.
- User starts a `/tdd` workflow.
- User runs `/prototype` for throw‑away validation.
- User calls `write-a-skill` to scaffold a new skill.

## Workflow Overview
1. **Clarify Requirements** – Ask the user for any missing details.
2. **Draft Plan / PRD** – Generate a concise plan with goals, acceptance criteria, and task breakdown.
3. **Decompose into Issues** – Create vertical tracer‑bullet issues.
4. **TDD Loop** – Write a failing test, implement minimal code, refactor.
5. **Prototype (Optional)** – Scaffold quick prototype to validate assumptions.
6. **Review & Approval** – Present the plan for user approval before proceeding.

## Expected Output
- Structured implementation plan markdown.
- PRD ticket created in the issue tracker.
- List of issues with dependencies.
- Initial test files for TDD.
- Optional prototype files placed in a `prototype/` directory.

## Failure Modes
- Ambiguous requirements – abort and ask clarifying questions.
- Missing test framework – report and suggest setup.
- Conflict with existing issues – highlight and request resolution.

## Combinations
- Often combined with `debugging-protocol.md` for bug‑fix planning.
- May invoke `knowledgebase-protocol.md` to fetch background information.
