import os

def generate_file_tree_markdown(directory, base_url_tree, base_url_blob, relative_path="", depth=0, ignored_directories=None, ignored_file_extensions=None, ignored_files=None):
    """Recursively generates a GitHub-flavored Markdown file tree with labeled directories and custom file links."""
    if ignored_directories is None:
        ignored_directories = []
    if ignored_file_extensions is None:
        ignored_file_extensions = []
    if ignored_files is None:
        ignored_files = []

    tree = ""
    indent = "  " * depth  # Indentation for tree structure

    try:
        items = sorted(os.listdir(directory))  # Sort items for consistent output
    except PermissionError:
        return f"{indent}- [Permission Denied]\n"

    for item in items:
        item_path = os.path.join(directory, item)
        item_relative_path = os.path.join(relative_path, item)

        # Define labels for depth-based directories
        if depth == 0:
            label = "directory"
        elif depth == 1:
            label = "subdirectory"
        elif depth == 2:
            label = "subsubdirectory"
        elif depth == 3:
            label = "subsubsubdirectory"
        else:
            label = "subsubsubsubdirectory"

        if os.path.isdir(item_path):
            if item in ignored_directories:
                continue  # Skip ignored directories
            repo_url = f"{base_url_tree}/{item_relative_path}".replace("\\", "/")
            tree += f"{indent}- <a href=\"{repo_url}\">{item}/ {label}</a>\n"
            tree += generate_file_tree_markdown(
                item_path, base_url_tree, base_url_blob, item_relative_path, depth + 1, ignored_directories, ignored_file_extensions, ignored_files
            )
        else:
            # Skip ignored file types or specific files
            if any(item.endswith(ext) for ext in ignored_file_extensions) or item in ignored_files:
                continue
            # Handle .pdf and .tex files with specific link format
            if item.endswith(".pdf"):
                file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
                file_name = os.path.splitext(item)[0]  # Get file name without extension
                tree += f"{indent}- <a href=\"{file_url}\">{file_name} PDF file</a>\n"
            elif item.endswith(".tex"):
                file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
                file_name = os.path.splitext(item)[0]  # Get file name without extension
                tree += f"{indent}- <a href=\"{file_url}\">{file_name} raw TeX file</a>\n"
            else:
                tree += f"{indent}- {item}\n"

    return tree

def write_file_tree_to_readme(root_dir, output_file, base_url_tree, base_url_blob, ignored_directories=None, ignored_file_extensions=None, ignored_files=None):
    """Writes the directory tree to a Markdown-formatted README file."""
    try:
        tree = generate_file_tree_markdown(
            root_dir, base_url_tree, base_url_blob, ignored_directories=ignored_directories, ignored_file_extensions=ignored_file_extensions, ignored_files=ignored_files
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Description\n\n")
            f.write("This repository contains my LaTeX notes and projects. Mostly for my own reference, but I am big fan of open source, so feel free to use it as you wish. (With credit of course.)\n\n")
            f.write("## Additional Resources\n\n")
            f.write('<a href="https://latex.net/texlive/">Compile LaTeX files online</a>\n\n')
            f.write("### Project Directory Tree\n\n")
            f.write(tree)
        print(f"File tree written to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    root_directory = "."  # Change to the directory you want to scan
    output_file = "README.md"  # Output file name
    github_base_url_tree = "https://github.com/ScamanderWayne/WayneTeX/tree/main"  # Base URL for directories
    github_base_url_blob = "https://github.com/ScamanderWayne/WayneTeX/blob/main"  # Base URL for files
    ignored_directories = [".git"]  # Directories to ignore
    ignored_file_extensions = [
        ".aux", ".fdb_latexmk", ".fls", ".log", ".synctex.gz", ".py", ".out", ".bib", ".run.xml", ".bbl", ".blg", ".md", ".txt", ".png", ".jpg"
    ]  # File types to ignore
    ignored_files = [".gitattributes", ".gitignore"]  # Specific files to ignore
    write_file_tree_to_readme(
        root_directory, output_file, github_base_url_tree, github_base_url_blob, ignored_directories, ignored_file_extensions, ignored_files
    )

# this file was generated fully by ChatGPT on 2024-11-24 and I claim no ownership over it. Just mere changes after it was generated.