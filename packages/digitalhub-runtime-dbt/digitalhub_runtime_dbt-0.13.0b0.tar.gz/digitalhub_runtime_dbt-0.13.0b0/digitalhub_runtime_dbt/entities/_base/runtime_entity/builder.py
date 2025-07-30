# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.runtime_entity.builder import RuntimeEntityBuilder
from digitalhub.entities.task._base.utils import build_task_actions

from digitalhub_runtime_dbt.entities._commons.enums import EntityKinds, TaskActions


class RuntimeEntityBuilderDbt(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_DBT.value
    TASKS_KINDS = build_task_actions(
        [
            (
                EntityKinds.TASK_DBT_TRANSFORM.value,
                TaskActions.TRANSFORM.value,
            )
        ]
    )
    RUN_KIND = EntityKinds.RUN_DBT.value
