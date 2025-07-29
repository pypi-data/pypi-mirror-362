# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Mock service ext."""

from invenio_records_resources.resources import RecordResource
from invenio_records_resources.services import RecordService

from .administration.mock import MockView
from .config import ServiceConfig
from .resource import MockResource


class MockExtension:
    """Mock extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Init app."""
        mock_service = RecordService(ServiceConfig)
        mock_resource = RecordResource(MockResource, mock_service)

        app.extensions["mock-module"] = self
        #  Adds resource's config name as a class attribute.
        self.__dict__[MockView.resource_config] = mock_resource
