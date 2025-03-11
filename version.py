# 🌀 Version management with Eidosian precision and clarity! 🎯
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃             E I D O S I A N   V E R S I O N   M O D U L E          ┃
# ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
# ┃ A fully structured, humor-tinged, self-aware, and flow-oriented    ┃
# ┃ approach ensuring each symbol supports the universal design.       ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""
Version information for the Ollama Forge package, refined with Eidosian principles:
• Contextual Integrity  • Humor as Cognitive Leverage  • Exhaustive but Concise
• Flow and Synergy      • Personal yet Universal       • Recursive Refinement
• Precision as Style    • Velocity as Intelligence     • Structure as Control
• Self-Awareness as Foundation

┌────────────────────────────────────────────────┐
│ 📊 VERSION ARCHITECTURE - EIDOSIAN PRECISION   │
├────────────────────────────────────────────────┤
│ Client version: 0.1.9                          │
│ Minimum Ollama server version: 0.1.11          │
│ Version pattern: MAJOR.MINOR.PATCH             │
└────────────────────────────────────────────────┘
"""

import os
import sys
import re
import logging
from datetime import datetime
from typing import Tuple, Dict, Union, Any, TypeVar, Protocol, List

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔄 Type Definitions - Precision and Correctness
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
T = TypeVar('T')
VersionLike = Union[str, 'SimpleVersion', Any]  # Generic type to handle various version formats
VersionDict = Dict[str, Union[int, bool, str]]  # Type for version comparison results

# Protocol for version objects - structural typing at its finest
class VersionProtocol(Protocol):
    major: int
    minor: int
    patch: int
    def __lt__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔍 Logging Setup - Self-Awareness through Observation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger("ollama_forge.version")
if os.environ.get("OLLAMA_FORGE_DEBUG") == "1":
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.debug("📝 Version module loaded with debug logging")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 Version Constants - Adaptive Import Strategy
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Use a configuration class to avoid constant redefinition issues
class VersionConfig:
    """Container for version configuration to avoid constant redefinition"""
    __version__ = "0.1.9"
    min_ollama_version = "0.1.11" 
    release_date = "2025-01-15"
    major = 0
    minor = 1
    patch = 9
    source = "direct_constants"

# Initialize with default values
version_config = VersionConfig()

try:
    from ollama_forge.config import (
        VERSION,
        VERSION_MAJOR,
        VERSION_MINOR, 
        VERSION_PATCH,
        VERSION_RELEASE_DATE
    )
    # Update with imported values
    version_config.__version__ = VERSION
    version_config.major = VERSION_MAJOR
    version_config.minor = VERSION_MINOR
    version_config.patch = VERSION_PATCH
    version_config.release_date = VERSION_RELEASE_DATE
    version_config.source = "config_module"
    logger.debug("✅ Version imported from config module")
except ImportError:
    # Fallback uses the default values we already set
    logger.debug("⚠️ Using direct version constants (config module not found)")

# Export constants for public use - creating only once with minimal changes
__version__ = version_config.__version__  
# Define these as references to the config object, not as new constants
# This solves the constant redefinition warnings
def get_major() -> int: return version_config.major
def get_minor() -> int: return version_config.minor
def get_patch() -> int: return version_config.patch
def get_release_date() -> str: return version_config.release_date

# Define properties-like constants that route through functions to avoid redefinition
MINIMUM_OLLAMA_VERSION = version_config.min_ollama_version
_VERSION_SOURCE = version_config.source

def get_version_tuple() -> Tuple[int, int, int]:
    """Return version as a tuple of (major, minor, patch). 🎯"""
    return (get_major(), get_minor(), get_patch())

def get_version_string() -> str:
    """Return the full version string, ensuring minimal clutter. ⚡"""
    return __version__

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔢 Version Parsing - Flexible Tools, Precise Results
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SimpleVersion:
    """
    A simplified version parser upholding precision and minimalism.
    Each comparison operator has purpose in semantic versioning.
    """
    def __init__(self, version_str: str):
        self._version_str = version_str
        self._is_valid = False
        
        # Parse with precision - extract exactly what's needed
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:[-.]?(.+))?$', version_str)
        if (match):
            self.major = int(match.group(1))
            self.minor = int(match.group(2))
            self.patch = int(match.group(3))
            # For compatibility with packaging.version
            self.micro = self.patch
            self.prerelease = match.group(4) if match.group(4) else None
            self._is_valid = True
        else:
            # Safe defaults - prevent unexpected behavior
            self.major = self.minor = self.patch = self.micro = 0
            self.prerelease = None
            if version_str:  # Only log if there was content to parse
                logger.warning(f"⚠️ Invalid version format: {version_str}")

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SimpleVersion):
            return NotImplemented
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        # Handle prerelease: None > any string (release > prerelease)
        if self.prerelease is None and other.prerelease is not None:
            return False
        if self.prerelease is not None and other.prerelease is None:
            return True
        return (self.prerelease or "") < (other.prerelease or "")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimpleVersion):
            return NotImplemented
        return ((self.major, self.minor, self.patch, self.prerelease) == 
                (other.major, other.minor, other.patch, other.prerelease))

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, SimpleVersion):
            return NotImplemented
        return other < self

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, SimpleVersion):
            return NotImplemented
        return self > other or self == other
        
    def __le__(self, other: object) -> bool:
        if not isinstance(other, SimpleVersion):
            return NotImplemented
        return self < other or self == other
        
    def __repr__(self) -> str:
        """String representation for debugging - part of self-awareness 🔍"""
        prerelease_str = f"-{self.prerelease}" if self.prerelease else ""
        return f"SimpleVersion({self._version_str}→{self.major}.{self.minor}.{self.patch}{prerelease_str})"
        
    def __str__(self) -> str:
        """User-friendly representation - humor meets clarity 😊"""
        prerelease_str = f"-{self.prerelease}" if self.prerelease else ""
        return f"{self.major}.{self.minor}.{self.patch}{prerelease_str}" + (
            "" if self._is_valid else " [⚠️ parsed from invalid format]"
        )

def parse_version(version_str: str, fallback_to_simple: bool = True) -> Any:
    """
    Parse version strings with Eidosian elegance and precision. 🔍
    
    Unifies multiple parsing approaches into a single, robust function:
    • Tries packaging.version for maximum compatibility
    • Falls back to SimpleVersion for resilience and consistent behavior
    • Normalizes input for greater flexibility
    • Self-aware error handling and graceful recovery
    
    Args:
        version_str: Version string to parse
        fallback_to_simple: Whether to use SimpleVersion as fallback (default: True)
        
    Returns:
        Parsed version object with comparison capabilities
    """
    
    # Remove leading 'v' or 'V' for flexibility
    cleaned_version = re.sub(r'^[vV]', '', version_str.strip())
    
    # Try packaging.version first - the industry standard
    try:
        from packaging.version import parse as packaging_parse
        parsed_version = packaging_parse(cleaned_version)
        logger.debug(f"✅ Version parsed with packaging: {version_str} → {parsed_version}")
        return parsed_version
    except ImportError:
        logger.debug("📦 packaging module not available, using SimpleVersion")
        return SimpleVersion(cleaned_version)
    except Exception as e:
        if not fallback_to_simple:
            # Re-raise if no fallback requested - precision through clarity
            logger.error(f"❌ Version parsing failed: {e}")
            raise
        
        # Graceful degradation - self-awareness in action
        logger.debug(f"⚠️ Packaging parser failed, using SimpleVersion fallback: {e}")
        return SimpleVersion(cleaned_version)

# Track the parser implementation for diagnostic purposes
version_parser_impl = "hybrid"
logger.debug("🔧 Using hybrid version parser with packaging priority and SimpleVersion fallback")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✨ Formatting & Presentation - Style with Substance
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def format_version_with_style(version: VersionLike) -> str:
    """
    Formats version string with visual elegance - Precision as Style principle.
    
    Args:
        version: Version string or object
        
    Returns:
        Stylized version string with perfect balance of clarity and aesthetics
    """
    try:
        # Handle version as string
        if isinstance(version, str):
            v = parse_version(version)
        else:
            # Try to use as-is if it's already a version object
            v = version
            
        # Adapt to different version object structures
        if hasattr(v, 'major') and hasattr(v, 'minor'):
            # Use patch or micro depending on what's available
            patch_value = getattr(v, 'patch', getattr(v, 'micro', 0))
            return f"v{v.major}.{v.minor}.{patch_value}"
            
        # Fallback for unknown version formats - still produce something useful
        return f"v{version}"
        
    except Exception as e:
        # Recovery with humor - make error states recognizable yet friendly
        logger.debug(f"Version formatting error: {e}")
        return f"v{version} (universal interpretation mode 🌌)"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧪 Compatibility Checking - Trust But Verify
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def is_compatible_ollama_version(version_str: str) -> bool:
    """
    Checks Ollama version compatibility with incisive precision:
    • Clear, focused verification
    • Meaningful feedback on failure
    • Graceful error handling
    
    Args:
        version_str: Version string to check against minimum
        
    Returns:
        True if compatible, False otherwise
    """
    try:
        min_version = parse_version(MINIMUM_OLLAMA_VERSION)
        current_version = parse_version(version_str)
        result = current_version >= min_version
        
        if not result:
            logger.warning(
                f"⚠️ Version {version_str} is below minimum {MINIMUM_OLLAMA_VERSION} - "
                f"like trying to run a sports car on cooking oil! 🏎️🛢️"
            )
        return result
        
    except Exception as e:
        # Precise error handling with information that helps fix the problem
        logger.error(f"❌ Version comparison failed: {e}")
        logger.debug(f"Version strings: comparing '{version_str}' with '{MINIMUM_OLLAMA_VERSION}'")
        return False  # Safe fallback - err on the side of caution

def calculate_version_delta(v1: str, v2: str) -> VersionDict:
    """
    Calculates the difference between version components.
    Flow and structure combine with contextual integrity.
    
    Args:
        v1: First version string (the "from" version)
        v2: Second version string (the "to" version)
        
    Returns:
        Dictionary with delta for each component, showing the version journey
    """
    try:
        ver1 = parse_version(v1)
        ver2 = parse_version(v2)
        
        # Extract components based on available attributes
        # Handle both SimpleVersion and packaging.Version
        if hasattr(ver1, 'patch') and hasattr(ver2, 'patch'):
            patch1, patch2 = ver1.patch, ver2.patch
        else:
            # Assume micro attribute (packaging.Version)
            patch1 = getattr(ver1, 'micro', 0)
            patch2 = getattr(ver2, 'micro', 0)
            
        return {
            "major": ver2.major - ver1.major,
            "minor": ver2.minor - ver1.minor,
            "patch": patch2 - patch1,
            "is_upgrade": ver2 > ver1,
            "is_downgrade": ver2 < ver1,
            "is_same": ver2 == ver1
        }
    except Exception as e:
        # Humor as cognitive aid - error becomes memorable
        logger.error(f"🙈 Version comparison went quantum: {e}")
        return {
            "major": 0, 
            "minor": 0, 
            "patch": 0,
            "is_upgrade": False, 
            "is_downgrade": False,
            "is_same": False,
            "error": str(e)
        }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔄 Version Management - Intelligent Updates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def update_version_universally(new_version: str) -> None:
    """
    Updates all references to the current version throughout the codebase:
    • Precise targeting for exactly what should change
    • Self-aware logging to track progress
    • Graceful failure handling to never leave things broken
    
    Args:
        new_version: New version string to apply globally
    """
    import os
    import re

    global __version__
    current_version = __version__
    start_time = datetime.now()  # ⏱️ Timing for self-reflection

    if current_version == new_version:
        logger.info(f"No version change needed. Current version is already {new_version}. ✅")
        return

    # 🎯 Validate with precision - Structure as Control
    version_match = re.match(r'^(\d+)\.(\d+)\.(\d+)', new_version)
    if not version_match:
        logger.error(f"Invalid version format: {new_version}. Expected format: X.Y.Z 🚫")
        return

    # Store new version components in local variables to avoid constant redefinition
    new_major_val = int(version_match.group(1))
    new_minor_val = int(version_match.group(2))
    new_patch_val = int(version_match.group(3))

    replaced_any = False
    files_updated: List[str] = []
    files_examined = 0
    
    # 🔄 Version change logging - Self-awareness in action
    logger.info(f"🚀 Updating version: {current_version} → {new_version}")
    logger.info(f"  Major: {get_major()} → {new_major_val}")
    logger.info(f"  Minor: {get_minor()} → {new_minor_val}")
    logger.info(f"  Patch: {get_patch()} → {new_patch_val}")

    # Recursive refinement: scanning directories, ensuring no hidden or extraneous paths
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for root, dirs, files in os.walk(repo_root):
        # Skip unnecessary directories - velocity through precision
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in 
                  ["__pycache__", "dist", "build", "venv", ".venv", ".git", "node_modules"]]
                  
        for name in files:
            # Skip non-text files and hidden files - focus on what matters
            if name.startswith('.') or not any(name.endswith(ext) for ext in 
                                              [".py", ".md", ".rst", ".txt", ".toml", ".yaml", ".yml", ".cfg"]):
                continue
                
            filepath = os.path.join(root, name)
            files_examined += 1
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Look for various ways the version might be specified
                new_content = re.sub(
                    rf'(version\s*=\s*["\']){re.escape(current_version)}(["\'])',
                    rf'\g<1>{new_version}\g<2>',
                    content
                )
                new_content = re.sub(
                    rf'(__version__\s*=\s*["\']){re.escape(current_version)}(["\'])',
                    rf'\g<1>{new_version}\g<2>',
                    new_content
                )
                new_content = re.sub(
                    rf'(VERSION_MAJOR\s*=\s*){get_major()}',
                    rf'\g<1>{new_major_val}',
                    new_content
                )
                new_content = re.sub(
                    rf'(VERSION_MINOR\s*=\s*){get_minor()}',
                    rf'\g<1>{new_minor_val}',
                    new_content
                )
                new_content = re.sub(
                    rf'(VERSION_PATCH\s*=\s*){get_patch()}',
                    rf'\g<1>{new_patch_val}',
                    new_content
                )

                # Update files only if something changed - avoid unnecessary writes
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    replaced_any = True
                    files_updated.append(filepath)
                    logger.debug(f"✏️ Updated version in {filepath}")
            except Exception as e:
                logger.error(f"❌ Error processing file {filepath}: {str(e)}")

    # Special handling for critical packaging files
    pyproject_path = os.path.join(repo_root, "pyproject.toml")
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path, "r", encoding="utf-8") as f:
                pyproject_content = f.read()
                
            # Enhanced pattern matching for pyproject.toml version
            new_pyproject_content = re.sub(
                r'(version\s*=\s*["\'])' + re.escape(current_version) + r'(["\'])',
                rf'\g<1>{new_version}\g<2>',
                pyproject_content
            )
            
            if new_pyproject_content != pyproject_content:
                with open(pyproject_path, "w", encoding="utf-8") as f:
                    f.write(new_pyproject_content)
                replaced_any = True
                files_updated.append(pyproject_path)
                logger.debug(f"✏️ Updated version in pyproject.toml")
        except Exception as e:
            logger.error(f"❌ Error updating pyproject.toml: {str(e)}")

    # ⏱️ Performance metrics - Velocity as Intelligence
    duration = (datetime.now() - start_time).total_seconds()
    
    # Update in-memory version values if files were changed
    if replaced_any:
        __version__ = new_version
        # Use the version_config to update values without redefining constants
        version_config.major = new_major_val
        version_config.minor = new_minor_val
        version_config.patch = new_patch_val
        
        # Precision in reporting with contextual details
        logger.info(f"🎉 Updated version from {current_version} to {new_version} in {len(files_updated)} files")
        logger.info(f"⚡ Processed {files_examined} files in {duration:.2f} seconds ({files_examined/duration:.1f} files/sec)")
        
        # Humor as cognitive aid - different messages based on performance
        if duration < 1.0:
            logger.info("🚀 Version updated faster than a caffeinated cheetah!")
        elif duration < 3.0:  
            logger.info("⚡ Version update complete - lightning fast!")
        else:
            logger.info("✅ Version update complete - slow and steady wins the race")
            
        # List files updated at debug level - detail when needed, not when distracting
        for file in files_updated[:5]:  # Show the first few
            logger.debug(f"  - {file}")
        if len(files_updated) > 5:
            logger.debug(f"  - ...and {len(files_updated) - 5} more files")
    else:
        # Clear feedback when nothing happened
        if files_examined > 10:
            logger.info(f"🔍 Examined {files_examined} files but found no version references to update")
            logger.info("Like searching for a digital needle in a haystack... and finding no needle!")
        else:
            logger.info("📭 No version references found. Nothing updated.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 Diagnostics - Self-Aware System
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_version_status() -> Dict[str, Any]:
    """
    Returns detailed version status information - Self-Awareness principle.
    Comprehensive yet concise report for troubleshooting and diagnostics.
    
    Returns:
        Dictionary with detailed version info and diagnostics
    """
    return {
        "version": __version__,
        "components": {
            "major": get_major(),
            "minor": get_minor(),
            "patch": get_patch()
        },
        "release_date": get_release_date(),
        "minimum_ollama_version": MINIMUM_OLLAMA_VERSION,
        "version_source": _VERSION_SOURCE,
        "module_path": __file__,
        "system_info": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "timestamp": datetime.now().isoformat()
        }
    }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 Command-line Interface - Velocity Through Tools
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    # Elegant entry point with character - striking and memorable
    print("╔═════════════════════════════════════════╗")
    print("║  🌀 Ollama Forge Version Utility 🌀     ║")
    print("╚═════════════════════════════════════════╝")
    
    # Flow - parse commands with clear, structured logic
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "get":
            print(f"📊 Version: {format_version_with_style(__version__)}")
            
        elif command == "check-compatible":
            if len(sys.argv) > 2:
                is_compatible = is_compatible_ollama_version(sys.argv[2])
                print(f"🔍 Version {sys.argv[2]} is {'✅ compatible' if is_compatible else '❌ incompatible'}")
            else:
                print("❌ Please provide a version to check")
                
        elif command == "update":
            if len(sys.argv) > 2:
                update_version_universally(sys.argv[2])
            else:
                print("❌ Please provide a new version")
                
        elif command == "status":
            import json
            print(json.dumps(get_version_status(), indent=2))
            
        elif command == "compare":
            if len(sys.argv) > 3:
                delta = calculate_version_delta(sys.argv[2], sys.argv[3])
                print(f"📊 Version comparison: {sys.argv[2]} → {sys.argv[3]}")
                print(f"  Major: {delta['major']}, Minor: {delta['minor']}, Patch: {delta['patch']}")
                if delta.get('is_upgrade'):
                    print("  🔼 This is an upgrade")
                elif delta.get('is_downgrade'):
                    print("  🔽 This is a downgrade")
                else:
                    print("  ⏸️ Versions are equivalent")
            else:
                print("❌ Please provide two versions to compare")
                
        else:
            # Clear help when invalid commands are given
            print(f"❓ Unknown command: {command}")
            print("Run without arguments to see available commands")
    else:
        # Concise but complete help menu - information at the point of need
        print(f"📦 Current version: {format_version_with_style(__version__)}")
        print("\nAvailable commands:")
        print("  get                     - Display current version")
        print("  check-compatible <VER>  - Check if version is compatible")
        print("  update <VER>            - Update version universally")
        print("  compare <VER1> <VER2>   - Compare two versions")
        print("  status                  - Show detailed version status")
