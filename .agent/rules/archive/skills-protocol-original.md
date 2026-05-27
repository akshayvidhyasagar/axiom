# Axiom Agent Toolchain and Skill Protocols

---
purpose: Detailed worksheets for all custom agent skills and tools in the workspace
when_to_use: When executing any custom skill command (/diagnose, /tdd, /save, etc.) or calling MCP servers
when_not_to_use: For general code modifications or simple file edits
companion_protocols: "[[core-agent-rules.md]], [[protocol-router.md]]"
---

## MCP Servers

### airweave
- **One-line purpose** — Semantic search query execution across external/internal indexed quant sources.
- **Exact trigger** — When local wiki searches (`qmd wiki/ "<query>"`) return thin findings on a quant trading concept (e.g. regime detection) and external semantic research is required.
- **Step-by-step workflow** — 
  1. Confirm that semantic search is permitted under the current phase policy.
  2. Invoke `search-software-c7fb3h` with the target quant concept query.
  3. Review retrieved text chunks and select the top 2-3 most relevant items.
  4. Synthesize the findings and hand them over to `wiki-ingest` to update or create concepts.
- **Expected output** — JSON payload containing semantically relevant text fragments, URL metadata, and confidence scores.
- **Failure modes** — API key missing or connection timeout → Log failure in `wiki/log.md` and fall back to web search using Google Search MCP.
- **Combinations** — Pair with `autoresearch` to feed external research queries, or run before `wiki-ingest` to import the findings into the vault.

### github
- **One-line purpose** — Interaction with the remote GitHub repository for managing issues, pull requests, labels, and metadata.
- **Exact trigger** — When generating implementation tickets from a PRD (via `/to-issues`) or triaging incoming bug reports (via `/triage`).
- **Step-by-step workflow** — 
  1. Verify active token in environment (`GITHUB_PERSONAL_ACCESS_TOKEN`).
  2. Call `list_issues` or `search_issues` to find matching issue contexts.
  3. Execute `create_issue` or `add_issue_comment` to update state on the tracker.
- **Expected output** — JSON payload with created resource details, issue number, and URL.
- **Failure modes** — Rate limiting or token expired → Abort, report to user, log error in `wiki/log.md`, and default to writing local markdown issues in `.scratch/`.
- **Combinations** — Run `/to-prd` first, then `/to-issues` (which invokes GitHub MCP to publish tickets), then `/triage` to label.

### gitnexus
- **One-line purpose** — Structural analysis of codebase graph imports, call chains, and module dependencies.
- **Exact trigger** — Run before editing any module file to analyze imports and determine blast radius.
- **Step-by-step workflow** — 
  1. Run `gitnexus analyze` to refresh the index.
  2. Call `gitnexus_impact` to trace upstream callers.
  3. Call `gitnexus_context` on the suspect symbol to verify direct dependencies.
- **Expected output** — Dependency import list, caller/callee counts, and cohesion score metrics.
- **Failure modes** — Stale index warnings → Run `npx gitnexus analyze` in the shell first to rebuild the graph database.
- **Combinations** — Call `gitnexus-cli` to update index, query relationships using `gitnexus-exploring` or `gitnexus-debugging`, then run `/diagnose` to fix.

### obsidian
- **One-line purpose** — Interfaces with local Obsidian REST API for vault synchronisation checks and metadata patches.
- **Exact trigger** — Run at session start to verify local REST API connection, and after saving a wiki page to patch properties without rewriting the file.
- **Step-by-step workflow** — 
  1. Run curl or API tool to check status of the REST service (`GET /vault/wiki/hot.md`).
  2. Use `PATCH /vault/<path>` with `Target-Type: frontmatter` to update fields (e.g. tag additions, status updates).
- **Expected output** — HTTP 200/204 response codes confirming the property patch was applied.
- **Failure modes** — Connection refused / Port offline → Append `[obsidian-sync: offline]` to `wiki/log.md` and edit frontmatter directly on disk.
- **Combinations** — Run `/save` or `wiki-ingest` to write files, then call Obsidian API to synchronize properties.

### sequential-thinking
- **One-line purpose** — Chain-of-thought planning and decomposition of complex architectural decisions.
- **Exact trigger** — Designing a new quantifier model interface or debugging a non-obvious runtime error with >3 interdependent unknowns.
- **Step-by-step workflow** — 
  1. Call `sequentialthinking` with initial problem statement.
  2. Iterate through reasoning steps, validating assumptions one-by-one.
  3. Document the final derived strategy in the implementation plan.
