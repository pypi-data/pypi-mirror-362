import inspect
import os
import sys
from importlib.metadata import distribution

def get_python_execution_info():
    """Return information about the Python interpreter executing this script"""
    return {
        "executable_path": sys.executable,
        "version": sys.version,
        "version_info": sys.version_info,
        "platform": sys.platform
    }

def get_class_info(cls):
    """Return detailed information about a class"""
    # Get the module where the class is defined
    module = inspect.getmodule(cls)
    module_name = module.__name__ if module else "built-in"

    # Try to get the source file
    try:
        source_file = inspect.getsourcefile(cls) or "built-in or compiled"
    except (TypeError, OSError):
        source_file = "built-in or compiled"

    # Try to get the installation package
    package_info = None
    if module_name and module_name != "builtins":
        try:
            dist = distribution(module_name.split('.')[0])
            package_info = {
                "package_name": dist.metadata["Name"],
                "version": dist.version,
                "install_location": dist.locate_file('').as_posix(),
                "install_source": "pip"  # Simplification - could be conda, etc.
            }
        except Exception:
            # If not installed via pip, try to find the file path
            try:
                if module and hasattr(module, '__file__'):
                    package_info = {
                        "package_name": module_name.split('.')[0],
                        "version": "N/A",
                        "install_location": os.path.dirname(module.__file__),
                        "install_source": "local_file"
                    }
            except Exception:
                pass # Could not determine package info

    methods = []
    attributes = []
    for name in dir(cls):
        if name.startswith('__'):
            continue
        obj = getattr(cls, name)
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            methods.append(name)
        else:
            attributes.append(name)

    return {
        "class_name": cls.__name__,
        "module": module_name,
        "source_file": source_file,
        "package_info": package_info,
        "methods": methods,
        "attributes": attributes
    }