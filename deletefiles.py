import os
import glob

def delete_files():
    filetypes_delete = [".aux",".fdb_latexmk",".fls",".log",".synctex.gz",".out",".run.xml",".bbl",".blg"]  # files to delete
    directory = os.getcwd()
    files_to_delete = []
    
    for filetype in filetypes_delete:
        files_to_delete.extend(glob.glob(f"{directory}/**/*{filetype}", recursive=True))
    
    if not files_to_delete:
        print("No matching files found.")
        return
    
    print("The following files will be deleted:")
    for file in files_to_delete:
        print(file)
    
    confirm = input("Do you want to proceed with deletion? (yes/no): ").strip().lower()
    if confirm == "yes":
        for file in files_to_delete:
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
    else:
        print("Deletion aborted.")

if __name__ == "__main__":
    delete_files()
