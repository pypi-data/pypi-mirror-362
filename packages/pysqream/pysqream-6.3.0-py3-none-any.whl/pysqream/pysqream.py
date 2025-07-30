"""
SQream Native Python API
"""

import time
from datetime import datetime, date, time as t
from pysqream.connection import Connection
from pysqream.server.connection_params import ConnectionParams
from typing import Union


def connect(host: str, port: int, database: str, username: str, password: str, clustered: bool = False,
            use_ssl: bool = False, service: str = "sqream", log: Union[bool, str] = False, **kwargs):
    """
    Connect to a SQream database.

    Establishes a connection to a SQream database using the provided credentials
    and connection parameters.

    Args:
        host (str): The hostname or IP address of the SQream server.
        port (int): The port number of the SQream server.
        database (str): The name of the database to connect to.
        username (str): The username for database authentication.
        password (str): The password for database authentication.
        clustered (bool, optional): Indicates if the database is clustered.
            Defaults to False.
        use_ssl (bool, optional): Specifies whether to use SSL encryption.
            Defaults to False.
        service (str, optional): The service name. Defaults to "sqream".
        log (Union[bool, str], optional): Enables or configures logging.
            - If `True`, enables logging to default path "/tmp/pysqream_logs.log".
            - If `False` (default), disables logging.
            - If a string is provided, it's treated as the path to the log file.
        **kwargs: Additional keyword arguments. These can include:
            - `logging_level` (str, optional): Sets the logging level (e.g., "DEBUG", "INFO", "WARNING", "ERROR"). Defaults to "INFO".

    Returns:
        Connection: A SQream database connection object.  Use this object to
            execute queries and interact with the database.

    Raises:
        Exception:  If the connection to the database fails.

    Example:
        ```python
        # Basic connection
        conn = connect("localhost", 5000, "mydb", "user", "password")

        # Connection to a clustered database and custom logging
        conn = connect("192.168.1.10", 5000, "cluster_db", "cluster_user", "cluster_pass",
                      clustered=True, log="sqream_connections.log")
        ```

    For full documentation, including advanced connection options and API details,
    please refer to the PySQream project page on PyPI:
    [https://pypi.org/project/pysqream/](https://pypi.org/project/pysqream/)
    """

    conn_params = ConnectionParams(host, port, database, username, password, clustered, use_ssl, service)
    conn = Connection(
        conn_params,
        log=log,
        base_connection=True,
        allow_array=kwargs.get("allow_array", True),
        logging_level=kwargs.get("logging_level", "INFO")
    )

    return conn


#  DB-API compatibility
#  -------------------
""" To fully comply to Python's DB-API 2.0 database standard. Ignore when using internally """


class _DBAPITypeObject:
    """DB-API type object which compares equal to all values passed to the constructor.
        https://www.python.org/dev/peps/pep-0249/#implementation-hints-for-module-authors
    """
    def __init__(self, *values):
        self.values = values

    def __eq__(self, other):
        return other in self.values


# Type objects and constructors required by the DB-API 2.0 standard
Binary = memoryview
Date = date
Time = t
Timestamp = datetime


STRING = "STRING"
BINARY = _DBAPITypeObject("BYTES", "RECORD", "STRUCT")
NUMBER = _DBAPITypeObject("INTEGER", "INT64", "FLOAT", "FLOAT64", "NUMERIC",
                          "BOOLEAN", "BOOL")
DATETIME = _DBAPITypeObject("TIMESTAMP", "DATE", "TIME", "DATETIME")
ROWID = "ROWID"


def DateFromTicks(ticks):
    return Date.fromtimestamp(ticks)


def TimeFromTicks(ticks):
    return Time(
        *time.localtime(ticks)[3:6]
    )  # localtime() returns a namedtuple, fields 3-5 are hr/min/sec


def TimestampFromTicks(ticks):
    return Timestamp.fromtimestamp(ticks)


# DB-API global parameters
apilevel = '2.0' 
threadsafety = 1  # Threads can share the module but not a connection
paramstyle = 'qmark'
