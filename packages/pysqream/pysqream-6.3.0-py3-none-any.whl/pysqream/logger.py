import os
import inspect
import logging
import logging.handlers
import uuid


class CustomFormatter(logging.Formatter):
    """
    Custom log formatter that conditionally displays connection and statement IDs
    and includes the source of the log message
    """

    def __init__(self, fmt="%(asctime)s - %(name)s - %(levelname)s - %(context)s%(message)s"):
        super().__init__(fmt)

    def format(self, record):
        context = []

        if hasattr(record, "source_object") and record.source_object:
            context.append(f"[{record.source_object}]")

        if hasattr(record, "connection_id") and record.connection_id:
            context.append(f"[Connection ID:{record.connection_id}]")

        if hasattr(record, "statement_id") and record.statement_id:
            context.append(f"[Statement ID:{record.statement_id}]")

        record.context = ' '.join(context) + ' ' if context else ''

        return super().format(record)


class ContextLogger:
    """
    Enhanced logger with context tracking for connections and statements
    """

    def __init__(self):
        self.logger = logging.getLogger(f"pysqream_logger.{str(uuid.uuid4())[:8]}")
        self.logger.disabled = True
        self.logger.propagate = False

    def start_logging(self, log_path: str, max_backup_count: int = 50, when: str = "midnight", logging_level: str = "INFO"):
        """
        Start logging with timed rotating file handler
        """

        try:
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            handler = logging.handlers.TimedRotatingFileHandler(filename=log_path, when=when, interval=1,
                                                                backupCount=max_backup_count, encoding="utf-8", delay=False)
        except Exception as e:
            raise Exception(f"Bad log path was given '{log_path}', please verify path is valid and no forbidden characters were used. Error: {e}")

        self.logger.setLevel(logging_level.upper())
        handler.setLevel(logging_level.upper())
        handler.setFormatter(CustomFormatter())

        self.logger.handlers.clear()
        self.logger.addHandler(handler)
        self.logger.disabled = False

        return self.logger

    def stop_logging(self):
        """
        Iterates over a copy of handlers while modifying original list and closing each handler.
        Stop logging and remove all handlers
        """

        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        self.logger.handlers.clear()
        self.logger.disabled = True

    def _get_caller_info(self):
        """
        Retrieve caller information by traversing the call stack.
        Skipping frames within ContextLogger (current object).
        Trying to retrieve class name, if class name is not found then trying module name
        """

        frame = inspect.currentframe()
        try:
            while frame:
                frame = frame.f_back
                if not frame:
                    break

                if frame.f_locals.get("self") and frame.f_locals["self"].__class__.__name__ == type(self).__name__:
                    continue

                locals_dict = frame.f_locals
                if "self" in locals_dict:
                    return locals_dict["self"].__class__.__name__

                module_name = frame.f_globals.get("__name__", '')
                if module_name:
                    return module_name
        except Exception:
            pass

        return "Unknown"

    def _log_with_context(self, level, msg_or_callable, connection_id=None, statement_id=None, source_object=None):
        """
        Log a message with optional connection and statement ids and source object context
        Supports lazy evaluation through callables
        """

        if not self.logger.isEnabledFor(level):
            return

        msg = msg_or_callable() if callable(msg_or_callable) else msg_or_callable

        if source_object is None:
            source_object = self._get_caller_info()

        extra = {
            "connection_id": connection_id or None,
            "statement_id": statement_id or None,
            "source_object": source_object or None
        }

        self.logger.log(level, msg, extra=extra)

    def debug(self, msg_or_callable, connection_id=None, statement_id=None, source_object=None):
        """
        Debug level logging
        """

        self._log_with_context(logging.DEBUG, msg_or_callable, connection_id=connection_id, statement_id=statement_id, source_object=source_object)

    def info(self, msg_or_callable, connection_id=None, statement_id=None, source_object=None):
        """
        Info level logging
        """

        self._log_with_context(logging.INFO, msg_or_callable, connection_id=connection_id, statement_id=statement_id, source_object=source_object)

    def warning(self, msg_or_callable, connection_id=None, statement_id=None, source_object=None):
        """
        Warning level logging
        """

        self._log_with_context(logging.WARNING, msg_or_callable, connection_id=connection_id, statement_id=statement_id, source_object=source_object)

    def error(self, msg_or_callable, connection_id=None, statement_id=None, source_object=None):
        """
        Error level logging
        """

        self._log_with_context(logging.ERROR, msg_or_callable, connection_id=connection_id, statement_id=statement_id, source_object=source_object)

    def log_and_raise(self, exception_type, error_msg, connection_id=None, statement_id=None, source_object=None):
        """
        Log an error and raise an exception with optional context
        """

        self._log_with_context(logging.ERROR, error_msg, connection_id=connection_id, statement_id=statement_id, source_object=source_object)
        raise exception_type(error_msg)
