from typing import Any

import typer

app = typer.Typer()


@app.command()
def events(
    etag: str,
    account: str,
    limit: int = 10,
    ascending: bool = False,
    lastkey: str = None,
):
    pass


@app.command()
def summary(etag: str):
    pass


@app.command()
def errors(etag: str, limit: int = 10, ascending: bool = False, lastkey: str = None):
    pass


@app.command()
def artifacts(
    stack_name: str,
    account: str,
    region: str,
    limit: int = 10,
    ascending: bool = False,
    lastkey: str = None,
):
    pass


@app.command()
def artifacts_history(
    stack_name: str,
    account: str,
    region: str,
    limit: int = 10,
    ascending: bool = False,
    lastkey: str = None,
):
    pass


def get_presigned_url(s3_url: str):
    pass
