#!/usr/bin/env python3
"""
Configuration settings for normal probability distribution.
"""

from pydantic.dataclasses import dataclass, Field
from pypassist.dataclass.decorators.viewer import viewer


@viewer
@dataclass
class NormalDistributionSettings:
    """Configuration for Gaussian (Normal) probability distribution.

    Defines the parameters for generating samples from a normal
    distribution, which is characterized by its mean (μ) and
    standard deviation (σ).

    Attributes:
        mu (float, optional): Mean (location) of the distribution.
            Determines the central tendency of the generated samples.
            - Controls the center of the bell-shaped curve
            - Must be non-negative
            Defaults to 0.

        sigma (float, optional): Standard deviation (scale) of the distribution.
            Determines the spread of the generated samples.
            - Controls the width of the bell-shaped curve
            - Larger values result in more spread-out samples
            - Must be non-negative
            Defaults to 1.

    Example:
        # Configure a normal distribution with custom parameters
        settings = NormalDistributionSettings(
            mu=10,    # Mean shifted to 10
            sigma=2   # Narrower distribution
        )
    """

    mu: float = Field(default=0, ge=0)
    sigma: float = Field(default=1, ge=0)
