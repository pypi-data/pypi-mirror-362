"""
This module defines classes for creating and evaluating check-able items with
operands, operators, and results. It supports immediate checks, continuous checks
over a duration, and checks that must become true within a specified duration.

Example usage:
    >>> from zelos_sdk.pytest.checker.items import (
            CheckerItem,
            ForDurationCheckerItem,
            WithinDurationCheckerItem,
        )

    # Immediate check evaluation
    >>> assert CheckerItem(lhs=1, op="==", rhs=1)
    >>>
    >>> if CheckerItem(lhs=1, op="==", rhs=1):
    ...     print("success")
    ...
    success

    # Check that a condition remains true for a specific duration (blocking)
    >>> def on_check_complete(item):
    ...     print(f"Check complete: {item.result}")
    ...
    >>> item = ForDurationCheckerItem(lhs=signal, op="==", rhs=expected_value, duration_s=5, interval_s=0.1, callback=on_check_complete)
    ...
    Check complete: True

    # Check that a condition remains true for a specific duration (non-blocking)
    >>> item = ForDurationCheckerItem(lhs=signal, op="==", rhs=expected_value, duration_s=5, interval_s=0.1, blocking=False, callback=on_check_complete)
    >>> # Do other tasks while the check is running
    >>> print("Waiting for check to complete...")
    >>> time.sleep(6)
    ...
    Waiting for check to complete...
    Check complete: True

    # Check that a condition becomes true within a specific duration (blocking)
    >>> item = WithinDurationCheckerItem(lhs=signal, op="==", rhs=expected_value, duration_s=5, interval_s=0.1, callback=on_check_complete)
    >>> if item.result:
    ...     print("Condition became true within the specified duration")
    ...
    Condition became true within the specified duration

    # Check that a condition becomes true within a specific duration (non-blocking)
    >>> item = WithinDurationCheckerItem(lhs=signal, op="==", rhs=expected_value, duration_s=5, interval_s=0.1, blocking=False, callback=on_check_complete)
    >>> # Do other tasks while the check is running
    >>> print("Waiting for check to complete...")
    >>> time.sleep(6)
    ...
    Waiting for check to complete...
    Check complete: True
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Union
import logging
import threading
import time

from colorama import Fore, Style
from zelos_sdk.trace import TraceSourceCacheLastField

# from zelos_sdk.core.events import CheckerEvalEvent, OnCheckerEvalEmitter
from . import ops

log = logging.getLogger("zelos-checker")


@dataclass(kw_only=True, slots=True)
class CheckerOperand:
    """
    Represents a check-able operand, which can contain a static value or be
    linked to a signal providing dynamic values.

    :param value: The value of the operand.
    :param name: The name of the operand.
    """

    value: Any = None
    name: Optional[str] = None
    _sig: Optional[TraceSourceCacheLastField] = None

    def get(self) -> Any:
        """Get the value for the operand"""
        if self._sig is not None:
            self.value = self._sig.get()
        return self.value

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the data to a dictionary.

        :return: Dictionary representation of the CheckerItem.
        """
        return {"name": self.name, "value": self.value}

    def __post_init__(self):
        if self._sig is not None:
            self.name = self._sig.name

    def __str__(self) -> str:
        if self.name:
            return f"{self.name} ({self.value})"
        return f"{self.value}"


