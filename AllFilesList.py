import os
from collections import Counter

def generate_file_tree(directory, depth=0, ignored_directories=None, prefix=""):
    """Recursively generates a file tree structure with a tree-like visual format."""
    if ignored_directories is None:
        ignored_directories = []

    tree = ""
    try:
        items = sorted(os.listdir(directory))  # Sort for consistent output
    except PermissionError:
        return f"{prefix}[Permission Denied]\n"

    total_items = len(items)
    for i, item in enumerate(items):
        item_path = os.path.join(directory, item)
        is_last_item = (i == total_items - 1)

        if os.path.isdir(item_path):
            if item in ignored_directories:
                continue
            tree += f"{prefix}{'└── ' if is_last_item else '├── '}{item}/\n"
            tree += generate_file_tree(item_path, depth + 1, ignored_directories, prefix + ("    " if is_last_item else "│   "))
        else:
            tree += f"{prefix}{'└── ' if is_last_item else '├── '}{item}\n"

    return tree

def get_file_extensions(directory, ignored_directories=None):
    """Collects and counts file extensions in the directory."""
    if ignored_directories is None:
        ignored_directories = []

    extensions_counter = Counter()
    for root, dirs, files in os.walk(directory):
        # Exclude ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_directories]
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:  # Only count files with extensions
                extensions_counter[ext] += 1

    return extensions_counter

def write_file_tree_to_file(root_dir, output_file, ignored_directories=None):
    """Writes the directory tree and file extension counts to a file."""
    try:
        tree = generate_file_tree(root_dir, ignored_directories=ignored_directories)
        extensions_counter = get_file_extensions(root_dir, ignored_directories)

        # Prepare the extensions list
        extensions_list = "\n".join(
            f"{ext} ({count})" for ext, count in sorted(extensions_counter.items())
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree)
            f.write("\n\n\n")  # Add three lines of whitespace
            f.write("File Extensions and Counts:\n")
            f.write(extensions_list)

        print(f"File tree and extension counts saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    root_directory = "."  # Change to the directory you want to scan
    output_file = "file_tree.txt"  # Output file name
    ignored_directories = [".git"]  # Directories to ignore
    write_file_tree_to_file(root_directory, output_file, ignored_directories)
