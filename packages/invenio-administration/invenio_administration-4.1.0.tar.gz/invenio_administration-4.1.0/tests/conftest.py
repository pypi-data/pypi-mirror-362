# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-administration is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""
from collections import namedtuple

import pytest
from flask_security import login_user
from invenio_access.models import ActionRoles, Role
from invenio_access.permissions import superuser_access
from invenio_accounts.testutils import login_user_via_session
from invenio_app.factory import create_app as _create_app
from invenio_records_resources.resources import RecordResource
from invenio_records_resources.services import RecordService
from mock_module.administration.mock import MockView
from mock_module.config import ServiceConfig
from mock_module.resource import MockResource

from invenio_administration.permissions import administration_access_action


@pytest.fixture(scope="module")
def celery_config():
    """Override pytest-invenio fixture.

    TODO: Remove this fixture if you add Celery support.
    """
    return {}


@pytest.fixture(scope="module")
def extra_entry_points():
    """Register extra entry point."""
    return {
        "invenio_administration.views": [
            "mock_module = mock_module.administration.mock:MockView",
            "mock_module = mock_module.administration.mock:MockViewAlternate",
        ],
        "invenio_base.apps": [
            "test = mock_module.ext:MockExtension",
        ],
    }


@pytest.fixture
def admin_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed.

    WHY: This is needed because expansion of ActionNeed is
         done on the basis of a User/Role being associated with that Need.
         If no User/Role is associated with that Need (in the DB), the
         permission is expanded to an empty list.
    """
    role = Role(name="admin-access", id="admin-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=administration_access_action, role=role)
    db.session.add(action_role)

    db.session.commit()

    return action_role.need


@pytest.fixture()
def admin(UserFixture, app, db, admin_role_need):
    """Admin user for requests."""
    u = UserFixture(
        email="admin@inveniosoftware.org",
        password="admin",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "admin-access")

    datastore.add_role_to_user(u.user, role)
    db.session.commit()
    return u


@pytest.fixture
def superuser_identity(admin, superuser_role_need):
    """Superuser identity fixture."""
    identity = admin.identity
    identity.provides.add(superuser_role_need)
    return identity


@pytest.fixture
def superuser_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed.

    WHY: This is needed because expansion of ActionNeed is
         done on the basis of a User/Role being associated with that Need.
         If no User/Role is associated with that Need (in the DB), the
         permission is expanded to an empty list.
    """
    role = Role(name="superuser-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=superuser_access, role=role)
    db.session.add(action_role)

    db.session.commit()

    return action_role.need


RunningApp = namedtuple(
    "RunningApp",
    [
        "app",
        "superuser_identity",
        "location",
        "cache",
    ],
)


@pytest.fixture(scope="module")
def app_config(app_config):
    """Application configuration fixture."""
    app_config["THEME_FRONTPAGE"] = False
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return _create_app


@pytest.fixture
def running_app(
    app,
    superuser_identity,
    location,
    cache,
):
    """This fixture provides an app with the typically needed db data loaded.

    All of these fixtures are often needed together, so collecting them
    under a semantic umbrella makes sense.
    """
    return RunningApp(
        app,
        superuser_identity,
        location,
        cache,
    )


@pytest.fixture
def test_app(running_app):
    """Get current app."""
    return running_app.app


@pytest.fixture
def client_with_login(client, admin):
    """Log in a user to the client."""
    user = admin.user
    login_user(user)
    login_user_via_session(client, email=user.email)
    return client


@pytest.fixture
def current_admin_menu(test_app):
    """Current Admin flask menu instance."""
    return test_app.extensions["menu"].root_node


@pytest.fixture
def current_admin_ext(test_app):
    """Current invenio-administration extension."""
    return test_app.extensions["invenio-administration"]


@pytest.fixture
def mock_service():
    """Creates a mock service."""
    service = RecordService(ServiceConfig)
    return service


@pytest.fixture
def mock_resource(mock_service):
    """Creates a mock resource."""
    return RecordResource(MockResource, mock_service)


@pytest.fixture(scope="function", autouse=True)
def register_mock_extension(test_app, mock_resource, mock_extension_name):
    """Creates a register a mock extension. Feature is used automatically all tests."""

    class MockExtension:
        def __init__(self, app=None):
            """Extension initialization."""
            if app:
                self.init_app(app)

        def init_app(self, app):
            app.extensions[mock_extension_name] = self
            #  Adds resource's config name as a class attribute.
            self.__dict__[MockView.resource_config] = mock_resource

    ext = MockExtension(test_app)
    return ext


@pytest.fixture
def mock_extension(test_app, mock_extension_name):
    """Creates a mock extension."""
    return test_app.extensions.get(mock_extension_name)


@pytest.fixture
def mock_extension_name():
    """Retrieves mock extension name."""
    return "mock-module"


@pytest.fixture
def current_admin_core(current_admin_ext):
    """Current Admin instance."""
    return current_admin_ext.administration


@pytest.fixture
def current_admin_bluepint(current_admin_core):
    """Retrieve admin blueprint."""
    return current_admin_core.blueprint
