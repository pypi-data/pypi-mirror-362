#!/usr/bin/env python3
"""
Random generation method.
"""

import random

import pandas as pd

from ...base import GenMethod
from .settings import RandomGenMethodSettings


class RandomGenMethod(GenMethod, register_name="random"):
    """
    Random generation method.
    """

    SETTINGS_DATACLASS = RandomGenMethodSettings

    def __init__(self, settings=None):
        if settings is None:
            settings = RandomGenMethodSettings()
        super().__init__(settings)

        ## -- cache
        self.weights = None
        self.vocabulary = None

    def populate_column(self, data, col_name):
        """
        Generate a Series of values to populate the specified column in a DataFrame.

        Args:
            data (pd.DataFrame): Input DataFrame for which to generate values.
            col_name (str): Name of the column to populate.

        Returns:
            pd.Series: A Series of generated values, same length and index as `data`.
        """
        vocab = self.settings.vocabulary
        weights = self.settings.weights
        size = len(data)

        values = random.choices(vocab, weights=weights, k=size)

        ## -- cache
        self.weights = weights
        self.vocabulary = vocab

        return pd.Series(values, index=data.index, name=col_name)

    def summary_desc(self):
        """
        Returns a summary description of the settings.
        """
        return f"RandomGenMethod(vocabulary={self.vocabulary}, weights={self.weights})"
