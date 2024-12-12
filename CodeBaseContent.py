import os

def generate_directory_structure(root_dir, structure_output_file, code_output_file, ignore_paths=None, code_extensions=None):
    """
    Generate a tree-like directory structure of the given directory and write it to a file.
    Also write the content of code files to a separate file if they match the given extensions.
    
    :param root_dir: The root directory to scan.
    :param structure_output_file: The file to write the directory structure to.
    :param code_output_file: The file to write the code content to.
    :param ignore_paths: A list of directory and file paths to ignore, relative to the root directory.
    :param code_extensions: A list of code file extensions to include for writing their content.
    """
    if ignore_paths is None:
        ignore_paths = []

    if code_extensions is None:
        code_extensions = [".py", ".dart", ".java", ".js", ".html", ".css"]

    # Add .git to ignore paths by default
    ignore_paths.append(os.path.normpath(os.path.join(root_dir, '.git')))

    # Normalize the ignore paths relative to the root directory
    ignore_paths = [os.path.normpath(os.path.join(root_dir, path)) for path in ignore_paths]

    with open(structure_output_file, 'w') as structure_file, open(code_output_file, 'w') as code_file:
        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Check if any parent directory is in the ignore list
            if any(ignored_path in dirpath for ignored_path in ignore_paths):
                continue

            # Compute depth for proper indentation
            depth = dirpath.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * depth
            structure_file.write(f'{indent}{os.path.basename(dirpath)}/\n')
            subindent = ' ' * 4 * (depth + 1)

            # Filter and write files, ignoring specific files in the ignore list
            for filename in filenames:
                file_path = os.path.normpath(os.path.join(dirpath, filename))
                if not any(ignored_path in file_path for ignored_path in ignore_paths):
                    structure_file.write(f'{subindent}{filename}\n')
                    
                    # If the file is a code file, write its content to the code output file
                    if any(filename.endswith(ext) for ext in code_extensions):
                        # Compute the relative path from the root directory
                        relative_path = os.path.relpath(file_path, root_dir)
                        code_file.write(f"\n{relative_path}:\n")
                        try:
                            with open(file_path, 'r') as code_content:
                                code_file.write(code_content.read())
                        except Exception as e:
                            code_file.write(f"Error reading {relative_path}: {e}\n")

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

            # Ask the user for specific code file extensions to include
            code_extensions_input = input("Enter code file extensions to include (comma-separated, e.g., .py,.js,.html) or leave blank for default (.py,.dart,.java,.js,.html,.css): ")
            code_extensions = [ext.strip() for ext in code_extensions_input.split(",")] if code_extensions_input else None

            # Create the output file names based on the directory name
            structure_output_file = f"{directory_name}_structure.txt"
            code_output_file = f"{directory_name}_code_content.txt"

            # Generate the directory structure and save it to the file, ignoring specific paths and writing code content
            generate_directory_structure(root_directory, structure_output_file, code_output_file, ignore_paths=ignore_paths, code_extensions=code_extensions)

            # Get the absolute paths to the saved files
            structure_output_file_path = os.path.abspath(structure_output_file)
            code_output_file_path = os.path.abspath(code_output_file)

            print(f"Directory structure saved to: {structure_output_file_path}")
            print(f"Code content saved to: {code_output_file_path}")
