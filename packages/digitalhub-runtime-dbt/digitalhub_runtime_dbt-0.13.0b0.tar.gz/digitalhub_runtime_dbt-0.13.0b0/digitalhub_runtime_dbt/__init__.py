# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_dbt.entities._commons.enums import EntityKinds
from digitalhub_runtime_dbt.entities.function.dbt.builder import FunctionDbtBuilder
from digitalhub_runtime_dbt.entities.run.dbt_run.builder import RunDbtRunBuilder
from digitalhub_runtime_dbt.entities.task.dbt_transform.builder import TaskDbtTransformBuilder

entity_builders = (
    (EntityKinds.FUNCTION_DBT.value, FunctionDbtBuilder),
    (EntityKinds.RUN_DBT.value, RunDbtRunBuilder),
    (EntityKinds.TASK_DBT_TRANSFORM.value, TaskDbtTransformBuilder),
)

try:
    from digitalhub_runtime_dbt.runtimes.builder import RuntimeDbtBuilder

    runtime_builders = ((kind, RuntimeDbtBuilder) for kind in [e.value for e in EntityKinds])
except ImportError:
    runtime_builders = tuple()
