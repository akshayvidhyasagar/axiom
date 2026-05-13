# AXIOM Onboarding

Read this first if you are: returning after a long absence, a new agent, or unsure where to start.

## What this system is
AXIOM is a quantitative alpha research system. It generates factors, detects market regimes, routes models, constructs portfolios, and simulates execution. The repo is also an Obsidian vault — wiki/ is the living knowledge base.

## Mandatory read order on first contact
1. This file
2. ANTIGRAVITY.md — full agent behavior spec
3. wiki/hot.md — current state snapshot
4. docs/PRD.md — phase checkboxes and acceptance criteria

## What not to touch without reading first
- docs/DECISIONS.md — read before any architectural change
- .raw/ — immutable, never write here
- wiki/log.md and docs/CHANGELOG.md — append only, never edit past entries

## Who owns what
- Phase sign-off: Akshay says "mark Phase N complete" — Antigravity handles all file updates
- wiki/hot.md: Antigravity overwrites each session end
- .raw/: Akshay populates manually via Obsidian Web Clipper
