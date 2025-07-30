"""Test Component Builds."""

import sys
from collections.abc import Generator
from functools import cache

import pytest
import typer

from .cli.app import app

__all__ = ["do_test"]


@app.command(name="test")
def do_test() -> None:
    """Test if the cells in the project can be built."""
    from gdsfactoryplus.project import maybe_find_docode_project_dir

    project_dir = maybe_find_docode_project_dir()
    if project_dir is None:
        print(  # noqa: T201
            "Could not start tests. Please run tests inside a GDSFactory+ project.",
            file=sys.stderr,
        )
        raise typer.Exit(1)

    exit_code = pytest.main(["-s", __file__])
    if exit_code != 0:
        raise typer.Exit(exit_code)


@cache
def get_pdk():  # noqa: ANN202
    """Get the pdk."""
    from gdsfactoryplus.core.shared import activate_pdk_by_name
    from gdsfactoryplus.settings import get_settings

    return activate_pdk_by_name(get_settings().pdk.name)


def _iter_cells() -> Generator[str]:
    yield from get_pdk().cells


@pytest.mark.parametrize("cell_name", _iter_cells())
def test_build(cell_name: str) -> None:
    """Test if a cell can be built."""
    print(cell_name)  # noqa: T201
    func = get_pdk().cells[cell_name]
    func()
