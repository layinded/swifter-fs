import importlib
import os  # Import os to use os.path.sep
from pathlib import Path


def dynamic_import(directory: str, package: str):
    """
    Dynamically imports all modules in a given directory, including subfolders.

    :param directory: The directory containing modules to import.
    :param package: The base package name (e.g., 'custom' or 'backend.custom').
    :return: A dictionary of imported modules {module_name: module}
    """
    imported_modules = {}
    directory_path = Path(directory)

    if not directory_path.exists():
        return imported_modules

    for path in directory_path.rglob("*.py"):
        if path.name.startswith("__") or not path.is_file():
            continue

        # Convert path to a dotted module path (compatible with importlib)
        relative_path = path.relative_to(directory_path).with_suffix("")
        module_name = f"{package}.{str(relative_path).replace(os.path.sep, '.')}"

        try:
            module = importlib.import_module(module_name)
            imported_modules[module_name] = module
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")

    return imported_modules
