#!/usr/bin/env python3
"""
Time design configuration for state sequence generation.
"""

from typing import Union

from pydantic.dataclasses import dataclass
from pypassist.dataclass.decorators.viewer import viewer
from pypassist.fallback.typing import List

from ....distribution.base import Distribution
from ....time_strategy.base import TimeStrategy
from ...base.utils import ensure_calendar_aware_int
from ...base.granularity import Granularity


@viewer
@dataclass
class StateTimeDesign:
    """Configuration for temporal design of state sequences.

    Defines strategies for generating initial timestamps, sampling
    state start times, and determining state durations in temporal
    sequence generation.

    Attributes:
        t0_strategy (Union[str, TimeStrategy], optional):
            Strategy to generate the initial timestamp (T0) for
            each state sequence.
            - Can be a string identifier or TimeStrategy instance
            - Determines the starting point of each sequence
            Defaults to "sequence_specific" strategy.

        sampling_strategy (Union[str, TimeStrategy], optional):
            Strategy used to determine the start times of
            individual states within a sequence.
            - Can be a string identifier or TimeStrategy instance
            - Controls the temporal distribution of state transitions
            Defaults to "sequence_specific" strategy.

        last_state_durations (Union[str, Distribution, List[Union[int, float]]], optional):
            Configuration for the duration of the last state in each sequence.
            - String: Distribution name for generating durations
            - Distribution instance: Custom duration distribution
            - List of values: Predefined duration options
            - Values interpreted based on specified granularity
            Defaults to "uniform" distribution.

        granularity (Granularity, optional):
            Temporal granularity used to interpret duration values.
            - Controls how duration values are applied
            - Supports both fixed and calendar-aware time units
            Defaults to Granularity.DAY.

    Example:
        # Configure state time design with custom strategies
        time_design = StateTimeDesign(
            t0_strategy="fixed",
            sampling_strategy="sequence_specific",
            last_state_durations=[7, 14, 30],
            granularity=Granularity.DAY
        )
    """

    t0_strategy: Union[str, TimeStrategy] = "sequence_specific"
    sampling_strategy: Union[str, TimeStrategy] = "sequence_specific"
    last_state_durations: Union[str, Distribution, List[Union[int, float]]] = "uniform"
    granularity: Granularity = Granularity.DAY

    def __post_init__(self):
        """Validate and process last state duration configuration.

        Performs post-initialization validation:
        - Checks that duration values are numeric
        - Ensures calendar-aware granularities use integer values
        """
        if isinstance(self.last_state_durations, list):
            if not all(isinstance(x, (int, float)) for x in self.last_state_durations):
                raise ValueError(
                    f"Invalid interval durations: {self.last_state_durations}."
                    " If list is provided, all elements must be integers or floats."
                )

        if self.granularity.is_calendar_based:
            converted = ensure_calendar_aware_int(
                self.last_state_durations, self.granularity
            )
            self.interval_durations = converted
