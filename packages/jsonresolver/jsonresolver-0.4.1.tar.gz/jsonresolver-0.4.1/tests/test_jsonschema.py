# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define unit tests to test core functionality."""

import pytest
from jsonschema import RefResolutionError, validate

from jsonresolver import JSONResolver
from jsonresolver.contrib.jsonschema import ref_resolver_factory


def test_key_resolver():
    """Test JSONSchema validation with custom reference resolver."""
    example_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "authors": {"$ref": "http://localhost:4000/schema/authors.json#"}
        },
        "additionalProperties": False,
    }
    data = {"authors": [{"name": "Ellis"}]}

    json_resolver = JSONResolver(plugins=["demo.schema"])
    resolver_cls = ref_resolver_factory(json_resolver)
    resolver = resolver_cls.from_schema(example_schema)
    assert validate(data, example_schema, resolver=resolver) is None

    resolver = resolver_cls.from_schema(example_schema["properties"]["authors"])
    assert (
        validate(
            data["authors"], example_schema["properties"]["authors"], resolver=resolver
        )
        is None
    )


def test_missing_route():
    """Test orignal resolver."""
    example_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {"authors": {"$ref": "file:///missing.json#"}},
        "additionalProperties": False,
    }
    data = {"authors": [{"name": "Ellis"}]}

    json_resolver = JSONResolver(plugins=["demo.schema"])
    resolver_cls = ref_resolver_factory(json_resolver)
    resolver = resolver_cls.from_schema(example_schema)
    with pytest.raises(RefResolutionError):
        list(validate(data, example_schema, resolver=resolver))
