import os

def generate_directory_structure(root_dir, output_file, ignore_paths=None):
    """
    Generate a tree-like directory structure of the given directory and write it to a file.
    :param root_dir: The root directory to scan.
    :param output_file: The file to write the directory structure to.
    :param ignore_paths: A list of directory and file paths to ignore, relative to the root directory.
    """
    if ignore_paths is None:
        ignore_paths = []

    # Add .git to ignore paths by default
    ignore_paths.append(os.path.normpath(os.path.join(root_dir, '.git')))

    # Normalize the ignore paths relative to the root directory
    ignore_paths = [os.path.normpath(os.path.join(root_dir, path)) for path in ignore_paths]

    with open(output_file, 'w') as f:
        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Check if any parent directory is in the ignore list
            if any(ignored_path in dirpath for ignored_path in ignore_paths):
                continue

            # Compute depth for proper indentation
            depth = dirpath.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * depth
            f.write(f'{indent}{os.path.basename(dirpath)}/\n')
            subindent = ' ' * 4 * (depth + 1)

            # Filter and write files, ignoring specific files in the ignore list
            for filename in filenames:
                file_path = os.path.normpath(os.path.join(dirpath, filename))
                if not any(ignored_path in file_path for ignored_path in ignore_paths):
                    f.write(f'{subindent}{filename}\n')

if __name__ == "__main__":
    while True:
        root_directory = input("Enter the root directory path (or type 'exit' to quit): ")

        # Allow the user to exit the program by typing "exit"
        if root_directory.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        # Check if the directory exists
        if not os.path.exists(root_directory) or not os.path.isdir(root_directory):
            print(f"Error: The directory '{root_directory}' does not exist. Please provide a valid absolute or relative path.")
        else:
            # Extract the directory name from the full path
            directory_name = os.path.basename(os.path.normpath(root_directory))

            # Ask the user for specific directories or files to ignore, relative to the root directory
            ignore_paths_input = input("Enter relative paths of directories/files to ignore (comma-separated, or leave blank to ignore none): ")
            ignore_paths = [p.strip() for p in ignore_paths_input.split(",")] if ignore_paths_input else []

            # Create the output file name based on the directory name
            output_file = f"{directory_name}_structure.txt"

            # Generate the directory structure and save it to the file, ignoring specific paths
            generate_directory_structure(root_directory, output_file, ignore_paths=ignore_paths)

            # Get the absolute path to the saved file
            output_file_path = os.path.abspath(output_file)

            print(f"Directory structure saved to: {output_file_path}")
