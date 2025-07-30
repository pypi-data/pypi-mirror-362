#!/usr/bin/env python
"""
Utilities for working with Jupyter notebooks.
"""


def is_in_ipynb():
    """Check if the code is running in a Jupyter Notebook."""
    try:
        from IPython import get_ipython  # pylint: disable=import-outside-toplevel

        return get_ipython() is not None and "IPKernelApp" in get_ipython().config
    except (ImportError, AttributeError):
        return False
