import subprocess
import sys

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
        # "FourthScript.py", Replace with the path to your next script
    ]

    for script in scripts_to_run:
        run_script(script)

if __name__ == "__main__":
    main()
