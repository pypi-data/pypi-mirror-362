# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define decorators for easier plugin definition."""

import sys

from werkzeug.routing import Rule

from . import hookimpl


def route(string, host=None):
    """Register rule on decorated function."""

    def decorator(f):
        """Inject plugin implementation."""

        @hookimpl.hookimpl
        def jsonresolver_loader(url_map):
            """Plugin implementation."""
            url_map.add(Rule(string, endpoint=f, host=host))

        # Register jsonresolver_loader on original module
        setattr(sys.modules[f.__module__], "jsonresolver_loader", jsonresolver_loader)
        return f

    return decorator
