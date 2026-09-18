# Vanilla Markdown → navigation: what the build step can and can't derive

Maintainers write plain GitHub Flavored Markdown in `docs/`. No front
matter, no Liquid, no HTML. `_plugins/vanilla_docs.rb` turns that tree into
the site at build time.

## The constraint nobody expects

**Jekyll does not render a Markdown file that has no YAML front matter.**
It treats it as a static file and copies it through verbatim — the `.md`
lands in the output as `.md`, never becoming HTML. This is true for pages
*and* for collection documents; `defaults:` in `_config.yml` does not change
it, because the presence of front matter is itself the signal to render.

Verified:

```
_site/pages-style/no-front-matter.md        <- copied, not rendered
_site/updated-docs/collection-no-fm.md      <- copied, not rendered
```

So "maintainers write vanilla Markdown" is not a stock-Jekyll configuration.
Something has to synthesize what front matter would normally supply. That is
what the generator does, and it is why this only works on Actions — the
built-in GitHub Pages builder runs in safe mode and will not load
`_plugins/`.

## What the build step derives, reliably

| Derived | From | Used for |
|---|---|---|
| Page title | first `#` in the file | `<h1>`, breadcrumb, sidebar entry, `<title>` |
| In-page TOC | every `##` / `###` | "On this page" sidebar list |
| Anchor ids | the **rendered** HTML | TOC links that always resolve |
| Section title | the directory's `index.md` `#`, else the directory name | sidebar and breadcrumb |
| Within-section order | optional `NN-` filename prefix | sidebar order |
| URL | path, with `NN-` stripped | `docs/getting-started/10-accounts.md` → `/docs/getting-started/accounts/` |

Anchor ids are read out of the rendered HTML rather than computed from the
heading text. That matters: kramdown suffixes duplicate headings (`#dup`,
`#dup-1`), and any attempt to re-implement its slugging drifts. Reading the
output means the TOC links are the ids kramdown actually emitted. Verified:
0 dead in-page anchors across the built site.

## What headings cannot give you

**Ordering.** This is the real limit, and it is the thing that matters most
for documentation. Headings tell you what a page is called, never where it
belongs in a reading sequence. Without a signal, files sort alphabetically,
which puts "Advanced Tuning" before "Getting Started". Two ways out, both
supported:

- a `NN-` filename prefix (`10-accounts.md`, `20-launch.md`), stripped from
  the URL — keeps ordering visible in the file tree and in GitHub's own
  listing, costs maintainers nothing but a two-digit prefix;
- a hand-maintained list, which is what `_data/navigation.yml` is for.

**Which sections belong in the global navbar.** That is editorial, not
derivable. `_data/navigation.yml` stays hand-maintained on purpose.

**Anything about a directory with no `index.md`.** The generator falls back
to humanizing the directory name (`getting-started` → "Getting Started"),
which is usually fine and occasionally wrong. Add an `index.md` when it is
wrong.

**Cross-references.** A link to a page that moves is a dead link; nothing in
the heading structure catches it. The link check in CI does.

## GFM support, measured

Kramdown's GFM parser covers most of it. Verified against a fixture page
(`docs/markdown-reference.md`, which stays in the site so a kramdown upgrade
breaks visibly):

Works as on GitHub — tables with alignment, fenced code with language and
syntax highlighting, strikethrough, task lists with checkboxes, footnotes,
duplicate-heading id suffixing, and soft line breaks (kramdown does not hard
wrap, matching GitHub's rendering of `.md` files in a repository).

Did **not** work, and is now handled by the generator:

- **GitHub alert callouts.** `> [!NOTE]` came out as a blockquote with a
  literal `[!NOTE]` in the body text. Now mapped to a styled callout.
  Deliberately not Bootstrap's `.alert-info` / `.alert-warning`: Decorator's
  `base.css` has no rules for the `-info`/`-warning`/`-danger` families, so
  those render in stock Bootstrap colors on a UC San Diego page.
- **Bare URLs.** Not linked. Now autolinked, skipping anything already
  inside an anchor, inline code, a code block, or an attribute — verified no
  nested `<a>` and no `<a>` inside `<code>`.

Still unsupported, documented for maintainers rather than worked around:
`:emoji:` shortcodes stay literal, and bare `www.` URLs are not linked.

## Honest assessment

For **in-page navigation** — the "On this page" TOC — headings are entirely
sufficient, and the result is better than hand-maintained because it cannot
go stale.

For **between-page navigation**, headings get you titles and grouping but
not sequence. The `NN-` prefix convention closes that gap at a cost of two
characters per filename, which is the cheapest option that keeps ordering
visible to someone browsing the repo on GitHub. Expect to keep the top-level
navbar hand-maintained regardless; it is four lines of YAML and it is an
editorial decision.

The thing to watch is that the generator is now load-bearing custom code. It
is ~150 lines of Ruby that runs on every build. If that is more than the team
wants to own, the alternative is a purpose-built docs generator — MkDocs
Material or Docusaurus both consume vanilla Markdown natively and solve
ordering with a small nav file — at the cost of re-doing the Decorator chrome
integration, which is the part this repo has already verified.
