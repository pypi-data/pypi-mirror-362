"""
Action discovery system for automatically finding and registering actions from entry points.
"""

from typing import Any, Dict, List, Type, Union
import importlib
import importlib.metadata
import inspect
import logging

from . import ActionsRegistry
from .types import ActionDiscoveryError, ActionImportError, ActionRegistrationError

logger = logging.getLogger(__name__)


def import_target(target_str: str) -> Union[Type[Any], Any]:
    """
    Import a target specified as a string.

    The target can be specified either as a module path or as a module path with
    an attribute (separated by ':'). For example:
        - "my_package.actions"
        - "my_package.devices:Thermostat"

    :param target_str: String specification of import target
    :return: Imported class/function/object
    :raises ActionImportError: If the target cannot be imported
    """
    try:
        if ":" in target_str:
            module_path, attribute = target_str.split(":", 1)
        else:
            module_path, attribute = target_str, None

        # Validate inputs
        if not module_path or not isinstance(module_path, str):
            raise ValueError("Module path must be a non-empty string")
        if attribute is not None and not isinstance(attribute, str):
            raise ValueError("Attribute must be a string if specified")

        # Attempt import
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ActionImportError(f"Could not import module '{module_path}': {e}")

        if attribute:
            if not hasattr(module, attribute):
                raise ActionImportError(f"Module '{module_path}' has no attribute '{attribute}'")
            return getattr(module, attribute)
        return module

    except Exception as e:
        # Convert any other exceptions to ActionImportError
        if not isinstance(e, ActionImportError):
            raise ActionImportError(f"Error importing '{target_str}': {e}") from e
        raise


def register_module_actions(module: Any, service_name: str, registry: ActionsRegistry) -> Dict[str, List[str]]:
    """
    Register all actions found in a module.

    Scans the module for:
    1. Functions decorated with @action
    2. Pre-instantiated objects with action methods

    :param module: Module to scan for actions
    :param service_name: Service name to register actions under
    :return: Dictionary mapping types to lists of registered action names
    :raises ActionRegistrationError: If registration fails critically
    """
    if not module:
        raise ActionRegistrationError("Module cannot be None")
    if not service_name or not isinstance(service_name, str):
        raise ActionRegistrationError("Service name must be a non-empty string")
    if not hasattr(module, "__name__"):
        raise ActionRegistrationError("Module must have a __name__ attribute")

    try:
        registered = {
            "functions": [],  # Standalone functions
            "instances": [],  # Pre-instantiated class instances
        }

        # Get all module members once for performance
        members = inspect.getmembers(module)

        # First pass: collect all classes with action methods
        action_classes = {
            name: cls
            for name, cls in members
            if inspect.isclass(cls) and any(hasattr(value, "_action") for value in cls.__dict__.values())
        }

        # Second pass: register everything
        for name, obj in members:
            # Skip private members
            if name.startswith("_"):
                continue

            try:
                # Case 1: Standalone functions with @action decorator
                if inspect.isfunction(obj) and hasattr(obj, "_action"):
                    registry.register(obj, name=f"{service_name}/{name}")
                    registered["functions"].append(f"{service_name}/{name}")
                    logger.debug(f"Registered function action: {service_name}/{name}")
                    continue

                # Case 2: Pre-instantiated objects with action methods
                if isinstance(obj, tuple(action_classes.values())):
                    registry.register(obj, name=service_name)
                    registered["instances"].append(f"{service_name}/{name}")
                    logger.debug(f"Registered instance action: {service_name}/{name}")
                    continue

            except Exception as e:
                logger.warning(f"Error registering {name}: {str(e)}", exc_info=True)
                continue

        # Log registration summary
        total = sum(len(items) for items in registered.values())
        if total > 0:
            logger.debug(
                f"Registered {total} actions from {service_name}: "
                f"{len(registered['functions'])} functions, "
                f"{len(registered['instances'])} instances"
            )
        else:
            logger.warning(f"No actions found in module: {module.__name__}")

        return registered

    except Exception as e:
        raise ActionRegistrationError(f"Critical error registering actions from {module.__name__}: {str(e)}") from e


def discover_actions(
    entry_point_group: str = "zelos_sdk.actions", skip_errors: bool = True, registry: ActionsRegistry = None
) -> Dict[str, List[str]]:
    """
    Discover and register all actions from entry points.

    :param entry_point_group: Entry point group to scan for actions
    :param skip_errors: If True, continue after errors; if False, raise exceptions
    :return: Dictionary mapping entry point names to lists of registered actions
    :raises ActionDiscoveryError: If discovery fails and skip_errors is False
    """
    registered_actions = {}

    try:
        entry_points = list(importlib.metadata.entry_points(group=entry_point_group))
        if not entry_points:
            logger.debug(f"No entry points found in group '{entry_point_group}'")
            return registered_actions

        for entry_point in entry_points:
            try:
                logger.debug(f"Loading actions from {entry_point.name}")

                # Import and validate the target
                target = import_target(entry_point.module)

                # Register actions based on target type
                if inspect.ismodule(target):
                    registered = register_module_actions(target, entry_point.name, registry)
                    if any(actions for actions in registered.values()):
                        registered_actions[entry_point.name] = registered
                        logger.debug(f"Successfully loaded actions from {entry_point.name}: {registered}")
                    else:
                        logger.debug(f"No actions found in module: {entry_point.module}")
                else:
                    registry.register(entry_point.name, target)
                    registered_actions[entry_point.name] = ["direct"]
                    logger.debug(f"Successfully loaded direct action from {entry_point.name}")

            except Exception as e:
                msg = f"Error loading actions from {entry_point.name}: {e}"
                if skip_errors:
                    logger.error(msg, exc_info=True)
                else:
                    raise ActionDiscoveryError(msg) from e

        return registered_actions

    except Exception as e:
        msg = f"Action discovery failed: {e}"
        if skip_errors:
            logger.error(msg, exc_info=True)
            return registered_actions
        raise ActionDiscoveryError(msg) from e
