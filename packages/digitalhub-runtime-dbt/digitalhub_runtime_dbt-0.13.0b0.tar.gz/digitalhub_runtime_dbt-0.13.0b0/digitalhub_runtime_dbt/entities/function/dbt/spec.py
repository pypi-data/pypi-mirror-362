# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.spec import FunctionSpec, FunctionValidator

from digitalhub_runtime_dbt.entities.function.dbt.models import SourceValidator


class FunctionSpecDbt(FunctionSpec):
    """
    FunctionSpecDbt specifications.
    """

    def __init__(self, source: dict) -> None:
        super().__init__()
        self.source = source


class FunctionValidatorDbt(FunctionValidator):
    """
    FunctionValidatorDbt validator.
    """

    source: SourceValidator
    """Source code."""
