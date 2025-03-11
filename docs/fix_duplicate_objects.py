#!/usr/bin/env python3
# 🌀 Eidosian Duplicate Object Harmonizer
"""
Duplicate Object Harmonizer - Bringing Peace to Documentation Conflicts

This script identifies and resolves duplicate object descriptions in Sphinx 
documentation by adding strategic :noindex: directives, preventing build warnings
while maintaining semantic integrity.

Following Eidosian principles of:
- Structure as Control: Each object deserves exactly one canonical definition
- Precision as Style: Fixing only what needs fixing, with surgical accuracy
- Velocity as Intelligence: Fast, efficient scanning and targeted modifications
"""

import re
import sys
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Counter
import time

# 📊 Self-Aware Logging System
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
)
logger = logging.getLogger("eidosian_docs.duplicate_harmonizer")

class DuplicateObjectHarmonizer:
    """
    Identifies and resolves duplicate object descriptions with Eidosian precision.
    Like a diplomatic negotiator resolving namespace border disputes! 🏛️✨
    """
    
    def __init__(self, docs_dir: Path):
        """Initialize with the documentation directory to process."""
        self.docs_dir = Path(docs_dir)  # 📁 Documentation territory
        self.seen_objects: Dict[str, Path] = {}  # 🔍 First sighting registry
        self.fixed_count = 0  # 🧮 Victory counter
        self.collision_tracker = Counter()  # 📊 Conflict statistics
    
    def fix_duplicate_objects(self) -> int:
        """
        Find and fix all duplicate object descriptions with mathematical precision.
        
        Returns:
            Number of files fixed - a metric of harmony achieved! 🏆
        """
        # Reset counters for fresh run - tabula rasa
        self.seen_objects.clear()
        self.fixed_count = 0
        self.collision_tracker.clear()
        
        start_time = time.time()  # ⏱️ Track performance - velocity is intelligence!
        
        # 🔍 Phase 1: Reconnaissance - map the territory
        rst_files = list(self.docs_dir.glob("**/*.rst"))
        logger.info(f"🔎 Scanning {len(rst_files)} RST files for duplicate objects")
        
        # 🎯 Phase 2: Strategic intervention - fix duplicates with surgical precision
        for rst_file in rst_files:
            self._process_file(rst_file)
                
        # 📊 Phase 3: After-action report - knowledge is power
        duration = time.time() - start_time
        logger.info(f"✅ Fixed {self.fixed_count} duplicate object descriptions in {duration:.2f}s")
        
        # Show collision statistics if any were found
        if self.collision_tracker:
            top_collisions = self.collision_tracker.most_common(5)
            logger.info("📈 Top collision objects:")
            for obj_name, count in top_collisions:
                logger.info(f"  • {obj_name}: {count} occurrences")
        
        return self.fixed_count
    
    def _process_file(self, rst_file: Path) -> None:
        """Process a single RST file for duplicate objects."""
        try:
            with open(rst_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract object descriptions with precision - find:
            # .. py:<type>:: <object_name>
            # Where type can be class, function, method, attribute, etc.
            modified = False
            matches = list(re.finditer(r'(\.\. py:[a-z]+:: ([a-zA-Z0-9_\.]+)(?:\([^)]*\))?)', content))
            
            for match in matches:
                full_match = match.group(1)
                object_name = match.group(2)
                
                # Already seen this object elsewhere? Conflict detected!
                if object_name in self.seen_objects:
                    self.collision_tracker[object_name] += 1
                    
                    # Only add :noindex: if it doesn't already have it
                    check_range = content[match.start():match.start() + len(full_match) + 50]
                    if ':noindex:' not in check_range:
                        insert_pos = match.end()
                        content = content[:insert_pos] + "\n   :noindex:" + content[insert_pos:]
                        logger.debug(f"🔧 Added :noindex: to {object_name} in {rst_file.name}")
                        modified = True
                else:
                    # First sighting - claim territory
                    self.seen_objects[object_name] = rst_file
            
            # Only write if changes were made - efficient file I/O
            if modified:
                with open(rst_file, "w", encoding="utf-8") as f:
                    f.write(content)
                self.fixed_count += 1
                logger.info(f"✅ Fixed duplicates in {rst_file.name}")
                
        except Exception as e:
            # Elegant error handling - grace under pressure
            logger.error(f"❌ Error processing {rst_file}: {e}")

# 🚀 CLI Interface - the event horizon
if __name__ == "__main__":
    # Fancy ASCII art banner - because documentation deserves style!
    print("""
╭──────────────────────────────────────────╮
│ 🌀 EIDOSIAN DUPLICATE OBJECT HARMONIZER 🌀 │
│   Where every object finds its true home   │
╰──────────────────────────────────────────╯
""")
    
    # Parse command line arguments with elegance
    docs_dir = Path(__file__).parent  # Default: script's directory
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            print("\n🌟 Usage Options:")
            print("  python fix_duplicate_objects.py [docs_dir]")
            print("\n📝 Examples:")
            print("  python fix_duplicate_objects.py ../docs")
            print("  python fix_duplicate_objects.py")
            sys.exit(0)
        else:
            docs_dir = Path(sys.argv[1])
    
    # Verify directory exists - safety first!
    if not docs_dir.is_dir():
        logger.error(f"❌ Not a directory: {docs_dir}")
        sys.exit(1)
    
    # Create harmonizer and run it - execution is poetry in motion
    logger.info(f"🚀 Initializing for {docs_dir}")
    harmonizer = DuplicateObjectHarmonizer(docs_dir)
    fixed_count = harmonizer.fix_duplicate_objects()
    
    # Informative exit message - because endings matter too
    if fixed_count > 0:
        print(f"\n🎉 Success! Fixed {fixed_count} files with duplicate objects")
    else:
        print("\n✨ Perfect harmony already achieved! No duplicates found")
