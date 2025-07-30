"""
Print trace events to stdout functionality for the trace plugin.
"""

from typing import Generator

from zelos_sdk import TraceStdout
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add command line options for logging."""
    group = parser.getgroup("zelos", description="Zelos tracing plugin")
    group.addoption(
        "--zelos-trace-stdout",
        action="store_true",
        help="Enable printing of trace events to stdout",
    )
    group.addoption(
        "--zelos-trace-stdout-level",
        action="store",
        default="info",
        help="Set the log level for trace events printed to stdout",
    )


@pytest.fixture(scope="session", autouse=True)
def trace_stdout(request) -> Generator[None, None, None]:
    """Initialize logging for the entire test session."""
    if not request.config.getoption("--zelos-trace-stdout"):
        yield
        return

    log_level = request.config.getoption("--zelos-trace-stdout-level")
    with TraceStdout(log_level=log_level):
        yield
