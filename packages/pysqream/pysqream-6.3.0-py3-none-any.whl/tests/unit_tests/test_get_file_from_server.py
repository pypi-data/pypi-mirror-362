import sys
import pytest
from pysqream.cursor import Cursor, Error
from unittest.mock import patch, MagicMock, mock_open, call


@patch('pysqream.cursor.validate_disk_space')
@patch('pysqream.cursor.get_unique_filename')
class TestGetFileFromServer:
    """
    Test cases for the cursor.__get_file_from_server method
    """

    @pytest.fixture
    def cursor_mock(self):
        """
        Create a mocked cursor object with necessary attributes
        """

        cursor = MagicMock()
        cursor._Cursor__prepare_params = {"local_file_write": "/path/to/file.txt"}
        cursor._Cursor__query_type_out = {"getFileSize": 1024}
        cursor._Cursor__unsorted_data_columns = []
        cursor._Cursor__more_to_fetch = True
        cursor._Cursor__logger = MagicMock()
        cursor._Cursor__fetch = MagicMock()

        def mock_log_and_raise(exception_class, message):
            raise exception_class(message)

        cursor._Cursor__logger.log_and_raise.side_effect = mock_log_and_raise

        return cursor

    def _setup_fetch_behavior(self, cursor_mock, data_chunks):
        """
        Set up the fetch behavior to return data chunks sequentially
        """

        # An index to track which chunk to return next
        self.data_index = 0
        self.data_chunks = data_chunks

        def mock_fill_data_buffer():
            if cursor_mock._Cursor__unsorted_data_columns and len(cursor_mock._Cursor__unsorted_data_columns) > 0:
                return cursor_mock._Cursor__unsorted_data_columns[0]
            return None

        cursor_mock._Cursor__fill_data_buffer = mock_fill_data_buffer

        def mock_fetch():
            if self.data_index < len(self.data_chunks):
                chunk = self.data_chunks[self.data_index]
                self.data_index += 1

                if chunk is not None:
                    cursor_mock._Cursor__unsorted_data_columns.clear()
                    cursor_mock._Cursor__unsorted_data_columns.append(chunk)

        cursor_mock._Cursor__fetch.side_effect = mock_fetch

    @patch('builtins.open', new_callable=mock_open)
    def test_get_file_from_server_basic(self, mock_open, mock_get_unique, mock_validate, cursor_mock):
        """
        Test basic file download functionality
        """

        mock_get_unique.return_value = "/path/to/unique_file.txt"
        self._setup_fetch_behavior(cursor_mock, [b"data1", b"data2", None])

        Cursor._Cursor__get_file_from_server(cursor_mock)

        mock_get_unique.assert_called_once_with("/path/to/file.txt")
        mock_validate.assert_called_once_with("/path/to/unique_file.txt", 1024)
        mock_open.assert_called_once_with("/path/to/unique_file.txt", "wb")

        file_handle = mock_open()
        assert file_handle.write.call_count == 2
        expected_calls = [call(b"data1"), call(b"data2")]
        file_handle.write.assert_has_calls(expected_calls)
        assert cursor_mock._Cursor__more_to_fetch is False

        debug_calls = [
            call("Reading file from server and writing to local path: /path/to/unique_file.txt"),
            call("Successfully read file from server to path: '/path/to/unique_file.txt'")
        ]
        cursor_mock._Cursor__logger.debug.assert_has_calls(debug_calls)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_file_from_server_no_data(self, mock_open, mock_get_unique, mock_validate, cursor_mock):
        """Test behavior when no data is returned."""

        mock_get_unique.return_value = "/path/to/unique_file.txt"
        # Set up fetch to return empty/null data immediately
        self._setup_fetch_behavior(cursor_mock, [None])

        Cursor._Cursor__get_file_from_server(cursor_mock)

        mock_get_unique.assert_called_once_with("/path/to/file.txt")
        mock_validate.assert_called_once_with("/path/to/unique_file.txt", 1024)
        mock_open.assert_called_once_with("/path/to/unique_file.txt", "wb")

        # File should be created but no data written
        file_handle = mock_open()
        assert file_handle.write.call_count == 0

        cursor_mock._Cursor__logger.debug.assert_any_call("Successfully read file from server to path: '/path/to/unique_file.txt'")

    @patch('builtins.open')
    def test_get_file_from_server_file_error(self, mock_open, mock_get_unique, mock_validate, cursor_mock):
        """Test error handling when file operations fail."""

        mock_get_unique.return_value = "/path/to/unique_file.txt"
        mock_open.side_effect = IOError("Disk full")

        with pytest.raises(Exception) as exc_info:
            Cursor._Cursor__get_file_from_server(cursor_mock)

        assert "Failed to save file on local disk" in str(exc_info.value)
        assert "Disk full" in str(exc_info.value)

        mock_get_unique.assert_called_once()
        mock_validate.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_get_file_from_server_large_chunks(self, mock_open, mock_get_unique, mock_validate, cursor_mock):
        """Test handling of multiple large data chunks."""

        mock_get_unique.return_value = "/path/to/unique_file.txt"

        # Create multiple chunks of binary data
        chunk_count = 5
        chunks = [b"X" * 1024 for _ in range(chunk_count)]
        chunks.append(None)  # end marker

        self._setup_fetch_behavior(cursor_mock, chunks)

        Cursor._Cursor__get_file_from_server(cursor_mock)

        # Verify file was written with the correct number of chunks
        file_handle = mock_open()
        assert file_handle.write.call_count == chunk_count

        # Each chunk should be 1024 bytes
        for i in range(chunk_count):
            file_handle.write.assert_any_call(b"X" * 1024)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_file_from_server_empty_chunks(self, mock_open, mock_get_unique, mock_validate, cursor_mock):
        """Test handling of empty data chunks."""

        mock_get_unique.return_value = "/path/to/unique_file.txt"

        # Create a very simple sequence - just one non-empty chunk
        data_chunks = [b"test_data", None]

        self._setup_fetch_behavior(cursor_mock, data_chunks)

        Cursor._Cursor__get_file_from_server(cursor_mock)

        # Check file writes
        file_handle = mock_open()
        print(f"Write calls: {file_handle.write.call_args_list}", file=sys.stderr)

        assert file_handle.write.call_count == 1
        file_handle.write.assert_called_once_with(b"test_data")

    @patch('builtins.open', new_callable=mock_open)
    def test_get_file_from_server_disk_space_error(self, mock_open, mock_get_unique, mock_validate, cursor_mock):
        """Test handling of insufficient disk space."""

        mock_get_unique.return_value = "/path/to/unique_file.txt"

        mock_validate.side_effect = RuntimeError("Not enough disk space")

        with pytest.raises(Error) as exc_info:
            Cursor._Cursor__get_file_from_server(cursor_mock)

        assert "Not enough disk space" in str(exc_info.value)

        # File should not be opened if validation fails
        mock_open.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_get_file_from_server_fetch_error(self, mock_open, mock_get_unique, cursor_mock):
        """Test handling of fetch errors."""

        mock_get_unique.return_value = "/path/to/unique_file.txt"

        cursor_mock._Cursor__fetch.side_effect = Exception("Network error")

        def mock_log_and_raise(exception_class, message):
            raise exception_class(message)

        cursor_mock._Cursor__logger.log_and_raise.side_effect = mock_log_and_raise

        with pytest.raises(Error) as exc_info:
            Cursor._Cursor__get_file_from_server(cursor_mock)

        assert "Failed to save file on local disk" in str(exc_info.value)
        assert "Network error" in str(exc_info.value)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_file_from_server_zero_file_size(self, mock_open, mock_get_unique, mock_validate, cursor_mock):
        """Test handling of zero file size."""

        # Set file size to 0
        cursor_mock._Cursor__query_type_out = {"getFileSize": 0}

        mock_get_unique.return_value = "/path/to/unique_file.txt"
        self._setup_fetch_behavior(cursor_mock, [None])

        Cursor._Cursor__get_file_from_server(cursor_mock)

        # Should still validate with zero size
        mock_validate.assert_called_once_with("/path/to/unique_file.txt", 0)
        mock_open.assert_called_once()
