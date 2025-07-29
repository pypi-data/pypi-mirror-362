#!/usr/bin/env python3
"""Settings configuration for Fixed Time Strategy in temporal sequence generation."""

from typing import Union
import logging
from datetime import datetime

from pydantic.dataclasses import dataclass, Field
from pypassist.dataclass.decorators.viewer import viewer
from pypassist.fallback.typing import List

from ....generator.base.utils import ensure_calendar_aware_int
from ....generator.base.granularity import Granularity


LOGGER = logging.getLogger(__name__)


def sampling_steps_factory():
    """Generate default sampling step durations.

    Returns:
        list: Default list of sampling steps from 1 to 9.
    """
    return list(range(1, 10))


@viewer
@dataclass
class FixedTimeStrategySettings:
    """Configuration settings for fixed-interval temporal sequence sampling.

    Defines a deterministic time sampling strategy with fixed intervals
    between sequence points, supporting various time granularities.

    Args:
        t0_date (datetime, optional): Initial reference timestamp
            for sequence generation. Defaults to current time.
        sampling_steps (List[Union[int, float]], optional):
            Incremental steps between sampling points.
            - Steps are applied sequentially
            - List wraps if more values are needed
            - Values interpreted based on specified granularity
            Defaults to [1, 2, 3, 4, 5, 6, 7, 8, 9].
        granularity (Granularity, optional): Time unit for interpreting
            sampling steps.
            - Supports calendar and fixed-duration granularities
            - Calendar units (MONTH, YEAR) require integer steps
            Defaults to DAY.

    Example:
        # Generate sequences with steps of 1 week, 1 month, 3 months
        FixedTimeStrategySettings(
            t0_date=datetime(2025, 1, 1),
            sampling_steps=[7, 30, 90],
            granularity=Granularity.DAY
        )
    """

    t0_date: datetime = Field(default_factory=datetime.now)
    sampling_steps: List[Union[int, float]] = Field(
        default_factory=sampling_steps_factory
    )
    granularity: Granularity = Granularity.DAY

    def __post_init__(self):
        """Validate and process sampling step configuration.

        Performs post-initialization validation:
        - Checks that values are numeric
        - Ensures calendar-aware granularities use integer values
        """
        if isinstance(self.sampling_steps, list):
            if not all(isinstance(x, (int, float)) for x in self.sampling_steps):
                raise ValueError(
                    f"Invalid sampling steps: {self.sampling_steps}."
                    " If list is provided, all elements must be integers or floats."
                )

        if self.granularity.is_calendar_based:
            converted = ensure_calendar_aware_int(self.sampling_steps, self.granularity)
            self.sampling_steps = converted
