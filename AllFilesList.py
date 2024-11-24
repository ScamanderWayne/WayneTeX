import os

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
        # Check if the current item is a directory
        is_last_item = (i == total_items - 1)

        if os.path.isdir(item_path):
            # Skip ignored directories
            if item in ignored_directories:
                continue
            # Draw directory and recurse into it
            tree += f"{prefix}{'└── ' if is_last_item else '├── '}{item}/\n"
            tree += generate_file_tree(item_path, depth + 1, ignored_directories, prefix + ("    " if is_last_item else "│   "))
        else:
            # Draw file
            tree += f"{prefix}{'└── ' if is_last_item else '├── '}{item}\n"

    return tree

def write_file_tree_to_file(root_dir, output_file, ignored_directories=None):
    """Writes the directory tree to a file with a tree-like view."""
    try:
        tree = generate_file_tree(root_dir, ignored_directories=ignored_directories)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree)
        print(f"File tree saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    root_directory = "."  # Change to the directory you want to scan
    output_file = "file_tree.txt"  # Output file name
    ignored_directories = [".git"]  # Directories to ignore
    write_file_tree_to_file(root_directory, output_file, ignored_directories)
