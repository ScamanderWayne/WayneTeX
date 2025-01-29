import os
import fitz  # PyMuPDF
from PIL import Image

# Function to list all PDFs in the repository
def list_pdfs(directory):
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("No PDFs found in the directory.")
        return []
    for i, pdf in enumerate(pdf_files):
        print(f"{i+1}. {pdf}")
    return pdf_files

# Function to convert a PDF page to PNG
def pdf_page_to_png(pdf_path, page_num, output_dir):
    pdf_doc = fitz.open(pdf_path)
    page = pdf_doc.load_page(page_num)  # Page number is 0-indexed
    pix = page.get_pixmap()  # Render page to image
    output_png = os.path.join(output_dir, f"page_{page_num+1}.png")
    pix.save(output_png)
    print(f"Saved page {page_num+1} as {output_png}")

# Main function to handle user inputs and print pages as PNGs
def main():
    current_dir = os.getcwd()
    pdf_files = list_pdfs(current_dir)
    
    if not pdf_files:
        return

    # Ask user for the PDF to select
    selected_pdf_idx = int(input("Select a PDF by number: ")) - 1
    selected_pdf = pdf_files[selected_pdf_idx]
    pdf_path = os.path.join(current_dir, selected_pdf)

    # Open the selected PDF and list its pages
    pdf_doc = fitz.open(pdf_path)
    total_pages = pdf_doc.page_count
    print(f"The PDF has {total_pages} pages.")
    
    # Ask user which pages to print
    page_numbers_input = input(f"Enter the page numbers to print (1-{total_pages}), separated by commas: ")
    page_numbers = [int(num.strip()) - 1 for num in page_numbers_input.split(',') if num.strip().isdigit()]
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Convert selected pages to PNG
    for page_num in page_numbers:
        if 0 <= page_num < total_pages:
            pdf_page_to_png(pdf_path, page_num, output_dir)
        else:
            print(f"Invalid page number: {page_num + 1}")

if __name__ == "__main__":
    main()
