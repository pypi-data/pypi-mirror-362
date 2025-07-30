FusePyStarter
=============

**FusePyStarter** is a modern project template designed to simplify the initial setup of Python projects by providing a solid foundation with best practices built in from day one. It helps you avoid common setup pitfalls and enforces consistency so you can focus on what matters: writing great code.

Why FusePyStarter?
------------------

- **Consistency:** Includes EditorConfig and Ruff to maintain uniform code style and linting across your team.
- **Safety:** Integrates MyPy for static type checking to catch bugs early.
- **Automation:** Pre-configured pre-commit hooks automate code quality checks.
- **Productivity:** Environment management and logging setup included for scalable projects.
- **Quality:** Built-in testing and code coverage ensure reliability and maintainability.

With FusePyStarter, starting your Python project is no longer a hurdle but a streamlined experience that scales from simple scripts to complex AI engineering workflows.

Repository Links
----------------

- **Source Code**: https://github.com/sunil-fm/FusePyStarter.git
- **Issue Tracker**: https://github.com/sunil-fm/FusePyStarter/issues

Features
--------

FusePyStarter is equipped with powerful tools and integrations that promote consistency, automation, and maintainability right from the start. These features are grouped into two key areas: **code quality & consistency** and **project automation & scalability**.

**Code Quality & Consistency**

- `EditorConfig <https://sunil-fm.github.io/FusePyStarter/initialization/editorconfig.html>`_ — Ensures consistent indentation, line endings, and formatting across editors and IDEs.
- `Ruff <https://sunil-fm.github.io/FusePyStarter/initialization/ruff.html>`_ — A lightning-fast Python linter and formatter.
- `MyPy <https://sunil-fm.github.io/FusePyStarter/initialization/mypy.html>`_ — Performs static type checking to catch type-related bugs early.
- `pre-commit <https://sunil-fm.github.io/FusePyStarter/initialization/pre-commit.html>`_ — Automates code quality checks via Git hooks.

**Project Automation & Scalability**

- `Dynaconf <https://sunil-fm.github.io/FusePyStarter/setup/dynaconf.html>`_ — Flexible and layered configuration management system.
- `Fire <https://sunil-fm.github.io/FusePyStarter/setup/fire.html>`_ — Instantly generates CLI interfaces from your Python code.
- `Logging <https://sunil-fm.github.io/FusePyStarter/setup/logging.html>`_ — Built-in, configurable logging setup for debugging and observability.
- `Pytest <https://sunil-fm.github.io/FusePyStarter/setup/pytest.html>`_ — A mature and powerful testing framework.
- `Coverage <https://ghimiresunil.github.io/PyFoundry/setup/coverage.html>`_ — Tracks code coverage during test runs.
- `pytest-cov <https://sunil-fm.github.io/FusePyStarter/setup/pytest-cov.html>`_ — Integrates `coverage` directly with `pytest`.
- `Tox <https://sunil-fm.github.io/FusePyStarter/setup/tox.html>`_ — Automates testing across different Python environments and dependency sets.

These tools work together to provide a seamless development experience — whether you're building a quick prototype or a production-grade system.

Quick Start
-----------

1. Install the latest framework for Python if you haven't already:

   .. code-block:: console

      $ pip install -U fusepystarter
      # or, using uv
      $ uv add fusepystarter

2. Initialize your project:

   .. code-block:: console

      $ fusepystarter init

3. Create a repository and push your project.

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

   Replace ``.env.example`` with ``.env`` to configure your working environment, and replace
   ``.secrets.example`` with ``.secrets.toml`` to store your actual secret values.

   Make sure to exclude ``.secrets.toml`` from version control to keep your secrets secure.

Learn More
----------

For more detailed tutorials and documentation, visit the official `FusePyStarter Tutorial <https://sunil-fm.github.io/FusePyStarter/tutorial.html>`_.

Contribute or Follow Along
--------------------------

FusePyStarter is evolving. Star the repository, follow development, or contribute by submitting issues and pull requests!
