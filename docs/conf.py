# filepath: /home/lloyd/Development/eidos/ollama_forge_repo/docs/conf.py
# ╔═════════════════════════════════════════════════════╗
# ║  S P H I N X   C O N F I G  –  E I D O S I A N   M O D E  ║
# ╚═════════════════════════════════════════════════════╝
# Embracing minimalism, humor, depth, and flawless structure 🔄🎯

import os
import sys
import subprocess
from pathlib import Path
import logging
import importlib.util
from typing import Dict, List, Set, Tuple, Optional, Any, Union
import re

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
try:
    REPO_ROOT = Path(__file__).resolve().parent.parent
    logger.info(f"🏛️ Repository root detected at: {REPO_ROOT}")
except Exception as e:
    logger.warning(f"⚠️ Could not detect repository root: {e}")
    REPO_ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent

DOCS_DIR = REPO_ROOT / "docs"  # 📁 Documentation home
BUILD_DIR = DOCS_DIR / "_build"  # 🏗️ Where artifacts materialize
sys.path.insert(0, os.path.abspath(str(REPO_ROOT)))  # 🔍 Make imports work flawlessly

# 🗺️ Documentation Cartography - The Map of Knowledge
DOC_MAPPING = {
    "ollama_forge": {
        "path": REPO_ROOT / "ollama_forge",
        "patterns": ["*.py"],
        "priority": 100,  # Highest priority - core API always comes first
        "section": "api_docs",
        "title": "API Reference",
        "description": "Auto-generated API documentation from source code"
    },
    "examples": {
        "path": REPO_ROOT / "examples",
        "patterns": ["*.py"],
        "priority": 90,
        "section": "examples",
        "title": "Examples",
        "description": "Example code showing usage patterns"
    },
    "helpers": {
        "path": REPO_ROOT / "helpers",
        "patterns": ["*.py"],
        "priority": 85,
        "section": "features",
        "title": "Helper Utilities",
        "description": "Support utilities and helper functions"
    },
    "tests": {
        "path": REPO_ROOT / "tests",
        "patterns": ["*.py"],
        "include_dir": False,
        "priority": 80,
        "section": "guides",
        "title": "Testing Guide",
        "description": "Test suite and quality assurance"
    },
    "docs_md": {
        "path": DOCS_DIR,
        "patterns": ["*.md"],
        "exclude_patterns": ["README.md", "_templates/**", "_build/**", "_static/**"],
        "priority": 70,
        "section": "core_docs",
        "title": "Core Documentation",
        "description": "Core narrative documentation"
    },
    "docs_rst": {
        "path": DOCS_DIR,
        "patterns": ["*.rst"],
        "exclude_patterns": ["_templates/**", "_build/**", "_static/**"],
        "priority": 65,
        "section": "core_docs",
        "title": "Core Documentation",
        "description": "Core narrative documentation (RST)"
    },
    "user_content": {
        "path": DOCS_DIR / "user_content",
        "patterns": ["*.md", "*.rst"],
        "priority": 60,
        "section": "user_docs",
        "title": "Community Contributions",
        "description": "User-generated content and contributions",
        "optional": True
    }
}

DOCUMENTATION_CATEGORIES = {
    "getting_started": {
        "caption": "📚 Getting Started",
        "description": "Introduction and initial setup",
        "priority": 100,
        "items": []
    },
    "core_docs": {
        "caption": "🛠️ Core Documentation",
        "description": "Main documentation and reference",
        "priority": 90,
        "items": []
    },
    "features": {
        "caption": "🔄 Features & Capabilities",
        "description": "Feature-specific documentation",
        "priority": 80,
        "items": []
    },
    "guides": {
        "caption": "🧠 Guides & References",
        "description": "Guides, tutorials and references",
        "priority": 70,
        "items": []
    },
    "api_docs": {
        "caption": "🧩 API Endpoints",
        "description": "API documentation and endpoints",
        "priority": 60,
        "items": []
    },
    "examples": {
        "caption": "📋 Examples",
        "description": "Example code and usage patterns",
        "priority": 50,
        "items": []
    },
    "user_docs": {
        "caption": "👥 Community Contributions",
        "description": "User-contributed documentation",
        "priority": 40,
        "items": []
    }
}

