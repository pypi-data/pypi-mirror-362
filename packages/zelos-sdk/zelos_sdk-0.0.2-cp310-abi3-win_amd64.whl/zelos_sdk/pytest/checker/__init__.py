"""
Checker plugin for pytest.

Use via:

  pytest_plugins = ["zelos_sdk.pytest.checker"]

"""

import logging

import pytest

from .checker import Checker

__all__ = [
    "check_config",
    # Fixtures must be here to be discovered by pytest for the 'zelos_sdk.pytest.plugins' catchall
    "check",
]

log = logging.getLogger("zelos-checker")


check_config = pytest.mark.check_config


@pytest.fixture(scope="function")
def check(request):
    """checker object"""
    config = request.node.get_closest_marker("check_config")
    config_kwargs = {}

    # if a check_config marker was a decorated onto to a test, than grab out the config
    # params and pass them to the checker.
    if config is not None:
        config_kwargs["fail_fast"] = config.kwargs.get("fail_fast", True)

    with Checker(title=request.node.name, **config_kwargs) as _check:
        yield _check


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item):
    # This is important, it ensures we run the test and then come back after
    yield
    check = item.funcargs.get("check")

    # If the `fail_fast` flag was set to false, then we want to make sure we evaluate
    # all the check items and fail the test if one or more failed.
    __tracebackhide__ = True
    if check and check._checks and not check._fail_fast:
        if not all(item.result for item in check._checks):
            pytest.fail("One or more checks failed, please see the Zelos Checkerboard for more information.")
