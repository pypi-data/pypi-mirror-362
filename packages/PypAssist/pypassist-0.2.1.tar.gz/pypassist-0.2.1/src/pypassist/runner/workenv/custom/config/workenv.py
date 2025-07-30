"""
Custom work environment configuration.
"""

from pydantic.dataclasses import dataclass, Field

from .....fallback.typing import Dict
from .....dataclass.decorators.exportable.decorator import exportable
from .....dataclass.decorators.wenv.decorator import wenv
from .processor import CustomProcessorConfig
from .sink import CustomSinkConfig
from .source import CustomSourceConfig


@wenv
@exportable(strategy="wenv", stem_file="workenv_defaults")
@dataclass
class CustomWorkEnvConfig:
    """
    Custom work environment configuration.
    """

    processors: Dict[str, CustomProcessorConfig] = Field(default_factory=dict)
    sink: Dict[str, CustomSinkConfig] = Field(default_factory=dict)
    sources: Dict[str, CustomSourceConfig] = Field(default_factory=dict)
