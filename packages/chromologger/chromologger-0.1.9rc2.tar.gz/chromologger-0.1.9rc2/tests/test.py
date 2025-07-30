# pip install chromologger
import chromologger as ch

l = ch.Logger()

# Registro básico de información
l.log(f'Autor: {ch.__author__} - Versión: {ch.__version__}')

# Registro de errores
try:
    tutosrivegamer
except NameError as e:
    l.log_e(e)