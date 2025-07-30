# importscanner

> A lightweight CLI tool to list and classify Python imports: standard library, pip-installed (third-party), and local modules.

## 📦 Features

- Detects and lists:
  - ✅ Standard Library imports
  - ✅ Third-Party (pip-installed) packages
  - ✅ Local custom modules
- Optionally generates `requirements.txt`
- Works on any Python project
- Clean logging to console and file (`importscanner.log`)
- Handles syntax errors, broken files, and missing packages gracefully

---

## 🚀 Installation

```bash
# From PyPI (once published)
pip install importscanner

# Or clone and install locally
git clone https://github.com/harshmeet-1029/importscanner.git.git
cd importscanner
pip install .
