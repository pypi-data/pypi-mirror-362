

import os
import sys
import shutil
import threading
import time
from time import sleep
from typing import List
from tqdm import TMonitor, tqdm

from types import ModuleType


def are_we_in_docker() -> bool:
    """Check if this code is running in a docker container."""
    return os.path.exists('/.dockerenv')


def add_path_to_python(src_path: str) -> None:
    """Add a directory to the Python path for importing modules.

    Removes the path if it already exists, then inserts it at the beginning
    of sys.path to ensure it takes priority over installed packages.

    Args:
        src_path: Directory path to add to Python path

    Raises:
        FileNotFoundError: If the path doesn't exist
        NotADirectoryError: If the path is not a directory
    """
    src_path = os.path.abspath(src_path)
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"The path doesn't exist: {src_path}")
    if not os.path.isdir(src_path):
        raise NotADirectoryError(f"The path doesn't exist: {src_path}")

    if src_path in sys.path:
        sys.path.remove(src_path)
    sys.path.insert(0, src_path)


def assert_is_loaded_from_source(
    source_dir: str, module: ModuleType, print_confirmation=False
) -> None:
    """Assert a module is loaded from source code, not an installation.

    Asserts that the loaded module's source code is located within the given
    directory, regardless of whether it's file is located in that folder or is
    nested in subfolders.

    Args:
        source_dir: a directory in which the module's source should be
        module: the module to check
    """
    module_path = os.path.abspath(module.__file__)
    source_path = os.path.abspath(source_dir)
    assert (
        source_path in module_path
    ), (
        f"The module `{module.__name__}` has been loaded from an installion, "
        "not this source code!\n"
        f"Desired source dir: {source_path}\n"
        f"Loaded module path: {module_path}\n"
    )
    if print_confirmation:
        print(f"Using module {module.__name__} from {module_path}")


def polite_wait(n_sec: int) -> None:
    """Wait for the given duration, displaying a progress bar.

    Args:
        n_sec: Number of seconds to wait
    """
    # print(f"{n_sec}s patience...")
    for i in tqdm(range(n_sec), leave=False):
        time.sleep(1)


def await_thread_cleanup(timeout: int = 5) -> bool:
    """Wait for all threads to exit, with a timeout and progress bar.

    Args:
        timeout: Maximum seconds to wait for thread cleanup

    Returns:
        True if only the main thread remains, False if other threads persist
    """
    def get_threads() -> List[threading.Thread]:
        """Get all active threads except tqdm monitor threads."""
        return [
            x for x in threading.enumerate() if not isinstance(x, TMonitor)
        ]

    for i in tqdm(range(timeout), leave=False):
        if len(get_threads()) == 1:
            break
        sleep(1)

    return len(get_threads()) == 1

def get_thread_names():
    """Get a list of the names of all active threads."""
    return [thread.name for thread in threading.enumerate()]

def set_env_var(name: str, value: str | bool | int, override: bool = True):
    """
    Set an environment variable with optional overriding behavior.

    Args:
        name (str): The name of the environment variable to set.
        value (str): The value to assign to the environment variable.
        override (bool, optional): Whether to overwrite the variable if it is already set.
                                   Defaults to False.

    Behavior:
        - If 'override' is True, the environment variable will always be set to 'value'.
        - If 'override' is False, the variable will only be set if it is not already defined.
    """
    if isinstance(value, bool):
        value = int(value)
    if isinstance(value, int):
        value = str(value)
    if override or name not in os.environ:
        os.environ[name] = value

def make_dir(dir_path: str, clear_existing: bool = False) -> str:
    """Create a directory, handling the case where it already exists."""
    if clear_existing and os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    return dir_path


def delete_path(path: bool) -> bool:
    """Delete the specified file or folder."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)

def ensure_dirs_exist(*dirs):
    """Ensure that all directories in the list exist."""
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path