- **Expected output** — Multi-step thinking trace concluding with a validated design option or bug explanation.
- **Failure modes** — Excessive token consumption → Limit thinking cycles to 5, then default to interactive query with user.
- **Combinations** — Pair with `/grill-me` to stress-test a plan, or use before `/diagnose` to form hypotheses.

### shadcn
- **One-line purpose** — Command generation and audit verification for Tailwind CSS/shadcn components and page blocks.
- **Exact trigger** — Mandatory whenever building or editing a user interface or layout in the dashboard.
- **Step-by-step workflow** — 
  1. Call `search_items_in_registries` for blocks/primitives.
  2. Use `view_items_in_registries` and `get_item_examples_from_registries` to study code.
  3. Call `get_add_command_for_items` to generate the installation command.
  4. Run command in terminal, then call `get_audit_checklist` to verify layout.
- **Expected output** — Installed component files under `components/ui/` and verified audit checklists.
- **Failure modes** — Dependency resolution error or broken theme variable → Re-apply variables in `src/index.css` and verify.
- **Combinations** — Pair with `/prototype` (UI branch) to preview components in toggleable views.

---

## Matt Pocock Skills

### caveman
<!-- read: .agent/skills/matt_polock/caveman/SKILL.md -->
- **One-line purpose** — Terse communication mode that drops articles and fluff to cut token usage by 75%.
- **Exact trigger** — User says "caveman mode", "talk like caveman", or context window size exceeds 80%.
- **Step-by-step workflow** — 
  1. Strip all articles (a/an/the) and polite filler (sure/certainly) from replies.
  2. Use causality arrows (X -> Y) and abbreviate technical terms (DB/auth/fn).
  3. Keep code blocks and errors exact.
- **Expected output** — Terse technical fragments conveying complete accuracy with minimal tokens.
- **Failure modes** — Destructive confirmation prompts or security warnings → Temporarily drop caveman for safety clarity, then resume.
- **Combinations** — Pair with `/diagnose` or `/tdd` during heavy file-editing sessions to conserve token budget.

### diagnose
<!-- read: .agent/skills/matt_polock/diagnose/SKILL.md -->
- **One-line purpose** — Disciplined diagnosis workflow for hard bugs: reproduce, minimize, hypothesize, instrument, and test.
- **Exact trigger** — User reports a bug, failing test, or performance regression.
- **Step-by-step workflow** — 
  1. Construct a deterministic, fast feedback loop (failing test, HTTP curl script, CLI invocation).
  2. Reproduce the bug and capture exact error outputs.
  3. Generate 3-5 ranked, falsifiable hypotheses and present them to the user.
  4. Instrument the suspect code path using uniquely tagged logs (`[DEBUG-xxxx]`).
  5. Apply the fix and run the regression tests.
- **Expected output** — Verified fix, new regression test, and all debug logs cleaned up.
- **Failure modes** — Flaky or non-deterministic bug → Increase execution stress (run 100x, add timing sleeps) to raise reproduction rate.
- **Combinations** — Use `gitnexus-debugging` first to map callers, then sequential-thinking to rank hypotheses, then `/diagnose` to resolve.

### grill-me
<!-- read: .agent/skills/matt_polock/grill-me/SKILL.md -->
- **One-line purpose** — Relentlessly interviews the user to challenge a plan or design option.
- **Exact trigger** — User wants to stress-test a proposed implementation plan or says "grill me".
- **Step-by-step workflow** — 
  1. Ask questions one at a time, providing a recommended option for each decision branch.
  2. Wait for feedback before proceeding to the next question.
  3. Explore the codebase first if a question can be answered by looking at the files.
- **Expected output** — Deep alignment on plan details with clear design decisions.
- **Failure modes** — User becomes unresponsive → Proceed with recommended default choices.
- **Combinations** — Run `/grill-me` before `/to-prd` to align on requirements.

### grill-with-docs
<!-- read: .agent/skills/matt_polock/grill-with-docs/SKILL.md -->
- **One-line purpose** — Challenging design plans against `CONTEXT.md` vocabulary and documented ADRs.
- **Exact trigger** — Planning a feature build that introduces new terms or could impact existing core boundaries.
- **Step-by-step workflow** — 
  1. Read glossary terms in `CONTEXT.md` and active ADRs.
  2. Interview user one question at a time.
  3. Challenge vague terms and reconcile conflicts between glossary and proposed plan.
  4. Update `CONTEXT.md` terms immediately as decisions crystallize.
- **Expected output** — Reconciled terminology, updated `CONTEXT.md` glossary, and drafted ADRs.
- **Failure modes** — Contradicting active ADRs → Highlight friction and offer to update/re-open the ADR.
- **Combinations** — Run `/grill-with-docs` first, then `/to-prd` to write the specification.

