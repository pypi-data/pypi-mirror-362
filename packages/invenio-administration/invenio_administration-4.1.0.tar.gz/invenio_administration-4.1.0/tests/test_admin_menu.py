# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration menu test module."""

from mock_module.administration.mock import MockView


def test_menu_generation(current_admin_menu, current_admin_core, test_app):
    # Retrieve mock module's view from registered views.
    registered_view = list(
        filter(lambda x: x.view_class.name == MockView.name, current_admin_core.views)
    )
    assert len(registered_view) == 1

    mock_view = registered_view[0].view_class
    category = mock_view.category
    name = mock_view.name

    # register menu items on flask-menu instance
    current_admin_core._menu.register_menu_entries(current_admin_menu)
    # default admin navigation menu
    flask_menu_admin_instance = current_admin_menu.submenu("admin_navigation")

    # check if menu category was made correctly and has children
    category_menu = flask_menu_admin_instance.submenu(category)
    assert category_menu.text == category
    assert len(category_menu.children) > 0
    # menu entry from the registered view
    menu_entry_filter = [x for x in category_menu.children if x.text == name]

    # check if correct menu entry made under the category
    assert len(menu_entry_filter) == 1
    menu_entry = menu_entry_filter[0]
    # assert menu_entry._endpoint == test_view.endpoint

    # needs context to generate url from endpoint
    app_context = test_app.app_context()
    test_context = test_app.test_request_context()
    with app_context, test_context:
        assert menu_entry.url == f"{current_admin_core.url}/{mock_view.url}"
