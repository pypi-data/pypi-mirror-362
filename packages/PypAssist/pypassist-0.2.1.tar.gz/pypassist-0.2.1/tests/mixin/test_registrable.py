#!/usr/bin/env python3
"""
Test registrable.py mixin.
"""

import unittest

from pypassist.mixin.registrable import Registrable
from pypassist.mixin.registrable.exceptions import (
    UnregisteredTypeError,
)


class MyBaseClass(Registrable):  # pylint: disable=too-few-public-methods
    """
    Subclass of Registrable that serves as a base class for registrable classes.
    """

    _REGISTER = {}


class FooMyBaseClass(
    MyBaseClass, register_name="foo"
):  # pylint: disable=too-few-public-methods
    """
    First registrable class for testing. This is registered during setup.
    """


class BarMyBaseClass(
    MyBaseClass, register_name="bar"
):  # pylint: disable=too-few-public-methods
    """
    Second registrable class for testing. This is not registered during setup.
    """


class TestRegistrable(unittest.TestCase):
    """
    Test Registrable.
    """

    def test_get_registered_case_insensitive(self):
        """
        Registrable subclasses are returned on request with case-insensitive names.
        """
        self.assertEqual(MyBaseClass.get_registered("fOo"), FooMyBaseClass)
        self.assertEqual(MyBaseClass.get_registered("baR"), BarMyBaseClass)

    def test_manual_registration(self):
        """
        Test manual registration.
        """
        FooMyBaseClass.register(register_name="foo")
        self.assertEqual(MyBaseClass.get_registered("foo"), FooMyBaseClass)

    def test_get_unregistered(self):
        """
        Requesting unregistered subclasses raises a UnregisteredTypeError.
        """
        MyBaseClass.clear_registered()

        with self.assertRaises(UnregisteredTypeError):
            MyBaseClass.get_registered(
                "foo", retry_with_reload=True, submod="nonexistent"
            )

    def test_get_unregistered_close_matches(self):
        """
        Requesting unregistered subclasses raises a UnregisteredTypeError.
        This with close matches.
        """
        with self.assertRaises(UnregisteredTypeError, msg="Did you mean 'foo'?"):
            MyBaseClass.get_registered("FooW")


if __name__ == "__main__":
    unittest.main()
