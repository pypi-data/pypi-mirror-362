# Alphi
*Monitorización de procesos a través de logs*

## Para qué sirve?
Escribe tus logs una vez y deja que el bot los envíe hacia diferentes rutas

## Uso básico

```python
from tai_alphi import Alphi

bot = Alphi()

logger = bot.get_logger()

logger.debug('Some DEBUG msg')
logger.info('Some INFO msg')
logger.warning('Some WARNING msg')
logger.error('Some ERROR msg')
logger.critical('Some CRITICAL msg')
```

## Instalación
**Poetry**
```bash
poetry add tai-alphi
```
**Pip**
```bash
pip install tai-alphi
```

#### Dependencias requeridas

`pydantic` `tomli`
> [!NOTE]
> Se instalan con el paquete

#### Dependencias opcionales
`pymongo` `logtail`
> [!WARNING]
> No se instalan automáticamente con el paquete  
> Deben instalarse por separado

## Rutas
El paquete permite actualmente enrutar logs hacia 4 destinos:
- Consola
- MSFT Teams
- MongoDB / CosmosDB
- Logtail
  
Las rutas se pueden configurar individualmente definiendo qué información (y de qué forma) va a llegar a cada una.

## Configuración
Para empezar a utilizar el bot no es necesario configurarlo, sin embargo su funcionalidad sería limitada.
> [!NOTE]
> Por defecto, el bot sin configuración está limitado a:
> - 1 logger
> - 1 ruta > Consola

La configuración del bot consiste en pasar una serie de `settings` que aportan versatilidad a la hora de organizar el flujo de información.

### Settings
Las settings se pueden definir como `dict` o escribiendo un archivo `.toml`

La sintaxis de `.toml` es human readable por lo que es la opción recomendada.

#### TOML
Para escribir el archivo `.toml` hay una [plantilla](examples/settings.toml) que describe las `settings` admitidas.

En general las configuraciones se construyen a partir de:
`[<logger_name>.<ruta>]`

Donde para cada `logger_name` podemos ir definiendo la configuración de cada una de sus `rutas`

**Ejemplo:**  
La siguiente configuración define el logger `my_logger` y enruta logs hacia:
- `consola`
- `teams` 
- `nosql`

> [!NOTE]
> La ruta `consola` viene activada por defecto

```toml
# settings.toml
[my_logger.teams]
enabled = true

[my_logger.nosql]
enabled = true
```

#### Credenciales
Para que las rutas `teams` `nosql` funcionen es necesario pasar credenciales de acceso. Esto debe hacerse desde el código por seguridad.

```python
# example.py
from tai_alphi import Alphi

settings = 'settings.toml'

bot = Alphi(settings)

bot.set_teams(webhook=<teams WEBHOOK>)

bot.set_nosql(
    user=<cosmos USER>,
    pwd=<cosmos PWD>,
    host=<cosmos HOST>,
    port=<cosmos PORT>,
    db_name=<cosmos DB>,
    collection_name=<cosmos COL>
)

my_logger = bot.get_logger()

my_logger.debug('Some DEBUG msg')
my_logger.info('Some INFO msg')
my_logger.warning('Some WARNING msg')
my_logger.error('Some ERROR msg')
my_logger.critical('Some CRITICAL msg')
```

Si unimos la configuración en `settings.toml` y las credenciales establecidas en `example.py` tenemos configurado `my_logger` para que emita los mensajes (con su contexto) hacia `consola` `teams` y `nosql`

### Documentación de la configuración
#### Rutas disponibles
  `consola` > emite logs por consola  
  `nosql` > emite logs a CosmosDB  
  `teams` > emite logs a un canal de Teams  
  `logtail` > emite logs a la plataforma de BetterStack

#### Parámetros globales de cada ruta
  `enabled` > determina si la ruta está activa o no  
  `log_level` > determina el límite inferior de los logs que serán enrutados  
  `display_info` > determina los segmentos que contextualizan a los logs  
  `time_format` > determina el formato del timestamp

#### Valores permitidos
  `enabled`: `bool` > true | false  
  `log_level`: `str` > 'DEBUG' | 'INFO' | 'WARN' | 'ERROR' | 'CRIT'  
  `display_info`: `list[str]` > ['asctime', 'filename', 'funcName', 'levelname',
                             'lineno', 'module', 'pathname']  
  `time_format`: `str` > https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

#### Parámetros específicos de cada ruta

`teams`  

  `project`: `str` > Título del proyecto  
  `pipeline`: `str` > Nombre del proceso  
  `notifications`: `list` > listado de correos a notificar ante error  

