"""
Defines an abstract base class for contextual objects that open/close connections
"""

from abc import ABC, abstractmethod
from threading import Event
from typing import Any
import logging

log = logging.getLogger(__name__)


class ContextBase(ABC):
    """
    Abstract base class that defines methods a Context must implement.

    Contextual objects are ones that should be opened or closed, like a file or connection.
    """

    def __init__(self, **kwargs: Any) -> None:
        self._is_open = Event()
        super().__init__(**kwargs)

    @property
    def is_open(self) -> bool:
        """Returns true if opened, else false"""
        return self._is_open.is_set()

    @property
    def is_closed(self) -> bool:
        """Returns true if closed, else false"""
        return not self.is_open

    @abstractmethod
    def _open(self) -> None:
        """Private interface for opening a connection/file/etc."""

    @abstractmethod
    def _close(self) -> None:
        """Private interface for closing a connection/file/etc."""

    def open(self) -> None:
        """Public interface for opening a connection/file/etc."""
        if not self.is_open:
            log.debug("Opening %s", self)
            try:
                self._open()
                self._is_open.set()
                log.debug("%s now open", self)
            except Exception as e:
                log.error("Failed to open %s: %s", self, e)
                raise

    def close(self) -> None:
        """Public interface for closing a connection/file/etc."""
        if self.is_open:
            log.debug("Closing %s", self)
            # De-assert prior to close() since some threads could loop on `while is_open`:
            self._is_open.clear()
            try:
                self._close()
                log.debug("%s now closed", self)
            except Exception as e:
                log.error("Failed to close %s: %s", self, e)
                raise

    def __enter__(self) -> "ContextBase":
        """Contextual open. Called using 'with'"""
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Contextual close. Called after 'with'"""
        self.close()

    def __del__(self) -> None:
        """Ensure we close properly upon deletion of an object"""
        try:
            # Only perform the close check if properly constructed
            if hasattr(self, "is_open") and self.is_open:
                log.warning("Unclosed context, closing `%s` on __del__", self)
                self.close()
        except Exception as e:
            log.exception("Exception on __del__, ensure __init__ is called or check the close sequence: %s", e)

    def __repr__(self) -> str:
        """String representation for debugging and logging"""
        return f"<{self.__class__.__name__}(is_open={self.is_open})>"
