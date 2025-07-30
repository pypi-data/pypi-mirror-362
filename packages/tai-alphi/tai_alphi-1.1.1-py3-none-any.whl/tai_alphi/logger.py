import logging
from functools import partial
from tai_alphi.formatters import AlphiFormatters
from tai_alphi.handlers import (
    TeamsHandler,
    ConsoleHandler,
    CosmosHandler
)
from tai_alphi.config import LoggerConfig
from tai_alphi.resources import CosmosDB
from tai_alphi.exceptions.dependencies import optional_dependencies

class LoggerFactory(logging.Logger):

    def __init__(
            self,
            logger_config: LoggerConfig,
            name: str,
            nosql: CosmosDB,
            logtail_token: str,
            teams_webhook: str,
            dev: bool
        ) -> None:
        
        super().__init__(name, logging.DEBUG)

        self.logger_config = logger_config
        self.dev = dev
        self.name = name
        self.nosql = nosql
        self.logtail_token = logtail_token
        self.teams_webhook = teams_webhook

        self._handlers = {}
    

    def set_logger(self, exec_info: bool):

        self._add_consola()

        if self.check_nosql: self._add_nosql()

        if self.check_teams: self._add_teams()

        if self.check_logtail: self._add_logtail()

        for _, handler in self._handlers.items():
            self.addHandler(handler)
        
        # SHOWING SOME WARNINGS
        if self.logger_config.nosql.enabled and not self.nosql:
            self.warning(f'El logger: "{self.name}" no tiene configurada la conexión a CosmosDB.')
            self.warning('Es necesario usar: bot.set_nosql. Configuración no añadida.')
            
        if self.logger_config.teams.enabled and not self.teams_webhook:
            self.warning(f'El logger: "{self.name}" no tiene configurada la conexión a Teams.')
            self.warning('Es necesario usar: bot.set_teams. Configuración no añadida.')
            
        if self.logger_config.logtail.enabled and not self.logtail_token:
            self.warning(f'El logger: "{self.name}" no tiene configurada la conexión a LogTail.')
            self.warning('Es necesario usar: bot.set_logtail. Configuración no añadida.')
                
        
        if exec_info:
            self.error = partial(self.error, exc_info=True)
            self.critical = partial(self.critical, exc_info=True)

        return self
    
    @property
    def check_nosql(self) -> bool:
        return bool(not self.dev and self.logger_config.nosql.enabled and self.nosql and self.nosql.client)
    
    @property
    def check_teams(self) -> bool:
        return bool(not self.dev and self.logger_config.teams.enabled and self.teams_webhook)
    
    @property
    def check_logtail(self) -> bool:
        return bool(not self.dev and self.logger_config.logtail.enabled and self.logtail_token)
 
    @property
    def formatters(self) -> AlphiFormatters:
        return AlphiFormatters(self.logger_config, self.name, self.dev)
    
    def _add_consola(self) -> None:

        handler = ConsoleHandler()
        handler.setFormatter(self.formatters.consola)
        handler.setLevel(self.logger_config.consola.log_level)
        self._handlers.update(consola=handler)
    
    def _add_teams(self) -> None:

        handler = TeamsHandler(self.teams_webhook, self.logger_config.teams)
        handler.setFormatter(self.formatters.teams)
        handler.setLevel(self.logger_config.teams.log_level)
        self._handlers.update(teams=handler)
    
    def _add_logtail(self) -> None:

        with optional_dependencies():
            from logtail import LogtailHandler

        handler = LogtailHandler(source_token=self.logtail_token)
        handler.setLevel(self.logger_config.logtail.log_level)
        self._handlers.update(logtail=handler)
    
    def _add_nosql(self) -> None:

        collection = self.nosql.get_collection()
        handler = CosmosHandler(collection, self.logger_config.nosql.expiration)
        handler.setFormatter(self.formatters.nosql)
        handler.setLevel(self.logger_config.nosql.log_level)
        self._handlers.update(nosql=handler)

    def set_nosql_collection(self, db_name: str=None, collection_name: str=None) -> None:
        
        if self.check_nosql:

            collection = self.nosql.get_collection(db_name, collection_name)
            handler = CosmosHandler(collection, self.logger_config.nosql.expiration)
            handler.setFormatter(self.formatters.nosql)
            handler.setLevel(self.logger_config.nosql.log_level)

            old_handler = self._handlers.get('nosql', None)
            if old_handler:
                self.removeHandler(old_handler)

            self._handlers.update(nosql=handler)

            self.addHandler(handler)
    
    def set_teams_webhook(self, webhook: str) -> None:
        self.teams_webhook = webhook
        
        handler = TeamsHandler(self.teams_webhook, self.logger_config.teams)
        handler.setFormatter(self.formatters.teams)
        handler.setLevel(self.logger_config.teams.log_level)

        old_handler = self._handlers.get('teams', None)
        if old_handler:
            self.removeHandler(old_handler)

        self._handlers.update(teams=handler)

        self.addHandler(handler)
