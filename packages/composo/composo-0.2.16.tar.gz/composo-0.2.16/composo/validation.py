"""
Type validation utilities for chat session types
"""

from typing import (
    Iterable as IterableType,
    List,
    get_args,
    get_origin,
    Any,
    Type,
    Union,
    Tuple,
)
from deepdiff import DeepDiff
from pydantic import TypeAdapter, ValidationError
from collections.abc import Iterable as IterableABC


def normalize_iterables(typ: Type[Any]) -> Type[Any]:
    """
    Pydantic's TypeAdapter does not handle the Iterable type correctly, so we cast it to List using this function.
    """
    origin = get_origin(typ)
    args = get_args(typ)

    if origin is IterableType or origin is IterableABC:
        return List[normalize_iterables(args[0])]

    if origin is Union:
        return Union[tuple(normalize_iterables(arg) for arg in args)]

    return typ


def validate_raw_chat_conforms_to_type(
    data: object, type_to_validate: Type[Any]
) -> Tuple[bool, str]:
    """
    Validate data against a type and return validation result with error message.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        - If valid: (True, "")
        - If invalid: (False, detailed_error_message)
    """
    try:
        adjusted_type = normalize_iterables(type_to_validate)
        adapter = TypeAdapter(adjusted_type)

        # Parse using Pydantic
        parsed = adapter.validate_python(data)

        # Convert back to Python-native data (dict/list)
        parsed_back_to_dict = adapter.dump_python(parsed, mode="json")

        diff = DeepDiff(parsed_back_to_dict, data, verbose_level=2)

        # Deep compare input and parsed-back version
        if diff == {}:
            return True, ""
        else:
            return False, diff.pretty()

    except ValidationError as e:
        return False, f"Unexpected validation error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error during validation: {str(e)}"
