# Frontend & Component Design Protocol

---
purpose: Guidelines for building distinctive, dark-first interfaces with high-density layouts and accessible elements
when_to_use: When designing dashboards, refactoring UI components, adding forms, tables, modals, or writing visual styling
when_not_to_use: When executing backend backtests, performing quantitative research, or querying raw option directories
companion_protocols: "[[core-agent-rules.md]], [[mcp-usage-protocol.md]]"
relevant_mcps: shadcn
relevant_skills: "frontend-design"
---

This protocol governs how you structure, style, and verify interfaces in AXIOM. It ensures visual consistency, accessibility compliance, and robust integration of shadcn / Base UI components.

---

## 1. Protocol Trigger Scenario
Activate this protocol automatically whenever the active task includes any UI, styling, layout, or frontend element:
- Keywords: `dashboard`, `page`, `component`, `button`, `form`, `table`, `modal`, `tabs`, `styling`, `contrast`, `UI/UX`, `beautify`.
- Commands: Any custom slash commands related to UI redesign or layout alignment.

---

## 2. Structured Frontend Workflow

### Step 1: Understand the Interface Purpose
- Identify the target user and the core data hierarchy.
- Determine the page density: Axiom prefers high information density with compact spacing (4px grid).
- Establish which data points require Monospace rendering (`Geist Mono`): strategy IDs,option codes, transaction hashes, dates, and currency values.

### Step 2: Consult the Frontend Design Skill
- Open and read the `frontend-design` skill definition: [.agent/skills/frontend-design/SKILL.md](file:///.agent/skills/frontend-design/SKILL.md).
- Keep its constraints (dark-first, Geist fonts, cold cyan rings, Base UI primitives, Vanilla JSX) active.

### Step 3: Discover and Install via Shadcn MCP
- Pair the task with the shadcn MCP server to discover components:
  1. Call `search_items_in_registries` or `list_items_in_registries` to identify matching pre-built blocks or UI elements.
  2. View configuration and dependencies using `view_items_in_registries`.
  3. Install the component using the terminal command: `npx shadcn@latest add [component]` (components will be installed as `.jsx` files inside `components/ui/` automatically).
  4. Call `get_audit_checklist` to verify file integration hygiene.

### Step 4: Assemble and Style the Layout
- Structure the page layout with clean HTML5 semantic landmarks.
- Integrate the newly installed components or custom styled panels.
- Apply `.glass-panel` to floating cards, modals, and overlays.
- Never write hardcoded colors. Use CSS variables defined in `src/index.css` (`bg-background`, `bg-card`, `border-border`, etc.).

### Step 5: Verify the User Experience
- **Focus Rings**: Verify all interactive elements show a Cold Cyan ring (`focus-visible:ring-ring`) when keyboard focused.
- **A11y**: Ensure all inputs have associated labels, and dialog components have descriptive close actions.
- **Contrast & Hierarchy**: Verify primary metrics are distinct, and secondary text is readably styled in `text-muted-foreground`.

---

## 3. Definition of Done (DoD) for UI Tasks
A frontend task is officially **complete** only when it satisfies these criteria:
- [ ] **No Hardcoded Colors**: Every element maps to system CSS variables (`bg-card`, `text-muted-foreground`, etc.).
- [ ] **Zero TypeScript**: All files are written in Vanilla Javascript/JSX (`.js`/`.jsx`). No `.ts` or `.tsx` files exist in components.
- [ ] **Base UI standard**: Components utilize `@base-ui/react` and not `@radix-ui/react`.
- [ ] **Data Monospace**: Strategy hashes, option parameters, backtest outcomes, dates, and times are strictly in `font-mono`.
- [ ] **Accessibility Compliance**: Fully keyboard navigable with clean outlines; Zod validation hooks configured on all forms.
- [ ] **No Heavy Shadows**: Relies entirely on sharp borders (`border-border`) and `.glass-panel` overlays.
