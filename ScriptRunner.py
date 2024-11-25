import subprocess
import sys
import os

def run_script(script_name):
    """Function to run a Python script using subprocess."""
    try:
        print(f"Running script: {script_name}")
        result = subprocess.run([sys.executable, script_name], check=True, text=True, capture_output=True)
        print(f"Output from {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred while running {script_name}: {e}")

def main():
    scripts_to_run = [
        "TreeFileListToREADME.py",
        "PDFlist.py",
        "AllFilesList.py",
        "mypackages.py",
        os.path.join("MyPackages", "sourcecontrol.py"),  # Add sourcecontrol.py
    ]

    for script in scripts_to_run:
        if os.path.exists(script):  # Check if the script exists
            run_script(script)
        else:
            print(f"Script not found: {script}")

if __name__ == "__main__":
    main()
