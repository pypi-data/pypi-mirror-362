#!/usr/bin/env python3
"""
Base configuration types for workflow module.
"""

import pathlib
from typing import Optional, Any

from pydantic.dataclasses import dataclass

from ....dataclass.decorators.wenv.validation import is_wenv
from ....dataclass.decorators.exportable.decorator import exportable
from ....fallback.typing import Dict, List
from ...workenv.component.exceptions import InvalidComponentError


@dataclass
class StepConfig:
    """Step configuration."""

    component_path: str  # Format: "category.name" (e.g. "sources.file")
    name: Optional[str] = None
    inputs: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    save_results: bool = True
    exist_ok: bool = False
    _output_dir: Optional[str] = None
    _workflow_output_dir: Optional[str] = None

    def __post_init__(self):
        if self.name is None:
            self.name = self.component_path.split(".")[-1]

    @property
    def output_dir(self):
        """Return Path to output directory."""
        if self._output_dir:
            return pathlib.Path(self._output_dir).resolve()
        return pathlib.Path(self._workflow_output_dir).resolve() / self.name

    def get_component(self, workenv):
        """Get component from nested sections.

        Args:
            workenv: Work environment instance

        Returns:
            Component instance
        """
        component_path = self.component_path
        *attr_path, dict_key = component_path.split(".")

        section_name = attr_path[0]
        current = getattr(workenv.config, section_name)

        if is_wenv(current):
            current = getattr(workenv, f"{section_name}")
            remaining_path = ".".join([*attr_path[1:], dict_key])
            return current.get_component(remaining_path)

        if not isinstance(current, dict):
            ## Direct component instance
            return getattr(workenv, f"{section_name}")

        component_dict = getattr(workenv, f"{section_name}")
        if dict_key not in component_dict:
            raise InvalidComponentError(
                f"{self.__class__.__name__}: Component '{dict_key}' not found in section '{section_name}'. "
                f"Available components: {', '.join(component_dict.keys())}"
            )
        return component_dict[dict_key]


@exportable(stem_file="template")
@dataclass
class WorkflowConfig:
    """Workflow configuration."""

    name: str
    steps: List[Dict]
    output_dir: str
    save_results: bool = True
    exist_ok: bool = False

    def __post_init__(self):
        step_defaults = {"exist_ok": self.exist_ok, "save_results": self.save_results}
        self.steps = [
            StepConfig(
                **{**step_defaults, **step, "_workflow_output_dir": self.output_dir}
            )
            for step in self.steps
        ]
