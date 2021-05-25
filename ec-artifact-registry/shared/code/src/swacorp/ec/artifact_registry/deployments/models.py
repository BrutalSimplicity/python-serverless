from dataclasses import dataclass
from typing import Any, List, Mapping, Optional


@dataclass
class DeploymentArtifactEntity:
    key: str
    stack_name: str
    version: str
    latest_deployment: str
    timestamp: str
    metadata: Optional[Mapping[str, Any]]


@dataclass
class DeploymentArtifactGroupEntity:
    group_id: int
    artifacts: List[DeploymentArtifactEntity]


@dataclass
class DeploymentPlanEntity:
    deployment_groups: List[DeploymentArtifactGroupEntity]


@dataclass
class DeploymentEntity:
    selector: str
    version: str
    timestamp: str
    criteria: Optional[Any]
    plan: DeploymentPlanEntity
    metadata: Optional[Mapping[str, Any]]
