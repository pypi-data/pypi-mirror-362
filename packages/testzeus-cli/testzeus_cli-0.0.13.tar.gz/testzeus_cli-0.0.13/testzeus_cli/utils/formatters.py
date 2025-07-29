"""
Output formatting utilities for TestZeus CLI.
"""

import json
import yaml
from typing import Any, Dict, List, Optional, Set
from rich.console import Console
from rich.table import Table

console = Console()

# Fields to completely exclude from display
EXCLUDED_FIELDS = {
    "collectionId",
    "collection",
    "collectionName",
    "collection_id",
    "collection_name",
}


def format_output(data: Any, format_type: str = "table") -> None:
    """
    Format and print output based on the specified format type

    Args:
        data: Data to format (dict, list, or primitive)
        format_type: Output format type ("table", "json", or "yaml")
    """
    if format_type == "json":
        # Use regular print() for JSON to avoid Rich console formatting that can corrupt JSON
        print(json.dumps(data, indent=2, default=format_object_for_json))
    elif format_type == "yaml":
        console.print(yaml.dump(data, sort_keys=False, default_flow_style=False))
    else:  # table format
        if isinstance(data, dict):
            format_dict_as_table(data)
        elif isinstance(data, list):
            format_list_as_table(data)
        else:
            # Simple value, just print it
            console.print(str(data))


def format_object_for_json(obj: Any) -> Any:
    """
    Format complex objects for JSON serialization

    Args:
        obj: Object to format

    Returns:
        JSON serializable representation of the object
    """
    # If the object has a data property (like SDK models)
    if hasattr(obj, "data") and isinstance(obj.data, dict):
        return _ensure_json_serializable(obj.data)

    # If the object has __dict__
    if hasattr(obj, "__dict__"):
        return _ensure_json_serializable(obj.__dict__)

    # Default to string representation
    return str(obj)


def _ensure_json_serializable(obj: Any) -> Any:
    """
    Recursively ensure an object is JSON serializable
    
    Args:
        obj: Object to make JSON serializable
        
    Returns:
        JSON serializable representation
    """
    if isinstance(obj, dict):
        return {key: _ensure_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_ensure_json_serializable(item) for item in obj]
    elif isinstance(obj, str):
        # Ensure proper string handling - strings should be returned as-is
        # Python's json.dumps will handle proper escaping
        return obj
    elif isinstance(obj, (int, float, bool)) or obj is None:
        # Primitives that are JSON serializable
        return obj
    elif hasattr(obj, "data") and isinstance(obj.data, dict):
        return _ensure_json_serializable(obj.data)
    elif hasattr(obj, "__dict__"):
        return _ensure_json_serializable(obj.__dict__)
    else:
        # Convert everything else to string
        return str(obj)


def format_value_for_display(value: Any) -> str:
    """
    Format a value for display in table output

    Args:
        value: Value to format

    Returns:
        String representation suitable for display
    """
    # If value is a dictionary with id/name fields, show a friendly representation
    if isinstance(value, dict) and "id" in value:
        if "name" in value:
            return f"{value['name']} ({value['id']})"
        return f"ID: {value['id']}"

    # If value is a list of dictionaries with ids, summarize
    if (
        isinstance(value, list)
        and value
        and all(isinstance(x, dict) and "id" in x for x in value)
    ):
        if len(value) == 1 and "name" in value[0]:
            return f"{value[0]['name']} ({value[0]['id']})"
        return f"{len(value)} items"

    # If value is a list of strings
    if isinstance(value, list) and value and all(isinstance(x, str) for x in value):
        if len(value) <= 3:
            return ", ".join(value)
        return f"{len(value)} items: {', '.join(value[:2])}..."

    # If value has a data attribute
    if hasattr(value, "data") and isinstance(value.data, dict):
        data = value.data
        if "name" in data and "id" in data:
            return f"{data['name']} ({data['id']})"
        elif "id" in data:
            return f"ID: {data['id']}"

    # Format nested structures
    if isinstance(value, dict) or isinstance(value, list):
        try:
            json_str = json.dumps(value, default=format_object_for_json)
            if len(json_str) > 50 and not (isinstance(value, dict) and "id" in value):
                return f"{json_str[:50]}..."
            return json_str
        except Exception as e:
            print(f"Error formatting value for display: {e}")
            return str(value)

    # Default string representation
    return str(value)


