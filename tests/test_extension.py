import unittest
import markdown
from markdown_admonition_headings import HeadingAdmonitionExtension


class TestHeadingAdmonitions(unittest.TestCase):
    def setUp(self):
        self.md = markdown.Markdown(
            extensions=[HeadingAdmonitionExtension(), "toc"]
        )

    def test_default_heading_level_for_ccard(self):
        text = '!!! ccard "Default Title"\n    Card content'
        html = self.md.convert(text)
        self.assertIn('<h2 class="admonition-title" id="default-title">Default Title</h2>', html)
        self.assertIn('<a href="#default-title">Default Title</a>', self.md.toc)

    def test_explicit_h3_heading_level(self):
        text = '!!! ccard h3 "Nested Subtitle"\n    Sub content'
        html = self.md.convert(text)
        self.assertIn('<h3 class="admonition-title" id="nested-subtitle">Nested Subtitle</h3>', html)
        self.assertIn('<a href="#nested-subtitle">Nested Subtitle</a>', self.md.toc)

    def test_custom_slug_override(self):
        text = '!!! ccard h3 "Original Title" {:better-slug}\n    Content'
        html = self.md.convert(text)
        self.assertIn('<h3 class="admonition-title" id="better-slug">Original Title</h3>', html)
        self.assertIn('<a href="#better-slug">Original Title</a>', self.md.toc)

    def test_custom_slug_with_hash_syntax(self):
        text = '!!! ccard "Another Title" {: #custom-id }\n    Content'
        html = self.md.convert(text)
        self.assertIn('<h2 class="admonition-title" id="custom-id">Another Title</h2>', html)
        self.assertIn('<a href="#custom-id">Another Title</a>', self.md.toc)

    def test_toc_nesting_hierarchy(self):
        text = (
            "# Main\n\n"
            '!!! ccard "Section 1"\n    Content\n\n'
            '!!! ccard h3 "Subsection 1.1"\n    Content\n\n'
            '!!! ccard "Section 2"\n    Content\n'
        )
        self.md.convert(text)
        toc = self.md.toc
        self.assertIn('<a href="#main">Main</a>', toc)
        self.assertIn('<a href="#section-1">Section 1</a>', toc)
        self.assertIn('<a href="#subsection-11">Subsection 1.1</a>', toc)
        self.assertIn('<a href="#section-2">Section 2</a>', toc)

    def test_standard_admonition_fallback(self):
        # A standard admonition without ccard or h1-h6 should remain a <p>
        text = '!!! note "Standard Note"\n    Regular note content'
        html = self.md.convert(text)
        self.assertIn('<p class="admonition-title">Standard Note</p>', html)

    def test_admonition_body_not_rendered_as_code_block(self):
        text = (
            '!!! ccard "Title"\n'
            '    This is regular text with **bold**.\n'
            '\n'
            '    * Item 1\n'
            '    * Item 2\n'
        )
        html = self.md.convert(text)
        self.assertNotIn('<pre>', html)
        self.assertNotIn('<code>', html)
        self.assertIn('<p>This is regular text with <strong>bold</strong>.</p>', html)
        self.assertIn('<ul>', html)
        self.assertIn('<li>Item 1</li>', html)


    def test_multi_paragraph_admonition(self):
        text = (
            '!!! ccard "Multi Paragraph"\n'
            '    Paragraph one.\n'
            '\n'
            '    Paragraph two.\n'
        )
        html = self.md.convert(text)
        self.assertIn('<p>Paragraph one.</p>', html)
        self.assertIn('<p>Paragraph two.</p>', html)
        self.assertNotIn('<pre>', html)

    def test_empty_title_admonition(self):
        text = '!!! note ""\n    No title content'
        html = self.md.convert(text)
        self.assertNotIn('admonition-title', html)
        self.assertIn('<p>No title content</p>', html)

    def test_unspecified_title_admonition(self):
        text = '!!! note\n    Default title content'
        html = self.md.convert(text)
        self.assertIn('<p class="admonition-title">Note</p>', html)


if __name__ == "__main__":
    unittest.main()
