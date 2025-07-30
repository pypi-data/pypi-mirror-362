"""
This module provides a framework for defining and using descriptive operations, primarily
utilized in assertion checks. The core of this framework is the `DescriptiveOp` class, which
wraps callable operations with descriptive text.

Example Usage:
--------------
```python
from zelos_sdk.pytest.checker import ops

# Registering custom operations
def custom_op(x, y): return x * 2 == y
ops.register_op(ops.DescriptiveOp(custom_op, "double equals"))

# Using a registered operation
eq_op = ops.get_op("equals")
assert eq_op(3, 3)

# Listing all available operations
ops.list_ops()
# prints -> ['equals', 'double equals']
```
"""

from inspect import signature
from typing import Callable, Dict
import logging
import math
import operator

import pytest

log = logging.getLogger("zelos-checker")


class OpsError(Exception):
    """Base exception class for operator errors."""


class DescriptiveOp:
    """
    Represents a descriptive callable operation. This is used to display more descriptive
    text in the check board operator output.

    :param op: A callable object that implements the operation logic.
    :param description: A string describing the operation. Defaults to name of function.
    """

    def __init__(self, op: Callable[..., bool], description: str = None) -> None:
        # Ensure the operator is a callable
        if not callable(op):
            raise OpsError(f"Function '{op}' is not callable.")

        # Ensure the operator requires at least 1 operand
        params = list(signature(op).parameters.keys())
        if len(params) == 0:
            raise OpsError(f"Function '{op}' must take at least 1 argument.")

        self.desc: str = description or op.__name__
        self.op: Callable[..., bool] = op
        self.params: list[str] = params
        self.is_unary = len(params) == 1

    def __call__(self, *args, **kwargs) -> bool:
        """
        Executes the operation with the provided arguments.

        :param args: Arguments to pass to the operation's function.
        :param kwargs: Additional keyword arguments to pass to the operation's function.
        :return: The result of the operation as a boolean.
        :raises OpsError: If there is an error in executing the operation.
        """
        try:
            return self.op(*args, **kwargs)
        except Exception as err:
            raise OpsError(
                f"Error calling operation '{self.desc}' with args='{args}' kwargs='{kwargs}': {err}"
            ) from err

    def __str__(self) -> str:
        return f"{self.params[0]} {self.desc}" + f" {' '.join(self.params[1:])}" if not self.is_unary else ""


# Global registry of descriptive operations
_ops_registry: Dict[str, DescriptiveOp] = {}


def register_op(op: DescriptiveOp, overwrite: bool = False) -> None:
    """
    Registers a new operation using its description as the key. Optionally allows
    overwriting an existing operation.

    :param op: Instance of DescriptiveOp to be registered.
    :param overwrite: Boolean flag to allow overwriting existing operations (default is False).
    :raises ValueError: If an operation with the same description is already registered
                         and overwrite is False.
    """
    if op.desc in _ops_registry and not overwrite:
        raise ValueError(f"Operation with description '{op.desc}' already registered.")

    log.debug("Registered operation with description '%s'.", op.desc)
    _ops_registry[op.desc] = op


def get_op(description: str) -> DescriptiveOp:
    """
    Retrieves an operation based on its description.

    :param description: The description of the operation.
    :return: Instance of DescriptiveOp corresponding to the description.
    :raises OpsError: If no operation matches the description.
    """
    if description not in _ops_registry:
        msg = f"No operation found for description '{description}'. Registered ops: {list_ops()}"
        log.error(msg)
        raise OpsError(msg)
    return _ops_registry[description]


def list_ops() -> list:
    """
    Returns a list of all registered operation descriptions.

    :return: List of operation descriptions.
    """
    return list(_ops_registry.keys())


def pytest_approx(lhs, rhs, rel=None, abs=None, nan_ok=False):
    """Wraps the pytest approx function"""
    return lhs == pytest.approx(rhs, rel, abs, nan_ok)


"""
Register some default operations in to the registry
"""
register_op(DescriptiveOp(operator.eq, "="))
register_op(DescriptiveOp(operator.eq, "=="))
register_op(DescriptiveOp(operator.eq, "is"))
register_op(DescriptiveOp(operator.eq, "is equal to"))

register_op(DescriptiveOp(operator.ne, "!="))
register_op(DescriptiveOp(operator.ne, "is not"))
register_op(DescriptiveOp(operator.ne, "is not equal to"))

register_op(DescriptiveOp(operator.gt, ">"))
register_op(DescriptiveOp(operator.ge, ">="))
register_op(DescriptiveOp(operator.gt, "is greater than"))
register_op(DescriptiveOp(operator.ge, "is greater than or equal to"))

register_op(DescriptiveOp(operator.lt, "<"))
register_op(DescriptiveOp(operator.le, "<="))
register_op(DescriptiveOp(operator.lt, "is less than"))
register_op(DescriptiveOp(operator.le, "is less than or equal to"))

register_op(DescriptiveOp(lambda x, y: x in y, "in"))
register_op(DescriptiveOp(lambda x, y: x in y, "is in"))
register_op(DescriptiveOp(lambda x, y: x not in y, "not in"))
register_op(DescriptiveOp(lambda x, y: x not in y, "is not in"))

register_op(DescriptiveOp(math.isclose, "is close to"))
register_op(DescriptiveOp(math.isclose, "is around"))

register_op(DescriptiveOp(pytest_approx, "~="))
register_op(DescriptiveOp(pytest_approx, "is approximately"))
register_op(DescriptiveOp(pytest_approx, "is approximately equal to"))

register_op(DescriptiveOp(lambda x, y: x % y == 0, "is divisible by"))

register_op(DescriptiveOp(lambda x, y: y in x, "contains"))
register_op(DescriptiveOp(lambda x, y: x.startswith(y), "starts with"))
register_op(DescriptiveOp(lambda x, y: x.endswith(y), "ends with"))

register_op(DescriptiveOp(lambda x: len(x) == 0, "is empty"))
register_op(DescriptiveOp(lambda x, y: len(x) == y, "has length"))

register_op(DescriptiveOp(lambda x: x > 0, "is positive"))
register_op(DescriptiveOp(lambda x: x <= 0, "is not positive"))

register_op(DescriptiveOp(lambda x: x < 0, "is negative"))
register_op(DescriptiveOp(lambda x: x >= 0, "is not negative"))

register_op(DescriptiveOp(lambda x: x is True, "is true"))
register_op(DescriptiveOp(lambda x: x is True, "is True"))
register_op(DescriptiveOp(lambda x: x is False, "is false"))
register_op(DescriptiveOp(lambda x: x is False, "is False"))

register_op(DescriptiveOp(isinstance, "is instance of"))
register_op(DescriptiveOp(hasattr, "has attribute"))
