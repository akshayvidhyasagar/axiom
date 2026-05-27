# Planning Protocol

---
purpose: Guidelines for requirements gathering, specifications, PRDs, and task/issue breakdowns
when_to_use: When designing features, writing plans/PRDs, or splitting work into tickets
when_not_to_use: During quick debugging runs or simple code fixes
companion_protocols: "[[core-agent-rules.md]], [[mcp-usage-protocol.md]]"
relevant_mcps: github, gitnexus
relevant_skills: "/to-prd, /to-issues, /grill-me, /grill-with-docs"
---

This protocol outlines how to gather requirements, document implementation plans, compose PRDs, and break down tasks into vertical slices (tracer bullets) ready for implementation.

---

## 1. Requirements Gathering & Grilling
- **Explore Code First**: Before asking the user any questions, check the codebase and active ADRs. Do not ask questions that the code can answer.
- **Grilling Sessions**: If requirements are unclear, initiate a `/grill-me` (for execution details) or `/grill-with-docs` (if domain terminology or glossary mappings are needed) session.
- **Terminology Normalization**: Validate that proposed terms align with the vocabulary inside `CONTEXT.md`. Highlight conflicts immediately.

---

## 2. Implementation Plans (markdown artifacts)
When starting any significant design shift or new feature phase, create or update the `implementation_plan.md` artifact:
- **Design Tree**: Document design branches and hard-to-reverse alternatives.
- **Glossary & ADRs**: Propose new domain terms or ADRs if they represent hard-to-reverse trade-offs.
- **Verification Plan**: Include both automated tests (commands to run) and manual checks.
- **User Review**: Set `request_feedback: true` in metadata and pause for explicit user approval before execution.

---

## 3. Product Requirements Documents (PRDs)
When synthesizing conversation details into a formal PRD (via `/to-prd`), follow this exact layout on the issue tracker:
- **Problem Statement**: The problem from the user's perspective.
- **Solution**: The user-facing solution.
- **User Stories**: An extensive, numbered list of stories in format: *As an <actor>, I want <feature>, so that <benefit>*.
- **Implementation Decisions**: Specific modular boundaries, interface type shapes, and schema changes. Avoid volatile file paths or code snippets (except schema/state prototypes).
- **Testing Decisions**: Behavior-focused verification seams and references to codebase prior art.
- **Out of Scope**: Explicitly bound what will not be built.

---

## 4. Vertical Tracer Bullet Breakdown
When dividing a plan or PRD into trackable issues (via `/to-issues`), apply these rules:
- **Vertical Slices**: Each issue must cut through all integration layers (schema, logic, endpoint, UI, tests). A completed issue must be independently demoable. Do not create horizontal slices (e.g. "Create database tables", "Create API endpoints").
- **Dependency Ordering**: Publish issues in dependency order so that blocking tickets can be referenced.
- **Triage Metadata**: Label issues as `ready-for-agent` (AFK-implementable) or `ready-for-human` (needs human evaluation).
- **Tracer-Bullet Recipe**:
  1. `/grill-with-docs` - align on glossary terms and draft `CONTEXT.md` updates.
  2. `/to-prd` - compile decisions into a formal PRD and post to tracker.
  3. `/to-issues` - break the PRD into vertical, independently-grabbable issues.
  4. `/tdd` - pick issues in order and implement.

---

## 5. Planning Skills Reference Catalog

This catalog details the specific commands, triggers, expected outputs, and operational parameters for planning skills.

### Covered Skills & Tools
- `/grill-me` (Interactive design/clarification interview)
- `/grill-with-docs` (Terminology validation and context alignment)
- `/to-prd` (Synthesizing plan into issue tracker specifications)
- `/to-issues` (Decomposing plan into vertical issues)
- `/tdd` (Test-driven implementation loop execution)
- `/prototype` (Throw-away spike verification)
- `write-a-skill` (Automated custom skill scaffolding)

### Triggers & Usage
- **Requirement Grilling**: Invoke `/grill-me` or `/grill-with-docs` when task instructions are ambiguous, missing domain context, or terminology is not normalized.
- **Spec Synthesizing**: Invoke `/to-prd` when compiling decisions into a formal tracker PRD.
- **Task Decomposing**: Invoke `/to-issues` to break the plan into vertical tracer bullets.
- **Implementation & Spikes**: Invoke `/tdd` for vertical-slice test-first coding, or `/prototype` for validation spikes.

### Expected Output & Artifacts
- **Interactive Interview**: Dynamic choices or interactive terminal questionnaire mapping execution design trees.
- **Tracker PRD**: Structured ticket posted to issue tracker specifying Problem, Solution, User Stories, and modular boundaries.
- **Tracer Issues**: Structured set of vertical issues with dependencies and triage metadata.
- **Spike Sandbox**: Throw-away code sandboxed in `prototype/` directory.

### Failure Modes & Remediation
- **Requirements Ambiguity**: If grilling reveals unresolved requirements, **stop execution** and ask clarifying questions directly.
- **Missing Testing Framework**: If `/tdd` is invoked but no runner is configured, report the gap, propose configuration, and install first.
- **Task Overlap**: If `/to-issues` generates items conflicting with existing issues, flag the overlap to the user before posting.