### handoff
<!-- read: .agent/skills/matt_polock/handoff/SKILL.md -->
- **One-line purpose** — Compiling current conversation and task state into a handoff document for the next session.
- **Exact trigger** — Ready to hand over to a fresh agent or ending session with incomplete tasks.
- **Step-by-step workflow** — 
  1. Summarize outstanding work, blocked paths, and next tasks.
  2. Reference existing artifacts (plans, diffs, issues) rather than copying them.
  3. Redact API keys or credentials.
  4. Save report to the OS temporary directory (`$TMPDIR`).
- **Expected output** — Handoff markdown file created in OS temp directory.
- **Failure modes** — Missing temp directory path → Write to `/tmp` or user home path.
- **Combinations** — Run `/zoom-out` to document module state, then save handoff.

### improve-codebase-architecture
<!-- read: .agent/skills/matt_polock/improve-codebase-architecture/SKILL.md -->
- **One-line purpose** — Identifying refactoring opportunities to deepen interfaces and improve testability.
- **Exact trigger** — Code contains shallow modules (interfaces as complex as implementation) or tightly-coupled dependencies.
- **Step-by-step workflow** — 
  1. Explore codebase and vocabulary in `CONTEXT.md`.
  2. Write refactoring candidates to an HTML report in OS temp directory.
  3. Include before/after Mermaid diagrams for each candidate.
  4. Grill user on chosen candidate to refine interfaces.
- **Expected output** — HTML report file opened for user detailing candidate refactors.
- **Failure modes** — Report contains invalid Mermaid syntax → Re-verify syntax by avoiding nested quotes or brackets.
- **Combinations** — Run `gitnexus-exploring` first to find coupling, then this skill, then grill user, then `/to-prd`.

### prototype
<!-- read: .agent/skills/matt_polock/prototype/SKILL.md -->
- **One-line purpose** — Scaffolds a throwaway prototype to test state/business logic or user interface variations.
- **Exact trigger** — Want to explore designs or validate a state machine model before committing to production files.
- **Step-by-step workflow** — 
  1. Pick a branch: Logic (terminal app) or UI (toggleable layout variations).
  2. Scaffolds code next to target modules, named clearly as a prototype.
  3. Run it with a single project command, surfacing state transitions.
  4. Fold validated decisions into real code and delete the prototype.
- **Expected output** — Runnable scratch script or UI variation routing.
- **Failure modes** — Leaving stale prototype code in repository → Delete files once the design question is answered.
- **Combinations** — Use `/grill-with-docs` to align on glossary, prototype the logic, then write production code via `/tdd`.

### tdd
<!-- read: .agent/skills/matt_polock/tdd/SKILL.md -->
- **One-line purpose** — Test-driven development loop using vertical slices (Tracer Bullets) to build features.
- **Exact trigger** — Implementing new business logic or fixing bugs in critical paths.
- **Step-by-step workflow** — 
  1. Confirm public interfaces and target behaviors with user.
  2. Write ONE integration-style test first (RED).
  3. Write minimal code to pass the test (GREEN).
  4. Refactor code while green, running tests at each step.
  5. Repeat loop for the next behavior.
- **Expected output** — Behavior-focused integration tests and minimal implementation code.
- **Failure modes** — Mocking internal collaborators or horizontal slicing (writing all tests first) → Write tests only for public interfaces one slice at a time.
- **Combinations** — Break plan into issues via `/to-issues`, then run `/tdd` on each issue sequentially.

### to-issues
<!-- read: .agent/skills/matt_polock/to-issues/SKILL.md -->
- **One-line purpose** — Breaking down an implementation plan or PRD into thin vertical tracer-bullet issues.
- **Exact trigger** — Preparing to execute a finalized PRD or plan.
- **Step-by-step workflow** — 
  1. Scan plan and explore target codebase.
  2. Draft tracer-bullet issues containing complete vertical slices (UI to Database).
  3. Present list of issues to user, indicating blockages (HITL vs AFK).
  4. Publish approved issues to GitHub issues or local markdown files.
- **Expected output** — Created tickets in issue tracker mapped in dependency order.
- **Failure modes** — Missing issue tracker configuration → Run `/setup-matt-pocock-skills` first.
- **Combinations** — Write PRD using `/to-prd`, break it down using `/to-issues`, then build via `/tdd`.

### to-prd
<!-- read: .agent/skills/matt_polock/to-prd/SKILL.md -->
- **One-line purpose** — Synthesizes conversation context and codebase understanding into a formal PRD.
- **Exact trigger** — User wants to outline scope and acceptance criteria for a new feature.
- **Step-by-step workflow** — 
  1. Explore codebase to understand current implementation.
  2. Outline modules to build or modify, seeking opportunities for deep modules.
  3. Write PRD using template (Problem, Solution, User Stories, Decisions, Testing).
  4. Publish the PRD to the issue tracker.
