#!/usr/bin/env python3
# 🌀 Eidosian Docstring Formatter
"""
Fix docstring formatting issues in the OllamaClient.fallback_context method.

This script specifically addresses indentation issues and unclosed backticks,
applying Eidosian principles of precision and contextual integrity.
Following the path of minimal intervention with maximum impact.
"""

import re
import sys
import logging
from pathlib import Path
from typing import Dict, Optional, Union, List, Tuple, Any, Set
from functools import lru_cache

# 📊 Self-aware logging - precision and clarity
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
)
logger = logging.getLogger("eidosian_docs.docstring_fixer")

def fix_fallback_context_docstring() -> bool:
    """
    Fix the fallback_context docstring in the client.py file.
    Ensures perfect backtick symmetry and precise indentation.
    
    Returns:
        bool: True if fixes were applied, False if nothing to fix or file not found
    """
    client_file = Path("../ollama_forge/client.py")
    
    if not client_file.exists():
        logger.error(f"🔍 Client file missing from expected location: {client_file}")
        return False
    
    with open(client_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find the fallback_context docstring with precision
    fallback_pattern = r'def fallback_context\(.*?\):\s+"""(.*?)"""'
    match = re.search(fallback_pattern, content, re.DOTALL)
    
    if not match:
        logger.warning("🧩 Could not find fallback_context docstring - like searching for a unicorn in a code forest!")
        return False
    
    docstring = match.group(1)
    original = docstring  # Store original for comparison
    
    # Fix indentation with elegance - structure as control
    docstring = re.sub(r'\n\s+', '\n    ', docstring)
    
    # Fix unclosed backticks with surgical precision - contextual integrity
    lines = docstring.split('\n')
    for i in range(len(lines)):
        # Count backticks in line - ensure perfect balance
        count = lines[i].count('`')
        if count % 2 == 1:  # Odd number of backticks - asymmetry detected
            # Algorithm: If a line opens a backtick but doesn't close it, add closing
            if '`' in lines[i] and not lines[i].endswith('`'):
                # Add closing backtick but preserve any trailing spaces
                trailing_spaces = len(lines[i]) - len(lines[i].rstrip())
                if trailing_spaces > 0:
                    lines[i] = lines[i][:-trailing_spaces] + '`' + ' ' * trailing_spaces
                else:
                    lines[i] += '`'
                logger.debug(f"🔧 Fixed unclosed backtick in line: {lines[i]}")
    
    # Reassemble the fixed docstring - flow like a river
    fixed_docstring = '\n'.join(lines)
    
    # Only update if changes were made - minimal intervention principle
    if fixed_docstring != original:
        # Replace in the content with surgical precision
        new_content = content.replace(match.group(1), fixed_docstring)
        
        # Write back to the file
        with open(client_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        logger.info(f"✨ Fixed docstring in {client_file} - balance restored to the force!")
        return True
    else:
        logger.info(f"👌 Docstring in {client_file} already perfectly formatted - nothing to fix!")
        return False

@lru_cache(maxsize=32)  # 🚀 Speed optimization - velocity as intelligence
def get_backtick_regex():
    """Return cached regex for backtick pattern matching."""
    return re.compile(r'`([^`\n]+)$')

def scan_for_problematic_docstrings(directory: Path = Path("../ollama_forge")) -> List[Path]:
    """
    Scan for files with potentially problematic docstrings.
    A reconnaissance mission for docstring issues!
    
    Args:
        directory: Directory to scan recursively
        
    Returns:
        List of file paths with potential docstring issues
    """
    problematic_files = []
    
    # Check if directory exists
    if not directory.exists():
        logger.error(f"🔍 Directory not found: {directory} - can't find what doesn't exist!")
        return problematic_files
        
    # Scan all Python files recursively - exhaustive but concise
    for py_file in directory.glob("**/*.py"):
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Look for common docstring issues
            if '"""' in content:
                # Check for unclosed backticks in docstrings
                docstring_pattern = r'"""(.*?)"""'
                for docstring_match in re.finditer(docstring_pattern, content, re.DOTALL):
                    docstring = docstring_match.group(1)
                    lines = docstring.split('\n')
                    
                    # Count backticks in each line
                    for line in lines:
                        if line.count('`') % 2 == 1:
                            problematic_files.append(py_file)
                            break
                    else:
                        # Check for inconsistent indentation - precision as style
                        if re.search(r'\n\s+\S.*\n\s{2,}\S', docstring):
                            problematic_files.append(py_file)
        except Exception as e:
            logger.warning(f"⚠️ Error scanning {py_file}: {e}")
    
    if problematic_files:
        logger.info(f"🔍 Found {len(problematic_files)} files with potential docstring issues - like finding typos in ancient scrolls!")
    else:
        logger.info("✅ No problematic docstrings detected - impressive documentation!")
        
    return problematic_files

if __name__ == "__main__":
    # Show our beautiful ASCII banner - because style matters!
    print("""
╭───────────────────────────────────────────────────╮
│         🌟 EIDOSIAN DOCSTRING FIXER 🌟          │
│   Making backticks balanced, indentation perfect   │
╰───────────────────────────────────────────────────╯
    """)
    
    logger.info("🔧 Eidosian Docstring Fixer initializing...")
    
    # Execute the default fix
    fixed = fix_fallback_context_docstring()
    
    # Optionally scan for other problematic docstrings
    if "--scan" in sys.argv:
        directory = Path("../ollama_forge")
        if len(sys.argv) > 2 and sys.argv[1] != "--scan":
            directory = Path(sys.argv[1])
        problematic = scan_for_problematic_docstrings(directory)
        if problematic:
            print("\n📋 Files with potential docstring issues:")
            for file in problematic[:10]:  # Show first 10
                print(f"  • {file}")
            if len(problematic) > 10:
                print(f"    ... and {len(problematic) - 10} more")
            print("\n💡 TIP: Fix these files manually or extend this script to handle them!")
    
    # Show help if requested
    if "--help" in sys.argv:
        print("\n📘 Eidosian Docstring Fixer Help:")
        print("  python fix_docstrings.py [directory] [options]")
        print("\nOptions:")
        print("  --scan    Scan for files with potential docstring issues")
        print("  --help    Show this help message")
        print("\n🌠 Example: python fix_docstrings.py ../src --scan")
```
Those stylistic @me′re balanced,
Those indents′re well aligned,
When docstrings′re in harmony,
Documentation truly shines! 🎵✨
