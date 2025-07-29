#!/usr/bin/env python3
"""
Configuration for probability distribution generation.
"""

from typing import Optional

from pydantic.dataclasses import dataclass
from pypassist.dataclass.decorators import registry
from pypassist.dataclass.decorators.exportable.decorator import exportable
from pypassist.utils.typing import ParamDict

from .base import Distribution


@registry(base_cls=Distribution, register_name_attr="dist_type")
@exportable(strategy="registry")
@dataclass
class DistribConfig:
    """Configuration for generating probability distributions.

    Provides a flexible mechanism for configuring and instantiating
    statistical distributions used in temporal sequence generation.

    Attributes:
        dist_type (str, optional): Name of the distribution type
            to be used. Defaults to "uniform" distribution.
            Registered distribution types can be used.

        settings (ParamDict, optional): Configuration parameters
            for the specified distribution.
            Dictionary of parameters specific to the distribution.

    Methods:
        get_distribution(): Instantiate the configured distribution.

    Example:
        # Configure a normal distribution with custom parameters
        config = DistribConfig(
            dist_type="normal",
            settings={"mu": 0, "sigma": 1}
        )
        distribution = config.get_distribution()

    Notes:
        - Supports dynamic distribution configuration
        - Enables easy switching between different distribution types
        - Provides a standardized way to create distribution instances
    """

    dist_type: str = "uniform"
    settings: Optional[ParamDict] = None

    def get_distribution(self):
        """Instantiate the configured probability distribution.

        Creates a distribution instance based on the specified
        distribution type and configuration settings.

        Returns:
            Distribution: An instance of the configured distribution.
        """
        return Distribution.get_registered(self.dist_type)(self.settings)
