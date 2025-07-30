import os
from tai_alphi.config import AlphiConfig
from tai_alphi.logger import LoggerFactory, LoggerConfig
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
        self._dynamic_configs = {}  # Configuraciones dinámicas que pueden cambiar
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
    def configure_logger(cls, logger_name: str, config: dict):
        """
        Método de clase para configurar un logger dinámicamente.
        """
        instance = cls.get_instance()
        instance.add_logger_config(logger_name, config)
    
    @classmethod
    def configure_multiple_loggers(cls, configs: dict[str, dict]):
        """
        Método de clase para configurar múltiples loggers dinámicamente.
        """
        instance = cls.get_instance()
        instance.add_multiple_logger_configs(configs)
    
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
            # Usar la configuración efectiva (dinámica, archivo o por defecto)
            logger_config = self._get_effective_config(name)

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
    
    def add_logger_config(self, logger_name: str, config: dict):
        """
        Añade o actualiza la configuración de un logger específico.
        Si el logger ya existe, se reconfigura automáticamente.
        """
        
        # Validar la configuración usando el esquema
        validated_config = LoggerConfig(**config)
        
        # Almacenar en configuraciones dinámicas
        self._dynamic_configs[logger_name] = validated_config
        
        # Si el logger ya existe, reconfigurarlo
        if logger_name in self._loggers:
            self._reconfigure_logger(logger_name)
    
    def add_multiple_logger_configs(self, configs: dict[str, dict]):
        """
        Añade o actualiza múltiples configuraciones de loggers.
        """
        for logger_name, config in configs.items():
            self.add_logger_config(logger_name, config)
    
    def _reconfigure_logger(self, logger_name: str):
        """
        Reconfigura un logger existente con nueva configuración.
        """
        if logger_name not in self._loggers:
            return
        
        # Obtener la nueva configuración
        new_config = self._get_effective_config(logger_name)
        
        # Crear un nuevo logger con la nueva configuración
        new_logger = LoggerFactory(
            logger_config=new_config,
            name=logger_name,
            nosql=self.nosql,
            logtail_token=self.logtail_token,
            teams_webhook=self.teams_webhook,
            dev=False  # Asumir que no es dev por defecto
        ).set_logger(False)  # Sin exec_info por defecto
        
        # Reemplazar el logger existente
        self._loggers[logger_name] = new_logger
    
    def _get_effective_config(self, logger_name: str):
        """
        Obtiene la configuración efectiva para un logger, considerando:
        1. Configuraciones dinámicas añadidas
        2. Configuraciones del archivo de configuración
        3. Configuración por defecto
        """
        # Prioridad 1: Configuración dinámica
        if logger_name in self._dynamic_configs:
            return self._dynamic_configs[logger_name]
        
        # Prioridad 2: Configuración del archivo
        if logger_name in self.config.root:
            return self.config.root[logger_name]
        
        # Prioridad 3: Configuración por defecto
        return self.config.root[self.default_logger_name]
    
    def remove_logger_config(self, logger_name: str):
        """
        Elimina la configuración dinámica de un logger.
        El logger volverá a usar la configuración del archivo o la por defecto.
        """
        if logger_name in self._dynamic_configs:
            del self._dynamic_configs[logger_name]
            
            # Si el logger existe, reconfigurarlo
            if logger_name in self._loggers:
                self._reconfigure_logger(logger_name)
    
    def get_logger_config(self, logger_name: str):
        """
        Obtiene la configuración actual de un logger.
        """
        return self._get_effective_config(logger_name)
    
    def list_configured_loggers(self) -> dict[str, str]:
        """
        Lista todos los loggers configurados con su fuente de configuración.
        """
        result = {}
        
        # Loggers con configuración dinámica
        for name in self._dynamic_configs:
            result[name] = "dynamic"
        
        # Loggers con configuración de archivo
        for name in self.config.root:
            if name not in result:
                result[name] = "file"
        
        return result
