FusePyStarter
=============

FusePyStarteris a modern project template designed to simplify the initial setup of Python projects by providing a solid foundation with best practices built in from day one. It helps you avoid common setup pitfalls and enforces consistency so you can focus on what matters: writing great code.

Why FusePyStarter?
------------------

- **Consistency:** Includes EditorConfig and Ruff to maintain uniform code style and linting across your team.
- **Safety:** Integrates MyPy for static type checking to catch bugs early.
- **Automation:** Pre-configured pre-commit hooks automate code quality checks.
- **Productivity:** Environment management and logging setup included for scalable projects.
- **Quality:** Built-in testing and code coverage ensure reliability and maintainability.

With PyFoundry, starting your Python project is no longer a hurdle but a streamlined experience that scales from simple scripts to complex AI engineering workflows.

Repository Links
-------------------

- **Source Code**: https://github.com/sunil-fm/FusePyStarter.git
- **Issue Tracker**: https://github.com/sunil-fm/FusePyStarter/issues

Contents
-----------

Project Initialization
~~~~~~~~~~~~~~~~~~~~~~

The project is configured with tools that promote consistency and maintainability from the beginning:

- `editorconfig`_ — Ensures consistent indentation, line endings, and formatting across different editors.
- `ruff`_ — Ultra-fast linter and formatter for Python.
- `mypy`_ — Static type checker for Python.
- `pre-commit`_ — Framework for managing and maintaining multi-language pre-commit hooks.

Project Setup
~~~~~~~~~~~~~

The core project setup integrates tools for configuration, CLI handling, testing, and automation:

- `dynaconf`_ — Flexible configuration management.
- `fire`_ — CLI generation from Python code.
- `logging`_ — Built-in logging configuration for visibility and debugging.
- `pytest`_ — Simple yet powerful test framework.
- `coverage`_ — Monitors code coverage during test execution.
- `pytest-cov`_ — Plugin for integrating coverage with pytest.
- `tox`_ — Automates testing across multiple Python environments.

Project deployment
~~~~~~~~~~~~~~~~~~

Build docs with Sphinx, automate with GitHub Actions, and publish on GitHub Pages.

- `sphinx`_ — For generating structured project documentation.
- `gh-actions`_ — To automate documentation builds and deployment on every push or pull request, using a CI/CD pipeline.
- `gh-pages`_ — Deploy documentation or project pages directly from the main branch using Sphinx.
- `pypi-release`_ — Prepare to publish the package to PyPI.

Getting Started with uv
----------------------------

1. **Clone the repository**

   .. code-block:: bash

      git clone https://github.com/sunil-fm/FusePyStarter.git
      cd FusePyStarter

2. **Create a virtual environment**

   .. code-block:: bash

      uv venv .venv
      source .venv/bin/activate

3. **Install project dependencies**

   .. code-block:: bash

      uv sync

Environment Examples
--------------------

Sample `.env.example` file for Dynaconf environment:

.. code-block:: ini

   ENV_FOR_DYNACONF=dev
   DYNACONF_APP_NAME=FusePyStarter

Sample `.secrets.example` file:

.. code-block:: ini

   [default]
   access_key = "my_access_key"
   secret_key = "my_secret_key"
   db_user_name = "username"
   db_password = "password"

   [dev]
   access_key = "my_access_key-dev"
   secret_key = "my_secret_key-dev"
   db_user_name = "username-dev"
   db_password = "password-dev"

   [stage]
   access_key = "my_access_key-stg"
   secret_key = "my_secret_key-stg"
   db_user_name = "username-stg"
   db_password = "password-stg"

   [prod]
   access_key = "my_access_key-prod"
   secret_key = "my_secret_key-prod"
   db_user_name = "username-prod"
   db_password = "password-prod"

.. note::

   Replace ``.env.examples`` with ``.env`` to configure your working environment, and replace
   ``.secrets.examples.toml`` with ``.secrets.toml`` to store your actual secret values.

   Make sure to exclude ``.secrets.toml`` from version control to keep your secrets secure.

Coming Soon
--------------

Planned future integrations:

- **Github Issue Template** — Report issue and suggestion template.

Contribute or Follow Along
-----------------------------

FusePyStarter is evolving. Star the repository, follow development, or contribute by submitting issues and pull requests!

.. _editorconfig: https://sunil-fm.github.io/FusePyStarter/initialization/editorconfig.html
.. _ruff: https://sunil-fm.github.io/FusePyStarter/initialization/ruff.html
.. _mypy: https://sunil-fm.github.io/FusePyStarter/initialization/mypy.html
.. _pre-commit: https://sunil-fm.github.io/FusePyStarter/initialization/pre-commit.html
.. _dynaconf: https://sunil-fm.github.io/FusePyStarter/setup/dynaconf.html
.. _fire: https://sunil-fm.github.io/FusePyStarter/setup/fire.html
.. _logging: https://sunil-fm.github.io/FusePyStarter/setup/logging.html
.. _pytest: https://sunil-fm.github.io/FusePyStarter/setup/pytest.html
.. _coverage: https://ghimiresunil.github.io/PyFoundry/setup/coverage.html
.. _pytest-cov: https://sunil-fm.github.io/FusePyStarter/setup/pytest-cov.html
.. _tox: https://sunil-fm.github.io/FusePyStarter/setup/tox.html
.. _sphinx: https://sunil-fm.github.io/FusePyStarter/deployment/sphinx.html
.. _gh-actions: https://sunil-fm.github.io/FusePyStarter/deployment/gh-actions.html
.. _gh-pages: https://sunil-fm.github.io/FusePyStarter/deployment/gh-pages.html
.. _pypi-release: https://sunil-fm.github.io/FusePyStarter/deployment/pypi-release.html
