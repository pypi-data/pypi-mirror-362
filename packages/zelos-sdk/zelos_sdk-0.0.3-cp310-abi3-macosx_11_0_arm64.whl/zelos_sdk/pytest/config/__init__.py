"""
Config plugin for pytest.

Use via:

  pytest_plugins = ["zelos_sdk.pytest.config"]

"""

from datetime import datetime
from pathlib import Path


def pytest_addhooks(pluginmanager):
    """This example assumes the hooks are grouped in the 'hooks' module."""
    from . import hooks  # pylint: disable=import-outside-toplevel

    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser):
    """Add options for the pytest invocation"""
    parser.addoption("--zelos-local-artifacts-dir", help="Local artifacts output directory")
    parser.addoption("--zelos-artifact-basename", help="Artifact basename format", default="{date:%Y%m%d-%H%M%S}-zelos")


def pytest_configure(config):
    """Configurations for the pytest invocation"""
    zelos_local_artifacts_dir = config.getoption("zelos_local_artifacts_dir")
    if zelos_local_artifacts_dir:
        config.zelos_local_artifacts_dir = config.rootpath / Path(zelos_local_artifacts_dir)
        config.zelos_local_artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Generate the report name from the given format string
    zelos_artifact_basename_format = config.getoption("zelos_artifact_basename")
    zelos_artifact_basename_args = {"date": datetime.now()}

    config.option.zelos_artifact_basename = zelos_artifact_basename_format.format(**zelos_artifact_basename_args)

    config.pluginmanager.hook.pytest_zelos_configure(config=config)
