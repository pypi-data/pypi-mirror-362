import os
import sys

sys.path.insert(0, os.path.abspath("../src"))
project = "tex2image"
copyright = "2025, Olympiad Bot"
author = "Olympiad Bot"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx_autodoc_typehints",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx_mdinclude",
]

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
}
autodoc_preserve_defaults = True
always_document_param_types = True

html_theme = "sphinx_rtd_theme"
