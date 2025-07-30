#!/usr/bin/env python3
"""Progress bar."""

import logging

from ..utils.ipynb import is_in_ipynb

LOGGER = logging.getLogger(__name__)


# Fallback class if tqdm is not available
class DummyTqdm:
    """A no-op progress bar fallback when tqdm is not available."""

    def __init__(self, *args, **kwargs):
        self.total = kwargs.get("total", None)
        self.n = 0

    def update(self, n=1):
        """
        Mimic tdqm update method.
        """
        self.n += n

    def close(self):
        """
        Mimic tdqm close method.
        """

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()


# Try to import tqdm, use dummy if not available
try:
    # pylint: disable=W0611
    if is_in_ipynb():
        from tqdm.notebook import tqdm  # For Jupyter Notebooks

        LOGGER.debug("Using tqdm for notebooks.")
    else:
        from tqdm import tqdm  # For normal environments

        LOGGER.debug("Using standard tqdm.")
except ImportError:
    tqdm = DummyTqdm  # pylint: disable=C0103
    LOGGER.debug("tqdm not available, progress bar disabled.")
