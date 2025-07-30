"""Main module for the FusePyStarter CLI interface."""

import os
import subprocess

import fire
import toml  # type: ignore[import-untyped]
from cookiecutter import exceptions
from cookiecutter.main import cookiecutter
from distutils import spawn

from fusepystarter import __version__
from fusepystarter.decorators import logger


class Main:
    """Main CLI handler for FusePyStarter.

    Attributes:
        _version (str): The current version of the package.
    """

    _version: str

    @property
    def version(self) -> str:
        """Get the current version of the package.

        Returns:
            str: The current version string.
        """
        try:
            return self._version
        except AttributeError:
            self._version = __version__
            return self._version

    @staticmethod
    def _get_project_meta() -> dict:
        """Load project metadata from `pyproject.toml`.

        Returns:
            dict: Metadata defined under the `[project]` section.
        """
        return toml.load("pyproject.toml")["project"]

    @staticmethod
    def init() -> None:
        """Initialize a new project using FusePyStarter cookiecutter template.

        This function performs:
        - Git, Python3, and uv installation (if not found)
        - Project scaffolding using cookiecutter
        - Virtual environment creation using uv
        - Installation of project and dev dependencies
        - Pre-commit hook installation

        Returns:
            None:  This method doesn't return anything meaningful.
        """
        if not spawn.find_executable("git"):
            logger.warning("git not installed in your system")
            logger.info("Installing git...")
            subprocess.run(["sudo", "apt", "install", "-y", "git"])

        if not spawn.find_executable("python3"):
            logger.warning("python3 not installed in your system")
            logger.info("Installing python3...")
            subprocess.run(["sudo", "apt", "install", "-y", "python3"])

        if not spawn.find_executable("uv"):
            logger.warning("uv not found")
            logger.info("Installing uv via official install script...")
            subprocess.run(
                "curl -LsSf https://astral.sh/uv/install.sh | sh",
                shell=True,
                check=True,
            )

        while True:
            try:
                path = cookiecutter("gh:sunil-fm/FusePyStarter")
                os.chdir(path)

                subprocess.run(["git", "init"])

                logger.info("Creating virtual environment with uv...")
                subprocess.run(["uv", "venv", ".venv"])

                logger.info("Installing dependencies...")
                subprocess.run(["uv", "sync"])

                logger.info("Installing dev dependencies...")
                subprocess.run(["uv", "sync", "--dev"])

                logger.info("Installing pre-commit hooks...")
                subprocess.run([".venv/bin/python", "-m", "pre_commit", "install"])
                break

            except exceptions.OutputDirExistsException as e:
                logger.error(str(e))
                break
            except exceptions.RepositoryNotFound:
                logger.error("Download incomplete!")
            except exceptions.FailedHookException:
                logger.error("Please enter valid inputs")


def main() -> None:  #
    """Entry point for the FusePyStarter CLI.

    Returns:
        None: This method doesn't return anything meaningful.
    """
    fire.Fire(Main)
