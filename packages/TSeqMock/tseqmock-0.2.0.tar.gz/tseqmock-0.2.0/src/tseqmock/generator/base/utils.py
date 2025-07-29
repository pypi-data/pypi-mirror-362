#!/usr/bin/env python3
"""
Utility functions for temporal sequence generation.
"""

import logging

LOGGER = logging.getLogger(__name__)


def ensure_calendar_aware_int(list_values, granularity):
    """Validate and convert values for calendar-aware time granularities.

    Ensures that values used with calendar-based granularities
    (MONTH, YEAR) are integers, converting float values when possible
    and raising errors for non-integer floats.

    Args:
        list_values (List[Union[int, float]]): Input values to validate.
        granularity (Granularity): Time granularity to check against.

    Returns:
        List[int]: Converted integer values.

    Raises:
        ValueError: If non-integer float values are provided for
        calendar-based granularities.

    Example:
        # Convert float values for monthly granularity
        values = [1.0, 2.0, 3.5]  # Will raise ValueError
        values = [1.0, 2.0, 3.0]  # Will convert to [1, 2, 3]
    """
    converted = []
    for x in list_values:
        if isinstance(x, float) and not x.is_integer():
            raise ValueError(
                f"Non-integer float value '{x}' is not allowed with "
                f"calendar-based granularity ({granularity})."
            )
        if isinstance(x, float):
            LOGGER.warning(
                "Float value %s will be converted to integer for "
                "calendar-based granularity (%s).",
                x,
                granularity,
            )
            x = int(x)
        converted.append(x)
    return converted
