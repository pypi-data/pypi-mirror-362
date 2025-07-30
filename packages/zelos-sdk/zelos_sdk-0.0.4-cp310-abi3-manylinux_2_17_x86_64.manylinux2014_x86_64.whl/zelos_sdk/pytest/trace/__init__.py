# Disable import ordering check for this file due to import shenanigans
# ruff: noqa: I001

"""
Zelos Cloud trace plugin

Use via:

  pytest_plugins = ["zelos_sdk.pytest.trace"]

"""

from typing import Generator
import logging

from zelos_sdk import TracePublishClientConfig
import pytest
import zelos_sdk


# TODO(tkeairns): This import pattern is a mess, think of a better way to manage these modules
# Import module-specific addoption/configure functions
from ._file import pytest_configure as file_pytest_configure
from ._file import pytest_addoption as file_pytest_addoption
from ._logging import pytest_addoption as logging_pytest_addoption
from ._stdout import pytest_addoption as stdout_pytest_addoption

# We are exposing this hookwrapper directly
from ._file import pytest_runtest_makereport as pytest_runtest_makereport

# Fixtures need to be exposed to the pytest.plugins namespace to be picked up
from ._file import trace_file_class as trace_file_class
from ._file import trace_file_function as trace_file_function
from ._file import trace_file_module as trace_file_module
from ._file import trace_file_session as trace_file_session
from ._logging import trace_logging as trace_logging
from ._stdout import trace_stdout as trace_stdout

log = logging.getLogger(__name__)

DEFAULT_TRACE_FORWARD_URL = "grpc://localhost:2300"


def pytest_addhooks(pluginmanager):
    """This example assumes the hooks are grouped in the 'hooks' module."""
    from . import hooks  # pylint: disable=import-outside-toplevel

    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Parses flags that can enable/disable specific event handlers.

    :param parser: A pytest Parser object to add the command-line options.
    """
    group = parser.getgroup("zelos", description="Zelos tracing plugin")
    group.addoption("--zelos-log", action="store_true", help="Enable Zelos SDK logs")
    group.addoption("--zelos-log-level", action="store", default="info", help="Set the Zelos SDK log level")
    group.addoption("--zelos-trace", action="store_true", help="Enable tracing to the Zelos Agent")
    group.addoption("--zelos-trace-url", action="store", default=DEFAULT_TRACE_FORWARD_URL, help="Set the url")

    file_pytest_addoption(parser)
    logging_pytest_addoption(parser)
    stdout_pytest_addoption(parser)


def pytest_configure(config):
    """Initialize trace file tracking when pytest starts"""
    # Initialize the trace files tracking dictionary
    file_pytest_configure(config)


@pytest.fixture(scope="session", autouse=True)
def zelos_session(request) -> Generator[None, None, None]:
    """Initialize Zelos session-level fixtures."""

    log_level = None
    if request.config.getoption("--zelos-log"):
        log_level = request.config.getoption("--zelos-log-level")

    if request.config.getoption("--zelos-trace"):
        trace_grpc_url = request.config.getoption("--zelos-trace-url")
        config = TracePublishClientConfig(url=trace_grpc_url)
        zelos_sdk.init(client_config=config, log_level=log_level)
    elif request.config.getoption("--zelos-log"):
        zelos_sdk.enable_logging(log_level)
