#!/usr/bin/env python3
"""
Time design configuration for event sequence generation.
"""

from typing import Union

from pydantic.dataclasses import dataclass
from pypassist.dataclass.decorators.viewer import viewer

from ....time_strategy.base import TimeStrategy


@viewer
@dataclass
class EventTimeDesign:
    """Configuration for temporal design of event sequences.

    Defines strategies for generating initial timestamps and
    sampling event dates in temporal sequence generation.

    Attributes:
        t0_strategy (Union[str, TimeStrategy], optional):
            Strategy to generate the initial timestamp (T0) for
            each event sequence.
            - Can be a string identifier or TimeStrategy instance
            - Determines the starting point of each sequence
            Defaults to "sequence_specific" strategy.

        sampling_strategy (Union[str, TimeStrategy], optional):
            Strategy used to sample dates for individual events
            within a sequence.
            - Can be a string identifier or TimeStrategy instance
            - Controls the temporal distribution of events
            Defaults to "sequence_specific" strategy.

    Example:
        # Configure custom time design for event sequences
        time_design = EventTimeDesign(
            t0_strategy="fixed",  # Use fixed initial timestamp
            sampling_strategy="sequence_specific"  # Flexible event sampling
        )
    """

    t0_strategy: Union[str, TimeStrategy] = "sequence_specific"
    sampling_strategy: Union[str, TimeStrategy] = "sequence_specific"
