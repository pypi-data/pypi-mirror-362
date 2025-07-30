"""
Default zelos trace file name hook
"""

from pytest import hookspec


@hookspec(firstresult=True)
def pytest_zelos_trace_file_name(request):
    """Return the default value for the config file command line option."""
