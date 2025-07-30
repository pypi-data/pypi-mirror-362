import numpy as np
import pandas as pd
from mmap import mmap
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any, List, Union
from pysqream.globals import ROWS_PER_FLUSH, TYPE_MAPPER


class PackingError(Exception):
    """
    Custom exception for packing errors
    """

    def __init__(self, message: str, col_idx: int = None, col_type: str = None):
        self.message = message
        if col_idx is not None and col_type is not None:
            self.message = f"Error packing column {col_idx + 1} of type '{col_type}', error is: {message}"
        super().__init__(self.message)


@dataclass
class ColumnMetadata:
    """
    Metadata for a column to be packed/unpacked
    """

    col_idx: int
    col_type: Union[str, list[str]]  # Support for both regular and array types. array is represented as list of two strings, example: ['ftArray', 'ftInt']
    size: int
    nullable: bool
    tvc: bool
    scale: int


@dataclass
class ColumnData:
    """
    Actual data received from server from fetch request.
    Used on unpack function
    """

    data_column: Union[memoryview, bytes]
    nullable: Union[memoryview, bool]
    array_lengths: Union[memoryview, None]
    true_nvarchar: Union[memoryview, bool]


class ColumnPacker(ABC):
    """
    Abstract base class for column packers
    """

    uses_standard_packing: bool = True

    def __init__(self, metadata: ColumnMetadata):
        self.metadata: ColumnMetadata = metadata
        self.buf_map: Union[mmap, None] = None
        self.buf_idx: int = 0

    @staticmethod
    def _is_null(nullable_byte: int) -> bool:
        return nullable_byte == 1

    def pack(self, data: Union[List[Any], np.ndarray]) -> bytes:
        """
        Template method that defines the packing algorithm structure.
        """

        if self.uses_standard_packing:
            self.allocate_buf_map()
            self.handle_nulls(data)
            return self._pack_data(data)

        return self._pack_custom(data)

    @abstractmethod
    def unpack(self, column_data: ColumnData) -> List[Any]:
        """
        Abstract method that subclasses must implement to define their specific unpacking extract logic.
        """

        pass

    @abstractmethod
    def _pack_data(self, data: List[Any]) -> bytes:
        """
        Abstract method that subclasses must implement to define their specific packing logic.
        """

        pass

    def _pack_custom(self, data: Union[List[np.ndarray], List[Union[List[Any], None]]]) -> bytes:
        """
        Custom packing logic for subclasses that don't use the standard flow.
        Only needs to be implemented if 'uses_standard_packing' is False.
        """

        raise NotImplementedError("Custom packing not implemented for this packer")

    def _cast_data_by_pack_code(self, column_data: ColumnData):
        column_data.data_column = column_data.data_column.cast(TYPE_MAPPER.get_pack_code(self.metadata.col_type))

    @staticmethod
    def _cast_data_to_bytes(column_data: ColumnData):
        column_data.data_column = column_data.data_column.tobytes()

    def allocate_buf_map(self):
        """
        Allocate bytes buffer which we send to the server
        """

        self.buf_map = mmap(-1, ((1 if self.metadata.nullable else 0) + (self.metadata.size if self.metadata.size != 0 else 104)) * ROWS_PER_FLUSH)

    def clear(self):
        """
        Clears the byte buffer
        """

        if self.buf_map:
            self.buf_map.close()

    def handle_nulls(self, data: List[Any]) -> int:
        """
        Handle null values in the column data.
        Writes nulls into the buffer and increments the buffer index
        """

        if not self.metadata.nullable:
            return 0

        idx = -1

        while True:
            try:
                while True:
                    idx += 1
                    val = data[idx]
                    if any(val is x for x in [None, pd.NA]) or pd.isna(val):
                        break
            except IndexError:
                break

            self.buf_map.seek(self.buf_idx + idx)
            self.buf_map.write(b'\x01')
            data[idx] = TYPE_MAPPER.get_default_value(self.metadata.col_type, self.metadata.size)

        self.buf_idx = len(data)

    def write_packed_data(self, packed_data: Union[list, bytes]) -> bytes:
        """
        Helper method to write packed data to buffer
        """

        self.buf_map.seek(self.buf_idx)
        self.buf_map.write(bytearray(packed_data))
        self.buf_idx += len(packed_data)

        return self.buf_map[:self.buf_idx]
