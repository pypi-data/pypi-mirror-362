import subprocess
import sys
import time
import webbrowser
import threading

from typing import Annotated, Optional

import typer

from . import console
from .. import __version__
from .. import app as medic_app

# Use print from `rich` library
print = console.print

app = typer.Typer()

PYPI_PROJECT_NAME = "medic-ml"

@app.callback(invoke_without_command=True, no_args_is_help=True)
def main(
    version: bool = typer.Option(False, "--version", "-v", help="MeDIC CLI version")
):
    """
    MeDIC CLI!
    """
    if version:
        typer.echo(__version__)
        typer.Exit()


@app.command(name="ui")
def ui(
    port: Annotated[Optional[int], typer.Option("--port", "-p", help="Specify the port of the app")] = 5000,
    verbose: Annotated[Optional[str], typer.Option("--verbose", "-v", help="Specifiy verbosity")] = "debug"
):
    """Launch the web application"""
    print("verbose", verbose)
    page_url = f"http://127.0.0.1:{port}"

    def startWebPage(url, wait_time: int = 0):
        """Open a browser on localhost at a url after a given wait_time"""
        time.sleep(wait_time)
        webbrowser.open(url)
    
    start_web_page_thread = threading.Thread(
        target=startWebPage,
        args=(page_url, 5)
    )
    start_web_page_thread.start()
    medic_app.run(debug=False, host='0.0.0.0', port=port)


@app.command()
def update():
    """Update the medic project to the latest version"""

    # See https://stackoverflow.com/a/50255019 for installation of a python package
    pip_infos = (
        subprocess.run(
            [sys.executable, "-m", "pip", "show", PYPI_PROJECT_NAME],
            check=True,
            capture_output=True,
        )
        .stdout.decode('latin-1')
        .split("\n")
    )

    editable_identifier_str = "Editable project location: "
    editable_project_location = [l for l in pip_infos if editable_identifier_str in l]
    if editable_project_location:
        print(
            "[cyan]medic[/cyan] is installed in editable mode, it should already be up to date."
        )
        print(f"Current version: {__version__}")
        return

    # medic was installed with pipx
    if "pipx" in sys.executable:
        print("[cyan]medic[/cyan] is managed by [cyan]pipx[/cyan]")
        update_function = [
            "pipx",
            "upgrade",
            PYPI_PROJECT_NAME
        ]
        print("The following command will update [cyan]medic[/cyan]:")
        print(" ".join(update_function), end="\n\n")
        typer.confirm("Do you want to proceed?", abort=True)

        # pipx is verbose enough
        subprocess.run(update_function, check=True)
        return

    # Update medic with the current Python interpreter
    update_function = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-U",
        PYPI_PROJECT_NAME
    ]
    print("The following command will update [cyan]medic[/cyan]:")
    print(" ".join(update_function), end="\n\n")
    typer.confirm("Do you want to proceed?", abort=True)

    subprocess.run(update_function, check=True, capture_output=True)
    new_version = subprocess.run(
        [sys.executable, "-m", "medic", "--version"], capture_output=True
    ).stdout.decode().strip()
    print(f"[cyan]medic[/cyan] updated to {new_version}")


# This is expose for documentation purposes
typer_click_object = typer.main.get_command(app)
