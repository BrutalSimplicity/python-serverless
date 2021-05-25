from swacorp.ec.dde.manifest.package import pack
from typing import Any, List

import typer

app = typer.Typer()


@app.command()
def pack(path: str, destination: str = None, name: str = None):
    pass


@app.command()
def deploy(services: List[str] = ["dde", "registry"]):
    pass
