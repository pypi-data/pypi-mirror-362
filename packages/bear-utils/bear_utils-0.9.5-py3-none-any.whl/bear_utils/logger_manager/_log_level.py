from typing import Literal

from bear_utils.constants._meta import IntValue as Value, RichIntEnum

FAILURE: Literal[45] = 45
ERROR: Literal[40] = 40
WARNING: Literal[30] = 30
WARN: Literal[30] = WARNING
INFO: Literal[20] = 20
SUCCESS: Literal[15] = 15
DEBUG: Literal[10] = 10
VERBOSE: Literal[5] = 5
NOTSET: Literal[0] = 0


class LogLevel(RichIntEnum):
    """Enumeration for logging levels."""

    NOTSET = Value(NOTSET, "NOTSET", default=NOTSET)
    VERBOSE = Value(VERBOSE, "VERBOSE", default=VERBOSE)
    DEBUG = Value(DEBUG, "DEBUG", default=DEBUG)
    INFO = Value(INFO, "INFO", default=INFO)
    WARNING = Value(WARNING, "WARNING", default=WARNING)
    ERROR = Value(ERROR, "ERROR", default=ERROR)
    FAILURE = Value(FAILURE, "FAILURE", default=FAILURE)
    SUCCESS = Value(SUCCESS, "SUCCESS", default=SUCCESS)


level_to_name = {
    FAILURE: "FAILURE",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    SUCCESS: "SUCCESS",
    DEBUG: "DEBUG",
    VERBOSE: "VERBOSE",
    NOTSET: "NOTSET",
}

name_to_level = {
    "FAILURE": FAILURE,
    "ERROR": ERROR,
    "WARN": WARNING,
    "WARNING": WARNING,
    "INFO": INFO,
    "SUCCESS": SUCCESS,
    "DEBUG": DEBUG,
    "VERBOSE": VERBOSE,
    "NOTSET": NOTSET,
}
