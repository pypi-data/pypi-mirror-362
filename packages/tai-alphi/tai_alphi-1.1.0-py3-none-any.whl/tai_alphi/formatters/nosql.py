from logging import (
    Formatter,
    LogRecord
)

class NoSQLFormatter(Formatter):

    def __init__(self, segments, datefmt):
        super().__init__()
        self.segments = segments
        self.datefmt = datefmt

        self._formatter = None

    def format(self, record: LogRecord) -> str:

        record.message = record.getMessage()
        
        if 'asctime' in self.segments:
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = {attr: getattr(record, attr) for attr in self.segments}
        message_dict['message'] = record.message
        
        if record.exc_info:

            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return message_dict