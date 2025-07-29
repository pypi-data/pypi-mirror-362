#!/usr/bin/env python3
"""
Abstract base class for temporal sequence time strategies.
"""

from abc import ABC, abstractmethod

from pypassist.mixin.registrable import Registrable
from pypassist.mixin.settings import SettingsMixin
from pydantic_core import core_schema


class TimeStrategy(ABC, Registrable, SettingsMixin):
    """Abstract base class for generating temporal sequence timestamps.

    Provides a standardized interface for creating custom time generation
    strategies with registration and settings management capabilities.

    Attributes:
        _REGISTER (dict): Registry of available time strategy types.
        _TYPE_SUBMODULE (str): Submodule path for time strategy implementations.

    Example:
        # Typical usage in subclasses
        class FixedTimeStrategy(TimeStrategy):
            def add_t0_column(self, df, t0_col="__T0__"):
                # Implement initial timestamp generation
                pass

            def populate_timeline(self, df, seq_sizes):
                # Implement timeline population strategy
                pass
    """

    _REGISTER = {}
    _TYPE_SUBMODULE = "type"

    def __init__(self, settings):
        """Initialize time strategy with configuration settings.

        Args:
            settings (dict, optional): Configuration parameters
                for the time strategy.
        """
        Registrable.__init__(self)
        SettingsMixin.__init__(self, settings)

    @classmethod
    def init(cls, time_strategy_name, settings=None):
        """Initialize a time strategy from its registered name.

        Args:
            time_strategy_name (str): Name of the time strategy to instantiate.
            settings (dict, optional): Configuration settings for the
                time strategy.

        Returns:
            TimeStrategy: Instantiated time strategy object.

        Raises:
            KeyError: If the time strategy name is not registered.
        """
        return cls.get_registered(time_strategy_name)(settings)

    @abstractmethod
    def add_t0_column(self, df, t0_col="__T0__"):
        """Add initial timestamp column to the input dataframe.

        Generates the base timestamp for each sequence in the dataframe.

        Args:
            df (pd.DataFrame): Input dataframe to modify.
            t0_col (str, optional): Name of the initial timestamp column.
                Defaults to "__T0__".

        Returns:
            pd.DataFrame: Dataframe with added initial timestamp column.
        """

    @abstractmethod
    def populate_timeline(self, df, seq_sizes, t0_col="__T0__", time_col="__TIME__"):
        """Generate timestamps for each sequence based on initial timestamps.

        Expands the dataframe by adding precise timestamps for each
        sequence element.

        Args:
            df (pd.DataFrame): Input dataframe to expand.
            seq_sizes (list of int): Number of elements in each sequence.
            t0_col (str, optional): Name of the initial timestamp column.
                Defaults to "__T0__".
            time_col (str, optional): Name of the generated timestamp column.
                Defaults to "__TIME__".

        Returns:
            pd.DataFrame: Dataframe with expanded timestamp information.
        """

    @abstractmethod
    def summary_desc(self):
        """Generate a summary description of time strategy settings.

        Returns:
            str: Concise description of the time strategy's
                configuration and key parameters.
        """

    def __get_pydantic_core_schema__(self, handler):  # pylint: disable=unused-argument
        """Provide a custom Pydantic schema for flexible validation.

        Returns:
            core_schema: A Pydantic core schema for the time strategy.
        """
        return core_schema.any_schema()
