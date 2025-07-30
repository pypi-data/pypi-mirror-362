import os
import pytest
import logging
import tempfile
import shutil
import time
from unittest.mock import patch
from pysqream.logger import ContextLogger, CustomFormatter
from pysqream.globals import DEFAULT_LOG_PATH


@pytest.fixture
def temp_log_dir():
    """
    Fixture to create and clean up a temporary directory for log files
    """

    test_dir = tempfile.mkdtemp()

    yield test_dir

    # Attempt to remove log files and directory with retry mechanism
    for attempt in range(3):
        try:
            logging.shutdown()
            time.sleep(0.5)
            shutil.rmtree(test_dir)
            break
        except PermissionError:
            time.sleep(1)
        except Exception as e:
            print(f"Error cleaning up temp directory: {e}")
            break


@pytest.fixture
def context_logger():
    """
    Fixture to create a fresh ContextLogger instance for each test
    """

    logger = ContextLogger()
    logger.stop_logging()

    yield logger

    logger.stop_logging()


class TestLogger:

    def test_start_logging_default_path(self, context_logger):
        """
        Test starting logging with default path
        """

        log = context_logger.start_logging(DEFAULT_LOG_PATH)

        assert log is not None
        assert not context_logger.logger.disabled
        assert len(context_logger.logger.handlers) == 1

    def test_start_logging_custom_path(self, context_logger, temp_log_dir):
        """
        Test starting logging with a custom log path
        """

        custom_log_path = os.path.join(temp_log_dir, 'custom_log.log')
        log = context_logger.start_logging(log_path=custom_log_path)

        assert log is not None
        assert not context_logger.logger.disabled
        assert os.path.exists(custom_log_path)

    def test_start_logging_invalid_path(self, context_logger):
        """
        Test that an invalid log path raises an exception
        """

        with patch("os.path.dirname", side_effect=PermissionError(13, 'Access is denied')):
            with pytest.raises(Exception, match="Bad log path was given"):
                context_logger.start_logging(log_path='/some/protected/path/logfile.log')

    def test_stop_logging(self, context_logger):
        """
        Test stopping logging
        """

        context_logger.start_logging(DEFAULT_LOG_PATH)
        context_logger.stop_logging()

        assert context_logger.logger.disabled
        assert len(context_logger.logger.handlers) == 0

    @pytest.mark.parametrize("config_level,log_method,should_appear", [
        # when configured at DEBUG level
        ('debug', 'debug', True),
        ('debug', 'info', True),
        ('debug', 'warning', True),
        ('debug', 'error', True),

        # when configured at INFO level
        ('info', 'debug', False),     # debug shouldn't appear in INFO level
        ('info', 'info', True),
        ('info', 'warning', True),
        ('info', 'error', True),

        # when configured at WARNING level
        ('warning', 'debug', False),  # debug shouldn't appear in WARNING level
        ('warning', 'info', False),   # info shouldn't appear in WARNING level
        ('warning', 'warning', True),
        ('warning', 'error', True),

        # when configured at ERROR level
        ('error', 'debug', False),    # debug shouldn't appear in ERROR level
        ('error', 'info', False),     # info shouldn't appear in ERROR level
        ('error', 'warning', False),  # warning shouldn't appear in ERROR level
        ('error', 'error', True),
    ])
    def test_log_level_filtering(self, context_logger, temp_log_dir, config_level, log_method, should_appear):
        """
        Test that log messages are properly filtered based on the configured log level.

        Parameters:
        - config_level: The level to configure the logger with
        - log_method: The logging method to call ('debug', 'info', etc.)
        - log_level: The numeric level of the log method
        - should_appear: Whether the message should appear in the log file
        """

        log_path = os.path.join(temp_log_dir, f'{config_level}_{log_method}_test.log')
        context_logger.start_logging(log_path, logging_level=config_level)
        method = getattr(context_logger, log_method)
        message = f"{log_method.upper()} test message"
        method(message, connection_id='test_conn', statement_id='test_stmt', source_object='TestClass')

        with open(log_path, 'r') as f:
            log_content = f.read()

        if should_appear:
            assert message in log_content
            assert 'test_conn' in log_content
            assert 'test_stmt' in log_content
            assert 'TestClass' in log_content
        else:
            assert message not in log_content

    def test_log_and_raise(self, context_logger, temp_log_dir):
        """
        Test log_and_raise method
        """

        log_path = os.path.join(temp_log_dir, 'raise_test.log')
        context_logger.start_logging(log_path)

        with pytest.raises(ValueError, match="Test error message"):
            context_logger.log_and_raise(
                ValueError,
                "Test error message",
                connection_id='test_conn',
                statement_id='test_stmt'
            )

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "Test error message" in log_content
        assert "test_conn" in log_content
        assert "test_stmt" in log_content

    def test_custom_formatter(self):
        """
        Test the CustomFormatter
        """

        formatter = CustomFormatter()

        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test_path',
            lineno=10,
            msg='Test message',
            args=(),
            exc_info=None
        )

        record.connection_id = 5
        record.statement_id = 100
        record.source_object = 'TestClass'

        formatted_message = formatter.format(record)

        assert '[TestClass]' in formatted_message
        assert '[Connection ID:5]' in formatted_message
        assert '[Statement ID:100]' in formatted_message
        assert 'Test message' in formatted_message

    def test_custom_formatter_connection_id_null(self):
        """
        Test the CustomFormatter
        """

        formatter = CustomFormatter()

        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test_path',
            lineno=10,
            msg='Test message',
            args=(),
            exc_info=None
        )

        record.connection_id = None
        record.statement_id = 100
        record.source_object = 'TestClass'

        formatted_message = formatter.format(record)

        assert '[TestClass]' in formatted_message
        assert '[Connection ID:' not in formatted_message
        assert '[Statement ID:100]' in formatted_message
        assert 'Test message' in formatted_message

    def test_custom_formatter_no_connection_id(self):
        """
        Test the CustomFormatter
        """

        formatter = CustomFormatter()

        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test_path',
            lineno=10,
            msg='Test message',
            args=(),
            exc_info=None
        )

        record.statement_id = 100
        record.source_object = 'TestClass'

        formatted_message = formatter.format(record)

        assert '[TestClass]' in formatted_message
        assert '[Connection ID:' not in formatted_message
        assert '[Statement ID:100]' in formatted_message
        assert 'Test message' in formatted_message

    def test_custom_formatter_statement_id_null(self):
        """
        Test the CustomFormatter
        """

        formatter = CustomFormatter()

        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test_path',
            lineno=10,
            msg='Test message',
            args=(),
            exc_info=None
        )

        record.connection_id = 5
        record.statement_id = None
        record.source_object = 'TestClass'

        formatted_message = formatter.format(record)

        assert '[TestClass]' in formatted_message
        assert '[Connection ID:5]' in formatted_message
        assert '[Statement ID:' not in formatted_message
        assert 'Test message' in formatted_message

    def test_custom_formatter_no_statement_id(self):
        """
        Test the CustomFormatter
        """

        formatter = CustomFormatter()

        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test_path',
            lineno=10,
            msg='Test message',
            args=(),
            exc_info=None
        )

        record.connection_id = 5
        record.source_object = 'TestClass'

        formatted_message = formatter.format(record)

        assert '[TestClass]' in formatted_message
        assert '[Connection ID:5]' in formatted_message
        assert '[Statement ID:' not in formatted_message
        assert 'Test message' in formatted_message

    def test_start_logging_twice_different_levels(self, context_logger, temp_log_dir):
        """
        Test behavior when start_logging is called twice on the same file with different logging levels.

        This test checks if the second call to start_logging with a different level properly
        changes the logging level for the same file.
        """

        log_path = os.path.join(temp_log_dir, 'multiple_levels.log')

        context_logger.start_logging(log_path, logging_level='debug')

        context_logger.debug("Debug message 1", source_object='TestClass')
        context_logger.info("Info message 1", source_object='TestClass')

        context_logger.start_logging(log_path, logging_level='warning')

        context_logger.debug("Debug message 2", source_object='TestClass')  # Should not appear
        context_logger.info("Info message 2", source_object='TestClass')    # Should not appear
        context_logger.warning("Warning message", source_object='TestClass')  # Should appear
        context_logger.error("Error message", source_object='TestClass')      # Should appear

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "Debug message 1" in log_content
        assert "Info message 1" in log_content

        assert "Debug message 2" not in log_content  # Should be filtered out by WARNING level
        assert "Info message 2" not in log_content   # Should be filtered out by WARNING level
        assert "Warning message" in log_content
        assert "Error message" in log_content

    def test_logger_is_enabled_for_correct_levels(self, context_logger):
        """
        Test that isEnabledFor returns correct values based on configured level.
        This test will fail if self.logger.setLevel() is not called in start_logging.
        """

        # Initially logger is disabled, so isEnabledFor should return False for all levels
        assert context_logger.logger.isEnabledFor(logging.DEBUG) is False
        assert context_logger.logger.isEnabledFor(logging.INFO) is False
        assert context_logger.logger.isEnabledFor(logging.WARNING) is False
        assert context_logger.logger.isEnabledFor(logging.ERROR) is False

        # After start_logging with DEBUG, all levels should be enabled
        context_logger.start_logging(DEFAULT_LOG_PATH, logging_level='debug')
        assert context_logger.logger.isEnabledFor(logging.DEBUG) is True
        assert context_logger.logger.isEnabledFor(logging.INFO) is True
        assert context_logger.logger.isEnabledFor(logging.WARNING) is True
        assert context_logger.logger.isEnabledFor(logging.ERROR) is True

        # After start_logging with ERROR, only ERROR and above should be enabled
        context_logger.start_logging(DEFAULT_LOG_PATH, logging_level='error')
        assert context_logger.logger.isEnabledFor(logging.DEBUG) is False
        assert context_logger.logger.isEnabledFor(logging.INFO) is False
        assert context_logger.logger.isEnabledFor(logging.WARNING) is False
        assert context_logger.logger.isEnabledFor(logging.ERROR) is True
