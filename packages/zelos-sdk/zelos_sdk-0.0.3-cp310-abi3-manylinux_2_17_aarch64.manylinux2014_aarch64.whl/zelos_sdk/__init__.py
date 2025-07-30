# Disable ruff reformatting of imports in this file and complaining about wildcard imports
# ruff: noqa: I001, F403

# Import the rust module into the root of our package
# https://github.com/PyO3/pyo3/issues/759#issuecomment-1813396106
from .zelos_sdk import *

# This requires the rust module to be imported first
from .trace import TraceSourceCacheLast, TraceSourceCacheLastEvent, TraceSourceCacheLastField
from .actions import action, actions_registry

# Explicit imports with 'as' aliases to satisfy type checkers
from .zelos_sdk import (
    TracePublishClient as TracePublishClient,
    TracePublishClientConfig as TracePublishClientConfig,
    TraceSource as TraceSource,
    enable_logging as enable_logging,
    init_global_client as init_global_client,
    init_global_source as init_global_source,
)

from ._actions import (
    init_global_actions_registry as init_global_actions_registry,
    init_global_actions_client as init_global_actions_client,
)

from typing import Optional

_INITIALIZED = False


def init(
    name: Optional[str] = None,
    *,
    url: Optional[str] = None,
    client_config: Optional[TracePublishClientConfig] = None,
    log_level: Optional[str] = None,
    trace: bool = True,
    actions: bool = False,
    block: bool = False,
) -> None:
    """
    Initialize the Zelos SDK tracing and actions systems.

    Args:
        name: A unique identifier for your application. Defaults to "python".
        client_config: Configuration options for the TracePublishClient.
            Can include: url, batch_size, batch_timeout_ms.
        log_level: Logging level to enable, None disables logging.
        trace: Whether to initialize the trace system. Defaults to True.
        actions: Whether to initialize the actions system. Defaults to False.
        block: Whether to block the current thread until exit. Defaults to False.

    Examples:
        >>> # Initialize with defaults
        >>> init()
        >>>
        >>> # Initialize with custom name
        >>> init("my_app")
        >>>
        >>> # Initialize with custom config
        >>> init(
        ...     "my_app",
        ...     client_config=TracePublishClientConfig(
        ...         url="grpc://localhost:2300",
        ...     ),
        ...     log_level="debug"
        ... )
        >>>
        >>> # Initialize only logging, no tracing or actions
        >>> init(log_level="debug", trace=False)
        >>>
        >>> # Initialize actions and block until exit
        >>> init(actions=True, block=True)
    """
    name = name or "python"

    global _INITIALIZED
    _INITIALIZED = True

    if log_level is not None:
        enable_logging(log_level)

    if trace:
        client_config = client_config or TracePublishClientConfig()
        if url is not None:
            client_config.url = url

        init_global_client(client_config)
        init_global_source(name)

    if actions:
        init_global_actions_client(name=name, url=url)

    if block:
        import time

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Ctrl+C received, exiting...")


def initialized() -> bool:
    return _INITIALIZED


__all__ = [
    # SDK initialization
    "init",
    # Trace
    "TraceSourceCacheLast",
    "TraceSourceCacheLastEvent",
    "TraceSourceCacheLastField",
    # Actions
    "action",
    "actions_registry",
]
