import logging
import os
import sys

# TODO LOGGER_MINIMAL_SEVERITY_DEFAULT
LOGGER_MINIMUM_SEVERITY = os.getenv("LOGGER_MINIMUM_SEVERITY", "INFO").upper()
# logging expects NOTSET/DEBUG/INFO/WARNING/ERROR/FATAL/CRITICAL
if LOGGER_MINIMUM_SEVERITY.isdigit():
    # TODO logger_minimal_severity_default_value
    logger_minimum_severity = int(LOGGER_MINIMUM_SEVERITY)
    # TODO Change Magic Numbers and use the values from Logger.MessageSeverity
    if logger_minimum_severity < 400:
        # TODO LOGGER_MINIMAL_SEVERITY_DEFAULT_NAME =
        # TODO Change "DEBUG", "INFO", "WARNING" ... into enum values from Logger.MessageSeverity
        LOGGER_MINIMUM_SEVERITY = "DEBUG"
    elif logger_minimum_severity < 600:
        LOGGER_MINIMUM_SEVERITY = "INFO"
    elif logger_minimum_severity < 700:
        LOGGER_MINIMUM_SEVERITY = "WARNING"
    elif logger_minimum_severity < 800:
        LOGGER_MINIMUM_SEVERITY = "ERROR"
    else:
        LOGGER_MINIMUM_SEVERITY = "CRITICAL"

logging.basicConfig(level=LOGGER_MINIMUM_SEVERITY, stream=sys.stdout,
                    format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class MiniLogger:
    # TODO Can we have one generic function called by all as we have a lot of duplicated code here?

    # TODO: print the caller function name

    @staticmethod
    def start(message: str = "", object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        if object is None:
            logger.debug(f"START - {message}")
        else:
            logger.debug(f"START - {message} - {object}")

    @staticmethod
    def end(message: str = "", object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
        """
        if object is None:
            logger.debug(f"END - {message}")
        else:
            logger.debug(f"END - {message} - {object}")

    # TODO convert all those methods (debug, info, warning, error) into one unified private method
    # TODO Add to the unified private method print of the name of method, version and line number of the calling function/method to the mini_logger methods  # noqa: E501
    @staticmethod
    def debug(message: str = "", object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        if object is None:
            logger.debug(f"DEBUG - {message}")
        else:
            logger.debug(f"DEBUG {message} - {object}")

    @staticmethod
    def info(message: str = "", object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        if object is None:
            logger.info(f"INFO - {message}")
        else:
            logger.info(f"INFO {message} - {object}")

    @staticmethod
    def warning(message: str = "", object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        # TODO Add the source of the message - We should add the object or atleast some parts of it
        if object is None:
            logger.warning(f"WARNING - {message}")
        else:
            logger.warning(f"WARNING {message} - {object}")

    @staticmethod
    def error(message: str = "", object: dict = None):
        """
        Print a log error message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        if object is None:
            logger.error(f"ERROR - {message}")
        else:
            logger.error(f"ERROR - {message} - {object}")

    @staticmethod
    def exception(message: str = "", object: Exception or dict = None):
        """
        Print a log error message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict / Exception): The object / Exception to be printed.
        """
        if isinstance(object, Exception):
            exception = object
        elif isinstance(object, dict):
            exception = object.get("exception")
        else:
            exception = None

        if object is None:
            logger.exception(f"EXCEPTION - {message}")
        else:
            logger.exception(f"EXCEPTION- {message} - {object}", exc_info=exception)