`nosql`  

  `expiration`: `float` > tiempo (en días) a partir del instante de emisión donde se eliminan los logs  

#### Argumentos por defecto de cada ruta

`consola`  

  `enabled`=true  
  `log_level`='INFO'  
  `display_info`=['asctime', 'levelname']  
  `time_format`='%H:%M:%S'  

`teams`

  `enabled`=false  
  `log_level`='INFO'  
  `display_info`=['asctime', 'levelname']  
  `time_format`='%H:%M:%S'  
  `project`='Project Name'  
  `pipeline`='Pipeline Name'  
  `notifications`=[]  

`nosql`  

  `enabled`=false  
  `log_level`='INFO'  
  `display_info`=['asctime', 'levelname']  
  `time_format`='%Y-%m-%d %H:%M:%S'  
  `expiration`=null (por defecto no elimina registros)  

`logtail`  

  `enabled`=false  
  `log_level`='INFO'  
  `display_info`=['asctime', 'levelname']  
  `time_format`='%Y-%m-%d %H:%M:%S'  

## Uso avanzado
El paquete permite definir/configurar más de un logger y sus rutas asociadas. Lo que determina la configuración de cada logger es su `logger_name`.

**Ejemplo:**  
La siguiente configuración dos loggers `logger1` y `logger2`  
Donde:  
`logger1` enruta hacia `consola` + `teams`  
`logger2` enruta hacia `consola` + `nosql`
> [!NOTE]
> La ruta `consola` viene activada por defecto

```toml
# settings.toml
[logger1.teams]
enabled = true

[logger2.nosql]
enabled = true
```
Aquí la clave consiste en capturar los dos loggers en variables diferentes:
```python
# example.py
from tai_alphi import Alphi

settings = 'settings.toml'

bot = Alphi(settings)

bot.set_teams(webhook=<teams WEBHOOK>)

bot.set_nosql(
    user=<cosmos USER>,
    pwd=<cosmos PWD>,
    host=<cosmos HOST>,
    port=<cosmos PORT>,
    db_name=<cosmos DB>,
    collection_name=<cosmos COL>
)

logger1 = bot.get_logger(logger_name='logger1')
logger2 = bot.get_logger(logger_name='logger2')

logger1.debug('Some DEBUG msg') # consola + teams
logger1.info('Some INFO msg') # consola + teams
logger1.warning('Some WARNING msg') # consola + teams

logger2.error('Some ERROR msg') # consola + nosql
logger2.critical('Some CRITICAL msg') # consola + nosql
```

Para terminar si añadimos un tercer logger `logger3` y queremos que enrute hacia `consola` y `nosql` **pero en una colección distinta hacia la que enruta `logger2`** sería:

```toml
# settings.toml
[logger1.teams]
enabled = true

[logger2.nosql]
enabled = true

[logger3.nosql]
enabled = true
```
Aquí la clave consiste en capturar los dos loggers en variables diferentes:
```python
# example.py
from tai_alphi import Alphi

settings = 'settings.toml'

bot = Alphi(settings)

bot.set_teams(webhook=<teams WEBHOOK>)

bot.set_nosql(
    user=<cosmos USER>,
    pwd=<cosmos PWD>,
    host=<cosmos HOST>,
    port=<cosmos PORT>,
    db_name=<cosmos DB>,
    collection_name=<cosmos COL>
)

logger1 = bot.get_logger(logger_name='logger1')
logger2 = bot.get_logger(logger_name='logger2')
logger3 = bot.get_logger(logger_name='logger3')

logger3.set_nosql_collection(collection_name='new_col')

logger1.debug('Some DEBUG msg') # consola + teams
logger1.info('Some INFO msg') # consola + teams
logger1.warning('Some WARNING msg') # consola + teams

logger2.error('Some ERROR msg') # consola + nosql
logger2.critical('Some CRITICAL msg') # consola + nosql

logger3.error('Some ERROR msg') # consola + nosql (new_col)
logger3.critical('Some CRITICAL msg') # consola + nosql (new_col)
```

## Desarrollo interno

La librería `tai_alphi` es una extensión personalizada del módulo de `logging` de Python que proporciona funcionalidad adicional para registrar logs en varios destinos, incluidos bases de datos NoSQL y Microsoft Teams.

## Core

### class `Alphi`

La clase `Alphi` hereda de `AlphiConfig` y sirve como la interfaz principal para crear y gestionar loggers.

#### Parámetros

- **`settings`**: `os.PathLike | dict | None` (default: `None`)
  - Entrada de la configuración de los loggers

#### Métodos

**`get_logger(logger_name: str=None, dev: bool=False, exec_info: bool=False) -> LoggerFactory`**

