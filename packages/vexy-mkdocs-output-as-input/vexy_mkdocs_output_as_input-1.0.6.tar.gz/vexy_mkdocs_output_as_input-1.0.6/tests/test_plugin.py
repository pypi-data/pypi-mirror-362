# this_file: more/mkdocs-plugins/vexy-mkdocs-output-as-input/tests/test_plugin.py
"""Tests for vexy-mkdocs-output-as-input plugin."""

import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from mkdocs_output_as_input.plugin import OutputAsInputPlugin


class TestOutputAsInputPlugin:
    """Test cases for OutputAsInputPlugin."""

    @pytest.fixture
    def plugin(self):
        """Create a plugin instance."""
        plugin = OutputAsInputPlugin()
        # Initialize plugin configuration with defaults
        plugin.config = {
            "stage_dir": "stage",
            "html_element": "main",
            "target_tag": "article",
            "include_frontmatter": True,
            "preserve_links": False,
            "minify": False,
            "prettify": False,
            "verbose": False,
        }
        return plugin

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory."""
        with tempfile.TemporaryDirectory() as td:
            yield Path(td)

    @pytest.fixture
    def mkdocs_config(self, temp_dir):
        """Create a mock MkDocs config."""
        config = {
            "site_dir": str(temp_dir / "site"),
            "docs_dir": str(temp_dir / "docs"),
        }
        # Create directories
        Path(config["site_dir"]).mkdir(parents=True)
        Path(config["docs_dir"]).mkdir(parents=True)
        return config

    def test_default_config(self, plugin):
        """Test plugin with default configuration."""
        assert plugin.config["stage_dir"] == "stage"
        assert plugin.config["html_element"] == "main"
        assert plugin.config["target_tag"] == "article"
        assert plugin.config["include_frontmatter"] is True
        assert plugin.config["verbose"] is False

    def test_on_config_stores_paths(self, plugin, mkdocs_config):
        """Test that on_config stores site and docs directories."""
        plugin.on_config(mkdocs_config)

        assert plugin.site_dir == Path(mkdocs_config["site_dir"])
        assert plugin.docs_dir == Path(mkdocs_config["docs_dir"])

    def test_on_page_read_source_captures_content(self, plugin, mkdocs_config, temp_dir):  # noqa: ARG002
        """Test capturing source content and frontmatter."""
        # Create a source file
        docs_dir = Path(mkdocs_config["docs_dir"])
        src_file = docs_dir / "test.md"
        src_file.write_text("""---
title: Test Page
category: Testing
---

# Test Content

This is test content.
""")

        # Create mock page
        mock_file = Mock()
        mock_file.src_path = "test.md"
        mock_file.abs_src_path = str(src_file)

        page = Mock()
        page.file = mock_file

        # Process the page
        plugin.on_config(mkdocs_config)
        result = plugin.on_page_read_source(page, mkdocs_config)

        assert result is None  # Should return None to let MkDocs continue
        assert "test.md" in plugin.source_files
        assert plugin.source_files["test.md"]["frontmatter"]["title"] == "Test Page"
        assert plugin.source_files["test.md"]["frontmatter"]["category"] == "Testing"

    def test_on_page_read_source_no_frontmatter(self, plugin, mkdocs_config, temp_dir):  # noqa: ARG002
        """Test capturing content without frontmatter."""
        # Create a source file without frontmatter
        docs_dir = Path(mkdocs_config["docs_dir"])
        src_file = docs_dir / "no_fm.md"
        src_file.write_text("# No Frontmatter\n\nJust content.")

        # Create mock page
        mock_file = Mock()
        mock_file.src_path = "no_fm.md"
        mock_file.abs_src_path = str(src_file)

        page = Mock()
        page.file = mock_file

        # Process the page
        plugin.on_config(mkdocs_config)
        plugin.on_page_read_source(page, mkdocs_config)

        assert "no_fm.md" in plugin.source_files
        assert plugin.source_files["no_fm.md"]["frontmatter"] == {}

    def test_on_post_build_creates_cousin_files(self, plugin, mkdocs_config, temp_dir):  # noqa: ARG002
        """Test creating cousin files after build."""
        # Setup directories
        docs_dir = Path(mkdocs_config["docs_dir"])
        site_dir = Path(mkdocs_config["site_dir"])

        # Create source file
        src_file = docs_dir / "test.md"
        src_file.write_text("""---
title: Test Page
---

