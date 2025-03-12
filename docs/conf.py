#!/usr/bin/env python3
# ╔═════════════════════════════════════════════════════╗
# ║  S P H I N X   C O N F I G  –  E I D O S I A N   M O D E  ║
# ╚═════════════════════════════════════════════════════╝
# Embracing minimalism, humor, depth, and flawless structure 🔄🎯

import os
import sys
import json
from datetime import datetime
from pathlib import Path
import logging
import importlib.util
from typing import Dict, List, Set, Tuple, Optional, Any, Union
import re
import shutil

# 🚀 Core Project Identity - Contextual Foundation
project = "Ollama Forge"
copyright = "2025, Lloyd Handyside"
author = "Lloyd Handyside"
version = "0.1.9"  # 🔢 Semantic versioning - precision matters
release = "0.1.9"  # 🎯 Release tracking - keep in sync for sanity

# 📊 Structured Logging - Self-Awareness Foundation
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
)
logger = logging.getLogger("eidosian_docs")  # 🧠 Centralized logger for all operations

# 🏛️ Repository Architecture - Structure as Control
REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"  # 📁 Documentation home
BUILD_DIR = DOCS_DIR / "_build"  # 🏗️ Where artifacts materialize
SOURCE_DIR = DOCS_DIR / "source"  # 📦 Source documentation
AUTO_DIR = DOCS_DIR / "auto"  # 🤖 Auto-generated documentation
sys.path.insert(0, os.path.abspath(str(REPO_ROOT)))  # 🔍 Make imports work flawlessly

# Create required directories if they don't exist
for directory in [
    DOCS_DIR / "_static",
    DOCS_DIR / "_templates", 
    AUTO_DIR / "api",
    AUTO_DIR / "extracted", 
    AUTO_DIR / "introspected"
]:
    directory.mkdir(parents=True, exist_ok=True)

# Create .gitkeep file for _static if it doesn't exist
gitkeep_file = DOCS_DIR / "_static" / ".gitkeep"
if not gitkeep_file.exists():
    with open(gitkeep_file, "w") as f:
        pass

# 🗺️ Documentation Cartography - The Map of Knowledge
DOCUMENTATION_CATEGORIES = {
    "getting_started": {
        "caption": "📚 Getting Started",
        "description": "Introduction and initial setup",
        "priority": 100,
        "path": SOURCE_DIR / "getting_started",
        "items": []
    },
    "concepts": {
        "caption": "🧩 Core Concepts",
        "description": "Fundamental concepts and principles",
        "priority": 90,
        "path": SOURCE_DIR / "concepts",
        "items": []
    },
    "examples": {
        "caption": "📋 Examples",
        "description": "Example code and usage patterns",
        "priority": 80,
        "path": SOURCE_DIR / "examples",
        "items": []
    },
    "guides": {
        "caption": "🧠 Guides & Tutorials",
        "description": "Guides, tutorials and how-tos",
        "priority": 70,
        "path": SOURCE_DIR / "guides",
        "items": []
    },
    "reference": {
        "caption": "🔍 API Reference",
        "description": "API documentation and references",
        "priority": 60,
        "path": SOURCE_DIR / "reference",
        "items": []
    },
}

# Function to convert RST to Markdown if needed
def convert_rst_to_md():
    """Convert any RST files to Markdown format for consistency."""
    import subprocess
    try:
        import pypandoc
        logger.info("🔄 Found pypandoc for RST to MD conversion")
        for rst_file in SOURCE_DIR.glob("**/*.rst"):
            md_file = rst_file.with_suffix(".md")
            try:
                pypandoc.convert_file(str(rst_file), "markdown", outputfile=str(md_file))
                logger.info(f"✅ Converted {rst_file.name} to Markdown")
                rst_file.unlink()  # Remove the original RST file
            except Exception as e:
                logger.warning(f"⚠️ Failed to convert {rst_file}: {e}")
    except ImportError:
        try:
            # Fallback to pandoc command line if available
            for rst_file in SOURCE_DIR.glob("**/*.rst"):
                md_file = rst_file.with_suffix(".md")
                subprocess.run(["pandoc", str(rst_file), "-o", str(md_file)])
                logger.info(f"✅ Converted {rst_file.name} to Markdown using pandoc")
                rst_file.unlink()  # Remove the original RST file
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("⚠️ Could not convert RST files. Install pypandoc or pandoc.")

