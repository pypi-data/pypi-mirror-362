#!/usr/bin/env python3
"""
Dynamic imports.
Largely inspired from a code made by Mike Rye.
"""

import importlib
import inspect
import logging
import pathlib
import sys
from collections import namedtuple

LOGGER = logging.getLogger(__name__)


ModuleInfo = namedtuple("ModuleInfo", ["name", "ispkg"])


def find_modules(search_path, base_package):
    """
    Find Python modules recursively and generate valid module names.

    Args:
        search_path (pathlib.Path): Path to search for modules
        base_package (str): Base package name for imports

    Returns:
        List[str]: List of fully qualified module names

    Raises:
        ImportError: If the search path doesn't exist or isn't a valid Python package
    """
    search_path = pathlib.Path(search_path).resolve()
    if not search_path.exists():
        raise ImportError(f"Module path not found: {search_path}")

    # Verify this is a valid Python package
    if not (search_path / "__init__.py").exists():
        raise ImportError(
            f"Not a valid Python package (missing __init__.py): {search_path}"
        )

    # Find the package root by looking for the first parent with __init__.py
    package_root = search_path
    while (
        package_root.parent.exists() and (package_root.parent / "__init__.py").exists()
    ):
        package_root = package_root.parent

    modules = []
    for file in search_path.rglob("*.py"):
        if file.name == "__init__.py":
            continue

        try:
            # Get the module path relative to the package root
            relative_path = file.relative_to(package_root)
            # Convert path parts to module name (e.g., path/to/module.py -> path.to.module)
            module_parts = list(relative_path.with_suffix("").parts)

            # Construct the full module name
            if base_package:
                module_parts.insert(0, base_package)

            module_name = ".".join(module_parts)
            modules.append(module_name)

        except ValueError as e:
            LOGGER.warning("Failed to compute module name for %s: %s", file, e)
            continue

    return modules


def import_types(suffix, base_class, submod="type"):
    """
    Import types from submodules dynamically.

    Args:
        suffix (str): Class name suffix to match (e.g., "Generator")
        base_class (type): Base class whose location will be used to find types
        submod (str): Subdirectory name to search in (default: "type")

    Yields:
        type: Classes that match the specified suffix and inherit from base_class

    Raises:
        ImportError: If the submodule path is not found or is not a valid Python package
    """
    base_path = pathlib.Path(inspect.getfile(base_class)).parent
    base_module = base_class.__module__.split(".")[0]  # Get root package name

    submod_path = (base_path / submod).resolve()
    if not submod_path.exists():
        raise ImportError(f"Submodule path not found: {submod_path}")

    LOGGER.debug(
        "Importing types from %s (resolved to %s)",
        submod,
        submod_path,
    )

    for module_name in find_modules(submod_path, base_module):
        try:
            LOGGER.debug("Importing %s", module_name)
            mod = importlib.import_module(module_name)

            for name, cls in inspect.getmembers(mod):
                if (
                    name.endswith(suffix)
                    and cls != base_class
                    and inspect.isclass(cls)
                    and issubclass(cls, base_class)
                ):
                    LOGGER.debug("Found %s", name)
                    yield cls

        except ImportError as e:
            LOGGER.warning("Failed to import %s: %s", module_name, e)


def reload_self():
    """
    Reload the calling module and update all references.

    Returns:
        Reloaded class object
    """
    stack = inspect.stack()
    prev_frame = stack[1]
    cls = prev_frame[0].f_locals["cls"]
    mod_name = cls.__module__

    mod = sys.modules[mod_name]
    LOGGER.debug("Reloading module: %s", mod)
    importlib.reload(mod)
    reloaded_cls = getattr(mod, cls.__name__)

    for frame in stack:
        for namespace in ("f_locals", "f_globals"):
            try:
                ns_vars = getattr(frame[0], namespace)
            except AttributeError:
                continue

            for key, val in list(ns_vars.items()):
                if val is cls:
                    ns_vars[key] = reloaded_cls

    return reloaded_cls
