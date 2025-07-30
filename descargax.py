"""
DescargaXApp
============
Aplicación de escritorio multiplataforma para descargar contenido multimedia de X.com (antes Twitter) 
usando una interfaz gráfica basada en ttkbootstrap.

Características principales:
- Permite pegar varias URLs de X.com para descargar videos e imágenes.
- Selección de carpeta de destino.
- Historial de descargas y opción de re-descargar.
- Cambio de tema visual claro/oscuro.
- Notificaciones de escritorio.
- Ventana "Acerca de" con información y acceso al repositorio.

Dependencias:
- Python 3.8+
- ttkbootstrap
- yt-dlp
- plyer
- Pillow (opcional para mostrar logo)

Uso:
Ejecuta el archivo para abrir la interfaz gráfica. Requiere tener las dependencias instaladas.
"""
import os
import json
import threading
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL
from plyer import notification
from datetime import datetime
import subprocess
import sys
from about import show_about

CONFIG_FILE = "config.json"
HISTORIAL_FILE = "historial.txt"

class DescargaXApp:
    def __init__(self, root):
        self.root = root
        self.config = self.load_config()
        self.theme = self.config.get("theme", "flatly")
        self.style = tb.Style(theme=self.theme)
        self.root = root

        root.title("DescargaX - Modern GUI")
        root.geometry("900x600")
        root.resizable(True, True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.url_label = tb.Label(self.root, text="Pega una o varias URLs de X.com (una por línea):")
        self.url_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        self.url_textbox = ScrolledText(self.root, height=7, autohide=True)
        self.url_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.add_context_menu(self.url_textbox.text)

        self.url_textbox.text.bind("<Control-a>", lambda e: (self.url_textbox.text.tag_add("sel", "1.0", "end"), "break"))
        self.url_textbox.text.bind("<Control-A>", lambda e: (self.url_textbox.text.tag_add("sel", "1.0", "end"), "break"))
        self.url_textbox.text.bind("<Control-x>", lambda e: self.url_textbox.text.event_generate("<<Cut>>"))
        self.url_textbox.text.bind("<Control-X>", lambda e: self.url_textbox.text.event_generate("<<Cut>>"))

        button_frame = tb.Frame(self.root)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        button_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        tb.Button(button_frame, text="Descargar", bootstyle=PRIMARY, command=self.start_download_thread).grid(row=0, column=0, sticky="ew", padx=5)
        tb.Button(button_frame, text="Carpeta destino", bootstyle=INFO, command=self.change_folder).grid(row=0, column=1, sticky="ew", padx=5)
        tb.Button(button_frame, text="Historial", bootstyle=SECONDARY, command=self.show_history).grid(row=0, column=2, sticky="ew", padx=5)
        tb.Button(button_frame, text="Borrar historial", bootstyle=DANGER, command=self.clear_history).grid(row=0, column=3, sticky="ew", padx=5)
        tb.Button(button_frame, text="Tema Claro/Oscuro", bootstyle=WARNING, command=self.toggle_theme).grid(row=0, column=4, sticky="ew", padx=5)
        tb.Button(button_frame, text="Acerca de", bootstyle=SUCCESS, command=lambda: show_about(self.root)).grid(row=0, column=5, sticky="ew", padx=5)
        tb.Button(button_frame, text="Salir", bootstyle=LIGHT, command=self.root.quit).grid(row=0, column=6, sticky="ew", padx=5)

        self.status_label = tb.Label(self.root, text=f"Carpeta: {self.config['download_folder']}", anchor="w")
        self.status_label.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

    def start_download_thread(self, urls=None):
        if not urls:
            urls = self.url_textbox.get("1.0", "end").strip().splitlines()
            urls = [u.strip() for u in urls if u.strip()]

        if not urls:
            messagebox.showwarning("Error", "Introduce al menos una URL.")
            return

        if not os.path.isdir(self.config["download_folder"]):
            self.change_folder()
            return

        threading.Thread(target=self.download_videos, args=(urls,), daemon=True).start()

    def download_videos(self, urls):
        success, failed = 0, 0
        downloaded_files = []

        self.status_label.config(text="Descargando...")

        for url in urls:
            try:
                output_template = os.path.join(self.config["download_folder"], '%(title)s.%(ext)s')
                ydl_opts = {
                    'outtmpl': output_template,
                    'format': 'best',
                    'quiet': True,
                    'noplaylist': True,
                    'ignoreerrors': True
                }

                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    if info:
                        filename = ydl.prepare_filename(info)
                        downloaded_files.append(filename)
                        self.log_history(url)
                        success += 1
            except Exception as e:
                print(f"Error con {url}: {e}")
                failed += 1

        msg = f"{success} descarga(s) completada(s), {failed} fallida(s)"
        self.status_label.config(text=msg)
        notification.notify(title="DescargaX", message=msg)

        if downloaded_files:
            answer = messagebox.askyesno("Reproducir", f"¿Deseas reproducir el último archivo descargado?\n\n{os.path.basename(downloaded_files[-1])}")
            if answer:
                self.play_file(downloaded_files[-1])

    def play_file(self, filepath):
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', filepath))
            elif os.name == 'nt':
                os.startfile(filepath)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', filepath))
            else:
                messagebox.showinfo("Reproducir", "No se pudo abrir el archivo.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def log_history(self, url):
        with open(HISTORIAL_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - {url}\n")

    def show_history(self):
        if not os.path.exists(HISTORIAL_FILE):
            messagebox.showinfo("Historial", "No hay historial.")
            return

        top = tb.Toplevel(self.root)
        top.title("Historial de descargas")
        top.geometry("800x400")
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        box = ScrolledText(top, autohide=True)
        box.grid(row=0, column=0, sticky="nsew")
        box.tag_configure("url", foreground="blue", underline=True)
        box.tag_bind("url", "<Button-1>", self.redownload_from_history)

        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            if "http" in line:
                timestamp, url = line.strip().split(" - ", 1)
                box.text.insert("end", f"{timestamp} - ")
                start = box.text.index("end")
                box.text.insert("end", f"{url}\n", "url")
                end = box.text.index("end")
                box.text.tag_add(url, start, end)

        box.text.config(state="disabled")
        self.add_context_menu(box.text)

    def redownload_from_history(self, event):
        widget = event.widget
        index = widget.index("@%s,%s" % (event.x, event.y))
        line = widget.get(index + " linestart", index + " lineend")
        if "http" in line:
            url = line.split(" - ")[-1].strip()
            confirm = messagebox.askyesno("Re-descargar", f"¿Volver a descargar?\n{url}")
            if confirm:
                self.start_download_thread([url])

    def clear_history(self):
        if os.path.exists(HISTORIAL_FILE):
            if messagebox.askyesno("Confirmar", "¿Borrar todo el historial?"):
                os.remove(HISTORIAL_FILE)
                messagebox.showinfo("Historial", "Historial borrado.")

    def change_folder(self):
        folder = filedialog.askdirectory(title="Selecciona carpeta de destino")
        if folder:
            self.config["download_folder"] = folder
            self.save_config()
            self.status_label.config(text=f"Carpeta: {folder}")

    def toggle_theme(self):
        themes = ["flatly", "darkly", "cyborg", "litera", "vapor"]
        current = self.theme
        next_index = (themes.index(current) + 1) % len(themes)
        new_theme = themes[next_index]
        self.theme = new_theme
        self.config["theme"] = new_theme
        self.save_config()
        self.style.theme_use(new_theme)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {
            "download_folder": os.path.expanduser("~"),
            "theme": "flatly"
        }

    def save_config(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def add_context_menu(self, widget):
        popup = tb.Menu(widget, tearoff=0)
        popup.add_command(label="Cortar", command=lambda: widget.event_generate("<<Cut>>"))
        popup.add_command(label="Copiar", command=lambda: widget.event_generate("<<Copy>>"))
        popup.add_command(label="Pegar", command=lambda: widget.event_generate("<<Paste>>"))
        widget.bind("<Button-3>", lambda e: self._show_popup(e, popup))
        widget.bind("<Button-2>", lambda e: self._show_popup(e, popup))

    def _show_popup(self, event, popup):
        try:
            popup.tk_popup(event.x_root, event.y_root)
        finally:
            popup.grab_release()

if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = DescargaXApp(root)
    root.mainloop()
