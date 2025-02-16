import importlib
from pathlib import Path


def dynamic_import(directory: str, package: str):
    """
    Dynamically imports all modules in a given directory.

    :param directory: The directory containing modules to import.
    :param package: The base package name (e.g., 'custom' or 'backend.custom').
    :return: A dictionary of imported modules {module_name: module}
    """
    imported_modules = {}
    directory_path = Path(directory)

    if not directory_path.exists():
        return imported_modules

    for file in directory_path.glob("*.py"):
        if file.name.startswith("__") or not file.is_file():
            continue

        module_name = f"{package}.{file.stem}"
        try:
            module = importlib.import_module(module_name)
            imported_modules[file.stem] = module
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")

    return imported_modules
