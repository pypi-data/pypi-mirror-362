import pytest
from pysqream.cursor import Cursor, BYTES_PER_FLUSH_LIMIT, Error
from unittest.mock import patch, MagicMock, mock_open


@patch('pysqream.cursor.validate_file_size')
@patch('builtins.open', new_callable=mock_open)
class TestPutFileToServer:
    """
    Test cases for the cursor.__put_file_to_server method
    """

    @pytest.fixture
    def cursor_mock(self):
        """
        Create a mocked cursor object with necessary attributes
        """

        cursor = MagicMock()
        cursor._Cursor__prepare_params = {"local_file_read": "/path/to/source.txt",
                                          "staging_area_file_limit_mb": 100}
        cursor._Cursor__client = MagicMock()
        cursor._Cursor__logger = MagicMock()

        def mock_log_and_raise(exception_class, message):
            raise exception_class(message)

        cursor._Cursor__logger.log_and_raise.side_effect = mock_log_and_raise

        return cursor

    def test_put_file_to_server_basic(self, mock_open, mock_validate, cursor_mock):
        """
        Test basic file upload functionality with a single chunk
        """

        mock_file = mock_open.return_value
        mock_file.read.side_effect = [b"test data", b""]

        Cursor._Cursor__put_file_to_server(cursor_mock)

        mock_validate.assert_called_once_with(
            "/path/to/source.txt",
            cursor_mock._Cursor__prepare_params["staging_area_file_limit_mb"]
        )

        # Check file was opened correctly
        mock_open.assert_called_once_with("/path/to/source.txt", "rb")

        # Check file was read with correct chunk size
        mock_file.read.assert_any_call(BYTES_PER_FLUSH_LIMIT)

        # Check data was sent to the server
        cursor_mock._Cursor__client.send_data.assert_any_call(1, [b"test data"], len(b"test data"))

        # Check empty data was sent to signal end of file
        cursor_mock._Cursor__client.send_data.assert_any_call(0, [], 0)

        # Check correct logs were written
        cursor_mock._Cursor__logger.debug.assert_any_call("Sending local file: '/path/to/source.txt' to server")
        cursor_mock._Cursor__logger.debug.assert_any_call("File '/path/to/source.txt' sent successfully.")

    def test_put_file_to_server_multiple_chunks(self, mock_open, mock_validate, cursor_mock):
        """
        Test uploading a file with multiple chunks
        """

        # Create chunks slightly smaller than the read size to ensure multiple reads
        chunk1 = b"X" * 1024
        chunk2 = b"Y" * 1024
        chunk3 = b"Z" * 512

        mock_file = mock_open.return_value
        mock_file.read.side_effect = [chunk1, chunk2, chunk3, b""]

        Cursor._Cursor__put_file_to_server(cursor_mock)

        mock_validate.assert_called_once()

        # Check the correct number of send_data calls were made
        assert cursor_mock._Cursor__client.send_data.call_count == 4  # 3 data chunks + 1 end signal

        # Verify each chunk was sent correctly
        cursor_mock._Cursor__client.send_data.assert_any_call(1, [chunk1], len(chunk1))
        cursor_mock._Cursor__client.send_data.assert_any_call(1, [chunk2], len(chunk2))
        cursor_mock._Cursor__client.send_data.assert_any_call(1, [chunk3], len(chunk3))
        cursor_mock._Cursor__client.send_data.assert_any_call(0, [], 0)

    def test_put_file_to_server_empty_file(self, mock_open, mock_validate, cursor_mock):
        """
        Test uploading an empty file
        """

        # Simulate an empty file
        mock_file = mock_open.return_value
        mock_file.read.return_value = b""

        Cursor._Cursor__put_file_to_server(cursor_mock)

        mock_validate.assert_called_once()

        # Check file was opened
        mock_open.assert_called_once_with("/path/to/source.txt", "rb")

        # Should only have one send_data call for the end signal
        assert cursor_mock._Cursor__client.send_data.call_count == 1
        cursor_mock._Cursor__client.send_data.assert_called_once_with(0, [], 0)

        # Success log should still be written
        cursor_mock._Cursor__logger.debug.assert_any_call("File '/path/to/source.txt' sent successfully.")

    def test_put_file_to_server_file_not_found(self, mock_open, mock_validate, cursor_mock):
        """
        Test handling of file not found error
        """

        # Simulate file not found
        mock_open.side_effect = FileNotFoundError("File not found")

        with pytest.raises(Error):
            Cursor._Cursor__put_file_to_server(cursor_mock)

        mock_validate.assert_called()

        # Ensure proper error was logged
        cursor_mock._Cursor__logger.log_and_raise.assert_called_once()
        args = cursor_mock._Cursor__logger.log_and_raise.call_args[0]
        assert args[0] == Error
        assert "File '/path/to/source.txt' not found" in args[1]

        # No data should be sent
        cursor_mock._Cursor__client.send_data.assert_not_called()

    def test_put_file_to_server_io_error(self, mock_open, mock_validate, cursor_mock):
        """
        Test handling of general IO errors during reading
        """

        # Open succeeds but read fails
        mock_file = mock_open.return_value
        mock_file.read.side_effect = IOError("Disk read error")

        with pytest.raises(Error):
            Cursor._Cursor__put_file_to_server(cursor_mock)

        mock_validate.assert_called_once()

        # Ensure proper error was logged
        cursor_mock._Cursor__logger.log_and_raise.assert_called_once()
        args = cursor_mock._Cursor__logger.log_and_raise.call_args[0]
        assert args[0] == Error
        assert "Error sending file" in args[1]
        assert "Disk read error" in args[1]

    def test_put_file_to_server_send_error(self, mock_open, mock_validate, cursor_mock):
        """
        Test handling of errors when sending data to server
        """

        mock_file = mock_open.return_value
        mock_file.read.return_value = b"test data"

        # Make send_data raise an exception
        cursor_mock._Cursor__client.send_data.side_effect = Exception("Network error")

        with pytest.raises(Error):
            Cursor._Cursor__put_file_to_server(cursor_mock)

        mock_validate.assert_called_once()

        # Ensure proper error was logged
        cursor_mock._Cursor__logger.log_and_raise.assert_called_once()
        args = cursor_mock._Cursor__logger.log_and_raise.call_args[0]
        assert args[0] == Error
        assert "Error sending file" in args[1]
        assert "Network error" in args[1]

    def test_put_file_to_server_exact_chunk_size(self, mock_open, mock_validate, cursor_mock):
        """
        Test behavior when file size is exactly a multiple of the chunk size
        """

        # Create data that's exactly one chunk size
        chunk = b"X" * BYTES_PER_FLUSH_LIMIT

        mock_file = mock_open.return_value
        mock_file.read.side_effect = [chunk, b""]

        Cursor._Cursor__put_file_to_server(cursor_mock)

        mock_validate.assert_called_once()

        # Should have two calls: one for data and one for end signal
        assert cursor_mock._Cursor__client.send_data.call_count == 2
        cursor_mock._Cursor__client.send_data.assert_any_call(1, [chunk], len(chunk))
        cursor_mock._Cursor__client.send_data.assert_any_call(0, [], 0)

    def test_file_size_validation_error(self, mock_open, mock_validate, cursor_mock):
        """
        Test handling when validate_file_size raises an exception
        """

        mock_validate.side_effect = RuntimeError("File size exceeds the allowed limit of 100 MB. Actual size: 150.42 MB.")

        with pytest.raises(Error):
            Cursor._Cursor__put_file_to_server(cursor_mock)

        mock_validate.assert_called_once()

        mock_open.assert_not_called()

        cursor_mock._Cursor__logger.log_and_raise.assert_called_once()
        args = cursor_mock._Cursor__logger.log_and_raise.call_args[0]
        assert args[0] == Error
        assert "Error sending file" in args[1]
        assert "File size exceeds the allowed limit" in args[1]

    def test_custom_file_size_limit(self, mock_open, mock_validate, cursor_mock):
        """
        Test with a custom file size limit
        """

        cursor_mock._Cursor__prepare_params["staging_area_file_limit_mb"] = 50

        mock_file = mock_open.return_value
        mock_file.read.side_effect = [b"test data", b""]

        Cursor._Cursor__put_file_to_server(cursor_mock)

        # Check validate_file_size was called with the custom limit
        mock_validate.assert_called_once_with("/path/to/source.txt", 50)

        # Verify the debug log contains the correct limit
        cursor_mock._Cursor__logger.debug.assert_any_call("Checking file size does not exceed allowed file limit mb: 50")

    def test_zero_file_size_limit(self, mock_open, mock_validate, cursor_mock):
        """
        Test with a zero file size limit (should only allow empty files)
        """

        cursor_mock._Cursor__prepare_params["staging_area_file_limit_mb"] = 0

        mock_file = mock_open.return_value
        mock_file.read.side_effect = [b"test data", b""]

        Cursor._Cursor__put_file_to_server(cursor_mock)

        # Check validate_file_size was called with zero limit
        mock_validate.assert_called_once_with("/path/to/source.txt", 0)

        # The rest of the process should continue as normal if validation passes
        assert cursor_mock._Cursor__client.send_data.call_count == 2
