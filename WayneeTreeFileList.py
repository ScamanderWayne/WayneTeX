import os

def generate_file_tree_markdown(directory, base_url_blob, parent_path="", ignored_directories=None, ignored_file_extensions=None, ignored_files=None):
    """
    Recursively generates a GitHub-flavored Markdown file tree with reset numbering for each directory.
    Excludes directories containing no valid files.
    """
    if ignored_directories is None:
        ignored_directories = []
    if ignored_file_extensions is None:
        ignored_file_extensions = []
    if ignored_files is None:
        ignored_files = []

    sub_tree = ""
    found_files = []  # List to store actual files in the current directory
    file_counter = 0  # Reset counter for each directory

    try:
        items = sorted(os.listdir(directory))  # Sort items for consistent output
    except PermissionError:
        return "- [Permission Denied]\n"

    for item in items:
        item_path = os.path.join(directory, item)
        current_path = os.path.join(parent_path, item).replace("\\", "/")  # Create full relative path

        if os.path.isdir(item_path):
            # Skip ignored directories
            if item in ignored_directories:
                continue

            # Recursively process subdirectories
            child_tree = generate_file_tree_markdown(
                item_path, base_url_blob, current_path, ignored_directories, ignored_file_extensions, ignored_files
            )

            # Include only if the subdirectory has files
            if child_tree.strip():
                sub_tree += child_tree
        else:
            # Check file conditions
            if any(item.endswith(ext) for ext in ignored_file_extensions) or item in ignored_files:
                continue

            # Increment local counter for this directory and add the file
            file_counter += 1

            file_url = f"{base_url_blob}/{current_path}".replace("\\", "/")
            file_name = os.path.splitext(item)[0]  # Get file name without extension

            if item.endswith(".pdf"):
                found_files.append(f'  {file_counter}. <a href="{file_url}">{file_name} PDF file</a>\n')
            elif item.endswith(".tex"):
                found_files.append(f'  {file_counter}. <a href="{file_url}">{file_name} raw TeX file</a>\n')
            else:
                found_files.append(f'  {file_counter}. <a href="{file_url}">{file_name} file</a>\n')

    # Include the directory only if it has files or valid subdirectories
    if found_files or sub_tree.strip():
        directory_header = f'- {parent_path}/\n' if parent_path else ""
        return directory_header + "".join(found_files) + sub_tree

    return ""  # Return empty if the directory has no files or subdirectories with files

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
        ".aux", ".fdb_latexmk", ".fls", ".log", ".synctex.gz", ".py", ".out", ".bib", ".run.xml", ".bbl", ".blg", ".md", ".txt", ".png", ".jpg"
    ]  # File types to ignore
    ignored_files = [".gitattributes", ".gitignore"]  # Specific files to ignore
    write_file_tree_to_readme(
        root_directory, output_file, github_base_url_blob, ignored_directories, ignored_file_extensions, ignored_files
    )
