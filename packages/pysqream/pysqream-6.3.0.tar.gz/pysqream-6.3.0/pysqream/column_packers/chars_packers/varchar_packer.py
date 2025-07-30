from typing import List, Any
from pysqream.globals import VARCHAR_ENCODING
from pysqream.column_packers.column_packer import ColumnPacker, ColumnData


class VarcharPacker(ColumnPacker):
    """
    Packs varchar data type
    """

    def _pack_data(self, data: List[str]) -> bytes:
        # Fixed-length varchar - encode and pad to fixed size
        encoded = [s.encode(VARCHAR_ENCODING)[:self.metadata.size].ljust(self.metadata.size, b' ')
                   for s in data]
        packed_strings = b''.join(encoded)

        return self.write_packed_data(packed_strings)

    def unpack(self, column_data: ColumnData) -> List[Any]:
        self._cast_data_to_bytes(column_data)

        varchar_size = self.metadata.size
        if self.metadata.nullable:
            col = []
            offset = 0
            for idx in column_data.nullable:
                if self._is_null(idx):
                    col.append(None)
                    offset = offset + varchar_size
                else:
                    col.append(column_data.data_column[offset:offset + varchar_size]
                               .decode("ascii", "ignore")
                               .replace('\x00', '')
                               .rstrip())
                    offset = offset + varchar_size
        else:
            col = [
                column_data.data_column[idx:idx + varchar_size].decode("ascii", "ignore").replace('\x00', '').rstrip()
                for idx in range(0, len(column_data.data_column), varchar_size)
            ]
        return col
