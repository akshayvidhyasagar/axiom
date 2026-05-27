# Debugging & Testing Protocol

---
purpose: Guidelines for bug diagnosis, instrumentation, TDD loops, and performance profiling
when_to_use: When reproducing bugs, fixing regressions, writing tests, or optimizing execution paths
when_not_to_use: For documentation updates or pure code formatting
companion_protocols: "[[core-agent-rules.md]], [[mcp-usage-protocol.md]]"
relevant_mcps: gitnexus, sequential-thinking
relevant_skills: "/diagnose, /tdd, /zoom-out, gitnexus-debugging"
---

This protocol outlines how to isolate bugs systematically, instrument code safely, apply test-driven development, and profile slow paths without causing regressions.

---

## 1. Disciplined Bug Diagnosis
Skip steps only when explicitly justified. Do not guess fixes.
- **Phase 1: Build a Feedback Loop**: Construct a fast, deterministic, agent-runnable pass/fail signal (e.g. unit/integration test, curl script, fuzzer harness). Spend disproportionate effort here; a 2-second deterministic loop is key to diagnosis.
- **Phase 2: Reproduce**: Confirm the loop replicates the exact symptom described by the user. Do not proceed until reproduced.
- **Phase 3: Hypothesize**: Generate 3-5 ranked, falsifiable hypotheses before testing any of them. Format: *If X is the cause, changing Y will make it disappear.* Present them to the user.
- **Phase 4: Instrument**: Change one variable at a time. Tag every debug log with a unique prefix, e.g. `[DEBUG-xxxx]`, for easy cleanup.
- **Phase 5: Fix & Regression-Test**: Write the regression test before the fix (if a correct test seam exists). Run tests, apply fix, watch them pass, then run the Phase 1 loop against the original scenario.
- **Phase 6: Cleanup**: Remove all tagged logs (`grep` the prefix) and throwaway files before declaring victory.

---

## 2. Test-Driven Development (TDD)
- **Behavior-Focused Integration Tests**: Tests must verify behavior through public interfaces, not internal implementation details. Good tests survive structural refactoring.
- **Incremental Loops**:
  - Vertical slices only (one test -> minimal code -> pass -> repeat).
  - Never write all tests first, then all implementations (horizontal slicing).
- **Refactoring Rules**: Never refactor code while in a RED (failing test) state. Get to GREEN first, then refactor, running tests at each step.

---

## 3. Performance & Regression Profiling
- **Baseline Harnesses**: For performance regressions, logs are often misleading. Establish a baseline measurement (timing harness, `performance.now()`, query plans).
- **Measurement Precision**: Isolate CPU, memory, and network resources. Measure first, compile findings, optimize, and verify against the baseline.

---

## 4. Hard Bug Recipe
1. `/zoom-out` - Map out callers and callers' contexts using glossary terms.
2. **sequential-thinking MCP** - Analyze interdependencies, state assumptions, and identify potential causes.
3. `/diagnose` - Create a deterministic repro loop, rank hypotheses, instrument, and fix.
4. `/tdd` - Write behavior-focused integration tests to lock down the fix.

---

## 5. Debugging Skills Reference Catalog

This catalog details the specific commands, triggers, expected outputs, and operational parameters for debugging skills.

### Covered Skills & Tools
- `/diagnose` (Structured bug diagnosis and instrumentation loop)
- `/zoom-out` (Fast, high-level context/glossary mapping)
- `sequential-thinking` (Multi-step chain-of-thought analysis)
- `gitnexus-debugging` (Read-only call chain analysis and bug pathfinding)

### Triggers & Usage
- **Bug Diagnosis**: Invoke `/diagnose` when a crash, unexpected behavior, or test regression is reported.
- **Context Gathering**: Invoke `/zoom-out` before modifying files to understand high-level code layout and callers.
- **Complex Reasoning**: Invoke `sequential-thinking` for reasoning on hard design problems with more than 3 unknown variables.
- **Tool-Based Call Trace**: Call `gitnexus-debugging` to extract upstream call chains and isolate where a bug is introduced.

### Expected Output & Artifacts
- **Bug Repro**: A fast, deterministic pass/fail reproducer (test case or script).
- **Hypothesis Log**: A list of 3-5 falsifiable hypotheses.
- **Trace Analysis**: Impact/blast radius analysis or call chain diagram.
- **Verified Code**: Regression-tested code with zero temporary debug logs remaining.

### Failure Modes & Remediation
- **Non-Reproducible Bugs**: If the issue cannot be replicated, **do not proceed** with changes. Re-evaluate steps, consult logs, or ask the user for details.
- **Stale Workspace Graph**: If GitNexus references stale code, run the indexing command to rebuild the repository map.
- **Refactoring Regressions**: If a bug fix breaks adjacent code, immediately revert and analyze tests in a GREEN state.