# Call the conversion function
try:
    convert_rst_to_md()
except Exception as e:
    logger.warning(f"⚠️ RST conversion error: {e}")

# Generate navigation structure from the documentation directories
def generate_navigation_structure():
    """
    Generate a navigation structure for the sidebar based on the actual files
    in the documentation directories.
    """
    nav_structure = {}
    
    for category, config in DOCUMENTATION_CATEGORIES.items():
        path = config["path"]
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Created directory for {category}: {path}")
        
        items = []
        
        # Find all Markdown files in this category directory
        for md_file in sorted(path.glob("**/*.md")):
            # Extract title from the file
            title = md_file.stem.replace("_", " ").title()
            if md_file.name.lower() in ["readme.md", "index.md"]:
                title = config["caption"].replace("📚 ", "").replace("🧩 ", "").replace("📋 ", "").replace("🧠 ", "").replace("🔍 ", "")
                priority = 0  # Always put index/readme at the top
            else:
                priority = 10
            
            # Get the URL relative to the docs directory
            url = str(md_file.relative_to(DOCS_DIR)).replace("\\", "/")
            
            items.append({
                "title": title,
                "url": url,
                "priority": priority
            })
        
        # Sort items by priority
        items.sort(key=lambda x: x["priority"])
        
        nav_structure[category] = {
            "caption": config["caption"],
            "description": config.get("description", ""),
            "items": items
        }
    
    return nav_structure

# Sphinx Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode", 
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",  # For Markdown support
    "sphinx.ext.intersphinx",
]

# Try to import autoapi extension
try:
    import autoapi
    extensions.append("autoapi.extension")
    autoapi_type = "python"
    autoapi_dirs = [str(REPO_ROOT / "ollama_forge")]
    autoapi_output_dir = str(AUTO_DIR / "api")
    autoapi_template_dir = str(DOCS_DIR / "_templates" / "autoapi") if (DOCS_DIR / "_templates" / "autoapi").exists() else None
    autoapi_options = [
        'members',
        'undoc-members',
        'private-members',
        'show-inheritance',
        'show-module-summary',
        'special-members',
        'imported-members',
    ]
    autoapi_add_toctree_entry = True
    autoapi_keep_files = True
    autoapi_python_class_content = 'both'
    logger.info(f"🔄 Using autoapi version: {autoapi.__version__}")
except ImportError:
    logger.warning("⚠️ sphinx-autoapi not installed, API documentation will be limited")

# Process before we load the navigation to ensure all files are discovered
nav_structure = generate_navigation_structure()

# Intersphinx configuration for cross-references
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# Markdown configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 4

# HTML Theme Configuration
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["eidosian-enhancer.js"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
    ".txt": "markdown",
}

# Theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "light_css_variables": {
        "color-brand-primary": "#5D44F3",
        "color-brand-content": "#5D44F3",
    },
    "dark_css_variables": {
        "color-brand-primary": "#9285F7",
        "color-brand-content": "#9285F7",
    },
    "navigation_with_keys": True,
}

# Add navigation to context
html_context = {
    "theme_sidebars": nav_structure,
    "project_info": {
        "name": project,
        "version": version,
        "release": release,
    }
}

# Custom sidebar if available
if (DOCS_DIR / "_templates" / "custom_sidebar.html").exists():
    html_sidebars = {
        "**": ["custom_sidebar.html", "sidebar/search.html"]
    }

