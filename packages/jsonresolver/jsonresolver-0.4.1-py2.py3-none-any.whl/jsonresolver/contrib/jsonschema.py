# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Module that implements ``RefResolver`` factory using ``JSONResolver``.

The ``ref_resolver_factory`` uses an instance of ``JSONResolver`` for
implementation of remote URL resolver. The resolver is used to retrieve JSON
object based on registered plugins.

Example:
.. code-block:: python

   >>> from jsonschema import validate
   >>> from jsonresolver import JSONResolver
   >>> from jsonresolver.contrib.jsonschema import ref_resolver_factory
   >>> schema = {'$ref': 'http://localhost:4000/schema/authors.json#'}
   >>> json_resolver = JSONResolver(plugins=['tests.demo.schema'])
   >>> resolver_cls = ref_resolver_factory(json_resolver)
   >>> resolver = resolver_cls.from_schema(schema)
   >>> validate(['foo', 'bar'], schema, resolver=resolver)


"""

from jsonschema import RefResolver as _RefResolver
from werkzeug.exceptions import NotFound


def ref_resolver_factory(resolver):
    """Generate new RefResolver class that uses given resolver."""

    class RefResolver(_RefResolver):
        """Implement custom remote URL resolver."""

        def resolve_remote(self, uri):
            """Resolve remove uri using given resolver."""
            try:
                result = resolver.resolve(uri)
                if self.cache_remote:
                    self.store[uri] = result
                return result
            except NotFound:
                return super().resolve_remote(uri)

    return RefResolver
