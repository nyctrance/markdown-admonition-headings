# Markdown Admonition Headings

A Python-Markdown extension that renders admonition callout titles as true HTML heading tags (`<h1>`–`<h6>`) with automatic Table-of-Contents hierarchy, heading permalinks, and custom slug overrides (`{:better-slug}`).

---

## The Problem

Standard Python-Markdown admonitions (`!!! note "Title"`) render their titles as simple `<p class="admonition-title">` paragraph elements. Because they are not genuine heading elements (`<h1>`–`<h6>`):
* They are **ignored by the Table of Contents** (`toc`) extension.
* They **cannot be nested** into your document's outline.
* They do not generate automatic heading anchors or permalinks.
* Adding custom slug syntax (like `{: #my-slug}`) after the title causes standard admonitions to fail parsing entirely.

## The Solution

`markdown-admonition-headings` replaces the standard admonition processor to:
1. **Convert titles into true headings**: Turn any callout title into an `<h1>`–`<h6>` element.
2. **Nest cleanly in the Table of Contents**: Sidebar navigation trees reflect the exact heading level specified.
3. **Support custom slug overrides**: Specify `{:better-slug}` or `{: #better-slug }` directly in the admonition header.
4. **Permalinks for free**: Heading permalink icons (`¶`) attach automatically.

---

## Installation

```bash
pip install markdown-admonition-headings
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/nyctrance/markdown-admonition-headings.git
```

---

## Usage

### MkDocs

In your `mkdocs.yml`:

```yaml
markdown_extensions:
  - admonition_headings
  - toc:
      permalink: true
```

*(Note: `admonition_headings` is a drop-in replacement for standard `admonition`).*

### In Python

```python
import markdown

md = markdown.Markdown(extensions=["admonition_headings", "toc"])
html = md.convert('!!! ccard h3 "Nested Subtitle" {:better-slug}\n    Content here')
```

---

## Syntax Examples

### Explicit Heading Levels (`h1`–`h6`)

Specify the heading level alongside your admonition type:

```markdown
!!! ccard h2 "Main Section"
    Content for main section...

!!! ccard h3 "Detailed Sub-topic"
    Content for detailed sub-topic...
```

Generated HTML:
```html
<div class="admonition ccard h2">
  <h2 class="admonition-title" id="main-section">Main Section</h2>
  <p>Content for main section...</p>
</div>
<div class="admonition ccard h3">
  <h3 class="admonition-title" id="detailed-sub-topic">Detailed Sub-topic</h3>
  <p>Content for detailed sub-topic...</p>
</div>
```

Resulting Table of Contents:
```text
• Main Section (H2)
  └── Detailed Sub-topic (H3)
```

---

### Custom Slug Overrides

Override the auto-generated slug using `{:custom-slug}` or `{: #custom-slug }`:

```markdown
!!! ccard h3 "Speed Trance Format & Rules" {:speed-trance-format}
    All practiced skills will be taught and rotated...
```

Generated HTML:
```html
<div class="admonition ccard h3">
  <h3 class="admonition-title" id="speed-trance-format">Speed Trance Format & Rules</h3>
  ...
</div>
```

Now you can link directly to this card from anywhere:
```markdown
[Read about the format](events.md#speed-trance-format)
```

---

### Works With All Admonition Types

You can use explicit heading levels on any built-in or custom admonition type:

```markdown
!!! danger h2 "Consequences & Boundaries" {:or-else-what}
    Ejection and community bans apply...

!!! tip h3 "Pro Tip"
    Always calibrate before deepening...
```

---

### Round-Robin Card Styling Recipe (for Material for MkDocs)

To give your cards cycling colors automatically, add this to your `docs/stylesheets/extra.css`:

```css
/* 5-Color Round-Robin Palette for .ccard */
.md-typeset :is(.admonition.ccard, details.admonition.ccard):nth-child(5n + 1 of .admonition.ccard) { --card-color: #a855f7; }
.md-typeset :is(.admonition.ccard, details.admonition.ccard):nth-child(5n + 2 of .admonition.ccard) { --card-color: #f59e0b; }
.md-typeset :is(.admonition.ccard, details.admonition.ccard):nth-child(5n + 3 of .admonition.ccard) { --card-color: #818cf8; }
.md-typeset :is(.admonition.ccard, details.admonition.ccard):nth-child(5n + 4 of .admonition.ccard) { --card-color: #2dd4bf; }
.md-typeset :is(.admonition.ccard, details.admonition.ccard):nth-child(5n + 5 of .admonition.ccard) { --card-color: #f472b6; }

.md-typeset .admonition.ccard {
  border-left-color: var(--card-color) !important;
  border-radius: 8px;
}

.md-typeset .admonition.ccard > .admonition-title {
  background-color: color-mix(in srgb, var(--card-color) 12%, transparent) !important;
  border-left-color: var(--card-color) !important;
}
```

Now any card tagged `ccard` rotates colors while keeping its document heading hierarchy!

---

## License

MIT License. Copyright (c) 2026 nyctrance.
