import os
import re
import shutil
from packaging import version
from subprocess import Popen, PIPE
from functools import wraps
from typing import Callable, TypeVar, Any


def get_ram_linux():
    vmstat, err = Popen('vmstat -s'.split(), stdout=PIPE, stderr=PIPE).communicate()

    return int(vmstat.splitlines()[0].split()[0])


def get_ram_windows():
    pass


def validate_file_size(file: str, file_limit_mb: int):
    """
    Validates given file does not exceed the allowed file size in mb
    """

    file_size_bytes = os.path.getsize(file)
    file_size_mb = file_size_bytes / (1024 * 1024)

    if file_size_mb > file_limit_mb:
        raise RuntimeError(f"File size exceeds the allowed limit of {file_limit_mb} MB. Actual size: {file_size_mb:.2f} MB.")


def validate_disk_space(path: str, file_size: int) -> None:
    """
    Check if there is enough disk space at the specified file path location.
    Raise exception if there isn't enough disk space.

    Args:
        path: Path to the file (not directory)
        file_size: Required file size in bytes
    """

    directory = os.path.dirname(path) or "."

    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist")

    free_space = shutil.disk_usage(directory).free

    if free_space < file_size:
        raise RuntimeError(f"Not enough disk space. Required: {file_size} bytes, available: {free_space} bytes.")


def get_unique_filename(filepath):
    """
    Generate a unique filename by adding incremental numbers if the file already exists.
    Example: If 'file.txt' exists, returns 'file (1).txt'.
    If 'file (1).txt' also exists, returns 'file (2).txt', and so on.
    """

    if not os.path.exists(filepath):
        return filepath

    directory, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)

    counter = 1
    pattern = re.compile(r'^(.*?)( \((\d+)\))?$')
    match = pattern.match(name)

    if match:
        base_name = match.group(1)
    else:
        base_name = name

    while True:
        new_name = f"{base_name} ({counter}){ext}"
        new_path = os.path.join(directory, new_name)

        if not os.path.exists(new_path):
            return new_path

        counter += 1


# Version compare
def version_compare(v1, v2) :
    if v2 is None or v1 is None:
        return None
    r1 = re.search("\\d{4}(\\.\\d+)+", v1)
    r2 = re.search("\\d{4}(\\.\\d+)+", v2)
    if r2 is None or r1 is None:
        return None
    v1 = version.parse(r1.group(0))
    v2 = version.parse(r2.group(0))
    return -1 if v1 < v2 else 1 if v1 > v2 else 0


def get_array_size(data_size: int, buffer_length: int) -> int:
    """Get the SQream ARRAY size by inner data size and buffer length

    Args:
        data_size: integer with the size of data inside ARRAY, for
          example for INT is 4, for BOOL is 1, etc.
        buffer_length: length of a chunk of buffer connected with one
          array

    Returns:
        An integer representing size of an ARRAY with fixed sized data
    """
    aligned_block_size = (data_size + 1) * 8  # data + 1 byte for null
    div, mod = divmod(buffer_length, aligned_block_size)
    size = div * 8
    if mod:
        size += int((mod - 8) / data_size)
    return size


def false_generator():
    """Generate endless sequence of False values

    Used for providing to zip(data, false_generator()) within data that
    is not nullable, so is_null value will also goes as False
    independent of size of data

    Example:
        >>> for val, is_null in zip([1, 2, 3, 4]], false_generator()):
        ...     print(val,is_null)
        ...
        1 False
        2 False
        3 False
        4 False

    Returns:
        A generator object that produces False value for each iteration
          endlessly
    """
    while True:
        yield False


class Error(Exception):
    pass


class Warning(Exception):
    pass


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class DataError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class IntegrityError(DatabaseError):
    pass


class InternalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass


class ArraysAreDisabled(DatabaseError):
    pass


T = TypeVar('T')


def dbapi_method(f: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to mark methods that are part of the DB-API 2.0 specification.
    This helps maintain compliance and prevents accidental removal.

    Reference: PEP 249 – Python Database API Specification v2.0
    https://peps.python.org/pep-0249/
    """

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        return f(*args, **kwargs)

    setattr(wrapper, "_is_dbapi", True)
    return wrapper


class DBAPIAttribute:
    """Wrapper class to mark an attribute as a DB-API attribute."""
    def __init__(self, value):
        self.value = value
        self._is_dbapi_attr = True  # Marked attribute

    def __repr__(self):
        return f"<DBAPIAttribute value={self.value}>"


def mark_dbapi_attribute(value):
    return DBAPIAttribute(value)
