import os

def print_directory(path, prefix=''):
    # Check the depth from the prefix, each "--" represents a level deeper
    if prefix.count('--') >= 2:
        return
    try:
        entries = os.listdir(path)
    except PermissionError:
        print(f"{prefix}{os.path.basename(path)}/ [Permission Denied]")
        return

    entries = sorted(entries)  # Sort to maintain consistent order
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    files = [entry for entry in entries if os.path.isfile(os.path.join(path, entry))]

    # Print directories first
    for directory in directories:
        print(f"{prefix}{directory}/")
        print_directory(os.path.join(path, directory), prefix + '--')

    # Then print files
    for file in files:
        print(f"{prefix}- {file}")

# Change '/path/to/your/wails/app' to the path of your Wails app directory
print_directory('c:\\Users\\alibi\\WayneTeX')