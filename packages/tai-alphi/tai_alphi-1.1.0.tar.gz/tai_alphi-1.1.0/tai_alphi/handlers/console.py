import sys
from logging import LogRecord, StreamHandler

class ConsoleHandler(StreamHandler):

    def __init__(self):
        super().__init__(sys.stdout)
    
    def emit(self, record: LogRecord) -> None:
        return super().emit(record)