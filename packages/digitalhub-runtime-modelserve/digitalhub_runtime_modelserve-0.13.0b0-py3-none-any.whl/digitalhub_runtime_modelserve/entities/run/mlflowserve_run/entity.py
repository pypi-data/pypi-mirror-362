# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.run.modelserve_run.entity import RunModelserveRun

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.run.mlflowserve_run.spec import RunSpecMlflowserveRun
    from digitalhub_runtime_modelserve.entities.run.mlflowserve_run.status import RunStatusMlflowserveRun


class RunMlflowserveRun(RunModelserveRun):
    """
    RunMlflowserveRun class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecMlflowserveRun,
        status: RunStatusMlflowserveRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecMlflowserveRun
        self.status: RunStatusMlflowserveRun
