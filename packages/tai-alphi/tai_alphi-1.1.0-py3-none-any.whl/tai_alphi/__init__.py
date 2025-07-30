import os
from tai_alphi.config import AlphiConfig
from tai_alphi.logger import LoggerFactory
from tai_alphi.resources import CosmosDB


class Alphi(AlphiConfig):
    _instance = None
    _initialized = False

    def __new__(cls, settings: os.PathLike | dict | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, settings: os.PathLike | dict | None = None):
        # Evitar inicialización múltiple
        if self._initialized:
            return
            
        self.default_logger_name = 'tai-logger'

        super().__init__(settings, self.default_logger_name)
        
        self.nosql: CosmosDB | None = None
        self.logtail_token: str | None = None
        self.teams_webhook: str | None = None

        self._loggers = {}
        self._initialized = True

    @classmethod
    def get_instance(cls, settings: os.PathLike | dict | None = None):
        """
        Obtiene la instancia singleton de Alphi.
        Si no existe, la crea con la configuración proporcionada.
        """
        if cls._instance is None:
            cls._instance = cls(settings)
        return cls._instance
    
    @classmethod
    def get_logger_by_name(cls, logger_name: str = None, dev: bool = False, exec_info: bool = False) -> LoggerFactory:
        """
        Método de clase para obtener un logger por nombre.
        Crea la instancia singleton si no existe.
        """
        instance = cls.get_instance()
        return instance.get_logger(logger_name, dev, exec_info)
    
    @classmethod
    def reset_instance(cls):
        """
        Resetea la instancia singleton. Útil para testing.
        """
        cls._instance = None
        cls._initialized = False

    def has_logger_config(self, logger_name: str) -> bool:
        """
        Verifica si existe una configuración específica para el logger dado.
        """
        return logger_name in self.config.root
    
    def get_available_logger_names(self) -> list[str]:
        """
        Retorna todos los nombres de loggers configurados, incluyendo el default.
        """
        return list(self.config.root.keys())

    @property
    def loggers(self) -> dict[str, LoggerFactory]:
        return self._loggers
    
    def _logger_name_selection(self, logger_name: str) -> str:
        """
        Selecciona el nombre del logger a usar.
        Si se proporciona un nombre, lo usa (independientemente de si está configurado).
        Si no se proporciona nombre, usa el primer logger configurado o el default.
        """
        if logger_name:
            return logger_name
        else:
            # Si no se especifica nombre, usar el primer logger configurado o el default
            if self.logger_no >= 1:
                return self.names[0]
            else:
                return self.default_logger_name

    def get_logger(self, logger_name: str=None, dev: bool=False, exec_info: bool=False) -> LoggerFactory:

        name = self._logger_name_selection(logger_name)
            
        if name in self.loggers:
            logger = self.loggers.get(name)
        else:
            # Verificar si existe configuración específica para este logger
            if name in self.config.root:
                logger_config = self.config.root[name]
            else:
                # Usar configuración por defecto (solo console handler)
                logger_config = self.config.root[self.default_logger_name]

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
