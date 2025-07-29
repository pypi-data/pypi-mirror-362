import sys


from ..log_level import LogLevel
from ..colored_text import ColoredText
from agora_utils import AgoraTimeStamp

class BaseHandler:
    """
    Base class for handlers
    """

    def __init__(self):
        self.timer_start = AgoraTimeStamp()
        self.level = LogLevel.INFO

    def set_level(self, level):
        """
        log level of the handler
        """
        self.level = level

    def write_to_stream(self, message, stream=sys.stdout):
        """
        Writes message to stream
        """
        stream.write(message)
        stream.flush()

    def write(self, stream, frame_info, log, level, coloring):
        """
        Writes to stream if level is greater than threshold
        """
        if level >= self.level:
            data = self.prepare_log(frame_info, level, log, coloring)
            self.write_to_stream(data, stream)

    def text_to_heading(self, frameinfo, text):
        """
        Writes text to heading
        """
        time_now = AgoraTimeStamp()
        millisec = int(
            (time_now - self.timer_start) 
        )
        line_no_text = f"""({str(millisec)})"""
        len_line_no_text = len(line_no_text)
        nums = max(80, len(text))
        dashes = "-" * nums
        justified_text = text.rjust(80)
        text_prefixed = line_no_text + justified_text[len_line_no_text:]
        return f"""{dashes}\n{text_prefixed}\n{dashes}\n"""

    def prepare_log(self, frame_info, level, log, coloring):
        """
        Prepares data to  be logged
        """
        time_now = AgoraTimeStamp()
        millisec = int(
            (time_now - self.timer_start) 
        )
        line_no = frame_info.lineno
        context = ""
        context_enums = [LogLevel.DEBUG, LogLevel.TRACE, LogLevel.ERROR]
        context_values = [e.value for e in context_enums]
        if level.value in context_values:
            fn_name = frame_info.function
            file_name = frame_info.filename
            context = f"""{file_name}({line_no}) {fn_name} : """

        log_level_code = level.name[0]
        data = f"""{log_level_code}({millisec}) - {context}{log}\n"""

        if level.value == LogLevel.INFO.value or not coloring:
            log_message = data
        elif level.value == LogLevel.WARN.value:
            log_message = ColoredText.yellow(data)
        elif level.value == LogLevel.TRACE.value:
            log_message = ColoredText.gray(data)
        elif level.value == LogLevel.DEBUG.value:
            log_message = ColoredText.green(data)
        elif level.value == LogLevel.ERROR.value:
            log_message = ColoredText.dark_red(data)
        elif level.value == LogLevel.FATAL.value:
            log_message = ColoredText.red(data)

        return log_message
