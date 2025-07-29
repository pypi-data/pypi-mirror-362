#!/usr/bin/env python3
"""
Profile configuration for temporal sequence generation.
"""

from typing import Union, Optional

from pydantic import field_validator
from pydantic.dataclasses import dataclass, Field
from pypassist.dataclass.decorators.viewer import viewer
from pypassist.fallback.typing import List, Dict

from ...distribution.base import Distribution
from ...method.base import GenMethod


@viewer
@dataclass
class Profile:
    """Configuration profile for generating temporal sequences.

    Defines generation parameters for mock data sequences.

    Args:
        n_seq (int, optional): Number of sequences to generate.
            Defaults to 10.
        sequence_size (Union[int, List[int], str, Distribution], optional):
            Sequence length configuration.
            - int: Fixed length for all sequences
            - List[int]: Variable lengths per sequence
            - str: Distribution name for random lengths
            - Distribution: Custom length distribution
            Defaults to 5.
        data_cols (Dict[str, Union[str, GenMethod]], optional):
            Generation method for each data column.
            - str: Method name from registry
            - GenMethod: Custom generation method
            Defaults to random generation.
        missing_data (Dict[str, float], optional):
            Percentage of missing data per column (0-1 range).
        profile_id (str, optional):
            Unique identifier for the profile.

    Raises:
        ValueError: If missing data or sequence size is invalid.

    Example:
        Profile(
            n_seq=5,
            sequence_size=10,
            data_cols={'event': 'random'},
            missing_data={'event': 0.1}
        )
    """

    n_seq: int = 10
    sequence_size: Union[int, List[int], str, Distribution] = 5
    data_cols: Dict[str, Union[str, GenMethod]] = Field(
        default_factory=lambda: {"data": "random"}
    )
    missing_data: Optional[Dict[str, float]] = None
    profile_id: Optional[str] = None

    @field_validator("missing_data", mode="before")
    @classmethod
    def validate_missing_data(cls, value):
        """Validate missing data percentage.

        Args:
            value (Dict[str, float]): Missing data configuration.

        Raises:
            ValueError: If any missing data value is not between 0 and 1.
        """
        if value:
            # Check that each value in the dictionary is between 0 and 1
            for key, v in value.items():
                if not (0 <= v <= 1):
                    raise ValueError(f"The value for '{key}' must be between 0 and 1.")
        return value

    @field_validator("sequence_size", mode="before")
    @classmethod
    def validate_sequence_size(cls, value):
        """Validate sequence size configuration.

        Args:
            value (Union[int, List[int]]): Sequence size configuration.

        Raises:
            ValueError: If sequence size is not a positive integer.
        """
        if value:
            if isinstance(value, int):
                if value <= 0:
                    raise ValueError("Sequence size must be greater than 0.")

            if isinstance(value, list):
                for v in value:
                    if v <= 0:
                        raise ValueError("Sequence size must be greater than 0.")

        return value
