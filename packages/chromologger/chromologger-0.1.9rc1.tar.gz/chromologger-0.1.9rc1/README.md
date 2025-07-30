# CHROMOLOGGER

---

<div align="center" style="display: flex; align-items: center; justify-content: center; margin: 10px 0; gap: 10px; max-height: 48px; height: 48px;">
  <a href="https://github.com/sponsors/tutosrive" target="_blank">
  <img src="https://img.shields.io/badge/Sponsor-%F0%9F%92%96%20Dev2Forge-blue?style=for-the-badge&logo=github" alt="Sponsor me on GitHub">
</a>
  <a href="https://ko-fi.com/D1D61GNZR1" target="_blank">
  <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor me on Ko-Fi">
</a>
</div>

---

<!-- Badges -->
  <div>
<!-- Total downloads -->
    <a href="https://pepy.tech/projects/chromologger"><img src="https://static.pepy.tech/badge/chromologger" alt="PyPI Downloads"></a>
<!-- Versión actual -->
    <a href="https://pypi.org/project/chromologger/"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/chromologger?label=chromologger"></a>
<!-- Python versions supported -->
    <a href="https://python.org/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/chromologger"></a> 
<!-- Author -->
    <a href="https://github.com/tutosrive"><img alt="Static Badge" src="https://img.shields.io/badge/Tutos%20Rive-Author-brightgreen"></a>
<!-- Licencia -->
    <a href="https://raw.githubusercontent.com/tutosrive/chromologger/main/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/tutosrive/chromologger"></a>
  </div>

```shell
pip install chromologger
```
---

> ### Visite [chromologger](https://docs.dev2forge.software/chromologger/) para más documentación

"**Chromologger**" es un módulo diseñado para facilitar la creación de registros (_logs_) en aplicaciones desarrolladas con **Python**. Proporciona una manera sencilla y estructurada de documentar eventos, errores y actividades en los programas, mejorando la capacidad de monitoreo y depuración del código.

> Ejemplo del registro de una `Excepción`: En una línea
```md
>  
[ERROR][2025-01-06 19:52:08.636560] - Exception - FileNotFoundError - File - c:\Users\srm\Desktop\msqlite\msqlite\__logger.py - ErrorLine: 35 - Messsage: [Errno 2] - No such file or directory: './data/log'
```

> Ejemplo del registro de ejecución: En una línea
```md
>  
[INFO][2025-01-06 20:52:08.636560] - El usuario ha modificado la configuración "xyz"'
```

> NOTA: Es necesario que el directorio donde se guardará el archivo esté creado, ÚNICAMENTE el **directorio**, el archivo se creará dentro de automáticamente...

## Métodos públicos disponibles:

- **log**: Permite guardar mensajes **generales** en el registro, es decir, **NO ERRORES**, mensajes de información _ordinaria_ (general).
- **log_e**: Permite registrar errores, es un registro más específico (Tomar registros de `Exception`)

## Versiones:
- `v0.1.9rc1`:
  - Se realizó una prueba de la versión `v0.1.9a2`, la cual es funcional
  - Esta version es para pruebas antes de la `Release`
- `v0.1.9a2`:
  - Se corrigió el nombre del archivo de `log` el cual en algunos sistemas causaba errores.
- `v0.1.9a1`:
  - Pruebas cambios en la apertura y escritura de archivos
  - Cambié la forma de obtener las rutas absolutas (cambio de usar el módulo `os` al objeto `pathlib.Path`)
  - Pruebas en rutas relativas (Se admite pasar como nombre de archivo rutas relativas)
    - Ejemplo: `log:Logger = Logger(../logs/operations.log)`, la ruta se "resolverá"
  - Cambio de la estructura del mensaje de registro
    - Antes: `2025-07-15 17:57:50.137718 - Este es un registro de prueba`
    - Ahora:
      - método `log(msg:str)`: `[INFO][2025-07-15 17:57:50.137718] - Este es un registro de prueba`
      - método `log_e(e:Exception)`: `[ERROR][2025-07-15 18:57:50.137718] - Exception - FileNotFoundError - File - c:\Users\srm\Desktop\Bridgex\bridgex\__logger.py - ErrorLine: 35 - Messsage: [Errno 2] - No such file or directory: './DirectorioNoExiste/log'`
- `v0.1.8`: Agrgué manejo de "errores" en el método `log_e(e: Exception)` y actualización del nombre de usuario
- `v0.1.7`: Errores menores
- `v0.1.6`: Actualización de dependencias 
- `v0.1.5`: Arreglé el error que generé en la `v0.1.4`, nunca importé el traceback :|
- `v0.1.4`: Se añadió el manejo de dependencias automáticas correctamente, antes las manejaba con `subpoccess`, pero ahora se hace con el `pip` original (`.toml[dependencies]`)
- `v0.1.3`: El usuario queda libre de instalar dependencias, se instalan automáticamente
- `v0.1.2`: Arreglo de errores por twine
- `v0.1.1`: Algunos errores arreglados
- `v0.1.0`: Versión inicial

Si desea conocer más acerca de, visite:
- [Web de soporte](https://docs.dev2forge.software/chromologger/)
- [Web pypi.org](https://pypi.org/project/chromologger/)
- [GitHub project](https://github.com/Dev2Forge/chromologger)
