"""
Logging functionality for the trace plugin.
"""

from typing import Generator
import logging

from zelos_sdk.hooks.logging import TraceLoggingHandler
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add command line options for logging."""
    group = parser.getgroup("zelos", description="Zelos tracing plugin")
    group.addoption(
        "--zelos-trace-logging",
        action="store_true",
        help="Enable forwarding of logs when tracing is enabled",
    )
    group.addoption(
        "--zelos-trace-logging-level",
        action="store",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the log level for forwarded logs",
    )
    group.addoption(
        "--zelos-trace-logging-source-name",
        action="store",
        default="logger",
        help="Set the name of the source for forwarded logs",
    )


@pytest.fixture(scope="session", autouse=True)
def trace_logging(request) -> Generator[None, None, None]:
    """Initialize logging for the entire test session."""
    if request.config.getoption("--zelos-trace-logging"):
        log_level = request.config.getoption("--zelos-trace-logging-level")
        log_name = request.config.getoption("--zelos-trace-logging-source-name")
        handler = TraceLoggingHandler(source_name=log_name, level=getattr(logging, log_level.upper()))
        logging.getLogger().addHandler(handler)
        yield handler
        logging.getLogger().removeHandler(handler)
    else:
        yield
