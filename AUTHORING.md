# Authoring and the build

Maintainers write plain GitHub Flavored Markdown in `docs/`. No front matter,
no template tags, no HTML. MkDocs turns that tree into the site.

## What the build derives

| Derived | From | Used for |
|---|---|---|
| Page title | the first `#` | `<h1>`, breadcrumb, sidebar entry, `<title>` |
| In-page TOC | every `##` / `###` | the "On this page" sidebar list |
| Section grouping and order | the `nav:` block in `mkdocs.yml` | navbar dropdowns and sidebar |
| Breadcrumb trail | `page.ancestors` | the breadcrumb |

`nav`, `page.toc` and `page.ancestors` are MkDocs' own template variables —
nothing here re-derives them. Ordering lives in `mkdocs.yml` rather than in
filenames, so a page can be renamed without renumbering its neighbours.

## Two conventions that matter

**One `#` per file, at the top.** It is the page's identity everywhere.

**Link to `dir/README.md`, never to `dir/`.** The drafts were authored for
GitHub, where `[Grading](../grading/)` renders that directory's README. MkDocs
publishes pages at directory URLs — `reference/glossary.md` becomes
`/reference/glossary/` — so a link it does not recognise as a document is
passed through untouched and then resolves *relative to the page*: from
`/reference/glossary/`, `../grading/` resolves to `/reference/grading/`, a 404.

`tools/import-docs.py` rewrites these on import (31 of them in the first
import), and `mkdocs build --strict` fails CI on any new one.

## What the import strips

`tools/import-docs.py` drops two kinds of editorial apparatus, because they
address the writing team rather than readers:

- **The leading `> **Draft for review.**` note** on each technical page — 32 of
  them — listing unverified claims, decisions awaiting a person, and missing
  figures. These stay in the upstream repository, which is where they are
  worked on.
- **The root README's "Status of This Documentation" and "Conventions"
  sections.** The first becomes actively false once the notes are gone, since
  it tells the reader that every technical page opens with one; the second is
  contributor guidance that belongs here, not on the site.

The importer will **refuse to run** if any source page has more than one
blockquote. On the first import every noted page had exactly one, always in the
same position, and no page used a blockquote for anything else — that is what
makes stripping safe. If the drafts start using blockquotes for real content,
the invariant breaks and the importer stops rather than silently eating a page.

Two things replace what the notes were doing for a reader:

- **A site-wide draft banner** on every page, from `extra.draft_banner` in
  `mkdocs.yml`. Clear that one value to remove it everywhere; there is no
  per-page markup to hunt down.
- **Visible figure placeholders.** The drafts mark an unpublished number with
  an HTML comment — `| Committed cost | <!-- FIGURE: 4 × the rate --> SU |`.
  Python-Markdown passes comments straight through, so a browser rendered that
  as `Committed cost |  SU`: a worked example with the number silently missing,
  reading as a typo rather than a gap. That was tolerable while each page
  carried a note explaining it. `tools/hooks.py` now renders 20 such markers as
  an inline *figure not published* placeholder, with the detail in the tooltip.

## GFM fidelity

Python-Markdown is **not** GFM. Two gaps are closed so that what renders on
GitHub renders here.

**Heading anchors.** GitHub *deletes* punctuation; Python-Markdown *replaces*
it with the separator and collapses runs:

```
"Peak & Off-Peak Hours"
    GitHub           ->  peak--off-peak-hours
    Python-Markdown  ->  peak-off-peak-hours
```

The drafts' cross-page links are written the GitHub way, so **34 anchor links
were broken by this one rule** on first import — every one a heading
containing `&` or `,`. `tools/hooks.py` installs a github-slugger-compatible
slugify in `on_config`, which fixed all 34. It is installed from the hook
rather than declared in `mkdocs.yml` because a `!!python/name:` reference needs
the project root on `PYTHONPATH` and MkDocs does not add it.

**Alert callouts.** `> [!NOTE]` is not native to Python-Markdown; it renders as
a blockquote with a literal `[!NOTE]` in the text. `tools/hooks.py` maps the
five GitHub alert types to canvas-scoped callouts. Deliberately not Bootstrap's
`.alert-info` / `.alert-warning`: Decorator's `base.css` has no rules for the
`-info`/`-warning`/`-danger` families, so those render in stock Bootstrap
colors on a UC San Diego page.

That transform is harder than it looks. **Python-Markdown merges consecutive
blank-line-separated blockquotes into one `<blockquote>`**, where GitHub keeps
them separate, so the hook splits *inside* a blockquote at each `[!TYPE]`
paragraph. A naive version silently swallowed the second and third callout
into the first.

`pymdown-extensions` supplies the rest — task lists, strikethrough, autolinks,
footnotes — all of which fail without it.

## Search

Site search is lunr, wired into **the Decorator's own search box** — the one in
the header, on every page. Its scope selector offers three choices: *This Site*
(the default, served by lunr) and the two campus scopes, which route back out
to the hosted search API.

- **The chrome form** posts `search-scope` and `search-term` to `/search/`.
- **`theme/js/search-scope.js`** runs in `<head>` on `/search/` and sends a
  campus-scoped query straight to `act.ucsd.edu`, before the page fetches the
  ~800KB index it would not use.
- **`/search/`** renders lunr results for the site scope. Only that page loads
  the search assets; the other 48 pages carry none of it.
- **`theme/search/main.js`** overrides the plugin's copy — a file of that name
  in the theme wins — which is how the upstream bugs below are fixed.

