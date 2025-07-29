#!/usr/bin/env python3
"""
Configuration settings for state sequence generation.
"""

from typing import Optional

from pydantic.dataclasses import dataclass, Field
from pypassist.dataclass.decorators.viewer import viewer
from pypassist.fallback.typing import List

from .time_design import StateTimeDesign
from ...base.settings import BaseSeqGeneratorSettings
from ...base.profile import Profile


@viewer
@dataclass
class StateOutputColumns:
    """Configuration for output columns in state sequence generation.

    Defines the column names for sequence identification and
    temporal attributes in generated state sequences.

    Attributes:
        id_column (str, optional): Name of the column containing
            unique sequence identifiers. Defaults to "id".
        start_column (str, optional): Name of the column containing
            state start timestamps. Defaults to "start_date".
        end_column (str, optional): Name of the column containing
            state end timestamps. Defaults to None.

    Example:
        # Customize output column names
        columns = StateOutputColumns(
            id_column="state_sequence_id",
            start_column="state_start_time",
            end_column="state_end_time"
        )
    """

    id_column: str = "id"
    start_column: str = "start_date"
    end_column: Optional[str] = None


@viewer
@dataclass
class StateSeqGeneratorSettings(BaseSeqGeneratorSettings):
    """Configuration settings for state sequence generation.

    Extends the base sequence generator settings with state-specific
    configuration options, including time design, output columns,
    and generation profiles.

    Attributes:
        time_design (StateTimeDesign, optional): Temporal design
            configuration for state sequence generation.
            Defaults to a new StateTimeDesign instance.
        profiles (List[Profile], optional): List of generation profiles
            to apply during sequence creation.
        sequence_id (str, optional): Base identifier for generated
            sequences. Defaults to "seq".
        output_columns (StateOutputColumns, optional): Configuration
            for output column naming. Defaults to standard state
            output column settings.

    Example:
        # Configure state sequence generator with custom settings
        settings = StateSeqGeneratorSettings(
            time_design=custom_time_design,
            profiles=[profile1, profile2],
            sequence_id="seq",
            output_columns=custom_columns
        )
    """

    time_design: StateTimeDesign = Field(default_factory=StateTimeDesign)
    profiles: Optional[List[Profile]] = None
    sequence_id: str = "seq"
    output_columns: StateOutputColumns = Field(default_factory=StateOutputColumns)
