#!/usr/bin/env python3
"""
Source mixin implementation.
"""

from ....utils.kwargs import validate_kwargs_signature
from ..component.source import SourceComponent
from .exceptions import InvalidProvideSignatureError, REQUIRE_KWARGS_SIGNATURE


class SourceMixin(SourceComponent):
    """Mixin that implements get_assetable_func for sources."""

    def get_assetable_func(self):
        """Convert provide method to assetable function.

        Returns:
            A function that can be used as a dagster asset
        """
        validate_kwargs_signature(
            obj=self,
            method_name="provide",
            required_params=REQUIRE_KWARGS_SIGNATURE,
            exception_type=InvalidProvideSignatureError,
        )

        def asset_func(**inputs):
            # Simply pass all inputs to provide
            return self.provide(**inputs)

        asset_func.__name__ = self.__class__.__name__
        return asset_func
