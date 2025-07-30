from pydantic import BaseModel, Field
from typing import List

# Modelo para validar la conexión a NoSQLDB
class NoSQLDBConfig(BaseModel):
    user: str = Field(description="Nombre de usuario para la base de datos")
    pwd: str = Field(description="Contraseña para la base de datos")
    host: str = Field(default='localhost', description="Host de la base de datos NoSQL")
    port: int = Field(default=27017, description="Puerto de la base de datos NoSQL", gt=0)
    db_name: str = Field(description="Nombre de la base de datos NoSQL")
    collection_name: str = Field(description="Nombre de la colección en la base de datos NoSQL")

# Modelo para validar la conexión a Teams
class TeamsConnectionConfig(BaseModel):
    webhook: str = Field(description="Webhook")
    proyecto: str = Field(description="Nombre proyecto")
    pipeline: str = Field(description="Nombre pipeline")
    notify_to: List[str] = Field(description="Emails notificar")