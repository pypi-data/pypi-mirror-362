from __future__ import annotations

import functools
from typing import Any, Union, List
from pysqream.column_buffer import ColumnsBuffer
from pysqream.globals import ROWS_PER_FLUSH, FETCH_MANY_DEFAULT, TYPE_MAPPER, BYTES_PER_FLUSH_LIMIT, TEXT_ITEM_SIZE
from pysqream.utils import (NotSupportedError, ProgrammingError, Error, ArraysAreDisabled, mark_dbapi_attribute, dbapi_method, validate_disk_space,
                            validate_file_size, get_unique_filename)
from pysqream.server.sqclient import SQClient
from pysqream.server.connection_params import ConnectionParams
from pysqream.logger import ContextLogger


class Cursor:
    """
    Represent a database cursor, which is used to manage the context of
    a statement (execute and fetch).

    Cursors created from the same connection are not
    isolated, i.e., any changes done to the database by a cursor are
    immediately visible by the other cursors.

    Base PEP 249 – Python Database API Specification v2.0
    https://peps.python.org/pep-0249/#id12
    """

    def __init__(self, conn_params: ConnectionParams, client: SQClient, connection_id: int, allow_array: bool, logger: ContextLogger):
        self.__logger = logger

        # DB-API must have attributes
        self.arraysize = mark_dbapi_attribute(FETCH_MANY_DEFAULT)
        self.rowcount = mark_dbapi_attribute(-1)
        self.lastrowid = mark_dbapi_attribute(None)
        self.description = mark_dbapi_attribute(None)

        # SQreamDB connection attributes
        self.__conn_params: ConnectionParams = conn_params
        self.__client: SQClient = client
        self.__connection_id: int = connection_id
        self.__allow_array: bool = allow_array

        # State management
        self.__open_statement: bool = False
        self.__is_cursor_closed: bool = False
        self.__is_connection_initiated_close: bool = False

        # Buffer and data management
        self.__buffer: ColumnsBuffer = ColumnsBuffer(self.__logger)  # flushing buffer every BUFFER_SIZE bytes
        self.__stmt_id: Union[id, None] = None  # For error handling when called out of order
        self.__statement_type: Union[str, None] = None
        self.__more_to_fetch: bool = False
        self.__capacity: int = 0

        # Data tracking
        self.__parsed_rows: List[Any] = []
        self.__row_size: int = 0
        self.__rows_per_flush: int = 0
        self.__cols: List = []
        self.__col_types: List = []
        self.__col_sizes: List = []
        self.__col_scales: List = []
        self.__unsorted_data_columns: List = []

    def __enter__(self) -> Cursor:
        """
        Implementation for context manager ("with" clause)
        """

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """
        Implementation for context manager ("with" clause)
        """

        self.close()

    def __iter__(self):
        """
        Implementation for iterating connection in for-in clause
        """

        for item in self.fetchall():
            yield item

    # DB-API Must have methods
    # ------------------------
    @dbapi_method
    def execute(self, statement: str, params: list[tuple[Any]] | tuple[[tuple[Any]]] | None = None,
                data_as: str = 'rows', amount: int | None = None) -> Cursor:
        """
        Execute a statement. If params was provided - compile statement first
        and replace all question marks on passed parameters.

        :param statement: str a statement to execute with placeholders
        :param params: list[tuple[Any]] | tuple[tuple[Any]]: sequence of parameters to ingest into query
        :param data_as: string type of passed params. Possible values (`alchemy_flat_list`, `numpy`, `rows` - default)
        :param amount: int - amount of values of given params to insert

        Examples:
            query: SELECT * FROM <table_name> WHERE id IN (?, ?, ?) AND price >= ?;
            params: [(1, 2, 3, 450.69),]

            query: SELECT * FROM <table_name> WHERE id = %s AND price < %s;
            params: [(1, 200.00),]

            query: INSERT INTO <table_name> (id, name, description, price) VALUES (?, ?, ?, ?);
            params: [(1, 'Ryan Gosling', 'Actor', 0.0),]
            for next params it is better to use `executemany`
            params: [(1, 'Ryan Gosling', 'Actor', 0.0), (2, 'Mark Wahlberg', 'No pain no gain', 150.0)]

            query: UPDATE <table_name> SET price = ?, description = ? WHERE name = ?;
            params: [(999.999, 'Best actor', 'Ryan Gosling'),]

            query: DELETE FROM <table_name> WHERE id = ? AND other like ?;
            params: [(404, 200),]
        """

        try:
            self.__verify_cur_open()
            self.__execute_sqream_statement(statement, params=params, data_as=data_as, amount=amount)
            self.__fill_description()
        except Exception as e:
            self.__close_stmt()
            raise e

        return self

    @dbapi_method
    def executemany(self, statement: str, rows_or_cols: list[tuple[Any]] | tuple[[tuple[Any]]] | None = None,
                    data_as: str = 'rows', amount: int | None = None) -> Cursor:
        """
        Execute a statement, preferably used for insertion

        :param statement: str a statement to execute with placeholders
        :param rows_or_cols: list[tuple[Any]] | tuple[tuple[Any]]: sequence of parameters to ingest into query
        :param data_as: string type of passed params. Possible values (`alchemy_flat_list`, `numpy`, `rows` - default)
        :param amount: int - amount of values of given params to insert
        """

        return self.execute(statement, params=rows_or_cols, data_as=data_as, amount=amount)

    @dbapi_method
    def fetchmany(self, size: int = None, data_as: str = 'rows', fetchone: bool = False):
        """
        Fetch an amount of result rows
        """

        self.__logger.info(f"Fetching {'all' if size == -1 else size} rows", connection_id=self.__connection_id, statement_id=self.__stmt_id)
        size = size or self.arraysize

        if self.__statement_type not in (None, 'SELECT'):
            self.__logger.log_and_raise(ProgrammingError, 'No open statement while attempting fetch operation',
                                        connection_id=self.__connection_id, statement_id=self.__stmt_id)

        if self.__more_to_fetch:
            if self.__prepare_params.get("local_file_write", False):
                self.__get_file_from_server()
            else:
                self.__fetch_and_parse(size, data_as)
                self.__logger.debug(f"Fetched {len(self.__parsed_rows) if self.__parsed_rows else 0} rows",
                                    connection_id=self.__connection_id, statement_id=self.__stmt_id)

        res = self.__parsed_rows[0:size if size != -1 else None]
        del self.__parsed_rows[:size if size != -1 else None]

        return (res if res else []) if not fetchone else (res[0] if res else None)

    @dbapi_method
    def fetchone(self, data_as: str = 'rows'):
        """
        Fetch one result row
        """

        if data_as not in ('rows',):
            self.__logger.log_and_raise(ProgrammingError, "Bad argument to fetchone()", connection_id=self.__connection_id, statement_id=self.__stmt_id)

        return self.fetchmany(1, data_as, fetchone=True)

    @dbapi_method
    def fetchall(self, data_as: str = 'rows'):
        """
        Fetch all result rows
        """

        if data_as not in ('rows',):
            self.__logger.log_and_raise(ProgrammingError, "Bad argument to fetchall()", connection_id=self.__connection_id, statement_id=self.__stmt_id)

        return self.fetchmany(-1, data_as)

    @dbapi_method
    def nextset(self):
        """
        No multiple result sets so currently always returns None
        """

        self.__logger.log_and_raise(NotSupportedError, "Nextset is not supported", connection_id=self.__connection_id)

    @dbapi_method
    def setinputsizes(self, sizes):
        self.__logger.log_and_raise(NotSupportedError, "Setinputsizes is not supported", connection_id=self.__connection_id)

    @dbapi_method
    def setoutputsize(self, size, column=None):
        self.__logger.log_and_raise(NotSupportedError, "Setoutputsize is not supported", connection_id=self.__connection_id)

    @dbapi_method
    def close(self):
        """
        Closes the statement against sqream, cleans the buffer and change the cursor status to closed
        """

        self.__close_stmt()
        self.__is_cursor_closed = True

    # Internal Methods
    # ----------------
    def get_statement_type(self) -> str:
        return self.__statement_type

    def get_statement_id(self) -> int:
        return self.__stmt_id

    def get_connection_id(self) -> int:
        return self.__connection_id

    def get_is_cursor_closed(self) -> bool:
        return self.__is_cursor_closed

    def __verify_cur_open(self) -> None:
        if self.__is_cursor_closed:
            self.__logger.log_and_raise(ProgrammingError,
                                        f"{'Connection' if self.__is_connection_initiated_close else 'Cursor'}"
                                        f" has been closed", connection_id=self.__connection_id)

    def __execute_sqream_statement(self, statement: str, params: list[Any] | tuple[Any] | None = None,
                                   data_as: str = "rows", amount: int | None = None) -> None:
        """
        High-level method overview:
        1) statement preparation + reconnect + execute
        2) queryTypeIn and queryTypeOut
        3) if queryTypeIn isn't empty is means statement was parameterized
        4) collect all information about all columns (such a col types, scales, row_size, etc.) and send it to server
        5) if statement was `select` - perform lists for fetching and do 4 step for queryTypeOut
        """

        if self.__open_statement:
            self.__close_stmt()

        self.__open_statement = True
        self.__more_to_fetch = True

        self.__stmt_id = self.__client.get_statement_id()
        self.__prepare_params = self.__client.prepare_statement(statement)

        if self.__prepare_params.get("reconnect", False):
            # If reconnect exists and issued, close socket, open a new socket with new port/ip sent be the reconnect response
            self.__client.reconnect(self.__stmt_id, self.__conn_params.database, self.__conn_params.service,
                                    self.__conn_params.username, self.__conn_params.password, self.__prepare_params["listener_id"], self.__prepare_params['ip'],
                                    self.__prepare_params['port_ssl'] if self.__conn_params.use_ssl else self.__prepare_params['port'])

        self.__logger.info(f"Executing statement: '{statement}'", connection_id=self.__connection_id, statement_id=self.__stmt_id)
        self.__client.execute_statement()
        self.__column_list = parameterized_columns = self.__client.get_query_type_in()

        if self.__prepare_params.get("local_file_read", False):
            self.__put_file_to_server()

        elif parameterized_columns:
            self.__handle_parameterized(data_as, params, amount)

        self.__query_type_out = self.__client.get_query_type_out()
        self.__column_list = self.__query_type_out.get('queryTypeNamed', [])

        if self.__column_list:  # if there is data in `queryTypeOut`, means it was a `SELECT` query
            self.__statement_type = "SELECT"
            self.__parsed_rows = []
            self.__unparsed_row_amount = 0
            self.__generate_columns_data()
            self.__fill_col_lists()
        else:
            self.__statement_type = "DML"
            self.__close_stmt()

    def __put_file_to_server(self):
        """
        Read local file content and send it to the server in binaries
        """

        local_file = self.__prepare_params["local_file_read"]
        file_limit_mb = self.__prepare_params["staging_area_file_limit_mb"]
        self.__logger.debug(f"Sending local file: '{local_file}' to server")
        self.__logger.debug(f"Checking file size does not exceed allowed file limit mb: {file_limit_mb}")

        try:
            validate_file_size(local_file, file_limit_mb)

            with open(local_file, "rb") as file:
                chunk = file.read(BYTES_PER_FLUSH_LIMIT)

                while chunk:
                    byte_list = [chunk]
                    self.__client.send_data(1, byte_list, len(chunk))
                    chunk = file.read(BYTES_PER_FLUSH_LIMIT)

                self.__client.send_data(0, [], 0)

            self.__logger.debug(f"File '{local_file}' sent successfully.")

        except FileNotFoundError:
            self.__logger.log_and_raise(Error, f"File '{local_file}' not found.")
        except Exception as e:
            self.__logger.log_and_raise(Error, f"Error sending file '{local_file}': {e}")

    def __get_file_from_server(self):
        """
        Get binaries from server and write them to a local file
        If the file already exists, an incremental number is added to the filename.
        """

        original_file_to_write = self.__prepare_params["local_file_write"]
        file_to_write = get_unique_filename(original_file_to_write)

        file_size = self.__query_type_out.get("getFileSize", 0)
        self.__logger.debug(f"Reading file from server and writing to local path: {file_to_write}")

        try:
            validate_disk_space(file_to_write, file_size)

            with open(file_to_write, 'wb') as output_stream:
                self.__fetch()  # fetch fills self.__unsorted_data_columns with a list of bytes we read
                data_buffer = self.__fill_data_buffer()

                while data_buffer and len(data_buffer):
                    output_stream.write(data_buffer)
                    self.__unsorted_data_columns.clear()
                    self.__fetch()
                    data_buffer = self.__fill_data_buffer()

            self.__more_to_fetch = False
            self.__logger.debug(f"Successfully read file from server to path: '{file_to_write}'")

        except Exception as e:
            self.__logger.log_and_raise(Error, f"Failed to save file on local disk: {str(e)}")

    def __fill_data_buffer(self):
        return self.__unsorted_data_columns[0] if len(self.__unsorted_data_columns) > 0 else None

    def __handle_parameterized(self, data_as: str, params: list[Any] | tuple[Any], amount: int | None) -> None:
        """
        prepares the data and send it to the server
        """

        # Check if arrays are allowed before executing the rest
        if not self.__validate_arrays_usage():
            self.__logger.log_and_raise(ArraysAreDisabled, "Arrays are disabled in this connection.",
                                        connection_id=self.__connection_id, statement_id=self.__stmt_id)

        self.__generate_columns_data()
        self.__fill_col_lists()

        self.__row_size = sum([sum(self.__col_sizes),
                               sum(null for null in self.__col_nul if null is True),
                               sum(tvc for tvc in self.__col_tvc if tvc is True)
                               ])

        if self.__row_size * ROWS_PER_FLUSH <= BYTES_PER_FLUSH_LIMIT:
            self.__rows_per_flush = int(ROWS_PER_FLUSH)
        else:
            self.__rows_per_flush = int(BYTES_PER_FLUSH_LIMIT / self.__row_size)

        self.__buffer.clear()

        if data_as == 'alchemy_flat_list':
            # Unflatten SQLalchemy data list
            row_len = len(self.__column_list)
            rows_or_cols = [params[i: i + row_len] for i in range(0, len(params), row_len)]
            data_as = 'rows'
        else:
            rows_or_cols = params

        if 'numpy' in repr(type(params[0])):
            data_as = 'numpy'

        column_lengths = [len(row_or_col) for row_or_col in rows_or_cols]

        if column_lengths.count(column_lengths[0]) != len(column_lengths):
            self.__logger.log_and_raise(ProgrammingError, "Inconsistent data sequences passed for inserting. Please use rows/columns of consistent length",
                                        connection_id=self.__connection_id, statement_id=self.__stmt_id)

        if data_as == 'rows':
            self.__capacity = amount or len(rows_or_cols)
            self.__cols = list(zip(*rows_or_cols))
        else:
            self.__cols = rows_or_cols
            self.__capacity = len(self.__cols)

        self.__send_columns()
        self.__column_list.clear()

    def __fill_col_lists(self) -> None:
        """
        fills the column list information - types, sizes and scales
        """

        self.__col_types.clear()
        self.__col_sizes.clear()
        self.__col_scales.clear()

        for type_tup in self.__col_type_tups:
            is_array = 'ftArray' in type_tup
            offset = 0
            _type = type_tup[0]
            if is_array:
                # for array other stuff like scale is shifted in type_tup
                offset = 1
                # Use tuple for ftArray that will be checked
                # only in buffer like 'ftArray' in col_type
                _type = type_tup[0:2]
            self.__col_types.append(_type)
            self.__col_sizes.append(type_tup[1 + offset] if type_tup[1 + offset] != 0 else TEXT_ITEM_SIZE)
            self.__col_scales.append(type_tup[2 + offset])

    def __validate_arrays_usage(self) -> bool:
        """
        Checks if the executing statement uses arrays and if they are allowed.

        Returns:
            bool: False if arrays are not allowed by connection, but used in
              statement, True otherwise.
        """

        if not self.__allow_array:
            for col in self.__column_list:
                if "ftArray" in col["type"]:
                    return False
        return True

    def __fill_description(self) -> None | List:
        """
        Getting parameters for the cursor's 'description' attribute, even for
        a query that returns no rows. For each column, this includes:
        (name, type_code, display_size, internal_size, precision, scale, null_ok)
        """

        if self.__statement_type != 'SELECT':
            self.description = None
            return self.description

        self.description = []
        for col_name, col_nullalbe, col_type_tup in zip(
                self.__col_names, self.__col_nul, self.__col_type_tups):
            type_code = TYPE_MAPPER.get_typecode(col_type_tup[0])  # Convert SQream type to DBAPI identifier
            display_size = internal_size = col_type_tup[
                1]  # Check if other size is available from API
            precision = 38
            scale = col_type_tup[2]

            self.description.append(
                (col_name, type_code, display_size, internal_size, precision,
                 scale, col_nullalbe))

        return self.description

    def __generate_columns_data(self) -> None:
        """
        In order to send data to server in parameterized queries or when we want to fetch data,
        we need to fill all attributes in the list below:
        1) col_names - list of column names
        2) col_tvc - list of `isTrueVarChar` values
        3) col_nul - list of nullable column properties
        4) col_type_tups - list with column types description (type, size, scale)
        5) col_names_map - dictionary with col_name and index (from 0) for every column

        Content could be received from 'queryTypeIn' or 'queryTypeOut' requests
        Server returns a list of columns data that looks like this:
        { "isTrueVarChar": false, "nullable": true, "type": ["ftInt", 4, 0] }
        """

        self.__col_names = [col.get("name", "") for col in self.__column_list]
        self.__col_tvc = [col["isTrueVarChar"] for col in self.__column_list]
        self.__col_nul = [col["nullable"] for col in self.__column_list]
        self.__col_type_tups = [col["type"] for col in self.__column_list]
        self.__col_names_map = {name: idx for idx, name in enumerate(self.__col_names)}

    def __send_columns(self) -> None:
        """
        Used for parameterized statements.
        After information about all columns was collected by `_execute_sqream_statement` and
        `_generate_columns_data_for_parameterized_statement` methods

        We need to send these data to server to make it inserts parameters via
        slicing a chunk of columns and pass to _send_column_chunk()
        """

        start_idx = 0
        while self.__cols != [()]:
            col_chunk = [col[start_idx:start_idx + self.__rows_per_flush] for col in self.__cols]
            chunk_len = len(col_chunk[0])
            if chunk_len == 0:
                break
            self.__send_column_chunk(col_chunk, chunk_len)
            start_idx += self.__rows_per_flush
            del col_chunk

            self.__logger.debug(f"Sent {chunk_len} rows of data", connection_id=self.__connection_id, statement_id=self.__stmt_id)

    def __send_column_chunk(self, cols: List = None, capacity: int = None) -> None:
        """
        Perform parameterized query - "put" json, header, binarized columns. Used by executemany()
        """

        cols = cols or self.__cols
        cols = cols if isinstance(cols, (list, tuple, set, dict)) else list(cols)

        capacity = capacity or self.__capacity
        # Send columns and metadata to be packed into our buffer
        packed_cols = self.__buffer.pack_columns(cols, capacity, self.__col_types,
                                                 self.__col_sizes, self.__col_nul,
                                                 self.__col_tvc, self.__col_scales)
        byte_count = functools.reduce(lambda c, n: c + len(n), packed_cols, 0)
        self.__client.send_data(capacity, packed_cols, byte_count)

    def __fetch(self):
        """
        sends fetch request to the server, keeps the unsorted data columns list
        """

        fetch_meta = self.__client.fetch()
        num_rows_fetched, column_sizes = fetch_meta['rows'], fetch_meta['colSzs']

        if num_rows_fetched == 0:
            self.__close_stmt()
            return num_rows_fetched

        # Get preceding header
        self.__client.receive(10)

        # Get data as memoryviews of bytearrays.
        self.__unsorted_data_columns = [memoryview(self.__client.receive(size)) for idx, size in enumerate(column_sizes)]
        self.__unparsed_row_amount = num_rows_fetched

    def __fetch_and_parse(self, requested_row_amount: int, data_as: str = "rows") -> None:
        """
        See if this amount of data is available or a fetch from sqream is required
        -1 - fetch all available data. Used by fetchmany()
        """

        if data_as == 'rows':
            self.__buffer.clear()

            self.__fetch()
            self.__more_to_fetch = bool(self.__unparsed_row_amount)  # __fetch() updates self.unparsed_row_amount

            while (requested_row_amount > len(self.__parsed_rows) or requested_row_amount == -1) and self.__more_to_fetch:
                unpacked_columns = self.__buffer.unpack_columns(
                    unsorted_data_columns=self.__unsorted_data_columns,
                    col_types=self.__col_types,
                    col_sizes=self.__col_sizes,
                    col_nul=self.__col_nul,
                    col_tvc=self.__col_tvc,
                    col_scales=self.__col_scales
                )

                self.__parsed_rows.extend(zip(*unpacked_columns))
                self.__unparsed_row_amount = 0
                self.__fetch()
                self.__more_to_fetch = bool(self.__unparsed_row_amount)  # _fetch() updates self.unparsed_row_amount

            self.__buffer.clear()
            self.__unsorted_data_columns.clear()

    def __close_stmt(self) -> None:
        """
        Closes open statement with SQREAM

        Raises:
            ProgrammingError: If server responds with invalid JSON
            ProgrammingError: If server responds with valid JSON,
              but it is not object
            OperationalError: If server responds with "error" key in JSON
        """

        if self.__open_statement:
            self.__logger.info("Closing statement", connection_id=self.__connection_id, statement_id=self.__stmt_id)
            self.__client.close_statement()
            self.__open_statement = False
            self.__buffer.clear()
            self.__logger.debug("Done executing statement", connection_id=self.__connection_id, statement_id=self.__stmt_id)
