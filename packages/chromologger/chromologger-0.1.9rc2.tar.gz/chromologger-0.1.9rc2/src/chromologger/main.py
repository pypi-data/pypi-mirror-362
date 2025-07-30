# v0.1.9rc2
"""chromologger es un módulo diseñado para facilitar la creación de registros (logs).

Diseñado para usarlo en aplicaciones desarrolladas con Python. 
Proporciona una manera sencilla y estructurada de documentar eventos, 
errores y actividades en los programas, mejorando la capacidad de monitoreo y 
depuración del código.

Requerimientos: 
    - chromolog==0.2.5

Historial de versiones:
    - v0.1.9rc2: Revise este enlace para más información (https://pypi.org/project/chromologger/0.1.9rc2)
    - v0.1.9rc1: Revise este enlace para más información (https://pypi.org/project/chromologger/0.1.9rc1)
    - v0.1.9a2: Revise este enlace para más información (https://pypi.org/project/chromologger/0.1.9a2)
    - v0.1.9a1: Revise este enlace para más información (https://pypi.org/project/chromologger/0.1.9a1)
    - v0.1.8: Agregué manejo de "errores" en el método `log_e(e: Exception)` y actualización del nombre de usuario
    - v0.1.7: Errores menores
    - v0.1.6: Actualización de dependencias 
    - v0.1.5: Arreglé el error que generé en la v0.1.4, nunca importé el traceback :|
    - v0.1.4: Se añadió el manejo de dependencias automáticas correctamente, antes las manejaba con `subpoccess`, pero ahora se hace con el `pip` original (`.toml[dependencies]`)
    - v0.1.3: El usuario queda libre de instalar dependencias, se instalan automáticamente
    - v0.1.2: Arreglo de errores por twine
    - v0.1.1: Algunos errores arreglados
    - v0.1.0: Versión inicial

Para saber más sobre el módulo, visite: [chromologger](https://docs.dev2forge.software)

@author Tutos Rive
"""
import inspect
from io import TextIOWrapper
from datetime import datetime
from typing import Optional, Union

from .utils.dates import Dates
from .utils.files_manager import FileManager
from chromolog import Print

__version__ = "0.1.9rc2"
__author__ = "Tutos Rive"

# Ruta absoluta de este módulo
current_path:str = FileManager.get_abs_dir(__file__)

# Escribir mensajes por consola con colores
printer_chromolog:Print = Print()

printer_chromolog.inf('Visite esta página (https://docs.dev2forge.software) antes de ejecutar este módulo')

class Logger:
    """Escribir registros de ejecución en archivos y almacenar sus registros claros y con fechas de ejecución exactas"""
    def __init__(self, log_file_name:str = 'log.log') -> None:
        # Nombre del archivo
        self.log_file_name:str = log_file_name

        # Directorio del Script que realizó la llamada
        self.caller_script = FileManager.get_abs_dir(inspect.currentframe().f_back.f_code.co_filename)

        # Ruta absoluta del archivo de 'log'
        self.path:str = f'{self.caller_script}/{self.log_file_name}' if log_file_name == 'log.log' else FileManager.get_abs_path(log_file_name)
        print(self.path)

        # Archivo abierto
        self.file:TextIOWrapper = self.__open()
    
    def __open(self) -> Union[TextIOWrapper, int]:
        """Abrir archivos

        Returns:
            `TextIOWrapper`: Archivo
                o
            `int`: `-1`: Error
        """
        try:
            # Retornar archivo
            return FileManager.open_file(self.path)
        except FileNotFoundError as e:
            # Escribir un registro "interno"
            self.__log(e)
            return -1

    def close(self) -> bool:
        """Tratar de cerrar el archivo el cual sigue en memoria"""
        # Verificar que realmente es un objeto archivo
        if type(self.file) == TextIOWrapper: self.file.close(); return True

        # Indica que el archivo NO se cerró
        return False

    def log(self, msg:any) -> None:
        """Crear registros

        Args:
            `msg:str`: Mensaje que se quiere registrar 
        """
        # Escribir mensaje de registro
        self.__write(msg)

        # Mostrar ruta del archivo log.log
        # Feature: Mostrar solo en modo "debug"
        printer_chromolog.inf(f'Revise {self.path} para ver los registros.')
    
    def log_e(self, e: Exception) -> None:
        """Registrar errores (`Exception`)

        Args:
            `e:Exception`: Excepción con la cual se trabajará
        """
        try:
            trace:dict = self.__traceback(e)
            msg:str = f'Exception: {e.__class__.__name__} - File: {trace.get("path")} - ErrorLine: {trace.get("line")} - Message: {e}'
            self.__write(msg, 'error')
        except Exception as e:
            self.__log(e)

    def __write(self, msg:str, log_type:Optional[str] = 'info') -> None:
        """Escribir registros en el archivo correspondiente

        Args:
            `msg:str`: Mensaje del registro que se escribirá
            ``
        """
        # Feature: Se trabajará con más de un solo archivo, tener una lista clara de sus rutas, para luego cerrarlos

        try:
            # Fecha-Hora actual
            __date:datetime = Dates.now_date()
            # Escribir mensaje en archivo
            self.file.writelines([f'[{log_type.upper()}][{__date}] - {msg}\n'])
        except Exception as e:
            # Crear registro en módulo
            self.__log(e)

    def __log(self, e:Exception) -> None:
        """Crear registros "internos" (Del propio módulo)

        Args:
            `e:Exception`: Excepción "capturada"
        """
        try:
            # Registro de excepciones (Ruta de archivo y línea de error)
            trace:dict = self.__traceback(e)

            # Ruta absoluta del archivo de 'logs' internos
            __log_file_intern:str = FileManager.join_paths(current_path, 'log.log')

            # Feature: Mostrar solo en modo "debug"
            printer_chromolog.err(f'Revise el archivo "log" que se encuentra en esta ruta: {__log_file_intern}')

            # Escribir registro del error "interno"
            FileManager.write_plain_text_file(__log_file_intern, f'[ERROR][{Dates.now_date()}] - Exception: {e.__class__.__name__} -File: {trace.get("path")} - ErrorLine: {trace.get("line")} - Message: {e}\n')
        except FileNotFoundError as e: printer_chromolog.exc(e)
        except TypeError as e: printer_chromolog.exc(e)
        except SyntaxError as e: printer_chromolog.exc(e)

    def __traceback(self, e:Exception) -> dict:
        """Obtener un registro preciso de la excepción

        Args:
            `e:Exception`: Excepción con la cual se trabajará

        Returns:
            `dict`: Diccionario con claves: line (Línea del error), path (Ruta del archivo de error)
        """
        import traceback
        trace_back = traceback.extract_tb(e.__traceback__)
        return {'line': trace_back[-1][1], 'path': trace_back[-1][0]}