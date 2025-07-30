"""
Actions system for Zelos SDK

This module provides a comprehensive action definition, registration, and execution system.
"""

import logging

# Import Rust bindings
from zelos_sdk._actions import (
    ActionsClient as ActionsClient,
)
from zelos_sdk._actions import (
    ActionsRegistry as ActionsRegistry,
)
from zelos_sdk._actions import (
    get_global_actions_client as get_global_actions_client,
)
from zelos_sdk._actions import (
    get_global_actions_registry as get_global_actions_registry,
)
from zelos_sdk._actions import (
    init_global_actions_client as init_global_actions_client,
)
from zelos_sdk._actions import (
    init_global_actions_registry as init_global_actions_registry,
)

from .core import (
    Action,
    ActionDecorator,
)
from .discovery import discover_actions
from .fields import (
    ArrayField,
    BaseField,
    BooleanField,
    DateField,
    EmailField,
    FileField,
    FilesField,
    IntegerField,
    NumberField,
    SelectField,
    TextField,
    create_field,
    register_field_type,
)
from .types import (
    ActionExecutionError,
    ActionResult,
    ActionValidationError,
    ExecuteStatus,
    FieldType,
    ValidationError,
    Widget,
)

logger = logging.getLogger(__name__)

# Globals
action = ActionDecorator()
actions_registry = get_global_actions_registry()
discover_actions(registry=actions_registry)

__all__ = [
    "action",
    "actions_registry",
    "discover_actions",
    "init_global_actions_registry",
    "get_global_actions_registry",
    "Action",
    "ActionRegistry",
    "ActionsClient",
    "ActionValidationError",
    "ActionExecutionError",
    "ValidationError",
    "ActionResult",
    "ExecuteStatus",
    "FieldType",
    "Widget",
    "BaseField",
    "TextField",
    "EmailField",
    "IntegerField",
    "NumberField",
    "DateField",
    "SelectField",
    "FileField",
    "BooleanField",
    "FilesField",
    "ArrayField",
    "create_field",
    "register_field_type",
]
