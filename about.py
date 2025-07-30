import os
import webbrowser
import ttkbootstrap as tb
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

# Referencia global para controlar instancia única
about_window_instance = None

def show_about(parent):
    global about_window_instance

    if about_window_instance and about_window_instance.winfo_exists():
        about_window_instance.lift()
        about_window_instance.focus()
        return

    about_window_instance = tb.Toplevel(parent)
    about_window_instance.title("Acerca de DescargaX")
    about_window_instance.geometry("500x600")
    about_window_instance.resizable(False, False)

    # Cierre controlado
    def on_close():
        global about_window_instance
        about_window_instance.destroy()
        about_window_instance = None

    about_window_instance.protocol("WM_DELETE_WINDOW", on_close)

    # Logo
    try:
        img_path = os.path.join("img", "logo.png")
        image = Image.open(img_path)
        image = image.resize((150, 150))
        photo = ImageTk.PhotoImage(image)
        logo_label = tb.Label(about_window_instance, image=photo)
        logo_label.image = photo
        logo_label.pack(pady=(10, 0))
    except Exception:
        tb.Label(about_window_instance, text="(No se pudo cargar el logo)").pack(pady=(10, 0))

    # Texto descriptivo con scroll
    text = ScrolledText(about_window_instance, wrap="word", height=15)
    text.pack(expand=True, fill="both", padx=10, pady=10)

    content = (
        "DescargaX\n"
        "\n"
        "Aplicación moderna para descargar contenido multimedia desde X.com (antes Twitter).\n"
        "\n"
        "Funciones principales:\n"
        "- Soporte para múltiples URLs simultáneas\n"
        "- Historial de descargas con opción a re-descargar\n"
        "- Notificaciones al terminar\n"
        "- Selector de carpeta destino persistente\n"
        "- Reproductor de contenido descargado\n"
        "- Temas claros y oscuros intercambiables\n"
        "- Interfaz responsiva y moderna con ttkbootstrap\n"
        "\n"
        "Desarrollado en Python con yt-dlp, ttkbootstrap, PIL, etc.\n"
        "\n"
        "Código abierto para uso educativo y personal."
    )

    text.insert("1.0", content)
    text.config(state="disabled")

    # Botones
    btn_frame = tb.Frame(about_window_instance)
    btn_frame.pack(pady=10)

    btn_github = tb.Button(
        btn_frame,
        text="Ver en GitHub",
        bootstyle="primary-outline",
        command=lambda: webbrowser.open("https://github.com/sapoclay/descargax")
    )
    btn_github.pack(side="left", padx=10)

    btn_close = tb.Button(
        btn_frame,
        text="Cerrar",
        command=on_close  # ahora usa el mismo handler que limpia la instancia
    )
    btn_close.pack(side="right", padx=10)
