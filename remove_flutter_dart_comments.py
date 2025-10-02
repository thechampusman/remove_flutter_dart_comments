#!/usr/bin/env python3
"""
Remove // and /* */ comments from all .dart files in a Flutter project.
This script tries to preserve string literals and character escapes.

USAGE:
  python remove_flutter_dart_comments.py
  or run: run_flutter_comment_remover.bat

Back up your project before running this script!
"""
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


def remove_comments(src: str) -> str:
    out = []
    i = 0
    n = len(src)
    in_single = False
    in_double = False
    in_triple_single = False
    in_triple_double = False
    in_block_comment = False
    in_line_comment = False
    while i < n:
        ch = src[i]


        if in_block_comment:
            if ch == '*' and i + 1 < n and src[i+1] == '/':
                in_block_comment = False
                i += 2
                continue
            else:
                i += 1
                continue

        if in_line_comment:
            if ch == '\n':
                in_line_comment = False
                out.append(ch)
            i += 1
            continue

        if in_triple_single:
            if ch == "'" and src[i:i+3] == "'''":
                out.append("'''")
                i += 3
                in_triple_single = False
                continue
            else:
                out.append(ch)
                i += 1
                continue

        if in_triple_double:
            if ch == '"' and src[i:i+3] == '"""':
                out.append('"""')
                i += 3
                in_triple_double = False
                continue
            else:
                out.append(ch)
                i += 1
                continue

        if in_single:
            if ch == "\\":

                if i + 1 < n:
                    out.append(ch)
                    out.append(src[i+1])
                    i += 2
                    continue
                else:
                    out.append(ch)
                    i += 1
                    continue
            if ch == "'":
                out.append(ch)
                in_single = False
                i += 1
                continue
            out.append(ch)
            i += 1
            continue

        if in_double:
            if ch == "\\":
                if i + 1 < n:
                    out.append(ch)
                    out.append(src[i+1])
                    i += 2
                    continue
                else:
                    out.append(ch)
                    i += 1
                    continue
            if ch == '"':
                out.append(ch)
                in_double = False
                i += 1
                continue
            out.append(ch)
            i += 1
            continue

        if ch == '/' and i + 1 < n:
            nxt = src[i+1]
            if nxt == '/':
                in_line_comment = True
                i += 2
                continue
            if nxt == '*':
                in_block_comment = True
                i += 2
                continue


        if ch == "'":
            if src[i:i+3] == "'''":
                in_triple_single = True
                out.append("'''")
                i += 3
                continue
            in_single = True
            out.append(ch)
            i += 1
            continue

        if ch == '"':
            if src[i:i+3] == '"""':
                in_triple_double = True
                out.append('"""')
                i += 3
                continue
            in_double = True
            out.append(ch)
            i += 1
            continue

        out.append(ch)
        i += 1

    return ''.join(out)


def process_file(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Failed to read {path}: {e}")
        return False

    cleaned = remove_comments(content)
    if cleaned == content:
        return True

    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"[OK] Cleaned: {path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write {path}: {e}")
        return False


