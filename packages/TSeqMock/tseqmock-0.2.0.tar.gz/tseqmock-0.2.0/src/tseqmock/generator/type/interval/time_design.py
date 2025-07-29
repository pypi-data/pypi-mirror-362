#!/usr/bin/env python3
"""
Time design configuration for interval sequence generation.
"""

from typing import Union

from pydantic.dataclasses import dataclass
from pypassist.dataclass.decorators.viewer import viewer
from pypassist.fallback.typing import List

from ....time_strategy.base import TimeStrategy
from ....distribution.base import Distribution
from ...base.utils import ensure_calendar_aware_int

from ...base.granularity import Granularity


@viewer
@dataclass
class IntervalTimeDesign:
    """Configuration for temporal design of interval sequences.

    Defines strategies for generating initial timestamps, sampling
    interval start times, and determining interval durations in
    temporal sequence generation.

    Attributes:
        t0_strategy (Union[str, TimeStrategy], optional):
            Strategy to generate the initial timestamp (T0) for
            each interval sequence.
            - Can be a string identifier or TimeStrategy instance
            - Determines the starting point of each sequence
            Defaults to "sequence_specific" strategy.

        sampling_strategy (Union[str, TimeStrategy], optional):
            Strategy used to determine the start times of
            individual intervals within a sequence.
            - Can be a string identifier or TimeStrategy instance
            - Controls the temporal distribution of intervals
            Defaults to "sequence_specific" strategy.

        interval_durations (Union[str, Distribution, List[Union[int, float]]], optional):
            Configuration for the duration of intervals in each sequence.
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
        # Configure interval time design with custom strategies
        time_design = IntervalTimeDesign(
            t0_strategy="fixed",
            sampling_strategy="sequence_specific",
            interval_durations=[1, 2, 3, 4],
            granularity=Granularity.HOUR
        )
    """

    t0_strategy: Union[str, TimeStrategy] = "sequence_specific"
    sampling_strategy: Union[str, TimeStrategy] = "sequence_specific"
    interval_durations: Union[str, Distribution, List[Union[int, float]]] = "uniform"
    granularity: Granularity = Granularity.DAY

    def __post_init__(self):
        """Validate and process interval duration configuration.

        Performs post-initialization validation:
        - Checks that duration values are numeric
        - Ensures calendar-aware granularities use integer values
        """
        if isinstance(self.interval_durations, list):
            if not all(isinstance(x, (int, float)) for x in self.interval_durations):
                raise ValueError(
                    f"Invalid interval durations: {self.interval_durations}."
                    " If list is provided, all elements must be integers or floats."
                )

        if self.granularity.is_calendar_based:
            converted = ensure_calendar_aware_int(
                self.interval_durations, self.granularity
            )
            self.interval_durations = converted
