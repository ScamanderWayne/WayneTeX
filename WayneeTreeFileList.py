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

    # Define colors for different file types (in HEX)
    pdf_color = "#FFB6C1"    # Light pinkish-red for .pdf files
    tex_color = "#ADD8E6"    # Light blue for .tex files
    cls_sty_color = "#32CD32"  # Lime green for .cls and .sty files
    
    # Define colors for directories based on depth (in HEX, cycling through dark colors)
    dir_colors = [
        "#9400D3",  # Dark violet (indigo)
        "#4B0082",  # Indigo
        "#0000FF",  # Blue
        "#00008B",  # Dark blue
        "#000080",  # Navy
        "#191970",  # Midnight blue
    ]

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
            label = "deeply-subdirectory"  # For any directory deeper than 3 levels

        # Set directory color based on depth (cycling through a set of dark colors)
        dir_color = dir_colors[depth % len(dir_colors)]

        if os.path.isdir(item_path):
            if item in ignored_directories:
                continue  # Skip ignored directories
            repo_url = f"{base_url_tree}/{item_relative_path}".replace("\\", "/")
            tree += f'{indent}- <a href="{repo_url}" style="color:{dir_color}">{item}/ {label}</a>\n'
            tree += generate_file_tree_markdown(
                item_path, base_url_tree, base_url_blob, item_relative_path, depth + 1, ignored_directories, ignored_file_extensions, ignored_files
            )
        else:
            # Skip ignored file types or specific files
            if any(item.endswith(ext) for ext in ignored_file_extensions) or item in ignored_files:
                continue

            # Handle .pdf, .tex, .cls, .sty files with specific link format
            if item.endswith(".pdf"):
                file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
                file_name = os.path.splitext(item)[0]  # Get file name without extension
                tree += f'{indent}- <a href="{file_url}" style="color:{pdf_color}">{file_name} PDF file</a>\n'
            elif item.endswith(".tex"):
                file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
                file_name = os.path.splitext(item)[0]  # Get file name without extension
                tree += f'{indent}- <a href="{file_url}" style="color:{tex_color}">{file_name} raw TeX file</a>\n'
            elif item.endswith(".cls") or item.endswith(".sty"):
                file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
                file_name = os.path.splitext(item)[0]  # Get file name without extension
                tree += f'{indent}- <a href="{file_url}" style="color:{cls_sty_color}">{file_name} LaTeX Class file</a>\n'
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
            f.write("This repository contains my LaTeX notes and projects. Mostly for my own reference, but I am a big fan of open source, so feel free to use it as you wish. (With credits of course.)\n\n")
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
