# Porting the Decorator chrome to MkDocs or Docusaurus

Both were spiked against the same content and measured with the same tool:
UCSD's own `checks/chrome-contract.mjs`, plus a headless-Chromium probe of
the live runtime with Jekyll and MkDocs as controls.

## Result

| | Jekyll (this repo) | MkDocs, custom theme | Docusaurus |
|---|---|---|---|
| Chrome gate | 6 × tier 2 only | **6 × tier 2 only** | 6 × tier 2 **+ 14 × tier 4** |
| Tier 4 clearable by `--accept`? | n/a | n/a | **no, by design** |
| `.row` computed style | `block` (correct) | `block` (correct) | **`flex` (grid broken)** |
| Decorator JS at runtime | clean | clean | clean *after* a fix |
| Vanilla Markdown | needs ~150-line plugin | **native** | native |
| Nav / TOC / breadcrumbs | custom plugin | **built in** | built in |
| GFM fidelity | native + ~40 lines | needs 1 dep + ~35 lines | native |

"6 × tier 2 only" is the same clean state this repo's Jekyll build reaches —
six "no golden recorded yet" findings awaiting a human baseline, nothing else.

## MkDocs — viable, and in one respect better than what we have

Reached parity with the Jekyll build. Tiers 1, 3 and 4 all pass.

**What MkDocs gives you for free that cost ~150 lines of Ruby here:** `nav`,
`page.toc`, and `page.ancestors` are first-class template variables. The
entire `_plugins/vanilla_docs.rb` generator — title extraction, TOC building,
section grouping, breadcrumb ancestry — is replaced by using the objects
MkDocs already hands the theme. Ordering comes from the explicit `nav:` block
in `mkdocs.yml`, so the `NN-` filename convention isn't needed either.

Use a **custom theme** (`theme: {name: null, custom_dir: theme}`), not a
Material override. A bespoke theme is just Jinja2 templates, so the Decorator
chrome *is* the theme and no third-party CSS loads at all. Material would
reintroduce the same class-collision problem Docusaurus has.

Work required, all of it verified:

1. **Port the chrome from Liquid to Jinja2.** Mechanical; the markup is
   unchanged. Half a day including the canvas templates.
2. **Use root-relative URLs in the chrome — one line, but load-bearing.**
   MkDocs' idiomatic `|url` filter emits paths relative to the current page,
   so the chrome's own links differ by directory depth (`../..` vs `..` vs
   `.`). That produced **5 tier 1 failures** — the chrome must be
   byte-identical across every route. Emitting `/{{ item.url }}` cleared all
   five.
3. **Add `pymdown-extensions` for GFM.** MkDocs uses Python-Markdown, which
   is *not* GFM. Out of the box, task lists, strikethrough and autolinks all
   failed. One dependency plus ~8 lines of config fixes those; measured.
4. **Port the alert-callout transform (~35 lines, `hooks.py`).** Harder than
   the Jekyll version for a specific reason: **Python-Markdown merges
   consecutive blank-line-separated blockquotes into one `<blockquote>`**,
   where GitHub and kramdown keep them separate. A naive port silently
   swallowed the second and third callout into the first. The hook has to
   split *inside* a blockquote at each `[!TYPE]` paragraph.
5. **Decide about search.** MkDocs bundles lunr.js, and enabling it produced
   a tier 4 finding; disabling it cleared the gate completely. The deeper
   issue is that the Decorator chrome already owns `#search`, `#q` and
   `#search-scope`, pointed at the campus-wide redirect, so a docs search
   needs its own UI inside the canvas with different ids. Same constraint
   applies to Jekyll — MkDocs just forces the decision sooner.

**Estimate: 1–2 days.** The migration is real but bounded, and it deletes
custom code rather than adding it.

## Docusaurus — blocked on CSS, not on effort

The chrome markup goes in fine. Swizzle `Layout`, drop Docusaurus' own
`Navbar`/`Footer`, and inject the chrome via `dangerouslySetInnerHTML` so
React never diffs inside it. Tiers 1, 2 and 3 all pass.

Two findings, one fixable and one not.

**Fixable — script placement (~15-line plugin).** Docusaurus' `scripts:`
config injects into `<head>`. The Decorator requires its stack at the end of
`<body>`, and this is not cosmetic: `base.min.js` runs
`$(".navbar-static-top .search-toggle")[0].addEventListener` with no null
guard, so in `<head>` it throws `TypeError: Cannot read properties of
undefined` and the desktop search toggle is dead. Jekyll and MkDocs controls
threw nothing, confirming it is placement, not a Decorator bug. A plugin
using `injectHtmlTags`/`postBodyTags` fixes it — after which the runtime
matches the controls exactly: Jasny registers, the drawer toggles, the
offcanvas clone appears, `body.canvas-slid` is set, no errors.

Worth stating plainly: **the React/jQuery conflict I expected did not
materialise.** With `dangerouslySetInnerHTML`, client-side navigation and
back/forward left the chrome intact and produced no duplicate drawers.

**Not fixable — Infima.** Docusaurus' CSS framework defines the *same class
names* as Bootstrap 3, which is what the Decorator chrome is built on:

| Selector | Infima | Bootstrap 3 / Decorator |
|---|---|---|
| `.row` | `display:flex; flex-wrap:wrap` | `margin-left:-15px` (**float grid**) |
| `.container` | `max-width:var(--ifm-container-width)` | Bootstrap responsive widths |
| `.navbar` | own background, shadow, fixed height | `.navbar-default` Decorator styling |
| `.footer` | own background, color, padding | Decorator blue `#00629b` |
| `.dropdown` | `display:inline-flex` | `position:relative` |

`.row` is the one that decides it. The Decorator's two-column layout is
Bootstrap's **float** grid with `pull-right`; Infima makes `.row` a flex
container. Measured in a real browser: `.row` computes to `display: flex` on
Docusaurus and `block` on both controls. That is the chrome's layout broken,
not merely recolored.

The gate reports 14 tier 4 findings, and **tier 4 cannot be cleared by
`--accept`** — deliberately, because the markup is intact so regenerating a
baseline would only hide the finding. Site CSS is also forbidden from
targeting chrome classes, so the normal override route is closed too.

I tested the obvious escape: stripping the colliding rules from the built
CSS. Removing 11 rules took tier 4 from 14 findings to 5. It does not reach
clean, and it is post-build regex surgery on minified vendor CSS that breaks
on every Docusaurus upgrade.

The only sound Docusaurus path is building on `@docusaurus/core` with a
custom theme that never loads `theme-classic`. That means reimplementing
navbar, sidebar, TOC, pagination and search in React — **1–2 weeks**, and it
discards most of the reason to choose Docusaurus.

## Recommendation

Stay on Jekyll, or move to MkDocs with a custom theme. Between those two it
is close: MkDocs deletes the custom generator and gives ordering a cleaner
home, Jekyll is already built and verified. MkDocs is the better long-term
shape if the team is more comfortable in Python than Ruby.

Do not use Docusaurus for a Decorator-chromed site. The blocker is not
effort, it is that Infima and Bootstrap 3 claim the same class vocabulary and
disagree about what `.row` means.

## Reproducing

```bash
# gate, from any built output directory
node checks/chrome-contract.mjs --check
```

Spikes were built from this repo's `docs/` tree unchanged.
