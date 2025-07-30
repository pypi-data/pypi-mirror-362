from tai_alphi.formatters.console import ConsoleFormatter
from tai_alphi.formatters.teams import TeamsFormatter
from tai_alphi.formatters.nosql import NoSQLFormatter
from tai_alphi.config import LoggerConfig

__all__ = ['AlphiFormatters']

class AlphiFormatters:

    def __init__(self, config: LoggerConfig, logger_name: str, dev: bool) -> None:
        self.config = config
        self.logger_name = logger_name
        self.dev = dev

        self._consola = None
        self._nosql = None
        self._teams = None
        self._logtail = None
    
    @property
    def consola(self) -> ConsoleFormatter:
        
        if not self._consola:

            segments = self.config.consola.display_info
            datefmt = self.config.consola.time_format

            self._consola = ConsoleFormatter(segments, datefmt, self.dev)
        
        return self._consola
    
    @property
    def nosql(self) -> NoSQLFormatter:

        if not self._nosql:

            segments = self.config.nosql.display_info
            datefmt = self.config.nosql.time_format

            self._nosql = NoSQLFormatter(segments, datefmt)
        
        return self._nosql
    
    @property
    def teams(self) -> TeamsFormatter:

        if not self._teams:

            segments = self.config.teams.display_info
            datefmt = self.config.teams.time_format

            self._teams = TeamsFormatter(segments, datefmt)
        
        return self._teams