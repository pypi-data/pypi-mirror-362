#!/usr/bin/env python3
"""
Uniform distribution class.
"""

import numpy as np

from .settings import UniformDistributionSettings
from ...base import Distribution


class UniformDistribution(Distribution, register_name="uniform"):
    """Generates random numbers following a uniform distribution."""

    SETTINGS_DATACLASS = UniformDistributionSettings

    def __init__(self, settings=None):
        if settings is None:
            settings = UniformDistributionSettings()
        super().__init__(settings)

    def sample(self, size=1):
        """
        Generates raw samples from the distribution

        Args:
            size: Number of samples to generate. Default to 1.

        Returns:
            Sampled value(s) within the natural range of the distribution
        """
        min_val = self.settings.min_val
        max_val = self.settings.max_val
        return np.random.uniform(min_val, max_val, size)

    def sample_normalized(self, size=1):
        """
        Generates normalized samples between 0 and 1

        Args:
            size: Number of samples to generate. Default to 1.

        Returns:
            Sampled value(s) normalized between 0 and 1
        """
        min_val = self.settings.min_val
        max_val = self.settings.max_val
        samples = self.sample(size)
        return (samples - min_val) / (max_val - min_val)

    def summary_desc(self):
        """
        Returns a summary description of the distribution settings.
        """
        return f"Uniform({self.settings.min_val}, {self.settings.max_val})"
