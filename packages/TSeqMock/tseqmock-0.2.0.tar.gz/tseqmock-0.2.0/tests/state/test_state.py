#!/usr/bin/env python3
"""
Test state sequence generator in tseqmock.
"""

import pytest
import numpy as np

from tseqmock.core import TSeqMocker
from tseqmock.exception import MissingProfilesError
from tseqmock.generator.base.profile import Profile
from tseqmock.generator.type.state.time_design import StateTimeDesign
from tseqmock.method.base import GenMethod
from tseqmock.time_strategy.base import TimeStrategy
from tseqmock.distribution.base import Distribution


class TestStateMocker:
    """
    Test suite for StateMocker functionality.
    """

    def test_basic_initialization(self):
        """
        Test basic initialization of state mocker.
        """
        mock = TSeqMocker("state")
        assert mock is not None
        assert mock.settings.profiles is None

    def test_basic_generation(self, state_mocker_basic, snapshot):
        """
        Test basic state sequence generation.
        """
        mock = state_mocker_basic
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
        Test state mocker with different profile parameters.
        """
        np.random.seed(seed)

        mock = TSeqMocker("state")

        gen_method = GenMethod.init("random")
        gen_method.update_settings(vocabulary=["HEALTHY", "SICK", "REMISSION"])

        mock.add_profile(
            Profile(
                n_seq=profile_params["n_seq"],
                sequence_size=profile_params["sequence_size"],
                data_cols={
                    "state": gen_method,
                },
                missing_data={"state": 0},
            )
        )

        distrib = Distribution.init("normal", settings={"mu": 3, "sigma": 100})
        time_strat = TimeStrategy.init("sequence_specific")

        time_strat.update_settings(
            distribution=distrib,
            min_date="1980-01-01",
            max_date="2026-01-01",
        )

        mock.set_time_design(
            time_design_settings=StateTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    def test_different_state_vocabularies(self, seed, snapshot):
        """
        Test state mocker with different state vocabularies.
        """
        np.random.seed(seed)

        mock = TSeqMocker("state")

        # Test with a different set of states
        gen_method = GenMethod.init("random")
        gen_method.update_settings(
            vocabulary=["NORMAL", "WARNING", "CRITICAL", "FAILURE"]
        )

        mock.add_profile(
            Profile(
                n_seq=7,
                sequence_size=[4, 6, 8],
                data_cols={
                    "state": gen_method,
                },
                missing_data={"state": 0},
            )
        )

        distrib = Distribution.init("normal", settings={"mu": 3, "sigma": 100})
        time_strat = TimeStrategy.init("sequence_specific")

        time_strat.update_settings(
            distribution=distrib,
            min_date="1980-01-01",
            max_date="2026-01-01",
        )

        mock.set_time_design(
            time_design_settings=StateTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    @pytest.mark.parametrize(
        "sequence_specific_time_params",
        [
            {
                "distribution": "uniform",
                "min_date": "2025-01-01",
                "max_date": "2025-12-31",
            },
            {
                "distribution": "normal",
                "min_date": "2020-01-01",
                "max_date": "2030-01-01",
            },
        ],
    )
    def test_sequence_specific_time_parameters(
        self, sequence_specific_time_params, seed, snapshot
    ):
        """
        Test state mocker with different sequence-specific time parameters.
        """
        np.random.seed(seed)

        mock = TSeqMocker("state")

        gen_method = GenMethod.init("random")
        gen_method.update_settings(vocabulary=["HEALTHY", "SICK", "REMISSION"])

        mock.add_profile(
            Profile(
                n_seq=5,
                sequence_size=[3, 5, 7],
                data_cols={
                    "state": gen_method,
                },
                missing_data={"state": 0},
            )
        )

        # Create distribution if needed
        if "settings" in sequence_specific_time_params:
            distrib = Distribution.init(
                "normal", settings=sequence_specific_time_params["settings"]
            )
            params = {
                k: v
                for k, v in sequence_specific_time_params.items()
                if k != "settings"
            }
            params["distribution"] = distrib
        else:
            params = sequence_specific_time_params

        time_strat = TimeStrategy.init("sequence_specific")
        time_strat.update_settings(**params)

        mock.set_time_design(
            time_design_settings=StateTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        sequence_data = mock()
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    def test_multiple_state_columns(self, seed, snapshot):
        """
        Test state mocker with multiple state columns.
        """
        np.random.seed(seed)

        mock = TSeqMocker("state")

        # Create two different state columns
        health_gen = GenMethod.init("random")
        health_gen.update_settings(vocabulary=["HEALTHY", "SICK", "REMISSION"])

        mood_gen = GenMethod.init("random")
        mood_gen.update_settings(vocabulary=["HAPPY", "SAD", "NEUTRAL", "ANXIOUS"])

        mock.add_profile(
            Profile(
                n_seq=8,
                sequence_size=[4, 6, 8],
                data_cols={
                    "health_state": health_gen,
                    "mood_state": mood_gen,
                },
                missing_data={
                    "health_state": 0,
                    "mood_state": 0.1,
                },  # 10% missing for mood
            )
        )

        distrib = Distribution.init("normal", settings={"mu": 3, "sigma": 100})
        time_strat = TimeStrategy.init("sequence_specific")

        time_strat.update_settings(
            distribution=distrib,
            min_date="1980-01-01",
            max_date="2026-01-01",
        )

        mock.set_time_design(
            time_design_settings=StateTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        sequence_data = mock()
        # Check that mood_state has some missing values
        assert sequence_data["mood_state"].isna().sum() > 0
        snapshot.assert_match(sequence_data.to_csv())
        snapshot.assert_match(mock.summary.to_csv())

    def test_error_handling_missing_profile(self):
        """
        Test error handling when no profile is added for state mocker.
        """
        mock = TSeqMocker("state")

        distrib = Distribution.init("normal", settings={"mu": 3, "sigma": 100})
        time_strat = TimeStrategy.init("sequence_specific")

        time_strat.update_settings(
            distribution=distrib,
            min_date="1980-01-01",
            max_date="2026-01-01",
        )

        mock.set_time_design(
            time_design_settings=StateTimeDesign(
                t0_strategy=time_strat,
                sampling_strategy=time_strat,
            )
        )

        # Generating data without adding a profile should raise an error
        with pytest.raises(MissingProfilesError):
            mock()
