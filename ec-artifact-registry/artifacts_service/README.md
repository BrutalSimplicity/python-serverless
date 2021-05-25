# Concepts

* **Selector**: A selector is any unique string used to identify a deployment. This service makes no attempt to attach semantic value to the identifiers for users of the service. An example might be `environment/region`.

* **Organizations**: An organization can be attached to a selector to help add some contextual business value. However, the onus is still on users to ensure they are using oganization values that make sense to them.

* **Artifact Key**: This will be generated from the stack name that is included with the manifest when the artifact gets uploaded.

* **Status ID**: ETags are used to view the status of a deployment.


## Deployment Plan

Artifacts must exist in the artifact registry before they can be assigned to a deployment. The process of creating or updating a deployment follows the sequence below.

![DeploymentPlanFlow](diagrams/out/deployment_plan.svg)

The following endpoints are available for interacting with the Artifact Registry API:

## Deployments

- `GET` Get Deployments by Selector
    * /deployments/{selector}
        * `selector`

- `GET` Get Deployments by Query
    * /deployments
        * `?selectors`
        * `?artifact_keys`

- `GET` Get Status of a Deployment
    * /deployments/{selector}/status/{status_id}
        * `selector`
        * `status_id`

- `POST` Create or Update a Deployment
    * /deployments
        * `selector`
        * `deployment_plan`

- `POST` Add an Artifact to the Deployment
    * /deployments/{selector}/artifact/{artifact_key}
        * `selector`
        * `artifact_key`

- `DELETE` Delete an Artifact from a Deployment 


> Note: the single add and delete methods are added to the api for convenience where individual teams may need to add or remove their artifacts from a deployment. However, the same dependency checks are maintained and removal will fail when their are artifacts in the plan dependent on it.

- `POST` Trigger a deployment
    * /_trigger
        * `selector`
        * `artifact_key`
    * _Mostly using internally for testing, but perhaps there is a valuable use case down the line_

- `POST` Get a Presigned Url
    * /presigned_url
        * 
