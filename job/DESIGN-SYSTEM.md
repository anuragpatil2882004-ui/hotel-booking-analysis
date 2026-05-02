# KodNest Premium Build System

A premium SaaS design system for B2C product companies. Calm, intentional, coherent, confident.

---

## Design Philosophy

- **Calm** — No gradients, glassmorphism, neon, or animation noise
- **Intentional** — Every decision serves clarity and purpose
- **Coherent** — One mind designed it; no visual drift
- **Confident** — Generous spacing, clear hierarchy, no hype language

---

## Color System (Maximum 4 Colors)

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#F7F6F3` | Page background (off-white) |
| Text Primary | `#111111` | Headings, body text |
| Accent | `#8B0000` | Primary actions, focus states, links |
| Success | `#5A6B5A` | Shipped, completed, positive feedback |
| Warning | `#9A7B4F` | In progress, attention needed |

**Do not add** gradients, neon colors, or decorative palettes.

---

## Typography

### Headings (Serif)
- Font: Cormorant Garamond
- Fallback: Georgia, Times New Roman
- Large, confident, generous spacing
- Letter-spacing: -0.02em

### Body (Sans-serif)
- Font: Source Sans 3
- Fallback: Helvetica Neue, Arial
- Size: 16–18px
- Line-height: 1.6–1.8
- Max width for text blocks: 720px

---

## Spacing Scale (Strict)

Use only these values: **8px, 16px, 24px, 40px, 64px**

| Token | Value |
|-------|-------|
| `--kn-space-xs` | 8px |
| `--kn-space-sm` | 16px |
| `--kn-space-md` | 24px |
| `--kn-space-lg` | 40px |
| `--kn-space-xl` | 64px |

Never use random spacing (13px, 27px, etc.). Whitespace is part of the design.

---

## Global Layout Structure

Every page follows this hierarchy:

```
[Top Bar]
    ├── Left: Project name
    ├── Center: Progress indicator (Step X / Y)
    └── Right: Status badge (Not Started / In Progress / Shipped)

[Context Header]
    ├── Large serif headline
    └── 1-line subtext, clear purpose

[Primary Workspace (70%)] | [Secondary Panel (30%)]
    ├── Main product interaction
    │   ├── Clean cards
    │   └── Predictable components
    └── Step explanation
        ├── Copyable prompt box
        └── Buttons: Copy, Build in Lovable, It Worked, Error, Add Screenshot

[Proof Footer]
    └── Checklist: □ UI Built □ Logic Working □ Test Passed □ Deployed
```

---

## Components

### Buttons
- **Primary**: Solid deep red (`#8B0000`), white text
- **Secondary**: Outlined, transparent background
- Same hover effect and border radius (`6px`) everywhere

### Inputs
- Clean borders, no heavy shadows
- Clear focus state (border + subtle ring)
- Height: 44px

### Cards
- Subtle border, no drop shadows
- Balanced padding (24px or 40px for large)

### Status Badges
- `kn-badge-not-started` — Neutral
- `kn-badge-in-progress` — Muted amber
- `kn-badge-shipped` — Muted green

---

## Interaction Rules

- Transitions: 150–200ms, ease-in-out
- No bounce, no parallax
- Hover states: subtle, consistent

---

## Error & Empty States

### Errors
- Explain what went wrong
- Explain how to fix it
- Never blame the user

### Empty States
- Provide the next action
- Never feel dead

---

## File Structure

```
design-system/
├── index.css      # Main entry (imports all)
├── tokens.css     # Colors, typography, spacing, layout variables
├── base.css       # Reset, typography, body
├── components.css # Buttons, inputs, cards, badges, prompt box, checklist
├── layout.css     # Top bar, context header, workspace, panel, proof footer
└── states.css     # Error and empty states
```

---

## Usage

```html
<link rel="stylesheet" href="design-system/index.css">
```

```css
@import './design-system/index.css';
```

---

*KodNest Premium Build System — One mind. No drift.*
