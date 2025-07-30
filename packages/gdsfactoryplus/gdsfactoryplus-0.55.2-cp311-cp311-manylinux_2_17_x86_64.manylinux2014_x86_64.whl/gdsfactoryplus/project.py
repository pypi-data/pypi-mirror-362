"""Find the GDSFactory+ project folder."""

import os


def maybe_find_docode_project_dir() -> str | None:
    """Find the GDSFactory+ project folder, return None if not found."""
    try:
        return find_docode_project_dir()
    except FileNotFoundError:
        return None


def find_docode_project_dir() -> str:
    """Find the GDSFactory+ project folder, raise FileNotFoundErorr if not found."""
    maybe_pyproject = os.path.join(os.path.abspath("."), "pyproject.toml")
    while not os.path.isfile(maybe_pyproject):
        prev_pyproject = maybe_pyproject
        maybe_pyproject = os.path.join(
            os.path.dirname(os.path.dirname(maybe_pyproject)), "pyproject.toml"
        )
        if prev_pyproject == maybe_pyproject:
            break
    if os.path.isfile(maybe_pyproject):
        return os.path.dirname(maybe_pyproject)
    msg = "No project dir found."
    raise FileNotFoundError(msg)
