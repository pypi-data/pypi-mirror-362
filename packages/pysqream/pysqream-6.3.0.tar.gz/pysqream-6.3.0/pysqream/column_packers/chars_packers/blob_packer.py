from typing import List, Any
from struct import pack_into
from pysqream.column_packers.column_packer import ColumnPacker, ColumnData
from pysqream.casting import lengths_to_pairs


class BlobPacker(ColumnPacker):
    """
    Packs blob data type
    """

    def _pack_data(self, data: List[str]) -> bytes:
        # For blobs, encode strings and pack lengths
        encoded = [s.encode('utf8') for s in data]
        packed_strings = b''.join(encoded)

        # Resize the buffer if not enough space for the current strings
        needed_buf_size = len(packed_strings) + 5 * len(data)

        if needed_buf_size > len(self.buf_map):
            self.buf_map.resize(needed_buf_size)

        # Pack nvarchar length column
        pack_into(f'{len(data)}i', self.buf_map, self.buf_idx, *[len(string) for string in encoded])

        self.buf_idx += 4 * len(data)

        return self.write_packed_data(packed_strings)

    def unpack(self, column_data: ColumnData) -> List[Any]:
        column_data.true_nvarchar = column_data.true_nvarchar.cast('i')
        self._cast_data_to_bytes(column_data)

        if self.metadata.nullable:
            col = [None if (self._is_null(n)) else column_data.data_column[start:end].decode('utf8')
                   for (start, end), n in zip(lengths_to_pairs(column_data.true_nvarchar), column_data.nullable)]
        else:
            col = [
                column_data.data_column[start:end].decode('utf8')
                for (start, end) in lengths_to_pairs(column_data.true_nvarchar)
            ]
        return col
