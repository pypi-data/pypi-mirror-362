# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Mock view for testing."""

from invenio_administration.views.base import AdminResourceListView


class MockView(AdminResourceListView):
    """Creates a mock AdminView for testing.

    resource_config must match the mock resource's name
    """

    name = "mock"
    category = "Test category"
    url = "mocked_details_url"
    resource_config = "mocks"


class MockViewAlternate(AdminResourceListView):
    """Creates a mock AdminView for testing.

    resource_config must match the mock resource's name
    """

    name = "mock alternate"
    category = "Test category"
    resource_config = "mocks"
    # url is None to force the name to be used as url
