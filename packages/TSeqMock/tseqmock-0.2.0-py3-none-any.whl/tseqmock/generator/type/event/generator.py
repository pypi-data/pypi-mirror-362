#!/usr/bin/env python3
"""
Generator for temporal event sequences with configurable strategies.
"""

import pandas as pd

from ...base.generator import SeqGenerator
from .settings import EventSeqGeneratorSettings


class EventSeqGenerator(SeqGenerator, register_name="event"):
    """Generator for creating synthetic temporal event sequences.

    Provides a flexible framework for generating event-based temporal
    sequences with customizable time strategies, data generation methods,
    and profile configurations.

    Attributes:
        SETTINGS_DATACLASS (Type[EventSeqGeneratorSettings]):
            Configuration class for event sequence generation.
        t0_strategy (TimeStrategy): Strategy for generating initial timestamps.
        sampling_strategy (TimeStrategy): Strategy for sampling event timestamps.
        methods_by_col (Dict[str, GenMethod]): Generation methods for each column.
        seq_sizes (List[int]): Sizes of generated sequences.

    Example:
        # Create an event sequence generator with custom configuration
        generator = EventSeqGenerator(
            settings=custom_settings
        )
        event_sequences = generator.generate()
    """

    SETTINGS_DATACLASS = EventSeqGeneratorSettings

    def __init__(self, settings=None):
        """Initialize event sequence generator.

        Args:
            settings (EventSeqGeneratorSettings, optional):
                Configuration for event sequence generation.
                Defaults to default EventSeqGeneratorSettings.
        """
        if settings is None:
            settings = EventSeqGeneratorSettings()
        super().__init__(settings)

        ## -- time design cache
        self.t0_strategy = None
        self.sampling_strategy = None

        ## -- profile-specific cache
        self.methods_by_col = None
        self.seq_sizes = None

    def generate(self):
        """Generate mock event sequence data.

        Generates temporal event sequences based on configured profiles,
        time strategies, and generation methods.

        Returns:
            pd.DataFrame: Generated event sequence data with timestamps
            and event attributes.
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

        return pd.concat(all_profiles, ignore_index=True)

    def _generate_single_profile(self, profile, index):
        """Generate data for a single generation profile.

        Args:
            profile (Profile): Configuration for sequence generation.
            index (int): Index of the current profile.

        Returns:
            pd.DataFrame: Generated event sequence data for the profile.
        """
        id_provided = profile.profile_id
        id_profile = id_provided if id_provided is not None else f"profile-{index}"
        data_profile = self._init_data(profile.n_seq, id_profile)
        seq_sizes = self._resolve_seq_sizes(profile.sequence_size, profile.n_seq)

        data_profile = self._sampling_time(data_profile, seq_sizes)
        data_profile = self._add_data_columns(data_profile, profile.data_cols)
        data_profile = self._apply_missing_data(data_profile, profile.missing_data)

        self._update_summary(data_profile, id_profile)

        return data_profile

    def _sampling_time(self, data, seq_sizes):
        """Sample timestamps for event sequences.

        Applies time strategies to generate initial and event timestamps.

        Args:
            data (pd.DataFrame): Input dataframe with sequence identifiers.
            seq_sizes (List[int]): Number of events in each sequence.

        Returns:
            pd.DataFrame: Dataframe with added timestamp columns.
        """
        sampling_strategy = self.sampling_strategy
        t0_strategy = self.t0_strategy

        data = t0_strategy.add_t0_column(data, t0_col="__T0__")
        data = sampling_strategy.populate_timeline(
            data,
            seq_sizes,
            t0_col="__T0__",
            time_col=self.settings.output_columns.time_column,
        )
        ## -- cache
        self.seq_sizes = seq_sizes

        return data

    def _add_data_columns(self, data, column_methods):
        """Generate and add custom data columns to event sequences.

        Applies generation methods to create event-specific attributes.

        Args:
            data (pd.DataFrame): Input dataframe with sequence timestamps.
            column_methods (Dict[str, Any]): Methods for generating column data.

        Returns:
            pd.DataFrame: Dataframe with additional event attributes.
        """
        methods_by_col = {
            col_name: self._resolve_method(method)
            for col_name, method in column_methods.items()
        }

        id_col = self.settings.output_columns.id_column
        data.set_index(id_col, inplace=True)
        grouped_data = data.groupby(id_col, group_keys=False)

        def _apply_column_methods(group):
            for col_name, method in methods_by_col.items():
                group[col_name] = method.populate_column(group, col_name)
            return group

        ## -- cache
        self.methods_by_col = methods_by_col

        data = grouped_data.apply(_apply_column_methods)
        return data.reset_index(drop=False)

    def _create_profile_data(self, unique_ids, id_profile):
        """Create metadata summary for a generated event sequence profile.

        Args:
            unique_ids (array-like): Unique sequence identifiers.
            id_profile (str): Identifier for the current profile.

        Returns:
            pd.DataFrame: Metadata summary of the generated profile.
        """
        id_col = self.settings.output_columns.id_column

        # Create base profile data
        profile_data = pd.DataFrame(
            {
                id_col: unique_ids,
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