class CheckerItemBase:
    """
    Represent an assertion item in the checker board.

    :param lhs: Left-hand side operand.
    :param op: Operator for the check.
    :param rhs: Right-hand side operand.
    :param duration_s: Duration for which the condition should be true.
    :param interval_s: Interval between condition checks.
    :param blocking: Whether the polling should be blocking.
    :param args: Additional arguments for the operator.
    :param kwargs: Additional keyword arguments for the operator.
    :param callback: Callback function to call after poll is done.
    """

    def __init__(
        self,
        lhs: Union[Any, TraceSourceCacheLastField],
        op: Union[str, ops.DescriptiveOp],
        rhs: Union[Any, TraceSourceCacheLastField] = None,
        duration_s: float = None,
        interval_s: float = None,
        blocking: bool = True,
        args: tuple = (),
        kwargs: dict = {},
        callback: Callable[["CheckerItemBase"], None] = None,
    ):
        if isinstance(lhs, TraceSourceCacheLastField):
            self.lhs = CheckerOperand(_sig=lhs)
        elif not isinstance(lhs, CheckerOperand):
            self.lhs = CheckerOperand(value=lhs)
        else:
            raise ValueError("Invalid type for lhs")

        self.op = ops.get_op(op) if isinstance(op, str) else op

        if not self.op.is_unary:
            if isinstance(rhs, TraceSourceCacheLastField):
                self.rhs = CheckerOperand(_sig=rhs)
            elif not isinstance(rhs, CheckerOperand):
                self.rhs = CheckerOperand(value=rhs)
            else:
                raise ValueError("Invalid type for rhs")
        else:
            self.rhs = None

        self.duration_s = duration_s
        self.interval_s = interval_s
        self.blocking = blocking
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.time_ns: int = None
        self.result: bool = None
        # TODO(tkeairns): Add back in the OnCheckerEvalEmitter
        # self.on_eval: OnCheckerEvalEmitter = OnCheckerEvalEmitter(self)

    @property
    def params(self) -> str:
        """Get all the parameters used for the operator."""
        params = str(self.args) if self.args else ""
        params += ", ".join(f"{k}={v}" for k, v in self.kwargs.items()) if self.kwargs else ""
        return params

    def eval(self) -> bool:
        """
        Evaluates the check and updates/returns the result.

        :return: Result of the evaluation.
        """
        self.time_ns = time.time_ns()
        if self.op.is_unary:
            self.result = self.op(self.lhs.get())
        else:
            self.result = self.op(self.lhs.get(), self.rhs.get(), *self.args, **self.kwargs)

        log.info("%s --> %s%s", self, f"{Fore.GREEN}PASSED" if self.result else f"{Fore.RED}FAILED", Style.RESET_ALL)
        # TODO(tkeairns): Add back in the CheckerEvalEvent
        # self.on_eval.send(CheckerEvalEvent(str(self), **self.to_dict()))
        return self.result

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the data to a dictionary.

        :return: Dictionary representation of the CheckerItem.
        """
        return {
            "lhs": self.lhs.to_dict() if self.lhs else {},
            "op": self.op.desc,
            "rhs": self.rhs.to_dict() if self.rhs else {},
            "duration_s": self.duration_s,
            "interval_s": self.interval_s,
            "blocking": self.blocking,
            "args": self.args,
            "kwargs": self.kwargs,
            "time_ns": self.time_ns,
            "result": self.result,
        }

    def __bool__(self) -> bool:
        return self.eval()


class ThreadedCheckerItemBase(CheckerItemBase):
    """
    Base class for checker items that involve threaded polling of a condition.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        __tracebackhide__ = True
        self._thread: Optional[threading.Thread] = None
        if self.blocking:
            self._poll_thread()
        else:
            self._thread = threading.Thread(target=self._poll_thread)
            self._thread.start()

    def _poll_thread(self) -> None:
        """Poll the condition based on specific implementation."""
        raise NotImplementedError("Subclasses should implement this method")

    def running(self) -> bool:
        """Check if the checker item is still running."""
        if self._thread:
            return self._thread.is_alive()
        return False

    def __del__(self):
        if self._thread and self._thread.is_alive():
            self._thread.join()


class CheckerItem(CheckerItemBase):
    """Checker item that evaluates the condition immediately upon creation."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.eval()
        if self.callback:
            self.callback(self)

    def __str__(self) -> str:
        base = f"{self.lhs} {self.op.desc}"
        if not self.op.is_unary:
            base += f" {self.rhs}"
        if self.params:
            base += f" with params {self.params}"
        return base


class ForDurationCheckerItem(ThreadedCheckerItemBase):
    """
    Checker item that ensures the condition is true continuously for a specific duration.
    """

    def _poll_thread(self) -> None:
        """Poll the condition continuously for the specified duration at a defined interval."""
        __tracebackhide__ = True
        end_time = time.perf_counter() + self.duration_s
        result = True
        while time.perf_counter() < end_time:
            if not self.eval():
                result = False
                break
            time.sleep(self.interval_s)
        self.result = result
        if self.callback:
            self.callback(self)

    def __str__(self) -> str:
        base = f"{self.lhs} {self.op.desc}"
        if not self.op.is_unary:
            base += f" {self.rhs}"
        if self.duration_s:
            base += f" for {self.duration_s}s"
        if self.params:
            base += f" with params {self.params}"
        return base


class WithinDurationCheckerItem(ThreadedCheckerItemBase):
    """
    Ensures that the condition becomes true within a specified duration.
    """

    def _poll_thread(self) -> None:
        """Poll the condition until it becomes true or the duration elapses."""
        __tracebackhide__ = True
        end_time = time.perf_counter() + self.duration_s
        result = False
        while time.perf_counter() < end_time:
            if self.eval():
                result = True
                break
            time.sleep(self.interval_s)
        self.result = result
        if self.callback:
            self.callback(self)

    def __str__(self) -> str:
        base = f"{self.lhs} {self.op.desc}"
        if not self.op.is_unary:
            base += f" {self.rhs}"
        if self.duration_s:
            base += f" within {self.duration_s}s"
        if self.params:
            base += f" with params {self.params}"
        return base
