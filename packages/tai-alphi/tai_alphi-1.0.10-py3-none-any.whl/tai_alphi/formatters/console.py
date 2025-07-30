from logging import (
    Formatter,
    LogRecord,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL
)

class ConsoleFormatter(Formatter):

    GREY = "\x1b[38;20m"
    BLUE = "\033[94m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    BOLD_PURPLE = "\x1b[36;1m"
    RESET = "\x1b[0m"

    def __init__(self, segments: list, datefmt: str, dev: bool=False):
        super().__init__()
        self.segments = "".join(f"[%({segment})s]" for segment in segments) + " %(message)s"
        self.datefmt = datefmt
        self.dev = dev
        self._formats = None
        self._formatters = None
    
    @property
    def dev_segment(self) -> str:
        return f"{self.BOLD_PURPLE}[DEV]{self.RESET}"
    
    @property
    def log_level_color(self) -> dict:
        return {
            DEBUG: self.GREY,
            INFO: self.BLUE,
            WARNING: self.YELLOW,
            ERROR: self.RED,
            CRITICAL: self.BOLD_RED,
        }
    
    @property
    def formats(self) -> dict[int, str]:

        def custom_fmt(log_level):

            fmt = self.log_level_color[log_level] + self.segments + self.RESET

            if self.dev: fmt = self.dev_segment + fmt
            
            return fmt
        
        if not self._formats:
            self._formats = {
                log_level: custom_fmt(log_level)
                for log_level in self.log_level_color
            }

        return self._formats
    
    @property
    def formatters(self) -> dict[int, str]:

        if not self._formatters:
            self._formatters = {
                log_level: Formatter(self.formats[log_level], datefmt=self.datefmt)
                for log_level in self.formats
            }

        return self._formatters

    def format(self, record: LogRecord) -> str:

        formatter = self.formatters[record.levelno]

        return formatter.format(record)