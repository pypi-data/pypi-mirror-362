import numpy as np
from pysqream.column_packers.number_packers.number_packer import NumberPacker
from pysqream.column_packers.number_packers.decimal_packer import DecimalPacker
from pysqream.column_packers.chars_packers.blob_packer import BlobPacker
from pysqream.column_packers.chars_packers.varchar_packer import VarcharPacker
from pysqream.column_packers.date_packers.date_packer import DatePacker
from pysqream.column_packers.date_packers.datetime_packer import DateTimePacker
from pysqream.column_packers.date_packers.timestamptz_packer import TimestampTzPacker
from pysqream.column_packers.array_packers.array_packer import ArrayPacker
from pysqream.column_packers.array_packers.numpy_array_packer import NumpyArrayPacker
from pysqream.column_packers.column_packer import ColumnMetadata, PackingError, ColumnPacker


def get_packer(metadata: ColumnMetadata, data: list = None) -> ColumnPacker:
    """
    Factory function to get appropriate packer for column type
    """

    # TODO: pack method of numpy array packer is not working well. it needs to be investigated and tested.
    #  till then, it is commented out and the native array packer below will be used.
    #  once fixed uncomment test_numpy_array, test_pack_numpy_array and test_numpy_array_packer_mixed_types in test_column_buffer.py
    # if data is not None and len(data) == 1 and isinstance(data[0], np.ndarray):
    #     return NumpyArrayPacker(metadata)

    if isinstance(metadata.col_type, list) and metadata.col_type[0] == 'ftArray':
        return ArrayPacker(metadata)

    packers = {
        'ftBool': NumberPacker,
        'ftUByte': NumberPacker,
        'ftShort': NumberPacker,
        'ftInt': NumberPacker,
        'ftLong': NumberPacker,
        'ftFloat': NumberPacker,
        'ftDouble': NumberPacker,
        'ftVarchar': VarcharPacker,
        'ftBlob': BlobPacker,
        'ftDate': DatePacker,
        'ftDateTime': DateTimePacker,
        'ftTimestampTz': TimestampTzPacker,
        'ftNumeric': DecimalPacker
    }

    packer_class = packers.get(metadata.col_type)
    if not packer_class:
        raise PackingError(f"Unsupported column type", col_idx=metadata.col_idx, col_type=metadata.col_type)

    return packer_class(metadata)
