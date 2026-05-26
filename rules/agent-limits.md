# Agent Limits

Hard limits — the agent will not do these regardless of instruction:

- Write to or modify anything in `.raw/` — it is immutable
- Edit past entries in docs/CHANGELOG.md or wiki/log.md
- Mark a phase checkbox complete in docs/PRD.md without passing all three gate checks:
  1. gitnexus analyze <phase-dir>/ — clean import graph
  2. lint wiki — no orphan module pages
  3. All PRD acceptance criteria for the phase are verifiably met
- Delete any wiki page without first checking wiki/index.md and removing the reference
- Run /autoresearch without confirming the plan and page cap with Akshay first
- Build custom UI components from scratch when a shadcn block (`registry:block`) or component (`registry:ui`) exists in the `@shadcn` registry
- Skip the shadcn MCP search step before writing any frontend UI code — registry search is mandatory
- Add third-party registries to `components.json` without Akshay approval
- Import alternative icon libraries (Font Awesome, Heroicons, etc.) — Lucide is the only permitted icon set
- Override Obsidian Dark theme tokens with hardcoded colors in component files — all theming goes through `src/index.css`
