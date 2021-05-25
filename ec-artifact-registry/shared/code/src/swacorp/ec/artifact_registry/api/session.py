import boto3
import os
from pathlib import Path


class SessionParams:
    def __init__(self, session: boto3.Session, env="dev", endpoint=None):
        env = env.lower() if env else env
        self._session = session
        self._swacert = (
            os.path.join(Path(__file__).parent, "certs", "swadevrootca1.pem")
            if env not in ["qa", "prod"]
            else os.path.join(Path(__file__).parent, "certs", f"swa{env}rootca1.pem")
        )
        self._endpoint = f"https://api.registry.ec.{env}.aws.swacorp.com"
        if env.lower() not in ["dev", "qa", "prod"]:
            self._endpoint = f"https://{env}.api.registry.ec.dev.aws.swacorp.com"
        if endpoint:
            self._endpoint = endpoint
