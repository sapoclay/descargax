# DescargaX

DescargaX es una aplicación de escritorio para descargar contenido multimedia de X.com (antes Twitter) de forma sencilla y visual.

## Requisitos

- Python 3.8 o superior
- Sistema operativo: Windows o Linux (GNOME, KDE, XFCE, etc.)
Las siguientes dependencias deben estar instaladas (salvo la primera, el resto se instalan automáticamente si ejecutas `run_app.py`):
  - rich (necesaria para ejecutar `run_app.py`)
  - yt-dlp
  - plyer
  - ttkbootstrap
  - Pillow
  - pystray

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/sapoclay/descargax.git
   cd descargax
   ```
2. Ejecuta el script de instalación y arranque:
   Antes de ejecutar el programa, es necesario instalar rich en nuestro sistema. Esto se puede hacer abriendo una terminal y escribiendo:
   
   ```bash
   pip install rich
   ```
   Después ya podemos iniciar la instalación y ejecución del programa escribiendo en la misma terminal:

   ```bash
   python3 run_app.py
   ```
   Esto creará un entorno virtual, instalará las dependencias y lanzará la aplicación.

## Funcionalidades

- Descarga de videos e imágenes de X.com pegando una o varias URLs (una por línea).
- Selección de carpeta de destino para las descargas.
- Historial de descargas y opción para re-descargar desde el historial.
- Borrado de historial.
- Cambio de tema visual (claro/oscuro y otros estilos).
- Notificaciones de escritorio al finalizar descargas.
- Reproducción directa del último archivo descargado.
- Ventana "About" con información y acceso al repositorio.
- Icono en la bandeja del sistema (solo en Windows y escritorios Linux compatibles).

## Limitaciones

- **Descarga desde X.com/Twitter:**
  - La descarga depende de la compatibilidad de yt-dlp con X.com. Si la plataforma cambia, puede dejar de funcionar.
  - No se pueden descargar contenidos privados o protegidos.
  - En GNOME, el icono de la bandeja no es funcional por limitaciones del entorno. Al cerrar la ventana, el programa se cierra completamente.
- **Autenticación:**
  - No se soporta autenticación para descargar contenido privado.
- **Soporte multiplataforma:**
  - El icono de la bandeja solo funciona en Windows y escritorios Linux compatibles (KDE, XFCE, etc.).
  - En GNOME, el programa se cierra al pulsar la X.

## Uso

1. Pega una o varias URLs de X.com en el cuadro de texto.
2. Selecciona la carpeta de destino si lo deseas.
3. Haz clic en "Descargar" para iniciar la descarga.
4. Consulta el historial, cambia el tema o accede a la ventana "About" para más información.

## Créditos

Desarrollado por [sapoclay](https://github.com/sapoclay) y [entreunosyceros](https://entreunosyceros.net).

---

Para dudas, sugerencias o reportes de errores, utiliza el [repositorio en GitHub](https://github.com/sapoclay/descargax).
