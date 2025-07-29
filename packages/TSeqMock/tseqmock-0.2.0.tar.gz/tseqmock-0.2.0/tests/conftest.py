#!/usr/bin/env python3
"""
Fixtures for testing tseqmock package.
"""

import pytest

from tseqmock.core import TSeqMocker
from tseqmock.generator.base.profile import Profile
from tseqmock.generator.type.event.time_design import EventTimeDesign
from tseqmock.generator.type.state.time_design import StateTimeDesign
from tseqmock.generator.type.interval.time_design import IntervalTimeDesign
from tseqmock.method.base import GenMethod
from tseqmock.time_strategy.base import TimeStrategy
from tseqmock.distribution.base import Distribution


@pytest.fixture
def seed():
    """
    Fixture for setting a consistent random seed.
    """
    return 42


@pytest.fixture
def event_mocker_basic(seed):
    """
    Create a basic event mocker with default settings.
    """
    mock = TSeqMocker("event", seed=seed)

    gen_method = GenMethod.init("random")
    gen_method.update_settings(
        vocabulary=[
            "login",
            "logout",
            "purchase",
            "search",
            "click",
            "hover",
            "scroll",
            "submit",
        ]
    )

    mock.add_profile(
        Profile(
            n_seq=10,
            sequence_size=[3, 4, 9, 3, 5],
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

    return mock


@pytest.fixture
def state_mocker_basic(seed):
    """
    Create a basic state mocker with default settings.
    """
    mock = TSeqMocker("state", seed=seed)

    gen_method = GenMethod.init("random")
    gen_method.update_settings(vocabulary=["HEALTHY", "SICK", "REMISSION"])

    mock.add_profile(
        Profile(
            n_seq=10,
            sequence_size=[3, 4, 9, 3, 5],
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

    return mock


@pytest.fixture
def interval_mocker_basic(seed):
    """
    Create a basic interval mocker with default settings.
    """
    mock = TSeqMocker("interval", seed=seed)

    gen_method = GenMethod.init("random")
    gen_method.update_settings(
        vocabulary=[
            "RESTING",
            "RESTAURANT",
            "CITY TOUR",
            "SHOPPING",
        ]
    )

    mock.add_profile(
        Profile(
            n_seq=10,
            sequence_size=[3, 4, 9, 3, 5],
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

    possible_intervals_durations = [1, 2, 3, 4]

    mock.set_time_design(
        time_design_settings=IntervalTimeDesign(
            t0_strategy=time_strat,
            sampling_strategy=time_strat,
            interval_durations=possible_intervals_durations,
            granularity="hour",
        )
    )

    return mock
