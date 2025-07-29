# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015, 2016 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test for detecting the lazy evaluation of decorated JSON resolver."""

import jsonresolver


class EndpointCallDetected(Exception):
    """Raise this ``exception`` to detect when a plugin is called in test."""


@jsonresolver.route("/test", host="localhost:4000")
def raising():
    """Raise an exception."""
    raise EndpointCallDetected
