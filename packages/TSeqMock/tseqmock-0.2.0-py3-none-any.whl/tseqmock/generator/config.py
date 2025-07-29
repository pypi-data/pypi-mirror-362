#!/usr/bin/env python3
"""
Configuration for tseqmock generator.
"""

from typing import Optional, Union

from pydantic.dataclasses import dataclass
from pypassist.dataclass.decorators import registry
from pypassist.dataclass.decorators.exportable.decorator import exportable
from pypassist.utils.typing import ParamDict

from .base.generator import SeqGenerator
from .base.settings import BaseSeqGeneratorSettings


@exportable(strategy="registry")
@registry(base_cls=SeqGenerator)
@dataclass
class GeneratorConfig:
    """Configuration for tseqmock generator."""

    name: str
    settings: Optional[Union[ParamDict, BaseSeqGeneratorSettings]] = None

    def get_generator(self):
        """
        Get the sequence generator.
        """
        return SeqGenerator.get_registered(self.name)(self.settings)
