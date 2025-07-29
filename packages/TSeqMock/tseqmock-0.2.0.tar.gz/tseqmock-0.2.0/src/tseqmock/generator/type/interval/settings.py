#!/usr/bin/env python3
"""
Configuration settings for interval sequence generation.
"""

from typing import Optional

from pydantic.dataclasses import dataclass, Field
from pypassist.dataclass.decorators.viewer import viewer
from pypassist.fallback.typing import List

from .time_design import IntervalTimeDesign
from ...base.settings import BaseSeqGeneratorSettings
from ...base.profile import Profile


@viewer
@dataclass
class IntervalOutputColumns:
    """Configuration for output columns in interval sequence generation.

    Defines the column names for sequence identification and
    temporal attributes in generated interval sequences.

    Attributes:
        id_column (str, optional): Name of the column containing
            unique sequence identifiers. Defaults to "id".
        start_column (str, optional): Name of the column containing
            interval start timestamps. Defaults to "start_date".
        end_column (str, optional): Name of the column containing
            interval end timestamps. Defaults to "end_date".

    Example:
        # Customize output column names
        columns = IntervalOutputColumns(
            id_column="interval_sequence_id",
            start_column="interval_start_time",
            end_column="interval_end_time"
        )
    """

    id_column: str = "id"
    start_column: str = "start_date"
    end_column: str = "end_date"


@viewer
@dataclass
class IntervalSeqGeneratorSettings(BaseSeqGeneratorSettings):
    """Configuration settings for interval sequence generation.

    Extends the base sequence generator settings with interval-specific
    configuration options, including time design, output columns,
    and generation profiles.

    Attributes:
        time_design (IntervalTimeDesign, optional): Temporal design
            configuration for interval sequence generation.
            Defaults to a new IntervalTimeDesign instance.
        profiles (List[Profile], optional): List of generation profiles
            to apply during sequence creation.
        sequence_id (str, optional): Base identifier for generated
            sequences. Defaults to "seq".
        output_columns (IntervalOutputColumns, optional): Configuration
            for output column naming. Defaults to standard interval
            output column settings.

    Example:
        # Configure interval sequence generator with custom settings
        settings = IntervalSeqGeneratorSettings(
            time_design=custom_time_design,
            profiles=[profile1, profile2],
            sequence_id="interval_seq",
            output_columns=custom_columns
        )
    """

    time_design: IntervalTimeDesign = Field(default_factory=IntervalTimeDesign)
    profiles: Optional[List[Profile]] = None
    sequence_id: str = "seq"
    output_columns: IntervalOutputColumns = Field(default_factory=IntervalOutputColumns)
