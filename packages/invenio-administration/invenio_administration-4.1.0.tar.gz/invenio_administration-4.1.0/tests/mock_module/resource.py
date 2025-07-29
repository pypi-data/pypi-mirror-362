# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Mock resource created for testing."""

from flask_resources import ResourceConfig


class MockResource(ResourceConfig):
    """Creates a mock resource for testing."""

    blueprint_name = "mocks"
    url_prefix = "/mocks"
