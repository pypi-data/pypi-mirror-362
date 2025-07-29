from logging import Logger

from bear_utils.logger_manager._log_level import FAILURE, SUCCESS, VERBOSE


class LoggerExtra(Logger):
    """A custom logger that just includes a few extra methods."""

    def verbose(self, msg: object, *args, **kwargs) -> None:
        """Log a verbose message."""
        self.log(VERBOSE, msg, *args, **kwargs)

    def success(self, msg: object, *args, **kwargs) -> None:
        """Log a success message."""
        self.log(SUCCESS, msg, *args, **kwargs)

    def failure(self, msg: object, *args, **kwargs) -> None:
        """Log a failure message."""
        self.log(FAILURE, msg, *args, **kwargs)
