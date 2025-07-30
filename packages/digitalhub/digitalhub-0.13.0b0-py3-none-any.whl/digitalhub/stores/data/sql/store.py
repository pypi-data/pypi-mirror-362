# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from digitalhub.stores.credentials.enums import CredsOrigin
from digitalhub.stores.data._base.store import Store
from digitalhub.stores.readers.data.api import get_reader_by_object
from digitalhub.utils.exceptions import StoreError
from digitalhub.utils.types import SourcesOrListOfSources

if typing.TYPE_CHECKING:
    from sqlalchemy.engine.row import Row

    from digitalhub.stores.credentials.configurator import Configurator
    from digitalhub.stores.data.sql.configurator import SqlStoreConfigurator


class SqlStore(Store):
    """
    SQL store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on SQL based storage.
    """

    def __init__(self, configurator: Configurator | None = None) -> None:
        super().__init__(configurator)
        self._configurator: SqlStoreConfigurator

    ##############################
    # I/O methods
    ##############################

    def download(
        self,
        src: str,
        dst: Path,
        overwrite: bool = False,
    ) -> str:
        """
        Download artifacts from storage.

        Parameters
        ----------
        src : str
            Path of the material entity.
        dst : str
            The destination of the material entity on local filesystem.
        overwrite : bool
            Specify if overwrite existing file(s).

        Returns
        -------
        str
            Destination path of the downloaded files.
        """
        table_name = self._get_table_name(src) + ".parquet"
        # Case where dst is not provided
        if dst is None:
            dst = Path(self._build_temp("sql")) / table_name
        else:
            self._check_local_dst(str(dst))
            path = Path(dst)

            # Case where dst is a directory
            if path.suffix == "":
                dst = path / table_name

            # Case where dst is a file
            elif path.suffix != ".parquet":
                raise StoreError("The destination path must be a directory or a parquet file.")

            self._check_overwrite(dst, overwrite)
            self._build_path(dst)

        schema = self._get_schema(src)
        table = self._get_table_name(src)
        return self._download_table(schema, table, str(dst))

    def upload(
        self,
        src: SourcesOrListOfSources,
        dst: str,
    ) -> list[tuple[str, str]]:
        """
        Upload an artifact to storage.

        Raises
        ------
        StoreError
            This method is not implemented.
        """
        raise StoreError("SQL store does not support upload.")

    def get_file_info(
        self,
        root: str,
        paths: list[tuple[str, str]],
    ) -> list[dict]:
        """
        Get file information from SQL based storage.

        Parameters
        ----------
        paths : list[str]
            List of source paths.

        Returns
        -------
        list[dict]
            Returns files metadata.
        """
        return []

    ##############################
    # Datastore methods
    ##############################

    def read_df(
        self,
        path: SourcesOrListOfSources,
        file_format: str | None = None,
        engine: str | None = None,
        **kwargs,
    ) -> Any:
        """
        Read DataFrame from path.

        Parameters
        ----------
        path : SourcesOrListOfSources
            Path(s) to read DataFrame from.
        file_format : str
            Extension of the file.
        engine : str
            Dataframe engine (pandas, polars, etc.).
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        Any
            DataFrame.
        """
        if isinstance(path, list):
            raise StoreError("SQL store can only read a single DataFrame at a time.")

        reader = self._get_reader(engine)
        schema = self._get_schema(path)
        table = self._get_table_name(path)
        sql_engine = self._check_factory(schema=schema)

        sa_table = Table(table, MetaData(), autoload_with=sql_engine)
        stm = select(sa_table)

        return reader.read_table(stm, sql_engine, **kwargs)

    def query(
        self,
        query: str,
        path: str,
        engine: str | None = None,
    ) -> Any:
        """
        Query data from database.

        Parameters
        ----------
        query : str
            The query to execute.
        path : str
            Path to the database.
        engine : str
            Dataframe engine (pandas, polars, etc.).

        Returns
        -------
        Any
            DataFrame.
        """
        reader = self._get_reader(engine)
        schema = self._get_schema(path)
        sql_engine = self._check_factory(schema=schema)
        return reader.read_table(query, sql_engine)

    def write_df(self, df: Any, dst: str, extension: str | None = None, **kwargs) -> str:
        """
        Write a dataframe to a database. Kwargs are passed to df.to_sql().

        Parameters
        ----------
        df : Any
            The dataframe to write.
        dst : str
            The destination of the dataframe.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        str
            Path of written dataframe.
        """
        schema = self._get_schema(dst)
        table = self._get_table_name(dst)
        return self._upload_table(df, schema, table, **kwargs)

    ##############################
    # Private I/O methods
    ##############################

    def _download_table(self, schema: str, table: str, dst: str) -> str:
        """
        Download a table from SQL based storage.

        Parameters
        ----------
        schema : str
            The origin schema.
        table : str
            The origin table.
        dst : str
            The destination path.

        Returns
        -------
        str
            The destination path.
        """
        engine = self._check_factory(schema=schema)

        # Read the table from the database
        sa_table = Table(table, MetaData(), autoload_with=engine)
        stm = select(sa_table)
        with engine.begin() as conn:
            result: list[Row] = conn.execute(stm).fetchall()

        # Parse the result
        data = {col: [row[idx] for row in result] for idx, col in enumerate(sa_table.columns.keys())}

        # Convert the result to a pyarrow table and
        # write the pyarrow table to a Parquet file
        arrow_table = pa.Table.from_pydict(data)
        pq.write_table(arrow_table, dst)

        engine.dispose()

        return dst

    def _upload_table(self, df: Any, schema: str, table: str, **kwargs) -> str:
        """
        Upload a table to SQL based storage.

        Parameters
        ----------
        df : DataFrame
            The dataframe.
        schema : str
            Destination schema.
        table : str
            Destination table.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        str
            The SQL URI where the dataframe was saved.
        """
        reader = get_reader_by_object(df)
        engine = self._check_factory()
        reader.write_table(df, table, engine, schema, **kwargs)
        engine.dispose()
        return f"sql://{engine.url.database}/{schema}/{table}"

    ##############################
    # Helper methods
    ##############################

    def _get_connection_string(self, origin: str) -> str:
        """
        Get the connection string.

        Parameters
        ----------
        origin : str
            The origin of the credentials.

        Returns
        -------
        str
            The connection string.
        """
        return self._configurator.get_sql_conn_string(origin)

    def _get_engine(self, origin: str, schema: str | None = None) -> Engine:
        """
        Create engine from connection string.

        Parameters
        ----------
        origin : str
            The origin of the credentials.
        schema : str
            The schema.

        Returns
        -------
        Engine
            An SQLAlchemy engine.
        """
        connection_string = self._get_connection_string(origin)
        if not isinstance(connection_string, str):
            raise StoreError("Connection string must be a string.")
        try:
            connect_args = {"connect_timeout": 30}
            if schema is not None:
                connect_args["options"] = f"-csearch_path={schema}"
            return create_engine(connection_string, connect_args=connect_args)
        except Exception as ex:
            raise StoreError(f"Something wrong with connection string. Arguments: {str(ex.args)}")

    def _check_factory(self, schema: str | None = None) -> Engine:
        """
        Check if the database is accessible and return the engine.

        Parameters
        ----------
        schema : str
            The schema.

        Returns
        -------
        Engine
            The database engine.
        """
        try:
            engine = self._get_engine(CredsOrigin.ENV.value, schema)
            self._check_access_to_storage(engine)
        except StoreError:
            engine = self._get_engine(CredsOrigin.FILE.value, schema)
            self._check_access_to_storage(engine)
        return engine

    @staticmethod
    def _parse_path(path: str) -> dict:
        """
        Parse the path and return the components.

        Parameters
        ----------
        path : str
            The path.

        Returns
        -------
        dict
            A dictionary containing the components of the path.
        """
        # Parse path
        err_msg = "Invalid SQL path. Must be sql://<database>/<schema>/<table> or sql://<database>/<table>"
        protocol, pth = path.split("://")
        components = pth.split("/")
        if protocol != "sql" or not (2 <= len(components) <= 3):
            raise ValueError(err_msg)

        # Get components
        database = components[0]
        table = components[-1]
        schema = components[1] if len(components) == 3 else "public"
        return {"database": database, "schema": schema, "table": table}

    def _get_schema(self, uri: str) -> str:
        """
        Get the name of the SQL schema from the URI.

        Parameters
        ----------
        uri : str
            The URI.

        Returns
        -------
        str
            The name of the SQL schema.
        """
        return str(self._parse_path(uri).get("schema"))

    def _get_table_name(self, uri: str) -> str:
        """
        Get the name of the table from the URI.

        Parameters
        ----------
        uri : str
            The URI.

        Returns
        -------
        str
            The name of the table
        """
        return str(self._parse_path(uri).get("table"))

    @staticmethod
    def _check_access_to_storage(engine: Engine) -> None:
        """
        Check if there is access to the storage.

        Parameters
        ----------
        engine : Engine
            An SQLAlchemy engine.

        Returns
        -------
        None

        Raises
        ------
        StoreError
            If there is no access to the storage.
        """
        try:
            engine.connect()
        except SQLAlchemyError:
            engine.dispose()
            raise StoreError("No access to db!")
