# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define unit tests to test core functionality."""

import importlib
from importlib.metadata import EntryPoint
from unittest.mock import patch

import pytest
from demo.raising import EndpointCallDetected
from demo.raising_hook import HookRegistrationDetected

from jsonresolver import JSONResolver


class MockEntryPoint(EntryPoint):
    """EntryPoint mock."""

    def load(self):
        """Load module from the mocked entry point."""
        if self.name == "importfail":
            raise ImportError()
        else:
            return importlib.import_module(self.name)


_mock_entry_points = {
    MockEntryPoint(name="demo.simple", value="demo.simple", group="espresso"),
    MockEntryPoint(name="demo.raising", value="demo.raising", group="raising"),
    MockEntryPoint(
        name="demo.raising_hook", value="demo.raising_hook", group="raising_hook"
    ),
    MockEntryPoint(name="demo.simple", value="demo.simple", group="doubletrouble"),
    MockEntryPoint(name="demo.simple", value="demo.simple", group="doubletrouble"),
    MockEntryPoint(name="importfail", value="test.importfail", group="importfail"),
}


def patch_entrypoints(func):
    """Patch importlib.metadata.Distribution.entry_points."""
    try:
        # python 3.9 with importlib_metadata
        import importlib_metadata

        return patch(
            "importlib_metadata.PathDistribution.entry_points", _mock_entry_points
        )(func)
    except ImportError:
        # importlib.metadata
        return patch(
            "importlib.metadata.PathDistribution.entry_points", _mock_entry_points
        )(func)


@patch_entrypoints
def test_entry_point_group():
    """Test the entry point group loading."""
    resolver = JSONResolver(entry_point_group="espresso")
    assert resolver.resolve("http://localhost:4000/test") == {"test": "test"}


def test_plugins():
    """Test the plugins loading."""
    resolver = JSONResolver(plugins=["demo.simple"])
    assert resolver.resolve("http://localhost:4000/test") == {"test": "test"}


@patch_entrypoints
def test_plugin_lazy_execution():
    """Test the lazy evaluation of loaded plugin."""
    # Plugin code should be called (i.e. raise exception) on resolve method
    resolver = JSONResolver(plugins=["demo.raising"])
    with pytest.raises(EndpointCallDetected) as exc_info:
        resolver.resolve("http://localhost:4000/test")
    assert exc_info.type is EndpointCallDetected

    # Same as above but loaded using entry point
    resolver = JSONResolver(entry_point_group="raising")
    with pytest.raises(EndpointCallDetected) as exc_info:
        resolver.resolve("http://localhost:4000/test")
    assert exc_info.type is EndpointCallDetected


@patch_entrypoints
def test_plugin_lazy_execution_hooks():
    """Test the lazy evaluation of loaded plugin through hooks."""
    # Plugin code should be called (i.e. raise exception) on resolve method
    resolver = JSONResolver(plugins=["demo.raising_hook"])
    with pytest.raises(HookRegistrationDetected) as exc_info:
        resolver.resolve("http://localhost:4000/test")
    assert exc_info.type is HookRegistrationDetected

    # Same as above but loaded using entry point
    resolver = JSONResolver(entry_point_group="raising_hook")
    with pytest.raises(HookRegistrationDetected) as exc_info:
        resolver.resolve("http://localhost:4000/test")
    assert exc_info.type is HookRegistrationDetected
