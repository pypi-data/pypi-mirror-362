# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define hook specification."""

import pluggy

hookspec = pluggy.HookspecMarker("jsonresolver")


@hookspec
def jsonresolver_loader(url_map):
    """Retrieve JSON document."""
    pass  # pragma: no cover
