# this_file: more/mkdocs-plugins/vexy-mkdocs-output-as-input/src/mkdocs_output_as_input/plugin.py
"""MkDocs plugin that captures HTML output and creates cousin Markdown files."""

import logging
from pathlib import Path
from typing import Any, Optional

import yaml
from bs4 import BeautifulSoup
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

logger = logging.getLogger(__name__)


class OutputAsInputPlugin(BasePlugin):
    """MkDocs plugin that captures HTML output and creates cousin Markdown files.

    This plugin:
    1. Lets the entire MkDocs build process run normally
    2. Tracks all source Markdown files and their YAML frontmatter
    3. After the build, creates a "stage" directory that replicates the source structure
    4. For each source Markdown file, creates a cousin file with original frontmatter 
       and extracted HTML
    """

    config_scheme = (
        ("stage_dir", config_options.Type(str, default="stage")),
        ("html_element", config_options.Type(str, default="main")),
        ("target_tag", config_options.Type(str, default="article")),
        ("verbose", config_options.Type(bool, default=False)),
    )

    def __init__(self):
        """Initialize the plugin."""
        super().__init__()
        self.source_files = {}
        self.site_dir = None
        self.docs_dir = None

    def on_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Store site and docs directories."""
        self.site_dir = Path(config["site_dir"])
        self.docs_dir = Path(config["docs_dir"])

        if self.config["verbose"]:
            logger.info(f"OutputAsInput: site_dir={self.site_dir}, docs_dir={self.docs_dir}")

        return config

    def on_page_read_source(self, page: Page, config: dict[str, Any]) -> Optional[str]:  # noqa: ARG002
        """Capture source Markdown content and frontmatter."""
        src_path = page.file.src_path

        # Read the full source content
        try:
            with open(page.file.abs_src_path, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.error(f"OutputAsInput: Failed to read {src_path}: {e}")
            return None

        # Extract frontmatter if present
        frontmatter = {}
        if content.startswith("---\n"):
            try:
                end_idx = content.find("\n---\n", 4)
                if end_idx > 0:
                    fm_text = content[4:end_idx]
                    frontmatter = yaml.safe_load(fm_text) or {}
            except yaml.YAMLError as e:
                logger.warning(f"OutputAsInput: Failed to parse frontmatter in {src_path}: {e}")

        self.source_files[src_path] = {
            "frontmatter": frontmatter,
            "abs_src_path": page.file.abs_src_path,
        }

        if self.config["verbose"]:
            logger.info(f"OutputAsInput: Captured source {src_path}")

        return None  # Let MkDocs continue with original content

    def on_post_build(self, config: dict[str, Any]) -> None:  # noqa: ARG002
        """After build, process all HTML files and create cousin Markdowns."""
        stage_dir = self.docs_dir.parent / self.config["stage_dir"]

        # Create stage directory
        stage_dir.mkdir(exist_ok=True)
        logger.info(f"OutputAsInput: Creating stage directory at {stage_dir}")

        # Process each tracked source file
        processed = 0
        for src_path, file_info in self.source_files.items():
            try:
                self._process_file(src_path, file_info, stage_dir)
                processed += 1
            except Exception as e:
                logger.error(f"OutputAsInput: Failed to process {src_path}: {e}")

        logger.info(f"OutputAsInput: Processed {processed}/{len(self.source_files)} files")

    def _process_file(self, src_path: str, file_info: dict[str, Any], stage_dir: Path) -> None:
        """Process a single file: extract HTML and create cousin Markdown."""
        # Determine HTML output path
        html_path = src_path.replace(".md", "/index.html")
        full_html_path = self.site_dir / html_path

        if not full_html_path.exists():
            # Try without the index.html suffix
            html_path = src_path.replace(".md", ".html")
            full_html_path = self.site_dir / html_path

        if not full_html_path.exists():
            logger.warning(f"OutputAsInput: No HTML output found for {src_path}")
            return

        # Read and parse HTML
        try:
            with open(full_html_path, encoding="utf-8") as f:
                html_content = f.read()
        except Exception as e:
            logger.error(f"OutputAsInput: Failed to read HTML {full_html_path}: {e}")
            return

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract target element
        target_element = soup.find(self.config["html_element"])
        if not target_element:
            logger.warning(
                f"OutputAsInput: No <{self.config['html_element']}> found in {full_html_path}"
            )
            return

        # Transform to target tag if different
        if self.config["target_tag"] != self.config["html_element"]:
            target_element.name = self.config["target_tag"]

        # Create cousin file path
        cousin_path = stage_dir / src_path
        cousin_path.parent.mkdir(parents=True, exist_ok=True)

        # Write cousin file
        try:
            with open(cousin_path, "w", encoding="utf-8") as f:
                # Write frontmatter if present
                if file_info["frontmatter"]:
                    f.write("---\n")
                    f.write(yaml.safe_dump(file_info["frontmatter"], default_flow_style=False))
                    f.write("---\n\n")

                # Write extracted HTML
                f.write(str(target_element))
                f.write("\n")

            if self.config["verbose"]:
                logger.info(f"OutputAsInput: Created cousin file {cousin_path}")

        except Exception as e:
            logger.error(f"OutputAsInput: Failed to write cousin file {cousin_path}: {e}")
