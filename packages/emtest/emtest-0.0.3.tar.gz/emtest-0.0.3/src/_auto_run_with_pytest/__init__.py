"""Rerun the orignially executed python script in pytest instead of python."""
import os
import sys

from emtest import run_pytest

# Configuration for standalone execution
BREAKPOINTS = False  # Set to True to enable debugger on test failures

path_parts = sys.argv[0].split(os.sep)
if not (
    path_parts[-1] == "pytest"
    or (
        len(path_parts) > 1
        and path_parts[-2] == "pytest"
        and path_parts[-1] == "__main__.py"
    )
):
    test_file = os.path.abspath(sys.argv[0])
    pytest_args=sys.argv[1:]
    # print("RERUNNING IN PYTEST:", test_file)

    # Use emtest's custom test runner with specific settings:
    run_pytest(
        test_path=test_file,              # Run tests in this file
        breakpoints=BREAKPOINTS,         # Enable/disable debugger on failures
        enable_print=True,               # Show print statements in tests
        pytest_args=pytest_args
    )

    sys.exit(-1)
else:
    # print("ALREADY RUNNING IN PYTEST")
    pass
