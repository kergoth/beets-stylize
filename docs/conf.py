"""Sphinx configuration."""

project = "Stylize Plugin for Beets"
author = "Christopher Larson"
copyright = "2024, Christopher Larson"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
