import enum


class LogLevel(enum.IntEnum):
    '''
    Logging Level enumeration
    '''
    TRACE = 0,  # Trace level - used for the finest level of debugging
    DEBUG = 1,  # Debug level - used for debugging - specifically log values that should not go to Release
    INFO = 2,  # Info level - general logging information - filename, line number,  and method are not included
    WARN = 3,  # Warning level - indicates something is not happening as expected
    ERROR = 4,  # Error level - indicates an error occurred, but not fatally
    FATAL = 5,  # Fatal level - generally used just before the application gives up
    OFF = 6    # Off Level - no logging will be produced at this level

    @classmethod
    def from_string(cls, level):
        '''
        convert text to enum value
        '''
        level = level.upper()
        if level in cls._member_names_:
            return LogLevel[level]
        else:
            return None
