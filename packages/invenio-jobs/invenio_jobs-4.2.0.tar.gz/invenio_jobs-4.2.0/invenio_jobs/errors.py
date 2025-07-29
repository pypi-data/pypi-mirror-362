# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Errors for logging."""


class TaskExecutionError(Exception):
    """Exception raised when the task is executed with errors."""

    def __init__(self, message="The task was executed with errors."):
        """Constructor for the TaskExecutionError class."""
        self.message = message
        super().__init__(message)
