"""Main module for the cookiecutter package."""

import os
import subprocess

import fire
import toml
from distutils import spawn

from cookiecutter import exceptions
from cookiecutter.main import cookiecutter
from src.decorators import logger


class Main:
    @property
    def version(self):
        try:
            return self._version
        except AttributeError:
            self._version = self._get_project_meta()["version"]
            return self._version

    @staticmethod
    def _get_project_meta():
        return toml.load("pyproject.toml")["project"]

    @staticmethod
    def init():
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
                subprocess.run(["uv", "venv", ".venv"], check=True)

                logger.info("Installing dependencies...")
                subprocess.run(["uv", "sync"], check=True)

                logger.info("Installing pre-commit hooks...")
                subprocess.run(
                    [".venv/bin/python", "-m", "pre_commit", "install"], check=True
                )
                break

            except exceptions.RepositoryNotFound:
                logger.error("Download incomplete!")
            except exceptions.FailedHookException:
                logger.error("Please enter valid inputs")
            except exceptions.OutputDirExistsException as e:
                logger.error(str(e))
                break


def main():
    fire.Fire(Main)
