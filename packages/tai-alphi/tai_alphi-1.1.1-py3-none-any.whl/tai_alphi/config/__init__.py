import os
import tomli
import logging
from pydantic import ValidationError
from .schemas import Config, LoggerConfig


__all__ = ['AlphiConfig', 'Config', 'LoggerConfig']

class AlphiConfig:

    def __init__(self, settings: os.PathLike | dict | None, default_logger_name: str) -> None:
        self.default_logger_name = default_logger_name
        self.settings = settings
        self._config: Config = None
    
    @property
    def logger_no(self) -> int:
        return len(self.names)
    
    @property
    def names(self) -> list[str]:
        """Retorna la lista de nombres de loggers configurados, excluyendo el default."""
        all_names = list(set(self.config.root.keys()))
        # Solo remover el default_logger_name si existe en la configuración
        if self.default_logger_name in all_names:
            all_names.remove(self.default_logger_name)
        return all_names

    @property
    def config(self) -> Config | None:
        """Propiedad para acceder a la configuración validada."""
        if not self._config:
            
            extra = None
            config = {self.default_logger_name: {}}

            try:
                
                if isinstance(self.settings, dict):
                    extra = self.settings

                elif isinstance(self.settings, str):
                    with open(self.settings, mode='rb') as f:
                        extra = tomli.load(f)

                if extra:
                    config.update(extra)
                
                self._config = Config(**config)
                
            except ValidationError as e:
                raise e
            
            except (ValueError, FileNotFoundError) as e:
                logging.error(f"Error al cargar o validar la configuración: {e}")
                raise e

        return self._config
    