- `logger_name`: devuelve el logger especificado en la configuración.
  - Si `logger_name=None`:
    - Si las `settings` del bot contienen solo un logger configurado, lo captura
    - Si no se han especificado `settings` devuelve un logger por defecto que solo emite por `consola`
    - Si se ha especificado más de un logger en `settings` devuelve un error.
- `dev`: desactiva todas las rutas a excepción de la consola
- `exec_info`: añade el traceback a los logs superiores a 'ERROR'

**`set_nosql(self, user: str, pwd: str, host: str, port: int, db_name: str, collection_name: str) -> CosmosDB`**
- `user` `pwd` Credenciales de la DB
- `host` `port` Información del servidor
- `db_name` `collection_name` Información del almacenamiento

**`set_logtail(self, token: str) -> str`**  

**`set_teams(self, webhook: str) -> str`**

### class `AlphiConfig`

La clase `AlphiConfig` es responsable de gestionar las configuraciones para la librería `tai-alphi`.

#### Atributos

- **`config_file`**: `str`
  - Ruta al archivo de configuración (generalmente en formato TOML).

- **`_config`**: `Optional[ConfigValidator]`
  - Contiene el objeto de configuración validado.

- **`_logtail_token`**: `Optional[LogtailConnectionConfig]`
  - Contiene la configuración de conexión de Logtail.

- **`_nosqlDB_conn_config`**: `Optional[NoSQLDBConnectionConfig]`
  - Contiene la configuración de conexión de la base de datos NoSQL.

- **`_teams_conn_config`**: `Optional[TeamsConnectionConfig]`
  - Contiene la configuración de conexión de Microsoft Teams.

#### Métodos

- **`_set_config(self) -> None`**
  - Carga y valida el archivo de configuración especificado por `config_file`.

- **`set_nosqlDB_conn_config(self, db_name: str, db_collection_name: str, db_user: str, db_password: str, db_host: str = 'localhost', db_port: int = 27017) -> None`**
  - Configura los parámetros de conexión para una base de datos NoSQL.
  - **Parámetros**:
    - `db_name` (str): El nombre de la base de datos NoSQL.
    - `db_collection_name` (str): El nombre de la colección de la base de datos.
    - `db_user` (str): El nombre de usuario para la base de datos.
    - `db_password` (str): La contraseña para el usuario de la base de datos.
    - `db_host` (str, opcional): El nombre del host para el servidor de la base de datos. Por defecto es `'localhost'`.
    - `db_port` (int, opcional): El número de puerto para el servidor de la base de datos. Por defecto es `27017`.

- **`set_logtail_token(self, token: str) -> None`**
  - Actualiza la configuración del token de Logtail.
  - **Parámetros**:
    - `token` (str): La cadena del token para la autenticación en Logtail.


### 3. Clase `AlphiLogger`

La clase `AlphiLogger` extiende la clase `logging.Logger` y proporciona características adicionales para el formateo y manejo personalizados.

#### Atributos

- **`_nosqlDB_conn_config`**: `NoSQLDBConnectionConfig`
  - Almacena la configuración para la conexión a la base de datos NoSQL.

- **`_logtail_token`**: `LogtailConnectionConfig`
  - Almacena la configuración para la integración con Logtail.

- **`config`**: `AlphiConfig`
  - Almacena el objeto de configuración del logger.

#### Métodos

- **`__set_formatter(self, handler_type: str, config: dict) -> None`**
  - Establece el formateador para un tipo de manejador dado. Los tipos de formateadores disponibles incluyen:
    - `ConsoleFormatter` (hereda de `BaseFormatter`)
    - `DictFormatter` (hereda de `BaseFormatter`)
    - `TeamsFormatter` (hereda de `logging.Formatter`)

- **`__create_handler(self, handler_type: str, config: dict) -> logging.Handler`**
  - Crea un manejador de logs basado en el tipo y la configuración especificados.
  - **Parámetros**:
    - `handler_type` (str): El tipo de manejador a crear (por ejemplo, `'console'`, `'file'`, `'teams'`).
    - `config` (dict): Un diccionario con la configuración específica para el manejador.

- **`__set_handlers(self) -> None`**
  - Configura y establece los manejadores para la instancia de `AlphiLogger`. Los posibles manejadores incluyen:
    - `ConsoleHandler` (hereda de `StreamHandler`)
    - `CosmosHandler` (hereda de `Handler`)
    - `TeamsHandler` (hereda de `Handler`)

- **`__set_logger(self) -> None`**
  - Llama a `__set_handlers` para configurar los manejadores del `AlphiLogger`.