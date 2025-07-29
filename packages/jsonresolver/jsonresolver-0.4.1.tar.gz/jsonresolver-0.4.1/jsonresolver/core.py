# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015, 2016 CERN.
#
# jsonresolver is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Resolve JSON objects from different URLs."""

import importlib
from urllib.parse import urlsplit

import pluggy
from werkzeug.routing import Map

from . import hookspec


class JSONResolver(object):
    """Resolve JSON objects based on rules in URL map."""

    def __init__(self, plugins=None, entry_point_group=None):
        """Initialize resolver with various plugins and entry point group."""
        self.pm = pluggy.PluginManager("jsonresolver")
        self.pm.add_hookspecs(hookspec)
        for plugin in plugins or []:
            self.pm.register(importlib.import_module(plugin))
        if entry_point_group:
            self.pm.load_setuptools_entrypoints(entry_point_group)
        self.url_map = None

    def _build_url_map(self):
        """Build an URL map from registered plugins."""
        self.url_map = Map(host_matching=True)
        self.pm.hook.jsonresolver_loader(url_map=self.url_map)

    def resolve(self, url):
        """Resolve given URL and use registered loader."""
        if self.url_map is None:
            self._build_url_map()
        parts = urlsplit(url)
        loader, args = self.url_map.bind(parts.netloc).match(parts.path)
        return loader(**args)
