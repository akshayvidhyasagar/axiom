# SKILL: Interrupt Handler

Trigger: session ends mid-task without completing the assigned goal (blocker, ambiguity, external dependency, token limit).

## Steps

1. **Do not run the full END protocol.**

2. **Write to wiki/hot.md under "Active Threads":**
   - What task was in progress
   - Exactly where it stopped (file, function, step number)
   - What is blocking completion
   - What the next session must do first

3. **Append to wiki/log.md at TOP:**
   `## [YYYY-MM-DD] chore | interrupt — <task title>`

4. **Commit:**
   ```bash
   git add -A
   git commit -m "chore: interrupt — <one line on what was left incomplete>"
   ```

5. **Do not update docs/CHANGELOG.md** — incomplete sessions do not get a changelog entry. The next session's END protocol will cover both sessions if needed.

## When to invoke
- Ambiguity that cannot be resolved without Akshay input
- Missing dependency (file, API key, data) that blocks all forward progress
- Session approaching context limit before task is complete
- Conflicting state discovered that requires a decision before proceeding