# Ensure custom CSS file exists
custom_css_path = DOCS_DIR / "_static" / "custom.css"
if not custom_css_path.exists():
    with open(custom_css_path, "w") as f:
        f.write("""/* Eidosian Custom Styles */
.eidosian-highlight {
    background-color: rgba(93, 68, 243, 0.1);
    border-left: 3px solid #5D44F3;
    padding: 0.5em 1em;
    margin: 1em 0;
}
div.highlight pre {
    border-radius: 0.3em;
    padding: 1em;
}
table.docutils {
    width: 100%;
    border-collapse: collapse;
}
table.docutils th, table.docutils td {
    padding: 0.5em;
    border: 1px solid #e1e4e5;
}
table.docutils th {
    background-color: #f3f4f7;
}
.principle {
    margin: 1.5em 0;
    padding: 1em;
    border-left: 3px solid #5D44F3;
    background-color: rgba(93, 68, 243, 0.05);
}
.principle-title {
    font-weight: bold;
    color: #5D44F3;
    margin-bottom: 0.5em;
}
""")
    logger.info("📝 Created custom CSS file")

# Ensure JS enhancer exists
js_enhancer_path = DOCS_DIR / "_static" / "eidosian-enhancer.js"
if not js_enhancer_path.exists():
    with open(js_enhancer_path, "w") as f:
        f.write("""/* Eidosian JavaScript Enhancer */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌀 Eidosian enhancer activated');
    
    // Add class to code blocks for styling
    document.querySelectorAll('div.highlight').forEach(function(element) {
        element.classList.add('eidosian-code');
    });
    
    // Create principle blocks
    document.querySelectorAll('h3').forEach(function(heading) {
        const text = heading.textContent.trim();
        if (text.includes(':')) {
            const [principle, description] = text.split(':');
            if (principle && description) {
                const wrapper = document.createElement('div');
                wrapper.className = 'principle';
                
                const title = document.createElement('div');
                title.className = 'principle-title';
                title.textContent = principle.trim();
                
                const content = document.createElement('div');
                content.textContent = description.trim();
                
                wrapper.appendChild(title);
                wrapper.appendChild(content);
                
                heading.parentNode.replaceChild(wrapper, heading);
            }
        }
    });
});
""")
    logger.info("📝 Created JavaScript enhancer")

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
}

# Configuration to avoid warning spam
nitpicky = True
nitpick_ignore = [
    ("py:class", "ConnectionError"),
    ("py:class", "ModelNotFoundError"),
    ("py:class", "InvalidRequestError"),
    ("py:class", "OllamaAPIError"),
    ("py:class", "argparse.ArgumentParser"),
    ("py:class", "argparse.Namespace"),
    ("py:class", "requests.Session"),
    ("py:class", "requests.Response"),
    ("py:class", "httpx.Response"),
    ("py:data", "typing.Any"),
    ("py:data", "typing.Optional"),
    ("py:data", "typing.Union"),
    ("py:data", "typing.Callable"),
    ("py:data", "typing.Tuple"),
    ("py:data", "Ellipsis"),
    ("py:data", "F"),
    ("py:class", "ollama_forge.exceptions.ConnectionError"),
    ("py:class", "ollama_forge.exceptions.ModelNotFoundError"),
    ("py:class", "ollama_forge.exceptions.InvalidRequestError"),
    ("py:class", "ollama_forge.exceptions.OllamaAPIError"),
    ('py:class', 'ollama_forge.exceptions.TimeoutError'),
]

suppress_warnings = [
    "toc.not_included",
    "autosectionlabel.*",
    "duplicate.label",
    "myst.header",
    "ref.python",
    "autoapi",
    "ref.class",
]

