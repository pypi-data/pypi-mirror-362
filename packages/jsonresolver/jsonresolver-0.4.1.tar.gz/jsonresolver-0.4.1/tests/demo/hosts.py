# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2016 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test plugin for JSON resolving using ``jsonresolver.route`` decorator."""

import jsonresolver


@jsonresolver.route("/test", host="inveniosoftware.org")
def sameroute_as_simple():
    """Return a fixed JSON."""
    return {"test": "inveniosoftware.org"}
