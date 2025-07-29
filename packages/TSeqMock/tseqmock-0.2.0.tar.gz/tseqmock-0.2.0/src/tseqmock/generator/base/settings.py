#!/usr/bin/env python3
"""
Base configuration settings for temporal sequence generation.
"""

import dataclasses
from typing import Any, Optional


@dataclasses.dataclass
class BaseSeqGeneratorSettings:
    """Base configuration for temporal sequence generator settings.

    Provides a minimal configuration structure for sequence generation,
    enforcing the definition of output column and time design specifications.

    Attributes:
        output_columns (Any): Configuration for output column specifications.
            Defines how generated sequence data will be structured and labeled.
        time_design (Any, optional): Configuration for temporal design of
            the sequence generation process. Specifies how timestamps
            and time-related attributes are generated.

    Example:
        # Typical usage in subclasses
        class EventGeneratorSettings(BaseSeqGeneratorSettings):
            output_columns: EventOutputColumns
            time_design: EventTimeDesign
            profiles: List[Profile] = None
    """

    output_columns: Any
    time_design: Any
    sequence_id: Optional[str] = "seq"
    profiles: Optional[list] = None
