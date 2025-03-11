#!/usr/bin/env python3
# 🌀 Eidosian Duplicate Object Resolver
"""
Add :noindex: directives to duplicate object descriptions in RST files.

This script systematically resolves duplicate object description warnings
by adding :noindex: directives to all instances except the first occurrence.
Pure Eidosian principles in action: minimal intervention, maximum impact.
"""

import re
import sys
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

# 📊 Self-aware logging - precise and informative
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
)
logger = logging.getLogger("eidosian_docs.noindex_resolver")

def add_noindex_directives(docs_dir: Path = Path("../docs")) -> int:
    """
    Add :noindex: directives to duplicate object descriptions.
    
    Args:
        docs_dir: Documentation directory to process
        
    Returns:
        Number of files modified
    """
    start_time = __import__('time').time()
    logger.info(f"🔍 Scanning for duplicate objects in {docs_dir}")
    
    # Track all seen objects and their locations
    object_registry = defaultdict(list)
    autoapi_dir = docs_dir / "autoapi"
    api_dir = docs_dir / "api"
    
    # Stage 1: Build registry of all objects
    for directory in [autoapi_dir, api_dir]:
        if not directory.exists():
            continue
        
        for rst_file in directory.glob("**/*.rst"):
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Find all object directives
                for match in re.finditer(r'^\.\. py:([a-z]+):: ([a-zA-Z0-9_\.\(\)]+)', content, re.MULTILINE):
                    obj_type = match.group(1)
                    obj_name = match.group(2)
                    
                    # Clean up object name by removing parameters
                    if '(' in obj_name:
                        obj_name = obj_name.split('(')[0]
                    
                    # Store complete directive to have exact match for replacement
                    object_registry[obj_name].append((rst_file, match.group(0)))
            except Exception as e:
                logger.warning(f"⚠️ Error scanning {rst_file}: {e}")
    
    # Stage 2: Identify duplicate objects
    duplicates = {obj: locations for obj, locations in object_registry.items() if len(locations) > 1}
    logger.info(f"🔍 Found {len(duplicates)} objects with duplicates")
    
    # Stage 3: Add :noindex: to all duplicates (preserving first occurrence)
    modified_files = set()
    for obj_name, locations in duplicates.items():
        # Skip first occurrence - it will be the primary definition
        for rst_file, directive in locations[1:]:
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if :noindex: already exists for this directive
                pattern = rf'{re.escape(directive)}\s*(:noindex:)?(\n|$)'
                match = re.search(pattern, content)
                if match and not match.group(1):
                    # :noindex: doesn't exist, add it
                    replacement = f"{directive}\n   :noindex:"
                    new_content = re.sub(pattern, f"{replacement}\\2", content, count=1)
                    
                    with open(rst_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    modified_files.add(rst_file)
                    logger.debug(f"✅ Added :noindex: to {obj_name} in {rst_file.name}")
            except Exception as e:
                logger.warning(f"⚠️ Error processing {rst_file}: {e}")
    
    duration = __import__('time').time() - start_time
    logger.info(f"✅ Added :noindex: directives to objects in {len(modified_files)} files in {duration:.2f}s")
    return len(modified_files)

def fix_inline_literal_references(docs_dir: Path = Path("../docs")) -> int:
    """
    Fix unclosed backticks and other inline literal issues in RST files.
    
    Args:
        docs_dir: Documentation directory to process
        
    Returns:
        Number of files modified
    """
    logger.info(f"🔍 Scanning for unclosed backticks in {docs_dir}")
    
    autoapi_dir = docs_dir / "autoapi"
    if not autoapi_dir.exists():
        logger.warning(f"⚠️ AutoAPI directory not found: {autoapi_dir}")
        return 0
    
    modified_files = 0
    for rst_file in autoapi_dir.glob("**/*.rst"):
        try:
            with open(rst_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Fix incomplete backticks in class links
            updated_content = re.sub(r'(:class:|:exc:)`([^`]+)(?=[^`]*$)', r'\1`\2`', content)
            
            # Fix indentation issues
            lines = updated_content.split('\n')
            for i in range(len(lines)):
                # Check and fix mixed indentation
                if lines[i].startswith('   ') and not lines[i].startswith('    ') and lines[i].strip():
                    lines[i] = '    ' + lines[i][3:]
            
            updated_content = '\n'.join(lines)
            
            if updated_content != content:
                with open(rst_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                modified_files += 1
                logger.debug(f"✅ Fixed inline literal issues in {rst_file.name}")
        except Exception as e:
            logger.warning(f"⚠️ Error processing {rst_file}: {e}")
    
    logger.info(f"✅ Fixed inline literal issues in {modified_files} files")
    return modified_files

if __name__ == "__main__":
    # Show our beautiful ASCII banner - because style matters!
    print("""
╭───────────────────────────────────────────────────╮
│       🌟 EIDOSIAN DUPLICATE OBJECT RESOLVER 🌟    │
│    Making :noindex: directives bring harmony      │
╰───────────────────────────────────────────────────╯
    """)
    
    docs_dir = Path("../docs")
    if len(sys.argv) > 1 and sys.argv[1] != "--help":
        docs_dir = Path(sys.argv[1])
    
    if "--help" in sys.argv:
        print("\n📘 Usage Options:")
        print("  python add_noindex.py [docs_dir] [options]")
        print("\nOptions:")
        print("  --fix-literals  Also fix inline literal reference issues")
        print("  --help          Show this help message")
    else:
        # Add :noindex: directives to duplicate objects
        fixed_count = add_noindex_directives(docs_dir)
        
        # Optionally fix inline literal issues
        if "--fix-literals" in sys.argv:
            literal_fixes = fix_inline_literal_references(docs_dir)
            print(f"\n✅ Total files fixed: {fixed_count + literal_fixes}")
        else:
            print(f"\n✅ Total files fixed: {fixed_count}")
        
        if fixed_count > 0:
            print("\n💡 TIP: Run Sphinx build again to verify all duplicates are resolved!")
        else:
            print("\n💡 TIP: No duplicate objects found - your docs are already harmonious!")
