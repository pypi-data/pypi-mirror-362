import os
import pytest
from unittest.mock import patch
from pysqream.utils import validate_file_size


class TestFileValidation:
    """
    Tests for validate_file_size function
    """

    def test_file_under_limit(self, tmp_path):
        """
        Test that a file under the size limit passes validation
        """

        test_file = tmp_path / "small_file.txt"
        test_file.write_text("This is a small test file")

        validate_file_size(str(test_file), 1)  # 1MB limit, should not raise any exception

    def test_file_over_limit(self, tmp_path):
        """
        Test that a file over the size limit raises RuntimeError
        """

        test_file = tmp_path / "big_file.bin"

        # Write just enough data to exceed the small limit (0.01MB = ~10KB)
        with open(test_file, 'wb') as f:
            f.write(b'0' * 15_000)  # writing 15KB of data

        with pytest.raises(RuntimeError) as excinfo:
            validate_file_size(str(test_file), 0.01)  # 0.01MB limit

        assert "File size exceeds the allowed limit of 0.01 MB" in str(excinfo.value)

    def test_file_exactly_at_limit(self, tmp_path):
        """
        Test a file exactly at the size limit passes validation
        """

        test_file = tmp_path / "exact_file.bin"

        with open(test_file, 'wb') as f:
            f.write(b'0' * 104_858)

        precise_limit = os.path.getsize(str(test_file))

        validate_file_size(str(test_file), precise_limit)

    def test_nonexistent_file(self):
        """
        Test that a non-existent file raises FileNotFoundError
        """

        non_existent_file = "/path/to/nonexistent/file.txt"

        with pytest.raises(FileNotFoundError):
            validate_file_size(non_existent_file, 10)

    def test_zero_size_file(self, tmp_path):
        """
        Test validation with an empty file. should pass with any limit.
        """

        empty_file = tmp_path / "empty.txt"
        empty_file.touch()

        validate_file_size(str(empty_file), 0.1)
        validate_file_size(str(empty_file), 0)

    def test_zero_limit(self, tmp_path):
        """
        Test validation with zero limit
        """

        test_file = tmp_path / "minimal.txt"
        test_file.write_text("Just a few bytes")

        with pytest.raises(RuntimeError) as excinfo:
            validate_file_size(str(test_file), 0)

        assert "File size exceeds the allowed limit of 0 MB" in str(excinfo.value)

    @patch('os.path.getsize')
    def test_large_file_mocked(self, mock_getsize):
        """
        Test with a mocked very large file (avoiding actual large file creation)
        """

        # Mock a 100 MB file
        mock_getsize.return_value = 104_857_600  # 100 MB in bytes

        # Test with 50 MB limit (should fail)
        with pytest.raises(RuntimeError) as excinfo:
            validate_file_size("mock_large_file.bin", 50)

        assert "File size exceeds the allowed limit of 50 MB" in str(excinfo.value)

        # Test with 200 MB limit (should pass)
        validate_file_size("mock_large_file.bin", 200)

    def test_negative_limit(self, tmp_path):
        """
        Test validation with negative limit (should raise ValueError)
        """

        test_file = tmp_path / "test.txt"
        test_file.write_text("Some content")

        # A negative limit doesn't make logical sense, but we should test how the function handles it
        # Expect it to treat negative limits as "exceeded" since any file size is greater than a negative number
        with pytest.raises(RuntimeError):
            validate_file_size(str(test_file), -1)
