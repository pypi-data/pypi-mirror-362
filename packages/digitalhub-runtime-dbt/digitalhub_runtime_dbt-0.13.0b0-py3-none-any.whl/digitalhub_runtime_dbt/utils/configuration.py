# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import shutil
import typing
from pathlib import Path

import psycopg2
from digitalhub.stores.credentials.enums import CredsEnvVar, CredsOrigin
from digitalhub.stores.data.api import get_store
from digitalhub.stores.data.s3.utils import get_bucket_and_key, get_s3_source
from digitalhub.utils.generic_utils import decode_base64_string, extract_archive, requests_chunk_download
from digitalhub.utils.git_utils import clone_repository
from digitalhub.utils.logger import LOGGER
from digitalhub.utils.uri_utils import (
    get_filename_from_uri,
    has_git_scheme,
    has_remote_scheme,
    has_s3_scheme,
    has_zip_scheme,
)
from psycopg2 import sql

if typing.TYPE_CHECKING:
    from digitalhub.stores.data.sql.configurator import SqlStoreConfigurator

##############################
# Templates
##############################

PROJECT_TEMPLATE = """
name: "{}"
version: "1.0.0"
config-version: 2
profile: "postgres"
model-paths: ["{}"]
models:
""".lstrip(
    "\n"
)

MODEL_TEMPLATE_VERSION = """
models:
  - name: {}
    latest_version: {}
    versions:
        - v: {}
          config:
            materialized: table
""".lstrip(
    "\n"
)

PROFILE_TEMPLATE = """
postgres:
    outputs:
        dev:
            type: postgres
            host: "{}"
            user: "{}"
            pass: "{}"
            port: {}
            dbname: "{}"
            schema: "public"
    target: dev
""".lstrip(
    "\n"
)


def generate_dbt_profile_yml(
    root: Path,
    configurator: CredsConfigurator,
) -> None:
    """
    Create dbt profiles.yml

    Parameters
    ----------
    root : Path
        The root path.
    configurator : CredsConfigurator
        The configurator.

    Returns
    -------
    None
    """
    profiles_path = root / "profiles.yml"
    host, port, user, password, db = configurator.get_creds()
    profiles_path.write_text(PROFILE_TEMPLATE.format(host, user, password, int(port), db))


def generate_dbt_project_yml(root: Path, model_dir: Path, project: str) -> None:
    """
    Create dbt_project.yml from 'dbt'

    Parameters
    ----------
    project : str
        The project name.

    Returns
    -------
    None
    """
    project_path = root / "dbt_project.yml"
    project_path.write_text(PROJECT_TEMPLATE.format(project, model_dir.name))


def generate_outputs_conf(model_dir: Path, sql: str, output: str, uuid: str) -> None:
    """
    Write sql code for the model and write schema
    and version detail for outputs versioning

    Parameters
    ----------
    sql : str
        The sql code.
    output : str
        The output table name.
    uuid : str
        The uuid of the model for outputs versioning.

    Returns
    -------
    None
    """
    sql_path = model_dir / f"{output}.sql"
    sql_path.write_text(sql)

    output_path = model_dir / f"{output}.yml"
    output_path.write_text(MODEL_TEMPLATE_VERSION.format(output, uuid, uuid))


def generate_inputs_conf(model_dir: Path, name: str, uuid: str) -> None:
    """
    Generate inputs confs dependencies for dbt project.

    Parameters
    ----------
    project : str
        The project name.
    inputs : list
        The list of inputs dataitems names.

    Returns
    -------
    None
    """
    # write schema and version detail for inputs versioning
    input_path = model_dir / f"{name}.yml"
    input_path.write_text(MODEL_TEMPLATE_VERSION.format(name, uuid, uuid))

    # write also sql select for the schema
    sql_path = model_dir / f"{name}_v{uuid}.sql"
    sql_path.write_text(f'SELECT * FROM "{name}_v{uuid}"')


##############################
# Utils
##############################


def get_output_table_name(outputs: list[dict]) -> str:
    """
    Get output table name from run spec.

    Parameters
    ----------
    outputs : list
        The outputs.

    Returns
    -------
    str
        The output dataitem/table name.

    Raises
    ------
    RuntimeError
        If outputs are not a list of one dataitem.
    """
    try:
        return outputs["output_table"]
    except IndexError as e:
        msg = f"Outputs must be a list of one dataitem. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e
    except KeyError as e:
        msg = f"Must pass reference to 'output_table'. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


##############################
# Source
##############################


