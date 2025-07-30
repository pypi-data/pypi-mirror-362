"""
Created on 27 May 2025

@author: ph1jb
"""

from configargparse import Namespace  # type: ignore
from pandas.core.frame import DataFrame
from pandas.io.sql import SQLTable
from sqlalchemy.dialects.mysql.dml import insert
from sqlalchemy.engine import URL
from sqlalchemy.engine.row import Row
from typing import Any, List, cast, Dict
from typing_extensions import TypedDict
import logging
import pandas
import sqlalchemy

# import pandas as pd


class MysqlOptions(TypedDict):
    user: str
    password: str
    host: str
    port: int
    database: str


class SqlalchemyOptions(TypedDict):
    username: str
    password: str
    host: str
    port: int
    database: str


logger = logging.getLogger(__name__)


class SqlaHandler:
    """Import DataFrames into a SQL database."""

    def __init__(self, engine: sqlalchemy.Engine):
        self.engine = engine

    @staticmethod
    def override_mysql_options(config: Namespace):
        """
        Override the MySQL options based on the provided configuration.

        Updates specific fields like database, host, user, and password if available.
        """
        if config.mysql_database:
            config.mysql_options.update({"database": config.mysql_database})
        if config.mysql_host:
            config.mysql_options.update({"host": config.mysql_host})
        if config.mysql_password:
            config.mysql_options.update({"password": config.mysql_password})
        if config.mysql_user:
            config.mysql_options.update({"user": config.mysql_user})

    @staticmethod
    def sqlalchemy_url(mysql_options: MysqlOptions, drivername="mysql+mysqlconnector") -> URL:
        """Get sqlalchemy URL object (used in create_engine) from mysql options."""
        sqlalchemy_keys = ("user", "password", "host", "port", "database")
        # Add SQL dialect and connector
        options_sqlalchemy0 = {k: v for (k, v) in mysql_options.items() if k in sqlalchemy_keys}

        # Replace mysql key user by sqlalchemy key username
        options_sqlalchemy0["username"] = options_sqlalchemy0.pop("user")
        options_sqlalchemy: SqlalchemyOptions = cast(SqlalchemyOptions, options_sqlalchemy0)
        query = {k: str(v) for (k, v) in mysql_options.items() if k not in sqlalchemy_keys}

        return URL.create(drivername, **options_sqlalchemy, query=query)

    def execute(self, statement, bindparams: Dict | None = None) -> None:
        """Execute a SQL statement with no return values (e.g. alter table).
        sqlalchemy.text compiles the statement into a cannonical form
        which can then be converted to the SQL dialect for the database in use. (We use MySQL).
        We use execute to (re)create and alter (e.g. add index) tables.
        To insert or select data use methods: df_to_sql or read_sql.
        """
        logger.debug("Executing %(statement)s", {"statement": statement})
        bindparams = bindparams if bindparams else {}
        with self.engine.connect() as connection:
            connection.execute(sqlalchemy.text(statement).bindparams(**bindparams))
            connection.commit()
        logger.debug("Executed %(statement)s", {"statement": statement})

    def fetchall(self, statement, bindparams: Dict | None = None) -> List[Row[Any]]:
        """Execute a SQL select statement, return all rows.
        sqlalchemy.text compiles the statement into a cannonical form
        which can then be converted to the SQL dialect for the database in use. (We use MySQL).
        We use execute to (re)create and alter (e.g. add index) tables.
        To insert or select Pandas DataFrames use methods: df_to_sql or read_sql.
        """
        logger.debug("Executing %(statement)s", {"statement": statement})
        bindparams = {} if bindparams is None else bindparams

        with self.engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(statement).bindparams(**bindparams))

            logger.debug("Executed %(statement)s", {"statement": statement})
            return [row for row in result]

    def fetchone(self, statement: str, bindparams: Dict | None = None) -> Row[Any] | None:
        """Execute a SQL select statement, return first row.
        sqlalchemy.text compiles the statement into a cannonical form
        which can then be converted to the SQL dialect for the database in use. (We use MySQL).
        We use execute to (re)create and alter (e.g. add index) tables.
        To insert or select Pandas DataFrames use methods: df_to_sql or read_sql.
        """
        logger.debug("Executing %(statement)s", {"statement": statement})
        bindparams = {} if bindparams is None else bindparams

        with self.engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(statement).bindparams(**bindparams))
            logger.debug("Executed %(statement)s", {"statement": statement})
        return result.first()

    def insert(self, statement, bindparams: Dict) -> None:
        """Execute a SQL statement with no return values (e.g. alter table).
        sqlalchemy.text compiles the statement into a cannonical form
        which can then be converted to the SQL dialect for the database in use. (We use MySQL).
        We use execute to (re)create and alter (e.g. add index) tables.
        To insert or select data use methods: df_to_sql or read_sql.
        """
        logger.debug("Inserting %(statement)s", {"statement": statement})
        with self.engine.connect() as connection:
            connection.execute(sqlalchemy.text(statement).bindparams(**bindparams))
            connection.commit()
        logger.debug("Inserted %(statement)s", {"statement": statement})

    def read_sql(self, table: str, **kwargs) -> DataFrame:
        """Select rows from database table into pandas DataFrame."""
        logger.debug("Selecting from table %(table)s", {"table": table})
        with self.engine.connect() as connection:
            if "chunksize" in kwargs.keys():
                df = pandas.concat(chunk for chunk in pandas.read_sql(table, connection, **kwargs))  # type: ignore
            else:
                df = pandas.read_sql(table, connection, **kwargs)  # type: ignore
        logger.debug("Selected from table %(table)s", {"table": table})
        return df

    def to_sql(self, df: DataFrame, table: str, **kwargs):
        """Insert a pandas DataFrame into a database table.
        # chunksize to avoid exceeding the SQL max_packet size. (MCS data files are large.)
        """
        nrows = len(df.index)
        logger.debug(
            "Inserting %(nrows)s rows into table: %(table)s",
            {"nrows": nrows, "table": table},
        )
        df.to_sql(table, self.engine, **kwargs)
        logger.debug(
            "Inserted %(nrows)s rows into table: %(table)s",
            {"nrows": nrows, "table": table},
        )

    @staticmethod
    def upsert(table: SQLTable, conn, keys, data_iter):
        """Method used by to_sql to do: SQL insert on duplicate key update
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html"""
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data)
        columns = keys[1:]
        d = {col: getattr(stmt.inserted, col) for col in columns}
        stmt = stmt.on_duplicate_key_update(**d)
        result = conn.execute(stmt)
        return result.rowcount
