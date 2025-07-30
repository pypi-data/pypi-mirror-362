# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.runtimes.builder import RuntimeBuilder

from digitalhub_runtime_dbt.runtimes.runtime import RuntimeDbt


class RuntimeDbtBuilder(RuntimeBuilder):
    """RuntaimeDbtBuilder class."""

    RUNTIME_CLASS = RuntimeDbt
