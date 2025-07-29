import os
import webbrowser
import ttkbootstrap as tb
from tkinter.scrolledtext import ScrolledText  # usar widget estándar
from PIL import Image, ImageTk

def show_about(parent):
    about_window = tb.Toplevel(parent)
    about_window.title("Acerca de DescargaX")
    about_window.geometry("500x600")
    about_window.resizable(False, False)

    # Logo
    try:
        img_path = os.path.join("img", "logo.png")
        image = Image.open(img_path)
        image = image.resize((150, 150))
        photo = ImageTk.PhotoImage(image)
        logo_label = tb.Label(about_window, image=photo)
        logo_label.image = photo
        logo_label.pack(pady=(10, 0))
    except Exception:
        tb.Label(about_window, text="(No se pudo cargar el logo)").pack(pady=(10, 0))

    # Texto descriptivo con scroll
    text = ScrolledText(about_window, wrap="word", height=15)
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

    # === Botones ===
    btn_frame = tb.Frame(about_window)
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
        command=about_window.destroy
    )
    btn_close.pack(side="right", padx=10)
