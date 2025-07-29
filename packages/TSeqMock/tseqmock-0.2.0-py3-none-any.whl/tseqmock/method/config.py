#!/usr/bin/env python3
"""
Configuration for data generation method selection.
"""

from typing import Optional

from pydantic.dataclasses import dataclass
from pypassist.dataclass.decorators import registry
from pypassist.dataclass.decorators.exportable.decorator import exportable
from pypassist.utils.typing import ParamDict

from .base import GenMethod


@registry(base_cls=GenMethod, register_name_attr="method_type")
@exportable(strategy="registry")
@dataclass
class GenMethodConfig:
    """Configuration for selecting and instantiating data generation methods.

    Provides a flexible mechanism for configuring and creating
    generation methods used in temporal sequence generation.

    Attributes:
        method_type (str, optional): Name of the generation method
            to be used. Defaults to "random" method.
            Registered method types can be used.

        settings (ParamDict, optional): Configuration parameters
            for the specified generation method.
            Dictionary of parameters specific to the method.

    Methods:
        get_generation_method(): Instantiate the configured generation method.

    Example:
        # Configure a custom generation method with specific settings
        config = GenMethodConfig(
            method_type="random",
            settings={"vocabulary": [1, 2, 3, 4, 5]}
        )
        generation_method = config.get_generation_method()

    Notes:
        - Supports dynamic method configuration
        - Enables easy switching between different generation strategies
        - Provides a standardized way to create generation method instances
    """

    method_type: str = "random"
    settings: Optional[ParamDict] = None

    def get_generation_method(self):
        """Instantiate the configured data generation method.

        Creates a generation method instance based on the specified
        method type and configuration settings.

        Returns:
            GenMethod: An instance of the configured generation method.
        """
        return GenMethod.get_registered(self.method_type)(self.settings)
