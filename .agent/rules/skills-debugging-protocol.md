# Skills Debugging Protocol

This file contains the detailed protocol for all debugging‑related skills.

## Covered Skills
- `diagnose`
- `zoom-out`
- `sequential-thinking`
- `gitnexus-debugging`
- `gitnexus-refactoring`
- `gitnexus-impact-analysis`

## Purpose
Provides a structured workflow for diagnosing bugs, performing root‑cause analysis, and applying refactorings with safety checks.

## Trigger Phrases
- User invokes `/diagnose` when a bug or failing test is reported.
- User runs `/zoom-out` to get a high‑level module map before debugging.
- User calls `/sequential-thinking` for complex multi‑step reasoning.
- User uses any GitNexus debugging MCP commands.

## Workflow Overview
1. **Reproduce Issue** – Create a minimal reproducible case or failing test.
2. **Gather Context** – Run `gitnexus-debugging` to obtain call‑chain and impact data.
3. **Hypothesis Generation** – Use `sequential-thinking` to list plausible causes.
4. **Instrument & Test** – Add logging or breakpoints as needed.
5. **Apply Fix** – Implement change, run tests, and verify.
6. **Safety Check** – Run `gitnexus-impact-analysis` to ensure no regressions.
7. **Documentation** – Record the bug fix in the wiki via `save`.

## Expected Output
- Reproduced test case or error log.
- Call‑chain trace and impact report.
- List of hypotheses with confidence levels.
- Fixed code with passing tests.
- Updated wiki entry documenting the bug and resolution.

## Failure Modes
- Non‑reproducible bug – abort and request more information.
- Missing GitNexus index – run `gitnexus-cli` to rebuild.
- Refactoring introduces regressions – revert and re‑analyse.

## Combinations
- Often paired with `planning-protocol.md` when fixing bugs as part of a larger feature.
- May invoke `knowledgebase-protocol.md` to fetch related documentation.
