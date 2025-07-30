import ast
import os
import sys
import logging
import argparse
from pathlib import Path

import importlib.metadata
from stdlib_list import stdlib_list

# ──────────────────────────────
# Optional Submodule to Package Mapping
# ──────────────────────────────
SUBMODULE_TO_PACKAGE = {
    "pkg_resources": "setuptools",
    # Add more if needed
}

# ──────────────────────────────
# Logger Setup
# ──────────────────────────────
def setup_logger(enable_file_log=False):
    logger = logging.getLogger("importscanner")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if enable_file_log:
        file_handler = logging.FileHandler("importscanner.log")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger

# ──────────────────────────────
# Utility Functions
# ──────────────────────────────

def is_stdlib(module_name: str) -> bool:
    try:
        version_str = f"{sys.version_info.major}.{sys.version_info.minor}"
        return module_name in stdlib_list(version_str)
    except Exception as e:
        logger.warning(f"Failed to check if '{module_name}' is stdlib: {e}")
        return False

def is_installed_package(module_name: str) -> bool:
    try:
        actual_name = SUBMODULE_TO_PACKAGE.get(module_name, module_name)
        importlib.metadata.version(actual_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False
    except Exception as e:
        logger.warning(f"Error checking installed package for '{module_name}': {e}")
        return False

def extract_imports_from_file(file_path: str) -> set:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except (SyntaxError, UnicodeDecodeError, OSError) as e:
        logger.error(f"Skipping {file_path}: {e}")
        return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
    return imports

def scan_directory(path: str) -> set:
    all_imports = set()
    logger.info(f"📂 Scanning directory: {path}")
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                imports = extract_imports_from_file(file_path)
                all_imports |= imports
    logger.debug(f"🔍 Total unique imports found: {len(all_imports)}")
    return all_imports

def classify_imports(imports: set):
    stdlib = set()
    third_party = set()
    local = set()

    for module in imports:
        if is_stdlib(module):
            stdlib.add(module)
        elif is_installed_package(module):
            third_party.add(module)
        else:
            local.add(module)

    return stdlib, third_party, local

def save_requirements(third_party: set):
    logger.info("💾 Saving requirements.txt...")
    try:
        with open("requirements.txt", "w") as f:
            for pkg in sorted(third_party):
                try:
                    version = importlib.metadata.version(pkg)
                    f.write(f"{pkg}=={version}\n")
                except Exception as e:
                    logger.warning(f"⚠️ Could not get version for '{pkg}': {e}")
                    f.write(f"{pkg}\n")
        logger.info("✅ requirements.txt saved.")
    except Exception as e:
        logger.error(f"❌ Failed to save requirements.txt: {e}")

# ──────────────────────────────
# Entry Point
# ──────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="list-imports",
        description="🔍 List and classify Python imports (standard, third-party, local) in your project directory.",
        epilog="""
Examples:
  list-imports
      Scan current directory and show all imports grouped by type.

  list-imports ./src --save
      Scan './src' directory and save third-party packages to requirements.txt

  list-imports --log
      Enable logging to 'importscanner.log'
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the Python project (default: current directory)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save third-party packages to a requirements.txt file",
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="Enable logging to importscanner.log (default: disabled)",
    )

    args = parser.parse_args()

    # Initialize logger based on --log flag
    global logger
    logger = setup_logger(enable_file_log=args.log)

    try:
        path = Path(args.path).resolve()
        if not path.exists() or not path.is_dir():
            logger.error(f"❌ Invalid path: {path}")
            print(f"❌ Invalid path: {path}")
            return

        all_imports = scan_directory(str(path))
        stdlib, third_party, local = classify_imports(all_imports)

        print("\n📦 Third-Party Packages (installed via pip):")
        if third_party:
            for mod in sorted(third_party):
                print(f"  - {mod}")
        else:
            print("  (None detected)")

        print("\n📁 Local Modules (your own project's files/modules):")
        if local:
            for mod in sorted(local):
                print(f"  - {mod}")
        else:
            print("  (None detected)")

        print("\n📚 Standard Library (built-in Python modules):")
        if stdlib:
            for mod in sorted(stdlib):
                print(f"  - {mod}")
        else:
            print("  (None detected)")

        if args.save:
            save_requirements(third_party)

    except Exception as e:
        logger.exception(f"❌ Unexpected error: {e}")
        print("❌ An unexpected error occurred. Check importscanner.log for details.")

if __name__ == "__main__":
    main()