- **Expected output** — PRD ticket created and labeled `ready-for-agent`.
- **Failure modes** — volatile code snippets in PRD → Limit to state machine schemas or type shapes from prototypes.
- **Combinations** — Grill user with `/grill-with-docs` first, then run `/to-prd`, then run `/to-issues`.

### triage
<!-- read: .agent/skills/matt_polock/triage/SKILL.md -->
- **One-line purpose** — Managing issue lifecycles through a state machine of categories (bug/enhancement) and states (needs-triage, ready-for-agent, etc.).
- **Exact trigger** — Reviewing incoming tickets or organizing a backlog.
- **Step-by-step workflow** — 
  1. Query tracker for unlabeled or `needs-triage` tickets.
  2. Recommend category and state with reasoning.
  3. Attempt bug reproduction.
  4. Post brief or triage notes, and apply labels.
- **Expected output** — Issues labeled and commented with structured triage notes or briefs.
- **Failure modes** — Unreproducible bug → Mark `needs-info` and request specific details from reporter.
- **Combinations** — Triage issue, run `/grill-with-docs` on it, then transition to `ready-for-agent` with brief.

### write-a-skill
<!-- read: .agent/skills/matt_polock/write-a-skill/SKILL.md -->
- **One-line purpose** — Scaffolding a new agent skill with metadata, instructions, and scripts.
- **Exact trigger** — A task requires custom automation or workflow instructions not covered by existing skills.
- **Step-by-step workflow** — 
  1. Gather requirements (triggers, use cases, scripts needed).
  2. Create a new directory under `.agent/skills/` containing `SKILL.md`.
  3. Add YAML frontmatter listing exact triggers.
  4. Review draft with user and publish.
- **Expected output** — New skill folder with valid `SKILL.md` instructions.
- **Failure modes** -> Missing "Use when" triggers in description -> Ensure first sentence defines capability, second lists triggers.
- **Combinations** — Create skill, run `wiki-lint` to check references, then update `wiki/index.md`.

### zoom-out
<!-- read: .agent/skills/matt_polock/zoom-out/SKILL.md -->
- **One-line purpose** — Instructs the agent to go up a layer of abstraction and provide a map of relevant modules and callers.
- **Exact trigger** — Being assigned a task in an unfamiliar area of the codebase.
- **Step-by-step workflow** — 
  1. Read domain glossary and active ADRs.
  2. Map all module relationships and callers in the target directory.
  3. Present map using project glossary terms.
- **Expected output** — High-level diagram and textual mapping of module structure.
- **Failure modes** — No glossary exists → Extract terms from files to compile a temporary outline.
- **Combinations** — Run `zoom-out` before `/improve-codebase-architecture` or `/diagnose`.

### setup-matt-pocock-skills
<!-- read: .agent/skills/matt_polock/setup-matt-pocock-skills/SKILL.md -->
- **One-line purpose** — Scaffolds configuration files (`issue-tracker.md`, `triage-labels.md`, `domain.md`) in `docs/agents/` and edits `AGENTS.md` to define issues, labels, and docs location.
- **Exact trigger** — First session setup, or when triage/to-issues skills cannot resolve issue trackers or labels.
- **Step-by-step workflow** — 
  1. Explore repository git remotes and existing docs paths.
  2. Present choices for Tracker, Triage, and Domain one-by-one to user.
  3. Write target markdown files to `docs/agents/` and update `AGENTS.md` block.
- **Expected output** — Valid config files under `docs/agents/` and configured section in `AGENTS.md`.
- **Failure modes** — Git remote absent → Default to local markdown tracking.
- **Combinations** — Must run before first execution of `to-issues`, `to-prd`, `triage`, `diagnose`, `tdd`, or `improve-codebase-architecture`.

---

## GitNexus Skills

### gitnexus-refactoring
<!-- read: .agent/skills/gitnexus/gitnexus-refactoring/SKILL.md -->
- **One-line purpose** — Coordinated renaming, splitting, or restructuring of codebase modules using GitNexus analysis.
- **Exact trigger** — Safe renaming of a load-bearing interface function or splitting a large quant service file.
- **Step-by-step workflow** — 
  1. Run `gitnexus_rename` with `dry_run: true` to preview changes.
  2. Review AST search edits (check for dynamic references).
  3. Call `gitnexus_rename` with `dry_run: false` to apply changes.
  4. Run tests and execute `gitnexus_detect_changes` to verify the modified scope.
