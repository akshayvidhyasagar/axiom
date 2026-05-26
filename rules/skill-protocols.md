# Skill Protocols

## Underused MCP Servers

### github
- **Trigger**: When a task explicitly requires GitHub context (e.g., creating a GitHub issue via `/to-issues`, triaging via `/triage`).
- **Workflow**:
  1. Ensure `rules/mcp-policy.md` permits the operation.
  2. Use the GitHub MCP tool as defined in the skill (`.agents/skills/to-issues` or `.agents/skills/triage`).
  3. Perform read‑only actions (list issues, fetch PR details) via MCP.
  4. For any write operation (create issue, add comment, update label) invoke the corresponding skill which internally calls the MCP.
- **Expected Output**: JSON responses from GitHub API, confirmation messages for created resources.
- **Failure Modes**:
  - Missing or expired `GITHUB_PERSONAL_ACCESS_TOKEN` → abort and log to `wiki/log.md`.
  - API rate limiting → back‑off and retry after 60 s.
  - Unauthorized scopes → report and request token with required scopes.

### sequential-thinking
- **Trigger**: Complex design or debugging tasks with >3 interdependent unknowns that can be resolved through reasoning alone.
- **Workflow**:
  1. Invoke the Sequential Thinking MCP via the `sequential-thinking` server.
  2. Break the problem into discrete reasoning steps using the tool's chain‑of‑thought capability.
  3. Capture each step's conclusion and feed it back to the agent for validation.
- **Expected Output**: Structured reasoning summary, decision points, and recommended actions.
- **Failure Modes**:
  - Excessive token consumption → limit to 3 reasoning cycles, then ask the user for clarification.
  - Ambiguous output → treat as incomplete and request clarification.

### airweave
- **Trigger**: When local wiki search (`qmd wiki "<query>"`) returns insufficient results and external semantic context is needed.
- **Workflow**:
  1. Run the Airweave search tool with the original query.
  2. Synthesize results using the `research/autoresearch` skill.
  3. Ingest any new concepts via `.agent/skills/wiki/ingest`.
- **Expected Output**: Retrieved snippets, citations, and optionally new wiki pages.
- **Failure Modes**:
  - No API key or invalid key → abort and log.
  - Returned >5 pages → truncate and ask user which are relevant.

## Underused GitNexus Skills

### gitnexus-debugging, gitnexus-exploring, gitnexus-guide, gitnexus-impact-analysis, gitnexus-refactoring
- **Trigger**: When a developer needs assistance beyond the basic `gitnexus-cli` analysis (e.g., impact analysis of a large refactor).
- **Workflow**:
  1. Run the specific skill's SKILL.md to set up the context.
  2. Call the underlying `gitnexus` MCP with the appropriate sub‑command (e.g., `gitnexus impact`).
  3. Review the JSON report and act accordingly.
- **Expected Output**: Detailed impact graph, suggested module changes, or debugging tips.
- **Failure Modes**:
  - Graph exceeds size limits → split into batches.
  - Circular dependency detection without a clear fix → flag for ADR creation.

## Underused Matt‑Pocock Skill Set

### caveman, diagnose, grill‑me, grill‑with‑docs, handoff, improve‑codebase‑architecture, prototype, to‑issues, to‑prd, triage, write‑a‑skill, zoom‑out
- **Trigger**: When the user explicitly requests one of these utilities (e.g., ` /diagnose `) or when a situation matches the described scenario in the skill's documentation.
- **Workflow**:
  1. Read the corresponding `SKILL.md`.
  2. Execute the skill via the agent command (`/diagnose`, `/to-issues`, etc.).
  3. Follow the step‑by‑step instructions inside the skill file.
- **Expected Output**: Depends on skill – usually a report, a set of GitHub issues, a prototype scaffold, or a handoff document.
- **Failure Modes**:
  - Missing prerequisites (e.g., no open issue tracker) → abort with explanatory message.
  - Skill attempts to write files outside the repository root → block and log.

*These protocols provide concrete activation points and safeguards for all currently under‑utilized components.*
