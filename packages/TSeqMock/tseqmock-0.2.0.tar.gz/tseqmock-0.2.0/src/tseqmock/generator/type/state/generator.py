#!/usr/bin/env python3
"""
Generator for state sequences.
"""

import pandas as pd
import numpy as np

from ....distribution.base import Distribution
from ...base.generator import SeqGenerator
from .settings import StateSeqGeneratorSettings


class StateSeqGenerator(SeqGenerator, register_name="state"):
    """
    Generator for state sequences.
    """

    SETTINGS_DATACLASS = StateSeqGeneratorSettings

    def __init__(self, settings=None):
        if settings is None:
            settings = StateSeqGeneratorSettings()
        super().__init__(settings)

        ## -- time design cache
        self.t0_strategy = None
        self.sampling_strategy = None
        self.last_state_durations = None

        ## -- profile-specific cache
        self.methods_by_col = None
        self.seq_sizes = None

    def generate(self):
        """
        Generate mock data.
        """
        ## -- reset summary
        self.summary = None
        self.t0_strategy = self._resolve_time_strategy(
            self.settings.time_design.t0_strategy
        )
        self.sampling_strategy = self._resolve_time_strategy(
            self.settings.time_design.sampling_strategy
        )

        ## -- loop over profiles
        all_profiles = []
        for i, profile in enumerate(self._iter_profile()):
            data_profile = self._generate_single_profile(profile, i)
            all_profiles.append(data_profile)

        data = pd.concat(all_profiles, ignore_index=True)
        return self._generate_end_columns_if_needed(data)

    def _generate_single_profile(self, profile, index):
        """Generate data for a single profile."""
        id_provided = profile.profile_id
        id_profile = id_provided if id_provided is not None else f"profile-{index}"
        data_profile = self._init_data(profile.n_seq, id_profile)
        seq_sizes = self._resolve_seq_sizes(profile.sequence_size, profile.n_seq)

        data_profile = self._sampling_time(data_profile, seq_sizes)
        data_profile = self._add_data_columns(data_profile, profile.data_cols)
        data_profile = self._apply_missing_data(data_profile, profile.missing_data)

        self._update_summary(data_profile, id_profile)

        return data_profile

    def _generate_end_columns_if_needed(self, data):
        if self.settings.output_columns.end_column is None:
            return data

        id_column = self.settings.output_columns.id_column
        start_column = self.settings.output_columns.start_column
        end_column = self.settings.output_columns.end_column
        data[end_column] = data.groupby(id_column)[start_column].shift(-1)

        ## last state
        last_state_duration = self._resolve_last_state_duration(data)
        last_states_mask = data[end_column].isna()
        which_nas = last_states_mask[last_states_mask].index
        len_nas = len(which_nas)
        if len_nas > 0:
            chosen_durations = np.random.choice(
                last_state_duration, size=len_nas, replace=True
            )

            data.loc[last_states_mask, end_column] = (
                data.loc[last_states_mask, start_column] + chosen_durations
            )

        ## -- update summary
        self.summary["_LAST_STATE_DURATION_"] = [self.last_state_durations] * len(
            self.summary
        )
        return data

    def _sampling_time(self, data, seq_sizes):
        """
        Sample a time from the time strategy.

        Args:
            data (pd.DataFrame): Input dataframe containing sequence or event data.
            seq_sizes (list of int): Sequence sizes

        Returns:
            A dataframe with columns "id" and "time".
        """
        sampling_strategy = self.sampling_strategy
        t0_strategy = self.t0_strategy

        data = t0_strategy.add_t0_column(data, t0_col="__T0__")
        data = sampling_strategy.populate_timeline(
            data,
            seq_sizes,
            t0_col="__T0__",
            time_col=self.settings.output_columns.start_column,
        )
        ## -- cache
        self.seq_sizes = seq_sizes

        return data

    def _add_data_columns(self, data, column_methods):
        """
        Generate and add custom data columns to the dataframe using group-specific methods.

        Each column in `column_methods` is computed by applying a custom method
        to each group of rows (grouped by sequence ID or similar identifier).

        Args:
            data (pd.DataFrame): Input dataframe containing sequence or event data.
            column_methods (Dict[str, Any]): A mapping from column names to method specifications.
                Each method will be resolved and applied to the grouped data to generate
                the corresponding column.

        Returns:
            pd.DataFrame: The original dataframe with new columns added.
        """
        methods_by_col = {
            col_name: self._resolve_method(method)
            for col_name, method in column_methods.items()
        }

        id_column = self.settings.output_columns.id_column
        data.set_index(id_column, inplace=True)
        grouped_data = data.groupby(id_column, group_keys=False)

        def _apply_column_methods(group):
            for col_name, method in methods_by_col.items():
                group[col_name] = method.populate_column(group, col_name)
            return group

        ## -- cache
        self.methods_by_col = methods_by_col

        data = grouped_data.apply(_apply_column_methods)
        return data.reset_index(drop=False)

    def _create_profile_data(self, unique_ids, id_profile):
        """
        Create a DataFrame containing profile information.

        Parameters:
        - unique_ids: Array of unique IDs in the profile
        - id_profile: Identifier for the current profile

        Returns:
        - DataFrame with profile metadata
        """
        id_column = self.settings.output_columns.id_column

        # Create base profile data
        profile_data = pd.DataFrame(
            {
                id_column: unique_ids,
                "_PROFILE_ID_": id_profile,
                "_SEQ_SIZE_": self.seq_sizes,
                "_T0_": self.t0_strategy.summary_desc(),
                "_TIME_SAMPLING_": self.sampling_strategy.summary_desc(),
            }
        )

        # Add column generation methods information
        data_col_summary = {
            f"_{col.upper()}-GENERATION_METHOD_": [method.summary_desc()]
            * len(unique_ids)
            for col, method in self.methods_by_col.items()
        }
        profile_data = pd.concat(
            [profile_data, pd.DataFrame(data_col_summary)],
            axis=1,
        )

        # Add missing data information if applicable
        if self.missing_data is not None:
            data_missing_summary = {
                f"_{col.upper()}-MISSING_DATA_": [rate] * len(unique_ids)
                for col, rate in self.missing_data.items()
            }
            profile_data = pd.concat(
                [profile_data, pd.DataFrame(data_missing_summary)],
                axis=1,
            )

        return profile_data

    def _resolve_last_state_duration(self, data):
        """
        Resolve last state durations.

        Args:
            data (pd.DataFrame): Input dataframe containing sequence data.

        Returns:
            list of timedelta: List of last state durations.
        """
        last_state_durations = self.settings.time_design.last_state_durations
        granularity = self.settings.time_design.granularity

        if isinstance(last_state_durations, str):
            last_state_durations = Distribution.get_registered(last_state_durations)()

        if isinstance(last_state_durations, Distribution):
            last_state_durations = last_state_durations.sample(len(data))

        self.last_state_durations = granularity.to_offsets(last_state_durations)
        return self.last_state_durations
