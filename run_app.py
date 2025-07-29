import os
import sys
import platform
import subprocess
import venv
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from rich import print

console = Console()
def is_venv_exists():
    venv_dir = '.venv'
    return os.path.exists(venv_dir) and os.path.isdir(venv_dir)

def create_venv():
    console.rule("[bold blue]Creando el entorno virtual")
    venv.create('.venv', with_pip=True)
    console.print("[green]Entorno virtual creado correctamente.")

def get_python_executable():
    if platform.system().lower() == 'windows':
        return os.path.join('.venv', 'Scripts', 'python.exe')
    return os.path.join('.venv', 'bin', 'python')

def get_pip_executable():
    if platform.system().lower() == 'windows':
        return os.path.join('.venv', 'Scripts', 'pip.exe')
    return os.path.join('.venv', 'bin', 'pip')

def install_requirements():
    pip_exe = get_pip_executable()
    requirements_file = 'requirements.txt'
    console.rule("[bold blue]Instalando dependencias")
    with Progress() as progress:
        task1 = progress.add_task("[cyan]Actualizando setuptools...", total=1)
        subprocess.run([pip_exe, 'install', '--upgrade', 'setuptools'], check=True)
        progress.update(task1, advance=1)
        if not os.path.exists(requirements_file):
            console.print(f"[red]Error: {requirements_file} no encontrado")
            sys.exit(1)
        task2 = progress.add_task("[cyan]Instalando desde requirements.txt...", total=1)
        subprocess.run([pip_exe, 'install', '-r', requirements_file], check=True)
        progress.update(task2, advance=1)
    console.print("[green]Dependencias instaladas correctamente.")

def run_main_app():
    python_exe = get_python_executable()
    main_file = 'descargax.py'
    if not os.path.exists(main_file):
        console.print(f"[red]Error: {main_file} no encontrado")
        sys.exit(1)
    console.rule("[bold blue]Iniciando la aplicación gráfica")
    subprocess.run([python_exe, main_file], check=True)

def main():
    os.chdir(Path(__file__).parent)
    if not is_venv_exists():
        create_venv()
    try:
        install_requirements()
        run_main_app()
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error ocurrido: {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()