def is_flutter_project(path: str) -> bool:
    """Check if the given path is a Flutter project directory"""
    flutter_indicators = ['pubspec.yaml', 'lib', 'android', 'ios']
    path_obj = Path(path)
    
    if not path_obj.exists() or not path_obj.is_dir():
        return False
        
    # Check for pubspec.yaml (most important indicator)
    pubspec_path = path_obj / 'pubspec.yaml'
    if pubspec_path.exists():
        try:
            with open(pubspec_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'flutter:' in content.lower():
                    return True
        except:
            pass
    
    # Check for lib directory (where Dart files are typically located)
    lib_dir = path_obj / 'lib'
    return lib_dir.exists() and lib_dir.is_dir()

def get_flutter_project_path_fallback() -> str:
    """Fallback text-based input when GUI fails"""
    print("\nFalling back to text input...\n")
    
    while True:
        folder_path = input("Enter the path to your Flutter project folder: ").strip()
        
        if not folder_path:
            print("❌ Please enter a valid path.\n")
            continue
            
        # Handle quotes around path
        folder_path = folder_path.strip('"\'')
        
        # Convert to absolute path
        folder_path = os.path.abspath(folder_path)
        
        if not os.path.exists(folder_path):
            print(f"❌ Path does not exist: {folder_path}\n")
            continue
            
        if not os.path.isdir(folder_path):
            print(f"❌ Path is not a directory: {folder_path}\n")
            continue
            
        if not is_flutter_project(folder_path):
            print(f"❌ This doesn't appear to be a Flutter project.")
            print(f"   Looking for: pubspec.yaml with 'flutter:' or lib/ directory")
            print(f"   Path: {folder_path}\n")
            
            choice = input("Do you want to continue anyway? (y/N): ").strip().lower()
            if choice not in ['y', 'yes']:
                continue
        
        print(f"✅ Flutter project detected: {folder_path}\n")
        return folder_path

def get_flutter_project_path() -> str:
    """Interactively get the Flutter project path from user using file dialog"""
    print("Flutter/Dart Comment Remover")
    print("=============================")
    print("This tool will remove all // and /* */ comments from Dart files.")
    print("\n⚠️  IMPORTANT: Back up your project before proceeding!\n")
    print("A file dialog will open to select your Flutter project folder...")
    
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    
    try:
        while True:
            # Open folder selection dialog
            folder_path = filedialog.askdirectory(
                title="Select Flutter Project Folder",
                mustexist=True
            )
            
            if not folder_path:
                # User cancelled
                print("\nOperation cancelled by user.")
                root.destroy()
                sys.exit(0)
            
            # Convert to absolute path
            folder_path = os.path.abspath(folder_path)
            
            if not is_flutter_project(folder_path):
                # Show message box for non-Flutter projects
                result = messagebox.askyesno(
                    "Not a Flutter Project",
                    f"This doesn't appear to be a Flutter project.\n\n"
                    f"Looking for: pubspec.yaml with 'flutter:' or lib/ directory\n"
                    f"Path: {folder_path}\n\n"
                    f"Do you want to continue anyway?",
                    icon='warning'
                )
                
                if not result:
                    continue
            else:
                messagebox.showinfo(
                    "Flutter Project Detected",
                    f"✅ Flutter project detected!\n\nPath: {folder_path}",
                    icon='info'
                )
            
            print(f"✅ Selected folder: {folder_path}\n")
            root.destroy()
            return folder_path
            
    except Exception as e:
        print(f"Error with file dialog: {e}")
        root.destroy()
        # Fallback to text input
        return get_flutter_project_path_fallback()

def main():
    try:
        root = get_flutter_project_path()
        
        # GUI confirmation before proceeding
        tk_root = tk.Tk()
        tk_root.withdraw()
        tk_root.lift()
        tk_root.attributes('-topmost', True)
        
        confirm = messagebox.askyesno(
            "Confirm Processing",
            f"About to remove comments from all .dart files in:\n\n{root}\n\n" +
            "⚠️ This will modify files in-place!\n\n" +
            "Are you sure you want to continue?",
            icon='warning'
        )
        
        tk_root.destroy()
        
        if not confirm:
            print("Operation cancelled.")
            return 0
        
        print("\nProcessing files...")
        
        dart_files = []
        for dirpath, dirnames, filenames in os.walk(root):
            for name in filenames:
                if name.endswith('.dart'):
                    dart_files.append(os.path.join(dirpath, name))

        if not dart_files:
            print('❌ No .dart files found in the specified directory.')
            return 0
        
        print(f"Found {len(dart_files)} .dart files to process...\n")

        failures = []
        processed = 0
        for p in dart_files:
            ok = process_file(p)
            if ok:
                processed += 1
            else:
                failures.append(p)

        print(f"\n📊 Processing complete:")
        print(f"   ✅ Successfully processed: {processed} files")
        if failures:
            print(f"   ❌ Failed to process: {len(failures)} files")
            print('\nFiles that failed to process:')
            for f in failures:
                print(f'   - {f}')
            
            # Show error dialog
            tk_root = tk.Tk()
            tk_root.withdraw()
            messagebox.showerror(
                "Processing Complete with Errors",
                f"Processed: {processed} files\nFailed: {len(failures)} files\n\nCheck console for details.",
                icon='error'
            )
            tk_root.destroy()
            return 2
        else:
            print(f"   ❌ Failed: 0 files")
            
            # Show success dialog
            tk_root = tk.Tk()
            tk_root.withdraw()
            messagebox.showinfo(
                "Processing Complete!",
                f"🎉 Successfully processed {processed} Dart files!\n\nComments have been removed from your Flutter project.",
                icon='info'
            )
            tk_root.destroy()

        print('\n🎉 All done! Comments have been removed from your Dart files.')
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
