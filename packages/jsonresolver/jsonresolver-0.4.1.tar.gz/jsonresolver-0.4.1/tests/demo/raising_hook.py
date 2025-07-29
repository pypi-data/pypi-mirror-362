# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test for detecting the lazy evaluation of hook-registered JSON resolver."""

import jsonresolver


class HookRegistrationDetected(Exception):
    """Raise this ``exception`` to detect when a hook is registered."""


@jsonresolver.hookimpl
def jsonresolver_loader(url_map):
    """Load the raising plugin as a Rule to URL map."""
    raise HookRegistrationDetected
