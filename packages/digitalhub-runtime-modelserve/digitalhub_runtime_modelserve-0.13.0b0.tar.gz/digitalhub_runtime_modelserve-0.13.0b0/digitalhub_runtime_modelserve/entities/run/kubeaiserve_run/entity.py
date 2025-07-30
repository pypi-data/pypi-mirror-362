# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.run.modelserve_run.entity import RunModelserveRun

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.spec import RunSpecKubeaiserveRun
    from digitalhub_runtime_modelserve.entities.run.kubeaiserve_run.status import RunStatusKubeaiserveRun


class RunKubeaiserveRun(RunModelserveRun):
    """
    RunKubeaiserveRun class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecKubeaiserveRun,
        status: RunStatusKubeaiserveRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecKubeaiserveRun
        self.status: RunStatusKubeaiserveRun
