#!/usr/bin/env python3
"""
Runner application configuration decorator.
"""

from pydantic.dataclasses import dataclass

from ....fallback.pydantic import is_pydantic_dataclass
from ....runner.workflow.config.base import WorkflowConfig
from ..wenv.validation import is_wenv
from .exceptions import RunnerAttributeError


def runner(_cls=None):
    """Decorator to ensure the configuration structure of a runner application.

    - Checks the presence of the workflow attribute: WorkflowConfig
    - Checks that workenv is a class decorated with @wenv
    - Adds utility methods for integration with Hydra
    """

    def wrap(cls):
        if not is_pydantic_dataclass(cls):
            cls = dataclass(cls)

        class RunnerAppConfig(cls):  # pylint: disable=C0115, R0903
            def __post_init__(self):
                if hasattr(super(), "__post_init__"):
                    super().__post_init__()

                if not hasattr(self, "workflow"):
                    raise RunnerAttributeError(
                        f"Missing required attribute 'workflow' in {self.__class__.__name__}. "
                        "Ensure you define a 'workflow' attribute in your runner app config dataclass."
                    )
                if not hasattr(self, "workenv"):
                    raise RunnerAttributeError(
                        f"Missing required attribute 'workenv' in {self.__class__.__name__}. "
                        "Ensure you define a 'workenv' attribute in your runner app config dataclass."
                    )

                if not isinstance(self.workflow, WorkflowConfig):
                    raise RunnerAttributeError(
                        f"Invalid type for 'workflow' in {self.__class__.__name__}. "
                        f"Expected 'WorkflowConfig', got {type(self.workflow).__name__}."
                    )
                if not is_wenv(self.workenv):
                    raise RunnerAttributeError(
                        f"Invalid work environment in {self.__class__.__name__}. "
                        "The 'workenv' attribute must be decorated with @wenv."
                    )

        RunnerAppConfig.__name__ = cls.__name__
        RunnerAppConfig.__qualname__ = cls.__qualname__
        RunnerAppConfig.__module__ = cls.__module__
        return RunnerAppConfig

    if _cls is None:
        return wrap
    return wrap(_cls)