# Exclude patterns for docs processing
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/__pycache__/**"]
templates_path = ["_templates"]
todo_include_todos = True
copybutton_prompt_text = ">>> "

# Document processing functions
def process_rst_to_md(app, docname, source):
    """Convert RST syntax to Markdown in source."""
    if docname.endswith(".rst"):
        source[0] = convert_rst_content_to_md(source[0])

def convert_rst_content_to_md(content):
    """Simple RST to MD conversion for common patterns."""
    # Convert RST directives to Markdown equivalents
    patterns = [
        (r"\.\. code-block:: (\w+)\n\n([\s\S]+?)(?=\n\n|\Z)", r"```\1\n\2\n```"),
        (r"\.\. note::\n\n([\s\S]+?)(?=\n\n|\Z)", r"> **Note**\n> \1"),
        (r"\.\. warning::\n\n([\s\S]+?)(?=\n\n|\Z)", r"> **Warning**\n> \1"),
        (r"\.\. toctree::\n\n([\s\S]+?)(?=\n\n|\Z)", r"<!-- toctree -->\n\1"),
        (r":ref:`([^<`]+)\s+<([^>]+)>`", r"[\1](#\2)"),
                "items": items
            }

html_theme_options = {
    "sidebar_hide_name": False,
    "light_css_variables": {
        "color-brand-primary": "#5D44F3",
        "color-brand-content": "#5D44F3",
    },
    "dark_css_variables": {
        "color-brand-primary": "#9285F7",
        "color-brand-content": "#9285F7",
    },
    "navigation_with_keys": True,
}

html_context = {
    "theme_sidebars": nav_structure,
    "project_info": {
        "name": project,
        "version": version,
        "release": release,
    }
}

if (DOCS_DIR / "_templates" / "custom_sidebar.html").exists():
    html_sidebars = {
        "**": ["custom_sidebar.html", "sidebar/search.html"]
    }

# Add this near the end of the file, before the setup function

# Prevent duplicate object warnings by using autodoc_default_options
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'inherited-members': False,
    # Add :noindex: to prevent duplicate object warnings
    'noindex': False
}

# Control how autoapi handles duplicates
autoapi_options = [
    'members',
    'undoc-members',
    'private-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
    'imported-members',
]

# Function to add :noindex: directives to all RST files
def setup(app):
    global eidosian_doc_manager
    eidosian_doc_manager = EidosianDocManager(app, REPO_ROOT, DOCS_DIR)
    app.connect("builder-inited", on_builder_init)
    app.connect("doctree-read", on_doctree_read)
    app.connect("build-finished", on_build_finished)
    app.connect("autodoc-process-docstring", track_api_object)
    app.add_css_file("custom.css")
    
    from sphinx.util import logging
    logger = logging.getLogger(__name__)
    
    # Track seen objects to detect duplicates
    seen_objects = {}
    
    def process_signature(app, objtype, fullname, obj, options, args, retann):
        # Add :noindex: option for duplicate objects
        if fullname in seen_objects:
            logger.debug(f"Adding :noindex: to duplicate object: {fullname}")
            options['noindex'] = True
        else:
            seen_objects[fullname] = True
        return None  # Let regular signature processing continue
    
    app.connect('autodoc-process-signature', process_signature)
    
    # Register our custom post-build function to add :noindex: directives
    app.connect('build-finished', add_noindex_to_duplicates_post_build)
    
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

def on_builder_init(app):
    logger.info("🚀 Eidosian documentation build initializing")
    fix_api_documentation_duplication(app)
    if eidosian_doc_manager:
        eidosian_doc_manager.on_builder_init()

def on_doctree_read(app, doctree):
    if eidosian_doc_manager:
        eidosian_doc_manager.on_doctree_read(doctree)

def fix_api_documentation_duplication(app):
    manual_api_dir = DOCS_DIR / "api"
    autoapi_dir = DOCS_DIR / "autoapi"
    docs_dirs_to_process = [manual_api_dir, autoapi_dir]
    for doc_dir in docs_dirs_to_process:
        if not doc_dir.exists():
            continue
        logger.info(f"🔍 Processing documentation in {doc_dir}")
        for rst_file in doc_dir.glob("**/*.rst"):
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()
                if doc_dir == manual_api_dir:
                    directives = [
                        "automodule",
                        "autoclass",
                        "autofunction",
                        "automethod",
                        "autoattribute"
                    ]
                    updated_content = content
                    for directive in directives:
                        pattern = rf"(^\.\.\s+{directive}::.*?)(?!\s+:noindex:)(\s*$)"
                        updated_content = re.sub(
                            pattern,
                            r"\1\n   :noindex:\2",
                            updated_content,
                            flags=re.MULTILINE
                        )
                    if updated_content != content:
                        with open(rst_file, "w", encoding="utf-8") as f:
                            f.write(updated_content)
                        logger.info(f"✓ Added :noindex: to manual API documentation in {rst_file.name}")
                if doc_dir == autoapi_dir:
                    updated_content = fix_docstring_formatting(content)
                    if updated_content != content:
                        with open(rst_file, "w", encoding="utf-8") as f:
                            f.write(updated_content)
                        logger.info(f"✓ Fixed formatting in {rst_file.name}")
            except Exception as e:
                logger.warning(f"⚠️ Could not process API file {rst_file}: {e}")

