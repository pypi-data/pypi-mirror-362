#!/usr/bin/env python3
"""
Runner config application export strategy.
"""

import dataclasses
import logging
import pathlib

from pydantic.dataclasses import dataclass

from ..base import ExportStrategy
from ...decorator import exportable
from ...validation import is_exportable
from ......fallback.typing import List, Dict

LOGGER = logging.getLogger(__name__)


@dataclass
class HydraDefaultConfig:
    """Default Hydra configuration."""

    BASE_OUTPUT_DIR: str = "./outputs"  # pylint: disable=C0103
    hydra: Dict = dataclasses.field(
        default_factory=lambda: {
            "run": {"dir": "${BASE_OUTPUT_DIR}/${now:%Y-%m-%d}/${now:%H-%M-%S}"},
            "sweep": {
                "dir": "${BASE_OUTPUT_DIR}/${now:%Y-%m-%d}/${now:%H-%M-%S}",
                "subdir": "run-${hydra:job.num}",
            },
        }
    )


@exportable(stem_file="config_template")
@dataclass
class TemplateDefaultConfigFile(HydraDefaultConfig):
    """Template default config file for a runner application."""

    defaults: List[str] = dataclasses.field(
        default_factory=lambda: [
            {"workflow": "..."},
            {"workenv": "workenv_template"},
            "_self_",
        ]
    )


class RunnerConfigExportStrategy(ExportStrategy, register_name="runner"):
    """Export strategy for runner config applications."""

    @classmethod
    def export(  # pylint: disable=too-many-arguments
        cls,
        data_cls,
        output_dir,
        format_type="yaml",
        exist_ok=False,
        makedirs=False,
        **kwargs,
    ):
        """
        Export the complete runner app configuration structure.
        """

        output_dir = pathlib.Path(output_dir).resolve()

        for field in dataclasses.fields(data_cls):
            field_type = field.type
            field_name = field.name
            if is_exportable(field_type):
                field_type.export(
                    output_dir / field_name,
                    format_type=format_type,
                    exist_ok=exist_ok,
                    makedirs=makedirs,
                    **kwargs,
                )
                continue

            LOGGER.warning(
                "Field %s of type %s is not exportable. Skipping.",
                field_name,
                field_type,
            )

        TemplateDefaultConfigFile.export(  # pylint: disable=no-member
            output_dir, format_type, exist_ok, makedirs, detailed=False
        )
