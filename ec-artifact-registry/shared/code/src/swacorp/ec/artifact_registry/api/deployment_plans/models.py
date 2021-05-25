from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class GetDeploymentPlanRequest:
    selector: str
    version: str


@dataclass
class GetDeploymentPlanQueryRequest:
    selectors: Optional[List[str]]


@dataclass
class CreateOrUpdateDeploymentPlanRequest:
    selector: str

    # TODO: Add artifact + dependency model
    artifacts: List[Any]

    # This is meant to hold information about how a selector
    # should be applied. Perhaps this will be similar to DDE
    # targets. Leaving it open for now.
    criteria: Optional[Any]


@dataclass
class AddArtifactToDeploymentPlanRequest:
    selector: str
    artifact_key: str


@dataclass
class DeleteArtifactForDeploymentPlanRequest:
    selector: str
    artifact_key: str


@dataclass
class TriggerDeploymentPlanRequest:
    selector: str
    version: str
    account: str
    region: str
