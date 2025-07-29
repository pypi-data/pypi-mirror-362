#!/usr/bin/env python3
"""Settings configuration for Sequence-Specific Time Strategy in temporal sequence generation."""

import logging
from typing import Union
from datetime import datetime, timedelta

from pydantic.dataclasses import dataclass, Field
from pypassist.dataclass.decorators.viewer import viewer

from ....distribution.base import Distribution

LOGGER = logging.getLogger(__name__)


@viewer
@dataclass
class SeqSpeTimeStrategySettings:
    """Configuration settings for sequence-specific temporal sampling.

    Defines a flexible time sampling strategy that generates timestamps
    using a probabilistic distribution within a specified date range.

    Args:
        distribution (Union[str, Distribution], optional):
            Probability distribution for generating normalized time deltas.
            - Samples timestamps from a normalized [0, 1] range
            - Can be a distribution name or Distribution instance
            Defaults to "uniform" distribution.
        min_date (datetime, optional):
            Lower bound for generated timestamps.
            Defaults to current datetime.
        max_date (datetime, optional):
            Upper bound for generated timestamps.
            Defaults to current datetime + 1 year.

    Example:
        # Generate timestamps using normal distribution
        # between Jan 2025 and Dec 2026
        SeqSpeTimeStrategySettings(
            distribution="normal",
            min_date=datetime(2025, 1, 1),
            max_date=datetime(2026, 12, 31)
        )
    """

    distribution: Union[str, Distribution] = "uniform"
    min_date: datetime = Field(default_factory=datetime.now)
    max_date: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(days=365)
    )
