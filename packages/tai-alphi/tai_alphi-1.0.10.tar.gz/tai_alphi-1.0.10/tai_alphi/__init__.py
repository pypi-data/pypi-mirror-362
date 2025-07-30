import os
from tai_alphi.config import AlphiConfig
from tai_alphi.logger import LoggerFactory
from tai_alphi.resources import CosmosDB


class Alphi(AlphiConfig):

    def __init__(self, settings: os.PathLike | dict | None=None):

        self.default_logger_name = 'tai-logger'

        super().__init__(settings, self.default_logger_name)
        
        self.nosql: CosmosDB | None = None
        self.logtail_token: str | None = None
        self.teams_webhook: str | None = None

        self._loggers = {}

    @property
    def loggers(self) -> dict[str, LoggerFactory]:
        return self._loggers
    
    def _logger_name_selection(self, logger_name: str) -> str:

        if logger_name:
    
            if self.logger_no == 1:
                from_config_logger = self.names[0]
                assert logger_name == from_config_logger, f'"{logger_name}" no coincide con el logger configurado "{from_config_logger}"'
            else:
                assert logger_name in self.names, f'"{logger_name}" no coincide con ninguno de los logger configurados "{self.names}"'
                
            name = logger_name

        else:

            if self.logger_no == 1:
                name = self.names[0]
            else:
                name = self.default_logger_name

        return name

    def get_logger(self, logger_name: str=None, dev: bool=False, exec_info: bool=False) -> LoggerFactory:

        name = self._logger_name_selection(logger_name)
            
        if name in self.loggers:

            logger = self.loggers.get(name)

        else:

            logger_config = self.config.root[name]

            logger = LoggerFactory(
                logger_config=logger_config,
                name=name,
                nosql=self.nosql,
                logtail_token=self.logtail_token,
                teams_webhook=self.teams_webhook,
                dev=dev
            ).set_logger(exec_info)
            
            self._loggers[name] = logger

        return logger
    
    def set_nosql(self, user: str, pwd: str, host: str, port: int,
                  db_name: str, collection_name: str) -> CosmosDB:
        
        if not self.nosql:

            self.nosql = CosmosDB(user, pwd, host, port, db_name, collection_name)
        
        return self.nosql
    
    def set_logtail(self, token: str) -> str:
        
        if not self.logtail_token:

            self.logtail_token = token
        
        return self.logtail_token
    
    def set_teams(self, webhook: str) -> str:

        if not self.teams_webhook:

            self.teams_webhook = webhook
        
        return self.teams_webhook
