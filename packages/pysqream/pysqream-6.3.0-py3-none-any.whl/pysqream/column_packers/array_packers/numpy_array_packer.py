import numpy as np
from struct import pack_into
from typing import Any, List
from pysqream.column_packers.column_packer import ColumnPacker, ColumnData


class NumpyArrayPacker(ColumnPacker):
    """
    Packs numpy array types
    """

    uses_standard_packing = False

    def _pack_data(self, data: List[Any]) -> bytes:
        raise NotImplementedError("Standard packing not implemented for numpy array packer")

    def _pack_custom(self, data: List[np.ndarray]) -> bytes:
        """
        Special handling for numpy arrays
        """

        self.allocate_buf_map()
        data = data[0]  # extract the numpy array

        capacity = len(data)

        # Pack null column if applicable
        if self.metadata.nullable:
            # Pack null indicators directly into the buffer
            null_flags = (1 if item in (np.nan, b'') else 0 for item in data)
            pack_into(f'{capacity}b', memoryview(self.buf_map), self.buf_idx, *null_flags)
            self.buf_idx += capacity

            # Replace Nones or invalid data with appropriate placeholders
            if data.dtype.kind == 'S':  # Handle binary strings (`S` for byte strings)
                pass  # b'' already handled
            elif data.dtype.kind == 'U':  # Handle Unicode strings (`U`)
                pass  # Assume no action needed
            else:  # Handle numeric replacements
                # Vectorized replacement for NaN (faster and cleaner)
                data[np.isnan(data)] = 0

        # Pack nvarchar length column if applicable
        if self.metadata.tvc:
            lengths_as_bytes = np.vectorize(len)(data).astype('int32').tobytes()
            self.write_packed_data(lengths_as_bytes)

        # Pack the actual data
        if data.dtype.kind == 'U':
            packed_data = ''.join(data).encode('utf8')
        else:
            packed_data = data.tobytes()

        self.write_packed_data(packed_data)

        return self.buf_map[:self.buf_idx]

    def unpack(self, column_data: ColumnData) -> List[Any]:
        raise NotImplementedError("Extract method is not implemented for this packer")
