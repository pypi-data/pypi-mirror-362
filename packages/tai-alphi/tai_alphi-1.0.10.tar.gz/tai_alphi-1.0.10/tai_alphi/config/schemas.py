from __future__ import annotations
from pydantic import BaseModel, Field, model_validator, field_validator, RootModel
from typing import Dict,List

class HandlerConfig(BaseModel):
    log_level: str = 'INFO'
    display_info: List[str] = ['asctime', 'levelname']

    @field_validator('log_level', mode='after')
    def log_level_validator(cls, log_level):

        allowed = {'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRIT'}

        if not log_level in allowed:
            raise ValueError(f'El valor de [log_level] = {log_level} no es valido. Debe ser algún valor de: {allowed}')
        
        return log_level

    @field_validator('display_info', mode='after')
    def display_info_validator(cls, segments):

        allowed = {'asctime', 'filename', 'funcName', 'levelname',
                    'lineno', 'module', 'pathname'}
        
        for segment in segments:
            if not segment in allowed:
                raise ValueError(f'El valor {segment} encontrado en [display_info] no es valido. Debe ser algún valor de: {allowed}')
        
        return segments


class ConsoleConfig(HandlerConfig):
    enabled: bool = True
    time_format: str = '%H:%M:%S'

class TeamsConfig(HandlerConfig):
    enabled: bool = False
    time_format: str = '%H:%M:%S'
    project: str = 'Project Name'
    pipeline: str = 'Pipeline Name'
    notifications: List[str] = []

class NoSQLConfig(HandlerConfig):
    enabled: bool = False
    time_format: str = '%Y-%m-%d %H:%M:%S'
    expiration: float | None = None

class LogTailConfig(HandlerConfig):
    enabled: bool = False

# Modelo Logger
class LoggerConfig(BaseModel):
    consola: ConsoleConfig = Field(default_factory=ConsoleConfig)
    teams: TeamsConfig = Field(default_factory=TeamsConfig)
    nosql: NoSQLConfig = Field(default_factory=NoSQLConfig)
    logtail: LogTailConfig = Field(default_factory=LogTailConfig)

    # Valida que solo existan etiquetas permitidas
    @model_validator(mode='before')
    def check_keys(cls, value):
        allowed_keys = {'consola', 'teams', 'nosql', 'logtail'}
        if not all(key in allowed_keys for key in value):
            raise ValueError(f'Las rutas (handlers) permitidas son {allowed_keys}')
        return value
    

# Modelo raíz para validar el diccionario completo
class Config(RootModel[Dict[str, LoggerConfig]]):

    # Validación para asegurar que todas las etiquetas de logger sean únicas
    @model_validator(mode='before')
    def check_unique_loggers(cls, logger_names: dict):
        if len(logger_names) != len(set(logger_names)):
            raise ValueError("Los nombres de los loggers deben ser únicos")
        return logger_names
