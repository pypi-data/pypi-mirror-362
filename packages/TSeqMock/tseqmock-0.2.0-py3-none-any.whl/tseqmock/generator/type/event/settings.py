#!/usr/bin/env python3
"""
Configuration settings for event sequence generation.
"""

from typing import Optional

from pydantic.dataclasses import dataclass, Field
from pypassist.dataclass.decorators.viewer import viewer
from pypassist.fallback.typing import List

from .time_design import EventTimeDesign
from ...base.settings import BaseSeqGeneratorSettings
from ...base.profile import Profile


@viewer
@dataclass
class EventOutputColumns:
    """Configuration for output columns in event sequence generation.

    Defines the column names for sequence identification and
    temporal attributes in generated event data.

    Attributes:
        id_column (str, optional): Name of the column containing
            unique sequence identifiers. Defaults to "id".
        time_column (str, optional): Name of the column containing
            event timestamps. Defaults to "date".

    Example:
        # Customize output column names
        columns = EventOutputColumns(
            id_column="event_sequence_id",
            time_column="event_timestamp"
        )
    """

    id_column: str = "id"
    time_column: str = "date"


@viewer
@dataclass
class EventSeqGeneratorSettings(BaseSeqGeneratorSettings):
    """Configuration settings for event sequence generation.

    Extends the base sequence generator settings with event-specific
    configuration options, including time design, output columns,
    and generation profiles.

    Attributes:
        time_design (EventTimeDesign, optional): Temporal design
            configuration for event sequence generation.
            Defaults to a new EventTimeDesign instance.
        profiles (List[Profile], optional): List of generation profiles
            to apply during sequence creation.
        sequence_id (str, optional): Base identifier for generated
            sequences. Defaults to "seq".
        output_columns (EventOutputColumns, optional): Configuration
            for output column naming. Defaults to standard event
            output column settings.

    Example:
        # Configure event sequence generator with custom settings
        settings = EventSeqGeneratorSettings(
            time_design=custom_time_design,
            profiles=[profile1, profile2],
            sequence_id="seq",
            output_columns=custom_columns
        )
    """

    time_design: EventTimeDesign = Field(default_factory=EventTimeDesign)
    profiles: Optional[List[Profile]] = None
    sequence_id: str = "seq"
    output_columns: EventOutputColumns = Field(default_factory=EventOutputColumns)
