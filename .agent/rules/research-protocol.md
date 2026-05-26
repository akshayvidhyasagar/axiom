# Research Protocol

---
purpose: Guidelines for autonomous research loops, web searches, and semantic document analysis
when_to_use: When researching quant trading concepts, analyzing papers, or expanding knowledge bases
when_not_to_use: During local codebase refactoring or routine debugging tasks
companion_protocols: "[[core-agent-rules.md]], [[mcp-usage-protocol.md]]"
relevant_mcps: airweave
relevant_skills: "/autoresearch"
---

This protocol outlines how to run autonomous research loops, search and fetch external sources efficiently, and synthesize findings into structured wiki assets.

---

## 1. Autonomous Research Loop (`/autoresearch`)
Follow Karpathy's autoresearch pattern. Output findings directly into the wiki vault.
- **Before Starting**: Read `references/program.md` to load specific confidence scoring objectives, preferred sources, and domain limits.
- **Topic Selection**:
  - *Explicit Topic*: Respect user verbatim requests (e.g. `/autoresearch [topic]`).
  - *Boundary Mode*: If no topic is passed, check if `scripts/boundary-score.py` is present. Run it to surface top 5 frontier pages and let the user select.
- **The Loop Steps**:
  1. *Broad Search*: Decompose the topic into 3-5 angles, run 2-3 searches per angle, and fetch top results. Extract claims, entities, and concepts.
  2. *Gap Fill*: Identify contradictions or missing details and run up to 5 targeted searches.
  3. *Synthesis Check*: Run one final pass if major gaps remain.
- ** Falsification & Contradictions**: Highlight if sources disagree. Do not merge conflicting claims silently.

---

## 2. Web Search & Fetch Constraints
- **De-cluttering**: If `defuddle` is available, run it on fetched URLs to strip ads and navigation clutter to save up to 60% tokens.
- **Token Discipline**:
  - Read `wiki/hot.md` first to see if details already exist.
  - Limit fetches to 3-5 pages per session. Never run unconstrained fetch loops.
  - Do not fetch information from training data if the query is specific to the vault's proprietary domains.

---

## 3. Filing Research Results
File all findings as structured Obsidian markdown pages:
- **`wiki/sources/`**: One summary page per major reference, containing confidence scores and key claims.
- **`wiki/concepts/`**: Distilled concepts. Check index first to update existing pages instead of duplicating.
- **`wiki/entities/`**: Person, organization, or product notes.
- **`wiki/questions/`**: Master synthesis page titled `Research: [Topic]`, detailing key findings, contradictions, and unresolved questions.
- **Registry Update**: Add all new files to `wiki/index.md`, prepend log entries, and update `wiki/hot.md`.

---

## 4. Quant Research & Ingest Recipe
1. **/autoresearch** - Research the quant topic, retrieve web text, and identify gaps.
2. **wiki-ingest** - Read the raw findings, check manifest hashes, and file pages with allocated DragonScale addresses.
3. **wiki-lint** - Run a health check to detect orphans, dead links, or duplicate concepts.
4. **/canvas** - Map concepts and entities onto a visual overview board.
