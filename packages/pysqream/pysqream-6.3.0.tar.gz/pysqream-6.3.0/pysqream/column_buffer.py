from pysqream.globals import BUFFER_SIZE
from pysqream.utils import DataError, ProgrammingError
from pysqream.column_packers.column_packer import ColumnMetadata, ColumnData, ColumnPacker
from pysqream.column_packers.packer_factory import get_packer
from typing import List, Dict, Union, Any
from pysqream.logger import ContextLogger


class ColumnsBuffer:
    """
    Handles the management of column buffers for database communication.
    Responsible for:
    - Managing data handlers for both packing and unpacking operations
    - Managing memory and cleanup of handlers
    """

    def __init__(self, logger: ContextLogger):
        self.logger = logger
        self.current_packers: List[ColumnPacker] = []
        self.buffer_size: int = BUFFER_SIZE  # currently not doing anything with buffer size
        self.metadata_cache: List[ColumnMetadata] = []  # cache metadata to reuse for unpacking

    def pack_columns(self, cols: List[Any], capacity: int, col_types: List[Union[str, list[str]]], col_sizes: List[int],
                     col_nul: List[Union[bool, memoryview]], col_tvc: List[Union[bool, memoryview]], col_scales: List[int]) -> List[bytes]:
        """
        Packs the given columns into byte buffers for transmission to the server.
        This method iterates over the columns, generates metadata for each column,
        and uses appropriate packer based on the column type. It stores the packers
        for later cleanup and returns the packed column data.
        """

        try:
            pool_params = list(zip(cols, range(len(col_types)), col_types, col_sizes, col_nul, col_tvc, col_scales))
            self.clear()

            packed_cols = []
            for col_tup in pool_params:
                # col: list of rows that could be lists that represents array or None
                # col_idx: integer index of inserting column,
                # col_type: string (enum) that represents data type that array contains, can be ftBool, ftInt, etc..
                # nullable: boolean that show whether column is nullable or not,
                # scale: integer represent Numerical Rating Scale, for numerical only
                # tvc: boolean isTrueVarChar
                col, col_idx, col_type, size, nullable, tvc, scale = col_tup
                metadata = ColumnMetadata(col_idx, col_type, size, nullable, tvc, scale)
                data = list(col)

                packer = get_packer(metadata, data=data)
                self.current_packers.append(packer)
                packed_cols.append(packer.pack(data))

            return packed_cols

        except DataError:
            raise
        except Exception as e:
            self.logger.log_and_raise(ProgrammingError, f"Error packing columns. Check that all types match the respective column types. Error raised is: {e}")

    @staticmethod
    def _get_raw_columns(unsorted_data_columns: List[memoryview], col_types: List[Union[str, list[str]]], col_sizes: List[int],
                         col_nul: List[Union[bool, memoryview]], col_tvc: List[Union[bool, memoryview]]) -> List[Dict]:
        """
        Processes a list of byte buffers into structured column data.
        Args:
            unsorted_data_columns: List of byte buffers representing column data.
            col_types: Data types of the columns.
            col_sizes: Sizes of the columns.
            col_nul: Boolean flags indicating whether columns are nullable.
            col_tvc: Boolean flags indicating whether columns have a "true nvarchar" property.
        Returns:
            A list of dictionaries representing processed columns.
        """

        data_iter = iter(unsorted_data_columns)  # using an iterator to avoid list modification inefficiency
        raw_columns = []

        for nullable, size, tvc, data_type in zip(col_nul, col_sizes, col_tvc, col_types):
            column = {}
            is_array = 'ftArray' in data_type

            column['nullable'] = next(data_iter) if nullable else False

            if is_array:
                column['array_lengths'] = next(data_iter)
            elif tvc:
                column['true_nvarchar'] = next(data_iter)

            column['data_column'] = next(data_iter)

            raw_columns.append(column)

        return raw_columns

    def unpack_columns(self, unsorted_data_columns: List[memoryview], col_types: List[Union[str, list[str]]], col_sizes: List[int],
                       col_nul: List[Union[bool, memoryview]], col_tvc: List[Union[bool, memoryview]], col_scales: List[int]
                       ) -> List[Union[memoryview, List]]:
        """
        Unpacks columns from wire format back into Python data types.
        """

        raw_columns = self._get_raw_columns(unsorted_data_columns, col_types, col_sizes, col_nul, col_tvc)

        try:
            if not self.metadata_cache or len(self.metadata_cache) != len(col_types):
                self.metadata_cache = [
                    ColumnMetadata(idx, col_type, size, nullable, tvc, scale)
                    for idx, (col_type, size, nullable, tvc, scale)
                    in enumerate(zip(col_types, col_sizes, col_nul, col_tvc, col_scales))
                ]

            unpacked_cols = []
            for idx, raw_col in enumerate(raw_columns):
                metadata = self.metadata_cache[idx]

                fetched_data = ColumnData(
                    data_column=raw_col['data_column'],
                    nullable=raw_col.get('nullable', False),
                    array_lengths=raw_col.get('array_lengths'),
                    true_nvarchar=raw_col.get('true_nvarchar', False)
                )

                packer = get_packer(metadata)
                self.current_packers.append(packer)
                unpacked_cols.append(packer.unpack(fetched_data))

            return unpacked_cols

        except Exception as e:
            message = f"Error unpacking columns from server data {e}"
            self.logger.log_and_raise(ProgrammingError, message)

    def clear(self):
        """
        Clear all current packers
        """

        for packer in self.current_packers:
            packer.clear()

        self.current_packers.clear()
        self.metadata_cache.clear()