# Test Content
""")

        # Create corresponding HTML output
        html_dir = site_dir / "test"
        html_dir.mkdir(parents=True)
        html_file = html_dir / "index.html"
        html_file.write_text("""<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<main class="main-content">
<h1>Test Content</h1>
<p>This is the HTML output.</p>
</main>
</body>
</html>""")

        # Simulate page capture
        plugin.on_config(mkdocs_config)
        plugin.source_files["test.md"] = {
            "frontmatter": {"title": "Test Page"},
            "abs_src_path": str(src_file),
        }

        # Run post build
        plugin.on_post_build(mkdocs_config)

        # Check cousin file was created
        stage_dir = docs_dir.parent / "stage"
        cousin_file = stage_dir / "test.md"

        assert cousin_file.exists()
        content = cousin_file.read_text()

        # Check frontmatter
        assert "---" in content
        assert "title: Test Page" in content

        # Check HTML content was extracted and transformed
        assert '<article class="main-content">' in content
        assert "<h1>Test Content</h1>" in content
        assert "<p>This is the HTML output.</p>" in content

    def test_on_post_build_missing_html(self, plugin, mkdocs_config, temp_dir):
        """Test handling missing HTML output."""
        # Setup
        plugin.on_config(mkdocs_config)
        plugin.source_files["missing.md"] = {
            "frontmatter": {},
            "abs_src_path": str(temp_dir / "missing.md"),
        }

        # Should not raise exception
        plugin.on_post_build(mkdocs_config)

    def test_on_post_build_missing_element(self, plugin, mkdocs_config, temp_dir):
        """Test handling HTML without target element."""
        # Setup directories
        site_dir = Path(mkdocs_config["site_dir"])

        # Create HTML without main element
        html_dir = site_dir / "test"
        html_dir.mkdir(parents=True)
        html_file = html_dir / "index.html"
        html_file.write_text("""<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<div>No main element here</div>
</body>
</html>""")

        # Setup plugin
        plugin.on_config(mkdocs_config)
        plugin.source_files["test.md"] = {
            "frontmatter": {},
            "abs_src_path": str(temp_dir / "test.md"),
        }

        # Should handle gracefully
        plugin.on_post_build(mkdocs_config)

    def test_custom_config_options(self, plugin, mkdocs_config, temp_dir):
        """Test with custom configuration options."""
        # Set custom config
        plugin.config["stage_dir"] = "custom_stage"
        plugin.config["html_element"] = "div"
        plugin.config["target_tag"] = "section"
        plugin.config["verbose"] = True

        # Setup
        docs_dir = Path(mkdocs_config["docs_dir"])
        site_dir = Path(mkdocs_config["site_dir"])

        # Create HTML with div instead of main
        html_file = site_dir / "test.html"
        html_file.write_text("""<!DOCTYPE html>
<html>
<body>
<div class="content">
<h1>Test</h1>
</div>
</body>
</html>""")

        plugin.on_config(mkdocs_config)
        plugin.source_files["test.md"] = {
            "frontmatter": {},
            "abs_src_path": str(temp_dir / "test.md"),
        }

        plugin.on_post_build(mkdocs_config)

        # Check custom stage dir
        stage_dir = docs_dir.parent / "custom_stage"
        cousin_file = stage_dir / "test.md"

        assert cousin_file.exists()
        content = cousin_file.read_text()

        # Check that div was transformed to section
        assert '<section class="content">' in content
        assert "<h1>Test</h1>" in content

    def test_invalid_yaml_frontmatter(self, plugin, mkdocs_config, temp_dir):  # noqa: ARG002
        """Test handling invalid YAML frontmatter."""
        # Create source with invalid YAML
        docs_dir = Path(mkdocs_config["docs_dir"])
        src_file = docs_dir / "invalid.md"
        src_file.write_text("""---
