# Pull in all fixtures, hooks, and markers by importing everything into the current namespace
# Formatters complain about the wildcard import, so we'll import the modules directly
import logging

from zelos_sdk.pytest.checker import check
from zelos_sdk.pytest.trace import (
    # Note: pytest_runtest_makereport is imported directly since it's a hookwrapper
    # and needs to be exposed directly to pytest
    pytest_runtest_makereport,
    trace_file_class,
    trace_file_function,
    trace_file_module,
    trace_file_session,
    trace_logging,
    trace_stdout,
    zelos_session,
)
import zelos_sdk.pytest.checker as checker
import zelos_sdk.pytest.config as config
import zelos_sdk.pytest.report as report
import zelos_sdk.pytest.trace as trace

logger = logging.getLogger(__name__)

_imported_modules = [
    ("config", config),
    ("trace", trace),
    ("report", report),
    ("checker", checker),
]


def pytest_addoption(parser):
    """Add options for plugin selection and delegate to enabled plugins"""
    # Delegate to enabled plugins
    for plugin_name, module in _imported_modules:
        if hasattr(module, "pytest_addoption"):
            try:
                module.pytest_addoption(parser)
            except Exception as e:
                logger.error(f"Error calling pytest_addoption for plugin '{plugin_name}': {e}")
                raise e


def pytest_configure(config):
    """Configure enabled plugins"""
    # Delegate to enabled plugins
    for plugin_name, module in _imported_modules:
        if hasattr(module, "pytest_configure"):
            try:
                module.pytest_configure(config)
            except Exception as e:
                logger.error(f"Error calling pytest_configure for plugin '{plugin_name}': {e}")
                raise e


def pytest_addhooks(pluginmanager):
    """Add hooks from enabled plugins"""
    # Delegate to enabled plugins
    for plugin_name, module in _imported_modules:
        if hasattr(module, "pytest_addhooks"):
            try:
                module.pytest_addhooks(pluginmanager)
            except Exception as e:
                logger.error(f"Error calling pytest_addhooks for plugin '{plugin_name}': {e}")
                raise e


def pytest_zelos_configure(config):
    """Delegate pytest_zelos_configure to enabled plugins"""
    # Delegate to enabled plugins that have this hook
    for plugin_name, module in _imported_modules:
        if hasattr(module, "pytest_zelos_configure"):
            try:
                module.pytest_zelos_configure(config)
            except Exception as e:
                logger.error(f"Error calling pytest_zelos_configure for plugin '{plugin_name}': {e}")


__all__ = [
    "check",
    "pytest_addhooks",
    "pytest_addoption",
    "pytest_configure",
    "pytest_runtest_makereport",
    "pytest_zelos_configure",
    "trace_file_class",
    "trace_file_function",
    "trace_file_module",
    "trace_file_session",
    "trace_logging",
    "trace_stdout",
    "zelos_session",
]
