# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Mock module tasks."""

from celery import shared_task


@shared_task
def mock_task(arg1, arg2, kwarg1=None, kwarg2=False, kwarg3="always"):
    """Mock task description."""
    pass