title: Test
invalid: [unclosed
---

# Content
""")

        # Create mock page
        mock_file = Mock()
        mock_file.src_path = "invalid.md"
        mock_file.abs_src_path = str(src_file)

        page = Mock()
        page.file = mock_file

        # Should handle gracefully
        plugin.on_config(mkdocs_config)
        plugin.on_page_read_source(page, mkdocs_config)

        assert "invalid.md" in plugin.source_files
        assert plugin.source_files["invalid.md"]["frontmatter"] == {}

    def test_file_read_error(self, plugin, mkdocs_config):
        """Test handling file read errors."""
        # Create mock page with non-existent file
        mock_file = Mock()
        mock_file.src_path = "nonexistent.md"
        mock_file.abs_src_path = "/path/to/nonexistent.md"

        page = Mock()
        page.file = mock_file

        # Should return None and log error
        plugin.on_config(mkdocs_config)
        result = plugin.on_page_read_source(page, mkdocs_config)

        assert result is None
        assert "nonexistent.md" not in plugin.source_files

    def test_on_post_build_no_docs_dir(self, plugin):
        """Test handling when docs_dir is None."""
        plugin.docs_dir = None
        plugin.on_post_build({})
        # Should handle gracefully without error

    def test_process_file_no_site_dir(self, plugin, temp_dir):
        """Test handling when site_dir is None."""
        plugin.site_dir = None
        stage_dir = temp_dir / "stage"
        stage_dir.mkdir()
        
        file_info = {"frontmatter": {}, "abs_src_path": str(temp_dir / "test.md")}
        plugin._process_file("test.md", file_info, stage_dir)
        # Should handle gracefully without error

    def test_include_frontmatter_option(self, plugin, mkdocs_config, temp_dir):
        """Test include_frontmatter configuration option."""
        docs_dir = Path(mkdocs_config["docs_dir"])
        site_dir = Path(mkdocs_config["site_dir"])

        # Create HTML output
        html_file = site_dir / "test.html"
        html_file.write_text("""<!DOCTYPE html>
<html>
<body>
<main>
<h1>Test Page</h1>
</main>
</body>
</html>""")

        plugin.on_config(mkdocs_config)
        
        # Test with include_frontmatter=True (default)
        plugin.source_files["test.md"] = {
            "frontmatter": {"title": "Test Title", "author": "Test Author"},
            "abs_src_path": str(temp_dir / "test.md"),
        }
        plugin.on_post_build(mkdocs_config)
        
        stage_dir = docs_dir.parent / "stage"
        cousin_file = stage_dir / "test.md"
        content = cousin_file.read_text()
        
        # Should include frontmatter
        assert "---" in content
        assert "title: Test Title" in content
        assert "author: Test Author" in content
        
        # Test with include_frontmatter=False
        plugin.config["include_frontmatter"] = False
        plugin.on_post_build(mkdocs_config)
        
        content = cousin_file.read_text()
        
        # Should NOT include frontmatter
        assert not content.startswith("---")
        assert "title: Test Title" not in content
        assert "author: Test Author" not in content
        # But should still have HTML content
        assert "<article>" in content
        assert "<h1>Test Page</h1>" in content

    def test_preserve_links_option(self, plugin, mkdocs_config, temp_dir):
        """Test preserve_links configuration option."""
        docs_dir = Path(mkdocs_config["docs_dir"])
        site_dir = Path(mkdocs_config["site_dir"])

        # Create HTML output with absolute links
        html_file = site_dir / "test.html"
        html_file.write_text("""<!DOCTYPE html>
<html>
<body>
<main>
<h1>Test Page</h1>
<a href="/docs/page.html">Link</a>
<img src="/images/pic.png">
<a href="https://example.com">External</a>
</main>
</body>
</html>""")

        plugin.on_config(mkdocs_config)
        plugin.source_files["test.md"] = {
            "frontmatter": {},
            "abs_src_path": str(temp_dir / "test.md"),
        }
        
        # Test with preserve_links=True
        plugin.config["preserve_links"] = True
        plugin.on_post_build(mkdocs_config)
        
        stage_dir = docs_dir.parent / "stage"
        cousin_file = stage_dir / "test.md"
        content = cousin_file.read_text()
        
        # Should convert absolute links to relative
        assert 'href="./docs/page.html"' in content
        assert 'src="./images/pic.png"' in content
        # External links should remain unchanged
        assert 'href="https://example.com"' in content

    def test_multiple_selectors(self, plugin, mkdocs_config, temp_dir):
        """Test extraction of multiple selectors."""
        docs_dir = Path(mkdocs_config["docs_dir"])
        site_dir = Path(mkdocs_config["site_dir"])

        # Create HTML with multiple elements
        html_file = site_dir / "test.html"
        html_file.write_text("""<!DOCTYPE html>
<html>
<body>
<header><h1>Header Content</h1></header>
<main><p>Main Content</p></main>
<aside><p>Sidebar Content</p></aside>
<footer><p>Footer Content</p></footer>
</body>
</html>""")

        plugin.on_config(mkdocs_config)
        plugin.source_files["test.md"] = {
            "frontmatter": {},
            "abs_src_path": str(temp_dir / "test.md"),
        }
        
        # Test with multiple selectors
        plugin.config["html_element"] = ["main", "aside"]
        plugin.on_post_build(mkdocs_config)
        
        stage_dir = docs_dir.parent / "stage"
        cousin_file = stage_dir / "test.md"
        content = cousin_file.read_text()
        
        # Should include both main and aside content wrapped in article
        assert "<article>" in content
        assert "Main Content" in content
        assert "Sidebar Content" in content
        # Should NOT include header or footer
        assert "Header Content" not in content
        assert "Footer Content" not in content

    def test_css_selectors(self, plugin, mkdocs_config, temp_dir):
        """Test CSS selector support."""
        docs_dir = Path(mkdocs_config["docs_dir"])
        site_dir = Path(mkdocs_config["site_dir"])

        # Create HTML with CSS selectable elements
        html_file = site_dir / "test.html"
        html_file.write_text("""<!DOCTYPE html>
<html>
<body>
<div class="content">
<h1>Title</h1>
<p class="highlight">Important</p>
<p>Normal</p>
</div>
<div class="sidebar">Sidebar</div>
</body>
</html>""")

        plugin.on_config(mkdocs_config)
        plugin.source_files["test.md"] = {
            "frontmatter": {},
            "abs_src_path": str(temp_dir / "test.md"),
        }
        
        # Test with CSS selector
        plugin.config["html_element"] = ".content"
        plugin.on_post_build(mkdocs_config)
        
        stage_dir = docs_dir.parent / "stage"
        cousin_file = stage_dir / "test.md"
        content = cousin_file.read_text()
        
        # Should extract div with class="content"
        assert "<article" in content
        assert "Title" in content
        assert "Important" in content
        assert "Normal" in content
        # Should NOT include sidebar
        assert "Sidebar" not in content

    def test_minify_option(self, plugin, mkdocs_config, temp_dir):
        """Test minify option."""
        docs_dir = Path(mkdocs_config["docs_dir"])
        site_dir = Path(mkdocs_config["site_dir"])

        # Create HTML with whitespace
        html_file = site_dir / "test.html"
        html_file.write_text("""<!DOCTYPE html>
<html>
<body>
<main>
    <h1>Title</h1>
    <p>
        Content with
        lots of whitespace
    </p>
</main>
</body>
</html>""")

        plugin.on_config(mkdocs_config)
        plugin.source_files["test.md"] = {
            "frontmatter": {},
            "abs_src_path": str(temp_dir / "test.md"),
        }
        
        # Test with minify=True
        plugin.config["minify"] = True
        plugin.on_post_build(mkdocs_config)
        
        stage_dir = docs_dir.parent / "stage"
        cousin_file = stage_dir / "test.md"
        content = cousin_file.read_text()
        
        # Should have no newlines in HTML (except final newline)
        lines = content.strip().split('\n')
        assert len(lines) == 1  # Only one line of HTML
        # Check that spaces between tags are removed
        assert "><" in content
        # Check that content is minified but preserves single spaces in text
        assert "Content with lots of whitespace" in content

    def test_prettify_option(self, plugin, mkdocs_config, temp_dir):
        """Test prettify option."""
        docs_dir = Path(mkdocs_config["docs_dir"])
        site_dir = Path(mkdocs_config["site_dir"])

        # Create compact HTML
        html_file = site_dir / "test.html"
        html_file.write_text("""<html><body><main><h1>Title</h1><p>Content</p></main></body></html>""")

        plugin.on_config(mkdocs_config)
        plugin.source_files["test.md"] = {
            "frontmatter": {},
            "abs_src_path": str(temp_dir / "test.md"),
        }
        
        # Test with prettify=True
        plugin.config["prettify"] = True
        plugin.on_post_build(mkdocs_config)
        
        stage_dir = docs_dir.parent / "stage"
        cousin_file = stage_dir / "test.md"
        content = cousin_file.read_text()
        
        # Should have proper indentation
        lines = content.strip().split('\n')
        assert len(lines) > 1  # Multiple lines
        assert any(" <" in line for line in lines)  # Has indentation

    def test_mutually_exclusive_options(self, plugin, mkdocs_config):
        """Test that minify and prettify are mutually exclusive."""
        plugin.config["minify"] = True
        plugin.config["prettify"] = True
        
        with pytest.raises(ValueError, match="Cannot use both 'minify' and 'prettify'"):
            plugin.on_config(mkdocs_config)
