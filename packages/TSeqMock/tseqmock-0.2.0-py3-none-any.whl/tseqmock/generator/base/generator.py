#!/usr/bin/env python3
"""
Abstract base class for temporal sequence generators in TSeqMock.
"""

from abc import ABC, abstractmethod
import random
import logging

import pandas as pd
import numpy as np

from pypassist.mixin.registrable import Registrable
from pypassist.mixin.settings import SettingsMixin

from ...method.base import GenMethod
from ...distribution.base import Distribution
from ...time_strategy.base import TimeStrategy


LOGGER = logging.getLogger(__name__)


class SeqGenerator(ABC, Registrable, SettingsMixin):
    """Abstract base class for generating temporal sequence data.

    Provides a flexible framework for creating synthetic temporal sequences
    with configurable generation strategies, missing data handling,
    and profile management.

    Attributes:
        _REGISTER (dict): Registry of available generator types.
        _TYPE_SUBMODULE (str): Relative path to generator type implementations.
        summary (pd.DataFrame): Metadata summary of generated sequences.
        missing_data (dict): Configuration of missing data applied.

    Methods:
        init: Class method to instantiate a generator by name.
        generate: Abstract method to generate mock data sequences.
        add_profile: Add generation profile to the generator.
        set_time_design: Configure time design for sequence generation.

    Example:
        # Typical usage in subclasses
        class EventGenerator(SeqGenerator):
            def generate(self):
                # Implement sequence generation logic
                pass
    """

    _REGISTER = {}
    _TYPE_SUBMODULE = "../type"

    def __init__(self, settings):
        """Initialize sequence generator with configuration settings.

        Args:
            settings (dict, optional): Configuration parameters
                for the sequence generator.
        """
        Registrable.__init__(self)
        SettingsMixin.__init__(self, settings)

        self.summary = None
        ## -- cache
        self.missing_data = None

    @classmethod
    def init(cls, generator_name, settings=None):
        """Initialize a generator from its registered name.

        Args:
            generator_name (str): Name of the generator to instantiate.
            settings (dict, optional): Configuration settings for the
                generator.

        Returns:
            SeqGenerator: Instantiated sequence generator.

        Raises:
            KeyError: If the generator name is not registered.
        """
        return SeqGenerator.get_registered(generator_name)(settings)

    @abstractmethod
    def generate(self):
        """Generate mock temporal sequence data.

        Abstract method to be implemented by subclasses.
        Defines the core logic for creating synthetic sequences.

        Returns:
            pd.DataFrame: Generated temporal sequence data.
        """

    def add_profile(self, profile_settings):
        """Add a generation profile to the generator.

        Appends a new profile configuration to the existing profiles.

        Args:
            profile_settings: Configuration for a new data generation profile.
        """
        curent_profiles = self.settings.profiles
        if curent_profiles is None:
            curent_profiles = []
        profile_settings = curent_profiles + [profile_settings]
        self.update_settings(profiles=profile_settings)

    def set_time_design(self, time_design_settings):
        """Configure temporal design for sequence generation.

        Args:
            time_design_settings: Settings defining time-related
            generation rules.
        """
        self.update_settings(time_design=time_design_settings)

    def _update_summary(self, data_profile, id_profile):
        """Update summary DataFrame with profile information.

        Aggregates metadata about generated sequences.

        Args:
            data_profile (pd.DataFrame): DataFrame containing profile data.
            id_profile (str): Identifier for the current profile.
        """
        id_col = self.settings.output_columns.id_column
        unique_ids = data_profile[id_col].unique()

        # Create profile data for the current profile
        profile_data = self._create_profile_data(unique_ids, id_profile)

        # Initialize summary or append to existing summary
        if self.summary is None:
            self.summary = profile_data
        else:
            self.summary = pd.concat([self.summary, profile_data], ignore_index=True)

    @abstractmethod
    def _create_profile_data(self, unique_ids, id_profile):
        """Create DataFrame with profile metadata.

        Abstract method to generate profile-specific metadata.

        Args:
            unique_ids (array-like): Unique sequence identifiers.
            id_profile (str): Identifier for the current profile.

        Returns:
            pd.DataFrame: Metadata for the generated profile.
        """

    def _init_data(self, n_seq, id_profile):
        """Initialize base DataFrame for sequence generation.

        Args:
            n_seq (int): Number of sequences to generate.
            id_profile (str, optional): Profile identifier.

        Returns:
            pd.DataFrame: Initialized DataFrame with sequence IDs.
        """
        seq_ids = self._get_sequences_ids(n_seq, id_profile)
        id_col = self.settings.output_columns.id_column

        ## -- Init dataframe
        init_df = pd.DataFrame(
            {id_col: seq_ids},
        )
        return init_df

    def _get_sequences_ids(self, n_seq, id_profile):
        """Generate unique sequence identifiers.

        Args:
            n_seq (int): Number of sequences to generate.
            id_profile (str, optional): Profile identifier.

        Returns:
            list: Unique sequence identifiers.
        """
        seq_ids = []
        for seq_index in range(n_seq):
            id_seq = f"{self.settings.sequence_id}-{seq_index}"
            if id_profile:
                id_seq = f"{id_seq}-{id_profile}"

            seq_ids.append(id_seq)
        return seq_ids

    def _apply_missing_data(self, data, missing_config):
        """Introduce missing values to the generated data.

        Args:
            data (pd.DataFrame): Input DataFrame.
            missing_config (dict): Configuration for missing data.

        Returns:
            pd.DataFrame: DataFrame with missing values applied.
        """
        if missing_config is None:
            return data

        for col_name, rate in missing_config.items():
            if col_name not in data.columns:
                LOGGER.warning(
                    "Missing data: column %s not found in data. Skipping.", col_name
                )
                continue

            mask = np.random.rand(len(data)) < rate
            data.loc[mask, col_name] = None

        ## -- cache
        self.missing_data = missing_config
        return data

    def _iter_profile(self):
        """Iterate over generator profiles.

        Yields:
            Profile configurations for the generator.
        """
        yield from self.settings.profiles

    def _resolve_seq_sizes(self, seq_size, n_seq):
        """Resolve sequence sizes for generation.

        Handles various input types for sequence size specification.

        Args:
            seq_size (Union[int, str, Distribution, List[int]]):
                Sequence size configuration.
            n_seq (int): Number of sequences to generate.

        Returns:
            List[int]: Resolved sequence sizes.

        Raises:
            ValueError: If sequence size configuration is invalid.
        """
        if isinstance(seq_size, str):
            seq_size = Distribution.get_registered(seq_size)()
        if isinstance(seq_size, Distribution):
            seq_size = round(seq_size.sample(n_seq))
        if isinstance(seq_size, int):
            seq_size = [seq_size] * n_seq
        if not isinstance(seq_size, list):
            raise ValueError(f"Invalid sequence size: {seq_size}. Must be a list.")
        if len(seq_size) != n_seq:
            seq_size = random.choices(seq_size, k=n_seq)

        return seq_size

    def _resolve_method(self, method):
        """Resolve generation method to a method instance.

        Args:
            method (Union[str, GenMethod]): Generation method.

        Returns:
            GenMethod: Instantiated generation method.
        """
        if isinstance(method, str):
            method = GenMethod.get_registered(method)()
        return method

    def _resolve_time_strategy(self, strategy):
        """Resolve time strategy to a strategy instance.

        Args:
            strategy (Union[str, TimeStrategy]): Time strategy.

        Returns:
            TimeStrategy: Instantiated time strategy.
        """
        if isinstance(strategy, str):
            strategy = TimeStrategy.get_registered(strategy)()
        return strategy
