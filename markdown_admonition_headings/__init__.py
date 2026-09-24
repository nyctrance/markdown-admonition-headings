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

    RE = re.compile(
        r'(?:^|\n)!!![ \t]*([\w\-]+(?: +[\w\-]+)*)(?: +"(.*?)")?(?: +\{:\s*#?([^\s\}]+)\s*\})? *(?:\n|$)'
    )

    def __init__(self, parser, default_heading_level="h2", auto_heading_classes=None):
        super().__init__(parser)
        if auto_heading_classes is None:
            auto_heading_classes = ["ccard"]
        self.default_heading_level = default_heading_level
        self.auto_heading_classes = auto_heading_classes

    def get_admonition_data(self, match: re.Match[str]):
        klass, raw_title = match.group(1).lower(), match.group(2)
        klass = self.RE_SPACES.sub(' ', klass)
        custom_slug = match.group(3)

        if raw_title is None:
            # no title was provided, use the capitalized class name as title
            title = klass.split(' ', 1)[0].capitalize()
        elif raw_title == '':
            # an explicit blank title should not be rendered
            title = None
        else:
            title = raw_title

        classes = klass.split()
        tag = next((c for c in classes if c in ("h1", "h2", "h3", "h4", "h5", "h6")), None)

        if tag is None and any(c in self.auto_heading_classes for c in classes):
            tag = self.default_heading_level

        if tag is None:
            tag = "p"

        return klass, title, tag, custom_slug

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            if m.start() > 0:
                self.parser.parseBlocks(parent, [block[:m.start()]])
            block = block[m.end():]  # removes the first line
            block, theRest = self.detab(block)
        else:
            sibling, block, theRest = self.parse_content(parent, block)

        if m:
            klass, title, tag, custom_slug = self.get_admonition_data(m)
            div = etree.SubElement(parent, 'div')
            div.set('class', f"{self.CLASSNAME} {klass}")
            if title:
                title_elem = etree.SubElement(div, tag)
                title_elem.text = title
                title_elem.set('class', self.CLASSNAME_TITLE)
                if custom_slug:
                    title_elem.set('id', custom_slug)
        else:
            # Sibling is a list item, but we need to wrap its content in <p>
            if sibling.tag in ('li', 'dd') and sibling.text:
                text = sibling.text
                sibling.text = ''
                p = etree.SubElement(sibling, 'p')
                p.text = text

            div = sibling

        self.parser.parseChunk(div, block)

        if theRest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, theRest)


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
