---
name: frontend-design
description: Production-grade frontend design and styling rules for Axiom. Use this skill when doing ANY UI/UX work, including building dashboards, cards, forms, tables, modals, interactive displays, charts, custom layouts, or adding shadcn/Base UI components.
when_to_use: When implementing user interfaces, writing/editing JSX components, configuring styles in index.css, refining layouts, or adding/modifying component primitives.
when_not_to_use: For backend algorithmic logic, mathematical data strategies, data client syncing, or pure CLI script maintenance.
companion_mcp: shadcn
classification: on-demand
---

# Frontend Design Skill — Axiom

Axiom uses a **high-precision, developer-grade** visual aesthetic inspired by sleek scientific tools, Notion, Vercel, and Linear. The design is dark-first, utilizing a slate neutral base, striking cold cyan highlights, border-based hierarchies, and glassmorphic micro-shadows.

---

## 1. Stack Definition

Axiom's actual stack is strictly configured as follows:
- **Core Library**: **React 19.2+** using modern, functional components.
- **Language**: **Vanilla Javascript & JSX (`.js`/`.jsx`)** only. Do NOT use TypeScript (`.ts`/`.tsx`).
- **Styling Engine**: **Tailwind CSS v4.3.0** (using new inline theme variables in `src/index.css` via `@theme inline`).
- **Primitives**: **Base UI (`@base-ui/react`)** for shadcn components (not Radix UI or headless UI).
- **Icons**: **Lucide Icons (`lucide-react`)** only.
- **Build System**: **Vite** (Vite config in workspace root).

---

## 2. Visual & Theme Tokens

All styles must reference the workspace variables inside `src/index.css` to match the **Axiom Obsidian Dark** palette:

| Token / Color | Value | CSS Variable | Purpose |
| :--- | :--- | :--- | :--- |
| **Page Background** | `#09090b` | `var(--background)` | Main dark backdrop |
| **Card / Panel Background** | `#111113` | `var(--card)` | Floating boxes and dashboard blocks |
| **Primary Text** | `#e4e4e7` | `var(--foreground)` | Readable headers and body |
| **Secondary Text** | `#71717a` | `var(--muted-foreground)` | Secondary descriptions and metadata labels |
| **Accent / Highlight** | `#00d4ff` | `var(--accent)` | Cold Cyan for interactive states, badges |
| **Borders & Dividers** | `hsl(240 4% 14%)` | `var(--border)` | Subtle structural lines (no heavy shadows) |
| **Focus Ring** | `#00d4ff` | `var(--ring)` | Active interactive keyboard rings |
| **Radius** | `0.5rem` (8px) | `var(--radius)` | Structural corner rounding |

### Special Visual Effect: `.glass-panel`
Always apply `.glass-panel` for cards, overlays, dialog backdrops, and floating panels:
```css
.glass-panel {
  background: oklch(1 0 0 / 0.03);
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
  border: 1px solid hsl(var(--border));
  border-radius: calc(var(--radius) + 4px);
  box-shadow:
    0 0 0 1px oklch(1 0 0 / 0.04),
    0 8px 32px oklch(0 0 0 / 0.4),
    inset 0 1px 0 oklch(1 0 0 / 0.08);
}
```

---

## 3. Typography & Hierarchy

- **UI Headings & Body**: `font-sans` (`'Geist'`, system-ui, sans-serif)
- **Data, Metadata, & Metrics**: `font-mono` (`'Geist Mono'`, monospace) — **MANDATORY** for:
  - Hash values, strategy IDs, option codes, transaction IDs.
  - Dates, times, timestamps, and raw matrix counts.
  - Floating-point calculations, backtest returns, or percentage stats.
- **Hierarchy via Weights**: Always use typography weights (`font-medium`, `font-semibold`) rather than shifting text colors, maintaining a high-legibility layout.

---

## 4. Component Selection Rules

When building interfaces, select elements in this order of precedence:
1. **shadcn Blocks (UI Layout Templates)**: If assembling dashboards, sidebars, charts, or tables, search for pre-configured shadcn blocks first using the shadcn MCP server.
2. **shadcn Primitives (Base UI)**: If a specific interactive element (e.g. `dialog`, `badge`, `tabs`, `scroll-area`, `sheet`) is needed, use the pre-installed components inside `components/ui/` built on `@base-ui/react`.
3. **Custom Styled Elements**: Only write custom JSX when no block or primitive exists. Style them using Tailwind classes combined with `.glass-panel` and standard variables.

---

## 5. Composition & Interaction Patterns

