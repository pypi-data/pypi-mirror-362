from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union
import base64
import binascii
import logging
import re

from .types import FieldType, ValidationError, Widget

logger = logging.getLogger(__name__)


# ---------------------------
# Factory Registry
# ---------------------------
# Mapping of field types to their corresponding classes
FIELD_TYPE_REGISTRY: Dict[str, Callable[..., "BaseField"]] = {}


def register_field_type(type_name: str):
    """
    Decorator to register a field class with a given type name.
    """

    def decorator(cls):
        FIELD_TYPE_REGISTRY[type_name.lower()] = cls
        return cls

    return decorator


# ---------------------------
# BaseField and Subclasses
# ---------------------------
class BaseField:
    """
    Base class for all fields.
    """

    def __init__(
        self,
        name: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = False,
        default: Any = None,
        widget: Optional[Widget] = None,
        ui_options: Optional[Dict[str, Any]] = None,
        placeholder: Optional[str] = None,
        requires: Optional[List[str]] = None,
        **kwargs,
    ):
        self.name = name
        self.title = title or name.replace("_", " ").title()
        self.description = description
        self.required = required
        self.default = default
        self.widget = widget
        self.field_type = FieldType.STRING  # Default field type
        self.ui_options = ui_options or {}
        self.placeholder = placeholder
        self.requires = requires or []
        self.extra = kwargs
        logger.debug(f"Initialized BaseField '{self.name}'")

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Return this field's JSON Schema. Subclasses may override to include additional constraints.
        """
        schema = {
            "type": self.field_type.value,
            "title": self.title,
            "default": self.default,
        }
        if self.description:
            schema["description"] = self.description
        return schema

    def to_ui_schema(self) -> Dict[str, Any]:
        """
        Return this field's UI Schema.
        """
        ui_schema = {}
        if self.widget:
            ui_schema["ui:widget"] = self.widget.value
        if self.description:
            ui_schema["ui:help"] = self.description
        if self.ui_options:
            ui_schema["ui:options"] = self.ui_options
        if self.placeholder is not None:
            ui_schema["ui:placeholder"] = self.placeholder
        return ui_schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate the field's value. Subclasses should override to implement specific validations.
        """
        logger.debug(f"Validating field '{self.name}' with value: {value}")
        if value is None:
            if self.required:
                raise ValidationError(self.name, "Field is required", "required")
            return value
        return value


