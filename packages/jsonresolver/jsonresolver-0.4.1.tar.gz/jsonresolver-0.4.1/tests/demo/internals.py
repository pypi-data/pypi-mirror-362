# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015, 2016 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Test adding JSON resolving rule using ``werkzeug.routing.Rule`` object."""

import requests
from werkzeug.routing import Rule

import jsonresolver


@jsonresolver.hookimpl
def jsonresolver_loader(url_map):
    """Load the resolver plugin as a Rule to URL map."""

    def endpoint(recid):
        return requests.get(
            "https://cds.cern.ch/record/{recid}?of=recjson".format(recid=recid)
        ).json

    url_map.add(Rule("/record/<recid>", endpoint=endpoint, host="cds.cern.ch"))
