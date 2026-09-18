# Decorator 5 → Jekyll: what folds in, what doesn't

An assessment of the [UC San Diego Decorator 5](https://developer.ucsd.edu/design/decorator/index.html)
front-end toolkit against what Jekyll can generate for this GitHub Pages site,
plus the scaffold in this repo that verifies it.

## The governing idea: chrome vs. canvas

Decorator is not a runtime include, a CDN widget, or a CMS-side decorator
despite the name. It is **hand-authored HTML that you copy**, plus CSS and JS
loaded from `cdn.ucsd.edu`. What you copy is governed by a formal contract
published in [`UCSD/decorator-kit`](https://github.com/UCSD/decorator-kit):

- **Chrome** — the page shell, identical on every page: header, title band,
  `#uc-emergency`, the mobile offcanvas drawer, the desktop navbar, *both*
  search blocks, and the footer. **Not yours to edit.**
- **Canvas** — `main#main-content`. Everything inside it is yours.

That split is what makes Jekyll a good fit rather than a workaround. The
contract explicitly anticipates generated sites: *"In a generated site one
shell file feeds every route; in a hand-authored site every page carries its
own copy."* Jekyll is the first case, which is the one the contract prefers.

## What folds into Jekyll

| Decorator element | Jekyll mechanism | Notes |
|---|---|---|
| Header, title band, drawer, navbar, footer | `_includes/decorator/*.html` + `_layouts/default.html` | Copied verbatim. One shell feeds every route. |
| Nav `<li>` links (drawer + navbar) | `_data/navigation.yml` + Liquid loop | Explicitly sanctioned — see below. |
| Site title in `.title-header` | `site.title` / `site.title_short` | Per-site by definition. |
| Breadcrumbs | `_includes/breadcrumbs.html` | Inside the canvas → freely generated. |
| Sidebar nav (`.main-content-nav`) | `_includes/sidebar-nav.html` | Inside the canvas → freely generated. |
| Page templates (two-column, blank-slate, three-column, homepage) | `_layouts/*.html` | One layout per template. |
| `<head>` metadata | Front matter → `_layouts/default.html` | `PAGETITLE`, `DESCRIPTION`, etc. |
| Body content | Markdown | Kramdown/GFM inside the canvas. |
| Site-specific CSS | `_sass/` + `assets/css/site.scss` | **Canvas-scoped only.** See below. |

### Why the nav links are safe to generate

`contracts/chrome-regions.json` marks the drawer's `ul.navmenu-nav` and the
navbar's `ul.nav.navbar-nav` as `ignoreChildrenOf`. Their children are emptied
before the chrome is hashed, precisely so a data-driven nav doesn't trip the
gate. The `<ul>` is chrome; the `<li>`s inside it are yours. This is designed
for exactly the Jekyll case.

### Why breadcrumbs and sidebar nav are safe to generate

In the shipped `two-column.html`, both sit *inside* `main#main-content`
(verified by byte offset: `<main>` at 6798, breadcrumb at 6907, sidebar at
31872, `<footer>` at 33062). They are canvas, not chrome.

## What does not fold in

**Decorator's CSS and JS must stay CDN-linked.** This is the big one, and it
directly limits the "just use raw Sass" approach.

The source Sass *does* compile — verified here, `app/styles/base.scss` and
`bootstrap.scss` both build clean under Dart Sass 1.104 (exit 0, ~100
`slash-div` and `@import` deprecation warnings, removed in Dart Sass 2.0/3.0).
So it is technically possible. Three reasons not to:

1. **Policy.** The contract is explicit: *"Keep Decorator CSS and JS pointed at
   `cdn.ucsd.edu`. Do not vendor them for serving."*
2. **A live defect in the vendored build.** `ucsd-decorator-v5@5.0.4`'s own
   `dist/css/base.min.css` emits eleven corrupted `rgb()` declarations mixing a
   unitless channel with percentages — invalid CSS that browsers drop entirely.
   The visible symptom is the active nav item falling back to Bootstrap grey
   `#e7e7e7` instead of `#004268`. The CDN copy is plain hex and has none of it.
3. **Drift you cannot detect.** The CDN is unversioned, has no manifest
   (`version.json` is 404), and its directory listing is 403. A self-compiled
   copy silently diverges from what campus actually serves, with no signal.

**Where raw Sass *is* the right tool:** your own canvas styles. Jekyll's
built-in Sass handles this with no extra toolchain — see `_sass/_canvas.scss`,
where every rule is scoped under `main#main-content`. That scoping is
load-bearing, not cosmetic: the shell and the canvas share the entire
Bootstrap 3 vocabulary, so a bare `.input-group { }` reaches into the drawer
search without naming a single chrome class.

Also dropped, as Cascade-CMS-specific or obsolete:

- `_resources/` paths, `respond.proxy.js`, IE8/IE9 conditional blocks
- `tdr_login` / TritonLink logout plumbing (`decorator.js`)
- `initFooter()` / `initCopyright()` helpers — the CDN `base.min.js` already
  fills `.footer-copyright-year`, which is why it ships empty. Don't emit a
  build-time year: it goes stale *and* it changes the pinned footer hash.
- developer.ucsd.edu's own Google Analytics tag

## Known upstream defects, and the two deviations made here

The shipped template contains markup that is broken over HTTPS. Both fixes are
technically chrome edits and both are flagged here rather than made silently:

1. **Logo path.** The template ships
   `http://cdn.ucsd.edu/developer/decorator/5.0.2/img/ucsd-footer-logo-white.png`
   — an `http://` URL under a `5.0.2` directory, inside a package versioned
   `5.0.4`. Mixed content on an HTTPS page. Changed to the path production
   actually serves: `https://cdn.ucsd.edu/cms/decorator-5/styles/img/…`.
2. **Navbar search action.** The drawer's form posts to
   `https://act.ucsd.edu/…`; the navbar's posts to `http://act.ucsd.edu/…`.
   The second is a mixed-content form submission, blocked by modern browsers.
   Raised to `https://`.

Neither is a restyle — both restore what production already does. They still
belong in a reviewed diff, which is what this PR is.

Two more upstream facts worth knowing:

- **Both search blocks must be copied, verbatim, once per container.** They
  look redundant (same `id="search"`, same `id="q"`) but dropping the navbar
  one removes search on every viewport above 768px, silently. The duplicate ids
  are deliberate.
- **`Decorator-V5.zip` is not a source of truth.** Re-cut 2026-07-22, it still
  ships a January 2023 `base.min.js` missing the runtime behavior the CDN
  serves. Read the npm package instead.

## Build path: Actions, not the built-in Pages builder

| | Built-in Pages builder | GitHub Actions |
|---|---|---|
| Jekyll | 3.10.0 (pinned) | any |
| Sass | jekyll-sass-converter 1.5.2 → Ruby Sass 3.7.4 (EOL 2019) | Dart Sass |
| Plugins | 47-gem allowlist, safe mode | any |
| Chrome integrity gate | **cannot run** (Node) | yes |

Verified against `https://pages.github.com/versions.json`. The gate is the
deciding factor: it's a Node check over built HTML, so the built-in builder
can't run it at all.

## Verification status of this scaffold

Built with Jekyll 4.4.1 / jekyll-sass-converter 3.1.0, then checked with
UCSD's own gate (`checks/chrome-contract.mjs --check`) against the built
`_site`:

- **Tier 1 (cross-page consistency) — pass.** All routes share byte-identical
  chrome. This is free with Jekyll and is the main structural win.
- **Tier 2 (golden fingerprint) — 6 findings, all "no golden recorded yet."**
  Expected first-run state. A human reviews the rendered chrome once and runs
  `--accept` to record the baseline. **Never run that from CI or an agent** —
  it overwrites the record that anything changed.
- **Tier 3 (structural contract) — pass.**
- **Tier 4 (styling/scripting) — pass.** No site CSS reaches the shell, and the
  page ground is unpainted.

Internal link check: 0 dead links.

## Open decisions

1. **Which template.** This scaffold demonstrates `two-column` (sidebar nav,
   the usual docs shape) and `blank-slate`. `three-column` and `homepage` are
   also available. The kit deliberately requires a human to choose.
2. **Whether to adopt the kit wiring** (`npx ucsd-decorator-kit add --with-ci`),
   which adds Dependabot on `ucsd-decorator-v5` + the kit, the CI gate, and
   agent rule files. Recommended, since the CDN moves without notice.
3. **Site search.** The template's search posts to the campus-wide redirect at
   `act.ucsd.edu` and offers only "All UCSD Sites" / "Faculty/Staff" — there is
   no "This Site" scope. Searching *this* site needs something else, and the
   search block itself is chrome.
