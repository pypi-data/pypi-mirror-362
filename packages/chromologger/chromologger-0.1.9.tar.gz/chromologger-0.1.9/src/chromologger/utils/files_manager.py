from typing import Union
from io import TextIOWrapper
from pathlib import Path

class FileManager:
	@staticmethod
	def open_file(file_relative_path:str, mode:str='a', encoding:str='utf-8') -> Union[TextIOWrapper, None]:
		"""Obtiene la ruta absoluta del archivo (Resuelve rutas relativas)

		Args:
			`file_relative_path:str`: Ruta relativa al archivo (Se resolverá su ruta absoluta)

		Returns:
			`str`: Ruta absoluta del archivo
		"""
		# Obtener ruta absoluta del archivo
		__file_path = FileManager.get_abs_path(file_relative_path)

		__file_opened:Union[TextIOWrapper, None] = None

		# Intenta abrir el archivo en modo "append"
		try: __file_opened = open(__file_path, mode=mode, encoding=encoding)
		# Reproduce la excepción registrada en caso de error
		except Exception as e: raise e

		return __file_opened

	@staticmethod
	def write_plain_text_file(file_path:str, message:str) -> None:
		try:
			# Se intenta esclarecer la ruta y abrir el archivo
			__file_opened: Union[TextIOWrapper, None] = FileManager.open_file(file_path)

			# Se intenta escribir el mensaje (Si hay archivo)
			if __file_opened is not None: __file_opened.write(str(message))
			__file_opened.close()
		except Exception as e: raise e

	@staticmethod
	def get_abs_path(relative_path:str) -> str: return str(Path(relative_path).resolve().absolute())

	@staticmethod
	def get_abs_dir(relative_path:str) -> str: return str(Path(relative_path).resolve().absolute().parent)

	@staticmethod
	def join_paths(base_path:str, *others_paths:str) -> str: return str(Path(base_path).resolve().absolute().joinpath(*others_paths).resolve().absolute())