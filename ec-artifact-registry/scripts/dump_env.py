import click
import os
from pathlib import Path


def dump_env(var: str, override: str = None, default: str = None):
    val = os.getenv(var) if not override else override
    return f"{var}={val}" if val else f"{var}={default}"


@click.command()
@click.option("--branch", "-b")
@click.option("--env", "-e")
@click.option("--acct", "-a")
def dump(branch, env, acct):
    (Path() / ".env").write_text(
        "\n".join(
            filter(
                None,
                [
                    dump_env("AWS_ACCESS_KEY_ID"),
                    dump_env("AWS_SECRET_ACCESS_KEY"),
                    dump_env("AWS_SESSION_TOKEN"),
                    dump_env("GIT_BRANCH", branch),
                    dump_env("DEPLOY_ENVIRONMENT", env),
                    "CI=1",
                    dump_env("AWS_ACCOUNT_ID", acct),
                ],
            )
        )
    )


if __name__ == "__main__":
    dump()
