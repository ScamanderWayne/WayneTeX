import os

def generate_file_tree(directory, depth=0, ignored_directories=None):
    """Recursively generates a file tree structure."""
    if ignored_directories is None:
        ignored_directories = []

    tree = ""
    indent = "  " * depth  # Indentation for the tree structure

    try:
        items = sorted(os.listdir(directory))  # Sort for consistent output
    except PermissionError:
        return f"{indent}[Permission Denied]\n"

    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            # Skip ignored directories
            if item in ignored_directories:
                continue
            # Append the directory and recursively process its contents
            tree += f"{indent}- {item}/\n"
            tree += generate_file_tree(item_path, depth + 1, ignored_directories)
        else:
            # Append the file
            tree += f"{indent}- {item}\n"

    return tree

def write_file_tree_to_file(root_dir, output_file, ignored_directories=None):
    """Writes the directory tree to a file."""
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
    output_file = "file_tree.md"  # Output file name
    ignored_directories = [".git"]  # Directories to ignore
    write_file_tree_to_file(root_directory, output_file, ignored_directories)
