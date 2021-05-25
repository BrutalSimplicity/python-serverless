# EC Artifact Registry

PutArtifact
DescribeArtifact
DeleteArtifact
ListArtifacts
GenerateDeploymentPlan


PutDeploymentPlan
ExecuteDeploymentPlan
DeleteDeploymentPlan
GetDeploymentStatus
GetDeploymentPlan

# Development Requirements

- `pipenv`
- When installing/updating packages be sure to be connected vpn for installing SWA-specific package (i.e. `swawesomo`). Once you have it installed in your vitual environment you can comment out the config when you need to update packages offline. You can also avoid the performance hit from updating packages by skipping the update for packages already locked with `--skip-lock`.
