#!/usr/bin/env python3
"""Tseqmock exceptions."""


class TSeqMockError(Exception):
    """Base class for tseqmock exceptions."""


class MissingProfilesError(TSeqMockError):
    """Raised when no profiles are defined in the settings."""
