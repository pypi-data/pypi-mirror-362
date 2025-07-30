# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities._commons.enums import EntityKinds
from digitalhub.entities.dataitem.crud import new_dataitem
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub.entities.dataitem.table.entity import DataitemTable

    from digitalhub_runtime_dbt.utils.configuration import CredsConfigurator


def materialize_dataitem(dataitem: DataitemTable, name: str, configurator: CredsConfigurator) -> str:
    """
    Materialize dataitem in postgres.

    Parameters
    ----------
    dataitem : Dataitem
        The dataitem.
    name : str
        The parameter SQL name.
    configurator : CredsConfigurator
        Creds configurator.

    Returns
    -------
    str
        The materialized table name.

    Raises
    ------
    EntityError
        If something got wrong during dataitem materialization.
    """
    try:
        LOGGER.info(f"Collecting dataitem '{dataitem.name}' as dataframe.")
        df = dataitem.as_df()

        database = configurator.get_database()
        table_name = f"{name}_v{dataitem.id}"
        LOGGER.info(f"Creating new dataitem '{table_name}'.")
        materialized_path = f"sql://{database}/public/{table_name}"
        materialized_dataitem: DataitemTable = new_dataitem(
            project=dataitem.project,
            name=table_name,
            kind=EntityKinds.DATAITEM_TABLE.value,
            path=materialized_path,
        )

        LOGGER.info(f"Writing dataframe to dataitem '{table_name}'.")
        materialized_dataitem.write_df(df=df, if_exists="replace")

        return table_name
    except Exception as e:
        msg = f"Something got wrong during dataitem {name} materialization. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise EntityError(msg) from e
