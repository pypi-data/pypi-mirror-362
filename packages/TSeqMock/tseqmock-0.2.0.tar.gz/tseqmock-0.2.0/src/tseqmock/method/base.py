#!/usr/bin/env python3
"""
Base abstract class for temporal sequence generation methods.
"""

from abc import ABC, abstractmethod

from pypassist.mixin.registrable import Registrable
from pypassist.mixin.settings import SettingsMixin
from pydantic_core import core_schema


class GenMethod(ABC, Registrable, SettingsMixin):
    """Abstract base class for temporal sequence generation methods.

    Provides a standardized interface for creating custom data generation
    strategies with registration and settings management capabilities.

    Attributes:
        _REGISTER (dict): Registry of available generation methods.
        _TYPE_SUBMODULE (str): Submodule path for method types.

    Methods:
        init: Class method to instantiate a method by name.
        populate_column: Abstract method to generate column values.
        summary_desc: Abstract method to describe method settings.

    Example:
        # Typical usage in subclasses
        class RandomMethod(GenMethod):
            def populate_column(self, data, col_name):
                # Implement custom generation logic
                pass
    """

    _REGISTER = {}
    _TYPE_SUBMODULE = "type"

    def __init__(self, settings):
        """Initialize generation method with settings.

        Args:
            settings (dict, optional): Configuration settings for the method.
        """
        Registrable.__init__(self)
        SettingsMixin.__init__(self, settings)

    @classmethod
    def init(cls, method_name, settings=None):
        """Initialize a generation method from its registered name.

        Args:
            method_name (str): Name of the generation method to instantiate.
            settings (dict, optional): Configuration settings for the method.

        Returns:
            GenMethod: Instantiated generation method.

        Raises:
            KeyError: If the method name is not registered.
        """
        return cls.get_registered(method_name)(settings)

    @abstractmethod
    def populate_column(self, data, col_name):
        """Generate values to populate a specific DataFrame column.

        This method must be implemented by subclasses to define
        the specific generation strategy for a column.

        Args:
            data (pd.DataFrame): Input DataFrame to generate values for.
            col_name (str): Name of the column to populate.

        Returns:
            pd.Series: Generated values with same length and index as input data.
        """

    @abstractmethod
    def summary_desc(self):
        """Generate a summary description of the method's settings.

        Returns:
            str: Concise description of the generation method configuration.
        """

    def __get_pydantic_core_schema__(self, handler):  # pylint: disable=unused-argument
        """Provide a custom Pydantic schema for flexible validation.

        Returns:
            core_schema: A Pydantic core schema for the method.
        """
        return core_schema.any_schema()
