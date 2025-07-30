import os
import shutil
import pytest
import tempfile
from unittest.mock import patch
from pysqream.utils import get_unique_filename


class TestGetUniqueFilename:
    """
    Test cases for the get_unique_filename utility function
    """

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Create a temporary directory for testing
        """

        self.temp_dir = tempfile.mkdtemp()
        yield

        shutil.rmtree(self.temp_dir)

    def test_nonexistent_file_returns_original_path(self):
        """
        Test that the original path is returned if the file doesn't exist
        """

        test_path = os.path.join(self.temp_dir, "nonexistent.txt")

        assert get_unique_filename(test_path) == test_path

    def test_existing_file_returns_incremented_path(self):
        """
        Test that a path with (1) is returned if the original file exists
        """

        test_path = os.path.join(self.temp_dir, "existing.txt")

        with open(test_path, 'w') as f:
            f.write("test")

        expected_path = os.path.join(self.temp_dir, "existing (1).txt")

        assert get_unique_filename(test_path) == expected_path

    def test_multiple_existing_files_return_correct_increment(self):
        """
        Test that the correct increment is used when multiple files exist
        """

        base_path = os.path.join(self.temp_dir, "multiple.txt")
        path_1 = os.path.join(self.temp_dir, "multiple (1).txt")
        path_2 = os.path.join(self.temp_dir, "multiple (2).txt")

        for path in [base_path, path_1, path_2]:
            with open(path, 'w') as f:
                f.write("test")

        expected_path = os.path.join(self.temp_dir, "multiple (3).txt")

        assert get_unique_filename(base_path) == expected_path

    def test_multiple_existing_files_except_first_return_correct_increment(self):
        """
        Test that the correct increment is used when multiple files exist but not the first.
        Then check that incrementation continues from latest
        """

        base_path = os.path.join(self.temp_dir, "multiple.txt")
        path_1 = os.path.join(self.temp_dir, "multiple (1).txt")
        path_2 = os.path.join(self.temp_dir, "multiple (2).txt")

        for path in [path_1, path_2]:
            with open(path, 'w') as f:
                f.write("test")

        expected_path = os.path.join(self.temp_dir, "multiple.txt")

        assert get_unique_filename(base_path) == expected_path

        expected_path = os.path.join(self.temp_dir, "multiple (3).txt")

        with open(base_path, 'w') as f:
            f.write("test")

        assert get_unique_filename(base_path) == expected_path

    def test_already_incremented_filename(self):
        """
        Test that a filename already containing an increment is handled correctly
        """

        base_path = os.path.join(self.temp_dir, "incremented (1).txt")

        with open(base_path, 'w') as f:
            f.write("test")

        expected_path = os.path.join(self.temp_dir, "incremented (2).txt")

        assert get_unique_filename(base_path) == expected_path

    def test_path_with_no_extension(self):
        """
        Test that files without extensions are handled correctly
        """

        test_path = os.path.join(self.temp_dir, "noextension")

        with open(test_path, 'w') as f:
            f.write("test")

        expected_path = os.path.join(self.temp_dir, "noextension (1)")

        assert get_unique_filename(test_path) == expected_path

    def test_path_with_dots_in_filename(self):
        """
        Test that files with multiple dots in the name are handled correctly
        """

        test_path = os.path.join(self.temp_dir, "file.name.with.dots.txt")

        with open(test_path, 'w') as f:
            f.write("test")

        expected_path = os.path.join(self.temp_dir, "file.name.with.dots (1).txt")

        assert get_unique_filename(test_path) == expected_path

    def test_many_existing_files(self):
        """
        Test with many existing files to ensure performance is reasonable
        """

        test_path = os.path.join(self.temp_dir, "manyfiles.txt")

        # Use patch to mock os.path.exists
        with patch('os.path.exists') as mock_exists:
            # Mock exists to return True for the first 100 attempts, then False
            mock_exists.side_effect = lambda path: '(100)' not in path

            expected_path = os.path.join(self.temp_dir, "manyfiles (100).txt")
            assert get_unique_filename(test_path) == expected_path