def save_function_source(path: Path, source_spec: dict) -> str:
    """
    Save function source.

    Parameters
    ----------
    path : Path
        Path where to save the function source.
    source_spec : dict
        Function source spec.

    Returns
    -------
    path
        Function code.
    """
    # Get relevant information
    code = source_spec.get("code")
    base64 = source_spec.get("base64")
    source = source_spec.get("source")
    handler: str = source_spec.get("handler")

    if code is not None:
        return code

    if base64 is not None:
        return decode_base64_string(base64)

    if source is None:
        raise RuntimeError("Function source not found in spec.")

    # Git repo
    if has_git_scheme(source):
        clone_repository(path, source)

    # Http(s) or s3 presigned urls
    elif has_remote_scheme(source):
        filename = path / get_filename_from_uri(source)
        if has_zip_scheme(source):
            requests_chunk_download(source.removeprefix("zip+"), filename)
            extract_archive(path, filename)
            filename.unlink()
        else:
            requests_chunk_download(source, filename)

    # S3 path
    elif has_s3_scheme(source):
        if not has_zip_scheme(source):
            raise RuntimeError("S3 source must be a zip file with scheme zip+s3://.")
        filename = path / get_filename_from_uri(source)
        bucket, key = get_bucket_and_key(source)
        get_s3_source(bucket, key, filename)
        extract_archive(path, filename)
        filename.unlink()

    if handler is not None:
        return (path / handler).read_text()

    # Unsupported scheme
    raise RuntimeError("Unable to collect source.")


##############################
# Creds configurator
##############################


class CredsConfigurator:
    def __init__(self, project: str) -> None:
        self.cfg: SqlStoreConfigurator = get_store(project, "sql://")._configurator
        self._valid_creds = None  # cache of valid creds

    def _test_connection(self, creds: tuple) -> bool:
        host, port, user, password, db = creds
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=db,
                user=user,
                password=password,
            )
            conn.close()
            return True
        except Exception:
            return False

    def get_creds(self) -> tuple:
        """
        Get valid database credentials (ENV first, then FILE).

        Returns
        -------
        tuple
            Database credentials tuple (host, port, user, password, database).

        Raises
        ------
        RuntimeError
            If no valid credentials are found.
        """
        if self._valid_creds is not None:
            return self._valid_creds

        for origin in (CredsOrigin.ENV.value, CredsOrigin.FILE.value):
            creds_dict = self.cfg.get_credentials(origin)
            creds = (
                creds_dict[CredsEnvVar.DB_HOST.value],
                creds_dict[CredsEnvVar.DB_PORT.value],
                creds_dict[CredsEnvVar.DB_USERNAME.value],
                creds_dict[CredsEnvVar.DB_PASSWORD.value],
                creds_dict[CredsEnvVar.DB_DATABASE.value],
            )
            if self._test_connection(creds):
                self._valid_creds = creds
                return creds

        raise RuntimeError("Unable to find valid database credentials (ENV or FILE).")

    def get_database(self) -> str:
        creds = self.get_creds()
        return creds[4]


##############################
# Engine
##############################


def get_connection(
    configurator: CredsConfigurator,
) -> psycopg2.extensions.connection:
    """
    Create a connection to postgres and return a session with autocommit enabled.

    Parameters
    ----------
    configurator : CredsConfigurator
        Creds configurator.

    Returns
    -------
    psycopg2.extensions.connection
        The connection to postgres.

    Raises
    ------
    RuntimeError
        If something got wrong during connection to postgres.
    """
    host, port, user, password, db = configurator.get_creds()
    try:
        return psycopg2.connect(
            host=host,
            port=port,
            database=db,
            user=user,
            password=password,
        )
    except Exception as e:
        msg = f"Unable to connect to postgres with validated credentials. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


##############################
# Cleanup
##############################


def cleanup(
    tables: list[str],
    tmp_dir: Path,
    configurator: CredsConfigurator,
) -> None:
    """
    Cleanup environment.

    Parameters
    ----------
    tables : list[str]
        List of tables to delete.
    tmp_dir : Path
        The temporary directory.
    configurator : CredsConfigurator
        Creds configurator.

    Returns
    -------
    None
    """
    try:
        connection = get_connection(configurator)
        with connection:
            with connection.cursor() as cursor:
                for table in tables:
                    LOGGER.info(f"Dropping table '{table}'.")
                    query = sql.SQL("DROP TABLE {table}").format(table=sql.Identifier(table))
                    cursor.execute(query)
    except Exception as e:
        msg = f"Something got wrong during environment cleanup. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e
    finally:
        LOGGER.info("Closing connection to postgres.")
        connection.close()

    LOGGER.info("Removing temporary directory.")
    shutil.rmtree(tmp_dir, ignore_errors=True)
