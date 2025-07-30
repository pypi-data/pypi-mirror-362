import os
import shutil
from importlib import resources
from pathlib import Path


def copy_module_folder(module_name, folder_name, destination):
    """
    Copies the content of a folder within a Python module to a given destination.

    Args:
        module_name (str): The name of the module where the folder resides.
        folder_name (str): The name of the folder to copy.
        destination (str): The destination path where the folder's content should be copied.

    Raises:
        FileNotFoundError: If the specified folder in the module does not exist.
        Exception: If any error occurs during the copy operation.
    """
    try:
        # Resolve the folder path within the module
        with resources.path(module_name, folder_name) as folder_path:
            if not folder_path.is_dir():
                raise FileNotFoundError(f"The folder '{folder_name}' does not exist in module '{module_name}'.")
            
            # Use copytree to copy the entire directory
            shutil.copytree(folder_path, destination, dirs_exist_ok=True)
            
            # print(f"Successfully copied contents of '{folder_name}' from module '{module_name}' to '{destination}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def copy_module_file(module_name, file_name, destination):
    """
    Copies a single file from a Python module to a specified destination.

    Args:
        module_name (str): The name of the module where the file resides.
        file_name (str): The name of the file to copy.
        destination (str): The full path to the destination (including file name).

    Raises:
        FileNotFoundError: If the specified file in the module does not exist.
        Exception: If any error occurs during the copy operation.
    """
    try:
        # Resolve the file path within the module
        with resources.path(module_name, file_name) as file_path:
            if not file_path.is_file():
                raise FileNotFoundError(f"The file '{file_name}' does not exist in module '{module_name}'.")
            
            # Copy the file to the destination
            shutil.copy(file_path, destination)
            
            # print(f"Successfully copied '{file_name}' from module '{module_name}' to '{destination}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def clean_folder(folder_path, items_to_keep=None):
    """
    Removes all files and subdirectories from the specified folder except for the given items.

    Args:
        folder_path (str): Path to the folder to clean.
        items_to_keep (list, optional): List of file or subdirectory names to keep (relative to the folder).
                                        If None, the folder will be completely emptied.

    Raises:
        ValueError: If the folder_path does not exist or is not a directory.
    """
    if not os.path.exists(folder_path):
        raise ValueError(f"The folder '{folder_path}' does not exist.")
    if not os.path.isdir(folder_path):
        raise ValueError(f"The path '{folder_path}' is not a directory.")

    # Normalize the items to keep (absolute paths for comparison)
    keep_paths = {os.path.abspath(os.path.join(folder_path, item)) for item in items_to_keep}

    # Iterate over all items in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # If items_to_keep is None, delete everything
        # Otherwise, delete items not in the keep list
        if items_to_keep is None or os.path.abspath(item_path) not in keep_paths:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove file or symlink
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directory


def find_local_paths(paths):
    """
    Finds the local paths of files relative to the directory containing 'main.py' or 'main.js'.

    Args:
        paths (list of str): List of file paths as strings.

    Returns:
        dict: A dictionary mapping absolute file paths to their relative local paths.

    Raises:
        ValueError: If neither 'main.py' nor 'main.js' is found in the provided paths.
    """
    # Convert to Path objects
    path_objects = [Path(p) for p in paths]
    
    # Look for main.*
    main_path = None
    for candidate in ("main.py", "main.js"):
        main_path = next((p for p in path_objects if p.name == candidate), None)
        if main_path:
            break
    if main_path is None:
        raise ValueError("No main.* file was found in the provided paths.")
    
    # Determine main.py root directory
    main_root = main_path.parent
    
    # Compute local paths
    local_paths = {p: f"{p.relative_to(main_root)}" for p in path_objects if p != main_path and main_root in p.parents}
    
    return local_paths