from __future__ import annotations

import time
import socket
from typing import Union, List, Dict
from struct import unpack
from pysqream.cursor import Cursor
from pysqream.server.sqsocket import SQSocket
from pysqream.server.sqclient import SQClient
from pysqream.server.connection_params import ConnectionParams
from pysqream.utils import ProgrammingError, Error, dbapi_method
from pysqream.globals import DEFAULT_LOG_PATH
from pysqream.logger import ContextLogger


class Connection:
    """
    Connection class used to interact with SQreamDB.
    The very first connection is called the "base connection".
    For every cursor we open, we create another connection since in sqream every statement should run in its own connection
    This another connection is called "sub connection".
    Every sub connection holds its cursor in cursors dict.
    The base connection holds all sub connections in sub_connections list.
    """

    def __init__(self, conn_params: ConnectionParams, log: Union[bool, str] = False, base_connection: bool = True,
                 reconnect_attempts: int = 3, reconnect_interval: int = 10, allow_array: bool = True, logging_level: str = "INFO",
                 context_logger: Union[ContextLogger] = None):
        self.__version: Union[str, None] = None
        self.__is_connection_closed: bool = False
        self.__connection_id: Union[int, None] = None
        self.__connect_to_socket: bool = False
        self.__connect_to_database: bool = False
        self.__reconnect_attempts: int = reconnect_attempts
        self.__reconnect_interval: int = reconnect_interval
        self.__base_connection: bool = base_connection
        self.__client: Union[SQClient, None] = None
        self.__cursors: Dict[int, Cursor] = {}
        self.__sub_connections: List[Connection] = []

        # SQreamDB connection parameters attributes
        self.__conn_params: ConnectionParams = conn_params
        self.__allow_array: bool = allow_array

        self.__logger = context_logger if context_logger else self.__set_logger(log, logging_level)
        self.__validate_attributes()
        self.__open_connection()
        self.__connect_database()

    def __set_logger(self, log: Union[bool, str], logging_level: str) -> ContextLogger:
        self.__logger = ContextLogger()

        if log:
            self.__logger.start_logging(DEFAULT_LOG_PATH if log is True else log, logging_level=logging_level)

        return self.__logger

    def __enter__(self) -> Connection:
        """
        Implementation for context manager ("with" clause)
        """

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """
        Implementation for context manager ("with" clause)
        """

        self.close()

    def __del__(self) -> None:
        """
        Finalizer for connection object. Closes all sub connections and their cursors
        """

        if not self.__is_connection_closed:
            try:
                self.__logger.debug("Try to destroy open connections", connection_id=self.__connection_id)
                self.close()
            except Exception as e:
                if "Trying to close a connection that's already closed" not in repr(e):
                    self.__logger.log_and_raise(ProgrammingError, e, connection_id=self.__connection_id)

        if self.__base_connection:
            self.__logger.stop_logging()

    def __iter__(self) -> Connection:
        """
        Implementation for iterating connection in for-in clause
        """

        for sub_conn in self.__sub_connections:
            yield sub_conn

    # DB-API Must have methods
    # ------------------------
    @dbapi_method
    def close(self) -> None:
        """
        If we are in base connection - iterate every sub connection and call its close method
        then, for every cursor we have in our connection, we call cursor close method
        """

        if not self.__connect_to_database:
            if self.__connect_to_socket:
                return self.__client.disconnect_socket()
            return

        if self.__base_connection:
            for sub_conn in self.__sub_connections:
                sub_conn.close()

        for con_id, cursor in self.__cursors.items():
            try:
                if not cursor.get_is_cursor_closed():
                    cursor._Cursor__is_connection_initiated_close = True
                    cursor.close()
            except Exception as e:
                self.__logger.log_and_raise(Error, f"Can't close connection - {e}", connection_id=con_id)

        self.__cursors.clear()
        self.__sub_connections.clear()
        self.__close_connection()
        self.__is_connection_closed = True

    @dbapi_method
    def cursor(self) -> Cursor:
        """
        Create a new sub-connection with the same connection parameters and create a cursor for that sub connection.
        We use a connection as the equivalent of a 'cursor'
        """

        self.__logger.debug("Create cursor", connection_id=self.__connection_id)
        self.__verify_con_open()
        sub_conn_params = ConnectionParams(self.__conn_params.origin_ip if self.__conn_params.clustered else self.__conn_params.ip,
                                           self.__conn_params.origin_port if self.__conn_params.clustered is True else self.__conn_params.port,
                                           self.__conn_params.database,
                                           self.__conn_params.username,
                                           self.__conn_params.password,
                                           self.__conn_params.clustered,
                                           self.__conn_params.use_ssl,
                                           self.__conn_params.service)
        sub_conn = Connection(
            sub_conn_params,
            base_connection=False,
            reconnect_attempts=self.__reconnect_attempts,
            reconnect_interval=self.__reconnect_interval,
            allow_array=self.__allow_array,
            context_logger=self.__logger
        )
        sub_conn.__verify_con_open()

        cur = Cursor(sub_conn.__conn_params, sub_conn.__client, sub_conn.__connection_id, sub_conn.__allow_array, self.__logger)
        sub_conn.__cursors[cur.get_connection_id()] = cur

        if self.__base_connection:
            self.__sub_connections.append(sub_conn)

        return cur

    @dbapi_method
    def commit(self):
        """
        DB-API requires this method, but SQream doesn't support transactions in the traditional sense
        """

        self.__logger.log_and_raise(NotImplementedError, "Commit called (not supported for SQreamDB)", connection_id=self.__connection_id)

    @dbapi_method
    def rollback(self):
        """
        DB-API requires this method, but SQream doesn't support transactions in the traditional sense
        """

        self.__logger.log_and_raise(NotImplementedError, "Rollback called (not supported for SQreamDB)", connection_id=self.__connection_id)

    # Internal Methods
    # ----------------
    def __validate_attributes(self):
        if not isinstance(self.__reconnect_attempts, int) or self.__reconnect_attempts < 0:
            self.__logger.log_and_raise(Exception, f"reconnect attempts should be a positive integer, got : {self.__reconnect_attempts}")
        if not isinstance(self.__reconnect_interval, int) or self.__reconnect_attempts < 0:
            self.__logger.log_and_raise(Exception, f"reconnect interval should be a positive integer, got : {self.__reconnect_interval}")

    def __open_connection(self) -> None:
        """
        Get proper ip and port from picker if needed and open a socket to the server. Used at __init__()
        If clustered is true -
         - open a non SSL socker for picker communication
         - Read the first 4 bytes to get readlen and read ip, then read 4 more bytes to get the port

        Then create socket and connect to actual SQreamd server
        """

        if self.__conn_params.clustered is True:
            picker_socket = SQSocket(self.__conn_params.origin_ip, self.__conn_params.origin_port, self.__logger, False)
            self.__client = SQClient(picker_socket)
            picker_socket.timeout(5)

            try:
                read_len = unpack('i', self.__client.receive(4))[0]
                picker_socket.timeout(None)
                self.__conn_params.ip = self.__client.receive(read_len)
                self.__conn_params.port = unpack('i', self.__client.receive(4))[0]
                picker_socket.close()
            except socket.timeout:
                self.__logger.log_and_raise(ProgrammingError, f"Connected with clustered=True, but apparently not a server picker port",
                                            connection_id=self.__connection_id)

        sqsocket = SQSocket(self.__conn_params.ip, self.__conn_params.port, self.__logger, self.__conn_params.use_ssl)
        self.__client = SQClient(sqsocket)
        self.__connect_to_socket = True

    def __connect_database(self) -> None:
        """
        Handle connection to database, with or without server picker
        """

        if self.__connect_to_socket:
            try:
                self.__connection_id, self.__version = self.__client.connect_to_socket(self.__conn_params.username,
                                                                                       self.__conn_params.password,
                                                                                       self.__conn_params.database,
                                                                                       self.__conn_params.service)
            except KeyError as e:
                self.__logger.log_and_raise(ProgrammingError, str(e))

            self.__logger.info(f"Connection opened to database {self.__conn_params.database}.", connection_id=self.__connection_id)
            self.__connect_to_database = True

    def __attempt_reconnect(self) -> bool:
        """
        Attempt to reconnect with exponential backoff
        """

        for attempt in range(self.__reconnect_attempts):
            wait_time = self.__reconnect_interval * (2 ** attempt)  # Exponential backoff
            self.__logger.info(f"Waiting {wait_time} seconds before reconnect attempt {attempt + 1}")
            time.sleep(wait_time)

            try:
                self.__logger.info(f"Reconnect attempt {attempt + 1}")
                self.__open_connection()
                self.__connect_database()
                self.__logger.info(f"Reconnection successful on attempt {attempt + 1}")
                return True
            except Exception as e:
                self.__logger.error(f"Reconnect attempt {attempt + 1} failed: {e}")

        self.__logger.log_and_raise(ConnectionRefusedError, f"All {self.__reconnect_attempts} reconnection attempts failed")

    def __close_connection(self) -> None:
        if self.__is_connection_closed:
            self.__logger.log_and_raise(ProgrammingError, f"Trying to close a connection that's already closed for database "
                                                        f"{self.__conn_params.database}", connection_id=self.__connection_id)
        self.__client.close_connection()
        self.__logger.info(f"Connection closed to database {self.__conn_params.database}.", connection_id=self.__connection_id)

    def __verify_con_open(self) -> None:
        if self.__is_connection_closed:
            self.__logger.log_and_raise(ProgrammingError, "Connection has been closed", connection_id=self.__connection_id)
