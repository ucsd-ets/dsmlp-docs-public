# Markdown Reference

What you can write in these files, and what it turns into. Everything on
this page is plain GitHub Flavored Markdown — no front matter, no Jekyll
tags, no HTML. If it renders correctly on GitHub, it renders here.

This page doubles as a rendering fixture: if a kramdown upgrade ever breaks
one of these, it breaks here first.

## Headings become navigation

Every `##` and `###` on a page is collected into the "On this page" list in
the sidebar, automatically. You do not need to maintain a table of contents.

The first `#` on the page becomes the page title, the breadcrumb label, and
the sidebar entry. Write exactly one, at the top.

## Tables

| Resource | Default | Enforcement |
|---|--:|:-:|
| Home directory | 100 GB | soft |
| Concurrent GPUs | 1 | hard |

## Code

Inline `launch-scipy-ml.sh`, and fenced blocks with a language get
syntax highlighting:

```python
def launch(gpus: int = 1) -> None:
    print(f"requesting {gpus}")
```

## Callouts

GitHub's alert syntax works:

> [!NOTE]
> Useful information a reader should know.

> [!WARNING]
> Home directories are not backed up.

> [!TIP]
> Pass `-i` to pin a specific container image.

Supported: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`.

## Lists, task lists, strikethrough

- [x] provisioned
- [ ] verified

~~Deprecated~~ items render struck through.

## Links

Ordinary [links](https://dsmlp-docs.ucsd.edu) work, and a bare URL like
https://dsmlp-docs.ucsd.edu is linked automatically.

Links between docs pages use the path the page is published at:
`[Accounts](/docs/getting-started/accounts/)`.

## Footnotes

Supported.[^1]

[^1]: Rendered at the bottom of the page with a back-link.

## What is not supported

- `:emoji:` shortcodes stay literal — paste the character instead.
- Bare `www.` URLs are not auto-linked; write the full `https://`.
- Raw HTML is discouraged: it can reach outside the content area and
  trip the Decorator chrome check.
