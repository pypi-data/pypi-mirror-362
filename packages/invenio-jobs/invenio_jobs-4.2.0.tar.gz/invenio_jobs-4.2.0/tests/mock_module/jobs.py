# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Mock module jobs."""

from invenio_jobs.jobs import JobType

from .tasks import mock_task

mock_job = JobType.create(
    arguments_schema=None,
    job_cls_name="MockJob",
    id_="update_expired_embargos",
    task=mock_task,
    description="Updates expired embargos",
    title="Update expired embargoes",
)
