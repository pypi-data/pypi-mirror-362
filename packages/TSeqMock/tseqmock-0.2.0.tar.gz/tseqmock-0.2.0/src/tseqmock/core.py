#!/usr/bin/env python3
"""
Core module for temporal sequence mock data generation.
"""

import logging
import random

import numpy as np

from .generator.base.generator import SeqGenerator
from .exception import MissingProfilesError

LOGGER = logging.getLogger(__name__)


class TSeqMocker:
    """Temporal sequence mock data generator.

    Generates synthetic temporal sequences with configurable parameters.

    Args:
        seq_type (str): Type of sequence to generate
            (e.g., 'event', 'state', 'interval').
        settings (dict, optional): Initial generator settings.
        seed (int, optional): Random seed for reproducibility.

    Attributes:
        stype (str): Sequence type.
        seed (int): Random seed used.
    """

    def __init__(self, seq_type, settings=None, seed=None):
        self._set_seed(seed)
        self.seed = seed
        self.stype = seq_type
        self._generator = SeqGenerator.init(seq_type, settings)
        self._data = None

    @property
    def data(self):
        """Retrieve last generated data, generating if not exists.

        Returns:
            pd.DataFrame: Last generated mock data.
        """
        if self._data is None:
            self._data = self()
        return self._data

    @property
    def settings(self):
        """Get current generator settings.

        Returns:
            Settings object for the current generator.
        """
        return self._generator.settings

    @property
    def summary(self):
        """Get summary of last generated data.

        Returns:
            Summary of generated mock data.
        """
        summary = self._generator.summary
        if summary is None:
            summary = self()
        return summary

    def __call__(self, **kwargs):
        """Generate mock data with optional settings update.

        Args:
            **kwargs: Keyword arguments to update generator settings.

        Returns:
            pd.DataFrame: Generated mock temporal sequence data.

        Raises:
            MissingProfilesError: If no profiles are defined.
        """
        self._generator.update_settings(**kwargs)
        if self.settings.profiles is None:
            raise MissingProfilesError("No profiles defined. Use add_profile()")

        self._data = self._generator.generate()
        return self._data

    def add_profile(self, profile_settings):
        """Add a generation profile to the mock data generator.

        Args:
            profile_settings: Configuration for data generation profile.
        """
        self._generator.add_profile(profile_settings)

    def set_time_design(self, time_design_settings):
        """Configure temporal design for sequence generation.

        Args:
            time_design_settings: Settings defining time-related generation rules.
        """
        self._generator.set_time_design(time_design_settings)

    def _set_seed(self, seed):
        """Set random seeds for reproducible generation.

        Args:
            seed (int, optional): Seed value for random number generators.
        """
        if seed is not None:
            # Seed both numpy and Python's built-in random module
            np.random.seed(seed)
            random.seed(seed)
