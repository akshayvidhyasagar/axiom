AXIOM Onboarding
Read this first if you are: returning after a long absence, a new agent, or unsure where to start.

What this system is
AXIOM is a quantitative alpha research system. It generates factors, detects market regimes, routes models, constructs portfolios, and simulates execution. The repo is also an Obsidian vault — wiki/ is the living knowledge base.

Mandatory read order on first contact
This file

AGENTS.md — full agent behavior spec, session protocol, commit convention

wiki/hot.md — current state snapshot (phase, next step, open issues)

docs/PRD.md — phase checkboxes and acceptance criteria

Key file reference
File Purpose Rule
AGENTS.md Agent behavior spec Read fully before any session
wiki/hot.md Live project state Overwritten by the agent each session end
docs/PRD.md Phase checkboxes Source of truth for what is done vs. pending
docs/CHANGELOG.md Session history Append only — never edit past entries
docs/ARCHITECTURE.md Module map and dependency graph Rebuild affected section on any file create/move/delete
docs/DECISIONS.md Architecture decision records Read before any non-trivial implementation choice
docs/ONBOARDING.md This file Update if system structure changes significantly
wiki/log.md Operation log Append only — new entries at TOP
wiki/index.md Master wiki catalog Update on every ingest or wiki restructure
wiki/gaps/_index.md Open questions and unresolved issues Add gaps as discovered; resolve inline
wiki/meta/session-log-template.md hot.md fill-in template Use at every session end
rules/agent-limits.md Hard behavioral limits Non-negotiable — read before any destructive operation
.agent/skills/interrupt/SKILL.md Mid-session interrupt procedure Invoke when session ends without completing goal
rules/mcp-policy.md Permitted operations and hard limits for all MCPs Read before invoking any MCP tool
.agents/skills/ mattpocock/skills Engineering and productivity skill workflows (TDD, diagnose, triage, etc.)
What not to touch without reading first
docs/DECISIONS.md — read before any architectural change

.raw/ — immutable, never write here under any circumstance

wiki/log.md and docs/CHANGELOG.md — append only, never edit past entries

docs/PRD.md acceptance criteria — never change without a PRD amendment entry in CHANGELOG

Who owns what
Responsibility Owner
Phase sign-off ("mark Phase N complete") Akshay — the agent handles all resulting file updates
wiki/hot.md overwrites agent — every session end
.raw/ population Akshay — manually via Obsidian Web Clipper
Obsidian graph view audits Akshay — check for orphan nodes after any wiki compile
Commit authorship agent — follows commit convention in AGENTS.md
If something looks wrong
Check wiki/hot.md — does it describe the current state accurately?

Check wiki/log.md — what was the last operation?

Check docs/CHANGELOG.md — what changed in the last session?

## Design System — Shadcn Blocks-First Protocol

AXIOM uses **shadcn/ui** as its mandatory frontend design system with a **blocks-first** approach. All frontend UI must be composed from shadcn registry items before writing custom code.

### Quick Reference

| What | Where |
|------|-------|
| Full protocol spec | `AGENTS.md → Shadcn Blocks-First Frontend Protocol` |
| MCP permitted operations | `rules/mcp-policy.md → shadcn/ui` |
| Theme variables | `src/index.css` |
| Registry config | `components.json` (root) |
| Installed components | `components/ui/` |
| Utilities | `lib/utils` |

### Blocks-First Workflow (mandatory for all UI work)

1. **Search blocks first** — Use `search_items_in_registries` to find `registry:block` items (dashboards, sidebars, charts, login pages).
2. **Fall to components** — If no block matches, search for `registry:ui` primitives (button, dialog, table).
3. **View examples** — Use `get_item_examples_from_registries` to study usage patterns.
4. **Install via MCP** — Use `get_add_command_for_items` to generate and run the install command.
5. **Audit** — Run `get_audit_checklist` after every installation.

### Rules

- Never build from scratch if a shadcn block or component exists.
- Never hardcode colors — use CSS variables from `src/index.css`.
- Never edit `components/ui/` files unless strictly necessary for Obsidian Dark theme overrides.
- Follow the aesthetic constraints in `AGENTS.md`.
- Always verify component installation with the audit checklist.
- Only the `@shadcn` registry is permitted — no third-party registries without Akshay approval.

If state is inconsistent, do not proceed — surface the discrepancy and ask Akshay before touching any file.