- **Expected output** — Coordinated edits applied across files, and passing test pipeline status.
- **Failure modes** — String or dynamic references missed → Run `gitnexus_query` to search codebase for occurrences.
- **Combinations** — Run `gitnexus-impact-analysis` first, apply renaming, then run `gitnexus_detect_changes`.

### gitnexus-debugging
<!-- read: .agent/skills/gitnexus/gitnexus-debugging/SKILL.md -->
- **One-line purpose** — Graph-based call-chain tracing to isolate bug origins and error throw sites.
- **Exact trigger** — Investigating a runtime exception, wrong return value, or performance slowdown.
- **Step-by-step workflow** — 
  1. Run `gitnexus_query` with the error message or suspect symptom.
  2. Call `gitnexus_context` on the suspect symbol to see callers and callees.
  3. Trace call chains using Cypher queries if necessary.
- **Expected output** — Trace showing callers, callees, execution flows, and external dependencies.
- **Failure modes** — Index is stale → Re-run CLI command `npx gitnexus analyze`.
- **Combinations** — Use first to isolate the bug source, then use `/diagnose` to fix it.

### gitnexus-exploring
<!-- read: .agent/skills/gitnexus/gitnexus-exploring/SKILL.md -->
- **One-line purpose** — Codebase exploration using clusters, cohesion scores, and execution flows.
- **Exact trigger** — Navigating unfamiliar sections of the repository or studying system architecture.
- **Step-by-step workflow** — 
  1. Read `gitnexus://repo/{name}/context` for stats and freshness.
  2. Read `clusters` to identify functional areas.
  3. Query flow names and deep-dive key symbols using `gitnexus_context`.
- **Expected output** — Textual map of cohesion areas, members, and call steps.
- **Failure modes** — Complex clusters with low cohesion scores → Map out sub-components to analyze separately.
- **Combinations** — Pair with `/zoom-out` or `/improve-codebase-architecture`.

### gitnexus-guide
<!-- read: .agent/skills/gitnexus/gitnexus-guide/SKILL.md -->
- **One-line purpose** — Reference guide for GitNexus MCP tools, resources, and Cypher database schema.
- **Exact trigger** — Designing a custom Cypher query or verifying available GitNexus capabilities.
- **Step-by-step workflow** — 
  1. Consult guide to map the task to the right GitNexus sub-skill.
  2. Read the resource tables to find the right URI scheme.
- **Expected output** — Code schema terms and example Cypher queries.
- **Failure modes** — Cypher query fails → Check syntax against schema nodes (File, Function, etc.) and relations (CALLS, IMPORTS).
- **Combinations** — Read before writing Cypher queries in `gitnexus-debugging`.

### gitnexus-cli
<!-- read: .agent/skills/gitnexus/gitnexus-cli/SKILL.md -->
- **One-line purpose** — Running CLI actions (analyze, status, clean, wiki) to manage the GitNexus database.
- **Exact trigger** — First-time workspace configuration, or index is stale after significant file updates.
- **Step-by-step workflow** — 
  1. Run `npx gitnexus status` to check freshness.
  2. Run `npx gitnexus analyze [--embeddings]` from the project root.
  3. Verify index loaded using `gitnexus://repo/{name}/context`.
- **Expected output** — Updated `.gitnexus/` graph database and refreshed context.
- **Failure modes** — Ran outside git repo -> Ensure working directory is a git repository.
- **Combinations** — Re-analyze index before starting exploring or debugging workflows.

### gitnexus-impact-analysis
<!-- read: .agent/skills/gitnexus/gitnexus-impact-analysis/SKILL.md -->
- **One-line purpose** — Mapping upstream blast radius of interface changes before editing files.
- **Exact trigger** — Modifying signature or return values of load-bearing functions or interfaces.
- **Step-by-step workflow** — 
  1. Call `gitnexus_impact` with target and direction: upstream.
  2. Check affected processes.
  3. Run `gitnexus_detect_changes` to verify risk level.
- **Expected output** — Risk assessment (Low, Medium, High, Critical) and caller lists grouped by depth.
- **Failure modes** — Missing transitive callers → Increase `maxDepth` argument.
- **Combinations** — Run before `/improve-codebase-architecture` or `gitnexus-refactoring`.

---

## Axiom-specific skills

### autoresearch
<!-- read: .agent/skills/research/autoresearch/SKILL.md -->
- **One-line purpose** — Iterative search and fetch loop that files synthesized findings directly into the wiki.
- **Exact trigger** — User requests a research loop on a quant trading concept, regime detection, or factor model.
- **Step-by-step workflow** — 
  1. Read objectives and domain limits from `references/program.md`.
  2. If boundary mode is active, query `./scripts/boundary-score.py --top 5`.
  3. Execute 3 rounds of WebSearch, WebFetch, gap identification, and confidence scoring.
  4. Write results to `wiki/sources/`, `wiki/concepts/`, and synthesis page.
  5. Update `wiki/index.md`, `wiki/log.md`, and `wiki/hot.md`.
