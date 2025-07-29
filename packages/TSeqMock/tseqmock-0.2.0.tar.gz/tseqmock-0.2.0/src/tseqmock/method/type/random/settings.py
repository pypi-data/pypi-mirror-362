#!/usr/bin/env python3
"""
Configuration settings for random data generation method.
"""

from typing import Optional, Any

import pandas as pd

from pydantic import field_validator
from pydantic.dataclasses import dataclass, Field
from pypassist.fallback.typing import List
from pypassist.dataclass.decorators.viewer import viewer


@viewer
@dataclass
class RandomGenMethodSettings:
    """Configuration for random data generation method.

    Defines parameters for generating random samples from a specified
    vocabulary with optional weighted probabilities.

    Attributes:
        vocabulary (List[Any], optional): Collection of values to
            randomly sample from during generation.
            - Can contain elements of any type
            - Cannot contain NaN (Not a Number) values
            Defaults to ["A", "B", "C"].

        weights (List[float], optional): Probability weights for
            sampling from the vocabulary.
            - Must have the same length as the vocabulary
            - Determines the likelihood of each vocabulary item being selected
            - If not provided, uniform sampling is used
            Defaults to None (uniform sampling).

    Example:
        # Configure random generation with custom vocabulary and weights
        settings = RandomGenMethodSettings(
            vocabulary=['cat', 'dog', 'bird'],
            weights=[0.5, 0.3, 0.2]  # Biased sampling
        )

    Notes:
        - Supports flexible random sampling strategies
        - Allows both uniform and weighted random selection
        - Validates vocabulary and weight configurations
    """

    vocabulary: List[Any] = Field(default_factory=lambda: ["A", "B", "C"])
    weights: Optional[List[float]] = None

    def __post_init__(self):
        """Validate vocabulary and weights configuration.

        Ensures that:
        - Weights list (if provided) matches vocabulary length
        - No NaN values are present in the vocabulary
        """
        if self.weights is not None and len(self.weights) != len(self.vocabulary):
            raise ValueError(
                "The length of the vocabulary and the weights must be the same."
            )

    @field_validator("vocabulary", mode="before")
    @classmethod
    def validate_vocabulary(cls, value):
        """Validate vocabulary to ensure no NaN values are present.

        Args:
            value (List[Any]): Input vocabulary to validate.

        Raises:
            ValueError: If any value in the vocabulary is NaN.

        Returns:
            List[Any]: Validated vocabulary.
        """
        if any(pd.isna(x) for x in value):
            raise ValueError("Vocabulary cannot contain NaN values.")
        return value
