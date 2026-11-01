import os
import shutil
from pathlib import Path

# Define extension mapping based on requirements
EXTENSION_MAP = {
    # Documents
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.xlsx': 'Documents',
    
    # Images
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    
    # Videos
    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.mov': 'Videos',
    
    # Archives
    '.zip': 'Archives',
    '.tar': 'Archives',
    '.gz': 'Archives',
    '.rar': 'Archives',
    
    # Code
    '.py': 'Code',
    '.js': 'Code',
    '.html': 'Code',
    '.css': 'Code'
}

def organize_directory(target_dir_path):
    target_dir = Path(target_dir_path)
    
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: The directory '{target_dir_path}' does not exist.")
        return

    print(f"Scanning and organizing: {target_dir.resolve()}\n")
    
    # Tracking counts for summary log
    stats = {category: 0 for category in set(EXTENSION_MAP.values())}
    stats['Unknown/Skipped'] = 0
    total_moved = 0

    # Iterating through items using os.scandir via pathlib for efficiency
    for path in target_dir.iterdir():
        # Skip directories and the script itself if run inside the same folder
        if path.is_dir() or path.name == 'organizer.py':
            continue
            
        file_extension = path.suffix.lower()
        category = EXTENSION_MAP.get(file_extension)

        if category:
            dest_folder = target_dir / category
            dest_file_path = dest_folder / path.name
            
            try:
                # Dynamically create category subfolder if it doesn't exist
                dest_folder.mkdir(exist_ok=True)
                
                # Naming collision handling
                if dest_file_path.exists():
                    # Append a numeric suffix if a file with the same name exists
                    base_name = path.stem
                    counter = 1
                    while dest_file_path.exists():
                        dest_file_path = dest_folder / f"{base_name}_{counter}{file_extension}"
                        counter += 1
                
                # Safely move the file
                shutil.move(str(path), str(dest_file_path))
                print(f"[MOVED] {path.name} -> {category}/{dest_file_path.name}")
                
                stats[category] += 1
                total_moved += 1

            except PermissionError:
                print(f"[ERR - Permission Denied] Could not move {path.name}")
                stats['Unknown/Skipped'] += 1
            except FileExistsError:
                print(f"[ERR - File Exists] Conflict moving {path.name}")
                stats['Unknown/Skipped'] += 1
            except Exception as e:
                print(f"[ERR - Unexpected] {e} while moving {path.name}")
                stats['Unknown/Skipped'] += 1
        else:
            stats['Unknown/Skipped'] += 1

    # Print Formatted Execution Summary
    print("\n" + "="*40)
    print("        EXECUTION SUMMARY LOG        ")
    print("="*40)
    for cat, count in stats.items():
        if count > 0:
            print(f" 📂 {cat:<18} : {count} file(s)")
    print("-"*40)
    print(f" Total Files Relocated    : {total_moved}")
    print("="*40)

if __name__ == "__main__":
    # You can change '.' to any absolute path (e.g., '/Users/username/Downloads')
    target_folder = input("Enter the directory path to organize (Press Enter for current directory '.'): ").strip()
    if not target_folder:
        target_folder = '.'
        
    organize_directory(target_folder)
