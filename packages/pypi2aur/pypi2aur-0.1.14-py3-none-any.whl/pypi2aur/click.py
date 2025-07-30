import click
from pypi2aur.constants import APP_VERSION, APP_NAME
from pypi2aur.kernel import createPKGBUILD, readPyPiDeps, syncPKGBUILD
from rich.console import Console


"""
Module: click.py

This module provides a command-line interface (CLI) for the pypi2aur tool, which generates and manages
PKGBUILD files for Arch Linux's AUR (Arch User Repository) from PyPI packages. The CLI is built using
the `click` library and includes commands for creating PKGBUILD files, synchronizing them with PyPI,
and displaying package dependencies.
"""

cl = Console()


@click.group()
@click.version_option(
    version=APP_VERSION, prog_name=APP_NAME, message=f"{APP_NAME} v{APP_VERSION}"
)
def cli() -> None:
    """
    pypi2aur - PyPi to AUR PKGBUILD generator and helper.

    This function serves as the main entry point for the CLI. It initializes the CLI group and
    displays the program name and version on every invocation.
    """
    cl.print(
        f"[bold blue]{APP_NAME}[/bold blue] [bold green]{APP_VERSION}[/bold green]"
    )


@cli.command()
@click.argument("pkg", required=True)
def create(pkg: str) -> None:
    """
    Create a new PKGBUILD file for a PyPI package.

    Args:
        pkg (str): Name of the PyPI package for which to create a PKGBUILD.

    Returns:
        None: This function does not return anything but generates a PKGBUILD file.
    """
    createPKGBUILD(pypiPackage=pkg)


@cli.command()
def sync() -> None:
    """
    Synchronize the PKGBUILD with the latest information from PyPI.

    Returns:
        None: This function does not return anything but updates the PKGBUILD file.
    """
    syncPKGBUILD()


@cli.command()
@click.argument("pkg", required=True)
def showdeps(pkg: str) -> None:
    """
    Read and show PyPI package dependencies.

    Args:
        pkg (str): Name of the PyPI package to analyze dependencies for.

    Returns:
        None: This function does not return anything but prints the dependencies.
    """
    readPyPiDeps(pypipackage=pkg)
