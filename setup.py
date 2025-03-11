#!/usr/bin/env python3
# 🌀 Setup with Eidosian thoroughness – bridging all dimensions seamlessly! 🌉
"""
╔══════════════════════════════════════════════════════════════════════════╗
║ 🌀 EIDOSIAN SETUP SCRIPT: WHERE FUNCTION MEETS FORM                     ║
║ 📐 PRECISION ARCHITECTURE FOR PACKAGE DISTRIBUTION                       ║
╚══════════════════════════════════════════════════════════════════════════╝

Legacy setup script for Ollama Forge. 
Each import path represents a layer of resilience 🛡️
Each fallback embodies recursive adaptation 🔄

📚 Eidosian Principles in Action:
1. 🎯 Contextual Integrity - No redundant imports, each path serves a purpose
2. 😄 Humor as Cognitive Leverage - "Epicenter of synergy" lightens complex imports
3. 🗜️ Exhaustive But Concise - Complete error handling without verbosity
4. 🌊 Flow Like a River - Smooth transitions between import attempts
5. 🔧 Hyper-Personal Yet Universal - Works locally or in any CI environment
6. 🔄 Recursive Refinement - Multiple fallback strategies for robustness
7. ✨ Precision as Style - Clean variable assignments with minimal overhead
8. ⚡ Velocity as Intelligence - Fast import paths with optimal checking
9. 🏛️ Structure as Control - Hierarchical import strategy with clear boundaries
10. 🔍 Self-Awareness as Foundation - Import failures trigger intelligent defaults
"""

import setuptools
import os
import sys
from pathlib import Path
import time

# ⏱️ Track import strategy performance
start_time = time.time()

# 🧠 Self-awareness check - validate environment before proceeding
if sys.version_info < (3, 8):
    sys.exit("🚨 Python 3.8+ required - your time machine is stuck in the past! 🕰️")

# 🧩 Import Strategy: Layered resilience with graceful degradation
try:
    # 🥇 Primary path: Direct module access for maximum performance
    config_path = Path(__file__).parent / "ollama_forge" / "config.py"
    if config_path.exists():
        sys.path.insert(0, str(config_path.parent))
        from config import (
            PACKAGE_NAME_NORMALIZED,
            get_version_string,
            get_author_string,
            get_email_string,
        )
        version = get_version_string()  # 📊 Version from source
        author = get_author_string()    # 👤 Author attribution 
        author_email = get_email_string()  # 📧 Contact pathway
        description = "Python client library and CLI for Ollama"
        import_path = "🔍 Direct config module"
    else:
        # 🥈 Secondary path: Package import with namespace resolution
        sys.path.insert(0, os.path.abspath('.'))
        from ollama_forge.config import (
            PACKAGE_NAME_NORMALIZED,
            get_version_string,
            get_author_string,
            get_email_string,
        )
        version = get_version_string()
        author = get_author_string()
        author_email = get_email_string()
        description = "Python client library and CLI for Ollama"
        import_path = "🔁 Package namespace resolution"
except ImportError:
    # 🛡️ Fallback shield: Default values ensure continuity
    version = "0.1.9"  # 🏷️ Baseline version
    author = "Lloyd Handyside, Eidos"  # ✍️ Attribution preserved
    author_email = "ace1928@gmail.com, syntheticeidos@gmail.com"
    description = "Python client library and CLI for Ollama"
    PACKAGE_NAME_NORMALIZED = "ollama_forge"
    import_path = "⚠️ Fallback values (ImportError shield activated)"

# ⚡ Performance metrics - because velocity matters
import_time = time.time() - start_time

# 📦 Package registration: Minimal yet complete
setuptools.setup(
    name=PACKAGE_NAME_NORMALIZED,  # 🏷️ Identity
    version=version,               # 🔢 Semantic versioning 
    author=author,                 # 👤 Creator attribution
    author_email=author_email,     # 📫 Contact vector
    description=description,       # 📝 Purpose statement
)

# 🔄 Self-reflection output - no wasted cycles
if os.environ.get("OLLAMA_FORGE_DEBUG") == "1":
    print(f"⚙️ Setup initialized via {import_path}")
    print(f"⏱️ Import strategy completed in {import_time:.6f}s")
    print(f"📦 Package: {PACKAGE_NAME_NORMALIZED} v{version}")
