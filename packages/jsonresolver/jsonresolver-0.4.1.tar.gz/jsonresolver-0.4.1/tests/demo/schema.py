# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015, 2016 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test plugin for JSON schema resolving using decorator."""

import jsonresolver


@jsonresolver.route("/schema/<path:name>", host="localhost:4000")
def schema(name):
    """Return a fixed JSON ``schema``."""
    assert name == "authors.json"
    return {"type": "array"}
