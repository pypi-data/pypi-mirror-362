#!/usr/bin/env python3
"""
Processor mixin implementation.
"""

import inspect

from ....utils.kwargs import validate_kwargs_signature
from ..component.processor import ProcessorComponent
from .exceptions import InvalidProcessSignatureError, REQUIRE_KWARGS_SIGNATURE


class ProcessorMixin(ProcessorComponent):
    """Mixin that implements get_assetable_func for processors."""

    def get_assetable_func(self):
        """Convert process method to assetable function.

        Returns:
            A function that can be used as a dagster asset
        """
        validate_kwargs_signature(
            obj=self,
            method_name="process",
            required_params=REQUIRE_KWARGS_SIGNATURE,
            exception_type=InvalidProcessSignatureError,
        )

        def asset_func(**inputs):
            # Simply pass all inputs to process
            return self.process(**inputs)

        # conserve name & signature & type hints
        asset_func.__name__ = self.__class__.__name__
        original_signature = inspect.signature(self.process)
        asset_func.__annotations__ = self.process.__annotations__
        asset_func.__signature__ = original_signature
        return asset_func