@register_field_type("text")
class TextField(BaseField):
    """
    Field for text input with optional length and pattern constraints.
    """

    def __init__(
        self,
        name: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(name, **kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
        self.field_type = FieldType.STRING

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        if self.min_length is not None:
            schema["minLength"] = self.min_length
        if self.max_length is not None:
            schema["maxLength"] = self.max_length
        if self.pattern:
            schema["pattern"] = self.pattern
        return schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        value = super().validate(value, form_data)
        if value is not None:
            if not isinstance(value, str):
                raise ValidationError(self.name, "Must be a string", "type")
            if self.min_length is not None and len(value) < self.min_length:
                raise ValidationError(self.name, f"Must be at least {self.min_length} characters", "minLength")
            if self.max_length is not None and len(value) > self.max_length:
                raise ValidationError(self.name, f"Must be at most {self.max_length} characters", "maxLength")
            if self.pattern and not re.match(self.pattern, value):
                raise ValidationError(self.name, f"Does not match pattern {self.pattern}", "pattern")
        return value


@register_field_type("email")
class EmailField(TextField):
    """
    Field for email input, inherits from TextField with a predefined pattern.
    """

    def __init__(self, name: str, **kwargs):
        kwargs.setdefault("widget", Widget.EMAIL)
        kwargs.setdefault("pattern", r"^[^@]+@[^@]+\.[^@]+$")
        super().__init__(name, **kwargs)


@register_field_type("integer")
class IntegerField(BaseField):
    """
    Field for integer input with optional min and max constraints.
    """

    def __init__(self, name: str, minimum: Optional[int] = None, maximum: Optional[int] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.minimum = minimum
        self.maximum = maximum
        self.field_type = FieldType.INTEGER

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        if self.minimum is not None:
            schema["minimum"] = self.minimum
        if self.maximum is not None:
            schema["maximum"] = self.maximum
        return schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        value = super().validate(value, form_data)
        if value is not None:
            if not isinstance(value, int):
                raise ValidationError(self.name, "Must be an integer", "type")
            if self.minimum is not None and value < self.minimum:
                raise ValidationError(self.name, f"Must be >= {self.minimum}", "minimum")
            if self.maximum is not None and value > self.maximum:
                raise ValidationError(self.name, f"Must be <= {self.maximum}", "maximum")
        return value


@register_field_type("number")
class NumberField(BaseField):
    """
    Field for numerical input (integer or float) with optional min and max constraints.
    """

    def __init__(self, name: str, minimum: Optional[float] = None, maximum: Optional[float] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.minimum = minimum
        self.maximum = maximum
        self.field_type = FieldType.NUMBER
        if self.widget is None:
            self.widget = Widget.NUMBER

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        if self.minimum is not None:
            schema["minimum"] = self.minimum
        if self.maximum is not None:
            schema["maximum"] = self.maximum
        return schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        value = super().validate(value, form_data)
        if value is not None:
            if not isinstance(value, (int, float)):
                raise ValidationError(self.name, "Must be a number", "type")
            if self.minimum is not None and value < self.minimum:
                raise ValidationError(self.name, f"Must be >= {self.minimum}", "minimum")
            if self.maximum is not None and value > self.maximum:
                raise ValidationError(self.name, f"Must be <= {self.maximum}", "maximum")
        return value


@register_field_type("date")
class DateField(TextField):
    """
    Field for date input, inherits from TextField with a predefined pattern and format.
    """

    def __init__(self, name: str, **kwargs):
        kwargs.setdefault("widget", Widget.DATE)
        # Default pattern for YYYY-MM-DD
        kwargs.setdefault("pattern", r"^\d{4}-\d{2}-\d{2}$")
        super().__init__(name, **kwargs)
        self.field_type = FieldType.STRING

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        schema["format"] = "date"
        return schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        value = super().validate(value, form_data)
        if value is not None:
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(self.name, "Invalid date", "invalid_date")
        return value


@register_field_type("select")
class SelectField(BaseField):
    """
    Field for selecting options from a predefined list. Supports dynamic choices based on dependencies.
    """

    def __init__(
        self,
        name: str,
        choices: Union[List[Any], Callable[..., List[Any]]],
        depends_on: Optional[Union[str, List[str]]] = None,
        **kwargs,
    ):
        super().__init__(name, requires=depends_on, **kwargs)
        self._choices_provider = choices if callable(choices) else (lambda: choices)
        if isinstance(depends_on, str):
            depends_on = [depends_on]
        self.depends_on = depends_on or []
        self.field_type = FieldType.STRING
        if self.widget is None:
            self.widget = Widget.SELECT

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)

        # Evaluate the dynamic choices each time we build the schema
        choices_list = self.get_choices(current_values)
        if not choices_list:
            schema["enum"] = []
        else:
            # NOTE: These can technically be oneOf fields also, but this is pretty complicated
            # rjsf wants a dict containing  const & title elements, but this seemed uncessairly complicated
            # to do support. For now, we will only support a list of choices (i.e. enums)
            #
            # One way to solve would be to check if the first item is a dict (value/label pairs),
            # and then use "oneOf":
            # if isinstance(choices_list[0], dict):
            #     schema["oneOf"] = [{"const": c["value"], "title": c["label"]} for c in choices_list]
            schema["enum"] = choices_list

        return schema

    def get_choices(self, current_values: Optional[Dict[str, Any]]) -> List[Any]:
        try:
            if self.depends_on and current_values:
                # Gather the relevant parent values
                args = [current_values.get(dep) for dep in self.depends_on]
                result = self._choices_provider(*args)
            else:
                result = self._choices_provider()
            return result or []
        except Exception as e:
            logger.error(f"Error getting choices for field '{self.name}': {e}")
            return []

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate that the selected value is among the allowed choices.
        """
        value = super().validate(value, form_data)

        if value is not None:
            try:
                if self.depends_on and form_data:
                    # Gather the relevant parent values
                    args = [form_data.get(dep) for dep in self.depends_on]
                    full_choices = self._choices_provider(*args)
                else:
                    full_choices = self._choices_provider()

                valid_values = [c["value"] if isinstance(c, dict) else c for c in full_choices]
                if value not in valid_values:
                    raise ValidationError(
                        self.name,
                        f"Invalid choice: {value}. Must be one of: {valid_values}",
                        "enum",
                    )
            except TypeError as e:
                # If the provider required more args than we had
                logger.error(f"SelectField.validate error for field '{self.name}': {e}")
                # Raise to surface the problem
                raise ValidationError(self.name, str(e), "configuration_error") from e

        return value


@register_field_type("file")
class FileField(BaseField):
    """
    Field for uploading a single file as a data URL.
    """

    def __init__(self, name: str, accept: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        if self.widget is None:
            self.widget = Widget.FILE
        self.accept = accept
        self.field_type = FieldType.STRING

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        schema["format"] = "data-url"
        return schema

    def to_ui_schema(self) -> Dict[str, Any]:
        ui_schema = super().to_ui_schema()
        if self.accept:
            opts = ui_schema.setdefault("ui:options", {})
            opts["accept"] = self.accept
        return ui_schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate that the value is a valid data URL with correct Base64 encoding.
        """
        value = super().validate(value, form_data)
        if value is not None:
            if not isinstance(value, str):
                raise ValidationError(self.name, "Must be a data URL string", "type")
            pattern = r"^data:(?P<mime>[\w/-]+);base64,(?P<data>[A-Za-z0-9+/=]+)$"
            m = re.match(pattern, value)
            if not m:
                raise ValidationError(self.name, "Must be a valid data URL", "format")
            try:
                base64.b64decode(m.group("data"), validate=True)
            except binascii.Error:
                raise ValidationError(self.name, "Invalid Base64 encoding", "base64")
        return value


@register_field_type("boolean")
class BooleanField(BaseField):
    """
    Field for boolean input.
    """

    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        if self.widget is None:
            self.widget = Widget.TOGGLE
        self.field_type = FieldType.BOOLEAN

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        schema["type"] = "boolean"
        return schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate that the value is a boolean.
        """
        value = super().validate(value, form_data)
        if value is not None and not isinstance(value, bool):
            raise ValidationError(self.name, "Must be a boolean", "type")
        return value


@register_field_type("files")
class FilesField(BaseField):
    """
    Field for uploading multiple files as data URLs.
    """

    def __init__(self, name: str, accept: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        if self.widget is None:
            self.widget = Widget.FILES
        self.accept = accept
        self.field_type = FieldType.ARRAY

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        schema["type"] = "array"
        schema["items"] = {"type": "string", "format": "data-url"}
        return schema

    def to_ui_schema(self) -> Dict[str, Any]:
        ui_schema = super().to_ui_schema()
        if self.accept:
            opts = ui_schema.setdefault("ui:options", {})
            opts["accept"] = self.accept
        return ui_schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate that the value is a list of valid data URLs.
        """
        value = super().validate(value, form_data)
        if value is not None:
            if not isinstance(value, list):
                raise ValidationError(self.name, "Must be a list of files", "type")
            for idx, file_str in enumerate(value):
                if not isinstance(file_str, str):
                    raise ValidationError(f"{self.name}[{idx}]", "Must be a data URL string", "type")
                if not re.match(r"^data:.*;base64,.*$", file_str):
                    raise ValidationError(f"{self.name}[{idx}]", "Must be a valid data URL", "format")
        return value


@register_field_type("array")
class ArrayField(BaseField):
    """
    Field for handling arrays of items, supporting both fixed and variable lengths.
    """

    def __init__(
        self,
        name: str,
        item: Union[Dict[str, Any], List[Dict[str, Any]]],
        additional_items: Optional[Dict[str, Any]] = None,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        unique_items: bool = False,
        **kwargs,
    ):
        super().__init__(name, **kwargs)
        self.min_items = min_items
        self.max_items = max_items
        self.unique_items = unique_items

        # Distinguish between "fixed items" (list) vs "single schema for items" (dict)
        if isinstance(item, list):
            self.item_list = [create_field(f"{name}_item_{i}", **item_def) for i, item_def in enumerate(item)]
            self.item = None
        else:
            self.item_list = None
            self.item = create_field(f"{name}_item", **item)

        self.additional_items = (
            create_field(f"{name}_additional_item", **additional_items) if additional_items else None
        )

        self.field_type = FieldType.ARRAY

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        schema["type"] = "array"

        if self.item_list:
            # Fixed item list
            schema["items"] = [fld.to_json_schema(current_values) for fld in self.item_list]
            if self.additional_items:
                schema["additionalItems"] = self.additional_items.to_json_schema(current_values)
        else:
            # Single item schema
            schema["items"] = self.item.to_json_schema(current_values) if self.item else {}
            if self.additional_items:
                schema["additionalItems"] = self.additional_items.to_json_schema(current_values)

        if self.min_items is not None:
            schema["minItems"] = self.min_items
        if self.max_items is not None:
            schema["maxItems"] = self.max_items
        if self.unique_items:
            schema["uniqueItems"] = True

        return schema

    def to_ui_schema(self) -> Dict[str, Any]:
        """
        Extend the base UI schema with items and additionalItems if necessary.
        """
        ui_schema = super().to_ui_schema()

        if self.item_list:
            # Fixed item list
            ui_schema["items"] = [fld.to_ui_schema() for fld in self.item_list]
            if self.additional_items:
                ui_schema["additionalItems"] = self.additional_items.to_ui_schema()
        else:
            # Single item schema
            ui_schema["items"] = self.item.to_ui_schema() if self.item else {}
            if self.additional_items:
                ui_schema["additionalItems"] = self.additional_items.to_ui_schema()

        return ui_schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Validate the array, enforcing constraints like min/max items, uniqueness, and item validations.
        """
        value = super().validate(value, form_data)
        if value is not None:
            if not isinstance(value, list):
                raise ValidationError(self.name, "Must be an array", "type")

            # Check min/max items
            if self.min_items is not None and len(value) < self.min_items:
                raise ValidationError(self.name, f"Must have at least {self.min_items} items", "minItems")
            if self.max_items is not None and len(value) > self.max_items:
                raise ValidationError(self.name, f"Must have at most {self.max_items} items", "maxItems")

            # Check unique items
            if self.unique_items:
                seen = set()
                for idx, entry in enumerate(value):
                    try:
                        # Attempt to add the entry to the set; if it's already present, it's a duplicate
                        seen.add(tuple(sorted(entry.items())) if isinstance(entry, dict) else entry)
                    except TypeError:
                        # For unhashable types, convert to string
                        entry_repr = str(entry)
                        if entry_repr in seen:
                            raise ValidationError(self.name, "Must have unique items", "uniqueItems")
                        seen.add(entry_repr)

            # Validate each sub-item
            for idx, subval in enumerate(value):
                if self.item_list:
                    # Fixed items
                    if idx < len(self.item_list):
                        value[idx] = self.item_list[idx].validate(subval, form_data)
                    else:
                        if self.additional_items:
                            value[idx] = self.additional_items.validate(subval, form_data)
                        else:
                            raise ValidationError(f"{self.name}[{idx}]", "Unexpected item", "additionalItems")
                else:
                    # Single item schema
                    if self.item:
                        value[idx] = self.item.validate(subval, form_data)
                    else:
                        raise ValidationError(f"{self.name}[{idx}]", "No item schema", "itemSchema")
        return value


@register_field_type("object")
class ObjectField(BaseField):
    """
    Field for object input, supporting nested properties.
    """

    def __init__(
        self,
        name: str,
        properties: Dict[str, Any],
        required: Optional[list] = None,
        **kwargs,
    ):
        super().__init__(name, **kwargs)
        self.properties = {
            prop_name: create_field(prop_name, **prop_schema) for prop_name, prop_schema in properties.items()
        }
        self.required = required or []
        self.field_type = FieldType.OBJECT if hasattr(FieldType, "OBJECT") else "object"

    def to_json_schema(self, current_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        schema = super().to_json_schema(current_values)
        schema["type"] = "object"
        schema["properties"] = {name: field.to_json_schema(current_values) for name, field in self.properties.items()}
        if self.required:
            schema["required"] = self.required
        return schema

    def validate(self, value: Any, form_data: Optional[Dict[str, Any]] = None) -> Any:
        value = super().validate(value, form_data)
        if value is not None:
            if not isinstance(value, dict):
                raise ValidationError(self.name, "Must be an object", "type")
            for req in self.required:
                if req not in value:
                    raise ValidationError(self.name, f"Missing required property: {req}", "required")
            for name, field in self.properties.items():
                if name in value:
                    value[name] = field.validate(value[name], form_data)
        return value


# ---------------------------
# Factory Function
# ---------------------------
def create_field(name: str, type: str, **kwargs) -> BaseField:
    """
    Factory method to create a field based on its type.

    :param name: The name of the field.
    :param type: The type of the field.
    :param kwargs: Additional keyword arguments for field initialization.
    :return: An instance of a subclass of BaseField.
    :raises ValueError: If the field type is unsupported or required arguments are missing.
    """
    logger.debug(f"Creating field '{name}' of type '{type}' with kwargs {kwargs}")

    # 'string' as an alias for 'text'
    type_key = type.lower()
    if type_key == "string":
        type_key = "text"

    # Handle widget conversion if provided as string
    widget = kwargs.get("widget")
    if isinstance(widget, str):
        widget_key = widget.lower()
        try:
            kwargs["widget"] = Widget[widget_key.upper()]
        except KeyError:
            logger.error(f"Invalid widget type: {widget}. Falling back to default widget 'TEXT'.")
            kwargs["widget"] = Widget.TEXT

    field_class = FIELD_TYPE_REGISTRY.get(type_key)
    if not field_class:
        logger.error(f"Unsupported field type: {type}")
        raise ValueError(f"Unsupported field type: {type}")

    # For 'select' and 'array' types, ensure required arguments are present
    if type_key == "select" and "choices" not in kwargs:
        logger.error("Select fields require 'choices' argument.")
        raise ValueError("Select fields require 'choices' argument.")
    if type_key == "array" and "item" not in kwargs:
        logger.error("Array fields require 'item' argument.")
        raise ValueError("Array fields require 'item' argument.")

    return field_class(name, **kwargs)