- **Expected output** — Structured pages written to vault, plus summary logged to `wiki/log.md`.
- **Failure modes** — Exceeding page limit bounds -> Truncate output list, report gap in synthesis.
- **Combinations** — Run `autoresearch` to gather concepts, then run `wiki-lint` to check links.

### interrupt
<!-- read: .agent/skills/interrupt/SKILL.md -->
- **One-line purpose** — Session interrupt handler to save progress and blockers when exiting mid-task.
- **Exact trigger** — Session ends mid-task due to ambiguity, missing API keys, or token limits.
- **Step-by-step workflow** — 
  1. Bypass the normal END protocol.
  2. Update `wiki/hot.md` under "Active Threads" with the task state, blocking issues, and next tasks.
  3. Prepend a chore/interrupt entry to the top of `wiki/log.md`.
  4. Commit staged changes with message: `chore: interrupt — <description>`.
- **Expected output** — Clean repository status and context cache updated in `wiki/hot.md`.
- **Failure modes** — Accidental write to `docs/CHANGELOG.md` → Do not edit the changelog on interrupted sessions.
- **Combinations** — Execute whenever a block occurs.

### wiki-lint
<!-- read: .agent/skills/wiki/lint/SKILL.md -->
- **One-line purpose** — Health check utility that audits the Obsidian wiki vault for links, frontmatter, and duplicate pages.
- **Exact trigger** — Weekly maintenance or starting a new phase in `docs/PRD.md`.
- **Step-by-step workflow** — 
  1. Scan for orphans, dead links, stale claims, and missing cross-references.
  2. If DragonScale addresses active, validate formatting, uniqueness, and map consistency.
  3. If semantic tiling active, query `tiling-check.py` to identify duplicates.
  4. Write report to `wiki/meta/lint-report-YYYY-MM-DD.md` and update index/dashboard.
- **Expected output** — Generated lint report listing issues and auto-fixed items.
- **Failure modes** — Duplicate pages found → Do not auto-merge; document in report for human review.
- **Combinations** — Run after a batch of `wiki-ingest` runs or `autoresearch`.

### wiki-ingest
<!-- read: .agent/skills/wiki/ingest/SKILL.md -->
- **One-line purpose** — Ingests articles, URL links, and images into the wiki while updating counters and index lists.
- **Exact trigger** — Processing a source document, URL, or image to store in the knowledge base.
- **Step-by-step workflow** — 
  1. Check `.raw/.manifest.json` file hash to verify if file was already ingested.
  2. Save cleaned text to `.raw/articles/` or image summaries to `.raw/images/`.
  3. Create summaries in `wiki/sources/`, and update concept/entity pages.
  4. If DragonScale active, allocate an address using `scripts/allocate-address.sh`.
  5. Update index, hot cache, and prepend entry to `wiki/log.md`.
- **Expected output** — Extracted wiki notes and updated master index.
- **Failure modes** -> Modifying raw files under `.raw/` -> Keep raw files read-only; write only index mappings.
- **Combinations** — Fetch URL with WebFetch MCP, ingest via `wiki-ingest`, then verify using `wiki-query`.

### wiki
<!-- read: .agent/skills/wiki/SKILL.md -->
- **One-line purpose** — Scaffolds, maintains, and routes operations within a persistent wiki vault.
- **Exact trigger** — Creating a new project vault or initializing core indexes.
- **Step-by-step workflow** — 
  1. Pick mode based on `references/modes.md`.
  2. Create folders, template notes, sub-indexes, index, log, and hot cache files.
  3. Write `.obsidian/snippets/vault-colors.css` and repository `AGENTS.md`.
- **Expected output** — Seeded folders, templates, CSS snippet files, and initialized git repository.
- **Failure modes** — Running over existing vault files → Verify backup exists first.
- **Combinations** — Run first, then ingest sources or research concepts.

### wiki-fold
<!-- read: .agent/skills/wiki/fold/SKILL.md -->
- **One-line purpose** — Summarizes chronological log entries into permanent fold pages.
- **Exact trigger** — Prepends of log entries reach exponent batch boundary (default 2^k = 16 entries) and need rollup.
- **Step-by-step workflow** — 
  1. Parse top 2^k log entries and build structured children lists.
  2. Run dry-run (stdout-only) to compile Outcomes and Themes.
  3. If commit, write fold page to `wiki/folds/{FOLD-ID}.md`.
  4. Prepend log entry and update index.