### Why this is not a chrome violation

`protected-regions.md` lists, for this form, what is "site-specific, expected to
differ": the `action` ("sites point at their own search index rather than the
campus redirector"), the `option` values ("a site index adds its own scope"),
and the ids on the term input and scope select ("safe to rename"). All three are
what this change uses. The gate confirms it: tier 3 passes unchanged.

What is **not** changed, and must not be:

| Reserved | Why |
|---|---|
| `id="search"` on the panel | `base.min.css` keys the drawer's mobile layout on it; rename or strip it and the drawer search stops rendering below 768px |
| `name="search-term"` | the hosted search API reads it document-wide |
| `name="search-scope"` | same, and tier 3 pins it explicitly |
| the duplicate `id="search"` across both blocks | intended by the Decorator; "fixing" it has shipped a regression before |

The ids **were** renamed, to `site-search-term-drawer` / `-navbar` and
`site-search-scope-drawer` / `-navbar`. Both blocks previously carried
`id="q"`, so a `<label for>` could only ever bind to the drawer's copy. This
site is the ZIP shape (no `ul.msearch`), so
`toggleIdsAndClassesBasedOnScreenWidth()` never runs here and the rename drops
nothing out of a swap.

The `sr-only` labels are new. The template ships this form with no label at
all, which `protected-regions.md` calls out as wanting a fix on both shapes.

Verified at both viewports: below 768px with the drawer open, the panel is
`#search`, `display: block`, and 49px tall — the floor that document gives as
the "did this collapse" tripwire for a working drawer search.

### Known trade-off

Campus-scope search now depends on JavaScript, because it routes through this
site. It did not before. `/search/` carries a `<noscript>` saying so and linking
to `www.ucsd.edu/search`.

### Four upstream bugs, fixed in the override

**Titles were double-escaped.** MkDocs writes titles into `search_index.json`
already HTML-escaped — 102 of 471 entries here contain `&amp;` — and upstream's
`main.js` escapes again, so results read "Service Units &amp;amp; Budgets".
Summaries are stored raw and still need escaping.

**Upstream reads only `q`.** The chrome form posts `search-term`, a reserved
name that cannot be renamed to `q`. Both are accepted.

**The permalink pilcrow was indexed.** `toc` runs with `permalink: true` and the
plugin indexes rendered text, so 49 of 471 summaries began "Datahub & DSMLP
Documentation ¶ …". `on_post_build` in `tools/hooks.py` strips it from the index
after the plugin writes it, keeping the anchors in the published HTML.

**Unguarded DOM lookups.** `displayResults` and `initSearch` both assume their
elements exist. Guards added.

### A heading slug once collided with a chrome id

Worth keeping in mind when adding pages. The page heading `# Search`
auto-slugged to `id="search"`, and Decorator's `base.min.css` carries
`#search { position: absolute !important }` for its own search panel — the
`<h1>` was torn out of flow and the body text rendered underneath it.
`tools/hooks.py` now prefixes any heading slug landing on a chrome-owned id with
`doc-`. That is the one place the site diverges from GitHub's anchors, and
`--strict` fails on a link relying on the old form.

### The tier 4 finding is a false positive

The gate reports:

```
chrome/styling/script
  file:     search/lunr.js:1373
  selector: function:<module>
  - .id = ... references a protected chrome token
```

Line 1373 is `this.id = lunr.TokenSet._nextId` — lunr numbering its own internal
token sets. It is not DOM access: lunr.js contains no DOM API calls at all (its
`document.` occurrences are all JSDoc comments) and it runs in a Web Worker.
The scanner sees `.id =` and cannot distinguish it from a runtime rewrite of a
chrome element's id.

Clearing it needs a reviewed exception, in `chrome-styling.local.json` at the
repository root. **That file is human-owned — an agent must not write it**, and
tier 4 cannot be cleared with `--accept`. A person adds:

```json
{
  "schemaVersion": 1,
  "allow": [
    {
      "file": "search/lunr.js",
      "selector": "function:<module>",
      "reason": "lunr.js:1373 is `this.id = lunr.TokenSet._nextId`, lunr numbering its own token sets. lunr.js makes no DOM calls and runs in a Web Worker, so it cannot reach a chrome element.",
      "reviewOn": "2027-09-19",
      "approvedBy": "<your name>"
    }
  ]
}
```

`reviewOn` is required and the exception stops applying past that date, so the
judgement gets revisited rather than becoming permanent.

## What CI enforces

1. `mkdocs build --strict` — a broken relative link or anchor fails the build.
2. The Decorator chrome integrity gate — see `DECORATOR.md`.
3. `tools/check-links.py` over the **built** HTML, which catches what MkDocs
   cannot: the theme's own root-relative chrome and sidebar links, and anchors
   after slugification.

Current state of the imported content: **0 dead links, 0 dead anchors across 48
pages**, strict build clean.

## Known gaps

- `docs/images/` contains only a README. It documents the naming convention
  and references `images/datahub-spawn-menu.png` as an example; that file does
  not exist yet, so the example renders as a broken image on `/images/`.
- The published pages no longer carry per-page status. The site-wide banner
  says the set is in draft, but it cannot say *which* claims on a given page
  are unverified — that detail lives only in the upstream notes. If per-page
  status matters for review, the upstream repo is the place to read it.
- The chrome integrity gate reports one tier 4 finding against
  `search/lunr.js`, and it is a false positive. See "Search" below.
