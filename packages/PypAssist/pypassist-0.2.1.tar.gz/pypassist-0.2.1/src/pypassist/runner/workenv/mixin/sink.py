#!/usr/bin/env python3
"""
Sink mixin implementation.
"""

from ....utils.kwargs import validate_kwargs_signature
from ..component.sink import SinkComponent
from .exceptions import InvalidConsumeSignatureError, REQUIRE_KWARGS_SIGNATURE


class SinkMixin(SinkComponent):
    """Mixin that implements get_assetable_func for sinks."""

    def get_assetable_func(self):
        """Convert consume method to assetable function.

        Returns:
            A function that can be used as a dagster asset
        """

        validate_kwargs_signature(
            obj=self,
            method_name="consume",
            required_params=REQUIRE_KWARGS_SIGNATURE,
            exception_type=InvalidConsumeSignatureError,
        )

        def asset_func(**inputs):
            # Simply pass all inputs to consume
            return self.consume(**inputs)

        asset_func.__name__ = self.__class__.__name__
        return asset_func
