#!/usr/bin/env python3
# 🌀 Version update tool with Eidosian elegance – precise and fluid! 🎯
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃             V E R S I O N   U P D A T E   T O O L               ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""
Synchronized version management for Ollama Forge.

This script ensures that version information is consistently updated
across all project files, maintaining a single source of truth.
It leverages the existing version management system while adding
specific attention to packaging files that need version updates.
"""

import re
import sys
from pathlib import Path
import argparse
from datetime import datetime
import importlib.util

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔍 Path and Module Setup - Finding Project Resources
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def find_repo_root() -> Path:
    """Find repository root directory from current location. 🏠"""
    current_path = Path(__file__).resolve()
    
    # Navigate up until we find a directory with .git, pyproject.toml, or setup.py
    for path in [current_path, *current_path.parents]:
        if any((path / marker).exists() for marker in [".git", "pyproject.toml", "setup.py"]):
            return path
    
    # Fallback to directory containing this script
    return current_path.parent.parent

REPO_ROOT = find_repo_root()
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
CONFIG_PATH = REPO_ROOT / "ollama_forge" / "config.py"
VERSION_PATH = REPO_ROOT / "version.py"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧰 Dynamic Module Loading - Flexible and Robust
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def import_module_from_path(path: Path, module_name: str):
    """Import a module from a file path. 🧩"""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load spec for {module_name} from {path}")
        
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔄 Version Management - Synchronized Updates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def update_version(new_version: str, dry_run: bool = False):
    """
    Update version across all project files.
    
    Args:
        new_version: The new version string (X.Y.Z format)
        dry_run: If True, only show what would be changed without making changes
    """
    start_time = datetime.now()
    print(f"🔍 Looking for version module...")
    
    # Try to use the existing version module if available
    try:
        version_module = import_module_from_path(VERSION_PATH, "version")
        current_version = version_module.__version__
        print(f"✅ Found version module. Current version: {current_version}")
        
        if not dry_run:
            print(f"🔄 Updating version from {current_version} to {new_version}")
            version_module.update_version_universally(new_version)
        else:
            print(f"🔍 DRY RUN: Would update version from {current_version} to {new_version}")
    except (ImportError, AttributeError) as e:
        print(f"⚠️ Could not use version module: {e}")
        print("🔧 Falling back to manual file updates")
        update_files_manually(new_version, dry_run)
    
    # Additional verification for pyproject.toml because it's critical for packaging
    verify_pyproject_version(new_version, dry_run)
    
    # Report completion time
    duration = (datetime.now() - start_time).total_seconds()
    print(f"⏱️ Version update completed in {duration:.2f} seconds")

def verify_pyproject_version(expected_version: str, dry_run: bool):
    """Verify pyproject.toml has correct version, update if needed."""
    if not PYPROJECT_PATH.exists():
        print(f"⚠️ Could not find pyproject.toml at {PYPROJECT_PATH}")
        return
        
    with open(PYPROJECT_PATH, 'r') as f:
        content = f.read()
        
    # Check if version is already correct
    pattern = r'version\s*=\s*["\']([^"\']+)["\']'
    match = re.search(pattern, content)
    if not match:
        print("⚠️ Could not find version in pyproject.toml")
        return
        
    current_version = match.group(1)
    
    if current_version == expected_version:
        print(f"✓ pyproject.toml already at version {expected_version}")
        return
        
    if dry_run:
        print(f"🔍 DRY RUN: Would update pyproject.toml: {current_version} → {expected_version}")
        return
        
    # Update pyproject.toml version
    new_content = re.sub(
        pattern,
        f'version = "{expected_version}"',
        content
    )
    
    with open(PYPROJECT_PATH, 'w') as f:
        f.write(new_content)
        
    print(f"📝 Updated pyproject.toml: {current_version} → {expected_version}")

def update_files_manually(new_version: str, dry_run: bool):
    """Update version in key files when version module cannot be used."""
    # Extract version components
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', new_version)
    if not match:
        print(f"❌ Invalid version format: {new_version}. Expected X.Y.Z format.")
        return
        
    major, minor, patch = map(int, match.groups())
    
    # Files to update with their patterns
    files_to_update = {
        PYPROJECT_PATH: [
            (r'version\s*=\s*["\']([^"\']+)["\']', f'version = "{new_version}"')
        ],
        CONFIG_PATH: [
            (r'VERSION_MAJOR\s*=\s*(\d+)', f'VERSION_MAJOR = {major}'),
            (r'VERSION_MINOR\s*=\s*(\d+)', f'VERSION_MINOR = {minor}'),
            (r'VERSION_PATCH\s*=\s*(\d+)', f'VERSION_PATCH = {patch}'),
            (r'VERSION\s*=\s*["\']([^"\']+)["\']', f'VERSION = "{new_version}"'),
        ],
        VERSION_PATH: [
            (r'__version__\s*=\s*["\']([^"\']+)["\']', f'__version__ = "{new_version}"'),
            (r'major\s*=\s*(\d+)', f'major = {major}'),
            (r'minor\s*=\s*(\d+)', f'minor = {minor}'),
            (r'patch\s*=\s*(\d+)', f'patch = {patch}'),
        ]
    }
    
    for file_path, patterns in files_to_update.items():
        if not file_path.exists():
            print(f"⚠️ File not found: {file_path}")
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        original_content = content
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
            
        if content != original_content:
            if dry_run:
                print(f"🔍 DRY RUN: Would update {file_path}")
            else:
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"📝 Updated {file_path}")
        else:
            print(f"✓ No changes needed in {file_path}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🏃 Command Line Interface - Streamlined Usage
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    """Command-line entrypoint with elegant argument parsing."""
    parser = argparse.ArgumentParser(
        description="Update version information across all project files"
    )
    parser.add_argument(
        "version",
        help="New version number (X.Y.Z format)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without making changes"
    )
    args = parser.parse_args()
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', args.version):
        print(f"❌ Invalid version format: {args.version}")
        print("Version must be in X.Y.Z format (e.g., 1.2.3)")
        return 1
    
    update_version(args.version, args.dry_run)
    return 0

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║  🌀 Ollama Forge Version Updater 🌀     ║")
    print("╚══════════════════════════════════════════╝")
    sys.exit(main())
