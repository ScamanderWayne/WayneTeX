import os

def generate_pdf_list(directory, base_url_blob, relative_path=""):
    """Generates a list of PDF files with links."""
    pdf_files = []
    try:
        items = sorted(os.listdir(directory))  # Sort items for consistent output
    except PermissionError:
        return []

    for item in items:
        item_path = os.path.join(directory, item)
        item_relative_path = os.path.join(relative_path, item)

        if os.path.isdir(item_path):
            # Recursively call for subdirectories
            pdf_files.extend(generate_pdf_list(item_path, base_url_blob, item_relative_path))
        elif item.endswith(".pdf"):
            file_url = f"{base_url_blob}/{item_relative_path}".replace("\\", "/")
            file_name = os.path.splitext(item)[0]  # Get file name without extension
            pdf_files.append(f"[{file_name} PDF file]({file_url})")
    
    return pdf_files

def write_pdf_list_to_file(root_dir, output_file, base_url_blob):
    """Writes the list of PDF files with links to an output file."""
    try:
        pdf_files = generate_pdf_list(root_dir, base_url_blob)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("## List of PDF Files\n\n")
            for pdf in pdf_files:
                f.write(f"{pdf}\n")
        print(f"PDF list written to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    root_directory = "."  # Change to the directory you want to scan
    output_file = "pdf_list.md"  # Output file name
    github_base_url_blob = "https://github.com/ScamanderWayne/WayneTeX/blob/main"  # Replace with your GitHub base URL
    write_pdf_list_to_file(root_directory, output_file, github_base_url_blob)
