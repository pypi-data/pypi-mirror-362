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
