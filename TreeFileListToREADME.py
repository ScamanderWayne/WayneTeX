import os

def generate_file_tree_markdown(directory, base_url_blob, relative_path="", depth=0, ignored_directories=None, ignored_file_extensions=None, ignored_files=None):
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

    pdf_counter = 1
    tex_counter = 2
    other_files_counter = 3  # Reset for each directory

    pdf_files = []
    tex_files = []
    bib_cls_sty_files = []
    other_files = []

    # Separate files into categories
    for item in items:
        item_path = os.path.join(directory, item)
        item_relative_path = os.path.join(relative_path, item)

        if os.path.isdir(item_path):
            if item in ignored_directories:
                continue  # Skip ignored directories
            tree += f'{indent}- {item}/\n'
            tree += generate_file_tree_markdown(
                item_path, base_url_blob, item_relative_path, depth + 1, ignored_directories, ignored_file_extensions, ignored_files
            )
        else:
            # Skip ignored file types or specific files
            if any(item.endswith(ext) for ext in ignored_file_extensions) or item in ignored_files:
                continue

            # Categorize files by type
            if item.endswith(".pdf"):
                pdf_files.append(item)
            elif item.endswith(".tex"):
                tex_files.append(item)
            elif item.endswith(".bib"):
                bib_cls_sty_files.append(item)
            elif item.endswith(".cls") or item.endswith(".sty"):
                bib_cls_sty_files.append(item)
            elif item.endswith(".pgf"):
                bib_cls_sty_files.append(item)
            elif item.endswith(".tikz"):
                bib_cls_sty_files.append(item)
            else:
                other_files.append(item)

    # Process and add files in the correct order with custom names
    for item in pdf_files:
        item_relative_path = os.path.join(relative_path, item)
        file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
        file_name = os.path.splitext(item)[0]  # Get file name without extension
        tree += f'{indent} 1. <a href="{file_url}">{file_name} PDF file</a>\n'
        pdf_counter += 1

    for item in tex_files:
        item_relative_path = os.path.join(relative_path, item)
        file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
        file_name = os.path.splitext(item)[0]  # Get file name without extension
        tree += f'{indent} 2. <a href="{file_url}">{file_name} raw TeX file</a>\n'
        tex_counter += 1

    for item in bib_cls_sty_files:
        item_relative_path = os.path.join(relative_path, item)
        file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
        file_name = os.path.splitext(item)[0]  # Get file name without extension
        
        # Custom naming for LaTeX-specific files
        if item.endswith(".bib"):
            tree += f'{indent} {other_files_counter}. <a href="{file_url}">{file_name} TeX Bibliography file</a>\n'
        elif item.endswith(".cls"):
            tree += f'{indent} {other_files_counter}. <a href="{file_url}">{file_name} TeX Class file</a>\n'
        elif item.endswith(".sty"):
            tree += f'{indent} {other_files_counter}. <a href="{file_url}">{file_name} TeX Style file</a>\n'
        elif item.endswith(".pgf"):
            tree += f'{indent} {other_files_counter}. <a href="{file_url}">{file_name} TeX Graphics (PGF) file</a>\n'
        elif item.endswith(".tikz"):
            tree += f'{indent} {other_files_counter}. <a href="{file_url}">{file_name} TeX Diagrams (TikZ) file</a>\n'
        
        other_files_counter += 1

    for item in other_files:
        item_relative_path = os.path.join(relative_path, item)
        file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
        file_name = os.path.splitext(item)[0]  # Get file name without extension
        file_extension = item.split('.')[-1]  # Get file extension without the dot
        tree += f'{indent} {other_files_counter}. <a href="{file_url}">{file_name} {file_extension} file</a>\n'
        other_files_counter += 1

    return tree

def write_file_tree_to_readme(root_dir, output_file, base_url_blob, ignored_directories=None, ignored_file_extensions=None, ignored_files=None):
    """Writes the directory tree to a Markdown-formatted README file."""
    try:
        tree = generate_file_tree_markdown(
            root_dir, base_url_blob, ignored_directories=ignored_directories, ignored_file_extensions=ignored_file_extensions, ignored_files=ignored_files
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("## Description\n\n")
            f.write("This repository contains my LaTeX notes and projects. Mostly for my own reference, but I am a big fan of open source, so feel free to use it as you wish. (With credits of course.)\n\n")
            f.write("## Additional Resources\n\n")
            f.write('<a href="https://latex.net/texlive/">Compile LaTeX files online</a>\n\n')
            f.write("## Project Directory Tree\n\n")
            f.write(tree)
        print(f"File tree written to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    root_directory = "."  # Change to the directory you want to scan
    output_file = "README.md"  # Output file name
    github_base_url_blob = "https://github.com/ScamanderWayne/WayneTeX/blob/main"  # Base URL for files
    ignored_directories = [".git"]  # Directories to ignore
    ignored_file_extensions = [
        ".aux", ".fdb_latexmk", ".fls", ".log", ".synctex.gz", ".py", ".out", ".run.xml", ".bbl", ".blg", ".md", ".txt", ".png", ".jpg"
    ]  # File types to ignore
    ignored_files = [".gitattributes", ".gitignore"]  # Specific files to ignore
    write_file_tree_to_readme(
        root_directory, output_file, github_base_url_blob, ignored_directories, ignored_file_extensions, ignored_files
    )