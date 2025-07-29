from __future__ import annotations
from typing import TypedDict, Literal, Union, Sequence, Any


class TableColumnFilterRule(TypedDict):
    """
    A single filter that is applied to a table column. For example: revenue > 1000.

    Required properties:
    - `operator`: The operator to use for the filter.
    - `value`: The value to filter by.
    - `key`: The key of the column to filter by.
    """

    operator: Literal[
        "is",
        "is_not",
        "includes",
        "not_includes",
        "greater_than",
        "greater_than_or_equal",
        "less_than",
        "less_than_or_equal",
        "is_empty",
        "is_not_empty",
        "has_any",
        "not_has_any",
        "has_all",
        "not_has_all",
    ]
    value: Any
    key: str


SNAKE_TO_CAMEL_CASE_OPERATOR_MAP = {
    "is": "is",
    "is_not": "isNot",
    "includes": "includes",
    "not_includes": "notIncludes",
    "greater_than": "greaterThan",
    "greater_than_or_equal": "greaterThanOrEqual",
    "less_than": "lessThan",
    "less_than_or_equal": "lessThanOrEqual",
    "is_empty": "isEmpty",
    "is_not_empty": "isNotEmpty",
    "has_any": "hasAny",
    "not_has_any": "notHasAny",
    "has_all": "hasAll",
    "not_has_all": "notHasAll",
}

CAMEL_TO_SNAKE_CASE_OPERATOR_MAP = {
    "is": "is",
    "isNot": "is_not",
    "includes": "includes",
    "notIncludes": "not_includes",
    "greaterThan": "greater_than",
    "greaterThanOrEqual": "greater_than_or_equal",
    "lessThan": "less_than",
    "lessThanOrEqual": "less_than_or_equal",
    "isEmpty": "is_empty",
    "isNotEmpty": "is_not_empty",
    "hasAny": "has_any",
    "notHasAny": "not_has_any",
    "hasAll": "has_all",
    "notHasAll": "not_has_all",
}


class FilterModelFormat:
    SNAKE: Literal["snake"] = "snake"
    CAMEL: Literal["camel"] = "camel"
    TYPE = Literal["snake", "camel"]


class TableColumnFilterGroup(TypedDict):
    """
    A group of filters that are applied to a table column. For example: (revenue > 1000) AND (revenue < 2000).

    Required properties:
    - `logic_operator`: The operator to use for the group. Either `"and"` or `"or"`.
    - `filters`: A list of filter rules or sub-groups to apply to the group.
    """

    logic_operator: Literal["and", "or"]
    filters: Sequence[Union[TableColumnFilterRule, TableColumnFilterGroup]]


TableColumnFilterModel = Union[TableColumnFilterRule, TableColumnFilterGroup, None]
"""
A filter model describes how to filter a table based on either a filter rule or group, which
is a collection of filter rules or sub-groups that can be nested to arbitrary depth.

For example:
- `TableColumnFilterRule`: revenue > 1000
- `TableColumnFilterGroup`: (revenue > 1000) AND (revenue < 2000)
- `TableColumnFilterGroup`: ((revenue > 1000) AND (revenue < 2000)) OR ((revenue > 3000) AND (revenue < 4000))
"""


def transform_advanced_filter_model(
    filter_model: TableColumnFilterModel, result_format: FilterModelFormat.TYPE
) -> TableColumnFilterModel:
    """
    Recursively transforms a TableColumnFilterModel from either snake_case to
    camelCase or camelCase to snake_case

    Specifically transforms:
    - 'logic_operator' key to 'logicOperator', or vice-versa
    - 'operator' key's value from snake_case to camelCase (e.g., 'is_not' to 'isNot'), or vice-versa

    Leaves 'key' and 'value' fields untouched.

    Args:
        filter_model: The filter model dictionary (or None).
        result_format: either 'snake' or 'camel'

    Returns:
        A new dictionary with transformed keys/values, or None if input is None
        or an error occurs during transformation.
    """
    if filter_model is None:
        return None

    try:
        result_logic_operator_key = (
            "logic_operator"
            if result_format == FilterModelFormat.SNAKE
            else "logicOperator"
        )
        input_logic_operator_key = (
            "logicOperator"
            if result_format == FilterModelFormat.SNAKE
            else "logic_operator"
        )

        # Check if it's a group (has 'logic_operator')
        # Note: Using .get() for runtime safety, although TypedDict defines keys
        if input_logic_operator_key in filter_model:
            transformed_filters: list[
                Union[TableColumnFilterRule, TableColumnFilterGroup]
            ] = []

            for f in filter_model.get("filters", []):  # type: ignore
                # Recursively transform nested filters
                transformed_filter = transform_advanced_filter_model(f, result_format)

                if transformed_filter is None:
                    # Propagate failure if a sub-transformation fails
                    return None

                transformed_filters.append(transformed_filter)

            new_filter_group: TableColumnFilterGroup = {
                result_logic_operator_key: filter_model.get(  # type: ignore
                    input_logic_operator_key, "and"
                ),
                "filters": transformed_filters,
            }

            return new_filter_group
        # Check if it's a clause (has 'operator')
        elif "operator" in filter_model:
            original_operator: str = filter_model.get("operator")  # type: ignore

            # Map the operator value to camelCase
            result_format_operator = (
                SNAKE_TO_CAMEL_CASE_OPERATOR_MAP.get(original_operator)
                if result_format == FilterModelFormat.CAMEL
                else CAMEL_TO_SNAKE_CASE_OPERATOR_MAP.get(original_operator)
            )

            if result_format_operator is None:
                # This indicates an invalid operator value not covered by the Literal type
                # or the map, treat as an error.
                raise ValueError(
                    f"Unknown or unmapped operator value: {original_operator}"
                )

            return {
                "operator": result_format_operator,  # type: ignore
                "value": filter_model.get("value"),
                "key": filter_model.get("key"),  # type: ignore
            }
        else:
            # Should not happen with valid TableColumnFilterModel input
            raise TypeError(
                "Input dictionary is neither a TableColumnFilterClause nor a TableColumnFilterGroup"
            )

    except Exception:
        # Return None if any error occurs during processing
        return None


def transform_advanced_filter_model_to_camel_case(
    filter_model: TableColumnFilterModel,
) -> TableColumnFilterModel:
    return transform_advanced_filter_model(
        filter_model, result_format=FilterModelFormat.CAMEL
    )


def transform_advanced_filter_model_to_snake_case(
    filter_model: TableColumnFilterModel,
) -> TableColumnFilterModel:
    return transform_advanced_filter_model(
        filter_model, result_format=FilterModelFormat.SNAKE
    )
