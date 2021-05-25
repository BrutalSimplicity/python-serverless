from dataclasses import dataclass
from typing import Optional


@dataclass
class GetDeploymentStatusRequest:
    id: str


@dataclass
class GetDeploymentStatusQueryRequest:
    selector: Optional[str]
