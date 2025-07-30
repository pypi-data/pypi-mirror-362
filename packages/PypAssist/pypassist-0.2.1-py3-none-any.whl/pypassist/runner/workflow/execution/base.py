#!/usr/bin/env python3
"""
Base execution concepts for workflow module.
"""

from abc import ABC, abstractmethod


class BaseStep(ABC):
    """Base class for workflow steps."""

    def __init__(self, config, workenv):
        self._config = config
        self.workenv = workenv
        self._component = self._config.get_component(self.workenv)

    @property
    def config(self):
        """Return step configuration."""
        return self._config

    @property
    def component(self):
        """Return step component."""
        return self._component

    @property
    def inputs(self):
        """Return step inputs."""
        return self.config.inputs

    @property
    def output_dir(self):
        """Return Path to output directory."""
        return self.config.output_dir

    @property
    def exist_ok(self):
        """Return exist_ok flag."""
        return self.config.exist_ok

    @property
    def save_results(self):
        """Return save_results flag."""
        return self.config.save_results

    @abstractmethod
    def execute(self, **inputs):
        """Execute the step."""


class BaseWorkflow(ABC):
    """Base class for workflows."""

    def __init__(self, config, workenv):
        self.config = config
        self._steps = []
        self._initialize_steps(workenv)

    @abstractmethod
    def _initialize_steps(self, workenv):
        """Initialize workflow steps."""

    @property
    def steps(self):
        """Return workflow steps."""
        return self._steps

    @property
    def components(self):
        """Return workflow components."""
        return [step.component for step in self.steps]

    @abstractmethod
    def execute(self):
        """Execute the workflow."""
