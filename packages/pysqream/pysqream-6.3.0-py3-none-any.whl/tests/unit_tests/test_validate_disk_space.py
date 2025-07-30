import shutil
import pytest
from collections import namedtuple
from pysqream.utils import validate_disk_space

DiskUsage = namedtuple("usage", ["total", "used", "free"])


class TestValidateDiskSpace:

    def test_valid_path_enough_space(self, tmp_path, monkeypatch):
        file_path = tmp_path / "file.txt"
        required_size = 100
        monkeypatch.setattr(shutil, "disk_usage", lambda p: DiskUsage(total=1000, used=100, free=900))

        validate_disk_space(str(file_path), required_size)  # Should not raise

    def test_valid_path_not_enough_space(self, tmp_path, monkeypatch):
        file_path = tmp_path / "file.txt"
        required_size = 1000
        monkeypatch.setattr(shutil, "disk_usage", lambda p: DiskUsage(total=1000, used=900, free=50))

        with pytest.raises(RuntimeError, match="Not enough disk space"):
            validate_disk_space(str(file_path), required_size)

    def test_directory_does_not_exist(self, tmp_path):
        non_existent_dir = tmp_path / "nonexistent"
        file_path = non_existent_dir / "file.txt"

        with pytest.raises(FileNotFoundError, match="Directory '.*' does not exist"):
            validate_disk_space(str(file_path), 100)

    def test_file_in_current_directory(self, monkeypatch):
        current_dir_file = "somefile.txt"
        required_size = 50
        monkeypatch.setattr(shutil, "disk_usage", lambda p: DiskUsage(total=1000, used=100, free=900))

        validate_disk_space(current_dir_file, required_size)  # Should not raise