def discover_repository_documentation():
    known_paths = {str(config["path"]) for config in DOC_MAPPING.values()}
    for potential_docs_dir in REPO_ROOT.glob("**/docs"):
        if (str(potential_docs_dir) in known_paths or
            "_build" in str(potential_docs_dir) or
            ".git" in str(potential_docs_dir)):
            continue
        has_docs = False
        for ext in [".md", ".rst", ".txt"]:
            if list(potential_docs_dir.glob(f"*{ext}")):
                has_docs = True
                break
        if has_docs:
            key = f"auto_{potential_docs_dir.relative_to(REPO_ROOT).as_posix().replace('/', '_')}"
            parent = potential_docs_dir.parent.name
            title = f"{parent.replace('_', ' ').title()} Documentation"
            logger.info(f"🔍 Discovered documentation directory: {potential_docs_dir}")
            DOC_MAPPING[key] = {
                "path": potential_docs_dir,
                "patterns": ["*.md", "*.rst", "*.txt"],
                "priority": 50,
                "section": "guides",
                "title": title,
                "description": f"Auto-discovered documentation from {parent}",
                "optional": True
            }

try:
    discover_repository_documentation()
except Exception as e:
    logger.warning(f"⚠️ Repository-wide documentation discovery failed: {e}")

def generate_navigation_structure():
    navigation = {}
    index_patterns = ["index.md", "index.rst", "README.md", "readme.md"]
    for source_key, source_config in DOC_MAPPING.items():
        path = source_config["path"]
        section = source_config["section"]
        if not path.exists() and source_config.get("optional", False):
            continue
        if not path.exists():
            logger.warning(f"⚠️ Documentation path doesn't exist: {path}")
            continue
        index_file = None
        for pattern in index_patterns:
            potential_index = path / pattern
            if potential_index.exists():
                index_file = potential_index
                break
        if index_file:
            title = source_config["title"]
            url = str(index_file.relative_to(DOCS_DIR)).replace(".md", ".html").replace(".rst", ".html")
            if section not in navigation:
                navigation[section] = []
            navigation[section].append({
                "title": title,
                "url": url,
                "priority": source_config.get("priority", 50)
            })
    for section in navigation:
        navigation[section] = sorted(navigation[section], key=lambda x: x.get("priority", 50))
    nav_structure = {}
    for category, config in DOCUMENTATION_CATEGORIES.items():
        if category in navigation:
            nav_structure[category] = {
                "caption": config["caption"],
                "description": config.get("description", ""),
                "items": navigation.get(category, [])
            }
    return nav_structure

try:
    spec = importlib.util.spec_from_file_location(
        "source_discovery", os.path.join(os.path.dirname(__file__), "source_discovery.py")
    )
    source_discovery = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source_discovery)
    discovery = source_discovery.DocumentationDiscovery(REPO_ROOT)
    logger.info("📚 Advanced document discovery engine loaded")
    try:
        documents = discovery.discover_all_documents()
        toc = discovery.generate_toc_structure(documents)
        toc_trees = discovery.generate_sphinx_toctree(toc)
        index_path = DOCS_DIR / "index.md"
        if "--update-index" in sys.argv and index_path.exists():
            logger.info("🔄 Updating index.md with generated TOC trees")
            discovery.write_index_with_toctrees(toc_trees)
    except Exception as e:
        logger.warning(f"⚠️ Error during document discovery: {e}")
except ImportError:
    logger.warning("⚠️ source_discovery.py not found, advanced features disabled")
    discovery = None

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",
    "sphinx.ext.intersphinx",
    "autoapi.extension",
]

