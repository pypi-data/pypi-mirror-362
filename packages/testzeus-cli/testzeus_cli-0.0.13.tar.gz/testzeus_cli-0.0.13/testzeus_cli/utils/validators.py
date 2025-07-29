"""
Input validation utilities for TestZeus CLI.
"""

from typing import Dict, List, Optional, TypeVar

T = TypeVar("T")


def validate_required_arg(value: Optional[T], name: str) -> T:
    """
    Validate that a required argument is provided

    Args:
        value: Argument value to validate
        name: Name of the argument for error message

    Returns:
        The value if valid

    Raises:
        ValueError: If the value is None
    """
    if value is None:
        raise ValueError(f"Required argument '{name}' is missing")
    return value


def validate_id(id_value: str, entity_type: str = "entity") -> str:
    """
    Validate that an ID is in the correct format for PocketBase

    Args:
        id_value: ID value to validate
        entity_type: Type of entity for error message

    Returns:
        The validated ID

    Raises:
        ValueError: If the ID is invalid
    """
    if (
        not id_value
        or not isinstance(id_value, str)
        or len(id_value) != 15
        or not id_value.isalnum()
    ):
        raise ValueError(
            f"Invalid {entity_type} ID: must be 15 alphanumeric characters"
        )
    return id_value.strip()


def parse_key_value_pairs(pairs: List[str]) -> Dict[str, str]:
    """
    Parse a list of key=value pairs into a dictionary

    Args:
        pairs: List of strings in 'key=value' format

    Returns:
        Dictionary of parsed key-value pairs

    Raises:
        ValueError: If any pair doesn't follow the key=value format
    """
    result = {}
    for pair in pairs:
        try:
            key, value = pair.split("=", 1)
            result[key.strip()] = value.strip()
        except ValueError:
            raise ValueError(
                f"Invalid format for key-value pair: '{pair}'. Expected 'key=value'"
            )
    return result
