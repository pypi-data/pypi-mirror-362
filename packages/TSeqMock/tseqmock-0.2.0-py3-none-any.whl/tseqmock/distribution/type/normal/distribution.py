#!/usr/bin/env python3
"""
Normal distribution class.
"""

from scipy.stats import truncnorm
import numpy as np

from .settings import NormalDistributionSettings
from ...base import Distribution


class NormalDistribution(Distribution, register_name="normal"):
    """Generates positive random numbers following a normal distribution."""

    SETTINGS_DATACLASS = NormalDistributionSettings

    def __init__(self, settings=None):
        if settings is None:
            settings = NormalDistributionSettings()
        super().__init__(settings)

    def sample(self, size=1):
        """
        Generates raw samples from the distribution.

        Args:
            size: Number of samples to generate. Default is 1.

        Returns:
            Sampled value(s) from a normal distribution N(mu, sigma)
        """
        return np.random.normal(self.settings.mu, self.settings.sigma, size=size)

    def sample_normalized(self, size=1):
        """
        Generates samples from a normal distribution truncated to the [0, 1] interval.

        Args:
            size: Number of samples to generate. Default is 1.

        Returns:
            Sampled value(s) in [0, 1] following a truncated normal distribution
            defined by settings.mu and settings.sigma.
        """
        mu = self.settings.mu
        sigma = self.settings.sigma
        return self._sample_truncated(size=size, mu=mu, sigma=sigma)

    @staticmethod
    def _sample_truncated(size, mu=0, sigma=1):
        """
        Samples from a normal distribution truncated to [0, 1].

        Args:
            size: Number of samples to generate.

        Returns:
            Array of sampled values in [0, 1]
        """
        a = (0 - mu) / sigma
        b = (1 - mu) / sigma
        return truncnorm.rvs(a, b, loc=mu, scale=sigma, size=size)

    def summary_desc(self):
        """
        Returns a summary description of the distribution settings.
        """
        return f"Normal({self.settings.mu}, {self.settings.sigma})"