# AutoAPI configuration - this helps prevent duplicate entries
autoapi_type = 'python'
autoapi_dirs = ['../ollama_forge']
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'imported-members',
]
autoapi_add_toctree_entry = True
autoapi_keep_files = True
autoapi_template_dir = '_templates/autoapi'
autoapi_python_class_content = 'both'

try:
    import autoapi
    logger.info(f"🔄 Using autoapi version: {autoapi.__version__}")
    autoapi_type = "python"
    autoapi_dirs = [str(DOC_MAPPING["ollama_forge"]["path"])]
    autoapi_ignore = ["__init__.py", "**/__pycache__/**"]
    autoapi_add_toctree_entry = False
    autoapi_options = [
        "members",
        "undoc-members",
        "private-members",
        "show-inheritance",
        "show-module-summary",
        "special-members",
        "imported-members",
        "noindex",
    ]
    _api_objects = set()

    def track_api_object(app, objtype, name, obj, options, lines):
        if hasattr(app.env, "_api_objects"):
            app.env._api_objects.add(name)
        else:
            app.env._api_objects = {name}
except ImportError:
    logger.warning("⚠️ sphinx-autoapi not installed, API documentation may be limited")

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'noindex': True,  # Add this to prevent duplicating objects
}

autosectionlabel_prefix_document = True
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_rtype = False
napoleon_type_aliases = {}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/__pycache__/**"]

html_theme = "furo"
html_static_path = ["_static"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
    ".txt": "markdown",
}
todo_include_todos = True
copybutton_prompt_text = ">>> "

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

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

nav_structure = generate_navigation_structure()

default_navigation = {
    "getting_started": [
        {"title": "Installation", "url": "installation.html", "priority": 10},
        {"title": "Quickstart", "url": "quickstart.html", "priority": 20},
        {"title": "Introduction", "url": "index.html", "priority": 5},
    ],
    "core_docs": [
        {"title": "API Reference", "url": "api_reference.html", "priority": 10},
        {"title": "Examples", "url": "examples.html", "priority": 20},
        {"title": "Advanced Usage", "url": "advanced_usage.html", "priority": 30},
    ],
    "features": [
        {"title": "Chat Completion", "url": "chat.html", "priority": 10},
        {"title": "Text Generation", "url": "generate.html", "priority": 20},
        {"title": "Embeddings", "url": "embed.html", "priority": 30},
        {"title": "Model Management", "url": "model_management.html", "priority": 40},
        {"title": "Error Handling", "url": "error_handling.html", "priority": 50},
    ],
    "guides": [
        {"title": "Conventions", "url": "conventions.html", "priority": 10},
        {"title": "Troubleshooting", "url": "troubleshooting.html", "priority": 20},
        {"title": "Eidosian Integration", "url": "eidosian_integration.html", "priority": 30},
        {"title": "Contributing", "url": "contributing.html", "priority": 40},
        {"title": "Changelog", "url": "changelog.html", "priority": 50},
    ],
    "api_docs": [
        {"title": "Version", "url": "version.html", "priority": 10},
        {"title": "Generate", "url": "generate.html", "priority": 20},
        {"title": "Chat", "url": "chat.html", "priority": 30},
        {"title": "Embed", "url": "embed.html", "priority": 40},
        {"title": "Models API", "url": "models_api.html", "priority": 50},
        {"title": "System API", "url": "system_api.html", "priority": 60},
    ],
}

for section, items in default_navigation.items():
    if section in nav_structure:
        if not nav_structure[section]["items"]:
            nav_structure[section]["items"] = items
    else:
        if section in DOCUMENTATION_CATEGORIES:
            nav_structure[section] = {
                "caption": DOCUMENTATION_CATEGORIES[section]["caption"],
                "description": DOCUMENTATION_CATEGORIES[section].get("description", ""),
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
