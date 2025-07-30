# 🧠 importscanner

> A lightweight CLI tool to list and classify Python imports: standard library, pip-installed (third-party), and local modules.

---

## 🎞️ Features

* 📚 **Categorizes Python imports**:

  * ✅ Standard Library modules
  * ✅ Third-party packages installed via `pip`
  * ✅ Your project's local modules
* ✍️ Optionally generates a `requirements.txt`
* 🦢 Works on any Python-based project or codebase
* 🧫 Graceful handling of broken files, bad syntax, and missing packages
* 📄 Optional logging to `importscanner.log`

---

## 🚀 Installation

### From PyPI (recommended):

```bash
pip install importscanner
```

### From source (GitHub):

```bash
git clone https://github.com/harshmeet-1029/importscanner.git
cd importscanner
pip install .
```

---

## 💻 Usage

Once installed, the CLI command is available as:

```bash
list-imports [directory] [--save] [--log]
```

### 🧪 Examples

#### ▶️ Basic usage (scan current directory):

```bash
list-imports
```

#### 📂 Scan a specific folder:

```bash
list-imports ./src
```

#### 📆 Save third-party packages to `requirements.txt`:

```bash
list-imports ./project --save
```

#### �� Enable log file output to `importscanner.log`:

```bash
list-imports --log
```

#### 📦 Combine all options:

```bash
list-imports ./backend --save --log
```

---

## 📂 Output Format

```
📦 Third-Party Packages (installed via pip):
  - requests
  - flask

📁 Local Modules (your own project's files/modules):
  - myutils
  - handlers

📚 Standard Library (built-in Python modules):
  - os
  - sys
  - json
```

---

## 📝 Notes

* Uses the `stdlib_list` package to detect standard library modules.
* Gracefully skips unreadable or invalid `.py` files.
* Supports Python 3.8+
