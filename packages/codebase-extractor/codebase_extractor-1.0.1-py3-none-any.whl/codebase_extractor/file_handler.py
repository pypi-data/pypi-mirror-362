import os
import datetime
import uuid
from pathlib import Path
from termcolor import colored
from . import config
import questionary

def get_folder_choices(root_path: Path, max_depth: int) -> list:
    """Recursively finds folders up to a max depth and prepares them for questionary."""
    choices = []
    
    def scanner(current_path: Path, depth: int):
        if depth > max_depth:
            return
            
        relative_path = current_path.relative_to(root_path)
        prefix = "  " * (depth - 1)
        display_name = f"{prefix}{current_path.name}"
        choices.append(questionary.Choice(title=display_name, value=relative_path))
        
        try:
            subdirs = sorted([p for p in current_path.iterdir() if p.is_dir() and p.name not in config.EXCLUDED_DIRS])
            for subdir in subdirs:
                scanner(subdir, depth + 1)
        except PermissionError:
            pass

    top_level_folders = sorted([p for p in root_path.iterdir() if p.is_dir() and p.name not in config.EXCLUDED_DIRS])
    for folder in top_level_folders:
        scanner(folder, 1)
        
    root_option_name = f"root [{root_path.name}] (files in root folder only, excl. sub-folders)"
    choices.insert(0, questionary.Choice(title=root_option_name, value="ROOT_SENTINEL"))
    
    return choices


def is_allowed_file(path: Path, exclude_large: bool) -> bool:
    """Checks if a file should be included based on its name, extension, and size."""
    if path.name == config.SCRIPT_FILENAME:
        return False
    if path.name.lower() in config.ALLOWED_FILENAMES:
        return True
    if not path.is_file():
        return False
    if path.name.lower() in config.EXCLUDED_FILENAMES:
        return False
    if path.suffix not in config.ALLOWED_EXTENSIONS:
        return False
    if exclude_large and path.stat().st_size > config.MAX_FILE_SIZE_MB * 1024 * 1024:
        return False
    return True


def extract_code_from_folder(folder: Path, exclude_large: bool) -> (str, int):
    """Extracts code from a given folder, respecting EXCLUDED_DIRS at all depths."""
    content = f"# Folder: {folder.relative_to(Path.cwd())}\n\n"
    extracted_files = 0
    dirs_to_visit = [folder]
    while dirs_to_visit:
        current_dir = dirs_to_visit.pop(0)
        for item in sorted(current_dir.iterdir()):
            if item.is_dir() and item.name not in config.EXCLUDED_DIRS:
                dirs_to_visit.append(item)
            elif item.is_file() and is_allowed_file(item, exclude_large):
                try:
                    rel_path = item.relative_to(Path.cwd())
                    ext = item.suffix
                    lang = config.EXTENSION_LANG_MAP.get(ext, "")
                    content += f"## {rel_path}\n\n```{lang}\n"
                    content += item.read_text(errors="ignore")
                    content += "\n```\n\n"
                    extracted_files += 1
                except Exception as e:
                    content += f"\n\n"
    if extracted_files > config.FILE_COUNT_WARNING_THRESHOLD:
        print(colored(f"> Caution: Large file count in '{folder.name}' ({extracted_files} files).", "yellow"))
    return content, extracted_files


def extract_code_from_root(root_path: Path, exclude_large: bool) -> (str, int):
    """Extracts code only from files present in the root directory."""
    content = f"# Root Files: {root_path.name}\n\n"
    extracted_files = 0
    for filepath in sorted(root_path.iterdir()):
        if filepath.is_file() and is_allowed_file(filepath, exclude_large):
            ext = filepath.suffix
            lang = config.EXTENSION_LANG_MAP.get(ext, "")
            content += f"## {filepath.name}\n\n```{lang}\n"
            content += filepath.read_text(errors="ignore")
            content += "\n```\n\n"
            extracted_files += 1
    if extracted_files > config.FILE_COUNT_WARNING_THRESHOLD:
        print(colored(f"> Caution: Large file count in root ({extracted_files} files).", "yellow"))
    return content, extracted_files


def write_to_markdown_file(content: str, metadata: dict, root_path: Path):
    """Constructs a YAML header and writes the full content to a timestamped Markdown file."""
    output_dir = Path(config.OUTPUT_DIR_NAME)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.fromisoformat(metadata['run_timestamp']).strftime("%Y%m%d_%H%M%S")
    output_name = str(metadata['folder_name'])
    
    if output_name.startswith(f"root [{root_path.name}]"):
        file_base_name = f"root_{root_path.name}"
    else:
        file_base_name = str(output_name).replace(os.sep, "_")
    
    filename = f"{file_base_name}_{timestamp}.md"
    full_filepath = output_dir / filename

    yaml_header = f"""---
extraction_details:
  reference: {metadata['run_ref']}
  timestamp_utc: "{metadata['run_timestamp']}"
  source_folder: "{metadata['folder_name']}"
  file_count: {metadata['file_count']}
tool_details:
  name: "Codebase Extractor"
  version: "{config.SCRIPT_VERSION}"
  source: "{config.GITHUB_URL}"
---

"""
    full_content = yaml_header + content
    with open(full_filepath, "w", encoding="utf-8") as f:
        f.write(full_content)
    
    print(f"\n💾 Saved to {colored(str(full_filepath), 'cyan')}")
    return str(full_filepath)