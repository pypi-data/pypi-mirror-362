# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from flask import Flask

from invenio_jobs import InvenioJobs


def test_version():
    """Test version import."""
    from invenio_jobs import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioJobs(app)
    assert "invenio-jobs" in app.extensions

    app = Flask("testapp")
    ext = InvenioJobs()
    assert "invenio-jobs" not in app.extensions
    ext.init_app(app)
    assert "invenio-jobs" in app.extensions
