AXIOM Onboarding
Read this first if you are: returning after a long absence, a new agent, or unsure where to start.

What this system is
AXIOM is a quantitative alpha research system. It generates factors, detects market regimes, routes models, constructs portfolios, and simulates execution. The repo is also an Obsidian vault — wiki/ is the living knowledge base.

Mandatory read order on first contact
This file

ANTIGRAVITY.md — full agent behavior spec, session protocol, commit convention

wiki/hot.md — current state snapshot (phase, next step, open issues)

docs/PRD.md — phase checkboxes and acceptance criteria

Key file reference
File Purpose Rule
ANTIGRAVITY.md Agent behavior spec Read fully before any session
wiki/hot.md Live project state Overwritten by Antigravity each session end
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
skills/interrupt/SKILL.md Mid-session interrupt procedure Invoke when session ends without completing goal
rules/mcp-policy.md Permitted operations and hard limits for all MCPs Read before invoking any MCP tool
What not to touch without reading first
docs/DECISIONS.md — read before any architectural change

.raw/ — immutable, never write here under any circumstance

wiki/log.md and docs/CHANGELOG.md — append only, never edit past entries

docs/PRD.md acceptance criteria — never change without a PRD amendment entry in CHANGELOG

Who owns what
Responsibility Owner
Phase sign-off ("mark Phase N complete") Akshay — Antigravity handles all resulting file updates
wiki/hot.md overwrites Antigravity — every session end
.raw/ population Akshay — manually via Obsidian Web Clipper
Obsidian graph view audits Akshay — check for orphan nodes after any wiki compile
Commit authorship Antigravity — follows commit convention in ANTIGRAVITY.md
If something looks wrong
Check wiki/hot.md — does it describe the current state accurately?

Check wiki/log.md — what was the last operation?

Check docs/CHANGELOG.md — what changed in the last session?

If state is inconsistent, do not proceed — surface the discrepancy and ask Akshay before touching any file.
