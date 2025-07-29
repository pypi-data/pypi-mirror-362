

from .testing_utils import set_env_var
import os
import sys
from typing import Any, Optional
from _pytest.terminal import TerminalReporter
from _pytest.config import Config
from _pytest.reports import TestReport
from termcolor import colored

from environs import Env
env_vars = Env()


class MinimalReporter(TerminalReporter):
    """Custom pytest reporter that provides clean, minimal output with colored symbols.

    This reporter suppresses most default pytest output and displays only:
    - ✓ for passed tests (green)
    - ✗ for failed tests (red) 
    - - for skipped tests (yellow)
    """

    def __init__(self, config: Config, print_errors: bool = True) -> None:
        super().__init__(config)
        self._tw.hasmarkup = True  # enables colored output safely
        self.print_errors = print_errors
        self.current_test_file = ""

    def report_collect(self, final: bool = False) -> None:
        pass

    def pytest_collection(self) -> None:
        pass

    def pytest_sessionstart(self, session: Any) -> None:
        """Override session start to suppress 'collected x items' message."""
        # print("pytest_sessionstart")
        pass  # suppress "collected x items"

    def pytest_runtest_logstart(self, nodeid: str, location: Any) -> None:
        """Override test start logging to suppress it."""
        # print("pytest_runtest_logstart")
        current_test_file = os.path.basename(location[0]).strip(".py")
        if current_test_file != self.current_test_file:
            self.current_test_file = current_test_file
            print(f"\n{self.current_test_file}")
        pass  # suppress test start lines

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        """Display minimal test results with colored symbols."""
        if report.when != "call":
            return

        test_name = report.nodeid.split("::")[-1]
        if report.passed:
            self.write("✓", green=True)
            # symbol = colored("✓", "green")
        elif report.failed:
            self.write("✗", red=True)
            # symbol = colored("✗", "red")
        elif report.skipped:
            self.write("-", yellow=True)
            # symbol = colored("-", "yellow")
        # self.write(f"{symbol} {test_name}")

        self.write(f" {test_name}\n")

        if self.print_errors and report.failed:
            print(colored(report.longreprtext, "red"))

    def summary_stats(self) -> None:
        """Override result counts to suppress them."""
        pass  # suppress result counts

    def pytest_terminal_summary(self, terminalreporter: Any, exitstatus: int, config: Config) -> None:
        """Override final summary output to suppress it."""
        pass  # suppress final summary output


# Environment Variable and CLI option to deactivate MinimalReporter
PYTEST_STANDARD_OUTPUT_ENV = "DEFAULT_TERMINAL_REPORTER"
PYTEST_STANDARD_OUTPUT_OPT = "--default-terminal-reporter"
if PYTEST_STANDARD_OUTPUT_OPT in sys.argv:
    set_env_var(PYTEST_STANDARD_OUTPUT_ENV, "1", True)


def configure_pytest_reporter(config: Config, print_errors=True) -> None:
    """Configure the minimal reporter if terminalreporter plugin is disabled.

    Args:
        config: Pytest configuration object
    """
    if env_vars.bool(PYTEST_STANDARD_OUTPUT_ENV, default=False):
        return
    minimal_reporter = MinimalReporter(config, print_errors=print_errors)
    # if terminalreporter plugin is disabled
    if "no:terminalreporter" in config.option.plugins:
        pluginmanager = config.pluginmanager
        pluginmanager.register(minimal_reporter, "minimal-reporter")

    if config.pluginmanager.has_plugin("terminalreporter"):
        reporter = config.pluginmanager.get_plugin("terminalreporter")
        config.pluginmanager.unregister(reporter, "terminalreporter")
        config.pluginmanager.register(minimal_reporter, "terminalreporter")


def run_pytest(
    test_path: str,
    breakpoints: bool = False,
    enable_print: bool = False,
    pytest_args: list[str] | None = None
) -> None:
    """Run pytest with customizable options for output control and debugging.

    Args:
        test_path: Path to the test file or directory to run
        breakpoints: If True, enables pytest debugger (--pdb) on failures
        deactivate_pytest_output: If True, uses minimal reporter instead of default output
        enable_print: If True, enables print statements in tests (-s flag)
    """
    if pytest_args:
        args = pytest_args
        if PYTEST_STANDARD_OUTPUT_OPT in args:
            args.remove(PYTEST_STANDARD_OUTPUT_OPT)
    else:
        args = []
    if enable_print:
        args.append("-s")  # -s disables output capturing
    if breakpoints:
        args.append("--pdb")
    os.system(f"{sys.executable} -m pytest {test_path} {' '.join(args)}")
