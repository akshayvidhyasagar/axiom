# Protocol Router

---
purpose: Dynamic dispatcher routing task scenarios to specific governing protocols
when_to_use: Run before executing any task to load relevant sub-rules
when_not_to_use: Never deactivated
companion_protocols: "[[core-agent-rules.md]]"
---

Use this router to determine which specific, on-demand protocols must be activated for your current task. Reading this file is always-on; reading the mapped protocols is mandatory when trigger conditions are met.

---

## 1. Scenario Dispatch Table

| Task Category | Scenario / Trigger Condition | Governing Protocol | Required Tools / Skills |
| :--- | :--- | :--- | :--- |
| **Ambiguity** | Task instructions are ambiguous, conflicting, or incomplete | `planning-protocol.md`<br>`mcp-usage-protocol.md` | `/grill-me`<br>`/grill-with-docs` |
| **Requirements & Design** | Drafting specifications, PRDs, or breaking down implementation plans | `planning-protocol.md` | `/to-prd`<br>`/to-issues` |
| **Feature Implementation** | Writing new codebase modules, functions, or refactoring green code | `planning-protocol.md`<br>`debugging-protocol.md` | `/tdd` |
| **Bugs & Performance** | Resolving crashes, unexpected behavior, profiler logs, or regressions | `debugging-protocol.md`<br>`mcp-usage-protocol.md` | `/diagnose`<br>`gitnexus-debugging` |
| **Refactoring & Code Review** | Changing interfaces, splitting files, resolving circular dependencies | `architecture-protocol.md`<br>`mcp-usage-protocol.md` | `/improve-codebase-architecture`<br>`gitnexus-refactoring` |
| **Information Gathering** | Searching external web resources, fetching papers, analyzing concept gaps | `research-protocol.md` | `/autoresearch`<br>`airweave` MCP |
| **Knowledge Capture** | Ingesting documents/images, writing wiki notes, canvas maps, log folds | `documentation-protocol.md` | `wiki-ingest`<br>`wiki-query`<br>`/save`<br>`/canvas` |
| **MCP Operations** | Directly invoking external servers (GitHub, Obsidian API, GitNexus, shadcn) | `mcp-usage-protocol.md` | `github`<br>`obsidian`<br>`gitnexus`<br>`shadcn` |
| **Skill Commands** | Invoking `/diagnose`, `/tdd`, `/triage`, `/save`, `/canvas`, etc. | `skills-mcp-index.md` | All 30 custom skills |

---

## 2. Precedence & Activation Policy

### Selective Activation Rule
- **Context Preservation**: Do not read all protocols into your context at once. Only open and read the specific protocol(s) mapped to your current active step.
- **Precedence**:
  1. Tool limits (`mcp-usage-protocol.md` and `core-agent-rules.md`) always take precedence over execution workflows.
  2. If a task spans multiple categories, read them sequentially according to the recipe order (e.g. read `planning-protocol.md` first to build, then `debugging-protocol.md` to test).

### Task Ambiguity Resolution Flow
1. If the user prompt is underspecified, **stop coding**.
2. Activate `/grill-with-docs` (if domain terminology conflicts exist) or `/grill-me` (for execution design trees).
3. Draft an implementation plan and PRD using the guidelines in `planning-protocol.md`.
4. Proceed only after explicit user approval.
