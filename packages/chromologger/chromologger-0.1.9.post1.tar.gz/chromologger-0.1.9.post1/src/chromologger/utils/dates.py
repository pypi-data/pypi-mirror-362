from datetime import datetime

class Dates:
	@staticmethod
	def now_date() -> datetime:
		"""Obtener la fecha-hora actual

		Returns:
			`datetime`: Hora actual exacta de ejecución
		"""
		return datetime.now()