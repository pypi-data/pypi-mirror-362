from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, overload
import asyncio
import logging

from .fields import BaseField, create_field
from .types import ActionExecutionError, ActionResult, ActionValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


class Action:
    """
    Defines an executable action with input validation and schema generation.

    This class wraps a callable (function or method) with metadata, parameter validation,
    and execution management. It supports both synchronous and asynchronous execution
    with timeout handling.

    Example:
        >>> @action("Add Numbers", "Add two numbers")
        ... @action.input("x", type="number", required=True)
        ... @action.input("y", type="number", required=True)
        ... def add(x: int, y: int) -> int:
        ...     return x + y
    """

    __slots__ = ("title", "description", "timeout", "fields", "name", "_func", "_instance", "_field_map")

    def __init__(
        self,
        callable_obj: Callable[..., T],
        title: str,
        description: Optional[str] = None,
        timeout: float = 30.0,
        fields: Optional[List[BaseField]] = None,
        instance: Optional[Any] = None,
    ) -> None:
        """
        Initialize an action with its callable and metadata.

        :param callable_obj: Function or method to execute
        :param title: Human-readable title for the action
        :param description: Optional description of what the action does
        :param timeout: Maximum execution time in seconds
        :param fields: List of input field definitions
        :param instance: Class instance if this is a bound method
        :raises ValueError: If timeout is not positive or title is empty
        :raises TypeError: If callable_obj is async (not supported)
        """
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if timeout <= 0:
            raise ValueError("Timeout must be positive")

        # Reject async functions
        if asyncio.iscoroutinefunction(callable_obj):
            raise TypeError("Async functions are not supported")

        self.title = title
        self.description = description
        self.timeout = timeout
        self.fields = fields or []
        self.name = callable_obj.__name__
        self._func = callable_obj
        self._instance = instance
        self._field_map = {f.name: f for f in self.fields}

    def to_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build a JSON Schema for this action's inputs.

        :param current_values: Optional dict of current form data, used for dynamic choices
        :return: A dictionary representing the JSON Schema
        """
        props = {}
        dependencies = {}

        # Pass current_values into each field, so a SelectField can re-run its choices
        # Reverse the fields to maintain the order of definition
        for field in reversed(self.fields):
            # Some fields (especially SelectField) can use current_values
            # to shape their "enum" or "oneOf" entries
            props[field.name] = field.to_json_schema(current_values)

            # If field has "requires" => property dependencies
            if field.requires:
                dependencies[field.name] = field.requires

        schema = {
            "title": self.title,
            "description": self.description,
            "type": "object",
            "properties": props,
        }

        # Mark required fields in top-level "required"
        required_field_names = [f.name for f in self.fields if f.required]
        if required_field_names:
            schema["required"] = required_field_names

        if dependencies:
            schema["dependencies"] = dependencies

        return schema

    def to_ui_schema(self) -> Dict[str, Any]:
        """
        UI Schema for this action's inputs and provides hints for
        rendering form inputs in a user interface.

        :return: A dictionary representing the UI Schema
        """
        # Reverse the fields to maintain the order of definition
        return {field.name: field.to_ui_schema() for field in reversed(self.fields)}

    def execute(self, **kwargs: Any) -> Union[T, ActionResult]:
        """
        Execute the action with the given parameters.

        Validates all inputs, checks required fields, and executes the underlying
        callable. Only synchronous functions are supported.

        The method handles different return types:
        - Regular values: Returned as-is (success)
        - None: Returned as empty success result
        - ActionResult: Returned as-is (explicit status control)
        - Exceptions: Raised as ActionExecutionError (failure)

        :param kwargs: Keyword arguments to pass to the callable
        :return: Result of the callable execution or ActionResult
        :raises ValidationError: If input validation fails or required fields are missing
        :raises ActionExecutionError: If execution fails
        """
        # Validate inputs
        for name, value in kwargs.items():
            if name not in self._field_map:
                raise ActionValidationError(f"Unknown field: {name}")
            field = self._field_map[name]
            # Pass kwargs as the form_data for dependent validation
            kwargs[name] = field.validate(value, kwargs)

        # Check for missing required
        missing = [f.name for f in self.fields if f.required and f.name not in kwargs]
        if missing:
            raise ActionValidationError(f"Missing required fields: {', '.join(missing)}")

        # Either bound method or function
        func = self._func.__get__(self._instance, self._instance.__class__) if self._instance else self._func

        # Reject async functions
        if asyncio.iscoroutinefunction(func):
            raise ActionExecutionError(f"Action '{self.name}' is async but async functions are not supported")

        try:
            result = func(**kwargs)

            # Handle different return types
            if isinstance(result, ActionResult):
                # Explicit ActionResult - return as-is
                return result
            elif result is None:
                # None result - return empty success
                return ActionResult.success({})
            else:
                # Regular value - return as success
                return ActionResult.success(result)

        except Exception as e:
            logger.error("Error executing action '%s': %s", self.name, str(e))
            raise ActionExecutionError(str(e)) from e

    def __repr__(self) -> str:
        """
        :return: A string representation of the Action
        """
        return f"Action(name='{self.name}', title='{self.title}')"


class ActionDecorator:
    """
    Provides the @action decorator interface for defining actions with input fields.

    This class enables a fluent decorator syntax for creating actions and defining
    their input parameters. It supports both function and method decoration.

    Example:
        >>> @action("Add Numbers", "Add two numbers")
        ... @action.input("x", type="number", required=True)
        ... @action.input("y", type="number", required=True)
        ... def add(x: int, y: int) -> int:
        ...     return x + y

        # Or with keyword arguments:
        >>> @action(title="Add Numbers", description="Add two numbers")
        ... @action.input("x", type="number", required=True)
        ... def add(x: int, y: int) -> int:
        ...     return x + y
    """

    def __init__(self):
        """Initialize the decorator with its input field decorator."""
        self.input = self._input_decorator

    @overload
    def __call__(self, func: F) -> F: ...

    @overload
    def __call__(self, title: str, description: Optional[str] = None, timeout: float = 30.0) -> Callable[[F], F]: ...

    def __call__(
        self,
        title_or_func: Union[str, Callable[..., T], F] = None,
        description: Optional[str] = None,
        timeout: float = 30.0,
        **kwargs: Any,
    ) -> Union[F, Callable[[F], F]]:
        """
        Create an action decorator or decorate a function directly.
        Supports both positional and keyword arguments.

        Can be used as:
            @action
            @action("title")
            @action("title", "description")
            @action(title="title")
            @action(title="title", description="description")

        :param title_or_func: Function to decorate or the action title
        :param description: Optional description of what the action does
        :param timeout: Maximum execution time in seconds
        :param kwargs: Additional keyword arguments (title can be passed here)
        :return: Decorated function or a decorator function
        :raises ValueError: If timeout is not positive or title is invalid
        """
        # Handle keyword argument for title
        if "title" in kwargs:
            if title_or_func is not None:
                raise ValueError("Cannot specify title both positionally and as keyword")
            title_or_func = kwargs.pop("title")

        # Handle @action case (no arguments)
        if title_or_func is None:

            def decorator(func: F) -> F:
                return self._create_action(func, func.__name__.replace("_", " ").title(), description, timeout)

            return decorator

        # Handle @action case (with function)
        if callable(title_or_func):
            return self._create_action(
                title_or_func, title_or_func.__name__.replace("_", " ").title(), description, timeout
            )

        # Handle @action("title") case
        if not isinstance(title_or_func, str) or not title_or_func.strip():
            raise ValueError("Title must be a non-empty string")
        if timeout <= 0:
            raise ValueError("Timeout must be positive")

        def decorator(func: F) -> F:
            return self._create_action(func, title_or_func, description, timeout)

        return decorator

    def _create_action(self, func: F, title: str, description: Optional[str], timeout: float) -> F:
        """
        Create and attach an action to a function.

        :param func: Function to attach action to
        :param title: Action title
        :param description: Action description
        :param timeout: Action timeout
        :return: The decorated function
        :raises TypeError: If the function is async (not supported)
        """
        # Reject async functions during registration
        if asyncio.iscoroutinefunction(func):
            raise TypeError(f"Function '{func.__name__}' is async but async functions are not supported")

        fields = getattr(func, "_action_fields", [])
        action = Action(func, title, description, timeout, fields)

        func._action = action
        func._action_fields = fields

        # Auto-register with global registry (functions and static methods only)
        try:
            from zelos_sdk._actions import get_global_actions_registry

            registry = get_global_actions_registry()

            # Check if this is a method (has class in qualname)
            if hasattr(func, "__qualname__") and "." in func.__qualname__:
                # This is a method - check if it's a static method
                is_static = isinstance(func, staticmethod)

                if is_static:
                    # This is a static method, auto-register it with class prefix
                    action_name = func.__qualname__.replace(".", "/")
                    registry.register(func, name=action_name)
                    logger.debug(f"Auto-registered static method action: {action_name}")
                else:
                    # This is an instance method - don't auto-register, needs instance
                    logger.debug(f"Skipping auto-registration for instance method {func.__qualname__} (needs instance)")
            else:
                # This is a regular function, auto-register it
                registry.register(func)
                logger.debug(f"Auto-registered function action: {func.__name__}")
        except Exception as e:
            logger.warning(f"Failed to auto-register action {func.__name__}: {e}")

        return func

    @staticmethod
    def _input_decorator(name: str, type: str = "text", **kwargs: Any) -> Callable[[F], F]:
        """
        Define an input field for an action.

        :param name: Name of the input field
        :param type: Type of the input field
        :param kwargs: Additional field configuration
        :return: Decorator function that will add the field
        :raises ValueError: If field name or type is invalid
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Field name must be a non-empty string")
        if not isinstance(type, str) or not type.strip():
            raise ValueError("Field type must be a non-empty string")

        def decorator(func: F) -> F:
            if not hasattr(func, "_action_fields"):
                func._action_fields = []
            field = create_field(name, type, **kwargs)
            func._action_fields.append(field)
            return func

        return decorator
