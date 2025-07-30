import subprocess
import sys
import importlib
import time # For timestamp in log file
import ast # For parsing Python code
import os # For file path operations

# --- Self-check and install for pkg_resources ---
# This block ensures pkg_resources is available before it's used later in this file.
try:
    import pkg_resources
except ImportError:
    print("Package 'pkg_resources' (from setuptools) not found. Attempting to install 'setuptools'...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
        print("Successfully installed 'setuptools'.")
        import pkg_resources # Try importing again after installation
    except subprocess.CalledProcessError as e:
        print(f"Error installing 'setuptools': {e}")
        print("ModuleMaster requires 'setuptools' to get package versions. Please install it manually: pip install setuptools")
        sys.exit(1) # Exit if critical internal dependency cannot be met
    except Exception as e:
        print(f"An unexpected error occurred during 'setuptools' installation: {e}")
        sys.exit(1)
# --- End of self-check for pkg_resources ---


def _get_imported_modules_from_file(filepath):
    """
    Parses a Python file and extracts top-level imported module names.
    This function performs static analysis and does not execute the code.
    It extracts the base module name for both 'import' and 'from ... import' statements.
    """
    imported_modules = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=filepath)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # For `import module_name` or `import package.module`
                    # We only care about the top-level name for pip install
                    imported_modules.add(alias.name.split('.')[0]) 
            elif isinstance(node, ast.ImportFrom):
                # For `from package.module import name`
                if node.module:
                    # Get the top-level package name
                    imported_modules.add(node.module.split('.')[0]) 
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: Syntax error in {filepath}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while parsing {filepath}: {e}")
        sys.exit(1)
    return imported_modules

def auto():
    """
    Automatically discovers required modules from the Python file that calls this function,
    then checks if they are installed. If not, it attempts to install them
    using their exact import name as the pip package name.
    Logs automatically installed packages and reports installation errors.

    This function determines the calling script's filepath automatically.
    """
    # Determine the filepath of the script that called this function.
    # sys._getframe(1) gets the frame of the caller.
    # This is an internal CPython detail, but practical for this kind of utility.
    try:
        caller_filepath = sys._getframe(1).f_globals['__file__']
    except (AttributeError, KeyError):
        print("Error: Could not determine the calling script's file path automatically.")
        print("Please ensure mm.auto() is called directly from your main script.")
        sys.exit(1)

    print(f"Analyzing '{caller_filepath}' for required modules...")
    imported_modules = _get_imported_modules_from_file(caller_filepath)
    
    missing_modules = [] # Stores module_name strings
    installed_this_session = []
    
    AUTO_INSTALLED_LOG_FILE = "auto-installed_modules.txt"

    for module_name in imported_modules:
        try:
            # Try to import the module to check if it's installed
            importlib.import_module(module_name)
        except ImportError:
            missing_modules.append(module_name)
        except Exception as e:
            print(f"Warning: Unexpected error when checking module '{module_name}': {e}")

    if not missing_modules:
        print("All required Python packages are already installed.")
        return

    print(f"The following modules are missing: {', '.join(missing_modules)}")
    print("Attempting to install them automatically using their import names as package names...")

    for module_name in missing_modules:
        # In 'dumb' mode, the pip package name is assumed to be the same as the module name.
        package_name_for_pip = module_name 
        
        try:
            print(f"Installing '{package_name_for_pip}'...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name_for_pip])
            print(f"Successfully installed '{package_name_for_pip}'.")
            
            # After successful installation, try to get the version and record it
            try:
                dist = pkg_resources.get_distribution(package_name_for_pip)
                installed_this_session.append(f"{package_name_for_pip}=={dist.version}")
            except pkg_resources.DistributionNotFound:
                installed_this_session.append(f"{package_name_for_pip} (version unknown after install)")
            
            # Attempt to import the module after installation to make it available for the calling script
            importlib.import_module(module_name)

        except subprocess.CalledProcessError as e:
            print(f"Error installing package '{package_name_for_pip}': {e}")
            print(f"This might be due to a mismatch between the import name and the pip package name, or other installation issues.")
            print(f"Please install '{package_name_for_pip}' manually using: pip install <correct-package-name>")
            sys.exit(1) # Exit if a critical package cannot be installed
        except Exception as e:
            print(f"An unexpected error occurred during installation of '{package_name_for_pip}': {e}")
            sys.exit(1)
    
    print("All specified packages are now installed (or attempted).")

    # Write the list of auto-installed modules to a file
    if installed_this_session:
        try:
            with open(AUTO_INSTALLED_LOG_FILE, 'a') as f: # 'a' for append mode
                f.write(f"\n--- Auto-installed on {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                for item in installed_this_session:
                    f.write(f"{item}\n")
            print(f"Auto-installed modules logged to {AUTO_INSTALLED_LOG_FILE}")
        except IOError as e:
            print(f"Error writing to {AUTO_INSTALLED_LOG_FILE}: {e}")
