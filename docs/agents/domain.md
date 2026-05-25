# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`docs/DECISIONS.md`** - read the architectural decisions and history that touch the area you are about to work in.
- **`wiki/`** - check the wiki notes (or specific decisions in `wiki/decisions/` or `rules/`) if you need more system context.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skill (`/grill-with-docs`) creates them lazily when terms or decisions actually get resolved.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`).

## Flag ADR/Decision conflicts

If your output contradicts an existing decision in `docs/DECISIONS.md`, surface it explicitly rather than silently overriding:

> _Contradicts Decision <Number/Title> (e.g. event-sourced orders) — but worth reopening because…_
