#!/usr/bin/env python3
"""Unit tests for the @runner decorator."""

import unittest
from typing import Dict, Any, List
from pydantic.dataclasses import dataclass

from pypassist.dataclass.decorators.runner import runner, RunnerAttributeError
from pypassist.dataclass.decorators.wenv import wenv
from pypassist.runner.workflow.config.base import WorkflowConfig


class TestRunnerDecorator(unittest.TestCase):
    """Test cases for the @runner decorator functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""

        @dataclass
        class MinimalWorkflow(WorkflowConfig):
            """Minimal workflow for testing."""

            name: str = "test"
            steps: List[Dict] = None
            output_dir: str = "./output"

            def __post_init__(self):
                if self.steps is None:
                    self.steps = [{"component_path": "test.op"}]
                super().__post_init__()

        cls.MinimalWorkflow = MinimalWorkflow

    def test_basic_decoration(self):
        """Test basic decoration of a dataclass."""

        @wenv
        @dataclass
        class TestWorkEnv:
            """Test work environment."""

            settings: Dict[str, Any] = None

        @runner
        @dataclass
        class TestConfig:
            """Test configuration class."""

            workflow: self.MinimalWorkflow
            workenv: TestWorkEnv

        # Create an instance with valid workflow and workenv
        config = TestConfig(
            workflow=self.MinimalWorkflow(),
            workenv=TestWorkEnv(settings={"param": "value"}),
        )

        # Verify instance creation succeeds
        self.assertIsInstance(config.workflow, WorkflowConfig)
        self.assertTrue(hasattr(config.workenv, "_WENV_"))

    def test_invalid_setup(self):
        """Test handling of invalid setup configuration."""

        # Test missing workflow attribute
        @runner
        @dataclass
        class MissingWorkflowConfig:
            """Test config missing workflow attribute."""

            workenv: Dict[str, Any]

            def __post_init__(self):
                if hasattr(super(), "__post_init__"):
                    super().__post_init__()

        with self.assertRaises(RunnerAttributeError):
            MissingWorkflowConfig(workenv={"settings": {}})

        # Test missing workenv attribute
        @runner
        @dataclass
        class MissingWorkEnvConfig:
            """Test config missing workenv attribute."""

            workflow: self.MinimalWorkflow

            def __post_init__(self):
                if hasattr(super(), "__post_init__"):
                    super().__post_init__()

        with self.assertRaises(RunnerAttributeError):
            MissingWorkEnvConfig(workflow=self.MinimalWorkflow())

        # Test invalid workflow type
        @dataclass
        class InvalidWorkflow:
            """Invalid workflow (not inheriting from WorkflowConfig)."""

            name: str = "test"

        @runner
        @dataclass
        class InvalidWorkflowConfig:
            """Test config with invalid workflow type."""

            workflow: InvalidWorkflow
            workenv: Dict[str, Any]

            def __post_init__(self):
                if hasattr(super(), "__post_init__"):
                    super().__post_init__()

        with self.assertRaises(RunnerAttributeError):
            InvalidWorkflowConfig(
                workflow=InvalidWorkflow(name="test"), workenv={"settings": {}}
            )

        # Test invalid workenv type
        @dataclass
        class InvalidWorkEnv:
            """Invalid work environment (missing @wenv decorator)."""

            settings: Dict[str, Any] = None

        @runner
        @dataclass
        class InvalidWorkEnvConfig:
            """Test config with invalid workenv type."""

            workflow: self.MinimalWorkflow
            workenv: InvalidWorkEnv

            def __post_init__(self):
                if hasattr(super(), "__post_init__"):
                    super().__post_init__()

        with self.assertRaises(RunnerAttributeError):
            InvalidWorkEnvConfig(
                workflow=self.MinimalWorkflow(), workenv=InvalidWorkEnv()
            )


if __name__ == "__main__":
    unittest.main()
