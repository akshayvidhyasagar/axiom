# AXIOM — AlphaAXIOM Trading System

**Agent:** agent
**Mode:** B (GitHub/Repo) + E (Research)
**Owner:** Akshay Vidhyasagar
**Purpose:** Quantitative alpha research — factor generation, regime detection, model routing, portfolio construction, execution simulation

---

## Session Protocol

### START (every session, no exceptions — execute all 7 steps before touching any file)

1. **Git state check**
   ```bash
   git log --oneline -5
   git status
   ```
   If there are uncommitted changes from a previous session, commit them first:
   ```bash
   git add -A && git commit -m "chore: uncommitted changes from previous session"
   ```
   Confirm permitted MCP operations in `.agent/rules/mcp-usage-protocol.md` before invoking any tools.

2. **Read wiki/hot.md** — 500-word context cache. This is the primary bootstrap. Read fully before anything else.

3. **Read docs/PRD.md** — only if hot.md indicates a phase transition is imminent or the current phase is ambiguous. Otherwise, use hot.md's phase summary and skip to Step 4.

4. **Read docs/CHANGELOG.md last 3 entries** — understand what changed recently and what was left incomplete.

5. **Run GitNexus on active phase directory**
   ```bash
   gitnexus analyze <active-phase-dir>/
   ```
   If Phase 0: `gitnexus analyze .` (whole repo — no code yet)
   Report the import graph and any structural issues before proceeding.

6. **Query wiki for relevant concepts**
   If the task touches any concept (regime, factors, signals, portfolio, execution):
   ```bash
   $QMD wiki/ "<concept keyword>"
   ```
   Then read the returned pages. Maximum 5 pages per query.

7. **Check Obsidian sync** (if Local REST API is online)
   ```bash
   curl -sk -H "Authorization: Bearer $OBSIDIAN_KEY" "https://127.0.0.1:27124/vault/wiki/hot.md" | head -30
   ```
   Confirm Obsidian and filesystem are in sync. If they diverge, filesystem is canonical. If the curl returns an error or connection is refused, skip this step and append `[obsidian-sync: offline]` to the session's log.md entry. Filesystem is canonical regardless.

### END (every session where any file was touched — all 5 steps mandatory)

1. **Overwrite wiki/hot.md completely**
   - Under 500 words
   - Sections: Last Updated, Current State, Key Known Issues, Active Threads, Recent Changes
   - Reflect actual current state — not aspirational

2. **Append to docs/CHANGELOG.md**
   Format:
   ```
   ## [YYYY-MM-DD] — <session summary in one line>
   - <bullet per meaningful change>
   ```
   Never edit past entries.

3. **Append to wiki/log.md at TOP**
   Format: `## [YYYY-MM-DD] <operation type> | <title>`
   Operation types: ingest | query | lint | migration | arch | feat | fix | chore

4. **Update wiki/index.md** if any wiki pages were created, modified, or deleted.

5. **Commit**
   ```bash
   git add -A
   git commit -m "<type>: <description>"
   ```
   Use commit convention from `.agent/rules/core-agent-rules.md`. Canonical doc changes in separate commits from code.

### INTERRUPT (if session ends mid-task without completing the goal)

1. Write current task state under "Active Threads" in wiki/hot.md — what was in progress, what is blocked, what the next concrete step is.
2. Commit with: `chore: interrupt — <one line on what was left incomplete>`
Do not run the full END protocol on an interrupted session. hot.md entry is mandatory regardless.

---

## Engineering Principles

These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding
*Don't assume. Don't hide confusion. Surface tradeoffs.*
- **State assumptions explicitly.** If uncertain, ask.
- **Present alternatives.** If multiple interpretations exist, present them — don't pick silently.
- **Push back for simplicity.** If a simpler approach exists, say so.
- **Stop on ambiguity.** If something is unclear, name what's confusing. Ask.

### 2. Simplicity First
*Minimum code that solves the problem. Nothing speculative.*
- **No gold-plating.** No features beyond what was asked.
- **No premature abstraction.** No abstractions for single-use code.
- **No unnecessary flexibility.** No "configurability" that wasn't requested.
- **Sane error handling.** No error handling for impossible scenarios.
- **Conciseness.** If you write 200 lines and it could be 50, rewrite it.
- **Seniority Test.** "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
*Touch only what you must. Clean up only your own mess.*
- **Stay in scope.** Don't "improve" adjacent code, comments, or formatting.
- **Respect established code.** Don't refactor things that aren't broken.
- **Match style.** Match existing style, even if you'd do it differently.
- **Mention dead code.** If you notice unrelated dead code, mention it — don't delete it.
- **Orphan management.** Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead code unless asked.
- **The Traceability Test.** Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
*Define success criteria. Loop until verified.*
- **Verifiable goals.**
  - "Add validation" → "Write tests for invalid inputs, then make them pass"
  - "Fix the bug" → "Write a test that reproduces it, then make it pass"
  - "Refactor X" → "Ensure tests pass before and after"
- **State the plan.** For multi-step tasks, state a brief plan:
  1. [Step] → verify: [check]
  2. [Step] → verify: [check]
  3. [Step] → verify: [check]

---

## Authoritative Agent Configurations

For all operational details, boundaries, routing tables, and skill sheets, consult:
- **Core Rules**: [.agent/rules/core-agent-rules.md](file:///.agent/rules/core-agent-rules.md)
- **Protocol Router**: [.agent/rules/protocol-router.md](file:///.agent/rules/protocol-router.md)
