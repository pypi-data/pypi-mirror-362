from typing import Any, Dict
import enum

# Import Rust types from the native module
try:
    from zelos_sdk._actions import ActionResult as RustActionResult
    from zelos_sdk._actions import ExecuteStatus as RustExecuteStatus

    _RUST_TYPES_AVAILABLE = True
except ImportError:
    _RUST_TYPES_AVAILABLE = False


class ExecuteStatus(enum.Enum):
    """Enumeration of action execution status values."""

    PASS = "PASS"
    FAIL = "FAIL"


class ActionResult:
    """
    Result wrapper for action execution that includes both the result value and execution status.

    This class provides a clean way to return explicit success/failure results from actions
    while maintaining the simple return patterns for most use cases.

    When Rust types are available, this class wraps the native Rust ActionResult.
    """

    def __init__(self, value: Any, status: ExecuteStatus):
        """
        Initialize an ActionResult.

        Args:
            value: The result value (can be any JSON-serializable type)
            status: The execution status (PASS or FAIL)
        """
        if _RUST_TYPES_AVAILABLE:
            # Use Rust types when available
            rust_status = RustExecuteStatus.Pass if status == ExecuteStatus.PASS else RustExecuteStatus.Fail
            self._rust_result = RustActionResult(value, rust_status)
            self.value = value
            self.status = status
        else:
            # Fallback to pure Python implementation
            self.value = value
            self.status = status
            self._rust_result = None

    @classmethod
    def success(cls, value: Any) -> "ActionResult":
        """Create a successful result."""
        return cls(value, ExecuteStatus.PASS)

    @classmethod
    def failure(cls, value: Any) -> "ActionResult":
        """Create a failure result."""
        return cls(value, ExecuteStatus.FAIL)

    @classmethod
    def error(cls, value: Any) -> "ActionResult":
        """Create an error result."""
        return cls(value, ExecuteStatus.FAIL)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"value": self.value, "status": self.status.value}

    def __repr__(self) -> str:
        return f"ActionResult(value={self.value!r}, status={self.status.value})"


class FieldType(enum.Enum):
    """Enumeration of supported field types for action inputs."""

    ARRAY = "array"
    BINARY = "string"
    BOOLEAN = "boolean"
    DATE = "string"
    DATE_TIME = "string"
    EMAIL = "string"
    INTEGER = "integer"
    NULL = "null"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"
    TIME = "string"
    URI = "string"
    UUID = "string"

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Check if a value is a valid field type."""
        return value in [item.value for item in cls]


class Widget(enum.Enum):
    """
    Enumeration of supported UI widgets for action inputs.

    Widgets are grouped by their primary type and usage.
    """

    # Text Input Widgets
    TEXT = "TextWidget"
    TEXTAREA = "TextareaWidget"
    EMAIL = "EmailWidget"
    URL = "URLWidget"
    PASSWORD = "PasswordWidget"

    # Numeric Widgets
    NUMBER = "NumberWidget"
    UPDOWN = "UpDownWidget"
    RANGE = "RangeWidget"

    # Selection Widgets
    SELECT = "SelectWidget"
    RADIO = "RadioWidget"
    CHECKBOX = "CheckboxWidget"
    TOGGLE = "ToggleWidget"
    MULTI_SELECT = "MultiSelectWidget"

    # Date/Time Widgets
    DATE = "DateWidget"
    TIME = "TimeWidget"
    DATE_TIME = "DateTimeWidget"

    # File Widgets
    FILE = "FileWidget"
    FILES = "FilesWidget"

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Check if a value is a valid widget type."""
        return value in [item.value for item in cls]


class ValidationError(Exception):
    """
    Exception raised for validation errors in fields.

    :param field_name: The name of the field where validation failed.
    :param message: Description of the validation error.
    :param code: Error code categorizing the type of validation error.
    """

    def __init__(self, field_name: str, message: str, code: str = "invalid"):
        super().__init__(f"{field_name}: {message}")
        self.field_name = field_name
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"{self.field_name}: {self.message} ({self.code})"


class ActionValidationError(Exception):
    """Exception raised for validation errors in actions."""


class ActionExecutionError(Exception):
    """Exception raised when executing an action fails."""


class ActionDiscoveryError(Exception):
    """Base exception for action discovery errors."""


class ActionImportError(ActionDiscoveryError):
    """Raised when an action target cannot be imported."""


class ActionRegistrationError(ActionDiscoveryError):
    """Raised when an action cannot be registered."""