def fix_docstring_formatting(content: str) -> str:
    pattern_indentation = r"(```python.*?\n.*?)(\n\s+)(.*?)```"
    content = re.sub(pattern_indentation, r"\1\3", content, flags=re.DOTALL)
    content = re.sub(r"(`+)([^`]+)$", r"\1\2\1", content, flags=re.MULTILINE)
    return content

def on_build_finished(app, exception):
    if exception is None:
        logger.info("✅ Eidosian documentation build completed successfully")
        if eidosian_doc_manager:
            eidosian_doc_manager.on_build_finished()
        build_dir = app.outdir
        try:
            generate_docs_registry(Path(build_dir))
        except Exception as e:
            logger.error(f"❌ Error generating documentation registry: {e}")
    else:
        logger.error(f"❌ Eidosian documentation build failed: {exception}")

def generate_docs_registry(build_dir):
    registry = []
    html_files = list(build_dir.glob("**/*.html"))
    for html_file in html_files:
        rel_path = html_file.relative_to(build_dir)
        try:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
            title_match = re.search(r"<title>(.*?)</title>", content)
            title = title_match.group(1) if title_match else str(rel_path)
            registry.append({
                "path": str(rel_path),
                "title": title,
                "size": html_file.stat().st_size,
                "last_modified": html_file.stat().st_mtime
            })
        except Exception as e:
            logger.warning(f"⚠️ Error processing {html_file}: {e}")
    import json
    registry_path = build_dir / "docs_registry.json"
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": import_time(),
            "doc_count": len(registry),
            "items": registry
        }, f, indent=2)
    logger.info(f"📋 Generated documentation registry with {len(registry)} entries")

def import_time():
    from datetime import datetime
    return datetime.now().isoformat()

