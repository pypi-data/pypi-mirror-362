# Codebase Extractor

<p align="center">
  <strong>A user-friendly CLI tool to extract project source code into structured Markdown files.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT%20(Modified)-yellow.svg" alt="License: MIT (Modified)">

</p>
<p align="center">
  💡 <b>Love this tool?</b> Found a bug or have an idea? Share it on <a href="https://github.com/lukaszlekowski/codebase-extractor">GitHub</a>! <br>
  🤝 <b>Connect with me</b> on <a href="https://www.linkedin.com/in/lukasz-lekowski">LinkedIn</a>. <br>
  ☕ <b>Enjoying it?</b> Support development with a <a href="https://www.buymeacoffee.com/lukaszlekowski">coffee</a>!
</p>

---

## 🚀 Overview

Codebase Extractor is a command-line interface (CLI) tool designed to scan a project directory and consolidate all relevant source code into neatly organized Markdown files. It's perfect for creating a complete project snapshot for analysis, documentation, or providing context to Large Language Models (LLMs) like GPT-4, Gemini, or Claude.

The tool is highly configurable, allowing you to select specific folders, exclude large files, and intelligently ignore common directories like `node_modules` and `.git`.

---

## ✨ Key Features

- **Interactive & User-Friendly:** A guided, multi-step CLI experience that makes selecting options simple and clear.
- **Smart Filtering:** Automatically excludes common dependency folders, build artifacts, version control directories, and IDE configuration files.
- **Flexible Selection Modes:** Choose to extract the entire project with one command, or dive into a specific selection mode.
- **🌳 Nested Folder Selection:** Interactively browse and select specific sub-folders from a tree-like view.
- **🔢 Configurable Scan Depth:** You decide how many levels deep the script should look for folders when building the selection tree.
- **YAML Metadata:** Each generated Markdown file is prepended with a YAML front matter block containing useful metadata like a unique run ID, timestamp, and file count for easy tracking and parsing.
- **🚀 Quick Start Mode:** Use the `--no-instructions` flag to skip the detailed intro guide on subsequent runs.
- **Safe & Robust:** Features graceful exit handling (`Ctrl+C`) and provides clear feedback during the extraction process.

---

## 🚀 Installation

This guide will walk you through installing and running the Codebase Extractor.

### Step 1: Ensure Python is Installed

Make sure you have Python 3.9 or newer installed. You can check your version by opening your terminal and running:

```bash
python3 --version
```

### Step 2: Install the Package

The recommended way to install is directly from PyPI using pip, which comes with Python.

#### ▶️ For macOS & Linux Users

Open your terminal and run the following command:

```bash
pip3 install codebase-extractor
```

If you encounter a permission denied error, your system may require you to install it for your user account only:

```bash
pip3 install --user codebase-extractor
```

In this case, you may need to add the user script directory to your PATH. The installer will provide the necessary command if this is required.

#### ▶️ For Windows Users

Open Command Prompt or PowerShell and run the following command:

```bash
pip install codebase-extractor
```

If the pip command is not found, you can try using the Python executable directly:

```bash
python -m pip install codebase-extractor
```

#### 💡 Pro Tip: Using pipx

For a more advanced, isolated installation, we recommend using pipx. This ensures the tool's dependencies do not conflict with other Python projects on your system.

```bash
pipx install codebase-extractor
```

---

## ▶️ Usage

### Basic Usage

Once installed, you can run the tool from any terminal window. Navigate to your project's root directory and run the command:

```bash
code-extractor
```

The script will then guide you through the extraction process.

## Quick Start

For repeat usage, you can skip the detailed introductory guide by using the `--no-instructions` or `-ni` flag:

```bash
code-extractor --no-instructions
```

### The Process

The tool will guide you through a series of prompts:

- **Initial Setup [1/2]**: A yes/no question to skip files larger than 1MB.
- **Extraction Mode [2/2]**: Choose whether to extract the entire project (`Everything`) or select specific folders.

### Specific Selection (if chosen):

- **Scan Depth**: You'll be asked how many sub-folder levels to scan for the selection list (defaults to 3).
- **Folder Tree**: You'll see a checklist of available folders and sub-folders to extract. The script handles selections intelligently:
  - Selecting a parent folder automatically includes all its sub-folders, so you don’t need to select them individually.
  - To extract only a sub-folder’s contents, select the sub-folder but not its parent.
  - The special `root [...]` option extracts only the files in your project's main directory, ignoring all sub-folders.

### Output Details

All output files are saved in a `CODEBASE_EXTRACTS` directory within your project folder. Each generated Markdown file includes a YAML metadata header with a unique reference ID, timestamp, and file count for easy tracking and parsing.

## 📜 License

This project is licensed under a modified MIT License. Please see the [LICENSE](LICENSE) file for the full text.

The standard MIT License has been amended with a single, important attribution requirement:

If you use, copy, or modify any part of this software, you must include a clear and visible attribution to the original author and project in your derivative work.

This attribution must include:

- A link back to this original GitHub repository: [https://github.com/lukaszlekowski/codebase-extractor](https://github.com/lukaszlekowski/codebase-extractor)
- A link to the author's LinkedIn profile: [https://www.linkedin.com/in/lukasz-lekowski](https://www.linkedin.com/in/lukasz-lekowski)
