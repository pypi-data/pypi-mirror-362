#!/usr/bin/env python3
"""
Test event sequence generator in tseqmock.
"""

import pytest
import numpy as np

from tseqmock.core import TSeqMocker
from tseqmock.exception import MissingProfilesError
from tseqmock.generator.base.profile import Profile
from tseqmock.generator.type.event.time_design import EventTimeDesign
from tseqmock.method.base import GenMethod
from tseqmock.time_strategy.base import TimeStrategy


class TestEventMocker:
    """
    Test suite for EventMocker functionality.
    """

    def test_basic_initialization(self):
        """
        Test basic initialization of event mocker.
        """
        mock = TSeqMocker("event")
        assert mock is not None
        assert mock.settings.profiles is None

    def test_basic_generation(self, event_mocker_basic, snapshot):
        """
        Test basic event sequence generation.
        """
        mock = event_mocker_basic
        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    @pytest.mark.parametrize(
        "profile_params",
        [
            {"n_seq": 5, "sequence_size": [2, 3, 4]},
            {"n_seq": 15, "sequence_size": [5, 10, 15]},
        ],
    )
    def test_profile_parameters(self, profile_params, seed, snapshot):
        """
        Test event mocker with different profile parameters.
        """
        mock = TSeqMocker("event", seed=seed)

        gen_method = GenMethod.init("random")
        gen_method.update_settings(vocabulary=np.random.uniform(0, 1, 100))

        mock.add_profile(
            Profile(
                n_seq=profile_params["n_seq"],
                sequence_size=profile_params["sequence_size"],
                data_cols={
                    "event": gen_method,
                },
                missing_data={"event": 0},
            )
        )

        time_strat = TimeStrategy.init("fixed")
        time_strat.update_settings(
            t0_date="2025-01-01",
            sampling_steps=[7, 25, 62],
            granularity="day",
        )

        mock.set_time_design(
            time_design_settings=EventTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    @pytest.mark.parametrize(
        "fixed_time_params",
        [
            {
                "t0_date": "2025-01-01",
                "sampling_steps": [7, 25, 62],
                "granularity": "day",
            },
            {
                "t0_date": "2024-06-01",
                "sampling_steps": [1, 3, 7],
                "granularity": "week",
            },
        ],
    )
    def test_time_strategy_parameters(self, fixed_time_params, seed, snapshot):
        """
        Test event mocker with different time strategy parameters.
        """
        mock = TSeqMocker("event", seed=seed)

        gen_method = GenMethod.init("random")
        gen_method.update_settings(vocabulary=np.random.uniform(0, 1, 100))

        mock.add_profile(
            Profile(
                n_seq=5,
                sequence_size=[3, 5, 7],
                data_cols={
                    "event": gen_method,
                },
                missing_data={"event": 0},
            )
        )

        time_strat = TimeStrategy.init("fixed")
        time_strat.update_settings(**fixed_time_params)

        mock.set_time_design(
            time_design_settings=EventTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    def test_multiple_profiles(self, seed, snapshot):
        """
        Test event mocker with multiple profiles.
        """
        mock = TSeqMocker("event", seed=seed)

        # Create two different profiles
        gen_method1 = GenMethod.init("random")
        gen_method1.update_settings(vocabulary=np.random.uniform(0, 1, 100))

        gen_method2 = GenMethod.init("random")
        gen_method2.update_settings(vocabulary=np.random.uniform(10, 20, 100))

        # Add first profile
        mock.add_profile(
            Profile(
                n_seq=5,
                sequence_size=[3, 4, 5],
                data_cols={
                    "event": gen_method1,
                    "severity": gen_method2,
                },
                missing_data={
                    "event": 0,
                    "severity": 0.2,
                },  # 20% missing values for severity
            )
        )

        # Add second profile
        mock.add_profile(
            Profile(
                n_seq=3,
                sequence_size=[2, 3],
                data_cols={
                    "event": gen_method2,
                    "severity": gen_method1,
                },
                missing_data={"event": 0, "severity": 0},
            )
        )

        time_strat = TimeStrategy.init("fixed")
        time_strat.update_settings(
            t0_date="2025-01-01",
            sampling_steps=[7, 25, 62],
            granularity="day",
        )

        mock.set_time_design(
            time_design_settings=EventTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        sequence_data = mock()

        # Check that severity has missing values (due to the first profile's 20% missing specification)
        assert sequence_data["severity"].isna().sum() > 0
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    def test_error_handling_missing_profile(self):
        """
        Test error handling when no profile is added.
        """
        mock = TSeqMocker("event")

        time_strat = TimeStrategy.init("fixed")
        time_strat.update_settings(
            t0_date="2025-01-01",
            sampling_steps=[7, 25, 62],
            granularity="day",
        )

        mock.set_time_design(
            time_design_settings=EventTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        # Generating data without adding a profile should raise an error
        with pytest.raises(MissingProfilesError):
            mock()