class EidosianDocManager:
    """
    Central coordinator for all documentation processing tasks.
    Follows Eidosian principles with universal synergy.
    """
    def __init__(self, app, repo_root, docs_dir):
        self.app = app
        self.repo_root = repo_root
        self.docs_dir = docs_dir
        self.modules = {}
        self.load_modules()

    def load_modules(self):
        module_files = {
            "source_discovery": self.docs_dir / "source_discovery.py",
            "fix_cross_refs": self.docs_dir / "fix_cross_refs.py",
            "autoapi_fixer": self.docs_dir / "autoapi_fixer.py",
            "update_toctrees": self.docs_dir / "update_toctrees.py",
            "docstring_fixer": self.docs_dir / "docstring_fixer.py",
            "fix_docs": self.docs_dir / "fix_docs.py"
        }
        for name, path in module_files.items():
            if path.exists():
                try:
                    spec = importlib.util.spec_from_file_location(name, path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        self.modules[name] = module
                        logger.info(f"✅ Loaded module: {name}")
                    else:
                        logger.warning(f"⚠️ Could not load spec for module: {name}")
                except Exception as e:
                    logger.warning(f"⚠️ Error loading module {name}: {e}")
            else:
                logger.debug(f"Module not available: {name}")

    def on_builder_init(self):
        if "fix_cross_refs" in self.modules:
            try:
                self.modules["fix_cross_refs"].fix_ambiguous_references(self.repo_root)
                self.modules["fix_cross_refs"].fix_python_imports(self.repo_root)
                if hasattr(self.modules["fix_cross_refs"], "create_intersphinx_mapping"):
                    self.modules["fix_cross_refs"].create_intersphinx_mapping(self.repo_root)
                logger.info("🔍 Fixed cross-references")
            except Exception as e:
                logger.error(f"❌ Error fixing cross references: {e}")
        if "docstring_fixer" in self.modules:
            try:
                fixer = self.modules["docstring_fixer"].DocstringFixer(self.docs_dir)
                fixed = fixer.fix_all_files()
                logger.info(f"📝 Fixed docstrings in {fixed} files")
            except Exception as e:
                logger.error(f"❌ Error fixing docstrings: {e}")
        self._ensure_required_files()

    def on_doctree_read(self, doctree):
        if ("update_toctrees" in self.modules
            and hasattr(self.modules["update_toctrees"], "process_doctree")):
            try:
                self.modules["update_toctrees"].process_doctree(doctree)
            except Exception as e:
                logger.warning(f"⚠️ Error processing doctree: {e}")

    def on_build_finished(self):
        if "autoapi_fixer" in self.modules:
            try:
                fixer = self.modules["autoapi_fixer"].AutoAPIFixer(self.docs_dir)
                fixed = fixer.fix_all_files()
                logger.info(f"🔧 Fixed AutoAPI documentation in {fixed} files")
            except Exception as e:
                logger.error(f"❌ Error fixing AutoAPI documentation: {e}")
        if "source_discovery" in self.modules:
            try:
                discovery = self.modules["source_discovery"].DocumentationDiscovery(self.repo_root)
                documents = discovery.discover_all_documents()
                toc = discovery.generate_toc_structure(documents)
                toctrees = discovery.generate_sphinx_toctree(toc)
                discovery.mark_orphaned_documents()
                logger.info(f"📌 Processed documentation structure")
            except Exception as e:
                logger.error(f"❌ Error in document discovery: {e}")

    def _ensure_required_files(self):
        static_dir = self.docs_dir / "_static"
        if not static_dir.exists():
            static_dir.mkdir(exist_ok=True)
        custom_css = static_dir / "custom.css"
        if not custom_css.exists():
            with open(custom_css, "w") as f:
                f.write("""/* Eidosian Custom Styles */
.eidosian-highlight {
    background-color: rgba(93, 68, 243, 0.1);
    border-left: 3px solid #5D44F3;
    padding: 0.5em 1em;
    margin: 1em 0;
}
div.highlight pre {
    border-radius: 0.3em;
    padding: 1em;
}
table.docutils {
    width: 100%;
    border-collapse: collapse;
}
table.docutils th, table.docutils td {
    padding: 0.5em;
    border: 1px solid #e1e4e5;
}
table.docutils th {
    background-color: #f3f4f7;
}
.principle {
    margin: 1.5em 0;
    padding: 1em;
    border-left: 3px solid #5D44F3;
    background-color: rgba(93, 68, 243, 0.05);
}
.principle-title {
    font-weight: bold;
    color: #5D44F3;
    margin-bottom: 0.5em;
}
""")
            logger.info("📝 Created custom CSS file")

def add_noindex_to_duplicates_post_build(app, exception):
    """Add :noindex: directives to prevent duplicate object warnings."""
    if exception:
        return
        
    try:
        from pathlib import Path
        import re
        import logging
        logger = logging.getLogger('sphinx.autoapi')
        
        # Process all autoapi RST files
        autoapi_dir = Path(app.outdir) / '_build/autoapi'
        if not autoapi_dir.exists():
            autoapi_dir = Path(app.outdir).parent / 'autoapi'
            
        if not autoapi_dir.exists():
            return
            
        file_count = 0
        for rst_file in autoapi_dir.glob('**/*.rst'):
            with open(rst_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Add :noindex: to all object descriptions if not already present
            modified = False
            for obj_type in ['class', 'method', 'function', 'attribute', 'data']:
                pattern = fr'(\.\. py:{obj_type}:: [^\n]+\n)(?!   :noindex:)'
                matches = list(re.finditer(pattern, content))
                
                if matches:
                    pos_offset = 0
                    for match in matches:
                        directive = match.group(1)
                        pos = match.start() + pos_offset
                        new_content = directive + "   :noindex:\n"
                        content = content[:pos] + new_content + content[pos + len(directive):]
                        pos_offset += len("   :noindex:\n")
                        modified = True
                
            if modified:
                with open(rst_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                file_count += 1
                    
        if file_count > 0:
            logger.info(f"Added :noindex: directives to {file_count} files")
    except Exception as e:
        logger.warning(f"Error adding :noindex: directives: {e}")
