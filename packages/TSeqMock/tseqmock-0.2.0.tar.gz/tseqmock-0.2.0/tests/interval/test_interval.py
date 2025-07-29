#!/usr/bin/env python3
"""
Test interval sequence generator in tseqmock.
"""

import pytest

from tseqmock.core import TSeqMocker
from tseqmock.exception import MissingProfilesError
from tseqmock.generator.base.profile import Profile
from tseqmock.generator.type.interval.time_design import IntervalTimeDesign
from tseqmock.method.base import GenMethod
from tseqmock.time_strategy.base import TimeStrategy


class TestIntervalMocker:
    """
    Test suite for IntervalMocker functionality.
    """

    def test_basic_initialization(self):
        """
        Test basic initialization of interval mocker.
        """
        mock = TSeqMocker("interval")
        assert mock is not None
        assert mock.settings.profiles is None

    def test_basic_generation(self, interval_mocker_basic, snapshot):
        """
        Test basic interval sequence generation.
        """
        mock = interval_mocker_basic
        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    @pytest.mark.parametrize(
        "interval_durations",
        [
            [1, 2, 3],
            [12, 24, 48],
        ],
    )
    def test_interval_durations(self, interval_durations, seed, snapshot):
        """
        Test interval mocker with different interval durations.
        """
        mock = TSeqMocker("interval", seed=seed)

        gen_method = GenMethod.init("random")
        gen_method.update_settings(
            vocabulary=["RESTING", "RESTAURANT", "CITY TOUR", "SHOPPING"]
        )

        mock.add_profile(
            Profile(
                n_seq=5,
                sequence_size=[3, 4, 5],
                data_cols={
                    "interval": gen_method,
                },
            )
        )

        time_strat = TimeStrategy.init("sequence_specific")

        time_strat.update_settings(
            distribution="uniform",
            min_date="2025-07-01",
            max_date="2025-08-01",
        )

        mock.set_time_design(
            time_design_settings=IntervalTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
                interval_durations=interval_durations,
                granularity="hour",
            )
        )

        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    @pytest.mark.parametrize(
        "granularity",
        [
            "hour",
            "day",
            "week",
        ],
    )
    def test_granularity_options(self, granularity, seed, snapshot):
        """
        Test interval mocker with different granularity options.
        """
        mock = TSeqMocker("interval", seed=seed)

        gen_method = GenMethod.init("random")
        gen_method.update_settings(
            vocabulary=["RESTING", "RESTAURANT", "CITY TOUR", "SHOPPING"]
        )

        mock.add_profile(
            Profile(
                n_seq=5,
                sequence_size=[3, 4, 5],
                data_cols={
                    "interval": gen_method,
                },
            )
        )

        time_strat = TimeStrategy.init("sequence_specific")

        time_strat.update_settings(
            distribution="uniform",
            min_date="2025-07-01",
            max_date="2025-08-01",
        )

        mock.set_time_design(
            time_design_settings=IntervalTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
                interval_durations=[1, 2, 3],
                granularity=granularity,
            )
        )

        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    def test_interval_multiple_columns(self, seed, snapshot):
        """
        Test interval mocker with multiple data columns.
        """
        mock = TSeqMocker("interval", seed=seed)

        interval_gen = GenMethod.init("random")
        interval_gen.update_settings(
            vocabulary=["RESTING", "RESTAURANT", "CITY TOUR", "SHOPPING"]
        )

        location_gen = GenMethod.init("random")
        location_gen.update_settings(
            vocabulary=["HOME", "DOWNTOWN", "PARK", "BEACH", "MALL"]
        )

        participants_gen = GenMethod.init("random")
        participants_gen.update_settings(vocabulary=[1, 2, 3, 4, 5])

        mock.add_profile(
            Profile(
                n_seq=7,
                sequence_size=[3, 5, 7],
                data_cols={
                    "interval": interval_gen,
                    "location": location_gen,
                    "participants": participants_gen,
                },
                missing_data={"interval": 0, "location": 0.1, "participants": 0.2},
            )
        )

        time_strat = TimeStrategy.init("sequence_specific")

        time_strat.update_settings(
            distribution="uniform",
            min_date="2025-07-01",
            max_date="2025-08-01",
        )

        mock.set_time_design(
            time_design_settings=IntervalTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
                interval_durations=[1, 2, 3, 4],
                granularity="hour",
            )
        )

        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    def test_error_handling_missing_profile(self):
        """
        Test error handling when no profile is added.
        """
        mock = TSeqMocker("interval")

        time_strat = TimeStrategy.init("fixed")
        time_strat.update_settings(
            t0_date="2025-01-01",
            sampling_steps=[7, 25, 62],
            granularity="day",
        )

        mock.set_time_design(
            time_design_settings=IntervalTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
                interval_durations=[1, 2, 3, 4],
                granularity="hour",
            )
        )

        # Generating data without adding a profile should raise an error
        with pytest.raises(MissingProfilesError):
            mock()
