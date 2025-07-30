"""Contains pysqream global variables"""

import sys
from pysqream.utils import get_ram_windows, get_ram_linux
from pysqream.type_mapper import TypeMapper
WIN = sys.platform in ('win32', 'cygwin')
MAC = sys.platform in ('darwin',)
PROTOCOL_VERSION = 8
SUPPORTED_PROTOCOLS = 6, 7, 8
BUFFER_SIZE = 100 * int(1e6)  # For setting auto-flushing on netrwork insert
ROWS_PER_FLUSH = 1000000
BYTES_PER_FLUSH_LIMIT = 200 * 1024 * 1024
TEXT_ITEM_SIZE = 100
DEFAULT_CHUNKSIZE = 0  # Dummy variable for some jsons
FETCH_MANY_DEFAULT = 1  # default parameter for fetchmany()
VARCHAR_ENCODING = 'ascii'
CAN_SUPPORT_PARAMETERS = True
CAN_SUPPORT_CLUSTER_FILES = True

CYTHON = False # Cython IS NOT SUPPORTED
clean_sqream_errors = False
support_pandas = False

if WIN:
    get_ram = get_ram_windows()
elif MAC:
    get_ram = None
else:
    get_ram = get_ram_linux()

TYPE_MAPPER = TypeMapper()

DEFAULT_LOG_PATH = "/tmp/pysqream_logs.log"
SQREAM_OLDEST_DATETIME_LONG = 2980282101661696  # datetime(1900, 1, 1) equivalent as a long
SQREAM_OLDEST_DATE_LONG = 693901  # date(1900, 1, 1) equivalent as a long
SQREAM_OLDEST_DATETIME2 = (  # ftTimestampTz
    0,              # utc_offset_seconds (no offset)
    0,              # nano_seconds (no sub-millisecond part)
    0,              # time_as_int (midnight, no milliseconds)
    693901         # date_as_int (1900-01-01)
)
