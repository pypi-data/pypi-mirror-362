#!/usr/bin/env python3
"""Sequence-specific time strategy."""


import datetime

import numpy as np

from ....distribution.base import Distribution
from ...base import TimeStrategy
from .settings import SeqSpeTimeStrategySettings


class SeqSpeTimeStrategy(TimeStrategy, register_name="sequence_specific"):
    """
    Sequence-specific time strategy where T0 is specific to each sequence.
    """

    SETTINGS_DATACLASS = SeqSpeTimeStrategySettings

    def __init__(self, settings=None):
        if settings is None:
            settings = SeqSpeTimeStrategySettings()
        super().__init__(settings)

        ## -- cached distribution
        self.distribution = None

    def summary_desc(self):
        """
        Returns a summary description of the settings.
        """
        return (
            f"SeqSpeTimeStrategy(distribution={self.distribution.summary_desc()}, "
            f"min_date={self.settings.min_date.isoformat()}, "
            f"max_date={self.settings.max_date.isoformat()})"
        )

    def add_t0_column(self, df, t0_col="__T0__"):
        """
        Add T0 column to dataframe based on distribution.

        Args:
            df (pd.DataFrame): Input dataframe
            t0_col (str): Name of the column to add. Defaults to "__T0__".

        Returns:
            pd.DataFrame: The original dataframe with the added column.
        """
        ## -- Settings
        distribution = self._resolve_distribution(self.settings.distribution)
        min_date = self.settings.min_date
        max_date = self.settings.max_date
        id_col = df.columns[0]
        id_values = df[id_col].unique()
        num_sequences = len(id_values)

        ## -- Generate
        normalized_positions = distribution.sample_normalized(num_sequences)
        min_timestamp = min_date.timestamp()
        max_timestamp = max_date.timestamp()
        timestamp_range = max_timestamp - min_timestamp
        t0_timestamps = min_timestamp + normalized_positions * timestamp_range
        mapping = {
            id_: datetime.datetime.fromtimestamp(ts)
            for id_, ts in zip(id_values, t0_timestamps)
        }
        df[t0_col] = df[id_col].map(mapping)

        self._update_cached_distribution(distribution)

        return df

    def populate_timeline(self, df, seq_sizes, t0_col="__T0__", time_col="__TIME__"):
        """
        Populate timeline with timestamps based on distribution.

        Args:
            df (pd.DataFrame): Input dataframe
            seq_sizes (list of int): Sequence sizes
            t0_col (str): Name of the T0 column. Defaults to "__T0__".
            time_col (str): Name of the time column. Defaults to "__TIME__".

        Returns:
            pd.DataFrame: The expanded dataframe with timestamps.
        """
        # Create expanded dataframe
        repeated_data = df.loc[df.index.repeat(seq_sizes)].reset_index(drop=True)

        # Add position within each group (not needed in final result but used for processing)
        repeated_data["pos"] = repeated_data.groupby(
            df.index.repeat(seq_sizes)
        ).cumcount()

        # Generate all timestamps
        all_times = self._generate_timestamps(df, seq_sizes, t0_col)
        repeated_data[time_col] = all_times

        return repeated_data.drop(columns=["pos", t0_col])

    def _generate_timestamps(self, df, seq_sizes, t0_col):
        """Generate all timestamps based on distribution."""
        # Prepare distribution samples
        total_extra = sum(seq_sizes) - len(seq_sizes)
        distribution = self._resolve_distribution(self.settings.distribution)
        normalized = np.array(distribution.sample_normalized(total_extra))
        max_ts = self.settings.max_date.timestamp()

        all_times = []
        offset = 0

        for i, row in df.iterrows():
            t0 = row[t0_col]
            n = seq_sizes[i]

            if n == 1:
                all_times.append(t0)
            else:
                # Generate and sort additional timestamps
                additional_times = self._calculate_additional_times(
                    t0, normalized[offset : offset + n - 1], max_ts
                )
                offset += n - 1
                all_times.extend(additional_times)

        self._update_cached_distribution(distribution)

        return all_times

    def _calculate_additional_times(self, t0, deltas, max_ts):
        """Calculate sorted timestamps for a single row."""
        t0_ts = t0.timestamp()
        timestamps = [t0_ts + d * (max_ts - t0_ts) for d in deltas]
        additional_times = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]
        return sorted([t0] + additional_times)

    def _resolve_distribution(self, distribution):
        """
        Resolve a distribution object from a string or Distribution.

        Args:
            distribution: String name of registered distribution or Distribution object

        Returns:
            Distribution: Resolved distribution object
        """
        if isinstance(distribution, str):
            return Distribution.get_registered(distribution)()
        return distribution

    def _update_cached_distribution(self, distribution):
        self.distribution = distribution
