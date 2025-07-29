# this_file: more/mkdocs-plugins/vexy-mkdocs-output-as-input/src/mkdocs_output_as_input/__init__.py
"""MkDocs Output as Input Plugin."""

from mkdocs_output_as_input.plugin import OutputAsInputPlugin

try:
    from mkdocs_output_as_input._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

__all__ = ["OutputAsInputPlugin"]
