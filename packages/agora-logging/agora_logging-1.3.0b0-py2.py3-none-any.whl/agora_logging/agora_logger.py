import sys
from functools import wraps
from inspect import currentframe, getframeinfo

from .handlers.stream_handler import StreamHandler
from .log_level import LogLevel


def log_message(log_function):
    """
    Decorator that wraps context of the file and cast the message to str
    """
    @wraps(log_function)
    def wrapper(self, message):
        log_function(self, str(message))
    return wrapper


class AgoraLogger():
    """
    Logger class 

    Returns:
        logger object: Singleton logger object
    """
    loggers = []

    def __init__(self, level=None):
        self.name = "root"
        self.level = LogLevel.INFO if level is None else level
        self.log_coloring = True
        self.handler = StreamHandler(self.level)

    def __str__(self):
        return f'''AgoraLogger<{self.name}>'''

    @classmethod
    def get_logger(cls):
        """
        Get the singleton logger
        """
        return cls.add_logger()

    @classmethod
    def add_logger(cls):
        """
        Adds a new logger if it does not exist

        Returns:
            singleton logger
        """
        if len(cls.loggers) >= 1:
            return cls.loggers[0]
        new_logger = AgoraLogger()
        cls.loggers.append(new_logger)
        return new_logger

    def set_log_coloring(self, log_coloring):
        if isinstance(log_coloring, str):
            log_coloring = bool(log_coloring)
        if log_coloring is None:
            log_coloring = True
        else:            
            self.log_coloring = log_coloring            


    def set_level(self, level):
        """
        Set the LogLevel of the logger

        Args:
            level (str|instance of loglevel): sets the LogLevel
        """
        if level == "":
            return
        if isinstance(level, str):
            level = LogLevel.from_string(level)
        if level is None:
            self.write(LogLevel.ERROR, "Invalid value for verbosity")
        else:
            self.level = level
            self.handler.level = level
            

    def write_log(self, frame_info, log, level):
        self.handler.write(sys.stdout, frame_info, log, level, self.log_coloring)

    def write_exception_log(self, exception_message):
        self.handler.write_to_stream(exception_message, sys.stdout)
        sys.stdout.flush()

    def write(self, level: LogLevel, message):
        message = str(message)
        frameinfo = getframeinfo(currentframe().f_back)
        self.write_log(frameinfo, message, level)

    def exception(self, ex: Exception, message, level:LogLevel = LogLevel.WARN):
        message = str(message)
        frameinfo = getframeinfo(currentframe().f_back)
        self.write_log(frameinfo, message, level)
        self.write_exception_log(str(ex)+"\n")

    def write_unhandled_exception(self, ex: Exception, message, frameinfo):
        if not isinstance(message, str):
            self.write(
                LogLevel.ERROR, f'''Expected an instance of 'str', received {type(message)}''')
            return 0
        self.write_log(frameinfo, message, LogLevel.WARN)
        if self.level != LogLevel.OFF:
            self.write_exception_log(str(ex)+"\n")

    @log_message
    def heading(self, message):
        """
        Writes a heading message to the log

        Args:
            message (str): the message
        """
        message = str(message)
        frameinfo = getframeinfo(currentframe().f_back)
        self.handler.heading(frameinfo, message)

    @log_message
    def trace(self, message):
        """
        Writes a trace (LogLevel.TRACE) message to the log

        Args:
            message (str): the message
        """
        frameinfo = getframeinfo(currentframe().f_back.f_back)
        self.write_log(frameinfo, message, LogLevel.TRACE)

    @log_message
    def debug(self, message):
        """
        Writes a debug (LogLevel.DEBUG) message to the log

        Args:
            message (str): the message
        """
        frameinfo = getframeinfo(currentframe().f_back.f_back)
        self.write_log(frameinfo, message, LogLevel.DEBUG)

    @log_message
    def error(self, message):
        """
        Writes an error (LogLevel.ERROR) message to the log

        Args:
            message (str): the message
            """
        frameinfo = getframeinfo(currentframe().f_back.f_back)
        self.write_log(frameinfo, message, LogLevel.ERROR)

    @log_message
    def warn(self, message):
        """
        Writes a warning (LogLevel.WARN) message to the log

        Args:
            message (str): the message
        """
        frameinfo = getframeinfo(currentframe().f_back.f_back)
        self.write_log(frameinfo, message, LogLevel.WARN)

    @log_message
    def info(self, message):
        """
        Writes a informational (LogLevel.INFO) message to the log

        Args:
            message (str): the message
        """
        frameinfo = getframeinfo(currentframe().f_back.f_back)
        self.write_log(frameinfo, message, LogLevel.INFO)

    @log_message
    def fatal(self, message):
        """
        Writes a fatal (LogLevel.FATAL) message to the log

        Args:
            message (str): the message
        """
        frameinfo = getframeinfo(currentframe().f_back.f_back)
        self.write_log(frameinfo, message, LogLevel.FATAL)


logger = AgoraLogger.get_logger()
log_verbosity = LogLevel.INFO
if log_verbosity is not None:
    logger.set_level(log_verbosity)
