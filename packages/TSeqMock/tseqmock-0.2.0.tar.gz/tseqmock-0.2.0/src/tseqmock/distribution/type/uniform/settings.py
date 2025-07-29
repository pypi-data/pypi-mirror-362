#!/usr/bin/env python3
"""
Configuration settings for uniform probability distribution.
"""

from pydantic.dataclasses import dataclass, Field
from pypassist.dataclass.decorators.viewer import viewer


@viewer
@dataclass
class UniformDistributionSettings:
    """Configuration for Uniform probability distribution.

    Defines the parameters for generating samples from a uniform
    distribution, where all values within a specified range have
    equal probability of being selected.

    Attributes:
        min_val (int, optional): Lower bound of the distribution range.
            Determines the minimum possible value for generated samples.
            - Inclusive lower limit of the sampling range
            - Must be less than max_val
            Defaults to 1.

        max_val (int, optional): Upper bound of the distribution range.
            Determines the maximum possible value for generated samples.
            - Inclusive upper limit of the sampling range
            - Must be greater than min_val
            Defaults to 10.

    Example:
        # Configure a uniform distribution with custom range
        settings = UniformDistributionSettings(
            min_val=5,   # Lower bound set to 5
            max_val=15   # Upper bound set to 15
        )
    """

    min_val: int = 1
    max_val: int = 10
