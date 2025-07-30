import atexit
import warnings 
warnings.filterwarnings("ignore", category=UserWarning) 
from logging import error
from tai_alphi.resources.validations import NoSQLDBConfig
from tai_alphi.exceptions.dependencies import optional_dependencies

class CosmosDB:

    def __init__(self, user: str, pwd: str, host: str, port: int,
                  db_name: str, collection_name: str) -> None:
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name
        self._config = None
        self._client = None

    @property
    def config(self) -> NoSQLDBConfig | None:
        """Propiedad para acceder a la configuración de NoSQL DB."""

        if not self._config:
            self._config = NoSQLDBConfig(
                user=self.user,
                pwd=self.pwd,
                host=self.host,
                port=self.port,
                db_name=self.db_name,
                collection_name=self.collection_name
            )
        
        return self._config
    
    @property
    def connected(self) -> bool:

            with optional_dependencies():
                from pymongo import errors
            
            try:
                # Probar la conexión ejecutando un comando simple
                self.client.admin.command('ping')  
                return True     
            
            except errors.ServerSelectionTimeoutError as e:
                self._client = None
                error(f"Error de tiempo de espera al seleccionar el servidor de MongoDB: {e}")
            
            except errors.OperationFailure as e:
                self._client = None
                error(f"Error al conectar a MongoDB: {e}")
            
            except errors.ConnectionFailure as e:
                self._client = None
                error(f"Error al conectar a MongoDB: {e}")
            
            except errors.ConfigurationError as e:
                self._client = None
                error(f"Error de configuración en MongoDB: {e}")
            
            except Exception as e:
                self._client = None
                error(f"Ha ocurrido un error inesperado: {e}")
            
            return False
    
    @property
    def client(self):

        if not self._client:

            with optional_dependencies():
                from pymongo import MongoClient
            
            # Intentar conectar al cliente MongoDB
            self._client = MongoClient(
                host=self.config.host,
                port=self.config.port,
                tls=True,
                retrywrites=False,
                username=self.config.user,
                password=self.config.pwd,
                connectTimeoutMS=10000,
                serverSelectionTimeoutMS=10000, 
                socketTimeoutMS=10000
            )

            # Registrar el cierre del cliente al salir
            atexit.register(self._client.close)
        
        return self._client
    
    def get_collection(self, db_name: str=None, collection_name: str=None):

        if self.connected:

            db = self.client[db_name or self.config.db_name]

            collection = db.get_collection(collection_name or self.config.collection_name)

            return collection
    