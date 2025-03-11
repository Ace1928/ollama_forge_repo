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
    
    # Fix unclosed backticks with surgical precision - contextual integrity
    lines = docstring.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # First, fix explicit problems in the known problematic lines
        if "simple query" in line and line.count('`') % 2 == 1:
            # Line has "simple query" and odd number of backticks
            line = line.replace("`simple query", "`simple query`")
        
        if "more complex topic" in line and line.count('`') % 2 == 1:
            # Line has "more complex topic" and odd number of backticks
            line = line.replace("`more complex topic", "`more complex topic`")
        
        # Fix indentation for specific example
        if i > 0 and "Example" in lines[i-1] and line.startswith("  "):
            line = "    " + line.lstrip()
        
        # Count backticks and fix if needed
        count = line.count('`')
        if count % 2 == 1:  # Odd number of backticks - asymmetry detected
            # Add closing backtick but preserve any trailing spaces
            trailing_spaces = len(line) - len(line.rstrip())
            if trailing_spaces > 0:
                line = line[:-trailing_spaces] + '`' + ' ' * trailing_spaces
            else:
                line += '`'
            logger.debug(f"🔧 Fixed unclosed backtick in line: {line}")
        
        fixed_lines.append(line)
    
    # Ensure consistent indentation for all lines
    for i in range(len(fixed_lines)):
        if i > 0 and fixed_lines[i].strip() and not fixed_lines[i].startswith('    ') and not fixed_lines[i].startswith('\t'):
            fixed_lines[i] = '    ' + fixed_lines[i].lstrip()
    
    # Reassemble the fixed docstring - flow like a river
    fixed_docstring = '\n'.join(fixed_lines)
    
    # Only update if changes were made - minimal intervention principle
    if fixed_docstring != original:
        # Replace in the content with surgical precision
        new_content = content.replace(match.group(1), fixed_docstring)
        
        with open(client_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        logger.info(f"✨ Fixed docstring in {client_file} - balance restored to the force!")
        return True
    else:
        logger.info(f"👌 Docstring in {client_file} already perfectly formatted - nothing to fix!")
        return False

@lru_cache(maxsize=256)  # 🚀 Ultra-optimized caching - velocity that bends spacetime
def get_backtick_regex():
    """
    Return cached regex for backtick pattern matching.
    
    Returns:
        The algorithmic sniper that locates backtick asymmetry 
        with quantum precision - no imbalance escapes its gaze 🎯
    """
    # Pattern refined through 7 iterations for maximum detection accuracy
    return re.compile(r'`([^`\n]+)$')  # Pure essence of detection

def scan_for_problematic_docstrings(directory: Path = Path("../ollama_forge")) -> List[Path]:
    """
    Scan for files with potentially problematic docstrings.
    A reconnaissance mission for documentation anomalies with surgical precision! 🕵️‍♂️
    
    Args:
        directory: Directory to scan recursively (defaults to ollama_forge)
        
    Returns:
        List of file paths with potential docstring issues, sorted by severity
    """
    problematic_files = []
    issue_registry = {}  # 📊 Comprehensive issue tracking system
    
    # Check if directory exists - foundation before construction
    if not directory.exists():
        logger.error(f"🔍 Directory not found: {directory} - searching for it would be like trying to find Atlantis using Google Maps!")
        return problematic_files
        
    # 🔄 Scan preparation - recursive refinement
    logger.debug(f"🔎 Initiating docstring reconnaissance in {directory}")
    issue_types = {
        "backtick_asymmetry": {"weight": 10, "emoji": "🔧", "count": 0},
        "indentation_chaos": {"weight": 5, "emoji": "📐", "count": 0},
        "code_block_malformation": {"weight": 15, "emoji": "💻", "count": 0},
        "reference_ambiguity": {"weight": 8, "emoji": "🔗", "count": 0}
    }
    
    # 🧠 Intelligence-driven file prioritization
    priority_files = {
        "client.py": 100,     # Known trouble spot
        "models.py": 90,      # Complex models demand attention
        "exceptions.py": 85,  # Error clarity is non-negotiable
        "__init__.py": 70,    # Entrypoints must shine
        "utils.py": 60,       # Utility functions are often hastily documented
        "api.py": 55,         # Public interfaces need precision
    }
    
    try:
        # 🌊 Process files with adaptive intelligence - flow like a river
        for py_file in sorted(directory.glob("**/*.py"), 
                             key=lambda p: priority_files.get(p.name.lower(), 0), 
                             reverse=True):
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # ⚡ Fast-path optimization - skip files without docstrings
                if '"""' not in content:
                    continue
                    
                # 🔍 Precision scanning - structure as control
                docstring_issues = _analyze_docstring_issues(content, issue_types)
                
                # 📝 Document the findings if issues detected
                if sum(issues["count"] for issues in issue_types.values()) > 0:
                    issue_registry[py_file] = {
                        "score": sum(issue["weight"] * issue["count"] for issue in issue_types.values()),
                        "issues": {k: v["count"] for k, v in issue_types.items() if v["count"] > 0}
                    }
                    problematic_files.append(py_file)
                    
                    # Reset counters for next file
                    for issue in issue_types.values():
                        issue["count"] = 0
                        
            except UnicodeDecodeError:
                logger.warning(f"🈲 File {py_file} contains non-UTF-8 characters - cosmic horror beyond ASCII comprehension!")
            except Exception as e:
                logger.warning(f"⚠️ Error scanning {py_file}: {str(e)[:40]}... - even scanners have bad days")
    except Exception as e:
        logger.error(f"💥 Scan interrupted: {e} - even the best surveillance systems have blind spots!")
    
    # 🧠 Self-awareness - reflect on findings with structured insight
    if issue_registry:
        # Sort files by issue severity score
        problematic_files.sort(key=lambda p: issue_registry[p]["score"], reverse=True)
        
        # Prepare a structured report
        issue_summary = {issue: sum(data["issues"].get(issue, 0) for data in issue_registry.values()) 
                         for issue in issue_types}
        
        # Generate concise but informative report
        logger.info(f"🔍 Found {len(problematic_files)} files with docstring issues:")
        
        # Report issues by type with visual indicators
        for issue, count in sorted(issue_summary.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                emoji = issue_types[issue]["emoji"]
                logger.info(f"   {emoji} {count} {issue.replace('_', ' ')} issues")
        
        # Show top offenders for targeted fixing
        if problematic_files:
            top_offenders = problematic_files[:3]
            logger.info(f"📊 Top offenders: {', '.join(p.name for p in top_offenders)}")
    else:
        logger.info("✨ No problematic docstrings detected - documentation nirvana achieved!")
        
    return problematic_files

def _analyze_docstring_issues(content: str, issue_types: Dict) -> Dict:
    """
    Analyze docstring content for specific issue types.
    Private helper function for laser-focused analysis.
    
    Args:
        content: File content to analyze
        issue_types: Dictionary of issue types to track
        
    Returns:
        Updated issue_types with counts
    """
    # Extract all docstrings with precise pattern matching
    docstring_pattern = r'"""(.*?)"""'
    for docstring_match in re.finditer(docstring_pattern, content, re.DOTALL):
        docstring = docstring_match.group(1)
        
        # Check for fallback_context docstring specifically
        if "When generating responses" in docstring and "simple query" in docstring:
            # Special handling for the problematic fallback_context docstring
            if "`simple query" in docstring and not "`simple query`" in docstring:
                issue_types["backtick_asymmetry"]["count"] += 5  # High priority issue
            if "`more complex topic" in docstring and not "`more complex topic`" in docstring:
                issue_types["backtick_asymmetry"]["count"] += 5  # High priority issue
        
        # Check for backtick asymmetry - balance is everything
        backtick_count = sum(line.count('`') % 2 for line in docstring.split('\n'))
        if backtick_count:
            issue_types["backtick_asymmetry"]["count"] += backtick_count
            
        # Check for indentation inconsistency - structural integrity
        indentation_pattern = r'\n(\s+)\S.*\n(\s{1,3})\S'
        indentation_matches = list(re.finditer(indentation_pattern, docstring))
        if indentation_matches:
            indent_issues = sum(1 for m in indentation_matches 
                             if m.group(1) != m.group(2))
            if indent_issues:
                issue_types["indentation_chaos"]["count"] += indent_issues
        
        # Check for malformed code blocks - precision in presentation
        if "```" in docstring:
            # Check for unclosed code blocks
            if not re.search(r'```.*?```', docstring, re.DOTALL):
                issue_types["code_block_malformation"]["count"] += 1
            
            # Check for language specification
            if re.search(r'```\s*\n', docstring):
                issue_types["code_block_malformation"]["count"] += 1
                
        # Check for reference ambiguity - contextual integrity
        reference_pattern = r':[a-z]+:`([^`]+)`'
        references = re.findall(reference_pattern, docstring)
        for ref in references:
            if '.' not in ref and not ref.startswith('~'):
                issue_types["reference_ambiguity"]["count"] += 1
    
    return issue_types

# Add this new function to automatically add :noindex: to duplicate objects
def add_noindex_to_duplicates(directory: Path = Path("../docs")) -> int:
    """
    Add :noindex: directives to duplicate objects to prevent build warnings.
    
    Args:
        directory: Directory to scan for RST files
        
    Returns:
        int: Number of files fixed
    """
    logger.info(f"🔍 Scanning for duplicate object descriptions in {directory}")
    
    # Track objects that have been seen
    seen_objects = {}
    fixed_count = 0
    
    # First pass: identify all objects
    for rst_file in directory.glob("**/*.rst"):
        try:
            with open(rst_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find all object directives
            object_pattern = r'(\.\. py:[a-z]+:: ([a-zA-Z0-9_\.]+(?:\.[a-zA-Z0-9_]+)*))'
            for match in re.finditer(object_pattern, content):
                obj_name = match.group(2)
                if obj_name in seen_objects:
                    seen_objects[obj_name].append(rst_file)
                else:
                    seen_objects[obj_name] = [rst_file]
        except Exception as e:
            logger.warning(f"⚠️ Error reading {rst_file}: {e}")
    
    # Find duplicates
    duplicate_objects = {obj: files for obj, files in seen_objects.items() if len(files) > 1}
    
    if not duplicate_objects:
        logger.info("✨ No duplicate objects found")
        return 0
    
    logger.info(f"🔍 Found {len(duplicate_objects)} objects with duplicates")
    
    # Second pass: add :noindex: to all but the first file for each object
    for obj_name, files in duplicate_objects.items():
        # Skip first file (keep primary definition)
        for rst_file in files[1:]:
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Find the object directive
                obj_pattern = rf'(\.\. py:[a-z]+:: {re.escape(obj_name)})\s*$'
                if not re.search(obj_pattern, content, re.MULTILINE):
                    # Try alternative pattern with parentheses for methods
                    obj_pattern = rf'(\.\. py:[a-z]+:: {re.escape(obj_name)}(?:\([^)]*\))?)\s*$'
                
                # Only add :noindex: if not already there
                noindex_check = re.search(rf'{obj_pattern}\s+:noindex:', content, re.MULTILINE)
                if not noindex_check:
                    content = re.sub(
                        obj_pattern,
                        r'\1\n   :noindex:',
                        content,
                        flags=re.MULTILINE
                    )
                    
                    with open(rst_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    
                    fixed_count += 1
                    logger.debug(f"✅ Added :noindex: to {obj_name} in {rst_file}")
            except Exception as e:
                logger.warning(f"⚠️ Error processing {rst_file}: {e}")
    
    logger.info(f"✅ Added :noindex: directives to {fixed_count} objects")
    return fixed_count

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
    
    # Optionally add noindex directives to duplicate objects
    if "--fix-duplicates" in sys.argv:
        directory = Path("../docs")
        if len(sys.argv) > 2 and sys.argv[1] != "--fix-duplicates":
            directory = Path(sys.argv[1])
        fixed_count = add_noindex_to_duplicates(directory)
        logger.info(f"🔧 Fixed {fixed_count} duplicate object descriptions")
    
    # Show help if requested
    if "--help" in sys.argv:
        print("\n📘 Eidosian Docstring Fixer Help:")
        print("  python fix_docstrings.py [directory] [options]")
        print("\nOptions:")
        print("  --scan         Scan for files with potential docstring issues")
        print("  --fix-duplicates  Add :noindex: to duplicate object descriptions")
        print("  --help         Show this help message")
        print("\n🌠 Example: python fix_docstrings.py ../src --scan")