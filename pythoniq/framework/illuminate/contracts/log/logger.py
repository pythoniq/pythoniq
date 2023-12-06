"""
/**
 * Describes a logger instance.
 *
 * The message MUST be a string or object implementing __toString().
 *
 * The message MAY contain placeholders in the form: {foo} where foo
 * will be replaced by the context data in key "foo".
 *
 * The context array can contain arbitrary data. The only assumption that
 * can be made by implementors is that if an Exception instance is given
 * to produce a stack trace, it MUST be in a key named "exception".
 *
 * See https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-3-logger-interface.md
 * for the full interface specification.
 */
"""
class Logger:
    # System is unusable.
    def emergency(self, message: str, context: dict) -> None:
        pass

    # Action must be taken immediately.
    # Example: Entire website down, database unavailable, etc. This should trigger the SMS alerts and wake you up.
    def alert(self, message: str, context: dict) -> None:
        pass

    # Critical conditions.
    # Example: Application component unavailable, unexpected exception.
    def critical(self, message: str, context: dict) -> None:
        pass

    # Runtime errors that do not require immediate action but should typically be logged and monitored.
    def error(self, message: str, context: dict) -> None:
        pass

    # Exceptional occurrences that are not errors.
    # Example: Use of deprecated APIs, poor use of an API, undesirable things that are not necessarily wrong.
    def warning(self, message: str, context: dict) -> None:
        pass

    # Normal but significant events.
    def notice(self, message: str, context: dict) -> None:
        pass

    # Interesting events.
    # Example: User logs in, SQL logs.
    def info(self, message: str, context: dict) -> None:
        pass

    #  Detailed debug information.
    def debug(self, message: str, context: dict) -> None:
        pass

    # Logs with an arbitrary level.
    def log(self, level: any, message: list | dict | str, context: dict = {}) -> None:
        pass
