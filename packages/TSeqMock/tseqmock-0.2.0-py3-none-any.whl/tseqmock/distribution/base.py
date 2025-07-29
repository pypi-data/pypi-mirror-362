#!/usr/bin/env python3
"""
Abstract base class for statistical distributions in temporal sequence generation.
"""

from abc import ABC, abstractmethod

from pypassist.mixin.registrable import Registrable
from pypassist.mixin.settings import SettingsMixin
from pydantic_core import core_schema


class Distribution(ABC, Registrable, SettingsMixin):
    """Abstract base class for statistical sampling distributions.

    Provides a standardized interface for creating custom probability
    distributions with registration and settings management capabilities.

    Attributes:
        _REGISTER (dict): Registry of available distribution types.
        _TYPE_SUBMODULE (str): Submodule path for distribution implementations.

    Methods:
        init: Class method to instantiate a distribution by name.
        sample: Abstract method to generate raw distribution samples.
        sample_normalized: Abstract method to generate normalized samples.
        summary_desc: Abstract method to describe distribution settings.

    Example:
        # Typical usage in subclasses
        class NormalDistribution(Distribution):
            def sample(self, size=1):
                # Implement normal distribution sampling
                pass

            def sample_normalized(self, size=1):
                # Implement normalized sampling
                pass
    """

    _REGISTER = {}
    _TYPE_SUBMODULE = "type"

    def __init__(self, settings):
        """Initialize distribution with configuration settings.

        Args:
            settings (dict, optional): Configuration parameters
                for the distribution.
        """
        Registrable.__init__(self)
        SettingsMixin.__init__(self, settings)

    @classmethod
    def init(cls, distribution_name, settings=None):
        """Initialize a distribution from its registered name.

        Args:
            distribution_name (str): Name of the distribution to instantiate.
            settings (dict, optional): Configuration settings for the
                distribution.

        Returns:
            Distribution: Instantiated distribution object.

        Raises:
            KeyError: If the distribution name is not registered.
        """
        return cls.get_registered(distribution_name)(settings)

    @abstractmethod
    def sample(self, size=1):
        """Generate raw samples from the distribution.

        Args:
            size (int, optional): Number of samples to generate.
                Defaults to 1.

        Returns:
            array-like: Sampled value(s) within the distribution's
                natural range.
        """

    @abstractmethod
    def sample_normalized(self, size=1):
        """Generate samples normalized between 0 and 1.

        Transforms distribution samples to a standard [0, 1] range.

        Args:
            size (int, optional): Number of samples to generate.
                Defaults to 1.

        Returns:
            array-like: Sampled value(s) normalized between 0 and 1.
        """

    @abstractmethod
    def summary_desc(self):
        """Generate a summary description of distribution settings.

        Returns:
            str: Concise description of the distribution's
                configuration and key parameters.
        """

    def __get_pydantic_core_schema__(self, handler):  # pylint: disable=unused-argument
        """Provide a custom Pydantic schema for flexible validation.

        Returns:
            core_schema: A Pydantic core schema for the distribution.
        """
        return core_schema.any_schema()
