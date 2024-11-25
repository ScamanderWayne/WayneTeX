import os
import shutil
import platform

def get_texmf_path():
    """Determine the target texmf directory based on the OS."""
    if platform.system() == "Windows":
        return r"C:\Users\alibi\texmf\tex\latex\waynepackages"
    else:
        return os.path.expanduser("~/texmf/tex/latex/waynepackages")

def get_relative_paths(directory):
    """
    Recursively collect all file paths in a directory,
    relative to the directory root.
    """
    relative_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), directory)
            relative_paths.append(relative_path)
    return set(relative_paths)

def sync_directories(source_dir, target_dir):
    """
    Synchronize files between source and target directories.
    Files in target_dir not present in source_dir will be deleted.
    """
    source_files = get_relative_paths(source_dir)
    target_files = get_relative_paths(target_dir)
    
    # Find files in target directory that are not in the source
    extra_files = target_files - source_files
    
    # Delete extra files
    for relative_path in extra_files:
        target_file_path = os.path.join(target_dir, relative_path)
        print(f"Deleting: {target_file_path}")
        os.remove(target_file_path)
    
    print("Synchronization complete.")

if __name__ == "__main__":
    my_packages_dir = os.path.join(os.getcwd(), "MyPackages")
    texmf_dir = get_texmf_path()

    # Ensure source and target directories exist
    if not os.path.exists(my_packages_dir):
        print(f"Source directory does not exist: {my_packages_dir}")
        exit(1)
    if not os.path.exists(texmf_dir):
        print(f"Target directory does not exist: {texmf_dir}")
        exit(1)
    
    # Sync directories
    sync_directories(my_packages_dir, texmf_dir)
