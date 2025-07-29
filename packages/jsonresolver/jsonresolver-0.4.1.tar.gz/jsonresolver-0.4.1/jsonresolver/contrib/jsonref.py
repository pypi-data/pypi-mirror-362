# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Module that implements ``JsonLoader`` factory using ``JSONResolver``.

Use ``json_loader_factory`` if you want to take advantage of default
``JsonLoader.get_remote_json`` method for URIs that are not handled
by your ``JSONResolver`` instance.

Example:
.. code-block:: python

   >>> from jsonref import replace_refs
   >>> from jsonresolver import JSONResolver
   >>> from jsonresolver.contrib.jsonref import json_loader_factory
   >>> schema = {'$ref': 'http://localhost:4000/schema/authors.json#'}
   >>> json_resolver = JSONResolver(plugins=['tests.demo.schema'])
   >>> loader_cls = json_loader_factory(json_resolver)
   >>> loader = loader_cls(cache_results=False)
   >>> dict(replace_refs(schema, loader=loader))
   {'type': 'array'}

   # if you do not want default fallback:
   >>> dict(replace_refs(schema, loader=json_resolver.resolve))
   {'type': 'array'}
"""

import json
import warnings
from urllib import parse as urlparse
from urllib.request import urlopen

from jsonref import URIDict
from werkzeug.exceptions import NotFound

try:
    # If requests >=1.0 is available, we will use it
    import requests

    if not callable(requests.Response.json):
        requests = None
except ImportError:
    requests = None


class _JsonLoader:
    """Provides a callable.

    This means it takes a URI, and returns the loaded JSON referred
    to by that URI. Uses :mod:`requests` if available for HTTP URIs, and falls
    back to :mod:`urllib`. By default it keeps a cache of previously loaded
    documents.

    See: https://github.com/gazpachoking/jsonref/pull/43

    :param store: A pre-populated dictionary matching URIs to loaded JSON
        documents
    :param cache_results: If this is set to false, the internal cache of
        loaded JSON documents is not used
    """

    def __init__(self, store=(), cache_results=True):
        """Construct."""
        self.store = URIDict(store)
        self.cache_results = cache_results

    def __call__(self, uri, **kwargs):
        """Return the loaded JSON referred to by `uri`.

        :param uri: The URI of the JSON document to load
        :param kwargs: Keyword arguments passed to :func:`json.loads`
        """
        if uri in self.store:
            return self.store[uri]
        else:
            result = self.get_remote_json(uri, **kwargs)
            if self.cache_results:
                self.store[uri] = result
            return result

    def get_remote_json(self, uri, **kwargs):
        """Get remote json.

        Provides a callable which takes a URI, and returns the loaded JSON referred
        to by that URI. Uses :mod:`requests` if available for HTTP URIs, and falls
        back to :mod:`urllib`.
        """
        scheme = urlparse.urlsplit(uri).scheme

        if scheme in ["http", "https"] and requests:
            # Prefer requests, it has better encoding detection
            resp = requests.get(uri)
            # If the http server doesn't respond normally then raise exception
            # e.g. 404, 500 error
            resp.raise_for_status()
            try:
                result = resp.json(**kwargs)
            except TypeError:
                warnings.warn("requests >=1.2 required for custom kwargs to json.loads")
                result = resp.json()
        else:
            # Otherwise, pass off to urllib and assume utf-8
            with urlopen(uri) as content:
                result = json.loads(content.read().decode("utf-8"), **kwargs)

        return result


def json_loader_factory(resolver):
    """Generate new ``JsonLoader`` class that uses given resolver."""

    class JsonLoader(_JsonLoader):
        """Implement custom remote reference resolver."""

        def get_remote_json(self, uri, **kwargs):
            """Resolve remove uri using given resolver."""
            try:
                return resolver.resolve(uri)
            except NotFound:
                return super().get_remote_json(uri, **kwargs)

    return JsonLoader
