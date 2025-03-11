# ╔═════════════════════════════════════════════════════╗
# ║  S P H I N X   C O N F I G  –  E I D O S I A N   M O D E  ║
# ╚═════════════════════════════════════════════════════╝
# Embracing minimalism, humor, depth, and flawless structure 🔄🎯

import os
import sys
import subprocess

# Project metadata (Precision, no fluff)
project = "Ollama Forge"
copyright = "2025, Lloyd Handyside"
author = "Lloyd Handyside"
version = "0.1.9"  # Updated to match pyproject.toml
release = "0.1.9"  # Updated to match pyproject.toml

# Ensure project root is on sys.path for synergy 🚀
sys.path.insert(0, os.path.abspath(".."))

def run_autoapi():
    """
    🔬 EIDOSIAN Routine: Auto-generate API docs, removing redundancy,
    maximizing clarity with ephemeral elegance 🌀.
    """
    subprocess.run(["sphinx-apidoc", "-o", "docs/api", "../ollama_forge"], check=True)

# Trigger autoapi for fluid integration
run_autoapi()

# Extensions reflecting universal adaptability 🌐
extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",
]

# Eidosian disambiguation of duplicate labels with fractal awareness 🔍
autosectionlabel_prefix_document = True

# Concise yet thorough autoapi configuration 🎯
autoapi_type = "python"
autoapi_dirs = ["../ollama_forge"]
autoapi_ignore = ["__init__.py"]
autoapi_add_toctree_entry = True
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

# Napoleon settings for expanded doc charm 🌟
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_rtype = False
napoleon_type_aliases = {}

# Templates and exclusions, streamlined for clarity ⛑️
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Furo theme for modern aesthetics 🎨
html_theme = "furo"
html_static_path = ["_static"]

# Source suffixes with universal coverage 🌍
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# TODO and copybutton for user-friendly synergy ✔️
todo_include_todos = True
copybutton_prompt_text = ">>> "