- **Expected output** — Rollup fold document summarizing key outcomes.
- **Failure modes** — Output generated in dry-run triggers PostToolUse hook → Ensure dry-run writes only to stdout, not disk files.
- **Combinations** — Run weekly after active `wiki-ingest` batches.

### wiki-query
<!-- read: .agent/skills/wiki/query/SKILL.md -->
- **One-line purpose** — Answering queries using vault files with citations and filing answers back.
- **Exact trigger** — Answering factual questions about quant models, regimes, or data sources.
- **Step-by-step workflow** — 
  1. Choose mode (Quick: hot/index only; Standard: 3-5 pages; Deep: full vault).
  2. Read files sequentially and synthesize answers in present tense.
  3. Cite with wikilinks: `[[Page Name]]`.
  4. Offer to save synthesis as a permanent question page.
- **Expected output** — Citations-backed response and optional question page in `wiki/questions/`.
- **Failure modes** — Gaps in vault coverage → Report specific subtopic gap and offer to search rather than fabricating.
- **Combinations** — Run `wiki-query`, then run `/save` to preserve standard or deep outputs.

### canvas
<!-- read: .agent/skills/utils/canvas/SKILL.md -->
- **One-line purpose** — Visual mapping of nodes, images, and text files inside Obsidian canvases.
- **Exact trigger** — User wants to visual-map a concept structure, prototype layout, or folder overview.
- **Step-by-step workflow** — 
  1. Read target canvas JSON file.
  2. Auto-position the new node within the target group zone.
  3. Generate unique ID using timestamp to avoid collisions.
  4. Write node parameters to canvas JSON.
- **Expected output** — Visual node added to canvas file.
- **Failure modes** — Overlapping nodes -> Verify aspect ratios and zone coordinate bounds.
- **Combinations** — Pair with `autoresearch` or `/banana` to present visuals.

### save
<!-- read: .agent/skills/utils/save/SKILL.md -->
- **One-line purpose** — Saving conversation threads or design results to the wiki as permanent notes.
- **Exact trigger** — Chat yielding a valuable quant design, API specification, or architectural decision.
- **Step-by-step workflow** — 
  1. Determine note type (synthesis/concept/source/decision/session).
  2. Extract content in declarative present tense.
  3. Write file with frontmatter and update `wiki/index.md` and `wiki/log.md`.
- **Expected output** — Created note in the correct wiki directory, indexed.
- **Failure modes** — Saving trivial Q&A or duplicate items → Update existing page instead.
- **Combinations** — Run after standard/deep `wiki-query` sessions.

### obsidian-markdown
<!-- read: .agent/skills/obsidian/obsidian-markdown/SKILL.md -->
- **One-line purpose** — Reference for formatting Obsidian Flavored Markdown syntax (wikilinks, callouts, frontmatter properties).
- **Exact trigger** — Writing or editing wiki notes or templates.
- **Step-by-step workflow** — 
  1. Refer to tables for wikilink format (`[[Note\|Display]]`), embeds (`![[image.png]]`), and callouts (`> [!contradiction]`).
  2. Enforce flat properties and YYYY-MM-DD dates in frontmatter.
- **Expected output** — Well-formed markdown pages.
- **Failure modes** — Malformed YAML lists or double brackets in unquoted fields → Quote wikilinks in YAML properties.
- **Combinations** — Use during `/save` and `wiki-ingest`.

---

## Workflows

#### 1. Feature Build Recipe
1. **/grill-with-docs** — challenge design ideas, align on quant vocabulary, and update `CONTEXT.md` glossary.
2. **/to-prd** — convert conversation context into a structured PRD ticket.
3. **/to-issues** — decompose the PRD into vertical, tracer-bullet implementation issues.
4. **/tdd** — pick issues in dependency order and write code via test-driven loops.

#### 2. Hard Bug Recipe
1. **/zoom-out** — mapping module structures and callers.
2. **sequential-thinking MCP** — analyze relationships and establish hypotheses.
3. **/diagnose** — build feedback loop, reproduce bug, rank hypotheses, instrument, and verify fix.
4. **/tdd** — write integration test at correct seam, implement code, and check regression.

#### 3. Quant Research & Ingest Recipe
1. **/autoresearch** — research a new quant concept using WebSearch, fetches, and gap checks.
2. **wiki-ingest** — process the resulting documents, write to `wiki/sources/`, and update concepts.
3. **wiki-lint** — check frontmatter gaps, dead links, and semantic duplicates.
4. **wiki-fold** — rollup chronological logs after the active batch completes.

