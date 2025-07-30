"""
MigraCraft Version Information
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Release information
RELEASE_NAME = "Artisan"
RELEASE_DATE = "2025-01-16"

# Features introduced in this version
FEATURES = [
    "YAML-driven schema definitions",
    "Differential migrations",
    "Multi-language entity generation",
    "Comprehensive schema validation",
    "Foreign key support",
    "Index management",
    "PostgreSQL functions support",
    "Rollback migrations",
    "Modular architecture"
]

# Supported languages for entity generation
SUPPORTED_LANGUAGES = [
    "typescript",
    "python", 
    "dart",
    "java",
    "cpp",
    "csharp",
    "go"
]

def get_version():
    """Get the version string"""
    return __version__

def get_version_info():
    """Get version info as tuple"""
    return __version_info__

def print_banner():
    """Print MigraCraft banner"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                        MigraCraft 🛠️                         ║
║              Craft perfect PostgreSQL migrations              ║
║                                                              ║
║  Version: {__version__} ({RELEASE_NAME})                               ║
║  Released: {RELEASE_DATE}                                   ║
║                                                              ║
║  Languages: {len(SUPPORTED_LANGUAGES)} supported for entity generation        ║
║  Features: {len(FEATURES)} core features                                ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)
