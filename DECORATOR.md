# Decorator 5 in this site: what folds in, what doesn't

An assessment of the [UC San Diego Decorator 5](https://developer.ucsd.edu/design/decorator/index.html)
front-end toolkit against what a static site generator can carry, and how
this repo does it with MkDocs.

## The governing idea: chrome vs. canvas

Decorator is not a runtime include, a CDN widget, or a CMS-side decorator
despite the name. It is **hand-authored HTML that you copy**, plus CSS and JS
loaded from `cdn.ucsd.edu`. What you copy is governed by a formal contract
published in [`UCSD/decorator-kit`](https://github.com/UCSD/decorator-kit):

- **Chrome** — the page shell, identical on every page: header, title band,
  `#uc-emergency`, the mobile offcanvas drawer, the desktop navbar, *both*
  search blocks, and the footer. **Not yours to edit.**
- **Canvas** — `main#main-content`. Everything inside it is yours.

That split is what makes a generated site a good fit rather than a workaround. The
contract explicitly anticipates generated sites: *"In a generated site one
shell file feeds every route; in a hand-authored site every page carries its
own copy."* A generated site is the first case, which is the one the
contract prefers.

## What folds into the theme

| Decorator element | MkDocs mechanism | Notes |
|---|---|---|
| Header, title band, drawer, navbar, footer | `theme/partials/chrome-*.html` + `theme/main.html` | Copied verbatim. One shell feeds every route. |
| Nav `<li>` links (drawer + navbar) | MkDocs' `nav` object, from `mkdocs.yml` | Explicitly sanctioned — see below. |
| Site title in `.title-header` | `config.site_name` / `extra.site_name_short` | Per-site by definition. |
| Breadcrumbs | `theme/partials/breadcrumbs.html`, from `page.ancestors` | Inside the canvas → freely generated. |
| Sidebar nav (`.main-content-nav`) | `theme/partials/sidebar.html`, from `nav` + `page.toc` | Inside the canvas → freely generated. |
| `<head>` metadata | `theme/main.html` | `PAGETITLE`, `DESCRIPTION`, etc. |
| Body content | Markdown | Python-Markdown inside the canvas. |
| Site-specific CSS | `theme/css/site.css` | **Canvas-scoped only.** See below. |

The theme is bespoke (`theme: {name: null, custom_dir: theme}`), not a
Material override. That is the point: no third-party CSS framework loads, so
nothing can collide with the Bootstrap 3 vocabulary the chrome is built on.

**Chrome URLs are root-relative on purpose.** MkDocs' idiomatic `|url` filter
emits paths relative to the current page, which makes the chrome differ by
directory depth — measured as 5 tier 1 "cross-page consistency" failures,
because the chrome must be byte-identical on every route. Do not "fix" the
`/{{ item.url }}` links in `theme/partials/chrome-header.html` to use `|url`.

### Why the nav links are safe to generate

`contracts/chrome-regions.json` marks the drawer's `ul.navmenu-nav` and the
navbar's `ul.nav.navbar-nav` as `ignoreChildrenOf`. Their children are emptied
before the chrome is hashed, precisely so a data-driven nav doesn't trip the
gate. The `<ul>` is chrome; the `<li>`s inside it are yours. This is designed
for exactly this case.

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

**Where site-authored CSS *is* fine:** your own canvas styles. See
`theme/css/site.css`, where every rule is scoped under `main#main-content`. That scoping is
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

The built-in GitHub Pages builder only builds Jekyll, and it runs in safe mode,
so it can build neither this MkDocs site nor the Node-based chrome integrity
gate. `.github/workflows/build-and-deploy.yml` does both.

## Verification status

Built with MkDocs 1.6.1 (`--strict`, zero warnings), then checked with UCSD's
own gate (`checks/chrome-contract.mjs --check`) against the built `_site`:

- **Tier 1 (cross-page consistency) — pass.** All 48 routes share identical
  chrome. Free with a generated site, and the main structural win.
- **Tier 2 (golden fingerprint) — 6 findings, all "no golden recorded yet."**
  Expected first-run state. A human reviews the rendered chrome once and runs
  `--accept` to record the baseline. **Never run that from CI or an agent** —
  it overwrites the record that anything changed.
- **Tier 3 (structural contract) — pass.**
- **Tier 4 (styling/scripting) — pass.** No site CSS reaches the shell, and the
  page ground is unpainted.

Also verified in a headless browser at 1280px and 390px: no JS errors, the
offcanvas drawer toggles and clones as designed, `.row` computes to `block`
(the Bootstrap float grid is intact), the navbar does not wrap, and there is no
horizontal scroll. Link check over the built HTML: 0 dead links, 0 dead
anchors across 48 pages.

In-site search is lunr, wired into the Decorator's own search box. Enabling it
surfaced a real instance of the risk this contract describes: the page heading
`# Search` auto-slugged to `id="search"`, which Decorator's `base.min.css`
absolutely positions for its own search panel, tearing the `<h1>` out of flow.
Heading slugs that would land on a chrome-owned id are now prefixed. The gate's
one remaining tier 4 finding against `search/lunr.js` is a false positive and
needs a human-written exception — see AUTHORING.md.

## Deviations from the shipped template

Three, all deliberate and all matching what live campus sites serve:

1. **Header and footer logo** — the template ships
   `http://cdn.ucsd.edu/developer/decorator/5.0.2/img/…`, an `http://` URL under
   a `5.0.2` directory inside a package versioned `5.0.4`. Mixed content on an
   HTTPS page. Raised to the path production serves.
2. **Navbar search action** — the template's is `http://act.ucsd.edu/…` where
   the drawer's is `https://`. A mixed-content form submission, browser-blocked.
3. **Search form** — `action` points at this site's own `/search/`, a
   "This Site" scope option is added, the term input and scope select carry
   renamed ids, and both controls have `sr-only` labels. `protected-regions.md`
   lists the first three as site-specific and expected to differ, and calls the
   missing labels out as wanting a fix. Tier 3 passes unchanged. The panel's
   `id="search"` and the `search-term` / `search-scope` names are untouched —
   all three are load-bearing document-wide.
4. **Footer links** — the template ships only "Terms & Conditions" and
   "Feedback". Measured 2026-09 against live sites, `edtech.ucsd.edu` and
   `developer.ucsd.edu` both publish four: Accessibility, Privacy, Terms of Use
   and Feedback. The template's pair is stale, and an Accessibility link is
   close to standard on a UC page. Approved by the site owner as a chrome
   change rather than made on a tool's initiative.

## How this compares to a live Cascade site

Measured 2026-09 against `edtech.ucsd.edu` with the same gate:

| | This site | edtech.ucsd.edu |
|---|---|---|
| Gate result | 6 findings, all tier 2 baseline | 12 — **2 tier 1**, 6 tier 2, **4 tier 3** |
| `title-logo` href | `https://www.ucsd.edu` | `http://www.ucsd.edu` |
| Chrome across pages | identical | differs (`tabindex`, logo `alt`) |
| Site search | none | `/search/index.html` (Cascade) |

edtech is the Cascade CMS variant: it emits `ul.msearch` and the 768px id-swap
described in the kit, drops `.layout-login`, and uses `name="as_sitesearch"` in
the navbar where the template uses `search-scope` — which is what fails tier 3.
Its chrome also drifts page to page, which a generated site cannot do.

What it has that this site does not is Cascade infrastructure: a per-site
search collection and a `/search/index.html` to post to.

## Open decisions

1. **Record the chrome golden baseline.** Until a human does, CI's gate step is
   `continue-on-error`.
2. **Write `chrome-styling.local.json`** for the lunr false positive, so the
   gate can run clean. AUTHORING.md has the exact entry.
3. **Whether to adopt the kit wiring** (`npx ucsd-decorator-kit add --with-ci`),
   which adds Dependabot on `ucsd-decorator-v5` plus the kit. Recommended,
   since the CDN moves without notice.
