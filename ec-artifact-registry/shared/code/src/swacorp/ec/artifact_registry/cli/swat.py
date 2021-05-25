import typer
from swacorp.ec.artifact_registry.cli.deployments import app as deployments_app
from swacorp.ec.artifact_registry.cli.package import app as package_app

swat = typer.Typer()

swat.add_typer(deployments_app, name="deployments")
swat.add_typer(package_app, name="package")

if __name__ == "__main__":
    swat()
