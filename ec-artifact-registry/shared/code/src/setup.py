import os
from pathlib import Path
from setuptools import setup, find_namespace_packages

version = os.environ.get("LIB_VERSION")
if version is None:
    version = (Path(__file__).parent / "version").read_text()

setup(
    name="ec-artifact-registry-shared-lib",
    version=version,
    author="Enterprise Cloud",
    author_email="EnterpriseCloud@wnco.com",
    packages=find_namespace_packages(include="swacorp.*"),
    install_requires=[
        "boto3",
        "swawesomo",
        "six",
        "pyyaml",
    ],
    package_data={"": ["*.pem"]},
    python_requires=">=3.8",
    scripts=["swacorp/ec/artifact_registry/cli/swat.py"],
)
