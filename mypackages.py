import os
import shutil
import platform

# Define the directory to search
directory = "MyPackages"

# Determine the target directory based on the OS
if platform.system() == "Windows":
    target_directory = r"C:\Users\alibi\texmf\tex\latex\waynepackages"
else:
    target_directory = os.path.expanduser("~/texmf/tex/latex/waynepackages")

# Create the target directory if it doesn't exist
os.makedirs(target_directory, exist_ok=True)

# List to hold the found files
cls_files = []
sty_files = []

# List to hold failed copies
failed_files = []

# Function to extract the description after %about:
def extract_about_description(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip().startswith("%about:"):
                    # Return the description following %about:
                    return line.strip().replace("%about:", "").strip()
    except Exception as e:
        return f"Error reading file: {e}"

# Walk through the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        # Check if the file ends with .cls or .sty
        if file.endswith('.cls'):
            file_path = os.path.join(root, file)
            cls_files.append(file_path)
        elif file.endswith('.sty'):
            file_path = os.path.join(root, file)
            sty_files.append(file_path)

# Copy the found files to the target directory and gather about descriptions
cls_descriptions = {}
sty_descriptions = {}

for cls_file in cls_files:
    try:
        shutil.copy(cls_file, target_directory)
        print(f"Copied {cls_file} to {target_directory}")
        cls_descriptions[cls_file] = extract_about_description(cls_file)
    except Exception as e:
        failed_files.append(f"{cls_file} - {str(e)}")

for sty_file in sty_files:
    try:
        shutil.copy(sty_file, target_directory)
        print(f"Copied {sty_file} to {target_directory}")
        sty_descriptions[sty_file] = extract_about_description(sty_file)
    except Exception as e:
        failed_files.append(f"{sty_file} - {str(e)}")

# If there are any failed copies, log them in failtocopy.txt
if failed_files:
    failtocopy_path = os.path.join(os.getcwd(), "failtocopy.txt")
    with open(failtocopy_path, "w") as fail_file:
        for failed in failed_files:
            fail_file.write(f"{failed}\n")
    print(f"Failed to copy some files. See {failtocopy_path} for details.")

# Create a README.md file listing the found .cls and .sty files and their descriptions
readme_path = os.path.join(directory, "README.md")
with open(readme_path, "w") as readme_file:
    readme_file.write("# List of .cls and .sty Files\n\n")
    
    readme_file.write("## .cls Files:\n")
    for cls_file in cls_files:
        description = cls_descriptions.get(cls_file, "No description available.")
        readme_file.write(f"- {os.path.relpath(cls_file, directory)}  -- {description}\n")
    
    readme_file.write("\n## .sty Files:\n")
    for sty_file in sty_files:
        description = sty_descriptions.get(sty_file, "No description available.")
        readme_file.write(f"- {os.path.relpath(sty_file, directory)}  -- {description}\n")

print(f"README.md has been created in {directory}")