def format_dict_as_table(data: Dict[str, Any], title: Optional[str] = None) -> None:
    """
    Format a dictionary as a table

    Args:
        data: Dictionary to format
        title: Optional table title
    """
    # Special handling for paginated responses
    if "items" in data and isinstance(data["items"], list):
        # Print pagination info
        if "page" in data and "per_page" in data and "total_items" in data:
            console.print(
                f"Page {data['page']} of {(data['total_items'] + data['per_page'] - 1) // data['per_page']} "
                f"(showing {len(data['items'])} of {data['total_items']} items)"
            )

        # Format the items
        format_list_as_table(data["items"], title)
        return

    # Standard dictionary rendering
    table = Table(title=title)
    table.add_column("Key", style="cyan")
    table.add_column("Value")

    for key, value in data.items():
        # Skip excluded fields
        if key.lower() in EXCLUDED_FIELDS or any(
            excluded in key.lower() for excluded in EXCLUDED_FIELDS
        ):
            continue

        # Format the value for display
        value_str = format_value_for_display(value)
        table.add_row(key, value_str)

    console.print(table)


def format_list_as_table(data: List[Any], title: Optional[str] = None) -> None:
    """
    Format a list as a table

    Args:
        data: List to format
        title: Optional table title
    """
    if not data:
        console.print("[yellow]No data available[/yellow]")
        return

    # Get all keys from all dictionaries
    all_keys: Set[str] = set()
    for item in data:
        if isinstance(item, dict):
            all_keys.update(item.keys())
        elif hasattr(item, "data") and isinstance(item.data, dict):
            all_keys.update(item.data.keys())

    # Remove excluded fields
    for field in list(all_keys):
        if field.lower() in EXCLUDED_FIELDS or any(
            excluded in field.lower() for excluded in EXCLUDED_FIELDS
        ):
            all_keys.discard(field)

    # If list of dictionaries
    if all_keys:
        # Create table with columns for each key
        table = Table(title=title, show_lines=True)

        # Keep table manageable - use most common/important fields
        # Prioritize certain fields - order determines display order
        priority_fields = [
            "id",
            "name",
            "status",
            "created",
            "updated",
            "start_time",
            "end_time",
            "test",  # Add test reference
            "duration",  # Add test duration
            "tenant",  # Add tenant reference
        ]

        # Limit max columns to make output more readable
        max_display_columns = 6  # Reduce from 10 to 6 for better readability

        # First ensure we have id and name if they exist
        filtered_keys = set()
        for key in ["id", "name"]:
            if key in all_keys:
                filtered_keys.add(key)

        # Then add other priority fields until we reach the limit
        for key in priority_fields:
            if (
                key in all_keys
                and key not in filtered_keys
                and len(filtered_keys) < max_display_columns
            ):
                filtered_keys.add(key)

        # If we still have room, add some non-priority fields
        if len(filtered_keys) < max_display_columns:
            remaining_keys = sorted(list(all_keys - filtered_keys))
            remaining_keys = remaining_keys[: max_display_columns - len(filtered_keys)]
            filtered_keys.update(remaining_keys)

        # Sort columns with priority fields first
        columns = sorted(
            filtered_keys,
            key=lambda x: (priority_fields.index(x) if x in priority_fields else 999,),
        )

        # Add columns to table with appropriate width for IDs
        for key in columns:
            if key == "id":
                # For ID column: full width, no wrap, no justify
                table.add_column("ID", min_width=30, max_width=30, no_wrap=True)
            elif key == "name":
                # For name column: more space, allow wrap
                table.add_column("Name", min_width=40, max_width=40, overflow="fold")
            elif key == "status":
                # For status: smaller fixed width
                table.add_column("Status", min_width=10, max_width=10, justify="center")
            else:
                # For other columns: standard format
                table.add_column(key.capitalize(), width=20, overflow="ellipsis")

        # Add rows
        for item in data:
            # Handle both dict items and objects with data attribute
            item_data = item
            if hasattr(item, "data") and isinstance(item.data, dict):
                item_data = item.data

            if isinstance(item_data, dict):
                # Extract values for each column
                row_values = []
                for key in columns:
                    if key in item_data:
                        value = item_data.get(key, "")
                        # Format for display
                        formatted_value = format_value_for_display(value)
                        # For IDs, don't truncate
                        if key == "id" and value:
                            formatted_value = str(value)
                    else:
                        formatted_value = ""
                    row_values.append(formatted_value)

                table.add_row(*row_values)
            else:
                # Item isn't a dict, just add as a single column
                table.add_row(str(item))

        console.print(table)
    else:
        # Simple list of primitive values
        table = Table(title=title)
        table.add_column("Value")

        for item in data:
            table.add_row(str(item))

        console.print(table)


def should_print_message(format_type: str) -> bool:
    """
    Check if messages should be printed based on format type.
    
    Args:
        format_type: Output format type ("table", "json", or "yaml")
        
    Returns:
        True if messages should be printed, False if format is json
    """
    return format_type != "json"


def print_message(message: str, format_type: str) -> None:
    """
    Print a message only if the format is not json.
    
    Args:
        message: Message to print
        format_type: Output format type
    """
    if should_print_message(format_type):
        console.print(message)
