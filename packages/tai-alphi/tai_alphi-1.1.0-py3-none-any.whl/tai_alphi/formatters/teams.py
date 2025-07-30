from logging import (
    Formatter,
    LogRecord,
)

class TeamsFormatter(Formatter):

    def __init__(self, segments: list, datefmt: str):
        super().__init__()
        self.segments = "".join(f"[%({segment})s]" for segment in segments) + "%(message)s"
        self.datefmt = datefmt
        self._formatter = None
    
    @property
    def formatter(self) -> Formatter:

        if not self._formatter:

            self._formatter = Formatter(self.segments, datefmt=self.datefmt)

        return self._formatter

    def format(self, record: LogRecord) -> str:

        return self.formatter.format(record)