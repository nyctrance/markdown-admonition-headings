"""
markdown_admonition_headings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Python-Markdown extension that renders admonition callout titles as true
HTML heading tags (<h1>–<h6>) with automatic Table-of-Contents hierarchy,
heading permalinks, and custom slug overrides ({:better-slug}).
"""

import re
import xml.etree.ElementTree as etree
from markdown.extensions import Extension
from markdown.extensions.admonition import AdmonitionProcessor


class HeadingAdmonitionProcessor(AdmonitionProcessor):
    """
    Enhanced AdmonitionProcessor that:
    1. Supports optional heading levels in class list (e.g. `h1` through `h6`).
    2. Supports default heading level for specified card classes (e.g. `ccard` -> `h2`).
    3. Supports custom slug overrides at end of declaration (e.g. `{:better-slug}` or `{: #better-slug }`).
    4. Renders the title element as a heading tag (<h1-h6>) so Python-Markdown's
       Table of Contents (TOC) extension automatically indexes it, computes anchors,
       and attaches permalinks.
    """

    # Matches:
    # !!! type [h1-h6] "Title" [{: [#]custom-slug}]
    # ???[+] type [h1-h6] "Title" [{: [#]custom-slug}]
    RE = re.compile(
        r'(?:^|\n)!!! ?([\w\-]+(?: +[\w\-]+)*)(?: +"(.*?)")?(?: +\{:\s*#?([^\s\}]+)\s*\})? *(?:\n|$)'
    )

    def __init__(self, parser, default_heading_level="h2", auto_heading_classes=None):
        super().__init__(parser)
        if auto_heading_classes is None:
            auto_heading_classes = ["ccard"]
        self.default_heading_level = default_heading_level
        self.auto_heading_classes = auto_heading_classes

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            if block.startswith(' ' * self.tab_length):
                block = block[m.end():]
                status = 'sub'
            elif block.startswith('!!!'):
                status = 'new'
                total_class = m.group(1)
                title = m.group(2)
                custom_slug = m.group(3)
                block = block[m.end():]
            else:
                status = 'orphan'
        else:
            status = 'sub'

        if status == 'new':
            classes = total_class.split()
            # Check for explicit h1-h6 in classes
            tag = next((c for c in classes if c in ("h1", "h2", "h3", "h4", "h5", "h6")), None)

            # If not specified, check if any class matches auto-heading classes
            if tag is None and any(c in self.auto_heading_classes for c in classes):
                tag = self.default_heading_level

            if tag is None:
                tag = "p"

            div = etree.SubElement(parent, "div", attrib={"class": f"admonition {total_class}"})
            if title is not None:
                title_attrs = {"class": "admonition-title"}
                if custom_slug:
                    title_attrs["id"] = custom_slug
                h = etree.SubElement(div, tag, attrib=title_attrs)
                h.text = title
            elif self.first_as_title:
                self.first_as_title = False
                title_attrs = {"class": "admonition-title"}
                if custom_slug:
                    title_attrs["id"] = custom_slug
                h = etree.SubElement(div, tag, attrib=title_attrs)
                h.text = classes[0].capitalize()

            self.parser.parseBlocks(div, [block])
        elif status == 'sub':
            self.parser.parseBlocks(sibling, [block])


class HeadingAdmonitionExtension(Extension):
    """Python-Markdown extension for Heading Admonitions."""

    def __init__(self, **kwargs):
        self.config = {
            "default_level": ["h2", "Default heading level when auto-heading class is present"],
            "auto_classes": [["ccard"], "Classes that automatically convert titles to headings"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        default_level = self.getConfig("default_level")
        auto_classes = self.getConfig("auto_classes")
        md.parser.blockprocessors.register(
            HeadingAdmonitionProcessor(
                md.parser,
                default_heading_level=default_level,
                auto_heading_classes=auto_classes,
            ),
            "admonition",
            105,
        )


def makeExtension(**kwargs):
    return HeadingAdmonitionExtension(**kwargs)
