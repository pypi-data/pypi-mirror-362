"""
Created on 27 May 2025

@author: ph1jb
"""

from configargparse import Namespace  # type: ignore
from pandas.core.frame import DataFrame
from pytest import fixture, mark
from sqlahandler import SqlaHandler
from unittest.mock import MagicMock, ANY, Mock
import pytest
import sqlalchemy.sql


class TestSqlaHandler:
    @fixture
    def mock_connection(self):
        return MagicMock()

    @fixture
    def mock_engine(self):
        return MagicMock()

    @fixture
    def mock_query_handler(self, mock_engine):
        return SqlaHandler(mock_engine)

    @fixture()
    def mysql_options_default(self):
        """Refreshed before each use. OK to update."""
        return {
            "autocommit": True,
            "database": "database_is_not_set",
            "host": "database_host_is_not_set",
            "password": "database_password_is_not_set",
            "raise_on_warnings": True,
            "time_zone": "UTC",
            "user": "database_user_is_not_set",
        }

    def test_execute(self, mocker, mock_engine):
        query_handler = SqlaHandler(mock_engine)
        statement = "fetchall * from table"
        mock_text = mocker.patch("sqlahandler.sqlalchemy.text")
        query_handler.execute(statement)
        mock_text.assert_called_once_with(statement)
        mock_engine.connect.assert_called_once()

    def test_fetchall(self, mock_engine):
        mock_connection = MagicMock()
        mock_result = [(1, "Alice"), (2, "Bob")]

        # Setup context manager behavior
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_connection.execute.return_value = mock_result

        # Instantiate your client with the mocked engine
        client = SqlaHandler(mock_engine)

        # Execute the method
        statement = "SELECT id, name FROM users"
        results = client.fetchall(statement)

        # Assertions
        mock_connection.execute.assert_called_once()
        executed_sql = mock_connection.execute.call_args[0][0]
        assert isinstance(executed_sql, sqlalchemy.sql.elements.TextClause)
        assert str(executed_sql) == statement
        assert results == mock_result

    def test_fetchone(self, mock_engine):
        mock_connection = MagicMock()
        mock_result = Mock()
        mock_result1 = [(1, "Alice"), (2, "Bob")]

        # Setup context manager behavior
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_connection.execute.return_value = mock_result
        mock_result.first = Mock(return_value=mock_result1)

        # Instantiate your client with the mocked engine
        client = SqlaHandler(mock_engine)

        # Execute the method
        statement = "SELECT id, name FROM users"
        results = client.fetchone(statement)

        # Assertions
        mock_connection.execute.assert_called_once()
        executed_sql = mock_connection.execute.call_args[0][0]
        assert isinstance(executed_sql, sqlalchemy.sql.elements.TextClause)
        assert str(executed_sql) == statement
        assert results == mock_result1

    def test_get_sqlalchemy_url_object(self):
        mysql_options = {
            "autocommit": True,
            "compress": True,
            "database": "DatabaseNotSet",
            "host": "HostNotSet",
            "password": "redacted",
            "raise_on_warnings": True,
            "port": "3306",
            "time_zone": "utc",
            "user": "capacity",
        }
        result = SqlaHandler.sqlalchemy_url(mysql_options)
        expected = (
            "mysql+mysqlconnector://capacity:***@HostNotSet:3306/DatabaseNotSet"
            "?autocommit=True&compress=True&raise_on_warnings=True&time_zone=utc"
        )

        assert str(result) == expected

    def test_insert_executes_sql_statement(self, mocker):
        # Arrange
        mock_text = mocker.patch("sqlahandler.sqlalchemy.text")
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection

        handler = SqlaHandler(engine=mock_engine)
        statement = "ALTER TABLE my_table ADD COLUMN new_col INT"
        bindparams = {"param": "value"}

        mock_text_obj = MagicMock()
        mock_text.return_value = mock_text_obj
        mock_text_obj.bindparams.return_value = "compiled_sql"

        # Act
        handler.insert(statement, bindparams)

        # Assert
        mock_engine.connect.assert_called_once()
        mock_text.assert_called_once_with(statement)
        mock_text_obj.bindparams.assert_called_once_with(**bindparams)
        mock_connection.execute.assert_called_once_with("compiled_sql")
        mock_connection.commit.assert_called_once()

    @mark.parametrize(
        "arg, key",
        [
            ("mysql_database", "database"),
            ("mysql_host", "host"),
            ("mysql_password", "password"),
            ("mysql_user", "user"),
        ],
    )
    def test_override_mysql_options_env(self, arg, key, mysql_options_default) -> None:
        mysql_args = {
            "mysql_database": None,
            "mysql_host": None,
            "mysql_password": None,
            "mysql_user": None,
        }
        mysql_args.update({arg: arg})
        config: Namespace = Namespace(**mysql_args, mysql_options=mysql_options_default)
        SqlaHandler.override_mysql_options(config)
        assert config.mysql_options.get(key) == arg

    def test_read_sql(self, mocker, mock_engine):
        df = DataFrame({"a": [0, 1, 2]})
        table = "test_table"
        columns = ("col1", "col2")
        mock_pd_read_sql = mocker.patch("sqlahandler.pandas.read_sql", return_value=df)
        query_handler = SqlaHandler(mock_engine)
        query_handler.read_sql(table, columns=columns)
        mock_pd_read_sql.assert_called_once_with(table, ANY, columns=columns)

    def test_read_sql_chunked(self, mocker, mock_engine):
        df_l = [DataFrame({"a": [0, 1, 2]})]
        table = "test_table"
        columns = ("col1", "col2")
        mock_pd_read_sql = mocker.patch("sqlahandler.pandas.read_sql", return_value=df_l)
        query_handler = SqlaHandler(mock_engine)
        query_handler.read_sql(table, columns=columns, chunksize=10)
        mock_pd_read_sql.assert_called_once_with(table, ANY, columns=columns, chunksize=10)

    # Test SqlaHandler.insert_df
    @mark.parametrize("table", ["fit", "mcs", "repd", "solarmedia"])
    def test_to_sql(self, mock_engine, mock_query_handler, table):
        nrows = 2
        kwargs = {}
        df = MagicMock()
        df.index.return_value = nrows
        mock_query_handler.to_sql(df, table)
        df.to_sql.assert_called_once_with(table, mock_engine, **kwargs)
