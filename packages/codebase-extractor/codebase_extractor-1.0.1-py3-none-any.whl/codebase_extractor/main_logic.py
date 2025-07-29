import os
import sys
import time
import datetime
import uuid
import shutil
import argparse
from pathlib import Path
from typing import List, Optional

import questionary
from halo import Halo
from termcolor import colored
from prompt_toolkit.styles import Style
from questionary import Validator, ValidationError

# Import from our new modules
from . import config
from . import ui
from . import file_handler

class NumberValidator(Validator):
    """Validates that the input is a positive integer."""
    def validate(self, document):
        try:
            value = int(document.text)
            if value <= 0:
                raise ValidationError(
                    message="Please enter a positive number.",
                    cursor_position=len(document.text))
        except ValueError:
            raise ValidationError(
                message="Please enter a valid number.",
                cursor_position=len(document.text))

def main():
    """Main function to run the CLI application."""
    exit_message = colored("\nExtraction aborted by user. Closing Code Extractor. Goodbye.", "red")

    try:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '-ni', '--no-instructions',
            action='store_true'
        )
        args, _ = parser.parse_known_args()
        
        ui.clear_screen()
        ui.print_banner()
        
        if not args.no_instructions:
            ui.show_instructions()
        else:
            input(colored("\nPress Enter to begin...", "green"))
            ui.clear_screen()

        root_path = Path.cwd()
        
        select_style = Style([('qmark', 'fg:#FFA500'), ('pointer', 'fg:#FFA500'), ('highlighted', 'fg:black bg:#FFA500'), ('selected', 'fg:black bg:#FFA500')])
        checkbox_style = Style([('qmark', 'fg:#FFA500'), ('pointer', 'fg:#FFA500'), ('highlighted', 'fg:#FFA500'), ('selected', 'fg:#FFA500'), ('checkbox-selected', 'fg:#FFA500')])

        print("=== Extraction Settings ===")
        exclude_large = questionary.select("[1/2] -- Exclude files larger than 1MB?", choices=["yes", "no"], style=select_style, instruction=" ").ask()
        if exclude_large is None:
            # This check is now inside the try block, but we handle the exit gracefully.
            raise KeyboardInterrupt

        exclude_large = exclude_large == "yes"
        print()

        folders_to_process = set()
        process_root_files = False
        
        run_ref = str(uuid.uuid4())
        run_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        selection_mode = questionary.select("[2/2] -- What do you want to extract?", choices=["Everything (all folders and root files)", "Specific folders/root from a list"], style=select_style, instruction=" ").ask()
        if selection_mode is None:
            raise KeyboardInterrupt

        if selection_mode == "Everything (all folders and root files)":
            folders_to_process.update([p for p in root_path.iterdir() if p.is_dir() and p.name not in config.EXCLUDED_DIRS])
            process_root_files = True
        else:
            depth_str = questionary.text(
                "-- How many levels deep should we scan for folders?",
                default="3",
                validate=NumberValidator,
                style=select_style
            ).ask()
            if depth_str is None:
                raise KeyboardInterrupt
            scan_depth = int(depth_str)

            folder_choices = file_handler.get_folder_choices(root_path, max_depth=scan_depth)
            selected_options = None
            confirm_exit = False
            
            checkbox_instruction = "(Arrows to move, Space to select, A to toggle, I to invert)"

            while not selected_options:
                selection = questionary.checkbox(
                    "-- Select folders/sub-folders to extract (must select at least one):", 
                    choices=folder_choices, 
                    style=checkbox_style,
                    instruction=checkbox_instruction
                ).ask()
                
                if selection is None:
                    if confirm_exit:
                        raise KeyboardInterrupt
                    else:
                        confirm_exit = True
                        print(colored("\n[!] Press Ctrl+C again to exit.", "yellow"))
                        continue
                
                confirm_exit = False
                
                if not selection:
                    print(colored("[!] Error: You must make a selection.", "red"))
                    continue
                    
                selected_options = selection
                break
            
            if "ROOT_SENTINEL" in selected_options:
                process_root_files = True
                selected_options.remove("ROOT_SENTINEL")

            selected_paths = [root_path / p for p in selected_options]
            sorted_paths = sorted(selected_paths, key=lambda p: len(p.parts))
            
            final_paths = set()
            for path in sorted_paths:
                if not any(path.is_relative_to(parent) for parent in final_paths):
                    final_paths.add(path)
            
            folders_to_process.update(final_paths)

        print()
        total_files_extracted = 0

        for folder_path in sorted(list(folders_to_process)):
            with Halo(text=f"Extracting {folder_path.relative_to(root_path)}...", spinner="dots"):
                time.sleep(0.1)
                folder_md, folder_count = file_handler.extract_code_from_folder(folder_path, exclude_large)
                if folder_count > 0:
                    metadata = {"run_ref": run_ref, "run_timestamp": run_timestamp, "folder_name": str(folder_path.relative_to(root_path)), "file_count": folder_count}
                    file_handler.write_to_markdown_file(folder_md, metadata, root_path)
                    total_files_extracted += folder_count
                    print(f"✅ Extracted {folder_count} file(s) from: {folder_path.relative_to(root_path)}")
                else:
                    print(f"[!] No extractable files in: {folder_path.relative_to(root_path)}")
            print("")

        if process_root_files:
            root_display_name = f"root [{root_path.name}] (files in root folder only, excl. sub-folders)"
            with Halo(text=f"Extracting {root_display_name}...", spinner="dots"):
                time.sleep(0.1)
                root_md, root_count = file_handler.extract_code_from_root(root_path, exclude_large)
                if root_count > 0:
                    metadata = {"run_ref": run_ref, "run_timestamp": run_timestamp, "folder_name": root_display_name, "file_count": root_count}
                    file_handler.write_to_markdown_file(root_md, metadata, root_path)
                    total_files_extracted += root_count
                    print(f"✅ Extracted {root_count} file(s) from the root directory")
                else:
                    print("[!] No extractable files in the root directory")
            print("")
            
        try:
            width = shutil.get_terminal_size((80, 20)).columns
        except OSError:
            width = 80

        if total_files_extracted > 0:
            output_dir_path = Path(config.OUTPUT_DIR_NAME).resolve()
            print(colored(f"Success! A total of {total_files_extracted} file(s) have been extracted.", "grey", "on_green"))
            print(f"Files saved in: {colored(str(output_dir_path), 'cyan')}")
        else:
            print(colored("Extraction complete, but no files matched the criteria.", "yellow"))
        
        print("\n")
        print("-" * width)
        print("💡 Love this tool? Found a bug? Share your feedback on GitHub:")
        print(config.GITHUB_URL + "\n")
        print("🤝 Connect with the author on LinkedIn:")
        print(config.LINKEDIN_URL + "\n")
        print("☕ Enjoying this tool? You can support its development with a coffee!")
        print("https://www.buymeacoffee.com/lukaszlekowski\n")

    except KeyboardInterrupt:
        print(exit_message)
        sys.exit(0)