# Component Documentation Template

This file defines the **section order, content rules, and formatting conventions** that `scripts/generate-doc.mjs` implements. Treat it as the spec — the converter already applies every rule here, so do not hand-assemble docs by checking off this list.

---

## Section Order

Every generated doc follows this structure (omit any section that has no data):

1. **Frontmatter** *(optional, `--frontmatter` flag)* — YAML block: title, description, status, version, category, tags, figma URL, source, lastUpdated.
2. **Overview** — `# ComponentName`, links row (`Open in Figma` | `View Source` | `Storybook`), `## Overview` prose, optional `### When to Use` / `### When NOT to Use` bullet lists parsed from the component description.
3. **Component Anatomy** — `## Component Anatomy`: variant count list (COMPONENT_SET only), then `### Design Structure (Figma)` fenced code block with the ASCII layer tree.
4. **Variants** — `## Variants`: Variant Matrix table (background + text/icon color per variant, token names preferred), Icon Mapping table (if icons present), Configurable Properties table (variants/booleans/textProps).
5. **Token Specification** — `## Token Specification`: Color Tokens table (element → Figma variable → hex), Spacing Tokens table (property → Figma variable → px value).
6. **Typography** — `## Typography`: table of unique text styles (element, font, weight, size, line height, letter spacing). Deduplicated by `fontFamily:weight:size:lineHeight`.
7. **Content Guidelines** — `## Content Guidelines`: subsections parsed from the component description (`### <heading>`). Omit if empty.
8. **Implementation** *(optional, `--code-info`)* — `## Implementation`: Source Files table, Import snippet, Variant Definition snippet, Component API props table, Sub-components, Events, Slots, Usage Examples.
9. **Accessibility** — `## Accessibility`: bullet list from `accessibilityNotes` parsed out of description, or a placeholder note if none found.
10. **Design Annotations** — `## Design Annotations`: each annotation with category label, markdown body, and pinned properties list. Placeholder if none found.
11. **Design-Code Parity** *(optional, `--code-info` + COMPONENT_SET)* — `## Design-Code Parity`: Variant Coverage table (In Figma / In Code / Status).
12. **Changelog** *(optional, `--code-info`)* — `## Changelog`: table of version / date / changes entries.

---

## Key Rules

### `cleanVariantName`
Convert raw Figma variant names like `Type=Image, Size=12` → `Image / 12`:
- Extract the **value** side of each `Key=Value` pair.
- Join with ` / `.
- If no `Key=Value` pattern is found, return the name unchanged.

### Omit empty sections
Do not emit a section heading if it would have no content (no rows, no bullets, no prose).

### Prefer token names over hardcoded values
In all token/color tables, show the Figma variable name (e.g. `` `color/primary/500` ``) alongside the resolved hex. If no variable is bound, show `—` (a signal to replace the hardcode with a token).

### Description parsing (for Overview, Content Guidelines, Accessibility)
Parse the component description for these plain-text or `### ` / `**` headers:
- `When to Use` → `parsedDesc.whenToUse[]`
- `When NOT to Use` / `When to Not Use` / `Don't Use` → `parsedDesc.whenNotToUse[]`
- `Accessibility` / `A11y` → `parsedDesc.accessibilityNotes[]`
- `Content Guidelines` / `Content Requirements` / `Writing Guidelines` → `parsedDesc.contentGuidelines[]`

Everything before the first recognized header becomes `parsedDesc.overview`.

### Links row format
```
**[Open in Figma](<figma-url>)** | **[View Source](<path>)** | **[Storybook](<path>)**
```
Only include links for which data is available.

### Variant matrix column set
- Always: `Variant`, `Background`, `Text/Icon Color`
- Add `Icon` column only if any variant has icon instances detected.

### Typography deduplication
Skip rows with identical `fontFamily:fontWeight:fontSize:lineHeight` key — show each unique style once.