### 5.1 Forms & Input Patterns
- **Validation**: Use **Zod** schema validations on the client side.
- **Status States**:
  - Valid: Outline/border remains `border-border`.
  - Focus: Ring expands with Cold Cyan: `focus-visible:ring-ring`.
  - Invalid: Border flashes red `border-destructive` and uses `aria-invalid="true"`.
- **Labels**: Always associate labels with inputs using HTML `htmlFor` and unique, descriptive IDs.

### 5.2 Dashboards & Cards
- Use standard `<Card>` components with explicit `size="default"` or `size="sm"` variables.
- Utilise `@container/card-header` and `group/card` classes for responsive sub-layouts.
- Use a **4px grid spacing system** (e.g., `gap-1`, `gap-2`, `gap-4`, `p-4`, `py-3`).

### 5.3 Data Tables
- Use `font-mono` for data rows.
- Ensure column headers are clearly distinct using `text-muted-foreground` and `font-medium`.
- Pad cells tightly to maintain high information density without visual clutter.

### 5.4 Dialogs & Sheets
- Dialog overlays must use `.glass-panel` styling with custom backdrop filters.
- Dialog transitions must slide or fade smoothly using `tw-animate-css` directives.

### 5.5 Destructive Actions
- Any action that deletes data, resets backtest caches, or truncates strategies must use a destructive button:
  ```jsx
  <Button variant="destructive">Delete Strategy</Button>
  ```
- Must be accompanied by a double-confirmation modal or warning tooltip.

---

## 6. Feedback States: Loading, Empty, & Error

Do not show blank screens. Ever. Provide deterministic feedback:
- **Loading State**: Use `<Skeleton>` components matching the layout of the target data card. Never use raw text "Loading...".
- **Empty State**: Show a muted illustration or icon from `lucide-react` paired with a clear, cyan call-to-action button (e.g., "Generate First Factor").
- **Error State**: Render inline red alert blocks with a prominent "Retry" action. Keep detailed error messages (like Python stack traces) folded inside a `<details>` tag in `font-mono`.

---

## 7. Accessibility (A11y) Requirements

- **Interactive Outlines**: All interactive buttons, inputs, and tabs must have clear focus rings: `focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50`.
- **Keyboard Navigation**: Tabs, modals, and sheets must be fully keyboard navigable (automatic via Base UI primitives).
- **Contrast**: Text contrast must exceed `4.5:1` against backgrounds (checked by standard neutral-slate colors).
- **Semantics**: Use HTML5 elements (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`) to define page structures.

---

## 8. Anti-Patterns to Avoid

- ❌ **NO TypeScript**: Never write `.ts` or `.tsx` files. The project is strictly Javascript/JSX (`.js`/`.jsx`).
- ❌ **NO Radix UI imports**: Do not install `@radix-ui/react-*` components. Axiom is standardized on `@base-ui/react` (Base UI).
- ❌ **NO Hardcoded Colors**: Never use custom hex strings (e.g. `#ffffff` or `bg-white`) in components. Always use Tailwind theme tokens (`bg-background`, `bg-card`, `border-border`, etc.).
- ❌ **NO Legacy Tailwind Config**: Do not attempt to modify a `tailwind.config.js` file. Tailwind CSS v4 is used; configure custom theme colors directly inside `src/index.css` via `@theme inline`.
- ❌ **NO Heavy Drop Shadows**: Avoid traditional large box shadows. Rely on sharp borders (`border-border`) and the custom backdrop-filter blur of `.glass-panel`.

---

## 9. Workflow Steps with Shadcn MCP

When adding new components to the interface:
1. **Discover**: Call the shadcn MCP tools to check for available components:
   - Call `search_items_in_registries({ query: "chart" })` or similar to see options.
   - Call `view_items_in_registries({ name: "chart" })` to inspect code and peer dependencies.
2. **Install**:
   - Use the terminal command: `npx shadcn@latest add [component]` (this command will automatically install the component as Javascript `.jsx` file inside `components/ui/` since `"tsx": false` is configured).
3. **Verify**:
   - Call `get_audit_checklist` from the shadcn MCP server to run a post-installation audit on the component files.
4. **Scaffold**: Integrate the component into the page using the visual and theme tokens defined in this skill.

---

## 10. Quality Checklist

- [ ] Does the component file end with `.jsx`? (No `.tsx` allowed)
- [ ] Are all imports from `@base-ui/react` (Base UI) and not `@radix-ui`?
- [ ] Are all colors mapped to CSS variables (`bg-background`, `border-border`, `bg-card`)?
- [ ] Are dates, timestamps, code snippets, IDs, and financial metrics in `font-mono`?
- [ ] Does the design look stunning in dark mode using `.glass-panel` where appropriate?
- [ ] Have you tested keyboard focus ring visibility (`focus-visible`) on all interactive buttons/links?
