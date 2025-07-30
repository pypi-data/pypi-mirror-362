#!/usr/bin/env python3
"""
Utilities for working with Hydra.
"""

import os
from pathlib import Path


def get_working_dir():
    """Get working directory where the app was launched from.

    Returns:
        Path: Working directory path
    """
    # Get absolute path of the current working directory
    return Path(os.getcwd()).resolve()


def get_config_path():
    """Get path to config directory relative to working directory.

    Returns:
        Path: Path to config directory
    """
    working_dir = get_working_dir()
    return working_dir / "config"
