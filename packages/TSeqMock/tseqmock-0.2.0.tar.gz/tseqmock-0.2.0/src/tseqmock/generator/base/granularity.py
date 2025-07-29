#!/usr/bin/env python3
"""
Temporal granularity.

Note: Duplicated from tanat to avoid circular dependency
"""

import enum

import pandas as pd

from pypassist.enum.enum_str import EnumStrMixin


@enum.unique
class Granularity(EnumStrMixin, enum.Enum):
    """Enumeration of temporal granularity units for time-based operations.

    Defines standard time units for precise temporal sequence generation
    and manipulation, with support for both fixed and calendar-aware
    time increments.

    Attributes:
        HOUR: Hourly time resolution.
        DAY: Daily time resolution.
        WEEK: Weekly time resolution.
        MONTH: Monthly time resolution (calendar-aware).
        YEAR: Yearly time resolution (calendar-aware).

    Example:
        # Using granularity for time-based operations
        gran = Granularity.WEEK
        offsets = gran.to_offsets([1, 2, 3])  # Weekly increments
        is_calendar = gran.is_calendar_based  # False
    """

    UNIT = enum.auto()
    HOUR = enum.auto()
    DAY = enum.auto()
    WEEK = enum.auto()
    MONTH = enum.auto()
    YEAR = enum.auto()

    @property
    def pandas_freq(self):
        """Convert Granularity enum to pandas frequency string.

        Returns:
            str: Pandas-compatible frequency string.
        """
        freq_mapping = {
            Granularity.HOUR: "h",
            Granularity.DAY: "D",
            Granularity.WEEK: "W",
            Granularity.MONTH: "M",
            Granularity.YEAR: "Y",
        }
        return freq_mapping[self]

    @property
    def is_calendar_based(self):
        """Determine if the granularity is calendar-aware.

        Calendar-aware units (MONTH, YEAR) have variable durations
        based on calendar rules.

        Returns:
            bool: True for MONTH and YEAR, False otherwise.
        """
        return self in [Granularity.MONTH, Granularity.YEAR]

    def to_offsets(self, values):
        """Convert values to time offset objects.

        Generates time increments based on the granularity:
        - Calendar units (MONTH, YEAR) use DateOffset
        - Fixed units (WEEK, DAY, HOUR) use Timedelta

        Args:
            values (Iterable[int]): Increment values to convert.

        Returns:
            Union[TimedeltaIndex, List[DateOffset]]:
            Time offsets corresponding to input values.
        """
        ## -- Calendar-aware
        if self == Granularity.MONTH:
            return [pd.DateOffset(months=v) for v in values]
        if self == Granularity.YEAR:
            return [pd.DateOffset(years=v) for v in values]

        ## -- Fixed units
        if self == Granularity.WEEK:
            return pd.to_timedelta([v * 7 for v in values], unit="D")
        # DAY or HOUR
        return pd.to_timedelta(values, unit=self.pandas_freq)

    def truncate(self, dates):
        """Truncate dates to the start of their respective periods.

        Aligns timestamps to the beginning of the time unit defined
        by the granularity.

        Args:
            dates (Sequence[datetime]): Timestamps to truncate.

        Returns:
            Sequence[datetime]: Timestamps aligned to period starts.
        """
        return pd.to_datetime(dates).dt.to_period(self.pandas_freq).dt.start_time
