#!/usr/bin/env python3
"""
Kwargs utils.
"""

import inspect


def validate_kwargs_signature(
    obj, method_name, required_params, exception_type=TypeError
):
    """
    Validate that the method of a given object has the required parameters in its signature.

    Args:
        obj: The object containing the method to validate.
        method_name (str): Name of the method to inspect.
        required_params (list): List of required keyword argument names.
        exception_type (Exception): Type of exception to raise if validation fails.

    Raises:
        exception_type: If the method's signature does not contain the required parameters.
    """
    method = getattr(obj, method_name, None)
    if method is None:
        raise AttributeError(
            f"{obj.__class__.__name__} has no method named '{method_name}'"
        )

    signature = inspect.signature(method)
    func_params = signature.parameters

    missing_params = [param for param in required_params if param not in func_params]
    if missing_params:
        raise exception_type(
            f"Method '{method_name}' in class '{obj.__class__.__name__}' "
            f"is missing required parameters: {missing_params}"
        )
