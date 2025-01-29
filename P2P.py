import os
import fitz  # PyMuPDF
from PIL import Image

def convert_pdf_to_png(pdf_path, output_png_path, output_straight_png_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    total_pages = doc.page_count
    # Determine grid size
    grid_width = 5  # Fixed number of columns
    grid_height = (total_pages + grid_width - 1) // grid_width  # Rounded up rows
    if grid_height > 5:  # If there are more than 5 rows, switch to wider layout
        grid_height = 5
        grid_width = (total_pages + grid_height - 1) // grid_height  # Calculate new columns

    # Create an empty blank image with the appropriate size
    page_width, page_height = doc[0].rect.width, doc[0].rect.height
    img_width = int(grid_width * page_width)  # Ensure it's an integer
    img_height = int(grid_height * page_height)  # Ensure it's an integer
    result_image = Image.new("RGBA", (img_width, img_height), (255, 255, 255, 0))  # transparent background
    
    # Create the straight PNG output (stacking vertically)
    straight_img_height = int(total_pages * page_height)  # Ensure it's an integer
    straight_image = Image.new("RGBA", (int(page_width), straight_img_height), (255, 255, 255, 0))  # transparent background
    
    # Iterate through each page and paste it into the correct position on both result images
    for i in range(total_pages):
        page = doc.load_page(i)  # Get the i-th page
        pix = page.get_pixmap()  # Render page to pixmap (image)
        
        row = i // grid_width
        col = i % grid_width
        x_offset = int(col * page_width)
        y_offset = int(row * page_height)
        
        # Create the page image and paste it on the result grid image
        page_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        result_image.paste(page_img, (x_offset, y_offset))

        # Stack the pages vertically in straight image (ensure y_offset is an integer)
        straight_y_offset = int(i * page_height)  # Explicitly cast to integer
        straight_image.paste(page_img, (0, straight_y_offset))

    # Save the final result as PNG (grid layout)
    result_image.save(output_png_path)
    
    # Save the straight output as PNG (stacked vertically)
    straight_image.save(output_straight_png_path)

def scan_pdf_files(directory):
    # Scan the directory and subdirectories for PDF files
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def main():
    # Get the current working directory
    directory = os.getcwd()
    
    # Scan for PDF files
    pdf_files = scan_pdf_files(directory)
    
    # If no PDF files were found, exit
    if not pdf_files:
        print("No PDF files found in the repository.")
        return
    
    # Display the list of PDF files
    print("Please select a PDF file to convert to PNG:")
    for idx, pdf_file in enumerate(pdf_files, start=1):
        print(f"{idx}. {pdf_file}")
    
    # Ask the user to select a PDF file by number
    choice = int(input(f"Enter a number (1-{len(pdf_files)}): "))
    
    if choice < 1 or choice > len(pdf_files):
        print("Invalid selection.")
        return
    
    # Get the selected PDF file and output paths
    selected_pdf = pdf_files[choice - 1]
    base_name = os.path.splitext(os.path.basename(selected_pdf))[0]
    output_png = f"{base_name}.png"
    output_straight_png = f"{base_name}-straight.png"
    
    # Convert the selected PDF to PNG (both grid and straight)
    convert_pdf_to_png(selected_pdf, output_png, output_straight_png)
    print(f"PNG file saved as {output_png}")
    print(f"Straight PNG file saved as {output_straight_png}")

if __name__ == "__main__":
    main()
