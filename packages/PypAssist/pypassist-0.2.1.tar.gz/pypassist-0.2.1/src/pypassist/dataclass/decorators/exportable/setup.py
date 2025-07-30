#!/usr/bin/env python3
"""
Setup for exportable.
"""

from dataclasses import dataclass


@dataclass
class ExportableSetup:
    """
    Setup configuration for exportable.

    Attributes:
        strategy (str): Export strategy
        hide_private (bool): Whether to hide private attributes during export
        stem_file (str): Base filename without extension for export.
            If None, the dataclass name will be used
    """

    strategy: str = "default"
    hide_private: bool = True
    stem_file: str = None
