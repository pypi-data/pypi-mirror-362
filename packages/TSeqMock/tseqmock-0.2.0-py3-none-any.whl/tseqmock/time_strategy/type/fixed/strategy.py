#!/usr/bin/env python3
"""Fixed time strategy."""

from ...base import TimeStrategy
from .settings import FixedTimeStrategySettings


class FixedTimeStrategy(TimeStrategy, register_name="fixed"):
    """
    Fixed time strategy where T0 is fixed for all sequences.
    """

    SETTINGS_DATACLASS = FixedTimeStrategySettings

    def __init__(self, settings=None):
        if settings is None:
            settings = FixedTimeStrategySettings()
        super().__init__(settings)

        ## -- cache
        self.sampling_steps = None

    def summary_desc(self):
        """
        Returns a summary description of the settings.
        """
        return (
            f"FixedTimeStrategy(t0_date={self.settings.t0_date.isoformat()}, "
            f"sampling_steps={self.sampling_steps})"
        )

    def add_t0_column(self, df, t0_col="__T0__"):
        """
        Add T0 column to dataframe based provided date.

        Args:
            df (pd.DataFrame): Input dataframe
            t0_col (str): Name of the column to add. Defaults to "__T0__".

        Returns:
            pd.DataFrame: The original dataframe with the added column.
        """
        df[t0_col] = self.settings.t0_date
        return df

    def populate_timeline(self, df, seq_sizes, t0_col="__T0__", time_col="__TIME__"):
        """
        Populate timeline with timestamps based on timedeltas provided.

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
        id_col = df.columns[0]
        repeated_data = self._apply_offsets(repeated_data, id_col, t0_col, time_col)

        return repeated_data.drop(columns=["pos", t0_col])

    def _apply_offsets(self, df, id_col, t0_col="__T0__", time_col="__TIME__"):
        """
        Add offsets to the T0 column.

        Args:
            df (pd.DataFrame): Input dataframe
            id_col (str): Name of the id column
            t0_col (str): Name of the T0 column. Defaults to "__T0__".
            time_col (str): Name of the time column. Defaults to "__TIME__".

        Returns:
            pd.DataFrame: The original dataframe with the added column.
        """
        l_offsets = self._resolve_offsets()
        max_len = len(l_offsets)

        def apply_group(group):
            times = [group.iloc[0][t0_col]]  #  init : [T0, ]
            for i in range(1, len(group)):
                index = (i % max_len) - 1
                dt = l_offsets[index]
                times.append(times[-1] + dt)
            group[time_col] = times
            return group

        df.set_index(id_col, inplace=True)
        df = df.groupby(id_col, group_keys=False).apply(apply_group)
        return df.reset_index()

    def _resolve_offsets(self):
        """
        Resolve offsets from granularity.
        """
        sampling_steps = self.settings.sampling_steps
        granularity = self.settings.granularity
        self.sampling_steps = granularity.to_offsets(sampling_steps)
        return self.sampling_steps
