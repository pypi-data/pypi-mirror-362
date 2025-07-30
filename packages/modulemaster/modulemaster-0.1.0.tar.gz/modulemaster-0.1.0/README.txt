# modulemaster - Automatic Python Dependency Installer (mm)

`modulemaster` (abbreviated `mm`) is a lightweight and "dumb" Python module designed to automatically check for and install missing project dependencies by analyzing the import statements in the calling script. It aims to simplify the initial setup process for Python applications by attempting to resolve common dependency issues on the fly.

## How it Works

`modulemaster` operates with a straightforward, hands-off approach to dependency management:

1.  **Self-Sufficiency Check:** Upon execution, `modulemaster` first verifies the presence of its own critical internal dependency, `setuptools` (which provides `pkg_resources`). If `setuptools` is missing, `modulemaster` will attempt to install it automatically to ensure its core functionality.
2.  **Caller Analysis:** When you invoke `mm.auto()` from your main Python script (e.g., `app.py`), `modulemaster` intelligently identifies the path to that calling file.
3.  **Import Discovery:** It then performs static analysis on the calling file's source code using Python's `ast` (Abstract Syntax Tree) module. This allows `modulemaster` to accurately identify all top-level `import` statements (e.g., `import flask`) and `from ... import` statements (e.g., `from sqlalchemy import create_engine`).
4.  **Direct Installation Attempt:** For every unique, top-level module name discovered (e.g., `flask`, `requests`, `sqlalchemy`), `modulemaster` attempts to install a `pip` package with the *exact same name*. It does not try to infer alternative package names.
5.  **Version Logging:** Any packages that `modulemaster` successfully installs during its execution are meticulously logged. This log, including the package name and its installed version, is appended to a file named `auto-installed_modules.txt` in the current working directory.
6.  **"Dumb" Behavior & Strict Error Reporting:**
    * `modulemaster` is intentionally designed to be "dumb" regarding package naming conventions. It **does not** attempt to map an import name (like `werkzeug.security`) to a different `pip` package name (like `Werkzeug`).
    * If a package installation fails for any reason (e.g., the `pip` package name doesn't match the import name, network issues, or the package simply doesn't exist on PyPI), `modulemaster` will print a clear error message to the console detailing the failure. Crucially, it will then **exit the program** (`sys.exit(1)`). This strict behavior ensures that you, as the developer, are immediately alerted to unresolvable dependencies, preventing your application from running in a potentially broken state. The responsibility for correcting import names or manually installing packages with non-standard names (e.g., `pip install Werkzeug` instead of `pip install werkzeug.security`) lies with the developer.

## Installation

To make `modulemaster` available for use across all your Python projects, you need to install it into your Python environment.

1.  **Prepare Files:** Ensure you have the `modulemaster.py`, `setup.py`, and this `README.txt` file located together in a dedicated directory (e.g., `modulemaster_installer/`).
2.  **Navigate to Directory:** Open your terminal or command prompt and navigate to the `modulemaster_installer/` directory.
3.  **Install with Pip:** Execute the following `pip` command:
    ```bash
    pip install .
    ```
    * The `.` (dot) signifies the current directory, instructing `pip` to find and install the package defined by the `setup.py` file within it.
    * **Highly Recommended:** Always perform this installation within a Python [virtual environment](https://docs.python.org/3/library/venv.html) to isolate your project's dependencies and avoid conflicts with other Python projects or your system's Python installation.

## Usage in Your Python Application

Once `modulemaster` is installed in your environment, integrating it into any of your Python applications is incredibly simple:

1.  **Add to Top of Script:** Place these two lines at the **very beginning** of your main Python application file (e.g., `app.py`), *before* any other `import` statements that you want `modulemaster` to manage:

    ```python
    from modulemaster import mm
    mm.auto()

    # Now, you can safely import the rest of your application's modules.
    # For example:
    # from flask import Flask
    # import requests
    # from sqlalchemy import create_engine
    # import chromadb
    # import tiktoken
    # from dotenv import load_dotenv
    # from langchain_text_splitters import RecursiveCharacterTextSplitter
    # from werkzeug.security import generate_password_hash
    ```modulemaster` will automatically analyze this file, identify its imports, and attempt to install any missing corresponding packages.

## `auto-installed_modules.txt`

When `modulemaster` runs and successfully installs one or more missing modules, it will create (or append to, if it already exists) a file named `auto-installed_modules.txt`. This file will be located in the directory from which your application was executed. It serves as a helpful log, listing the package names and their installed versions, providing a clear record of what `modulemaster` handled.

## Limitations (Important Considerations)

* **No Name Mapping:** As designed, `modulemaster` does not infer `pip` package names from import names if they differ. For example, if your code has `import sqlalchemy`, `modulemaster` will attempt to `pip install sqlalchemy`. If the correct package name on PyPI is `SQLAlchemy`, this installation will fail. In such cases, you will need to manually install the correct package (e.g., `pip install SQLAlchemy`) or adjust your import statement if an alternative, directly named module exists.
* **Top-Level Imports Only:** `modulemaster` analyzes only top-level `import` and `from ... import` statements. It will not detect modules that are imported dynamically (e.g., within a function or conditionally) or through more complex programmatic means.
* **Error Exiting:** `modulemaster` is designed for strict dependency enforcement. If it encounters an unresolvable installation error (e.g., a package not found, a network issue, or a naming mismatch), it will `sys.exit(1)`, stopping your application's execution. This is intentional to prevent your application from running with critical missing dependencies, forcing immediate developer attention.
* **No Version Resolution:** `modulemaster` does not handle version conflicts or specific version requirements. It simply attempts to install the latest available version of a missing package. For complex dependency trees or strict version control, you should still rely on a `requirements.txt` file and `pip install -r`.
