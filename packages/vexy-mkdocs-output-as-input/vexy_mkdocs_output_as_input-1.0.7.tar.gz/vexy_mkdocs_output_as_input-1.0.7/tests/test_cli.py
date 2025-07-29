"""Tests for the CLI tool."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from mkdocs_output_as_input.cli import (
    extract_frontmatter,
    main,
    process_file,
    process_html,
)


class TestCLI:
    """Test cases for CLI functionality."""

    def test_extract_frontmatter_with_frontmatter(self):
        """Test extracting YAML frontmatter from content."""
        content = """---
title: Test Title
author: Test Author
---

# Content here
"""
        frontmatter, body = extract_frontmatter(content)
        
        assert frontmatter == {"title": "Test Title", "author": "Test Author"}
        assert body.strip() == "# Content here"

    def test_extract_frontmatter_without_frontmatter(self):
        """Test extracting from content without frontmatter."""
        content = "# Just content"
        frontmatter, body = extract_frontmatter(content)
        
        assert frontmatter == {}
        assert body == "# Just content"

    def test_extract_frontmatter_invalid_yaml(self):
        """Test handling invalid YAML frontmatter."""
        content = """---
title: Test
invalid: [unclosed
---

# Content
"""
        frontmatter, body = extract_frontmatter(content)
        
        # Should handle gracefully
        assert frontmatter == {}
        assert body == content

    def test_process_html_basic(self):
        """Test basic HTML processing."""
        html = """<!DOCTYPE html>
<html>
<body>
<main class="content">
<h1>Title</h1>
<p>Content</p>
</main>
</body>
</html>"""
        
        result = process_html(html)
        
        assert result is not None
        assert '<article class="content">' in result
        assert '<h1>Title</h1>' in result
        assert '<p>Content</p>' in result

    def test_process_html_custom_element_and_tag(self):
        """Test processing with custom element and tag."""
        html = """<html>
<body>
<div id="content">
<h1>Title</h1>
</div>
</body>
</html>"""
        
        result = process_html(html, html_element="div", target_tag="section")
        
        assert result is not None
        assert '<section id="content">' in result
        assert '<h1>Title</h1>' in result

    def test_process_html_element_not_found(self):
        """Test handling when element not found."""
        html = "<html><body><p>No main element</p></body></html>"
        
        result = process_html(html)
        
        assert result is None

    def test_process_html_preserve_links(self):
        """Test preserving relative links."""
        html = """<html>
<body>
<main>
<a href="/docs/page.html">Link</a>
<img src="/images/pic.png">
<a href="https://example.com">External</a>
</main>
</body>
</html>"""
        
        result = process_html(html, preserve_links=True)
        
        assert result is not None
        assert 'href="./docs/page.html"' in result
        assert 'src="./images/pic.png"' in result
        assert 'href="https://example.com"' in result  # External unchanged

    def test_process_html_minify(self):
        """Test HTML minification."""
        html = """<html>
<body>
<main>
    <h1>Title</h1>
    <p>Content</p>
</main>
</body>
</html>"""
        
        result = process_html(html, minify=True)
        
        assert result is not None
        assert "\n" not in result
        assert "  " not in result

    def test_process_html_prettify(self):
        """Test HTML prettification."""
        html = "<html><body><main><h1>Title</h1><p>Content</p></main></body></html>"
        
        result = process_html(html, prettify=True)
        
        assert result is not None
        assert "\n" in result
        assert " <h1>" in result  # Indented

    def test_process_file_basic(self, tmp_path):
        """Test basic file processing."""
        # Create input HTML file
        input_file = tmp_path / "input.html"
        input_file.write_text("""<html>
<body>
<main>
<h1>Test Page</h1>
</main>
</body>
</html>""")
        
        output_file = tmp_path / "output.md"
        
        process_file(input_file, output_file)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "<article>" in content
        assert "<h1>Test Page</h1>" in content

    def test_process_file_with_frontmatter(self, tmp_path):
        """Test processing with frontmatter from corresponding .md file."""
        # Create input HTML file
        input_file = tmp_path / "page.html"
        input_file.write_text("<html><body><main><h1>Page</h1></main></body></html>")
        
        # Create corresponding markdown file with frontmatter
        md_file = tmp_path / "page.md"
        md_file.write_text("""---
title: Test Page
author: Test Author
---

# Original content
""")
        
        output_file = tmp_path / "output.md"
        
        process_file(input_file, output_file)
        
        content = output_file.read_text()
        assert "---" in content
        assert "title: Test Page" in content
        assert "author: Test Author" in content
        assert "<article>" in content

    def test_process_file_no_frontmatter(self, tmp_path):
        """Test processing without frontmatter."""
        input_file = tmp_path / "input.html"
        input_file.write_text("<html><body><main><h1>Page</h1></main></body></html>")
        
        output_file = tmp_path / "output.md"
        
        process_file(input_file, output_file, include_frontmatter=False)
        
        content = output_file.read_text()
        assert not content.startswith("---")
        assert "<article>" in content

    def test_process_file_creates_output_dir(self, tmp_path):
        """Test that output directory is created if needed."""
        input_file = tmp_path / "input.html"
        input_file.write_text("<html><body><main><h1>Page</h1></main></body></html>")
        
        output_file = tmp_path / "subdir" / "output.md"
        
        process_file(input_file, output_file)
        
        assert output_file.exists()
        assert output_file.parent.exists()

    def test_cli_process_command(self, tmp_path):
        """Test CLI process command."""
        input_file = tmp_path / "input.html"
        input_file.write_text("<html><body><main><h1>Test</h1></main></body></html>")
        
        output_file = tmp_path / "output.md"
        
        with patch("sys.argv", ["mkdocs-output-as-input", "process", 
                               str(input_file), str(output_file)]):
            result = main()
        
        assert result == 0
        assert output_file.exists()

    def test_cli_custom_options(self, tmp_path):
        """Test CLI with custom options."""
        input_file = tmp_path / "input.html"
        input_file.write_text("<html><body><div id='content'><h1>Test</h1></div></body></html>")
        
        output_file = tmp_path / "output.md"
        
        with patch("sys.argv", [
            "mkdocs-output-as-input", "process",
            str(input_file), str(output_file),
            "--html-element", "div",
            "--target-tag", "section",
            "--no-frontmatter",
            "--preserve-links",
            "--prettify",
            "--verbose"
        ]):
            result = main()
        
        assert result == 0
        content = output_file.read_text()
        assert "<section" in content
        assert not content.startswith("---")

    def test_cli_mutually_exclusive_options(self, tmp_path):
        """Test that minify and prettify are mutually exclusive."""
        input_file = tmp_path / "input.html"
        input_file.write_text("<html><body><main><h1>Test</h1></main></body></html>")
        
        output_file = tmp_path / "output.md"
        
        with patch("sys.argv", [
            "mkdocs-output-as-input", "process",
            str(input_file), str(output_file),
            "--minify", "--prettify"
        ]):
            result = main()
        
        assert result == 1  # Should fail

    def test_cli_no_command(self):
        """Test CLI with no command shows help."""
        with patch("sys.argv", ["mkdocs-output-as-input"]):
            result = main()
        
        assert result == 1

    def test_cli_file_not_found(self, tmp_path):
        """Test CLI with non-existent input file."""
        input_file = tmp_path / "nonexistent.html"
        output_file = tmp_path / "output.md"
        
        with patch("sys.argv", ["mkdocs-output-as-input", "process",
                               str(input_file), str(output_file)]):
            result = main()
        
        assert result == 1