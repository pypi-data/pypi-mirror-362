from struct import pack_into
from typing import Any, List
from abc import abstractmethod
from pysqream.globals import TYPE_MAPPER
from pysqream.column_packers.column_packer import ColumnPacker, ColumnData


class AbstractDatePacker(ColumnPacker):
    """
    Abstract date packer for date and datetime data types
    """

    def _pack_data(self, data: List[str]) -> bytes:
        values = [self._transform_value(d) for d in data]
        pack_into(f'{len(data)}{TYPE_MAPPER.get_pack_code(self.metadata.col_type)}',
                  memoryview(self.buf_map), self.buf_idx, *values)
        self.buf_idx += len(data) * self.metadata.size

        return self.buf_map[:self.buf_idx]

    def unpack(self, column_data: ColumnData):
        self._cast_data_by_pack_code(column_data)

        if self.metadata.nullable:
            col = [self._backward_transform_value(d, is_null=self._is_null(n))
                   for d, n in zip(column_data.data_column, column_data.nullable)]
        else:
            col = [self._backward_transform_value(d) for d in column_data.data_column]
        return col

    @abstractmethod
    def _transform_value(self, value: Any) -> Any:
        pass

    @abstractmethod
    def _backward_transform_value(self, value: Any, is_null: bool = False) -> Any:
        pass