#### 4. Refactoring & Code Deepening Recipe
1. **gitnexus-impact-analysis** — trace blast radius of the target changes.
2. **/improve-codebase-architecture** — identify refactoring opportunities and generate HTML candidates review.
3. **/grill-with-docs** — stress-test candidate designs and write ADR decisions in `docs/DECISIONS.md`.
4. **gitnexus-refactoring** — runcoordinated renames or file splits, run tests, and check changes.

---

## Summary Matrix

| Skill / MCP Name | One-line Purpose | Primary Trigger | Key Combinations |
|---|---|---|---|
| **airweave** | Semantic quant source search | Local wiki returns thin findings | `autoresearch`, `wiki-ingest` |
| **github** | remote issue/PR tracker interaction | Ticketing plans or triaging bugs | `/to-issues`, `/to-prd`, `/triage` |
| **gitnexus** | Codebase import and graph analysis | Before editing module files | `gitnexus-cli`, `/diagnose` |
| **obsidian** | Vault REST API patches | Sync checks or frontmatter updates | `/save`, `wiki-ingest` |
| **sequential-thinking** | Multi-step reasoning loops | Designs or bugs with >3 unknowns | `/grill-me`, `/diagnose` |
| **shadcn** | frontend components and block management | Building or editing layouts | `/prototype` (UI branch) |
| **caveman** | Drops articles/fluff to cut tokens | context window >80% or user command | `/diagnose`, `/tdd` |
| **diagnose** | Disciplined debugging loop | Bug report or failing tests | `gitnexus-debugging`, `/tdd` |
| **grill-me** | Relentless design interviews | Planning feature architecture | `/to-prd` |
| **grill-with-docs** | Challenge plans against glossary | Terminology/ADR conflict risks | `/to-prd`, `CONTEXT.md` updates |
| **handoff** | Handoff document compilation | Session ends with pending work | `/zoom-out` |
| **improve-codebase-architecture** | Deepens modules for testability | Shallow modules or tight coupling | `gitnexus-exploring`, `/grill-with-docs` |
| **prototype** | Throwaway code validation | Sanity-checking state or UI designs | `/grill-with-docs`, `/tdd` |
| **tdd** | Vertical red-green-refactor loop | Writing business logic/fixes | `/to-issues` |
| **to-issues** | Decomposes plans into tickets | finalized PRD or plan is ready | `/to-prd`, `/tdd` |
| **to-prd** | PRD ticket generation | Ready to specify feature scope | `/grill-with-docs`, `/to-issues` |
| **triage** | Ticket lifecycle management | Backlog grooming/evaluating issues | `/grill-with-docs` |
| **write-a-skill** | new agent skill scaffold | Automation needs not covered by skills | `wiki-lint` |
| **zoom-out** | High-level module maps | Navigating unfamiliar modules | `/improve-codebase-architecture` |
| **setup-matt-pocock-skills** | Skill workspace config | Initial setup or missing target context | `to-issues`, `triage`, `diagnose` |
| **gitnexus-refactoring** | Coordinated symbol rename/splits | Renaming load-bearing functions | `gitnexus-impact-analysis` |
| **gitnexus-debugging** | Call-chain bug tracing | exceptions or wrong returns | `/diagnose` |
| **gitnexus-exploring** | Area and process navigations | Code architecture analysis | `/zoom-out`, `improve-codebase-architecture` |
| **gitnexus-guide** | Schema and tool reference | Designing Cypher queries | `gitnexus-debugging` |
| **gitnexus-cli** | Indexing and database updates | First-time use or stale graph index | Exploring / debugging skills |
| **gitnexus-impact-analysis** | Blast radius calculations | before updating interfaces | `gitnexus-refactoring` |
| **autoresearch** | iterative quant research loops | Researching quant concepts | `wiki-lint`, `canvas` |
| **interrupt** | Interrupt session state save | Session halts mid-task | `wiki/hot.md` update |
| **wiki-lint** | Health check vault auditor | Starting new phases or weekly | `wiki-ingest`, `wiki-fold` |
| **wiki-ingest** | Ingestion of raw sources | Processing files, URLs, or images | `wiki-query`, `allocate-address` |
| **wiki** | coordinate vault layouts | Scaffolding a new vault | `wiki-ingest` |
| **wiki-fold** | Rollup of chronological logs | Exponent batch boundaries reached | `wiki-lint` |
| **wiki-query** | Citations-backed answer engine | Answering domain queries | `/save` |
| **canvas** | visual notes map placement | visual overview/diagram needs | `autoresearch`, `/banana` |
| **save** | Files answers as wiki notes | Resolving useful designs/synthesis | `wiki-query` |
| **obsidian-markdown** | Obsidian syntax formatting | Writing/editing wiki pages | `/save`, `wiki-ingest` |
